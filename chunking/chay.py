"""Dựng chunk cho mọi phương pháp → data/chunks/<pp>_s<seed>.jsonl

  A       seed 0 (đúng đề: cửa sổ từ từ đầu tiên) + seed 1, 2, 3 (độ lệch cố định mỗi văn bản) — chỉ đo truy hồi
  B       seed 0..3 chỉ để đếm (seed chỉ ảnh hưởng cửa sổ fallback của văn bản không có Điều); nhúng seed 0
  C, D    seed 0 — hai baseline của đề cương: theo dấu câu, theo ngữ nghĩa
  A+, A_H, B− seed 0 — đối chứng, chỉ đo truy hồi
  B+ không có file riêng: dùng chunk của B, mở rộng lên Điều cha lúc sinh.

    python -m chunking.chay              # bỏ qua file đã có
    python -m chunking.chay --chi C D    # chỉ các phương pháp này
    python -m chunking.chay --force

D phải nhúng từng câu trước (nặng: chạy qua systemd-run như khi nhúng chunk, xem tools/nhung_tat_ca.sh).
"""
import argparse

import cau_hinh as ch
from chunking import fixed, semantic, sentence, structural
from chunking.base import ghi_jsonl, nap_van_ban

PHUONG_PHAP = {
    "A": (fixed.chunk, (0,) + ch.SEEDS),            # 4 seed: đo truy hồi
    "A+": (fixed.chunk_a_cong, (0,)),
    "B": (structural.chunk, (0,) + ch.SEEDS),       # 4 seed chỉ để đếm; nhúng seed 0
    "A_H": (structural.chunk_ah, (0,)),
    "B-": (structural.chunk_b_tru, (0,)),
    "C": (sentence.chunk, (0,)),
    "D": (semantic.chunk, (0,)),
}


def ten_tep(pp: str, seed: int):
    return ch.CHUNKS / f"{pp.replace('+', 'cong').replace('-', 'tru')}_s{seed}.jsonl"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--chi", nargs="*", metavar="PP", help="chỉ dựng các phương pháp này (A, A+, B, A_H, B-, C, D)")
    a = ap.parse_args()
    docs = nap_van_ban()
    for pp, (ham, seeds) in PHUONG_PHAP.items():
        if a.chi and pp not in a.chi:
            continue
        if pp == "D" and (a.force or not all(ten_tep(pp, s).exists() for s in seeds)):
            semantic.chuan_bi(docs)
        for s in seeds:
            p = ten_tep(pp, s)
            if p.exists() and not a.force:
                print("có rồi:", p.name)
                continue
            cs = [c for d in docs for c in ham(d, s)]
            ghi_jsonl(p, cs)
            print(f"{p.name}: {len(cs)} chunk")


if __name__ == "__main__":
    main()
