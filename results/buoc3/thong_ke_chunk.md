# Thống kê chunk (bước 3)

Tập: 80 văn bản (`data/manifest.csv`). Seed 0 = cửa sổ bắt đầu từ từ đầu tiên (đúng đề).

| Phương pháp | Số chunk | Trung vị từ | Max từ | Min từ | Fallback | VB mất chunk | Vượt 512 token | Từ tiền tố TB | Ký tự không phủ |
|---|---|---|---|---|---|---|---|---|---|
| A | 5.172 | 300 | 300 | 6 | 0.0% | 0 | 6 (0.1%) | 0 | 0 |
| A+ | 5.172 | 300 | 300 | 6 | 0.0% | 0 | 17 (0.3%) | 16 | 0 |
| B | 13.035 | 94 | 372 | 3 | 0.4% | 0 | 41 (0.3%) | 38 | 0 |
| A_H | 5.172 | 300 | 300 | 6 | 0.0% | 0 | 64 (1.2%) | 36 | 0 |
| B- | 13.035 | 94 | 372 | 3 | 0.4% | 0 | 4 (0.0%) | 0 | 0 |

- **Số từ** tính trên phần nội dung (không tính tiền tố). **Vượt 512 token**: đếm bằng tokenizer của halong_embedding trên chuỗi đem nhúng (tiền tố + nội dung) — phần vượt bị cắt mất khi nhúng.
- **Ký tự không phủ** = ký tự không trắng của văn bản không thuộc chunk nào (phải = 0: không để mất văn bản).
- A_H, B− là đối chứng chỉ đo truy hồi; B+ dùng chính chunk của B.
- B: ngưỡng 350 từ đo từ dòng "Điều N"; dòng tiêu đề Chương/Mục đứng ngay trước được gắn vào đầu chunk (để không mất ký tự nào) nhưng không tính vào ngưỡng — vì vậy số từ lớn nhất của B có thể nhỉnh hơn ngưỡng.

## B theo tầng

- Cả Điều (≤ 350 từ): 4.785 chunk; tách theo khoản: 6.190; tách tiếp theo điểm: 1.927; ngoài Điều (phần đầu văn bản, chú thích VBHN): 86; fallback (văn bản không có Điều): 47.
- Chunk dưới 50 từ: B 2.996 (23.0%) — so với A 16 (chỉ là đuôi văn bản). Đây là dữ liệu cho nhược điểm 6 (chunk quá nhỏ mất ngữ cảnh).
- Fallback theo nhóm (chunk fallback / tổng chunk của nhóm): khong_dieu: 47/47, luat: 0/8185, nd_tt: 0/3252, sua_doi: 0/878, vbhn: 0/673

## Số chunk theo seed

| Phương pháp | seed 0 | seed 1 | seed 2 | seed 3 |
|---|---|---|---|---|
| A | 5.172 | 5.215 | 5.215 | 5.206 |
| A+ | 5.172 | 5.215 | 5.215 | 5.206 |
| B | 13.035 | 13.041 | 13.040 | 13.038 |
