"""Truy hồi trên KHO OCR: nếu văn bản chỉ có bản scan, OCR rồi mới đưa vào RAG thì mất bao nhiêu?

Kho OCR = 80 văn bản của đồ án, trong đó mọi văn bản CÓ bản PDF gốc (ocr/data/pdf) được thay text chuẩn bằng
text OCR (ocr/data/ocr/<nguồn>/); văn bản không có PDF giữ nguyên text chuẩn. Chunk bằng A300 và B (cấu hình gốc)
→ A300ocr, B_gococr; so với A300, B_goc nhúng cùng thiết bị (thuc_nghiem/chay.py).

Chấm bằng đúng gold cũ: gold là vị trí ký tự trong data/clean, nên vị trí mỗi chunk OCR được CHIẾU về data/clean
qua dóng hàng từng từ (difflib, không autojunk). Từ OCR không khớp lấy vị trí của từ khớp gần nhất phía trước/sau.
Văn bản chỉ dùng được nếu dóng hàng phủ ≥ NGUONG_KHOP từ chuẩn — thấp hơn thì OCR quá hỏng để chiếu,
giữ text chuẩn và ghi lại (không bỏ ngầm).

    python -m thuc_nghiem.kho_ocr chunk --nguon tesseract_bo_do
    NHUNG_DEVICE=cuda python -m rag.chi_muc A300ocr_s0 B_gococr_s0
    python -m thuc_nghiem.kho_ocr danh_gia --nguon tesseract_bo_do
"""
import argparse
import bisect
import csv
import difflib
import json
import re
import time
from dataclasses import replace

import cau_hinh as ch
from chunking import fixed, structural
from chunking.base import nap_van_ban
from eval import cham
from eval.chay_truy_hoi import _gom
from rag.kiem_chi_muc import chot_chan
from thuc_nghiem.chay import RA, _kiem_thu_muc, cham_chi_muc, chuan_bi

OCR = ch.GOC / "ocr" / "data" / "ocr"
NGUONG_KHOP = 0.6
RE_TU = re.compile(r"\S+")


def chieu(ocr: str, chuan: str):
    """Trả hàm f(a, b) → (a', b'): vị trí ký tự [a, b) trong text OCR → vị trí tương ứng trong text chuẩn,
    và tỷ lệ từ chuẩn được dóng khớp."""
    wo = [(m.start(), m.end()) for m in RE_TU.finditer(ocr)]
    wc = [(m.start(), m.end()) for m in RE_TU.finditer(chuan)]
    sm = difflib.SequenceMatcher(None, [ocr[a:b] for a, b in wo], [chuan[a:b] for a, b in wc], autojunk=False)
    khop = {}
    for blk in sm.get_matching_blocks():
        for t in range(blk.size):
            khop[blk.a + t] = blk.b + t
    io = sorted(khop)
    ty_le = len(khop) / max(1, len(wc))

    def tu_chuan(i: int, sau: bool) -> int:
        """Từ chuẩn ứng với từ OCR thứ i (gần nhất phía trước, hoặc phía sau nếu `sau`)."""
        if i in khop:
            return khop[i]
        k = bisect.bisect_left(io, i)
        if sau and k < len(io):
            return khop[io[k]]
        return khop[io[k - 1]] if k > 0 else 0

    starts = [a for a, _ in wo]

    def f(a: int, b: int) -> tuple[int, int]:
        i = max(0, bisect.bisect_right(starts, a) - 1)
        j = max(i, bisect.bisect_left(starts, b) - 1)
        x, y = tu_chuan(i, sau=True), tu_chuan(j, sau=False)
        if y < x:
            y = x
        return wc[x][0], wc[y][1]

    return f, ty_le


def dung_chunk(nguon: str) -> None:
    _kiem_thu_muc()
    docs = nap_van_ban()
    co_ocr = {p.stem: p for p in (OCR / nguon).glob("*.txt")}
    bao_cao = []
    out = {"A300ocr": [], "B_gococr": []}
    for d in docs:
        dung = d
        f = None
        if d.doc_id in co_ocr:
            t = co_ocr[d.doc_id].read_text().replace("\f", "\n")
            f, ty_le = chieu(t, d.text)
            bao_cao.append({"id": d.doc_id, "so_hieu": d.so_hieu, "ty_le_khop": round(ty_le, 4),
                            "dung_ocr": ty_le >= NGUONG_KHOP})
            if ty_le >= NGUONG_KHOP:
                dung = replace(d, text=t)
            else:
                f = None
        for ten, ham in (("A300ocr", fixed.chunk), ("B_gococr", structural.chunk)):
            for c in ham(dung, 0):
                c = c.dict()
                if f:   # chiếu vị trí về text chuẩn để chấm bằng gold cũ; text giữ nguyên chữ OCR
                    c["start"], c["end"] = f(c["start"], c["end"])
                    for k in ("dieu_start", "dieu_end"):
                        c.pop(k, None)   # B+ mở rộng theo vị trí Điều trong text — không dùng ở đây
                    c["ocr"] = nguon
                out[ten].append(c)
    for ten, cs in out.items():
        p = ch.CHUNKS / f"{ten}_s0.jsonl"
        tam = p.with_suffix(".tmp")      # như chunking.base.ghi_jsonl, nhưng chunk đã là dict
        with open(tam, "w") as fp:
            for c in cs:
                fp.write(json.dumps(c, ensure_ascii=False) + "\n")
        tam.replace(p)
        print(f"{p.name}: {len(cs)} chunk")
    RA.mkdir(parents=True, exist_ok=True)
    with open(RA / f"kho_ocr_dong_hang_{nguon}.csv", "w", newline="") as fp:
        w = csv.DictWriter(fp, list(bao_cao[0]))
        w.writeheader()
        w.writerows(bao_cao)
    dung_duoc = sum(r["dung_ocr"] for r in bao_cao)
    print(f"{len(bao_cao)} văn bản có OCR, dùng được {dung_duoc} (khớp ≥ {NGUONG_KHOP:.0%}); "
          f"tỷ lệ khớp trung vị {sorted(r['ty_le_khop'] for r in bao_cao)[len(bao_cao) // 2]:.1%}")


def danh_gia(nguon: str) -> None:
    _kiem_thu_muc()
    ten = ["A300_s0", "A300ocr_s0", "B_goc_s0", "B_gococr_s0"]
    chot_chan(ten)
    t_all = time.monotonic()
    ds, td, vec = chuan_bi()
    dung = {r["id"] for r in csv.DictReader(open(RA / f"kho_ocr_dong_hang_{nguon}.csv")) if r["dung_ocr"] == "True"}
    diem, thoi_gian = {}, {}
    for idx in ten:
        cham_chi_muc(idx, ("khong", "bge"), ds, td, vec, diem, thoi_gian)
    taps = {"tất cả": list(range(len(ds))),
            "gold nằm trong văn bản đã OCR": [i for i, x in enumerate(ds)
                                               if all(g["doc_id"] in dung for g in x["gold"])]}
    nhom = [x["loai"] for x in ds]
    md = ["# Truy hồi trên kho OCR", "",
          f"Nguồn OCR: `{nguon}`. {len(dung)} văn bản được thay text chuẩn bằng text OCR. "
          f"Hiệu số: OCR − text chuẩn, bootstrap ghép cặp 95%; **đậm** = khoảng tin cậy không chứa 0. "
          f"Thời gian chấm {time.monotonic() - t_all:.0f}s.", ""]
    dong = []
    for tt, idx in taps.items():
        md += [f"## {tt} ({len(idx)} câu)", "", "| Chunk | Rerank | Độ đo | Text chuẩn | OCR | OCR − chuẩn |",
               "|---|---|---|---:|---:|---|"]
        for pp in ("A300", "B_goc"):
            for cd in ("khong", "bge"):
                a, b = diem[(pp, cd)], diem[(pp + "ocr", cd)]
                ga, gb = _gom(a, idx), _gom(b, idx)
                for d in ("R@1", "R@5", "R@1200t", "MRR"):
                    h, lo, hi = cham.bootstrap_hieu([a[d][i] for i in idx], [b[d][i] for i in idx],
                                                    nhom=[nhom[i] for i in idx])
                    dam = "**" if lo > 0 or hi < 0 else ""
                    md.append(f"| {pp} | {cd} | {d} | {ga[d]:.3f} | {gb[d]:.3f} | "
                              f"{dam}{h:+.3f}{dam} [{lo:+.3f}; {hi:+.3f}] |")
                    dong.append({"tap": tt, "n": len(idx), "pp": pp, "rerank": cd, "do_do": d,
                                 "chuan": round(ga[d], 4), "ocr": round(gb[d], 4), "hieu": round(h, 4),
                                 "ci_duoi": round(lo, 4), "ci_tren": round(hi, 4)})
        md.append("")
    with open(RA / "kho_ocr.csv", "w", newline="") as fp:
        w = csv.DictWriter(fp, list(dong[0]))
        w.writeheader()
        w.writerows(dong)
    (RA / "kho_ocr.md").write_text("\n".join(md) + "\n")
    print("\n".join(md))


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("lenh", choices=("chunk", "danh_gia"))
    ap.add_argument("--nguon", default="tesseract_bo_do", help="thư mục trong ocr/data/ocr/")
    a = ap.parse_args()
    dung_chunk(a.nguon) if a.lenh == "chunk" else danh_gia(a.nguon)


if __name__ == "__main__":
    main()
