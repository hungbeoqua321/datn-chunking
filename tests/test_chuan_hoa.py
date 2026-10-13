"""Test bộ chuẩn hoá trên các mẫu HTML nhỏ, mỗi mẫu là một ca lỗi thật đã gặp khi crawl vbpl.vn."""
from crawl.chuan_hoa import RE_TIEU_DE_B, bo_dau_cuoi, chuan_hoa, do_tieu_de, text_tho


def dong(t: str) -> list[str]:
    return [x for x in t.split("\n") if x]


def test_tieu_de_vo_do_the_inline():
    # docx chuyển sang HTML: mỗi từ một <span> → crawl thô ra "Điều ⏎ 1. ⏎ Phạm vi"
    html = '<p><strong><span>Điều</span> <span>1.</span> <span>Phạm vi điều chỉnh</span></strong></p><p>Nội dung.</p>'
    tho = text_tho(html)
    assert not any(RE_TIEU_DE_B.match(x) for x in tho.split("\n"))
    assert do_tieu_de(tho, [1])["thieu"] == 1
    sach = chuan_hoa(html)
    assert dong(sach)[0] == "Điều 1. Phạm vi điều chỉnh"
    assert do_tieu_de(sach, [1])["thieu"] == 0


def test_ten_dieu_o_dong_ke_va_ky_tu_eth():
    html = "<p>Ðiều 5.</p><p>Quyền và nghĩa vụ</p><p>1. Khoản một.</p>"
    assert dong(chuan_hoa(html))[:2] == ["Điều 5. Quyền và nghĩa vụ", "1. Khoản một."]


def test_ten_chuong_bi_br_ngat_va_dong_trang_tri():
    html = "<p>________</p><p>Chương IV</p><p><b>KIỂM TRA, GIÁM SÁT;<br/>HOÀN TRẢ KINH PHÍ</b></p><p>Điều 9. Tên</p>"
    assert dong(chuan_hoa(html)) == ["Chương IV", "KIỂM TRA, GIÁM SÁT; HOÀN TRẢ KINH PHÍ", "Điều 9. Tên"]


def test_br_giua_cau():
    html = "<p>2. Cơ quan có thẩm quyền xem xét<br/>quyết định trong thời hạn 10 ngày.</p><p>a) điểm a.</p>"
    assert dong(chuan_hoa(html)) == ["2. Cơ quan có thẩm quyền xem xét quyết định trong thời hạn 10 ngày.", "a) điểm a."]


def test_chu_thich_li_footnote():
    html = ('<p>Điều 1. Tên<sup class="footnote-ref">[2]</sup></p><p>Nội dung.</p><hr class="footnotes-sep"/>'
            '<ol class="footnotes-list"><li class="footnote-item" id="fn-2"><p>Nghị định 1/2026/NĐ-CP có căn cứ:</p>'
            '<p>Điều 2 của Luật số 9/2025/QH15 …</p><a class="footnote-backref">↩</a></li>'
            '<li class="footnote-item" id="fn-3"><p>Khoản này được bổ sung.</p></li></ol>')
    d = dong(chuan_hoa(html))
    assert d[-2].startswith("[2] Nghị định 1/2026/NĐ-CP có căn cứ: Điều 2 của Luật")
    assert d[-1] == "[3] Khoản này được bổ sung."
    assert "↩" not in "".join(d)
    # đoạn chú thích mở đầu bằng "Điều 2 của …" KHÔNG thành tiêu đề Điều
    assert sum(bool(RE_TIEU_DE_B.match(x)) for x in d) == 1


def test_bo_can_cu_nho_nhan_chu_ky_phu_luc():
    t = "\n".join([
        "THÔNG TƯ", "Căn cứ Luật A;", "Nghị định 5/2020/NĐ-CP quy định …;", "Theo đề nghị của Vụ trưởng;",
        "Điều 1. Phạm vi", "Nội dung một.", "Điều 2. Hiệu lực", "Thông tư có hiệu lực.",
        "Nơi nhận:", "- Như Điều 2;", "- Lưu: VT.", "KT. BỘ TRƯỞNG", "THỨ TRƯỞNG", "Nguyễn Văn A",
        "Phụ lục I", "Mẫu đơn …", "Nơi nhận:", "- Bộ X.",
    ]) + "\n"
    sach, bo = bo_dau_cuoi(t, [1, 2])
    assert dong(sach) == ["THÔNG TƯ", "Điều 1. Phạm vi", "Nội dung một.", "Điều 2. Hiệu lực", "Thông tư có hiệu lực."]
    assert bo["can_cu"] == 3 and bo["noi_nhan"] == 3 and bo["chu_ky"] == 3 and bo["phu_luc_tu"] > 0


def test_khoi_chu_ky_giua_van_ban():
    # quyết định 3 Điều + quy chế kèm theo; khối xác thực VBHN kẹp giữa hai phần
    t = "\n".join([
        "Điều 1. Ban hành kèm theo Quyết định này Quy chế.", "Điều 2. Hiệu lực.", "Điều 3. Trách nhiệm thi hành.",
        "BỘ CÔNG THƯƠNG", "Số: 56/VBHN-BCT", "Nơi nhận:", "- Bộ Tư pháp;", "XÁC THỰC VĂN BẢN HỢP NHẤT",
        "KT. BỘ TRƯỞNG", "(Đã ký)", "Nguyễn Văn B",
        "QUY CHẾ", "Xây dựng chương trình", "Chương I", "QUY ĐỊNH CHUNG", "Điều 1. Phạm vi", "Nội dung.",
    ]) + "\n"
    sach, bo = bo_dau_cuoi(t, [1, 2, 3])
    d = dong(sach)
    assert d[3] == "QUY CHẾ" and "Nơi nhận:" not in d and bo["khoi_giua"] == 1


def test_cong_van_khong_bo_can_cu():
    t = "Kính gửi: Các Bộ\nCăn cứ ý kiến của Thủ tướng, đề nghị các Bộ thực hiện.\nKT. BỘ TRƯỞNG\nNguyễn Văn C\n"
    sach, bo = bo_dau_cuoi(t, [])
    assert "Căn cứ ý kiến" in sach and bo["can_cu"] == 0
