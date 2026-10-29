# Gán nhãn trích dẫn — pilot

**120 dòng** cần gán nhãn tay (mỗi biến thể 40 dòng, phân tầng theo 5 nhóm). Còn 206 dòng giữ làm dự trữ.

Ba biến thể hiện ra là **X, Y, Z** và đã được **làm mù** — bảng giải mã nằm ở `eval/giai_ma_pilot.json`, đừng mở trước khi gán nhãn xong.

Với mỗi dòng, điền hai cột cuối:

- **Trích dẫn người đọc thấy**: các trích dẫn bạn ĐỌC ĐƯỢC trong câu trả lời (ghi tay, kể cả khi regex bỏ sót).
- **regex**: một trong bốn giá trị — **Đúng** (regex bóc khớp đúng những gì bạn thấy) · **Thiếu** (có trích dẫn mà regex không bóc được) · **Thừa** (regex bóc ra thứ không phải trích dẫn) · **Sai** (regex bóc nhưng sai số hiệu/Điều/khoản).

---

## 001

| | |
|---|---|
| mã dòng | `001` |
| qid | `q072` |
| nhóm | xuyen_khoan |
| biến thể | **Z** |
| gold | 36/2024/QH15 Điều 80 khoản 2 + 36/2024/QH15 Điều 80 khoản 3 |
| regex bóc được | 36/2024/QH15 Điều 3 |

**Câu trả lời nguyên văn:**

> Người có mặt tại nơi xảy ra tai nạn giao thông đường bộ được sử dụng phương tiện liên quan đến vụ tai nạn để chở người bị thương đi cấp cứu nhưng chỉ được thực hiện trong trường hợp không có phương tiện nào khác.  
> 
> Phải lưu ý:  
> - Xác định vị trí phương tiện và vị trí nạn nhân tại hiện trường;  
> - Không được làm thay đổi, mất dấu vết liên quan đến vụ tai nạn;  
> - Trường hợp có người chết phải giữ nguyên hiện trường và che đậy thi thể.  
> 
> Căn cứ: Điều 3 của 36/2024/QH15.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 36/2024/QH15 Điều 3 | Đúng |

---

## 002

| | |
|---|---|
| mã dòng | `002` |
| qid | `q260` |
| nhóm | dieu_dai · trung lập |
| biến thể | **Z** |
| gold | 200/2026/NĐ-CP Điều 9 khoản 4 + 200/2026/NĐ-CP Điều 9 khoản 4 điểm e |
| regex bóc được | 200/2026/NĐ-CP Điều 21 |

**Câu trả lời nguyên văn:**

> Ngoài các trách nhiệm chung, ngân hàng và công ty quản lý quỹ khi mua bán trái phiếu doanh nghiệp phát hành riêng lẻ còn phải tuân theo quy định tại Điều 21 của Nghị định 200/2026/NĐ-CP về việc thực hiện giao dịch trái phiếu theo quy định.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 200/2026/NĐ-CP Điều 21 | Đúng |

---

## 003

| | |
|---|---|
| mã dòng | `003` |
| qid | `q047` |
| nhóm | don_gian |
| biến thể | **Z** |
| gold | 10/2026/VBHN-NĐ-BNV Điều 67 |
| regex bóc được | 170/2025/NĐ-CP Điều 67 khoản 1 điểm a |

**Câu trả lời nguyên văn:**

> Ủy ban nhân dân cấp tỉnh có trách nhiệm thống nhất quản lý công chức và thực hiện các nội dung quản lý công chức trên địa bàn, căn cứ Điều 67 khoản 1 điểm a của 170/2025/NĐ-CP.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 170/2025/NĐ-CP Điều 67 khoản 1 điểm a | Đúng |

---

## 004

| | |
|---|---|
| mã dòng | `004` |
| qid | `q128` |
| nhóm | dieu_dai |
| biến thể | **X** |
| gold | 107/2026/TT-BTC Điều 10 khoản 7 + 107/2026/TT-BTC Điều 10 khoản 7 điểm a |
| regex bóc được | 107/2026/TT-BTC Điều 11 |

**Câu trả lời nguyên văn:**

> Không được. Theo Điều 11 khoản e của 107/2026/TT-BTC: "Nghiêm cấm mọi hành vi can thiệp làm thay đổi thông tin, số liệu trình bày trên báo cáo tài chính đã được nộp cho cơ quan có thẩm quyền hoặc đã được công khai. Trường hợp phải điều chỉnh thông tin, số liệu trình bày trên báo cáo tài chính đã được nộp cho cơ quan có thẩm quyền hoặc đã được công khai thì phải đảm bảo theo quy định của pháp luật kế toán và các văn bản có liên quan."

| Trích dẫn người đọc thấy | regex |
|---|---|
| 107/2026/TT-BTC Điều 11 khoản e | Thiếu |

---

## 005

| | |
|---|---|
| mã dòng | `005` |
| qid | `q220` |
| nhóm | don_gian · trung lập |
| biến thể | **X** |
| gold | 107/2026/TT-BTC Điều 7 khoản 1 |
| regex bóc được | 107/2026/TT-BTC Điều 7 khoản 1 |

**Câu trả lời nguyên văn:**

> Khi cung cấp hồ sơ, chứng từ cho kế toán trong quá trình thi hành án dân sự, người cung cấp phải chịu trách nhiệm về sự chính xác, trung thực, hợp pháp, hợp lệ của các chứng từ, tài liệu đã cung cấp, số liệu ghi trên hồ sơ, chứng từ chuyển cho kế toán ghi sổ.  
> Căn cứ: Điều 7 khoản 1 của 107/2026/TT-BTC.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 107/2026/TT-BTC Điều 7 khoản 1 | Đúng |

---

## 006

| | |
|---|---|
| mã dòng | `006` |
| qid | `q055` |
| nhóm | don_gian |
| biến thể | **X** |
| gold | 10/2026/VBHN-NĐ-BNV Điều 40 |
| regex bóc được | 10/2026/VBHN-NĐ-BNV Điều 40; 300/2026/NĐ-CP Điều 19 |

**Câu trả lời nguyên văn:**

> - Công chức làm báo cáo tự nhận xét, đánh giá việc thực hiện chức trách, nhiệm vụ trong thời gian giữ chức vụ, gửi cấp có thẩm quyền trong thời hạn 15 ngày kể từ ngày nhận được thông báo của cấp có thẩm quyền.  
> - Chậm nhất 45 ngày kể từ ngày nhận được báo cáo, cấp có thẩm quyền tiến hành:  
>   a) Tập thể lãnh đạo thảo luận, xem xét, biểu quyết bằng phiếu kín; nhân sự phải đạt tỷ lệ trên 50% thành viên đồng ý; nếu đạt 50% thì do người đứng đầu quyết định; đồng thời báo cáo đầy đủ các ý kiến khác.  
>   b) Lấy ý kiến bằng văn bản của cấp có thẩm quyền.  
>   c) Căn cứ kết quả bỏ phiếu và kết quả lấy ý kiến (nếu có), người đứng đầu ra quyết định theo thẩm quyền hoặc trình cơ quan có thẩm quyền xem xét, quyết định.  
> 
> Căn cứ: Điều 40 của 10/2026/VBHN-NĐ-BNV (sửa đổi, bổ sung tại Điều 19 của 300/2026/NĐ-CP).

| Trích dẫn người đọc thấy | regex |
|---|---|
| 10/2026/VBHN-NĐ-BNV Điều 40; 300/2026/NĐ-CP Điều 19 | Đúng |

---

## 007

| | |
|---|---|
| mã dòng | `007` |
| qid | `q010` |
| nhóm | don_gian |
| biến thể | **X** |
| gold | 03/2020/TT-BXD Điều 2 khoản 1 |
| regex bóc được | 83/2026/VBHN-TT-BXD Điều 2 khoản 1 |

**Câu trả lời nguyên văn:**

> Hồ sơ thiết kế kiến trúc là thành phần của hồ sơ thiết kế xây dựng được thực hiện thẩm định, phê duyệt theo quy định của Luật xây dựng.  
> Căn cứ: Điều 2 khoản 1 của 83/2026/VBHN-TT-BXD.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 83/2026/VBHN-TT-BXD Điều 2 khoản 1 | Đúng |

---

## 008

| | |
|---|---|
| mã dòng | `008` |
| qid | `q126` |
| nhóm | dieu_dai |
| biến thể | **Z** |
| gold | 259/2026/NĐ-CP Điều 31 khoản 4 |
| regex bóc được | 259/2026/NĐ-CP Điều 4 khoản 2 |

**Câu trả lời nguyên văn:**

> Điều 4 khoản 2 của 259/2026/NĐ-CP.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 259/2026/NĐ-CP Điều 4 khoản 2 | Đúng |

---

## 009

| | |
|---|---|
| mã dòng | `009` |
| qid | `q127` |
| nhóm | dieu_dai |
| biến thể | **X** |
| gold | 135/2025/QH15 Điều 3 + 135/2025/QH15 Điều 3 khoản 29 |
| regex bóc được | 135/2025/QH15 Điều 29 khoản 1 |

**Câu trả lời nguyên văn:**

> Sự cố công trình xây dựng theo Điều 29 khoản 1 của 135/2025/QH15.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 135/2025/QH15 Điều 29 khoản 1 | Đúng |

---

## 010

| | |
|---|---|
| mã dòng | `010` |
| qid | `q050` |
| nhóm | don_gian |
| biến thể | **X** |
| gold | 10/2026/VBHN-NĐ-BNV Điều 14 |
| regex bóc được | *(không bóc được gì)* |

**Câu trả lời nguyên văn:**

> Không đủ căn cứ trong ngữ cảnh được cung cấp.

| Trích dẫn người đọc thấy | regex |
|---|---|
| (không có) | Đúng |

---

## 011

| | |
|---|---|
| mã dòng | `011` |
| qid | `q042` |
| nhóm | don_gian |
| biến thể | **Z** |
| gold | 32/2024/QH15 Điều 42 khoản 3 |
| regex bóc được | 32/2024/QH15 Điều 3 khoản 3 |

**Câu trả lời nguyên văn:**

> Không được.  
> Điều 3 khoản 3 của 32/2024/QH15: Vợ, chồng, cha, mẹ, con, anh, chị, em của thành viên Hội đồng quản trị, thành viên Hội đồng thành viên, Tổng giám đốc (Giám đốc) tổ chức tín dụng và vợ, chồng của những người này không được là Kế toán trưởng hoặc là người phụ trách tài chính của tổ chức tín dụng đó.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 32/2024/QH15 Điều 3 khoản 3 | Đúng |

---

## 012

| | |
|---|---|
| mã dòng | `012` |
| qid | `q209` |
| nhóm | don_gian · trung lập |
| biến thể | **X** |
| gold | 33/2005/QH11 Điều 410 khoản 2 |
| regex bóc được | 33/2005/QH11 Điều 410 khoản 3 |

**Câu trả lời nguyên văn:**

> Không, nếu hợp đồng phụ bị vô hiệu thì hợp đồng chính không bị chấm dứt, trừ trường hợp các bên có thỏa thuận hợp đồng phụ là một phần không thể tách rời của hợp đồng chính.  
> Căn cứ: Điều 410 khoản 3 của 33/2005/QH11.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 33/2005/QH11 Điều 410 khoản 3 | Đúng |

---

## 013

| | |
|---|---|
| mã dòng | `013` |
| qid | `q146` |
| nhóm | khong_co_dieu |
| biến thể | **X** |
| gold | 05/TB-VPCP (đoạn) |
| regex bóc được | *(không bóc được gì)* |

**Câu trả lời nguyên văn:**

> Không đủ căn cứ trong ngữ cảnh được cung cấp.

| Trích dẫn người đọc thấy | regex |
|---|---|
| (không có) | Đúng |

---

## 014

| | |
|---|---|
| mã dòng | `014` |
| qid | `q141` |
| nhóm | khong_co_dieu |
| biến thể | **Z** |
| gold | 334/CT-TTg (đoạn) |
| regex bóc được | 334/CT-TT Điều 2 |

**Câu trả lời nguyên văn:**

> - Rà soát, xây dựng các dự án đầu tư bảo vệ và phát triển rừng, dự kiến kế hoạch khoán bảo vệ rừng, khoanh nuôi tái sinh rừng, trồng rừng mới cho 2 năm 2009 và 2010, có địa điểm, địa danh cụ thể trên bản đồ và trên thực địa trong các dự án cơ sở; có giải pháp, tính toán bố trí nguồn lực để tổ chức thực hiện dự án có kết quả tại địa phương mình.  
> - Tuyên truyền giáo dục nhân dân, phối hợp ngăn chặn, xử lý nghiêm hành vi xâm hại rừng.  
> - Củng cố bộ máy Ban Quản lý rừng phòng hộ và Ban Quản lý Dự án trồng mới 5 triệu ha rừng, tăng cường hệ thống khuyến lâm cơ sở, tổ chức đào tạo, tập huấn nghiệp vụ cho cán bộ quản lý và kỹ thuật các cấp, thường xuyên kiểm tra, đôn đốc thực hiện dự án cơ sở, bảo đảm chất lượng, chống thất thoát, lãng phí.  
> - Thực hiện việc giao đất, giao rừng, cho thuê rừng theo hướng dẫn của Bộ Tài nguyên và Môi trường.  
> - Chủ tịch Ủy ban nhân dân tỉnh chịu trách nhiệm trước Thủ tướng Chính phủ về kết quả thực hiện kế hoạch trồng mới 5 triệu ha rừng đã được giao đến năm 2010 của địa phương mình.  
> 
> Căn cứ: Điều 2, 3, 10 của 334/CT-TTg.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 334/CT-TTg Điều 2; Điều 3; Điều 10 | Thiếu |

---

## 015

| | |
|---|---|
| mã dòng | `015` |
| qid | `q072` |
| nhóm | xuyen_khoan |
| biến thể | **Y** |
| gold | 36/2024/QH15 Điều 80 khoản 2 + 36/2024/QH15 Điều 80 khoản 3 |
| regex bóc được | 36/2024/QH15 Điều 80 khoản 3 |

**Câu trả lời nguyên văn:**

> Người có mặt tại nơi xảy ra tai nạn giao thông đường bộ có thể dùng chính chiếc xe liên quan đến vụ tai nạn để chở người bị thương đi cấp cứu, nhưng chỉ được thực hiện trong trường hợp không có phương tiện nào khác và phải đảm bảo:
> 
> - Xác định vị trí phương tiện, vị trí nạn nhân tại hiện trường;  
> - Không được làm thay đổi, mất dấu vết liên quan đến vụ tai nạn giao thông đường bộ;  
> - Trường hợp có người chết phải giữ nguyên hiện trường và che đậy thi thể.  
> 
> Căn cứ: Điều 80 khoản 3 của 36/2024/QH15.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 36/2024/QH15 Điều 80 khoản 3 | Đúng |

---

## 016

| | |
|---|---|
| mã dòng | `016` |
| qid | `q128` |
| nhóm | dieu_dai |
| biến thể | **Z** |
| gold | 107/2026/TT-BTC Điều 10 khoản 7 + 107/2026/TT-BTC Điều 10 khoản 7 điểm a |
| regex bóc được | *(không bóc được gì)* |

**Câu trả lời nguyên văn:**

> Không đủ căn cứ trong ngữ cảnh được cung cấp.

| Trích dẫn người đọc thấy | regex |
|---|---|
| (không có) | Đúng |

---

## 017

| | |
|---|---|
| mã dòng | `017` |
| qid | `q001` |
| nhóm | don_gian |
| biến thể | **Y** |
| gold | 69/2025/QH15 Điều 14 khoản 7 |
| regex bóc được | 69/2025/QH15 Điều 14 khoản 7 |

**Câu trả lời nguyên văn:**

> Chính phủ quy định điều kiện, trình tự, thủ tục, thẩm quyền cấp, cấp lại, điều chỉnh, thu hồi Giấy chứng nhận đủ điều kiện hoạt động dịch vụ tồn trữ hóa chất.  
> Điều 14 khoản 7 của 69/2025/QH15.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 69/2025/QH15 Điều 14 khoản 7 | Đúng |

---

## 018

| | |
|---|---|
| mã dòng | `018` |
| qid | `q051` |
| nhóm | don_gian |
| biến thể | **X** |
| gold | 10/2026/VBHN-NĐ-BNV Điều 66 |
| regex bóc được | 80/2025/QH Điều 2 khoản 2; 10/2026/VBHN-NĐ-BNV Điều 64 khoản 2 |

**Câu trả lời nguyên văn:**

> Theo quy định hiện hành, ngoài việc quản lý công chức, bộ, cơ quan ngang bộ còn thực hiện nhiệm vụ:  
> - Quy định tại khoản 2 Điều 2 Nghị định này, thực hiện quản lý công chức thuộc phạm vi quản lý theo quy định của Luật Cán bộ, công chức số 80/2025/QH15 và theo quy định tại Nghị định này.  
> 
> Căn cứ: Điều 64 khoản 2 của 10/2026/VBHN-NĐ-BNV.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 10/2026/VBHN-NĐ-BNV Điều 64 khoản 2; Điều 2 khoản 2 của Nghị định này | Thiếu |

---

## 019

| | |
|---|---|
| mã dòng | `019` |
| qid | `q215` |
| nhóm | don_gian · trung lập |
| biến thể | **Y** |
| gold | 360/2026/NĐ-CP Điều 42 khoản 2 |
| regex bóc được | 360/2026/NĐ-CP Điều 42 khoản 2 |

**Câu trả lời nguyên văn:**

> Trung tâm giáo dục được tổ chức hoạt động trở lại sau khi cấp có thẩm quyền xác nhận đã khắc phục đầy đủ nguyên nhân dẫn đến việc đình chỉ hoặc hết thời hạn 05 ngày làm việc kể từ ngày nhận được báo cáo mà cấp có thẩm quyền không có ý kiến yêu cầu tiếp tục kiểm tra, xử lý.  
> Căn cứ: Điều 42 khoản 2 của 360/2026/NĐ-CP.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 360/2026/NĐ-CP Điều 42 khoản 2 | Đúng |

---

## 020

| | |
|---|---|
| mã dòng | `020` |
| qid | `q235` |
| nhóm | dan_chieu · trung lập |
| biến thể | **X** |
| gold | 101/2015/QH13 Điều 128 khoản 4 điểm c + 101/2015/QH13 Điều 178 |
| regex bóc được | 101/2015/QH13 Điều 128 khoản 4; 101/2015/QH13 Điều 178 |

**Câu trả lời nguyên văn:**

> - Biên bản kê biên phải ghi rõ tên và tình trạng từng tài sản bị kê biên.  
> - Ý kiến, khiếu nại của những người có mặt được ghi vào biên bản, có chữ ký xác nhận của họ và của người tiến hành kê biên.  
> - Người tham gia tố tụng, điều tra viên, cán bộ điều tra cùng ký tên vào biên bản.  
> 
> Căn cứ:  
> Điều 128 khoản 4 của 101/2015/QH13; Điều 178 của 101/2015/QH13.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 101/2015/QH13 Điều 128 khoản 4; 101/2015/QH13 Điều 178 | Đúng |

---

## 021

| | |
|---|---|
| mã dòng | `021` |
| qid | `q029` |
| nhóm | don_gian |
| biến thể | **Z** |
| gold | 32/2024/QH15 Điều 7 khoản 2 |
| regex bóc được | 32/2024/QH15 Điều 7 khoản 2 |

**Câu trả lời nguyên văn:**

> Tổ chức tín dụng có quyền từ chối yêu cầu cấp tín dụng, cung ứng các dịch vụ khác nếu thấy không đủ điều kiện, không có hiệu quả, không phù hợp với quy định của pháp luật.  
> Điều 7 khoản 2 của 32/2024/QH15.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 32/2024/QH15 Điều 7 khoản 2 | Đúng |

---

## 022

| | |
|---|---|
| mã dòng | `022` |
| qid | `q047` |
| nhóm | don_gian |
| biến thể | **Y** |
| gold | 10/2026/VBHN-NĐ-BNV Điều 67 |
| regex bóc được | 10/2026/VBHN-NĐ-BNV Điều 67 khoản 1 điểm a |

**Câu trả lời nguyên văn:**

> Ủy ban nhân dân cấp tỉnh có trách nhiệm thống nhất quản lý công chức và thực hiện các nội dung quản lý công chức trên địa bàn.  
> Căn cứ: Điều 67 khoản 1 điểm a của 10/2026/VBHN-NĐ-BNV.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 10/2026/VBHN-NĐ-BNV Điều 67 khoản 1 điểm a | Đúng |

---

## 023

| | |
|---|---|
| mã dòng | `023` |
| qid | `q127` |
| nhóm | dieu_dai |
| biến thể | **Z** |
| gold | 135/2025/QH15 Điều 3 + 135/2025/QH15 Điều 3 khoản 29 |
| regex bóc được | 135/2025/QH15 Điều 55 khoản 1 |

**Câu trả lời nguyên văn:**

> Sự cố công trình xây dựng theo Điều 55 khoản 1 của 135/2025/QH15.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 135/2025/QH15 Điều 55 khoản 1 | Đúng |

---

## 024

| | |
|---|---|
| mã dòng | `024` |
| qid | `q048` |
| nhóm | don_gian |
| biến thể | **X** |
| gold | 21/VBHN-BTC Điều 13 khoản 1 |
| regex bóc được | 19/2021/TT-BTC Điều 13 khoản 1 điểm b |

**Câu trả lời nguyên văn:**

> - Gửi thông báo tiếp nhận trong thời hạn **chậm nhất 15 phút** kể từ khi nhận được hồ sơ đăng ký thuế điện tử.  
> - Thông báo nêu rõ: **thời gian, địa điểm trả kết quả**, đồng thời **yêu cầu người nộp thuế mang hồ sơ giấy đến trụ sở cơ quan thuế**.  
> 
> Căn cứ: Điều 13 khoản 1 điểm b của 19/2021/TT-BTC.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 19/2021/TT-BTC Điều 13 khoản 1 điểm b | Đúng |

---

## 025

| | |
|---|---|
| mã dòng | `025` |
| qid | `q122` |
| nhóm | dieu_dai |
| biến thể | **Z** |
| gold | 59/2020/QH14 Điều 4 + 59/2020/QH14 Điều 4 khoản 25 |
| regex bóc được | 59/2020/QH14 Điều 17 khoản 1 |

**Câu trả lời nguyên văn:**

> Theo quy định tại Điều 17 khoản 1 của 59/2020/QH14: Tổ chức, cá nhân có quyền thành lập và quản lý doanh nghiệp tại Việt Nam theo quy định của Luật này, trừ trường hợp quy định tại khoản 2 Điều này.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 59/2020/QH14 Điều 17 khoản 1 | Đúng |

---

## 026

| | |
|---|---|
| mã dòng | `026` |
| qid | `q124` |
| nhóm | dieu_dai |
| biến thể | **Z** |
| gold | 200/2026/NĐ-CP Điều 9 khoản 5 + 200/2026/NĐ-CP Điều 9 khoản 5 điểm d |
| regex bóc được | *(không bóc được gì)* |

**Câu trả lời nguyên văn:**

> Không đủ căn cứ trong ngữ cảnh được cung cấp.

| Trích dẫn người đọc thấy | regex |
|---|---|
| (không có) | Đúng |

---

## 027

| | |
|---|---|
| mã dòng | `027` |
| qid | `q271` |
| nhóm | xuyen_khoan · trung lập |
| biến thể | **X** |
| gold | 32/2024/QH15 Điều 51 khoản 4 |
| regex bóc được | 32/2024/QH15 Điều 166 khoản 5 |

**Câu trả lời nguyên văn:**

> Không vi phạm quy định.  
> Theo Điều 166 khoản 5 của 32/2024/QH15: "Trường hợp Hội đồng quản trị, Hội đồng thành viên, Ban kiểm soát của tổ chức tín dụng hết nhiệm kỳ mà tổ chức tín dụng được kiểm soát đặc biệt chưa bầu, bổ nhiệm Hội đồng quản trị, Hội đồng thành viên, Ban kiểm soát nhiệm kỳ mới thì Hội đồng quản trị, Hội đồng thành viên, Ban kiểm soát của nhiệm kỳ vừa kết thúc tiếp tục thực hiện việc quản trị, kiểm soát tổ chức tín dụng theo quy định của pháp luật cho đến khi Hội đồng quản trị, Hội đồng thành viên, Ban kiểm soát của nhiệm kỳ mới tiếp quản công việc."

| Trích dẫn người đọc thấy | regex |
|---|---|
| 32/2024/QH15 Điều 166 khoản 5 | Đúng |

---

## 028

| | |
|---|---|
| mã dòng | `028` |
| qid | `q070` |
| nhóm | xuyen_khoan |
| biến thể | **X** |
| gold | 32/2024/QH15 Điều 43 khoản 1 + 32/2024/QH15 Điều 43 khoản 2 |
| regex bóc được | 32/2024/QH15 Điều 43 khoản 2 điểm a; ? Điều 43 khoản 1; 24/QH15 Điều 43 khoản 2 điểm a |

**Câu trả lời nguyên văn:**

> Theo Điều 43 khoản 2 a của 32/2024/QH15: thành viên Hội đồng thành viên không được đồng thời đảm nhiệm chức vụ người điều hành tổ chức tín dụng đó, **trừ trường hợp là Tổng giám đốc (Giám đốc) của tổ chức tín dụng đó**.
> 
> Do đó, **thành viên Hội đồng quản trị không độc lập** được phép kiêm nhiệm chức Tổng giám đốc của chính tổ chức tín dụng đó, **nếu họ là Tổng giám đốc**.
> 
> Tuy nhiên, câu hỏi đặt về mối quan hệ giữa **Chủ tịch Hội đồng quản trị** và **thành viên Hội đồng quản trị không độc lập**.
> 
> Theo Điều 43 khoản 1: Chủ tịch Hội đồng quản trị **không được đồng thời là người điều hành** của tổ chức tín dụng đó.
> 
> Vì vậy, **Chủ tịch Hội đồng quản trị không được kiêm nhiệm chức Tổng giám đốc**.
> 
> Tuy nhiên, **thành viên Hội đồng quản trị không độc lập** được phép kiêm nhiệm chức Tổng giám đốc nếu họ là Tổng giám đốc.
> 
> → Câu trả lời: **Thành viên Hội đồng quản trị không độc lập được phép kiêm nhiệm chức Tổng giám đốc của tổ chức tín dụng đó, nếu họ là Tổng giám đốc**.
> 
> Căn cứ: Điều 43 khoản 2 a của 32/24/QH15.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 32/2024/QH15 Điều 43 khoản 2 điểm a; Điều 43 khoản 1 cùng luật; 32/24/QH15 Điều 43 khoản 2 điểm a | Sai |

---

## 029

| | |
|---|---|
| mã dòng | `029` |
| qid | `q266` |
| nhóm | xuyen_khoan · trung lập |
| biến thể | **X** |
| gold | 200/2026/NĐ-CP Điều 12 khoản 3 điểm b |
| regex bóc được | 200/2026/NĐ-CP Điều 12 khoản 3 điểm c; 200/2026/NĐ-CP Điều 5 khoản 4 |

**Câu trả lời nguyên văn:**

> Không được thực hiện nếu không đáp ứng điều kiện mua lại trước hạn đối với người sở hữu trái phiếu không chấp thuận việc thay đổi điều kiện, điều khoản hoặc mục đích phát hành.
> 
> Cụ thể:  
> - Theo điểm c khoản 3 Điều 12 Nghị định 200/2026/NĐ-CP: "Mua lại trước hạn trái phiếu của người sở hữu trái phiếu không chấp thuận việc thay đổi điều kiện, điều khoản của trái phiếu, việc thay đổi mục đích phát hành tại phương án phát hành đối với trường hợp việc thay đổi đã được những người sở hữu trái phiếu đại diện từ 65% tổng số trái phiếu trở lên chấp thuận."  
> - Theo khoản 4 Điều 5 Nghị định 200/2026/NĐ-CP: "Đối với trái phiếu phát hành tại thị trường trong nước, doanh nghiệp chỉ được thay đổi điều kiện, điều khoản của trái phiếu... khi đã hoàn thành việc mua lại trái phiếu trước hạn đối với những người sở hữu trái phiếu không chấp thuận việc thay đổi điều kiện, điều khoản của trái phiếu hoặc thay đổi mục đích phát hành tại phương án phát hành."
> 
> → Do đó, việc thay đổi điều kiện hoặc mục đích phát hành chỉ được thực hiện sau khi đã hoàn thành việc mua lại trước hạn đối với người sở hữu không đồng ý.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 200/2026/NĐ-CP Điều 12 khoản 3 điểm c; 200/2026/NĐ-CP Điều 5 khoản 4 | Đúng |

---

## 030

| | |
|---|---|
| mã dòng | `030` |
| qid | `q141` |
| nhóm | khong_co_dieu |
| biến thể | **X** |
| gold | 334/CT-TTg (đoạn) |
| regex bóc được | 334/CT-TT Điều 2; 334/CT-TT Điều 3; 334/CT-TT Điều 10 |

**Câu trả lời nguyên văn:**

> - Rà soát, xây dựng các dự án đầu tư bảo vệ và phát triển rừng, dự kiến kế hoạch khoán bảo vệ rừng, khoanh nuôi tái sinh rừng, trồng rừng mới cho 2 năm 2009 và 2010, có địa điểm, địa danh cụ thể trên bản đồ và trên thực địa trong các dự án cơ sở; có giải pháp, tính toán bố trí nguồn lực để tổ chức thực hiện dự án có kết quả tại địa phương mình.  
> Điều 2 của 334/CT-TTg.
> 
> - Tuyên truyền giáo dục nhân dân, làm tốt công tác bảo vệ và phát triển rừng, phối hợp ngăn chặn, xử lý nghiêm hành vi xâm hại rừng.  
> Điều 3 của 334/CT-TTg.
> 
> - Giao đất, giao rừng, cho thuê rừng: các địa phương khẩn trương thực hiện việc giao đất lâm nghiệp cho các tổ chức, hộ gia đình, cá nhân và cộng đồng thôn, bản, bảo đảm từng diện tích đất có chủ cụ thể để thực hiện các nhiệm vụ còn lại của dự án trồng mới 5 triệu ha rừng.  
> Điều 10 của 334/CT-TTg.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 334/CT-TTg Điều 2; 334/CT-TTg Điều 3; 334/CT-TTg Điều 10 | Đúng |

---

## 031

| | |
|---|---|
| mã dòng | `031` |
| qid | `q220` |
| nhóm | don_gian · trung lập |
| biến thể | **Z** |
| gold | 107/2026/TT-BTC Điều 7 khoản 1 |
| regex bóc được | 107/2026/TT-BTC Điều 7 khoản 1 |

**Câu trả lời nguyên văn:**

> Khi cung cấp hồ sơ, chứng từ cho kế toán trong quá trình thi hành án dân sự, người cung cấp phải chịu trách nhiệm về sự chính xác, trung thực, hợp pháp, hợp lệ của các chứng từ, tài liệu đã cung cấp, số liệu ghi trên hồ sơ, chứng từ chuyển cho kế toán ghi sổ.  
> 
> Căn cứ: Điều 7 khoản 1 của 107/2026/TT-BTC.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 107/2026/TT-BTC Điều 7 khoản 1 | Đúng |

---

## 032

| | |
|---|---|
| mã dòng | `032` |
| qid | `q093` |
| nhóm | dan_chieu |
| biến thể | **Y** |
| gold | 101/2015/QH13 Điều 52 khoản 1 + 101/2015/QH13 Điều 49 |
| regex bóc được | 101/2015/QH13 Điều 52 khoản 1 |

**Câu trả lời nguyên văn:**

> Vì kiểm sát viên hoặc kiểm tra viên phải từ chối hoặc bị thay đổi khi đã tiến hành tố tụng trong vụ án đó với tư cách là Điều tra viên, Cán bộ điều tra, Thẩm phán, Hội thẩm, Thẩm tra viên hoặc Thư ký Tòa án (Điều 52 khoản 1 của 101/2015/QH13).

| Trích dẫn người đọc thấy | regex |
|---|---|
| 101/2015/QH13 Điều 52 khoản 1 | Đúng |

---

## 033

| | |
|---|---|
| mã dòng | `033` |
| qid | `q142` |
| nhóm | khong_co_dieu |
| biến thể | **X** |
| gold | 04/CT-BTC (đoạn) |
| regex bóc được | 9/CT-TT |

**Câu trả lời nguyên văn:**

> Chỉ thị số 09/CT-TTg của Thủ tướng Chính phủ.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 09/CT-TTg | Đúng |

---

## 034

| | |
|---|---|
| mã dòng | `034` |
| qid | `q260` |
| nhóm | dieu_dai · trung lập |
| biến thể | **Y** |
| gold | 200/2026/NĐ-CP Điều 9 khoản 4 + 200/2026/NĐ-CP Điều 9 khoản 4 điểm e |
| regex bóc được | 200/2026/NĐ-CP Điều 9 khoản 4 điểm e |

**Câu trả lời nguyên văn:**

> Theo ngữ cảnh, ngoài các trách nhiệm chung, ngân hàng và công ty quản lý quỹ khi mua, giao dịch, chuyển nhượng trái phiếu doanh nghiệp riêng lẻ còn phải thực hiện theo quy định của pháp luật chuyên ngành.
> 
> → Căn cứ: Điều 9 khoản 4 điểm e của Nghị định số 200/2026/NĐ-CP.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 200/2026/NĐ-CP Điều 9 khoản 4 điểm e | Đúng |

---

## 035

| | |
|---|---|
| mã dòng | `035` |
| qid | `q037` |
| nhóm | don_gian · trung lập |
| biến thể | **Z** |
| gold | 107/2026/TT-BTC Điều 7 khoản 2 |
| regex bóc được | 107/2026/TT-BTC Điều 2 khoản 2 |

**Câu trả lời nguyên văn:**

> Khi có các khoản tiền, tài sản tồn đọng, Chấp hành viên phải:  
> - ĐỀ XUẤT biện pháp xử lý các khoản tiền, tài sản tồn đọng theo quy định của pháp luật với Thủ trưởng đơn vị.  
> **Căn cứ: Điều 2 khoản 2 của 107/2026/TT-BTC**.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 107/2026/TT-BTC Điều 2 khoản 2 | Đúng |

---

## 036

| | |
|---|---|
| mã dòng | `036` |
| qid | `q217` |
| nhóm | don_gian · trung lập |
| biến thể | **Y** |
| gold | 307/2026/NĐ-CP Điều 6 khoản 1 |
| regex bóc được | 307/2026/NĐ-CP Điều 6 khoản 2 |

**Câu trả lời nguyên văn:**

> Khi thành lập mới một thôn do sáp nhập các thôn cũ từ ngày 26 tháng 5 năm 2026, số lượng người có uy tín của thôn mới được Chủ tịch Ủy ban nhân dân cấp xã quyết định tùy theo tình hình thực tế nhưng không vượt quá tổng số người có uy tín của các thôn trước khi sáp nhập.  
> Căn cứ: Điều 6 khoản 2 của 307/2026/NĐ-CP.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 307/2026/NĐ-CP Điều 6 khoản 2 | Đúng |

---

## 037

| | |
|---|---|
| mã dòng | `037` |
| qid | `q271` |
| nhóm | xuyen_khoan · trung lập |
| biến thể | **Y** |
| gold | 32/2024/QH15 Điều 51 khoản 4 |
| regex bóc được | 32/2024/QH15 Điều 51 khoản 4 |

**Câu trả lời nguyên văn:**

> Không vi phạm quy định.  
> Điều 51 khoản 4 của 32/2024/QH15.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 32/2024/QH15 Điều 51 khoản 4 | Đúng |

---

## 038

| | |
|---|---|
| mã dòng | `038` |
| qid | `q055` |
| nhóm | don_gian |
| biến thể | **Z** |
| gold | 10/2026/VBHN-NĐ-BNV Điều 40 |
| regex bóc được | 10/2026/VBHN-NĐ-BNV Điều 41 |

**Câu trả lời nguyên văn:**

> - Chậm nhất 45 ngày kể từ ngày nhận được báo cáo tự nhận xét, đánh giá của công chức, cấp có thẩm quyền tiến hành các thủ tục sau:
>   a) Tập thể lãnh đạo cơ quan, tổ chức, đơn vị thảo luận, xem xét, nếu công chức còn sức khỏe, uy tín, đáp ứng được yêu cầu nhiệm vụ thì thống nhất biểu quyết bằng phiếu kín. Nhân sự được đề nghị kéo dài thời gian giữ chức vụ lãnh đạo, quản lý phải đạt tỷ lệ trên 50% tổng số thành viên tập thể lãnh đạo đồng ý; trường hợp nhân sự đạt tỷ lệ 50% thì do người đứng đầu quyết định; đồng thời báo cáo đầy đủ các ý kiến khác nhau để cấp có thẩm quyền xem xét, quyết định.
>   b) Lấy ý kiến bằng văn bản của cấp có thẩm quyền.
>   c) Căn cứ kết quả bỏ phiếu và kết quả lấy ý kiến (nếu có), người đứng đầu cơ quan, tổ chức, đơn vị ra quyết định kéo dài thời gian giữ chức vụ lãnh đạo, quản lý đến tuổi nghỉ hưu đối với công chức theo thẩm quyền hoặc trình cơ quan có thẩm quyền xem xét, quyết định.
> 
> Điều 41 của 10/2026/VBHN-NĐ-BNV.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 10/2026/VBHN-NĐ-BNV Điều 41 | Đúng |

---

## 039

| | |
|---|---|
| mã dòng | `039` |
| qid | `q057` |
| nhóm | xuyen_khoan |
| biến thể | **X** |
| gold | 101/2015/QH13 Điều 122 khoản 1 + 101/2015/QH13 Điều 122 khoản 2 |
| regex bóc được | 101/2015/QH13 Điều 122 khoản 2 |

**Câu trả lời nguyên văn:**

> Bị can vi phạm nghĩa vụ cam đoan quy định tại khoản 2 Điều 122 của 101/2015/QH13 thì bị tạm giam và số tiền đã đặt bị tịch thu, nộp ngân sách nhà nước.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 101/2015/QH13 Điều 122 khoản 2 | Đúng |

---

## 040

| | |
|---|---|
| mã dòng | `040` |
| qid | `q217` |
| nhóm | don_gian · trung lập |
| biến thể | **X** |
| gold | 307/2026/NĐ-CP Điều 6 khoản 1 |
| regex bóc được | 307/2026/NĐ-CP Điều 6 khoản 2 |

**Câu trả lời nguyên văn:**

> Khi thành lập mới một thôn do sáp nhập các thôn cũ từ ngày 26 tháng 5 năm 2026, số lượng người có uy tín của thôn mới được Chủ tịch Ủy ban nhân dân cấp xã quyết định tùy theo tình hình thực tế, nhưng không vượt quá tổng số người có uy tín của các thôn trước khi sáp nhập.  
> Căn cứ: Điều 6 khoản 2 của 307/2026/NĐ-CP.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 307/2026/NĐ-CP Điều 6 khoản 2 | Đúng |

---

## 041

| | |
|---|---|
| mã dòng | `041` |
| qid | `q001` |
| nhóm | don_gian |
| biến thể | **X** |
| gold | 69/2025/QH15 Điều 14 khoản 7 |
| regex bóc được | 69/2025/QH15 Điều 14 khoản 5 |

**Câu trả lời nguyên văn:**

> Chính phủ quy định điều kiện, trình tự, thủ tục, thẩm quyền cấp, cấp lại, điều chỉnh, thu hồi Giấy chứng nhận đủ điều kiện hoạt động dịch vụ tồn trữ hóa chất.  
> Điều 14 khoản 5 của 69/2025/QH15.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 69/2025/QH15 Điều 14 khoản 5 | Đúng |

---

## 042

| | |
|---|---|
| mã dòng | `042` |
| qid | `q070` |
| nhóm | xuyen_khoan |
| biến thể | **Y** |
| gold | 32/2024/QH15 Điều 43 khoản 1 + 32/2024/QH15 Điều 43 khoản 2 |
| regex bóc được | *(không bóc được gì)* |

**Câu trả lời nguyên văn:**

> Không đủ căn cứ trong ngữ cảnh được cung cấp.

| Trích dẫn người đọc thấy | regex |
|---|---|
| (không có) | Đúng |

---

## 043

| | |
|---|---|
| mã dòng | `043` |
| qid | `q072` |
| nhóm | xuyen_khoan |
| biến thể | **X** |
| gold | 36/2024/QH15 Điều 80 khoản 2 + 36/2024/QH15 Điều 80 khoản 3 |
| regex bóc được | 36/2024/QH15 Điều 80 khoản 3 |

**Câu trả lời nguyên văn:**

> Không được. Người có mặt tại hiện trường phải tuân thủ các quy định về bảo vệ hiện trường, không được làm thay đổi, mất dấu vết liên quan đến vụ tai nạn. Nếu phải dùng phương tiện để đưa người bị thương đi cấp cứu, phải xác định vị trí phương tiện và nạn nhân tại hiện trường, không được làm thay đổi, mất dấu vết. Trách nhiệm này được quy định tại Điều 80 khoản 3 của 36/2024/QH15.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 36/2024/QH15 Điều 80 khoản 3 | Đúng |

---

## 044

| | |
|---|---|
| mã dòng | `044` |
| qid | `q029` |
| nhóm | don_gian |
| biến thể | **X** |
| gold | 32/2024/QH15 Điều 7 khoản 2 |
| regex bóc được | 32/2024/QH15 Điều 7 khoản 2; ? Điều 134; ? Điều 134 khoản 1 điểm a; ? Điều 134 khoản 1 điểm b; ? Điều 134 khoản 4; ? Điều 134 khoản 5; ? Điều 134 khoản 6; ? Điều 134 khoản 7 |

**Câu trả lời nguyên văn:**

> Tổ chức tín dụng được quyền từ chối yêu cầu cấp tín dụng của khách hàng trong các trường hợp sau:
> 
> - Không đủ điều kiện, không có hiệu quả, không phù hợp với quy định của pháp luật (Điều 7 khoản 2 của 32/2024/QH15).
> 
> - Khách hàng thuộc các đối tượng bị cấm cấp tín dụng theo quy định tại Điều 134, bao gồm:
>   - Thành viên Hội đồng quản trị, Tổng giám đốc, Phó Tổng giám đốc và các chức danh tương đương của tổ chức tín dụng hoặc chi nhánh ngân hàng nước ngoài (Điều 134 khoản 1 a);
>   - Vợ, chồng, cha, mẹ, con, anh, chị, em của các cá nhân nêu trên (Điều 134 khoản 1 b);
>   - Doanh nghiệp hoạt động trong lĩnh vực kinh doanh chứng khoán là công ty con, công ty liên kết của tổ chức tín dụng (Điều 134 khoản 4);
>   - Cấp tín dụng trên cơ sở bảo đảm bằng cổ phiếu của tổ chức tín dụng hoặc công ty con, công ty liên kết của tổ chức tín dụng (Điều 134 khoản 5);
>   - Cấp tín dụng để góp vốn, mua cổ phần của tổ chức tín dụng (Điều 134 khoản 6);
>   - Mua, nắm giữ, đầu tư vào trái phiếu doanh nghiệp (Điều 134 khoản 7).

| Trích dẫn người đọc thấy | regex |
|---|---|
| 32/2024/QH15 Điều 7 khoản 2; Điều 134 khoản 1 điểm a, khoản 1 điểm b, khoản 4, 5, 6, 7 cùng luật | Đúng |

---

## 045

| | |
|---|---|
| mã dòng | `045` |
| qid | `q141` |
| nhóm | khong_co_dieu |
| biến thể | **Y** |
| gold | 334/CT-TTg (đoạn) |
| regex bóc được | 334/CT-TT Điều 2; 334/CT-TT Điều 3; 334/CT-TT Điều 10 |

**Câu trả lời nguyên văn:**

> - Rà soát, xây dựng các dự án đầu tư bảo vệ và phát triển rừng, dự kiến kế hoạch khoán bảo vệ rừng, khoanh nuôi tái sinh rừng, trồng rừng mới cho 2 năm 2009 và 2010, có địa điểm, địa danh cụ thể trên bản đồ và trên thực địa trong các dự án cơ sở; có giải pháp, tính toán bố trí nguồn lực để tổ chức thực hiện dự án có kết quả tại địa phương mình.  
> Điều 2 của 334/CT-TTg.
> 
> - Tuyên truyền giáo dục nhân dân, làm tốt công tác bảo vệ và phát triển rừng, phối hợp ngăn chặn, xử lý nghiêm hành vi xâm hại rừng.  
> Điều 3 của 334/CT-TTg.
> 
> - Giao đất, giao rừng, cho thuê rừng: các địa phương khẩn trương thực hiện việc giao đất lâm nghiệp cho các tổ chức, hộ gia đình, cá nhân và cộng đồng thôn, bản, bảo đảm từng diện tích đất có chủ cụ thể để thực hiện các nhiệm vụ còn lại của dự án trồng mới 5 triệu ha rừng.  
> Điều 10 của 334/CT-TTg.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 334/CT-TTg Điều 2; 334/CT-TTg Điều 3; 334/CT-TTg Điều 10 | Đúng |

---

## 046

| | |
|---|---|
| mã dòng | `046` |
| qid | `q042` |
| nhóm | don_gian |
| biến thể | **X** |
| gold | 32/2024/QH15 Điều 42 khoản 3 |
| regex bóc được | 32/2024/QH15 Điều 42 khoản 3 |

**Câu trả lời nguyên văn:**

> Không được.  
> Điều 42 khoản 3 của 32/2024/QH15.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 32/2024/QH15 Điều 42 khoản 3 | Đúng |

---

## 047

| | |
|---|---|
| mã dòng | `047` |
| qid | `q015` |
| nhóm | don_gian |
| biến thể | **Z** |
| gold | 19/2021/TT-BTC Điều 3 khoản 1 |
| regex bóc được | 21/VBHN-BTC Điều 3 |

**Câu trả lời nguyên văn:**

> Giao dịch thuế điện tử là các giao dịch được các cơ quan, tổ chức, cá nhân thực hiện bằng phương thức điện tử thuộc phạm vi điều chỉnh của Thông tư này.  
> Điều 3 của 21/VBHN-BTC

| Trích dẫn người đọc thấy | regex |
|---|---|
| 21/VBHN-BTC Điều 3 | Đúng |

---

## 048

| | |
|---|---|
| mã dòng | `048` |
| qid | `q143` |
| nhóm | khong_co_dieu |
| biến thể | **Z** |
| gold | 334/CT-TTg (đoạn) |
| regex bóc được | *(không bóc được gì)* |

**Câu trả lời nguyên văn:**

> Không đủ căn cứ trong ngữ cảnh được cung cấp.

| Trích dẫn người đọc thấy | regex |
|---|---|
| (không có) | Đúng |

---

## 049

| | |
|---|---|
| mã dòng | `049` |
| qid | `q127` |
| nhóm | dieu_dai |
| biến thể | **Y** |
| gold | 135/2025/QH15 Điều 3 + 135/2025/QH15 Điều 3 khoản 29 |
| regex bóc được | 135/2025/QH15 Điều 55 khoản 1 điểm a |

**Câu trả lời nguyên văn:**

> Sự cố công trình xây dựng theo Điều 55 khoản 1 điểm a, b, c của Luật Xây dựng số 135/2025/QH15.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 135/2025/QH15 Điều 55 khoản 1 điểm a b c | Thiếu |

---

## 050

| | |
|---|---|
| mã dòng | `050` |
| qid | `q124` |
| nhóm | dieu_dai |
| biến thể | **Y** |
| gold | 200/2026/NĐ-CP Điều 9 khoản 5 + 200/2026/NĐ-CP Điều 9 khoản 5 điểm d |
| regex bóc được | 200/2026/NĐ-CP Điều 9 khoản 4 điểm g |

**Câu trả lời nguyên văn:**

> Nhà đầu tư có quyền đòi bên bán cung cấp đầy đủ nội dung công bố thông tin của doanh nghiệp phát hành theo quy định tại Nghị định này khi mua trái phiếu trên thị trường thứ cấp.  
> Căn cứ: Điều 9 khoản 4 điểm g của 200/2026/NĐ-CP.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 200/2026/NĐ-CP Điều 9 khoản 4 điểm g | Đúng |

---

## 051

| | |
|---|---|
| mã dòng | `051` |
| qid | `q090` |
| nhóm | dan_chieu |
| biến thể | **Z** |
| gold | 101/2015/QH13 Điều 248 khoản 2 + 101/2015/QH13 Điều 132 khoản 2 |
| regex bóc được | ? Điều 132 khoản 2; 101/2015/QH13 Điều 248 khoản 2 |

**Câu trả lời nguyên văn:**

> Quyết định đình chỉ vụ án phải ghi rõ lý do đình chỉ và các nội dung quy định tại khoản 2 Điều 132 của Bộ luật này.  
> Căn cứ: Điều 248 khoản 2 của 101/2015/QH13.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 101/2015/QH13 Điều 248 khoản 2; Điều 132 khoản 2 của Bộ luật này | Thiếu |

---

## 052

| | |
|---|---|
| mã dòng | `052` |
| qid | `q144` |
| nhóm | khong_co_dieu |
| biến thể | **X** |
| gold | 1408/CT-TTg (đoạn) |
| regex bóc được | 1408/CT-TT Điều 3 |

**Câu trả lời nguyên văn:**

> Công an các cấp cần:
> - Xây dựng và thực hiện các kế hoạch đấu tranh quyết liệt, liên tục với tội phạm xâm hại trẻ em, tội phạm trong lứa tuổi chưa thành niên;
> - Tăng cường công tác xác minh đối với hồ sơ của trẻ em có nguồn gốc không rõ ràng nhưng được giới thiệu làm con nuôi người nước ngoài;
> - Nghiêm khắc xử lý các hành vi làm giả hồ sơ về nguồn gốc của trẻ em, đưa hối lộ, nhận hối lộ liên quan đến việc giải quyết cho trẻ em làm con nuôi người nước ngoài hoặc lợi dụng việc giới thiệu, giải quyết, đăng ký cho trẻ em làm con nuôi người nước ngoài để trục lợi, thu lợi vật chất bất hợp pháp.
> 
> Căn cứ: Điều 3 khoản b của Chỉ thị số 1408/CT-TTg.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 1408/CT-TTg Điều 3 khoản b | Thiếu |

---

## 053

| | |
|---|---|
| mã dòng | `053` |
| qid | `q051` |
| nhóm | don_gian |
| biến thể | **Y** |
| gold | 10/2026/VBHN-NĐ-BNV Điều 66 |
| regex bóc được | ? Điều 64 khoản 1; ? Điều 64 khoản 1 điểm e; 10/2026/VBHN-NĐ-BNV Điều 66 |

**Câu trả lời nguyên văn:**

> Theo quy định hiện hành, ngoài việc quản lý công chức, bộ, cơ quan ngang bộ còn thực hiện các nhiệm vụ sau đối với cán bộ:
> 
> - Thực hiện nội dung quản lý công chức quy định tại khoản 1 Điều 64 Nghị định này, trừ trường hợp phân cấp theo quy định tại khoản 2 Điều này và các nội dung thuộc thẩm quyền của cơ quan sử dụng công chức theo quy định của Luật Cán bộ, công chức số 80/2025/QH15 và quy định tại Nghị định này.  
> - Phân cấp việc thực hiện các nội dung quy định tại điểm d, điểm đ, điểm e khoản 1 Điều 64 Nghị định này, trừ những nội dung thuộc thẩm quyền của cơ quan sử dụng công chức theo quy định của Luật Cán bộ, công chức số 80/2025/QH15 và quy định tại Nghị định này.  
> - Thực hiện các nội dung quản lý cán bộ theo phân cấp quản lý cán bộ của cấp có thẩm quyền.  
> 
> Căn cứ: Điều 66 của 10/2026/VBHN-NĐ-BNV.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 10/2026/VBHN-NĐ-BNV Điều 66; Điều 64 khoản 1 điểm d đ e và khoản 2 Điều này, nội bộ | Thiếu |

---

## 054

| | |
|---|---|
| mã dòng | `054` |
| qid | `q093` |
| nhóm | dan_chieu |
| biến thể | **X** |
| gold | 101/2015/QH13 Điều 52 khoản 1 + 101/2015/QH13 Điều 49 |
| regex bóc được | 24/2004/QH11 Điều 48; 101/2015/QH13 Điều 52 |

**Câu trả lời nguyên văn:**

> Một kiểm sát viên hoặc kiểm tra viên phải từ chối hoặc bị thay đổi khi tham gia vào một vụ án vì họ đã tiến hành tố tụng trong vụ án đó với tư cách là Thẩm phán, Hội thẩm nhân dân, Kiểm sát viên, Thư ký Toà án, Điều tra viên, Cán bộ điều tra, hoặc người thân thích với người tham gia tố tụng, theo Điều 48 của Bộ luật Tố tụng dân sự số 24/2004/QH11 và Điều 52 của Bộ luật Tố tụng hình sự số 101/2015/QH13.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 24/2004/QH11 Điều 48; 101/2015/QH13 Điều 52 | Đúng |

---

## 055

| | |
|---|---|
| mã dòng | `055` |
| qid | `q271` |
| nhóm | xuyen_khoan · trung lập |
| biến thể | **Z** |
| gold | 32/2024/QH15 Điều 51 khoản 4 |
| regex bóc được | 32/2024/QH15 Điều 5 khoản 4 |

**Câu trả lời nguyên văn:**

> Có vi phạm quy định.
> 
> Căn cứ: Điều 5 khoản 4 của 32/2024/QH15 quy định: "Ban kiểm soát của nhiệm kỳ vừa kết thúc tiếp tục hoạt động cho đến khi Ban kiểm soát của nhiệm kỳ mới tiếp quản công việc."
> 
> → Trong tình huống Ban kiểm soát nhiệm kỳ cũ chưa được thay thế, nhưng vẫn đang thực hiện nhiệm vụ, thì việc này **không vi phạm** quy định, vì được phép tiếp tục hoạt động đến khi nhiệm kỳ mới được bầu. 
> 
> Do đó, **không vi phạm** quy định.  
> 
> Sai sót trong câu hỏi: Câu hỏi đặt là "có vi phạm hay không?" nhưng thực tế theo văn bản, việc này được phép.  
> 
> → **Không vi phạm quy định.**
> 
> Căn cứ: Điều 5 khoản 4 của 32/2024/QH15.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 32/2024/QH15 Điều 5 khoản 4 | Đúng |

---

## 056

| | |
|---|---|
| mã dòng | `056` |
| qid | `q046` |
| nhóm | don_gian |
| biến thể | **Z** |
| gold | 21/VBHN-BTC Điều 35 khoản 2 điểm a |
| regex bóc được | 105/2020/TT-BTC |

**Câu trả lời nguyên văn:**

> Cơ quan thuế căn cứ vào thông tin trên Hệ thống thông tin đăng ký thuế do Hệ thống thông tin quốc gia về đăng ký doanh nghiệp, đăng ký hợp tác xã gửi đến và quy định tại Thông tư số 105/2020/TT-BTC, Quy chế trao đổi thông tin giữa Bộ Kế hoạch và Đầu tư và Bộ Tài chính để xử lý và trả kết quả hồ sơ.

| Trích dẫn người đọc thấy | regex |
|---|---|
| (không có trích dẫn nguồn; thân bài nhắc 105/2020/TT-BTC) | Thừa |

---

## 057

| | |
|---|---|
| mã dòng | `057` |
| qid | `q220` |
| nhóm | don_gian · trung lập |
| biến thể | **Y** |
| gold | 107/2026/TT-BTC Điều 7 khoản 1 |
| regex bóc được | 107/2026/TT-BTC Điều 7 khoản 1 |

**Câu trả lời nguyên văn:**

> Khi cung cấp hồ sơ, chứng từ cho kế toán trong quá trình thi hành án dân sự, người cung cấp phải chịu trách nhiệm về sự chính xác, trung thực, hợp pháp, hợp lệ của các chứng từ, tài liệu đã cung cấp, số liệu ghi trên hồ sơ, chứng từ chuyển cho kế toán ghi sổ.  
> Căn cứ: Điều 7 khoản 1 của 107/2026/TT-BTC.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 107/2026/TT-BTC Điều 7 khoản 1 | Đúng |

---

## 058

| | |
|---|---|
| mã dòng | `058` |
| qid | `q144` |
| nhóm | khong_co_dieu |
| biến thể | **Z** |
| gold | 1408/CT-TTg (đoạn) |
| regex bóc được | 1408/CT-TT Điều 2 |

**Câu trả lời nguyên văn:**

> Công an các cấp cần:
> - Xây dựng và thực hiện các kế hoạch đấu tranh quyết liệt, liên tục với tội phạm xâm hại trẻ em, tội phạm trong lứa tuổi chưa thành niên;
> - Tăng cường công tác xác minh đối với hồ sơ của trẻ em có nguồn gốc không rõ ràng nhưng được giới thiệu làm con nuôi người nước ngoài;
> - Nghiêm khắc xử lý các hành vi làm giả hồ sơ về nguồn gốc của trẻ em, đưa hối lộ, nhận hối lộ liên quan đến việc giải quyết cho trẻ em làm con nuôi người nước ngoài hoặc lợi dụng việc giới thiệu, giải quyết, đăng ký cho trẻ em làm con nuôi người nước ngoài để trục lợi, thu lợi vật chất bất hợp pháp.  
> 
> Căn cứ: Điều 2 khoản a, b của 1408/CT-TTg.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 1408/CT-TTg Điều 2 khoản a b | Thiếu |

---

## 059

| | |
|---|---|
| mã dòng | `059` |
| qid | `q146` |
| nhóm | khong_co_dieu |
| biến thể | **Z** |
| gold | 05/TB-VPCP (đoạn) |
| regex bóc được | *(không bóc được gì)* |

**Câu trả lời nguyên văn:**

> Không đủ căn cứ trong ngữ cảnh được cung cấp.

| Trích dẫn người đọc thấy | regex |
|---|---|
| (không có) | Đúng |

---

## 060

| | |
|---|---|
| mã dòng | `060` |
| qid | `q142` |
| nhóm | khong_co_dieu |
| biến thể | **Y** |
| gold | 04/CT-BTC (đoạn) |
| regex bóc được | 9/CT-TT |

**Câu trả lời nguyên văn:**

> Chỉ thị số 09/CT-TTg của Thủ tướng Chính phủ.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 09/CT-TTg | Đúng |

---

## 061

| | |
|---|---|
| mã dòng | `061` |
| qid | `q214` |
| nhóm | don_gian · trung lập |
| biến thể | **X** |
| gold | 200/2026/NĐ-CP Điều 15 khoản 3 |
| regex bóc được | ? Điều 9 khoản 4; 200/2026/NĐ-CP Điều 15 khoản 3 |

**Câu trả lời nguyên văn:**

> Nhà đầu tư mua trái phiếu là cá nhân phải ký văn bản xác nhận đã thực hiện các quy định tại các điểm a, b, c và d khoản 4 Điều 9 Nghị định này.  
> Căn cứ: Điều 15 khoản 3 của 200/2026/NĐ-CP

| Trích dẫn người đọc thấy | regex |
|---|---|
| 200/2026/NĐ-CP Điều 15 khoản 3; Điều 9 khoản 4 điểm a b c d của Nghị định này | Thiếu |

---

## 062

| | |
|---|---|
| mã dòng | `062` |
| qid | `q057` |
| nhóm | xuyen_khoan |
| biến thể | **Z** |
| gold | 101/2015/QH13 Điều 122 khoản 1 + 101/2015/QH13 Điều 122 khoản 2 |
| regex bóc được | 101/2015/QH13 Điều 122 khoản 2 |

**Câu trả lời nguyên văn:**

> Bị can vi phạm nghĩa vụ cam đoan quy định tại khoản 2 Điều 122 của 101/2015/QH13 thì bị tạm giam và số tiền đã đặt bị tịch thu, nộp ngân sách nhà nước.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 101/2015/QH13 Điều 122 khoản 2 | Đúng |

---

## 063

| | |
|---|---|
| mã dòng | `063` |
| qid | `q010` |
| nhóm | don_gian |
| biến thể | **Z** |
| gold | 03/2020/TT-BXD Điều 2 khoản 1 |
| regex bóc được | 83/2026/VBHN-TT-BXD Điều 2 |

**Câu trả lời nguyên văn:**

> Hồ sơ thiết kế kiến trúc là một trong các thành phần của hồ sơ thiết kế xây dựng, được thực hiện và thẩm định, phê duyệt theo quy định của Luật Xây dựng.  
> Điều 2 của 83/2026/VBHN-TT-BXD.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 83/2026/VBHN-TT-BXD Điều 2 | Đúng |

---

## 064

| | |
|---|---|
| mã dòng | `064` |
| qid | `q050` |
| nhóm | don_gian |
| biến thể | **Y** |
| gold | 10/2026/VBHN-NĐ-BNV Điều 14 |
| regex bóc được | ? Điều 13; 300/2026/NĐ-CP Điều 4 khoản 1 |

**Câu trả lời nguyên văn:**

> Theo quy định hiện hành, người phụ trách công tác tổ chức cán bộ của cơ quan có thẩm quyền tuyển dụng có trách nhiệm nghiên cứu, đề xuất tiếp nhận đối với người đáp ứng đủ tiêu chuẩn, điều kiện theo quy định tại Điều 13 Nghị định này.  
> Căn cứ: Điều 4 khoản 1 của 300/2026/NĐ-CP.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 300/2026/NĐ-CP Điều 4 khoản 1; Điều 13 của Nghị định này | Thiếu |

---

## 065

| | |
|---|---|
| mã dòng | `065` |
| qid | `q126` |
| nhóm | dieu_dai |
| biến thể | **Y** |
| gold | 259/2026/NĐ-CP Điều 31 khoản 4 |
| regex bóc được | ? Điều 2 khoản 2; 259/2026/NĐ-CP Điều 31 khoản 4 |

**Câu trả lời nguyên văn:**

> Căn cứ điều kiện cụ thể của cơ quan, tổ chức, người đứng đầu cơ quan quản lý viên chức tại khoản 2 Điều 2 Nghị định này quy định cụ thể về: Thẩm quyền bổ nhiệm; nguyên tắc xác định nguồn nhân sự tại chỗ, nguồn nhân sự từ nơi khác đối với trường hợp đơn vị có tổ chức cấu thành, bảo đảm phù hợp với quy định của Đảng và quy định tại Nghị định này.
> 
> Điều 31 khoản 4 của 259/2026/NĐ-CP.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 259/2026/NĐ-CP Điều 31 khoản 4; Điều 2 khoản 2 của Nghị định này | Đúng |

---

## 066

| | |
|---|---|
| mã dòng | `066` |
| qid | `q037` |
| nhóm | don_gian · trung lập |
| biến thể | **Y** |
| gold | 107/2026/TT-BTC Điều 7 khoản 2 |
| regex bóc được | 107/2026/TT-BTC Điều 7 khoản 2 |

**Câu trả lời nguyên văn:**

> Khi có các khoản tiền, tài sản tồn đọng, Chấp hành viên phải kịp thời đề xuất biện pháp xử lý theo quy định của pháp luật với Thủ trưởng đơn vị.  
> Căn cứ: Điều 7 khoản 2 của 107/2026/TT-BTC.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 107/2026/TT-BTC Điều 7 khoản 2 | Đúng |

---

## 067

| | |
|---|---|
| mã dòng | `067` |
| qid | `q046` |
| nhóm | don_gian |
| biến thể | **Y** |
| gold | 21/VBHN-BTC Điều 35 khoản 2 điểm a |
| regex bóc được | 21/VBHN-BTC Điều 35 khoản 2 điểm a |

**Câu trả lời nguyên văn:**

> Cơ quan thuế căn cứ vào thông tin trên Hệ thống thông tin đăng ký thuế do Hệ thống thông tin quốc gia về đăng ký doanh nghiệp, đăng ký hợp tác xã gửi đến và quy định tại Thông tư số 105/2020/TT-BTC, Quy chế trao đổi thông tin giữa Bộ Kế hoạch và Đầu tư và Bộ Tài chính để xử lý và trả kết quả hồ sơ đăng ký doanh nghiệp, hợp tác xã. 
> 
> Điều 35 khoản 2 điểm a của 21/VBHN-BTC.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 21/VBHN-BTC Điều 35 khoản 2 điểm a | Đúng |

---

## 068

| | |
|---|---|
| mã dòng | `068` |
| qid | `q048` |
| nhóm | don_gian |
| biến thể | **Z** |
| gold | 21/VBHN-BTC Điều 13 khoản 1 |
| regex bóc được | 19/2021/TT-BTC Điều 4 khoản 1 điểm a |

**Câu trả lời nguyên văn:**

> Chậm nhất 15 phút kể từ khi nhận được hồ sơ đăng ký giao dịch bằng phương thức điện tử của người nộp thuế.  
> Thông báo đó nêu:  
> - Trường hợp chấp nhận: gửi thông tin về tài khoản giao dịch thuế điện tử;  
> - Trường hợp không chấp nhận: nêu lý do không chấp nhận để người nộp thuế hoàn chỉnh thông tin, ký điện tử và gửi lại hoặc liên hệ cơ quan thuế được hướng dẫn, hỗ trợ.  
> 
> Căn cứ: Điều 4 khoản 1, điểm a, b, c của Thông tư 19/2021/TT-BTC.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 19/2021/TT-BTC Điều 4 khoản 1 điểm a b c | Thiếu |

---

## 069

| | |
|---|---|
| mã dòng | `069` |
| qid | `q235` |
| nhóm | dan_chieu · trung lập |
| biến thể | **Z** |
| gold | 101/2015/QH13 Điều 128 khoản 4 điểm c + 101/2015/QH13 Điều 178 |
| regex bóc được | 101/2015/QH13 Điều 178 |

**Câu trả lời nguyên văn:**

> - Biên bản kê biên phải ghi rõ tên và tình trạng từng tài sản bị kê biên.  
> - Ý kiến, khiếu nại của những người có mặt liên quan đến việc kê biên được ghi vào biên bản.  
> - Người tham gia tố tụng, điều tra viên, cán bộ điều tra cùng ký tên vào biên bản.  
> 
> Căn cứ:  
> Điều 178 của 101/2015/QH13.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 101/2015/QH13 Điều 178 | Đúng |

---

## 070

| | |
|---|---|
| mã dòng | `070` |
| qid | `q118` |
| nhóm | dieu_dai |
| biến thể | **Z** |
| gold | 19/2021/TT-BTC Điều 10 khoản 3 |
| regex bóc được | 19/2021/TT-BTC Điều 42 |

**Câu trả lời nguyên văn:**

> Người nộp thuế thực hiện đăng ký giao dịch thuế điện tử thông qua tổ chức cung cấp dịch vụ T-VAN theo quy định tại Điều 42 của Thông tư 19/2021/TT-BTC.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 19/2021/TT-BTC Điều 42 | Đúng |

---

## 071

| | |
|---|---|
| mã dòng | `071` |
| qid | `q118` |
| nhóm | dieu_dai |
| biến thể | **Y** |
| gold | 19/2021/TT-BTC Điều 10 khoản 3 |
| regex bóc được | 19/2021/TT-BTC Điều 42 |

**Câu trả lời nguyên văn:**

> Người nộp thuế thực hiện theo quy định tại Điều 42 của Thông tư số 19/2021/TT-BTC.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 19/2021/TT-BTC Điều 42 | Đúng |

---

## 072

| | |
|---|---|
| mã dòng | `072` |
| qid | `q215` |
| nhóm | don_gian · trung lập |
| biến thể | **X** |
| gold | 360/2026/NĐ-CP Điều 42 khoản 2 |
| regex bóc được | 360/2026/NĐ-CP Điều 42 khoản 2 |

**Câu trả lời nguyên văn:**

> Trung tâm giáo dục được tổ chức hoạt động trở lại sau khi cấp có thẩm quyền xác nhận đã khắc phục đầy đủ nguyên nhân dẫn đến việc đình chỉ hoặc hết thời hạn 05 ngày làm việc kể từ ngày nhận được báo cáo mà cấp có thẩm quyền không có ý kiến yêu cầu tiếp tục kiểm tra, xử lý.
> 
> Căn cứ: Điều 42 khoản 2 của 360/2026/NĐ-CP.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 360/2026/NĐ-CP Điều 42 khoản 2 | Đúng |

---

## 073

| | |
|---|---|
| mã dòng | `073` |
| qid | `q093` |
| nhóm | dan_chieu |
| biến thể | **Z** |
| gold | 101/2015/QH13 Điều 52 khoản 1 + 101/2015/QH13 Điều 49 |
| regex bóc được | 101/2015/QH13 Điều 52 khoản 1; ? Điều 49 |

**Câu trả lời nguyên văn:**

> Vì theo Điều 52 khoản 1 chữ a và b của 101/2015/QH13: Kiểm sát viên, Kiểm tra viên phải từ chối tiến hành tố tụng hoặc bị thay đổi khi thuộc một trong các trường hợp: a) Trường hợp quy định tại Điều 49 của Bộ luật này; b) Đã tiến hành tố tụng trong vụ án đó với tư cách là Điều tra viên, Cán bộ điều tra, Thẩm phán, Hội thẩm, Thẩm tra viên hoặc Thư ký Tòa án.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 101/2015/QH13 Điều 52 khoản 1 điểm a b; Điều 49 của Bộ luật này | Thiếu |

---

## 074

| | |
|---|---|
| mã dòng | `074` |
| qid | `q266` |
| nhóm | xuyen_khoan · trung lập |
| biến thể | **Y** |
| gold | 200/2026/NĐ-CP Điều 12 khoản 3 điểm b |
| regex bóc được | 200/2026/NĐ-CP Điều 12 khoản 3 điểm c |

**Câu trả lời nguyên văn:**

> Không được thực hiện nếu không có sự đồng ý của người sở hữu trái phiếu.  
> Điều 12 khoản 3 điểm c của 200/2026/NĐ-CP quy định: doanh nghiệp chỉ được mua lại trái phiếu trước hạn của người sở hữu không chấp thuận việc thay đổi điều kiện, điều khoản hoặc mục đích phát hành nếu việc thay đổi đã được những người sở hữu trái phiếu đại diện từ 65% tổng số trái phiếu trở lên chấp thuận.  
> Do đó, nếu không có sự đồng ý từ 65% người sở hữu trái phiếu, việc thay đổi điều kiện hoặc mục đích phát hành không được thực hiện.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 200/2026/NĐ-CP Điều 12 khoản 3 điểm c | Đúng |

---

## 075

| | |
|---|---|
| mã dòng | `075` |
| qid | `q148` |
| nhóm | khong_co_dieu |
| biến thể | **X** |
| gold | 9367 TC/PC (đoạn) |
| regex bóc được | ? Điều 5 khoản 2 |

**Câu trả lời nguyên văn:**

> Việc đính chính đã bỏ các điểm sau khỏi danh mục:  
> - Điểm 54 (Quyết định số 164/2000/QĐ-BTC ngày 10/10/2000)  
> - Điểm 115 (Quyết định số 214/2003/QĐ-BTC ngày 18/12/2003)  
> - Điểm 121 (Quyết định số 01/2000/QĐ-BVGCP ngày 5/1/2000)  
> 
> Căn cứ: Điều 5 khoản 2 của 9367 TC/PC.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 9367 TC/PC Điều 5 khoản 2 | Đúng |

---

## 076

| | |
|---|---|
| mã dòng | `076` |
| qid | `q051` |
| nhóm | don_gian |
| biến thể | **Z** |
| gold | 10/2026/VBHN-NĐ-BNV Điều 66 |
| regex bóc được | 10/2026/VBHN-NĐ-BNV Điều 73; 300/2026/NĐ-CP Điều 2 |

**Câu trả lời nguyên văn:**

> Theo quy định hiện hành, ngoài việc quản lý công chức, Bộ, cơ quan ngang bộ còn thực hiện nhiệm vụ:
> 
> - Xây dựng, duy trì, cập nhật, phát triển hệ thống thông tin quản lý công chức và cơ sở dữ liệu quốc gia về cán bộ, công chức;  
> - Lập, quản lý hồ sơ công chức; thực hiện chế độ báo cáo, thống kê đội ngũ;  
> - Thực hiện nội dung quản lý khác trong công tác cán bộ theo thẩm quyền và theo quy định của Đảng.  
> 
> Căn cứ: Điều 73 của 10/2026/VBHN-NĐ-BNV; Điều 2 khoản b của 300/2026/NĐ-CP.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 10/2026/VBHN-NĐ-BNV Điều 73; 300/2026/NĐ-CP Điều 2 khoản b | Thiếu |

---

## 077

| | |
|---|---|
| mã dòng | `077` |
| qid | `q048` |
| nhóm | don_gian |
| biến thể | **Y** |
| gold | 21/VBHN-BTC Điều 13 khoản 1 |
| regex bóc được | 19/2021/TT-BTC Điều 13 khoản 2 điểm b; 21/VBHN-BTC Điều 13 khoản 2 điểm b |

**Câu trả lời nguyên văn:**

> Theo quy định hiện hành, sau khi tiếp nhận hồ sơ đăng ký thuế lần đầu bằng phương thức điện tử, Cổng thông tin điện tử của Tổng cục Thuế gửi Thông báo tiếp nhận cho người nộp thuế **chậm nhất 15 phút** kể từ khi nhận được hồ sơ điện tử của người nộp thuế.
> 
> Thông báo đó **nêu rõ thời gian, địa điểm trả kết quả**, đồng thời yêu cầu người nộp thuế mang hồ sơ giấy đến trụ sở cơ quan thuế.  
> 
> Căn cứ:  
> - Điều 13 khoản 2 điểm b của Thông tư số 19/2021/TT-BTC  
> - Điều 13 khoản 2 điểm b của Văn bản hợp nhất số 21/VBHN-BTC

| Trích dẫn người đọc thấy | regex |
|---|---|
| 19/2021/TT-BTC Điều 13 khoản 2 điểm b; 21/VBHN-BTC Điều 13 khoản 2 điểm b | Đúng |

---

## 078

| | |
|---|---|
| mã dòng | `078` |
| qid | `q001` |
| nhóm | don_gian |
| biến thể | **Z** |
| gold | 69/2025/QH15 Điều 14 khoản 7 |
| regex bóc được | 69/2025/QH15 Điều 7 khoản 1 |

**Câu trả lời nguyên văn:**

> Chính phủ quy định chi tiết điều kiện, trình tự, thủ tục, thẩm quyền cấp, cấp lại, điều chỉnh, thu hồi Giấy chứng nhận đủ điều kiện hoạt động dịch vụ tồn trữ hóa chất.  
> Điều 7 khoản 1 của 69/2025/QH15.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 69/2025/QH15 Điều 7 khoản 1 | Đúng |

---

## 079

| | |
|---|---|
| mã dòng | `079` |
| qid | `q090` |
| nhóm | dan_chieu |
| biến thể | **X** |
| gold | 101/2015/QH13 Điều 248 khoản 2 + 101/2015/QH13 Điều 132 khoản 2 |
| regex bóc được | 101/2015/QH13 Điều 132 khoản 2 |

**Câu trả lời nguyên văn:**

> Quyết định đình chỉ vụ án phải ghi rõ lý do đình chỉ và các nội dung quy định tại khoản 2 Điều 132 của Bộ luật Tố tụng hình sự số 101/2015/QH13.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 101/2015/QH13 Điều 132 khoản 2 | Đúng |

---

## 080

| | |
|---|---|
| mã dòng | `080` |
| qid | `q055` |
| nhóm | don_gian |
| biến thể | **Y** |
| gold | 10/2026/VBHN-NĐ-BNV Điều 40 |
| regex bóc được | 10/2026/VBHN-NĐ-BNV Điều 40; 300/2026/NĐ-CP Điều 19 |

**Câu trả lời nguyên văn:**

> - Công chức làm báo cáo tự nhận xét, đánh giá việc thực hiện chức trách, nhiệm vụ trong thời gian giữ chức vụ, gửi cấp có thẩm quyền trong thời hạn 15 ngày kể từ ngày nhận được thông báo của cấp có thẩm quyền.  
> - Chậm nhất 45 ngày kể từ ngày nhận được báo cáo, cấp có thẩm quyền tiến hành:  
>   a) Tập thể lãnh đạo thảo luận, xem xét, biểu quyết bằng phiếu kín; nhân sự phải đạt tỷ lệ trên 50% thành viên đồng ý; nếu đạt 50% thì do người đứng đầu quyết định; đồng thời báo cáo đầy đủ các ý kiến khác.  
>   b) Lấy ý kiến bằng văn bản của cấp có thẩm quyền.  
>   c) Căn cứ kết quả bỏ phiếu và kết quả lấy ý kiến (nếu có), người đứng đầu ra quyết định theo thẩm quyền hoặc trình cơ quan có thẩm quyền xem xét, quyết định.  
> 
> Căn cứ: Điều 40 của 10/2026/VBHN-NĐ-BNV (sửa đổi, bổ sung tại Điều 19 của 300/2026/NĐ-CP).

| Trích dẫn người đọc thấy | regex |
|---|---|
| 10/2026/VBHN-NĐ-BNV Điều 40; 300/2026/NĐ-CP Điều 19 | Đúng |

---

## 081

| | |
|---|---|
| mã dòng | `081` |
| qid | `q010` |
| nhóm | don_gian |
| biến thể | **Y** |
| gold | 03/2020/TT-BXD Điều 2 khoản 1 |
| regex bóc được | 83/2026/VBHN-TT-BXD Điều 2 khoản 1 |

**Câu trả lời nguyên văn:**

> Hồ sơ thiết kế kiến trúc là thành phần của hồ sơ thiết kế xây dựng được thực hiện thẩm định, phê duyệt theo quy định của Luật xây dựng.  
> Căn cứ: Điều 2 khoản 1 của 83/2026/VBHN-TT-BXD.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 83/2026/VBHN-TT-BXD Điều 2 khoản 1 | Đúng |

---

## 082

| | |
|---|---|
| mã dòng | `082` |
| qid | `q042` |
| nhóm | don_gian |
| biến thể | **Y** |
| gold | 32/2024/QH15 Điều 42 khoản 3 |
| regex bóc được | 32/2024/QH15 Điều 42 khoản 3 |

**Câu trả lời nguyên văn:**

> Không được.  
> Điều 42 khoản 3 của 32/2024/QH15.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 32/2024/QH15 Điều 42 khoản 3 | Đúng |

---

## 083

| | |
|---|---|
| mã dòng | `083` |
| qid | `q142` |
| nhóm | khong_co_dieu |
| biến thể | **Z** |
| gold | 04/CT-BTC (đoạn) |
| regex bóc được | 9/CT-TT |

**Câu trả lời nguyên văn:**

> Chỉ thị số 09/CT-TTg của Thủ tướng Chính phủ.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 09/CT-TTg | Đúng |

---

## 084

| | |
|---|---|
| mã dòng | `084` |
| qid | `q214` |
| nhóm | don_gian · trung lập |
| biến thể | **Y** |
| gold | 200/2026/NĐ-CP Điều 15 khoản 3 |
| regex bóc được | 200/2026/NĐ-CP Điều 9 khoản 4 |

**Câu trả lời nguyên văn:**

> Nhà đầu tư mua trái phiếu là cá nhân phải ký văn bản xác nhận đã thực hiện các quy định tại các điểm a, b, c và d khoản 4 Điều 9 Nghị định 200/2026/NĐ-CP.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 200/2026/NĐ-CP Điều 9 khoản 4 điểm a b c d | Thiếu |

---

## 085

| | |
|---|---|
| mã dòng | `085` |
| qid | `q070` |
| nhóm | xuyen_khoan |
| biến thể | **Z** |
| gold | 32/2024/QH15 Điều 43 khoản 1 + 32/2024/QH15 Điều 43 khoản 2 |
| regex bóc được | *(không bóc được gì)* |

**Câu trả lời nguyên văn:**

> Không đủ căn cứ trong ngữ cảnh được cung cấp.

| Trích dẫn người đọc thấy | regex |
|---|---|
| (không có) | Đúng |

---

## 086

| | |
|---|---|
| mã dòng | `086` |
| qid | `q209` |
| nhóm | don_gian · trung lập |
| biến thể | **Y** |
| gold | 33/2005/QH11 Điều 410 khoản 2 |
| regex bóc được | 33/2005/QH11 Điều 410 khoản 3 |

**Câu trả lời nguyên văn:**

> Không, nếu hợp đồng phụ bị vô hiệu thì hợp đồng chính không bị chấm dứt, trừ trường hợp các bên có thỏa thuận hợp đồng phụ là một phần không thể tách rời của hợp đồng chính.  
> Căn cứ: Điều 410 khoản 3 của 33/2005/QH11.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 33/2005/QH11 Điều 410 khoản 3 | Đúng |

---

## 087

| | |
|---|---|
| mã dòng | `087` |
| qid | `q037` |
| nhóm | don_gian · trung lập |
| biến thể | **X** |
| gold | 107/2026/TT-BTC Điều 7 khoản 2 |
| regex bóc được | 107/2026/TT-BTC Điều 7 khoản 2 |

**Câu trả lời nguyên văn:**

> Chấp hành viên phải kịp thời đề xuất biện pháp xử lý các khoản tiền, tài sản tồn đọng theo quy định của pháp luật với Thủ trưởng đơn vị.  
> Điều 7 khoản 2 của 107/2026/TT-BTC

| Trích dẫn người đọc thấy | regex |
|---|---|
| 107/2026/TT-BTC Điều 7 khoản 2 | Đúng |

---

## 088

| | |
|---|---|
| mã dòng | `088` |
| qid | `q122` |
| nhóm | dieu_dai |
| biến thể | **X** |
| gold | 59/2020/QH14 Điều 4 + 59/2020/QH14 Điều 4 khoản 25 |
| regex bóc được | 59/2020/QH14 Điều 25 khoản 1 |

**Câu trả lời nguyên văn:**

> Theo quy định tại Điều 25 khoản 1 của 59/2020/QH14: Người thành lập doanh nghiệp là cá nhân, tổ chức thành lập hoặc góp vốn để thành lập doanh nghiệp.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 59/2020/QH14 Điều 25 khoản 1 | Đúng |

---

## 089

| | |
|---|---|
| mã dòng | `089` |
| qid | `q046` |
| nhóm | don_gian |
| biến thể | **X** |
| gold | 21/VBHN-BTC Điều 35 khoản 2 điểm a |
| regex bóc được | 105/2020/TT-BTC |

**Câu trả lời nguyên văn:**

> Cơ quan thuế căn cứ vào thông tin trên Hệ thống thông tin đăng ký thuế do Hệ thống thông tin quốc gia về đăng ký doanh nghiệp, đăng ký hợp tác xã gửi đến và quy định tại Thông tư số 105/2020/TT-BTC, Quy chế trao đổi thông tin giữa Bộ Kế hoạch và Đầu tư và Bộ Tài chính để xử lý và trả kết quả hồ sơ.

| Trích dẫn người đọc thấy | regex |
|---|---|
| (không có trích dẫn nguồn; thân bài nhắc 105/2020/TT-BTC) | Thừa |

---

## 090

| | |
|---|---|
| mã dòng | `090` |
| qid | `q217` |
| nhóm | don_gian · trung lập |
| biến thể | **Z** |
| gold | 307/2026/NĐ-CP Điều 6 khoản 1 |
| regex bóc được | 307/2026/NĐ-CP Điều 6 khoản 2 |

**Câu trả lời nguyên văn:**

> Theo Điều 6 khoản 2 của 307/2026/NĐ-CP: Chủ tịch Ủy ban nhân dân cấp xã tùy theo tình hình thực tế, quyết định số lượng người có uy tín của thôn mới nhưng không vượt quá tổng số người có uy tín của các thôn trước khi sáp nhập.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 307/2026/NĐ-CP Điều 6 khoản 2 | Đúng |

---

## 091

| | |
|---|---|
| mã dòng | `091` |
| qid | `q029` |
| nhóm | don_gian |
| biến thể | **Y** |
| gold | 32/2024/QH15 Điều 7 khoản 2 |
| regex bóc được | 32/2024/QH15 Điều 7 khoản 2; 32/2024/QH15 Điều 103 khoản 1; ? Điều 134 khoản 1; 32/2024/QH15 Điều 134 khoản 3 |

**Câu trả lời nguyên văn:**

> Tổ chức tín dụng được quyền từ chối yêu cầu cấp tín dụng của khách hàng trong những trường hợp sau:
> 
> - Không đủ điều kiện, không có hiệu quả, không phù hợp với quy định của pháp luật (Điều 7 khoản 2 của 32/2024/QH15).
> 
> - Khách hàng cung cấp thông tin sai sự thật, vi phạm nội dung thỏa thuận trong hợp đồng, thỏa thuận cấp tín dụng, hợp đồng bảo đảm (Điều 103 khoản 1 của 32/2024/QH15).
> 
> - Khách hàng thuộc đối tượng quy định tại khoản 1 Điều 134, không được cấp tín dụng nếu bảo đảm do đối tượng đó cung cấp (Điều 134 khoản 3 của 32/2024/QH15).

| Trích dẫn người đọc thấy | regex |
|---|---|
| 32/2024/QH15 Điều 7 khoản 2; 32/2024/QH15 Điều 103 khoản 1; 32/2024/QH15 Điều 134 khoản 3; Điều 134 khoản 1 cùng luật | Đúng |

---

## 092

| | |
|---|---|
| mã dòng | `092` |
| qid | `q215` |
| nhóm | don_gian · trung lập |
| biến thể | **Z** |
| gold | 360/2026/NĐ-CP Điều 42 khoản 2 |
| regex bóc được | 360/2026/NĐ-CP Điều 42 khoản 2 |

**Câu trả lời nguyên văn:**

> Trung tâm giáo dục được tổ chức hoạt động trở lại sau khi cấp có thẩm quyền xác nhận đã khắc phục đầy đủ nguyên nhân dẫn đến việc đình chỉ hoặc hết thời hạn 05 ngày làm việc kể từ ngày nhận được báo cáo mà cấp có thẩm quyền không có ý kiến yêu cầu tiếp tục kiểm tra, xử lý.  
> Căn cứ: Điều 42 khoản 2 của 360/2026/NĐ-CP.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 360/2026/NĐ-CP Điều 42 khoản 2 | Đúng |

---

## 093

| | |
|---|---|
| mã dòng | `093` |
| qid | `q148` |
| nhóm | khong_co_dieu |
| biến thể | **Z** |
| gold | 9367 TC/PC (đoạn) |
| regex bóc được | 9367/TC Điều 5 khoản 2 |

**Câu trả lời nguyên văn:**

> Việc đính chính đã bỏ các điểm sau khỏi danh mục:  
> - Điểm 54: Quyết định số 164/2000/QĐ-BTC ngày 10/10/2000  
> - Điểm 115: Quyết định số 214/2003/QĐ-BTC ngày 18/12/2003  
> - Điểm 121: Quyết định số 01/2000/QĐ-BVGCP ngày 5/1/2000  
> 
> Căn cứ: Điều 5 khoản 2 của 9367/TC/PC.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 9367/TC/PC Điều 5 khoản 2 | Đúng |

---

## 094

| | |
|---|---|
| mã dòng | `094` |
| qid | `q050` |
| nhóm | don_gian |
| biến thể | **Z** |
| gold | 10/2026/VBHN-NĐ-BNV Điều 14 |
| regex bóc được | 10/2026/VBHN-NĐ-BNV Điều 2 khoản 2 |

**Câu trả lời nguyên văn:**

> Theo quy định hiện hành, người đứng đầu cơ quan có thẩm quyền tuyển dụng có trách nhiệm quyết định tiếp nhận vào làm công chức đối với các trường hợp quy định tại khoản 1 Điều này nếu đáp ứng các tiêu chuẩn, điều kiện sau.
> 
> Căn cứ: Điều 2 khoản 2 của 10/2026/VBHN-NĐ-BNV.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 10/2026/VBHN-NĐ-BNV Điều 2 khoản 2 | Đúng |

---

## 095

| | |
|---|---|
| mã dòng | `095` |
| qid | `q214` |
| nhóm | don_gian · trung lập |
| biến thể | **Z** |
| gold | 200/2026/NĐ-CP Điều 15 khoản 3 |
| regex bóc được | 200/2026/NĐ-CP Điều 9 khoản 4 |

**Câu trả lời nguyên văn:**

> Nhà đầu tư mua trái phiếu là cá nhân phải ký văn bản xác nhận đã thực hiện các quy định tại các điểm a, b, c và d khoản 4 Điều 9 Nghị định 200/2026/NĐ-CP.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 200/2026/NĐ-CP Điều 9 khoản 4 điểm a b c d | Thiếu |

---

## 096

| | |
|---|---|
| mã dòng | `096` |
| qid | `q090` |
| nhóm | dan_chieu |
| biến thể | **Y** |
| gold | 101/2015/QH13 Điều 248 khoản 2 + 101/2015/QH13 Điều 132 khoản 2 |
| regex bóc được | 101/2015/QH13 Điều 132 khoản 2 |

**Câu trả lời nguyên văn:**

> Quyết định đình chỉ vụ án phải ghi rõ lý do đình chỉ và các nội dung quy định tại khoản 2 Điều 132 của Bộ luật Tố tụng hình sự số 101/2015/QH13.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 101/2015/QH13 Điều 132 khoản 2 | Đúng |

---

## 097

| | |
|---|---|
| mã dòng | `097` |
| qid | `q209` |
| nhóm | don_gian · trung lập |
| biến thể | **Z** |
| gold | 33/2005/QH11 Điều 410 khoản 2 |
| regex bóc được | 33/2005/QH11 Điều 411 khoản 3 |

**Câu trả lời nguyên văn:**

> Không. Theo Điều 411 khoản 3 của 33/2005/QH11: "Sự vô hiệu của hợp đồng phụ không làm chấm dứt hợp đồng chính, trừ trường hợp các bên thoả thuận hợp đồng phụ là một phần không thể tách rời của hợp đồng chính."

| Trích dẫn người đọc thấy | regex |
|---|---|
| 33/2005/QH11 Điều 411 khoản 3 | Đúng |

---

## 098

| | |
|---|---|
| mã dòng | `098` |
| qid | `q264` |
| nhóm | xuyen_khoan · trung lập |
| biến thể | **Z** |
| gold | 126/2025/QH15 Điều 28 khoản 2 điểm c |
| regex bóc được | 126/2025/QH15 Điều 5 khoản 2 |

**Câu trả lời nguyên văn:**

> Có được xét cấp thẻ nhà báo.  
> Căn cứ: Điều 5 khoản 2 của 126/2025/QH15.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 126/2025/QH15 Điều 5 khoản 2 | Đúng |

---

## 099

| | |
|---|---|
| mã dòng | `099` |
| qid | `q015` |
| nhóm | don_gian |
| biến thể | **Y** |
| gold | 19/2021/TT-BTC Điều 3 khoản 1 |
| regex bóc được | 19/2021/TT-BTC Điều 3 khoản 1 |

**Câu trả lời nguyên văn:**

> Giao dịch thuế điện tử là các giao dịch được các cơ quan, tổ chức, cá nhân thực hiện bằng phương thức điện tử thuộc phạm vi điều chỉnh của Thông tư này.  
> Điều 3 khoản 1 của 19/2021/TT-BTC

| Trích dẫn người đọc thấy | regex |
|---|---|
| 19/2021/TT-BTC Điều 3 khoản 1 | Đúng |

---

## 100

| | |
|---|---|
| mã dòng | `100` |
| qid | `q146` |
| nhóm | khong_co_dieu |
| biến thể | **Y** |
| gold | 05/TB-VPCP (đoạn) |
| regex bóc được | *(không bóc được gì)* |

**Câu trả lời nguyên văn:**

> Không đủ căn cứ trong ngữ cảnh được cung cấp.

| Trích dẫn người đọc thấy | regex |
|---|---|
| (không có) | Đúng |

---

## 101

| | |
|---|---|
| mã dòng | `101` |
| qid | `q260` |
| nhóm | dieu_dai · trung lập |
| biến thể | **X** |
| gold | 200/2026/NĐ-CP Điều 9 khoản 4 + 200/2026/NĐ-CP Điều 9 khoản 4 điểm e |
| regex bóc được | *(không bóc được gì)* |

**Câu trả lời nguyên văn:**

> Không đủ căn cứ trong ngữ cảnh được cung cấp.

| Trích dẫn người đọc thấy | regex |
|---|---|
| (không có) | Đúng |

---

## 102

| | |
|---|---|
| mã dòng | `102` |
| qid | `q015` |
| nhóm | don_gian |
| biến thể | **X** |
| gold | 19/2021/TT-BTC Điều 3 khoản 1 |
| regex bóc được | 19/2021/TT-BTC Điều 3 khoản 1 |

**Câu trả lời nguyên văn:**

> Giao dịch thuế điện tử là các giao dịch được các cơ quan, tổ chức, cá nhân thực hiện bằng phương thức điện tử thuộc phạm vi điều chỉnh của Thông tư này.  
> Căn cứ: Điều 3 khoản 1 của 19/2021/TT-BTC.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 19/2021/TT-BTC Điều 3 khoản 1 | Đúng |

---

## 103

| | |
|---|---|
| mã dòng | `103` |
| qid | `q122` |
| nhóm | dieu_dai |
| biến thể | **Y** |
| gold | 59/2020/QH14 Điều 4 + 59/2020/QH14 Điều 4 khoản 25 |
| regex bóc được | 59/2020/QH14 Điều 4 khoản 25 |

**Câu trả lời nguyên văn:**

> Người thành lập doanh nghiệp là cá nhân, tổ chức thành lập hoặc góp vốn để thành lập doanh nghiệp.  
> Điều 4 khoản 25 của 59/2020/QH14.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 59/2020/QH14 Điều 4 khoản 25 | Đúng |

---

## 104

| | |
|---|---|
| mã dòng | `104` |
| qid | `q118` |
| nhóm | dieu_dai |
| biến thể | **X** |
| gold | 19/2021/TT-BTC Điều 10 khoản 3 |
| regex bóc được | 19/2021/TT-BTC Điều 42 |

**Câu trả lời nguyên văn:**

> Người nộp thuế thực hiện theo quy định tại Điều 42 của Thông tư số 19/2021/TT-BTC.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 19/2021/TT-BTC Điều 42 | Đúng |

---

## 105

| | |
|---|---|
| mã dòng | `105` |
| qid | `q126` |
| nhóm | dieu_dai |
| biến thể | **X** |
| gold | 259/2026/NĐ-CP Điều 31 khoản 4 |
| regex bóc được | 10/2026/VBHN-NĐ-BNV Điều 5 khoản 2 |

**Câu trả lời nguyên văn:**

> Điều 5 khoản 2 của 10/2026/VBHN-NĐ-BNV

| Trích dẫn người đọc thấy | regex |
|---|---|
| 10/2026/VBHN-NĐ-BNV Điều 5 khoản 2 | Đúng |

---

## 106

| | |
|---|---|
| mã dòng | `106` |
| qid | `q018` |
| nhóm | don_gian |
| biến thể | **X** |
| gold | 200/2026/NĐ-CP Điều 39 khoản 2 |
| regex bóc được | 200/2026/NĐ-CP Điều 39 khoản 2 |

**Câu trả lời nguyên văn:**

> - Báo cáo định kỳ hàng quý, hằng năm.  
> - Báo cáo trong trường hợp phát hiện doanh nghiệp phát hành có hành vi vi phạm pháp luật trong việc thực hiện các cam kết với nhà đầu tư.  
> 
> Căn cứ: Điều 39 khoản 2 của 200/2026/NĐ-CP.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 200/2026/NĐ-CP Điều 39 khoản 2 | Đúng |

---

## 107

| | |
|---|---|
| mã dòng | `107` |
| qid | `q264` |
| nhóm | xuyen_khoan · trung lập |
| biến thể | **Y** |
| gold | 126/2025/QH15 Điều 28 khoản 2 điểm c |
| regex bóc được | 126/2025/QH15 Điều 28 khoản 2 |

**Câu trả lời nguyên văn:**

> Có được xét cấp thẻ nhà báo.  
> Căn cứ: Điều 28 khoản 2 của 126/2025/QH15.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 126/2025/QH15 Điều 28 khoản 2 | Đúng |

---

## 108

| | |
|---|---|
| mã dòng | `108` |
| qid | `q143` |
| nhóm | khong_co_dieu |
| biến thể | **Y** |
| gold | 334/CT-TTg (đoạn) |
| regex bóc được | 334/CT-TT Điều 10 khoản 1 |

**Câu trả lời nguyên văn:**

> Việc giao đất lâm nghiệp cho tổ chức, hộ gia đình, cá nhân và cộng đồng thôn, bản phải bảo đảm từng diện tích đất có chủ cụ thể.  
> Căn cứ: Điều 10 khoản 1 của 334/CT-TTg.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 334/CT-TTg Điều 10 khoản 1 | Đúng |

---

## 109

| | |
|---|---|
| mã dòng | `109` |
| qid | `q124` |
| nhóm | dieu_dai |
| biến thể | **X** |
| gold | 200/2026/NĐ-CP Điều 9 khoản 5 + 200/2026/NĐ-CP Điều 9 khoản 5 điểm d |
| regex bóc được | 200/2026/NĐ-CP Điều 5 |

**Câu trả lời nguyên văn:**

> Nhà đầu tư mua lại trái phiếu doanh nghiệp riêng lẻ từ một nhà đầu tư khác có quyền đòi bên bán cung cấp đầy đủ nội dung công bố thông tin của doanh nghiệp phát hành theo quy định tại Nghị định này.  
> Căn cứ: Điều 5 khoản g của Nghị định số 200/2026/NĐ-CP.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 200/2026/NĐ-CP Điều 5 khoản g | Thiếu |

---

## 110

| | |
|---|---|
| mã dòng | `110` |
| qid | `q018` |
| nhóm | don_gian |
| biến thể | **Y** |
| gold | 200/2026/NĐ-CP Điều 39 khoản 2 |
| regex bóc được | 200/2026/NĐ-CP Điều 39 khoản 2 |

**Câu trả lời nguyên văn:**

> Đại diện người sở hữu trái phiếu thực hiện chế độ báo cáo cho Sở giao dịch chứng khoán định kỳ hàng quý, hằng năm và báo cáo trong trường hợp phát hiện doanh nghiệp phát hành có hành vi vi phạm pháp luật trong việc thực hiện các cam kết với nhà đầu tư.  
> Căn cứ: Điều 39 khoản 2 của 200/2026/NĐ-CP.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 200/2026/NĐ-CP Điều 39 khoản 2 | Đúng |

---

## 111

| | |
|---|---|
| mã dòng | `111` |
| qid | `q144` |
| nhóm | khong_co_dieu |
| biến thể | **Y** |
| gold | 1408/CT-TTg (đoạn) |
| regex bóc được | 1408/CT-TT Điều 3 |

**Câu trả lời nguyên văn:**

> Công an các cấp cần:
> - Xây dựng và thực hiện các kế hoạch đấu tranh quyết liệt, liên tục với tội phạm xâm hại trẻ em, tội phạm trong lứa tuổi chưa thành niên;
> - Tăng cường công tác xác minh đối với hồ sơ của trẻ em có nguồn gốc không rõ ràng nhưng được giới thiệu làm con nuôi người nước ngoài;
> - Nghiêm khắc xử lý các hành vi làm giả hồ sơ về nguồn gốc của trẻ em, đưa hối lộ, nhận hối lộ liên quan đến việc giải quyết cho trẻ em làm con nuôi người nước ngoài hoặc lợi dụng việc giới thiệu, giải quyết, đăng ký cho trẻ em làm con nuôi người nước ngoài để trục lợi, thu lợi vật chất bất hợp pháp.
> 
> Căn cứ: Điều 3 khoản b của Chỉ thị số 1408/CT-TTg.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 1408/CT-TTg Điều 3 khoản b | Thiếu |

---

## 112

| | |
|---|---|
| mã dòng | `112` |
| qid | `q235` |
| nhóm | dan_chieu · trung lập |
| biến thể | **Y** |
| gold | 101/2015/QH13 Điều 128 khoản 4 điểm c + 101/2015/QH13 Điều 178 |
| regex bóc được | ? Điều 128 khoản 4 điểm a; 101/2015/QH13 Điều 128 khoản 4; 101/2015/QH13 Điều 178 |

**Câu trả lời nguyên văn:**

> - Biên bản kê biên phải ghi rõ tên và tình trạng từng tài sản bị kê biên.  
> - Ý kiến, khiếu nại của những người có mặt (điểm a khoản 4 Điều 128) được ghi vào biên bản, có chữ ký xác nhận của họ và của người tiến hành kê biên.  
> - Những người phải ký tên: người tiến hành kê biên, những người có mặt gồm bị can, bị cáo hoặc người đủ 18 tuổi trong gia đình hoặc người đại diện của bị can, bị cáo, đại diện chính quyền xã, phường, thị trấn nơi có tài sản bị kê biên, người chứng kiến.  
> 
> Căn cứ:  
> Điều 128 khoản 4 của 101/2015/QH13  
> Điều 178 của 101/2015/QH13

| Trích dẫn người đọc thấy | regex |
|---|---|
| 101/2015/QH13 Điều 128 khoản 4; 101/2015/QH13 Điều 178; điểm a khoản 4 Điều 128 nội bộ | Thiếu |

---

## 113

| | |
|---|---|
| mã dòng | `113` |
| qid | `q148` |
| nhóm | khong_co_dieu |
| biến thể | **Y** |
| gold | 9367 TC/PC (đoạn) |
| regex bóc được | ? Điều 1 |

**Câu trả lời nguyên văn:**

> Việc đính chính đã bỏ các điểm sau khỏi danh mục:  
> - Điểm 54 (Quyết định số 164/2000/QĐ-BTC ngày 10/10/2000)  
> - Điểm 115 (Quyết định số 214/2003/QĐ-BTC ngày 18/12/2003)  
> - Điểm 121 (Quyết định số 01/2000/QĐ-BVGCP ngày 5/1/2000)  
> 
> Căn cứ: Điều 1 của 9367 TC/PC.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 9367 TC/PC Điều 1 | Đúng |

---

## 114

| | |
|---|---|
| mã dòng | `114` |
| qid | `q266` |
| nhóm | xuyen_khoan · trung lập |
| biến thể | **Z** |
| gold | 200/2026/NĐ-CP Điều 12 khoản 3 điểm b |
| regex bóc được | 200/2026/NĐ-CP Điều 5 khoản 3 |

**Câu trả lời nguyên văn:**

> Không được thực hiện nếu không có sự đồng ý từ 65% tổng số trái phiếu cùng loại đang lưu hành trở lên.  
> Căn cứ: Điều 5 khoản 3 của 200/2026/NĐ-CP.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 200/2026/NĐ-CP Điều 5 khoản 3 | Đúng |

---

## 115

| | |
|---|---|
| mã dòng | `115` |
| qid | `q143` |
| nhóm | khong_co_dieu |
| biến thể | **X** |
| gold | 334/CT-TTg (đoạn) |
| regex bóc được | 334/CT-TT Điều 10 khoản 1 |

**Câu trả lời nguyên văn:**

> Việc giao đất lâm nghiệp cho tổ chức, hộ gia đình, cá nhân và cộng đồng thôn, bản phải bảo đảm từng diện tích đất có chủ cụ thể.  
> Căn cứ: Điều 10 khoản 1 của 334/CT-TTg.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 334/CT-TTg Điều 10 khoản 1 | Đúng |

---

## 116

| | |
|---|---|
| mã dòng | `116` |
| qid | `q018` |
| nhóm | don_gian |
| biến thể | **Z** |
| gold | 200/2026/NĐ-CP Điều 39 khoản 2 |
| regex bóc được | 200/2026/NĐ-CP Điều 39 khoản 2 |

**Câu trả lời nguyên văn:**

> - Báo cáo định kỳ hàng quý, hằng năm;  
> - Báo cáo trong trường hợp phát hiện doanh nghiệp phát hành có hành vi vi phạm pháp luật trong việc thực hiện các cam kết với nhà đầu tư.  
> 
> Căn cứ: Điều 39 khoản 2 của 200/2026/NĐ-CP.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 200/2026/NĐ-CP Điều 39 khoản 2 | Đúng |

---

## 117

| | |
|---|---|
| mã dòng | `117` |
| qid | `q264` |
| nhóm | xuyen_khoan · trung lập |
| biến thể | **X** |
| gold | 126/2025/QH15 Điều 28 khoản 2 điểm c |
| regex bóc được | 126/2025/QH15 Điều 28 khoản 1 điểm c |

**Câu trả lời nguyên văn:**

> Có được xét cấp thẻ nhà báo.  
> Căn cứ: Điều 28 khoản 1 điểm c của 126/2025/QH15.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 126/2025/QH15 Điều 28 khoản 1 điểm c | Đúng |

---

## 118

| | |
|---|---|
| mã dòng | `118` |
| qid | `q047` |
| nhóm | don_gian |
| biến thể | **X** |
| gold | 10/2026/VBHN-NĐ-BNV Điều 67 |
| regex bóc được | 10/2026/VBHN-NĐ-BNV Điều 67 khoản 1 điểm a |

**Câu trả lời nguyên văn:**

> Ủy ban nhân dân cấp tỉnh có trách nhiệm thống nhất quản lý công chức và thực hiện các nội dung quản lý công chức trên địa bàn.  
> Căn cứ: Điều 67 khoản 1 điểm a của 10/2026/VBHN-NĐ-BNV.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 10/2026/VBHN-NĐ-BNV Điều 67 khoản 1 điểm a | Đúng |

---

## 119

| | |
|---|---|
| mã dòng | `119` |
| qid | `q057` |
| nhóm | xuyen_khoan |
| biến thể | **Y** |
| gold | 101/2015/QH13 Điều 122 khoản 1 + 101/2015/QH13 Điều 122 khoản 2 |
| regex bóc được | 101/2015/QH13 Điều 122 khoản 2 |

**Câu trả lời nguyên văn:**

> Theo khoản 2 Điều 122 của 101/2015/QH13: Bị can, bị cáo vi phạm nghĩa vụ cam đoan quy định tại khoản này thì bị tạm giam và số tiền đã đặt bị tịch thu, nộp ngân sách nhà nước.

| Trích dẫn người đọc thấy | regex |
|---|---|
| 101/2015/QH13 Điều 122 khoản 2 | Đúng |

---

## 120

| | |
|---|---|
| mã dòng | `120` |
| qid | `q128` |
| nhóm | dieu_dai |
| biến thể | **Y** |
| gold | 107/2026/TT-BTC Điều 10 khoản 7 + 107/2026/TT-BTC Điều 10 khoản 7 điểm a |
| regex bóc được | 107/2026/TT-BTC Điều 10 khoản 7 |

**Câu trả lời nguyên văn:**

> Không được. Điều 10 khoản 7 của 107/2026/TT-BTC quy định: "Đơn vị không được phép thay đổi thông tin, số liệu trên sổ kế toán sau khi đã khóa sổ kế toán và báo cáo tài chính, báo cáo nghiệp vụ thi hành án dân sự đã được nộp cho cơ quan có thẩm quyền."

| Trích dẫn người đọc thấy | regex |
|---|---|
| 107/2026/TT-BTC Điều 10 khoản 7 | Đúng |

---

