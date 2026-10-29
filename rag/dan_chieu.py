"""Dò dẫn chiếu tường minh trong một chunk và kéo đơn vị đích vào ngữ cảnh sinh (phương pháp E3).

Ba dạng dò được, lấy từ lối viết thật trong VBQPPL:

  1. **cùng văn bản**  — "khoản 2 Điều 14 của Luật này", "Điều 7 Nghị định này", "Điều này"
  2. **khác văn bản**  — "Điều 35 của 19/2021/TT-BTC", "khoản 1 Điều 5 Nghị định 100/2019/NĐ-CP"
  3. **trong cùng Điều** — "trừ trường hợp quy định tại khoản 3", "theo quy định tại điểm a khoản 2"

CHỈ THEO MỘT BƯỚC: đơn vị đích được kéo vào nguyên văn, nhưng dẫn chiếu NẰM TRONG đơn vị đích
thì không theo tiếp. Theo nhiều bước sẽ nở ra rất nhanh và không còn kiểm soát được ngân sách.

Đếm được: số dẫn chiếu theo được / không theo được, tách cùng văn bản với khác văn bản — xem
`THONG_KE`. Không theo được thường vì đích nằm ngoài kho 80 văn bản, hoặc số Điều không có thật.
"""
import collections
import re

import cau_hinh as ch
from chunking.base import nap_van_ban
from eval import don_vi, trich_dan

# "của Luật này / Nghị định này / Thông tư này / Bộ luật này …"
_NAY = r"(?:của\s+)?(?:Luật|Bộ\s+luật|Nghị\s+định|Thông\s+tư|Quyết\s+định|Nghị\s+quyết|Pháp\s+lệnh|Chỉ\s+thị|Điều\s+lệ|Quy\s+chế|Quy\s+định)\s+này"
# khoản/điểm đứng trước Điều: "điểm a khoản 2 Điều 14"
_TRUOC = r"(?:điểm\s+(?P<diem>[a-zđ])\s+)?(?:khoản\s+(?P<khoan>\d+)\s+)?"

RE_CUNG_VB = re.compile(rf"{_TRUOC}Điều\s+(?P<dieu>\d+)\s*(?:,\s*)?{_NAY}", re.U | re.I)
# "khoản 3 Điều này", "điểm a khoản 2 Điều này" — đích là ĐIỀU ĐANG ĐỌC, không phải Điều khác
RE_DIEU_NAY = re.compile(rf"{_TRUOC}Điều\s+này", re.U | re.I)
RE_KHAC_VB = re.compile(
    rf"{_TRUOC}Điều\s+(?P<dieu>\d+)\s*(?:,\s*)?(?:của\s+)?"
    r"(?:Luật|Bộ\s+luật|Nghị\s+định|Thông\s+tư|Quyết\s+định|Nghị\s+quyết|Pháp\s+lệnh)?\s*"
    r"(?:số\s+)?(?P<sh>\d{1,5}\s*/\s*(?:\d{4}\s*/\s*)?[A-ZĐ]{2,}[a-zđ]{0,3}[0-9]*(?:\s*-\s*[A-ZĐ]{2,}[a-zđ]{0,3}[0-9]*)*)",
    re.U)
# "trừ trường hợp quy định tại khoản 3", "theo quy định tại điểm a khoản 2" — KHÔNG kèm Điều
RE_TRONG_DIEU = re.compile(
    r"(?:trừ\s+trường\s+hợp\s+|theo\s+)?quy\s+định\s+tại\s+"
    r"(?:điểm\s+(?P<diem>[a-zđ])\s+)?khoản\s+(?P<khoan>\d+)(?!\s*(?:,\s*)?\d+\s*(?:,|và|\s)*\s*Điều\s+\d)",
    re.U | re.I)

THONG_KE = collections.Counter()
_DV: dict[str, dict] = {}
_SH2DOC: dict[frozenset, str] = {}
_DOCS = None


def _nap():
    global _DOCS
    if _DOCS is None:
        _DOCS = {d.doc_id: d for d in nap_van_ban()}
        for d in _DOCS.values():
            k = trich_dan.khoa_tu_chuoi(d.so_hieu)
            if k:
                _SH2DOC[k] = d.doc_id
    return _DOCS


def _don_vi(doc_id: str) -> dict:
    if doc_id not in _DV:
        ci = don_vi.chi_muc(_nap()[doc_id])
        _DV[doc_id] = {(u.dieu, u.khoan, u.diem): u for lv in ci.values() for u in lv}
    return _DV[doc_id]


def quet(text: str, doc_id: str, dieu_hien: int | None) -> list[tuple[str, str, tuple]]:
    """Dẫn chiếu tìm thấy trong `text` → [(loại, doc_id đích, (dieu, khoan, diem))], đã bỏ trùng."""
    _nap()
    ra, thay = [], set()

    def them(loai, dich, kh):
        if dich and kh not in thay:
            thay.add(kh)
            ra.append((loai, dich, kh))

    for m in RE_CUNG_VB.finditer(text):
        kh = (int(m["dieu"]), int(m["khoan"]) if m["khoan"] else None, m["diem"])
        them("cung_vb", doc_id, kh)
    for m in RE_KHAC_VB.finditer(text):
        k = trich_dan.khoa_tu_chuoi(m["sh"])
        dich = _SH2DOC.get(k) if k else None
        kh = (int(m["dieu"]), int(m["khoan"]) if m["khoan"] else None, m["diem"])
        if dich is None:
            THONG_KE["khac_vb_ngoai_kho"] += 1
            continue
        them("khac_vb", dich, kh)
    if dieu_hien is not None:
        for m in RE_DIEU_NAY.finditer(text):
            them("trong_dieu", doc_id, (dieu_hien, int(m["khoan"]) if m["khoan"] else None, m["diem"]))
        for m in RE_TRONG_DIEU.finditer(text):
            them("trong_dieu", doc_id, (dieu_hien, int(m["khoan"]), m["diem"]))
    return ra


def keo(text: str, doc_id: str, dieu_hien: int | None) -> list[dict]:
    """Đơn vị đích của mọi dẫn chiếu trong `text`. Một bước, không theo dẫn chiếu của dẫn chiếu."""
    _nap()
    ra = []
    for loai, dich, (d, k, dm) in quet(text, doc_id, dieu_hien):
        bang = _don_vi(dich)
        u = bang.get((d, k, dm)) or bang.get((d, k, None)) or bang.get((d, None, None))
        if u is None:
            THONG_KE[f"{loai}_khong_thay"] += 1
            continue
        THONG_KE[f"{loai}_theo_duoc"] += 1
        t = _nap()[dich].text[u.start:u.end]
        ra.append({"nhan": u.nhan(), "text": f"[dẫn chiếu → {u.nhan()}]\n{t}",
                   "doc_id": dich, "so_hieu": u.so_hieu, "start": u.start, "end": u.end,
                   "loai": loai, "so_tu": len(t.split()) + 6})
    return ra
