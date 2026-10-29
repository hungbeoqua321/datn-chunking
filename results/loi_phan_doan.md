
---

## Gold trung lập cho nhóm xuyên khoản: khó dựng vì chính cấu trúc văn bản luật

Nhóm `xuyen_khoan` cần gold **trung lập** — span cố ý KHÔNG trùng ranh giới cấu trúc, cắt từ giữa
khoản quy tắc rồi vắt sang khoản ngoại lệ. Khi dựng bù ba câu thay cho ba câu bị loại, nguồn ứng
viên cạn rất nhanh, và lý do nằm ở đặc điểm của văn bản quy phạm pháp luật chứ không ở bộ lọc.

### Số liệu lọc

Xuất phát từ 100 cặp khoản quy tắc–ngoại lệ **có dẫn chiếu tường minh** đã quét được
(`eval/cap_xuyen_khoan_ung_vien.json`, khoản ngoại lệ trỏ đích danh khoản quy tắc):

| Bước lọc | Còn lại |
|---|---:|
| Cặp có dẫn chiếu tường minh | **100** |
| Hai khoản **liền kề** (điều kiện để một span vắt qua được) | **72** |
| Bỏ văn bản thuộc **họ phiên bản** (tránh nhiễu bản cũ/bản mới) | **54** |
| Điều đó **chưa dùng** làm gold ở câu khác | **51** |
| Trần **2 câu GIỮ/văn bản** + khoản quy tắc **≥ 2 câu** | **4** |

Từ 4 ứng viên cuối: 1 bị giám khảo loại, **3 không có chỗ đặt span**. Kết quả chỉ dựng được **2/3**
câu bù, phải hạ chỉ tiêu gold trung lập của nhóm từ 6 xuống 5.

### Hai nguyên nhân, đều thuộc về cấu trúc văn bản

**1. Khoản quy tắc thường chỉ có MỘT câu.** Ở vòng lọc áp dụng đầu tiên, **18/22** ứng viên rụng vì
lý do này. Khoản luật điển hình là một câu dài duy nhất đã gói sẵn cả quy tắc lẫn mệnh đề loại trừ
("… trừ trường hợp quy định tại khoản N Điều này"). Muốn span bắt đầu ở *giữa* khoản mà vẫn là câu
trọn vẹn thì phải có câu thứ hai — thứ phần lớn khoản không có.

**2. Khoản dạng danh sách điểm không có chỗ đặt span.** Ba ứng viên cuối cùng đều rụng ở đây. Ví dụ
34/2024/QH15 Điều 62 khoản 1 và 135/2025/QH15 Điều 48 khoản 1: mọi "câu" sau câu đầu đều là
`a)`, `b)`, `c)`… — vừa **là đầu một đơn vị cấu trúc**, vừa mở đầu bằng **chữ thường**. Đặt điểm bắt
đầu span ở bất kỳ chỗ nào trong số đó đều trùng ranh giới cấu trúc, tức mất đúng tính trung lập cần có.

### Vì sao ghi lại

Đây là một **giới hạn của thiết kế đánh giá** chứ không phải lỗi cài đặt: với VBQPPL, "cắt giữa một
đơn vị pháp lý mà vẫn giữ câu trọn vẹn" là việc thường xuyên **không làm được**. Nó cũng là một quan
sát độc lập cho phương pháp B — nếu chính người ra đề còn khó tìm chỗ cắt không trùng ranh giới
khoản, thì ranh giới khoản đúng là đường cắt tự nhiên của loại văn bản này.
