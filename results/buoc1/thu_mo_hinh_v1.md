# Thử mô hình sinh `Qwen3-4B-Instruct-2507-Q4_0` (không phải dữ liệu thực nghiệm)

| # | Điều gold | Token vào | Token ra | Giây | Trích đúng Điều gold | Đúng dạng | Từ chối đúng |
|---|---|---|---|---|---|---|---|
| 1 | 25 | 740 | 54 | 32 | ✗ | ✗ |  |
| 2 | 113 | 1122 | 43 | 46 | ✓ | ✓ |  |
| 3 | 105 | 1046 | 50 | 45 | ✗ | ✗ |  |
| 4 | 107 | 1197 | 41 | 48 | ✗ | ✗ |  |
| 5 | 139 | 895 | 64 | 39 | ✗ | ✗ |  |
| 6 | 20 | 1402 | 81 | 65 | ✗ | ✗ |  |
| 7 | 35 | 1680 | 314 | 126 | ✗ | ✗ |  |
| 8 | 46 | 1249 | 63 | 55 | ✗ | ✗ |  |
| 9 | 91 | 863 | 48 | 36 | ✓ | ✓ |  |
| 10 | 169 | 999 | 138 | 56 | ✗ | ✗ |  |
| 11 | — | 655 | 13 | 23 |  | ✗ | ✓ |
| 12 | — | 653 | 13 | 23 |  | ✗ | ✓ |

- Trích đúng Điều gold: **2/10**; đúng dạng "Điều X (khoản Y) của 45/2019/QH14": **2/10**; từ chối đúng khi thiếu căn cứ: **2/2**
- Thời gian trung bình: **49 giây/câu**

## Câu trả lời

**Thời gian thử việc tối đa đối với công việc của người quản lý doanh nghiệp là bao lâu?** (gold: Điều 25)

> Thời gian thử việc tối đa đối với công việc của người quản lý doanh nghiệp là 180 ngày, căn cứ theo Điều 25 khoản 1 của Nghị định 45/2019/QH14.

**Người lao động làm việc đủ 12 tháng cho một người sử dụng lao động được nghỉ hằng năm bao nhiêu ngày trong điều kiện bình thường?** (gold: Điều 113)

> 12 ngày làm việc đối với người làm công việc trong điều kiện bình thường (Điều 113 khoản 1 a của 45/2019/QH14).

**Thời giờ làm việc bình thường của người lao động tối đa là bao nhiêu giờ trong một ngày?** (gold: Điều 105)

> Thời giờ làm việc bình thường của người lao động không quá 08 giờ trong 01 ngày theo Điều 105 khoản 1 của Nghị định 45/2019/QH14.

**Số giờ làm thêm của người lao động không được vượt quá bao nhiêu giờ trong một tháng?** (gold: Điều 107)

> Không quá 40 giờ trong 01 tháng.  
> Căn cứ: Điều 107 khoản 2 của QH14 số 45/2019.

**Lao động nữ được nghỉ thai sản trước và sau khi sinh con bao lâu?** (gold: Điều 139)

> Lao động nữ được nghỉ thai sản trước và sau khi sinh con là 06 tháng; thời gian nghỉ trước khi sinh không quá 02 tháng.  
> Căn cứ: Điều 139 khoản 1 của Nghị định 45/2019/QH14.

**Hợp đồng lao động phải được giao kết theo những loại nào?** (gold: Điều 20)

> Hợp đồng lao động phải được giao kết theo một trong các loại sau đây:  
> a) Hợp đồng lao động không xác định thời hạn;  
> b) Hợp đồng lao động xác định thời hạn.  
> 
> Căn cứ: Điều 20 khoản 1 của Nghị định 45/2019/QH14.

**Người lao động có quyền đơn phương chấm dứt hợp đồng lao động không cần báo trước trong những trường hợp nào?** (gold: Điều 35)

> Người lao động có quyền đơn phương chấm dứt hợp đồng lao động không cần báo trước trong các trường hợp sau:
> 
> a) Không được bố trí theo đúng công việc, địa điểm làm việc hoặc không được bảo đảm điều kiện làm việc theo thỏa thuận, trừ trường hợp quy định tại Điều 29 của Bộ luật này;  
> b) Không được trả đủ lương hoặc trả lương không đúng thời hạn, trừ trường hợp quy định tại khoản 4 Điều 97 của Bộ luật này;  
> c) Bị người sử dụng lao động ngược đãi, đánh đập hoặc có lời nói, hành vi nhục mạ, hành vi làm ảnh hưởng đến sức khỏe, nhân phẩm, danh dự; bị cưỡng bức lao động;  
> d) Bị quấy rối tình dục tại nơi làm việc;  
> đ) Lao động nữ mang thai phải nghỉ việc theo quy định tại khoản 1 Điều 138 của Bộ luật này;  
> e) Đủ tuổi nghỉ hưu theo quy định tại Điều 169 của Bộ luật này, trừ trường hợp các bên có thỏa thuận khác;  
> g) Người sử dụng lao động cung cấp thông tin không trung thực theo quy định tại khoản 1 Điều 16 của Bộ luật này làm ảnh hưởng đến việc thực hiện hợp đồng lao động.  
> 
> Căn cứ: Điều 35 khoản 2 của QH14 số 45/2019.

**Người sử dụng lao động có trách nhiệm chi trả trợ cấp thôi việc cho người lao động đã làm việc thường xuyên từ bao lâu trở lên?** (gold: Điều 46)

> Người sử dụng lao động có trách nhiệm chi trả trợ cấp thôi việc cho người lao động đã làm việc thường xuyên từ đủ 12 tháng trở lên.  
> Căn cứ: Điều 46 khoản 1 của QH14 số 45/2019.

**Mức lương tối thiểu được xác lập theo đâu?** (gold: Điều 91)

> Mức lương tối thiểu được xác lập theo vùng, ấn định theo tháng, giờ.  
> Căn cứ: Điều 91 khoản 2 của 45/2019/QH14.

**Tuổi nghỉ hưu của người lao động trong điều kiện lao động bình thường được điều chỉnh theo lộ trình như thế nào?** (gold: Điều 169)

> Tuổi nghỉ hưu của người lao động trong điều kiện lao động bình thường được điều chỉnh theo lộ trình như sau:  
> - Kể từ năm 2021, tuổi nghỉ hưu là đủ 60 tuổi 03 tháng đối với lao động nam và đủ 55 tuổi 04 tháng đối với lao động nữ;  
> - Sau đó, cứ mỗi năm tăng thêm 03 tháng đối với lao động nam và 04 tháng đối với lao động nữ.  
> 
> Căn cứ: Điều 169 khoản 2 của QH14 số 45/2019.

**Thuế suất thuế giá trị gia tăng đối với hàng xuất khẩu là bao nhiêu?** (gold: Điều None)

> Không đủ căn cứ trong ngữ cảnh được cung cấp.

**Mức phạt khi vượt đèn đỏ đối với xe máy là bao nhiêu?** (gold: Điều None)

> Không đủ căn cứ trong ngữ cảnh được cung cấp.
