# Môi trường chạy thực nghiệm

- Máy: `aarch64`, CPU `Neoverse-N1`, 4 nhân, RAM 23 GB, không GPU
- Hệ điều hành: Ubuntu 22.04.5 LTS, glibc 2.35
- Python 3.12.13

## Thư viện

| Gói | Phiên bản |
|---|---|
| torch | 2.14.1+cpu |
| sentence-transformers | 6.1.0 |
| transformers | 5.19.0 |
| huggingface_hub | 1.33.0 |
| numpy | 2.5.4 |
| pandas | 3.0.6 |
| matplotlib | 3.11.2 |
| pyarrow | 26.0.0 |
| requests | 2.34.2 |
| beautifulsoup4 | 4.15.0 |
| lxml | 6.1.3 |
| openai | 3.29.0 |
| fastapi | 0.143.0 |
| uvicorn | 0.54.0 |
| markdown-it-py | 4.2.0 |
| pytest | 9.1.1 |

## Mô hình

- Nhúng: `contextboxai/halong_embedding` @ `b57776031035f70ed2030d2e35ecc533eb0f8f71` (trước đây `hiieu/halong_embedding`); model.safetensors sha256 `2fd083778d8b1f54d7ad106d1e279b5e0f6f2f9f71ae095cf91107b6e54131ab`
- Sinh: `unsloth/Qwen3-4B-Instruct-2507-GGUF` @ `a06e946bb6b655725eafa393f4a9745d460374c9`
  - `Qwen3-4B-Instruct-2507-Q4_0.gguf` sha256 `e0ba675d86ab277c61701c6793659b2ae801d95e3be791464c321e6fbf613be2`
  - `Qwen3-4B-Instruct-2507-Q4_K_M.gguf` sha256 `3605803b982cb64aead44f6c1b2ae36e3acdb41d8e46c8a94c6533bc4c67e597`
- llama.cpp: tag `b11577`, commit `cbe28bb3cb0758f0c566a9a3561766821aeb0748`, build `-DGGML_NATIVE=ON` (tools/build-llama.sh)
- Cờ llama-server: `-m "$MO_HINH" --alias "$(basename "$MO_HINH" .gguf)" --host 127.0.0.1 --port "${CONG:-8082}" -t 3 -tb 3 -c 4096 -np 1 -b 512 -ub 512 --poll 0 --no-webui --jinja -fa on --no-cache-prompt --seed 42`
