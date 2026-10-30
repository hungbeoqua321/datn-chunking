# Chất lượng OCR trên bản scan gốc

60 văn bản, 2509 trang; mọi cấu hình chấm trên cùng tập này. CER/WER gộp (tổng lỗi / tổng độ dài text chuẩn). Chi tiết từng văn bản: `ocr/ket_qua_ocr.csv`.

| Cấu hình | CER không tính chèn | CER | WER | CER bỏ dấu | Lỗi do dấu | Giây/trang |
|---|---:|---:|---:|---:|---:|---:|
| tesseract_bo_do | 22.03% | 28.68% | 33.55% | 27.48% | 1.21% | 6.40 |

CER ở đây là cận trên: số trang, dòng chữ ký số và chữ trong dấu giáp lai có trên bản scan nhưng không có trong text chuẩn nên bị tính là lỗi chèn.

## Chỉ tính PDF phủ đủ text chuẩn (ký tự OCR ≥ 80% text chuẩn)

| Cấu hình | Văn bản | CER không tính chèn | CER | Lỗi do dấu |
|---|---:|---:|---:|---:|
| tesseract_bo_do | 56 | 3.22% | 12.20% | 1.50% |

PDF KHÔNG phủ đủ (4) — vbpl chỉ lưu một phần văn bản:

- 95/2015/QH13 (`96117`): 55 trang, OCR 118,700 / chuẩn 267,816 ký tự
- 100/2015/QH13 (`96122`): 41 trang, OCR 89,517 / chuẩn 553,533 ký tự
- 101/2015/QH13 (`96172`): 45 trang, OCR 101,403 / chuẩn 516,644 ký tự
- 222/2026/NĐ-CP (`b6ab9020-8bbe-11f1-b2d0-6b22a52408be`): 77 trang, OCR 154,245 / chuẩn 301,625 ký tự
