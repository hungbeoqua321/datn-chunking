# Chất lượng OCR trên bản scan gốc

155 văn bản, 5743 trang; mọi cấu hình chấm trên cùng tập này. CER/WER gộp (tổng lỗi / tổng độ dài text chuẩn). Chi tiết từng văn bản: `ocr/ket_qua_ocr.csv`.

| Cấu hình | CER không tính chèn | CER | WER | CER bỏ dấu | Lỗi do dấu | Giây/trang |
|---|---:|---:|---:|---:|---:|---:|
| tesseract_bo_do | 20.71% | 31.79% | 36.98% | 30.51% | 1.28% | 5.18 |

CER ở đây là cận trên: số trang, dòng chữ ký số và chữ trong dấu giáp lai có trên bản scan nhưng không có trong text chuẩn nên bị tính là lỗi chèn.

## Chỉ tính PDF phủ đủ text chuẩn (ký tự OCR ≥ 80% text chuẩn)

| Cấu hình | Văn bản | CER không tính chèn | CER | Lỗi do dấu |
|---|---:|---:|---:|---:|
| tesseract_bo_do | 148 | 6.04% | 20.24% | 1.50% |

PDF KHÔNG phủ đủ (7) — vbpl chỉ lưu một phần văn bản:

- 91/2015/QH13 (`95942`): 78 trang, OCR 171,505 / chuẩn 367,913 ký tự
- 92/2015/QH13 (`96115`): 82 trang, OCR 191,693 / chuẩn 494,132 ký tự
- 95/2015/QH13 (`96117`): 55 trang, OCR 118,700 / chuẩn 267,816 ký tự
- 100/2015/QH13 (`96122`): 41 trang, OCR 89,517 / chuẩn 553,533 ký tự
- 101/2015/QH13 (`96172`): 45 trang, OCR 101,403 / chuẩn 516,644 ký tự
- 222/2026/NĐ-CP (`b6ab9020-8bbe-11f1-b2d0-6b22a52408be`): 77 trang, OCR 154,245 / chuẩn 301,625 ký tự
- 127/2026/TT-BTC (`d18bec90-a834-11f1-b084-310b2ec8546f`): 3 trang, OCR 7,407 / chuẩn 230,726 ký tự

Không chấm (1) — vbpl không có text chuẩn, chỉ có PDF (OCR là nguồn chữ duy nhất):

- 50/2019/QH14 (`139882`)
