# Nhật ký sửa lỗi

Phụ lục của quyển. Mỗi mục ghi: phát hiện ngày nào, lệch ở đâu, **vì sao các lần kiểm trước lọt**,
và sửa thế nào. Mục đích không phải kể công sửa lỗi mà là cho người đọc thấy chỗ nào trong quy
trình từng không đáng tin, và cái gì đã được dựng lên để nó không lặp lại.

---

## 2026-10-20 — Chỉ mục `Btru_s0` (B−) lệch tệp chunk ở 2 chunk

### Lệch ở đâu

Chỉ mục `data/index/Btru_s0/` và tệp `data/chunks/Btru_s0.jsonl` **cùng có đúng 12.718 chunk**,
nhưng **2 chunk khác nội dung**, ở vị trí 12422 và 12423, đều thuộc văn bản **56/VBHN-BCT**
(văn bản hợp nhất của 72/2010/QĐ-TTg).

Chỗ lệch nằm đúng ranh giới giữa phần cuối của văn bản chính và phần **ban hành kèm theo**:

| | Chunk 12422 | Chunk 12423 |
|---|---|---|
| Tệp chunk (đúng) | Điều 3, `[1498:1733]`, 49 từ | mở đầu **QUY CHẾ** ban hành kèm theo, `[1734:2359]`, 136 từ, `kem_theo="Quy chế Xây dựng, quản lý và thực hiện"` |
| Chỉ mục (cũ, sai) | cùng mở đầu nhưng `end` khác | bắt đầu muộn hơn, ở `Chương I / QUY ĐỊNH CHUNG / Điều 1` |

Không phải lệch một trường phụ mà **lệch ranh giới thật**: chỉ mục cắt ở một chỗ, tệp chunk cắt ở
chỗ khác. Nguyên nhân gốc là thay đổi cách xử lý văn bản **ban hành kèm theo** (Quy chế, Điều lệ…
đánh số lại từ Điều 1, mang không gian số riêng qua trường `kem_theo`): tệp chunk được dựng lại
theo luật mới, chỉ mục thì không.

### Vì sao các lần kiểm trước lọt

Ba lớp phòng vệ lần lượt thủng:

1. **Thông báo "XONG" của lệnh nhúng.** `rag.chi_muc` bỏ qua tệp đã có chỉ mục khi thiếu `--force`,
   chỉ in `có rồi:` rồi trả về bình thường, nên `tools/nhung_tat_ca.sh` vẫn in `XONG NHÚNG`. Chạy
   lại không sửa được gì mà vẫn báo thành công.
2. **Kiểm bằng đếm số dòng.** Đây là lớp tôi tự thêm sau khi phát hiện chỉ mục C và D lệch. Nó bắt
   được C (5.637 so với 5.640) và D (7.718 so với 7.673), nhưng **mù với `Btru_s0`** vì số chunk hai
   bên bằng nhau tuyệt đối: 12.718 = 12.718. Đã có lần báo cáo "12/12 chỉ mục khớp" dựa trên đúng
   lớp kiểm này — tức là một kết luận sai, phát biểu một cách tự tin.
3. **Vân nội dung băm ba điểm** (chunk đầu / giữa / cuối). Lớp này thêm vào cùng ngày, vẫn mù, vì
   hai chunk lệch nằm ở vị trí 12422–12423 trên tổng 12.718 — không trùng vị trí 0, 6.359 hay
   12.717. Đo lại trên dữ liệu giả: băm ba điểm lọt 5/6 ca thử, chỉ bắt được chunk nằm đúng chính
   giữa.

Điểm chung của cả ba: đều kiểm **dấu hiệu gián tiếp** (lệnh có báo lỗi không, số dòng có bằng nhau
không, vài mẫu có giống nhau không) thay vì kiểm **chính thứ cần đúng** là toàn bộ nội dung đem nhúng.

### Hậu quả nếu không phát hiện

B− là đối chứng "chunk của B nhưng không gắn tiền tố", dùng để tách ảnh hưởng của tiền tố khỏi ảnh
hưởng của ranh giới. Nếu pilot chạy trước khi phát hiện, riêng dòng B− trong bảng ablation sẽ được
chấm trên một chỉ mục không ứng với tệp chunk của nó, và **không có dấu hiệu nào trong kết quả cho
thấy điều đó** — con số vẫn ra, vẫn hợp lý, chỉ là sai.

### Sửa thế nào

1. Nhúng lại: `python -m rag.chi_muc --force Btru_s0` — **16 giây** (phần lớn chuỗi đã có trong bộ
   đệm nội dung).
2. **Đổi vân nội dung sang băm TOÀN BỘ chuỗi đem nhúng theo đúng thứ tự**, thay cho băm ba điểm.
   Có cộng cả số lượng chunk và dấu ngăn cách giữa các chunk, nên bắt được cả ca đổi một chunk bất
   kỳ lẫn ca đảo thứ tự hai chunk. Chi phí đo thật: **4,4 giây** cho toàn kho ~90.000 chunk.
3. **Dựng chốt chặn `rag/kiem_chi_muc.py`**, bắt buộc chạy trước mọi lần đánh giá, kiểm ba lớp:
   số chunk, vân nội dung toàn bộ, và kích thước `emb.f32` so với `n × 768 × 4`. Lệch là dừng,
   không đánh giá. Trong mã đánh giá gọi `chot_chan()` ở dòng đầu.
4. **Sửa `rag.chi_muc` để không còn im lặng**: bỏ qua thì in `BỎ QUA: <tên> — đã có chỉ mục, dùng
   --force để ghi đè` và thoát **mã 3**; `tools/nhung_tat_ca.sh` bắt mã 3, dừng hẳn và **không in
   `XONG NHÚNG`**.
5. Tệp cố ý không nhúng phải khai báo tường minh kèm lý do trong hằng số `KHONG_NHUNG`
   (hiện là `B_s1..3`: B không phụ thuộc seed nên chỉ nhúng seed 0) — bỏ qua có chủ đích, không
   bỏ qua im lặng.
6. Test hồi quy: `tests/test_kiem_chi_muc.py`, 12 test, trong đó có ca **một chunk ở quãng giữa đổi
   nội dung** (tham số hoá 4 vị trí cố ý tránh đầu/giữa/cuối) và ca **đảo chỗ hai chunk** — đúng hai
   ca mà bản băm ba điểm bỏ lọt.

### Bài học ghi vào quyển

Một phép kiểm chỉ đáng tin tới mức nó kiểm đúng thứ cần đúng. Đếm dòng là kiểm **kích thước**, không
phải kiểm **nội dung**; nó bắt được hai ca đầu (C, D) nên tạo cảm giác an toàn, rồi mù với ca thứ ba.
Lỗi này không do thuật toán phân đoạn mà do **quy trình**: một bước có thể âm thầm không làm gì mà
vẫn báo thành công. Chi phí để đóng hẳn khe hở là 4,4 giây mỗi lần chạy.
