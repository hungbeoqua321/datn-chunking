# Kế hoạch phân tích (cam kết TRƯỚC khi chạy đánh giá)

Tệp này được commit trước bước 5, kèm hash của `eval/questions.jsonl` (dòng cuối), để chứng minh độ đo chính,
cách chấm và cách kết luận được chốt trước khi thấy số liệu — không chọn độ đo sau khi đã biết kết quả.

## So sánh chính (bảng kết luận)
- **A** (cửa sổ 300 từ) với **B** (theo Điều → khoản → điểm). Đề cương so sánh hai phương pháp này; các biến thể khác
  là đối chứng, xếp ở phần riêng.
- **Độ đo chính:** Recall@5 (τ = 0,5) trên toàn bộ bộ câu hỏi, B − A, bootstrap ghép cặp 1000 lần phân tầng theo nhóm,
  CI95 percentile. Khoảng chứa 0 → ghi "chưa đủ bằng chứng", không viết "B tốt hơn".
- **Độ đo phụ có kiểm định:** B − A theo 5 nhóm câu hỏi trên Recall@5, hiệu chỉnh Holm cho 5 phép so sánh (báo cả p gốc
  và p đã hiệu chỉnh; McNemar chính xác cho recall nhị phân). Mọi độ đo khác ghi là **thăm dò**.

## Hai trục so sánh — bắt buộc báo cả hai
1. **Cố định số chunk k** (Recall@1/3/5/10, MRR): đúng như đề; trả lời "trong k kết quả đầu, có gold không".
2. **Cố định ngân sách từ W** (Recall@300/600/1500 từ nội dung): lấy chunk theo thứ hạng tới khi đủ W từ rồi dừng.
   Lý do: B có chunk trung vị 93 từ, A 300 từ; ở cùng k = 5, A đưa ra ≈ 1.500 từ còn B ≈ 465 từ — B lợi về độ mịn
   (xếp hạng chính xác hơn) nhưng thiệt về lượng thông tin, nên Recall@k khập khiễng theo cả hai chiều. Trục W so
   ở cùng lượng văn bản. Kết luận chỉ chắc khi hai trục cùng chiều; nếu ngược chiều thì báo đúng như vậy.
- Kèm: số từ / số token trung bình thật sự truy hồi ở mỗi k và mỗi W, cho mọi phương pháp.

## Sinh câu trả lời
- Ngữ cảnh cho mô hình sinh lấy theo **cùng một ngân sách 2.000 token** (tokenizer của mô hình sinh) cho mọi phương
  pháp, không cố định số khối (B được nhiều khối hơn A vì chunk nhỏ hơn). Báo cáo số khối và số từ nội dung thực dùng.
- Mô hình sinh chạy tại chỗ trên CPU (Qwen3-4B-Instruct-2507 Q4_0, llama.cpp, temperature 0): ~1,5–2 phút/câu.
  Vì vậy **truy hồi chạy đủ 3 seed** (rẻ), còn **sinh chỉ chạy 1 seed (seed 0)** cho A, B, B+; A+ sinh thêm nếu còn thời
  gian. Lựa chọn này ghi rõ trong báo cáo.
- Độ chính xác trích dẫn: 3 mức (văn bản / Điều / khoản), tách P(trích được) × P(đúng | trích được); "không đủ căn cứ"
  tính là sai; kèm tỷ lệ từ chối, tỷ lệ trích dẫn bịa, độ chính xác của các bộ trích dẫn.

## Đối chứng (phần riêng, không vào bảng kết luận)
- **A+** (A + tiêu đề văn bản): nếu B thắng A nhưng chỉ ngang A+ → lợi thế đến từ gắn metadata, không phải từ cắt đúng
  ranh giới điều khoản, và kết luận phải đổi.
- **A_H** (cửa sổ + tiền tố phân cấp), **B−** (B không tiền tố): hiệu ứng ranh giới = ½[(B−−A)+(B−A_H)],
  hiệu ứng tiền tố = ½[(A_H−A)+(B−B−)] — chỉ đo truy hồi.
- **B+** (B mở rộng lên Điều cha khi sinh): so với B ở trục ngân sách W và ở mức sinh.

## Độ ổn định
- 3 seed lệch điểm bắt đầu cửa sổ (A, A+, fallback của B): trung bình và min–max.
- 3 lần lấy mẫu phân tầng 80% bộ câu hỏi (đúng chữ "chia tập" của đề): trung bình và min–max.
- Độ nhạy: τ = 0,9; bootstrap theo cụm văn bản. Chênh lệch < 0,01 coi là nhiễu (theo đề), luôn kèm CI và số câu.

## Nhược điểm 2 (tiêu đề Điều vỡ do crawl)
- Đo trên vbpl.vn: 0,28% (212 văn bản ứng viên) / 0,51% (80 văn bản chọn) trước chuẩn hoá, 0% sau. Báo cáo viết thẳng:
  nhược điểm này **phụ thuộc nguồn crawl**, không phải thuộc tính của phương pháp — đặt cạnh số liệu công bố của nhóm
  DSC 2026 (62,3%), kèm cách đo của hai bên. Thêm thí nghiệm: chạy B trên text thô (chưa chuẩn hoá) của các văn bản
  có tiêu đề vỡ để đo chuẩn hoá cứu được bao nhiêu.

## Rò rỉ
- Nếu một phương pháp thắng áp đảo ở một nhóm: kiểm tra trên tập trung lập (gold không theo ranh giới cấu trúc), theo
  tam phân vị độ trùng từ câu hỏi–gold, theo cờ "câu hỏi nhắc số Điều/số hiệu", và so với BM25.
