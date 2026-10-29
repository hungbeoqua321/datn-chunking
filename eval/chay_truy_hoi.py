"""Đánh giá TẦNG TRUY HỒI cho mọi phương pháp — không cần bộ bóc trích dẫn, không gọi mô hình sinh.

    python -m eval.chay_truy_hoi            # chạy hết, ghi results/metrics_truy_hoi.{csv,md}

Ba phần:
  1. A, C, D, B trên 110 câu chính — Recall@k (k=1,3,5,10), Recall@W (W=300,600,1200), MRR.
     Tách 5 nhóm câu hỏi và tách gold trung lập / gold trùng ranh giới. Hiệu B − baseline kèm
     bootstrap ghép cặp 95%.
  2. B và 7 cấu hình E trên 35 câu manh_con, tách tập mất câu dẫn (15) và tập tầng cuối (21).
  3. Hai tập con bản cũ: đếm số lần mỗi phương pháp lấy về chunk của BẢN CŨ.

Chốt chặn chỉ mục chạy trước. Mọi con số ghi ra file, không in rồi thôi.
"""
import argparse
import collections
import csv
import json
import time

import cau_hinh as ch
from chunking.base import nap_van_ban
from eval import cham, don_vi
from rag import truy_hoi
from rag.kiem_chi_muc import chot_chan

CAU_HOI = ch.GOC / "eval/questions.jsonl"
MANH_CON = ch.GOC / "eval/manh_con.draft.jsonl"
QUET_BAN_CU = ch.GOC / "eval/quet_ban_cu_embedding.json"
CSV_RA = ch.RESULTS / "metrics_truy_hoi.csv"
MD_RA = ch.RESULTS / "metrics_truy_hoi.md"

PP_CHINH = [("A", "A_s0"), ("C", "C_s0"), ("D", "D_s0"), ("B", "B_s0")]
PP_E = [("B", "B_s0"), ("Eduoi", "Eduoi_s0"), ("Etren", "Etren_s0"), ("Etat_d", "Etat_d_s0"),
        ("Etat_k", "Etat_k_s0"), ("Etat_n", "Etat_n_s0"), ("Etat_s", "Etat_s_s0"),
        ("Echi_s", "Echi_s_s0")]
K = (1, 3, 5, 10)
W = ch.NGAN_SACH_TU
DO_DO = [f"R@{k}" for k in K] + [f"R@{w}t" for w in W] + ["MRR"]

# 11 câu trong tập con "bản cũ nhiễu thật" (results/phuong_phap_quet_ban_cu.md §3.1); q041 và q100
# đã bị XOÁ ở vòng duyệt bộ câu hỏi nên chỉ còn 9 — lọc lại theo bộ hiện hành chứ không chép cứng.
BAN_CU_NHIEU = ["q005", "q007", "q016", "q041", "q058", "q060", "q064", "q069", "q097", "q100", "q206"]


def _td_cho(golds, van_ban, so_hieu, dv, cap, phien_ban):
    """Bản tương đương của từng đơn vị gold → {chỉ số gold: [bản tương đương]}."""
    ra = {}
    for i, g in enumerate(golds):
        b = cham.ban_tuong_duong(g, van_ban, so_hieu, dv, cap, phien_ban)
        if b:
            ra[i] = b
    return ra


def _do(golds, kq, td):
    """Mọi độ đo của MỘT câu hỏi trên MỘT phương pháp."""
    r = {f"R@{k}": cham.recall_k(golds, kq, k, td=td) for k in K}
    for w in W:
        r[f"R@{w}t"] = cham.recall_k(golds, cham.cat_theo_tu(kq, w), 10**9, td=td)
    r["MRR"] = cham.mrr(golds, kq, k=10, td=td)
    return r


def _gom(diem: dict[str, list[dict]], tap: list[int]) -> dict[str, float]:
    """Trung bình từng độ đo trên các câu có chỉ số trong `tap`."""
    return {d: sum(diem[d][i] for i in tap) / len(tap) for d in DO_DO} if tap else {}


def chay_bo(ds, pps, van_ban, so_hieu, dv, cap, nhan=""):
    """Chấm mọi phương pháp trên một bộ câu hỏi. Trả {pp: {độ đo: [điểm từng câu]}}."""
    td = [_td_cho(x["gold"], van_ban, so_hieu, dv, cap, bool(x.get("phien_ban"))) for x in ds]
    vec = [truy_hoi.nhung_cau_hoi(x["question"]) for x in ds]
    ra, top = {}, {}
    for ten, idx in pps:
        t0 = time.monotonic()
        diem = {d: [] for d in DO_DO}
        top[ten] = []
        for i, x in enumerate(ds):
            kq = [c for c, _ in truy_hoi.tim(idx, vec[i], k=ch.K_UNG_VIEN)]
            top[ten].append(kq)
            for d, v in _do(x["gold"], kq, td[i]).items():
                diem[d].append(v)
        ra[ten] = diem
        print(f"  {nhan}{ten:7s} R@5={sum(diem['R@5'])/len(ds):.3f} "
              f"R@1200t={sum(diem['R@1200t'])/len(ds):.3f} MRR={sum(diem['MRR'])/len(ds):.3f} "
              f"({time.monotonic()-t0:.0f}s)", flush=True)
    return ra, top


def main() -> None:
    argparse.ArgumentParser(description=__doc__,
                            formatter_class=argparse.RawDescriptionHelpFormatter).parse_args()
    t_all = time.monotonic()
    chot_chan([i for _, i in PP_CHINH] + [i for _, i in PP_E])

    docs = nap_van_ban()
    van_ban = {d.doc_id: d.text for d in docs}
    so_hieu = {d.doc_id: d.so_hieu for d in docs}
    cap = cham.doc_cap()
    # chi_muc đắt → chỉ dựng cho văn bản NẰM TRONG bảng cặp tương đương, chỗ khác không cần
    can = {d.doc_id for d in docs if d.so_hieu in cap}
    dv = {}
    for d in docs:
        if d.doc_id in can:
            ci = don_vi.chi_muc(d)
            dv[d.doc_id] = ci["dieu"] + ci["khoan"] + ci["diem"] + ci["doan"]
    print(f"văn bản: {len(docs)} | dựng đơn vị cho {len(dv)} văn bản có cặp tương đương", flush=True)

    chinh = [json.loads(l) for l in open(CAU_HOI) if l.strip()]
    mc = [json.loads(l) for l in open(MANH_CON) if l.strip()]
    print(f"bộ chính {len(chinh)} câu | manh_con {len(mc)} câu", flush=True)

    print("\n— bộ chính —", flush=True)
    d_chinh, top_chinh = chay_bo(chinh, PP_CHINH, van_ban, so_hieu, dv, cap)
    print("\n— manh_con —", flush=True)
    d_mc, _ = chay_bo(mc, PP_E, van_ban, so_hieu, dv, cap)

    # ── các tập con ────────────────────────────────────────────────────────
    nhom = [x["loai"] for x in chinh]
    tap_chinh = {"tất cả": list(range(len(chinh)))}
    for g in sorted({x["loai"] for x in chinh}):
        tap_chinh[f"nhóm {g}"] = [i for i, x in enumerate(chinh) if x["loai"] == g]
    tap_chinh["gold trung lập"] = [i for i, x in enumerate(chinh) if x.get("trung_lap")]
    tap_chinh["gold trùng ranh giới"] = [i for i, x in enumerate(chinh) if not x.get("trung_lap")]

    tap_mc = {"tất cả": list(range(len(mc))),
              "mất câu dẫn": [i for i, x in enumerate(mc) if x.get("tap_mat_cau_dan")],
              "tầng cuối": [i for i, x in enumerate(mc) if x.get("tap_tang_cuoi")]}

    # ── ghi CSV (dạng dài) ─────────────────────────────────────────────────
    dong = []
    for bo, diem, taps in (("chinh", d_chinh, tap_chinh), ("manh_con", d_mc, tap_mc)):
        for pp in diem:
            for ten_tap, idx in taps.items():
                g = _gom(diem[pp], idx)
                for d in DO_DO:
                    dong.append({"loai_dong": "diem", "bo": bo, "pp": pp, "tap": ten_tap,
                                 "n": len(idx), "do_do": d, "gia_tri": round(g[d], 4),
                                 "ci_duoi": "", "ci_tren": ""})
    # hiệu số. Bộ chính: B − từng baseline (B là hướng chính), và C − A, D − A để thấy hai
    # baseline kia đứng đâu so với baseline gốc. manh_con: từng cấu hình E − B.
    cap_hieu = ([("chinh", d_chinh, tap_chinh, pp, "B") for pp in d_chinh if pp != "B"]
                + [("chinh", d_chinh, tap_chinh, "A", pp) for pp in ("C", "D")]
                + [("manh_con", d_mc, tap_mc, "B", pp) for pp in d_mc if pp != "B"])
    for bo, diem, taps, a, b in cap_hieu:
        for ten_tap, idx in taps.items():
            nh = [nhom[i] for i in idx] if bo == "chinh" else None
            for d in DO_DO:
                x = [diem[a][d][i] for i in idx]
                y = [diem[b][d][i] for i in idx]
                h, lo, hi = cham.bootstrap_hieu(x, y, nhom=nh)
                dong.append({"loai_dong": "hieu", "bo": bo, "pp": f"{b} − {a}", "tap": ten_tap,
                             "n": len(idx), "do_do": d, "gia_tri": round(h, 4),
                             "ci_duoi": round(lo, 4), "ci_tren": round(hi, 4)})

    # ── tập con bản cũ ─────────────────────────────────────────────────────
    quet = {x["qid"]: x for x in json.load(open(QUET_BAN_CU))}
    sh2doc = collections.defaultdict(list)
    for d, s in so_hieu.items():
        sh2doc[s].append(d)
    bo_cu = {}
    for ten, chon in (("ban_cu_nhieu", lambda x: x["qid"] in BAN_CU_NHIEU),
                      ("phien_ban", lambda x: bool(x.get("phien_ban")))):
        idx = [i for i, x in enumerate(chinh) if chon(x)]
        cu = {}
        for i in idx:
            x = chinh[i]
            if x.get("phien_ban_cu"):
                cu[i] = {g["doc_id"] for g in x["phien_ban_cu"]}
            else:                                     # lấy số hiệu bản cũ từ chuỗi "cặp" của bản quét
                s = quet.get(x["qid"], {}).get("cap", "")
                sh = s.split("↔")[-1].strip().split(" ")[0] if "↔" in s else ""
                cu[i] = set(sh2doc.get(sh, []))
        bo_cu[ten] = (idx, cu)
        for pp in d_chinh:
            for k in (5, 10):
                n = sum(1 for i in idx if any(c["doc_id"] in cu[i] for c in top_chinh[pp][i][:k]))
                dong.append({"loai_dong": "ban_cu", "bo": ten, "pp": pp, "tap": f"top-{k}",
                             "n": len(idx), "do_do": "số câu lấy về bản cũ", "gia_tri": n,
                             "ci_duoi": "", "ci_tren": ""})

    with open(CSV_RA, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["loai_dong", "bo", "pp", "tap", "n", "do_do",
                                          "gia_tri", "ci_duoi", "ci_tren"])
        w.writeheader()
        w.writerows(dong)
    print(f"\n→ {CSV_RA} ({len(dong)} dòng)", flush=True)
    viet_md(dong, len(chinh), len(mc), bo_cu, time.monotonic() - t_all)
    print(f"→ {MD_RA}", flush=True)
    print(f"tổng {time.monotonic()-t_all:.0f}s", flush=True)


def _lay(dong, **kw):
    return [d for d in dong if all(d[k] == v for k, v in kw.items())]


def _o(d):
    """Ô hiệu số: giá trị kèm CI, in đậm nếu CI không chứa 0."""
    v, lo, hi = d["gia_tri"], d["ci_duoi"], d["ci_tren"]
    s = f"{v:+.3f} [{lo:+.3f}; {hi:+.3f}]"
    return f"**{s}**" if (lo > 0 or hi < 0) else s


def viet_md(dong, n_chinh, n_mc, bo_cu, giay):
    L = [f"# Độ đo tầng truy hồi — {time.strftime('%Y-%m-%d %H:%M')}", "",
         f"Sinh bằng `python -m eval.chay_truy_hoi`, **{giay:.0f} giây**. Số liệu thô: "
         f"`results/metrics_truy_hoi.csv`.", "",
         f"Bộ chính **{n_chinh} câu**, manh_con **{n_mc} câu**. τ = {cham.TAU}; Recall@W đếm cả "
         "tiền tố, lấy chunk nguyên; bootstrap ghép cặp 1000 lần, phân tầng theo nhóm câu hỏi.", "",
         "**Đây là độ đo TẦNG TRUY HỒI.** Độ chính xác trích dẫn chưa có — phần gán nhãn tay "
         "120 câu trả lời chưa xong.", ""]

    def bang_diem(bo, taps, pps, tieu="phương pháp"):
        out = [f"| {tieu} | n | " + " | ".join(DO_DO) + " |", "|---|---:|" + "---:|" * len(DO_DO)]
        for tap in taps:
            if len(taps) > 1:
                out.append(f"| *{tap}* | | " + " | " * (len(DO_DO) - 1) + " |")
            for pp in pps:
                r = {d["do_do"]: d for d in _lay(dong, loai_dong="diem", bo=bo, pp=pp, tap=tap)}
                if not r:
                    continue
                out.append(f"| {pp} | {r[DO_DO[0]]['n']} | "
                           + " | ".join(f"{r[d]['gia_tri']:.3f}" for d in DO_DO) + " |")
        return out

    def bang_hieu(bo, taps, cot):
        pps = sorted({d["pp"] for d in _lay(dong, loai_dong="hieu", bo=bo)})
        out = [f"| hiệu | tập | " + " | ".join(cot) + " |", "|---|---|" + "---|" * len(cot)]
        for pp in pps:
            for tap in taps:
                r = {d["do_do"]: d for d in _lay(dong, loai_dong="hieu", bo=bo, pp=pp, tap=tap)}
                if r:
                    out.append(f"| {pp} | {tap} | " + " | ".join(_o(r[c]) for c in cot) + " |")
        return out

    taps_chinh = [d["tap"] for d in _lay(dong, loai_dong="diem", bo="chinh", pp="B")]
    taps_chinh = list(dict.fromkeys(taps_chinh))
    L += ["## 1. Bộ chính — A, C, D, B", ""] + bang_diem("chinh", taps_chinh, ["A", "C", "D", "B"])
    L += ["", "### Hiệu số B − baseline (bootstrap ghép cặp 95%; **đậm** = CI không chứa 0)", ""]
    L += bang_hieu("chinh", taps_chinh, ["R@5", "R@1200t", "MRR"])

    taps_mc = list(dict.fromkeys(d["tap"] for d in _lay(dong, loai_dong="diem", bo="manh_con", pp="B")))
    L += ["", "## 2. manh_con — E so với B", ""]
    L += bang_diem("manh_con", taps_mc, [p for p, _ in PP_E], "cấu hình")
    L += ["", "### Hiệu số cấu hình − B (bootstrap ghép cặp 95%)", ""]
    L += bang_hieu("manh_con", taps_mc, ["R@5", "R@1200t", "MRR"])

    L += ["", "## 3. Tập con bản cũ — số câu có chunk BẢN CŨ trong top-k", "",
          "| tập con | n | phương pháp | top-5 | top-10 |", "|---|---:|---|---:|---:|"]
    for ten in bo_cu:
        for pp in ["A", "C", "D", "B"]:
            r5 = _lay(dong, loai_dong="ban_cu", bo=ten, pp=pp, tap="top-5")
            r10 = _lay(dong, loai_dong="ban_cu", bo=ten, pp=pp, tap="top-10")
            if r5:
                L.append(f"| {ten} | {r5[0]['n']} | {pp} | {r5[0]['gia_tri']} | {r10[0]['gia_tri']} |")
    L += ["", "`phien_ban`: bản cũ nằm trong bảng tương đương nên lấy về **không phải lỗi**. "
          "`ban_cu_nhieu`: bản cũ **ngoài** bảng tương đương — lấy về là nhiễu thật.", ""]
    MD_RA.write_text("\n".join(L) + "\n")


if __name__ == "__main__":
    main()
