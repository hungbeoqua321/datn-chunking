"""Dựng chunk cho mọi phương pháp → data/chunks/<pp>_s<seed>.jsonl

  A, A+   seed 0 (đúng đề: cửa sổ từ từ đầu tiên) + seed 1, 2, 3 (độ lệch ngẫu nhiên cố định mỗi văn bản)
  B       seed 0..3 (seed chỉ ảnh hưởng cửa sổ fallback của văn bản không có Điều)
  A_H, B− seed 0 (đối chứng 2×2, chỉ đo truy hồi)
  B+ không có file riêng: dùng chunk của B, mở rộng lên Điều cha lúc sinh.

    python -m chunking.chay            # bỏ qua file đã có
    python -m chunking.chay --force
"""
import argparse

import cau_hinh as ch
from chunking import fixed, structural
from chunking.base import ghi_jsonl, nap_van_ban

PHUONG_PHAP = {
    "A": (fixed.chunk, (0,) + ch.SEEDS),
    "A+": (fixed.chunk_a_cong, (0,) + ch.SEEDS),
    "B": (structural.chunk, (0,) + ch.SEEDS),
    "A_H": (structural.chunk_ah, (0,)),
    "B-": (structural.chunk_b_tru, (0,)),
}


def ten_tep(pp: str, seed: int):
    return ch.CHUNKS / f"{pp.replace('+', 'cong').replace('-', 'tru')}_s{seed}.jsonl"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    docs = nap_van_ban()
    for pp, (ham, seeds) in PHUONG_PHAP.items():
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
