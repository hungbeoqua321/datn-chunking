"""Thử nghiệm mở rộng trên máy cá nhân: giới hạn độ dài chunk × rerank. KHÔNG thuộc thiết kế gốc của đồ án.

Câu hỏi: (1) đổi giới hạn N từ của chunk thì truy hồi đổi thế nào, cho cả cửa sổ cố định (A) lẫn cắt theo cấu
trúc (B)? (2) xếp lại bằng cross-encoder có cải thiện không, và cải thiện cho cách cắt nào?

  A<N>   cửa sổ cố định N từ, không chồng lấn (A gốc = A300)
  B<N>   cắt Điều → Khoản → Điểm, khối > N từ thì tách tiếp; văn bản không có Điều dùng cửa sổ N từ
  B_goc  B đúng như đồ án (ngưỡng 350, cửa sổ 300) — đối chứng: phải trùng B gốc
  N ∈ {100, 200, 300, 500}

Mọi thứ nằm trong thuc_nghiem/data/ — PHẢI chạy với CHUNKS_DIR / INDEX_DIR trỏ vào đó (script tự kiểm):

    set CHUNKS_DIR=thuc_nghiem/data/chunks INDEX_DIR=thuc_nghiem/data/index (xem docs/thuc-nghiem-mo-rong.md)
    python -m thuc_nghiem.chay chunk                       # dựng chunk (bỏ qua file đã có)
    NHUNG_DEVICE=cuda python -m rag.chi_muc A100_s0 ...    # nhúng
    python -m thuc_nghiem.chay danh_gia                    # chốt chặn chỉ mục rồi chấm
                                                           # → thuc_nghiem/ket_qua/metrics.{csv,md}

Chấm bằng đúng hàm của eval/chay_truy_hoi.py (Recall@k, Recall@W, MRR, bản tương đương) trên 110 câu chính.
Rerank: lấy K_UNG_VIEN = 50 ứng viên dense, cross-encoder chấm lại, xếp theo điểm mới.
"""
import argparse
import csv
import json
import time

import cau_hinh as ch
from chunking import base, fixed, structural
from chunking.base import ghi_jsonl, nap_van_ban
from eval import cham, don_vi
from eval.chay_truy_hoi import CAU_HOI, DO_DO, _do, _gom, _td_cho
from rag import truy_hoi
from rag.kiem_chi_muc import chot_chan

GIOI_HAN = (100, 200, 300, 500)
RA = ch.GOC / "thuc_nghiem" / "ket_qua"
CHE_DO = ("khong", "bge", "aiteam")   # không rerank / hai cross-encoder


def cau_hinh_chunk() -> dict:
    """{tên: (hàm chunk, CUA_SO, DIEU_TOI_DA)}"""
    ra = {}
    for n in GIOI_HAN:
        ra[f"A{n}"] = (fixed.chunk, n, ch.DIEU_TOI_DA)
        ra[f"B{n}"] = (structural.chunk, n, n)
    ra["B_goc"] = (structural.chunk, 300, 350)
    return ra


def _kiem_thu_muc() -> None:
    if ch.CHUNKS == ch.DATA / "chunks" or ch.INDEX == ch.DATA / "index":
        raise SystemExit("Đặt CHUNKS_DIR và INDEX_DIR sang thuc_nghiem/data/ — không ghi vào data/ của đồ án.")


def dung_chunk(force: bool = False) -> None:
    _kiem_thu_muc()
    docs = nap_van_ban()
    cu = (ch.CUA_SO, ch.DIEU_TOI_DA, base.cua_so.__defaults__)
    for ten, (ham, cs, dtd) in cau_hinh_chunk().items():
        p = ch.CHUNKS / f"{ten}_s0.jsonl"
        if p.exists() and not force:
            print("có rồi:", p.name)
            continue
        # cua_so(co=ch.CUA_SO) lấy giá trị mặc định LÚC ĐỊNH NGHĨA (300) — B cắt khoản/điểm dài bằng mặc định đó,
        # nên phải đổi cả __defaults__ thì giới hạn N mới áp lên mọi tầng.
        ch.CUA_SO, ch.DIEU_TOI_DA, base.cua_so.__defaults__ = cs, dtd, (cs, 0)
        try:
            ds = [c for d in docs for c in ham(d, 0)]
        finally:
            ch.CUA_SO, ch.DIEU_TOI_DA, base.cua_so.__defaults__ = cu
        ghi_jsonl(p, ds)
        tu = sorted(c.n_words for c in ds)
        print(f"{p.name}: {len(ds)} chunk, trung vị {tu[len(tu) // 2]} từ, lớn nhất {tu[-1]}")


def chuan_bi() -> tuple[list, list, list]:
    """(câu hỏi, bản tương đương của gold, vector câu hỏi) — như eval/chay_truy_hoi.py."""
    docs = nap_van_ban()
    van_ban = {d.doc_id: d.text for d in docs}
    so_hieu = {d.doc_id: d.so_hieu for d in docs}
    cap = cham.doc_cap()
    dv = {}
    for d in docs:
        if d.so_hieu in cap:
            ci = don_vi.chi_muc(d)
            dv[d.doc_id] = ci["dieu"] + ci["khoan"] + ci["diem"] + ci["doan"]
    ds = [json.loads(l) for l in open(CAU_HOI) if l.strip()]
    td = [_td_cho(x["gold"], van_ban, so_hieu, dv, cap, bool(x.get("phien_ban"))) for x in ds]
    vec = [truy_hoi.nhung_cau_hoi(x["question"]) for x in ds]
    return ds, td, vec


def cham_chi_muc(idx: str, che_do: tuple[str, ...], ds, td, vec, diem: dict, thoi_gian: dict) -> None:
    """Chấm một chỉ mục với từng chế độ rerank, ghi vào diem[(tên, chế độ)] = {độ đo: [điểm từng câu]}."""
    dense = [[c for c, _ in truy_hoi.tim(idx, vec[i], k=ch.K_UNG_VIEN)] for i in range(len(ds))]
    for cd in che_do:
        t0 = time.monotonic()
        if cd == "khong":
            kq = dense
        else:
            from rag import rerank
            kq = [[c for c, _ in rerank.xep_lai(cd, x["question"], dense[i])] for i, x in enumerate(ds)]
        k = (idx.removesuffix("_s0"), cd)
        thoi_gian[k] = time.monotonic() - t0
        diem[k] = {d: [] for d in DO_DO}
        for i, x in enumerate(ds):
            for d, v in _do(x["gold"], kq[i], td[i]).items():
                diem[k][d].append(v)
        print(f"  {k[0]:9s} rerank={cd:7s} R@1={sum(diem[k]['R@1']) / len(ds):.3f} "
              f"R@5={sum(diem[k]['R@5']) / len(ds):.3f} MRR={sum(diem[k]['MRR']) / len(ds):.3f} "
              f"({thoi_gian[k]:.0f}s)", flush=True)


def danh_gia(che_do: tuple[str, ...]) -> None:
    _kiem_thu_muc()
    ten = [f"{t}_s0" for t in cau_hinh_chunk()]
    chot_chan(ten)
    t_all = time.monotonic()
    ds, td, vec = chuan_bi()
    diem, thoi_gian = {}, {}
    for idx in ten:
        cham_chi_muc(idx, che_do, ds, td, vec, diem, thoi_gian)

    nhom = [x["loai"] for x in ds]
    taps = {"tất cả": list(range(len(ds)))}
    for g in sorted(set(nhom)):
        taps[f"nhóm {g}"] = [i for i, x in enumerate(nhom) if x == g]
    dong = []
    for (pp, cd), dd in diem.items():
        for tt, idx in taps.items():
            for d, v in _gom(dd, idx).items():
                dong.append({"loai_dong": "diem", "pp": pp, "rerank": cd, "tap": tt, "n": len(idx), "do_do": d,
                             "gia_tri": round(v, 4), "ci_duoi": "", "ci_tren": "", "so_voi": ""})
    # hiệu số kèm bootstrap ghép cặp 95%: (1) mọi cấu hình − A300 không rerank (baseline đồ án);
    # (2) rerank − cùng chỉ mục không rerank (tác dụng riêng của rerank)
    cap_hieu = [((pp, cd), ("A300", "khong")) for pp, cd in diem if (pp, cd) != ("A300", "khong")]
    cap_hieu += [((pp, cd), (pp, "khong")) for pp, cd in diem if cd != "khong" and pp != "A300"]
    for (b, a) in cap_hieu:
        for tt, idx in taps.items():
            nh = [nhom[i] for i in idx]
            for d in DO_DO:
                h, lo, hi = cham.bootstrap_hieu([diem[a][d][i] for i in idx], [diem[b][d][i] for i in idx], nhom=nh)
                dong.append({"loai_dong": "hieu", "pp": b[0], "rerank": b[1], "tap": tt, "n": len(idx), "do_do": d,
                             "gia_tri": round(h, 4), "ci_duoi": round(lo, 4), "ci_tren": round(hi, 4),
                             "so_voi": f"{a[0]}/{a[1]}"})
    RA.mkdir(parents=True, exist_ok=True)
    with open(RA / "metrics.csv", "w", newline="") as f:
        w = csv.DictWriter(f, list(dong[0]))
        w.writeheader()
        w.writerows(dong)
    viet_md(dong, diem, thoi_gian, len(ds), time.monotonic() - t_all)
    print(f"→ {RA / 'metrics.csv'} ({len(dong)} dòng), {RA / 'metrics.md'}; tổng {time.monotonic() - t_all:.0f}s")


def viet_md(dong, diem, thoi_gian, n, giay) -> None:
    def o(pp, cd, d, tap="tất cả"):
        return next(x["gia_tri"] for x in dong if x["loai_dong"] == "diem" and x["pp"] == pp
                    and x["rerank"] == cd and x["tap"] == tap and x["do_do"] == d)

    def h(pp, cd, d, so_voi, tap="tất cả"):
        x = next(x for x in dong if x["loai_dong"] == "hieu" and x["pp"] == pp and x["rerank"] == cd
                 and x["tap"] == tap and x["do_do"] == d and x["so_voi"] == so_voi)
        dam = "**" if x["ci_duoi"] > 0 or x["ci_tren"] < 0 else ""
        return f"{dam}{x['gia_tri']:+.3f}{dam} [{x['ci_duoi']:+.3f}; {x['ci_tren']:+.3f}]"

    pps = list(dict.fromkeys(pp for pp, _ in diem))
    cds = list(dict.fromkeys(cd for _, cd in diem))
    md = ["# Thử nghiệm mở rộng: giới hạn độ dài chunk × rerank", "",
          f"{n} câu hỏi chính, chấm bằng hàm của `eval/chay_truy_hoi.py`. Nhúng trên GPU (RTX 2050), "
          f"rerank lấy {ch.K_UNG_VIEN} ứng viên dense. Tổng thời gian chấm {giay:.0f}s. "
          "Hiệu số: bootstrap ghép cặp 95% (1000 lần, phân tầng theo nhóm câu hỏi); **đậm** = khoảng tin cậy "
          "không chứa 0.", ""]
    for d in ("R@1", "R@5", "R@1200t", "MRR"):
        md += [f"## {d}", "", "| Chunk | " + " | ".join(f"rerank={c}" for c in cds) + " |",
               "|---|" + "---:|" * len(cds)]
        md += [f"| {pp} | " + " | ".join(f"{o(pp, c, d):.3f}" for c in cds) + " |" for pp in pps]
        md.append("")
    md += ["## Hiệu so với baseline A300 (không rerank)", "", "| Cấu hình | R@5 | MRR |", "|---|---|---|"]
    for pp, cd in diem:
        if (pp, cd) != ("A300", "khong"):
            md.append(f"| {pp} / {cd} | {h(pp, cd, 'R@5', 'A300/khong')} | {h(pp, cd, 'MRR', 'A300/khong')} |")
    md += ["", "## Tác dụng riêng của rerank (so với cùng chỉ mục không rerank)", "",
           "| Cấu hình | R@1 | R@5 | MRR |", "|---|---|---|---|"]
    for pp, cd in diem:
        if cd != "khong":
            sv = f"{pp}/khong"
            md.append(f"| {pp} / {cd} | {h(pp, cd, 'R@1', sv)} | {h(pp, cd, 'R@5', sv)} | {h(pp, cd, 'MRR', sv)} |")
    md += ["", "## Thời gian rerank (110 câu)", "", "| Chunk | " + " | ".join(c for c in cds if c != "khong") + " |",
           "|---|" + "---:|" * (len(cds) - 1)]
    md += [f"| {pp} | " + " | ".join(f"{thoi_gian[(pp, c)]:.0f}s" for c in cds if c != "khong") + " |" for pp in pps]
    (RA / "metrics.md").write_text("\n".join(md) + "\n")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("lenh", choices=("chunk", "danh_gia"))
    ap.add_argument("--rerank", nargs="*", default=list(CHE_DO), choices=CHE_DO)
    ap.add_argument("--force", action="store_true", help="chunk: dựng lại dù file đã có")
    a = ap.parse_args()
    dung_chunk(a.force) if a.lenh == "chunk" else danh_gia(tuple(a.rerank))


if __name__ == "__main__":
    main()
