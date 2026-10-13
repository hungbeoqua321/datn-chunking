#!/bin/bash
# Build llama.cpp (tag b11577) cho CPU aarch64 — chạy qua systemd-run để giới hạn CPU.
set -euo pipefail
cd "$(dirname "$0")/llama.cpp"
export PATH="$(dirname "$0")/../.venv-tools/bin:$PATH"
cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=Release -DGGML_NATIVE=ON -DLLAMA_OPENSSL=OFF \
  -DLLAMA_BUILD_TESTS=OFF -DLLAMA_BUILD_EXAMPLES=OFF -DLLAMA_USE_PREBUILT_UI=OFF
cmake --build build -j3 --target llama-server llama-bench llama-tokenize
