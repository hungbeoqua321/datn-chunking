"""Bộ tách câu (C, D) và phân đoạn ngữ nghĩa (D) — các ca dấu chấm KHÔNG kết câu trong văn bản pháp luật."""
import numpy as np
import pytest

from chunking import semantic, sentence
from chunking.base import Document


def cau(t: str) -> list[str]:
    return [t[a:b] for a, b in sentence.tach_cau(t)]


def test_tieu_de_dieu_khong_cat():
    t = "Điều 5. Phạm vi điều chỉnh\nLuật này quy định về hợp đồng. Luật này áp dụng với doanh nghiệp."
    assert cau(t) == ["Điều 5. Phạm vi điều chỉnh", "Luật này quy định về hợp đồng.",
                      "Luật này áp dụng với doanh nghiệp."]
    assert cau("Điều 51a. Bổ sung điều mới") == ["Điều 51a. Bổ sung điều mới"]
    assert cau("Chương II. QUY ĐỊNH CHUNG") == ["Chương II. QUY ĐỊNH CHUNG"]


def test_nhan_khoan_muc_khong_cat():
    assert cau("1. Người lao động có quyền sau đây: Được trả lương.") == ["1. Người lao động có quyền sau đây: Được trả lương."]
    assert cau("1.1. Hồ sơ gồm Đơn đề nghị.") == ["1.1. Hồ sơ gồm Đơn đề nghị."]
    assert cau("II. Nội dung") == ["II. Nội dung"]
    # dấu chấm kết câu thật trong khoản vẫn cắt
    assert cau("2. Khoản này có hai câu. Câu thứ hai.") == ["2. Khoản này có hai câu.", "Câu thứ hai."]


def test_so_hieu_khong_bi_cat():
    t = "Thông tư số 05/2025/TT-BXD và Nghị định số 12/2025/NĐ-CP quy định chi tiết Luật này."
    assert cau(t) == [t]
    # dấu chấm sau số hiệu ở cuối câu là kết câu thật
    assert cau("Theo Nghị định số 12/2025/NĐ-CP. Nghị định này có hiệu lực.") == [
        "Theo Nghị định số 12/2025/NĐ-CP.", "Nghị định này có hiệu lực."]


def test_tieu_de_giua_dong_va_nhan_trong_nhay():
    # hồi quy từ dữ liệu thật: tiêu đề Điều nằm giữa dòng; văn bản sửa đổi trích nguyên văn khoản/Điều trong nháy
    assert cau("theo quy định tại Thông tư này. Điều 33. Quy định chuyển tiếp") == [
        "theo quy định tại Thông tư này.", "Điều 33. Quy định chuyển tiếp"]
    t = 'Sửa đổi, bổ sung khoản 3 Điều 43 như sau: "3. Trình tự lập, thẩm định dự án."'
    assert cau(t) == [t]
    t = 'Sửa đổi, bổ sung Điều 41 "Điều 41. Hồ sơ bổ nhiệm lại"'
    assert cau(t) == [t]
    t = 'Bổ sung khoản 1a vào sau khoản 1 như sau: "1a. Việc giám định thực hiện theo quy định."'
    assert cau(t) == [t]
    assert cau("hồ sơ mời thầu. 1b. Yêu cầu nhà thầu làm rõ.") == ["hồ sơ mời thầu.", "1b. Yêu cầu nhà thầu làm rõ."]


def test_viet_tat_so_va_ten_mien():
    assert cau("Các khoản phí, lệ phí, v.v. được miễn.") == ["Các khoản phí, lệ phí, v.v. được miễn."]
    assert cau("Trụ sở tại TP. Hồ Chí Minh và Hà Nội.") == ["Trụ sở tại TP. Hồ Chí Minh và Hà Nội."]
    assert cau("Phạt từ 1.000.000 đồng đến 2.000.000 đồng.") == ["Phạt từ 1.000.000 đồng đến 2.000.000 đồng."]
    assert cau("Tra cứu tại vbpl.vn hoặc Cổng thông tin.") == ["Tra cứu tại vbpl.vn hoặc Cổng thông tin."]
    assert cau("Ông N. V. An ký thay.") == ["Ông N. V. An ký thay."]


def test_hoi_than_va_xuong_dong():
    assert cau("Có được miễn không? Được miễn! Hết.") == ["Có được miễn không?", "Được miễn!", "Hết."]
    assert cau("Dòng một\n\nDòng hai  ") == ["Dòng một", "Dòng hai"]


def test_phu_het_khong_chong_lan():
    t = "Điều 1. Tên\n1. Câu một. Câu hai? Câu ba!\n  a) điểm a;\nb) điểm b./."
    vt = sentence.tach_cau(t)
    co = bytearray(len(t))
    for a, b in vt:
        assert not any(co[a:b])
        co[a:b] = b"\x01" * (b - a)
    assert all(co[i] or t[i].isspace() for i in range(len(t)))


def test_gom_toi_da_300_tu_va_cau_dai_bi_cat_cua_so():
    """Chính sách trần chung: câu đơn dài hơn trần KHÔNG còn đứng nguyên mà bị cắt bằng cửa sổ cố
    định kiểu A (câu 320 từ → 300 + 20). Trước khi áp chính sách, chunk này để nguyên 320 từ."""
    dai = " ".join(["dài"] * 320) + "."
    t = "\n".join(["Câu " + " ".join(["x"] * 99) + "."] * 4 + [dai, "Câu cuối."])
    cs = sentence.chunk(Document("d", "1/2020/QH14", "Luật", "Luật mẫu", t))
    assert [c.n_words for c in cs] == [300, 100, 300, 20, 2]
    assert max(c.n_words for c in cs) <= 300
    assert all(c.dieu_so is None and c.tien_to == "" and c.text == t[c.start:c.end] for c in cs)


def _vec_chu_de(cs: list[str]) -> np.ndarray:
    """Vector giả theo TỈ LỆ mèo/chó trong chuỗi được nhúng.

    D nhúng CỤM 3 CÂU (buffer_size=1 như bản gốc LangChain), nên cụm vắt qua ranh giới chủ đề là
    HỖN HỢP chứ không thuần một bên — vector giả phải phản ánh điều đó, nếu không ranh giới đo được
    sẽ lệch đúng bằng bề rộng cụm."""
    V = np.array([[c.count("mèo") + 0.05, c.count("chó") + 0.05] for c in cs], dtype=float)
    return V / np.linalg.norm(V, axis=1, keepdims=True)


def test_d_cat_o_cho_doi_chu_de():
    # ≥ 20 câu: dưới ngưỡng đó D rơi về cách gom của C (văn bản quá ngắn, phân vị vô nghĩa)
    t = "\n".join([f"Con mèo số {i} " + " ".join(["kêu"] * 8) + "." for i in range(12)] +
                  [f"Con chó số {i} " + " ".join(["sủa"] * 8) + "." for i in range(12)])
    cs = semantic.chunk(Document("d", "x", "Luật", "y", t), vec=_vec_chu_de)
    assert len(cs) == 2 and "mèo" in cs[0].text and "chó" not in cs[0].text and "chó" in cs[1].text
    assert all(c.tien_to == "" and c.dieu_so is None for c in cs)


def test_d_rang_buoc_50_350_tu():
    # một chủ đề dài 600 từ → phải tách ≤ 350; một mẩu 10 từ lạc đề ở giữa → bị gộp (không còn đoạn < 50 từ)
    t = "\n".join([f"Con mèo {i} " + " ".join(["kêu"] * 28) + "." for i in range(10)] + ["Con chó sủa " + "to " * 7 + "."] +
                  [f"Con mèo {i} " + " ".join(["kêu"] * 28) + "." for i in range(10, 20)])
    cs = semantic.chunk(Document("d", "x", "Luật", "y", t), vec=_vec_chu_de)
    assert all(c.n_words <= semantic.TOI_DA for c in cs)
    assert all(c.n_words >= semantic.TOI_THIEU for c in cs)
    assert "".join(t[c.start:c.end] for c in cs).replace("\n", "") == t.replace("\n", "")


@pytest.mark.parametrize("ham", [sentence.chunk])
def test_van_ban_rong(ham):
    assert ham(Document("d", "x", "Luật", "y", "  \n ")) == []


def test_d_van_ban_ngan_roi_ve_c():
    """Dưới 20 câu thì phân vị 95 vô nghĩa (ít khoảng cách, p95 ≈ max) → D gom như C và đánh dấu
    fallback=True. Vector giả KHÔNG được gọi tới trong nhánh này."""
    def _khong_duoc_goi(cs):
        raise AssertionError("văn bản ngắn không được nhúng")

    t = "\n".join([f"Câu số {i} " + " ".join(["chữ"] * 10) + "." for i in range(10)])
    cs = semantic.chunk(Document("d", "x", "Luật", "y", t), vec=_khong_duoc_goi)
    assert cs and all(c.fallback and c.method == "D" for c in cs)
    assert "".join(t[c.start:c.end] for c in cs).replace("\n", "") == t.replace("\n", "")


def test_d_bien_do_gop_khong_vuot_tran_gop():
    """Gộp đoạn dưới sàn được phép nhỉnh hơn trần, nhưng không bao giờ quá TRAN_GOP."""
    t = "\n".join([f"Con mèo {i} " + " ".join(["kêu"] * 28) + "." for i in range(10)] +
                  ["Con chó sủa " + "to " * 7 + "."] +
                  [f"Con mèo {i} " + " ".join(["kêu"] * 28) + "." for i in range(10, 20)])
    cs = semantic.chunk(Document("d", "x", "Luật", "y", t), vec=_vec_chu_de)
    assert all(c.n_words <= semantic.TRAN_GOP for c in cs)
