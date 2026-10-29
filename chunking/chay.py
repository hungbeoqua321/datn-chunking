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
from chunking import fixed, hybrid, semantic, sentence, structural
from chunking.base import ghi_jsonl, nap_van_ban
from chunking.hybrid import CongTac

PHUONG_PHAP = {
    "A": (fixed.chunk, (0,) + ch.SEEDS),            # 4 seed: đo truy hồi
    "A+": (fixed.chunk_a_cong, (0,)),
    "B": (structural.chunk, (0,) + ch.SEEDS),       # 4 seed chỉ để đếm; nhúng seed 0
    "A_H": (structural.chunk_ah, (0,)),
    "B-": (structural.chunk_b_tru, (0,)),
    "C": (sentence.chunk, (0,)),
    "D": (semantic.chunk, (0,)),
}

# Phương pháp E và bộ cắt bỏ thành phần (ablation). Tên tệp nói rõ thành phần nào BỊ TẮT,
# vì đó là thứ phép đo muốn tách: chênh lệch so với "E đầy đủ" là đóng góp của thành phần đó.
# Cả bộ cắt bỏ dùng biến thể bản lề "duoi" để chỉ còn đúng một biến thay đổi.
PHUONG_PHAP_E = {
    "Eduoi":  CongTac(True, True, True, True, "duoi"),      # E đầy đủ, câu bản lề thuộc mảnh dưới
    "Etren":  CongTac(True, True, True, True, "tren"),      # E đầy đủ, câu bản lề thuộc mảnh trên
    "Etat_d": CongTac(False, True, True, True, "duoi"),     # tắt dẫn Điều
    "Etat_k": CongTac(True, False, True, True, "duoi"),     # tắt dẫn khoản
    "Etat_n": CongTac(True, True, False, True, "duoi"),     # tắt nhãn mảnh
    "Etat_s": CongTac(True, True, True, False, "duoi"),     # tắt semantic → tầng cuối là cửa sổ như B
    "Echi_s": CongTac(False, False, False, True, "duoi"),   # chỉ semantic, không bù ngữ cảnh
}


def ten_tep(pp: str, seed: int):
    return ch.CHUNKS / f"{pp.replace('+', 'cong').replace('-', 'tru')}_s{seed}.jsonl"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--chi", nargs="*", metavar="PP",
                    help="chỉ dựng các phương pháp này (A, A+, B, A_H, B-, C, D, hoặc tên cấu hình E)")
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

    can_e = [t for t in PHUONG_PHAP_E if not a.chi or t in a.chi]
    can_e = [t for t in can_e if a.force or not (ch.CHUNKS / f"{t}_s0.jsonl").exists()]
    if can_e:
        hybrid.chuan_bi(docs)          # nhúng cụm câu của các đơn vị tầng cuối (dùng bộ đệm nội dung)
    for t in can_e:
        cs = [c for d in docs for c in hybrid.chunk(d, 0, PHUONG_PHAP_E[t])]
        ghi_jsonl(ch.CHUNKS / f"{t}_s0.jsonl", cs)
        print(f"{t}_s0.jsonl: {len(cs)} chunk")


if __name__ == "__main__":
    main()
