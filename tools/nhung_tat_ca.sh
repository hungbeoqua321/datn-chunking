#!/bin/bash
# Nhúng mọi tệp chunk theo thứ tự ưu tiên (chỉ mục chính trước). Bộ đệm theo nội dung nên chạy lại sẽ tiếp tục.
# Chạy qua systemd-run để giới hạn CPU (không tranh với các site đang chạy):
#   sudo systemd-run --unit=datn-nhung --uid=ubuntu --gid=ubuntu -p WorkingDirectory=$PWD -p CPUWeight=1 \
#     -p AllowedCPUs=1-3 -p MemoryMax=8G -p Nice=19 tools/nhung_tat_ca.sh
set -euo pipefail
cd "$(dirname "$0")/.."
export SO_LUONG=3 OMP_NUM_THREADS=3 OMP_WAIT_POLICY=PASSIVE TOKENIZERS_PARALLELISM=false
# Một seed cho mọi tệp, trừ A trần (seed 1–3, chỉ đo truy hồi). D: nhúng từng câu → dựng chunk D → nhúng chunk D.
# Thứ tự có thể đổi bằng biến DS (vd. DS="B_s0 Btru_s0"); "D" = bước dựng D.
for t in ${DS:-A_s0 C_s0 Acong_s0 D A_s1 A_s2 A_s3 B_s0 Btru_s0 A_H_s0}; do
  if [ "$t" = D ]; then
    .venv/bin/python -u -m chunking.chay --chi D
    t=D_s0
  fi
  if ! .venv/bin/python -u -m rag.chi_muc "$t"; then
    rc=$?
    [ "$rc" = 3 ] && { echo "DỪNG: $t bị BỎ QUA — chỉ mục cũ còn nguyên. Chạy lại với --force."; exit 3; }
    echo "DỪNG: $t lỗi (mã $rc)"; exit "$rc"
  fi
done
.venv/bin/python -u -m rag.kiem_chi_muc || { echo "DỪNG: chỉ mục lệch tệp chunk"; exit 4; }
echo "XONG NHÚNG"
