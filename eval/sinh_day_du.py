"""Sinh câu trả lời cho MỌI phương pháp — lượt chạy trên máy local có GPU.

Trên VPS chỉ sinh A, B, B+ (bộ chính), E3 (26 câu dẫn chiếu) và manh_con; C và D chỉ đo truy hồi.
Ở đây sinh hết, cấu hình khoá theo cau_hinh y hệt VPS: ngân sách 1200 từ, K_UNG_VIEN 50,
MAX_TOKENS 384, nhiệt độ 0, cùng lời nhắc (rag/sinh.py).

  bộ chính  110 câu × A, C, D, B, B+, E, E2, E3                         = 880 lượt → pilot_tra_loi.jsonl (khoá "pp")
  manh_con   35 câu × B, B+, Eduoi, Etren, Etat_d/k/n/s, Echi_s, E2, E3 = 420 lượt → manh_con_tra_loi.jsonl (khoá "cau_hinh")

Định dạng dòng giống hệt eval/pilot.py, eval/manh_con_chay.py, eval/chay_e3.py nên eval/ket_qua.py và
eval/cham_trich_dan.py chấm thẳng được. Ghi vào ch.RESULTS — chạy với KET_QUA_DIR=results/local_gpu để
không đụng số VPS trong results/. Ghi tiếp được: cặp (qid, phương pháp) đã có thì bỏ qua. Chạm trần
MAX_TOKENS → hạng mục "cắt trần", vẫn trong mẫu.

    python -m eval.sinh_day_du --kiem          # đếm việc còn lại
    python -m eval.sinh_day_du                 # cả hai bộ
    python -m eval.sinh_day_du --bo chinh --pp A B
"""
import argparse
import collections
import json
import time

import cau_hinh as ch
from rag import sinh, truy_hoi
from rag.kiem_chi_muc import chot_chan
from rag.sinh import LoiCat

# phương pháp → chỉ mục truy hồi. "E" ở bộ chính là E đầy đủ (Eduoi), như cấu hình 2 của manh_con.
PP_CHINH = {"A": "A", "C": "C", "D": "D", "B": "B", "B+": "B+", "E": "Eduoi_s0", "E2": "E2", "E3": "E3"}
PP_MANH_CON = {"B": "B_s0", "B+": "B+", "Eduoi": "Eduoi_s0", "Etren": "Etren_s0", "Etat_d": "Etat_d_s0",
               "Etat_k": "Etat_k_s0", "Etat_n": "Etat_n_s0", "Etat_s": "Etat_s_s0", "Echi_s": "Echi_s_s0",
               "E2": "E2", "E3": "E3"}
BO = {"chinh": (ch.GOC / "eval/questions.jsonl", "pilot_tra_loi.jsonl", "pp", PP_CHINH),
      "manh_con": (ch.GOC / "eval/manh_con.draft.jsonl", "manh_con_tra_loi.jsonl", "cau_hinh", PP_MANH_CON)}


def _nap(p, khoa):
    ds = [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()] if p.exists() else []
    return ds, {(y["qid"], y[khoa]) for y in ds if y.get("tra_loi") or y.get("cat_tran")}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--kiem", action="store_true")
    ap.add_argument("--bo", nargs="*", choices=list(BO), default=list(BO))
    ap.add_argument("--pp", nargs="*", help="chỉ các phương pháp này")
    ap.add_argument("--toi-da", type=int, help="dừng sau N lượt (đo nhịp)")
    a = ap.parse_args()

    viec = []
    for ten in a.bo:
        p_hoi, tep, khoa, pps = BO[ten]
        hoi = sorted((json.loads(l) for l in open(p_hoi, encoding="utf-8") if l.strip()), key=lambda x: x["qid"])
        _, xong = _nap(ch.RESULTS / tep, khoa)
        chon = [p for p in pps if not a.pp or p in a.pp]
        thieu = [(ten, x, p) for x in hoi for p in chon if (x["qid"], p) not in xong]
        print(f"{ten}: {len(hoi)} câu × {len(chon)} = {len(hoi) * len(chon)} lượt | đã có "
              f"{len(hoi) * len(chon) - len(thieu)} | còn {len(thieu)}", flush=True)
        viec += thieu
    if a.toi_da:
        viec = viec[:a.toi_da]
    if a.kiem or not viec:
        return

    chot_chan(sorted({truy_hoi.TEP.get(BO[t][3][p], BO[t][3][p]) for t, _, p in viec}))
    cl = sinh.client()
    ch.RESULTS.mkdir(parents=True, exist_ok=True)
    t0, cat, theo_dot = time.monotonic(), [], collections.defaultdict(float)
    vec: dict[str, object] = {}
    for i, (ten, x, pp) in enumerate(viec, 1):
        _, tep, khoa, pps = BO[ten]
        p_tra = ch.RESULTS / tep
        ds, _ = _nap(p_tra, khoa)
        if x["question"] not in vec:
            vec.clear()
            vec[x["question"]] = truy_hoi.nhung_cau_hoi(x["question"])
        idx = pps[pp]
        kq = truy_hoi.tim(idx, vec[x["question"]], k=ch.K_UNG_VIEN)
        khoi = truy_hoi.ngu_canh(idx, kq, ngan_sach=ch.NGAN_SACH_NGU_CANH_TU, k=ch.K_UNG_VIEN)
        t1, loi_cat = time.monotonic(), ""
        bien_the = f"local_{pp}" if ten == "chinh" else f"local_manh_con_{pp}"
        try:
            r = sinh.tra_loi(x["question"], khoi, cl, {"qid": x["qid"], "bien_the": bien_the, "seed": 0})
        except LoiCat as e:
            loi_cat, r = str(e), {"tra_loi": ""}
            cat.append((ten, x["qid"], pp))
        theo_dot[(ten, pp)] += time.monotonic() - t1
        dong = {"qid": x["qid"], khoa: pp, "loai": x["loai"], "trung_lap": bool(x.get("trung_lap")),
                "question": x["question"], "gold": x["gold"], "tra_loi": r["tra_loi"],
                "cat_tran": bool(loi_cat), "ly_do_cat": loi_cat, "so_khoi": len(khoi),
                "so_tu_ngu_canh": sum(len(b["text"].split()) for b in khoi),
                "chunk_id": [b["chunk_id"] for b in khoi]}
        if ten == "manh_con":
            dong["chi_muc"] = idx
        if pp in ("E3", "E3b"):
            dong["so_don_vi_dich"] = sum(1 for b in khoi if b.get("dan_chieu"))
        ds.append(dong)
        p_tra.write_text("\n".join(json.dumps(y, ensure_ascii=False) for y in ds) + "\n", encoding="utf-8")
        print(f"  [{i}/{len(viec)}] {ten} {x['qid']} {pp}  {time.monotonic() - t1:.1f}s "
              f"(tb {(time.monotonic() - t0) / i:.1f}s)" + ("  ← CẮT TRẦN" if loi_cat else ""), flush=True)
    print(f"→ xong {len(viec)} lượt trong {time.monotonic() - t0:.0f}s. Cắt trần: {len(cat)} {cat}", flush=True)
    print("thời gian sinh theo đợt (s): " + json.dumps({f"{t}/{p}": round(s) for (t, p), s in theo_dot.items()},
                                                      ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
