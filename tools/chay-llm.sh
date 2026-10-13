#!/bin/bash
# Chạy llama-server (endpoint tương thích OpenAI) cho mô hình sinh.
# Các cờ được ghim để kết quả tái lập được: 1 slot (không gộp lô), không cache prompt,
# số luồng / kích thước lô cố định. Đổi cờ = đổi thực nghiệm.
set -euo pipefail
GOC="$(cd "$(dirname "$0")/.." && pwd)"
MO_HINH="${MO_HINH:-$GOC/models/Qwen3-4B-Instruct-2507-Q4_0.gguf}"
exec "$GOC/tools/llama.cpp/build/bin/llama-server" \
  -m "$MO_HINH" --alias "$(basename "$MO_HINH" .gguf)" \
  --host 127.0.0.1 --port "${CONG:-8082}" \
  -t 3 -tb 3 -c 4096 -np 1 -b 512 -ub 512 --poll 0 \
  --no-webui --jinja -fa on --no-cache-prompt --seed 42
