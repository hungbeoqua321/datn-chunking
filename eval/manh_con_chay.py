"""Sinh câu trả lời cho bộ `manh_con` trên 8 cấu hình — đo đóng góp từng thành phần của E.

Bộ `manh_con` là bộ câu hỏi nhắm thẳng vào mảnh con: câu trả lời nằm ở một mảnh bị tách ra
khỏi đơn vị pháp lý cha, nên mất câu dẫn. Đó đúng là chỗ E định bù.

Tám cấu hình, theo đúng thứ tự người duyệt chốt:

  1. B        — đối chứng, không có thành phần nào của E
  2. Eduoi    — E đầy đủ, câu bản lề thuộc mảnh dưới
  3. Etren    — E đầy đủ, câu bản lề thuộc mảnh trên
  4. Etat_d   — E đầy đủ TRỪ dẫn Điều
  5. Etat_k   — E đầy đủ TRỪ dẫn khoản
  6. Etat_n   — E đầy đủ TRỪ nhãn mảnh
  7. Etat_s   — E đầy đủ TRỪ semantic (tầng cuối quay về cửa sổ cố định như B)
  8. Echi_s   — CHỈ semantic, không bù ngữ cảnh

Cấu hình 4–8 đều dùng bản lề "duoi" để mỗi dòng chỉ lệch E đầy đủ đúng MỘT biến.

Đây là phép cắt bỏ (ablation) kiểu BỎ-MỘT: chênh lệch giữa "E đầy đủ" và "E tắt X" là đóng góp
của X *khi đã có các thành phần kia*. Khác với kiểu BẬT-MỘT (chỉ X, tắt hết còn lại), vốn đo
đóng góp của X *khi đứng một mình*. Hai cách trả lời hai câu hỏi khác nhau; dòng 8 giữ lại một
điểm kiểu BẬT-MỘT cho riêng semantic.

    python -m eval.manh_con_chay           # sinh, ghi tiếp được
    python -m eval.manh_con_chay --kiem    # chỉ in việc còn phải làm rồi thoát

Tham số sinh khoá theo cau_hinh, giống hệt pilot: ngân sách 1200 từ, K_UNG_VIEN 50, MAX_TOKENS 384.
"""
import argparse
import collections
import json
import time

import cau_hinh as ch
from rag import sinh, truy_hoi
from rag.kiem_chi_muc import chot_chan
from rag.sinh import LoiCat

CAU_HOI = ch.GOC / "eval/manh_con.draft.jsonl"
TRA_LOI = ch.RESULTS / "manh_con_tra_loi.jsonl"
BI_CAT = ch.RESULTS / "manh_con_bi_cat.jsonl"

# (tên cấu hình, tên chỉ mục) — thứ tự này là thứ tự chạy và thứ tự lên bảng.
CAU_HINH: list[tuple[str, str]] = [
    ("B",      "B_s0"),
    ("Eduoi",  "Eduoi_s0"),
    ("Etren",  "Etren_s0"),
    ("Etat_d", "Etat_d_s0"),
    ("Etat_k", "Etat_k_s0"),
    ("Etat_n", "Etat_n_s0"),
    ("Etat_s", "Etat_s_s0"),
    ("Echi_s", "Echi_s_s0"),
    # E2 — bản E sửa theo kết quả truy hồi 22/10: truy hồi trên chỉ mục "chỉ semantic" (không
    # nhúng gì mới), bù ngữ cảnh ở TẦNG SINH bằng cách mở rộng lên Điều cha như B+.
    ("E2", "E2"),
    ("B+", "B+"),          # đối chứng cho E2: cùng cách dựng ngữ cảnh, khác chỉ mục truy hồi
]


def _da_co() -> dict[tuple[str, str], dict]:
    if not TRA_LOI.exists():
        return {}
    return {(y["qid"], y["cau_hinh"]): y
            for y in map(json.loads, TRA_LOI.read_text().splitlines())
            if y.get("tra_loi") or y.get("cat_tran")}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--kiem", action="store_true", help="chỉ đếm việc còn lại, không sinh")
    a = ap.parse_args()

    ds = [json.loads(l) for l in open(CAU_HOI) if l.strip()]
    xong = _da_co()
    tong = len(ds) * len(CAU_HINH)
    thieu = [(x, ten, idx) for x in ds for ten, idx in CAU_HINH if (x["qid"], ten) not in xong]
    print(f"bộ manh_con: {len(ds)} câu × {len(CAU_HINH)} cấu hình = {tong} lượt", flush=True)
    print(f"  đã có {len(xong)} | còn thiếu {len(thieu)}", flush=True)
    if xong:
        print("  đã có theo cấu hình: " +
              str(dict(collections.Counter(k[1] for k in xong))), flush=True)
    if a.kiem or not thieu:
        return

    # E2 và B+ không có tệp chunk riêng — chúng dùng chỉ mục của phương pháp khác, dịch qua
    # truy_hoi.TEP trước khi đưa cho chốt chặn, nếu không chốt chặn đi tìm "E2.jsonl".
    chot_chan(sorted({truy_hoi.TEP.get(idx, idx) for _, idx in CAU_HINH}))
    cl = sinh.client()
    ra = list(xong.values())
    t0 = time.monotonic()
    lam = 0
    cat: list[tuple[str, str]] = []
    vec: dict[str, object] = {}
    for x, ten, idx in thieu:
        if x["qid"] not in vec:
            vec.clear()                          # chỉ giữ vector của câu đang chạy
            vec[x["qid"]] = truy_hoi.nhung_cau_hoi(x["question"])
        kq = truy_hoi.tim(idx, vec[x["qid"]], k=ch.K_UNG_VIEN)
        khoi = truy_hoi.ngu_canh(idx, kq, ngan_sach=ch.NGAN_SACH_NGU_CANH_TU, k=ch.K_UNG_VIEN)
        try:
            r = sinh.tra_loi(x["question"], khoi, cl,
                             {"qid": x["qid"], "bien_the": f"manh_con_{ten}", "seed": 0})
        except LoiCat as e:
            # Chạm trần MAX_TOKENS → câu trả lời DỞ DANG. KHÔNG hạ trần, KHÔNG loại khỏi mẫu:
            # ghi thành hạng mục "cắt trần" (eval/ket_qua.py), vẫn tính là ĐÃ LÀM nên cặp này
            # có mặt trong mẫu số của mọi bảng. Ghi thêm một dòng vào BI_CAT để tra cứu nhanh.
            with open(BI_CAT, "a") as f:
                f.write(json.dumps({"qid": x["qid"], "cau_hinh": ten, "chi_muc": idx,
                                    "loi": str(e)}, ensure_ascii=False) + "\n")
            cat.append((x["qid"], ten))
            loi_cat = str(e)
            r = {"tra_loi": ""}
        else:
            loi_cat = ""
        ra.append({"qid": x["qid"], "cau_hinh": ten, "chi_muc": idx, "loai": x["loai"],
                   "trung_lap": bool(x.get("trung_lap")), "question": x["question"],
                   "gold": x["gold"], "tra_loi": r["tra_loi"],
                   "cat_tran": bool(loi_cat), "ly_do_cat": loi_cat, "so_khoi": len(khoi),
                   "so_tu_ngu_canh": sum(len(k["text"].split()) for k in khoi),
                   "chunk_id": [k["chunk_id"] for k in khoi]})
        TRA_LOI.write_text("\n".join(json.dumps(y, ensure_ascii=False) for y in ra) + "\n")
        lam += 1
        dt = time.monotonic() - t0
        print(f"  [{lam}/{len(thieu)}] {x['qid']} {ten}  {dt / lam:.0f}s/câu"
              + ("  ← CẮT TRẦN" if loi_cat else ""), flush=True)
    print(f"→ {TRA_LOI} ({len(ra)} câu trả lời)", flush=True)
    if cat:
        print(f"CẮT TRẦN, ghi thành hạng mục riêng, VẪN trong mẫu ({len(cat)}): "
              + ", ".join(f"{q}/{c}" for q, c in cat), flush=True)
        print(f"   chi tiết: {BI_CAT}", flush=True)


if __name__ == "__main__":
    main()
