# Thử nghiệm mở rộng (máy cá nhân): OCR, rerank, độ dài chunk

**Không thuộc thiết kế gốc** của đồ án — mọi số gốc trong `results/` giữ nguyên. Mọi thứ ghi vào `ocr/` và
`thuc_nghiem/`; chỉ mục thử nghiệm nằm ở `thuc_nghiem/data/` (không lẫn với `data/index`).

## Tiến độ

| Việc | Trạng thái | Kết quả / thời gian thật |
|---|---|---|
| Tải PDF gốc (bản scan có dấu đỏ) của 80 văn bản | ✅ xong | 60/80 có PDF: 25 scan thuần, 20 lai, 15 có lớp chữ; 2.509 trang, 332 MB; 369 s |
| So sánh engine OCR trên mẫu 8 văn bản / 98 trang | ✅ xong | CER không tính chèn: Tesseract bỏ dấu đỏ **1,73%** (2,9 s/trang), ảnh gốc 1,74%, EasyOCR 7,43% (9,4 s/trang, ~12 GB RAM ở 300 dpi) — [`ocr/ket_qua_ocr_so_sanh.md`](../ocr/ket_qua_ocr_so_sanh.md) |
| OCR toàn bộ 60 PDF (Tesseract, bỏ dấu đỏ, 6 tiến trình) | ✅ xong, 3.638 s | 56 PDF phủ đủ: **mất 3,22% text chuẩn**, 1,50% do sai dấu; 4 PDF vbpl chỉ lưu một phần — [`ocr/ket_qua_ocr.md`](../ocr/ket_qua_ocr.md) |
| Chunk 100/200/300/500 từ (A và B) | ✅ dựng chunk xong (12 s) | A300, B_goc trùng tuyệt đối A, B gốc |
| Nhúng 9 chỉ mục thử nghiệm trên GPU (~118 nghìn chunk) | 🔄 đang chạy | A300 330 s, B_goc 441 s (~17 vector/s với chunk 300 từ) |
| Rerank (bge-reranker-v2-m3, Vietnamese_Reranker) × 9 chỉ mục | ⏳ | — |
| Truy hồi trên kho OCR (A300, B thay text chuẩn bằng text OCR) | ⏳ | — |

## Dữ liệu OCR

```
ocr/data/pdf/<id>.pdf      bản PDF gốc vbpl.vn lưu kèm văn bản (phần lớn là bản scan có dấu đỏ)
ocr/data/docs/<id>.txt     text CHUẨN tương ứng (= data/clean_full) — đáp án để chấm OCR
ocr/data/ocr/<cấu hình>/   text OCR + thời gian từng trang
ocr/data/manifest_pdf.csv  id, số hiệu, sha256, số trang, số trang có lớp chữ
```

60 PDF (332 MB) **không nằm trong git** — tải `datn-ocr-pdf.zip` ở release **`ocr-pdf-2026-10-30`**, giải nén tại
gốc repo. Trong git có sẵn 2 bản scan mẫu ở `ocr/data/mau/` để xem dấu đỏ.

PDF lấy từ gateway của Bộ Tư pháp (`vbpl-bientap-gateway.moj.gov.vn`, chỉ mở cho IP Việt Nam), **không đụng
`data/raw`**. Bản PDF thường có thêm phụ lục / biểu mẫu mà text chuẩn không có, nên CER thô bị phình (tới 66%);
độ đo chính là **CER không tính chèn** = (thay thế + xoá) / độ dài text chuẩn.

## Cài môi trường OCR (tách khỏi `.venv` đã ghim)

```bash
"$(uv python find 3.12.13)" -m venv .venv-ocr
.venv-ocr/Scripts/python -m pip install -r requirements-ocr.txt                       # torch cu130 + EasyOCR, 128 s
# Tesseract 5.5.3 không cần quyền admin: micromamba (một tệp exe) + conda-forge          49 s
curl -L -o tools/mm/micromamba.exe https://github.com/mamba-org/micromamba-releases/releases/latest/download/micromamba-win-64
MAMBA_ROOT_PREFIX=tools/mm/root tools/mm/micromamba.exe create -y -p tools/tesseract-env -c conda-forge tesseract
curl -L -o tools/tesseract-env/share/tessdata/vie.traineddata https://github.com/tesseract-ocr/tessdata_best/raw/main/vie.traineddata
```

## Lệnh chạy

```bash
export PYTHONUTF8=1
# OCR
.venv-ocr/Scripts/python -m ocr.tai_pdf                                   # tải PDF gốc + text chuẩn
OMP_THREAD_LIMIT=1 .venv-ocr/Scripts/python -m ocr.quet --engine tesseract --tien-xu-ly bo_do --phan 1/6   # ×6 song song
.venv-ocr/Scripts/python -m ocr.danh_gia                                  # → ocr/ket_qua_ocr.{csv,md}

# Độ dài chunk × rerank
.venv/Scripts/python -m rag.rerank --tai                                  # 2 reranker, ghim revision
export CHUNKS_DIR=thuc_nghiem/data/chunks INDEX_DIR=thuc_nghiem/data/index
.venv/Scripts/python -m thuc_nghiem.chay chunk
NHUNG_DEVICE=cuda .venv/Scripts/python -m rag.chi_muc A100_s0 A200_s0 A300_s0 A500_s0 B100_s0 B200_s0 B300_s0 B500_s0 B_goc_s0
.venv/Scripts/python -m thuc_nghiem.chay danh_gia                         # → thuc_nghiem/ket_qua/metrics.{csv,md}

# Kho OCR
.venv/Scripts/python -m thuc_nghiem.kho_ocr chunk --nguon tesseract_bo_do
NHUNG_DEVICE=cuda .venv/Scripts/python -m rag.chi_muc A300ocr_s0 B_gococr_s0
.venv/Scripts/python -m thuc_nghiem.kho_ocr danh_gia --nguon tesseract_bo_do   # → thuc_nghiem/ket_qua/kho_ocr.md
```

`A<N>`: cửa sổ cố định N từ. `B<N>`: cắt Điều → Khoản → Điểm, khối > N từ thì tách tiếp (tiền tố phân cấp không
tính vào N). Chấm bằng đúng hàm của `eval/chay_truy_hoi.py` trên 110 câu chính, hiệu số kèm bootstrap ghép cặp 95%.
