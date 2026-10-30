# Phân tích lỗi trích dẫn — B và E2 (bộ chính 110 câu, lượt local GPU)

Nguồn: `chi_tiet_cau.jsonl`, `pilot_tra_loi.jsonl` cùng thư mục (bước 1–2). Câu *sai* = đúng toàn phần mức Điều bằng 0. Mỗi câu sai vào đúng một thùng, xét theo thứ tự T6 → T1 → T2 → T5 → T4 → T3 (lỗi đầu chuỗi trước: đã không truy hồi được thì không xét trích dẫn). Bộ bóc trích dẫn là regex đã chốt (khớp 0,825 với 120 nhãn tay), không sửa.

| thùng | định nghĩa |
|---|---|
| T1 truy hồi hụt | gold không nằm trọn trong 50 ứng viên |
| T2 ngoài ngân sách | có trong 50 ứng viên nhưng không vào ngữ cảnh 1.200 từ |
| T3 có mà không dẫn | gold trong ngữ cảnh, không trích sai, nhưng thiếu gold |
| T4 dẫn sai | có ít nhất một trích dẫn không phải gold |
| T5 từ chối sai | gold trong ngữ cảnh mà mô hình từ chối |
| T6 cắt trần | chạm 384 token |

## 1. Bảng đếm

| thùng | B | E2 |
|---|---:|---:|
| đúng | 59 | 48 |
| T1 truy hồi hụt | 3 | 5 |
| T2 ngoài ngân sách | 12 | 17 |
| T3 có mà không dẫn | 4 | 5 |
| T4 dẫn sai | 30 | 32 |
| T5 từ chối sai | 1 | 0 |
| T6 cắt trần | 1 | 3 |

### Theo nhóm (B / E2)

| nhóm | n | T1 | T2 | T3 | T4 | T5 | T6 |
|---|---:|---|---|---|---|---|---|
| don_gian | 50 | 0 / 0 | 4 / 8 | 1 / 0 | 13 / 11 | 0 / 0 | 1 / 2 |
| dieu_dai | 19 | 1 / 3 | 2 / 3 | 0 / 1 | 2 / 6 | 0 / 0 | 0 / 0 |
| xuyen_khoan | 17 | 0 / 0 | 1 / 1 | 0 / 0 | 2 / 3 | 1 / 0 | 0 / 1 |
| khong_co_dieu | 15 | 0 / 0 | 2 / 2 | 0 / 1 | 13 / 12 | 0 / 0 | 0 / 0 |
| dan_chieu | 9 | 2 / 2 | 3 / 3 | 3 / 3 | 0 / 0 | 0 / 0 | 0 / 0 |

### T4 tách nhỏ

| loại | B | E2 |
|---|---:|---:|
| bịa Điều cho văn bản không chia Điều | 13 | 12 |
| dẫn nhầm Điều | 4 | 10 |
| dẫn thừa (đủ gold, thêm Điều khác) | 11 | 9 |
| đúng số Điều, sai văn bản (bản hợp nhất / bản khác) | 2 | 1 |
| *trong đó có ≥ 1 Điều không hề có trong ngữ cảnh (tự đoán)* | 14 | 18 |

### T1 tách nhỏ

| loại | B | E2 |
|---|---:|---:|
| hụt một phần gold (≥ 1 đơn vị đã vào 50 ứng viên) | 3 | 5 |

### Câu đổi thùng giữa B và E2

| B → E2 | số câu |
|---|---:|
| đúng → T4 | 10 |
| T4 → T2 | 4 |
| đúng → T2 | 3 |
| T4 → đúng | 2 |
| đúng → T1 | 2 |
| T2 → đúng | 2 |
| T4 → T6 | 1 |
| T3 → T2 | 1 |
| T2 → T6 | 1 |
| T5 → đúng | 1 |
| T4 → T3 | 1 |
| đúng → T3 | 1 |

## 2. Ví dụ thật — 3 câu mỗi thùng

Ngữ cảnh rút gọn: mỗi khối = số hiệu + 30 từ đầu; ★ = khối chạm gold (độ phủ ≥ τ = 0,5). Lý do: tự động từ số liệu, kèm nhận xét đọc tay.

### T1 — truy hồi hụt (8 lượt: B 3, E2 5)

**q090 · B · dan_chieu** — Quyết định đình chỉ vụ án hình sự phải ghi rõ những nội dung gì?

- gold: 101/2015/QH13 Điều 248 khoản 2; 101/2015/QH13 Điều 132 khoản 2
- ngữ cảnh: #1 [101/2015/QH13] [101/2015/QH13] [Bộ luật Tố tụng hình sự số 101/2015/QH13] > Chương XXI > Mục II > Điều 282. Đình chỉ vụ án Điều 282. Đình chỉ vụ án 1. Thẩm … ‖ #2 [101/2015/QH13] [101/2015/QH13] [Bộ luật Tố tụng hình sự số 101/2015/QH13] > Chương XVII > Điều 234. Kết luận điều tra trong trường hợp đình chỉ điều tra Điều 234. Kết luận … ‖ ★#3 [101/2015/QH13] [101/2015/QH13] [Bộ luật Tố tụng hình sự số 101/2015/QH13] > Chương XIX > Điều 248. Đình chỉ vụ án Điều 248. Đình chỉ vụ án 1. Viện kiểm sát quyết … ‖ #4 [101/2015/QH13] [101/2015/QH13] [Bộ luật Tố tụng hình sự số 101/2015/QH13] > Chương XXI > Mục II > Điều 281. Tạm đình chỉ vụ án Điều 281. Tạm đình chỉ vụ án … ‖ #5 [100/2015/QH13] [100/2015/QH13] [Bộ luật Hình sự số 100/2015/QH13] > Chương VIII > Mục 1 > Điều 51. Các tình tiết giảm nhẹ trách nhiệm hình sự > Khoản 2 2. Khi … ‖ #6 [24/2004/QH11] [24/2004/QH11] [Bộ luật Tố tụng dân sự số 24/2004/QH11] > Chương XVIII > Điều 300. Huỷ bản án, quyết định đã có hiệu lực pháp luật và đình chỉ giải … ‖ #7 [101/2015/QH13] [101/2015/QH13] [Bộ luật Tố tụng hình sự số 101/2015/QH13] > Chương XX > Điều 260. Bản án > Khoản 2 > Điểm g g) Quyết định của Hội đồng xét … ‖ #8 [101/2015/QH13] [101/2015/QH13] [Bộ luật Tố tụng hình sự số 101/2015/QH13] > Chương VI > Điều 106. Xử lý vật chứng > Khoản 1 Điều 106. Xử lý vật chứng 1. Việc …
- trả lời: Quyết định đình chỉ vụ án phải ghi rõ lý do đình chỉ và các nội dung quy định tại khoản 2 Điều 132 của Bộ luật Tố tụng hình sự số 101/2015/QH13.
- trích bóc được: Điều 132 khoản 2
- lý do: chunk gold đầu tiên ở hạng 3; độ phủ gold trong 50 ứng viên 0.00

**q127 · B · dieu_dai** — Trong thi công xây dựng, khi xảy ra tình trạng công trình hoặc phần kết cấu phụ trợ bị hư hỏng nghiêm trọng đến mức có nguy cơ sập đổ, điều đó được coi là gì?

- gold: 135/2025/QH15 Điều 3; 135/2025/QH15 Điều 3 khoản 29
- ngữ cảnh: ★#1 [135/2025/QH15] [135/2025/QH15] [Luật Xây dựng số 135/2025/QH15] > Chương I > Điều 3. Giải thích từ ngữ > Khoản 29 29. Sự cố công trình xây dựng là hư hỏng vượt … ‖ #2 [135/2025/QH15] [135/2025/QH15] [Luật Xây dựng số 135/2025/QH15] > Chương IV > Mục 2 > Điều 55. Sự cố công trình xây dựng Điều 55. Sự cố công trình xây dựng 1. … ‖ #3 [135/2025/QH15] [135/2025/QH15] [Luật Xây dựng số 135/2025/QH15] > Chương I > Điều 3. Giải thích từ ngữ > Khoản 30 30. Vùng nguy hiểm trong thi công xây dựng công trình … ‖ #4 [45/2024/QH15] [45/2024/QH15] [Luật Di sản văn hóa số 45/2024/QH15] > Chương III > Mục 1 > Điều 30. Dự án đầu tư xây dựng, xây dựng công trình, nhà ở riêng … ‖ #5 [135/2025/QH15] [135/2025/QH15] [Luật Xây dựng số 135/2025/QH15] > Chương IV > Mục 2 > Điều 51. An toàn trong thi công xây dựng công trình Điều 51. An toàn trong thi …
- trả lời: Sự cố công trình xây dựng theo Điều 55 khoản 1 điểm a, b, c của Luật Xây dựng số 135/2025/QH15.
- trích bóc được: Điều 55 khoản 1, Điều 55 khoản 1, Điều 55 khoản 1
- lý do: chunk gold đầu tiên ở hạng 1; độ phủ gold trong 50 ứng viên 0.00

**q259 · B · dan_chieu** — Khi xét lại quyết định của Tòa án về yêu cầu công nhận và cho thi hành phán quyết của Trọng tài nước ngoài bị kháng cáo, kháng nghị, nếu người phải thi hành vắng mặt thì phiên họp có vẫn được tiến hành không và trong trường hợp nào?

- gold: 24/2004/QH11 Điều 373 khoản 2; 24/2004/QH11 Điều 369 khoản 3
- ngữ cảnh: ★#1 [24/2004/QH11] [24/2004/QH11] [Bộ luật Tố tụng dân sự số 24/2004/QH11] > Chương XXIX > Điều 369. Phiên họp xét đơn yêu cầu Điều 369. Phiên họp xét đơn yêu cầu 1. … ‖ #2 [24/2004/QH11] [24/2004/QH11] [Bộ luật Tố tụng dân sự số 24/2004/QH11] > Chương XXVII > Điều 355. Phiên họp xét đơn yêu cầu Điều 355. Phiên họp xét đơn yêu cầu 1. … ‖ #3 [101/2015/QH13] [101/2015/QH13] [Bộ luật Tố tụng hình sự số 101/2015/QH13] > Chương XXII > Mục II > Điều 351. Sự có mặt của người bào chữa, người bảo vệ quyền và … ‖ #4 [24/2004/QH11] [24/2004/QH11] [Bộ luật Tố tụng dân sự số 24/2004/QH11] > Chương XIV > Mục 2 > Điều 215. Xem xét, quyết định hoãn phiên toà khi có người vắng mặt … ‖ #5 [24/2004/QH11] [24/2004/QH11] [Bộ luật Tố tụng dân sự số 24/2004/QH11] > Chương XIV > Mục 1 > Điều 205. Sự có mặt của người giám định Điều 205. Sự có mặt … ‖ #6 [24/2004/QH11] [24/2004/QH11] [Bộ luật Tố tụng dân sự số 24/2004/QH11] > Chương XIV > Mục 1 > Điều 206. Sự có mặt của người phiên dịch Điều 206. Sự có mặt …
- trả lời: Khi người phải thi hành vắng mặt, phiên họp vẫn được tiến hành nếu người phải thi hành hoặc người đại diện hợp pháp của họ đã được triệu tập hợp lệ đến lần thứ hai mà vẫn vắng mặt, theo Điều 369 khoản 3 của 24/2004/QH11.
- trích bóc được: Điều 369 khoản 3
- lý do: chunk gold đầu tiên ở hạng 1; độ phủ gold trong 50 ứng viên 0.00

### T2 — ngoài ngân sách (29 lượt: B 12, E2 17)

**q014 · B · don_gian** — Sau khi ra quyết định trưng cầu giám định trong vụ án hình sự, cơ quan trưng cầu phải chuyển hồ sơ, đối tượng giám định cho người giám định trong thời hạn bao lâu?

- gold: 101/2015/QH13 Điều 205 khoản 3
- ngữ cảnh: #1 [101/2015/QH13] [101/2015/QH13] [Bộ luật Tố tụng hình sự số 101/2015/QH13] > Chương XXIV > Điều 367. Thủ tục xem xét bản án tử hình trước khi thi hành > Khoản 1 … ‖ #2 [101/2015/QH13] [101/2015/QH13] [Bộ luật Tố tụng hình sự số 101/2015/QH13] > Chương XIX > Điều 244. Chuyển hồ sơ vụ án và bản cáo trạng đến Tòa án Điều 244. Chuyển … ‖ #3 [101/2015/QH13] [101/2015/QH13] [Bộ luật Tố tụng hình sự số 101/2015/QH13] > Chương XXV > Điều 376. Chuyển hồ sơ vụ án để xem xét kháng nghị theo thủ tục giám đốc … ‖ #4 [101/2015/QH13] [101/2015/QH13] [Bộ luật Tố tụng hình sự số 101/2015/QH13] > Chương X > Điều 169. Chuyển vụ án để điều tra > Khoản 4 4. Trong thời hạn 03 ngày … ‖ #5 [101/2015/QH13] [101/2015/QH13] [Bộ luật Tố tụng hình sự số 101/2015/QH13] > Chương XVIII > Điều 239. Thẩm quyền truy tố > Khoản 2 2. Trong thời hạn 03 ngày kể từ … ‖ #6 [101/2015/QH13] [101/2015/QH13] [Bộ luật Tố tụng hình sự số 101/2015/QH13] > Chương XV > Điều 213. Kết luận giám định Điều 213. Kết luận giám định 1. Kết luận giám định … ‖ #7 [101/2015/QH13] [101/2015/QH13] [Bộ luật Tố tụng hình sự số 101/2015/QH13] > Chương XIX > Điều 249. Phục hồi vụ án > Khoản 3 3. Trong thời hạn 03 ngày kể từ … ‖ #8 [101/2015/QH13] [101/2015/QH13] [Bộ luật Tố tụng hình sự số 101/2015/QH13] > Chương X > Điều 169. Chuyển vụ án để điều tra > Khoản 3 3. Thủ tục chuyển vụ án …
- trả lời: Không đủ căn cứ trong ngữ cảnh được cung cấp.
- trích bóc được: (không có)
- lý do: chunk gold đầu tiên ở hạng 15; ngữ cảnh 8 khối / 1098 từ đã đầy trước khi tới

**q024 · B · don_gian** — Trong tố tụng dân sự, người bị tố cáo có nghĩa vụ gì khi cơ quan, người có thẩm quyền yêu cầu cung cấp thông tin, tài liệu và khi có quyết định xử lý?

- gold: 24/2004/QH11 Điều 400 khoản 2
- ngữ cảnh: #1 [34/2024/QH15] [34/2024/QH15] [Luật Tổ chức Toà án nhân dân số số: 34/2024/QH15] > Chương I > Điều 15. Việc thu thập tài liệu, chứng cứ trong xét xử, giải quyết vụ … ‖ #2 [101/2015/QH13] [101/2015/QH13] [Bộ luật Tố tụng hình sự số 101/2015/QH13] > Chương XXXIII > Điều 479. Quyền và nghĩa vụ của người tố cáo Điều 479. Quyền và nghĩa vụ của … ‖ #3 [24/2004/QH11] [24/2004/QH11] [Bộ luật Tố tụng dân sự số 24/2004/QH11] > Chương II > Điều 24. Bảo đảm quyền khiếu nại, tố cáo trong tố tụng dân sự Điều 24. Bảo … ‖ #4 [24/2004/QH11] [24/2004/QH11] [Bộ luật Tố tụng dân sự số 24/2004/QH11] > Chương XXXIII > Điều 399. Quyền, nghĩa vụ của người tố cáo Điều 399. Quyền, nghĩa vụ của người tố … ‖ #5 [101/2015/QH13] [101/2015/QH13] [Bộ luật Tố tụng hình sự số 101/2015/QH13] > Chương IV > Điều 71. Trách nhiệm thông báo, giải thích và bảo đảm thực hiện quyền và nghĩa vụ … ‖ #6 [101/2015/QH13] [101/2015/QH13] [Bộ luật Tố tụng hình sự số 101/2015/QH13] > Chương II > Điều 17. Trách nhiệm của cơ quan, người có thẩm quyền tiến hành tố tụng Điều 17. … ‖ #7 [24/2004/QH11] [24/2004/QH11] [Bộ luật Tố tụng dân sự số 24/2004/QH11] > Chương II > Điều 7. Trách nhiệm cung cấp chứng cứ của cá nhân, cơ quan, tổ chức có thẩm … ‖ #8 [24/2004/QH11] [24/2004/QH11] [Bộ luật Tố tụng dân sự số 24/2004/QH11] > Chương XII > Điều 173. Nhiệm vụ, quyền hạn của Thẩm phán khi lập hồ sơ vụ án Điều 173. … ‖ #9 [101/2015/QH13] [101/2015/QH13] [Bộ luật Tố tụng hình sự số 101/2015/QH13] > Chương XXIX > Điều 435. Quyền và nghĩa vụ của người đại diện theo pháp luật của pháp nhân > …
- trả lời: Không đủ căn cứ trong ngữ cảnh được cung cấp.
- trích bóc được: (không có)
- lý do: chunk gold đầu tiên ở hạng 37; ngữ cảnh 9 khối / 1158 từ đã đầy trước khi tới

**q048 · B · don_gian** — Theo quy định hiện hành, sau khi tiếp nhận hồ sơ đăng ký thuế lần đầu bằng phương thức điện tử, Cổng thông tin điện tử của Tổng cục Thuế gửi thông báo tiếp nhận cho người nộp thuế trong thời hạn nào và thông báo đó nêu những nội dung gì?

- gold: 21/VBHN-BTC Điều 13 khoản 1
- ngữ cảnh: #1 [19/2021/TT-BTC] [19/2021/TT-BTC] [Thông tư số 19/2021/TT-BTC Hướng dẫn giao dịch điện tử trong lĩnh vực thuế] > Chương II > Mục 2 > Điều 13. Tiếp nhận hồ sơ và trả … ‖ #2 [19/2021/TT-BTC] [19/2021/TT-BTC] [Thông tư số 19/2021/TT-BTC Hướng dẫn giao dịch điện tử trong lĩnh vực thuế] > Chương II > Mục 2 > Điều 13. Tiếp nhận hồ sơ và trả … ‖ #3 [19/2021/TT-BTC] [19/2021/TT-BTC] [Thông tư số 19/2021/TT-BTC Hướng dẫn giao dịch điện tử trong lĩnh vực thuế] > Chương II > Mục 3 > Điều 16. Khai thuế điện tử > Khoản … ‖ #4 [19/2021/TT-BTC] [19/2021/TT-BTC] [Thông tư số 19/2021/TT-BTC Hướng dẫn giao dịch điện tử trong lĩnh vực thuế] > Chương II > Mục 5 > Điều 27. Tiếp nhận hồ sơ đề nghị … ‖ #5 [21/VBHN-BTC] [21/VBHN-BTC] [Văn bản hợp nhất số 21/VBHN-BTC hợp nhất Thông tư số 19/2021/TT-BTC hướng dẫn giao dịch điện tử trong lĩnh vực thuế] > Chương II > Mục 2 > … ‖ #6 [19/2021/TT-BTC] [19/2021/TT-BTC] [Thông tư số 19/2021/TT-BTC Hướng dẫn giao dịch điện tử trong lĩnh vực thuế] > Chương II > Mục 2 > Điều 13. Tiếp nhận hồ sơ và trả … ‖ #7 [21/VBHN-BTC] [21/VBHN-BTC] [Văn bản hợp nhất số 21/VBHN-BTC hợp nhất Thông tư số 19/2021/TT-BTC hướng dẫn giao dịch điện tử trong lĩnh vực thuế] > Chương II > Mục 3 > …
- trả lời: Chậm nhất 15 phút kể từ khi nhận được hồ sơ điện tử của người nộp thuế. Thông báo tiếp nhận nêu rõ thời gian, địa điểm trả kết quả, đồng thời yêu cầu người nộp thuế mang hồ sơ giấy đến trụ sở cơ quan thuế. Căn cứ: Điều 13 khoản 2 điểm b của Thông tư số 19/2021/TT-BTC.
- trích bóc được: Điều 13 khoản 2
- lý do: chunk gold đầu tiên ở hạng — (gold rải nhiều chunk, không chunk nào ≥ τ); ngữ cảnh 7 khối / 1083 từ đã đầy trước khi tới

### T3 — có mà không dẫn (9 lượt: B 4, E2 5)

**q046 · B · don_gian** — Theo quy định hiện hành, cơ quan thuế căn cứ vào những thông tin và quy định nào để xử lý, trả kết quả hồ sơ đăng ký doanh nghiệp, hợp tác xã nhận qua Hệ thống thông tin quốc gia về đăng ký doanh nghiệp, đăng ký hợp tác xã?

- gold: 21/VBHN-BTC Điều 35 khoản 2
- ngữ cảnh: #1 [19/2021/TT-BTC] [19/2021/TT-BTC] [Thông tư số 19/2021/TT-BTC Hướng dẫn giao dịch điện tử trong lĩnh vực thuế] > Chương III > Điều 35. Tiếp nhận và giải quyết hồ sơ đăng ký … ‖ #2 [21/VBHN-BTC] [21/VBHN-BTC] [Văn bản hợp nhất số 21/VBHN-BTC hợp nhất Thông tư số 19/2021/TT-BTC hướng dẫn giao dịch điện tử trong lĩnh vực thuế] > Chương III > Điều 35. Tiếp … ‖ #3 [19/2021/TT-BTC] [19/2021/TT-BTC] [Thông tư số 19/2021/TT-BTC Hướng dẫn giao dịch điện tử trong lĩnh vực thuế] > Chương III > Điều 35. Tiếp nhận và giải quyết hồ sơ đăng ký … ‖ ★#4 [21/VBHN-BTC] [21/VBHN-BTC] [Văn bản hợp nhất số 21/VBHN-BTC hợp nhất Thông tư số 19/2021/TT-BTC hướng dẫn giao dịch điện tử trong lĩnh vực thuế] > Chương III > Điều 35. Tiếp …
- trả lời: Cơ quan thuế căn cứ vào thông tin trên Hệ thống thông tin đăng ký thuế do Hệ thống thông tin quốc gia về đăng ký doanh nghiệp, đăng ký hợp tác xã gửi đến và quy định tại Thông tư số 105/2020/TT-BTC, Quy chế trao đổi thông tin giữa Bộ Kế hoạch và Đầu tư và Bộ Tài chính để xử lý và trả kết quả hồ sơ.
- trích bóc được: (không có)
- lý do: gold ở khối #4 / 4; độ phủ 0.00, độ chính xác 0.00

**q094 · B · dan_chieu** — Khi nào bên thế chấp được phép thay thế tài sản thế chấp mà không cần sự đồng ý của bên nhận thế chấp?

- gold: 33/2005/QH11 Điều 354 khoản 1; 33/2005/QH11 Điều 349 khoản 3
- ngữ cảnh: ★#1 [33/2005/QH11] [33/2005/QH11] [Bộ luật Dân sự số 33/2005/QH11] > Chương XVII > Mục 5 > Điều 354. Thay thế và sửa chữa tài sản thế chấp Điều 354. Thay thế và … ‖ ★#2 [33/2005/QH11] [33/2005/QH11] [Bộ luật Dân sự số 33/2005/QH11] > Chương XVII > Mục 5 > Điều 349. Quyền của bên thế chấp tài sản Điều 349. Quyền của bên thế chấp … ‖ #3 [33/2005/QH11] [33/2005/QH11] [Bộ luật Dân sự số 33/2005/QH11] > Chương XVII > Mục 5 > Điều 342. Thế chấp tài sản Điều 342. Thế chấp tài sản 1. Thế chấp tài … ‖ #4 [33/2005/QH11] [33/2005/QH11] [Bộ luật Dân sự số 33/2005/QH11] > Chương XVII > Mục 5 > Điều 356. Hủy bỏ việc thế chấp tài sản Điều 356. Hủy bỏ việc thế chấp … ‖ #5 [33/2005/QH11] [33/2005/QH11] [Bộ luật Dân sự số 33/2005/QH11] > Chương XVII > Mục 5 > Điều 348. Nghĩa vụ của bên thế chấp tài sản Điều 348. Nghĩa vụ của bên …
- trả lời: Khi tài sản thế chấp là hàng hóa luân chuyển trong quá trình sản xuất, kinh doanh, bên thế chấp được phép thay thế tài sản thế chấp mà không cần sự đồng ý của bên nhận thế chấp, theo Điều 349 khoản 3 của Bộ luật Dân sự số 33/2005/QH11.
- trích bóc được: Điều 349 khoản 3
- lý do: gold ở khối #1 / 5; độ phủ 0.50, độ chính xác 1.00

**q097 · B · dan_chieu** — Trong vận chuyển hàng hóa bằng đường biển, ai là người nhận hàng hợp pháp khi vận đơn là vận đơn theo lệnh, vận đơn vô danh hoặc vận đơn đích danh?

- gold: 95/2015/QH13 Điều 147 khoản 5; 95/2015/QH13 Điều 162
- ngữ cảnh: ★#1 [95/2015/QH13] [95/2015/QH13] [Bộ luật Hàng hải số 95/2015/QH13] > Chương VII > Mục 1 > Điều 162. Chuyển nhượng vận đơn Điều 162. Chuyển nhượng vận đơn 1. Vận đơn theo … ‖ #2 [42-LCT/HĐNN8] [42-LCT/HĐNN8] [Bộ luật Hàng hải số 42-LCT/HĐNN8] > Chương V > Mục C > Điều 84. Vận đơn có thể được chuyển nhượng theo các nguyên tắc sau đây: Điều … ‖ ★#3 [95/2015/QH13] [95/2015/QH13] [Bộ luật Hàng hải số 95/2015/QH13] > Chương VII > Mục 1 > Điều 147. Các bên liên quan đến hợp đồng vận chuyển hàng hóa bằng đường biển … ‖ #4 [95/2015/QH13] [95/2015/QH13] [Bộ luật Hàng hải số 95/2015/QH13] > Chương VII > Mục 1 > Điều 159. Ký phát vận đơn Điều 159. Ký phát vận đơn 1. Theo yêu cầu … ‖ #5 [95/2015/QH13] [95/2015/QH13] [Bộ luật Hàng hải số 95/2015/QH13] > Chương VII > Mục 1 > Điều 164. Áp dụng đối với vận đơn suốt đường biển Điều 164. Áp dụng đối … ‖ #6 [42-LCT/HĐNN8] [42-LCT/HĐNN8] [Bộ luật Hàng hải số 42-LCT/HĐNN8] > Chương V > Mục C > Điều 83. 1- Vận đơn có thể được ký phát dưới các dạng sau đây: Điều … ‖ #7 [42-LCT/HĐNN8] [42-LCT/HĐNN8] [Bộ luật Hàng hải số 42-LCT/HĐNN8] > Chương V > Mục C > Điều 87. 1- Việc vận chuyển hàng hoá được thực hiện với sự tham gia của … ‖ #8 [95/2015/QH13] [95/2015/QH13] [Bộ luật Hàng hải số 95/2015/QH13] > Chương VII > Mục 1 > Điều 166. Nghĩa vụ trả hàng Điều 166. Nghĩa vụ trả hàng Khi tàu biển đến …
- trả lời: - Khi vận đơn là vận đơn theo lệnh: Người cuối cùng có quyền phát lệnh trả hàng trong vận đơn theo lệnh là người nhận hàng hợp pháp. Căn cứ: Điều 162 khoản 1 của 95/2015/QH13. - Khi vận đơn là vận đơn vô danh: Người xuất trình vận đơn vô danh là người nhận hàng hợp pháp. Căn cứ: Điều 162 khoản 2 của 95/2015/QH13. - Khi vận đơn là vận đơn đích danh: Người có tên trong …
- trích bóc được: Điều 162 khoản 1, Điều 162 khoản 2, Điều 162 khoản 3
- lý do: gold ở khối #1 / 8; độ phủ 0.50, độ chính xác 1.00

### T4 — dẫn sai (62 lượt: B 30, E2 32)

**q003 · B · don_gian** — Người vi phạm nội quy phiên tòa hoặc phiên hòa giải, đối thoại tại Tòa án có thể bị áp dụng những biện pháp xử lý nào?

- gold: 34/2024/QH15 Điều 139 khoản 4
- ngữ cảnh: ★#1 [34/2024/QH15] [34/2024/QH15] [Luật Tổ chức Toà án nhân dân số số: 34/2024/QH15] > Chương VII > Điều 139. Nội quy phiên tòa, phiên họp Điều 139. Nội quy phiên tòa, phiên … ‖ #2 [101/2015/QH13] [101/2015/QH13] [Bộ luật Tố tụng hình sự số 101/2015/QH13] > Chương XXXII > Điều 467. Xử lý người vi phạm nội quy phiên tòa Điều 467. Xử lý người vi … ‖ #3 [24/2004/QH11] [24/2004/QH11] [Bộ luật Tố tụng dân sự số 24/2004/QH11] > Chương XXXII > Điều 387. Biện pháp xử lý người vi phạm nội quy phiên toà Điều 387. Biện pháp … ‖ #4 [34/2024/QH15] [34/2024/QH15] [Luật Tổ chức Toà án nhân dân số số: 34/2024/QH15] > Chương VII > Điều 138. Phòng hòa giải, đối thoại Điều 138. Phòng hòa giải, đối thoại 1. … ‖ #5 [33/2005/QH11] [33/2005/QH11] [Bộ luật Dân sự số 33/2005/QH11] > Chương II > Điều 12. Nguyên tắc hoà giải Điều 12. Nguyên tắc hoà giải Trong quan hệ dân sự, việc hoà … ‖ #6 [24/2004/QH11] [24/2004/QH11] [Bộ luật Tố tụng dân sự số 24/2004/QH11] > Chương XIV > Mục 4 > Điều 233. Phát biểu khi tranh luận và đối đáp Điều 233. Phát biểu …
- trả lời: - Bị Thẩm phán chủ tọa phiên tòa quyết định xử phạt hành chính, phạt tiền, cảnh cáo, buộc rời khỏi phòng xử án hoặc tạm giữ hành chính (Điều 467 khoản 1 của 101/2015/QH13). - Bị cấm vào hoặc buộc rời khỏi phòng xử án, phòng hòa giải, đối thoại (Điều 139 khoản 3 của 34/2024/QH15). - Bị tạm giữ hành chính hoặc truy cứu trách nhiệm hình sự theo quy định của pháp luật (Điều 139 khoản 4 …
- trích bóc được: Điều 467 khoản 1, Điều 139 khoản 3, Điều 139 khoản 4, Điều 387 khoản 1, Điều 467 khoản 3, Điều 387
- lý do: gold ở khối #1 / 6; độ phủ 1.00, độ chính xác 0.33; dẫn thừa (đủ gold, thêm Điều khác)

**q008 · B · don_gian** — Khi kinh doanh dịch vụ tại một bảo tàng, doanh nghiệp cần đảm bảo điều gì để không vi phạm quy định?

- gold: 45/2024/QH15 Điều 81 khoản 2
- ngữ cảnh: ★#1 [45/2024/QH15] [45/2024/QH15] [Luật Di sản văn hóa số 45/2024/QH15] > Chương VI > Điều 81. Kinh doanh dịch vụ bảo tàng Điều 81. Kinh doanh dịch vụ bảo tàng 1. Cơ … ‖ #2 [45/2024/QH15] [45/2024/QH15] [Luật Di sản văn hóa số 45/2024/QH15] > Chương I > Điều 9. Các hành vi bị nghiêm cấm > Khoản 10 10. Kinh doanh dịch vụ về di … ‖ #3 [45/2024/QH15] [45/2024/QH15] [Luật Di sản văn hóa số 45/2024/QH15] > Chương VI > Điều 80. Kinh doanh di vật, cổ vật Điều 80. Kinh doanh di vật, cổ vật 1. Tổ … ‖ #4 [45/2024/QH15] [45/2024/QH15] [Luật Di sản văn hóa số 45/2024/QH15] > Chương III > Mục 2 > Điều 46. Yêu cầu bảo vệ, bảo quản di vật, cổ vật, bảo vật quốc … ‖ #5 [45/2024/QH15] [45/2024/QH15] [Luật Di sản văn hóa số 45/2024/QH15] > Chương VI > Điều 79. Kinh doanh giám định di vật, cổ vật Điều 79. Kinh doanh giám định di vật, … ‖ #6 [314/2026/NĐ-CP] [314/2026/NĐ-CP] [Nghị định số 314/2026/NĐ-CP Quy định hoạt động của sàn dữ liệu] > Chương IV > Điều 17. Điều kiện đối với dữ liệu, sản phẩm, dịch vụ về …
- trả lời: Khi kinh doanh dịch vụ tại một bảo tàng, doanh nghiệp cần đảm bảo: - Hoạt động kinh doanh dịch vụ bảo tàng phải phù hợp với nhiệm vụ của bảo tàng quy định tại Điều 68 của Luật Di sản văn hóa số 45/2024/QH15. - Đáp ứng một trong các điều kiện tại khoản 1 Điều 81 của Luật này: được thành lập bảo tàng công lập theo quy định tại Điều 65 hoặc được cấp giấy phép hoạt …
- trích bóc được: Điều 68, Điều 81 khoản 1, Điều 65, Điều 67, Điều 9 khoản 10
- lý do: gold ở khối #1 / 6; độ phủ 1.00, độ chính xác 0.20; dẫn thừa (đủ gold, thêm Điều khác)

**q011 · B · don_gian** — Bên chậm thực hiện nghĩa vụ dân sự có trách nhiệm gì đối với bên có quyền?

- gold: 33/2005/QH11 Điều 286 khoản 2
- ngữ cảnh: #1 [33/2005/QH11] [33/2005/QH11] [Bộ luật Dân sự số 33/2005/QH11] > Chương XVII > Mục 3 > Điều 306. Trách nhiệm dân sự do chậm tiếp nhận việc thực hiện nghĩa vụ dân … ‖ ★#2 [33/2005/QH11] [33/2005/QH11] [Bộ luật Dân sự số 33/2005/QH11] > Chương XVII > Mục 2 > Điều 286. Chậm thực hiện nghĩa vụ dân sự Điều 286. Chậm thực hiện nghĩa vụ … ‖ #3 [33/2005/QH11] [33/2005/QH11] [Bộ luật Dân sự số 33/2005/QH11] > Chương XVII > Mục 3 > Điều 305. Trách nhiệm dân sự do chậm thực hiện nghĩa vụ dân sự Điều 305. … ‖ #4 [33/2005/QH11] [33/2005/QH11] [Bộ luật Dân sự số 33/2005/QH11] > Chương XVII > Mục 6 > Điều 376. Hoàn thành nghĩa vụ dân sự trong trường hợp bên có quyền chậm tiếp … ‖ #5 [33/2005/QH11] [33/2005/QH11] [Bộ luật Dân sự số 33/2005/QH11] > Chương XVII > Mục 3 > Điều 302. Trách nhiệm dân sự do vi phạm nghĩa vụ dân sự Mục 3 TRÁCH … ‖ #6 [33/2005/QH11] [33/2005/QH11] [Bộ luật Dân sự số 33/2005/QH11] > Chương XVII > Mục 2 > Điều 288. Chậm tiếp nhận việc thực hiện nghĩa vụ dân sự Điều 288. Chậm tiếp … ‖ #7 [33/2005/QH11] [33/2005/QH11] [Bộ luật Dân sự số 33/2005/QH11] > Chương XVII > Mục 2 > Điều 285. Thời hạn thực hiện nghĩa vụ dân sự Điều 285. Thời hạn thực hiện …
- trả lời: Bên chậm thực hiện nghĩa vụ dân sự phải: - Thông báo ngay cho bên có quyền về việc không thực hiện nghĩa vụ đúng thời hạn (Điều 286 khoản 1 của 33/2005/QH11). - Nếu quá thời hạn và nghĩa vụ vẫn chưa được hoàn thành, phải thực hiện nghĩa vụ và bồi thường thiệt hại (Điều 305 khoản 1 của 33/2005/QH11). - Trả lãi đối với số tiền chậm trả theo lãi suất cơ bản do Ngân hàng Nhà …
- trích bóc được: Điều 286 khoản 1, Điều 305 khoản 1, Điều 305 khoản 2
- lý do: gold ở khối #2 / 7; độ phủ 1.00, độ chính xác 0.50; dẫn thừa (đủ gold, thêm Điều khác)

### T5 — từ chối sai (1 lượt: B 1, E2 0)

**q070 · B · xuyen_khoan** — Trong một tổ chức tín dụng, giữa Chủ tịch Hội đồng quản trị và một thành viên Hội đồng quản trị không độc lập, ai được phép kiêm nhiệm chức Tổng giám đốc của chính tổ chức tín dụng đó?

- gold: 32/2024/QH15 Điều 43 khoản 1; 32/2024/QH15 Điều 43 khoản 2
- ngữ cảnh: ★#1 [32/2024/QH15] [32/2024/QH15] [Luật Các tổ chức tín dụng số 32/2024/QH15] > Chương IV > Mục 1 > Điều 43. Những trường hợp không cùng đảm nhiệm chức vụ > Khoản 1 … ‖ #2 [32/2024/QH15] [32/2024/QH15] [Luật Các tổ chức tín dụng số 32/2024/QH15] > Chương I > Điều 4. Giải thích từ ngữ > Khoản 26 26. Người quản lý tổ chức tín dụng … ‖ #3 [32/2024/QH15] [32/2024/QH15] [Luật Các tổ chức tín dụng số 32/2024/QH15] > Chương IV > Mục 5 > Điều 79. Hội đồng thành viên của tổ chức tín dụng là công ty … ‖ ★#4 [32/2024/QH15] [32/2024/QH15] [Luật Các tổ chức tín dụng số 32/2024/QH15] > Chương IV > Mục 1 > Điều 43. Những trường hợp không cùng đảm nhiệm chức vụ > Khoản 2 … ‖ #5 [32/2024/QH15] [32/2024/QH15] [Luật Các tổ chức tín dụng số 32/2024/QH15] > Chương IV > Mục 1 > Điều 43. Những trường hợp không cùng đảm nhiệm chức vụ > Khoản 3 … ‖ #6 [32/2024/QH15] [32/2024/QH15] [Luật Các tổ chức tín dụng số 32/2024/QH15] > Chương IV > Mục 3 > Điều 70. Nhiệm vụ, quyền hạn của Hội đồng quản trị của tổ chức … ‖ #7 [32/2024/QH15] [32/2024/QH15] [Luật Các tổ chức tín dụng số 32/2024/QH15] > Chương IV > Mục 6 > Điều 96. Quyền, nghĩa vụ của Tổng giám đốc (Giám đốc) của tổ chức … ‖ #8 [32/2024/QH15] [32/2024/QH15] [Luật Các tổ chức tín dụng số 32/2024/QH15] > Chương IV > Mục 6 > Điều 88. Nhiệm vụ, quyền hạn của Hội đồng quản trị của tổ chức … ‖ #9 [32/2024/QH15] [32/2024/QH15] [Luật Các tổ chức tín dụng số 32/2024/QH15] > Chương IV > Mục 6 > Điều 87. Hội đồng quản trị của tổ chức tín dụng là hợp tác … ‖ #10 [32/2024/QH15] [32/2024/QH15] [Luật Các tổ chức tín dụng số 32/2024/QH15] > Chương IV > Mục 6 > Điều 96. Quyền, nghĩa vụ của Tổng giám đốc (Giám đốc) của tổ chức … ‖ #11 [32/2024/QH15] [32/2024/QH15] [Luật Các tổ chức tín dụng số 32/2024/QH15] > Chương IV > Mục 2 > Điều 55. Tổng giám đốc (Giám đốc) Điều 55. Tổng giám đốc (Giám đốc) …
- trả lời: Không đủ căn cứ trong ngữ cảnh được cung cấp.
- trích bóc được: (không có)
- lý do: gold ở khối #1 nhưng mô hình từ chối

### T6 — cắt trần (4 lượt: B 1, E2 3)

**q021 · B · don_gian** — Khi sử dụng kinh phí hỗ trợ từ Quỹ hỗ trợ xây dựng chính sách, pháp luật, cần đảm bảo những nguyên tắc và điều kiện nào?

- gold: 10/2026/TT-BTP Điều 3 khoản 1
- ngữ cảnh: ★#1 [10/2026/TT-BTP] [10/2026/TT-BTP] [Thông tư số 10/2026/TT-BTP Hướng dẫn việc hỗ trợ, tài trợ và quản lý, sử dụng kinh phí hỗ trợ, tài trợ của Quỹ hỗ trợ xây dựng chính … ‖ #2 [10/2026/TT-BTP] [10/2026/TT-BTP] [Thông tư số 10/2026/TT-BTP Hướng dẫn việc hỗ trợ, tài trợ và quản lý, sử dụng kinh phí hỗ trợ, tài trợ của Quỹ hỗ trợ xây dựng chính … ‖ #3 [10/2026/TT-BTP] [10/2026/TT-BTP] [Thông tư số 10/2026/TT-BTP Hướng dẫn việc hỗ trợ, tài trợ và quản lý, sử dụng kinh phí hỗ trợ, tài trợ của Quỹ hỗ trợ xây dựng chính … ‖ #4 [10/2026/TT-BTP] [10/2026/TT-BTP] [Thông tư số 10/2026/TT-BTP Hướng dẫn việc hỗ trợ, tài trợ và quản lý, sử dụng kinh phí hỗ trợ, tài trợ của Quỹ hỗ trợ xây dựng chính … ‖ #5 [10/2026/TT-BTP] [10/2026/TT-BTP] [Thông tư số 10/2026/TT-BTP Hướng dẫn việc hỗ trợ, tài trợ và quản lý, sử dụng kinh phí hỗ trợ, tài trợ của Quỹ hỗ trợ xây dựng chính … ‖ #6 [10/2026/TT-BTP] [10/2026/TT-BTP] [Thông tư số 10/2026/TT-BTP Hướng dẫn việc hỗ trợ, tài trợ và quản lý, sử dụng kinh phí hỗ trợ, tài trợ của Quỹ hỗ trợ xây dựng chính … ‖ #7 [10/2026/TT-BTP] [10/2026/TT-BTP] [Thông tư số 10/2026/TT-BTP Hướng dẫn việc hỗ trợ, tài trợ và quản lý, sử dụng kinh phí hỗ trợ, tài trợ của Quỹ hỗ trợ xây dựng chính …
- trả lời: (rỗng)
- trích bóc được: (không có)
- lý do: chạm 384 token khi đang trả lời

**q029 · E2 · don_gian** — Tổ chức tín dụng được quyền từ chối yêu cầu cấp tín dụng của khách hàng trong những trường hợp nào?

- gold: 32/2024/QH15 Điều 7 khoản 2
- ngữ cảnh: ★#1 [32/2024/QH15] [32/2024/QH15] [Luật Các tổ chức tín dụng số 32/2024/QH15] > Chương I > Điều 7. Quyền tự chủ trong hoạt động kinh doanh Điều 7. Quyền tự chủ trong hoạt … ‖ #2 [32/2024/QH15] [32/2024/QH15] [Luật Các tổ chức tín dụng số 32/2024/QH15] > Chương V > Mục 1 > Điều 102. Xét duyệt cấp tín dụng, kiểm tra sử dụng vốn vay, tài … ‖ #3 [32/2024/QH15] [32/2024/QH15] [Luật Các tổ chức tín dụng số 32/2024/QH15] > Chương VII > Điều 134. Những trường hợp không được cấp tín dụng Chương VII CÁC HẠN CHẾ ĐỂ BẢO …
- trả lời: (rỗng)
- trích bóc được: (không có)
- lý do: chạm 384 token khi đang trả lời

**q064 · E2 · xuyen_khoan** — Người vi phạm quy định về an toàn giao thông đường bộ bị phạt khác nhau thế nào giữa trường hợp đã gây tai nạn chết người hoặc thiệt hại tài sản và trường hợp mới có khả năng thực tế gây thiệt hại nếu không được ngăn chặn kịp thời?

- gold: 100/2015/QH13 Điều 260 khoản 1; 100/2015/QH13 Điều 260 khoản 5
- ngữ cảnh: #1 [100/2015/QH13] [100/2015/QH13] [Bộ luật Hình sự số 100/2015/QH13] > Chương XXI > Mục 1 > Điều 261. Tội cản trở giao thông đường bộ Điều 261. Tội cản trở giao thông …
- trả lời: (rỗng)
- trích bóc được: (không có)
- lý do: chạm 384 token khi đang trả lời

## 3. Số liệu cho bảng cải tiến

Ước lượng *trên chính câu trả lời đã sinh* (không chạy lại) — là cận trên vì đổi lời nhắc có thể làm hỏng câu đang đúng.

| đo | B | E2 |
|---|---:|---:|
| T4 văn bản không chia Điều: bỏ số Điều bịa thì đúng | 12 | 11 |
| T3/T4: chỉ giữ trích dẫn đầu tiên thì đúng (gold 1 đơn vị) | 6 | 4 |
| T3/T4: bỏ trích dẫn của văn bản không phải gold thì đúng | 3 | 3 |
| T2: hạng chunk gold đầu tiên (999 = gold rải nhiều chunk, không chunk nào ≥ τ) | [1, 1, 2, 3, 4, 5, 6, 11, 14, 15, 37, 999] | [2, 2, 2, 3, 3, 4, 4, 4, 4, 5, 6, 7, 11, 15, 16, 37, 999] |
| T1 / T5 / T6 | 3 / 1 / 1 | 5 / 0 / 3 |

## 4. Nhận xét (đọc tay các ví dụ trên)

- **T4 là thùng lớn nhất** (B 30, E2 32), và gần một nửa không phải lỗi hiểu luật: ở nhóm `khong_co_dieu` mô hình **bịa số Điều** cho văn bản vốn không chia Điều (thông báo, chỉ thị) — q139 "Điều 5 khoản 2 của 05/TB-VPCP". Nội dung trả lời thường đúng; chỉ cần bỏ số Điều là khớp gold (12 câu B, 11 câu E2). Đây là lý do cả 8 phương pháp đều 0,000 ở nhóm này (bảng 2 của metrics_trich_dan.md).
- **Dẫn thừa**: mô hình dẫn thêm Điều ở văn bản khác có trong ngữ cảnh (q003 dẫn cả Điều 467 BLTTHS và Điều 387 BLTTDS bên cạnh Điều 139 Luật TCTAND đúng). Tiêu chí chính *khớp hoàn toàn* phạt mọi trích dẫn thừa (cột phụ *đủ gold* thì không).
- **E2 thua B chủ yếu vì mở rộng Điều**: 10 câu B đúng mà E2 rơi vào T4, gần hết là *dẫn nhầm Điều*. Khối mở rộng lên cả Điều dài làm ngữ cảnh còn 1–2 khối; nhãn "Điều N" chỉ ở đầu khối nên mô hình gán khoản sang Điều khác hoặc lấy số khoản làm số Điều (q120: gold Điều 89 khoản 6 → E2 dẫn "Điều 6"; q039: Điều 46 khoản 3 → "Điều 3 khoản 3"). Đây là vấn đề *nhãn trong ngữ cảnh*, không phải truy hồi (R@5 của E2 = B).
- **Đúng số Điều, sai văn bản**: dẫn bản khác của cùng văn bản. Từ 30/10 bảng cặp tương đương được áp ở tầng trích dẫn, nên q010 (dẫn 83/2026/VBHN-TT-BXD thay 03/2020/TT-BXD, cùng Điều 2 khoản 1) nay tính là đúng; các ca còn lại ở thùng này là câu phiên bản (không áp bảng cặp) hoặc cặp văn bản ngoài bảng.
- **T1 đều là hụt một phần** gold nhiều đơn vị: một đơn vị vào 50 ứng viên, đơn vị kia (thường là đích dẫn chiếu, nhóm `dan_chieu`) thì không. Riêng q127 (và q122, cùng dạng): gold có một đơn vị cấp Điều mà span là **câu dẫn** "Trong Luật này, các từ ngữ dưới đây được hiểu như sau:" (12 từ, KHÔNG phải cả Điều — bản trước ghi sai, xem `results/nhat_ky_sua_loi.md` 30/10). Câu dẫn nằm trong chunk "Điều 3 … Khoản 1", chunk đó đứng hạng 779 (q122: 2.156) nên không vào 50 ứng viên.
- **T2**: chunk gold đầu tiên ở hạng ≤ 6 ở 7/12 câu B — phần lớn là gold nhiều đơn vị, một đơn vị đã vào ngữ cảnh, đơn vị kia nằm ngoài 1.200 từ.
- **T5, T6 nhỏ**. q021 cắt trần ở cả 8 phương pháp (câu trả lời liệt kê dài, chạm 384 token) — lỗi của câu hỏi chứ không của phương pháp.

## 5. Cải tiến — xếp theo số câu kỳ vọng cứu được

Số câu: cận trên ước trên câu trả lời đã sinh (mục 3), B / E2. Regex chấm **không đổi**. Sau khi duyệt (30/10): giữ #1, #2, #3 làm thử nghiệm ở bước 4 (`results/local_gpu/thu_them.md`, mỗi mục có kiểm soát chạy cùng lượt); #6 xử lý bằng sửa bộ chấm; **bỏ** bốn đề xuất cũ: chỉ dẫn đơn vị trực tiếp trả lời (dẫn thừa), E3 + rerank, MAX_TOKENS 512, lời nhắc bớt thận trọng.

| # | thùng | cách sửa | câu kỳ vọng (B / E2) | chi phí | rủi ro với tính công bằng | trạng thái |
|---:|---|---|---|---|---|---|
| 1 | T4 bịa Điều | Lời nhắc P1: "đoạn không có 'Điều' thì chỉ ghi số hiệu, không tự đặt số Điều" | ≤ 12 / ≤ 11 | 1 dòng lời nhắc; sinh lại cả 8 phương pháp | Trung bình: C và D sẽ bớt *tự đoán* — báo trước/sau P1 cho C và D ở nhóm `khong_co_dieu` | thử nghiệm 4.5: P1 × 8 phương pháp, kiểm soát lời nhắc gốc cùng lượt |
| 2 | T4 dẫn nhầm sau mở rộng | Tầng sinh: gắn lại nhãn "(Điều N khoản k)" ở đầu mỗi khoản trong khối mở rộng (không đụng chuỗi nhúng) | 0 / ≤ 10 | ~20 dòng ở `truy_hoi.ngu_canh` | Thấp: biến thể riêng E2n, E2 không đổi | thử nghiệm 4.5: E2n so với kiểm soát E2 |
| 3 | T2 ngoài ngân sách | Ngân sách 600 / 1.200 / 1.800 / 2.400 từ | ≤ 12 / ≤ 17 | 2.400 từ vượt n_ctx 4096 → nâng n_ctx 8192 **chỉ cho lượt 2.400 từ** | Thấp nếu mọi phương pháp cùng ngân sách | thử nghiệm 4.2 |
| 6 | T4 sai văn bản | Áp bảng cặp tương đương **đã chốt** (`eval/cap_tuong_duong.csv`) ở tầng trích dẫn như tầng truy hồi; câu phiên bản không áp | đã áp: B +1, E2 +1 (q010) | 0 | Thấp: luật tương đương có từ trước, đã ghi trong `eval/cham.py` là dùng cho cả hai tầng; trước 30/10 tầng trích dẫn bỏ sót — đây là sửa lỗi cài đặt, không phải luật mới | đã làm (`results/nhat_ky_sua_loi.md`) |

Thời gian chạy: 25 s.
