# datn-chunking — phân đoạn văn bản quy phạm pháp luật cho RAG

README này chỉ gồm: **cài đặt → kiểm tra cài đúng → chạy local để tự test → sửa lỗi thường gặp.**
Nội dung đồ án: [`docs/do-an.md`](docs/do-an.md). Thử nghiệm mở rộng (OCR, rerank, độ dài chunk):
[`docs/thuc-nghiem-mo-rong.md`](docs/thuc-nghiem-mo-rong.md).

## Cần có

- **Python 3.12** (64-bit) và **Git**. Windows: gõ lệnh trong **Git Bash** (cài kèm Git).
- ~6 GB đĩa trống. GPU không bắt buộc.

## 1. Cài đặt

Luôn cài vào **môi trường ảo (venv)** — một thư mục `.venv/` riêng trong repo, không đụng Python của máy, cài hỏng
thì xoá `.venv` làm lại là xong.

**① Lấy mã nguồn**

```bash
git clone https://github.com/hungbeoqua321/datn-chunking.git
cd datn-chunking
git config core.autocrlf false && git rm -rq --cached . && git reset -q --hard   # chỉ Windows
```

**② Tạo và bật venv**

```bash
python -m venv .venv               # Linux/macOS: python3.12 -m venv .venv
source .venv/Scripts/activate      # Windows (Git Bash). Linux/macOS: source .venv/bin/activate
```

Bật xong, đầu dòng lệnh có `(.venv)`. Mọi lệnh `python`, `pip` sau đó đều chạy trong venv.
**Mỗi lần mở terminal mới phải bật lại** (dòng `source …` ở trên).

**③ Cài thư viện** — chọn một dòng:

```bash
pip install -r requirements.txt                                   # CPU — mặc định, đúng như đồ án
pip install -r requirements-cu130.txt -c requirements-cu130.lock  # GPU NVIDIA (chỉ khác torch)
```

Mất khoảng 10 phút (tải torch ~2,5 GB). Phiên bản đã ghim sẵn, **không** nâng cấp gói nào.

**④ Tải mô hình và dữ liệu**

```bash
export PYTHONUTF8=1                # chỉ Windows — đặt mỗi lần mở terminal (hoặc 1 lần: setx PYTHONUTF8 1)
cp .env.example .env
python tools/tai_mo_hinh.py        # ~3,3 GB vào models/, tự kiểm sha256
```

Dữ liệu: vào **Releases → `du-lieu`** của repo, tải **`docs.zip`** (bắt buộc) và `pdf.zip` (chỉ cho thử nghiệm OCR),
giải nén **ngay tại thư mục repo** — trong zip đã có sẵn `data/…`, `ocr/…`.

```bash
unzip docs.zip                     # hoặc bấm đúp trên Windows; kiểm: sha256sum -c SHA256SUMS.txt
```

**⑤ Mô hình sinh llama.cpp** (chỉ cần cho phần hỏi đáp)

- Linux: `tools/build-llama.sh`
- Windows: tải từ [llama.cpp release `b11577`](https://github.com/ggml-org/llama.cpp/releases/tag/b11577) tệp
  `llama-b11577-bin-win-cpu-x64.zip`, giải vào `tools/llama.cpp/build/bin/`.
  Có GPU: thêm `llama-b11577-bin-win-cuda-13.4-x64.zip` + `cudart-llama-bin-win-cuda-13.4-x64.zip`, giải vào
  `tools/llama.cpp/build-cuda/bin/`.

## 2. Kiểm tra cài thành công

```bash
python -m rag.nhung --kiem     # mong đợi: OK — khớp model card (lệch điểm lớn nhất 0.0000)
python -m pytest -q            # mong đợi: 140 passed
python -m rag.kiem_chi_muc     # mong đợi: chỉ mục khớp tệp chunk: 17/17
```

Cả ba đúng như trên là cài xong. Sai chỗ nào xem [mục 4](#4-lỗi-thường-gặp).

## 3. Chạy local để tự test

Hai terminal, cả hai đều **bật venv** trước.

```bash
# Terminal 1 — mô hình sinh, cổng 8082
tools/chay-llm.sh              # CPU   (GPU: tools/chay-llm-gpu.sh)
```

```bash
# Terminal 2 — web, cổng 8081
python -m uvicorn web.app:app --host 127.0.0.1 --port 8081
```

Mở **http://127.0.0.1:8081** — `/` hỏi đáp (~70 s/câu trên CPU), `/ket-qua` số liệu, `/duyet` bộ câu hỏi,
`/loi-phan-doan`, `/slide`. Thử bằng lệnh (kết thúc bằng `event: xong`):

```bash
curl -N http://127.0.0.1:8081/api/hoi -H "Content-Type: application/json; charset=utf-8" --data-binary @tools/hoi_thu.json
```

## 4. Lỗi thường gặp

| Triệu chứng | Nguyên nhân | Cách sửa |
|---|---|---|
| `Python was not found` / `python3.12: command not found` | chưa cài Python, hoặc Windows đang trỏ tới lối tắt Microsoft Store | cài Python 3.12 từ python.org (tích *Add to PATH*), mở lại terminal. Hoặc: `winget install astral-sh.uv && uv python install 3.12` rồi `"$(uv python find 3.12)" -m venv .venv` |
| `No module named ensurepip` khi tạo venv (Ubuntu/Debian) | thiếu gói venv | `sudo apt install python3.12-venv` |
| PowerShell báo `running scripts is disabled` khi bật venv | chính sách chặn script | dùng Git Bash, hoặc chạy 1 lần `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` rồi `.venv\Scripts\Activate.ps1` |
| `pip` báo `No matching distribution found for torch==2.14.1+...` | Python không phải 3.12 64-bit | `python --version` phải ra `3.12.x`; xoá `.venv`, tạo lại bằng đúng Python 3.12 |
| Không cài được bản GPU (`+cu130`) | driver NVIDIA cũ / không có GPU | dùng bản CPU: `pip install -r requirements.txt` — kết quả đúng như đồ án |
| `UnicodeEncodeError` / `UnicodeDecodeError: 'charmap'`, hoặc ~23 test hỏng | Windows mở tệp bằng cp1252 | `export PYTHONUTF8=1` (lâu dài: `setx PYTHONUTF8 1`, mở lại terminal) |
| `$'\r': command not found` khi chạy `tools/*.sh` | Git đổi xuống dòng sang CRLF | chạy lại dòng `git config core.autocrlf false …` ở bước ① |
| `ModuleNotFoundError: No module named 'torch'` (hoặc gói khác) | quên bật venv | `source .venv/Scripts/activate` (Linux: `.venv/bin/activate`) |
| `SAI sha256` khi tải mô hình | tải đứt giữa chừng | `python tools/tai_mo_hinh.py --force` |
| `rag.kiem_chi_muc` thoát mã 1 / thiếu `data/…` | `docs.zip` giải nén sai chỗ (ra `data/data/…` hoặc nằm ngoài repo) | giải nén lại tại thư mục repo sao cho có `datn-chunking/data/index/` |
| Web hỏi đáp báo `Chưa có chỉ mục vector` | chưa có `docs.zip` | bước ④ |
| Web hỏi đáp báo `ConnectionError` | chưa bật mô hình sinh | bật Terminal 1; `curl http://127.0.0.1:8082/health` phải ra `{"status":"ok"}` |
| `{"message":"Loading model"}` (503) | mô hình đang nạp | đợi 10–30 giây |
| `tools/llama.cpp/build/bin/llama-server: No such file` | chưa làm bước ⑤ | bước ⑤ |
| GPU báo `out of memory` | VRAM < 3 GB trống | tắt chương trình khác dùng GPU, hoặc dùng `tools/chay-llm.sh` (CPU) |
| `curl … -d '{"cau_hoi": "…"}'` ra chữ lỗi / `ill-formed UTF-8` | Git Bash Windows làm hỏng chữ có dấu trong tham số | gửi qua tệp: `--data-binary @tools/hoi_thu.json` |
| `Address already in use` (cổng 8081/8082) | đang có một bản chạy rồi | tắt bản cũ, hoặc đổi cổng: `--port 8090`, `CONG=8083 tools/chay-llm.sh` |

**Vẫn không cài được?**

1. Làm lại sạch: xoá thư mục `.venv`, làm lại từ bước ②, dùng **bản CPU** (`requirements.txt`).
2. Chỉ cần **xem kết quả**: bước ①②③ là đủ, chạy web (Terminal 2) — `/ket-qua`, `/duyet`, `/loi-phan-doan`
   không cần dữ liệu lẫn mô hình. Hoặc đọc thẳng các tệp `.md` trong [`results/`](results/) trên GitHub.
