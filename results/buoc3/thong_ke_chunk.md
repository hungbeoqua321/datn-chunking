# Thống kê chunk (bước 3)

Tập: 80 văn bản (`data/manifest.csv`). Seed 0 = cửa sổ bắt đầu từ từ đầu tiên (đúng đề).

| Phương pháp | Số chunk | Trung vị từ | Max từ | Min từ | Fallback | VB mất chunk | Vượt 512 token | Từ tiền tố TB | Ký tự không phủ |
|---|---|---|---|---|---|---|---|---|---|
| A | 5.172 | 300 | 300 | 6 | 0.0% | 0 | 6 (0.1%) | 0 | 0 |
| A+ | 5.172 | 300 | 300 | 6 | 0.0% | 0 | 17 (0.3%) | 16 | 0 |
| B | 12.718 | 97 | 372 | 3 | 0.4% | 0 | 44 (0.3%) | 38 | 0 |
| A_H | 5.172 | 300 | 300 | 6 | 0.0% | 0 | 65 (1.3%) | 36 | 0 |
| B- | 12.718 | 97 | 372 | 3 | 0.4% | 0 | 4 (0.0%) | 0 | 0 |
| C | 5.640 | 281 | 300 | 10 | 0.0% | 0 | 5 (0.1%) | 0 | 0 |
| D | 7.673 | 199 | 385 | 25 | 0.1% | 0 | 7 (0.1%) | 0 | 0 |

- **Số từ** tính trên phần nội dung (không tính tiền tố). **Vượt 512 token**: đếm bằng tokenizer của halong_embedding trên chuỗi đem nhúng (tiền tố + nội dung) — phần vượt bị cắt mất khi nhúng.
- **Ký tự không phủ** = ký tự không trắng của văn bản không thuộc chunk nào (phải = 0: không để mất văn bản).
- C (theo dấu câu) và D (theo ngữ nghĩa) là hai baseline của đề cương, cùng họ không nhìn cấu trúc với A; chỉ đo truy hồi.
- A+, A_H, B− là đối chứng chỉ đo truy hồi; B+ dùng chính chunk của B.
- B: ngưỡng 350 từ đo từ dòng "Điều N"; dòng tiêu đề Chương/Mục đứng ngay trước được gắn vào đầu chunk (để không mất ký tự nào) nhưng không tính vào ngưỡng — vì vậy số từ lớn nhất của B có thể nhỉnh hơn ngưỡng.

## B theo tầng

- Cả Điều (≤ 350 từ): 4.847 chunk; tách theo khoản: 5.901; tách tiếp theo điểm: 1.837; ngoài Điều (phần đầu văn bản, chú thích VBHN): 86; fallback (văn bản không có Điều): 47.
- Chunk dưới 50 từ: B 2.781 (21.9%) — so với A 16 (chỉ là đuôi văn bản). Đây là dữ liệu cho nhược điểm 6 (chunk quá nhỏ mất ngữ cảnh).
- Fallback theo nhóm (chunk fallback / tổng chunk của nhóm): khong_dieu: 47/47, luat: 0/8167, nd_tt: 0/3252, sua_doi: 0/579, vbhn: 0/673

## Số chunk theo seed

| Phương pháp | seed 0 | seed 1 | seed 2 | seed 3 |
|---|---|---|---|---|
| A | 5.172 | 5.215 | 5.215 | 5.206 |
| B | 12.718 | 12.724 | 12.723 | 12.721 |

- **B không phụ thuộc seed:** số chunk qua 4 seed chỉ lệch 6 trên 12.718; seed 1: 12.671/12.724 chunk trùng nguyên văn seed 0, 53 chunk khác (53/53 là cửa sổ fallback của văn bản không có Điều); seed 2: 12.672/12.723 chunk trùng nguyên văn seed 0, 51 chunk khác (51/51 là cửa sổ fallback của văn bản không có Điều); seed 3: 12.672/12.721 chunk trùng nguyên văn seed 0, 49 chunk khác (49/49 là cửa sổ fallback của văn bản không có Điều). Vì vậy B và B− chỉ nhúng một lần (seed 0).
- **A trần** chạy 4 seed, chỉ đo truy hồi (không sinh câu trả lời), để chứng minh dịch điểm bắt đầu cửa sổ chỉ là nhiễu. A+, A_H, B−, B+ và khâu sinh: một seed (0).

## Nhãn Điều/khoản/điểm của B có đúng không

Đối chiếu với cây cấu trúc của chính vbpl.vn (`data/raw/<id>.cay.json`, độc lập với regex của B): chunk sai khi đơn vị nó mang nhãn không tồn tại trong cây hoặc không chồng lên chunk. Chunk có nhãn mà cây thiếu node (node chỉ là tham chiếu "$n", hoặc cây không có cấp con) ghi là không kiểm được.

| Nhóm | Sai / kiểm được | Tỉ lệ sai | Không kiểm được |
|---|---|---|---|
| luat | 12 / 6124 | 0.2% | 1767 |
| nd_tt | 0 / 2321 | 0.0% | 896 |
| sua_doi | 4 / 272 | 1.5% | 297 |
| vbhn | 11 / 343 | 3.2% | 310 |

- Văn bản sửa đổi, đo bằng bộ dò khối trích dẫn mở/đóng (cách thứ hai): 32/569 chunk (5.6%) có nhãn lấy từ dòng nằm trong trích dẫn.
- B bỏ qua dòng nằm trong khối trích dẫn nguyên văn khi dò Điều/khoản/điểm (chunking/structural.py, dong_trich_dan). Trước khi sửa: sửa đổi 35,7% theo cây, 52,0% theo bộ dò mở/đóng (commit trước).
- Văn bản ban hành kèm theo (Quy chế… đánh số lại từ Điều 1): Điều trong đó mang không gian số riêng (trường kem_theo, tiền tố "> Quy chế … > Điều N"); cây vbpl không có node cho phần này nên các chunk đó ghi là không kiểm được. Trước khi sửa: VBHN 11,7% (43/368).
- Bộ đo theo cây tính là SAI cả khi nhãn Điều đúng với dòng "Điều N" trong văn bản nhưng cây vbpl thiếu node (cây của VBHN không đồng bộ với nội dung hợp nhất ở các Điều đã sửa, có chú thích [n]) — tỉ lệ trên là cận trên.
- Quyết định: VBHN 3.2% ≤ 10% → giữ trong phần chấm trích dẫn chính.
