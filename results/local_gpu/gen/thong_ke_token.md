# Thống kê token các lần gọi mô hình sinh

Nguồn: `results\local_gpu\gen\nhat_ky_goi.jsonl` (1248 lần gọi). Chạm trần = token_prompt + token_tra_loi ≥ n_ctx; bị cắt = ly_do_dung là `length`. Hai cột này khác 0 nghĩa là job đã bị dừng ở lần gọi đó.

| Biến thể | Lần gọi | token_prompt trung vị | token_prompt max | max prompt + trả lời | n_ctx | Biên nhỏ nhất tới trần | Chạm trần | Bị cắt | Số khối TV | Từ ngữ cảnh TV | Giây TV |
|---|---|---|---|---|---|---|---|---|---|---|---|
| local_A | 110 | 1883 | 2445 | 2565 | 4096 | 1531 | 0 | 1 | 4 | 1200 | 3 |
| local_B | 110 | 2030 | 2684 | 2794 | 4096 | 1302 | 0 | 1 | 6 | 1114 | 3 |
| local_B+ | 110 | 1729 | 2684 | 2782 | 4096 | 1314 | 0 | 3 | 2 | 1024 | 3 |
| local_C | 110 | 1761 | 2513 | 2593 | 4096 | 1503 | 0 | 2 | 4 | 1102 | 3 |
| local_D | 110 | 1770 | 2486 | 2601 | 4096 | 1495 | 0 | 2 | 5 | 1078 | 3 |
| local_E | 110 | 2040 | 2684 | 2794 | 4096 | 1302 | 0 | 1 | 6 | 1122 | 3 |
| local_E2 | 110 | 1729 | 2684 | 2782 | 4096 | 1314 | 0 | 3 | 2 | 1024 | 3 |
| local_E3 | 110 | 1785 | 2684 | 2782 | 4096 | 1314 | 0 | 2 | 3 | 1116 | 3 |
| local_manh_con_B | 31 | 2048 | 2467 | 2675 | 4096 | 1421 | 0 | 1 | 7 | 1131 | 4 |
| local_manh_con_B+ | 31 | 1657 | 2289 | 2374 | 4096 | 1722 | 0 | 0 | 1 | 1000 | 3 |
| local_manh_con_E2 | 30 | 1670 | 2289 | 2374 | 4096 | 1722 | 0 | 0 | 1 | 1004 | 3 |
| local_manh_con_E3 | 30 | 1748 | 2289 | 2374 | 4096 | 1722 | 0 | 0 | 2 | 1142 | 3 |
| local_manh_con_E3b | 30 | 1984 | 2467 | 2675 | 4096 | 1421 | 0 | 1 | 6 | 1132 | 3 |
| local_manh_con_Echi_s | 30 | 2014 | 2467 | 2675 | 4096 | 1421 | 0 | 0 | 7 | 1112 | 4 |
| local_manh_con_Eduoi | 31 | 1968 | 2561 | 2712 | 4096 | 1384 | 0 | 1 | 6 | 1104 | 3 |
| local_manh_con_Etat_d | 31 | 1984 | 2561 | 2712 | 4096 | 1384 | 0 | 1 | 6 | 1096 | 3 |
| local_manh_con_Etat_k | 31 | 1991 | 2467 | 2675 | 4096 | 1421 | 0 | 0 | 7 | 1107 | 4 |
| local_manh_con_Etat_n | 31 | 1965 | 2561 | 2712 | 4096 | 1384 | 0 | 1 | 6 | 1105 | 4 |
| local_manh_con_Etat_s | 31 | 1992 | 2561 | 2712 | 4096 | 1384 | 0 | 2 | 6 | 1113 | 3 |
| local_manh_con_Etren | 31 | 1992 | 2561 | 2712 | 4096 | 1384 | 0 | 1 | 6 | 1110 | 4 |
