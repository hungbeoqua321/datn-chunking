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

## Chạy trên máy cá nhân

Repo chỉ chứa **mã nguồn và kết quả**. Phần nặng lấy ở hai chỗ khác: `data/` tải từ **GitHub Release**
(mục 1 dưới đây), `models/` tải từ HuggingFace bằng `tools/tai_mo_hinh.py`, `tools/llama.cpp/` build tại chỗ.

### 1. Lấy bộ dữ liệu

Bộ dữ liệu phát hành ở **GitHub Release `du-lieu`** của chính repo này, gồm 2 tệp zip (giải nén **tại gốc repo**,
trong zip đã có sẵn `data/…`, `ocr/…`; kiểm bằng `SHA256SUMS.txt`):

| Tệp | Nén | Nội dung | Bắt buộc? |
|---|---:|---|---|
| `docs.zip` | 546 MB | `data/raw`, `data/clean`, `data/clean_full`, `data/manifest.csv` (bản chụp vbpl.vn đã dùng), `data/chunks/`, `data/index/` | **Có** |
| `pdf.zip` | 343 MB | `ocr/data/pdf/` — bản PDF gốc (scan có dấu đỏ) của 60/80 văn bản | Chỉ cho thử nghiệm OCR |

```bash
gh release download du-lieu -D /tmp/datn-data          # hoặc tải bằng trình duyệt
( cd /tmp/datn-data && sha256sum -c SHA256SUMS.txt )
unzip /tmp/datn-data/docs.zip                           # tại gốc repo
```

`docs.zip` trùng tệp-theo-tệp với các gói `.tar.*` phát hành trước đây (đóng gói bằng `tools/dong_goi_zip.py`).

Hai thứ **cố ý không có** trong release:

- `models/` (3,3 GB) — tải lại bằng `python tools/tai_mo_hinh.py`, đã ghim revision và kiểm sha256.
- `data/index/cache.f32` (474 MB) — chỉ là bộ đệm lúc dựng chỉ mục, truy hồi đọc `<tên>/emb.f32` nên không cần.
  Thiếu nó thì lần dựng lại chỉ mục sau phải nhúng lại từ đầu.

> ⚠️ **Đừng crawl lại.** Bộ câu hỏi và đáp án vàng gắn với đúng bản chụp vbpl.vn trong `docs.zip`;
> crawl lại ra bản khác thì số hiệu và số Điều trong gold lệch, mọi con số trong `results/` không tái lập được.

Chỉ dùng corpus rồi dựng lại chunk và chỉ mục tại chỗ — chỉ nên làm nếu máy mạnh hơn VPS:

```bash
.venv/bin/python -m chunking.chay     # dựng lại data/chunks/
tools/nhung_tat_ca.sh                 # dựng lại data/index/ — rất lâu
```

### 2. Môi trường Python

Y như phần [Môi trường](#môi-trường): Python 3.12, `.venv`, `requirements.txt`. Nếu máy có GPU NVIDIA thì
**vẫn cài torch bản CPU theo `requirements.txt`** — đổi sang bản CUDA là đổi điều kiện thực nghiệm, phần nhúng
có thể ra vector khác ở chữ số cuối.

```bash
python3.12 -m venv .venv
.venv/bin/pip install -r requirements.txt
cp .env.example .env
.venv/bin/python -m rag.nhung --kiem      # phải khớp model card
.venv/bin/python -m pytest -q             # 140 test
```

### 3. Mô hình sinh

`tools/llama.cpp/` không có trong repo lẫn release — build tại chỗ, **đúng tag `b11577`** (script đã ghim sẵn):

```bash
python tools/tai_mo_hinh.py   # models/ — mô hình nhúng + Qwen3-4B GGUF, kiểm sha256
tools/build-llama.sh          # tools/llama.cpp/
tools/chay-llm.sh             # llama-server tại 127.0.0.1:8082
```

`tools/chay-llm.sh` ghim `-t 3 -tb 3 -c 4096 -np 1 -b 512 -ub 512 --no-cache-prompt --seed 42` cho VPS 4 nhân.
**Giữ nguyên mọi cờ** nếu muốn tái lập số cũ — kể cả trên máy nhiều nhân hơn. Chỉ đổi `CONG=<cổng>` và
`MO_HINH=<đường dẫn gguf>` qua biến môi trường.

### 4. Chốt chặn rồi mới đánh giá

```bash
.venv/bin/python -m rag.kiem_chi_muc     # lệch là thoát mã 1 → DỪNG
```

### 5. Web xem kết quả

```bash
.venv/bin/uvicorn web.app:app --host 127.0.0.1 --port 8081
```

### Máy cá nhân Windows + GPU (đã chạy thật 29–30/10/2026)

Máy: Windows 11, i5-11400H (12 luồng), RAM 16 GB, **RTX 2050 4 GB** (driver 621.01). Không dùng WSL.
Mọi lệnh dưới đây chạy trong **Git Bash** tại gốc repo. Thời gian là thời gian thật đo trên máy này.

**Ba bẫy của Windows — làm trước tiên:**

1. `git config core.autocrlf false` rồi checkout lại (`git rm -rq --cached . && git reset -q --hard`). Git for Windows
   mặc định đổi xuống dòng sang CRLF → script `.sh` hỏng, vân nội dung jsonl/csv lệch.
2. Mọi lệnh Python chạy với **`PYTHONUTF8=1`** — không có thì `open()` dùng cp1252 và 23 test hỏng.
3. Python 3.12.13 (bản VPS dùng) **không có bộ cài Windows** (3.12 chỉ còn bản vá bảo mật) → cài qua `uv`.

```bash
export PYTHONUTF8=1
winget install astral-sh.uv                                    # 19 s cùng bước dưới
uv python install 3.12.13
"$(uv python find 3.12.13)" -m venv .venv
.venv/Scripts/python -m pip install -r requirements-cu130.txt -c requirements-cu130.lock    # 573 s
cp .env.example .env
.venv/Scripts/python tools/tai_mo_hinh.py                      # 133 s, kiểm sha256
.venv/Scripts/python -m rag.nhung --kiem                       # khớp model card, lệch 0.0000
.venv/Scripts/python -m pytest -q                              # 140/140
```

`requirements-cu130.*` **chỉ khác bản gốc ở dòng torch** (`2.14.1+cu130` thay `+cpu`); mọi gói khác đúng lock.
Khác biệt do Windows: thêm `colorama`, `tzdata`; không có `uvloop` (không hỗ trợ Windows, không ảnh hưởng số).

**llama.cpp:** không build — tải bản build chính thức của **đúng tag `b11577`** (commit `cbe28bb3c`, kiểm digest):
`llama-b11577-bin-win-cpu-x64.zip` giải vào `tools/llama.cpp/build/bin/` (đường `chay-llm.sh` dùng),
`llama-b11577-bin-win-cuda-13.4-x64.zip` + `cudart-llama-bin-win-cuda-13.4-x64.zip` giải vào `tools/llama.cpp/build-cuda/bin/`.

```bash
tools/chay-llm.sh        # CPU, đúng cờ của VPS
tools/chay-llm-gpu.sh    # GPU: y hệt cờ, chỉ thêm -ngl 99 — sinh ~40 token/s (VPS: 9), 3,0 GB VRAM
```

**Biến môi trường thêm cho máy cá nhân** (mặc định giữ y hành vi cũ):

| Biến | Mặc định | Dùng khi |
|---|---|---|
| `NHUNG_DEVICE` | `cpu` | `cuda` để nhúng trên GPU (thử nghiệm mới) |
| `KET_QUA_DIR` | `results/` | chạy tái lập ra thư mục khác, không ghi đè số gốc |
| `CHUNKS_DIR`, `INDEX_DIR` | `data/chunks`, `data/index` | thử nghiệm mở rộng dựng chỉ mục riêng |

**Cổng kiểm tra:** `rag.chi_muc A_s0 B_s0` thoát **mã 3** (BỎ QUA — đã có chỉ mục, không phải thành công);
`rag.kiem_chi_muc` thoát 0, 17/17. ⚠️ **Đừng chạy `rag.chi_muc --tat-ca`**: nó nhúng cả `B_s1..3` (cố ý không nhúng).

**Tái lập truy hồi** (`KET_QUA_DIR=thuc_nghiem/tai_lap python -m eval.chay_truy_hoi`, 46 s): **926/953 dòng khớp
tuyệt đối** với `results/metrics_truy_hoi.csv`. 27 dòng lệch đều thuộc D (R@1 0,4091 → 0,4182 = 1 câu/110) do
**hoà điểm tuyệt đối** giữa hai chunk cùng nội dung ở bản cũ/bản mới của một văn bản — numpy ARM và x86 phá hoà khác
nhau. Chi tiết: [`thuc_nghiem/tai_lap/GHI_CHU.md`](../thuc_nghiem/tai_lap/GHI_CHU.md).

### Prompt để nhờ Claude Code dựng hộ

Dán nguyên hai khối dưới đây vào Claude Code trên máy cá nhân (khối **Hệ thống** vào system prompt /
`CLAUDE.md`, khối **Con người** vào ô chat).

#### Hệ thống

```text
Bạn là kỹ sư dựng lại môi trường cho một đồ án tốt nghiệp đã chạy xong trên VPS Linux aarch64,
nay chuyển sang máy cá nhân. Mục tiêu là chạy lại ĐÚNG số cũ, không phải làm cho nó chạy được.

Ràng buộc, không được tự ý bỏ qua:
- Mọi phiên bản đều đã ghim: Python 3.12, requirements.txt (torch bản CPU), mô hình nhúng
  halong_embedding revision b57776031035f70ed2030d2e35ecc533eb0f8f71, llama.cpp tag b11577,
  Qwen3-4B-Instruct-2507-Q4_0 revision a06e946bb6b655725eafa393f4a9745d460374c9.
  Không nâng, không đổi sang bản CUDA, không thay mô hình.
- Không crawl lại dữ liệu. data/raw, data/clean, data/clean_full, data/manifest.csv lấy từ
  GitHub Release du-lieu (docs.zip); crawl lại làm lệch đáp án vàng.
- Không sửa cờ trong tools/chay-llm.sh. Đổi cờ = đổi thực nghiệm.
- Trước mọi lệnh đánh giá phải chạy python -m rag.kiem_chi_muc; thoát khác 0 thì DỪNG, không
  chạy tiếp, không tự sửa chỉ mục.
- rag.chi_muc thoát mã 3 nghĩa là BỎ QUA vì đã có chỉ mục cũ, không phải thành công.

Cách làm việc:
- Trả lời bằng tiếng Việt.
- Báo thời gian thật của từng bước nặng (cài đặt, build llama.cpp, nhúng, sinh).
- Lệnh nào hỏng thì dán nguyên văn lỗi, đừng tóm tắt lại.
- Không chạy lại bước đã có kết quả trong results/; mọi script tự bỏ qua nếu file đã có.
- Đọc README.md trước khi gõ lệnh đầu tiên.
```

#### Con người

```text
Dựng lại đồ án datn-chunking trên máy này và chạy cho tới khi ra được kết quả.

Tôi đã có:
- repo clone từ github.com/hungbeoqua321/datn-chunking
- gh đã đăng nhập bằng tài khoản hungbeoqua321 (repo private)

Làm theo README.md (cài đặt → kiểm tra → chạy local); chi tiết ở mục "Chạy trên máy cá nhân" của docs/do-an.md:
1. Tải bộ dữ liệu từ GitHub Release du-lieu (docs.zip), kiểm sha256, giải vào data/.
   Rồi tải mô hình bằng python tools/tai_mo_hinh.py (KHÔNG có trong release).
2. Dựng .venv theo requirements.txt, copy .env.example thành .env.
3. Chạy rag.nhung --kiem và pytest -q — báo số test xanh.
4. Build llama.cpp đúng tag b11577 bằng tools/build-llama.sh,
   rồi bật tools/chay-llm.sh.
5. Chạy rag.kiem_chi_muc. Lệch thì dừng và báo tôi, đừng tự sửa.
6. Bật web bằng uvicorn và cho tôi đường dẫn xem kết quả.

Mỗi bước xong thì báo thời gian thật. Bước nào hỏng thì dừng ở đó, dán lỗi nguyên văn
và nói rõ cần tôi làm gì.
```

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
