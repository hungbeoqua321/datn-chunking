# Kiểm cài sạch theo README — 2026-11-03

Cài vào thư mục trống `E:\WEB\cai_sach` trên chính máy local (Windows 11, Git Bash), làm đúng thứ tự README mục 1–2. Bản CPU (`requirements.txt`), mã ở commit a60e33f.

| bước | kết quả | thời gian thật |
|---|---|---:|
| ① clone + autocrlf | thoát 0 | 8 s |
| ② venv | thoát 0 — **lệch README**: `python` trên PATH là bí danh Microsoft Store, báo `cannot execute: required file not found`; dùng CPython 3.12.13 có sẵn của uv | 9 s |
| ③ `pip install -r requirements.txt` | thoát 0 | 381 s |
| ④ `tools/tai_mo_hinh.py` | thoát 0 | 357 s |
| ④ tải `docs.zip` (release `du-lieu`) + `sha256sum -c` | `docs.zip: OK` | 63 s |
| ④ giải nén | thoát 0 | 9 s |
| `python -m rag.nhung --kiem` | `OK — khớp model card (lệch điểm lớn nhất 0.0000)` | 37 s |
| `python -m pytest -q` | 140 passed | 8 s |
| `python -m rag.kiem_chi_muc` | `chỉ mục khớp tệp chunk: 17/17` | 7 s |
| `python -m eval.chay_truy_hoi` (KET_QUA_DIR riêng) | thoát 0 (lần đầu thoát 1 vì thư mục KET_QUA_DIR riêng chưa tạo — `FileNotFoundError … metrics_truy_hoi.csv`; tạo thư mục rồi chạy lại) | 47 s |

## Truy hồi B, 110 câu

| | R@5 | R@1200 từ | MRR |
|---|---:|---:|---:|
| cài sạch | 0,791 | 0,782 | 0,579 |
| local (`results/local_gpu/metrics_truy_hoi.csv`) | 0,791 | 0,782 | 0,579 |
| VPS (`results/metrics_truy_hoi.csv`) | 0,791 | 0,782 | 0,579 |

So toàn bộ `metrics_truy_hoi.csv`:

- với local: 280/280 điểm chung trùng tuyệt đối (B bộ chính 40/40), 225/225 hiệu số trùng giá trị; cận khoảng tin cậy lệch tối đa 0,020 vì local tính bootstrap bằng `eval.bang_day_du`, cài sạch bằng `eval.chay_truy_hoi` (hai đoạn mã rút mẫu khác thứ tự).
- với VPS (cùng script): 448/448 điểm chung, B 64/64 trùng; lệch 9 giá trị, đều của D (VD D gold trùng ranh giới MRR 0,5009 sạch / 0,4944 VPS). Cài sạch trùng local ở các giá trị D này; vì sao bảng VPS lệch thì chưa xác định.
