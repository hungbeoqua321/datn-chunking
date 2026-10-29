"""Sinh câu trả lời cho E3 — E2 cộng theo dẫn chiếu tường minh một bước (rag/dan_chieu.py).

    python -m eval.chay_e3              # sinh, ghi tiếp được
    python -m eval.chay_e3 --kiem       # chỉ đếm việc còn lại

Hai bộ:
  * bộ chính — chỉ **26 câu** thuộc hai nhóm có dẫn chiếu thật: `dan_chieu` (9) và
    `xuyen_khoan` (17). Ghi vào results/pilot_tra_loi.jsonl với pp = "E3".
  * manh_con — cả **35 câu**. Ghi vào results/manh_con_tra_loi.jsonl với cau_hinh = "E3".

Tham số sinh khoá theo cau_hinh, giống hệt mọi đợt trước. Ca chạm trần MAX_TOKENS ghi thành
hạng mục "cắt trần" (eval/ket_qua.py), vẫn nằm trong mẫu.
"""
import argparse
import collections
import json
import time

import cau_hinh as ch
from eval import ket_qua  # noqa: F401  (giữ cho rõ hạng mục dùng chung)
from rag import dan_chieu, sinh, truy_hoi
from rag.kiem_chi_muc import chot_chan
from rag.sinh import LoiCat

NHOM_E3 = ("dan_chieu", "xuyen_khoan")
# E3b chỉ chạy bộ chính; manh_con hầu như không có dẫn chiếu nên không chạy (19/35 câu của E3
# không kéo được đơn vị đích nào).
CHI_BO_CHINH = ("E3b",)
BO = [("chinh", ch.GOC / "eval/questions.jsonl", ch.RESULTS / "pilot_tra_loi.jsonl", "pp"),
      ("manh_con", ch.GOC / "eval/manh_con.draft.jsonl",
       ch.RESULTS / "manh_con_tra_loi.jsonl", "cau_hinh")]


def _nap(p, khoa):
    ds = [json.loads(l) for l in open(p) if l.strip()] if p.exists() else []
    return ds, {(y["qid"], y[khoa]) for y in ds if y.get("tra_loi") or y.get("cat_tran")}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--kiem", action="store_true")
    ap.add_argument("--pp", default="E3", help="E3 hoặc E3b")
    a = ap.parse_args()
    PP = a.pp
    viec = []
    for ten, p_hoi, p_tra, khoa in BO:
        if PP in CHI_BO_CHINH and ten != "chinh":
            continue
        hoi = [json.loads(l) for l in open(p_hoi) if l.strip()]
        if ten == "chinh":
            hoi = [x for x in hoi if x["loai"] in NHOM_E3]
        _, xong = _nap(p_tra, khoa)
        thieu = [x for x in hoi if (x["qid"], PP) not in xong]
        print(f"{ten}: {len(hoi)} câu | đã có {len(hoi)-len(thieu)} | còn {len(thieu)}", flush=True)
        viec += [(ten, p_tra, khoa, x) for x in thieu]
    if a.kiem or not viec:
        return
    chot_chan([truy_hoi.TEP[PP]])
    cl = sinh.client()
    t0, cat = time.monotonic(), []
    for i, (ten, p_tra, khoa, x) in enumerate(viec, 1):
        ds, _ = _nap(p_tra, khoa)
        qv = truy_hoi.nhung_cau_hoi(x["question"])
        kq = truy_hoi.tim(PP, qv, k=ch.K_UNG_VIEN)
        khoi = truy_hoi.ngu_canh(PP, kq, ngan_sach=ch.NGAN_SACH_NGU_CANH_TU, k=ch.K_UNG_VIEN)
        loi_cat = ""
        try:
            r = sinh.tra_loi(x["question"], khoi, cl,
                             {"qid": x["qid"], "bien_the": PP, "seed": 0})
        except LoiCat as e:
            loi_cat, r = str(e), {"tra_loi": ""}
            cat.append((ten, x["qid"]))
        ds.append({"qid": x["qid"], khoa: PP, "loai": x["loai"],
                   "trung_lap": bool(x.get("trung_lap")), "question": x["question"],
                   "gold": x["gold"], "tra_loi": r["tra_loi"],
                   "cat_tran": bool(loi_cat), "ly_do_cat": loi_cat,
                   "so_khoi": len(khoi), "so_don_vi_dich": sum(1 for b in khoi if b.get("dan_chieu")),
                   "so_tu_ngu_canh": sum(len(b["text"].split()) for b in khoi),
                   "chunk_id": [b["chunk_id"] for b in khoi]})
        p_tra.write_text("\n".join(json.dumps(y, ensure_ascii=False) for y in ds) + "\n")
        print(f"  [{i}/{len(viec)}] {ten} {x['qid']}  "
              f"{(time.monotonic()-t0)/i:.0f}s/câu" + ("  ← CẮT TRẦN" if loi_cat else ""), flush=True)
    print(f"→ xong. Cắt trần: {len(cat)} {cat}", flush=True)
    print("THỐNG KÊ DẪN CHIẾU: " + json.dumps(dict(sorted(dan_chieu.THONG_KE.items())),
                                              ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
