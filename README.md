# Thực nghiệm phân đoạn văn bản quy phạm pháp luật cho RAG

Đồ án tốt nghiệp: **"Nghiên cứu phương pháp phân đoạn văn bản quy phạm pháp luật cho bài toán RAG"**.

Câu hỏi cần trả lời bằng số liệu: phân đoạn bám cấu trúc pháp lý (Điều → Khoản → Điểm) có cho kết quả hỏi đáp
VBQPPL tốt hơn phân đoạn theo số từ cố định không; tốt hơn bao nhiêu, ở loại câu hỏi nào, và chỗ nào không tốt hơn.
Biến duy nhất thay đổi giữa các nhánh là **cách phân đoạn**; mô hình nhúng, cách truy hồi, k, mô hình sinh và prompt giữ nguyên.

| Ký hiệu | Phương pháp |
|---|---|
| **A** | cửa sổ cố định 300 từ, không chồng lấn (baseline) |
| **A+** | A + tiền tố `[Số hiệu] [Trích yếu]` — đối chứng, tách phần lợi do *tiêu đề văn bản* khỏi phần lợi do *cắt theo cấu trúc* |
| **B** | cắt theo Điều → Khoản → Điểm (Điều/khoản > 350 từ mới tách tiếp), tiền tố phân cấp lặp ở mọi chunk con |
| **B+** | chunk của B; truy hồi ở mức khoản rồi mở rộng lên cả Điều cha trước khi đưa cho mô hình sinh |
| A_H, B− | đối chứng chỉ đo truy hồi: cửa sổ + tiền tố phân cấp / chunk B bỏ tiền tố |

## Môi trường

- VPS Linux aarch64 (Ampere Neoverse-N1, 4 nhân, 23 GB RAM), **không GPU** — mọi thứ chạy trên CPU.
- Python 3.12, venv tại `.venv`, phiên bản ghim trong `requirements.txt` (đầy đủ: `requirements.lock`).

```bash
python3.12 -m venv .venv
.venv/bin/pip install -r requirements.txt     # torch bản CPU lấy từ index của PyTorch
.venv/bin/python tools/tai_mo_hinh.py         # tải mô hình (ghim revision, kiểm sha256)
cp .env.example .env                          # cấu hình endpoint mô hình sinh
```

### Mô hình nhúng

`hiieu/halong_embedding` — repo nay đã chuyển thành `contextboxai/halong_embedding`, ghim revision
`b57776031035f70ed2030d2e35ecc533eb0f8f71`. Đã kiểm trong config chứ không giả định:

- `modules.json`: Transformer → Pooling (**mean**) → **Normalize** ⇒ vector đã chuẩn hoá L2, cosine = tích vô hướng;
- `sentence_bert_config.json`: `max_seq_length = 512` token (tính cả `<s>` `</s>`), dài hơn bị cắt — tỷ lệ chunk bị cắt được đo và báo cáo;
- `config_sentence_transformers.json`: `prompts` rỗng ⇒ **không** thêm tiền tố `query:` / `passage:` như họ e5.

Smoke test: `python -m rag.nhung --kiem` tái hiện đúng thứ hạng và điểm trong model card.

### Mô hình sinh (chạy tại chỗ, không cần API key)

Code gọi mô hình sinh qua endpoint **tương thích OpenAI**, cấu hình bằng `LLM_BASE_URL`, `LLM_API_KEY`, `LLM_MODEL`
trong `.env` (không có trong git). Endpoint là `llama-server` của [llama.cpp](https://github.com/ggml-org/llama.cpp)
chạy ngay trên VPS:

- llama.cpp tag `b11577` (commit `cbe28bb3cb0758f0c566a9a3561766821aeb0748`), build từ mã nguồn: `tools/build-llama.sh`
  (bản build sẵn cho arm64 cần glibc mới hơn Ubuntu 22.04 của VPS);
- mô hình **Qwen3-4B-Instruct-2507**, GGUF của unsloth, revision `a06e946bb6b655725eafa393f4a9745d460374c9`,
  giấy phép Apache-2.0; sha256 ghim trong `tools/tai_mo_hinh.py`;
- chạy bằng `tools/chay-llm.sh`: `temperature=0` (giải mã tham lam), `--seed 42`, **1 slot** (không gộp lô),
  **tắt cache prompt**, số luồng và kích thước lô cố định — để chạy lại ra đúng kết quả cũ. Mọi câu trả lời còn được
  lưu vào `results/gen/` nên chạy lại đánh giá không sinh lại.

## Dữ liệu

Nguồn chính: **vbpl.vn** — Cơ sở dữ liệu quốc gia về pháp luật (Bộ Tư pháp), lấy qua "server action" của trang
Next.js (xem chú thích trong `crawl/vbpl.py`; robots.txt cho phép, giữ ≤ 1 request/giây). Dự phòng: bộ HuggingFace
`th1nhng0/vietnamese-legal-documents` (crawl từ vbpl.vn, CC-BY-4.0). HTML gốc lưu ở `data/raw/`, text ở `data/clean/`.

## Chạy

Kiểm thử: `.venv/bin/python -m pytest -q`.

Mỗi bước ghi kết quả ra file và **tự bỏ qua nếu file đã có**; thêm `--force` để chạy lại. Mọi script có `--help`.

| Bước | Lệnh | Kết quả |
|---|---|---|
| 1 | `python tools/tai_mo_hinh.py`; `tools/build-llama.sh` | mô hình (ghim, kiểm sha256), llama-server |
| 1 | `python -m rag.nhung --kiem` | smoke test mô hình nhúng (khớp model card) |
| 1 | `python tools/thu_mo_hinh.py` (cần `tools/chay-llm.sh` đang chạy) | `results/buoc1/thu_mo_hinh.md` — thử định dạng trích dẫn |
| 1 | `python tools/do_toc_do_nhung.py`; `llama-bench` | `results/buoc1/toc_do_nhung.md`, `llama-bench.md` |
| 2 | `python -m crawl.thu_thap` (+ `--bo-sung-khong-dieu 10`) | `data/raw/` — HTML gốc + metadata + cây cấu trúc vbpl |
| 2 | `python -m crawl.chuan_hoa` | `data/clean/`, `data/clean_full/`, `data/thong_ke_chuan_hoa.jsonl` |
| 2 | `python -m crawl.chon_van_ban` | `data/manifest.csv` (bản sao: `results/buoc2/manifest.csv`) |
| 2 | `python -m crawl.thong_ke` | `results/buoc2/thong_ke_du_lieu.md` |

*(Bảng được bổ sung theo từng bước.)*

## Truy cập kết quả

*(Bổ sung ở bước 9: `https://$DATN_HOST/bao-cao`, …)*
