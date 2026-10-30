# datn-chunking — phân đoạn văn bản quy phạm pháp luật cho RAG

README này chỉ gồm: **cài môi trường → kiểm tra cài đúng → chạy local để tự test.**
Nội dung đồ án, dữ liệu, cách chạy từng bước thực nghiệm: [`docs/do-an.md`](docs/do-an.md).
Thử nghiệm mở rộng (OCR, rerank, độ dài chunk): [`docs/thuc-nghiem-mo-rong.md`](docs/thuc-nghiem-mo-rong.md).

## Yêu cầu

- Python **3.12** (bản đã dùng: 3.12.13), Git. Windows: chạy mọi lệnh trong **Git Bash**.
- ~6 GB đĩa (dữ liệu 1,2 GB + mô hình 3,3 GB). GPU NVIDIA không bắt buộc.

## 1. Cài đặt

```bash
git clone https://github.com/hungbeoqua321/datn-chunking.git
cd datn-chunking
```

**Windows — làm thêm trước:**

```bash
git config core.autocrlf false && git rm -rq --cached . && git reset -q --hard   # giữ xuống dòng LF
export PYTHONUTF8=1          # đặt cho MỌI lệnh python trên Windows (không có thì 23 test hỏng vì cp1252)
winget install astral-sh.uv && uv python install 3.12.13    # 3.12.13 không có bộ cài Windows chính thức
```

**Môi trường Python** — chọn một:

```bash
# Linux / CPU (đúng như VPS)
python3.12 -m venv .venv
.venv/bin/pip install -r requirements.txt

# Windows / GPU NVIDIA (chỉ khác torch: 2.14.1+cu130)
"$(uv python find 3.12.13)" -m venv .venv
.venv/Scripts/python -m pip install -r requirements-cu130.txt -c requirements-cu130.lock
```

Dưới đây viết `python` cho gọn: Linux là `.venv/bin/python`, Windows là `.venv/Scripts/python`.

```bash
cp .env.example .env
python tools/tai_mo_hinh.py        # models/: mô hình nhúng + Qwen3-4B GGUF, ghim revision, kiểm sha256
```

**Dữ liệu** — tải ở release **`du-lieu-2026-10-29`** của repo (repo private: đăng nhập GitHub trên trình duyệt,
hoặc `gh release download du-lieu-2026-10-29`), giải nén **tại gốc repo**:

| Hệ điều hành | Tệp | Giải nén |
|---|---|---|
| Windows | `datn-corpus.zip`, `datn-chunks.zip`, `datn-index.zip` | bấm đúp, hoặc `Expand-Archive <tệp> -DestinationPath .` |
| Linux | `datn-corpus.tar.gz`, `datn-chunks.tar.zst`, `datn-index.tar.zst` | `tar -xzf …` / `zstd -dc … \| tar -x` |

Kiểm tra tải đủ: `sha256sum -c SHA256SUMS.txt` (hoặc `SHA256SUMS-zip.txt`). **Không crawl lại dữ liệu.**

**Mô hình sinh (llama.cpp, đúng tag `b11577`):**

```bash
# Linux: build từ mã nguồn
tools/build-llama.sh

# Windows: tải bản build chính thức b11577 ở github.com/ggml-org/llama.cpp/releases/tag/b11577
#   llama-b11577-bin-win-cpu-x64.zip                      → giải vào tools/llama.cpp/build/bin/
#   llama-b11577-bin-win-cuda-13.4-x64.zip + cudart-llama-bin-win-cuda-13.4-x64.zip
#                                                         → giải vào tools/llama.cpp/build-cuda/bin/  (nếu có GPU)
```

## 2. Kiểm tra cài thành công

```bash
python -m rag.nhung --kiem     # mong đợi: "OK — khớp model card (lệch điểm lớn nhất 0.0000), chuẩn L2 = 1"
python -m pytest -q            # mong đợi: 140 passed
python -m rag.kiem_chi_muc     # mong đợi: "chỉ mục khớp tệp chunk: 17/17", thoát mã 0
```

Lệnh thứ ba thoát mã 1 là dữ liệu tải thiếu hoặc lệch — **dừng, tải lại**, đừng chạy đánh giá.

## 3. Chạy local để tự test

Mở hai cửa sổ terminal tại gốc repo.

```bash
# Cửa sổ 1 — mô hình sinh, cổng 8082
tools/chay-llm.sh              # CPU, đúng cờ của đồ án
tools/chay-llm-gpu.sh          # hoặc GPU (thêm -ngl 99), ~3 GB VRAM

curl http://127.0.0.1:8082/health          # mong đợi: {"status":"ok"} (đợi vài giây lúc nạp mô hình)
```

```bash
# Cửa sổ 2 — web
python -m uvicorn web.app:app --host 127.0.0.1 --port 8081
```

Mở **http://127.0.0.1:8081**:

| Trang | Nội dung |
|---|---|
| `/` | hỏi đáp — cần cửa sổ 1 đang chạy; ~70 s/câu trên CPU (i5-11400H) |
| `/ket-qua` | số liệu thực nghiệm |
| `/duyet` | bộ câu hỏi |
| `/loi-phan-doan` | các lỗi phân đoạn |
| `/slide` | slide bảo vệ (cần mạng: tải reveal.js từ CDN) |
| `/healthz` | kiểm tra web đang chạy |

Không bật cửa sổ 1 thì các trang khác vẫn mở được; trang hỏi đáp vẫn hiện các đoạn truy hồi được nhưng phần câu trả
lời báo `ConnectionError`.

Thử nhanh không cần trình duyệt (câu trả lời trả về dạng luồng, kết thúc bằng `event: xong`):

```bash
curl -N http://127.0.0.1:8081/api/hoi -H "Content-Type: application/json; charset=utf-8" \
     --data-binary @tools/hoi_thu.json
```

(Gửi qua tệp chứ không `-d '…'`: Git Bash trên Windows làm hỏng chữ có dấu trong tham số dòng lệnh.)
