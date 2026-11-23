# Phân đoạn văn bản quy phạm pháp luật cho RAG

Hướng dẫn này đưa bạn từ một máy trống tới lúc hỏi đáp được trên trình duyệt. Cứ làm lần lượt từ trên xuống,
mỗi bước đều có dòng "**xong khi…**" để bạn biết đã đúng chưa rồi mới đi tiếp.

## Bạn cần chuẩn bị

- **Python 3.12 bản 64-bit** — tải ở [python.org](https://www.python.org/downloads/), lúc cài nhớ tích
  *Add python.exe to PATH*. Các bản 3.11, 3.13 **không** dùng được (thư viện đã ghim theo 3.12).
- **Git** — tải ở [git-scm.com](https://git-scm.com/). Trên Windows, Git cài kèm **Git Bash**:
  mọi lệnh trong README này gõ trong Git Bash, không phải CMD hay PowerShell.
- Khoảng **8 GB đĩa trống** (thư viện ~2,5 GB, mô hình ~3,3 GB, dữ liệu ~1,5 GB lúc giải nén).
- GPU **không** bắt buộc — mọi số liệu trong đồ án đều chạy lại được bằng CPU.

Mất khoảng **30–40 phút**, phần lớn là ngồi chờ tải.

## 1. Cài đặt

### ① Lấy mã nguồn

```bash
git clone https://github.com/hungbeoqua321/datn-chunking.git
cd datn-chunking
```

Trên **Windows** chạy thêm dòng này (để Git không đổi kiểu xuống dòng, nếu không các script `.sh` sẽ báo lỗi):

```bash
git config core.autocrlf false && git rm -rq --cached . && git reset -q --hard
```

**Xong khi:** đang đứng trong thư mục `datn-chunking`, gõ `ls` thấy `rag/`, `eval/`, `tools/`, `README.md`.

### ② Tạo môi trường ảo (venv)

Venv là một thư mục `.venv/` nằm trong repo, chứa riêng Python và thư viện của đồ án — không đụng tới Python
của máy. Cài hỏng thì xoá `.venv` đi làm lại, không ảnh hưởng gì khác.

```bash
python -m venv .venv                 # Linux/macOS: python3.12 -m venv .venv
source .venv/Scripts/activate        # Linux/macOS: source .venv/bin/activate
export PYTHONUTF8=1                  # chỉ Windows, nhưng BẮT BUỘC — thiếu là lỗi khi in tiếng Việt
```

**Xong khi:** đầu dòng lệnh hiện `(.venv)`, và `python --version` ra `Python 3.12.x`.

> **Mỗi lần mở terminal mới** phải chạy lại hai dòng `source …` và `export PYTHONUTF8=1`.
> Muốn khỏi gõ `export` mỗi lần (Windows): chạy một lần `setx PYTHONUTF8 1` rồi mở terminal mới.

### ③ Cài thư viện

Chọn **một** trong hai dòng:

```bash
pip install -r requirements.txt                                   # CPU — chọn dòng này nếu không chắc
pip install -r requirements-cu130.txt -c requirements-cu130.lock  # có GPU NVIDIA (chỉ khác bản torch)
```

Mất khoảng 5–10 phút. Các phiên bản đã ghim sẵn — **đừng** `pip install --upgrade` gói nào.

**Xong khi:** dòng cuối có `Successfully installed …`, không có chữ `ERROR`.

### ④ Tải mô hình

```bash
cp .env.example .env
python tools/tai_mo_hinh.py
```

Tải ~3,3 GB từ Hugging Face vào `models/` (mô hình nhúng halong_embedding và Qwen3-4B), tự kiểm sha256.

**Xong khi:** in ra `ok sha256 model.safetensors` và `ok sha256 Qwen3-4B-Instruct-2507-Q4_0.gguf`.

### ⑤ Tải dữ liệu

Dữ liệu (văn bản luật đã tải từ vbpl.vn, chunk, chỉ mục vector) quá lớn để đưa vào git nên được để ở mục
[**Releases → `du-lieu`**](https://github.com/hungbeoqua321/datn-chunking/releases/tag/du-lieu) của repo.
Có hai gói:

| Gói | Dung lượng | Cần khi nào | Giải nén ra |
|---|---:|---|---|
| **`docs.zip`** | 546 MB | **luôn cần** — thiếu thì không chạy được hỏi đáp và đánh giá | `data/` |
| `pdf.zip` | 785 MB | chỉ khi muốn chạy lại thử nghiệm OCR trên 60 PDF scan gốc | `ocr/data/pdf/` |

**Cách 1 — dùng script (nên dùng):**

```bash
python tools/tai_du_lieu.py          # tải docs.zip
python tools/tai_du_lieu.py pdf      # (tuỳ chọn) tải thêm pdf.zip
```

Script tự làm hết: tải về, kiểm sha256, giải nén đúng chỗ, xoá tệp zip cho đỡ chật đĩa.
**Mạng chập chờn, bị đứt giữa chừng?** Cứ chạy lại đúng lệnh đó — script tải **tiếp** từ chỗ đã có
(phần đang tải dở nằm ở `data/_tai/`), không phải tải lại từ đầu. Bản thân script cũng tự thử lại khi mất mạng.
Không cần tài khoản GitHub.

**Cách 2 — tải bằng trình duyệt hoặc IDM** (khi máy chặn Python ra mạng, hoặc bạn quen dùng trình quản lý tải):
bấm vào tên tệp ở [trang release](https://github.com/hungbeoqua321/datn-chunking/releases/tag/du-lieu) để tải,
rồi đưa đường dẫn tệp cho script để nó kiểm và giải nén:

```bash
python tools/tai_du_lieu.py --tu ~/Downloads/docs.zip
python tools/tai_du_lieu.py pdf --tu ~/Downloads/pdf.zip
```

(Đừng tự giải nén bằng tay — rất dễ giải ra sai chỗ thành `data/data/…`. Script kiểm cả việc này.)

**Cách 3 — dùng `curl`** (không có Python, ví dụ tải sẵn trên máy khác): `-C -` để tải tiếp khi bị đứt.

```bash
curl -L -C - --retry 20 -O https://github.com/hungbeoqua321/datn-chunking/releases/download/du-lieu/docs.zip
```

Sau đó vẫn dùng `python tools/tai_du_lieu.py --tu docs.zip` để kiểm và giải nén.

**Xong khi:** script in `xong: có data/index/`.

#### Dữ liệu mẫu có sẵn trong git (không cần tải)

Nếu chỉ muốn **thử OCR** mà chưa muốn tải `pdf.zip` 785 MB: trong git đã có sẵn
2 PDF scan mẫu ở [`ocr/data/mau/`](ocr/data/mau/) cùng văn bản chuẩn để so ở `ocr/data/docs/`.
Xem phần [Đọc PDF scan](#tuỳ-chọn-đọc-pdf-scan) bên dưới.

### ⑥ Cài llama.cpp để mô hình trả lời câu hỏi

Chỉ cần nếu bạn muốn **hỏi đáp**; chỉ xem kết quả thì bỏ qua bước này.

- **Linux:** `tools/build-llama.sh`
- **Windows:** vào [llama.cpp release `b11577`](https://github.com/ggml-org/llama.cpp/releases/tag/b11577),
  tải `llama-b11577-bin-win-cpu-x64.zip`, giải nén vào `tools/llama.cpp/build/bin/`.
  Có GPU NVIDIA thì tải thêm `llama-b11577-bin-win-cuda-13.4-x64.zip` và `cudart-llama-bin-win-cuda-13.4-x64.zip`,
  giải nén cả hai vào `tools/llama.cpp/build-cuda/bin/`.

**Xong khi:** có tệp `tools/llama.cpp/build/bin/llama-server` (Windows: `llama-server.exe`).

## 2. Kiểm tra cài thành công

```bash
python -m rag.nhung --kiem     # mong đợi: OK — khớp model card (lệch điểm lớn nhất 0.0000)
python -m pytest -q            # mong đợi: 140 passed
python -m rag.kiem_chi_muc     # mong đợi: chỉ mục khớp tệp chunk: 17/17
```

Ra đúng cả ba dòng như trên là cài xong. Sai ở đâu thì tra bảng [Lỗi thường gặp](#4-lỗi-thường-gặp).

## 3. Chạy thử trên máy

Cần **hai terminal**, cả hai đều phải bật venv trước (`source .venv/Scripts/activate` và `export PYTHONUTF8=1`).

```bash
# Terminal 1 — mô hình trả lời, cổng 8082. Để nguyên cửa sổ này, đừng tắt.
tools/chay-llm.sh              # có GPU: tools/chay-llm-gpu.sh
```

```bash
# Terminal 2 — trang web, cổng 8081
python -m uvicorn web.app:app --host 127.0.0.1 --port 8081
```

Mở trình duyệt vào **http://127.0.0.1:8081**:

| Trang | Để làm gì |
|---|---|
| `/` | hỏi đáp (CPU mất ~70 giây/câu, GPU nhanh hơn nhiều) |
| `/ket-qua` | số liệu thực nghiệm |
| `/duyet` | bộ 110 câu hỏi đánh giá |
| `/loi-phan-doan` | ví dụ lỗi phân đoạn |
| `/slide` | slide bảo vệ |

Trang hỏi đáp còn cho phép:

- **Hỏi trên tài liệu của bạn:** tải lên tệp .pdf, .docx, .txt hoặc .md, rồi tích *Kèm tài liệu tôi đã tải lên*.
  PDF scan sẽ được OCR (~3 giây/trang), việc này cần cài thêm [môi trường OCR](#tuỳ-chọn-đọc-pdf-scan).
  Tệp .docx và .txt thì không cần.
- **Tìm trong 212 văn bản** (toàn bộ văn bản đã tải từ vbpl.vn) thay vì 80 văn bản của đồ án. Kho này phải dựng
  một lần: `python -m rag.kho dung-day-du`.

Không muốn mở trình duyệt thì thử bằng lệnh (kết quả kết thúc bằng `event: xong`):

```bash
curl -N http://127.0.0.1:8081/api/hoi -H "Content-Type: application/json; charset=utf-8" --data-binary @tools/hoi_thu.json
```

### Tuỳ chọn: đọc PDF scan

OCR dùng một venv **riêng** tên `.venv-ocr`, tách khỏi `.venv` của đồ án để thư viện hai bên không xung đột:

```bash
python -m venv .venv-ocr
.venv-ocr/Scripts/python -m pip install -r requirements-ocr.txt      # Linux: .venv-ocr/bin/python
```

Cài thêm **Tesseract** (chương trình nhận dạng chữ):

- **Linux:** `sudo apt install tesseract-ocr tesseract-ocr-vie`
- **Windows** (không cần quyền admin, cài gọn trong `tools/`):

```bash
curl -L -o tools/mm/micromamba.exe --create-dirs https://github.com/mamba-org/micromamba-releases/releases/latest/download/micromamba-win-64
MAMBA_ROOT_PREFIX=tools/mm/root tools/mm/micromamba.exe create -y -p tools/tesseract-env -c conda-forge tesseract
curl -L -o tools/tesseract-env/share/tessdata/vie.traineddata https://github.com/tesseract-ocr/tessdata_best/raw/main/vie.traineddata
```

Thử trên PDF mẫu có sẵn trong git (không cần `pdf.zip`):

```bash
.venv-ocr/Scripts/python -m ocr.doc_pdf ocr/data/mau/70fbb4a0-c0df-11f1-8027-6f84f5cae5b7.pdf
```

**Xong khi:** in ra JSON có `"so_trang": 3, "trang_ocr": 3`.

## 4. Lỗi thường gặp

| Bạn thấy | Vì sao | Cách sửa |
|---|---|---|
| `Python was not found` / `python3.12: command not found` / Git Bash báo `python: cannot execute: required file not found` | chưa cài Python, hoặc Windows đang trỏ `python` tới lối tắt Microsoft Store | cài Python 3.12 từ python.org (tích *Add to PATH*), mở lại terminal. Hoặc: `winget install astral-sh.uv && uv python install 3.12` rồi `"$(uv python find 3.12)" -m venv .venv` |
| `UnicodeEncodeError` / `UnicodeDecodeError: 'charmap'`, hoặc ~23 test hỏng (Windows) | Python đang dùng bảng mã cp1252, không có chữ tiếng Việt | `export PYTHONUTF8=1` (lâu dài: `setx PYTHONUTF8 1` rồi mở terminal mới), chạy lại lệnh |
| `No module named ensurepip` khi tạo venv (Ubuntu/Debian) | thiếu gói venv | `sudo apt install python3.12-venv` |
| PowerShell báo `running scripts is disabled` khi bật venv | Windows chặn chạy script | dùng Git Bash. Hoặc chạy một lần `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` rồi `.venv\Scripts\Activate.ps1` |
| `No matching distribution found for torch==2.14.1+...` | Python không phải 3.12 64-bit | `python --version` phải ra `3.12.x`. Xoá `.venv`, tạo lại bằng đúng Python 3.12 |
| Không cài được bản GPU (`+cu130`) | driver NVIDIA cũ, hoặc máy không có GPU | dùng bản CPU `pip install -r requirements.txt` — kết quả vẫn đúng như đồ án |
| `ModuleNotFoundError: No module named 'torch'` (hoặc gói khác) | quên bật venv | `source .venv/Scripts/activate` (Linux: `.venv/bin/activate`) |
| `$'\r': command not found` khi chạy `tools/*.sh` | Git đã đổi kiểu xuống dòng sang CRLF | chạy dòng `git config core.autocrlf false …` ở bước ① |
| `SAI sha256` khi tải mô hình | tải bị đứt giữa chừng | `python tools/tai_mo_hinh.py --force` |
| Tải dữ liệu đứng yên hoặc báo `mạng lỗi … thử lại` | mạng chập chờn, hoặc mạng chặn GitHub | cứ để script tự thử lại; tắt đi thì chạy lại lệnh, nó tải tiếp từ chỗ cũ. Vẫn không được: đổi mạng (4G), hoặc tải bằng trình duyệt/IDM rồi dùng `--tu` (bước ⑤ ở trên) |
| `SAI sha256 cho docs.zip` | tệp tải về bị hỏng, hoặc tải bằng trình duyệt chưa xong | dùng cách 1: script đã xoá tệp hỏng, chạy lại để tải lại. Nếu dùng `--tu`: tải lại tệp đó |
| `rag.kiem_chi_muc` thoát mã 1, hoặc báo thiếu `data/…` | chưa tải dữ liệu, hoặc tự giải nén sai chỗ (ra `data/data/…`) | xoá thư mục `data/` giải sai rồi chạy `python tools/tai_du_lieu.py` |
| Web hỏi đáp báo `Chưa có chỉ mục vector` | chưa có dữ liệu | bước ⑤ (tải dữ liệu) |
| Web hỏi đáp báo `ConnectionError` | chưa bật mô hình trả lời | bật Terminal 1. Kiểm: `curl http://127.0.0.1:8082/health` phải ra `{"status":"ok"}` |
| `{"message":"Loading model"}` (503) | mô hình đang nạp | đợi 10–30 giây |
| `tools/llama.cpp/build/bin/llama-server: No such file` | chưa cài llama.cpp | bước ⑥ (cài llama.cpp) |
| GPU báo `out of memory` | còn chưa tới 3 GB VRAM trống | tắt chương trình khác đang dùng GPU, hoặc chạy bản CPU `tools/chay-llm.sh` |
| `curl … -d '{"cau_hoi": "…"}'` ra chữ lỗi / `ill-formed UTF-8` | Git Bash trên Windows làm hỏng chữ có dấu trong tham số | gửi câu hỏi qua tệp: `--data-binary @tools/hoi_thu.json` |
| Tải PDF lên báo `Chưa cài môi trường OCR (.venv-ocr)` | chưa cài phần đọc PDF scan | làm [phần đó](#tuỳ-chọn-đọc-pdf-scan), hoặc tải lên .docx/.txt thay vì PDF |
| `OCR hỏng: … Failed loading language 'vie'` | Tesseract thiếu dữ liệu tiếng Việt | chạy lệnh `curl` cuối ở phần đọc PDF scan. Linux: `sudo apt install tesseract-ocr-vie` |
| Không lấy được chữ nào từ PDF | ảnh quá mờ hoặc trang trắng | quét lại ở ≥ 300 dpi |
| Ô *212 văn bản* bị mờ, không chọn được | chưa dựng kho đầy đủ | `python -m rag.kho dung-day-du` (cần có dữ liệu ở bước ⑤) |
| `Address already in use` (cổng 8081/8082) | đang có một bản chạy rồi | tắt bản cũ, hoặc đổi cổng: `--port 8090`, `CONG=8083 tools/chay-llm.sh` |

**Vẫn không cài được?**

1. **Làm lại từ đầu cho sạch:** xoá thư mục `.venv`, làm lại từ bước ②, dùng bản CPU (`requirements.txt`).
2. **Chỉ cần xem kết quả:** làm bước ①②③ là đủ, rồi bật web (Terminal 2). Các trang `/ket-qua`, `/duyet`,
   `/loi-phan-doan` không cần dữ liệu hay mô hình. Hoặc đọc thẳng các tệp `.md` trong
   [`results/`](results/) ngay trên GitHub.
