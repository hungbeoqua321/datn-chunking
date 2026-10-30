#!/bin/bash
# Bước 0 trên máy local: dựng lại TOÀN BỘ chunk + nhúng lại TOÀN BỘ trên GPU vào thư mục riêng, rồi chạy lại truy hồi.
# Không đụng data/chunks, data/index, results/ (bản VPS). Bộ đệm vector mới tinh → mọi vector đều tính trên GPU,
# kể cả cụm câu dùng để cắt D và tầng semantic của E.
#   thuc_nghiem/tai_lap_gpu/chay.sh 2>&1 | tee thuc_nghiem/tai_lap_gpu/nhat_ky.txt
set -uo pipefail
cd "$(dirname "$0")/../.."
export PYTHONUTF8=1 NHUNG_DEVICE=cuda TOKENIZERS_PARALLELISM=false
export CHUNKS_DIR=thuc_nghiem/tai_lap_gpu/chunks INDEX_DIR=thuc_nghiem/tai_lap_gpu/index KET_QUA_DIR=thuc_nghiem/tai_lap_gpu
PY=.venv/Scripts/python.exe
[ -x "$PY" ] || PY=.venv/bin/python
buoc() { echo "== $1 $(date +%T)"; T0=$(date +%s); }
xong() { echo "== $1 xong: $(( $(date +%s) - T0 )) s"; }

buoc CHUNK; $PY -u -m chunking.chay || { echo "DỪNG: dựng chunk lỗi"; exit 1; }; xong CHUNK
buoc VAN; $PY tools/so_van_chunk.py "$CHUNKS_DIR" --ra thuc_nghiem/tai_lap_gpu/van_chunk.md; echo "van exit=$?"; xong VAN
DS="A_s0 A_s1 A_s2 A_s3 Acong_s0 A_H_s0 B_s0 Btru_s0 C_s0 D_s0 Eduoi_s0 Etren_s0 Etat_d_s0 Etat_k_s0 Etat_n_s0 Etat_s_s0 Echi_s_s0"
for t in $DS; do
  buoc "NHUNG $t"; $PY -u -m rag.chi_muc "$t" 2>&1 | grep -v "Loading weights"; rc=${PIPESTATUS[0]}
  [ "$rc" = 3 ] && { echo "DỪNG: $t bị BỎ QUA (mã 3) — thư mục mới không được có chỉ mục cũ"; exit 3; }
  [ "$rc" = 0 ] || { echo "DỪNG: $t lỗi (mã $rc)"; exit "$rc"; }
  xong "NHUNG $t"
done
buoc KIEM; $PY -m rag.kiem_chi_muc || { echo "DỪNG: chốt chặn chỉ mục lệch"; exit 4; }; xong KIEM
buoc TRUY_HOI; $PY -m eval.chay_truy_hoi 2>&1 | grep -v "Loading weights" | tail -20; echo "truy_hoi exit=${PIPESTATUS[0]}"; xong TRUY_HOI
echo "BUOC0_XONG"
