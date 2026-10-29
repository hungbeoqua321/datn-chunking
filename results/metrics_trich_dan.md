# Độ chính xác trích dẫn — 2026-10-28 06:31

Sinh bằng `python -m eval.cham_trich_dan`. Số thô: `results/metrics_trich_dan.csv`.

Bộ bóc trích dẫn đã kiểm với **nhãn tay 120 dòng, độ khớp 0,825** (`results/kiem_regex_trich_dan.md`) — mọi con số dưới đây mang sẵn sai số đó.

*đúng toàn phần* = phủ hết gold, không thừa; *độ phủ* = tỉ lệ đơn vị gold được trích; *độ chính xác* = tỉ lệ trích dẫn trỏ đúng gold. Cột cuối là *đúng toàn phần* khi so tới cấp **khoản** thay vì chỉ cấp **Điều**.

## 1. Bộ chính — 110 câu × 3 biến thể

| biến thể | n | đạt | từ chối | cắt trần | đúng toàn phần | độ phủ | độ chính xác | đúng toàn phần (khoản) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| A | 110 | 96 | 13 | 1 | **0.182** | 0.250 | 0.233 | 0.127 |
| B | 110 | 103 | 5 | 2 | **0.536** | 0.682 | 0.647 | 0.382 |
| B+ | 110 | 100 | 9 | 1 | **0.445** | 0.559 | 0.528 | 0.227 |

## 2. manh_con — 35 câu

| cấu hình | n | đạt | từ chối | cắt trần | đúng toàn phần | độ phủ | độ chính xác | đúng toàn phần (khoản) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| B | 35 | 27 | 8 | 0 | **0.257** | 0.457 | 0.338 | 0.143 |
| B+ | 35 | 24 | 11 | 0 | **0.200** | 0.257 | 0.224 | 0.114 |
| Eduoi | 35 | 28 | 6 | 1 | **0.286** | 0.400 | 0.338 | 0.171 |
| E2 | 35 | 26 | 9 | 0 | **0.200** | 0.257 | 0.224 | 0.114 |
| E3 | 35 | 25 | 10 | 0 | **0.200** | 0.257 | 0.224 | 0.114 |

### Cắt trần — E2 cạnh B+

Đặc tả E2 sửa ngày 26/10: chỉ chép câu dẫn của **Điều**, không chép câu dẫn của **khoản**. Lý do là mc031: mọi cấu hình bật `dan_khoan` đều chạm trần MAX_TOKENS ở câu đó (5/5), mọi cấu hình tắt nó thì không (5/5); `dan_dieu` không phân biệt được hai nhóm.

| cấu hình | cắt trần | câu nào |
|---|---:|---|
| B | 0 | *(không có)* |
| B+ | 0 | *(không có)* |
| Eduoi | 1 | mc031 |
| E2 | 0 | *(không có)* |

E2 và B+ cùng **0 ca** — cả hai đều không chép câu dẫn khoản vào ngữ cảnh.


### E2 trùng B+ — ghi lại như một kết quả âm

| | trùng / 35 câu |
|---|---:|
| chunk truy hồi được (`chunk_id`) | 0 |
| số từ ngữ cảnh | 30 |
| **câu trả lời, giống từng ký tự** | **29** |

Truy hồi khác nhau hoàn toàn — không câu nào trùng `chunk_id`, vì E2 đọc chỉ mục `Echi_s_s0` còn B+ đọc `B_s0`. Nhưng **29/35 câu trả lời giống nhau từng ký tự**: cả hai đều mở rộng khối lên **Điều cha**, mà tập Điều cha thì trùng nhau, nên chữ đưa cho mô hình là một. Giải mã tham lam (temperature 0) cho ra đúng cùng câu.

**Bước mở rộng lên Điều cha xoá sạch khác biệt do phân đoạn ngữ nghĩa tạo ra.** E2 như đang thiết kế không thể khác B+ một cách đo được — đây là giới hạn của thiết kế, không phải của dữ liệu.


## 4. Kiểm định — McNemar ghép cặp, hiệu chỉnh Holm

Độ đo kiểm định là **trích dẫn đúng toàn phần** (nhị phân từng câu). Hiệu chỉnh Holm tính riêng trong từng bộ.

### Bộ chính, 110 câu

| cặp | p (McNemar) | p sau Holm | kết luận ở mức 0,05 |
|---|---:|---:|---|
| A vs B | 2.78e-09 | 8.34e-09 | **khác biệt có ý nghĩa** |
| A vs B+ | 1.08e-06 | 2.17e-06 | **khác biệt có ý nghĩa** |
| B vs B+ | 0.0525 | 0.0525 | chưa kết luận được |

### manh_con, 35 câu

| cặp | p (McNemar) | p sau Holm | kết luận ở mức 0,05 |
|---|---:|---:|---|
| B+ vs Eduoi | 0.453 | 1 | chưa kết luận được |
| Eduoi vs E2 | 0.453 | 1 | chưa kết luận được |
| Eduoi vs E3 | 0.453 | 1 | chưa kết luận được |
| B vs B+ | 0.688 | 1 | chưa kết luận được |
| B vs E2 | 0.688 | 1 | chưa kết luận được |
| B vs E3 | 0.688 | 1 | chưa kết luận được |
| B vs Eduoi | 1 | 1 | chưa kết luận được |
| B+ vs E2 | 1 | 1 | chưa kết luận được |
| B+ vs E3 | 1 | 1 | chưa kết luận được |
| E2 vs E3 | 1 | 1 | chưa kết luận được |


## 3. E3 — theo dẫn chiếu tường minh, 26 câu bộ chính

26 câu = 9 nhóm `dan_chieu` + 17 nhóm `xuyen_khoan`, đúng hai nhóm có dẫn chiếu để theo. **E3** nền E2 (mở rộng lên Điều cha), **E3b** nền B (không mở rộng).

### Cả 26 câu

| | n | đạt | từ chối | cắt trần | trích dẫn đúng | trả lời thiếu |
|---|---:|---:|---:|---:|---:|---:|
| B | 26 | 23 | 2 | 1 | **0.577** | 0.346 |
| B+ | 26 | 23 | 3 | 0 | **0.500** | 0.423 |
| E3 | 26 | 23 | 3 | 0 | **0.577** | 0.385 |
| E3b | 26 | 22 | 3 | 1 | **0.423** | 0.385 |

| hiệu số | trích dẫn đúng | trả lời thiếu |
|---|---|---|
| E3 trừ B | +0.000 [-0.154; +0.154] | +0.038 [-0.154; +0.192] |
| E3b trừ B | -0.154 [-0.308; -0.038] | +0.038 [-0.077; +0.154] |
| E3 trừ B+ | +0.077 [+0.000; +0.192] | -0.038 [-0.115; +0.000] |
| E3b trừ B+ | -0.077 [-0.231; +0.077] | -0.038 [-0.192; +0.115] |

### Riêng 9 câu `dan_chieu`

| | n | đạt | từ chối | cắt trần | trích dẫn đúng | trả lời thiếu |
|---|---:|---:|---:|---:|---:|---:|
| B | 9 | 8 | 1 | 0 | **0.222** | 0.778 |
| B+ | 9 | 7 | 2 | 0 | **0.222** | 0.778 |
| E3 | 9 | 7 | 2 | 0 | **0.222** | 0.778 |
| E3b | 9 | 8 | 1 | 0 | **0.111** | 0.667 |

| hiệu số | trích dẫn đúng | trả lời thiếu |
|---|---|---|
| E3 trừ B | +0.000 [+0.000; +0.000] | +0.000 [+0.000; +0.000] |
| E3b trừ B | -0.111 [-0.333; +0.000] | -0.111 [-0.333; +0.000] |
| E3 trừ B+ | +0.000 [+0.000; +0.000] | +0.000 [+0.000; +0.000] |
| E3b trừ B+ | -0.111 [-0.333; +0.000] | -0.111 [-0.333; +0.000] |

