"""Bóc trích dẫn "Điều X khoản Y (điểm z) của <số hiệu>" khỏi câu trả lời của mô hình sinh.

Mô hình nhỏ hay viết lệch số hiệu ("Nghị định 45/2019/QH14", "QH14 số 45/2019"), viết khoản trước Điều
("khoản 2 Điều 5"), hoặc ghi điểm không có chữ "điểm" ("Điều 113 khoản 1 a"). Bộ phân tích chấp nhận các
biến thể này; số hiệu so khớp theo TẬP thành phần {số, năm, ký hiệu} nên đảo thứ tự hay thêm/bớt tên loại
văn bản vẫn nhận ra. Mỗi trích dẫn trả về: (so_hieu_chuan | None, dieu | None, khoan | None, diem | None).
"""
import re
import unicodedata

# số hiệu dạng chuẩn: 45/2019/QH14, 100/2019/NĐ-CP, 112/2026/VBHN-TT-NHNN, 4197/BQP-PC
RE_SO_HIEU = re.compile(r"\b(\d{1,5})\s*/\s*(?:(\d{4})\s*/\s*)?([A-ZĐ][A-ZĐ0-9]*(?:\s*-\s*[A-ZĐ0-9]+)*)", re.U)
# dạng đảo: "QH14 số 45/2019"
RE_SO_HIEU_DAO = re.compile(r"\b([A-ZĐ][A-ZĐ0-9]*(?:-[A-ZĐ0-9]+)*)\s+số\s+(\d{1,5})\s*/\s*(\d{4})\b", re.U)
RE_DIEU = re.compile(r"Điều\s+(\d+[a-zđ]?)", re.U)
RE_KHOAN_SAU = re.compile(r"^\s*,?\s*(?:tại\s+)?khoản\s+(\d+)", re.U | re.I)
RE_KHOAN_TRUOC = re.compile(r"khoản\s+(\d+)\s*,?\s*(?:của\s+)?$", re.U | re.I)
RE_DIEM_SAU = re.compile(r"^\s*,?\s*(?:điểm\s+)?([a-zđ])\b(?!\w)", re.U)
RE_DIEM_TRUOC = re.compile(r"điểm\s+([a-zđ])\s*,?\s*$", re.U | re.I)


def chuan(s: str) -> str:
    return unicodedata.normalize("NFC", s).replace("Ð", "Đ")


def khoa_so_hieu(so: str, nam: str | None, ky_hieu: str) -> frozenset:
    ky = re.sub(r"\s+", "", ky_hieu).upper()
    phan = {so.lstrip("0") or "0", ky}
    if nam:
        phan.add(nam)
    return frozenset(phan)


def khoa_tu_chuoi(so_hieu: str) -> frozenset | None:
    """Khoá so khớp của một số hiệu chuẩn (lấy từ metadata)."""
    s = chuan(so_hieu)
    m = RE_SO_HIEU.search(s) or None
    if m:
        return khoa_so_hieu(m.group(1), m.group(2), m.group(3))
    m = RE_SO_HIEU_DAO.search(s)
    return khoa_so_hieu(m.group(2), m.group(3), m.group(1)) if m else None


def _so_hieu_gan(doan: str) -> frozenset | None:
    m = RE_SO_HIEU_DAO.search(doan)
    if m:
        return khoa_so_hieu(m.group(2), m.group(3), m.group(1))
    m = RE_SO_HIEU.search(doan)
    return khoa_so_hieu(m.group(1), m.group(2), m.group(3)) if m else None


def boc(tra_loi: str) -> list[tuple]:
    """Danh sách trích dẫn trong câu trả lời, theo thứ tự xuất hiện, bỏ trùng."""
    s = chuan(tra_loi or "")
    ra: list[tuple] = []
    for m in RE_DIEU.finditer(s):
        dieu = m.group(1)
        truoc, sau = s[max(0, m.start() - 40):m.start()], s[m.end():m.end() + 120]
        khoan = diem = None
        mk = RE_KHOAN_SAU.match(sau)
        if mk:
            khoan = mk.group(1)
            sau2 = sau[mk.end():]
            md = RE_DIEM_SAU.match(sau2)
            if md:
                diem = md.group(1)
        else:
            mk = RE_KHOAN_TRUOC.search(truoc)
            if mk:
                khoan = mk.group(1)
                md = RE_DIEM_TRUOC.search(truoc[:mk.start()])
                if md:
                    diem = md.group(1)
        # số hiệu: trong phần còn lại của câu (tới dấu chấm xuống dòng / Điều kế tiếp)
        het = re.search(r"Điều\s+\d|\n\n", sau)
        doan = sau[:het.start()] if het else sau
        sh = _so_hieu_gan(doan)
        t = (sh, int(re.match(r"\d+", dieu).group()), int(khoan) if khoan else None, diem)
        if t not in ra:
            ra.append(t)
    # văn bản không chia Điều: chỉ ghi số hiệu
    if not ra:
        sh = _so_hieu_gan(s)
        if sh:
            ra.append((sh, None, None, None))
    return ra


def tu_choi(tra_loi: str) -> bool:
    return "không đủ căn cứ" in chuan(tra_loi or "").lower()
