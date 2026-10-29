"""Ba hạng mục kết quả — "cắt trần" phải là cột riêng và KHÔNG được biến mất khỏi mẫu.

Quyết định của người duyệt (22/10): giữ MAX_TOKENS 384, câu chạm trần tính là trả lời hỏng
loại "cắt trần", xuất thành cột riêng trong mọi bảng, không loại khỏi mẫu.
"""
import pytest

from eval.ket_qua import LOAI, bang, dem, phan_loai


@pytest.mark.parametrize("r, mong", [
    ({"tra_loi": "Theo khoản 2 Điều 5 …"}, "dat"),
    ({"tra_loi": "Không đủ căn cứ trong đoạn trích."}, "tu_choi"),
    ({"tra_loi": "", "cat_tran": True}, "cat_tran"),
    ({"tra_loi": "Theo Điều 5 …", "cat_tran": True}, "cat_tran"),   # cắt trần thắng, dù có chữ
    ({"tra_loi": None}, "dat"),
])
def test_phan_loai(r, mong):
    assert phan_loai(r) == mong


def test_cat_tran_khong_bi_gop_vao_tu_choi():
    """Gộp vào 'từ chối' là sai bản chất: từ chối là mô hình ĐỌC xong rồi nói không đủ căn cứ,
    cắt trần là mô hình chưa nói hết câu."""
    d = dem([{"pp": "A", "tra_loi": "", "cat_tran": True}], "pp")
    assert d["A"] == {"dat": 0, "tu_choi": 0, "cat_tran": 1}


def test_tong_ba_hang_muc_bang_co_mau():
    rows = ([{"pp": "A", "tra_loi": "x"}] * 7
            + [{"pp": "A", "tra_loi": "không đủ căn cứ"}] * 2
            + [{"pp": "A", "tra_loi": "", "cat_tran": True}])
    v = dem(rows, "pp")["A"]
    assert sum(v.values()) == len(rows) == 10, "cỡ mẫu không được hụt đi vì ca cắt trần"


def test_moi_hang_muc_deu_co_cot_du_bang_khong():
    v = dem([{"pp": "B", "tra_loi": "x"}], "pp")["B"]
    assert set(v) == set(LOAI) and v["cat_tran"] == 0


def test_bang_luon_in_du_ba_cot():
    ra = bang([{"pp": "A", "tra_loi": "x"}], "pp")
    assert "cắt trần" in ra and "từ chối" in ra and "đạt" in ra
    assert ra.count("|") >= 10
