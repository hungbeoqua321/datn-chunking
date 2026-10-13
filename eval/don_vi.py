"""Chỉ mục cấu trúc ĐỘC LẬP với bộ phân đoạn B — dùng để chọn gold và chấm trích dẫn.

Khác B ở chỗ: tách MỌI Điều thành khoản và MỌI khoản thành điểm (không có ngưỡng 350 từ), chỉ nhận dãy khoản /
điểm đánh số LIÊN TIẾP (1, 2, 3… / a, b, c, d, đ, e…) nên không nhầm dòng đánh số trong bảng; Điều thật xác định bằng
crawl.chuan_hoa.phan_loai_tieu_de (đối chiếu cây cấu trúc vbpl.vn, loại Điều trong ngoặc trích dẫn). Mỗi Điều ghi
`b_parse_ok`: số khoản tìm được có khớp số khoản trong cây vbpl không (None nếu cây không có).

Đơn vị: {doc_id, so_hieu, dieu, khoan, diem, start, end} — vị trí ký tự trong data/clean/<doc_id>.txt.

    python -m eval.don_vi            # in thống kê nhanh
"""
import argparse
import json
import re
from dataclasses import asdict, dataclass

import cau_hinh as ch
from chunking.base import Document, nap_van_ban
from crawl.chuan_hoa import dieu_ky_vong, phan_loai_tieu_de, vung_chu_thich

THU_TU_DIEM = list("abcdđeghiklmnopqrstuvxy")
RE_KHOAN = re.compile(r"^(\d+)[.)]\s")
RE_DIEM = re.compile(r"^([a-zđ])\)\s")


@dataclass
class DonVi:
    doc_id: str
    so_hieu: str
    dieu: int | None
    khoan: int | None
    diem: str | None
    start: int
    end: int
    b_parse_ok: bool | None = None

    def nhan(self) -> str:
        if self.dieu is None:
            return self.so_hieu
        s = f"Điều {self.dieu}"
        if self.khoan is not None:
            s = f"khoản {self.khoan} " + s
        if self.diem is not None:
            s = f"điểm {self.diem} " + s
        return s + f" của {self.so_hieu}"

    def dict(self) -> dict:
        return asdict(self)


def _dong(text: str) -> list[tuple[int, str]]:
    ra, i = [], 0
    for x in text.split("\n"):
        ra.append((i, x))
        i += len(x) + 1
    return ra


def _day_lien_tiep(ung: list[tuple[int, str]], thu_tu) -> list[tuple[int, str]]:
    """Giữ dãy mốc đánh số liên tiếp dài nhất bắt đầu từ phần tử đầu của thứ tự (1 hoặc a)."""
    tot, hien = [], []
    for vt, nhan in ung:
        k = thu_tu(nhan)
        if k == 0:
            hien = [(vt, nhan)]
        elif hien and k == thu_tu(hien[-1][1]) + 1:
            hien.append((vt, nhan))
        else:
            continue
        if len(hien) > len(tot):
            tot = list(hien)
    return tot


def _cay_khoan(doc_id: str) -> dict[int, int]:
    """{số Điều: số khoản} theo cây vbpl.vn."""
    p = ch.RAW / f"{doc_id}.cay.json"
    if not p.exists():
        return {}
    cay = json.loads(p.read_text())
    ra: dict[int, int] = {}

    def di(nut):
        for n in nut or []:
            if n.get("level") == "Article":
                m = re.match(r"\s*Điều\s+(\d+)", n.get("title") or "")
                if m:
                    ra[int(m.group(1))] = sum(1 for c in n.get("children") or [] if c.get("level") == "Clause")
            di(n.get("children"))

    if isinstance(cay, list):
        di(cay)
    return ra


def chi_muc(doc: Document) -> dict:
    """{'dieu': [DonVi], 'khoan': [DonVi], 'diem': [DonVi], 'doan': [DonVi] (văn bản không có Điều: từng đoạn)}."""
    t = doc.text
    dong = _dong(t)
    ds = [x for _, x in dong]
    kv, _ = dieu_ky_vong(doc.doc_id, (ch.CLEAN_FULL / f"{doc.doc_id}.txt").read_text())
    ct = vung_chu_thich(ds)
    het = dong[ct][0] if ct is not None else len(t)
    that = [(dong[i][0], n) for i, n, ok in phan_loai_tieu_de(ds, kv) if ok and dong[i][0] < het]
    cay = _cay_khoan(doc.doc_id)
    ra = {"dieu": [], "khoan": [], "diem": [], "doan": []}
    if not that:
        for vt, x in dong:
            if len(x.split()) >= 8 and vt < het:
                ra["doan"].append(DonVi(doc.doc_id, doc.so_hieu, None, None, None, vt, vt + len(x)))
        return ra
    for i, (a, n) in enumerate(that):
        b = that[i + 1][0] if i + 1 < len(that) else het
        while b > a and t[b - 1].isspace():
            b -= 1
        dong_dieu = [(vt, x) for vt, x in dong if a < vt < b]
        mk = _day_lien_tiep([(vt, m.group(1)) for vt, x in dong_dieu if (m := RE_KHOAN.match(x))], lambda s: int(s) - 1)
        ok = (len(mk) == cay[n]) if n in cay and cay[n] else None
        ra["dieu"].append(DonVi(doc.doc_id, doc.so_hieu, n, None, None, a, b, ok))
        for j, (ka, so) in enumerate(mk):
            kb = mk[j + 1][0] if j + 1 < len(mk) else b
            while kb > ka and t[kb - 1].isspace():
                kb -= 1
            ra["khoan"].append(DonVi(doc.doc_id, doc.so_hieu, n, int(so), None, ka, kb, ok))
            dong_k = [(vt, x) for vt, x in dong if ka < vt < kb]
            md = _day_lien_tiep([(vt, m.group(1)) for vt, x in dong_k if (m := RE_DIEM.match(x))],
                                lambda s: THU_TU_DIEM.index(s) if s in THU_TU_DIEM else -9)
            for h, (da, chu) in enumerate(md):
                db = md[h + 1][0] if h + 1 < len(md) else kb
                while db > da and t[db - 1].isspace():
                    db -= 1
                ra["diem"].append(DonVi(doc.doc_id, doc.so_hieu, n, int(so), chu, da, db, ok))
    return ra


def main() -> None:
    argparse.ArgumentParser(description=__doc__).parse_args()
    tong = {"dieu": 0, "khoan": 0, "diem": 0, "doan": 0, "ok": 0, "lech": 0, "khong_cay": 0}
    for d in nap_van_ban():
        cm = chi_muc(d)
        for k in ("dieu", "khoan", "diem", "doan"):
            tong[k] += len(cm[k])
        for u in cm["dieu"]:
            tong["ok" if u.b_parse_ok else "lech" if u.b_parse_ok is False else "khong_cay"] += 1
    print(tong)


if __name__ == "__main__":
    main()
