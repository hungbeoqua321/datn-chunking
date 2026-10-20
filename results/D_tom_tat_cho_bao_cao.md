# Phương pháp D — phân đoạn theo ngữ nghĩa

*(Bản rút gọn để đưa vào chương 3. Chi tiết kỹ thuật đầy đủ xem `results/phuong_phap_D_semantic_chunking.md`.)*

## Nguồn

D lấy từ lớp `SemanticChunker` của thư viện LangChain, dựa trên notebook "5 Levels of Text Splitting"
của Greg Kamradt — **mã thư viện và tài liệu hướng dẫn, không phải công trình đã bình duyệt**. Các hạn
chế nêu dưới đây là những gì quan sát được khi áp nó lên văn bản quy phạm pháp luật tiếng Việt.

## Cách làm

Tách văn bản thành từng câu, rồi tính **độ giống nhau giữa mỗi câu và câu liền sau**. Chỗ nào độ
giống **tụt mạnh** thì coi là ý đã chuyển và đặt ranh giới. "Tụt mạnh" không lấy số cứng mà lấy mốc
**theo phân vị 95 tính riêng trong từng văn bản** — khoảng 5% chỗ tụt sâu nhất thành ranh giới.

Để so sánh được với ba phương pháp kia trên cùng ngân sách từ, đồ án thêm ràng buộc **50–350 từ**:
đoạn dài quá thì cắt tiếp ở chỗ tụt sâu nhất bên trong, đoạn ngắn quá thì gộp sang đoạn bên cạnh gần
nghĩa hơn. Văn bản dưới 20 câu thì phân vị mất ý nghĩa nên chuyển sang cách gom của C.

## Kết quả thực nghiệm

Đo trên 80 văn bản:

| Phương pháp | Số chunk | Trung vị từ | Dài nhất | Ngắn nhất | Ký tự bị mất |
|---|---:|---:|---:|---:|---:|
| A — kích thước cố định | 5.172 | 300 | 300 | 6 | 0 |
| C — dấu câu | 5.640 | 281 | 300 | 10 | 0 |
| **D — ngữ nghĩa** | **7.673** | **199** | **385** | **25** | **0** |
| B — cấu trúc pháp lý | 12.718 | 97 | 372 | 3 | 0 |

D chạy trót lọt trên toàn kho, **không mất ký tự nào**, gần như không chunk nào vượt giới hạn đọc của
mô hình nhúng (7 trên 7.673). Về độ mịn, D nằm giữa A/C và B.

Hai chỗ nới ràng buộc, đều được đếm: 205 chunk (2,7%) nằm trong dải 350–385 từ do được phép nhỉnh
hơn trần để hấp thụ đoạn quá ngắn (nhờ vậy chỉ còn 5 chunk dưới sàn 50 từ), và 8 chunk sinh từ 6 văn
bản quá ngắn phải chuyển sang cách gom của C. Trần thiết kế của D vì thế là **385 từ**, không phải 350.

Cần nói rõ để tránh hiểu nhầm có lợi cho kết luận: **baseline D đang được nới trần rộng hơn chính
phương pháp đề xuất B** — 385 từ so với 372, và 2,7% số chunk vượt trần so với 0,13%.

## Ba nhóm hạn chế

**Thứ nhất, ngưỡng phân vị đo độ dài chứ không đo nội dung.** Lấy mốc theo phân vị 95 nghĩa là văn
bản nào cũng có khoảng 5% số chỗ nối câu thành ranh giới, bất kể có thật sự chuyển ý hay không. Văn
bản đồng nhất vẫn bị cắt đúng chừng ấy chỗ; văn bản nhiều chủ đề lại bị cắt thiếu. Hệ quả là số chunk
gần như chỉ phụ thuộc độ dài văn bản chứ không phụ thuộc nội dung. Đây là khiếm khuyết của chính cách
đặt ngưỡng, không phải lỗi cài đặt, nên không sửa được nếu vẫn giữ D làm mốc so sánh.

**Thứ hai, D không bám được cấu trúc điều khoản.** Ranh giới do D đặt ra hoàn toàn dựa vào nội dung
câu chữ, nên có thể rơi vào giữa một khoản và tách phần quy tắc khỏi phần ngoại lệ của chính quy tắc
đó. Với văn bản pháp luật, đây là kiểu cắt sai nguy hiểm nhất: hệ thống lấy về phần quy tắc, trả lời
nghe có lý, nhưng thiếu mất ngoại lệ. Thêm nữa, đơn vị "câu" mà D dựa vào không trùng với đơn vị câu
của văn bản luật — một khoản gồm nhiều điểm thường bị nhận nhầm thành một câu rất dài — nên ngay từ
bước đầu tiên D đã làm việc trên đơn vị không đúng với văn bản.

**Thứ ba, chi phí cao và phụ thuộc mô hình nhúng.** Khác ba phương pháp kia vốn chỉ đọc văn bản một
lượt, D phải tính vector cho từng câu của toàn kho trước khi cắt được chunk đầu tiên — khoảng ba giờ
máy trên 80 văn bản. Quan trọng hơn, ranh giới của D là hàm của mô hình nhúng: đổi mô hình là ra bộ
chunk khác, trong khi A, B, C cho kết quả giống hệt ở mọi lần chạy. Kết quả của D vì thế khó tái lập
hơn hẳn — một chi phí phải ghi nhận khi so sánh, không chỉ là chi tiết kỹ thuật.

## Những chỗ đã sửa trước khi chạy đánh giá

Ba lỗi cài đặt đã sửa trước khi lấy số: nhúng theo cụm ba câu đúng bản gốc thay vì từng câu rời; cắt
những "câu" dài quá trần bằng cửa sổ cố định; và chuyển văn bản dưới 20 câu sang cách gom của C.
