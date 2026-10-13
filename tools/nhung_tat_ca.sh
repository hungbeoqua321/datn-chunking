#!/bin/bash
# Nhúng mọi tệp chunk theo thứ tự ưu tiên (chỉ mục chính trước). Bộ đệm theo nội dung nên chạy lại sẽ tiếp tục.
# Chạy qua systemd-run để giới hạn CPU (không tranh với các site đang chạy):
#   sudo systemd-run --unit=datn-nhung --uid=ubuntu --gid=ubuntu -p WorkingDirectory=$PWD -p CPUWeight=1 \
#     -p AllowedCPUs=1-3 -p MemoryMax=8G -p Nice=19 tools/nhung_tat_ca.sh
set -euo pipefail
cd "$(dirname "$0")/.."
export SO_LUONG=3 OMP_NUM_THREADS=3 OMP_WAIT_POLICY=PASSIVE TOKENIZERS_PARALLELISM=false
# B, B−, A+, A_H: nhúng một lần (seed 0). A trần: thêm seed 1–3, chỉ để đo truy hồi.
for t in A_s0 Acong_s0 B_s0 Btru_s0 A_H_s0 A_s1 A_s2 A_s3; do
  .venv/bin/python -u -m rag.chi_muc "$t"
done
echo "XONG NHÚNG"
