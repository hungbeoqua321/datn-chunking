#!/bin/bash
# Sinh file site nginx từ mẫu với hostname lấy từ biến DATN_HOST (trong .env). Đổi domain = sửa một biến.
#   deploy/render.sh > /tmp/datn.conf
set -euo pipefail
cd "$(dirname "$0")/.."
DATN_HOST="${DATN_HOST:-$(grep -E '^DATN_HOST=' .env | cut -d= -f2-)}"
[ -n "$DATN_HOST" ] || { echo "thiếu DATN_HOST" >&2; exit 1; }
export DATN_HOST
envsubst '${DATN_HOST}' < deploy/nginx-datn.conf.mau
