import pytest

from eval.trich_dan import boc, khoa_tu_chuoi, tu_choi

K = khoa_tu_chuoi("45/2019/QH14")


def test_dang_chuan():
    assert boc("Căn cứ: Điều 25 khoản 1 của 45/2019/QH14.") == [(K, 25, 1, None)]


def test_so_hieu_dao_va_them_loai():
    assert boc("Điều 107 khoản 2 của QH14 số 45/2019.")[0] == (K, 107, 2, None)
    assert boc("theo Điều 105 khoản 1 của Nghị định 45/2019/QH14")[0] == (K, 105, 1, None)


def test_khoan_truoc_dieu_va_diem():
    assert boc("Theo điểm a khoản 2 Điều 5 của 12/2020/NĐ-CP")[0] == (khoa_tu_chuoi("12/2020/NĐ-CP"), 5, 2, "a")
    assert boc("(Điều 113 khoản 1 a của 45/2019/QH14)")[0] == (K, 113, 1, "a")
    assert boc("Điều 7, khoản 3, điểm đ của 45/2019/QH14")[0] == (K, 7, 3, "đ")


def test_dan_chieu_noi_dung_duoc_gan_so_hieu_gan_nhat():
    """Quy tắc chấm (23/10): trích dẫn không nêu số hiệu ("của Bộ luật này") lấy số hiệu của
    trích dẫn TƯỜNG MINH gần nhất trong cùng câu trả lời. Trước đây để None → hiện ra "?"."""
    t = boc("trừ trường hợp quy định tại Điều 29 của Bộ luật này; Căn cứ: Điều 35 khoản 2 của 45/2019/QH14.")
    assert (K, 29, None, None) in t and (K, 35, 2, None) in t


def test_khong_co_so_hieu_nao_thi_lay_mac_dinh_cua_chunk():
    t = boc("Theo Điều 29 khoản 1 của Bộ luật này.", mac_dinh=K)
    assert t == [(K, 29, 1, None)]
    assert boc("Theo Điều 29 khoản 1 của Bộ luật này.") == [(None, 29, 1, None)]


def test_giu_trich_dan_trong_than_bai():
    """Quy tắc 24/10: KHÔNG lọc riêng mục "Căn cứ" nữa — trích dẫn trong thân bài vẫn tính."""
    t = ("Theo quy định tại Điều 7 của 105/2020/TT-BTC thì ...\n"
         "Căn cứ: Điều 35 khoản 2 của 45/2019/QH14.")
    assert len(boc(t)) == 2 and boc(t)[0][0] == khoa_tu_chuoi("105/2020/TT-BTC")


def test_so_hieu_khong_kem_dieu_la_NHAC_TOI_khong_boc():
    """Số hiệu đứng giữa thân bài mà không kèm Điều chỉ là nhắc tới văn bản."""
    assert boc("quy định tại Thông tư số 105/2020/TT-BTC, Quy chế trao đổi thông tin ...") == []


def test_van_ban_von_khong_chia_dieu_thi_so_hieu_CHINH_LA_trich_dan():
    """Chỉ thị, Công văn… không có Điều: khi đó số hiệu trần là trích dẫn hợp lệ."""
    t = boc("Chỉ thị số 09/CT-TTg của Thủ tướng Chính phủ.", cho_phep_khong_dieu=True)
    assert len(t) == 1 and set(t[0][0]) == {"09", "CT-TTG"} and t[0][1] is None


def test_liet_ke_dieu_tach_thanh_nhieu_trich_dan():
    t = boc("Căn cứ: Điều 2, 3, 10 của 334/CT-TTg.")
    assert [x[1] for x in t] == [2, 3, 10] and all(set(x[0]) == {"334", "CT-TTG"} for x in t)


@pytest.mark.parametrize("chuoi, mong", [
    ("Theo Điều 2 khoản a b của 1408/CT-TTg.", [(2, None, "a"), (2, None, "b")]),
    ("Điều 5 khoản g của 200/2026/NĐ-CP", [(5, None, "g")]),
    ("Điều 9 khoản 4 điểm a, b, c và d của 200/2026/NĐ-CP", [(9, 4, "a"), (9, 4, "b"), (9, 4, "c"), (9, 4, "d")]),
    ("Điều 4 khoản 1 điểm a b c của 19/2021/TT-BTC", [(4, 1, "a"), (4, 1, "b"), (4, 1, "c")]),
])
def test_khoan_diem_bang_chu_boc_du_danh_sach(chuoi, mong):
    """"khoản b" là ĐIỂM về mặt pháp lý dù mô hình gọi nhầm là khoản."""
    assert [(x[1], x[2], x[3]) for x in boc(chuoi)] == mong


@pytest.mark.parametrize("chuoi, so, ky", [
    ("Căn cứ: 09/CT-TTg.", "09", "CT-TTg"),          # ký hiệu có chữ thường
    ("Căn cứ: 334/CT-TTg.", "334", "CT-TTg"),
    ("Căn cứ: 9367 TC/PC.", "9367", "TC/PC"),        # số hiệu kiểu cũ, ngăn bằng khoảng trắng
    ("Căn cứ: 9367/TC/PC.", "9367", "TC/PC"),        # kiểu cũ, ngăn bằng dấu chéo
])
def test_ba_mau_so_hieu_truoc_day_bi_hong(chuoi, so, ky):
    """Ký hiệu được chuẩn hoá về CHỮ HOA để làm khoá so khớp, nên so sánh theo bản hoa."""
    t = boc(chuoi, cho_phep_khong_dieu=True)
    assert len(t) == 1, t
    assert set(t[0][0]) == {so, ky.upper()}, t[0][0]


def test_giu_so_0_dau():
    """`09/CT-TTg` KHÁC `9/CT-TTg` — lstrip("0") cũ làm hai số hiệu khác nhau trùng khoá."""
    a = boc("Căn cứ: 09/CT-TTg.", cho_phep_khong_dieu=True)[0][0]
    b = boc("Căn cứ: 9/CT-TTg.", cho_phep_khong_dieu=True)[0][0]
    assert a != b and "09" in a


def test_gold_khop_du_hoa_thuong_va_dau_ngan_cach():
    """So với gold phải bỏ qua hoa/thường ở ký hiệu, và coi khoảng trắng như dấu chéo."""
    assert khoa_tu_chuoi("9367 TC/PC") == khoa_tu_chuoi("9367/TC/PC")
    assert khoa_tu_chuoi("04/CT-BTC") == khoa_tu_chuoi("04/ct-btc")
    assert khoa_tu_chuoi("9367 TC/PC") == boc("Điều 5 khoản 2 của 9367/TC/PC")[0][0]


def test_van_ban_khong_chia_dieu_va_tu_choi():
    assert boc("Căn cứ: 4197/BQP-PC.", cho_phep_khong_dieu=True) == \
        [(khoa_tu_chuoi("4197/BQP-PC"), None, None, None)]
    assert tu_choi("Không đủ căn cứ trong ngữ cảnh được cung cấp.")
    assert not tu_choi("Điều 5 của 45/2019/QH14")


def test_ky_tu_D_sai():
    # Ð (U+00D0, Eth) hay lẫn vào HTML cũ thay cho Đ (U+0110)
    assert boc("Ðiều 9 của 45/2019/QH14")[0][1] == 9
