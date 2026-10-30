# Bước 0 trên máy local — tái lập trước khi chạy gì mới

Ngày chạy 2026-10-30. Mọi chunk và chỉ mục dựng lại vào `thuc_nghiem/tai_lap_gpu/` (lệnh: `thuc_nghiem/tai_lap_gpu/chay.sh`,
nhật ký `nhat_ky.txt`); `data/` và `results/` của VPS không bị đụng.

## 1. Kiểm thử

`python -m pytest -q` → **140 passed, 0 failed** (8 s).

## 2. Chốt chặn chỉ mục

`python -m rag.kiem_chi_muc` → **17/17 khớp**, mã thoát 0 — cả trên `data/index` (bản VPS) lẫn `thuc_nghiem/tai_lap_gpu/index`
(bản dựng lại). B_s1..3 cố ý không nhúng như trên VPS.

## 3. Vân chunk so với VPS

**20/20 tệp trùng tuyệt đối** — vân (sha1 toàn bộ chuỗi đem nhúng, đúng thứ tự) và từng chunk cả metadata: A (4 seed), A+, A_H,
B (4 seed), B−, C, D, 7 cấu hình E. Bảng: [`thuc_nghiem/tai_lap_gpu/van_chunk.md`](../../thuc_nghiem/tai_lap_gpu/van_chunk.md).

D và tầng semantic của E cắt theo vector cụm câu; ở đây vector đó tính lại **trên GPU từ bộ đệm rỗng** (47.729 cụm câu cho D) mà
ranh giới vẫn trùng 100% — sai số số thực GPU/CPU không làm dịch ranh giới nào.

Ghi chú: 4 trường (`cau_dan_lap`, `kem_theo`, `vi_tri_manh`, `tong_so_manh`) thêm vào `chunking/base.py` cùng phương pháp E
(3f66faf), sau khi VPS dựng chunk A/B/C — bản VPS thiếu trường, bản mới ghi giá trị rỗng. Phép so coi rỗng ≡ thiếu.

## 4. Nhúng lại toàn bộ trên GPU + truy hồi 110 câu

Nhúng 17 chỉ mục trên RTX 2050: **3.541 s** (A ~315 s/seed ≈ 17 chunk/s; các cấu hình E 23–88 s nhờ bộ đệm theo nội dung).
Dựng chunk (gồm nhúng cụm câu D, E): 718 s. Truy hồi 110 câu + manh_con: 28 s.

| Recall@5 (110 câu) | VPS | Local GPU | Lệch |
|---|---:|---:|---:|
| A | 0,691 | 0,691 | 0 |
| C | 0,754 (0,7545) | 0,755 (0,7545) | 0 — cùng 83/110, chỉ khác cách làm tròn khi viết tay |
| D | 0,709 | 0,709 | 0 |
| B | 0,791 | 0,791 | 0 |

So từng dòng `metrics_truy_hoi.csv` (952 dòng số): **925/952 trùng tuyệt đối**. 27 dòng lệch đều dính D (9 dòng điểm của D, 9 dòng
B − D, 9 dòng D − A): R@1 D 0,4091 → 0,4182 = **đúng 1 câu/110**, do hoà điểm tuyệt đối giữa hai chunk cùng nội dung ở bản cũ /
bản mới của một văn bản — numpy x86 và ARM phá hoà khác nhau (phân tích: `thuc_nghiem/tai_lap/GHI_CHU.md`). Kết quả GPU này
**trùng 0 dòng khác** với lần tái lập trước dùng chính vector VPS → vector GPU không đổi thứ hạng nào. Mọi lệch đều < 0,02.

## 5. Khối 0 — môi trường

| | |
|---|---|
| CPU | Intel Core i5-11400H, 6 nhân / 12 luồng |
| GPU | NVIDIA GeForce RTX 2050, **4 GB VRAM**, driver 621.01, CUDA 13 |
| RAM | 15,7 GB |
| Hệ điều hành | Windows 11, Python 3.12.13, torch 2.14.1+cu130 |
| Mô hình nhúng | `contextboxai/halong_embedding` @ b5777603 (768 chiều), chạy GPU |
| Mô hình sinh | Qwen3-4B-Instruct-2507, GGUF **Q4_0**, llama.cpp b11577 (cbe28bb3) bản CUDA, `-ngl 99` (mọi lớp lên GPU) |
| n_ctx | 4096, 1 slot, nhiệt độ 0, seed 42, MAX_TOKENS 384 — cờ y hệt `tools/chay-llm.sh` (`tools/chay-llm-gpu.sh` chỉ thêm `-ngl 99`) |
| VRAM mô hình sinh | 3,0 GB (mô hình nhúng truy vấn chạy CPU khi sinh để không tràn 4 GB) |
| **Nhịp sinh, 10 câu thật (B, bộ chính)** | **3,8 s/câu** trung bình, trung vị 3,0 s; ~22 token/s; prompt trung vị 2.034 token, trả lời 64 token; 0 cắt trần. VPS: trung vị 102 s/câu → nhanh ~27 lần |

## Điều phải biết trước bước 1: sinh KHÔNG trùng VPS từng chữ

Cùng 10 câu, **ngữ cảnh đưa vào mô hình trùng 10/10** với VPS, nhưng **câu trả lời chỉ trùng từng ký tự 6/10**, tập trích dẫn bóc
được trùng 7/10. Lý do: cùng tệp Q4_0, nhưng kernel CUDA khác kernel CPU ARM → logit lệch rất nhỏ, giải mã tham lam rẽ nhánh ở
token sát nút. Ví dụ q011: VPS dẫn "Điều 286 khoản 2", local dẫn "Điều 286 khoản 1"; q004: local bỏ phần diễn giải, chỉ ghi căn cứ.

Trên GPU, sinh là **tất định**: chạy lại đúng 10 câu đó lần hai → trùng tuyệt đối 10/10. Vậy số local tái lập được trên máy local,
nhưng tầng trích dẫn local **không so từng câu được** với tầng trích dẫn VPS — chỉ so được theo phân phối, và chênh lệch giữa hai
máy là một nguồn nhiễu cùng cỡ với nhiễu đổi seed (bước 4.1 sẽ đo cỡ đó).
