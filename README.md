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

## Chốt chặn chỉ mục — chạy TRƯỚC mọi lần đánh giá

```bash
python -m rag.kiem_chi_muc      # lệch là mã thoát 1, DỪNG, không đánh giá
```

Kiểm mỗi tệp `data/chunks/*.jsonl` so với `data/index/<tên>/`: số chunk, **vân nội dung**
(chunk đầu/giữa/cuối — bắt được trường hợp dựng lại chunk mà số dòng tình cờ không đổi) và
kích thước `emb.f32`. Tệp cố ý không nhúng khai báo tường minh trong `KHONG_NHUNG`
(hiện là `B_s1..3`: B không phụ thuộc seed, chỉ nhúng seed 0).

Trong mã đánh giá, gọi ở dòng đầu:

```python
from rag.kiem_chi_muc import chot_chan
chot_chan()
```

⚠️ `rag.chi_muc` **bỏ qua** tệp đã có chỉ mục nếu thiếu `--force`, in `BỎ QUA` và thoát mã **3**;
`tools/nhung_tat_ca.sh` dừng hẳn, **không in `XONG NHÚNG`**. Lý do: sau khi sửa cài đặt C và D, tệp
chunk đổi nhưng chỉ mục vẫn là bản cũ mà lệnh vẫn báo thành công — suýt nữa pilot chấm C và D trên
đúng bản lỗi vừa sửa.

## Slide bảo vệ

Deck reveal.js (bản ghim **5.1.0**), một file duy nhất `web/static/slide.html`, phục vụ tại:

```
https://$DATN_HOST/slide
```

### Xuất PDF để nộp kèm quyển

reveal.js in PDF qua tham số `?print-pdf` (chỉ Chrome/Chromium cho kết quả đúng):

1. Mở `https://$DATN_HOST/slide?print-pdf`
2. `Ctrl+P` (macOS: `Cmd+P`)
3. Đặt **Destination: Save as PDF**, **Layout: Landscape**, **Margins: None**,
   bật **Background graphics** (không bật thì mất nền và viền bảng).
4. Save.

Hoặc không mở trình duyệt:

```bash
google-chrome --headless --disable-gpu --no-pdf-header-footer \
  --print-to-pdf=slide.pdf "https://$DATN_HOST/slide?print-pdf"
```

⚠️ **Mỗi slide phải vừa một trang.** Nếu một slide bị tràn sang trang thứ hai thì cắt bớt chữ
trên slide đó, đừng chỉnh cỡ chữ riêng lẻ — hệ thiết kế chỉ có ba cỡ chữ, khai báo một lần ở
đầu `slide.html`.

⚠️ **Deck tải reveal.js từ cdnjs.cloudflare.com** nên **cần mạng khi trình chiếu**. Phòng bảo vệ
không chắc có mạng: xuất sẵn bản PDF theo hướng dẫn trên và mang theo, hoặc tải reveal.js về
`web/static/` rồi đổi hai thẻ `<link>` và một thẻ `<script>` trong `slide.html` sang đường dẫn nội bộ.
Font (Be Vietnam Pro) đã tự host sẵn nên không phụ thuộc mạng.
