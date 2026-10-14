# Duyệt bộ câu hỏi đánh giá (nháp)

Mỗi câu: sửa `Trạng thái:` (GIỮ / XOÁ; câu dự phòng đổi DỰ PHÒNG → GIỮ nếu muốn dùng) và sửa thẳng dòng `Câu hỏi:`. Xong chạy `python -m eval.duyet --chot`.

Tổng 175 câu nháp; cần giữ: don_gian 50 (trung lập ≥ 16), xuyen_khoan 18 (trung lập ≥ 6), dan_chieu 12 (trung lập ≥ 4), dieu_dai 20 (trung lập ≥ 6), khong_co_dieu 15 (trung lập ≥ 5).

**TRUNG LẬP** = gold cố ý KHÔNG trùng ranh giới cấu trúc (1–3 câu bắt đầu giữa khoản/điểm/đoạn, có thể vắt sang khoản kế) — tập số chính của báo cáo. Câu không ghi TRUNG LẬP có gold trùng ranh giới khoản (B có lợi thế cấu trúc), báo riêng. Câu DỰ PHÒNG: đổi thành GIỮ nếu muốn thay câu bị XOÁ cùng nhóm, cùng loại gold.

## Tóm tắt cờ sàng lọc tự động (chỉ để bạn biết xem kỹ chỗ nào — quyết định giữ/bỏ là của bạn)

| Nhóm | Câu GIỮ (trung lập) | Không cờ | Gold đáng ngờ | Không trả lời được | Sai ý đồ nhóm | Mơ hồ | Lộ đáp án | Kiểm tra tự động | Gold ở bản cũ |
|---|---|---|---|---|---|---|---|---|---|
| don_gian | 44 (14) | 15 | 5 | 3 | 9 | 19 | 2 | 0 | 0 |
| xuyen_khoan | 18 (6) | 2 | 0 | 1 | 8 | 10 | 4 | 0 | 0 |
| dan_chieu | 10 (4) | 4 | 0 | 0 | 4 | 1 | 1 | 2 | 0 |
| dieu_dai | 19 (6) | 7 | 0 | 0 | 0 | 6 | 7 | 0 | 0 |
| khong_co_dieu | 15 (5) | 4 | 3 | 1 | 0 | 5 | 4 | 0 | 0 |

## q001 · don_gian · khoan

Trạng thái: GIỮ
Câu hỏi: Doanh nghiệp muốn tồn trữ hóa chất cần làm thế nào để được cấp giấy chứng nhận đủ điều kiện hoạt động?

*Đáp án nháp của mô hình:* Cần đáp ứng các điều kiện quy định, thực hiện trình tự, thủ tục và được cơ quan có thẩm quyền cấp giấy chứng nhận đủ điều kiện hoạt động dịch vụ tồn trữ hóa chất.

**Sàng lọc:** chỉ trả lời được một phần từ gold; không đúng ý đồ nhóm — Gold là khoản giao Chính phủ quy định chi tiết nên chỉ trả lời được 'do Chính phủ quy định'; điều kiện cấp thực chất nằm ở khoản 5 cùng Điều. Giấy chứng nhận này cấp cho đơn vị làm DỊCH VỤ tồn trữ, không phải cho mọi doanh nghiệp tồn trữ. Đáp án nháp không nêu được Chính phủ. · Gợi ý câu hỏi: Ai quy định điều kiện, trình tự, thủ tục cấp, cấp lại và thu hồi Giấy chứng nhận đủ điều kiện hoạt động dịch vụ tồn trữ hóa chất?

**Gold: 69/2025/QH15 Điều 14 khoản 7**

> 7. Chính phủ quy định chi tiết điểm b và điểm c khoản 1 Điều này; quy định nội dung Giấy chứng nhận đủ điều kiện hoạt động dịch vụ tồn trữ hóa chất; điều kiện, trình tự, thủ tục, thẩm quyền cấp, cấp lại, điều chỉnh, thu hồi Giấy chứng nhận đủ điều kiện hoạt động dịch vụ tồn trữ hóa chất.

---
## q002 · don_gian · khoan

Trạng thái: GIỮ
Câu hỏi: Công dân hoặc tổ chức nào được phép đăng, phát thông tin trên các sản phẩm thông tin có tính chất báo chí?

*Đáp án nháp của mô hình:* Các cá nhân, tổ chức được phép đăng, phát thông tin trên các sản phẩm thông tin có tính chất báo chí nếu thông tin thuộc các nội dung quy định tại các khoản 1 đến 11 của Điều này.

**Sàng lọc:** KHÔNG trả lời được từ gold; không đúng ý đồ nhóm; gold đáng ngờ — Gold là một khoản trong Điều 'Các hành vi bị nghiêm cấm' nhưng thiếu câu dẫn này, lại dẫn chiếu khoản 1–11 không có trong gold. Câu hỏi và đáp án nháp hiểu ngược thành 'được phép đăng, phát', đồng thời hỏi 'ai' trong khi gold không nói về chủ thể. · Gợi ý câu hỏi: Có được đăng, phát trên sản phẩm thông tin có tính chất báo chí những thông tin thuộc loại mà pháp luật cấm đăng, phát trên báo chí không?

**Gold: 126/2025/QH15 Điều 8 khoản 14**

> 14. Đăng, phát trên sản phẩm thông tin có tính chất báo chí thông tin quy định tại các khoản 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 và 11 Điều này.

---
## q003 · don_gian · khoan

Trạng thái: GIỮ
Câu hỏi: Nếu một người vi phạm nội quy trong phiên tòa thì có thể bị xử lý như thế nào?

*Đáp án nháp của mô hình:* Có thể bị cấm vào phòng xử án, buộc rời khỏi phòng, bị xử phạt vi phạm hành chính, tạm giữ hành chính hoặc truy cứu trách nhiệm hình sự tùy theo tính chất và mức độ vi phạm.

**Sàng lọc:** câu hỏi mơ hồ — Bộ luật Tố tụng hình sự 2015, Điều 467 (có trong kho) cũng quy định xử lý người vi phạm nội quy phiên tòa; khoản 3 cùng Điều cũng có nội dung gần giống. Câu hỏi chung chung nên dễ khớp nhầm. · Gợi ý câu hỏi: Người vi phạm nội quy phiên tòa hoặc phiên hòa giải, đối thoại tại Tòa án có thể bị áp dụng những biện pháp xử lý nào?

**Gold: 34/2024/QH15 Điều 139 khoản 4**

> 4. Người vi phạm nội quy phiên tòa thì tùy tính chất, mức độ vi phạm có thể bị cấm vào hoặc buộc rời khỏi phòng xử án, phòng hòa giải, đối thoại, bị xử phạt vi phạm hành chính, tạm giữ hành chính hoặc truy cứu trách nhiệm hình sự theo quy định của pháp luật.

---
## q004 · don_gian · khoan

Trạng thái: GIỮ
Câu hỏi: Khi có kháng nghị về một bản án đã có hiệu lực pháp luật, thì hội đồng giám đốc thẩm sẽ xem xét điều gì?

*Đáp án nháp của mô hình:* Hội đồng giám đốc thẩm sẽ xem xét lại phần quyết định của bản án đó nếu có kháng nghị hoặc nếu nội dung kháng nghị có liên quan.

**Sàng lọc:** câu hỏi mơ hồ — Câu hỏi không nêu loại tố tụng. Bộ luật Tố tụng hình sự 2015, Điều 387 (có trong kho) quy định ngược lại: xem xét toàn bộ vụ án. Gold chỉ có khoản 1, bỏ ngoại lệ ở khoản 2. · Gợi ý câu hỏi: Trong tố tụng dân sự, Hội đồng giám đốc thẩm được xem xét lại những phần nào của bản án, quyết định đã có hiệu lực pháp luật bị kháng nghị?

**Gold: 24/2004/QH11 Điều 296 khoản 1**

> 1. Hội đồng giám đốc thẩm chỉ xem xét lại phần quyết định của bản án, quyết định đã có hiệu lực pháp luật bị kháng nghị hoặc có liên quan đến việc xem xét nội dung kháng nghị.

---
## q005 · don_gian · khoan

Trạng thái: GIỮ
Câu hỏi: Khi người lao động làm việc tại một doanh nghiệp từ đủ 12 tháng trở lên và hợp đồng lao động chấm dứt theo quy định, họ có được hưởng trợ cấp thôi việc không?

*Đáp án nháp của mô hình:* Có, người lao động được hưởng trợ cấp thôi việc nếu đã làm việc từ đủ 12 tháng trở lên, với mức trợ cấp bằng một nửa tháng tiền lương cho mỗi năm làm việc, trừ một số trường hợp đặc biệt như đã đủ điều kiện hưởng lương hưu hoặc theo quy định tại điểm e khoản 1 Điều 36 của Bộ luật.

**Sàng lọc:** câu hỏi mơ hồ — Bộ luật Lao động 2012, Điều 48 (có trong kho) có quy định trợ cấp thôi việc gần giống: đủ 12 tháng, nửa tháng lương. Câu hỏi khớp cả hai bản. · Gợi ý câu hỏi: Người lao động làm việc thường xuyên từ đủ 12 tháng trở lên nhưng đã đủ điều kiện hưởng lương hưu thì khi chấm dứt hợp đồng lao động có được trợ cấp thôi việc không?

**Gold: 45/2019/QH14 Điều 46 khoản 1**

> 1. Khi hợp đồng lao động chấm dứt theo quy định tại các khoản 1, 2, 3, 4, 6, 7, 9 và 10 Điều 34 của Bộ luật này thì người sử dụng lao động có trách nhiệm trả trợ cấp thôi việc cho người lao động đã làm việc thường xuyên cho mình từ đủ 12 tháng trở lên, mỗi năm làm việc được trợ cấp một nửa tháng tiền lương, trừ trường hợp đủ điều kiện hưởng lương hưu theo quy định của pháp luật về bảo hiểm xã hội và trường hợp quy định tại điểm e khoản 1 Điều 36 của Bộ luật này.

---
## q006 · don_gian · khoan

Trạng thái: XOÁ
Câu hỏi: Nếu một hành vi phạm tội được thực hiện có tổ chức hoặc lợi dụng nghề nghiệp thì sẽ bị xử lý như thế nào?

*Đáp án nháp của mô hình:* Sẽ bị phạt tù từ mười năm đến hai mươi năm hoặc tù chung thân.

**⚠ Bản cũ:** gold ở BẢN CŨ, bản mới cũng có trong kho — 15/1999/QH10 Điều 118 ↔ 100/2015/QH13 Điều 149: KHÁC ÍT (chứa 0.69)
**Sàng lọc:** câu hỏi mơ hồ; gold đáng ngờ — Gold là khoản 2 của tội cố ý truyền HIV cho người khác (theo tiêu đề Điều) nhưng không chứa tên tội. 'Có tổ chức, lợi dụng nghề nghiệp' là tình tiết tăng nặng của rất nhiều tội; Bộ luật Hình sự 2015, Điều 149 cũng có tội này. · Gợi ý câu hỏi: Người cố ý truyền HIV cho người khác mà phạm tội có tổ chức hoặc lợi dụng nghề nghiệp thì bị phạt như thế nào?

**Gold: 15/1999/QH10 Điều 118 khoản 2**

> 2. Phạm tội thuộc một trong các trường hợp sau đây, thì bị phạt tù từ mười năm đến hai mươi năm hoặc tù chung thân:
> a) Có tổ chức;
> b) Đối với nhiều người;
> c) Đối với người chưa thành niên;
> d) Đối với người đang thi hành công vụ hoặc vì lý do công vụ của nạn nhân;
> đ) Lợi dụng nghề nghiệp.

---
## q007 · don_gian · khoan

Trạng thái: GIỮ
Câu hỏi: Nếu một người vận chuyển bị chậm trả hàng, họ có phải bồi thường không?

*Đáp án nháp của mô hình:* Chỉ phải bồi thường nếu bên nhận hàng được thông báo bằng văn bản về việc chậm trả trong vòng 60 ngày kể từ ngày hàng hóa lẽ ra được giao theo hợp đồng.

**Sàng lọc:** câu hỏi mơ hồ — Câu hỏi thiếu bối cảnh đường biển và thời hạn thông báo; trong cùng Bộ luật còn các Điều miễn hoặc giới hạn trách nhiệm do chậm trả hàng dễ khớp nhầm. Đáp án nháp sai: thông báo phải gửi TỚI người vận chuyển. Gold dính tiêu đề 'Mục 3' ở cuối. · Gợi ý câu hỏi: Để người vận chuyển hàng hóa bằng đường biển phải bồi thường tổn thất do chậm trả hàng, thông báo về việc chậm trả phải được gửi trong thời hạn bao lâu?

**Gold: 95/2015/QH13 Điều 174 khoản 4**

> 4. Người vận chuyển không phải bồi thường đối với tổn thất phát sinh do việc chậm trả hàng, trừ trường hợp thông báo về việc chậm trả hàng bằng văn bản được gửi tới người vận chuyển trong vòng 60 ngày kể từ ngày hàng hóa lẽ ra được giao theo thỏa thuận trong hợp đồng.

---
## q008 · don_gian · khoan

Trạng thái: GIỮ
Câu hỏi: Khi kinh doanh dịch vụ tại một bảo tàng, doanh nghiệp cần đảm bảo điều gì để không vi phạm quy định?

*Đáp án nháp của mô hình:* Hoạt động kinh doanh phải phù hợp với nhiệm vụ và mục đích được quy định tại bảo tàng, nhằm bảo vệ và phát huy giá trị di sản văn hóa.

**Sàng lọc:** không thấy vấn đề — Gold dính tiêu đề 'Chương VII…' ở cuối. Đáp án nháp bịa thêm ý 'bảo vệ, phát huy giá trị di sản' lấy từ tiêu đề chương.

**Gold: 45/2024/QH15 Điều 81 khoản 2**

> 2. Hoạt động kinh doanh dịch vụ bảo tàng phải phù hợp với nhiệm vụ của bảo tàng quy định tại Điều 68 của Luật này.

---
## q009 · don_gian · khoan

Trạng thái: GIỮ
Câu hỏi: Khi muốn công bố thông tin về tình hình bay của một chuyến bay, cần làm gì trước tiên?

*Đáp án nháp của mô hình:* Cần phải kiểm tra, xác nhận và được phê chuẩn theo thẩm quyền quy định.

**Sàng lọc:** chỉ trả lời được một phần từ gold — Câu hỏi diễn giải sai 'dữ liệu hàng không, tin tức hàng không' thành 'thông tin về tình hình bay của một chuyến bay'. · Gợi ý câu hỏi: Dữ liệu và tin tức hàng không phải đáp ứng điều kiện gì trước khi được đưa vào khai thác, sử dụng hoặc công bố?

**Gold: 222/2026/NĐ-CP Điều 111 khoản 4**

> 4. Dữ liệu hàng không và tin tức hàng không chỉ được đưa vào khai thác, sử dụng hoặc công bố khi đã được kiểm tra, xác nhận, phê chuẩn theo thẩm quyền, trình tự, thủ tục quy định.

---
## q010 · don_gian · khoan

Trạng thái: GIỮ
Câu hỏi: Người thiết kế kiến trúc cần nộp hồ sơ gì để được thẩm định và phê duyệt?

*Đáp án nháp của mô hình:* Cần nộp hồ sơ thiết kế kiến trúc, đây là một phần của hồ sơ thiết kế xây dựng được thẩm định và phê duyệt theo quy định của Luật xây dựng.

**Sàng lọc:** chỉ trả lời được một phần từ gold; không đúng ý đồ nhóm — Gold chỉ nói hồ sơ thiết kế kiến trúc là một phần của hồ sơ thiết kế xây dựng, không liệt kê cần nộp gì (danh mục nằm ở khoản 2) và không nói ai nộp. Đáp án nháp lặp lại ý trong câu hỏi. · Gợi ý câu hỏi: Hồ sơ thiết kế kiến trúc có vị trí như thế nào trong hồ sơ thiết kế xây dựng và được thẩm định, phê duyệt theo luật nào?

**Gold: 03/2020/TT-BXD Điều 2 khoản 1**

> 1. Hồ sơ thiết kế kiến trúc là thành phần của hồ sơ thiết kế xây dựng được thực hiện thẩm định, phê duyệt theo quy định của Luật xây dựng.

---
## q011 · don_gian · khoan

Trạng thái: GIỮ
Câu hỏi: Nếu một bên không thực hiện nghĩa vụ đúng thời hạn, họ cần làm gì để thông báo cho bên kia?

*Đáp án nháp của mô hình:* Phải thông báo ngay cho bên có quyền về việc không thực hiện nghĩa vụ đúng thời hạn.

**Sàng lọc:** câu hỏi mơ hồ — Câu hỏi gần như tự chứa đáp án ('để thông báo') và thiếu bối cảnh dân sự. Điều 287 khoản 1 cùng Bộ luật (hoãn thực hiện nghĩa vụ) cũng yêu cầu 'thông báo ngay cho bên có quyền' nên dễ nhầm. · Gợi ý câu hỏi: Bên chậm thực hiện nghĩa vụ dân sự có trách nhiệm gì đối với bên có quyền?

**Gold: 33/2005/QH11 Điều 286 khoản 2**

> 2. Bên chậm thực hiện nghĩa vụ dân sự phải thông báo ngay cho bên có quyền về việc không thực hiện nghĩa vụ đúng thời hạn.

---
## q012 · don_gian · khoan

Trạng thái: XOÁ
Câu hỏi: Khi muốn thay đổi vị trí làm việc của một cán bộ lãnh đạo, người ta cần làm gì?

*Đáp án nháp của mô hình:* Phải có quyết định của cấp có thẩm quyền về công tác cán bộ.

**⚠ Bản cũ:** gold ở BẢN CŨ, bản mới cũng có trong kho — 170/2025/NĐ-CP Điều 24 ↔ 10/2026/VBHN-NĐ-BNV Điều 23: KHÁC ÍT (chứa 0.84)
**Sàng lọc:** gold đáng ngờ — Gold có thể đã hết hiệu lực: Điều 24 của 170/2025/NĐ-CP đã bị 300/2026/NĐ-CP thay toàn bộ (nay là xếp lương), câu gold không còn trong văn bản hợp nhất 10/2026/VBHN-NĐ-BNV; ý tương tự chuyển sang Điều 23 khoản 3 điểm a. Câu hỏi dùng 'cán bộ' thay vì 'công chức'.

**Gold: 170/2025/NĐ-CP Điều 24 khoản 1**

> 1. Thay đổi vị trí việc làm lãnh đạo, quản lý được thực hiện theo quyết định của cấp có thẩm quyền về công tác cán bộ.

---
## q013 · don_gian · khoan

Trạng thái: XOÁ
Câu hỏi: Nếu người lao động yêu cầu thương lượng tập thể, doanh nghiệp có được từ chối không?

*Đáp án nháp của mô hình:* Không được từ chối, doanh nghiệp phải tham gia thương lượng.

**⚠ Bản cũ:** gold ở BẢN CŨ, bản mới cũng có trong kho — 10/2012/QH13 Điều 68 ↔ 45/2019/QH14 Điều 70 khoản 1: KHÁC ÍT (chứa 0.74)
**Sàng lọc:** câu hỏi mơ hồ — Gold thuộc Bộ luật Lao động 2012 (đã bị thay thế). Bộ luật Lao động 2019, Điều 70 (có trong kho) cũng quy định 'bên nhận được yêu cầu không được từ chối việc thương lượng', nên câu hỏi khớp cả hai.

**Gold: 10/2012/QH13 Điều 68 khoản 1**

> 1. Mỗi bên đều có quyền yêu cầu thương lượng tập thể, bên nhận được yêu cầu không được từ chối việc thương lượng. Trong thời hạn 07 ngày làm việc, kể từ ngày nhận được yêu cầu thương lượng, các bên thoả thuận thời gian bắt đầu phiên họp thương lượng.

---
## q014 · don_gian · khoan

Trạng thái: GIỮ
Câu hỏi: Khi có quyết định trưng cầu giám định, thì cơ quan nào phải thực hiện việc giao hồ sơ và đối tượng giám định cho tổ chức hoặc cá nhân được thuê để thực hiện giám định?

*Đáp án nháp của mô hình:* Cơ quan trưng cầu giám định phải giao hoặc gửi quyết định trưng cầu giám định, hồ sơ và đối tượng giám định cho tổ chức, cá nhân thực hiện giám định.

**Sàng lọc:** lộ đáp án / nhắc văn bản — Câu hỏi chép gần nguyên văn gold, và đáp án ('cơ quan trưng cầu giám định') suy ra ngay từ câu hỏi. Từ 'được thuê' dùng sai; bỏ qua ý chính là thời hạn 24 giờ. · Gợi ý câu hỏi: Sau khi ra quyết định trưng cầu giám định trong vụ án hình sự, cơ quan trưng cầu phải chuyển hồ sơ, đối tượng giám định cho người giám định trong thời hạn bao lâu?

**Gold: 101/2015/QH13 Điều 205 khoản 3**

> 3. Trong thời hạn 24 giờ kể từ khi ra quyết định trưng cầu giám định, cơ quan trưng cầu giám định phải giao hoặc gửi quyết định trưng cầu giám định, hồ sơ, đối tượng trưng cầu giám định cho tổ chức, cá nhân thực hiện giám định; gửi quyết định trưng cầu giám định cho Viện kiểm sát có thẩm quyền thực hành quyền công tố và kiểm sát điều tra.

---
## q015 · don_gian · khoan

Trạng thái: GIỮ
Câu hỏi: Giao dịch thuế điện tử là gì?

*Đáp án nháp của mô hình:* Là các giao dịch được thực hiện bằng phương thức điện tử giữa các cơ quan, tổ chức, cá nhân trong lĩnh vực thuế.

**Cờ tự động:** trùng từ cao (86%)
**Sàng lọc:** không thấy vấn đề

**Gold: 19/2021/TT-BTC Điều 3 khoản 1**

> 1. "Giao dịch thuế điện tử" là các giao dịch được các cơ quan, tổ chức, cá nhân thực hiện bằng phương thức điện tử thuộc phạm vi điều chỉnh của Thông tư này.

---
## q016 · don_gian · khoan

Trạng thái: GIỮ
Câu hỏi: Nếu một người không tố giác tội phạm của người thân như ông, bà, cha, mẹ, con, cháu, anh chị em ruột hoặc vợ chồng thì có bị xử lý hay không?

*Đáp án nháp của mô hình:* Không bị xử lý nếu người đó không tố giác tội phạm của người thân, trừ khi tội phạm liên quan đến an ninh quốc gia hoặc các tội đặc biệt nghiêm trọng khác.

**Sàng lọc:** câu hỏi mơ hồ — Bộ luật Hình sự 1999, Điều 22 khoản 2 (có trong kho) có quy định tương đương, nên câu hỏi khớp cả hai bộ luật.

**Gold: 100/2015/QH13 Điều 19 khoản 2**

> 2. Người không tố giác là ông, bà, cha, mẹ, con, cháu, anh chị em ruột, vợ hoặc chồng của người phạm tội không phải chịu trách nhiệm theo quy định tại khoản 1 Điều này, trừ trường hợp không tố giác các tội xâm phạm an ninh quốc gia hoặc tội đặc biệt nghiêm trọng khác quy định tại Điều 389 của Bộ luật này.

---
## q017 · don_gian · khoan

Trạng thái: XOÁ
Câu hỏi: Nếu một hộ kinh doanh không thực hiện hoặc thực hiện không đầy đủ chế độ kế toán và hóa đơn theo quy định, thì sẽ phải nộp thuế giá trị gia tăng như thế nào?

*Đáp án nháp của mô hình:* Sẽ nộp thuế giá trị gia tăng theo phương pháp khoán thuế.

**⚠ Bản cũ:** gold ở BẢN CŨ, bản mới cũng có trong kho — 48/2024/QH15 Điều 12 ↔ 114/VBHN-VPQH Điều 11: KHÁC NHIỀU hoặc không còn (chứa 0.52)
**Sàng lọc:** lộ đáp án / nhắc văn bản; gold đáng ngờ — Gold có thể đã hết hiệu lực: khoản này đã bị Luật 149/2025/QH15 bãi bỏ (hiệu lực 01/01/2026) và không còn trong 114/VBHN-VPQH. Câu hỏi chép gần nguyên văn vế điều kiện của gold.

**Gold: 48/2024/QH15 Điều 12 khoản 3**

> 3. Hộ, cá nhân sản xuất, kinh doanh không thực hiện hoặc thực hiện không đầy đủ chế độ kế toán, hóa đơn, chứng từ theo quy định của pháp luật thì nộp thuế giá trị gia tăng theo phương pháp khoán thuế quy định tại Luật Quản lý thuế.

---
## q018 · don_gian · khoan

Trạng thái: GIỮ
Câu hỏi: Người sở hữu trái phiếu cần báo cáo điều gì cho Sở giao dịch chứng khoán?

*Đáp án nháp của mô hình:* Cần báo cáo định kỳ hàng quý và hàng năm, cũng như báo cáo khi phát hiện doanh nghiệp phát hành có hành vi vi phạm pháp luật trong việc thực hiện cam kết với nhà đầu tư.

**Sàng lọc:** chỉ trả lời được một phần từ gold — Sai chủ thể: gold quy định cho ĐẠI DIỆN người sở hữu trái phiếu, không phải người sở hữu trái phiếu. · Gợi ý câu hỏi: Đại diện người sở hữu trái phiếu doanh nghiệp riêng lẻ phải báo cáo Sở giao dịch chứng khoán vào những thời điểm hoặc trường hợp nào?

**Gold: 200/2026/NĐ-CP Điều 39 khoản 2**

> 2. Đại diện người sở hữu trái phiếu thực hiện chế độ báo cáo cho Sở giao dịch chứng khoán định kỳ hàng quý, hằng năm và báo cáo trong trường hợp phát hiện doanh nghiệp phát hành có hành vi vi phạm pháp luật trong việc thực hiện các cam kết với nhà đầu tư.

---
## q019 · don_gian · khoan

Trạng thái: GIỮ
Câu hỏi: Khi một công ty chuyển đổi thành công ty khác, thì công ty mới có phải chịu trách nhiệm với các khoản nợ của công ty cũ không?

*Đáp án nháp của mô hình:* Có, công ty mới sẽ kế thừa toàn bộ quyền và lợi ích hợp pháp, cũng như phải chịu trách nhiệm về các khoản nợ, bao gồm nợ thuế, nợ hợp đồng lao động và các nghĩa vụ khác của công ty cũ.

**Sàng lọc:** câu hỏi mơ hồ — Câu gold lặp y hệt ở Điều 202, 203, 204 cùng Luật (các loại chuyển đổi khác nhau), nhưng câu hỏi không nêu loại hình chuyển đổi. Gold là Điều 202: công ty trách nhiệm hữu hạn chuyển thành công ty cổ phần. · Gợi ý câu hỏi: Khi công ty trách nhiệm hữu hạn chuyển đổi thành công ty cổ phần, công ty sau chuyển đổi có phải chịu các khoản nợ, kể cả nợ thuế, của công ty trước chuyển đổi không?

**Gold: 59/2020/QH14 Điều 202 khoản 4**

> 4. Công ty chuyển đổi đương nhiên kế thừa toàn bộ quyền và lợi ích hợp pháp, chịu trách nhiệm về các khoản nợ, gồm cả nợ thuế, hợp đồng lao động và nghĩa vụ khác của công ty được chuyển đổi.

---
## q020 · don_gian · khoan

Trạng thái: GIỮ
Câu hỏi: Công ty đầu tư nước ngoài tại Việt Nam cần làm gì để đảm bảo tuân thủ quy định về quản lý ngoại hối?

*Đáp án nháp của mô hình:* Cần được thanh tra, kiểm tra và giám sát việc mở, sử dụng tài khoản vốn đầu tư theo quy định, đồng thời tuân thủ các xử lý hành vi vi phạm pháp luật về ngoại hối.

**Sàng lọc:** KHÔNG trả lời được từ gold; không đúng ý đồ nhóm; câu hỏi mơ hồ; gold đáng ngờ — Gold là trách nhiệm của Ngân hàng Nhà nước Khu vực (chủ thể chỉ có ở tiêu đề Điều, gold không có), nhưng câu hỏi gán cho công ty đầu tư nước ngoài. · Gợi ý câu hỏi: Ngân hàng Nhà nước Khu vực có trách nhiệm gì trong việc kiểm tra, giám sát việc mở và sử dụng tài khoản vốn đầu tư trực tiếp nước ngoài?

**Gold: 38/2026/TT-NHNN Điều 16 khoản 2**

> 2. Thanh tra, kiểm tra, giám sát tình hình chấp hành quy định liên quan đến việc mở và sử dụng tài khoản vốn đầu tư quy định tại Thông tư này theo thẩm quyền. Thực hiện xử lý các hành vi vi phạm pháp luật trong lĩnh vực ngoại hối theo quy định của pháp luật.

---
## q021 · don_gian · khoan

Trạng thái: GIỮ
Câu hỏi: Khi sử dụng kinh phí hỗ trợ từ Quỹ hỗ trợ xây dựng chính sách, pháp luật, cần đảm bảo những nguyên tắc và điều kiện nào?

*Đáp án nháp của mô hình:* Phải tuân thủ nguyên tắc công khai, minh bạch, hiệu quả, tiết kiệm, phòng chống tham nhũng, lãng phí, tiêu cực và lợi ích nhóm, đồng thời đảm bảo đúng mục tiêu, phạm vi, đối tượng và điều kiện quy định, tránh trục lợi và hướng lái chính sách.

**Sàng lọc:** không thấy vấn đề — Câu hỏi ổn. Đáp án nháp thiếu ý phải tuân thủ Nghị quyết 197/2025/QH15, Nghị định 289/2025/NĐ-CP và pháp luật ngân sách.

**Gold: 10/2026/TT-BTP Điều 3 khoản 1**

> 1. Việc thực hiện kinh phí hỗ trợ, tài trợ của Quỹ phải bảo đảm tuân thủ nguyên tắc quy định tại Nghị quyết số 197/2025/QH15 về một số cơ chế, chính sách đặc biệt tạo đột phá trong xây dựng và tổ chức thi hành pháp luật, Nghị định số 289/2025/NĐ-CP, quy định của pháp luật về ngân sách nhà nước và quy định tại Thông tư này; bảo đảm đúng mục tiêu, phạm vi, đối tượng, điều kiện, nguồn tài chính của Quỹ; công khai, minh bạch, hiệu quả, tiết kiệm, phòng chống tham nhũng, lãng phí, tiêu cực, lợi ích nhóm, cục bộ và ngăn chặn mọi biểu hiện trục lợi, hướng lái chính sách trong công tác xây dựng chính sách, pháp luật.

---
## q022 · don_gian · khoan

Trạng thái: GIỮ
Câu hỏi: Khi dừng khai thác một công trình sử dụng chung, người quyết định cần làm gì trước khi thực hiện?

*Đáp án nháp của mô hình:* Phải thông báo bằng văn bản đến các tổ chức, cá nhân và hộ gia đình đang sử dụng công trình về quyết định dừng khai thác.

**Sàng lọc:** không thấy vấn đề — Gold không nói thông báo phải làm 'trước khi thực hiện'; câu hỏi thêm chi tiết về thời điểm mà gold không có. · Gợi ý câu hỏi: Khi quyết định dừng khai thác, sử dụng một công trình xây dựng sử dụng chung, người ra quyết định phải làm gì đối với những người đang sử dụng công trình?

**Gold: 135/2025/QH15 Điều 67 khoản 2**

> 2. Khi quyết định dừng khai thác, sử dụng đối với công trình sử dụng chung, chủ đầu tư, chủ sở hữu, chủ quản lý, sử dụng công trình hoặc cơ quan nhà nước có thẩm quyền phải thông báo bằng văn bản đến các tổ chức, cá nhân, hộ gia đình sử dụng công trình về quyết định của mình.

---
## q023 · don_gian · đầu khoản/điểm (không trung lập: span bắt đầu ngay đầu khoản hoặc điểm)

Trạng thái: GIỮ
Câu hỏi: Khi tổ chức một cuộc họp của doanh nghiệp, cần ghi rõ những thông tin nào về người tham gia kiểm phiếu?

*Đáp án nháp của mô hình:* Cần ghi rõ họ, tên và chữ ký của Chủ tịch Hội đồng quản trị, người giám sát kiểm phiếu và người kiểm phiếu.

**Sàng lọc:** chỉ trả lời được một phần từ gold; câu hỏi mơ hồ; gold đáng ngờ — Gold là điểm e đứng riêng, thiếu câu dẫn 'biên bản kiểm phiếu' khi lấy ý kiến cổ đông bằng văn bản (không phải cuộc họp). Câu hỏi nói 'cuộc họp' nên dễ khớp với biên bản họp Đại hội đồng cổ đông hoặc Hội đồng quản trị (Điều 150, 158). · Gợi ý câu hỏi: Biên bản kiểm phiếu khi lấy ý kiến cổ đông bằng văn bản phải có họ, tên, chữ ký của những ai?

**Gold: 59/2020/QH14 Điều 149 khoản 5**

> e) Họ, tên, chữ ký của Chủ tịch Hội đồng quản trị, người giám sát kiểm phiếu và người kiểm phiếu.

---
## q025 · don_gian · đầu khoản/điểm (không trung lập: span bắt đầu ngay đầu khoản hoặc điểm)

Trạng thái: GIỮ
Câu hỏi: Nếu chủ tọa hoặc người ghi biên bản không ký biên bản họp, thì biên bản đó có hiệu lực không?

*Đáp án nháp của mô hình:* Biên bản vẫn có hiệu lực nếu được tất cả thành viên khác của Hội đồng quản trị tham dự họp ký và đầy đủ các nội dung quy định.

**Sàng lọc:** câu hỏi mơ hồ — Quy định gần giống có ở Điều 60 (biên bản họp Hội đồng thành viên) và Điều 150 (biên bản họp Đại hội đồng cổ đông) cùng Luật; câu hỏi không nêu đây là họp Hội đồng quản trị. · Gợi ý câu hỏi: Biên bản họp Hội đồng quản trị có hiệu lực không nếu chủ tọa và người ghi biên bản từ chối ký?

**Gold: 59/2020/QH14 Điều 158 khoản 2**

> Trường hợp chủ tọa, người ghi biên bản từ chối ký biên bản họp nhưng nếu được tất cả thành viên khác của Hội đồng quản trị tham dự họp ký và có đầy đủ nội dung theo quy định tại các điểm a, b, c, d, đ, e, g và h khoản 1 Điều này thì biên bản này có hiệu lực.

---
## q027 · don_gian · đầu khoản/điểm (không trung lập: span bắt đầu ngay đầu khoản hoặc điểm)

Trạng thái: DỰ PHÒNG
Câu hỏi: Ủy ban Thẩm phán Tòa án quân sự quân khu có những nhiệm vụ gì?

*Đáp án nháp của mô hình:* Ủy ban Thẩm phán có nhiệm vụ thảo luận về chương trình, kế hoạch công tác của Tòa án quân sự quân khu và thảo luận báo cáo công tác của Chánh án Tòa án quân sự quân khu.

**Sàng lọc:** chỉ trả lời được một phần từ gold; gold đáng ngờ — Gold cắt danh sách sau điểm b, thiếu các điểm c, d, đ của cùng khoản, trong khi câu hỏi đòi toàn bộ nhiệm vụ. · Gợi ý câu hỏi: Ủy ban Thẩm phán Tòa án quân sự quân khu thảo luận những nội dung nào liên quan đến kế hoạch và báo cáo công tác của Tòa án?

**Gold: 34/2024/QH15 Điều 71 khoản 2**

> Ủy ban Thẩm phán Tòa án quân sự quân khu và tương đương có nhiệm vụ, quyền hạn sau đây:
> a) Thảo luận về chương trình, kế hoạch công tác của Tòa án quân sự quân khu và tương đương;
> b) Thảo luận báo cáo công tác của Chánh án Tòa án quân sự quân khu và tương đương;

---
## q028 · don_gian · đầu khoản/điểm (không trung lập: span bắt đầu ngay đầu khoản hoặc điểm)

Trạng thái: DỰ PHÒNG
Câu hỏi: Nếu phát hiện kiểm soát viên vi phạm nhiệm vụ, thì cần làm gì?

*Đáp án nháp của mô hình:* Phải gửi văn bản thông báo đến ban kiểm soát, yêu cầu người vi phạm ngừng hành vi vi phạm và khắc phục hậu quả.

**Sàng lọc:** không thấy vấn đề

**Gold: 59/2020/QH14 Điều 173 khoản 6**

> Trường hợp phát hiện có Kiểm soát viên vi phạm trong thực hiện quyền và nghĩa vụ được giao thì phải thông báo bằng văn bản đến Ban kiểm soát; yêu cầu người có hành vi vi phạm chấm dứt hành vi vi phạm và khắc phục hậu quả.

---
## q029 · don_gian · đầu khoản/điểm (không trung lập: span bắt đầu ngay đầu khoản hoặc điểm)

Trạng thái: DỰ PHÒNG
Câu hỏi: Người đi vay có thể bị từ chối cấp tín dụng không?

*Đáp án nháp của mô hình:* Có, tổ chức tín dụng có quyền từ chối yêu cầu cấp tín dụng nếu thấy không đủ điều kiện, không có hiệu quả hoặc không phù hợp với quy định của pháp luật.

**Sàng lọc:** không thấy vấn đề — Câu hỏi có/không quá chung: trả lời 'có' mà không cần truy hồi. Nên hỏi các trường hợp được từ chối. · Gợi ý câu hỏi: Tổ chức tín dụng được quyền từ chối yêu cầu cấp tín dụng của khách hàng trong những trường hợp nào?

**Gold: 32/2024/QH15 Điều 7 khoản 2**

> Tổ chức tín dụng, chi nhánh ngân hàng nước ngoài có quyền từ chối yêu cầu cấp tín dụng, cung ứng các dịch vụ khác nếu thấy không đủ điều kiện, không có hiệu quả, không phù hợp với quy định của pháp luật.

---
## q030 · don_gian · đầu khoản/điểm (không trung lập: span bắt đầu ngay đầu khoản hoặc điểm)

Trạng thái: DỰ PHÒNG
Câu hỏi: Công ty phát hành trái phiếu cần được kiểm tra, giám sát về những yếu tố nào liên quan đến việc đánh giá và xếp hạng tín nhiệm?

*Đáp án nháp của mô hình:* Công ty cần được kiểm tra, giám sát về hoạt động kiểm toán, định giá và xếp hạng tín nhiệm khi phát hành trái phiếu doanh nghiệp.

**Sàng lọc:** KHÔNG trả lời được từ gold; không đúng ý đồ nhóm; câu hỏi mơ hồ; gold đáng ngờ — Gold là trách nhiệm của Bộ Tài chính (chủ thể chỉ có ở tiêu đề Điều) trong việc giám sát tổ chức kiểm toán, thẩm định giá, xếp hạng tín nhiệm. Câu hỏi lại hỏi về việc kiểm tra công ty phát hành. · Gợi ý câu hỏi: Bộ Tài chính có trách nhiệm gì đối với tổ chức kiểm toán, doanh nghiệp thẩm định giá và tổ chức xếp hạng tín nhiệm cung cấp dịch vụ liên quan đến trái phiếu doanh nghiệp riêng lẻ?

**Gold: 200/2026/NĐ-CP Điều 43 khoản 3**

> Quản lý, giám sát, kiểm tra tổ chức kiểm toán, doanh nghiệp thẩm định giá, tổ chức xếp hạng tín nhiệm khi cung cấp dịch vụ liên quan đến trái phiếu doanh nghiệp riêng lẻ theo quy định của pháp luật về kiểm toán, pháp luật về giá, pháp luật về xếp hạng tín nhiệm.

---
## q031 · don_gian · đầu khoản/điểm (không trung lập: span bắt đầu ngay đầu khoản hoặc điểm)

Trạng thái: DỰ PHÒNG
Câu hỏi: Môi giới hàng hải là gì?

*Đáp án nháp của mô hình:* Là dịch vụ làm trung gian giúp các bên tham gia giao dịch trong lĩnh vực hàng hải như ký kết hợp đồng vận chuyển, bảo hiểm, thuê tàu, mua bán tàu biển hoặc thuê thuyền viên.

**Sàng lọc:** câu hỏi mơ hồ — Bộ luật Hàng hải 1990 (42-LCT/HĐNN8, có trong kho), Điều 150 có định nghĩa gần giống ('người môi giới hàng hải là người làm trung gian…'). · Gợi ý câu hỏi: Môi giới hàng hải được hiểu là loại dịch vụ gì và làm trung gian cho những loại hợp đồng nào?

**Gold: 95/2015/QH13 Điều 244 khoản 1**

> Môi giới hàng hải là dịch vụ làm trung gian cho các bên liên quan trong việc giao dịch, đàm phán, ký kết hợp đồng vận chuyển, hợp đồng bảo hiểm hàng hải, hợp đồng thuê tàu, hợp đồng mua bán tàu biển, hợp đồng lai dắt tàu biển, hợp đồng thuê thuyền viên và các hợp đồng khác liên quan đến hoạt động hàng hải theo hợp đồng môi giới hàng hải.

---
## q032 · don_gian · đầu khoản/điểm (không trung lập: span bắt đầu ngay đầu khoản hoặc điểm)

Trạng thái: DỰ PHÒNG
Câu hỏi: Nếu một cán bộ đang thi hành nhiệm vụ và dùng vũ lực gây thương tích cho người khác, với mức thương tật từ 31% trở lên, thì sẽ bị xử lý như thế nào?

*Đáp án nháp của mô hình:* Sẽ bị phạt cải tạo không giam giữ đến ba năm hoặc phạt tù từ ba tháng đến ba năm.

**⚠ Bản cũ:** gold ở BẢN CŨ, bản mới cũng có trong kho — 15/1999/QH10 Điều 107 ↔ 100/2015/QH13 Điều 137: KHÁC ÍT (chứa 0.63)
**Sàng lọc:** câu hỏi mơ hồ — Gold thuộc Bộ luật Hình sự 1999. Bộ luật Hình sự 2015, Điều 137 (có trong kho) cùng tội nhưng ngưỡng là 31–60% và mức tù 6 tháng–3 năm, nên đáp án lệch theo bản luật. Câu hỏi bỏ điều kiện 'ngoài những trường hợp pháp luật cho phép'. · Gợi ý câu hỏi: Người trong khi thi hành công vụ dùng vũ lực ngoài những trường hợp pháp luật cho phép, gây thương tích cho người khác với tỷ lệ thương tật từ 31% trở lên thì bị phạt như thế nào?

**Gold: 15/1999/QH10 Điều 107 khoản 1**

> Người nào trong khi thi hành công vụ dùng vũ lực ngoài những trường hợp pháp luật cho phép gây thương tích hoặc tổn hại cho sức khoẻ của người khác mà tỷ lệ thương tật từ 31% trở lên, thì bị phạt cải tạo không giam giữ đến ba năm hoặc phạt tù từ ba tháng đến ba năm.

---
## q033 · don_gian · đầu khoản/điểm (không trung lập: span bắt đầu ngay đầu khoản hoặc điểm)

Trạng thái: DỰ PHÒNG
Câu hỏi: Trong việc tuyển dụng và quản lý viên chức, cơ quan nào có quyền quyết định các nội dung thuộc thẩm quyền của đơn vị sự nghiệp công lập?

*Đáp án nháp của mô hình:* Cơ quan quản lý đơn vị sự nghiệp công lập có quyền quyết định các nội dung thuộc thẩm quyền của đơn vị đó.

**Sàng lọc:** KHÔNG trả lời được từ gold; không đúng ý đồ nhóm; câu hỏi mơ hồ — Câu hỏi hiểu sai gold. Gold (Điều 57: nhiệm vụ của bộ, cơ quan ngang bộ) nói về việc phân cấp thực hiện nội dung quản lý viên chức, trừ những nội dung thuộc thẩm quyền của đơn vị sự nghiệp công lập hoặc của cơ quan quản lý đơn vị đó; gold không nói cơ quan nào quyết định. Đáp án nháp chỉ lặp lại câu hỏi. · Gợi ý câu hỏi: Khi bộ, cơ quan ngang bộ phân cấp việc thực hiện nội dung quản lý viên chức, những nội dung nào không được đưa vào phạm vi phân cấp?

**Gold: 259/2026/NĐ-CP Điều 57 khoản 2**

> Phân cấp việc thực hiện các nội dung quy định tại điểm d khoản 1 Điều 55 Nghị định này, trừ những nội dung thuộc thẩm quyền của cơ quan quản lý đơn vị sự nghiệp công lập hoặc thuộc thẩm quyền của đơn vị sự nghiệp công lập theo quy định của Luật Viên chức số 129/2025/QH15, quy định tại Nghị định này.

---
## q035 · don_gian · đầu khoản/điểm (không trung lập: span bắt đầu ngay đầu khoản hoặc điểm)

Trạng thái: DỰ PHÒNG
Câu hỏi: Nếu một công trình xây dựng có nguy cơ mất an toàn thì có thể tiếp tục sử dụng không?

*Đáp án nháp của mô hình:* Không, chỉ được tiếp tục sử dụng khi công trình đã khắc phục sự cố hoặc được loại bỏ các nguy cơ gây mất an toàn.

**Sàng lọc:** không thấy vấn đề

**Gold: 135/2025/QH15 Điều 67 khoản 3**

> Việc khai thác, sử dụng công trình xây dựng chỉ được tiếp tục khi công trình đã được khắc phục sự cố hoặc được loại bỏ các nguy cơ gây mất an toàn.

---
## q036 · don_gian · đầu khoản/điểm (không trung lập: span bắt đầu ngay đầu khoản hoặc điểm)

Trạng thái: DỰ PHÒNG
Câu hỏi: Khi đăng ký hoạt động bay, doanh nghiệp vận chuyển cần cung cấp những thông tin gì về bản thân?

*Đáp án nháp của mô hình:* Cần cung cấp tên, địa chỉ bưu điện, thư điện tử của người khai thác tàu bay hoặc người vận chuyển, cùng với lịch bay.

**Sàng lọc:** câu hỏi mơ hồ — Cùng một danh mục 'Tên, địa chỉ bưu điện, thư điện tử...' lặp lại ở khoản 1, 5 và 6 của cùng Điều (đề nghị cấp phép, phép bay được cấp, phép bay sửa đổi). Câu hỏi nói 'đăng ký hoạt động bay', không khớp với 'đề nghị cấp phép bay (Cục Lãnh sự)'. Gold kết thúc ở 'b) Lịch bay:' còn bị cắt, nhưng phần a) cần cho câu trả lời vẫn đủ. · Gợi ý câu hỏi: Khi nộp đề nghị cấp phép bay đến Cục Lãnh sự, người đề nghị phải nêu những thông tin liên hệ nào của người khai thác tàu bay hoặc người vận chuyển?

**Gold: 222/2026/NĐ-CP Điều 18 khoản 1**

> a) Tên, địa chỉ bưu điện, thư điện tử của người khai thác tàu bay hoặc người vận chuyển;
> b) Lịch bay:

---
## q038 · don_gian · đầu khoản/điểm (không trung lập: span bắt đầu ngay đầu khoản hoặc điểm)

Trạng thái: DỰ PHÒNG
Câu hỏi: Nếu một người có trách nhiệm trong việc nhập khẩu, xuất khẩu hoặc sử dụng thuốc gây nghiện hoặc chất ma túy nhưng vi phạm quy định quản lý thì sẽ bị xử lý như thế nào?

*Đáp án nháp của mô hình:* Sẽ bị phạt tiền từ năm triệu đồng đến một trăm triệu đồng hoặc bị phạt tù từ một năm đến năm năm.

**⚠ Bản cũ:** gold ở BẢN CŨ, bản mới cũng có trong kho — 15/1999/QH10 Điều 201 ↔ 100/2015/QH13 Điều 259: KHÁC NHIỀU hoặc không còn (chứa 0.36)
**Sàng lọc:** câu hỏi mơ hồ — Gold thuộc Bộ luật Hình sự 1999. Kho còn có Bộ luật Hình sự 2015, trong đó tội tương ứng quy định khác (đòi hỏi đã bị xử lý trước, mức phạt khác), nên câu hỏi không nêu mốc thời gian sẽ mơ hồ. Câu hỏi chép khá sát phần điều kiện của gold. · Gợi ý câu hỏi: Theo quy định hình sự trước năm 2015, người có trách nhiệm trong việc xuất nhập khẩu, bảo quản hoặc sử dụng thuốc gây nghiện mà vi phạm quy định quản lý thì bị xử lý hình sự ra sao?

**Gold: 15/1999/QH10 Điều 201 khoản 1**

> Người nào có trách nhiệm trong việc xuất khẩu, nhập khẩu, mua bán, vận chuyển, bảo quản, phân phối, cấp phát, sử dụng thuốc gây nghiện hoặc các chất ma tuý khác mà vi phạm quy định về quản lý, sử dụng các chất đó, thì bị phạt tiền từ năm triệu đồng đến một trăm triệu đồng hoặc bị phạt tù từ một năm đến năm năm.

---
## q039 · don_gian · đầu khoản/điểm (không trung lập: span bắt đầu ngay đầu khoản hoặc điểm)

Trạng thái: DỰ PHÒNG
Câu hỏi: Nếu một cá nhân hoặc tổ chức có liên quan đến hóa chất bị chết, mất tích hoặc giải thể, và hóa chất đó không rõ nguồn gốc, thì chi phí xử lý sẽ lấy từ đâu?

*Đáp án nháp của mô hình:* Chi phí xử lý sẽ lấy từ nguồn ngân sách dự phòng cấp cho cơ quan có thẩm quyền xử phạt.

**Sàng lọc:** không thấy vấn đề — Câu hỏi nối các trường hợp bằng 'và', trong khi gold liệt kê các trường hợp riêng rẽ bằng 'hoặc'. Cụm 'có liên quan đến hóa chất' mơ hồ vì gold chỉ cá nhân, tổ chức quy định tại khoản 2. · Gợi ý câu hỏi: Khi cá nhân có trách nhiệm đã chết hoặc mất tích, tổ chức có trách nhiệm đã giải thể, phá sản, hoặc hóa chất không rõ nguồn gốc, thì chi phí xử lý hóa chất được lấy từ nguồn nào?

**Gold: 69/2025/QH15 Điều 46 khoản 3**

> Trường hợp cá nhân quy định tại khoản 2 Điều này bị chết hoặc mất tích; tổ chức quy định tại khoản 2 Điều này bị giải thể, phá sản; hóa chất, sản phẩm chứa chất độc không rõ nguồn gốc hoặc không xác định được chủ sở hữu thì chi phí xử lý hóa chất, sản phẩm chứa chất độc do cơ quan của người có thẩm quyền xử phạt ra quyết định thực hiện được lấy từ nguồn ngân sách dự phòng cấp cho cơ quan đó.

---
## q040 · don_gian · đầu khoản/điểm (không trung lập: span bắt đầu ngay đầu khoản hoặc điểm)

Trạng thái: DỰ PHÒNG
Câu hỏi: Cơ quan nào có quyền tổ chức tuyển dụng viên chức cho các đơn vị nhóm 3 và nhóm 4?

*Đáp án nháp của mô hình:* Các đơn vị nhóm 3 và nhóm 4 được tuyển dụng viên chức theo phân cấp của cơ quan quản lý viên chức hoặc theo ủy quyền từ cơ quan quản lý đơn vị sự nghiệp công lập.

**Sàng lọc:** không thấy vấn đề — Câu hỏi hỏi 'cơ quan nào', nhưng gold nói chính đơn vị nhóm 3, nhóm 4 tự tuyển dụng theo phân cấp hoặc ủy quyền. · Gợi ý câu hỏi: Đơn vị sự nghiệp công lập nhóm 3, nhóm 4 thực hiện tuyển dụng viên chức dựa trên cơ sở nào?

**Gold: 259/2026/NĐ-CP Điều 3 khoản 3**

> Đơn vị nhóm 3, đơn vị nhóm 4 thực hiện tuyển dụng viên chức theo phân cấp của cơ quan quản lý viên chức hoặc theo ủy quyền của cơ quan quản lý đơn vị sự nghiệp công lập.

---
## q041 · don_gian · đầu khoản/điểm (không trung lập: span bắt đầu ngay đầu khoản hoặc điểm)

Trạng thái: DỰ PHÒNG
Câu hỏi: Nếu một người cố ý làm lộ hoặc chiếm đoạt tài liệu bí mật công tác mà không thuộc các trường hợp đặc biệt thì sẽ bị xử lý như thế nào?

*Đáp án nháp của mô hình:* Bị phạt cải tạo không giam giữ đến 3 năm hoặc phạt tù từ 6 tháng đến 3 năm.

**Sàng lọc:** câu hỏi mơ hồ — Kho có cả Bộ luật Hình sự 1999 (Điều 286) với hành vi tương tự nhưng mức tù khác (từ 3 tháng thay vì 6 tháng). Câu hỏi không nêu mốc thời gian nên mơ hồ. · Gợi ý câu hỏi: Theo pháp luật hình sự hiện hành, người cố ý làm lộ bí mật công tác hoặc chiếm đoạt tài liệu bí mật công tác (không thuộc các tội đặc thù khác) bị phạt như thế nào?

**Gold: 100/2015/QH13 Điều 361 khoản 1**

> Người nào cố ý làm lộ bí mật công tác hoặc chiếm đoạt, mua bán, tiêu hủy tài liệu bí mật công tác, nếu không thuộc trường hợp quy định tại các điều 110, 337 và 342 của Bộ luật này, thì bị phạt cải tạo không giam giữ đến 03 năm hoặc phạt tù từ 06 tháng đến 03 năm.

---
## q042 · don_gian · đầu khoản/điểm (không trung lập: span bắt đầu ngay đầu khoản hoặc điểm)

Trạng thái: DỰ PHÒNG
Câu hỏi: Vợ, chồng, cha, mẹ, con, anh, chị, em của những người giữ chức vụ trong tổ chức tín dụng như thành viên Hội đồng quản trị, Tổng giám đốc có được làm kế toán trưởng hoặc người phụ trách tài chính của tổ chức đó không?

*Đáp án nháp của mô hình:* Không được làm kế toán trưởng hoặc người phụ trách tài chính của tổ chức tín dụng đó.

**Sàng lọc:** lộ đáp án / nhắc văn bản — Câu hỏi chép gần nguyên văn gold, gồm cả danh sách quan hệ thân nhân, các chức danh và 'Kế toán trưởng hoặc người phụ trách tài chính'. · Gợi ý câu hỏi: Người thân trong gia đình của thành viên Hội đồng quản trị hoặc Tổng giám đốc một tổ chức tín dụng có được giữ vị trí kế toán trưởng tại chính tổ chức đó không?

**Gold: 32/2024/QH15 Điều 42 khoản 3**

> Vợ, chồng, cha, mẹ, con, anh, chị, em của thành viên Hội đồng quản trị, thành viên Hội đồng thành viên, Tổng giám đốc (Giám đốc) tổ chức tín dụng và vợ, chồng của những người này không được là Kế toán trưởng hoặc là người phụ trách tài chính của tổ chức tín dụng đó.

---
## q043 · don_gian · đầu khoản/điểm (không trung lập: span bắt đầu ngay đầu khoản hoặc điểm)

Trạng thái: DỰ PHÒNG
Câu hỏi: Các điều kiện nào để bị coi là tội phạm có tổ chức, có tính chất chuyên nghiệp hoặc tái phạm nguy hiểm?

*Đáp án nháp của mô hình:* Khi hành vi phạm tội được thực hiện có sự tổ chức, có tính chất chuyên nghiệp và người phạm tội có tiền án, tiền sự hoặc có dấu hiệu tái phạm nguy hiểm, thì sẽ được coi là tội phạm có tổ chức, có tính chất chuyên nghiệp hoặc tái phạm nguy hiểm.

**⚠ Bản cũ:** gold ở BẢN CŨ, bản mới cũng có trong kho — 15/1999/QH10 Điều 157 ↔ 100/2015/QH13 Điều 195 khoản 2: GIỐNG (chứa 1.00)
**Sàng lọc:** KHÔNG trả lời được từ gold; không đúng ý đồ nhóm; câu hỏi mơ hồ; gold đáng ngờ — Gold chỉ gồm 3 nhãn tình tiết a–c, tách khỏi câu dẫn khoản 2 (tên tội, khung hình phạt). Gold không định nghĩa 'tội phạm có tổ chức...', các tình tiết này lại lặp ở rất nhiều điều. Đáp án nháp là bịa. Gold còn thuộc Bộ luật Hình sự 1999, trùng với bộ luật năm 2015.

**Gold: 15/1999/QH10 Điều 157 khoản 2**

> a) Có tổ chức;
> b) Có tính chất chuyên nghiệp;
> c) Tái phạm nguy hiểm;

---
## q024 · don_gian · trung_lap · TRUNG LẬP

Trạng thái: GIỮ
Câu hỏi: Khi có yêu cầu từ cơ quan, tổ chức hoặc cá nhân có thẩm quyền, người dân hoặc doanh nghiệp cần phải làm gì với thông tin và tài liệu liên quan?

*Đáp án nháp của mô hình:* Phải cung cấp thông tin và tài liệu liên quan khi được yêu cầu bởi cơ quan, tổ chức hoặc cá nhân có thẩm quyền.

**Sàng lọc:** chỉ trả lời được một phần từ gold; câu hỏi mơ hồ — Theo ngữ cảnh, gold là nghĩa vụ của người bị tố cáo trong tố tụng dân sự. Câu hỏi lại hỏi 'người dân hoặc doanh nghiệp' nên sai chủ thể và quá chung chung. Gold còn có ý 'chấp hành quyết định xử lý' mà câu hỏi bỏ qua. · Gợi ý câu hỏi: Trong tố tụng dân sự, người bị tố cáo có nghĩa vụ gì khi cơ quan, người có thẩm quyền yêu cầu cung cấp thông tin, tài liệu và khi có quyết định xử lý?

**Gold: 24/2004/QH11 Điều 400 khoản 2**

> cung cấp thông tin, tài liệu liên quan khi cơ quan, tổ chức, cá nhân có thẩm quyền yêu cầu;
> b) Chấp hành nghiêm chỉnh quyết định xử lý của cơ quan, tổ chức, cá nhân có thẩm quyền;

---
## q026 · don_gian · trung_lap · TRUNG LẬP

Trạng thái: GIỮ
Câu hỏi: Làm thế nào để đảm bảo việc sử dụng kinh phí hỗ trợ, tài trợ từ Quỹ được minh bạch và đúng mục đích?

*Đáp án nháp của mô hình:* Cần thực hiện kiểm tra, giám sát và công khai thông tin về việc hỗ trợ, tài trợ. Trường hợp sai phạm sẽ phải hoàn trả kinh phí và có thể bị bồi hoàn. Đồng thời, cần trích lập và sử dụng kinh phí quản lý từ nguồn tài trợ ngoài ngân sách nhà nước một cách hợp lý.

**Sàng lọc:** chỉ trả lời được một phần từ gold; không đúng ý đồ nhóm; câu hỏi mơ hồ; gold đáng ngờ — Gold là mảnh của phạm vi điều chỉnh (Điều 1), chỉ liệt kê tên các nội dung được hướng dẫn, không có quy định 'làm thế nào'. Đáp án nháp suy diễn. · Gợi ý câu hỏi: Ngoài tạm ứng, điều chỉnh và quyết toán kinh phí, phạm vi hướng dẫn về hỗ trợ, tài trợ của Quỹ hỗ trợ xây dựng chính sách, pháp luật còn gồm những nội dung nào?

**Gold: 10/2026/TT-BTP Điều 1 khoản 3**

> kiểm tra, giám sát, công khai thông tin về hỗ trợ, tài trợ; hoàn trả, bồi hoàn kinh phí hỗ trợ, tài trợ và trích lập, sử dụng kinh phí quản lý từ nguồn tài trợ ngoài ngân sách nhà nước của Quỹ.

---
## q034 · don_gian · trung_lap · TRUNG LẬP

Trạng thái: GIỮ
Câu hỏi: Khi kiểm tra báo cáo tài chính của một tổ chức tín dụng, người quản lý cần đánh giá những yếu tố nào để đảm bảo tính minh bạch và chính xác?

*Đáp án nháp của mô hình:* Cần đánh giá tính hợp lý, hợp pháp, trung thực và mức độ cẩn trọng trong công tác kế toán, thống kê và lập báo cáo tài chính.

**Sàng lọc:** không thấy vấn đề — Theo ngữ cảnh, đây là nhiệm vụ của Ban kiểm soát khi thẩm định báo cáo tài chính. Câu hỏi gán cho 'người quản lý' là sai chủ thể. · Gợi ý câu hỏi: Khi thẩm định báo cáo tài chính của tổ chức tín dụng, Ban kiểm soát phải đánh giá những khía cạnh nào của công tác kế toán, thống kê?

**Gold: 32/2024/QH15 Điều 52 khoản 4**

> đánh giá tính hợp lý, hợp pháp, trung thực và mức độ cẩn trọng trong công tác kế toán, thống kê và lập báo cáo tài chính.

---
## q037 · don_gian · trung_lap · TRUNG LẬP

Trạng thái: GIỮ
Câu hỏi: Làm thế nào để xử lý các khoản tiền hoặc tài sản còn lại khi thực hiện thi hành án dân sự?

*Đáp án nháp của mô hình:* Cần đề xuất kịp thời các biện pháp xử lý các khoản tiền, tài sản tồn đọng theo quy định của pháp luật với người đứng đầu đơn vị.

**Sàng lọc:** chỉ trả lời được một phần từ gold; câu hỏi mơ hồ — Gold là trách nhiệm của Chấp hành viên: kịp thời đề xuất biện pháp xử lý tiền, tài sản tồn đọng với Thủ trưởng đơn vị; gold không nêu cách xử lý. Câu hỏi dùng 'còn lại' thay cho 'tồn đọng' và không nêu chủ thể. · Gợi ý câu hỏi: Trong kế toán nghiệp vụ thi hành án dân sự, khi có các khoản tiền, tài sản tồn đọng thì Chấp hành viên phải làm gì?

**Gold: 107/2026/TT-BTC Điều 7 khoản 2**

> kịp thời đề xuất biện pháp xử lý các khoản tiền, tài sản tồn đọng theo quy định của pháp luật với Thủ trưởng đơn vị.

---
## q044 · don_gian · trung_lap · TRUNG LẬP

Trạng thái: GIỮ
Câu hỏi: Trong một tổ chức tín dụng, ai là những người có trách nhiệm giám sát hoạt động của tổ chức đó?

*Đáp án nháp của mô hình:* Chủ tịch, thành viên khác của Hội đồng thành viên và Trưởng ban, thành viên khác của Ban kiểm soát

**Sàng lọc:** KHÔNG trả lời được từ gold; không đúng ý đồ nhóm; câu hỏi mơ hồ; gold đáng ngờ — Gold chỉ là mảnh danh sách chức danh, không có câu dẫn. Theo ngữ cảnh, đó là những người mà Ban kiểm soát đặc biệt có quyền đình chỉ, tạm đình chỉ quyền và nghĩa vụ, không phải 'người giám sát'. Câu hỏi và đáp án nháp hiểu sai. · Gợi ý câu hỏi: Ban kiểm soát đặc biệt có quyền đình chỉ, tạm đình chỉ việc thực hiện quyền, nghĩa vụ của những chức danh nào thuộc Hội đồng thành viên và Ban kiểm soát của tổ chức tín dụng được kiểm soát đặc biệt?

**Gold: 32/2024/QH15 Điều 47 khoản 2**

> Chủ tịch, thành viên khác của Hội đồng thành viên; Trưởng ban, thành viên khác của Ban kiểm soát;

---
## q206 · don_gian · trung_lap · TRUNG LẬP

Trạng thái: GIỮ
Câu hỏi: Những loại thỏa ước lao động tập thể nào được quy định trong Bộ Luật Lao động?

*Đáp án nháp của mô hình:* Gồm thỏa ước lao động tập thể doanh nghiệp, thỏa ước lao động tập thể ngành, thỏa ước lao động tập thể có nhiều doanh nghiệp và các thỏa ước lao động tập thể khác.

**Sàng lọc:** lộ đáp án / nhắc văn bản — Câu hỏi nhắc tên văn bản (Bộ luật Lao động). · Gợi ý câu hỏi: Thỏa ước lao động tập thể gồm những loại nào?

**Gold: 45/2019/QH14 Điều 75 khoản 1**

> Thỏa ước lao động tập thể bao gồm thỏa ước lao động tập thể doanh nghiệp, thỏa ước lao động tập thể ngành, thỏa ước lao động tập thể có nhiều doanh nghiệp và các thỏa ước lao động tập thể khác.

---
## q207 · don_gian · trung_lap · TRUNG LẬP

Trạng thái: XOÁ
Câu hỏi: Khi vận chuyển quân sự bằng tàu buôn thì có áp dụng quy định về vận chuyển hàng hóa, hành khách và hành lý không?

*Đáp án nháp của mô hình:* Không áp dụng quy định về vận chuyển hàng hóa, hành khách và hành lý khi vận chuyển quân sự bằng tàu buôn.

**⚠ Bản cũ:** gold ở BẢN CŨ, bản mới cũng có trong kho — 42-LCT/HĐNN8 Điều 3 ↔ 95/2015/QH13 Điều 189: KHÁC NHIỀU hoặc không còn (chứa 0.25)
**Sàng lọc:** lộ đáp án / nhắc văn bản — Câu hỏi có/không chép gần nguyên văn gold, đáp án gần như lộ ngay trong câu hỏi. · Gợi ý câu hỏi: Loại hình vận chuyển nào bằng tàu buôn không chịu sự điều chỉnh của các quy định về vận chuyển hàng hóa, hành khách và hành lý?

**Gold: 42-LCT/HĐNN8 Điều 3**

> Các quy định về vận chuyển hàng hoá, hành khách và hành lý không áp dụng đối với việc vận chuyển quân sự bằng tầu buôn.

---
## q208 · don_gian · trung_lap · TRUNG LẬP

Trạng thái: GIỮ
Câu hỏi: Nếu một vụ án rất phức tạp, thì thời gian để trả lời có thể kéo dài bao nhiêu ngày?

*Đáp án nháp của mô hình:* Không quá 120 ngày kể từ ngày nhận được văn bản kiến nghị.

**Sàng lọc:** câu hỏi mơ hồ — Câu hỏi không nói 'trả lời' cái gì (kiến nghị xem xét lại bản án theo thủ tục giám đốc thẩm, tái thẩm) và tự đổi 'phức tạp' thành 'rất phức tạp'; chủ thể nằm ở câu liền trước gold. · Gợi ý câu hỏi: Khi Tòa án trả lời kiến nghị của cơ quan thi hành án về việc xem xét lại bản án theo thủ tục giám đốc thẩm, tái thẩm, nếu vụ án phức tạp thì thời hạn trả lời được kéo dài tối đa bao lâu?

**Gold: 101/2015/QH13 Điều 366**

> Trường hợp vụ án phức tạp thì thời hạn trả lời có thể kéo dài nhưng không quá 120 ngày kể từ ngày nhận được văn bản kiến nghị.

---
## q209 · don_gian · trung_lap · TRUNG LẬP

Trạng thái: GIỮ
Câu hỏi: Nếu một hợp đồng phụ bị vô hiệu thì hợp đồng chính có bị chấm dứt không?

*Đáp án nháp của mô hình:* Hợp đồng chính vẫn tiếp tục hiệu lực, trừ khi các bên đã đồng ý rằng hợp đồng phụ là một phần không thể tách rời của hợp đồng chính.

**Sàng lọc:** không thấy vấn đề

**Gold: 33/2005/QH11 Điều 410 khoản 2**

> Quy định này không áp dụng đối với các biện pháp bảo đảm thực hiện nghĩa vụ dân sự.
> 3. Sự vô hiệu của hợp đồng phụ không làm chấm dứt hợp đồng chính, trừ trường hợp các bên thoả thuận hợp đồng phụ là một phần không thể tách rời của hợp đồng chính.

---
## q210 · don_gian · trung_lap · TRUNG LẬP

Trạng thái: GIỮ
Câu hỏi: Thẩm phán Tòa án nhân dân được bổ nhiệm lại thì nhiệm kỳ của họ kết thúc khi nào?

*Đáp án nháp của mô hình:* Khi nghỉ hưu hoặc chuyển công tác khác

**Sàng lọc:** không thấy vấn đề

**Gold: 34/2024/QH15 Điều 100 khoản 2**

> Thẩm phán Tòa án nhân dân được bổ nhiệm lại có nhiệm kỳ đến khi nghỉ hưu hoặc chuyển công tác khác.

---
## q211 · don_gian · trung_lap · TRUNG LẬP

Trạng thái: GIỮ
Câu hỏi: Nếu một cơ quan hoặc tổ chức muốn dùng tạm thời lòng đường hoặc vỉa hè cho một sự kiện như lễ hội, hoạt động văn hóa, thì cần làm gì?

*Đáp án nháp của mô hình:* Phải có phương án sử dụng tạm thời và được cơ quan có thẩm quyền cho phép, sau đó cơ quan đó phải gửi thông báo cho cơ quan Cảnh sát giao thông.

**Sàng lọc:** không thấy vấn đề

**Gold: 36/2024/QH15 Điều 77 khoản 1**

> Trường hợp cần thiết sử dụng tạm thời lòng đường, vỉa hè phục vụ sự kiện chính trị, hoạt động văn hoá, thể thao và mục đích khác, cơ quan, tổ chức, cá nhân có nhu cầu sử dụng tạm thời lòng đường, vỉa hè phải có phương án sử dụng tạm thời lòng đường, vỉa hè và được cơ quan có thẩm quyền cho phép; cơ quan cho phép sử dụng tạm thời lòng đường, vỉa hè gửi thông báo ngay cho cơ quan Cảnh sát giao thông.

---
## q213 · don_gian · trung_lap · TRUNG LẬP

Trạng thái: GIỮ
Câu hỏi: Thời điểm nghỉ hưu của một viên chức được tính như thế nào?

*Đáp án nháp của mô hình:* Là ngày 01 của tháng liền kề sau tháng viên chức đủ tuổi nghỉ hưu theo quy định.

**Sàng lọc:** không thấy vấn đề

**Gold: 259/2026/NĐ-CP Điều 54 khoản 1**

> Thời điểm nghỉ hưu là ngày 01 của tháng liền kề sau tháng viên chức đủ tuổi nghỉ hưu theo quy định.

---
## q214 · don_gian · trung_lap · TRUNG LẬP

Trạng thái: GIỮ
Câu hỏi: Khi một cá nhân muốn mua trái phiếu doanh nghiệp, cần làm gì để đảm bảo tuân thủ quy định?

*Đáp án nháp của mô hình:* Cá nhân phải ký văn bản xác nhận đã thực hiện các quy định liên quan đến việc mua trái phiếu như được nêu trong quy định.

**Sàng lọc:** câu hỏi mơ hồ — Câu hỏi quá chung ('cần làm gì để tuân thủ quy định'), không nêu bối cảnh chào bán trái phiếu riêng lẻ; nội dung cần xác nhận nằm ở điểm a–d khoản 4 Điều 9, không có trong gold. · Gợi ý câu hỏi: Trong đợt chào bán trái phiếu doanh nghiệp riêng lẻ, nhà đầu tư mua trái phiếu là cá nhân phải thực hiện thủ tục gì?

**Gold: 200/2026/NĐ-CP Điều 15 khoản 3**

> Nhà đầu tư mua trái phiếu là cá nhân phải ký văn bản xác nhận đã thực hiện các quy định tại các điểm a, b, c và d khoản 4 Điều 9 Nghị định này.
> 4. Doanh nghiệp tổ chức chào bán trái phiếu theo phương thức phát hành được nêu trong Bản công bố thông tin trước đợt chào bán.

---
## q215 · don_gian · trung_lap · TRUNG LẬP

Trạng thái: GIỮ
Câu hỏi: Sau khi cơ sở giáo dục đã khắc phục hoàn toàn nguyên nhân dẫn đến việc bị đình chỉ, thì điều kiện nào để trung tâm giáo dục được phép hoạt động trở lại?

*Đáp án nháp của mô hình:* Sau khi khắc phục hoàn toàn nguyên nhân dẫn đến việc bị đình chỉ, cơ sở giáo dục sẽ được hoạt động trở lại nếu cơ quan có thẩm quyền xác nhận và không có ý kiến yêu cầu tiếp tục kiểm tra, xử lý trong vòng 05 ngày làm việc kể từ ngày nhận được báo cáo.

**Sàng lọc:** không thấy vấn đề — Câu hỏi dùng lẫn 'cơ sở giáo dục' và 'trung tâm giáo dục', tiền đề 'đã khắc phục hoàn toàn' hé một phần đáp án. Đáp án nháp sai khi nối hai điều kiện bằng 'và', trong khi gold ghi 'hoặc'. · Gợi ý câu hỏi: Trung tâm giáo dục bị đình chỉ hoạt động được tổ chức hoạt động trở lại khi nào?

**Gold: 360/2026/NĐ-CP Điều 42 khoản 2**

> Trung tâm giáo dục được tổ chức hoạt động trở lại sau khi cấp có thẩm quyền xác nhận đã khắc phục đầy đủ nguyên nhân dẫn đến việc đình chỉ hoặc hết thời hạn 05 ngày làm việc kể từ ngày nhận được báo cáo mà cấp có thẩm quyền không có ý kiến yêu cầu tiếp tục kiểm tra, xử lý.

---
## q216 · don_gian · trung_lap · TRUNG LẬP

Trạng thái: XOÁ
Câu hỏi: Nếu một cuộc đình công là bất hợp pháp và gây thiệt hại cho người sử dụng lao động thì ai phải chịu trách nhiệm bồi thường?

*Đáp án nháp của mô hình:* Tổ chức công đoàn lãnh đạo cuộc đình công phải bồi thường thiệt hại cho người sử dụng lao động.

**⚠ Bản cũ:** gold ở BẢN CŨ, bản mới cũng có trong kho — 10/2012/QH13 Điều 233 ↔ 45/2019/QH14 Điều 217 khoản 2: KHÁC ÍT (chứa 0.89)
**Sàng lọc:** không thấy vấn đề

**Gold: 10/2012/QH13 Điều 233 khoản 1**

> Trong trường hợp cuộc đình công là bất hợp pháp mà gây thiệt hại cho người sử dụng lao động thì tổ chức công đoàn lãnh đạo đình công phải bồi thường thiệt hại theo quy định của pháp luật.

---
## q217 · don_gian · trung_lap · TRUNG LẬP

Trạng thái: DỰ PHÒNG
Câu hỏi: Khi thành lập mới một thôn do sáp nhập các thôn cũ từ ngày 26 tháng 5 năm 2026, thì số người có uy tín của thôn mới được quyết định như thế nào?

*Đáp án nháp của mô hình:* Chủ tịch Ủy ban nhân dân cấp xã quyết định số lượng người có uy tín của thôn mới, nhưng không được vượt quá tổng số người có uy tín của các thôn trước khi sáp nhập.

**Sàng lọc:** không thấy vấn đề — Câu đầu của gold là mảnh 'Trừ trường hợp quy định tại khoản 2' nhưng phần sau đủ nghĩa; câu hỏi ổn.

**Gold: 307/2026/NĐ-CP Điều 6 khoản 1**

> Trừ trường hợp quy định tại khoản 2 Điều này.
> 2. Trường hợp thôn thành lập mới do sắp xếp, sáp nhập các thôn từ ngày 26 tháng 5 năm 2026, Chủ tịch Ủy ban nhân dân cấp xã tùy theo tình hình thực tế, quyết định số lượng người có uy tín của thôn mới nhưng không vượt quá tổng số người có uy tín của các thôn trước khi sáp nhập.

---
## q218 · don_gian · trung_lap · TRUNG LẬP

Trạng thái: DỰ PHÒNG
Câu hỏi: Hành vi phạm tội hoặc hậu quả của hành vi phạm tội xảy ra trên tàu bay, tàu biển Việt Nam hoặc trong vùng đặc quyền kinh tế, thềm lục địa của Việt Nam sẽ được xử lý như thế nào?

*Đáp án nháp của mô hình:* Sẽ được áp dụng quy định của Bộ luật Hình sự đối với hành vi đó.

**Sàng lọc:** chỉ trả lời được một phần từ gold; lộ đáp án / nhắc văn bản — Câu hỏi chép gần nguyên văn gold; 'xử lý như thế nào' mơ hồ, còn gold chỉ nói 'Quy định này cũng được áp dụng' mà không có câu trước để biết 'quy định này' là gì. · Gợi ý câu hỏi: Tội phạm xảy ra trên một chiếc máy bay mang quốc tịch Việt Nam hoặc ở thềm lục địa của Việt Nam có thuộc phạm vi áp dụng của luật hình sự Việt Nam không?

**Gold: 100/2015/QH13 Điều 5 khoản 1**

> Quy định này cũng được áp dụng đối với hành vi phạm tội hoặc hậu quả của hành vi phạm tội xảy ra trên tàu bay, tàu biển mang quốc tịch Việt Nam hoặc tại vùng đặc quyền kinh tế, thềm lục địa của Việt Nam.

---
## q219 · don_gian · trung_lap · TRUNG LẬP

Trạng thái: DỰ PHÒNG
Câu hỏi: Khi thực hiện nghiệm thu dự án được hỗ trợ từ Quỹ hỗ trợ xây dựng chính sách, pháp luật, cần kiểm tra những nội dung gì để xác định việc thanh toán kinh phí?

*Đáp án nháp của mô hình:* Cần xác định rõ sản phẩm và kết quả đã hoàn thành, mức độ đáp ứng mục tiêu và tiến độ, chất lượng, giá trị kinh phí đủ điều kiện thanh toán, số tiền còn lại để thanh toán và số tiền không sử dụng phải hoàn trả theo quy định.

**Sàng lọc:** không thấy vấn đề

**Gold: 10/2026/TT-BTP Điều 16 khoản 5**

> Biên bản nghiệm thu phải xác định rõ sản phẩm, kết quả đã hoàn thành; mức độ đáp ứng mục tiêu, phạm vi, nội dung, chất lượng, tiến độ; giá trị kinh phí đủ điều kiện thanh, quyết toán; số kinh phí còn được thanh, quyết toán; số kinh phí không sử dụng hoặc sử dụng không hết phải hoàn trả theo quy định tại Điều 22 của Thông tư này.

---
## q220 · don_gian · trung_lap · TRUNG LẬP

Trạng thái: DỰ PHÒNG
Câu hỏi: Khi cung cấp hồ sơ, chứng từ cho kế toán trong quá trình thi hành án dân sự, người cung cấp cần chịu trách nhiệm về điều gì?

*Đáp án nháp của mô hình:* Cần chịu trách nhiệm về sự chính xác, trung thực, hợp pháp và hợp lệ của các chứng từ, tài liệu cũng như số liệu ghi trên hồ sơ và chứng từ đó.

**Sàng lọc:** không thấy vấn đề

**Gold: 107/2026/TT-BTC Điều 7 khoản 1**

> Chịu trách nhiệm trước pháp luật về sự chính xác, trung thực, hợp pháp, hợp lệ của các chứng từ, tài liệu đã cung cấp, số liệu ghi trên hồ sơ, chứng từ chuyển cho kế toán ghi sổ.

---
## q221 · don_gian · trung_lap · TRUNG LẬP

Trạng thái: DỰ PHÒNG
Câu hỏi: Người nộp thuế có thể tra cứu thông tin giao dịch điện tử trước đó ở đâu và cách làm thế nào?

*Đáp án nháp của mô hình:* Người nộp thuế có thể tra cứu thông tin giao dịch điện tử trước đó trên Cổng thông tin điện tử của Tổng cục Thuế, Cổng thông tin điện tử của cơ quan nhà nước có thẩm quyền, hoặc tổ chức cung cấp dịch vụ T-VAN bằng cách sử dụng tài khoản hoặc mã giao dịch thuế điện tử đã được cấp.

**Sàng lọc:** không thấy vấn đề

**Gold: 19/2021/TT-BTC Điều 12 khoản 2**

> Người nộp thuế được tra cứu các thông tin của giao dịch điện tử trước đó trên Cổng thông tin điện tử của Tổng cục Thuế, Cổng thông tin điện tử của cơ quan nhà nước có thẩm quyền, tổ chức cung cấp dịch vụ T-VAN bằng cách sử dụng tài khoản hoặc mã giao dịch thuế điện tử đã được cấp cho đến khi chứng từ điện tử hết thời hạn lưu trữ theo quy định.

---
## q222 · don_gian · trung_lap · TRUNG LẬP

Trạng thái: DỰ PHÒNG
Câu hỏi: Khi bầu thành viên Hội đồng quản trị hoặc Kiểm soát viên của một công ty, thì cách xác định ai trúng cử là gì?

*Đáp án nháp của mô hình:* Xác định theo số phiếu bầu từ cao xuống thấp, bắt đầu từ ứng cử viên có số phiếu bầu cao nhất, cho đến khi đủ số thành viên theo quy định trong Điều lệ công ty.

**Sàng lọc:** không thấy vấn đề

**Gold: 59/2020/QH14 Điều 148 khoản 3**

> Người trúng cử thành viên Hội đồng quản trị hoặc Kiểm soát viên được xác định theo số phiếu bầu tính từ cao xuống thấp, bắt đầu từ ứng cử viên có số phiếu bầu cao nhất cho đến khi đủ số thành viên quy định tại Điều lệ công ty.

---
## q223 · don_gian · trung_lap · TRUNG LẬP

Trạng thái: DỰ PHÒNG
Câu hỏi: Người điều khiển xe máy chuyên dụng muốn chuyển từ hạng C lên hạng CE hoặc CX cần đáp ứng điều kiện tuổi nào?

*Đáp án nháp của mô hình:* Phải đủ 19 tuổi trở lên

**Sàng lọc:** câu hỏi mơ hồ — Gold nói về đào tạo chuyển tiếp giấy phép lái xe quân sự theo chỉ tiêu của Bộ Tổng Tham mưu, không phải 'người điều khiển xe máy chuyên dụng'; thiếu ngữ cảnh quân sự nên dễ lẫn với quy định nâng hạng giấy phép lái xe dân sự. · Gợi ý câu hỏi: Trong đào tạo lái xe quân sự, người được đào tạo chuyển tiếp từ hạng C lên hạng CE hoặc CX phải đáp ứng điều kiện gì về chỉ tiêu và độ tuổi?

**Gold: 131/2026/TT-BQP Điều 8 khoản 2**

> Các trường hợp đào tạo chuyển tiếp từ hạng C lên hạng CE hoặc CX theo chỉ tiêu của Bộ Tổng Tham mưu và phải đủ 19 tuổi trở lên.

---
## q045 · don_gian · phien_ban · phiên bản

Trạng thái: GIỮ
Câu hỏi: Khi một công chức lãnh đạo, quản lý được điều động đến vị trí có phụ cấp thấp hơn, thì trong thời gian nào đó họ vẫn được giữ nguyên phụ cấp chức vụ?

*Đáp án nháp của mô hình:* Trong thời gian 06 tháng

**Sàng lọc:** không đúng ý đồ nhóm — Khoản 1 (bảo lưu phụ cấp chức vụ 06 tháng) giống hệt bản cũ nên câu hỏi không phân biệt được phiên bản; phần thay đổi nằm ở khoản 2–3 (chế độ biệt phái). · Gợi ý câu hỏi: Theo quy định hiện hành, công chức được cử biệt phái đến nơi có chế độ phụ cấp, chính sách hỗ trợ đặc thù theo nghề, theo công việc hoặc theo địa bàn thì được hưởng những chế độ gì và do cơ quan nào chi trả?

**Gold: 10/2026/VBHN-NĐ-BNV Điều 27**

> Điều 27. Chế độ, chính sách đối với công chức được điều động, biệt phái[13]
> 1. Công chức giữ chức vụ lãnh đạo, quản lý được điều động đến vị trí công tác khác mà phụ cấp chức vụ mới thấp hơn phụ cấp chức vụ hiện đảm nhiệm thì được bảo lưu phụ cấp chức vụ trong thời gian 06 tháng.
> 2. Cơ quan, tổ chức, đơn vị cử công chức biệt phái có trách nhiệm trả lương và bảo đảm các quyền lợi khác của công chức trong thời gian được cử biệt phái. Trường hợp cơ quan, tổ chức, đơn vị nơi được cử đến biệt phái có chế độ phụ cấp, chính sách hỗ trợ đặc thù theo nghề, theo công việc hoặc theo địa bàn thì ngoài lương và các quyền lợi khác do cơ quan, tổ chức, đơn vị cử công chức biệt phái chi trả, công chức còn được hưởng các chế độ, chính sách đặc thù do cơ quan, tổ chức, đơn vị nơi được cử đến biệt phái chi trả.
> 3. Trường hợp công chức được cử biệt phái đến làm việc ở vùng có điều kiện kinh tế - xã hội đặc biệt khó khăn được hưởng các chế độ, chính sách ưu đãi khác theo quy định của pháp luật.

**Bản CŨ (đã bị 300/2026/NĐ-CP sửa): 170/2025/NĐ-CP Điều 27**

> Điều 27. Chế độ, chính sách đối với công chức được điều động, biệt phái
> 1. Công chức giữ chức vụ lãnh đạo, quản lý được điều động đến vị trí công tác khác mà phụ cấp chức vụ mới thấp hơn phụ cấp chức vụ hiện đảm nhiệm thì được bảo lưu phụ cấp chức vụ trong thời gian 06 tháng.
> 2. Cơ quan, tổ chức cử công chức biệt phái có trách nhiệm trả lương và bảo đảm các quyền lợi khác của công chức trong thời gian được cử biệt phái; bố trí công việc phù hợp cho công chức khi hết thời gian biệt phái. Trường hợp cơ quan, tổ chức nơi được cử đến biệt phái có chế độ, chính sách đặc thù thì ngoài lương và các quyền lợi khác do cơ quan, tổ chức cử công chức biệt phái chi trả, công chức còn được hưởng các chế độ, chính sách đặc thù do cơ quan, tổ chức nơi được cử đến biệt phái chi trả.
> 3. Trường hợp công chức được biệt phái đến làm việc ở miền núi, biên giới, hải đảo, vùng sâu, vùng xa, vùng dân tộc thiểu số, vùng có điều kiện kinh tế - xã hội đặc biệt khó khăn được hưởng các chế độ, chính sách ưu đãi theo quy định của pháp luật.

---
## q046 · don_gian · phien_ban · phiên bản

Trạng thái: GIỮ
Câu hỏi: Hiện nay, cơ quan thuế xử lý hồ sơ đăng ký, thay đổi hoặc giải thể doanh nghiệp, hợp tác xã như thế nào?

*Đáp án nháp của mô hình:* Cơ quan thuế căn cứ vào thông tin từ Hệ thống thông tin quốc gia về đăng ký doanh nghiệp, đăng ký hợp tác xã để xử lý và trả kết quả cho cơ quan đăng ký kinh doanh, đăng ký hợp tác xã trong thời hạn quy định, đồng thời cập nhật thông tin người nộp thuế vào Hệ thống thông tin đăng ký thuế.

**Sàng lọc:** không thấy vấn đề — Câu hỏi rộng; đáp án nháp bỏ qua đúng phần đã thay đổi (căn cứ Thông tư 86/2024 thay cho Thông tư 105/2020 và Quy chế trao đổi thông tin; chuyển trụ sở sang xã, phường, đặc khu) nên khó phân biệt bản cũ với bản mới. · Gợi ý câu hỏi: Theo quy định hiện hành, cơ quan thuế căn cứ vào những thông tin và quy định nào để xử lý, trả kết quả hồ sơ đăng ký doanh nghiệp, hợp tác xã nhận qua Hệ thống thông tin quốc gia về đăng ký doanh nghiệp, đăng ký hợp tác xã?

**Gold: 21/VBHN-BTC Điều 35 khoản 2 điểm a**

> a) Đối với hồ sơ cơ quan thuế phải trả kết quả (gồm hồ sơ đăng ký doanh nghiệp, đăng ký hợp tác xã; hồ sơ đăng ký thay đổi trụ sở sang xã, phường, đặc khu khác dẫn đến thay đổi cơ quan thuế quản lý; hồ sơ đăng ký giải thể doanh nghiệp, hợp tác xã; chấm dứt hoạt động chi nhánh, văn phòng đại diện, địa điểm kinh doanh) cho cơ quan đăng ký kinh doanh, đăng ký hợp tác xã qua Hệ thống thông tin quốc gia về đăng ký doanh nghiệp, đăng ký hợp tác xã:
> Cơ quan thuế căn cứ vào thông tin trên Hệ thống thông tin đăng ký thuế do Hệ thống thông tin quốc gia về đăng ký doanh nghiệp, đăng ký hợp tác xã gửi đến và quy định tại Thông tư số 86/2024/TT-BTC để xử lý và trả kết quả cho cơ quan đăng ký kinh doanh, đăng ký hợp tác xã qua Hệ thống thông tin quốc gia về đăng ký doanh nghiệp, đăng ký hợp tác xã theo đúng thời hạn quy định. Đồng thời, cập nhật thông tin của người nộp thuế vào Hệ thống thông tin đăng ký thuế. Cơ quan đăng ký kinh doanh, đăng ký hợp tác xã trả kết quả cho người nộp thuế theo quy định tại Luật Doanh nghiệp, Luật Hợp tác xã, Luật tổ chức tín dụng và các văn bản hướng dẫn thi hành.

**Bản CŨ (đã bị 40/2025/TT-BTC sửa): 19/2021/TT-BTC Điều 35 khoản 2 điểm a**

> a) Đối với hồ sơ cơ quan thuế phải trả kết quả (gồm hồ sơ đăng ký doanh nghiệp, đăng ký hợp tác xã; hồ sơ đăng ký thay đổi trụ sở sang quận, huyện, thị xã, tỉnh, thành phố khác dẫn đến thay đổi cơ quan thuế quản lý; hồ sơ đăng ký giải thể doanh nghiệp, hợp tác xã; chấm dứt hoạt động chi nhánh, văn phòng đại diện, địa điểm kinh doanh) cho cơ quan đăng ký kinh doanh, đăng ký hợp tác xã qua Hệ thống thông tin quốc gia về đăng ký doanh nghiệp, đăng ký hợp tác xã:
> Cơ quan thuế căn cứ vào thông tin trên Hệ thống thông tin đăng ký thuế do Hệ thống thông tin quốc gia về đăng ký doanh nghiệp, đăng ký hợp tác xã gửi đến và quy định tại Thông tư số 105/2020/TT-BTC, Quy chế trao đổi thông tin giữa Bộ Kế hoạch và Đầu tư và Bộ Tài chính để xử lý và trả kết quả cho cơ quan đăng ký kinh doanh, đăng ký hợp tác xã qua Hệ thống thông tin quốc gia về đăng ký doanh nghiệp, đăng ký hợp tác xã theo đúng thời hạn quy định. Đồng thời, cập nhật thông tin của người nộp thuế vào Hệ thống thông tin đăng ký thuế. Cơ quan đăng ký kinh doanh, đăng ký hợp tác xã trả kết quả cho người nộp thuế theo quy định tại Luật Doanh nghiệp, Luật Hợp tác xã, Luật tổ chức tín dụng và các văn bản hướng dẫn thi hành.

---
## q047 · don_gian · phien_ban · phiên bản

Trạng thái: GIỮ
Câu hỏi: Tại địa phương, cơ quan nào có trách nhiệm thống nhất quản lý công chức và thực hiện các nội dung quản lý công chức trên địa bàn?

*Đáp án nháp của mô hình:* Ủy ban nhân dân cấp tỉnh có trách nhiệm thống nhất quản lý công chức và thực hiện các nội dung quản lý công chức trên địa bàn tỉnh.

**Cờ tự động:** trùng từ cao (89%)
**Sàng lọc:** không thấy vấn đề

**Gold: 10/2026/VBHN-NĐ-BNV Điều 67**

> Điều 67. Nhiệm vụ, quyền hạn của Ủy ban, Chủ tịch Ủy ban nhân dân tỉnh, thành phố trực thuộc trung ương[37]
> 1. Nhiệm vụ của Ủy ban nhân dân cấp tỉnh:
> a) Thống nhất quản lý công chức trên địa bàn tỉnh; thực hiện quản lý cán bộ trong cơ quan nhà nước trên địa bàn tỉnh theo phân cấp thẩm quyền quản lý;
> b) Thực hiện các nội dung quản lý công chức quy định tại điểm a, điểm b, điểm c, điểm d, điểm e, điểm g, điểm h, điểm i khoản 1 Điều 64 Nghị định này, trừ trường hợp phân cấp theo quy định tại điểm c khoản này và các nội dung thuộc thẩm quyền quản lý của cơ quan sử dụng công chức;
> c) Phân cấp việc thực hiện các nội dung quy định tại khoản d khoản 1 Điều 64 Nghị định này;
> d) Thực hiện các nội dung quản lý cán bộ theo phân cấp quản lý cán bộ của cấp có thẩm quyền.
> 2. Nhiệm vụ của Chủ tịch Ủy ban nhân dân cấp tỉnh:
> a) Thực hiện nhiệm vụ quy định tại điểm a khoản 1 Điều 64 Nghị định này;
> b) Thực hiện nhiệm vụ theo ủy quyền của Ủy ban nhân dân cấp tỉnh; quyết định theo thẩm quyền đối với các nội dung được giao theo Nghị định này;
> c) Tổ chức thực hiện các nội dung quản lý công chức quy định tại điểm b, điểm c, điểm e, điểm g, điểm h, điểm i khoản 1 Điều 64 Nghị định này và ban hành các quyết định tương ứng để thực hiện quản lý đội ngũ;
> d) Tổ chức thực hiện các nội dung quản lý công chức quy định tại điểm d khoản 1 Điều 64 Nghị định này trong trường hợp Ủy ban nhân dân cấp tỉnh không phân cấp, ủy quyền cho cơ quan, tổ chức, cá nhân khác;
> đ) Phân cấp việc thực hiện các nội dung thuộc thẩm quyền; thực hiện các nội dung quản lý cán bộ theo phân cấp quản lý cán bộ của cấp có thẩm quyền.
> Điều 68. Trách nhiệm, thẩm quyền của cơ quan sử dụng công chức[38]
> 1. Tổ chức thực hiện các nhiệm vụ quy định tại điểm đ khoản 1 Điều 64 Nghị định này đối với công chức thuộc phạm vi quản lý theo quy định của Luật Cán bộ, công chức số 80/2025/QH15, quy định tại Nghị định này và phân cấp thẩm quyền quản lý cán bộ.
> 2. Thực hiện nhiệm vụ theo phân cấp, ủy quyền.
> 3. Đề xuất với cơ quan có thẩm quyền các nội dung liên quan đến quản lý công chức quy định tại điểm d khoản 1 Điều 64 Nghị định này theo thẩm quyền.
> 4. Thực hiện quy định tại điểm g, điểm h khoản 1 Điều 64 Nghị định này theo thẩm quyền.
> 5. Giải quyết khiếu nại, tố cáo theo quy định; thực hiện các nội dung quản lý công chức theo phân cấp quản lý cán bộ của cấp có thẩm quyền.

**Bản CŨ (đã bị 300/2026/NĐ-CP sửa): 170/2025/NĐ-CP Điều 67**

> Điều 67. Nhiệm vụ, quyền hạn của Ủy ban, Chủ tịch Ủy ban nhân dân tỉnh, thành phố trực thuộc Trung ương
> 1. Nhiệm vụ của Ủy ban nhân dân cấp tỉnh:
> a) Thực hiện nội dung quản lý công chức quy định tại khoản 1, khoản 3, khoản 4, khoản 7, khoản 9 Điều 64 Nghị định này, trừ trường hợp thực hiện phân cấp, ủy quyền theo quy định tại khoản 2 Điều này hoặc các nội dung thuộc thẩm quyền của cơ quan sử dụng theo quy định của Luật Cán bộ, công chức năm 2025;
> b) Phân cấp, ủy quyền cho Chủ tịch Ủy ban nhân dân cấp tỉnh, cơ quan chuyên môn, tổ chức hành chính khác thuộc Ủy ban nhân dân cấp tỉnh hoặc cơ quan tương đương cấp Sở, Ủy ban nhân dân, Chủ tịch Ủy ban nhân dân cấp xã thực hiện các nội dung quy định tại khoản 4 Điều 64 Nghị định này;
> c) Xây dựng Đề án vị trí việc làm; quyết định danh mục, số lượng vị trí việc làm; quản lý vị trí việc làm theo quy định của Đảng và của pháp luật;
> d) Thực hiện thống kê và báo cáo thống kê công chức theo quy định;
> đ) Hướng dẫn, kiểm tra việc thi hành các quy định của pháp luật đối với công chức thuộc phạm vi quản lý;
> e) Giải quyết khiếu nại, tố cáo theo phân cấp và theo quy định của pháp luật về khiếu nại, tố cáo.
> 2. Nhiệm vụ của Chủ tịch Ủy ban nhân dân cấp tỉnh:
> a) Thực hiện nhiệm vụ quy định tại khoản 1 Điều 64 Nghị định này và theo phân cấp, ủy quyền của Ủy ban nhân dân cấp tỉnh;
> b) Thực hiện hoặc phân cấp việc thực hiện nhiệm vụ quy định tại khoản 5 Điều 64 Nghị định này đối với công chức theo phân cấp thẩm quyền quản lý;
> c) Tổ chức thực hiện các nội dung quản lý công chức quy định tại các khoản 3, khoản 4, khoản 6, khoản 7, khoản 8 Điều 64 Nghị định này và ban hành hoặc phân cấp, ủy quyền việc ban hành các quyết định tương ứng để thực hiện quản lý đội ngũ công chức theo thẩm quyền, trừ những nội dung thuộc thẩm quyền của cơ quan sử dụng công chức theo quy định của Luật Cán bộ, công chức năm 2025.

---
## q048 · don_gian · phien_ban · phiên bản

Trạng thái: GIỮ
Câu hỏi: Người nộp thuế mới thành lập phải làm thế nào để đăng ký thuế lần đầu theo quy định hiện hành?

*Đáp án nháp của mô hình:* Người nộp thuế mới thành lập phải lập và gửi hồ sơ đăng ký thuế lần đầu bằng phương thức điện tử đến cơ quan thuế qua Cổng thông tin điện tử của Tổng cục Thuế.

**Cờ tự động:** trùng từ cao (86%)
**Sàng lọc:** không đúng ý đồ nhóm — Điểm a (lập và gửi hồ sơ bằng phương thức điện tử) giống hệt bản cũ; thay đổi duy nhất là điểm b bỏ yêu cầu mang hồ sơ giấy đến trụ sở cơ quan thuế, nhưng câu hỏi không đụng tới phần này. · Gợi ý câu hỏi: Theo quy định hiện hành, sau khi tiếp nhận hồ sơ đăng ký thuế lần đầu bằng phương thức điện tử, Cổng thông tin điện tử của Tổng cục Thuế gửi thông báo tiếp nhận cho người nộp thuế trong thời hạn nào và thông báo đó nêu những nội dung gì?

**Gold: 21/VBHN-BTC Điều 13 khoản 1**

> 1. Hồ sơ đăng ký thuế lần đầu
> a) Người nộp thuế mới thành lập hoặc bắt đầu phát sinh nghĩa vụ với NSNN thực hiện lập và gửi hồ sơ đăng ký thuế lần đầu theo quy định tại Thông tư số 105/2020/TT-BTC ngày 03/12/2020 của Bộ trưởng Bộ Tài chính hướng dẫn về đăng ký thuế (sau đây gọi là Thông tư số 105/2020/TT-BTC) bằng phương thức điện tử đến cơ quan thuế theo quy định tại điểm a khoản 5 Điều 4 Thông tư này.
> b) Cổng thông tin điện tử của Tổng cục Thuế tiếp nhận, đối chiếu thông tin và gửi Thông báo tiếp nhận hồ sơ đăng ký thuế điện tử (theo mẫu số 01-1/TB-TĐT ban hành kèm theo Thông tư này) cho người nộp thuế chậm nhất 15 phút kể từ khi nhận được hồ sơ đăng ký thuế của người nộp thuế vào địa chỉ thư điện tử hoặc số điện thoại người nộp thuế đã đăng ký với cơ quan thuế, thông báo nêu rõ thời gian, địa điểm trả kết quả.
> c) Trường hợp hồ sơ đăng ký thuế đủ điều kiện cấp mã số thuế theo quy định, cơ quan thuế giải quyết theo quy định tại Thông tư số 105/2020/TT-BTC.
> d) Trường hợp hồ sơ đăng ký thuế không đủ điều kiện cấp mã số thuế theo quy định, trong thời hạn 02 (hai) ngày làm việc kể từ ngày tiếp nhận hồ sơ ghi trên Thông báo tiếp nhận hồ sơ đăng ký thuế điện tử, cơ quan thuế gửi Thông báo không chấp nhận hồ sơ đăng ký thuế (theo mẫu số 01-2/TB-TĐT ban hành kèm theo Thông tư này) cho người nộp thuế qua Cổng thông tin điện tử của Tổng cục Thuế.
> Người nộp thuế có trách nhiệm gửi hồ sơ đăng ký thuế điện tử khác qua Cổng thông tin điện tử của Tổng cục Thuế để thay thế cho hồ sơ có sai sót đã gửi đến cơ quan thuế.

**Bản CŨ (đã bị 46/2024/TT-BTC sửa): 19/2021/TT-BTC Điều 13 khoản 1**

> 1. Hồ sơ đăng ký thuế lần đầu
> a) Người nộp thuế mới thành lập hoặc bắt đầu phát sinh nghĩa vụ với NSNN thực hiện lập và gửi hồ sơ đăng ký thuế lần đầu theo quy định tại Thông tư số 105/2020/TT-BTC ngày 03/12/2020 của Bộ trưởng Bộ Tài chính hướng dẫn về đăng ký thuế (sau đây gọi là Thông tư số 105/2020/TT-BTC) bằng phương thức điện tử đến cơ quan thuế theo quy định tại điểm a khoản 5 Điều 4 Thông tư này.
> b) Cổng thông tin điện tử của Tổng cục Thuế tiếp nhận, đối chiếu thông tin và gửi Thông báo tiếp nhận hồ sơ đăng ký thuế điện tử (theo mẫu số 01-1/TB-TĐT ban hành kèm theo Thông tư này) cho người nộp thuế chậm nhất 15 phút kể từ khi nhận được hồ sơ đăng ký thuế của người nộp thuế vào địa chỉ thư điện tử hoặc số điện thoại người nộp thuế đã đăng ký với cơ quan thuế, thông báo nêu rõ thời gian, địa điểm trả kết quả, đồng thời yêu cầu người nộp thuế mang hồ sơ giấy đến trụ sở cơ quan thuế.
> c) Trường hợp hồ sơ đăng ký thuế đủ điều kiện cấp mã số thuế theo quy định, cơ quan thuế giải quyết theo quy định tại Thông tư số 105/2020/TT-BTC.
> d) Trường hợp hồ sơ đăng ký thuế không đủ điều kiện cấp mã số thuế theo quy định, trong thời hạn 02 (hai) ngày làm việc kể từ ngày tiếp nhận hồ sơ ghi trên Thông báo tiếp nhận hồ sơ đăng ký thuế điện tử, cơ quan thuế gửi Thông báo không chấp nhận hồ sơ đăng ký thuế (theo mẫu số 01-2/TB-TĐT ban hành kèm theo Thông tư này) cho người nộp thuế qua Cổng thông tin điện tử của Tổng cục Thuế.
> Người nộp thuế có trách nhiệm gửi hồ sơ đăng ký thuế điện tử khác qua Cổng thông tin điện tử của Tổng cục Thuế để thay thế cho hồ sơ có sai sót đã gửi đến cơ quan thuế.

---
## q049 · don_gian · phien_ban · phiên bản

Trạng thái: GIỮ
Câu hỏi: Người trúng tuyển công chức phải đến nhận việc trong bao lâu kể từ ngày nhận được quyết định tuyển dụng?

*Đáp án nháp của mô hình:* Trong thời hạn 15 ngày kể từ ngày nhận được quyết định tuyển dụng, trừ trường hợp quyết định có quy định thời hạn khác hoặc được gia hạn.

**Cờ tự động:** trùng từ cao (90%)
**Sàng lọc:** không thấy vấn đề

**Gold: 10/2026/VBHN-NĐ-BNV Điều 19**

> Điều 19. Quyết định tuyển dụng và nhận việc[8]
> 1. Chậm nhất là 03 ngày làm việc kể từ ngày hết thời hạn hoàn thiện hồ sơ tuyển dụng theo quy định tại khoản 1 Điều 18 Nghị định này, người đứng đầu cơ quan có thẩm quyền tuyển dụng ra quyết định tuyển dụng và gửi tới người trúng tuyển. Nội dung quyết định tuyển dụng bao gồm việc tuyển dụng, bố trí vị trí việc làm và xếp ngạch tương ứng với vị trí việc làm tuyển dụng.
> 2. Chậm nhất là 15 ngày kể từ ngày nhận được quyết định tuyển dụng, người được tuyển dụng phải đến nhận việc, trừ trường hợp quyết định tuyển dụng quy định thời hạn khác hoặc được cơ quan có thẩm quyền tuyển dụng đồng ý gia hạn.
> 3. Trường hợp người được tuyển dụng không đến nhận việc trong thời hạn quy định tại khoản 2 Điều này thì quyết định tuyển dụng đương nhiên hết hiệu lực, trừ trường hợp được sự chấp thuận của người đứng đầu cơ quan có thẩm quyền tuyển dụng. Cơ quan sử dụng công chức báo cáo cơ quan có thẩm quyền tuyển dụng thực hiện các công việc quy định tại khoản 3, khoản 4 Điều 18 Nghị định này.

**Bản CŨ (đã bị 300/2026/NĐ-CP sửa): 170/2025/NĐ-CP Điều 19**

> Điều 19. Quyết định tuyển dụng và nhận việc
> 1. Chậm nhất là 05 ngày làm việc kể từ ngày hết thời hạn hoàn thiện hồ sơ tuyển dụng theo quy định tại khoản 1 Điều 18 Nghị định này, người đứng đầu cơ quan có thẩm quyền tuyển dụng ra quyết định tuyển dụng, gửi thông báo tới người trúng tuyển. Nội dung quyết định tuyển dụng bao gồm việc tuyển dụng, bố trí vị trí việc làm và xếp ngạch tương ứng với vị trí việc làm tuyển dụng. Cơ quan có thẩm quyền tuyển dụng có trách nhiệm yêu cầu cơ quan có thẩm quyền theo quy định của pháp luật về lý lịch tư pháp cấp Phiếu lý lịch tư pháp của người trúng tuyển.
> 2. Chậm nhất là 30 ngày kể từ ngày có quyết định tuyển dụng, người được tuyển dụng phải đến nhận việc, trừ trường hợp quyết định tuyển dụng quy định thời hạn khác hoặc được cơ quan có thẩm quyền tuyển dụng đồng ý gia hạn.
> 3. Trường hợp người được tuyển dụng không đến nhận việc trong thời hạn quy định tại khoản 2 Điều này hoặc Phiếu lý lịch tư pháp xác định thuộc một trong các trường hợp không được đăng ký dự tuyển công chức thì người đứng đầu cơ quan có thẩm quyền tuyển dụng hủy bỏ quyết định tuyển dụng.
> 4. Hết thời hạn quy định tại khoản 2 Điều này, cơ quan có thẩm quyền tuyển dụng thông báo công khai trên trang thông tin điện tử hoặc cổng thông tin điện tử của cơ quan và gửi thông báo tới những người dự tuyển có kết quả tuyển dụng thấp hơn liền kề (theo thứ tự) so với kết quả tuyển dụng của người trúng tuyển mà kết quả tuyển dụng bị hủy bỏ theo quy định tại khoản 2 Điều 18 Nghị định này hoặc quyết định tuyển dụng bị hủy bỏ theo quy định tại khoản 3 Điều này để hoàn thiện hồ sơ, ra quyết định tuyển dụng chậm nhất là 15 ngày kể từ ngày hết thời hạn quy định tại khoản 2 Điều này.
> Trường hợp có từ 02 người trở lên có kết quả tuyển dụng thấp hơn liền kề bằng nhau thì người đứng đầu cơ quan có thẩm quyền tuyển dụng quyết định người trúng tuyển theo quy định tại khoản 2 Điều 10 Nghị định này (trong trường hợp tổ chức thi tuyển) hoặc quy định tại khoản 2 Điều 12 Nghị định này (trong trường hợp tổ chức xét tuyển).

---
## q050 · don_gian · phien_ban · phiên bản

Trạng thái: GIỮ
Câu hỏi: Khi tiếp nhận công chức vào làm việc để bổ nhiệm giữ chức vụ lãnh đạo, quản lý thì cần làm thế nào theo quy định hiện hành?

*Đáp án nháp của mô hình:* Thực hiện theo quy trình bổ nhiệm đối với nguồn nhân sự từ nơi khác. Quyết định bổ nhiệm đồng thời là quyết định tiếp nhận vào làm công chức. Nếu cơ quan bổ nhiệm là cấp dưới thì phải báo cáo và được cơ quan có thẩm quyền tuyển dụng đồng ý trước khi ban hành quyết định bổ nhiệm.

**Cờ tự động:** trùng từ cao (86%)
**Sàng lọc:** không đúng ý đồ nhóm — Nội dung được hỏi (khoản 3) về thực chất tương đương khoản 5 bản cũ (theo quy trình nguồn nhân sự từ nơi khác, quyết định bổ nhiệm đồng thời là quyết định tiếp nhận, cấp dưới phải báo cáo xin đồng ý); thay đổi thực sự là bỏ Hội đồng kiểm tra, sát hạch ở khoản 1. Câu hỏi còn chép gần nguyên văn vế đầu khoản 3. · Gợi ý câu hỏi: Theo quy định hiện hành, ai có trách nhiệm nghiên cứu, đề xuất việc tiếp nhận người đủ tiêu chuẩn, điều kiện vào làm công chức?

**Gold: 10/2026/VBHN-NĐ-BNV Điều 14**

> Điều 14. Thủ tục tiếp nhận vào làm công chức[6]
> 1. Căn cứ nhu cầu sử dụng nhân lực đáp ứng được ngay yêu cầu công việc của cơ quan, tổ chức, đơn vị, người phụ trách công tác tổ chức cán bộ của cơ quan có thẩm quyền tuyển dụng nghiên cứu, đề xuất tiếp nhận đối với người đáp ứng đủ tiêu chuẩn, điều kiện theo quy định tại Điều 13 Nghị định này.
> 2. Người đứng đầu cơ quan có thẩm quyền tuyển dụng quyết định tiếp nhận công chức theo thẩm quyền.
> 3. Khi tiếp nhận vào làm công chức để bổ nhiệm giữ chức vụ lãnh đạo, quản lý thì thực hiện theo quy trình bổ nhiệm đối với nguồn nhân sự từ nơi khác. Quyết định bổ nhiệm đồng thời là quyết định tiếp nhận vào làm công chức.
> Trường hợp cơ quan có thẩm quyền bổ nhiệm là cấp dưới của cơ quan có thẩm quyền tuyển dụng thì cơ quan có thẩm quyền bổ nhiệm phải báo cáo và được cơ quan có thẩm quyền tuyển dụng đồng ý về việc tiếp nhận trước khi ban hành quyết định bổ nhiệm.

**Bản CŨ (đã bị 300/2026/NĐ-CP sửa): 170/2025/NĐ-CP Điều 14**

> Điều 14. Thủ tục tiếp nhận
> 1. Hội đồng kiểm tra, sát hạch:
> a) Người đứng đầu cơ quan có thẩm quyền tuyển dụng thành lập Hội đồng kiểm tra, sát hạch. Thành phần Hội đồng kiểm tra, sát hạch được thực hiện theo quy định tại khoản 1 Điều 8 Nghị định này;
> b) Nhiệm vụ, quyền hạn của Hội đồng kiểm tra, sát hạch:
> Kiểm tra về tiêu chuẩn, điều kiện, văn bằng, chứng chỉ, chứng nhận của người được đề nghị tiếp nhận theo yêu cầu của vị trí việc làm cần tuyển;
> Tổ chức sát hạch về trình độ hiểu biết chung và năng lực chuyên môn, nghiệp vụ của người được đề nghị tiếp nhận; nội dung sát hạch phải căn cứ vào yêu cầu của vị trí việc làm cần tuyển; hình thức sát hạch là vấn đáp;
> Báo cáo người đứng đầu cơ quan có thẩm quyền tuyển dụng về kết quả kiểm tra, sát hạch;
> c) Hội đồng kiểm tra, sát hạch làm việc theo nguyên tắc tập thể, quyết định theo đa số; trường hợp biểu quyết ngang nhau thì thực hiện theo ý kiến mà Chủ tịch Hội đồng kiểm tra, sát hạch đã biểu quyết. Hội đồng kiểm tra, sát hạch quyết định thành lập Tổ thư ký giúp việc trong trường hợp cần thiết.
> Hội đồng kiểm tra, sát hạch tự giải thể sau khi hoàn thành nhiệm vụ.
> 2. Không thành lập Hội đồng kiểm tra, sát hạch đối với các trường hợp sau:
> a) Tiếp nhận các trường hợp quy định tại điểm b, c và điểm đ khoản 1 Điều 13 vào công chức không giữ chức vụ lãnh đạo, quản lý;
> b) Tiếp nhận các trường hợp quy định tại khoản 1 Điều 13 Nghị định này vào làm công chức giữ chức vụ lãnh đạo, quản lý.
> 3. Không bố trí những người có quan hệ vợ, chồng, cha đẻ, mẹ đẻ; cha, mẹ (vợ hoặc chồng), cha nuôi, mẹ nuôi; con đẻ, con nuôi; anh, chị, em ruột; cô, dì, chú, bác, cậu ruột; anh, chị, em ruột của vợ hoặc chồng; vợ hoặc chồng của anh, chị, em ruột của người tham dự kiểm tra, sát hạch; những người đang trong thời hạn xử lý kỷ luật hoặc đang thi hành quyết định kỷ luật; những người đã bị xử lý về hành vi tham nhũng, tiêu cực làm thành viên Hội đồng kiểm tra, sát hạch.
> 4. Người đứng đầu cơ quan có thẩm quyền tuyển dụng quyết định tiếp nhận công chức theo thẩm quyền.
> 5. Khi tiếp nhận vào làm công chức để bổ nhiệm giữ chức vụ, chức danh lãnh đạo, quản lý thì thực hiện theo quy trình bổ nhiệm đối với nguồn nhân sự từ nơi khác. Quyết định bổ nhiệm đồng thời là quyết định tiếp nhận vào làm công chức và thực hiện như sau:
> a) Trường hợp cơ quan có thẩm quyền tuyển dụng đồng thời là cơ quan có thẩm quyền bổ nhiệm hoặc là cấp dưới của cơ quan có thẩm quyền bổ nhiệm thì quyết định bổ nhiệm đồng thời là quyết định tiếp nhận;
> b) Trường hợp cơ quan có thẩm quyền tuyển dụng là cấp trên của cơ quan có thẩm quyền bổ nhiệm thì cơ quan có thẩm quyền bổ nhiệm phải báo cáo và được cơ quan có thẩm quyền tuyển dụng đồng ý về việc tiếp nhận trước khi quyết định bổ nhiệm.

---
## q051 · don_gian · phien_ban · phiên bản

Trạng thái: GIỮ
Câu hỏi: Các bộ, cơ quan ngang bộ có trách nhiệm quản lý công chức như thế nào trong thực tế hiện nay?

*Đáp án nháp của mô hình:* Các bộ, cơ quan ngang bộ thực hiện quản lý công chức theo quy định, trừ những nội dung đã được phân cấp hoặc thuộc thẩm quyền của cơ quan sử dụng công chức, và thực hiện các nhiệm vụ quản lý cán bộ theo phân cấp của cấp có thẩm quyền.

**Sàng lọc:** câu hỏi mơ hồ — Câu hỏi quá rộng ('như thế nào trong thực tế' không bám văn bản); gold chủ yếu dẫn chiếu sang khoản 1 Điều 64 nên đáp án chung chung. · Gợi ý câu hỏi: Theo quy định hiện hành, ngoài việc quản lý công chức, bộ, cơ quan ngang bộ còn thực hiện nhiệm vụ gì đối với cán bộ?

**Gold: 10/2026/VBHN-NĐ-BNV Điều 66**

> Điều 66. Nhiệm vụ và quyền hạn của bộ, cơ quan ngang bộ, cơ quan quản lý công chức khác[36]
> 1. Thực hiện nội dung quản lý công chức quy định tại khoản 1 Điều 64 Nghị định này, trừ trường hợp phân cấp theo quy định tại khoản 2 Điều này và các nội dung thuộc thẩm quyền của cơ quan sử dụng công chức theo quy định của Luật Cán bộ, công chức số 80/2025/QH15 và quy định tại Nghị định này.
> 2. Phân cấp việc thực hiện các nội dung quy định tại điểm d, điểm đ, điểm e khoản 1 Điều 64 Nghị định này, trừ những nội dung thuộc thẩm quyền của cơ quan sử dụng công chức theo quy định của Luật Cán bộ, công chức số 80/2025/QH15 và quy định tại Nghị định này.
> 3. Thực hiện các nội dung quản lý cán bộ theo phân cấp quản lý cán bộ của cấp có thẩm quyền.

**Bản CŨ (đã bị 300/2026/NĐ-CP sửa): 170/2025/NĐ-CP Điều 66**

> Điều 66. Nhiệm vụ và quyền hạn của Bộ, cơ quan ngang Bộ, cơ quan quản lý công chức khác
> 1. Thực hiện nội dung quản lý công chức quy định tại khoản 3, khoản 4, khoản 5, khoản 7, khoản 9 Điều 64 Nghị định này, trừ trường hợp phân cấp, ủy quyền theo quy định tại khoản 2 Điều này và nội dung thuộc thẩm quyền của cơ quan sử dụng công chức theo quy định của Luật Cán bộ, công chức năm 2025.
> 2. Phân cấp, ủy quyền cho cơ quan sử dụng công chức thuộc phạm vi quản lý thực hiện các nội dung quy định tại khoản 4, khoản 5 Điều 64 Nghị định này, trừ những nội dung thuộc thẩm quyền của cơ quan sử dụng công chức theo quy định của Luật Cán bộ, công chức năm 2025.
> 3. Xây dựng, quản lý vị trí việc làm; quyết định danh mục, số lượng vị trí việc làm; quản lý vị trí việc làm theo quy định của Đảng và của pháp luật.
> 4. Quản lý chương trình bồi dưỡng theo yêu cầu của vị trí việc làm thuộc thẩm quyền quản lý.
> 5. Thực hiện thống kê và báo cáo thống kê công chức theo quy định.
> 6. Hướng dẫn, kiểm tra việc thi hành các quy định của pháp luật đối với công chức thuộc phạm vi quản lý.
> 7. Giải quyết khiếu nại, tố cáo theo phân cấp và theo quy định của pháp luật về khiếu nại, tố cáo.

---
## q052 · don_gian · phien_ban · phiên bản

Trạng thái: GIỮ
Câu hỏi: Khi tuyển dụng vào làm công chức, người được tuyển dụng sẽ được hưởng mức lương như thế nào?

*Đáp án nháp của mô hình:* Người được tuyển dụng sẽ được hưởng mức lương khởi điểm của ngạch công chức tương ứng với vị trí việc làm.

**Sàng lọc:** không thấy vấn đề — Đáp án nháp thiếu ngoại lệ: người đã có thời gian công tác có đóng BHXH bắt buộc thì được xem xét xếp vào bậc lương phù hợp, và người được tiếp nhận thì được tính thời gian công tác để xếp lương.

**Gold: 10/2026/VBHN-NĐ-BNV Điều 20**

> Điều 20. Xếp lương đối với người được tuyển dụng, tiếp nhận vào làm công chức[9]
> 1. Người được tuyển dụng, tiếp nhận vào vị trí việc làm xếp ngạch công chức nào thì được xếp hưởng mức lương khởi điểm của ngạch đó, trừ trường hợp quy định tại khoản 2, khoản 3 Điều này.
> 2. Trường hợp người được tuyển dụng vào làm công chức đã có thời gian công tác theo đúng quy định của pháp luật phù hợp với yêu cầu về trình độ chuyên môn, nghiệp vụ của vị trí việc làm được tuyển dụng, có đóng bảo hiểm xã hội bắt buộc (nếu không liên tục mà chưa nhận trợ cấp bảo hiểm xã hội một lần hoặc chưa hưởng chế độ phục viên, xuất ngũ thì được cộng dồn), được bố trí làm công việc theo đúng chuyên môn, nghiệp vụ trước đây đã đảm nhiệm thì người đứng đầu cơ quan có thẩm quyền tuyển dụng căn cứ thời gian công tác đó để xem xét, quyết định xếp vào bậc lương phù hợp ở ngạch công chức tương ứng theo vị trí việc làm được tuyển dụng.
> 3. Trường hợp người được tiếp nhận vào làm công chức có thời gian công tác theo đúng quy định của pháp luật, có đóng bảo hiểm xã hội bắt buộc (nếu không liên tục mà chưa nhận trợ cấp bảo hiểm xã hội một lần hoặc chưa hưởng chế độ phục viên, xuất ngũ thì được cộng dồn), làm công việc phù hợp với yêu cầu về trình độ chuyên môn, nghiệp vụ của vị trí việc làm được tiếp nhận thì thời gian công tác đó được tính làm căn cứ xếp lương ở ngạch công chức tương ứng theo vị trí việc làm được tiếp nhận.
> 4. Bộ Nội vụ hướng dẫn việc xếp lương đối với các trường hợp quy định tại Điều này.

**Bản CŨ (đã bị 300/2026/NĐ-CP sửa): 170/2025/NĐ-CP Điều 20**

> Điều 20. Xếp lương đối với người được tuyển dụng vào công chức đã có thời gian công tác có đóng bảo hiểm xã hội bắt buộc
> Trường hợp người được tuyển dụng vào công chức theo quy định tại Nghị định này đã có thời gian công tác theo đúng quy định của pháp luật phù hợp với yêu cầu về trình độ chuyên môn nghiệp vụ của vị trí việc làm được tuyển dụng, có đóng bảo hiểm xã hội bắt buộc (nếu không liên tục mà chưa nhận trợ cấp bảo hiểm xã hội một lần thì được cộng dồn), được bố trí làm công việc theo đúng chuyên môn, nghiệp vụ trước đây đã đảm nhiệm thì thời gian công tác đó được tính làm căn cứ để xếp lương ở ngạch công chức tương ứng theo vị trí việc làm được tuyển dụng.
> Bộ Nội vụ hướng dẫn chi tiết Điều này.

---
## q053 · don_gian · phien_ban · phiên bản

Trạng thái: GIỮ
Câu hỏi: Khi xem xét bổ nhiệm lại cho một công chức đang giữ chức vụ lãnh đạo, quản lý, cần những điều kiện nào cụ thể?

*Đáp án nháp của mô hình:* Công chức phải hoàn thành nhiệm vụ trong thời hạn giữ chức vụ, có kết quả thực hiện nhiệm vụ được đánh giá qua sản phẩm cụ thể; đáp ứng tiêu chuẩn chức danh lãnh đạo, quản lý tại thời điểm bổ nhiệm; cơ quan có nhu cầu về vị trí đó; đủ sức khỏe để thực hiện nhiệm vụ; và không thuộc các trường hợp bị xử lý kỷ luật, bị xem xét miễn nhiệm, từ chức hoặc không đáp ứng các tiêu chuẩn khác theo quy định.

**Sàng lọc:** không thấy vấn đề — Khoản 1–4 giống bản cũ. Đáp án nháp diễn giải sai khoản 5 (vốn dẫn chiếu điểm a, đ khoản 9 Điều 29 và khoản 3 Điều 36) và bỏ đoạn mới bổ sung ở khoản 1 về năm không hoàn thành nhiệm vụ do bất khả kháng hoặc do bị kỷ luật. · Gợi ý câu hỏi: Nếu trong thời hạn giữ chức vụ có năm công chức lãnh đạo, quản lý bị xếp loại không hoàn thành nhiệm vụ vì lý do bất khả kháng hoặc do bị kỷ luật thì tiêu chí hoàn thành nhiệm vụ để bổ nhiệm lại được xem xét như thế nào?

**Gold: 10/2026/VBHN-NĐ-BNV Điều 37**

> Điều 37. Tiêu chuẩn, điều kiện bổ nhiệm lại[21]
> 1. Hoàn thành nhiệm vụ trong thời hạn giữ chức vụ lãnh đạo, quản lý.
> Trường hợp trong thời hạn giữ chức vụ có năm xếp loại chất lượng không hoàn thành nhiệm vụ vì lý do bất khả kháng hoặc do bị xử lý kỷ luật mà không thuộc đối tượng bị xem xét miễn nhiệm, từ chức, cho thôi giữ chức vụ thì cấp có thẩm quyền bổ nhiệm thảo luận trong tập thể lãnh đạo, cấp ủy để xem xét, đánh giá toàn diện về năng lực, phẩm chất, uy tín, kết quả thực hiện nhiệm vụ được giao thể hiện bằng sản phẩm cụ thể đối với các năm còn lại và trong cả thời hạn giữ chức vụ để xem xét, quyết định việc đánh giá về tiêu chí hoàn thành nhiệm vụ trong thời hạn giữ chức vụ.
> 2. Đáp ứng tiêu chuẩn chức danh lãnh đạo, quản lý theo quy định của cơ quan có thẩm quyền tại thời điểm bổ nhiệm lại.
> 3. Cơ quan, tổ chức có nhu cầu về vị trí việc làm lãnh đạo, quản lý.
> 4. Đủ sức khỏe để hoàn thành nhiệm vụ và chức trách được giao.
> 5. Không thuộc một trong các trường hợp quy định tại điểm a, điểm đ khoản 9 Điều 29 Nghị định này; không thuộc một trong các trường hợp chưa xem xét bổ nhiệm lại quy định tại khoản 3 Điều 36 Nghị định này hoặc các trường hợp khác không đáp ứng tiêu chuẩn, điều kiện bổ nhiệm lại theo quy định của cấp có thẩm quyền.
> Trường hợp cơ quan, tổ chức, đơn vị đang trong thời gian thanh tra, kiểm tra thì cấp có thẩm quyền trao đổi với cơ quan thanh tra, kiểm tra về nhân sự được đề nghị bổ nhiệm lại trước khi quyết định.

**Bản CŨ (đã bị 300/2026/NĐ-CP sửa): 170/2025/NĐ-CP Điều 37**

> Điều 37. Tiêu chuẩn, điều kiện bổ nhiệm lại
> 1. Hoàn thành nhiệm vụ trong thời hạn giữ chức vụ lãnh đạo, quản lý.
> 2. Đáp ứng tiêu chuẩn chức danh lãnh đạo, quản lý theo quy định của cơ quan có thẩm quyền tại thời điểm bổ nhiệm lại.
> 3. Cơ quan, tổ chức có nhu cầu về vị trí việc làm lãnh đạo, quản lý.
> 4. Đủ sức khỏe để hoàn thành nhiệm vụ và chức trách được giao.
> 5. Không thuộc các trường hợp bị cấm đảm nhiệm chức vụ theo quy định của pháp luật.

---
## q054 · don_gian · phien_ban · phiên bản

Trạng thái: GIỮ
Câu hỏi: Khi xem xét bổ nhiệm lại hoặc kéo dài thời gian giữ chức vụ lãnh đạo, quản lý đến tuổi nghỉ hưu, người đứng đầu cơ quan cần làm những bước gì?

*Đáp án nháp của mô hình:* Cần có bản tự kiểm điểm và đánh giá, nhận xét của tập thể lãnh đạo cơ quan trong suốt thời gian giữ chức vụ.

**Sàng lọc:** chỉ trả lời được một phần từ gold; câu hỏi mơ hồ — Câu hỏi hỏi 'các bước' người đứng đầu phải làm, trong khi gold quy định về hồ sơ (lập theo Điều 35; bản tự kiểm điểm và nhận xét của tập thể lãnh đạo tính trong cả thời hạn giữ chức vụ), nên dễ trùng với Điều về thủ tục. · Gợi ý câu hỏi: Theo quy định hiện hành, trong hồ sơ đề nghị bổ nhiệm lại hoặc kéo dài thời gian giữ chức vụ lãnh đạo, quản lý đến tuổi nghỉ hưu, bản tự kiểm điểm và đánh giá, nhận xét của tập thể lãnh đạo phải bao quát khoảng thời gian nào?

**Gold: 10/2026/VBHN-NĐ-BNV Điều 41**

> Điều 41. Hồ sơ bổ nhiệm lại, kéo dài thời gian giữ chức vụ lãnh đạo, quản lý đến tuổi nghỉ hưu[24]
> Hồ sơ đề nghị bổ nhiệm lại, kéo dài thời gian giữ chức vụ thực hiện theo quy định tại Điều 35 Nghị định này; đối với bản tự kiểm điểm và đánh giá, nhận xét của tập thể lãnh đạo cơ quan, tổ chức, đơn vị thực hiện trong cả thời hạn giữ chức vụ.

**Bản CŨ (đã bị 300/2026/NĐ-CP sửa): 170/2025/NĐ-CP Điều 41**

> Điều 41. Hồ sơ bổ nhiệm lại, kéo dài thời gian giữ chức vụ lãnh đạo, quản lý đến tuổi nghỉ hưu
> 1. Hồ sơ đề nghị bổ nhiệm lại thực hiện theo quy định tại Điều 35 Nghị định này; đối với bản tự kiểm điểm thực hiện trong cả thời hạn giữ chức vụ. Đối với kết luận về tiêu chuẩn chính trị, trường hợp bổ nhiệm lại nhưng có tình tiết mới làm thay đổi kết luận trước đây thì phải có Kết luận của cấp ủy có thẩm quyền về tiêu chuẩn chính trị.
> 2. Hồ sơ đề nghị kéo dài thời gian giữ chức vụ lãnh đạo, quản lý đến tuổi nghỉ hưu, bao gồm:
> a) Tờ trình về việc đề nghị kéo dài thời gian giữ chức vụ lãnh đạo, quản lý đến tuổi nghỉ hưu do người đứng đầu cơ quan, tổ chức ký (đối với trường hợp trình cấp trên có thẩm quyền quyết định) hoặc do người đứng đầu cơ quan tham mưu về tổ chức cán bộ ký (đối với trường hợp người đứng đầu cơ quan có thẩm quyền quyết định);
> b) Biên bản họp và kết quả kiểm phiếu đề nghị kéo dài thời gian giữ chức vụ lãnh đạo, quản lý của tập thể lãnh đạo cơ quan, tổ chức;
> c) Sơ yếu lý lịch do cá nhân tự khai theo mẫu quy định, được cơ quan trực tiếp quản lý xác nhận, có dán ảnh màu khổ 4x6, chụp trong thời gian không quá 06 tháng;
> d) Bản tự nhận xét đánh giá việc thực hiện chức trách, nhiệm vụ trong thời hạn giữ chức vụ;
> đ) Đối với kết luận tiêu chuẩn chính trị: Trường hợp kéo dài thời gian giữ chức vụ lãnh đạo, quản lý nhưng có tình tiết mới làm thay đổi kết luận trước đây thì phải có Kết luận của cấp ủy có thẩm quyền về tiêu chuẩn chính trị;
> e) Nhận xét của chi ủy nơi cư trú đối với bản thân và gia đình. Trường hợp nơi cư trú của bản thân khác với nơi cư trú của gia đình thì phải lấy nhận xét của chi ủy nơi bản thân cư trú và nơi gia đình cư trú;
> g) Bản kê khai tài sản, thu nhập theo mẫu quy định;
> h) Giấy chứng nhận sức khỏe của cơ sở y tế có thẩm quyền cấp trong thời hạn 06 tháng.
> Trường hợp các thành phần trong hồ sơ đề nghị kéo dài thời gian giữ chức vụ lãnh đạo, quản lý đến tuổi nghỉ hưu quy định tại khoản 2 Điều này đã được cấp có thẩm quyền phê duyệt và tồn tại trong cơ sở dữ liệu quốc gia thì được sử dụng để thay thế bản giấy tương ứng.

---
## q055 · don_gian · phien_ban · phiên bản

Trạng thái: DỰ PHÒNG
Câu hỏi: Khi muốn kéo dài thời gian giữ chức vụ lãnh đạo, quản lý đến tuổi nghỉ hưu, công chức cần làm những bước gì?

*Đáp án nháp của mô hình:* Công chức phải làm báo cáo tự nhận xét, đánh giá việc thực hiện nhiệm vụ và gửi cho cấp có thẩm quyền trong thời hạn 15 ngày. Sau đó, tập thể lãnh đạo sẽ thảo luận, biểu quyết bằng phiếu kín, với yêu cầu ít nhất 50% thành viên đồng ý; nếu đạt 50% thì người đứng đầu quyết định, đồng thời báo cáo các ý kiến khác. Cấp có thẩm quyền sẽ xem xét và quyết định cuối cùng.

**Sàng lọc:** không thấy vấn đề — Thủ tục chủ yếu do cấp có thẩm quyền thực hiện, công chức chỉ phải làm báo cáo trong 15 ngày, nên câu hỏi lệch chủ thể. Đáp án nháp sai 'ít nhất 50%' (gold ghi trên 50%), bỏ thời hạn 45 ngày và bước lấy ý kiến bằng văn bản (đều là phần mới). Cuối gold có dấu ngoặc kép thừa. · Gợi ý câu hỏi: Theo quy định hiện hành, thủ tục kéo dài thời gian giữ chức vụ lãnh đạo, quản lý đến tuổi nghỉ hưu đối với công chức gồm những bước nào và thời hạn của từng bước ra sao?

**Gold: 10/2026/VBHN-NĐ-BNV Điều 40**

> Điều 40. Thủ tục kéo dài thời gian giữ chức vụ lãnh đạo, quản lý đến tuổi nghỉ hưu[23]
> 1. Công chức làm báo cáo tự nhận xét, đánh giá việc thực hiện chức trách, nhiệm vụ trong thời gian giữ chức vụ, gửi cấp có thẩm quyền kéo dài thời gian giữ chức vụ lãnh đạo, quản lý trong thời hạn 15 ngày kể từ ngày nhận được thông báo của cấp có thẩm quyền.
> 2. Chậm nhất 45 ngày kể từ ngày nhận được báo cáo tự nhận xét, đánh giá của công chức, cấp có thẩm quyền tiến hành các thủ tục sau đây:
> a) Tập thể lãnh đạo cơ quan, tổ chức, đơn vị thảo luận, xem xét, nếu công chức còn sức khỏe, uy tín, đáp ứng được yêu cầu nhiệm vụ thì thống nhất biểu quyết bằng phiếu kín.
> Nhân sự được đề nghị kéo dài thời gian giữ chức vụ lãnh đạo, quản lý phải đạt tỷ lệ trên 50% tổng số thành viên tập thể lãnh đạo đồng ý; trường hợp nhân sự đạt tỷ lệ 50% thì do người đứng đầu quyết định; đồng thời báo cáo đầy đủ các ý kiến khác nhau để cấp có thẩm quyền xem xét, quyết định.
> b) Lấy ý kiến bằng văn bản của cấp có thẩm quyền.
> c) Căn cứ kết quả bỏ phiếu và kết quả lấy ý kiến (nếu có), người đứng đầu cơ quan, tổ chức, đơn vị ra quyết định kéo dài thời gian giữ chức vụ lãnh đạo, quản lý đến tuổi nghỉ hưu đối với công chức theo thẩm quyền hoặc trình cơ quan có thẩm quyền xem xét, quyết định.".

**Bản CŨ (đã bị 300/2026/NĐ-CP sửa): 170/2025/NĐ-CP Điều 40**

> Điều 40. Thủ tục kéo dài thời gian giữ chức vụ lãnh đạo, quản lý đến tuổi nghỉ hưu
> 1. Chậm nhất 90 ngày trước ngày hết thời hạn bổ nhiệm, cấp có thẩm quyền kéo dài thời gian giữ chức vụ lãnh đạo, quản lý phải ra thông báo thực hiện việc xem xét kéo dài thời gian giữ chức vụ lãnh đạo, quản lý đến tuổi nghỉ hưu đối với công chức.
> 2. Công chức làm báo cáo tự nhận xét, đánh giá việc thực hiện chức trách, nhiệm vụ trong thời gian giữ chức vụ, gửi cấp có thẩm quyền kéo dài thời gian giữ chức vụ lãnh đạo, quản lý.
> 3. Người đứng đầu và tập thể lãnh đạo cơ quan, tổ chức thảo luận, xem xét, nếu công chức còn sức khỏe, uy tín, đáp ứng được yêu cầu nhiệm vụ thì thống nhất biểu quyết bằng phiếu kín.
> Nhân sự được đề nghị kéo dài thời gian giữ chức vụ lãnh đạo, quản lý phải đạt tỷ lệ trên 50% tổng số thành viên tập thể lãnh đạo đồng ý; trường hợp nhân sự đạt tỷ lệ 50% thì do người đứng đầu quyết định; đồng thời báo cáo đầy đủ các ý kiến khác nhau để cấp có thẩm quyền xem xét, quyết định.
> Người đứng đầu cơ quan, tổ chức ra quyết định theo thẩm quyền hoặc trình cơ quan có thẩm quyền xem xét, quyết định việc kéo dài thời gian giữ chức vụ lãnh đạo, quản lý đến tuổi nghỉ hưu đối với công chức.

---
## q257 · don_gian · trung_lap · TRUNG LẬP

Trạng thái: GIỮ
Câu hỏi: Có quy định về việc bổ sung xe ô tô cho các tỉnh, thành phố tùy theo diện tích tự nhiên được giao quản lý không?

*Đáp án nháp của mô hình:* Có, số lượng xe bổ sung phụ thuộc vào diện tích tự nhiên của tỉnh, thành phố: từ 15.000 đến dưới 18.000 km² bổ sung 1 xe, từ 18.000 đến dưới 21.000 km² bổ sung 2 xe, từ 21.000 đến dưới 24.000 km² bổ sung 3 xe, và từ 24.000 km² trở lên thì cứ tăng thêm 3.000 km² sẽ bổ sung thêm 1 xe.

**Sàng lọc:** câu hỏi mơ hồ — Câu hỏi có/không quá chung chung. Câu hỏi cũng diễn đạt sai chủ thể: người được bổ sung xe là đơn vị ngành dọc quản lý địa bàn nhiều tỉnh, không phải 'các tỉnh, thành phố'. Ngay điểm a liền trước cũng có mức bổ sung theo diện tích (ngưỡng 9.000 km2, cho đơn vị đóng trên 1 tỉnh), dễ lẫn. · Gợi ý câu hỏi: Đơn vị ngành dọc quản lý địa bàn gồm nhiều tỉnh, thành phố, có tổng diện tích tự nhiên khoảng 20.000 km2, thì được bổ sung thêm bao nhiêu xe ô tô vào tiêu chuẩn, định mức?

**Gold: 379/2026/NĐ-CP Điều 12 khoản 4 điểm b**

> Trường hợp tổng diện tích tự nhiên của các tỉnh, thành phố thuộc địa bàn được giao quản lý từ 15.000 km2 đến dưới 18.000 km2 được bổ sung 01 xe, từ 18.000 km2 đến dưới 21.000 km2 được bổ sung 02 xe, từ 21.000 km2 đến dưới 24.000 km2 được bổ sung 03 xe, từ 24.000 km2 trở lên thì cứ 3.000 km2 tăng thêm được bổ sung 01 xe.

---
## q056 · xuyen_khoan · ngoai_le

Trạng thái: DỰ PHÒNG
Câu hỏi: Một nhóm người muốn truyền lại kỹ năng làm nghề truyền thống như dệt lụa cho thế hệ sau, nhưng họ cũng cần sửa chữa một phần kiến trúc cổ để bảo vệ di tích lịch sử, thì việc này có được thực hiện không?

*Đáp án nháp của mô hình:* Việc truyền lại kỹ năng làm nghề truyền thống như dệt lụa được coi là trao truyền di sản văn hóa phi vật thể, phù hợp với quy tắc bảo vệ và phát triển bản sắc văn hóa. Tuy nhiên, nếu cần sửa chữa phần kiến trúc cổ để ngăn chặn di tích khỏi sập đổ, thì chỉ được thực hiện trong phạm vi chống đỡ, gia cố tạm thời, không được tháo rời toàn bộ cấu kiện, và vẫn phải đảm bảo việc bảo tồn di sản văn hóa được thực hiện đúng cách.

**⚠ Kiểm tra tự động:** hai gold không phải quan hệ quy tắc–ngoại lệ (Đoạn B không nêu ra bất kỳ ngoại lệ, giới hạn hay trường hợp loại trừ nào đối với quy định ở đoạn A; hai đoạn là độc lập, không có mối quan hệ biện chứng hay ngoại lệ giữa chúng.)
**Sàng lọc:** KHÔNG trả lời được từ gold; không đúng ý đồ nhóm; câu hỏi mơ hồ — Hai gold là hai định nghĩa không liên quan nhau (di sản phi vật thể, tu sửa cấp thiết di tích), không phải quy tắc–ngoại lệ; câu hỏi gộp hai ý rời và hỏi 'có được thực hiện không' trong khi gold không quy định điều này. · Gợi ý câu hỏi: Khi cần gia cố tạm thời để ngăn một di tích lịch sử - văn hóa khỏi bị sập đổ thì có được tháo rời toàn bộ cấu kiện kiến trúc của di tích không?

**Gold: 45/2024/QH15 Điều 3 khoản 1 — QUY TẮC**

> 1. Di sản văn hóa phi vật thể là tri thức, kỹ năng, tập quán, biểu đạt văn hóa cùng đồ vật, đồ tạo tác, không gian liên quan được cộng đồng, nhóm người, cá nhân thực hành, trao truyền qua nhiều thế hệ và hình thành nên bản sắc văn hóa của họ, không ngừng được trao truyền, bảo vệ, tái tạo, sáng tạo, có giá trị lịch sử, văn hóa, khoa học.

**Gold: 45/2024/QH15 Điều 3 khoản 23 — NGOẠI LỆ**

> 23. Tu sửa cấp thiết di tích là hoạt động sửa chữa hoặc chống đỡ, gia cố, gia cường tạm thời để ngăn chặn di tích khỏi bị sập đổ, hủy hoại nhưng không được tháo rời toàn bộ cấu kiện, thành phần kiến trúc của di tích lịch sử - văn hóa, danh lam thắng cảnh.

*Câu ngoại lệ (dùng chấm 'trả lời thiếu'):* Tu sửa cấp thiết di tích là hoạt động sửa chữa hoặc chống đỡ, gia cố, gia cường tạm thời để ngăn chặn di tích khỏi bị sập đổ, hủy hoại nhưng không được tháo rời toàn bộ cấu kiện, thành phần kiến trúc của di tích lịch sử - văn hóa, danh lam thắng cảnh.

---
## q057 · xuyen_khoan · ngoai_le

Trạng thái: GIỮ
Câu hỏi: Nếu một bị can bị tạm giam, có thể được thay thế bằng việc đặt tiền bảo đảm không, và nếu có, thì bị can phải cam kết những điều gì nếu vi phạm?

*Đáp án nháp của mô hình:* Có thể thay thế tạm giam bằng việc đặt tiền bảo đảm nếu xét thấy hành vi, nhân thân và tình trạng tài sản của bị can phù hợp. Trong trường hợp đó, bị can phải cam kết có mặt khi triệu tập, không bỏ trốn, không tiếp tục phạm tội, không mua chuộc hay làm sai lệch chứng cứ, không đe dọa người làm chứng hay bị hại. Nếu vi phạm, bị can sẽ bị tạm giam và số tiền bảo đảm sẽ bị tịch thu, nộp vào ngân sách nhà nước.

**Sàng lọc:** câu hỏi mơ hồ — Câu hỏi gộp ba ý và cụm 'cam kết những điều gì nếu vi phạm' lủng củng; khoản 2 là nghĩa vụ kèm hệ quả chứ không hẳn là ngoại lệ. · Gợi ý câu hỏi: Bị can được cho đặt tiền bảo đảm thay cho tạm giam nhưng sau đó không có mặt theo giấy triệu tập mà không có lý do bất khả kháng thì bị xử lý thế nào?

**Gold: 101/2015/QH13 Điều 122 khoản 1 — QUY TẮC**

> 1. Đặt tiền để bảo đảm là biện pháp ngăn chặn thay thế tạm giam. Căn cứ tính chất, mức độ nguy hiểm cho xã hội của hành vi, nhân thân và tình trạng tài sản của bị can, bị cáo, Cơ quan điều tra, Viện kiểm sát, Tòa án có thể quyết định cho họ hoặc người thân thích của họ đặt tiền để bảo đảm.

**Gold: 101/2015/QH13 Điều 122 khoản 2 — NGOẠI LỆ**

> 2. Bị can, bị cáo được đặt tiền phải làm giấy cam đoan thực hiện các nghĩa vụ:
> a) Có mặt theo giấy triệu tập, trừ trường hợp vì lý do bất khả kháng hoặc do trở ngại khách quan;
> b) Không bỏ trốn hoặc tiếp tục phạm tội;
> c) Không mua chuộc, cưỡng ép, xúi giục người khác khai báo gian dối, cung cấp tài liệu sai sự thật; không tiêu hủy, giả mạo chứng cứ, tài liệu, đồ vật của vụ án, tẩu tán tài sản liên quan đến vụ án; không đe dọa, khống chế, trả thù người làm chứng, bị hại, người tố giác tội phạm và người thân thích của những người này.
> Trường hợp bị can, bị cáo vi phạm nghĩa vụ cam đoan quy định tại khoản này thì bị tạm giam và số tiền đã đặt bị tịch thu, nộp ngân sách nhà nước.

*Câu ngoại lệ (dùng chấm 'trả lời thiếu'):* a) Có mặt theo giấy triệu tập, trừ trường hợp vì lý do bất khả kháng hoặc do trở ngại khách quan;

---
## q058 · xuyen_khoan · ngoai_le

Trạng thái: DỰ PHÒNG
Câu hỏi: Nếu một người gây cháy tại một khu dân cư và có nguy cơ làm chết hoặc gây thương tích cho người khác, nhưng chưa xảy ra thiệt hại thực tế, thì có bị xử lý theo quy định về phòng cháy, chữa cháy không?

*Đáp án nháp của mô hình:* Có thể bị xử lý theo quy định ngoại lệ nếu có nguy cơ gây thiệt hại cho tính mạng, sức khỏe hoặc tài sản của người khác mà không được ngăn chặn kịp thời, với mức phạt từ cảnh cáo đến tù từ 3 tháng đến 1 năm. Tuy nhiên, nếu đã xảy ra thiệt hại về người hoặc tài sản theo quy định thì sẽ bị xử lý nghiêm theo quy tắc, với mức phạt tù từ 2 năm đến 5 năm hoặc cải tạo không giam giữ đến 3 năm.

**⚠ Kiểm tra tự động:** hai gold không phải quan hệ quy tắc–ngoại lệ (Đoạn B nêu trường hợp có khả năng gây thiệt hại nhưng không được ngăn chặn kịp thời thì bị phạt nhẹ hơn, tức là là một ngoại lệ so với đoạn A, do đó có thể coi là trường hợp loại trừ hoặc giới hạn áp dụng quy định ở đoạn A.)
**Sàng lọc:** câu hỏi mơ hồ — Các cụm 'gây cháy' và 'xử lý theo quy định về phòng cháy, chữa cháy' dễ bị hiểu sang xử phạt hành chính, nên nói rõ là trách nhiệm hình sự. · Gợi ý câu hỏi: Người vi phạm quy định về phòng cháy, chữa cháy tuy chưa gây thiệt hại về người hay tài sản nhưng có khả năng thực tế gây thiệt hại nếu không được ngăn chặn kịp thời thì có bị truy cứu trách nhiệm hình sự không và hình phạt ra sao?

**Gold: 100/2015/QH13 Điều 313 khoản 1 — QUY TẮC**

> 1. Người nào vi phạm quy định về phòng cháy, chữa cháy thuộc một trong những trường hợp sau đây, thì bị phạt cải tạo không giam giữ đến 03 năm hoặc phạt tù từ 02 năm đến 05 năm:
> a) Làm chết 01 người hoặc gây thương tích hoặc gây tổn hại cho sức khỏe của 01 người với tỷ lệ tổn thương cơ thể 61% trở lên;
> b) Gây thương tích hoặc gây tổn hại cho sức khỏe của 02 người với tỷ lệ tổn thương cơ thể của mỗi người từ 31% đến 60%;
> c) Gây thương tích hoặc gây tổn hại cho sức khỏe của 03 người trở lên mà tổng tỷ lệ tổn thương cơ thể của những người này từ 61% đến 121%;
> d) Gây thiệt hại về tài sản từ 100.000.000 đồng đến dưới 500.000.000 đồng.

**Gold: 100/2015/QH13 Điều 313 khoản 5 — NGOẠI LỆ**

> 5. Phạm tội trong trường hợp có khả năng thực tế gây thiệt hại cho tính mạng, sức khỏe hoặc tài sản của người khác, nếu không được ngăn chặn kịp thời, thì bị phạt cảnh cáo, phạt cải tạo không giam giữ đến 01 năm hoặc bị phạt tù từ 03 tháng đến 01 năm.

*Câu ngoại lệ (dùng chấm 'trả lời thiếu'):* Phạm tội trong trường hợp có khả năng thực tế gây thiệt hại cho tính mạng, sức khỏe hoặc tài sản của người khác, nếu không được ngăn chặn kịp thời, thì bị phạt cảnh cáo, phạt cải tạo không giam giữ đến 01 năm hoặc bị phạt tù từ 03 tháng đến 01 năm.

---
## q059 · xuyen_khoan · ngoai_le

Trạng thái: GIỮ
Câu hỏi: Một hỗn hợp chất được tạo ra trong quá trình sản xuất có được coi là hóa chất không, nếu trong đó có chứa một lượng nhỏ dung môi mà khi tách ra thì tính chất của chất chính không thay đổi?

*Đáp án nháp của mô hình:* Có được coi là hóa chất, nhưng nếu dung môi đó khi tách ra không làm thay đổi tính chất của chất chính thì không thuộc trường hợp ngoại lệ và vẫn được xem là hóa chất theo quy định.

**Sàng lọc:** câu hỏi mơ hồ; lộ đáp án / nhắc văn bản — Câu hỏi chép gần nguyên văn ngoại lệ về dung môi và logic rối (hỗn hợp vẫn là hóa chất, chỉ dung môi không được tính vào 'chất'); đáp án nháp hiểu ngược ngoại lệ. · Gợi ý câu hỏi: Một hỗn hợp do doanh nghiệp tạo ra gồm một hợp chất và dung môi hòa tan, tách riêng được mà không làm đổi tính chất của hợp chất; hỗn hợp này có phải là hóa chất không và dung môi có được tính vào thành phần của chất không?

**Gold: 69/2025/QH15 Điều 2 khoản 1 — QUY TẮC**

> 1. Hóa chất là chất, hỗn hợp chất tự nhiên hoặc được con người khai thác, tạo ra.

**Gold: 69/2025/QH15 Điều 2 khoản 2 — NGOẠI LỆ**

> 2. Chất là đơn chất, hợp chất bao gồm cả tạp chất sinh ra trong quá trình chế biến; những phụ gia cần thiết để bảo đảm đặc tính lý, hóa ổn định; không bao gồm dung môi mà khi tách ra thì tính chất của chất đó không thay đổi.

*Câu ngoại lệ (dùng chấm 'trả lời thiếu'):* không bao gồm dung môi mà khi tách ra thì tính chất của chất đó không thay đổi.

---
## q060 · xuyen_khoan · ngoai_le

Trạng thái: GIỮ
Câu hỏi: Trong trường hợp hai bên tranh chấp cùng lựa chọn một trọng tài viên để giải quyết tranh chấp lao động, thì Ban trọng tài lao động sẽ được thành lập như thế nào và có cần phải có đa số đồng thuận để ra quyết định không?

*Đáp án nháp của mô hình:* Trong trường hợp hai bên cùng lựa chọn một trọng tài viên, Ban trọng tài lao động chỉ gồm 01 trọng tài viên đã được lựa chọn. Tuy nhiên, việc ra quyết định vẫn tuân theo nguyên tắc đa số, trừ trường hợp này.

**Sàng lọc:** lộ đáp án / nhắc văn bản — Câu hỏi chép gần nguyên văn điểm c khoản 4; đáp án nháp sai khi nói vẫn quyết định theo đa số. · Gợi ý câu hỏi: Nếu hai bên tranh chấp lao động thống nhất chỉ chọn chung một trọng tài viên thì Ban trọng tài lao động gồm mấy người và có quyết định theo nguyên tắc đa số không?

**Gold: 45/2019/QH14 Điều 185 khoản 4 — QUY TẮC**

> 4. Khi có yêu cầu giải quyết tranh chấp lao động theo quy định tại các điều 189, 193 và 197 của Bộ luật này, Hội đồng trọng tài lao động quyết định thành lập Ban trọng tài lao động để giải quyết tranh chấp như sau:
> a) Đại diện mỗi bên tranh chấp chọn 01 trọng tài viên trong số danh sách trọng tài viên lao động;
> b) Trọng tài viên lao động do các bên lựa chọn theo quy định tại điểm a khoản này thống nhất lựa chọn 01 trọng tài viên lao động khác làm Trưởng Ban trọng tài lao động;
> c) Trường hợp các bên tranh chấp cùng lựa chọn một trọng tài viên để giải quyết tranh chấp lao động thì Ban trọng tài lao động chỉ gồm 01 trọng tài viên lao động đã được lựa chọn.

**Gold: 45/2019/QH14 Điều 185 khoản 5 — NGOẠI LỆ**

> 5. Ban trọng tài lao động làm việc theo nguyên tắc tập thể và quyết định theo đa số, trừ trường hợp quy định tại điểm c khoản 4 Điều này.

*Câu ngoại lệ (dùng chấm 'trả lời thiếu'):* Ban trọng tài lao động làm việc theo nguyên tắc tập thể và quyết định theo đa số, trừ trường hợp quy định tại điểm c khoản 4 Điều này.

---
## q061 · xuyen_khoan · ngoai_le

Trạng thái: GIỮ
Câu hỏi: Nếu một cá nhân đang tham gia tố tụng thì chết, nhưng có người thừa kế, họ có được tham gia tố tụng không? Và nếu đó là một tổ chức không phải là pháp nhân thì sao?

*Đáp án nháp của mô hình:* Nếu cá nhân tham gia tố tụng chết, thì người thừa kế sẽ tham gia tố tụng. Tuy nhiên, nếu đó là một tổ chức không phải là pháp nhân và tổ chức đó chết hoặc bị giải thể, thì sẽ phải cử người khác làm đại diện tham gia tố tụng, và nếu tổ chức phải chấm dứt hoạt động thì thành viên của tổ chức sẽ tham gia tố tụng.

**Sàng lọc:** câu hỏi mơ hồ — Hai câu hỏi rời ghép lại, vế sau thiếu chủ thể (người đại diện của tổ chức chết); khoản 3 là trường hợp song song chứ không phải ngoại lệ của khoản 1; gold khoản 3 dính tiêu đề 'Mục 2'. · Gợi ý câu hỏi: Trong vụ án dân sự, nếu người đại diện của một đương sự là tổ chức không có tư cách pháp nhân chết khi đang tham gia tố tụng thì xử lý thế nào, và khác gì so với trường hợp đương sự là cá nhân chết?

**Gold: 24/2004/QH11 Điều 62 khoản 1 — QUY TẮC**

> 1. Trường hợp đương sự là cá nhân đang tham gia tố tụng chết mà quyền, nghĩa vụ về tài sản của họ được thừa kế thì người thừa kế tham gia tố tụng.

**Gold: 24/2004/QH11 Điều 62 khoản 3 — NGOẠI LỆ**

> 3. Trường hợp đương sự là tổ chức không phải là pháp nhân mà người đại diện hoặc người quản lý đang tham gia tố tụng chết thì tổ chức đó phải cử người khác làm đại diện để tham gia tố tụng; nếu tổ chức đó phải chấm dứt hoạt động, bị giải thể thì cá nhân là thành viên của tổ chức đó tham gia tố tụng.
> Mục 2
> Những người tham gia tố tụng khác

*Câu ngoại lệ (dùng chấm 'trả lời thiếu'):* Trường hợp đương sự là tổ chức không phải là pháp nhân mà người đại diện hoặc người quản lý đang tham gia tố tụng chết thì tổ chức đó phải cử người khác làm đại diện để tham gia tố tụng;

---
## q062 · xuyen_khoan · ngoai_le

Trạng thái: DỰ PHÒNG
Câu hỏi: Có thể huy động tổ chức hoặc cá nhân để tham gia bảo vệ an ninh mạng không, nếu tổ chức đó không phải là lực lượng chuyên trách hay có tổ chức độc lập trong bộ máy nhà nước?

*Đáp án nháp của mô hình:* Có thể huy động tổ chức hoặc cá nhân tham gia bảo vệ an ninh mạng nếu họ có năng lực, kinh nghiệm và điều kiện phù hợp, nhưng lực lượng này không phải là lực lượng chuyên trách, thường trực hay có tổ chức độc lập trong bộ máy nhà nước, cũng không phát sinh biên chế, chức danh hay thẩm quyền công vụ.

**Sàng lọc:** không đúng ý đồ nhóm; câu hỏi mơ hồ; lộ đáp án / nhắc văn bản — Câu hỏi biến nội dung khoản 2 thành điều kiện ('nếu không phải là lực lượng chuyên trách') và chép gần nguyên văn; muốn trả lời 'có' thì chỉ cần khoản 1. · Gợi ý câu hỏi: Tổ chức, cá nhân được huy động làm lực lượng dự bị bảo vệ an ninh mạng có được hưởng biên chế, chức danh hoặc quyền áp dụng biện pháp bảo vệ an ninh mạng không?

**Gold: 329/2026/NĐ-CP Điều 7 khoản 1 — QUY TẮC**

> 1. Lực lượng dự bị bảo vệ an ninh mạng là tổ chức, cá nhân có năng lực, kinh nghiệm, nhân lực, phương tiện, thiết bị, giải pháp kỹ thuật, sản phẩm, dịch vụ hoặc điều kiện phù hợp, được lập danh sách, quản lý, kết nối, phối hợp hoặc huy động tham gia bảo vệ an ninh mạng theo quy định tại điểm c khoản 1 Điều 30 Luật An ninh mạng.

**Gold: 329/2026/NĐ-CP Điều 7 khoản 2 — NGOẠI LỆ**

> 2. Lực lượng dự bị bảo vệ an ninh mạng không phải là lực lượng chuyên trách, lực lượng thường trực hoặc lực lượng có tổ chức độc lập trong bộ máy nhà nước; không làm phát sinh biên chế, chức danh, cấp bậc, thẩm quyền công vụ hoặc quyền áp dụng biện pháp bảo vệ an ninh mạng.

*Câu ngoại lệ (dùng chấm 'trả lời thiếu'):* Lực lượng dự bị bảo vệ an ninh mạng không phải là lực lượng chuyên trách, lực lượng thường trực hoặc lực lượng có tổ chức độc lập trong bộ máy nhà nước;

---
## q063 · xuyen_khoan · ngoai_le

Trạng thái: DỰ PHÒNG
Câu hỏi: Có được phép không cập nhật dữ liệu hàng không một cách nhanh chóng và không chính xác nếu tình huống đó thuộc trường hợp ngoại lệ?

*Đáp án nháp của mô hình:* Có thể cập nhật dữ liệu hàng không nhanh chóng trong trường hợp ngoại lệ, nhưng vẫn phải đảm bảo dữ liệu chính xác, đầy đủ, kịp thời và có thể kiểm chứng, phù hợp với mục đích sử dụng, đồng thời vẫn phải tuân thủ yêu cầu quản lý nhà nước về an toàn và hiệu quả hoạt động bay.

**⚠ Kiểm tra tự động:** hai gold không phải quan hệ quy tắc–ngoại lệ (Đoạn B không nêu ra bất kỳ ngoại lệ, giới hạn hoặc trường hợp loại trừ nào đối với quy định ở đoạn A; hai đoạn là song song, bổ sung nhau về yêu cầu đối với dữ liệu hàng không, chứ không phải một quy định là ngoại lệ của kia.)
**Sàng lọc:** chỉ trả lời được một phần từ gold; không đúng ý đồ nhóm; câu hỏi mơ hồ — Gold là hai yêu cầu chung, không có ngoại lệ nào; câu hỏi nhắc tới một 'trường hợp ngoại lệ' không tồn tại và diễn đạt phủ định rối. · Gợi ý câu hỏi: Dữ liệu và tin tức hàng không phải được quản lý theo nguyên tắc nào và phải đáp ứng những yêu cầu chất lượng gì?

**Gold: 222/2026/NĐ-CP Điều 111 khoản 1 — QUY TẮC**

> 1. Dữ liệu hàng không và tin tức hàng không phải được quản lý thống nhất, bảo đảm phục vụ an toàn, điều hòa, hiệu quả hoạt động bay và đáp ứng yêu cầu quản lý nhà nước về hàng không dân dụng.

**Gold: 222/2026/NĐ-CP Điều 111 khoản 2 — NGOẠI LỆ**

> 2. Dữ liệu hàng không và tin tức hàng không phải bảo đảm các yêu cầu về chính xác, đầy đủ, kịp thời, nhất quán, hợp lệ, có thể kiểm chứng và phù hợp với mục đích sử dụng.

*Câu ngoại lệ (dùng chấm 'trả lời thiếu'):* Dữ liệu hàng không và tin tức hàng không phải bảo đảm các yêu cầu về chính xác, đầy đủ, kịp thời, nhất quán, hợp lệ, có thể kiểm chứng và phù hợp với mục đích sử dụng.

---
## q064 · xuyen_khoan · ngoai_le

Trạng thái: DỰ PHÒNG
Câu hỏi: Nếu một người lái xe vi phạm quy định an toàn giao thông và có khả năng gây thiệt hại cho người khác nhưng chưa xảy ra tai nạn, thì có bị xử phạt không?

*Đáp án nháp của mô hình:* Có, người đó có thể bị phạt tiền từ 10.000.000 đồng đến 50.000.000 đồng, hoặc phạt cải tạo không giam giữ đến 01 năm, hoặc phạt tù từ 03 tháng đến 01 năm, nếu hành vi của họ có khả năng thực tế gây thiệt hại cho tính mạng, sức khỏe hoặc tài sản của người khác mà không được ngăn chặn kịp thời. Tuy nhiên, nếu hành vi đó đã dẫn đến làm chết người hoặc gây thương tích nặng, hoặc gây thiệt hại về tài sản từ 100.000.000 đồng đến dưới 500.000.000 đồng, thì mức phạt sẽ nặng hơn, từ 30.000.000 đồng đến 100.000.000 đồng, hoặc phạt tù từ 01 năm đến 05 năm.

**⚠ Kiểm tra tự động:** hai gold không phải quan hệ quy tắc–ngoại lệ (Đoạn B không nêu ra bất kỳ ngoại lệ, giới hạn hay trường hợp loại trừ nào cho quy định ở đoạn A; hai đoạn là song song, độc lập với nhau, không có mối quan hệ nào là ngoại lệ của bên kia.)
**Sàng lọc:** câu hỏi mơ hồ — Cụm 'có bị xử phạt không' dễ lẫn với xử phạt hành chính; nên nói rõ là trách nhiệm hình sự và hỏi mức hình phạt. · Gợi ý câu hỏi: Người tham gia giao thông đường bộ vi phạm quy định an toàn giao thông, chưa gây tai nạn nhưng có khả năng thực tế gây thiệt hại nếu không được ngăn chặn kịp thời thì có bị truy cứu trách nhiệm hình sự không, hình phạt thế nào?

**Gold: 100/2015/QH13 Điều 260 khoản 1 — QUY TẮC**

> 1. Người nào tham gia giao thông đường bộ mà vi phạm quy định về an toàn giao thông đường bộ thuộc một trong các trường hợp sau đây, thì bị phạt tiền từ 30.000.000 đồng đến 100.000.000 đồng, phạt cải tạo không giam giữ đến 03 năm hoặc phạt tù từ 01 năm đến 05 năm:
> a) Làm chết 01 người hoặc gây thương tích hoặc gây tổn hại cho sức khỏe của 01 người với tỷ lệ tổn thương cơ thể 61% trở lên;
> b) Gây thương tích hoặc gây tổn hại cho sức khỏe cho 02 người với tỷ lệ tổn thương cơ thể của mỗi người từ 31% đến 60%;
> c) Gây thương tích hoặc gây tổn hại cho sức khỏe cho 03 người trở lên mà tổng tỷ lệ tổn thương cơ thể của những người này từ 61% đến 121%;
> d) Gây thiệt hại về tài sản từ 100.000.000 đồng đến dưới 500.000.000 đồng.

**Gold: 100/2015/QH13 Điều 260 khoản 5 — NGOẠI LỆ**

> 5. Vi phạm quy định về an toàn giao thông đường bộ mà có khả năng thực tế dẫn đến hậu quả gây thiệt hại cho tính mạng, sức khỏe hoặc tài sản của người khác nếu không được ngăn chặn kịp thời, thì bị phạt tiền từ 10.000.000 đồng đến 50.000.000 đồng, phạt cải tạo không giam giữ đến 01 năm hoặc phạt tù từ 03 tháng đến 01 năm.

*Câu ngoại lệ (dùng chấm 'trả lời thiếu'):* Vi phạm quy định về an toàn giao thông đường bộ mà có khả năng thực tế dẫn đến hậu quả gây thiệt hại cho tính mạng, sức khỏe hoặc tài sản của người khác nếu không được ngăn chặn kịp thời, thì bị phạt tiền từ 10.000.000 đồng đến 50.000.000 đồng, phạt cải tạo không giam giữ đến 01 năm hoặc phạt tù từ 03 tháng đến 01 năm.

---
## q065 · xuyen_khoan · ngoai_le

Trạng thái: DỰ PHÒNG
Câu hỏi: Nếu một doanh nghiệp bán hàng hóa và gặp sự cố không thể sử dụng hóa đơn điện tử có mã của cơ quan thuế do lỗi kỹ thuật, thì doanh nghiệp đó có thể sử dụng hóa đơn điện tử có mã của cơ quan thuế trong thời gian xử lý sự cố không?

*Đáp án nháp của mô hình:* Doanh nghiệp có thể đến cơ quan thuế để sử dụng hóa đơn điện tử có mã của cơ quan thuế trong thời gian xử lý sự cố. Tuy nhiên, nếu sự cố xảy ra do các tình huống bất khả kháng như chiến tranh, bạo loạn, đình công hoặc rủi ro không do lỗi chủ quan của doanh nghiệp, thì doanh nghiệp được phép tạm ngừng gửi hóa đơn điện tử và phải ghi chép sổ sách, lưu giữ tài liệu chứng minh tình hình đó trong vòng 03 ngày làm việc kể từ ngày sự cố được khắc phục.

**⚠ Kiểm tra tự động:** hai gold không phải quan hệ quy tắc–ngoại lệ (Đoạn B nêu rõ trường hợp bất khả kháng khiến không thể lập, cấp mã hoặc truyền dữ liệu hóa đơn điện tử, trong đó người bán được phép thực hiện việc lập và gửi hóa đơn điện tử sau 03 ngày làm việc kể từ ngày sự cố được khắc phục, điều này là một ngoại lệ đối với quy trình trong đoạn A, tức là khi có sự cố do yếu tố bất khả kháng, người bán không cần phải liên hệ cơ quan thuế ngay lập tức hay phải sử dụng hóa đơn điện tử có mã của cơ quan thuế trong thời gian xử lý sự cố như quy định tại đoạn A.)
**Sàng lọc:** không đúng ý đồ nhóm; lộ đáp án / nhắc văn bản — Câu hỏi chép gần nguyên văn khoản 1 và chỉ cần khoản 1, không dùng khoản 5 (bất khả kháng); đáp án nháp đọc sai khoản 5. · Gợi ý câu hỏi: Người bán đang dùng hóa đơn điện tử có mã của cơ quan thuế nhưng phải ngừng kinh doanh do đình công nên không lập, truyền được hóa đơn đúng hạn thì xử lý thế nào, và khác gì so với khi chỉ gặp sự cố kỹ thuật?

**Gold: 254/2026/NĐ-CP Điều 14 khoản 1 — QUY TẮC**

> 1. Trường hợp người bán hàng hóa, cung cấp dịch vụ sử dụng hóa đơn điện tử có mã của cơ quan thuế nhưng gặp sự cố dẫn đến không sử dụng được hóa đơn điện tử có mã của cơ quan thuế thì liên hệ với cơ quan thuế hoặc tổ chức cung cấp dịch vụ để hỗ trợ xử lý sự cố. Trong thời gian xử lý sự cố, người bán hàng hóa, cung cấp dịch vụ có yêu cầu sử dụng hóa đơn điện tử có mã của cơ quan thuế thì đến cơ quan thuế để sử dụng hóa đơn điện tử có mã của cơ quan thuế.

**Gold: 254/2026/NĐ-CP Điều 14 khoản 5 — NGOẠI LỆ**

> 5. Trong trường hợp bất khả kháng theo quy định tại khoản 21 Điều 4 Luật Quản lý thuế số 108/2025/QH15 gồm chiến tranh, bạo loạn, đình công phải ngừng, nghỉ sản xuất, kinh doanh hoặc rủi ro không thuộc nguyên nhân, trách nhiệm chủ quan của người bán mà người bán hoặc cơ quan thuế không thể thực hiện việc lập, cấp mã hoặc truyền dữ liệu hóa đơn điện tử đúng thời hạn:
> a) Trong vòng 03 ngày làm việc kể từ ngày sự cố được khắc phục, người bán được thực hiện việc lập và gửi hóa đơn điện tử tới cơ quan thuế;
> b) Người bán có trách nhiệm ghi chép sổ sách kế toán về giao dịch mua bán, lưu giữ tài liệu chứng minh trường hợp bất khả kháng theo quy định.

*Câu ngoại lệ (dùng chấm 'trả lời thiếu'):* Trong trường hợp bất khả kháng theo quy định tại khoản 21 Điều 4 Luật Quản lý thuế số 108/2025/QH15 gồm chiến tranh, bạo loạn, đình công phải ngừng, nghỉ sản xuất, kinh doanh hoặc rủi ro không thuộc nguyên nhân, trách nhiệm chủ quan của người bán mà người bán hoặc cơ quan thuế không thể thực hiện việc lập, cấp mã hoặc truyền dữ liệu hóa đơn điện tử đúng thời hạn:

---
## q066 · xuyen_khoan · ngoai_le

Trạng thái: DỰ PHÒNG
Câu hỏi: Chánh Văn phòng Trung ương Đảng có được quyết định sử dụng xe ô tô cho các cơ quan thuộc đơn vị trực thuộc mình không, nếu đó là các tổ chức chính trị - xã hội ở trung ương như Liên đoàn Lao động không?

*Đáp án nháp của mô hình:* Chánh Văn phòng Trung ương Đảng có quyền quyết định sử dụng xe ô tô cho các cơ quan thuộc đơn vị trực thuộc, nhưng đối với các tổ chức chính trị - xã hội ở trung ương, việc quyết định thuộc về Ban Thường trực Ủy ban Trung ương Mặt trận Tổ quốc Việt Nam, trừ trường hợp Tổng Liên đoàn Lao động Việt Nam.

**Sàng lọc:** chỉ trả lời được một phần từ gold; không đúng ý đồ nhóm; câu hỏi mơ hồ — Câu hỏi rối và lấy ví dụ Liên đoàn Lao động, đúng trường hợp bị loại trừ ở khoản 9 nên gold không cho biết ai quyết định; khoản 9 là thẩm quyền của chủ thể khác, không phải ngoại lệ của khoản 1. · Gợi ý câu hỏi: Chánh Văn phòng Trung ương Đảng có thẩm quyền quyết định về xe ô tô của các tổ chức chính trị - xã hội ở trung ương không, hay thẩm quyền đó thuộc về ai?

**Gold: 379/2026/NĐ-CP Điều 5 khoản 1 — QUY TẮC**

> 1. Chánh Văn phòng Trung ương Đảng đối với xe ô tô của các cơ quan, đơn vị là đơn vị dự toán cấp dưới trực thuộc Văn phòng Trung ương Đảng.

**Gold: 379/2026/NĐ-CP Điều 5 khoản 9 — NGOẠI LỆ**

> 9. Ban Thường trực Ủy ban Trung ương Mặt trận Tổ quốc Việt Nam:
> a) Quyết định đối với xe ô tô của các cơ quan, đơn vị thuộc phạm vi quản lý, bao gồm Văn phòng Đảng ủy Mặt trận Tổ quốc, các đoàn thể Trung ương; không bao gồm các tổ chức chính trị - xã hội ở trung ương.
> b) Quyết định hoặc phân cấp thẩm quyền quyết định đối với các tổ chức chính trị - xã hội ở trung ương (trừ Tổng Liên đoàn Lao động Việt Nam).

*Câu ngoại lệ (dùng chấm 'trả lời thiếu'):* không bao gồm các tổ chức chính trị - xã hội ở trung ương.

---
## q067 · xuyen_khoan · ngoai_le

Trạng thái: DỰ PHÒNG
Câu hỏi: Công ty muốn thay đổi ngành nghề kinh doanh, thì cần bao nhiêu cổ đông đồng ý, và có trường hợp nào ngoại lệ không?

*Đáp án nháp của mô hình:* Cần ít nhất 65% cổ đông đại diện tại cuộc họp đồng ý, trừ các trường hợp được quy định trong Điều lệ công ty; tuy nhiên, nếu nội dung thay đổi ngành nghề thuộc các trường hợp được ngoại lệ, thì chỉ cần hơn 50% cổ đông đồng ý.

**⚠ Kiểm tra tự động:** hai gold không phải quan hệ quy tắc–ngoại lệ (Đoạn B chỉ nêu điều kiện thông qua nghị quyết với tỷ lệ cổ đông sở hữu trên 50%, trong khi đoạn A yêu cầu 65% phiếu biểu quyết, nên đoạn B không phải là ngoại lệ hay giới hạn áp dụng cho đoạn A, mà là một quy định song song, không liên quan đến việc loại trừ hoặc áp dụng điều kiện của đoạn A.)
**Sàng lọc:** chỉ trả lời được một phần từ gold; không đúng ý đồ nhóm; câu hỏi mơ hồ — Thiếu 'cổ phần' sau 'công ty'; tỷ lệ 65% chỉ cần khoản 1, còn các ngoại lệ thật (khoản 3, 4, 6) không có trong gold; vai bị đảo (khoản 2 mới là quy tắc chung); đáp án nháp sai. · Gợi ý câu hỏi: Tại cuộc họp Đại hội đồng cổ đông của công ty cổ phần, nghị quyết thay đổi ngành, nghề kinh doanh cần tỷ lệ tán thành bao nhiêu, và khác gì so với tỷ lệ thông qua các nghị quyết thông thường?

**Gold: 59/2020/QH14 Điều 148 khoản 1 — QUY TẮC**

> 1. Nghị quyết về nội dung sau đây được thông qua nếu được số cổ đông đại diện từ 65% tổng số phiếu biểu quyết trở lên của tất cả cổ đông dự họp tán thành, trừ trường hợp quy định tại các khoản 3, 4 và 6 Điều này; tỷ lệ cụ thể do Điều lệ công ty quy định:
> a) Loại cổ phần và tổng số cổ phần của từng loại;
> b) Thay đổi ngành, nghề và lĩnh vực kinh doanh;
> c) Thay đổi cơ cấu tổ chức quản lý công ty;
> d) Dự án đầu tư hoặc bán tài sản có giá trị từ 35% tổng giá trị tài sản trở lên được ghi trong báo cáo tài chính gần nhất của công ty, trừ trường hợp Điều lệ công ty quy định tỷ lệ hoặc giá trị khác;
> đ) Tổ chức lại, giải thể công ty;
> e) Vấn đề khác do Điều lệ công ty quy định.

**Gold: 59/2020/QH14 Điều 148 khoản 2 — NGOẠI LỆ**

> 2. Các nghị quyết được thông qua khi được số cổ đông sở hữu trên 50% tổng số phiếu biểu quyết của tất cả cổ đông dự họp tán thành, trừ trường hợp quy định tại các khoản 1, 3, 4 và 6 Điều này; tỷ lệ cụ thể do Điều lệ công ty quy định.

*Câu ngoại lệ (dùng chấm 'trả lời thiếu'):* Các nghị quyết được thông qua khi được số cổ đông sở hữu trên 50% tổng số phiếu biểu quyết của tất cả cổ đông dự họp tán thành, trừ trường hợp quy định tại các khoản 1, 3, 4 và 6 Điều này;

---
## q068 · xuyen_khoan · ngoai_le

Trạng thái: GIỮ
Câu hỏi: Văn phòng Chính phủ có được phân bổ xe ô tô cho các đơn vị trực thuộc không, nếu những đơn vị đó nằm trong phạm vi điều hòa của bộ, cơ quan trung ương?

*Đáp án nháp của mô hình:* Có, Văn phòng Chính phủ được phân bổ xe ô tô cho các đơn vị trực thuộc trong phạm vi điều hòa của bộ, cơ quan trung ương, nhưng không áp dụng với các trường hợp được nêu tại ngoại lệ, cụ thể là các đơn vị thuộc phạm vi điều hòa trong cục loại 1 và tương đương.

**Sàng lọc:** câu hỏi mơ hồ — Vế điều kiện 'nếu nằm trong phạm vi điều hòa của bộ, cơ quan trung ương' vòng vo; ngoại lệ thật (điều hòa trong phạm vi cục loại 1) không được hỏi tới; đáp án nháp hiểu sai điểm b. · Gợi ý câu hỏi: Văn phòng Chính phủ có được điều hòa xe ô tô giữa các đơn vị thuộc mình không, và đối với cục loại 1 thì phạm vi điều hòa xe bị giới hạn thế nào?

**Gold: 379/2026/NĐ-CP Điều 23 khoản 1 — QUY TẮC**

> 1. Đối tượng áp dụng: Văn phòng Trung ương Đảng, đơn vị dự toán cấp dưới trực thuộc Văn phòng Trung ương Đảng, Học viện Chính trị quốc gia Hồ Chí Minh, đơn vị sự nghiệp của Ban Chấp hành Trung ương Đảng, Văn phòng Chủ tịch nước, Văn phòng Chính phủ, bộ, cơ quan ngang bộ, Văn phòng Quốc hội, Kiểm toán nhà nước, Ủy ban Trung ương Mặt trận Tổ quốc Việt Nam (bao gồm các tổ chức chính trị - xã hội ở trung ương, trừ Tổng Liên đoàn Lao động Việt Nam), Tổng Liên đoàn Lao động Việt Nam, cơ quan khác ở trung ương (gọi chung là bộ, cơ quan trung ương).

**Gold: 379/2026/NĐ-CP Điều 23 khoản 2 — NGOẠI LỆ**

> 2. Phạm vi phân bổ (điều hòa) số lượng xe ô tô (không bao gồm đối tượng tại khoản 1 Điều 22 Nghị định này)
> a) Phân bổ (điều hòa) giữa các cơ quan, tổ chức, đơn vị thuộc bộ, cơ quan trung ương, trừ các trường hợp quy định tại điểm b khoản này.
> b) Phân bổ (điều hòa) trong phạm vi cục loại 1 và tương đương.

*Câu ngoại lệ (dùng chấm 'trả lời thiếu'):* Phạm vi phân bổ (điều hòa) số lượng xe ô tô (không bao gồm đối tượng tại khoản 1 Điều 22 Nghị định này)

---
## q069 · xuyen_khoan · ngoai_le

Trạng thái: GIỮ
Câu hỏi: Công ty sản xuất điện có được cho người lao động làm thêm giờ trong trường hợp xảy ra thiên tai không, và nếu có thì có giới hạn về số giờ làm thêm không?

*Đáp án nháp của mô hình:* Có, công ty được phép cho người lao động làm thêm giờ trong trường hợp xảy ra thiên tai do tính chất công việc cấp bách, không thể trì hoãn, và số giờ làm thêm không quá 300 giờ trong năm, nhưng vẫn phải tuân thủ giới hạn về thời gian làm việc bình thường và làm thêm theo quy định chung, cụ thể là không quá 200 giờ trong năm nếu không thuộc trường hợp ngoại lệ được quy định.

**Sàng lọc:** không thấy vấn đề — Vai bị đảo (khoản 2 là quy tắc chung 200 giờ, khoản 3 là ngoại lệ 300 giờ) nhưng câu hỏi vẫn dùng đủ cả hai khoản; đáp án nháp sai khi nói vẫn giới hạn 200 giờ.

**Gold: 45/2019/QH14 Điều 107 khoản 3 — QUY TẮC**

> 3. Người sử dụng lao động được sử dụng người lao động làm thêm không quá 300 giờ trong 01 năm trong một số ngành, nghề, công việc hoặc trường hợp sau đây:
> a) Sản xuất, gia công xuất khẩu sản phẩm hàng dệt, may, da, giày, điện, điện tử, chế biến nông, lâm, diêm nghiệp, thủy sản;
> b) Sản xuất, cung cấp điện, viễn thông, lọc dầu; cấp, thoát nước;
> c) Trường hợp giải quyết công việc đòi hỏi lao động có trình độ chuyên môn, kỹ thuật cao mà thị trường lao động không cung ứng đầy đủ, kịp thời;
> d) Trường hợp phải giải quyết công việc cấp bách, không thể trì hoãn do tính chất thời vụ, thời điểm của nguyên liệu, sản phẩm hoặc để giải quyết công việc phát sinh do yếu tố khách quan không dự liệu trước, do hậu quả thời tiết, thiên tai, hỏa hoạn, địch họa, thiếu điện, thiếu nguyên liệu, sự cố kỹ thuật của dây chuyền sản xuất;
> đ) Trường hợp khác do Chính phủ quy định.

**Gold: 45/2019/QH14 Điều 107 khoản 2 — NGOẠI LỆ**

> 2. Người sử dụng lao động được sử dụng người lao động làm thêm giờ khi đáp ứng đầy đủ các yêu cầu sau đây:
> a) Phải được sự đồng ý của người lao động;
> b) Bảo đảm số giờ làm thêm của người lao động không quá 50% số giờ làm việc bình thường trong 01 ngày; trường hợp áp dụng quy định thời giờ làm việc bình thường theo tuần thì tổng số giờ làm việc bình thường và số giờ làm thêm không quá 12 giờ trong 01 ngày; không quá 40 giờ trong 01 tháng;
> c) Bảo đảm số giờ làm thêm của người lao động không quá 200 giờ trong 01 năm, trừ trường hợp quy định tại khoản 3 Điều này.

*Câu ngoại lệ (dùng chấm 'trả lời thiếu'):* c) Bảo đảm số giờ làm thêm của người lao động không quá 200 giờ trong 01 năm, trừ trường hợp quy định tại khoản 3 Điều này.

---
## q070 · xuyen_khoan · ngoai_le

Trạng thái: GIỮ
Câu hỏi: Chủ tịch Hội đồng quản trị của một tổ chức tín dụng có được đồng thời là người điều hành của tổ chức tín dụng khác và thành viên Ban kiểm soát của một ngân hàng khác không?

*Đáp án nháp của mô hình:* Không được, vì theo quy tắc, Chủ tịch Hội đồng quản trị không được đồng thời là người điều hành, thành viên Ban kiểm soát của tổ chức tín dụng đó và tổ chức tín dụng khác. Tuy nhiên, có ngoại lệ nếu Chủ tịch Hội đồng quản trị của quỹ tín dụng nhân dân đồng thời là thành viên Hội đồng quản trị hoặc thành viên Ban kiểm soát của ngân hàng hợp tác xã.

**Cờ tự động:** trùng từ cao (89%)
**Sàng lọc:** không đúng ý đồ nhóm; lộ đáp án / nhắc văn bản — Trả lời 'không' chỉ cần khoản 1 (ngoại lệ quỹ tín dụng nhân dân cũng nằm trong khoản 1), không dùng tới khoản 2 về thành viên Hội đồng quản trị khác; câu hỏi chép gần nguyên văn. · Gợi ý câu hỏi: Trong một tổ chức tín dụng, giữa Chủ tịch Hội đồng quản trị và một thành viên Hội đồng quản trị không độc lập, ai được phép kiêm nhiệm chức Tổng giám đốc của chính tổ chức tín dụng đó?

**Gold: 32/2024/QH15 Điều 43 khoản 1 — QUY TẮC**

> 1. Chủ tịch Hội đồng quản trị, Chủ tịch Hội đồng thành viên của tổ chức tín dụng không được đồng thời là người điều hành, thành viên Ban kiểm soát của tổ chức tín dụng đó và tổ chức tín dụng khác, người quản lý doanh nghiệp khác, trừ trường hợp Chủ tịch Hội đồng quản trị của quỹ tín dụng nhân dân đồng thời là thành viên Hội đồng quản trị hoặc thành viên Ban kiểm soát của ngân hàng hợp tác xã.

**Gold: 32/2024/QH15 Điều 43 khoản 2 — NGOẠI LỆ**

> 2. Thành viên Hội đồng quản trị không phải là thành viên độc lập; thành viên Hội đồng thành viên của tổ chức tín dụng không được đồng thời đảm nhiệm một trong các chức vụ sau đây:
> a) Người điều hành tổ chức tín dụng đó, trừ trường hợp là Tổng giám đốc (Giám đốc) của tổ chức tín dụng đó;
> b) Người quản lý, người điều hành tổ chức tín dụng khác, người quản lý doanh nghiệp khác, trừ trường hợp là người quản lý, người điều hành công ty con của tổ chức tín dụng đó hoặc của công ty mẹ của tổ chức tín dụng đó hoặc trường hợp thực hiện phương án chuyển giao bắt buộc đã được phê duyệt;
> c) Kiểm soát viên, thành viên Ban kiểm soát của tổ chức tín dụng khác, doanh nghiệp khác.

*Câu ngoại lệ (dùng chấm 'trả lời thiếu'):* Thành viên Hội đồng quản trị không phải là thành viên độc lập;

---
## q071 · xuyen_khoan · ngoai_le

Trạng thái: DỰ PHÒNG
Câu hỏi: Một công ty có được phép tham gia hoạt động bao thanh toán nếu công ty đó là công ty liên kết của một tổ chức tín dụng không?

*Đáp án nháp của mô hình:* Công ty có thể tham gia hoạt động bao thanh toán nếu không phải là công ty con của tổ chức tín dụng và không vượt quá tỷ lệ sở hữu 11% vốn điều lệ hoặc cổ phần có quyền biểu quyết. Tuy nhiên, nếu công ty đó là công ty liên kết với tổ chức tín dụng và sở hữu trên 11% vốn hoặc cổ phần biểu quyết, thì không được tham gia hoạt động bao thanh toán theo quy định.

**⚠ Kiểm tra tự động:** hai gold không phải quan hệ quy tắc–ngoại lệ (Đoạn B không nêu ra bất kỳ ngoại lệ, giới hạn hay trường hợp loại trừ nào đối với quy định ở đoạn A; hai đoạn này là độc lập, không liên quan đến nhau về nội dung quy tắc hoặc ngoại lệ.)
**Sàng lọc:** KHÔNG trả lời được từ gold; không đúng ý đồ nhóm — Hai gold chỉ là định nghĩa (bao thanh toán, công ty liên kết), không quy định công ty nào được hoạt động bao thanh toán nên không trả lời được; đáp án nháp bịa. · Gợi ý câu hỏi: Một công ty mà tổ chức tín dụng nắm 15% vốn điều lệ nhưng không phải là công ty con thì có quan hệ gì với tổ chức tín dụng đó theo luật?

**Gold: 32/2024/QH15 Điều 4 khoản 1 — QUY TẮC**

> 1. Bao thanh toán là hình thức cấp tín dụng thông qua việc mua lại khoản phải thu của bên bán hoặc ứng trước tiền thanh toán thay cho bên mua theo hợp đồng mua, bán hàng hóa, cung ứng dịch vụ giữa bên mua và bên bán.

**Gold: 32/2024/QH15 Điều 4 khoản 11 — NGOẠI LỆ**

> 11. Công ty liên kết của tổ chức tín dụng là công ty mà tổ chức tín dụng hoặc tổ chức tín dụng và người có liên quan của tổ chức tín dụng sở hữu trên 11% vốn điều lệ hoặc trên 11% số cổ phần có quyền biểu quyết, nhưng không phải là công ty con của tổ chức tín dụng đó.

*Câu ngoại lệ (dùng chấm 'trả lời thiếu'):* Công ty liên kết của tổ chức tín dụng là công ty mà tổ chức tín dụng hoặc tổ chức tín dụng và người có liên quan của tổ chức tín dụng sở hữu trên 11% vốn điều lệ hoặc trên 11% số cổ phần có quyền biểu quyết, nhưng không phải là công ty con của tổ chức tín dụng đó.

---
## q072 · xuyen_khoan · ngoai_le

Trạng thái: DỰ PHÒNG
Câu hỏi: Nếu xảy ra tai nạn giao thông và có người bị nạn, người có mặt tại hiện trường có được sử dụng phương tiện của mình để đưa nạn nhân đi cấp cứu không, nếu không có phương tiện nào khác?

*Đáp án nháp của mô hình:* Có được sử dụng phương tiện để đưa nạn nhân đi cấp cứu nếu không có phương tiện nào khác, nhưng phải xác định rõ vị trí phương tiện và nạn nhân tại hiện trường, không được làm thay đổi hoặc mất dấu vết liên quan đến vụ tai nạn, và nếu có người chết phải giữ nguyên hiện trường và che đậy thi thể.

**Cờ tự động:** trùng từ cao (85%)
**Sàng lọc:** chỉ trả lời được một phần từ gold; câu hỏi mơ hồ; lộ đáp án / nhắc văn bản — Gold chỉ hạn chế việc dùng 'phương tiện liên quan đến vụ tai nạn' nhưng câu hỏi nói 'phương tiện của mình' nên lệch nghĩa; cụm 'không có phương tiện nào khác' làm lộ điều kiện của đáp án. · Gợi ý câu hỏi: Người có mặt tại nơi xảy ra tai nạn giao thông đường bộ muốn dùng chính chiếc xe liên quan đến vụ tai nạn để chở người bị thương đi cấp cứu thì có được không và phải lưu ý những gì?

**Gold: 36/2024/QH15 Điều 80 khoản 2 — QUY TẮC**

> 2. Người có mặt tại nơi xảy ra vụ tai nạn giao thông đường bộ có trách nhiệm sau đây:
> a) Giúp đỡ, cứu chữa kịp thời người bị nạn;
> b) Báo tin ngay cho cơ quan Công an, cơ sở khám bệnh, chữa bệnh hoặc Ủy ban nhân dân nơi gần nhất;
> c) Tham gia bảo vệ hiện trường;
> d) Tham gia bảo vệ tài sản của người bị nạn;
> đ) Cung cấp thông tin liên quan về vụ tai nạn theo yêu cầu của cơ quan có thẩm quyền.

**Gold: 36/2024/QH15 Điều 80 khoản 3 — NGOẠI LỆ**

> 3. Người được quy định tại khoản 1 và khoản 2 Điều này chỉ được sử dụng phương tiện liên quan đến vụ tai nạn giao thông đường bộ để đưa nạn nhân đi cấp cứu trong trường hợp không có phương tiện nào khác nhưng phải xác định vị trí phương tiện, vị trí nạn nhân tại hiện trường, không được làm thay đổi, mất dấu vết liên quan đến vụ tai nạn giao thông đường bộ. Trường hợp có người chết phải giữ nguyên hiện trường và che đậy thi thể.

*Câu ngoại lệ (dùng chấm 'trả lời thiếu'):* Người được quy định tại khoản 1 và khoản 2 Điều này chỉ được sử dụng phương tiện liên quan đến vụ tai nạn giao thông đường bộ để đưa nạn nhân đi cấp cứu trong trường hợp không có phương tiện nào khác nhưng phải xác định vị trí phương tiện, vị trí nạn nhân tại hiện trường, không được làm thay đổi, mất dấu vết liên quan đến vụ tai nạn giao thông đường bộ.

---
## q073 · xuyen_khoan · ngoai_le

Trạng thái: DỰ PHÒNG
Câu hỏi: Một người có thể dùng bút danh để ký tên trong hợp đồng hay không, nếu việc đó làm ảnh hưởng đến quyền lợi của người khác?

*Đáp án nháp của mô hình:* Có thể dùng bút danh trong hợp đồng nếu việc đó không gây thiệt hại đến quyền lợi hợp pháp của người khác, nhưng nếu gây thiệt hại thì không được phép.

**⚠ Kiểm tra tự động:** hai gold không phải quan hệ quy tắc–ngoại lệ (Đoạn B không phải là ngoại lệ, giới hạn hoặc trường hợp loại trừ đối với quy định ở đoạn A; hai đoạn này là độc lập, không mâu thuẫn nhau về nội dung pháp lý, vì đoạn A nói về quyền có họ, tên theo khai sinh, còn đoạn B nói về việc sử dụng bí danh, bút danh không gây thiệt hại đến quyền lợi hợp pháp của người khác. Không có sự liên hệ hay loại trừ trực tiếp giữa hai quy định.)
**Sàng lọc:** chỉ trả lời được một phần từ gold; không đúng ý đồ nhóm — Chỉ cần khoản 3 là trả lời được; khoản 1 không phải quy tắc mà khoản 3 loại trừ, và gold không nói gì về việc ký hợp đồng. · Gợi ý câu hỏi: Họ, tên của một cá nhân được xác định theo căn cứ nào, và cá nhân đó có được tùy ý dùng bút danh thay cho họ tên ấy không?

**Gold: 33/2005/QH11 Điều 26 khoản 1 — QUY TẮC**

> 1. Cá nhân có quyền có họ, tên. Họ, tên của một người được xác định theo họ, tên khai sinh của người đó.

**Gold: 33/2005/QH11 Điều 26 khoản 3 — NGOẠI LỆ**

> 3. Việc sử dụng bí danh, bút danh không được gây thiệt hại đến quyền, lợi ích hợp pháp của người khác.

*Câu ngoại lệ (dùng chấm 'trả lời thiếu'):* Việc sử dụng bí danh, bút danh không được gây thiệt hại đến quyền, lợi ích hợp pháp của người khác.

---
## q074 · xuyen_khoan · ngoai_le

Trạng thái: GIỮ
Câu hỏi: Khi thuê vận chuyển, nếu cả hai bên đã thỏa thuận mức cước phí khác với mức quy định thì bên thuê có phải thanh toán cước phí sau khi hàng hóa được chuyển lên phương tiện không?

*Đáp án nháp của mô hình:* Có, bên thuê vẫn phải thanh toán cước phí sau khi hàng hóa được chuyển lên phương tiện, trừ khi hai bên đã có thỏa thuận khác về việc thanh toán.

**Sàng lọc:** không đúng ý đồ nhóm; câu hỏi mơ hồ — Câu hỏi thực chất chỉ hỏi thời điểm thanh toán (chỉ cần khoản 2); tiền đề 'thỏa thuận mức cước khác mức quy định' thuộc khoản 1 nhưng không được hỏi nên chỉ gây nhiễu. · Gợi ý câu hỏi: Hai bên trong hợp đồng vận chuyển thỏa thuận mức cước thấp hơn mức pháp luật quy định và hẹn trả cước khi hàng tới nơi; bên thuê phải trả theo mức cước nào và vào thời điểm nào?

**Gold: 33/2005/QH11 Điều 538 khoản 1 — QUY TẮC**

> 1. Mức cước phí vận chuyển do các bên thoả thuận; nếu pháp luật có quy định về mức cước phí vận chuyển thì áp dụng mức cước phí đó.

**Gold: 33/2005/QH11 Điều 538 khoản 2 — NGOẠI LỆ**

> 2. Bên thuê vận chuyển phải thanh toán đủ cước phí vận chuyển sau khi tài sản được chuyển lên phương tiện vận chuyển, trừ trường hợp có thoả thuận khác.

*Câu ngoại lệ (dùng chấm 'trả lời thiếu'):* Bên thuê vận chuyển phải thanh toán đủ cước phí vận chuyển sau khi tài sản được chuyển lên phương tiện vận chuyển, trừ trường hợp có thoả thuận khác.

---
## q075 · xuyen_khoan · ngoai_le

Trạng thái: GIỮ
Câu hỏi: Một thành viên Hội đồng quản trị có được tham gia biểu quyết khi nội dung đó có xung đột lợi ích với chính mình không?

*Đáp án nháp của mô hình:* Không, nếu nội dung biểu quyết có xung đột lợi ích với thành viên thì thành viên đó không được tham gia biểu quyết, dù vẫn có quyền tham dự cuộc họp và thảo luận, nhưng phải chịu trách nhiệm trước Hội đồng quản trị và Đại hội thành viên về quyết định của mình.

**Sàng lọc:** không đúng ý đồ nhóm; câu hỏi mơ hồ — Khoản 4 đã chứa cả quy tắc lẫn ngoại lệ nên không cần khoản 1; câu hỏi chung chung về HĐQT, có thể khớp với nhiều luật, và gần trùng q180 (cùng luật). · Gợi ý câu hỏi: Thành viên Hội đồng quản trị của quỹ tín dụng nhân dân phải hành động vì lợi ích của ai khi thực hiện nhiệm vụ, và có được biểu quyết về vấn đề có xung đột lợi ích với bản thân không?

**Gold: 32/2024/QH15 Điều 90 khoản 1 — QUY TẮC**

> 1. Thực hiện quyền, nghĩa vụ của thành viên Hội đồng quản trị theo quy định nội bộ của Hội đồng quản trị và sự phân công của Chủ tịch Hội đồng quản trị một cách trung thực, cẩn trọng, vì lợi ích của ngân hàng hợp tác xã, quỹ tín dụng nhân dân, thành viên; chịu trách nhiệm về việc thực hiện quyền, nghĩa vụ của mình.

**Gold: 32/2024/QH15 Điều 90 khoản 4 — NGOẠI LỆ**

> 4. Tham dự cuộc họp Hội đồng quản trị, thảo luận và biểu quyết về nội dung thuộc nhiệm vụ, quyền hạn của Hội đồng quản trị, chịu trách nhiệm trước Đại hội thành viên và Hội đồng quản trị về quyết định của mình. Trường hợp nội dung biểu quyết có xung đột lợi ích với thành viên nào thì thành viên đó không được tham gia biểu quyết.

*Câu ngoại lệ (dùng chấm 'trả lời thiếu'):* Trường hợp nội dung biểu quyết có xung đột lợi ích với thành viên nào thì thành viên đó không được tham gia biểu quyết.

---
## q076 · xuyen_khoan · ngoai_le

Trạng thái: DỰ PHÒNG
Câu hỏi: Một thẩm phán có được tham gia xét xử lại cùng một vụ án sau khi đã tham gia xét xử sơ thẩm và phúc thẩm không?

*Đáp án nháp của mô hình:* Có được, nhưng chỉ trong trường hợp họ đã tham gia xét xử sơ thẩm, phúc thẩm, giám đốc thẩm hoặc tái thẩm, trừ khi họ là thành viên của Hội đồng Thẩm phán Toà án nhân dân tối cao hoặc Uỷ ban Thẩm phán Toà án nhân dân cấp tỉnh.

**Sàng lọc:** không đúng ý đồ nhóm; câu hỏi mơ hồ; gold đáng ngờ — Khoản 1 chỉ là mảnh 'thuộc trường hợp tại Điều 46', thiếu câu dẫn và không liên quan; ngoại lệ nằm gọn trong khoản 3; câu hỏi không nêu là tố tụng dân sự; đáp án nháp sai ('Có được'). · Gợi ý câu hỏi: Trong tố tụng dân sự, Thẩm phán đã xét xử sơ thẩm một vụ án có được tiếp tục xét xử vụ án đó theo thủ tục giám đốc thẩm không, và có ngoại lệ nào?

**Gold: 24/2004/QH11 Điều 47 khoản 1 — QUY TẮC**

> 1. Thuộc một trong những trường hợp quy định tại Điều 46 của Bộ luật này;

**Gold: 24/2004/QH11 Điều 47 khoản 3 — NGOẠI LỆ**

> 3. Họ đã tham gia xét xử sơ thẩm, phúc thẩm, giám đốc thẩm hoặc tái thẩm vụ án đó, trừ trường hợp là thành viên của Hội đồng Thẩm phán Toà án nhân dân tối cao, Uỷ ban Thẩm phán Toà án nhân dân cấp tỉnh thì vẫn được tham gia xét xử nhiều lần cùng một vụ án theo thủ tục giám đốc thẩm, tái thẩm;

*Câu ngoại lệ (dùng chấm 'trả lời thiếu'):* Họ đã tham gia xét xử sơ thẩm, phúc thẩm, giám đốc thẩm hoặc tái thẩm vụ án đó, trừ trường hợp là thành viên của Hội đồng Thẩm phán Toà án nhân dân tối cao, Uỷ ban Thẩm phán Toà án nhân dân cấp tỉnh thì vẫn được tham gia xét xử nhiều lần cùng một vụ án theo thủ tục giám đốc thẩm, tái thẩm;

---
## q077 · xuyen_khoan · ngoai_le

Trạng thái: GIỮ
Câu hỏi: Nếu một doanh nghiệp chậm trả tiền cho một công ty cung cấp dịch vụ, thì công ty đó có được gia hạn thời gian trả tiền không, và nếu không trả kịp thời, có phải trả lãi không?

*Đáp án nháp của mô hình:* Có, doanh nghiệp có thể được gia hạn thời gian trả tiền theo yêu cầu của bên có quyền. Nếu sau thời hạn gia hạn vẫn không trả, doanh nghiệp phải thực hiện nghĩa vụ và bồi thường thiệt hại. Ngoài ra, do trường hợp chậm trả tiền, doanh nghiệp phải trả lãi theo lãi suất cơ bản do Ngân hàng Nhà nước công bố tại thời điểm thanh toán, trừ khi có thỏa thuận khác hoặc pháp luật có quy định khác.

**Sàng lọc:** câu hỏi mơ hồ — Cần cả hai khoản, nhưng câu hỏi gộp hai ý và nhầm chủ thể: bên có quyền mới là bên gia hạn, chứ không phải 'được gia hạn'. · Gợi ý câu hỏi: Khi bên có nghĩa vụ chậm trả một khoản tiền, bên có quyền có thể xử lý thế nào và bên chậm trả có phải trả thêm lãi không?

**Gold: 33/2005/QH11 Điều 305 khoản 1 — QUY TẮC**

> 1. Khi nghĩa vụ dân sự chậm được thực hiện thì bên có quyền có thể gia hạn để bên có nghĩa vụ hoàn thành nghĩa vụ; nếu quá thời hạn này mà nghĩa vụ vẫn chưa được hoàn thành thì theo yêu cầu của bên có quyền, bên có nghĩa vụ vẫn phải thực hiện nghĩa vụ và bồi thường thiệt hại; nếu việc thực hiện nghĩa vụ không còn cần thiết đối với bên có quyền thì bên này có quyền từ chối tiếp nhận việc thực hiện nghĩa vụ và yêu cầu bồi thường thiệt hại.

**Gold: 33/2005/QH11 Điều 305 khoản 2 — NGOẠI LỆ**

> 2. Trong trường hợp bên có nghĩa vụ chậm trả tiền thì bên đó phải trả lãi đối với số tiền chậm trả theo lãi suất cơ bản do Ngân hàng Nhà nước công bố tương ứng với thời gian chậm trả tại thời điểm thanh toán, trừ trường hợp có thoả thuận khác hoặc pháp luật có quy định khác.

*Câu ngoại lệ (dùng chấm 'trả lời thiếu'):* Trong trường hợp bên có nghĩa vụ chậm trả tiền thì bên đó phải trả lãi đối với số tiền chậm trả theo lãi suất cơ bản do Ngân hàng Nhà nước công bố tương ứng với thời gian chậm trả tại thời điểm thanh toán, trừ trường hợp có thoả thuận khác hoặc pháp luật có quy định khác.

---
## q078 · xuyen_khoan · ngoai_le

Trạng thái: GIỮ
Câu hỏi: Một người không có quyền ủy quyền thực hiện một công việc cho doanh nghiệp, họ có phải báo cáo cho người giao việc về kết quả nếu doanh nghiệp yêu cầu không?

*Đáp án nháp của mô hình:* Có, người đó có nghĩa vụ thực hiện công việc phù hợp với khả năng của mình và phải báo cáo cho người có công việc nếu bị yêu cầu, trừ trường hợp người có công việc đã biết hoặc người thực hiện không biết nơi cư trú của người đó.

**Sàng lọc:** không đúng ý đồ nhóm; câu hỏi mơ hồ — Câu chữ lủng củng ('không có quyền ủy quyền', 'người giao việc'); chỉ cần khoản 3 vì ngoại lệ nằm ngay trong khoản 3. · Gợi ý câu hỏi: Người tự ý làm một công việc thay cho người khác mà không được ủy quyền phải thực hiện công việc đó ra sao, và có phải báo cho chủ công việc về kết quả không?

**Gold: 33/2005/QH11 Điều 595 khoản 1 — QUY TẮC**

> 1. Người thực hiện công việc không có ủy quyền có nghĩa vụ thực hiện công việc phù hợp với khả năng, điều kiện của mình.

**Gold: 33/2005/QH11 Điều 595 khoản 3 — NGOẠI LỆ**

> 3. Người thực hiện công việc không có ủy quyền phải báo cho người có công việc được thực hiện về quá trình, kết quả thực hiện công việc nếu có yêu cầu, trừ trường hợp người có công việc đã biết hoặc người thực hiện công việc không có ủy quyền không biết nơi cư trú của người đó.

*Câu ngoại lệ (dùng chấm 'trả lời thiếu'):* Người thực hiện công việc không có ủy quyền phải báo cho người có công việc được thực hiện về quá trình, kết quả thực hiện công việc nếu có yêu cầu, trừ trường hợp người có công việc đã biết hoặc người thực hiện công việc không có ủy quyền không biết nơi cư trú của người đó.

---
## q079 · xuyen_khoan · ngoai_le

Trạng thái: GIỮ
Câu hỏi: Một người đang làm chứng trong một vụ án có được bào chữa cho người bị buộc tội không?

*Đáp án nháp của mô hình:* Không, người đang làm chứng trong vụ án không được bào chữa vì đây là trường hợp ngoại lệ theo quy định, dù họ có thể được bào chữa trong các trường hợp khác, nhưng khi tham gia vụ án với tư cách là người làm chứng thì không được.

**Sàng lọc:** không đúng ý đồ nhóm — Chỉ cần khoản 4 điểm b là trả lời được, không cần khoản 1 (định nghĩa người bào chữa); nên nói rõ là làm chứng trong chính vụ án đó. · Gợi ý câu hỏi: Bị can nhờ một người từng làm chứng trong chính vụ án của mình làm người bào chữa; cơ quan tố tụng có tiếp nhận đăng ký bào chữa của người này không?

**Gold: 101/2015/QH13 Điều 72 khoản 1 — QUY TẮC**

> 1. Người bào chữa là người được người bị buộc tội nhờ bào chữa hoặc cơ quan có thẩm quyền tiến hành tố tụng chỉ định và được cơ quan, người có thẩm quyền tiến hành tố tụng tiếp nhận việc đăng ký bào chữa.

**Gold: 101/2015/QH13 Điều 72 khoản 4 — NGOẠI LỆ**

> 4. Những người sau đây không được bào chữa:
> a) Người đã tiến hành tố tụng vụ án đó; người thân thích của người đã hoặc đang tiến hành tố tụng vụ án đó;
> b) Người tham gia vụ án đó với tư cách là người làm chứng, người giám định, người định giá tài sản, người phiên dịch, người dịch thuật;
> c) Người đang bị truy cứu trách nhiệm hình sự, người bị kết án mà chưa được xoá án tích, người đang bị áp dụng biện pháp xử lý hành chính đưa vào cơ sở cai nghiện bắt buộc, cơ sở giáo dục bắt buộc.

*Câu ngoại lệ (dùng chấm 'trả lời thiếu'):* Những người sau đây không được bào chữa:

---
## q224 · xuyen_khoan · ngoai_le · TRUNG LẬP

Trạng thái: GIỮ
Câu hỏi: Nếu một người đang sử dụng đất và trồng cây trong khuôn viên đất của mình, nhưng rễ cây vượt quá ranh giới, thì có được để nguyên không?

*Đáp án nháp của mô hình:* Có được để nguyên nếu rễ và cành cây vượt quá ranh giới không gây tranh chấp và đã tồn tại từ ba mươi năm trở lên theo tập quán hoặc ranh giới đã xác lập; nếu không, phải xén rễ, tỉa cành phần vượt quá, trừ khi có thỏa thuận khác giữa các bên.

**Sàng lọc:** không đúng ý đồ nhóm; lộ đáp án / nhắc văn bản — Chỉ cần đoạn ngoại lệ (phải xén rễ, tỉa cành, trừ khi có thỏa thuận khác) là trả lời được; đoạn quy tắc về ranh giới theo tập quán/30 năm không cần dùng. Đáp án nháp còn ghép hai đoạn sai (cho để nguyên nếu đã tồn tại 30 năm). Câu hỏi chép khá sát lời văn đoạn ngoại lệ. · Gợi ý câu hỏi: Hai nhà có ranh giới đất xác định theo tập quán, đã tồn tại hơn ba mươi năm mà không ai tranh chấp; nếu rễ và cành cây của nhà này lan sang phía nhà kia thì chủ cây có buộc phải cắt bỏ phần lấn sang không?

**Gold: 33/2005/QH11 Điều 265 khoản 1 — QUY TẮC**

> Ranh giới cũng có thể được xác định theo tập quán hoặc theo ranh giới đã tồn tại từ ba mươi năm trở lên mà không có tranh chấp.

**Gold: 33/2005/QH11 Điều 265 khoản 2 — NGOẠI LỆ**

> Người sử dụng đất chỉ được trồng cây và làm các việc khác trong khuôn viên đất thuộc quyền sử dụng của mình và theo ranh giới đã được xác định; nếu rễ cây, cành cây vượt quá ranh giới thì phải xén rễ, tỉa cành phần vượt quá, trừ trường hợp có thoả thuận khác.

*Câu ngoại lệ (dùng chấm 'trả lời thiếu'):* Người sử dụng đất chỉ được trồng cây và làm các việc khác trong khuôn viên đất thuộc quyền sử dụng của mình và theo ranh giới đã được xác định; nếu rễ cây, cành cây vượt quá ranh giới thì phải xén rễ, tỉa cành phần vượt quá, trừ trường hợp có thoả thuận khác.

---
## q225 · xuyen_khoan · ngoai_le · TRUNG LẬP

Trạng thái: GIỮ
Câu hỏi: Khi cấp trưởng vắng mặt, cấp phó có được ủy quyền cho một cán bộ điều tra thực hiện nhiệm vụ của cấp trưởng không?

*Đáp án nháp của mô hình:* Cấp phó có thể ủy quyền cho cấp phó thực hiện nhiệm vụ của cấp trưởng khi cấp trưởng vắng mặt, nhưng không được ủy quyền cho cán bộ điều tra thực hiện nhiệm vụ đó.

**Cờ tự động:** trùng từ cao (92%)
**Sàng lọc:** câu hỏi mơ hồ — Không nói cấp trưởng/cấp phó của cơ quan nào nên dễ lẫn với quy định tương tự ở cơ quan khác (vd. Viện kiểm sát, câu q226); đáp án nháp viết lẫn 'cấp phó ủy quyền cho cấp phó'. · Gợi ý câu hỏi: Ở cơ quan được giao tiến hành một số hoạt động điều tra, khi cấp trưởng vắng mặt và một cấp phó được ủy quyền thay, cấp phó đó có thể giao lại nhiệm vụ cho cán bộ điều tra thực hiện không?

**Gold: 101/2015/QH13 Điều 40 khoản 1 điểm d — QUY TẮC**

> Khi cấp trưởng vắng mặt, một cấp phó được ủy quyền thực hiện nhiệm vụ, quyền hạn của cấp trưởng và chịu trách nhiệm trước cấp trưởng về nhiệm vụ được ủy quyền.

**Gold: 101/2015/QH13 Điều 40 khoản 4 — NGOẠI LỆ**

> Cấp trưởng, cấp phó không được ủy quyền cho cán bộ điều tra thực hiện nhiệm vụ, quyền hạn của mình.

*Câu ngoại lệ (dùng chấm 'trả lời thiếu'):* Cấp trưởng, cấp phó không được ủy quyền cho cán bộ điều tra thực hiện nhiệm vụ, quyền hạn của mình.

---
## q226 · xuyen_khoan · ngoai_le · TRUNG LẬP

Trạng thái: GIỮ
Câu hỏi: Nếu một Phó Viện trưởng Viện kiểm sát được ủy quyền thay thế Viện trưởng, thì có được ủy quyền cho một Kiểm sát viên thực hiện nhiệm vụ của Viện trưởng không?

*Đáp án nháp của mô hình:* Không, vì theo quy định, Phó Viện trưởng có thể được ủy quyền thay thế Viện trưởng, nhưng Viện trưởng và Phó Viện trưởng không được ủy quyền cho Kiểm sát viên thực hiện nhiệm vụ hoặc quyền hạn của mình.

**Sàng lọc:** không thấy vấn đề

**Gold: 101/2015/QH13 Điều 41 khoản 1 điểm đ — QUY TẮC**

> Khi vắng mặt, Viện trưởng Viện kiểm sát ủy quyền cho một Phó Viện trưởng Viện kiểm sát thực hiện nhiệm vụ, quyền hạn của Viện trưởng và chịu trách nhiệm trước Viện trưởng Viện kiểm sát về nhiệm vụ được ủy quyền.

**Gold: 101/2015/QH13 Điều 41 khoản 4 — NGOẠI LỆ**

> Viện trưởng, Phó Viện trưởng Viện kiểm sát không được ủy quyền cho Kiểm sát viên thực hiện nhiệm vụ, quyền hạn của mình.

*Câu ngoại lệ (dùng chấm 'trả lời thiếu'):* Viện trưởng, Phó Viện trưởng Viện kiểm sát không được ủy quyền cho Kiểm sát viên thực hiện nhiệm vụ, quyền hạn của mình.

---
## q227 · xuyen_khoan · ngoai_le · TRUNG LẬP

Trạng thái: GIỮ
Câu hỏi: Nếu một bên mua không trả lời trong thời gian dùng thử, thì có được coi là đã đồng ý mua sản phẩm không, và bên dùng thử có phải chịu trách nhiệm về những hao mòn thông thường hay không?

*Đáp án nháp của mô hình:* Có, nếu bên mua không trả lời trong thời hạn dùng thử thì sẽ được coi là đã chấp nhận mua theo các điều kiện đã thỏa thuận. Đồng thời, bên dùng thử không phải chịu trách nhiệm về những hao mòn thông thường do việc dùng thử gây ra.

**Sàng lọc:** câu hỏi mơ hồ — Ghép hai câu hỏi độc lập (im lặng có được coi là đồng ý mua không / có chịu hao mòn không); hai đoạn gold không thật sự có quan hệ quy tắc–ngoại lệ. · Gợi ý câu hỏi: Một người nhận máy về dùng thử, trong thời hạn dùng thử báo không mua và trả lại máy đã hơi cũ đi do sử dụng; người bán có được đòi bồi thường phần hao mòn đó không?

**Gold: 33/2005/QH11 Điều 460 khoản 1 — QUY TẮC**

> Trong thời hạn dùng thử, bên mua có thể trả lời mua hoặc không mua; nếu hết thời hạn dùng thử mà bên mua không trả lời thì coi như đã chấp nhận mua theo các điều kiện đã thoả thuận trước khi nhận vật dùng thử.

**Gold: 33/2005/QH11 Điều 460 khoản 3 — NGOẠI LỆ**

> Bên dùng thử không phải chịu trách nhiệm về những hao mòn thông thường do việc dùng thử gây ra và không phải hoàn trả hoa lợi do việc dùng thử mang lại.

*Câu ngoại lệ (dùng chấm 'trả lời thiếu'):* Bên dùng thử không phải chịu trách nhiệm về những hao mòn thông thường do việc dùng thử gây ra và không phải hoàn trả hoa lợi do việc dùng thử mang lại.

---
## q228 · xuyen_khoan · ngoai_le · TRUNG LẬP

Trạng thái: GIỮ
Câu hỏi: Trong trường hợp hợp đồng xây dựng bị chấm dứt do đơn phương, thì bên giao thầu có được thanh toán cho bên nhận thầu không, nếu hai bên chưa có thỏa thuận về thời gian và điều kiện thanh toán?

*Đáp án nháp của mô hình:* Có được thanh toán nếu hợp đồng bị đơn phương chấm dứt, nhưng chỉ thực hiện theo thỏa thuận giữa hai bên về thời gian, phương thức và điều kiện thanh toán; nếu không có thỏa thuận, bên giao thầu phải thanh toán đủ giá trị đúng thời hạn sau khi đã trừ tiền tạm ứng và các khoản tiền giữ lại theo hợp đồng.

**Sàng lọc:** KHÔNG trả lời được từ gold; không đúng ý đồ nhóm — Gold nói 'đơn phương quyết toán, thanh lý', không nói chấm dứt hợp đồng, và không quy định trường hợp chưa có thỏa thuận thanh toán; 'bên giao thầu có được thanh toán' sai chiều; đoạn quy tắc và ngoại lệ liên quan lỏng lẻo; đáp án nháp suy diễn sai. · Gợi ý câu hỏi: Khi hợp đồng xây dựng được một bên đơn phương quyết toán, thanh lý, bên giao thầu có phải thanh toán đủ và đúng hạn cho bên nhận thầu theo thỏa thuận trong hợp đồng, sau khi trừ tiền tạm ứng, không?

**Gold: 135/2025/QH15 Điều 87 khoản 1 — QUY TẮC**

> Việc quyết toán, thanh lý hợp đồng xây dựng bao gồm cả các trường hợp được đơn phương quyết toán, thanh lý hợp đồng xây dựng.

**Gold: 135/2025/QH15 Điều 87 khoản 2 điểm a — NGOẠI LỆ**

> Các bên thỏa thuận về phương thức, thời gian, hồ sơ và điều kiện thanh toán hoặc tạm thanh toán;
> b) Bên giao thầu phải thanh toán đủ giá trị và đúng thời hạn theo các thỏa thuận trong hợp đồng xây dựng của từng lần thanh toán cho bên nhận thầu sau khi đã giảm trừ tiền tạm ứng, các khoản tiền giữ lại theo thỏa thuận hợp đồng xây dựng, trừ trường hợp các bên có thỏa thuận khác;

*Câu ngoại lệ (dùng chấm 'trả lời thiếu'):* Các bên thỏa thuận về phương thức, thời gian, hồ sơ và điều kiện thanh toán hoặc tạm thanh toán;
b) Bên giao thầu phải thanh toán đủ giá trị và đúng thời hạn theo các thỏa thuận trong hợp đồng xây dựng của từng lần thanh toán cho bên nhận thầu sau khi đã giảm trừ tiền tạm ứng, các khoản tiền giữ lại theo thỏa thuận hợp đồng xây dựng, trừ trường hợp các bên có thỏa thuận khác;

---
## q229 · xuyen_khoan · ngoai_le · TRUNG LẬP

Trạng thái: DỰ PHÒNG
Câu hỏi: Khi thực hiện thanh toán bằng ngoại tệ trong quá trình thi hành án dân sự, có được sử dụng tỷ giá hạch toán để tính toán thu chi và làm căn cứ bán đấu giá không?

*Đáp án nháp của mô hình:* Có thể ghi sổ theo nguyên tệ và quy đổi ra đồng Việt Nam theo tỷ giá hạch toán thực tế tại ngày ghi sổ, nhưng tỷ giá hạch toán không được dùng làm căn cứ bán đấu giá, thu phí hoặc thanh toán bằng tiền thay thế như ngoại tệ, vàng, bạc, đồ cổ, kim khí quý, đá quý.

**⚠ Kiểm tra tự động:** hai gold không phải quan hệ quy tắc–ngoại lệ (Đoạn B nêu rõ giá hạch toán không được sử dụng cho các mục đích khác, tức là giới hạn việc sử dụng giá hạch toán như trong đoạn A, do đó đây là một ngoại lệ hoặc giới hạn đối với việc áp dụng quy tắc ở đoạn A, nên không phải là quy định song song hoặc độc lập.)
**Sàng lọc:** không thấy vấn đề — Đoạn ngoại lệ nói 'giá hạch toán' còn câu hỏi nói 'tỷ giá hạch toán'; cần kiểm tra hai cụm này có cùng nghĩa không.

**Gold: 107/2026/TT-BTC Điều 4 khoản 1 — QUY TẮC**

> Trường hợp thu - chi bằng ngoại tệ phải ghi sổ theo nguyên tệ và quy đổi ra đồng Việt Nam theo tỷ giá hạch toán thực tế tại ngày ghi sổ.

**Gold: 107/2026/TT-BTC Điều 4 khoản 5 — NGOẠI LỆ**

> Giá hạch toán không được sử dụng cho các mục đích khác như làm căn cứ bán đấu giá; trao đổi; thu phí; thanh toán bằng tiền thay ngoại tệ, vàng, bạc, đồ cổ, kim khí quý, đá quý,...

*Câu ngoại lệ (dùng chấm 'trả lời thiếu'):* Giá hạch toán không được sử dụng cho các mục đích khác như làm căn cứ bán đấu giá; trao đổi; thu phí; thanh toán bằng tiền thay ngoại tệ, vàng, bạc, đồ cổ, kim khí quý, đá quý,...

---
## q230 · xuyen_khoan · ngoai_le · TRUNG LẬP

Trạng thái: DỰ PHÒNG
Câu hỏi: Công ty có thể miễn nhiệm thành viên Hội đồng thành viên trong một nhiệm kỳ dài hơn 5 năm không, nếu có quy định trong Điều lệ công ty?

*Đáp án nháp của mô hình:* Không, thành viên Hội đồng thành viên chỉ được bổ nhiệm hoặc miễn nhiệm với nhiệm kỳ không quá 5 năm, trừ khi Điều lệ công ty có quy định khác.

**⚠ Kiểm tra tự động:** hai gold không phải quan hệ quy tắc–ngoại lệ (Đoạn B không nêu rõ ngoại lệ, giới hạn hoặc trường hợp loại trừ áp dụng cho quy định ở đoạn A, nên không thể kết luận rằng việc áp dụng đúng quy định đoạn A đòi hỏi phải biết đoạn B.)
**Sàng lọc:** chỉ trả lời được một phần từ gold; không đúng ý đồ nhóm; câu hỏi mơ hồ; gold đáng ngờ — Đoạn ngoại lệ (Điều lệ quy định khác về thời điểm nghị quyết có hiệu lực) không liên quan đến quy tắc nhiệm kỳ 05 năm, nên câu hỏi vô lý và đáp án nháp áp ngoại lệ sai chỗ; cũng không nói rõ loại công ty có chủ sở hữu bổ nhiệm thành viên Hội đồng thành viên. · Gợi ý câu hỏi: Trong công ty mà thành viên Hội đồng thành viên do chủ sở hữu bổ nhiệm, nhiệm kỳ tối đa của thành viên là bao lâu, và Điều lệ công ty có thể quy định khác về thời điểm nghị quyết của Hội đồng thành viên có hiệu lực không?

**Gold: 59/2020/QH14 Điều 80 khoản 1 — QUY TẮC**

> Thành viên Hội đồng thành viên do chủ sở hữu công ty bổ nhiệm, miễn nhiệm với nhiệm kỳ không quá 05 năm.

**Gold: 59/2020/QH14 Điều 80 khoản 6 — NGOẠI LỆ**

> Nghị quyết, quyết định của Hội đồng thành viên có hiệu lực kể từ ngày được thông qua hoặc từ ngày ghi tại nghị quyết, quyết định đó, trừ trường hợp Điều lệ công ty có quy định khác.

*Câu ngoại lệ (dùng chấm 'trả lời thiếu'):* Nghị quyết, quyết định của Hội đồng thành viên có hiệu lực kể từ ngày được thông qua hoặc từ ngày ghi tại nghị quyết, quyết định đó, trừ trường hợp Điều lệ công ty có quy định khác.

---
## q231 · xuyen_khoan · ngoai_le · TRUNG LẬP

Trạng thái: DỰ PHÒNG
Câu hỏi: Một trường chuyên biệt muốn chuyển địa điểm hoạt động có được không, nếu cơ quan có thẩm quyền đã có thông tin về cơ sở vật chất trong cơ sở dữ liệu quốc gia?

*Đáp án nháp của mô hình:* Có được, nhưng chỉ được chuyển địa điểm nếu đáp ứng điều kiện về cơ sở vật chất theo quy định; nếu cơ quan có thẩm quyền có thể khai thác thông tin về cơ sở vật chất từ cơ sở dữ liệu quốc gia thì không cần nộp bản sao hồ sơ.

**⚠ Kiểm tra tự động:** hai gold không phải quan hệ quy tắc–ngoại lệ (Đoạn B không đề cập đến điều kiện hoặc ngoại lệ nào liên quan đến việc thay đổi địa điểm hoạt động giáo dục như trong đoạn A, nên không có mối liên hệ hay giới hạn nào giữa hai đoạn về việc áp dụng quy tắc ở đoạn A)
**Sàng lọc:** không thấy vấn đề — Câu hỏi 'có được không' lẫn lộn hai việc: dữ liệu quốc gia chỉ miễn nộp bản sao hồ sơ, không miễn điều kiện cơ sở vật chất. · Gợi ý câu hỏi: Khi trường chuyên biệt xin thay đổi địa điểm hoạt động giáo dục mà thông tin cơ sở vật chất đã có sẵn trong cơ sở dữ liệu quốc gia, trường có còn phải đáp ứng điều kiện về cơ sở vật chất và nộp bản sao giấy tờ không?

**Gold: 360/2026/NĐ-CP Điều 6 khoản 1 điểm a — QUY TẮC**

> Đối với trường chuyên biệt, việc thay đổi địa điểm hoạt động giáo dục còn phải đáp ứng điều kiện về cơ sở vật chất để được cấp phép hoạt động giáo dục quy định tại Nghị định này;

**Gold: 360/2026/NĐ-CP Điều 6 khoản 2 điểm b — NGOẠI LỆ**

> Nhà trường không phải nộp bản sao các thành phần hồ sơ nếu cơ quan có thẩm quyền có thể khai thác, sử dụng thông tin tương ứng trong cơ sở dữ liệu quốc gia, cơ sở dữ liệu chuyên ngành hoặc đã được số hóa theo quy định.

*Câu ngoại lệ (dùng chấm 'trả lời thiếu'):* Nhà trường không phải nộp bản sao các thành phần hồ sơ nếu cơ quan có thẩm quyền có thể khai thác, sử dụng thông tin tương ứng trong cơ sở dữ liệu quốc gia, cơ sở dữ liệu chuyên ngành hoặc đã được số hóa theo quy định.

---
## q232 · xuyen_khoan · ngoai_le · TRUNG LẬP

Trạng thái: GIỮ
Câu hỏi: Nếu một cuộc họp Hội đồng quản trị của công ty không đủ số thành viên dự họp theo quy định, thì có thể triệu tập thêm lần thứ hai không, và nếu có, điều kiện nào phải thỏa mãn?

*Đáp án nháp của mô hình:* Có thể triệu tập thêm lần thứ hai nếu cuộc họp ban đầu không đủ số thành viên dự họp, nhưng chỉ được làm trong thời hạn 07 ngày kể từ ngày dự định họp lần đầu, trừ trường hợp Điều lệ công ty quy định thời hạn khác ngắn hơn. Trong trường hợp có nhiều thành viên có số phiếu bầu hoặc tỷ lệ phiếu bầu cao nhất và ngang nhau, thì các thành viên sẽ bầu theo nguyên tắc đa số để chọn một người triệu tập họp.

**Sàng lọc:** không đúng ý đồ nhóm — Chỉ cần đoạn ngoại lệ (triệu tập lần hai trong 07 ngày) là trả lời được; đoạn quy tắc về người triệu tập cuộc họp sau bầu cử không liên quan, đáp án nháp ghép vào gượng ép. · Gợi ý câu hỏi: Sau khi bầu Hội đồng quản trị mà có hai thành viên cùng đạt số phiếu cao nhất thì ai triệu tập cuộc họp, và nếu cuộc họp không đủ số thành viên dự thì được triệu tập lại trong thời hạn nào?

**Gold: 59/2020/QH14 Điều 157 khoản 1 — QUY TẮC**

> Cuộc họp này do thành viên có số phiếu bầu cao nhất hoặc tỷ lệ phiếu bầu cao nhất triệu tập và chủ trì. Trường hợp có nhiều hơn một thành viên có số phiếu bầu hoặc tỷ lệ phiếu bầu cao nhất và ngang nhau thì các thành viên bầu theo nguyên tắc đa số để chọn 01 người trong số họ triệu tập họp Hội đồng quản trị.

**Gold: 59/2020/QH14 Điều 157 khoản 8 — NGOẠI LỆ**

> Trường hợp cuộc họp được triệu tập theo quy định tại khoản này không đủ số thành viên dự họp theo quy định thì được triệu tập lần thứ hai trong thời hạn 07 ngày kể từ ngày dự định họp lần thứ nhất, trừ trường hợp Điều lệ công ty quy định thời hạn khác ngắn hơn.

*Câu ngoại lệ (dùng chấm 'trả lời thiếu'):* Trường hợp cuộc họp được triệu tập theo quy định tại khoản này không đủ số thành viên dự họp theo quy định thì được triệu tập lần thứ hai trong thời hạn 07 ngày kể từ ngày dự định họp lần thứ nhất, trừ trường hợp Điều lệ công ty quy định thời hạn khác ngắn hơn.

---
## q234 · xuyen_khoan · ngoai_le · TRUNG LẬP

Trạng thái: DỰ PHÒNG
Câu hỏi: Một đơn vị đề xuất hỗ trợ chi phí xây dựng chính sách nhưng không áp dụng phương thức khoán chi thì cần làm gì để đảm bảo yêu cầu về dự toán?

*Đáp án nháp của mô hình:* Đơn vị phải nộp văn bản, tài liệu quy định rõ khối lượng dự kiến, đơn giá, chi phí thực tế thị trường và căn cứ lập dự toán, đồng thời thực hiện đầy đủ các bước theo quy định về hỗ trợ, tài trợ trong trường hợp không áp dụng phương thức khoán chi.

**⚠ Kiểm tra tự động:** hai gold không phải quan hệ quy tắc–ngoại lệ (Đoạn B không nêu rõ ngoại lệ, giới hạn hoặc trường hợp loại trừ nào đối với đoạn A, nên không thể coi là ngoại lệ của đoạn A.)
**Sàng lọc:** không đúng ý đồ nhóm — Chỉ cần đoạn ngoại lệ về yêu cầu dự toán là trả lời được; đoạn quy tắc (đề xuất bổ sung kinh phí phải nộp tài liệu) không được dùng. · Gợi ý câu hỏi: Khi đề xuất Quỹ bổ sung kinh phí cho một nội dung chi không áp dụng phương thức khoán chi, chủ thể đề xuất phải nộp gì và dự toán phải thể hiện những thông tin nào?

**Gold: 10/2026/TT-BTP Điều 12 khoản 1 — QUY TẮC**

> Trường hợp đề xuất hỗ trợ, tài trợ đối với nội dung chi cần bổ sung kinh phí, chủ thể đề xuất hỗ trợ, tài trợ nộp cho Quỹ văn bản, tài liệu quy định tại khoản 2 Điều 11 của Thông tư này.

**Gold: 10/2026/TT-BTP Điều 12 khoản 2 — NGOẠI LỆ**

> Đối với các nội dung không áp dụng phương thức khoán chi theo quy định tại Thông tư này, dự toán phải thể hiện rõ khối lượng dự kiến, đơn giá, chi phí thực tế thị trường và căn cứ lập dự toán.

*Câu ngoại lệ (dùng chấm 'trả lời thiếu'):* Đối với các nội dung không áp dụng phương thức khoán chi theo quy định tại Thông tư này, dự toán phải thể hiện rõ khối lượng dự kiến, đơn giá, chi phí thực tế thị trường và căn cứ lập dự toán.

---
## q258 · xuyen_khoan · ngoai_le · TRUNG LẬP

Trạng thái: DỰ PHÒNG
Câu hỏi: Trong trường hợp cần tạm giam để phục hồi điều tra, thì việc trả hồ sơ để điều tra bổ sung có được thực hiện nhiều lần không?

*Đáp án nháp của mô hình:* Không, thẩm phán chủ tọa và Hội đồng xét xử chỉ được trả hồ sơ để điều tra bổ sung một lần theo quy định chung. Tuy nhiên, nếu có căn cứ cần tạm giam để phục hồi điều tra, thì thời hạn tạm giam không được vượt quá thời hạn quy định, và việc trả hồ sơ để điều tra bổ sung vẫn chỉ được thực hiện một lần, nhưng trong trường hợp này, thời hạn tạm giam sẽ được tính theo quy định riêng về phục hồi điều tra.

**Cờ tự động:** trùng từ cao (89%)
**Sàng lọc:** chỉ trả lời được một phần từ gold; không đúng ý đồ nhóm; câu hỏi mơ hồ — Đoạn ngoại lệ (khoản 4) chỉ giới hạn thời hạn tạm giam, không phải ngoại lệ của quy tắc 'chỉ trả hồ sơ một lần'. Vì vậy câu hỏi chỉ cần khoản 2 và tiền đề gắn tạm giam với số lần trả hồ sơ là sai. Câu hỏi cũng không nói ai trả hồ sơ: Viện kiểm sát được trả hai lần nhưng ý này nằm ngoài gold. Đáp án nháp lẫn lộn. · Gợi ý câu hỏi: Nếu cần tạm giam bị can trong thời gian điều tra bổ sung thì thời hạn tạm giam tối đa được giới hạn đến đâu và tính từ mốc nào?

**Gold: 101/2015/QH13 Điều 174 khoản 2 — QUY TẮC**

> Thẩm phán chủ tọa phiên tòa chỉ được trả hồ sơ để điều tra bổ sung một lần và Hội đồng xét xử chỉ được trả hồ sơ để điều tra bổ sung một lần.
> Thời hạn điều tra bổ sung tính từ ngày Cơ quan điều tra nhận lại hồ sơ vụ án và yêu cầu điều tra bổ sung.

**Gold: 101/2015/QH13 Điều 174 khoản 4 — NGOẠI LỆ**

> Trường hợp có căn cứ theo quy định của Bộ luật này cần phải tạm giam thì thời hạn tạm giam để phục hồi điều tra, điều tra bổ sung không được quá thời hạn phục hồi điều tra, điều tra bổ sung quy định tại khoản 1 và khoản 2 Điều này.
> Thời hạn tạm giam và gia hạn tạm giam trong trường hợp vụ án được điều tra lại thực hiện theo quy định tại Điều 173 của Bộ luật này.

*Câu ngoại lệ (dùng chấm 'trả lời thiếu'):* Trường hợp có căn cứ theo quy định của Bộ luật này cần phải tạm giam thì thời hạn tạm giam để phục hồi điều tra, điều tra bổ sung không được quá thời hạn phục hồi điều tra, điều tra bổ sung quy định tại khoản 1 và khoản 2 Điều này.
Thời hạn tạm giam và gia hạn tạm giam trong trường hợp vụ án được điều tra lại thực hiện theo quy định tại Điều 173 của Bộ luật này.

---
## q089 · dan_chieu · dan_chieu

Trạng thái: DỰ PHÒNG
Câu hỏi: Nếu một người vô ý làm lộ bí mật công tác hoặc làm mất tài liệu bí mật công tác và gây hậu quả nghiêm trọng, thì sẽ bị xử phạt như thế nào?

*Đáp án nháp của mô hình:* Bị phạt cảnh cáo, cải tạo không giam giữ đến hai năm hoặc phạt tù từ ba tháng đến hai năm; nếu gây hậu quả rất nghiêm trọng hoặc đặc biệt nghiêm trọng thì mức phạt có thể cao hơn, nhưng cụ thể phải căn cứ vào quy định về tội làm lộ bí mật nhà nước hoặc làm mất tài liệu bí mật nhà nước.

**⚠ Bản cũ:** gold ở BẢN CŨ, bản mới cũng có trong kho — 15/1999/QH10 Điều 287 ↔ 100/2015/QH13 Điều 362: KHÁC ÍT (chứa 0.61); 15/1999/QH10 Điều 264 ↔ 100/2015/QH13 Điều 338: KHÁC ÍT (chứa 0.64)
**⚠ Kiểm tra tự động:** trả lời được chỉ bằng đoạn nguồn (Đoạn nguồn nêu rõ rằng người vô ý làm lộ bí mật công tác hoặc làm mất tài liệu bí mật công tác gây hậu quả nghiêm trọng, rất nghiêm trọng hoặc đặc biệt nghiêm trọng sẽ bị phạt cảnh cáo, cải tạo không giam giữ đến hai năm hoặc phạt tù từ ba tháng đến hai năm, nên trả lời đầy đủ và cụ thể theo nội dung đoạn nguồn.)
**Sàng lọc:** không đúng ý đồ nhóm; lộ đáp án / nhắc văn bản — Câu hỏi về bí mật công tác trả lời trọn bằng đoạn nguồn, không cần đọc điều về bí mật nhà nước; câu hỏi chép gần nguyên văn đoạn nguồn. · Gợi ý câu hỏi: Một cán bộ vô ý làm mất tài liệu mật, gây hậu quả nghiêm trọng; mức hình phạt khác nhau thế nào tùy tài liệu đó là bí mật công tác hay bí mật nhà nước?

**Gold: 15/1999/QH10 Điều 287 khoản 1 — NGUỒN**

> 1. Người nào vô ý làm lộ bí mật công tác hoặc làm mất tài liệu bí mật công tác gây hậu quả nghiêm trọng, rất nghiêm trọng hoặc đặc biệt nghiêm trọng, nếu không thuộc trường hợp quy định tại Điều 264 của Bộ luật này, thì bị phạt cảnh cáo, cải tạo không giam giữ đến hai năm hoặc phạt tù từ ba tháng đến hai năm.

**Gold: 15/1999/QH10 Điều 264 — ĐÍCH**

> Điều 264. Tội vô ý làm lộ bí mật nhà nước, tội làm mất tài liệu bí mật nhà nước
> 1. Người nào vô ý làm lộ bí mật nhà nước hoặc làm mất tài liệu bí mật nhà nước, thì bị phạt cải tạo không giam giữ đến ba năm hoặc phạt tù từ sáu tháng đến ba năm.
> 2. Phạm tội gây hậu quả nghiêm trọng thì bị phạt tù từ hai năm đến bảy năm.
> 3. Người phạm tội còn có thể bị cấm đảm nhiệm chức vụ, cấm hành nghề hoặc làm công việc nhất định từ một năm đến năm năm.

---
## q090 · dan_chieu · dan_chieu

Trạng thái: GIỮ
Câu hỏi: Khi đình chỉ vụ án, cần ghi rõ những nội dung gì để đảm bảo tính minh bạch và đúng quy định?

*Đáp án nháp của mô hình:* Cần ghi rõ lý do và căn cứ đình chỉ vụ án, việc hủy bỏ biện pháp ngăn chặn hoặc cưỡng chế, xử lý vật chứng và tài liệu đã tạm giữ, cũng như các vấn đề liên quan khác. Nếu vụ án có nhiều bị can và lý do đình chỉ không liên quan đến tất cả, thì cần đình chỉ đối với từng bị can.

**⚠ Kiểm tra tự động:** trả lời được chỉ bằng đoạn nguồn (Đoạn nguồn nêu rõ rằng quyết định đình chỉ vụ án phải ghi rõ lý do và căn cứ đình chỉ vụ án, việc hủy bỏ biện pháp ngăn chặn, biện pháp cưỡng chế, xử lý vật chứng, tài liệu, đồ vật đã tạm giữ (nếu có), các vấn đề khác có liên quan và các nội dung quy định tại khoản 2 Điều 132 Bộ luật. Do đó, nội dung cần ghi rõ được nêu cụ thể trong đoạn nguồn, không chỉ nhắc đến điều luật mà đã nêu rõ các nội dung cụ thể.)
**Sàng lọc:** câu hỏi mơ hồ — Cần cả nguồn và đích nên đúng nhóm; nên nói rõ là vụ án hình sự vì tố tụng dân sự cũng có đình chỉ; đáp án nháp thiếu phần nội dung ở đoạn đích. · Gợi ý câu hỏi: Quyết định đình chỉ vụ án hình sự phải ghi rõ những nội dung gì?

**Gold: 101/2015/QH13 Điều 248 khoản 2 — NGUỒN**

> 2. Quyết định đình chỉ vụ án phải ghi rõ lý do và căn cứ đình chỉ vụ án, việc hủy bỏ biện pháp ngăn chặn, biện pháp cưỡng chế, xử lý vật chứng, tài liệu, đồ vật đã tạm giữ (nếu có), các vấn đề khác có liên quan và các nội dung quy định tại khoản 2 Điều 132 của Bộ luật này. Trường hợp vụ án có nhiều bị can mà căn cứ đình chỉ vụ án không liên quan đến tất cả các bị can thì quyết định đình chỉ vụ án đối với từng bị can.

**Gold: 101/2015/QH13 Điều 132 khoản 2 — ĐÍCH**

> 2. Văn bản tố tụng ghi rõ:
> a) Số, ngày, tháng, năm, địa điểm ban hành văn bản tố tụng;
> b) Căn cứ ban hành văn bản tố tụng;
> c) Nội dung của văn bản tố tụng;
> d) Họ tên, chức vụ, chữ ký của người ban hành văn bản tố tụng và đóng dấu.

---
## q091 · dan_chieu · dan_chieu

Trạng thái: XOÁ
Câu hỏi: Nếu một hợp đồng lao động bị tuyên bố vô hiệu toàn bộ do việc ký kết sai thẩm quyền, thì người lao động sẽ được xử lý như thế nào?

*Đáp án nháp của mô hình:* Cơ quan quản lý nhà nước về lao động sẽ hướng dẫn các bên ký lại hợp đồng lao động, đồng thời quyền và nghĩa vụ của người lao động sẽ được giải quyết theo quy định của pháp luật.

**Cờ tự động:** trùng từ cao (87%)
**⚠ Bản cũ:** gold ở BẢN CŨ, bản mới cũng có trong kho — 10/2012/QH13 Điều 52 ↔ 45/2019/QH14 Điều 51: KHÁC NHIỀU hoặc không còn (chứa 0.54); 10/2012/QH13 Điều 50 ↔ 45/2019/QH14 Điều 49 khoản 1: KHÁC NHIỀU hoặc không còn (chứa 0.44)
**Sàng lọc:** không đúng ý đồ nhóm; lộ đáp án / nhắc văn bản — Câu hỏi đã nêu sẵn 'ký sai thẩm quyền' nên chỉ cần đoạn nguồn, không cần danh sách ở đoạn đích; câu chữ chép gần nguyên văn. · Gợi ý câu hỏi: Hợp đồng lao động do một người không có thẩm quyền đại diện bên sử dụng lao động ký thì có hiệu lực không, và được xử lý thế nào?

**Gold: 10/2012/QH13 Điều 52 khoản 2 — NGUỒN**

> 2. Khi hợp đồng lao động bị tuyên bố vô hiệu toàn bộ thì xử lý như sau:
> a) Trong trường hợp do ký sai thẩm quyền quy định tại điểm b khoản 1 Điều 50 của Bộ luật này thì cơ quan quản lý nhà nước về lao động hướng dẫn các bên ký lại;
> b) Quyền, nghĩa vụ và lợi ích của người lao động được giải quyết theo quy định của pháp luật.

**Gold: 10/2012/QH13 Điều 50 khoản 1 — ĐÍCH**

> 1. Hợp đồng lao động vô hiệu toàn bộ khi thuộc một trong các trường hợp sau đây:
> a) Toàn bộ nội dung của hợp đồng lao động trái pháp luật;
> b) Người ký kết hợp đồng lao động không đúng thẩm quyền;
> c) Công việc mà hai bên đã giao kết trong hợp đồng lao động là công việc bị pháp luật cấm;
> d) Nội dung của hợp đồng lao động hạn chế hoặc ngăn cản quyền thành lập, gia nhập và hoạt động công đoàn của người lao động.

---
## q092 · dan_chieu · dan_chieu

Trạng thái: DỰ PHÒNG
Câu hỏi: Nếu một doanh nghiệp vi phạm pháp luật và bị xử phạt, thì điều kiện nào để bị đình chỉ hoạt động vĩnh viễn?

*Đáp án nháp của mô hình:* Khi doanh nghiệp phạm tội gây thiệt hại hoặc có khả năng gây thiệt hại đến tính mạng của nhiều người, gây sự cố môi trường hoặc ảnh hưởng xấu đến an ninh, trật tự, an toàn xã hội và không có khả năng khắc phục hậu quả, thì sẽ bị đình chỉ hoạt động vĩnh viễn.

**⚠ Kiểm tra tự động:** trả lời được chỉ bằng đoạn nguồn (Đoạn nguồn nêu rõ rằng pháp nhân thương mại phạm tội thuộc trường hợp quy định tại Điều 79 của Bộ luật này thì bị đình chỉ hoạt động vĩnh viễn, do đó điều kiện để bị đình chỉ hoạt động vĩnh viễn là phạm tội thuộc trường hợp quy định tại Điều 79 của Bộ luật.)
**Sàng lọc:** không đúng ý đồ nhóm; câu hỏi mơ hồ — Câu hỏi chung chung (lẫn xử phạt hành chính với hình sự), chỉ cần đoạn đích và không xuất phát từ tội cụ thể ở đoạn nguồn (gold không nêu tên tội); đáp án nháp bỏ sót khoản 2 Điều 79. · Gợi ý câu hỏi: Ngoài phạt tiền, pháp nhân thương mại phạm [tên tội của đoạn nguồn] có thể bị đình chỉ hoạt động vĩnh viễn khi nào, và trường hợp nào thì bị đình chỉ toàn bộ hoạt động?

**Gold: 100/2015/QH13 Điều 211 khoản 4 — NGUỒN**

> 4. Pháp nhân thương mại phạm tội quy định tại Điều này, thì bị phạt như sau:
> a) Phạm tội thuộc trường hợp quy định tại khoản 1 Điều này, thì bị phạt tiền từ 2.000.000.000 đồng đến 5.000.000.000 đồng;
> b) Phạm tội thuộc trường hợp quy định tại khoản 2 Điều này, thì bị phạt tiền từ 5.000.000.000 đồng đến 10.000.000.000 đồng;
> c) Phạm tội thuộc trường hợp quy định tại Điều 79 của Bộ luật này, thì bị đình chỉ hoạt động vĩnh viễn;
> d) Pháp nhân thương mại còn có thể bị phạt tiền từ 500.000.000 đồng đến 2.000.000.000 đồng, cấm kinh doanh, cấm hoạt động trong một số lĩnh vực nhất định từ 01 năm đến 03 năm hoặc cấm huy động vốn từ 01 năm đến 03 năm.

**Gold: 100/2015/QH13 Điều 79 — ĐÍCH**

> Điều 79. Đình chỉ hoạt động vĩnh viễn
> 1. Đình chỉ hoạt động vĩnh viễn là chấm dứt hoạt động của pháp nhân thương mại trong một hoặc một số lĩnh vực mà pháp nhân thương mại phạm tội gây thiệt hại hoặc có khả năng thực tế gây thiệt hại đến tính mạng của nhiều người, gây sự cố môi trường hoặc gây ảnh hưởng xấu đến an ninh, trật tự, an toàn xã hội và không có khả năng khắc phục hậu quả gây ra.
> 2. Pháp nhân thương mại được thành lập chỉ để thực hiện tội phạm thì bị đình chỉ vĩnh viễn toàn bộ hoạt động.

---
## q093 · dan_chieu · dan_chieu

Trạng thái: GIỮ
Câu hỏi: Tại sao một kiểm sát viên hoặc kiểm tra viên lại phải từ chối hoặc bị thay đổi khi tham gia vào một vụ án?

*Đáp án nháp của mô hình:* Vì họ đã từng tham gia vào vụ án đó với tư cách là điều tra viên, cán bộ điều tra, thẩm phán, hội thẩm, thẩm tra viên hoặc thư ký tòa án.

**Sàng lọc:** không thấy vấn đề — Cần cả nguồn và đích nên đúng ý đồ; nên đổi 'tại sao' thành 'trong trường hợp nào'; đáp án nháp bỏ sót các trường hợp ở đoạn đích. · Gợi ý câu hỏi: Trong vụ án hình sự, khi nào Kiểm sát viên, Kiểm tra viên không được tiếp tục tham gia giải quyết vụ án?

**Gold: 101/2015/QH13 Điều 52 khoản 1 — NGUỒN**

> 1. Kiểm sát viên, Kiểm tra viên phải từ chối tiến hành tố tụng hoặc bị thay đổi khi thuộc một trong các trường hợp:
> a) Trường hợp quy định tại Điều 49 của Bộ luật này;
> b) Đã tiến hành tố tụng trong vụ án đó với tư cách là Điều tra viên, Cán bộ điều tra, Thẩm phán, Hội thẩm, Thẩm tra viên hoặc Thư ký Tòa án.

**Gold: 101/2015/QH13 Điều 49 — ĐÍCH**

> Điều 49. Các trường hợp phải từ chối hoặc thay đổi người có thẩm quyền tiến hành tố tụng
> Người có thẩm quyền tiến hành tố tụng phải từ chối tiến hành tố tụng hoặc bị thay đổi khi thuộc một trong các trường hợp:
> 1. Đồng thời là bị hại, đương sự; là người đại diện, người thân thích của bị hại, đương sự hoặc của bị can, bị cáo;
> 2. Đã tham gia với tư cách là người bào chữa, người làm chứng, người giám định, người định giá tài sản, người phiên dịch, người dịch thuật trong vụ án đó;
> 3. Có căn cứ rõ ràng khác để cho rằng họ có thể không vô tư trong khi làm nhiệm vụ.

---
## q094 · dan_chieu · dan_chieu

Trạng thái: GIỮ
Câu hỏi: Khi nào bên thế chấp được phép thay thế tài sản thế chấp mà không cần sự đồng ý của bên nhận thế chấp?

*Đáp án nháp của mô hình:* Bên thế chấp chỉ được thay thế tài sản thế chấp khi tài sản đó là hàng hóa luân chuyển trong quá trình sản xuất, kinh doanh và đã có thỏa thuận với bên nhận thế chấp.

**Sàng lọc:** không thấy vấn đề — Đúng ý đồ, cần cả hai đoạn; đáp án nháp sai vì gộp hai điều kiện thành một và bỏ trường hợp có thỏa thuận khác.

**Gold: 33/2005/QH11 Điều 354 khoản 1 — NGUỒN**

> 1. Bên thế chấp chỉ được thay thế tài sản thế chấp khi có sự đồng ý của bên nhận thế chấp, nếu không có thoả thuận khác, trừ trường hợp quy định tại khoản 3 Điều 349 của Bộ luật này.

**Gold: 33/2005/QH11 Điều 349 khoản 3 — ĐÍCH**

> 3. Được bán, thay thế tài sản thế chấp, nếu tài sản đó là hàng hoá luân chuyển trong quá trình sản xuất, kinh doanh.
> Trong trường hợp bán tài sản thế chấp là hàng hoá luân chuyển trong quá trình sản xuất, kinh doanh thì quyền yêu cầu bên mua thanh toán tiền, số tiền thu được hoặc tài sản hình thành từ số tiền thu được trở thành tài sản thế chấp thay thế cho số tài sản đã bán.

---
## q095 · dan_chieu · dan_chieu

Trạng thái: GIỮ
Câu hỏi: Tại sao một nhóm lớp mầm non độc lập lại bị đình chỉ hoạt động?

*Đáp án nháp của mô hình:* Vì nhóm lớp đó có hành vi gian lận trong hồ sơ, không đảm bảo các điều kiện thành lập, hoạt động tại địa điểm không được phép, chưa triển khai hoạt động trong 12 tháng kể từ ngày được thành lập, hoặc vi phạm pháp luật đến mức phải đình chỉ hoạt động.

**⚠ Kiểm tra tự động:** trả lời được chỉ bằng đoạn nguồn (Đoạn nguồn nêu rõ các trường hợp cụ thể dẫn đến việc đình chỉ hoạt động của nhóm lớp mầm non độc lập, bao gồm gian lận hồ sơ, không bảo đảm điều kiện thành lập, hoạt động không đúng địa điểm, không triển khai hoạt động trong 12 tháng, hoặc vi phạm pháp luật đến mức phải đình chỉ. Do đó, câu hỏi được trả lời đầy đủ và cụ thể dựa trên đoạn nguồn.)
**Sàng lọc:** không đúng ý đồ nhóm — Danh sách các trường hợp đình chỉ trả lời được chỉ bằng đoạn nguồn; đoạn đích chỉ cần khi hỏi cụ thể về điều kiện thành lập; nên đổi 'tại sao' thành 'khi nào'. · Gợi ý câu hỏi: Một nhóm lớp mầm non độc lập đang hoạt động nhưng không còn đủ giáo viên đáp ứng yêu cầu vị trí việc làm thì có thể bị đình chỉ hoạt động không?

**Gold: 360/2026/NĐ-CP Điều 21 khoản 1 — NGUỒN**

> 1. Nhóm lớp mầm non độc lập bị đình chỉ hoạt động khi thuộc một trong các trường hợp sau đây:
> a) Có hành vi gian lận, cung cấp thông tin sai lệch trong hồ sơ để được thành lập hoặc cho phép thành lập;
> b) Trong quá trình hoạt động không bảo đảm một trong các điều kiện để được thành lập hoặc cho phép thành lập quy định tại Điều 19 Nghị định này;
> c) Tổ chức hoạt động giáo dục không đúng địa điểm trong quyết định thành lập hoặc cho phép thành lập;
> d) Trong thời hạn 12 tháng kể từ ngày quyết định thành lập hoặc cho phép thành lập có hiệu lực mà nhóm lớp mầm non độc lập không triển khai hoạt động giáo dục;
> đ) Vi phạm quy định của pháp luật đến mức phải đình chỉ hoạt động.

**Gold: 360/2026/NĐ-CP Điều 19 — ĐÍCH**

> Điều 19. Điều kiện thành lập nhóm lớp mầm non độc lập công lập hoặc cho phép thành lập nhóm lớp mầm non độc lập dân lập, tư thục
> 1. Có địa điểm, cơ sở vật chất, đồ dùng, đồ chơi, học liệu, thiết bị dạy học đáp ứng yêu cầu của chương trình giáo dục mầm non theo quy định của Bộ Giáo dục và Đào tạo.
> Nhóm lớp mầm non độc lập công lập chỉ được thành lập ở đặc khu trong trường hợp không đủ điều kiện thành lập trường mầm non theo quy định tại Nghị định này.
> 2. Có đội ngũ quản lý chuyên môn, giáo viên, nhân viên và người lao động đủ về số lượng, đáp ứng yêu cầu của vị trí việc làm để tổ chức hoạt động nuôi dưỡng, chăm sóc, giáo dục trẻ em đáp ứng các yêu cầu của chương trình giáo dục mầm non theo quy định của Bộ Giáo dục và Đào tạo.
> 3. Quy mô của nhóm, lớp trong nhóm lớp mầm non độc lập theo quy định của Bộ Giáo dục và Đào tạo.

---
## q096 · dan_chieu · dan_chieu

Trạng thái: DỰ PHÒNG
Câu hỏi: Khi nhập khẩu máy móc, thiết bị, dây chuyền công nghệ đã qua sử dụng, doanh nghiệp cần đáp ứng những điều kiện nào để được phép thông quan?

*Đáp án nháp của mô hình:* Doanh nghiệp phải nộp đầy đủ hồ sơ và tài liệu quy định, trong đó chứng thư giám định phải xác nhận dây chuyền công nghệ đáp ứng các tiêu chí về an toàn, tiết kiệm năng lượng, bảo vệ môi trường, công suất còn lại từ 85% trở lên, tiêu hao nguyên vật liệu và năng lượng không vượt quá 15% so với thiết kế, công nghệ không nằm trong danh mục hạn chế hoặc cấm chuyển giao, và công nghệ phải đang được sử dụng tại ít nhất 03 cơ sở sản xuất ở các nước thành viên OECD.

**Sàng lọc:** chỉ trả lời được một phần từ gold; câu hỏi mơ hồ; lộ đáp án / nhắc văn bản — Gold chỉ có tiêu chí cho dây chuyền công nghệ, không có cho máy móc, thiết bị; câu hỏi lặp gần nguyên tên văn bản. · Gợi ý câu hỏi: Khi doanh nghiệp nhập khẩu một dây chuyền công nghệ đã qua sử dụng, cơ quan hải quan chỉ cho thông quan khi nào và dây chuyền phải đạt những tiêu chí gì?

**Gold: 56/2026/TT-BKHCN Điều 7 khoản 2 — NGUỒN**

> 2. Doanh nghiệp nộp 01 bộ hồ sơ nhập khẩu và tài liệu quy định tại khoản 1 Điều này về cơ quan hải quan nơi đăng ký tờ khai hải quan.
> Cơ quan hải quan chỉ làm thủ tục thông quan khi hồ sơ nhập khẩu, tài liệu quy định tại khoản 1 Điều này đầy đủ, đúng quy định và chứng thư giám định ghi kết luận dây chuyền công nghệ đã qua sử dụng đáp ứng tiêu chí nhập khẩu quy định tại Điều 5 Thông tư này.

**Gold: 56/2026/TT-BKHCN Điều 5 — ĐÍCH**

> Điều 5. Tiêu chí nhập khẩu đối với dây chuyền công nghệ đã qua sử dụng
> Dây chuyền công nghệ đã qua sử dụng được phép nhập khẩu khi đáp ứng các tiêu chí sau:
> 1. Được sản xuất theo tiêu chuẩn:
> a) Phù hợp với quy định của quy chuẩn kỹ thuật quốc gia (QCVN) về an toàn, tiết kiệm năng lượng và bảo vệ môi trường;
> b) Trường hợp không có QCVN liên quan đến dây chuyền công nghệ nhập khẩu thì dây chuyền công nghệ phải được sản xuất theo tiêu chuẩn phù hợp với chỉ tiêu kỹ thuật của tiêu chuẩn quốc gia (TCVN) Việt Nam hoặc tiêu chuẩn quốc gia của một trong các nước G7, Hàn Quốc về an toàn, tiết kiệm năng lượng và bảo vệ môi trường.
> 2. Công suất (tính theo số lượng sản phẩm được tạo ra bởi dây chuyền công nghệ trong một đơn vị thời gian) hoặc hiệu suất còn lại phải đạt từ 85% trở lên so với công suất hoặc hiệu suất thiết kế.
> 3. Mức tiêu hao nguyên, vật liệu, năng lượng không vượt quá 15% so với thiết kế.
> 4. Công nghệ của dây chuyền công nghệ không thuộc Danh mục công nghệ hạn chế chuyển giao, Danh mục công nghệ cấm chuyển giao quy định tại Nghị định số 101/2026/NĐ-CP ngày 31 tháng 3 năm 2026 của Chính phủ quy định chi tiết một số điều và biện pháp để hướng dẫn thi hành Luật Chuyển giao công nghệ.
> 5. Công nghệ của dây chuyền công nghệ phải đang được sử dụng tại ít nhất 03 cơ sở sản xuất trong các nước thuộc Tổ chức Hợp tác và Phát triển Kinh tế (Organization for Economic Co-operation and Development - OECD).

---
## q097 · dan_chieu · dan_chieu

Trạng thái: GIỮ
Câu hỏi: Ai là người có quyền nhận hàng theo quy định của Bộ luật Hàng hải?

*Đáp án nháp của mô hình:* Người nhận hàng là người có quyền nhận hàng được quy định tại Điều 162 và Điều 187 của Bộ luật này, cụ thể, người có quyền nhận hàng là người được nêu trong vận đơn hoặc người được chuyển nhượng vận đơn theo quy định.

**Cờ tự động:** trùng từ cao (87%)
**Sàng lọc:** chỉ trả lời được một phần từ gold; lộ đáp án / nhắc văn bản — Câu hỏi nêu tên Bộ luật Hàng hải; đoạn nguồn dẫn tới hai Điều (162 và 187) nhưng gold chỉ có Điều 162 nên chỉ trả lời được một phần. · Gợi ý câu hỏi: Trong vận chuyển hàng hóa bằng đường biển, ai là người nhận hàng hợp pháp khi vận đơn là vận đơn theo lệnh, vận đơn vô danh hoặc vận đơn đích danh?

**Gold: 95/2015/QH13 Điều 147 khoản 5 — NGUỒN**

> 5. Người nhận hàng là người có quyền nhận hàng quy định tại Điều 162 và Điều 187 của Bộ luật này.

**Gold: 95/2015/QH13 Điều 162 — ĐÍCH**

> Điều 162. Chuyển nhượng vận đơn
> 1. Vận đơn theo lệnh được chuyển nhượng bằng cách ký hậu vận đơn. Người ký hậu cuối cùng có quyền phát lệnh trả hàng trong vận đơn theo lệnh là người nhận hàng hợp pháp.
> 2. Vận đơn vô danh được chuyển nhượng bằng cách người vận chuyển trao vận đơn vô danh đó cho người được chuyển nhượng. Người xuất trình vận đơn vô danh là người nhận hàng hợp pháp.
> 3. Vận đơn đích danh không được chuyển nhượng. Người có tên trong vận đơn đích danh là người nhận hàng hợp pháp.

---
## q098 · dan_chieu · dan_chieu

Trạng thái: DỰ PHÒNG
Câu hỏi: Nếu một người được ủy quyền quản lý tài sản, họ có thể trở thành chủ sở hữu tài sản đó không?

*Đáp án nháp của mô hình:* Không, người được ủy quyền quản lý tài sản không thể trở thành chủ sở hữu đối với tài sản đó, dù họ quản lý nó, vì việc trở thành chủ sở hữu chỉ xảy ra theo quy định về thời hiệu, như được nêu trong đoạn về thời hạn chiếm hữu.

**Sàng lọc:** không đúng ý đồ nhóm; câu hỏi mơ hồ; lộ đáp án / nhắc văn bản — Câu hỏi hỏi chung 'có thể trở thành chủ sở hữu không', trong khi gold chỉ loại trừ căn cứ thời hiệu; trả lời 'không' được ngay từ nguồn mà không cần đích. · Gợi ý câu hỏi: Một người được chủ nhà ủy quyền trông coi căn nhà liên tục, công khai hơn ba mươi năm; người đó có thể dựa vào thời gian chiếm hữu này để trở thành chủ sở hữu căn nhà không?

**Gold: 33/2005/QH11 Điều 185 khoản 2 — NGUỒN**

> 2. Người được ủy quyền quản lý tài sản không thể trở thành chủ sở hữu đối với tài sản được giao theo căn cứ về thời hiệu quy định tại khoản 1 Điều 247 của Bộ luật này.

**Gold: 33/2005/QH11 Điều 247 khoản 1 — ĐÍCH**

> 1. Người chiếm hữu, người được lợi về tài sản không có căn cứ pháp luật nhưng ngay tình, liên tục, công khai trong thời hạn mười năm đối với động sản, ba mươi năm đối với bất động sản thì trở thành chủ sở hữu tài sản đó, kể từ thời điểm bắt đầu chiếm hữu, trừ trường hợp quy định tại khoản 2 Điều này.

---
## q099 · dan_chieu · dan_chieu

Trạng thái: DỰ PHÒNG
Câu hỏi: Người bị kết án về tội ít nghiêm trọng và đã được hoãn chấp hành hình phạt có thể được miễn chấp hành hình phạt nếu trong thời gian hoãn có lập công không?

*Đáp án nháp của mô hình:* Có, nếu trong thời gian được hoãn chấp hành hình phạt đã lập công, thì theo đề nghị của Viện trưởng Viện Kiểm sát, Toà án có thể quyết định miễn chấp hành hình phạt.

**Cờ tự động:** trùng từ cao (97%)
**⚠ Bản cũ:** gold ở BẢN CŨ, bản mới cũng có trong kho — 15/1999/QH10 Điều 57 ↔ 100/2015/QH13 Điều 62: KHÁC NHIỀU hoặc không còn (chứa 0.49); 15/1999/QH10 Điều 61 ↔ 100/2015/QH13 Điều 67: KHÁC ÍT (chứa 0.87)
**⚠ Kiểm tra tự động:** trả lời được chỉ bằng đoạn nguồn (Đoạn nguồn nêu rõ rằng người bị kết án về tội ít nghiêm trọng đã được hoãn chấp hành hình phạt thì nếu trong thời gian được hoãn đã lập công, Toà án có thể quyết định miễn chấp hành hình phạt theo đề nghị của Viện trưởng Viện Kiểm sát, nên câu hỏi được trả lời đầy đủ và cụ thể dựa trên đoạn nguồn.)
**Sàng lọc:** không đúng ý đồ nhóm; lộ đáp án / nhắc văn bản — Câu hỏi chép gần nguyên văn đoạn nguồn và trả lời được mà không cần đọc điều về hoãn chấp hành hình phạt tù. · Gợi ý câu hỏi: Người bị phạt tù về tội ít nghiêm trọng được hoãn chấp hành vì nhu cầu công vụ, nếu trong thời gian hoãn lập công thì có thể được miễn chấp hành hình phạt không, và theo đề nghị của ai?

**Gold: 15/1999/QH10 Điều 57 khoản 3 — NGUỒN**

> 3. Đối với người bị kết án về tội ít nghiêm trọng đã được hoãn chấp hành hình phạt theo quy định tại Điều 61 của Bộ luật này, nếu trong thời gian được hoãn đã lập công, thì theo đề nghị của Viện trưởng Viện Kiểm sát, Toà án có thể quyết định miễn chấp hành hình phạt.

**Gold: 15/1999/QH10 Điều 61 — ĐÍCH**

> Điều 61. Hoãn chấp hành hình phạt tù
> 1. Người bị xử phạt tù có thể được hoãn chấp hành hình phạt trong các trường hợp sau đây:
> a) Bị bệnh nặng được hoãn cho đến khi sức khỏe được hồi phục;
> b) Phụ nữ có thai hoặc đang nuôi con dưới 36 tháng tuổi, thì được hoãn cho đến khi con đủ 36 tháng tuổi;
> c) Là người lao động duy nhất trong gia đình, nếu phải chấp hành hình phạt tù thì gia đình sẽ gặp khó khăn đặc biệt, được hoãn đến một năm, trừ trường hợp người đó bị kết án về các tội xâm phạm an ninh quốc gia hoặc các tội khác là tội rất nghiêm trọng, đặc biệt nghiêm trọng;
> d) Bị kết án về tội ít nghiêm trọng, do nhu cầu công vụ, thì được hoãn đến một năm.
> 2. Trong thời gian được hoãn chấp hành hình phạt tù, nếu người được hoãn chấp hành hình phạt lại phạm tội mới, thì Toà án buộc người đó phải chấp hành hình phạt trước và tổng hợp với hình phạt của bản án mới theo quy định tại Điều 51 của Bộ luật này.

---
## q100 · dan_chieu · dan_chieu

Trạng thái: DỰ PHÒNG
Câu hỏi: Nếu chủ sở hữu tài sản không yêu cầu nhận lại hoặc thanh toán nợ trong thời gian nào thì người trục vớt phải giao nộp tài sản cho cơ quan nhà nước có thẩm quyền?

*Đáp án nháp của mô hình:* Trong thời hạn 15 ngày kể từ ngày thông báo, nếu chủ sở hữu không yêu cầu nhận lại tài sản hay thanh toán nợ thì người trục vớt phải giao nộp tài sản cho cơ quan nhà nước có thẩm quyền, cụ thể là các bộ, ngành hoặc địa phương được quy định tại Điều 284 của Bộ luật Hàng hải.

**Cờ tự động:** trùng từ cao (86%)
**⚠ Kiểm tra tự động:** trả lời được chỉ bằng đoạn nguồn (Đoạn nguồn nêu rõ rằng trong thời hạn 15 ngày kể từ ngày thông báo, nếu chủ sở hữu tài sản không yêu cầu nhận lại hoặc không thanh toán nợ thì người trục vớt phải giao nộp tài sản cho cơ quan nhà nước có thẩm quyền, nên trả lời đầy đủ và cụ thể theo nội dung đoạn nguồn.)
**Sàng lọc:** không đúng ý đồ nhóm; lộ đáp án / nhắc văn bản — Câu hỏi chép gần nguyên văn và chỉ hỏi thời hạn nên trả lời bằng đoạn nguồn, không cần đoạn đích về cơ quan có thẩm quyền; đoạn đích còn dính tiêu đề 'Chương XV TAI NẠN ĐÂM VA'. · Gợi ý câu hỏi: Người trục vớt được tài sản chìm đắm là di sản văn hóa nhưng chủ sở hữu không đến nhận lại thì sau bao lâu phải giao nộp, và giao cho cơ quan nào chủ trì xử lý?

**Gold: 95/2015/QH13 Điều 282 khoản 3 — NGUỒN**

> 3. Trong thời hạn 15 ngày kể từ ngày thông báo mà chủ sở hữu tài sản không yêu cầu nhận lại tài sản hoặc không thanh toán các khoản nợ thì người trục vớt có nghĩa vụ giao nộp tài sản đó cho cơ quan nhà nước có thẩm quyền quy định tại Điều 284 của Bộ luật này.

**Gold: 95/2015/QH13 Điều 284 — ĐÍCH**

> Điều 284. Thẩm quyền xử lý tài sản chìm đắm
> 1. Bộ Giao thông vận tải chủ trì tổ chức xử lý tài sản chìm đắm gây nguy hiểm.
> 2. Bộ Văn hóa, Thể thao và Du lịch chủ trì tổ chức xử lý tài sản chìm đắm là di sản văn hóa.
> 3. Bộ Quốc phòng chủ trì tổ chức xử lý tài sản chìm đắm liên quan đến quốc phòng và tài sản chìm đắm trong khu vực quân sự.
> 4. Bộ Công an chủ trì tổ chức xử lý tài sản chìm đắm liên quan đến an ninh quốc gia.
> 5. Ủy ban nhân dân cấp tỉnh chủ trì tổ chức xử lý tài sản chìm đắm không thuộc tài sản quy định tại các khoản 1, 2, 3 và 4 Điều này.
> 6. Chính phủ quy định chi tiết việc xử lý tài sản chìm đắm.

---
## q101 · dan_chieu · dan_chieu

Trạng thái: GIỮ
Câu hỏi: Thư viện Quốc gia và các thư viện cấp tỉnh có thể lưu giữ những loại tài nguyên thông tin nào để phục vụ nghiên cứu?

*Đáp án nháp của mô hình:* Các thư viện này có thể lưu giữ tài nguyên thông tin có nội dung ảnh hưởng đến lợi ích của Nhà nước hoặc quyền lợi hợp pháp của cá nhân, tổ chức; tài nguyên thuộc bí mật nhà nước; bản gốc tài liệu cổ, quý hiếm hoặc di sản văn hóa; và bản gốc tài liệu bị hư hỏng, nhằm phục vụ hoạt động nghiên cứu.

**Sàng lọc:** không thấy vấn đề — Câu hỏi ổn; đáp án nháp sai vì liệt kê cả điểm a–d, trong khi đoạn nguồn chỉ dẫn chiếu điểm a (tài nguyên có nội dung mà nếu dùng rộng rãi có thể ảnh hưởng lợi ích Nhà nước, quyền và lợi ích hợp pháp của tổ chức, cá nhân).

**Gold: 46/2019/QH14 Điều 38 khoản 10 — NGUỒN**

> 10. Thư viện Quốc gia Việt Nam, thư viện chuyên ngành của Bộ, cơ quan ngang Bộ, cơ quan thuộc Chính phủ, Văn phòng Quốc hội, Tòa án nhân dân tối cao, Viện kiểm sát nhân dân tối cao và thư viện cấp tỉnh được lưu giữ tài nguyên thông tin quy định tại điểm a khoản 1 Điều 7 của Luật này để phục vụ hoạt động nghiên cứu.

**Gold: 46/2019/QH14 Điều 7 khoản 1 — ĐÍCH**

> 1. Tài nguyên thông tin hạn chế sử dụng trong thư viện bao gồm:
> a) Tài nguyên thông tin có nội dung thông tin nếu sử dụng rộng rãi có thể ảnh hưởng đến lợi ích của Nhà nước, quyền và lợi ích hợp pháp của cơ quan, tổ chức, cá nhân;
> b) Tài nguyên thông tin thuộc bí mật nhà nước, hạn chế sử dụng, tiếp cận có điều kiện, hạn chế quyền tiếp cận theo quy định của pháp luật về bảo vệ bí mật nhà nước, tiếp cận thông tin, lưu trữ;
> c) Bản gốc tài liệu cổ, quý hiếm, tài nguyên thông tin là di sản văn hóa đang lưu giữ trong thư viện;
> d) Bản gốc tài liệu bị hư hỏng.

---
## q102 · dan_chieu · dan_chieu

Trạng thái: DỰ PHÒNG
Câu hỏi: Nếu một bên gửi đơn kháng cáo sau thời hạn quy định, thì tòa án sẽ xử lý như thế nào?

*Đáp án nháp của mô hình:* Tòa án cấp sơ thẩm sẽ nhận đơn kháng cáo quá hạn và gửi đơn đó, cùng bản tường trình lý do và tài liệu, chứng cứ nếu có, cho Tòa án cấp phúc thẩm để xem xét.

**⚠ Kiểm tra tự động:** trả lời được chỉ bằng đoạn nguồn (Đoạn nguồn nêu rõ rằng nếu đơn kháng cáo quá thời hạn, Tòa án cấp sơ thẩm sẽ phải gửi đơn kháng cáo, bản tường trình của người kháng cáo về lý do kháng cáo quá hạn và tài liệu, chứng cứ, nếu có cho Tòa án cấp phúc thẩm, nên trả lời đầy đủ và cụ thể theo nội dung đoạn nguồn.)
**Sàng lọc:** không đúng ý đồ nhóm; câu hỏi mơ hồ — Trả lời được ngay từ đoạn nguồn (tòa sơ thẩm gửi đơn lên tòa phúc thẩm), không cần đoạn đích về thời hạn kháng cáo; câu hỏi không nói rõ là tố tụng dân sự nên dễ lẫn với tố tụng hình sự, hành chính. · Gợi ý câu hỏi: Trong vụ án dân sự, đương sự vắng mặt tại phiên tòa sơ thẩm, đến ngày thứ 20 kể từ khi được giao bản án mới nộp đơn kháng cáo; đơn này bị coi là gì và Tòa án cấp sơ thẩm phải xử lý ra sao?

**Gold: 24/2004/QH11 Điều 247 khoản 1 — NGUỒN**

> 1. Kháng cáo quá thời hạn quy định tại Điều 245 của Bộ luật này là kháng cáo quá hạn. Sau khi nhận được đơn kháng cáo quá hạn, Toà án cấp sơ thẩm phải gửi đơn kháng cáo, bản tường trình của người kháng cáo về lý do kháng cáo quá hạn và tài liệu, chứng cứ, nếu có cho Toà án cấp phúc thẩm.

**Gold: 24/2004/QH11 Điều 245 — ĐÍCH**

> Điều 245. Thời hạn kháng cáo
> 1. Thời hạn kháng cáo đối với bản án của Toà án cấp sơ thẩm là mười lăm ngày, kể từ ngày tuyên án; đối với đương sự không có mặt tại phiên toà thì thời hạn kháng cáo tính từ ngày bản án được giao cho họ hoặc được niêm yết.
> 2. Thời hạn kháng cáo đối với quyết định tạm đình chỉ, đình chỉ giải quyết vụ án của Toà án cấp sơ thẩm là bảy ngày, kể từ ngày người có quyền kháng cáo nhận được quyết định.
> 3. Trong trường hợp đơn kháng cáo gửi qua bưu điện thì ngày kháng cáo được tính căn cứ vào ngày bưu điện nơi gửi đóng dấu ở phong bì.

---
## q103 · dan_chieu · dan_chieu

Trạng thái: DỰ PHÒNG
Câu hỏi: Công chức trong Tòa án được hưởng tiền lương và phụ cấp như thế nào?

*Đáp án nháp của mô hình:* Công chức trong Tòa án được hưởng tiền lương và phụ cấp theo chế độ quy định tại pháp luật, trong đó Thẩm phán, Thẩm tra viên Tòa án, Thư ký Tòa án được ưu tiên về tiền lương và phụ cấp, cụ thể do Ủy ban Thường vụ Quốc hội quy định theo đề nghị của Chánh án Tòa án nhân dân tối cao.

**Sàng lọc:** không đúng ý đồ nhóm; câu hỏi mơ hồ; gold đáng ngờ — Đoạn nguồn là một mục liệt kê mất câu dẫn (văn bản gốc là chế độ đối với Thẩm phán), nên câu hỏi lệch chủ thể sang 'công chức trong Tòa án'. Nhóm này gồm nhiều đối tượng có chế độ khác nhau và trả lời được chỉ bằng đoạn đích. · Gợi ý câu hỏi: Thẩm phán được hưởng chế độ tiền lương, phụ cấp như thế nào và cơ quan nào quy định cụ thể chế độ đó?

**Gold: 34/2024/QH15 Điều 101 khoản 1 — NGUỒN**

> 1. Được hưởng tiền lương, phụ cấp theo quy định tại Điều 142 của Luật này;

**Gold: 34/2024/QH15 Điều 142 — ĐÍCH**

> Điều 142. Chế độ tiền lương, phụ cấp
> 1. Nhà nước có chính sách ưu tiên về tiền lương, phụ cấp đối với Thẩm phán, Thẩm tra viên Tòa án, Thư ký Tòa án.
> 2. Chế độ tiền lương và phụ cấp đối với Thẩm phán, Thẩm tra viên Tòa án, Thư ký Tòa án do Ủy ban Thường vụ Quốc hội quy định theo đề nghị của Chánh án Tòa án nhân dân tối cao.
> 3. Chế độ tiền lương, phụ cấp đối với công chức khác, viên chức và người lao động của Tòa án được thực hiện theo quy định của pháp luật.
> 4. Công chức, viên chức của Tòa án được điều động, luân chuyển, biệt phái tại các Tòa án được hưởng chế độ, chính sách theo quy định của pháp luật.

---
## q104 · dan_chieu · dan_chieu

Trạng thái: XOÁ
Câu hỏi: Khi người sử dụng lao động thôi việc cho người lao động theo quy định, thì phải trả khoản tiền gì và điều kiện nào để được tính?

*Đáp án nháp của mô hình:* Phải trả trợ cấp mất việc làm, với mức là mỗi năm làm việc được 01 tháng tiền lương, nhưng ít nhất bằng 02 tháng tiền lương, và thời gian làm việc được tính theo quy định tại Điều 49.

**⚠ Bản cũ:** gold ở BẢN CŨ, bản mới cũng có trong kho — 10/2012/QH13 Điều 45 ↔ 45/2019/QH14 Điều 42: KHÁC ÍT (chứa 0.67); 10/2012/QH13 Điều 49 ↔ 45/2019/QH14 Điều 47: KHÁC ÍT (chứa 0.78)
**Sàng lọc:** câu hỏi mơ hồ — Không nêu trường hợp thôi việc (sáp nhập, hợp nhất, chia, tách doanh nghiệp) nên dễ lẫn với trợ cấp thôi việc; câu hỏi hỏi gộp hai ý. Đáp án nháp thiếu điều kiện đã làm việc từ 12 tháng trở lên. · Gợi ý câu hỏi: Khi doanh nghiệp sáp nhập, hợp nhất hoặc chia, tách mà người sử dụng lao động cho người lao động thôi việc, người lao động được hưởng khoản trợ cấp nào và mức trợ cấp được tính ra sao?

**Gold: 10/2012/QH13 Điều 45 khoản 3 — NGUỒN**

> 3. Trong trường hợp người sử dụng lao động cho người lao động thôi việc theo quy định tại Điều này, thì phải trả trợ cấp mất việc làm cho người lao động theo quy định tại Điều 49 của Bộ luật này.

**Gold: 10/2012/QH13 Điều 49 — ĐÍCH**

> Điều 49. Trợ cấp mất việc làm
> 1. Người sử dụng lao động trả trợ cấp mất việc làm cho người lao động đã làm việc thường xuyên cho mình từ 12 tháng trở lên mà bị mất việc làm theo quy định tại Điều 44 và Điều 45 của Bộ luật này, mỗi năm làm việc trả 01 tháng tiền lương nhưng ít nhất phải bằng 02 tháng tiền lương.
> 2. Thời gian làm việc để tính trợ cấp mất việc làm là tổng thời gian người lao động đã làm việc thực tế cho người sử dụng lao động trừ đi thời gian người lao động đã tham gia bảo hiểm thất nghiệp theo quy định của Luật bảo hiểm xã hội và thời gian làm việc đã được người sử dụng lao động chi trả trợ cấp thôi việc.
> 3. Tiền lương để tính trợ cấp mất việc làm là tiền lương bình quân theo hợp đồng lao động của 06 tháng liền kề trước khi người lao động mất việc làm.

---
## q105 · dan_chieu · dan_chieu

Trạng thái: DỰ PHÒNG
Câu hỏi: Nếu một viên chức đã được xếp loại chất lượng nhưng sau này phát hiện có khuyết điểm hoặc không trung thực, thì có thể điều chỉnh lại xếp loại không?

*Đáp án nháp của mô hình:* Có thể điều chỉnh lại xếp loại chất lượng bằng cách cấp có thẩm quyền ban hành quyết định xếp loại mới để thay thế quyết định trước đó.

**⚠ Kiểm tra tự động:** trả lời được chỉ bằng đoạn nguồn (Đoạn nguồn nêu rõ rằng nếu phát hiện khuyết điểm hoặc không trung thực làm cho kết quả xếp loại không chính xác, thì cấp có thẩm quyền có thể ban hành quyết định xếp loại mới thay thế quyết định trước đó, tức là có thể điều chỉnh lại xếp loại.)
**Sàng lọc:** không đúng ý đồ nhóm; lộ đáp án / nhắc văn bản — Trả lời trọn từ đoạn nguồn, không cần đoạn đích về thẩm quyền; câu hỏi chép gần nguyên văn đoạn nguồn. · Gợi ý câu hỏi: Một viên chức là cấp phó của người đứng đầu đơn vị sự nghiệp công lập đã được xếp loại chất lượng, sau đó bị phát hiện kê khai không trung thực khiến kết quả sai; ai có thẩm quyền xếp loại lại và quyết định cũ được xử lý thế nào?

**Gold: 233/2026/NĐ-CP Điều 15 khoản 4 — NGUỒN**

> 4. Viên chức đã được xếp loại chất lượng nhưng sau đó phát hiện có khuyết điểm, không bảo đảm quy định về mức xếp loại hoặc thiếu trung thực làm cho kết quả không chính xác thì cấp có thẩm quyền xếp loại chất lượng tại Điều 13 Nghị định này ban hành quyết định xếp loại chất lượng mới thay thế quyết định đã ban hành trước đó.

**Gold: 233/2026/NĐ-CP Điều 13 — ĐÍCH**

> Điều 13. Thẩm quyền, trách nhiệm giao nhiệm vụ, theo dõi, đánh giá và xếp loại chất lượng viên chức
> 1. Căn cứ chức năng, nhiệm vụ của cơ quan, tổ chức, đơn vị, kế hoạch công tác (tháng, quý, năm) và nhiệm vụ được cấp có thẩm quyền giao, người đứng đầu đơn vị trực tiếp sử dụng viên chức phân công, giao nhiệm vụ cho viên chức thuộc phạm vi quản lý, bảo đảm nguyên tắc có số lượng, chất lượng, tiến độ cụ thể và phù hợp với vị trí việc làm.
> 2. Thẩm quyền, trách nhiệm theo dõi, đánh giá
> a) Người đứng đầu cơ quan quản lý đơn vị sự nghiệp công lập theo dõi, đánh giá đối với người đứng đầu đơn vị sự nghiệp công lập thuộc phạm vi quản lý.
> b) Người đứng đầu đơn vị sự nghiệp công lập theo dõi, đánh giá đối với cấp phó của mình và người đứng đầu các đơn vị cấu thành.
> c) Người đứng đầu đơn vị cấu thành theo dõi, đánh giá đối với cấp phó của mình và viên chức thuộc phạm vi sử dụng.
> 3. Thẩm quyền xếp loại chất lượng viên chức
> a) Người đứng đầu cơ quan quản lý đơn vị sự nghiệp công lập xếp loại chất lượng đối với viên chức quy định tại điểm a khoản 2 Điều này.
> b) Người đứng đầu đơn vị sự nghiệp công lập xếp loại chất lượng đối với viên chức quy định tại điểm b và điểm c khoản 2 Điều này.

---
## q106 · dan_chieu · dan_chieu

Trạng thái: DỰ PHÒNG
Câu hỏi: Khi có kháng cáo hoặc kháng nghị đối với quyết định của Toà án nhân dân cấp tỉnh, thì thời gian để Toà án nhân dân tối cao xem xét là bao lâu?

*Đáp án nháp của mô hình:* Thời hạn là một tháng, kể từ ngày nhận được hồ sơ, và thời hạn này có thể được kéo dài thêm không quá hai tháng nếu cần yêu cầu giải thích theo quy định tại Điều 353.

**⚠ Kiểm tra tự động:** trả lời được chỉ bằng đoạn nguồn (Đoạn nguồn nêu rõ thời hạn để Toà án nhân dân tối cao xem xét là một tháng, kể từ ngày nhận được hồ sơ, và trong trường hợp cần yêu cầu giải thích thì thời hạn được kéo dài nhưng không quá hai tháng.)
**Sàng lọc:** không đúng ý đồ nhóm; câu hỏi mơ hồ — Thời hạn nằm trọn ở đoạn nguồn, không cần đoạn đích về yêu cầu giải thích. Câu hỏi thiếu ngữ cảnh là thủ tục công nhận bản án dân sự của Tòa án nước ngoài, nên cụm 'quyết định của Tòa án cấp tỉnh' quá chung. · Gợi ý câu hỏi: Khi xét kháng cáo, kháng nghị quyết định của Tòa án cấp tỉnh về công nhận và cho thi hành bản án dân sự của Tòa án nước ngoài, nếu cần yêu cầu bên nước ngoài giải thích điểm chưa rõ thì văn bản yêu cầu phải gửi qua cơ quan nào và thời hạn xét được kéo dài tối đa bao lâu?

**Gold: 24/2004/QH11 Điều 359 khoản 1 — NGUỒN**

> 1. Toà án nhân dân tối cao xét quyết định của Toà án nhân dân cấp tỉnh bị kháng cáo, kháng nghị trong thời hạn một tháng, kể từ ngày nhận được hồ sơ; trường hợp cần phải yêu cầu giải thích theo quy định tại Điều 353 của Bộ luật này thì thời hạn này được kéo dài, nhưng không quá hai tháng.

**Gold: 24/2004/QH11 Điều 353 — ĐÍCH**

> Điều 353. Thụ lý hồ sơ và yêu cầu giải thích
> 1. Trong thời hạn ba ngày làm việc, kể từ ngày nhận được hồ sơ do Bộ Tư pháp chuyển đến, Toà án có thẩm quyền phải thụ lý và thông báo cho Viện kiểm sát cùng cấp biết.
> 2. Trong thời hạn chuẩn bị xét đơn yêu cầu, Toà án có quyền yêu cầu người gửi đơn, Toà án nước ngoài đã ra bản án, quyết định giải thích những điểm chưa rõ trong hồ sơ.
> Văn bản yêu cầu giải thích và văn bản trả lời được gửi thông qua Bộ Tư pháp Việt Nam.
> 3. Trong thời hạn bảy ngày, kể từ ngày nhận được văn bản của Toà án Việt Nam yêu cầu giải thích, Bộ Tư pháp gửi cho người gửi đơn yêu cầu hoặc Toà án nước ngoài văn bản yêu cầu giải thích đó.
> 4. Trong thời hạn bảy ngày, kể từ ngày nhận được văn bản trả lời yêu cầu giải thích, Bộ Tư pháp gửi cho Toà án Việt Nam đã yêu cầu văn bản trả lời đó.

---
## q107 · dan_chieu · dan_chieu

Trạng thái: DỰ PHÒNG
Câu hỏi: Khi nào thì cổ phần được coi là đã bán theo quy định của Luật doanh nghiệp?

*Đáp án nháp của mô hình:* Cổ phần được coi là đã bán khi được thanh toán đủ và thông tin về người mua được ghi đầy đủ vào sổ đăng ký cổ đông.

**⚠ Kiểm tra tự động:** trả lời được chỉ bằng đoạn nguồn (Đoạn nguồn nêu rõ rằng cổ phần được coi là đã bán khi được thanh toán đủ và thông tin về người mua được ghi đầy đủ vào sổ đăng ký cổ đông, kể từ thời điểm đó người mua trở thành cổ đông. Điều này trả lời cụ thể và đầy đủ câu hỏi về thời điểm cổ phần được coi là đã bán theo quy định của Luật doanh nghiệp.)
**Sàng lọc:** không đúng ý đồ nhóm; lộ đáp án / nhắc văn bản — Câu hỏi nêu tên Luật doanh nghiệp. Câu trả lời cho 'khi nào' lấy được ngay từ đoạn nguồn, không buộc phải đọc danh mục thông tin trong sổ đăng ký cổ đông ở đoạn đích. · Gợi ý câu hỏi: Người mua đã thanh toán đủ tiền mua cổ phần; công ty phải ghi những thông tin nào của người mua vào sổ đăng ký cổ đông thì cổ phần mới được coi là đã bán?

**Gold: 59/2020/QH14 Điều 124 khoản 4 — NGUỒN**

> 4. Cổ phần được coi là đã bán khi được thanh toán đủ và những thông tin về người mua quy định tại khoản 2 Điều 122 của Luật này được ghi đầy đủ vào sổ đăng ký cổ đông; kể từ thời điểm đó, người mua cổ phần trở thành cổ đông của công ty.

**Gold: 59/2020/QH14 Điều 122 khoản 2 — ĐÍCH**

> 2. Sổ đăng ký cổ đông phải bao gồm các nội dung chủ yếu sau đây:
> a) Tên, địa chỉ trụ sở chính của công ty;
> b) Tổng số cổ phần được quyền chào bán, loại cổ phần được quyền chào bán và số cổ phần được quyền chào bán của từng loại;
> c) Tổng số cổ phần đã bán của từng loại và giá trị vốn cổ phần đã góp;
> d) Họ, tên, địa chỉ liên lạc, quốc tịch, số giấy tờ pháp lý của cá nhân đối với cổ đông là cá nhân; tên, mã số doanh nghiệp hoặc số giấy tờ pháp lý của tổ chức, địa chỉ trụ sở chính đối với cổ đông là tổ chức;
> đ) Số lượng cổ phần từng loại của mỗi cổ đông, ngày đăng ký cổ phần.

---
## q235 · dan_chieu · dan_chieu · TRUNG LẬP

Trạng thái: GIỮ
Câu hỏi: Khi kê biên tài sản, cần làm gì để đảm bảo biên bản được hợp lệ và có thể sử dụng trong quá trình điều tra?

*Đáp án nháp của mô hình:* Phải lập biên bản ghi rõ tên và tình trạng từng tài sản bị kê biên, đọc cho những người có mặt nghe và cùng ký tên. Biên bản cũng phải ghi nhận các ý kiến bổ sung và lý do nếu không chấp nhận, và được người tham gia tố tụng, điều tra viên, cán bộ điều tra cùng ký tên.

**Sàng lọc:** không thấy vấn đề — Cụm 'hợp lệ và có thể sử dụng' không có trong gold; nên hỏi thẳng nội dung biên bản và người ký. · Gợi ý câu hỏi: Khi kê biên tài sản trong quá trình điều tra, biên bản kê biên phải ghi những gì, xử lý ý kiến bổ sung ra sao và những ai phải ký tên?

**Gold: 101/2015/QH13 Điều 128 khoản 4 điểm c — NGUỒN**

> Người tiến hành kê biên phải lập biên bản, ghi rõ tên và tình trạng từng tài sản bị kê biên. Biên bản được lập theo quy định tại Điều 178 của Bộ luật này, đọc cho những người có mặt nghe và cùng ký tên.

**Gold: 101/2015/QH13 Điều 178 — ĐÍCH**

> Ý kiến bổ sung, nhận xét được ghi vào biên bản; trường hợp không chấp nhận bổ sung thì ghi rõ lý do vào biên bản. Người tham gia tố tụng, Điều tra viên, Cán bộ điều tra cùng ký tên vào biên bản.

---
## q236 · dan_chieu · dan_chieu · TRUNG LẬP

Trạng thái: GIỮ
Câu hỏi: Khi nào thì cơ quan, tổ chức có thể thanh lý xe ô tô theo quy định?

*Đáp án nháp của mô hình:* Khi xe ô tô hết hạn sử dụng hoặc đáp ứng các điều kiện về niên hạn, tần suất sử dụng theo quy định của pháp luật.

**Sàng lọc:** chỉ trả lời được một phần từ gold; không đúng ý đồ nhóm — Câu hỏi chỉ cần đoạn đích, không xuất phát từ nội dung đoạn nguồn (xử lý xe, bảo đảm định mức xe phục vụ công tác chung); đoạn đích chỉ có điểm a của danh sách 'một trong các điều kiện' nên có thể thiếu điều kiện khác. · Gợi ý câu hỏi: Cơ quan nhà nước được xử lý xe ô tô phục vụ công tác chung khi xe đáp ứng những điều kiện thanh lý nào?

**Gold: 379/2026/NĐ-CP Điều 39 khoản 4 — NGUỒN**

> Khi đủ điều kiện thanh lý theo quy định tại khoản 2 Điều 4 Nghị định này hoặc thực hiện xử lý theo quy định của pháp luật về quản lý, sử dụng tài sản công, cơ quan, tổ chức, đơn vị thực hiện xử lý xe ô tô theo quy định của pháp luật về quản lý, sử dụng tài sản công, bảo đảm số lượng xe ô tô phục vụ công tác chung theo định mức quy định tại Nghị định này.

**Gold: 379/2026/NĐ-CP Điều 4 khoản 2 — ĐÍCH**

> Việc thanh lý xe ô tô được thực hiện khi đáp ứng một trong các điều kiện sau đây:
> a) Khi hết hạn sử dụng (hết thời gian sử dụng để tính hao mòn, khấu hao tài sản theo quy định về chế độ quản lý, tính hao mòn, khấu hao tài sản cố định áp dụng tại cơ quan, tổ chức, đơn vị quản lý, sử dụng xe ô tô hoặc hết niên hạn, tần suất sử dụng theo quy định của pháp luật).

---
## q237 · dan_chieu · dan_chieu · TRUNG LẬP

Trạng thái: DỰ PHÒNG
Câu hỏi: Khi phát hành hóa đơn điện tử, người kinh doanh cần đảm bảo nội dung nào để đảm bảo tính minh bạch và đúng với quy định pháp luật?

*Đáp án nháp của mô hình:* Hóa đơn điện tử phải ghi đầy đủ nội dung theo quy định của pháp luật về thuế, kế toán và các yêu cầu về thông tin giao dịch như hợp đồng, lệnh vận chuyển, mã khách hàng, đảm bảo phản ánh trung thực nội dung nghiệp vụ kinh tế phát sinh.

**Sàng lọc:** chỉ trả lời được một phần từ gold; không đúng ý đồ nhóm; câu hỏi mơ hồ — Câu hỏi hỏi nội dung bắt buộc, quá rộng; đoạn đích chỉ nêu thông tin tùy chọn ('có thể thể hiện' hợp đồng, lệnh vận chuyển, mã khách hàng) nên không thực sự trả lời ý bắt buộc, còn đoạn nguồn tự trả lời phần chung. · Gợi ý câu hỏi: Hóa đơn điện tử phải đáp ứng yêu cầu gì về định dạng và nội dung ghi trên hóa đơn, và ngoài các nội dung bắt buộc thì tùy đặc điểm giao dịch có thể thể hiện thêm những thông tin nào?

**Gold: 254/2026/NĐ-CP Điều 4 khoản 1 — NGUỒN**

> Hóa đơn điện tử phải theo định dạng chuẩn dữ liệu và phải ghi đầy đủ nội dung theo quy định của pháp luật về thuế, pháp luật về kế toán và quy định tại Điều 10 Nghị định này, bảo đảm phản ánh đầy đủ, trung thực nội dung nghiệp vụ kinh tế phát sinh.

**Gold: 254/2026/NĐ-CP Điều 10 khoản 5 — ĐÍCH**

> Tùy theo đặc điểm, tính chất giao dịch và yêu cầu quản lý, trên hóa đơn có thể thể hiện thông tin về hợp đồng mua bán, lệnh vận chuyển, mã khách hàng và các thông tin khác.

---
## q238 · dan_chieu · dan_chieu · TRUNG LẬP

Trạng thái: DỰ PHÒNG
Câu hỏi: Khi nào thì tòa án phải ra quyết định áp dụng biện pháp khẩn cấp tạm thời trong vụ việc dân sự?

*Đáp án nháp của mô hình:* Khi người yêu cầu không cần thực hiện biện pháp bảo đảm hoặc đã thực hiện biện pháp bảo đảm theo quy định, thì Thẩm phán phải ra quyết định áp dụng biện pháp khẩn cấp tạm thời trong vòng ba ngày kể từ ngày nhận đơn.

**⚠ Kiểm tra tự động:** trả lời được chỉ bằng đoạn nguồn (Đoạn nguồn nêu rõ điều kiện cụ thể khi nào tòa án phải ra quyết định áp dụng biện pháp khẩn cấp tạm thời: trong thời hạn ba ngày kể từ ngày nhận đơn, nếu người yêu cầu không phải thực hiện biện pháp bảo đảm hoặc ngay sau khi thực hiện biện pháp bảo đảm theo quy định tại Điều 120 Bộ luật Dân sự thì Thẩm phán phải ra quyết định áp dụng biện pháp khẩn cấp tạm thời.)
**Sàng lọc:** không đúng ý đồ nhóm — Đoạn nguồn đã tự trả lời (thời hạn 03 ngày, Thẩm phán ra quyết định ngay); đoạn đích về việc Tòa án gửi tiền bảo đảm vào ngân hàng không được câu hỏi dùng tới. · Gợi ý câu hỏi: Khi người yêu cầu áp dụng biện pháp khẩn cấp tạm thời phải nộp một khoản tiền bảo đảm, Thẩm phán phải ra quyết định áp dụng biện pháp khi nào và Tòa án phải xử lý khoản tiền bảo đảm đó ra sao?

**Gold: 24/2004/QH11 Điều 117 khoản 2 — NGUỒN**

> Trong thời hạn ba ngày kể từ ngày nhận đơn, nếu người yêu cầu không phải thực hiện biện pháp bảo đảm hoặc ngay sau khi người đó thực hiện biện pháp bảo đảm quy định tại Điều 120 của Bộ luật này thì Thẩm phán phải ra ngay quyết định áp dụng biện pháp khẩn cấp tạm thời; trường hợp không chấp nhận yêu cầu thì Thẩm phán phải thông báo bằng văn bản và nêu rõ lý do cho người yêu cầu biết.

**Gold: 24/2004/QH11 Điều 120 khoản 2 — ĐÍCH**

> Toà án phải làm thủ tục giao nhận và gửi ngay khoản tiền đó vào ngân hàng vào ngày làm việc tiếp theo.

---
## q239 · dan_chieu · dan_chieu · TRUNG LẬP

Trạng thái: GIỮ
Câu hỏi: Khi nhập khẩu máy móc, thiết bị đã qua sử dụng, nếu doanh nghiệp không cung cấp đầy đủ thông tin, cơ quan có thẩm quyền yêu cầu bổ sung tài liệu nào?

*Đáp án nháp của mô hình:* Cơ quan yêu cầu doanh nghiệp bổ sung bản sao Giấy chứng nhận đăng ký doanh nghiệp có đóng dấu của doanh nghiệp, và trong trường hợp cần thiết, sẽ thẩm xét hồ sơ do tổ chức giám định đề nghị thay đổi hoặc bổ sung phạm vi chỉ định.

**Sàng lọc:** không đúng ý đồ nhóm — Đoạn nguồn tự trả lời (bổ sung bản sao Giấy chứng nhận đăng ký doanh nghiệp có đóng dấu); đoạn đích (thẩm xét hồ sơ khi tổ chức giám định xin thay đổi phạm vi chỉ định) không liên quan đến câu hỏi; đáp án nháp trộn sai nội dung đích vào. · Gợi ý câu hỏi: Khi nhập khẩu máy móc, thiết bị đã qua sử dụng, chứng thư giám định phải do tổ chức nào cấp, và nếu tổ chức giám định đó đề nghị bổ sung phạm vi chỉ định với hồ sơ đầy đủ thì cơ quan chỉ định xử lý ra sao?

**Gold: 56/2026/TT-BKHCN Điều 10 khoản 2 điểm b — NGUỒN**

> Trường hợp không khai thác được thông tin hoặc thông tin khai thác được không đầy đủ, không chính xác, cơ quan có thẩm quyền tiếp nhận, giải quyết thủ tục hành chính yêu cầu doanh nghiệp bổ sung bản sao Giấy chứng nhận đăng ký doanh nghiệp có đóng dấu của doanh nghiệp;
> c) Chứng thư giám định được cấp bởi tổ chức giám định được chỉ định theo quy định tại Điều 12 Thông tư này.

**Gold: 56/2026/TT-BKHCN Điều 12 khoản 4 điểm a — ĐÍCH**

> Trường hợp tổ chức giám định đề nghị thay đổi, bổ sung, thu hẹp phạm vi chỉ định, nếu hồ sơ đăng ký đầy đủ và đúng quy định, cơ quan chỉ định tiến hành thẩm xét hồ sơ, không tổ chức đánh giá năng lực thực tế.

---
## q240 · dan_chieu · dan_chieu · TRUNG LẬP

Trạng thái: DỰ PHÒNG
Câu hỏi: Cơ quan thuế sẽ gửi kết quả giải đáp vướng mắc cho người nộp thuế bằng cách nào?

*Đáp án nháp của mô hình:* Cơ quan thuế sẽ gửi kết quả giải đáp vướng mắc cho người nộp thuế thông qua tin nhắn trên số điện thoại di động đã đăng ký.

**Sàng lọc:** chỉ trả lời được một phần từ gold; câu hỏi mơ hồ — Thiếu bối cảnh giao dịch điện tử và đối tượng cá nhân đăng ký nhận qua điện thoại; gold chỉ nêu tin nhắn thông báo cho trường hợp này, không phải mọi cách gửi kết quả. · Gợi ý câu hỏi: Trong giao dịch thuế điện tử, khi người nộp thuế là cá nhân đã đăng ký nhận kết quả qua điện thoại di động, cơ quan thuế thông báo kết quả giải đáp vướng mắc cho họ bằng cách nào?

**Gold: 19/2021/TT-BTC Điều 33 khoản 3 điểm b — NGUỒN**

> Cơ quan thuế gửi kết quả giải đáp vướng mắc cho người nộp thuế theo quy định tại khoản 2 Điều 5 Thông tư này.

**Gold: 19/2021/TT-BTC Điều 5 khoản 2 điểm a — ĐÍCH**

> Đối với NNT là cá nhân đăng ký nhận kết quả qua điện thoại di động, cơ quan thuế gửi tin nhắn để thông báo cho người nộp thuế biết qua số điện thoại di động đã đăng ký với cơ quan thuế về việc gửi các quyết định, thông báo và văn bản đó.

---
## q241 · dan_chieu · dan_chieu · TRUNG LẬP

Trạng thái: DỰ PHÒNG
Câu hỏi: Khi cần tạm đình chỉ hoạt động của một pháp nhân, thì cần điều kiện gì để quyết định đó được thực hiện?

*Đáp án nháp của mô hình:* Quyết định tạm đình chỉ hoạt động của pháp nhân phải được Viện kiểm sát cùng cấp phê chuẩn trước khi thi hành.

**Sàng lọc:** không đúng ý đồ nhóm; câu hỏi mơ hồ — Đoạn nguồn đã tự trả lời (phải được Viện kiểm sát phê chuẩn); đoạn đích là mảnh 'Trường hợp này, lệnh bắt...' không nêu những người có thẩm quyền nên không bổ sung gì; câu hỏi thiếu bối cảnh tố tụng hình sự. · Gợi ý câu hỏi: Trong tố tụng hình sự đối với pháp nhân, quyết định tạm đình chỉ có thời hạn hoạt động của pháp nhân cần đáp ứng điều kiện gì trước khi thi hành?

**Gold: 101/2015/QH13 Điều 439 khoản 1 — NGUỒN**

> Người có thẩm quyền quy định tại khoản 1 Điều 113 của Bộ luật này có quyền ra quyết định tạm đình chỉ có thời hạn hoạt động của pháp nhân. Quyết định tạm đình chỉ hoạt động của pháp nhân của những người quy định tại điểm a khoản 1 Điều 113 của Bộ luật này phải được Viện kiểm sát cùng cấp phê chuẩn trước khi thi hành.

**Gold: 101/2015/QH13 Điều 113 khoản 1 điểm a — ĐÍCH**

> Trường hợp này, lệnh bắt phải được Viện kiểm sát cùng cấp phê chuẩn trước khi thi hành;

---
## q243 · dan_chieu · dan_chieu · TRUNG LẬP

Trạng thái: GIỮ
Câu hỏi: Nếu có hai hoặc nhiều người có kết quả tuyển dụng bằng nhau và thấp hơn người liền kề, thì ai sẽ quyết định người trúng tuyển?

*Đáp án nháp của mô hình:* Người đứng đầu cơ quan, đơn vị có thẩm quyền tuyển dụng sẽ quyết định người trúng tuyển theo quy định về thứ tự ưu tiên, và nếu vẫn chưa xác định được thì sẽ quyết định thêm theo quy định của cơ quan đó.

**Sàng lọc:** không đúng ý đồ nhóm — Hỏi 'ai quyết định' thì đoạn nguồn đã trả lời (người đứng đầu cơ quan, đơn vị có thẩm quyền tuyển dụng), không cần đoạn đích; câu hỏi diễn đạt lệch ('bằng nhau và thấp hơn người liền kề'). · Gợi ý câu hỏi: Trong tuyển dụng viên chức bằng thi tuyển, nếu có từ hai người trở lên có kết quả thấp hơn liền kề bằng nhau thì người trúng tuyển được xác định thế nào, và nếu vẫn không xác định được theo thứ tự ưu tiên thì ai quyết định?

**Gold: 259/2026/NĐ-CP Điều 20 khoản 4 — NGUỒN**

> Trường hợp có từ 02 người trở lên có kết quả tuyển dụng thấp hơn liền kề bằng nhau thì người đứng đầu cơ quan, đơn vị có thẩm quyền tuyển dụng quyết định người trúng tuyển theo quy định tại khoản 2 Điều 12 Nghị định này (trong trường hợp tổ chức thi tuyển) hoặc quy định tại khoản 2 Điều 14 Nghị định này (trong trường hợp tổ chức xét tuyển).

**Gold: 259/2026/NĐ-CP Điều 12 khoản 2 điểm b — ĐÍCH**

> Trường hợp vẫn chưa xác định được người trúng tuyển theo thứ tự ưu tiên quy định tại khoản này thì người đứng đầu cơ quan, đơn vị có thẩm quyền tuyển dụng quyết định người trúng tuyển.

---
## q259 · dan_chieu · dan_chieu · TRUNG LẬP

Trạng thái: DỰ PHÒNG
Câu hỏi: Khi nào thì phiên họp xét lại quyết định bị kháng cáo, kháng nghị sẽ được tổ chức?

*Đáp án nháp của mô hình:* Khi người phải thi hành hoặc người đại diện hợp pháp của họ yêu cầu Toà án xét đơn vắng mặt họ hoặc đã được triệu tập hợp lệ đến lần thứ hai mà vẫn vắng mặt.

**Sàng lọc:** chỉ trả lời được một phần từ gold; câu hỏi mơ hồ — 'Khi nào được tổ chức' dễ hiểu thành câu hỏi về thời hạn; ý này nằm ở khoản 1 Điều 373 (một tháng), không phải đoạn đích. Đoạn đích chỉ nói khi nào phiên họp vẫn tiến hành dù người phải thi hành vắng mặt. Câu hỏi cũng thiếu ngữ cảnh (đây là thủ tục công nhận phán quyết của Trọng tài nước ngoài). · Gợi ý câu hỏi: Khi xét lại quyết định của Tòa án về yêu cầu công nhận và cho thi hành phán quyết của Trọng tài nước ngoài bị kháng cáo, kháng nghị, nếu người phải thi hành vắng mặt thì phiên họp có vẫn được tiến hành không và trong trường hợp nào?

**Gold: 24/2004/QH11 Điều 373 khoản 2 — NGUỒN**

> Phiên họp xét lại quyết định bị kháng cáo, kháng nghị được tiến hành như phiên họp xét đơn yêu cầu quy định tại Điều 369 của Bộ luật này.

**Gold: 24/2004/QH11 Điều 369 khoản 3 — ĐÍCH**

> Việc xét đơn yêu cầu vẫn được tiến hành, nếu người phải thi hành hoặc người đại diện hợp pháp của họ yêu cầu Toà án xét đơn vắng mặt họ hoặc đã được triệu tập hợp lệ đến lần thứ hai mà vẫn vắng mặt.

---
## q117 · dieu_dai · dieu_dai

Trạng thái: XOÁ
Câu hỏi: Ở cấp tỉnh, ai có quyền quy định cụ thể về quy trình và thành phần tham dự các bước trong việc bổ nhiệm cán bộ lãnh đạo, quản lý thuộc phạm vi phụ trách của đơn vị?

*Đáp án nháp của mô hình:* Chủ tịch Ủy ban nhân dân tỉnh quy định cụ thể về quy trình, thành phần tham dự các bước trong việc bổ nhiệm cán bộ lãnh đạo, quản lý thuộc phạm vi phụ trách của đơn vị.

**⚠ Bản cũ:** gold ở BẢN CŨ, bản mới cũng có trong kho — 170/2025/NĐ-CP Điều 33 ↔ 10/2026/VBHN-NĐ-BNV Điều 72: KHÁC NHIỀU hoặc không còn (chứa 0.47)
**Sàng lọc:** câu hỏi mơ hồ; lộ đáp án / nhắc văn bản — Câu hỏi chép gần nguyên văn gold. Câu hỏi dùng từ 'cán bộ' và không nói rõ là bổ nhiệm công chức nên dễ lẫn với quy định tương tự cho viên chức. Gold viết 'quyết định' thành phần tham dự, không phải 'quy định'. · Gợi ý câu hỏi: Ở cấp tỉnh, ai được giao quy định chi tiết trình tự, thủ tục bổ nhiệm công chức giữ chức vụ lãnh đạo, quản lý và quyết định những ai tham dự các bước của quy trình?

**Gold: 170/2025/NĐ-CP Điều 33 khoản 4 — ĐÍCH**

> 4. Căn cứ điều kiện cụ thể của cơ quan, tổ chức, Bộ trưởng, Thủ trưởng cơ quan ngang Bộ, người đứng đầu tổ chức do Chính phủ, Thủ tướng Chính phủ thành lập mà không phải là đơn vị sự nghiệp công lập, Chủ tịch Ủy ban nhân dân tỉnh, thành phố trực thuộc Trung ương quy định cụ thể về thẩm quyền, quy trình, thủ tục bổ nhiệm, trách nhiệm tổ chức cuộc họp các bước; quyết định cụ thể thành phần tham dự các bước trong quy trình bổ nhiệm các chức vụ, chức danh lãnh đạo, quản lý thuộc phạm vi phụ trách, bảo đảm phù hợp với nguyên tắc theo quy định của cấp có thẩm quyền, quy định tại Nghị định này và quy định khác có liên quan.

---
## q118 · dieu_dai · dieu_dai

Trạng thái: GIỮ
Câu hỏi: Người nộp thuế muốn đăng ký giao dịch với cơ quan thuế bằng cách điện tử thì phải làm thế nào?

*Đáp án nháp của mô hình:* Người nộp thuế cần đăng ký giao dịch thông qua tổ chức cung cấp dịch vụ T-VAN theo quy định.

**Sàng lọc:** chỉ trả lời được một phần từ gold; câu hỏi mơ hồ — Có nhiều cách đăng ký giao dịch điện tử (qua Cổng của Tổng cục Thuế, Cổng dịch vụ công, tổ chức T-VAN). Gold chỉ là câu dẫn chiếu cho trường hợp T-VAN, không chứa nội dung thủ tục. · Gợi ý câu hỏi: Người nộp thuế muốn đăng ký giao dịch điện tử với cơ quan thuế thông qua một tổ chức cung cấp dịch vụ T-VAN thì thực hiện theo thủ tục nào?

**Gold: 19/2021/TT-BTC Điều 10 khoản 3 — ĐÍCH**

> 3. Đăng ký giao dịch với cơ quan thuế bằng phương thức điện tử thông qua tổ chức cung cấp dịch vụ T-VAN: người nộp thuế thực hiện theo quy định tại Điều 42 Thông tư này.

---
## q119 · dieu_dai · dieu_dai

Trạng thái: GIỮ
Câu hỏi: Khi một doanh nghiệp đang giao dịch qua tổ chức cung cấp dịch vụ T-VAN nhưng đó là tổ chức đã ngừng cung cấp dịch vụ, thì doanh nghiệp đó phải làm gì tiếp theo?

*Đáp án nháp của mô hình:* Doanh nghiệp phải chuyển sang giao dịch qua Cổng thông tin điện tử của Tổng cục Thuế hoặc đăng ký giao dịch với một tổ chức cung cấp dịch vụ T-VAN khác.

**Sàng lọc:** lộ đáp án / nhắc văn bản — Câu hỏi lặp gần nguyên văn vế điều kiện của gold; cuối gold dính dòng tiêu đề Mục 2. Gold viết 'được đăng ký' (quyền lựa chọn) chứ không phải nghĩa vụ 'phải làm gì'. · Gợi ý câu hỏi: Nếu đơn vị trung gian truyền nhận dữ liệu thuế điện tử mà doanh nghiệp đang dùng ngừng cung cấp dịch vụ, doanh nghiệp có thể chuyển sang giao dịch điện tử với cơ quan thuế bằng cách nào?

**Gold: 19/2021/TT-BTC Điều 41 khoản 5 — DẪN**

> 5. Ngừng cung cấp dịch vụ T-VAN:

**Gold: 19/2021/TT-BTC Điều 41 khoản 5 điểm c — ĐÍCH**

> c) Người nộp thuế đang giao dịch qua tổ chức cung cấp dịch vụ T-VAN ngừng cung cấp dịch vụ được đăng ký để chuyển sang giao dịch qua Cổng thông tin điện tử của Tổng cục Thuế hoặc đăng ký giao dịch qua tổ chức cung cấp dịch vụ T-VAN khác.

---
## q120 · dieu_dai · dieu_dai

Trạng thái: GIỮ
Câu hỏi: Nếu một doanh nghiệp đã có giấy chứng nhận chất lượng an toàn kỹ thuật và bảo vệ môi trường trước ngày Luật Trật tự, an toàn giao thông đường bộ có hiệu lực, thì giấy chứng nhận đó có giá trị đến khi nào?

*Đáp án nháp của mô hình:* Giấy chứng nhận vẫn có giá trị đến hết thời hạn ghi trên giấy chứng nhận đó.

**Sàng lọc:** lộ đáp án / nhắc văn bản — Câu hỏi nêu tên luật; chủ thể 'doanh nghiệp' không khớp vì gold nói về giấy chứng nhận cấp cho phương tiện. · Gợi ý câu hỏi: Giấy chứng nhận chất lượng an toàn kỹ thuật và bảo vệ môi trường của xe đã được cấp trước khi luật mới về giao thông đường bộ có hiệu lực thì còn được sử dụng đến khi nào?

**Gold: 36/2024/QH15 Điều 89 khoản 6 — ĐÍCH**

> 6. Chứng nhận chất lượng an toàn kỹ thuật và bảo vệ môi trường được cấp trước ngày Luật này có hiệu lực thi hành thì có giá trị sử dụng đến hết thời hạn ghi trên giấy chứng nhận đó.

---
## q121 · dieu_dai · dieu_dai

Trạng thái: GIỮ
Câu hỏi: Người bán hàng hóa bán lưu động cần làm gì khi bán hàng theo quy định?

*Đáp án nháp của mô hình:* Khi bán hàng, phải lập hóa đơn điện tử theo quy định, đồng thời sử dụng phiếu xuất kho kiêm vận chuyển nội bộ như yêu cầu.

**Sàng lọc:** không thấy vấn đề

**Gold: 254/2026/NĐ-CP Điều 6 khoản 3 — DẪN**

> 3. Quy định về áp dụng hóa đơn điện tử, đối với một số trường hợp cụ thể theo yêu cầu quản lý như sau:

**Gold: 254/2026/NĐ-CP Điều 6 khoản 3 điểm đ — ĐÍCH**

> đ) Tổ chức, cá nhân xuất hàng hóa bán lưu động sử dụng phiếu xuất kho kiêm vận chuyển nội bộ theo quy định, khi bán hàng lập hóa đơn điện tử theo quy định.

---
## q122 · dieu_dai · dieu_dai

Trạng thái: GIỮ
Câu hỏi: Ai là người thành lập doanh nghiệp theo quy định?

*Đáp án nháp của mô hình:* Người thành lập doanh nghiệp là cá nhân hoặc tổ chức góp vốn để thành lập doanh nghiệp.

**Sàng lọc:** không thấy vấn đề — Câu hỏi ổn; đáp án nháp thiếu vế 'thành lập' (gold: cá nhân, tổ chức thành lập hoặc góp vốn để thành lập doanh nghiệp).

**Gold: 59/2020/QH14 Điều 4 — DẪN**

> Trong Luật này, các từ ngữ dưới đây được hiểu như sau:

**Gold: 59/2020/QH14 Điều 4 khoản 25 — ĐÍCH**

> 25. Người thành lập doanh nghiệp là cá nhân, tổ chức thành lập hoặc góp vốn để thành lập doanh nghiệp.

---
## q123 · dieu_dai · dieu_dai

Trạng thái: GIỮ
Câu hỏi: Có quy định về việc phân bổ ngân sách cho các quỹ khoa học, công nghệ và đổi mới sáng tạo không?

*Đáp án nháp của mô hình:* Có, ngân sách được phân bổ bằng lệnh chi tiền vào tài khoản của các quỹ tại Kho bạc Nhà nước, cụ thể cho các hoạt động như tài trợ nhiệm vụ, hỗ trợ lãi suất vay và triển khai hoạt động khoa học, công nghệ và đổi mới sáng tạo.

**Cờ tự động:** trùng từ cao (91%)
**Sàng lọc:** câu hỏi mơ hồ — Câu hỏi có/không quá chung, không chỉ ra khía cạnh cần hỏi (hình thức cấp kinh phí về các quỹ). · Gợi ý câu hỏi: Kinh phí tài trợ nhiệm vụ khoa học, công nghệ và đổi mới sáng tạo giao về các quỹ được cấp theo hình thức nào và chuyển vào đâu?

**Gold: 93/2025/QH15 Điều 63 khoản 3 — DẪN**

> 3. Việc phân bổ ngân sách nhà nước chi cho khoa học, công nghệ và đổi mới sáng tạo được thực hiện theo các nguyên tắc sau đây:

**Gold: 93/2025/QH15 Điều 63 khoản 3 điểm đ — ĐÍCH**

> đ) Kinh phí tài trợ, đặt hàng nhiệm vụ khoa học, công nghệ và đổi mới sáng tạo; kinh phí hỗ trợ lãi suất vay, hỗ trợ triển khai hoạt động khoa học, công nghệ và đổi mới sáng tạo giao về các quỹ quy định tại Điều 64 và Điều 65 của Luật này được cấp bằng lệnh chi tiền vào tài khoản của các quỹ tại Kho bạc Nhà nước;

---
## q124 · dieu_dai · dieu_dai

Trạng thái: GIỮ
Câu hỏi: Khi mua trái phiếu doanh nghiệp trên thị trường thứ cấp, nhà đầu tư có quyền yêu cầu người bán cung cấp những thông tin gì?

*Đáp án nháp của mô hình:* Nhà đầu tư có quyền yêu cầu người bán cung cấp đầy đủ nội dung công bố thông tin của doanh nghiệp phát hành theo quy định.

**Sàng lọc:** lộ đáp án / nhắc văn bản — Câu hỏi trùng từ ngữ gần nguyên văn với gold; nên nói rõ là trái phiếu doanh nghiệp riêng lẻ. · Gợi ý câu hỏi: Nhà đầu tư mua lại trái phiếu doanh nghiệp riêng lẻ từ một nhà đầu tư khác có quyền đòi bên bán cung cấp thông tin gì về doanh nghiệp phát hành?

**Gold: 200/2026/NĐ-CP Điều 9 khoản 5 — DẪN**

> 5. Quyền lợi của nhà đầu tư tham gia mua, giao dịch, chuyển nhượng trái phiếu doanh nghiệp riêng lẻ:

**Gold: 200/2026/NĐ-CP Điều 9 khoản 5 điểm d — ĐÍCH**

> d) Được yêu cầu người bán trái phiếu cung cấp đầy đủ nội dung công bố thông tin của doanh nghiệp phát hành theo quy định tại Nghị định này khi mua trái phiếu trên thị trường thứ cấp.

---
## q125 · dieu_dai · dieu_dai

Trạng thái: GIỮ
Câu hỏi: Các tổ chức đã kết nối với Cổng thông tin điện tử của Tổng cục Thuế trước khi Thông tư này có hiệu lực thì cần làm gì nếu vẫn muốn tiếp tục hoạt động?

*Đáp án nháp của mô hình:* Các tổ chức vẫn cần tiếp tục kết nối và đảm bảo đáp ứng các tiêu chuẩn kỹ thuật kết nối theo quy định, nếu không thì phải hoàn thiện để đạt yêu cầu.

**Sàng lọc:** câu hỏi mơ hồ; lộ đáp án / nhắc văn bản — Câu hỏi dùng 'Thông tư này' mà không rõ văn bản nào và chép gần nguyên văn gold. Chủ thể đúng là ngân hàng, tổ chức trung gian thanh toán chứ không phải 'các tổ chức' chung chung; gold nói 'tiếp tục kết nối', không phải 'tiếp tục hoạt động'. · Gợi ý câu hỏi: Ngân hàng đã kết nối hệ thống với cổng thông tin điện tử của cơ quan thuế từ trước khi quy định mới về giao dịch thuế điện tử có hiệu lực thì có được tiếp tục kết nối không, và nếu hệ thống chưa đạt chuẩn kỹ thuật thì phải làm gì?

**Gold: 19/2021/TT-BTC Điều 38 khoản 3 — DẪN**

> 3. Thủ tục kết nối kỹ thuật giữa Cổng thông tin điện tử của Tổng cục Thuế và hệ thống trao đổi thông tin của ngân hàng, tổ chức cung ứng dịch vụ trung gian thanh toán:

**Gold: 19/2021/TT-BTC Điều 38 khoản 3 điểm g — ĐÍCH**

> g) Tổ chức đã tham gia kết nối với Cổng thông tin điện tử của Tổng cục Thuế trước thời điểm Thông tư này có hiệu lực thi hành tiếp tục kết nối nếu vẫn đáp ứng các tiêu chuẩn kỹ thuật kết nối theo quy định tại Thông tư này và Quy chế trao đổi, cung cấp thông tin phục vụ thu NSNN của Tổng cục Thuế; trường hợp không đáp ứng các tiêu chuẩn kỹ thuật kết nối theo quy định thì tổ chức phải hoàn thiện để đảm bảo tiêu chuẩn kỹ thuật kết nối.

---
## q126 · dieu_dai · dieu_dai

Trạng thái: GIỮ
Câu hỏi: Khi tuyển dụng viên chức cho một cơ quan có tổ chức cấu thành, người đứng đầu cơ quan cần căn cứ vào điều kiện nào để quyết định bổ nhiệm và nguồn nhân sự?

*Đáp án nháp của mô hình:* Người đứng đầu cơ quan phải căn cứ vào điều kiện cụ thể của cơ quan, tổ chức để xác định nguồn nhân sự tại chỗ hoặc từ nơi khác, đảm bảo phù hợp với quy định của Đảng và quy định tại Nghị định.

**Sàng lọc:** chỉ trả lời được một phần từ gold; câu hỏi mơ hồ — Gold nói về việc người đứng đầu cơ quan quản lý viên chức quy định thẩm quyền bổ nhiệm và nguyên tắc xác định nguồn nhân sự, không phải tuyển dụng. Câu hỏi lẫn tuyển dụng với bổ nhiệm và hỏi gộp nhiều ý. · Gợi ý câu hỏi: Với đơn vị sự nghiệp công lập có các tổ chức cấu thành, ai quy định cụ thể thẩm quyền bổ nhiệm viên chức quản lý và nguyên tắc xác định nguồn nhân sự tại chỗ hay từ nơi khác?

**Gold: 259/2026/NĐ-CP Điều 31 khoản 4 — ĐÍCH**

> 4. Căn cứ điều kiện cụ thể của cơ quan, tổ chức, người đứng đầu cơ quan quản lý viên chức tại khoản 2 Điều 2 Nghị định này quy định cụ thể về: Thẩm quyền bổ nhiệm; nguyên tắc xác định nguồn nhân sự tại chỗ, nguồn nhân sự từ nơi khác đối với trường hợp đơn vị có tổ chức cấu thành, bảo đảm phù hợp với quy định của Đảng và quy định tại Nghị định này.

---
## q127 · dieu_dai · dieu_dai

Trạng thái: GIỮ
Câu hỏi: Trong thi công xây dựng, khi xảy ra tình trạng công trình hoặc phần kết cấu phụ trợ bị hư hỏng nghiêm trọng đến mức có nguy cơ sập đổ, điều đó được coi là gì?

*Đáp án nháp của mô hình:* Đây được coi là sự cố công trình xây dựng

**Sàng lọc:** không thấy vấn đề

**Gold: 135/2025/QH15 Điều 3 — DẪN**

> Trong Luật này, các từ ngữ dưới đây được hiểu như sau:

**Gold: 135/2025/QH15 Điều 3 khoản 29 — ĐÍCH**

> 29. Sự cố công trình xây dựng là hư hỏng vượt quá giới hạn an toàn cho phép, làm cho công trình xây dựng hoặc kết cấu phụ trợ thi công xây dựng công trình có nguy cơ sập đổ, đã sập đổ một phần hoặc toàn bộ trong quá trình thi công xây dựng và khai thác sử dụng công trình.

---
## q128 · dieu_dai · dieu_dai

Trạng thái: GIỮ
Câu hỏi: Khi đã hoàn thành việc lập báo cáo tài chính và báo cáo nghiệp vụ thi hành án dân sự, doanh nghiệp có được phép chỉnh sửa số liệu trên sổ kế toán không?

*Đáp án nháp của mô hình:* Không, doanh nghiệp không được phép thay đổi thông tin, số liệu trên sổ kế toán sau khi đã khóa sổ và báo cáo đã được nộp cho cơ quan có thẩm quyền.

**Sàng lọc:** chỉ trả lời được một phần từ gold — Chủ thể sai ('doanh nghiệp' thay vì đơn vị thi hành án dân sự) và điều kiện lệch: gold cấm sửa sau khi đã khóa sổ và báo cáo đã nộp cho cơ quan có thẩm quyền, không phải chỉ khi lập xong báo cáo. · Gợi ý câu hỏi: Cơ quan thi hành án dân sự có được sửa số liệu trên sổ kế toán sau khi đã khóa sổ và đã nộp báo cáo tài chính, báo cáo nghiệp vụ thi hành án cho cơ quan có thẩm quyền không?

**Gold: 107/2026/TT-BTC Điều 10 khoản 7 — DẪN**

> 7. Khoá sổ kế toán

**Gold: 107/2026/TT-BTC Điều 10 khoản 7 điểm a — ĐÍCH**

> a) Khoá sổ kế toán là việc cộng sổ để tính ra tổng số phát sinh bên Nợ, bên Có và số dư cuối kỳ của từng tài khoản kế toán hoặc tổng số thu, chi, tồn quỹ trong kỳ. Đơn vị không được phép thay đổi thông tin, số liệu trên sổ kế toán sau khi đã khóa sổ kế toán và báo cáo tài chính, báo cáo nghiệp vụ thi hành án dân sự đã được nộp cho cơ quan có thẩm quyền.

---
## q129 · dieu_dai · dieu_dai

Trạng thái: GIỮ
Câu hỏi: Các doanh nghiệp nhà nước, cơ quan Đảng, Mặt trận và tổ chức chính trị - xã hội nắm giữ 100% vốn điều lệ, đã mua xe ô tô từ nguồn kinh phí hoạt động sản xuất, kinh doanh trước khi có hiệu lực của nghị định này thì quản lý xe như thế nào?

*Đáp án nháp của mô hình:* Việc quản lý, sử dụng và xử lý xe ô tô thực hiện theo quy định của pháp luật về quản lý và đầu tư vốn nhà nước tại doanh nghiệp và các quy định liên quan, không áp dụng theo nghị định này.

**Cờ tự động:** trùng từ cao (91%)
**Sàng lọc:** câu hỏi mơ hồ; lộ đáp án / nhắc văn bản — Câu hỏi chép gần nguyên văn, dùng 'nghị định này' và hiểu sai chủ thể: gold nói về xe của doanh nghiệp do Nhà nước, cơ quan Đảng, Mặt trận, tổ chức chính trị - xã hội nắm 100% vốn, không phải về chính các cơ quan đó. · Gợi ý câu hỏi: Xe ô tô phục vụ công tác chung của doanh nghiệp do Nhà nước nắm giữ 100% vốn điều lệ, mua bằng nguồn kinh phí sản xuất, kinh doanh và đã đưa vào sử dụng trước khi quy định mới về tiêu chuẩn, định mức xe ô tô có hiệu lực, thì được quản lý, xử lý theo pháp luật nào?

**Gold: 379/2026/NĐ-CP Điều 39 khoản 10 — ĐÍCH**

> 10. Đối với xe ô tô phục vụ công tác chung của các doanh nghiệp do Nhà nước, cơ quan Đảng Cộng sản Việt Nam, Mặt trận Tổ quốc Việt Nam, tổ chức chính trị - xã hội nắm giữ 100% vốn điều lệ, bao gồm cả các doanh nghiệp là công ty con và đơn vị trực thuộc đã được mua sắm từ nguồn kinh phí hoạt động sản xuất, kinh doanh của doanh nghiệp và bố trí sử dụng theo quy định trước ngày Nghị định này có hiệu lực thi hành thì việc quản lý, sử dụng và xử lý xe ô tô thực hiện theo quy định của pháp luật về quản lý và đầu tư vốn nhà nước tại doanh nghiệp và pháp luật có liên quan; không thực hiện theo quy định tại Nghị định này.

---
## q130 · dieu_dai · dieu_dai

Trạng thái: GIỮ
Câu hỏi: Người lao động mua hàng hóa, dịch vụ tại Việt Nam để sử dụng trong hoạt động ngoại giao có được hoàn lại thuế giá trị gia tăng đã trả hay không?

*Đáp án nháp của mô hình:* Có, người lao động mua hàng hóa, dịch vụ tại Việt Nam để sử dụng trong hoạt động ngoại giao được hoàn lại số thuế giá trị gia tăng đã trả, cụ thể là số thuế ghi trên hóa đơn hoặc chứng từ thanh toán.

**Sàng lọc:** chỉ trả lời được một phần từ gold — Chủ thể sai: gold áp dụng cho đối tượng được hưởng quyền ưu đãi, miễn trừ ngoại giao, không phải 'người lao động' mua hàng cho 'hoạt động ngoại giao'. · Gợi ý câu hỏi: Người được hưởng quyền ưu đãi, miễn trừ ngoại giao mua hàng hóa, dịch vụ tại Việt Nam để sử dụng có được hoàn thuế giá trị gia tăng không, và số thuế được hoàn căn cứ vào chứng từ nào?

**Gold: 48/2024/QH15 Điều 15 khoản 7 — ĐÍCH**

> 7. Đối tượng được hưởng quyền ưu đãi miễn trừ ngoại giao theo quy định của pháp luật về ngoại giao mua hàng hóa, dịch vụ tại Việt Nam để sử dụng được hoàn số thuế giá trị gia tăng đã trả ghi trên hóa đơn giá trị gia tăng hoặc trên chứng từ thanh toán ghi giá thanh toán đã có thuế giá trị gia tăng.

---
## q131 · dieu_dai · dieu_dai

Trạng thái: DỰ PHÒNG
Câu hỏi: Người vận hành chuyến bay cần nộp đề nghị cấp, sửa đổi hoặc hủy bỏ phép bay đi, đến và bay qua lãnh thổ Việt Nam trước bao nhiêu ngày so với ngày dự kiến thực hiện chuyến bay?

*Đáp án nháp của mô hình:* Chậm nhất 07 ngày làm việc trước ngày dự kiến thực hiện chuyến bay

**Sàng lọc:** chỉ trả lời được một phần từ gold; câu hỏi mơ hồ — Gold chỉ quy định 07 ngày làm việc cho nhóm chuyến bay nêu tại một khoản khác (các điểm sau có thể có thời hạn khác), trong khi câu hỏi hỏi chung cho mọi chuyến bay. · Gợi ý câu hỏi: Đối với nhóm chuyến bay đầu tiên được liệt kê trong quy định về phép bay (cần nêu rõ loại chuyến bay), đề nghị cấp, sửa đổi, hủy bỏ phép bay đi, đến và bay qua lãnh thổ Việt Nam phải nộp chậm nhất bao lâu trước ngày dự kiến thực hiện chuyến bay?

**Gold: 222/2026/NĐ-CP Điều 17 khoản 3 — DẪN**

> 3. Thời hạn nộp đề nghị cấp, sửa đổi, hủy bỏ phép bay đi, đến và bay qua lãnh thổ Việt Nam:

**Gold: 222/2026/NĐ-CP Điều 17 khoản 3 điểm a — ĐÍCH**

> a) Chậm nhất 07 ngày làm việc trước ngày dự kiến thực hiện chuyến bay đối với các chuyến bay nêu tại khoản 1 Điều 16 của Nghị định này;

---
## q245 · dieu_dai · dieu_dai · TRUNG LẬP

Trạng thái: GIỮ
Câu hỏi: Khi cần cắm mốc giới cho khu vực bảo vệ di tích, thì cơ quan nào phải chịu trách nhiệm tổ chức hoặc ủy quyền thực hiện việc này?

*Đáp án nháp của mô hình:* Chủ tịch Ủy ban nhân dân cấp tỉnh

**Sàng lọc:** lộ đáp án / nhắc văn bản — Câu hỏi chép gần nguyên văn cụm 'chịu trách nhiệm tổ chức hoặc ủy quyền... cắm mốc giới khu vực bảo vệ di tích'; hỏi 'cơ quan nào' trong khi đáp án là một chức danh. · Gợi ý câu hỏi: Ai chịu trách nhiệm việc cắm mốc ranh giới vùng bảo vệ di tích và có thể giao cho những người nào thực hiện thay?

**Gold: 45/2024/QH15 Điều 27 khoản 6 — ĐÍCH**

> Hồ sơ trình Thủ tướng Chính phủ phải có ý kiến bằng văn bản của Hội đồng Di sản văn hóa quốc gia.
> 7. Chủ tịch Ủy ban nhân dân cấp tỉnh chịu trách nhiệm tổ chức hoặc ủy quyền cho người đứng đầu cơ quan chuyên môn về văn hóa cấp tỉnh hoặc Chủ tịch Ủy ban nhân dân cấp huyện thực hiện cắm mốc giới khu vực bảo vệ di tích.

---
## q246 · dieu_dai · dieu_dai · TRUNG LẬP

Trạng thái: GIỮ
Câu hỏi: Nếu người nộp thuế không chấp nhận được thông báo từ ngân hàng hoặc tổ chức thanh toán về việc nộp thuế điện tử, họ nên làm gì tiếp theo?

*Đáp án nháp của mô hình:* Người nộp thuế có thể căn cứ vào thông báo đó để hoàn chỉnh thông tin đăng ký hoặc liên hệ với cơ quan thuế, ngân hàng hoặc tổ chức thanh toán nơi có tài khoản để được hỗ trợ hướng dẫn.

**Sàng lọc:** không thấy vấn đề — Câu hỏi hiểu sai chủ thể: gold là ngân hàng hoặc tổ chức trung gian thanh toán không chấp nhận đăng ký nộp thuế điện tử, không phải người nộp thuế 'không chấp nhận được thông báo'. · Gợi ý câu hỏi: Khi ngân hàng hoặc tổ chức cung ứng dịch vụ trung gian thanh toán thông báo không chấp nhận đăng ký nộp thuế điện tử, người nộp thuế cần làm gì?

**Gold: 19/2021/TT-BTC Điều 10 khoản 5 — ĐÍCH**

> Trường hợp không chấp nhận, người nộp thuế căn cứ thông báo không chấp nhận nộp thuế điện tử của ngân hàng hoặc tổ chức cung ứng dịch vụ trung gian thanh toán để hoàn chỉnh thông tin đăng ký hoặc liên hệ với cơ quan thuế quản lý, ngân hàng hoặc tổ chức cung ứng dịch vụ trung gian thanh toán nơi có tài khoản để được hướng dẫn, hỗ trợ.

---
## q247 · dieu_dai · dieu_dai · TRUNG LẬP

Trạng thái: GIỮ
Câu hỏi: Khi đánh giá việc thực hiện nhiệm vụ trong lĩnh vực khoa học, công nghệ và đổi mới sáng tạo, người ta yêu cầu các cơ quan nào phải giải trình trách nhiệm?

*Đáp án nháp của mô hình:* Các Bộ, cơ quan ngang Bộ, cơ quan thuộc Chính phủ, cơ quan khác ở trung ương và địa phương phải giải trình trách nhiệm.

**Sàng lọc:** không thấy vấn đề — Câu hỏi gán thêm bối cảnh 'đánh giá việc thực hiện nhiệm vụ' không có trong gold; bối cảnh thực tế là nguyên tắc phân bổ ngân sách nhà nước chi cho khoa học, công nghệ và đổi mới sáng tạo. · Gợi ý câu hỏi: Theo nguyên tắc phân bổ ngân sách nhà nước chi cho khoa học, công nghệ và đổi mới sáng tạo, việc đánh giá gắn với trách nhiệm giải trình của những cơ quan nào?

**Gold: 93/2025/QH15 Điều 63 khoản 3 — DẪN**

> 3. Việc phân bổ ngân sách nhà nước chi cho khoa học, công nghệ và đổi mới sáng tạo được thực hiện theo các nguyên tắc sau đây:

**Gold: 93/2025/QH15 Điều 63 khoản 3 điểm c — ĐÍCH**

> Việc đánh giá gắn với trách nhiệm giải trình của Bộ, cơ quan ngang Bộ, cơ quan thuộc Chính phủ, cơ quan khác ở trung ương và địa phương;

---
## q248 · dieu_dai · dieu_dai · TRUNG LẬP

Trạng thái: GIỮ
Câu hỏi: Đối với doanh nghiệp phát hành trái phiếu chuyển đổi hoặc trái phiếu kèm chứng quyền riêng lẻ, cần điều kiện gì để được phê duyệt phương án phát hành?

*Đáp án nháp của mô hình:* Phương án phải được Đại hội đồng cổ đông phê duyệt theo quy định tại Luật Doanh nghiệp.

**Sàng lọc:** không thấy vấn đề — Gold nói về thẩm quyền phê duyệt (Đại hội đồng cổ đông), câu hỏi lại hỏi 'cần điều kiện gì' nên hơi lệch ý. · Gợi ý câu hỏi: Phương án chào bán riêng lẻ trái phiếu chuyển đổi hoặc trái phiếu kèm chứng quyền phải được cơ quan nào của doanh nghiệp phê duyệt, và việc biểu quyết thông qua thực hiện theo luật nào?

**Gold: 200/2026/NĐ-CP Điều 10 khoản 2 — DẪN**

> 2. Thẩm quyền phê duyệt và chấp thuận phương án phát hành trái phiếu:

**Gold: 200/2026/NĐ-CP Điều 10 khoản 2 điểm a — ĐÍCH**

> Phương án chào bán trái phiếu chuyển đổi riêng lẻ và chào bán trái phiếu kèm chứng quyền riêng lẻ phải được Đại hội đồng cổ đông phê duyệt. Việc biểu quyết thông qua Nghị quyết phê duyệt phương án phát hành thực hiện theo quy định tại Luật Doanh nghiệp số 59/2020/QH14.

---
## q249 · dieu_dai · dieu_dai · TRUNG LẬP

Trạng thái: GIỮ
Câu hỏi: Nếu một trường dự bị đại học vi phạm quy định, thì cơ quan nào sẽ xem xét và quyết định đình chỉ tuyển sinh hoặc đình chỉ hoạt động giáo dục?

*Đáp án nháp của mô hình:* Bộ trưởng Bộ Giáo dục và Đào tạo sẽ căn cứ vào kết quả kiểm tra để quyết định đình chỉ tuyển sinh hoặc đình chỉ hoạt động giáo dục.

**Sàng lọc:** không thấy vấn đề — Câu hỏi dùng lại khá sát cụm 'xem xét, quyết định đình chỉ tuyển sinh hoặc đình chỉ hoạt động giáo dục'; đáp án là chức danh (Bộ trưởng) chứ không phải 'cơ quan'; bỏ qua ý thời hạn 05 ngày làm việc. · Gợi ý câu hỏi: Khi đã đủ căn cứ để ngừng tuyển sinh hoặc ngừng hoạt động giáo dục của trường dự bị đại học, ai có thẩm quyền quyết định và phải quyết định trong thời hạn bao lâu?

**Gold: 360/2026/NĐ-CP Điều 35 khoản 3 — DẪN**

> 3. Đình chỉ tuyển sinh, đình chỉ hoạt động giáo dục:

**Gold: 360/2026/NĐ-CP Điều 35 khoản 3 điểm c — ĐÍCH**

> Trong thời hạn 05 ngày làm việc kể từ ngày đủ căn cứ đình chỉ, Bộ trưởng Bộ Giáo dục và Đào tạo căn cứ kết quả kiểm tra xem xét, quyết định đình chỉ tuyển sinh hoặc đình chỉ hoạt động giáo dục đối với trường dự bị đại học.

---
## q250 · dieu_dai · dieu_dai · TRUNG LẬP

Trạng thái: DỰ PHÒNG
Câu hỏi: Với tàu bay của doanh nghiệp Việt Nam, trong trường hợp nào thì Cục Hàng không Việt Nam có thể xem xét cấp phép bay đặc biệt?

*Đáp án nháp của mô hình:* Khi tàu bay đã được đánh giá đủ điều kiện bay sau khi khắc phục sự cố kỹ thuật và hồ sơ được xem xét kỹ lưỡng.

**Sàng lọc:** chỉ trả lời được một phần từ gold — Gold không liệt kê 'trường hợp nào' mà chỉ nói căn cứ (theo bộ quy chế an toàn tàu bay hoặc sau khi đánh giá hồ sơ khắc phục sự cố kỹ thuật); gold dùng 'người khai thác Việt Nam' chứ không phải 'doanh nghiệp'. · Gợi ý câu hỏi: Trong các trường hợp đặc biệt đối với tàu bay của người khai thác Việt Nam, Cục Hàng không Việt Nam xem xét cấp phép bay đặc biệt hoặc cấp phép bay dựa trên cơ sở nào?

**Gold: 222/2026/NĐ-CP Điều 17 khoản 6 — DẪN**

> 6. Các trường hợp đặc biệt:

**Gold: 222/2026/NĐ-CP Điều 17 khoản 6 điểm d — ĐÍCH**

> Trường hợp tàu bay của người khai thác Việt Nam, Cục Hàng không Việt Nam xem xét cấp phép bay đặc biệt (Special Flight Permit hoặc Ferry Flight Permit) theo quy định của bộ quy chế an toàn tàu bay hoặc xem xét cấp phép bay sau khi đánh giá hồ sơ khắc phục sự cố kỹ thuật, đánh giá tình trạng đủ điều kiện bay của tàu bay;

---
## q260 · dieu_dai · dieu_dai · TRUNG LẬP

Trạng thái: GIỮ
Câu hỏi: Khi các tổ chức tín dụng, chi nhánh ngân hàng nước ngoài và công ty quản lý quỹ đầu tư chứng khoán tham gia mua hoặc giao dịch trái phiếu doanh nghiệp riêng lẻ, họ phải tuân thủ điều gì?

*Đáp án nháp của mô hình:* Phải thực hiện theo quy định của pháp luật chuyên ngành

**Sàng lọc:** câu hỏi mơ hồ; lộ đáp án / nhắc văn bản — Câu hỏi chép gần nguyên văn chủ thể và cụm từ của gold ('tổ chức tín dụng, chi nhánh ngân hàng nước ngoài và công ty quản lý quỹ đầu tư chứng khoán', 'mua, giao dịch trái phiếu doanh nghiệp riêng lẻ'). 'Phải tuân thủ điều gì' quá rộng vì các điểm a–d của khoản 4 cũng áp dụng cho họ; gold chỉ là nghĩa vụ 'còn phải' bổ sung. · Gợi ý câu hỏi: Ngoài các trách nhiệm chung của nhà đầu tư, ngân hàng và công ty quản lý quỹ khi mua bán trái phiếu doanh nghiệp phát hành riêng lẻ còn phải tuân theo quy định nào nữa?

**Gold: 200/2026/NĐ-CP Điều 9 khoản 4 — DẪN**

> 4. Trách nhiệm của nhà đầu tư tham gia mua, giao dịch, chuyển nhượng trái phiếu doanh nghiệp riêng lẻ:

**Gold: 200/2026/NĐ-CP Điều 9 khoản 4 điểm e — ĐÍCH**

> Việc mua, giao dịch, chuyển nhượng trái phiếu doanh nghiệp riêng lẻ của các tổ chức tín dụng, chi nhánh ngân hàng nước ngoài và công ty quản lý quỹ đầu tư chứng khoán còn phải thực hiện theo quy định của pháp luật chuyên ngành;

---
## q139 · khong_co_dieu · doan

Trạng thái: GIỮ
Câu hỏi: Cán bộ, công chức, viên chức được cấp địa chỉ thư điện tử như thế nào?

*Đáp án nháp của mô hình:* Được bảo đảm cung cấp địa chỉ thư điện tử có tên miền .gov.vn.

**Sàng lọc:** câu hỏi mơ hồ — Câu hỏi thiếu ngữ cảnh (kế hoạch giai đoạn 2009-2010), yêu cầu thư điện tử .gov.vn có thể xuất hiện ở nhiều văn bản khác. · Gợi ý câu hỏi: Theo kết luận về kế hoạch ứng dụng công nghệ thông tin giai đoạn 2009-2010, yêu cầu về địa chỉ thư điện tử cấp cho cán bộ, công chức, viên chức là gì?

**Gold: 05/TB-VPCP (đoạn)**

> - Bảo đảm cung cấp cho cán bộ, công chức, viên chức địa chỉ thư điện tử với tên miền có đuôi .gov.vn.

---
## q140 · khong_co_dieu · doan

Trạng thái: GIỮ
Câu hỏi: Có cần bố trí người làm công tác bảo vệ, chăm sóc trẻ em tại các xã, phường, thị trấn không?

*Đáp án nháp của mô hình:* Có, các địa phương được yêu cầu bố trí người làm công tác bảo vệ, chăm sóc trẻ em tại xã, phường, thị trấn.

**Sàng lọc:** lộ đáp án / nhắc văn bản — Câu có/không chép gần nguyên cụm từ trong gold nên dễ đoán, lại bỏ qua ý chính là cơ quan chủ trì hướng dẫn. · Gợi ý câu hỏi: Cơ quan nào chủ trì hướng dẫn các địa phương bố trí người làm công tác bảo vệ, chăm sóc trẻ em ở cấp xã, và phối hợp với cơ quan nào?

**Gold: 1408/CT-TTg (đoạn)**

> 8. Bộ Nội vụ chủ trì, phối hợp với Bộ Lao động - Thương binh và Xã hội và các cơ quan liên quan hướng dẫn các địa phương bố trí người làm công tác bảo vệ, chăm sóc trẻ em ở xã, phường, thị trấn.

---
## q141 · khong_co_dieu · doan

Trạng thái: GIỮ
Câu hỏi: Các địa phương cần làm gì để triển khai kế hoạch trồng rừng mới trong giai đoạn 2009-2010?

*Đáp án nháp của mô hình:* Các địa phương cần rà soát và xây dựng dự án đầu tư bảo vệ và phát triển rừng, xác định rõ địa điểm cụ thể trên bản đồ và thực địa, cùng với giải pháp và nguồn lực để tổ chức thực hiện kế hoạch trồng rừng mới cho hai năm 2009 và 2010.

**Sàng lọc:** không thấy vấn đề

**Gold: 334/CT-TTg (đoạn)**

> 2. Căn cứ các kết quả đã thực hiện đến hết năm 2008 và nhu cầu bảo vệ phát triển rừng theo quy hoạch, các địa phương chỉ đạo việc rà soát, xây dựng các dự án đầu tư bảo vệ và phát triển rừng, dự kiến kế hoạch khoán bảo vệ rừng, khoanh nuôi tái sinh rừng, trồng rừng mới … cho 2 năm 2009 và 2010, có địa điểm, địa danh cụ thể trên bản đồ và trên thực địa trong các dự án cơ sở; có giải pháp, tính toán bố trí nguồn lực để tổ chức thực hiện dự án có kết quả tại địa phương mình.

---
## q142 · khong_co_dieu · doan

Trạng thái: GIỮ
Câu hỏi: Trong các tháng cuối năm 2013, doanh nghiệp và cơ quan nhà nước cần làm gì để chi ngân sách hiệu quả và tiết kiệm?

*Đáp án nháp của mô hình:* Cần điều hành chi ngân sách nhà nước chặt chẽ, hiệu quả và tiết kiệm theo đúng hướng dẫn của Thủ tướng Chính phủ.

**Sàng lọc:** chỉ trả lời được một phần từ gold; lộ đáp án / nhắc văn bản; gold đáng ngờ — Gold chỉ là dòng tiêu đề của mục 2, chưa có biện pháp cụ thể; câu hỏi chép 'hiệu quả và tiết kiệm' nên đáp án lặp lại câu hỏi, và 'doanh nghiệp' không phải chủ thể điều hành chi ngân sách. · Gợi ý câu hỏi: Trong các tháng cuối năm 2013, việc điều hành chi ngân sách nhà nước phải thực hiện theo chỉ thị nào của Thủ tướng Chính phủ?

**Gold: 04/CT-BTC (đoạn)**

> 2. Tiếp tục điều hành chi ngân sách nhà nước chặt chẽ, hiệu quả và tiết kiệm theo đúng Chỉ thị số 09/CT-TTg của Thủ tướng Chính phủ

---
## q143 · khong_co_dieu · doan

Trạng thái: GIỮ
Câu hỏi: Khi thực hiện dự án trồng mới 5 triệu ha rừng, địa phương cần làm gì để đảm bảo việc giao đất lâm nghiệp cho các hộ gia đình, cá nhân và cộng đồng?

*Đáp án nháp của mô hình:* Cần đảm bảo từng diện tích đất có chủ cụ thể để thực hiện các nhiệm vụ còn lại của dự án.

**Sàng lọc:** không thấy vấn đề — Gold giao việc hướng dẫn cho hai Bộ chứ không phải địa phương tự làm; câu hỏi bỏ sót đối tượng tổ chức và cộng đồng thôn, bản. · Gợi ý câu hỏi: Trong thực hiện dự án trồng mới 5 triệu ha rừng, việc giao đất lâm nghiệp cho tổ chức, hộ gia đình, cá nhân và cộng đồng thôn, bản phải bảo đảm yêu cầu gì?

**Gold: 334/CT-TTg (đoạn)**

> 10. Bộ Tài nguyên và Môi trường phối hợp với Bộ Nông nghiệp và Phát triển nông thôn hướng dẫn các địa phương thực hiện việc giao đất lâm nghiệp cho các tổ chức, hộ gia đình, cá nhân và cộng đồng thôn, bản, bảo đảm từng diện tích đất có chủ cụ thể để thực hiện các nhiệm vụ còn lại của dự án trồng mới 5 triệu ha rừng.

---
## q144 · khong_co_dieu · doan

Trạng thái: GIỮ
Câu hỏi: Công an các cấp cần làm gì để phòng chống tội phạm xâm hại trẻ em và các hành vi sai phạm liên quan đến việc làm con nuôi người nước ngoài?

*Đáp án nháp của mô hình:* Công an các cấp cần xây dựng và thực hiện kế hoạch đấu tranh quyết liệt, liên tục với tội phạm xâm hại trẻ em và các hành vi sai phạm trong lứa tuổi chưa thành niên, đồng thời tăng cường xác minh hồ sơ của trẻ em có nguồn gốc không rõ ràng được giới thiệu làm con nuôi người nước ngoài và nghiêm khắc xử lý các hành vi làm giả hồ sơ, hối lộ liên quan đến việc giải quyết con nuôi.

**Sàng lọc:** không thấy vấn đề

**Gold: 1408/CT-TTg (đoạn)**

> b) Chỉ đạo Công an các cấp: xây dựng và thực hiện các kế hoạch đấu tranh quyết liệt, liên tục với tội phạm xâm hại trẻ em, tội phạm trong lứa tuổi chưa thành niên; tăng cường công tác xác minh đối với hồ sơ của trẻ em có nguồn gốc không rõ ràng nhưng được giới thiệu làm con nuôi người nước ngoài; nghiêm khắc xử lý các hành vi làm giả hồ sơ về nguồn gốc của trẻ em, đưa hối lộ, nhận hối lộ liên quan đến việc giải quyết cho trẻ em làm con nuôi người nước ngoài hoặc lợi dụng việc giới thiệu, giải quyết, đăng ký cho trẻ em làm con nuôi người nước ngoài để trục lợi, thu lợi vật chất bất hợp pháp.

---
## q145 · khong_co_dieu · doan

Trạng thái: GIỮ
Câu hỏi: Làm thế nào để lập kế hoạch sửa chữa và nâng cấp các hồ đập trong tỉnh trước khi mùa mưa lũ đến?

*Đáp án nháp của mô hình:* Cần rà soát toàn bộ các hồ đập trong tỉnh và lập kế hoạch sửa chữa, nâng cấp trong những năm tới để báo cáo lên Bộ Nông nghiệp và Phát triển nông thôn.

**Sàng lọc:** chỉ trả lời được một phần từ gold; gold đáng ngờ — Gold là câu dẫn kết thúc bằng 'cụ thể như sau:' nên thiếu nội dung chi tiết; 'trước mùa mưa lũ' không khớp với 'trong những năm tới' trong gold. · Gợi ý câu hỏi: Sau khi rà soát toàn bộ hồ đập trong tỉnh, kế hoạch sửa chữa, nâng cấp hồ đập phải được báo cáo về cơ quan nào?

**Gold: 242/CT-BNN-TL (đoạn)**

> 6. Rà soát lại toàn bộ các hồ đập trong tỉnh nhằm lập kế hoạch sửa chữa, nâng cấp trong những năm tới báo cáo về Bộ Nông nghiệp và Phát triển nông thôn (Cục Thủy lợi), cụ thể như sau:

---
## q146 · khong_co_dieu · doan

Trạng thái: GIỮ
Câu hỏi: Có cần chuẩn bị kinh phí cho các dự án ứng dụng công nghệ thông tin cấp ngành trong giai đoạn 2009 - 2010 không?

*Đáp án nháp của mô hình:* Có, đã xác định rõ dự toán kinh phí cho các dự án ứng dụng công nghệ thông tin cấp ngành trong giai đoạn 2009 - 2010.

**Sàng lọc:** lộ đáp án / nhắc văn bản — Câu có/không chép cụm từ gold nên dễ đoán; đáp án nháp sai khi ghi 'đã xác định', trong khi gold là yêu cầu phải xây dựng đề án và xác định. · Gợi ý câu hỏi: Kế hoạch giai đoạn 2009-2010 yêu cầu làm gì đối với các dự án ứng dụng công nghệ thông tin đặc thù cấp ngành được triển khai tới địa phương?

**Gold: 05/TB-VPCP (đoạn)**

> - Xây dựng Đề án chuẩn bị đầu tư cho một số dự án ứng dụng công nghệ thông tin đặc thù cấp ngành được triển khai tới địa phương, xác định rõ dự toán kinh phí cho các dự án này trong giai đoạn 2009 - 2010.

---
## q147 · khong_co_dieu · doan

Trạng thái: GIỮ
Câu hỏi: Tại sao Bộ Tài chính phải sửa đổi Thông tư số 97/2004/TT-BTC về quản lý chi ngân sách bằng ngoại tệ?

*Đáp án nháp của mô hình:* Vì trong quá trình xây dựng và ban hành, đã phát hiện một số sai sót tại đoạn đầu và Mục III của Thông tư.

**Sàng lọc:** lộ đáp án / nhắc văn bản; gold đáng ngờ — Câu hỏi nêu số hiệu thông tư bị đính chính và gọi sai thành 'sửa đổi'; gold là đoạn mở đầu công văn, còn nội dung đính chính nằm ở đoạn sau. · Gợi ý câu hỏi: Thông tư năm 2004 hướng dẫn chế độ quản lý, chi trả, thanh toán các khoản chi ngân sách nhà nước bằng ngoại tệ qua Kho bạc Nhà nước bị đính chính vì lý do gì?

**Gold: 15642/TC-PC (đoạn)**

> Ngày 13 tháng 10 năm 2004, Bộ Tài chính đã ban hành Thông tư số 97/2004/TT-BTC hướng dẫn chế độ quản lý, chi trả, thanh toán các khoản chi ngân sách nhà nước bằng ngoại tệ qua Kho bạc Nhà nước. Trong quá trình xây dựng và ban hành văn bản nêu trên đã có một số sai sót tại đoạn đầu, Mục III của Thông tư. Nay xin được đính chính như sau:

---
## q148 · khong_co_dieu · doan

Trạng thái: GIỮ
Câu hỏi: Tại sao một số quyết định do Bộ Tài chính ban hành lại bị loại khỏi danh mục văn bản quy phạm pháp luật?

*Đáp án nháp của mô hình:* Vì những quyết định đó đã hết hiệu lực pháp luật, cụ thể là các quyết định được nêu trong danh mục đã được loại bỏ do hết hiệu lực đến ngày 31/12/2003.

**Sàng lọc:** KHÔNG trả lời được từ gold — Gold chỉ liệt kê các điểm bị bỏ khỏi danh mục, không nêu lý do, nên câu hỏi 'tại sao' không trả lời được và đáp án nháp là bịa. · Gợi ý câu hỏi: Việc đính chính danh mục văn bản quy phạm pháp luật do Bộ Tài chính ban hành hết hiệu lực đến 31/12/2003 đã bỏ những quyết định nào khỏi danh mục?

**Gold: 9367 TC/PC (đoạn)**

> 1. Bỏ các điểm theo thứ tự quy định tại Danh mục như sau: điểm 54 (Quyết định số 164/2000/QĐ-BTC ngày 10/10/2000), điểm 115 (Quyết định số 214/2003/QĐ-BTC ngày 18/12/2003) và điểm 121 (Quyết định số 01/2000/QĐ-BVGCP ngày 5/1/2000).

---
## q149 · khong_co_dieu · doan

Trạng thái: DỰ PHÒNG
Câu hỏi: Nếu có tiết kiệm chi ngân sách trong năm 2013, thì nguồn tiết kiệm đó sẽ được sử dụng như thế nào?

*Đáp án nháp của mô hình:* Nguồn tiết kiệm sẽ được bổ sung vào dự phòng ngân sách cấp đó và sử dụng theo quy định của Thủ tướng Chính phủ và hướng dẫn của Bộ Tài chính.

**Sàng lọc:** không thấy vấn đề

**Gold: 04/CT-BTC (đoạn)**

> Toàn bộ nguồn vốn đầu tư thu hồi, số tiết kiệm và cắt giảm dự toán chi thường xuyên năm 2013 thuộc ngân sách cấp nào thì bổ sung dự phòng ngân sách cấp đó và sử dụng theo quy định của Thủ tướng Chính phủ, hướng dẫn của Bộ Tài chính.

---
## q251 · khong_co_dieu · doan · TRUNG LẬP

Trạng thái: GIỮ
Câu hỏi: Nếu phát hiện doanh nghiệp sản xuất hoặc kinh doanh phân bón, thuốc bảo vệ thực vật giả, thì có thể xử lý như thế nào?

*Đáp án nháp của mô hình:* Có thể tạm đình chỉ kinh doanh, đình chỉ kinh doanh đến 12 tháng hoặc đình chỉ kinh doanh không thời hạn trên 12 tháng, tùy theo mức độ vi phạm.

**Sàng lọc:** chỉ trả lời được một phần từ gold; câu hỏi mơ hồ — Gold chỉ nói 'các hành vi gian lận nêu trên', không xác nhận là phân bón hay thuốc bảo vệ thực vật giả, và mở đầu bằng 'Đồng thời' nên còn biện pháp khác; câu hỏi chung chung dễ trùng với các nghị định xử phạt. · Gợi ý câu hỏi: Trong kết luận về chống gian lận trong kinh doanh xăng dầu và phân bón, thuốc bảo vệ thực vật giả, những hình thức đình chỉ kinh doanh nào được yêu cầu áp dụng và Bộ Tư pháp được giao việc gì khi cần thiết?

**Gold: 259/TB-VPCP (đoạn)**

> Đồng thời, áp dụng các hình thức tạm đình chỉ kinh doanh, đình chỉ kinh doanh đến 12 tháng và đình chỉ kinh doanh không thời hạn trên 12 tháng đối với các hành vi gian lận nêu trên; trường hợp cần thiết, Bộ Tư pháp nghiên cứu, trình Chính phủ điều chỉnh các quy định liên quan của luật pháp hiện hành về xử lý vi phạm hành chính.

---
## q252 · khong_co_dieu · doan · TRUNG LẬP

Trạng thái: GIỮ
Câu hỏi: Thông tư mới có hiệu lực từ ngày nào?

*Đáp án nháp của mô hình:* Sau 15 ngày kể từ ngày đăng Công báo

**Sàng lọc:** chỉ trả lời được một phần từ gold; câu hỏi mơ hồ — 'Thông tư mới' không xác định là thông tư nào; hỏi 'từ ngày nào' nhưng gold chỉ cho mốc tương đối (sau 15 ngày kể từ ngày đăng Công báo); đáp án trùng với q253. · Gợi ý câu hỏi: Bộ Tài chính đã đính chính điều khoản hiệu lực của một thông tư vốn ghi là thực hiện từ niên độ ngân sách năm 2004; sau đính chính, thông tư đó có hiệu lực khi nào?

**Gold: 15642/TC-PC (đoạn)**

> Các nội dung quy định tại Thông tư này được thực hiện từ niên độ ngân sách năm 2004; Thay thế Thông tư số 40/2001/TT-BTC ngày 5/6/2001 của Bộ Tài chính" thành đoạn: "Thông tư này có hiệu lực sau 15 ngày kể từ ngày đăng Công báo; Thay thế Thông tư số 40/2001/TT-BTC ngày 5/6/2001 của Bộ Tài chính".

---
## q253 · khong_co_dieu · doan · TRUNG LẬP

Trạng thái: GIỮ
Câu hỏi: Thông tư của Bộ Tài chính có hiệu lực thi hành sau bao lâu kể từ ngày đăng Công báo?

*Đáp án nháp của mô hình:* Sau 15 ngày kể từ ngày đăng Công báo

**Sàng lọc:** câu hỏi mơ hồ — Câu hỏi đúng với hầu hết thông tư của Bộ Tài chính, không có chi tiết phân biệt; đáp án trùng với q252. · Gợi ý câu hỏi: Theo văn bản đính chính của Bộ Tài chính về mục hiệu lực của một thông tư năm 2004, thông tư đó có hiệu lực khi nào và các văn bản hướng dẫn trước đây trái với nó được xử lý ra sao?

**Gold: 15638/TC-PC (đoạn)**

> Nay xin được đính chính, sửa Khoản 1 Mục C của Thông tư này như sau: "Thông tư này có hiệu lực thi hành sau 15 ngày kể từ ngày đăng Công báo. Các văn bản hướng dẫn trước đây trái với quy định tại Thông tư này đều bãi bỏ".
> Bộ Tài chính thông báo để các cơ quan biết và điều chỉnh trong quá trình thực hiện Thông tư.

---
## q261 · khong_co_dieu · doan · TRUNG LẬP

Trạng thái: GIỮ
Câu hỏi: Nếu một đơn vị chưa thực hiện hết dự toán chi thường xuyên được giao đến hết năm 2013 thì sẽ xảy ra chuyện gì?

*Đáp án nháp của mô hình:* Dự toán chi sẽ bị hủy bỏ, trừ những nhiệm vụ được chuyển nguồn theo quy định.

**Sàng lọc:** không thấy vấn đề

**Gold: 04/CT-BTC (đoạn)**

> Đến ngày 31 tháng 12 năm 2013, dự toán chi thường xuyên đã giao cho đơn vị sử dụng ngân sách nhưng triển khai thực hiện chưa hết sẽ bị hủy bỏ, trừ những nhiệm vụ chi được chuyển nguồn theo chế độ quy định.

---
## q262 · khong_co_dieu · doan · TRUNG LẬP

Trạng thái: XOÁ
Câu hỏi: Công văn này gửi đến những bộ, cơ quan nào và có mục đích gì?

*Đáp án nháp của mô hình:* Công văn gửi đến Văn phòng Chính phủ và các bộ: Nội vụ, Kế hoạch và Đầu tư, Lao động Thương binh và Xã hội, Tư pháp, với mục đích đính chính một thông tư của Bộ Tài chính.

**Sàng lọc:** chỉ trả lời được một phần từ gold; câu hỏi mơ hồ; gold đáng ngờ — Gold là phần 'Kính gửi' (nơi nhận), không phải nội dung quy định, và chỉ là một phần danh sách nơi nhận. Câu hỏi hỏi hai ý, trong đó ý 'mục đích' không có trong gold. 'Công văn này' cũng thiếu ngữ cảnh. Nên cân nhắc chọn lại gold ở phần thân công văn. · Gợi ý câu hỏi: Công văn của Bộ Tài chính cuối năm 2004 đính chính một thông tư hướng dẫn thực hiện quyết định của Thủ tướng được gửi tới những bộ, cơ quan trung ương nào?

**Gold: 15638/TC-PC (đoạn)**

> Kính gửi:
> - Văn phòng Chính phủ
> - Bộ Nội Vụ, Bộ Kế hoạch và Đầu tư, Bộ Lao động Thương binh và Xã hội, Bộ Tư pháp

---
## q263 · khong_co_dieu · doan · TRUNG LẬP

Trạng thái: GIỮ
Câu hỏi: Nếu một doanh nghiệp kê khai thuế giá trị gia tăng không đúng với mức thuế suất được quy định thì sẽ bị xử lý thế nào?

*Đáp án nháp của mô hình:* Sẽ bị truy thu thuế và bị phạt theo quy định hiện hành.

**Sàng lọc:** câu hỏi mơ hồ — Câu hỏi quá chung: 'kê khai sai thuế suất thì bị truy thu và phạt' đúng với rất nhiều văn bản về thuế. Câu hỏi thiếu ngữ cảnh của công văn (các mặt hàng gia dụng áp thuế suất GTGT 10% từ 1/1/2004). · Gợi ý câu hỏi: Từ năm 2004, cơ sở kinh doanh máy bơm nước gia đình, máy hút mùi nhà bếp hay sạc pin điện thoại nếu kê khai, nộp thuế GTGT không đúng mức thuế suất quy định thì bị xử lý thế nào?

**Gold: 8159/TC/TCT (đoạn)**

> Các cơ sở kinh doanh kê khai và nộp thuế GTGT không đúng mức thuế suất quy định sẽ bị xử lý truy thu và phạt theo quy định hiện hành.

---
