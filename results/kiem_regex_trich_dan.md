# Kiểm bộ bóc trích dẫn bằng regex so với nhãn tay

Nhãn tay **120/120 dòng**, chấm **hai vòng**: vòng một trên bản regex cũ, vòng hai trên bản đã sửa. Nguồn: `eval/nhan_trich_dan.md` (nhãn), `results/pilot_tra_loi.jsonl` (câu trả lời). Sinh bằng `python -m eval.ap_nhan`.

Độ khớp = tỉ lệ dòng người đọc chấm **Đúng**; khoảng tin cậy **Wilson 95%**.

## 1. Độ khớp từng biến thể sau khi sửa (đã giải mã)

| biến thể | mã mù | n | Đúng | Thiếu | Thừa | Sai | độ khớp | Wilson 95% |
|---|---|---:|---:|---:|---:|---:|---:|---|
| A | Z | 40 | 32 | 7 | 1 | 0 | **0.800** | [0.652; 0.895] |
| B | Y | 40 | 34 | 6 | 0 | 0 | **0.850** | [0.709; 0.929] |
| B+ | X | 40 | 33 | 5 | 1 | 1 | **0.825** | [0.681; 0.913] |
| **TỔNG** | — | 120 | 99 | 18 | 2 | 1 | **0.825** | [0.747; 0.883] |

## 1b. Trước và sau khi sửa bộ bóc

Hai lần chấm tay trên **cùng 120 dòng**: lần đầu chấm bản regex cũ, lần sau chấm bản đã sửa. Cùng một người đọc, cùng một tiêu chí, nên so được với nhau.

| | độ khớp | Wilson 95% | Đúng | Thiếu | Thừa | Sai |
|---|---:|---|---:|---:|---:|---:|
| regex cũ | **0.717** | [0.630; 0.790] | 86 | 18 | 2 | 14 |
| **regex đã sửa** | **0.825** | [0.747; 0.883] | 99 | 18 | 2 | 1 |

## 1c. Ba mẫu số hiệu đã sửa

| mẫu | số dòng dính | A | B | B+ | nhãn sau khi sửa |
|---|---:|---:|---:|---:|---|
| ký hiệu có chữ thường (CT-TTg) | 11 | 3 | 4 | 4 | Đúng 7, Thiếu 4 |
| số 0 đầu (09/…) | 6 | 2 | 2 | 2 | Đúng 6 |
| số hiệu kiểu cũ (9367 TC/PC) | 3 | 1 | 1 | 1 | Đúng 3 |

**Độ khớp cuối cùng: 0.825.** Phần Thiếu còn sót toàn là điểm và khoản viết bằng chữ (14/21 dòng lỗi), nhỏ và chia đều ba biến thể — **A 8 · B 6 · B+ 7**. Không chấm lại nữa; con số này là con số cuối dùng cho báo cáo.


## 2. Dòng Thiếu hoặc Sai — nhóm theo biến thể

Mỗi dòng ghi **chuỗi regex bóc được** và **chuỗi người đọc thấy**, để soi mẫu định dạng nào regex hụt một cách hệ thống.

### A — 7 dòng

| mã | nhãn | regex bóc được | người đọc thấy |
|---|---|---|---|
| 014 | Thiếu | 334/CT-TTG Điều 2; 334/CT-TTG Điều 3; 334/CT-TTG Điều 10 | 334/CT-TTg Điều 2; Điều 3; Điều 10 |
| 051 | Thiếu | 101/2015/QH13 Điều 132 khoản 2; 101/2015/QH13 Điều 248 khoản 2 | 101/2015/QH13 Điều 248 khoản 2; Điều 132 khoản 2 của Bộ luật này |
| 058 | Thiếu | 1408/CT-TTG Điều 2 điểm a; 1408/CT-TTG Điều 2 điểm b | 1408/CT-TTg Điều 2 khoản a b |
| 068 | Thiếu | 19/2021/TT-BTC Điều 4 khoản 1 điểm a; 19/2021/TT-BTC Điều 4 khoản 1 điểm b; 19/2021/TT-BTC Điều 4 khoản 1 điểm c | 19/2021/TT-BTC Điều 4 khoản 1 điểm a b c |
| 073 | Thiếu | 101/2015/QH13 Điều 52 khoản 1; 101/2015/QH13 Điều 49 | 101/2015/QH13 Điều 52 khoản 1 điểm a b; Điều 49 của Bộ luật này |
| 076 | Thiếu | 10/2026/VBHN-NĐ-BNV Điều 73; 300/2026/NĐ-CP Điều 2 điểm b | 10/2026/VBHN-NĐ-BNV Điều 73; 300/2026/NĐ-CP Điều 2 khoản b |
| 095 | Thiếu | 200/2026/NĐ-CP Điều 9 khoản 4 | 200/2026/NĐ-CP Điều 9 khoản 4 điểm a b c d |

### B — 6 dòng

| mã | nhãn | regex bóc được | người đọc thấy |
|---|---|---|---|
| 049 | Thiếu | 135/2025/QH15 Điều 55 khoản 1 điểm a; 135/2025/QH15 Điều 55 khoản 1 điểm b; 135/2025/QH15 Điều 55 khoản 1 điểm c | 135/2025/QH15 Điều 55 khoản 1 điểm a b c |
| 053 | Thiếu | 10/2026/VBHN-NĐ-BNV Điều 64 khoản 1; 10/2026/VBHN-NĐ-BNV Điều 64 khoản 1 điểm e; 10/2026/VBHN-NĐ-BNV Điều 66 | 10/2026/VBHN-NĐ-BNV Điều 66; Điều 64 khoản 1 điểm d đ e và khoản 2 Điều này, nội bộ |
| 064 | Thiếu | 300/2026/NĐ-CP Điều 13; 300/2026/NĐ-CP Điều 4 khoản 1 | 300/2026/NĐ-CP Điều 4 khoản 1; Điều 13 của Nghị định này |
| 084 | Thiếu | 200/2026/NĐ-CP Điều 9 khoản 4 | 200/2026/NĐ-CP Điều 9 khoản 4 điểm a b c d |
| 111 | Thiếu | 1408/CT-TTG Điều 3 điểm b | 1408/CT-TTg Điều 3 khoản b |
| 112 | Thiếu | 101/2015/QH13 Điều 128 khoản 4 điểm a; 101/2015/QH13 Điều 128 khoản 4; 101/2015/QH13 Điều 178 | 101/2015/QH13 Điều 128 khoản 4; 101/2015/QH13 Điều 178; điểm a khoản 4 Điều 128 nội bộ |

### B+ — 6 dòng

| mã | nhãn | regex bóc được | người đọc thấy |
|---|---|---|---|
| 004 | Thiếu | 107/2026/TT-BTC Điều 11 điểm e | 107/2026/TT-BTC Điều 11 khoản e |
| 018 | Thiếu | 80/2025/QH Điều 2 khoản 2; 10/2026/VBHN-NĐ-BNV Điều 64 khoản 2 | 10/2026/VBHN-NĐ-BNV Điều 64 khoản 2; Điều 2 khoản 2 của Nghị định này |
| 028 | Sai | 32/2024/QH15 Điều 43 khoản 2 điểm a; 32/2024/QH15 Điều 43 khoản 1; 24/QH15 Điều 43 khoản 2 điểm a | 32/2024/QH15 Điều 43 khoản 2 điểm a; Điều 43 khoản 1 cùng luật; 32/24/QH15 Điều 43 khoản 2 điểm a |
| 052 | Thiếu | 1408/CT-TTG Điều 3 điểm b | 1408/CT-TTg Điều 3 khoản b |
| 061 | Thiếu | 200/2026/NĐ-CP Điều 9 khoản 4; 200/2026/NĐ-CP Điều 15 khoản 3 | 200/2026/NĐ-CP Điều 15 khoản 3; Điều 9 khoản 4 điểm a b c d của Nghị định này |
| 109 | Thiếu | 200/2026/NĐ-CP Điều 5 điểm g | 200/2026/NĐ-CP Điều 5 khoản g |

