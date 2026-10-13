"""Bất biến của các bộ phân đoạn (trên văn bản mẫu nhỏ + trên toàn bộ dữ liệu nếu đã có)."""
import re

import pytest

import cau_hinh as ch
from chunking import fixed, structural
from chunking.base import Document, cua_so, do_lech

LUAT = """QUỐC HỘI
LUẬT MẪU
Chương I
QUY ĐỊNH CHUNG
Điều 1. Phạm vi điều chỉnh
Luật này quy định về việc mẫu.
Điều 2.
Giải thích từ ngữ
Trong Luật này, các từ ngữ dưới đây được hiểu như sau:
""" + "\n".join(f"{i}. Từ ngữ {i} là " + " ".join(["nội dung"] * 60) + "." for i in range(1, 6)) + """
Chương II
QUYỀN VÀ NGHĨA VỤ
Mục 1
QUYỀN
Điều 3. Quyền của người lao động
Người lao động có các quyền sau đây:
1. Quyền thứ nhất gồm:
""" + "\n".join(f"{c}) Điểm {c} " + " ".join(["chữ"] * 120) + ";" for c in "abcd") + """
2. Quyền thứ hai.
"""


def doc(text: str, so_hieu="1/2020/QH14", trich="Luật mẫu") -> Document:
    return Document(doc_id="x", so_hieu=so_hieu, loai_van_ban="Luật", trich_yeu=trich, text=text)


def khong_trang_ngoai_chunk(d: Document, cs) -> int:
    co = bytearray(len(d.text))
    for c in cs:
        co[c.start:c.end] = b"\x01" * (c.end - c.start)
    return sum(1 for i, x in enumerate(d.text) if not x.isspace() and not co[i])


@pytest.mark.parametrize("ham", [fixed.chunk, fixed.chunk_a_cong, structural.chunk, structural.chunk_b_tru,
                                 structural.chunk_ah])
def test_phu_het_va_khong_rong(ham):
    d = doc(LUAT)
    cs = ham(d, 0)
    assert khong_trang_ngoai_chunk(d, cs) == 0
    assert all(c.text.strip() and c.end > c.start for c in cs)
    assert all(d.text[c.start:c.end] in c.text for c in cs)  # nội dung nằm nguyên vẹn trong chuỗi đem nhúng


def test_cua_so_300_tu_khong_chong_lan():
    d = doc(" ".join(f"t{i}" for i in range(1000)))
    cs = fixed.chunk(d, 0)
    assert [c.n_words for c in cs] == [300, 300, 300, 100]
    assert all(a.end <= b.start for a, b in zip(cs, cs[1:]))
    assert all(c.dieu_so is None and c.khoan_so is None for c in cs)


def test_seed_lech_cua_so():
    d = doc(" ".join(f"t{i}" for i in range(1000)))
    o = do_lech(1, "x")
    assert 1 <= o < 300 and [n for *_, n in cua_so(d.text, 0, len(d.text), 300, o)][0] == o


def test_b_cac_tang_va_tien_to():
    d = doc(LUAT)
    cs = structural.chunk(d, 0)
    d1 = [c for c in cs if c.dieu_so == 1]
    assert len(d1) == 1 and d1[0].khoan_so is None                      # tầng 1: Điều ngắn giữ nguyên
    d2 = [c for c in cs if c.dieu_so == 2]
    assert d2[0].dieu_ten == "Giải thích từ ngữ"                         # tên điều ở dòng kế tiếp
    assert len(d2) == 5 and [c.khoan_so for c in d2] == [1, 2, 3, 4, 5]  # tầng 2: > 350 từ → theo khoản
    assert "Trong Luật này" in d2[0].text                                # phần dẫn gộp vào khoản đầu
    assert all("Điều 2. Giải thích từ ngữ" in c.tien_to for c in d2)     # tên điều lặp ở mọi chunk con
    d3 = [c for c in cs if c.dieu_so == 3]
    assert {c.diem for c in d3 if c.khoan_so == 1} == {"a", "b", "c", "d"}  # khoản > 350 từ → theo điểm
    assert all(c.chuong == "II" and c.muc == "1" for c in d3)
    assert d3[0].tien_to.startswith("[1/2020/QH14] [Luật mẫu] > Chương II > Mục 1 > Điều 3. Quyền của người lao động")
    assert all(c.dieu_start is not None and c.dieu_end > c.dieu_start for c in d2 + d3)
    assert all(c.text.startswith(c.tien_to + "\n") for c in cs)


def test_tang3_fallback_giong_a_cong():
    d = doc("Kính gửi các Bộ.\n" + " ".join(["nội dung"] * 400))
    for s in (0, 1, 2):
        b, a = structural.chunk(d, s), fixed.chunk_a_cong(d, s)
        assert all(c.fallback for c in b)
        assert [(c.start, c.end, c.text) for c in b] == [(c.start, c.end, c.text) for c in a]


def test_tang0_van_ban_rong():
    cs = structural.chunk(doc("   \n", trich="Công văn về việc X"), 0)
    assert len(cs) == 1 and "Công văn về việc X" in cs[0].text


def test_regex_cua_de():
    assert structural.RE_DIEU.match("Điều 12. Tên điều").groups() == ("12", "Tên điều")
    assert structural.RE_DIEU.match("Điều 12: Tên").group(1) == "12"
    assert not structural.RE_DIEU.match('"Điều 12. Trích dẫn')
    assert structural.RE_KHOAN.match("1. Khoản") and structural.RE_KHOAN.match("2) Khoản")
    assert not structural.RE_KHOAN.match("1.1. Mục con")
    assert structural.RE_DIEM.match("đ) điểm đ")


@pytest.mark.skipif(not (ch.CHUNKS / "B_s0.jsonl").exists(), reason="chưa dựng chunk")
def test_du_lieu_that_khong_mat_van_ban():
    from chunking.base import doc_jsonl, nap_van_ban
    docs = nap_van_ban()
    for ten in ("A_s0", "Acong_s0", "B_s0", "A_H_s0", "Btru_s0"):
        cs = doc_jsonl(ch.CHUNKS / f"{ten}.jsonl")
        assert {d.doc_id for d in docs} == {c.doc_id for c in cs}, ten
    # A+ và B trùng khớp ở nhóm không có Điều (cùng seed)
    nhom = {d.doc_id: d.nhom for d in docs}
    for s in (0, 1, 2, 3):
        a = [(c.doc_id, c.start, c.end, c.text) for c in doc_jsonl(ch.CHUNKS / f"Acong_s{s}.jsonl") if nhom[c.doc_id] == "khong_dieu"]
        b = [(c.doc_id, c.start, c.end, c.text) for c in doc_jsonl(ch.CHUNKS / f"B_s{s}.jsonl") if nhom[c.doc_id] == "khong_dieu"]
        assert a == b, s
    # mọi chunk con của một Điều đã tách đều mang tên Điều trong tiền tố
    for c in doc_jsonl(ch.CHUNKS / "B_s0.jsonl"):
        if c.dieu_so is not None:
            assert re.search(rf"> Điều {c.dieu_so}\b", c.tien_to)


# ── hồi quy cho các lỗi cài đặt do kiểm định ca biên tìm ra (results/buoc3/kiem_dinh_ca_bien.md) ──
def test_nguong_350_khong_tinh_tieu_de_chuong():
    tieu_de = "Chương II\n" + " ".join(["TIÊU ĐỀ"] * 15) + "\n"
    than = "Điều 3. Tên\n1. " + " ".join(["x"] * 165) + "\n2. " + " ".join(["y"] * 165)
    cs = [c for c in structural.chunk(doc(tieu_de + than), 0) if c.dieu_so == 3]
    assert len(cs) == 1 and cs[0].khoan_so is None and cs[0].chuong == "II"


def test_chuong_bi_ngat_dong_va_muc_la_ma():
    t = "Chương\nVIII QUYẾT ĐỊNH HÌNH PHẠT\nMục II\nTÊN MỤC\nĐiều 50. Căn cứ\nNội dung.\nMục A\nĐiều 51a. Bổ sung\nNội dung."
    cs = structural.chunk(doc(t), 0)
    assert cs[0].chuong == "VIII" and cs[0].muc == "II"
    assert cs[1].muc == "A" and cs[1].dieu_so == 51 and "> Điều 51a. Bổ sung" in cs[1].tien_to
