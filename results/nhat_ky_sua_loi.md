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

---

## 2026-10-20 — Giám khảo 4B kết luận ngược với chính lập luận của nó (q058, q065), và bỏ sót dẫn chiếu tường minh (q067)

### Lệch ở đâu

Bộ kiểm tra tự động trước khi chốt dùng chính mô hình sinh tại chỗ (Qwen3-4B, temperature 0) làm
giám khảo cho nhóm `xuyen_khoan`: *"Đoạn B có nêu một ngoại lệ áp dụng cho CHÍNH quy tắc ở đoạn A
không?"*. Ba câu bị gắn cờ `dat=False` (tức "không phải quan hệ quy tắc–ngoại lệ"), nhưng đọc kỹ
phần `ly_do` thì **hai câu có lập luận nói ngược lại chính kết luận**, và một câu kết luận sai sự thật:

| qid | Kết luận | Trích lập luận của chính nó | Thực chất |
|---|---|---|---|
| **q058** | `False` | *"…tức là **là một ngoại lệ** so với đoạn A, do đó **có thể coi là trường hợp loại trừ** hoặc giới hạn áp dụng quy định ở đoạn A."* | **Tự mâu thuẫn** — lập luận khẳng định ĐÚNG, kết luận trả về SAI |
| **q065** | `False` | *"…điều này **là một ngoại lệ** đối với quy trình trong đoạn A…"* | **Tự mâu thuẫn** — như trên |
| **q067** | `False` | *"Đoạn B không phải là ngoại lệ… mà là **một quy định song song, không liên quan**"* | **Nhất quán nhưng SAI SỰ THẬT** — xem dưới |

**q067 (59/2020/QH14 Điều 148)** là kiểu hỏng khác. Lập luận của giám khảo thẳng hàng với kết luận,
nhưng nó **bỏ sót một câu chữ nằm ngay trong đoạn được đưa cho nó đọc**: khoản 2 ghi rõ
*"…trừ trường hợp quy định tại **các khoản 1**, 3, 4 và 6 Điều này"* — tức khoản 2 **trỏ đích danh
khoản 1**. Hai khoản có liên kết tường minh, không hề "song song, không liên quan".

### Vì sao suýt lọt

Cả ba đều mang cờ trong `questions.jsonl`. Nếu chỉ đọc cột `dat` mà không đọc `ly_do`, ba câu này sẽ
bị loại khỏi bộ đánh giá — mất ba cặp quy tắc–ngoại lệ hợp lệ, trong đó q067 là cặp có **dẫn chiếu
tường minh**, tức thuộc loại chắc chắn nhất của nhóm. Cờ sai theo chiều "loại nhầm câu đúng" không
để lại dấu vết nào trong kết quả: bộ câu hỏi vẫn chạy, chỉ là nhỏ đi và yếu đi.

### Sửa thế nào

1. **Ghi đè cờ cho q065 và q067**, kèm lý do vào trường ghi chú của từng câu — không xoá cờ, để người
   đọc thấy cả cờ lẫn lý do ghi đè.
2. **q058 và q064** thay câu hỏi bằng dạng so sánh.
3. Giữ nguyên nguyên tắc chung *"cặp nào bộ kiểm tra nói rời nhau thì bỏ, không cứu"* — ba ca này là
   ngoại lệ **có chứng cứ đối chiếu được**, không phải nới nguyên tắc.

### Bài học ghi vào quyển

Mô hình 4B dùng làm giám khảo **không đáng tin ở mức kết luận nhị phân**. Trong ba ca, hai ca trường
`dat` mâu thuẫn với trường `ly_do` do chính nó sinh ra trong cùng một lần gọi. Vì vậy mọi cờ tự động
trong đồ án đều **chỉ gắn cờ, không bao giờ tự xoá câu** — đúng như thiết kế ban đầu của
`eval/kiem_tra.py` — và người duyệt phải đọc `ly_do` chứ không chỉ đọc `dat`. Một giám khảo tự mâu
thuẫn vẫn có ích nếu nó buộc người ta nhìn vào đúng chỗ; nó chỉ nguy hiểm khi được tin như nhãn cuối cùng.

---

## 2026-10-22 — Báo "1 ca cắt trần" trong khi thật ra có 6

### Lệch ở đâu

Trong lúc lượt sinh E chạy nền trên bộ `manh_con`, tôi báo tiến độ bốn lần, và cả bốn lần đều
nói **"1 ca bị cắt"**. Con số thật khi lượt chạy kết thúc là **6**:

| Câu | Cấu hình bị cắt trần |
|---|---|
| **mc031** | Eduoi · Etren · Etat_d · Etat_n · Etat_s — **5/8 cấu hình** |
| mc014 | Etat_s — 1/8 |

Sai số không phải 1 đơn vị mà **gấp sáu lần**, và nó đi kèm một nhận định sai theo: tôi viết
"tỉ lệ đến giờ 1/122, khớp với 1/253 đo trên pilot", tức là dùng con số sai để trấn an rằng
hiện tượng này hiếm như dự đoán. Tỉ lệ thật trên `manh_con` là **6/280 = 2,1%**, cao gấp năm lần
tỉ lệ 0,4% của pilot.

### Vì sao các lần kiểm trước lọt

Tôi đếm bằng cách đọc **dòng cuối** của tệp nhật ký:

```bash
tail -2 "$CLAUDE_JOB_DIR/tmp/chay_E.log"
wc -l < results/manh_con_bi_cat.jsonl
```

Lần kiểm đầu tiên rơi đúng vào lúc mới có một ca (`mc014/Etat_s`, ở lượt ~121/280). Năm ca của
`mc031` xảy ra muộn hơn, quanh lượt 240–280. Những lần kiểm sau tôi **chỉ nhìn `tail`** chứ không
đếm lại toàn tệp, nên con số 1 bị chép đi chép lại qua bốn lần báo cáo như thể nó vẫn đúng.

Hai thói quen cộng lại thành lỗi:

1. **Đếm một lần rồi tái sử dụng con số.** Một đại lượng đang tăng theo thời gian thì mỗi lần báo
   phải đếm lại, không được nhớ.
2. **`tail` để xem tiến độ bị dùng nhầm thành `tail` để đếm.** `tail -2` trả lời câu hỏi "đang
   chạy tới đâu", không trả lời câu hỏi "tổng cộng bao nhiêu".

### Hậu quả nếu không phát hiện

Con số 6 không chỉ là con số. Nó mang một **kết quả thật**: `mc031` bị cắt ở 5 cấu hình nhưng
**không bị cắt ở B, Etat_k và Echi_s** — đúng ba cấu hình **tắt `dan_khoan`**. Đối chiếu đầy đủ:

| | `dan_khoan` bật | `dan_khoan` tắt |
|---|---|---|
| mc031 cắt trần | 5/5 (Eduoi, Etren, Etat_d, Etat_n, Etat_s) | 0/5 (B, Etat_k, Echi_s, B+, E2) |

`dan_dieu` **không** phân biệt được hai nhóm: Etat_d tắt dẫn Điều mà vẫn cắt. Tức là **chép câu
dẫn của khoản vào mọi chunk điểm là nguyên nhân làm phình ngữ cảnh tới mức tràn trần**. Nếu tôi
cứ báo "1 ca", bằng chứng này nằm im trong tệp và không ai đọc tới; đặc tả E2 ngày 26/10 — *chỉ
chép câu dẫn của Điều, không chép câu dẫn của khoản* — chính là dựa trên nó.

### Sửa thế nào

1. Mọi lần báo số đếm đều **đếm lại từ đầu tệp**, không dùng `tail`:
   `python -c "...len([l for l in open(p)])"` hoặc `wc -l` trên toàn tệp, kèm phân tích theo nhóm.
2. `eval/manh_con_chay.py` in **tổng kết cuối lượt** liệt kê đích danh mọi cặp bị cắt, nên con số
   cuối không còn phụ thuộc vào việc tôi theo dõi đúng lúc hay không.
3. Cột **cắt trần** là cột cố định trong mọi bảng kết quả (`eval/ket_qua.py`), nên số này luôn
   hiện ra cạnh các số khác thay vì phải đi hỏi.

### Bài học ghi vào quyển

Lỗi này không nằm trong mã, nó nằm trong **cách tường thuật**. Một con số đang thay đổi mà được
báo lại nhiều lần thì mỗi lần là một phép đo mới, không phải một lần trích dẫn. Và khi một con số
nhỏ được dùng để nói "khớp với dự đoán", đó đúng là lúc phải kiểm lại nó kỹ nhất — vì nó đang
được dùng để đóng một câu hỏi, chứ không phải để mở một câu hỏi.

---

## 2026-10-30 — Bộ chấm trích dẫn: bảng cặp tương đương chưa được áp; rà gold `dieu_dai`; thêm tiêu chí phụ

### Lệch ở đâu

**(1) Bảng cặp tương đương bị bỏ sót ở tầng trích dẫn.** `eval/cham.py` ghi rõ bản tương đương E(G) "dùng cho cả
chấm truy hồi lẫn chấm trích dẫn", nhưng `eval/cham_trich_dan.cham_mot` chỉ so với khoá của chính gold. Mô hình dẫn
`83/2026/VBHN-TT-BXD` (văn bản hợp nhất, cùng Điều/khoản, nguyên văn giống hệt) thay cho `03/2020/TT-BXD` bị chấm sai,
trong khi ở tầng truy hồi chunk của bản hợp nhất đó được tính là trúng.

**(2) Rà 19 câu `dieu_dai`.** Yêu cầu: đơn vị dẫn là dòng tiêu đề Điều; câu nào có đơn vị gold lấy cả Điều thì sửa
gold. Kết quả rà: **0/19 câu có đơn vị gold lấy cả Điều** (đơn vị dài nhất 142 từ, là một khoản — q129). Hai câu q122,
q127 có một đơn vị cấp Điều (không khoản) mà span là **câu dẫn** "Trong Luật này, các từ ngữ dưới đây được hiểu như sau:"
(12 từ). Không sửa gold câu nào.

Bản phân tích lỗi ngày 30/10 (`results/local_gpu/phan_tich_loi.md` §4) đã viết sai rằng q127 hụt "vì gold là cả Điều 3".
Kiểm lại: câu dẫn nằm trong chunk B "Điều 3 … Khoản 1", chunk đó đứng hạng 779 (q122: hạng 2.156) nên không vào 50 ứng
viên. Dòng tiêu đề Điều nằm trong chính chunk đó, nên đổi span sang dòng tiêu đề cũng không đổi kết quả truy hồi; ở tầng
trích dẫn khoá chấm là (số hiệu, Điều 3), không phụ thuộc span. Câu sai đã được sửa trong `eval/phan_tich_loi.py`.

**(3) Một tiêu chí duy nhất phạt cả trích thừa.** "Đúng toàn phần" = đủ gold *và* không thừa. Thêm tiêu chí phụ
**đủ gold** (đủ mọi đơn vị gold, cho phép thừa). Mọi bảng trích dẫn báo hai cột: *khớp hoàn toàn* (chính, chính là "đúng
toàn phần" cũ) và *đủ gold* (phụ).

### Vì sao các lần kiểm trước lọt

Bộ chấm trích dẫn được kiểm bằng 120 nhãn tay — các nhãn đó kiểm **bộ bóc** (regex đọc ra Điều/khoản nào), không kiểm
**phép so với gold**. Câu dẫn bản hợp nhất bóc đúng, nên nhãn tay khớp; lỗi nằm ở bước so khoá ngay sau đó, nơi không
có phép kiểm nào. Lỗi (2) là lỗi tường thuật: một nhận định viết từ con số (độ phủ 0 trong 50 ứng viên) mà không mở gold
ra xem.

### Sửa thế nào

1. `cham_mot(r, muc, td)` nhận `td` từ `eval.chay_truy_hoi._td_cho` (cùng hàm tầng truy hồi dùng, câu phiên bản trả
   rỗng): trích dẫn trỏ vào bản tương đương được quy về đúng khoá gold.
2. `eval/bang_day_du.py` ghi cả kết quả trước sửa (`dieu_toan_phan_khong_td`) vào `chi_tiet_cau.jsonl` và in số câu đổi
   kết quả ở mục 0 của `metrics_trich_dan.md`.
3. Chấm lại, **không sinh lại**. Số lượt đổi kết quả (mức Điều, khớp hoàn toàn): bộ chính 7 lượt, đều 0 → 1 — q010 ở
   A, B, B+, E, E2, E3 và q015 ở A; manh_con 7 lượt (mc020 ở B, B+, Etat_k, Echi_s, E2, E3, E3b). Không lượt nào 1 → 0.
   Sửa (2): 0 lượt. Sửa (3): không đổi cột chính.
