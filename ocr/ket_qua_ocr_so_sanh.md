# Chất lượng OCR trên bản scan gốc

8 văn bản, 98 trang; mọi cấu hình chấm trên cùng tập này. CER/WER gộp (tổng lỗi / tổng độ dài text chuẩn). Chi tiết từng văn bản: `ocr/ket_qua_ocr.csv`.

| Cấu hình | CER không tính chèn | CER | WER | CER bỏ dấu | Lỗi do dấu | Giây/trang |
|---|---:|---:|---:|---:|---:|---:|
| tesseract_bo_do | 1.73% | 16.97% | 22.71% | 15.73% | 1.24% | 2.91 |
| tesseract_goc | 1.74% | 17.17% | 23.01% | 15.93% | 1.24% | 3.03 |
| easyocr_goc | 7.43% | 23.31% | 28.62% | 22.49% | 0.82% | 9.37 |

CER ở đây là cận trên: số trang, dòng chữ ký số và chữ trong dấu giáp lai có trên bản scan nhưng không có trong text chuẩn nên bị tính là lỗi chèn.
