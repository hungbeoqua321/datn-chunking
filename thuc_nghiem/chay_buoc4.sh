#!/bin/bash
# Bước 4 trên máy local: chạy một lệnh sinh, tự khởi động lại llama-server nếu server chết giữa chừng.
# Lệnh sinh ghi tiếp được (bỏ qua lượt đã có) nên chạy lại là an toàn — sinh trên GPU tất định.
# CHỐT GPU: sau khi server lên, VRAM đang dùng phải ≥ NGUONG_VRAM MiB; không đạt (GPU biến mất, server rơi về CPU)
# thì DỪNG hẳn, không sinh — câu trả lời sinh trên CPU khác GPU, không được trộn vào bộ số.
#
#   SERVER="bash tools/chay-llm-gpu.sh" NGUONG_VRAM=2500 bash thuc_nghiem/chay_buoc4.sh <nhãn> <lệnh sinh…>
set -u
cd "$(dirname "$0")/.."
NHAN="$1"; shift
SERVER="${SERVER:-bash tools/chay-llm-gpu.sh}"
NGUONG_VRAM="${NGUONG_VRAM:-2500}"
LAN_TOI_DA="${LAN_TOI_DA:-20}"
LOG="results/local_gpu/thu_them/giam_sat_${NHAN}.txt"
export PYTHONUTF8=1 CHUNKS_DIR=thuc_nghiem/tai_lap_gpu/chunks INDEX_DIR=thuc_nghiem/tai_lap_gpu/index NHUNG_DEVICE=cpu
export KET_QUA_DIR="${KET_QUA_DIR:-results/local_gpu}"
ghi() { echo "$(date '+%F %T') $*" | tee -a "$LOG"; }
tat_server() { taskkill //F //IM llama-server.exe > /dev/null 2>&1; sleep 3; }

for lan in $(seq 1 "$LAN_TOI_DA"); do
  tat_server
  $SERVER > "thuc_nghiem/llm_${NHAN}.log" 2>&1 &
  for _ in $(seq 1 150); do curl -s -m 2 localhost:8082/health | grep -q ok && break; sleep 2; done
  if ! curl -s -m 2 localhost:8082/health | grep -q ok; then ghi "lần $lan: server không lên — DỪNG"; tat_server; exit 3; fi
  vram=$(nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits 2>/dev/null | head -1)
  if [ -z "$vram" ] || [ "$vram" -lt "$NGUONG_VRAM" ]; then
    ghi "lần $lan: VRAM đang dùng '${vram}' MiB < $NGUONG_VRAM — server KHÔNG chạy trên GPU — DỪNG, không sinh"; tat_server; exit 4
  fi
  ghi "lần $lan: server lên, VRAM ${vram} MiB"
  .venv/Scripts/python.exe -m rag.kiem_chi_muc > /dev/null || { ghi "chốt chặn chỉ mục LỆCH — DỪNG"; tat_server; exit 1; }
  s=$(date +%s)
  "$@" >> "results/local_gpu/thu_them/nhat_ky_${NHAN}.txt" 2>&1
  ma=$?
  ghi "lần $lan: lệnh sinh thoát $ma sau $(( $(date +%s) - s )) s"
  if [ "$ma" -eq 0 ]; then tat_server; ghi "XONG"; exit 0; fi
  sleep 10
done
ghi "quá $LAN_TOI_DA lần — DỪNG"; tat_server; exit 5
