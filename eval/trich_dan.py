"""Bóc trích dẫn "Điều X khoản Y (điểm z) của <số hiệu>" khỏi câu trả lời của mô hình sinh.

Mô hình nhỏ hay viết lệch số hiệu ("Nghị định 45/2019/QH14", "QH14 số 45/2019"), viết khoản trước Điều
("khoản 2 Điều 5"), hoặc ghi điểm không có chữ "điểm" ("Điều 113 khoản 1 a"). Bộ phân tích chấp nhận các
biến thể này; số hiệu so khớp theo TẬP thành phần {số, năm, ký hiệu} nên đảo thứ tự hay thêm/bớt tên loại
văn bản vẫn nhận ra. Mỗi trích dẫn trả về: (so_hieu_chuan | None, dieu | None, khoan | None, diem | None).
"""
import re
import unicodedata

# Một mẩu ký hiệu: chạy hoa ít nhất 2 chữ, cho phép ĐUÔI THƯỜNG ngắn (TTg, BNg) và số đuôi (QH15).
# Đuôi thường là bắt buộc phải có, nếu không "09/CT-TTg" bị bóc thành "09/CT". Ràng buộc "ít nhất 2
# chữ hoa" để không nuốt nhầm một từ tiếng Việt viết hoa đầu câu ("Nghị", "Thông").
_KY = r"[A-ZĐ]{2,}[a-zđ]{0,3}[0-9]*"
# số hiệu dạng chuẩn: 45/2019/QH14, 100/2019/NĐ-CP, 112/2026/VBHN-TT-NHNN, 4197/BQP-PC, 09/CT-TTg
RE_SO_HIEU = re.compile(rf"\b(\d{{1,5}})\s*/\s*(?:(\d{{4}})\s*/\s*)?({_KY}(?:\s*-\s*{_KY})*)", re.U)
# số hiệu KIỂU CŨ: ký hiệu có dấu gạch chéo bên trong, năm nằm ngoài hoặc không có —
# "9367 TC/PC", "9367/TC/PC". Phải thử TRƯỚC RE_SO_HIEU, nếu không "9367/TC/PC" bị cắt còn "9367/TC".
RE_SO_HIEU_CU = re.compile(rf"\b(\d{{1,5}})\s*[/\s]\s*({_KY}(?:\s*-\s*{_KY})*(?:\s*/\s*{_KY}(?:\s*-\s*{_KY})*)+)", re.U)
# dạng đảo: "QH14 số 45/2019"
RE_SO_HIEU_DAO = re.compile(rf"\b({_KY}(?:-{_KY})*)\s+số\s+(\d{{1,5}})\s*/\s*(\d{{4}})\b", re.U)
# Dạng liệt kê "Điều 2, 3, 10 của X" — các số Điều tiếp theo đứng sau dấu phẩy, trước khi gặp
# "khoản"/"điểm" hay hết câu. Mỗi số là MỘT trích dẫn riêng.
RE_DIEU_TIEP = re.compile(r"^\s*(?:,|và)\s*(\d+[a-zđ]?)(?!\s*\d)", re.U)
# "khoản b" — mô hình hay viết "khoản" ở chỗ đáng lẽ là "điểm"; chữ cái luôn là ĐIỂM về mặt pháp lý.
RE_KHOAN_CHU_SAU = re.compile(r"^\s*,?\s*(?:tại\s+)?khoản\s+([a-zđ])\b(?!\w)", re.U | re.I)
# danh sách điểm: "a, b, c" / "a b c" / "a, b và c" ngay sau điểm/khoản-chữ đầu tiên
RE_DIEM_TIEP = re.compile(r"^\s*(?:,|và|;)?\s*([a-zđ])\b(?!\w)", re.U)
RE_DIEU = re.compile(r"Điều\s+(\d+[a-zđ]?)", re.U)
RE_KHOAN_SAU = re.compile(r"^\s*,?\s*(?:tại\s+)?khoản\s+(\d+)", re.U | re.I)
RE_KHOAN_TRUOC = re.compile(r"khoản\s+(\d+)\s*,?\s*(?:của\s+)?$", re.U | re.I)
RE_DIEM_SAU = re.compile(r"^\s*,?\s*(?:điểm\s+)?([a-zđ])\b(?!\w)", re.U)
RE_DIEM_TRUOC = re.compile(r"điểm\s+([a-zđ])\s*,?\s*$", re.U | re.I)


def chuan(s: str) -> str:
    return unicodedata.normalize("NFC", s).replace("Ð", "Đ")


def khoa_so_hieu(so: str, nam: str | None, ky_hieu: str) -> frozenset:
    """Khoá so khớp {số, năm, ký hiệu}. GIỮ SỐ 0 ĐẦU: "09/CT-TTg" khác "9/CT-TTg" — trước đây
    `lstrip("0")` biến 09 thành 9 nên bản bóc ra hiện sai số hiệu so với bản người đọc thấy."""
    ky = re.sub(r"\s+", "", ky_hieu).upper()
    phan = {so, ky}
    if nam:
        phan.add(nam)
    return frozenset(phan)


def khoa_tu_chuoi(so_hieu: str) -> frozenset | None:
    """Khoá so khớp của một số hiệu chuẩn (lấy từ metadata hoặc từ gold).

    Chuỗi gold là chuỗi NGẮN, có kiểm soát, nên viết hoa toàn bộ trước khi dò: nhờ vậy gold ghi
    thường ("04/ct-btc") vẫn khớp bản bóc ra ("04/CT-BTC"). Thử cả dạng KIỂU CŨ để "9367 TC/PC"
    (ngăn bằng khoảng trắng) cho cùng khoá với "9367/TC/PC" (ngăn bằng gạch chéo).
    """
    s = chuan(so_hieu).upper()
    m = RE_SO_HIEU_DAO.search(s)
    if m:
        return khoa_so_hieu(m.group(2), m.group(3), m.group(1))
    m = RE_SO_HIEU_CU.search(s)
    if m:
        return khoa_so_hieu(m.group(1), None, m.group(2))
    m = RE_SO_HIEU.search(s)
    return khoa_so_hieu(m.group(1), m.group(2), m.group(3)) if m else None


def _so_hieu_gan(doan: str) -> frozenset | None:
    m = RE_SO_HIEU_DAO.search(doan)
    if m:
        return khoa_so_hieu(m.group(2), m.group(3), m.group(1))
    m = RE_SO_HIEU_CU.search(doan)          # kiểu cũ trước: "9367/TC/PC" dài hơn "9367/TC"
    if m:
        return khoa_so_hieu(m.group(1), None, m.group(2))
    m = RE_SO_HIEU.search(doan)
    return khoa_so_hieu(m.group(1), m.group(2), m.group(3)) if m else None



def _danh_sach_diem(sau2: str, dau: str) -> list[str]:
    """Từ chữ cái điểm đầu tiên, gom tiếp danh sách "a, b, c" / "a b c" / "a, b và c"."""
    ds, con = [dau], sau2
    while True:
        m = RE_DIEM_TIEP.match(con)
        if not m or m.group(1) in ds:
            break
        ds.append(m.group(1))
        con = con[m.end():]
    return ds


def boc(tra_loi: str, mac_dinh: frozenset | None = None,
        cho_phep_khong_dieu: bool = False) -> list[tuple]:
    """Danh sách trích dẫn trong câu trả lời, theo thứ tự xuất hiện, bỏ trùng.

    QUY TẮC: một trích dẫn PHẢI CÓ ĐIỀU. Số hiệu đứng một mình giữa thân bài chỉ là *nhắc tới*
    văn bản, không phải trích dẫn, nên không bóc — trừ khi `cho_phep_khong_dieu` (văn bản đích
    vốn không chia Điều, ví dụ Chỉ thị: khi đó số hiệu CHÍNH LÀ trích dẫn).
    Trích dẫn trong thân bài vẫn được giữ; không còn lọc riêng mục "Căn cứ".

    mac_dinh: số hiệu của văn bản chunk truy hồi được, dùng khi cả câu trả lời không nêu số hiệu.

    Trích dẫn không nêu số hiệu ("Điều 132 khoản 2 của Bộ luật này") được gán số hiệu của trích
    dẫn TƯỜNG MINH GẦN NHẤT trong cùng câu trả lời — trước, rồi sau, cuối cùng `mac_dinh`.
    """
    s = chuan(tra_loi or "")
    ra: list[tuple] = []

    def them(sh, dieu, khoan, diems):
        for d in (diems or [None]):
            t = (sh, dieu, khoan, d)
            if t not in ra:
                ra.append(t)

    for m in RE_DIEU.finditer(s):
        dieu = m.group(1)
        truoc, sau = s[max(0, m.start() - 40):m.start()], s[m.end():m.end() + 120]
        khoan, diems = None, None
        mk = RE_KHOAN_SAU.match(sau)
        mkc = RE_KHOAN_CHU_SAU.match(sau)
        if mk:
            khoan = mk.group(1)
            sau2 = sau[mk.end():]
            md = RE_DIEM_SAU.match(sau2)
            if md:
                diems = _danh_sach_diem(sau2[md.end():], md.group(1))
        elif mkc:
            # "khoản b" → chữ cái là ĐIỂM, kể cả khi mô hình gọi nhầm là khoản
            diems = _danh_sach_diem(sau[mkc.end():], mkc.group(1))
        else:
            mk = RE_KHOAN_TRUOC.search(truoc)
            if mk:
                khoan = mk.group(1)
                md = RE_DIEM_TRUOC.search(truoc[:mk.start()])
                if md:
                    diems = [md.group(1)]
        # số hiệu: trong phần còn lại của câu (tới dấu chấm xuống dòng / Điều kế tiếp)
        het = re.search(r"Điều\s+\d|\n\n", sau)
        doan = sau[:het.start()] if het else sau
        sh = _so_hieu_gan(doan)
        so_dieu = int(re.match(r"\d+", dieu).group())
        them(sh, so_dieu, int(khoan) if khoan else None, diems)
        # "Điều 2, 3, 10 của X": các số sau dấu phẩy cũng là Điều, cùng số hiệu
        if not khoan and not diems:
            con = sau
            while (mt := RE_DIEU_TIEP.match(con)):
                them(sh, int(re.match(r"\d+", mt.group(1)).group()), None, None)
                con = con[mt.end():]
    if not ra and cho_phep_khong_dieu:
        sh = _so_hieu_gan(s)
        if sh:
            ra.append((sh, None, None, None))
    return _gan_so_hieu_thieu(ra, mac_dinh)


def _gan_so_hieu_thieu(ra: list[tuple], mac_dinh: frozenset | None) -> list[tuple]:
    """Lấp số hiệu None bằng trích dẫn tường minh gần nhất (trước, rồi sau), cuối cùng `mac_dinh`."""
    if not any(t[0] is None for t in ra):
        return ra
    co = [t[0] for t in ra]
    out = []
    for i, t in enumerate(ra):
        sh = t[0]
        if sh is None:
            sh = next((c for c in reversed(co[:i]) if c), None) \
                 or next((c for c in co[i + 1:] if c), None) or mac_dinh
        out.append((sh,) + t[1:])
    # lấp xong có thể sinh trùng (hai trích dẫn cùng Điều/khoản, một ghi số hiệu một không)
    thay, kq = set(), []
    for t in out:
        if t not in thay:
            thay.add(t)
            kq.append(t)
    return kq


def tu_choi(tra_loi: str) -> bool:
    return "không đủ căn cứ" in chuan(tra_loi or "").lower()
