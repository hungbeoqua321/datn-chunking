#!/bin/bash
# Biến thể GPU của tools/chay-llm.sh cho máy cá nhân (RTX 2050, Windows, bản build CUDA b11577).
# Giữ nguyên mọi cờ của chay-llm.sh, chỉ khác: binary ở build-cuda/ và thêm -ngl 99 (đưa mọi lớp lên GPU).
# ĐÂY LÀ ĐỔI ĐIỀU KIỆN THỰC NGHIỆM: kết quả sinh không kỳ vọng khớp số cũ chạy CPU aarch64.
set -euo pipefail
GOC="$(cd "$(dirname "$0")/.." && pwd)"
MO_HINH="${MO_HINH:-$GOC/models/Qwen3-4B-Instruct-2507-Q4_0.gguf}"
exec "$GOC/tools/llama.cpp/build-cuda/bin/llama-server" \
  -m "$MO_HINH" --alias "$(basename "$MO_HINH" .gguf)" \
  --host 127.0.0.1 --port "${CONG:-8082}" \
  -t 3 -tb 3 -c 4096 -np 1 -b 512 -ub 512 --poll 0 \
  --no-webui --jinja -fa on --no-cache-prompt --seed 42 \
  -ngl 99
