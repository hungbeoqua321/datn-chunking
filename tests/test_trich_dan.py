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


def test_dan_chieu_noi_dung_khong_co_so_hieu():
    t = boc("trừ trường hợp quy định tại Điều 29 của Bộ luật này; Căn cứ: Điều 35 khoản 2 của 45/2019/QH14.")
    assert (None, 29, None, None) in t and (K, 35, 2, None) in t


def test_van_ban_khong_chia_dieu_va_tu_choi():
    assert boc("Căn cứ: 4197/BQP-PC.") == [(khoa_tu_chuoi("4197/BQP-PC"), None, None, None)]
    assert tu_choi("Không đủ căn cứ trong ngữ cảnh được cung cấp.")
    assert not tu_choi("Điều 5 của 45/2019/QH14")


def test_ky_tu_D_sai():
    # Ð (U+00D0, Eth) hay lẫn vào HTML cũ thay cho Đ (U+0110)
    assert boc("Ðiều 9 của 45/2019/QH14")[0][1] == 9
