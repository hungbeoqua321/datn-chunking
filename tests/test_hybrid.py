"""Phương pháp E — bù ngữ cảnh cho mảnh con. Kiểm bằng dữ liệu giả, không nạp mô hình nhúng."""
import numpy as np
import pytest

from chunking import hybrid, structural
from chunking.base import Document
from chunking.hybrid import CongTac

TAT_HET = CongTac(dan_dieu=False, dan_khoan=False, nhan_manh=False, semantic=False)


def _vec(cs):
    """Vector giả theo tỉ lệ 'mèo'/'chó' trong CỤM 3 CÂU (E nhúng cụm, như D)."""
    V = np.array([[c.count("mèo") + 0.05, c.count("chó") + 0.05] for c in cs], dtype=float)
    return V / np.linalg.norm(V, axis=1, keepdims=True)


def _doc(t: str) -> Document:
    return Document("d1", "10/2025/QH15", "Luật", "Luật mẫu", t)


# ── bất biến quan trọng nhất: tắt hết công tắc thì E PHẢI trùng khít B ───────
def test_tat_het_trung_khit_b():
    t = ("Điều 1. Phạm vi\nLuật này quy định về thử nghiệm.\n"
         "Điều 2. Giải thích\nTrong Luật này, các từ ngữ sau đây được hiểu như sau:\n"
         "1. Thử nghiệm là hoạt động kiểm tra.\n2. Cơ quan là đơn vị nhà nước.\n")
    d = _doc(t)
    b, e = structural.chunk(d, 0), hybrid.chunk(d, 0, TAT_HET, vec=_vec)
    assert len(b) == len(e)
    for cb, ce in zip(b, e):
        assert (cb.start, cb.end) == (ce.start, ce.end)
        assert cb.tien_to == ce.tien_to


# ── thành phần (1a) câu dẫn của Điều ────────────────────────────────────────
def _doc_dai_co_dan(n_khoan=3, tu=200):
    """Điều > 350 từ, có câu dẫn thân trước khoản 1, nhiều khoản."""
    dan = "Người sử dụng lao động có các nghĩa vụ sau đây:"
    kh = "".join(f"{i}. " + " ".join(["nội"] * tu) + ".\n" for i in range(1, n_khoan + 1))
    return _doc(f"Điều 5. Nghĩa vụ\n{dan}\n{kh}"), dan


def test_dan_dieu_chep_vao_khoan_tu_thu_hai():
    d, dan = _doc_dai_co_dan()
    cs = hybrid.chunk(d, 0, CongTac(dan_dieu=True, dan_khoan=False, nhan_manh=False, semantic=False), vec=_vec)
    kh = [c for c in cs if c.khoan_so is not None]
    assert len(kh) >= 3
    # khoản 1 đã chứa sẵn câu dẫn trong thân (B gộp vào) → KHÔNG chép lại
    assert kh[0].cau_dan_lap == ""
    assert dan in kh[0].text
    # khoản 2 trở đi: câu dẫn được chép lại
    for c in kh[1:]:
        assert c.cau_dan_lap == dan and c.text.count(dan) == 1


def test_tat_dan_dieu_thi_khoan_sau_mat_cau_dan():
    d, dan = _doc_dai_co_dan()
    cs = hybrid.chunk(d, 0, TAT_HET, vec=_vec)
    kh = [c for c in cs if c.khoan_so is not None]
    assert all(c.cau_dan_lap == "" for c in kh)
    assert dan not in kh[1].text          # đúng hành vi của B: mất câu dẫn


# ── thành phần (1b) câu dẫn của khoản ───────────────────────────────────────
def test_dan_khoan_chep_vao_diem_tu_thu_hai():
    dan_k = "Hồ sơ gồm các giấy tờ sau đây:"
    diem = "".join(f"{c}) " + " ".join(["giấy"] * 200) + ".\n" for c in "abc")
    d = _doc(f"Điều 7. Hồ sơ\n1. {dan_k}\n{diem}")
    cs = hybrid.chunk(d, 0, CongTac(dan_dieu=False, dan_khoan=True, nhan_manh=False, semantic=False), vec=_vec)
    dm = [c for c in cs if c.diem is not None]
    assert len(dm) >= 3
    assert dm[0].cau_dan_lap == ""        # điểm a) đã có sẵn câu dẫn
    for c in dm[1:]:
        assert dan_k in c.cau_dan_lap


# ── thành phần (2) nhãn mảnh ────────────────────────────────────────────────
def test_nhan_manh_ghi_phan_i_tren_n():
    d = _doc("Điều 9. Dài\n" + " ".join(["từ"] * 900) + ".\n")
    cs = hybrid.chunk(d, 0, CongTac(dan_dieu=False, dan_khoan=False, nhan_manh=True, semantic=False), vec=_vec)
    assert len(cs) > 1
    n = len(cs)
    for i, c in enumerate(cs, 1):
        assert c.vi_tri_manh == i and c.tong_so_manh == n
        assert f"(phần {i}/{n})" in c.tien_to


def test_tat_nhan_manh_thi_tien_to_khong_co_nhan():
    d = _doc("Điều 9. Dài\n" + " ".join(["từ"] * 900) + ".\n")
    cs = hybrid.chunk(d, 0, TAT_HET, vec=_vec)
    assert len(cs) > 1
    assert all("(phần" not in c.tien_to for c in cs)


# ── thành phần (3) semantic CÓ CHẶN ─────────────────────────────────────────
def _doc_tang_cuoi():
    """Một Điều không có khoản, > 350 từ, đổi chủ đề giữa chừng → đi vào tầng cuối."""
    meo = "".join(f"Con mèo số {i} " + " ".join(["kêu"] * 18) + ".\n" for i in range(12))
    cho = "".join(f"Con chó số {i} " + " ".join(["sủa"] * 18) + ".\n" for i in range(12))
    return _doc(f"Điều 3. Vật nuôi\n{meo}{cho}")


def test_semantic_khong_vuot_ra_ngoai_don_vi():
    d = _doc_tang_cuoi()
    cs = hybrid.chunk(d, 0, CongTac(False, False, False, True, "duoi"), vec=_vec)
    kh = structural.phan_tich(d.text)
    dieu = next(k for k in kh if k.loai == "dieu")
    for c in cs:
        assert dieu.start <= c.start and c.end <= dieu.end, "ranh giới semantic vượt ra ngoài Điều"


def test_semantic_khong_mat_ky_tu():
    d = _doc_tang_cuoi()
    for bl in ("duoi", "tren"):
        cs = hybrid.chunk(d, 0, CongTac(False, False, False, True, bl), vec=_vec)
        phu = set()
        for c in cs:
            phu.update(range(c.start, c.end))
        assert all(i in phu or x.isspace() for i, x in enumerate(d.text))


def test_hai_bien_the_ban_le_cat_khac_cho():
    d = _doc_tang_cuoi()
    a = hybrid.chunk(d, 0, CongTac(False, False, False, True, "duoi"), vec=_vec)
    b = hybrid.chunk(d, 0, CongTac(False, False, False, True, "tren"), vec=_vec)
    assert [(c.start, c.end) for c in a] != [(c.start, c.end) for c in b]


def test_semantic_ton_trong_tran_san():
    d = _doc_tang_cuoi()
    cs = hybrid.chunk(d, 0, CongTac(False, False, False, True, "duoi"), vec=_vec)
    from chunking.semantic import TRAN_GOP
    assert all(c.n_words <= TRAN_GOP for c in cs)


# ── fallback: không có Điều → cửa sổ cố định, GIỐNG B (không phải C) ─────────
def test_khong_co_dieu_roi_ve_cua_so_nhu_b():
    t = "Kính gửi các đơn vị.\n" + " ".join(["chữ"] * 700) + ".\n"
    d = _doc(t)
    b, e = structural.chunk(d, 0), hybrid.chunk(d, 0, CongTac(), vec=_vec)
    assert [(c.start, c.end) for c in b] == [(c.start, c.end) for c in e]
    assert all(c.fallback for c in e)


@pytest.mark.parametrize("bl", ["duoi", "tren"])
def test_van_ban_rong(bl):
    cs = hybrid.chunk(_doc("  \n "), 0, CongTac(ban_le=bl), vec=_vec)
    assert len(cs) == 1 and cs[0].n_words > 0
