#!/bin/bash
# Bản sao tools/chay-llm-gpu.sh cho bước 4 (thử thêm, results/local_gpu/thu_them.md). Cờ y hệt, chỉ hai chỗ chỉnh qua biến:
#   CTX  (mặc định 4096) — 8192 cho quét ngân sách 2.400 từ (≈ 3.500 token ngữ cảnh + 384 trả lời vượt 4096)
#   NGL  (mặc định 99)   — số lớp đưa lên GPU; NGL=fit bỏ hẳn -ngl để llama.cpp (--fit, mặc định bật) tự chia lớp
#                          GPU/CPU vừa VRAM — dùng cho Qwen3-8B Q4_K_M (4,7 GB), không vừa 4 GB
# MO_HINH chọn tệp GGUF như chay-llm-gpu.sh. tools/chay-llm.sh và chay-llm-gpu.sh KHÔNG đổi.
set -euo pipefail
GOC="$(cd "$(dirname "$0")/.." && pwd)"
MO_HINH="${MO_HINH:-$GOC/models/Qwen3-4B-Instruct-2507-Q4_0.gguf}"
exec "$GOC/tools/llama.cpp/build-cuda/bin/llama-server" \
  -m "$MO_HINH" --alias "$(basename "$MO_HINH" .gguf)" \
  --host 127.0.0.1 --port "${CONG:-8082}" \
  -t 3 -tb 3 -c "${CTX:-4096}" -np 1 -b 512 -ub 512 --poll 0 \
  --no-webui --jinja -fa on --no-cache-prompt --seed 42 \
  $( [ "${NGL:-99}" = fit ] || echo -ngl "${NGL:-99}" )
