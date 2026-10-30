# Tái lập tầng truy hồi trên máy cá nhân

Chạy lại `python -m eval.chay_truy_hoi` trên máy cá nhân, ghi ra thư mục này thay vì `results/`
(`KET_QUA_DIR=thuc_nghiem/tai_lap`), để so với số gốc của VPS mà không ghi đè.

| | VPS (số gốc trong `results/`) | Máy cá nhân |
|---|---|---|
| Máy | aarch64 Neoverse-N1, Ubuntu 22.04 | x86_64 i5-11400H, Windows 11 |
| Python | 3.12.13 | 3.12.13 (uv, python-build-standalone) |
| torch | 2.14.1+cpu | 2.14.1+cu130, nhưng nhúng câu hỏi vẫn trên **CPU** (`NHUNG_DEVICE` mặc định) |
| Chỉ mục | — | chép nguyên từ release `du-lieu-2026-10-29`, `rag.kiem_chi_muc` thoát 0 (17/17) |

Chạy mất 46 s.

## Kết quả

`metrics_truy_hoi.csv`: **926/953 dòng khớp tuyệt đối** với `results/metrics_truy_hoi.csv`.
A, A trên 4 seed, B, C, mọi cấu hình E trên bộ manh_con, mọi tập con và khoảng tin cậy bootstrap đều trùng
tới chữ số cuối.

27 dòng lệch đều thuộc **D** (cùng hai hiệu `B − D`, `D − A` suy ra từ D). Lệch lớn nhất là **1 câu / 110**:

| Dòng | VPS | Máy cá nhân |
|---|---|---|
| D, tất cả, R@1 | 0,4091 | 0,4182 |
| D, tất cả, MRR | 0,5451 | 0,5496 |
| D, nhóm don_gian, R@1 | 0,44 | 0,46 |

## Nguyên nhân: hoà điểm tuyệt đối, không phải sai số float

Ở D có những câu mà chunk hạng 1 và hạng 2 có điểm **bằng nhau tuyệt đối** (khoảng cách 0). Lý do là hai chunk
**cùng nội dung** nhưng thuộc hai văn bản khác nhau (bản cũ / bản mới của cùng một văn bản). Ví dụ q010, q015,
q046, q048, q053. Khi hoà, thứ tự do `np.argpartition` + `np.argsort` (không ổn định) quyết định, mà thứ tự
này khác nhau giữa numpy trên ARM và x86. Gold trỏ vào một `doc_id` cụ thể nên R@1 đổi.

Vector chỉ mục giống hệt nhau, và các phương pháp khác không lệch. Điều này loại trừ khả năng do vector câu hỏi
lệch ở chữ số cuối.

Không sửa `rag/truy_hoi.py` vì sửa là đổi số của đồ án. Muốn kết quả độc lập nền tảng thì phải phá hoà bằng một
khoá ổn định (ví dụ thứ tự chunk trong chỉ mục: `np.lexsort((idx, -s))`).
