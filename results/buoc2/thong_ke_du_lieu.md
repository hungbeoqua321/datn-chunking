# Thống kê tập dữ liệu (bước 2)

Nguồn: vbpl.vn (CSDL quốc gia về pháp luật). Tập chọn: `data/manifest.csv` — **80 văn bản**, 1.540.178 từ (sau chuẩn hoá, đã bỏ Căn cứ/Nơi nhận/chữ ký/Phụ lục).

## Theo nhóm

| Nhóm | Số VB | Tổng từ | Trung vị từ/VB | Số Điều | VB có Chương | VB có Điều > 1500 từ |
|---|---|---|---|---|---|---|
| Luật, Bộ luật | 20 | 953.732 | 37.645 | 4.623 | 20 | 8 |
| Nghị định, Thông tư | 35 | 400.354 | 7.754 | 1.013 | 29 | 10 |
| Không có "Điều" | 10 | 12.731 | 910 | 0 | 0 | 0 |
| Sửa đổi, bổ sung | 10 | 88.795 | 6.019 | 124 | 0 | 0 |
| Văn bản hợp nhất | 5 | 84.566 | 10.999 | 167 | 5 | 3 |
| **Tổng** | **80** | **1.540.178** | 9.502 | 5.927 | 54 | 21 |

Nhãn phụ: **Điều dài** = có ít nhất một Điều > 1500 từ (không tính văn bản sửa đổi, vì Điều 1 của chúng dài do trích nguyên văn điều bị sửa); **họ phiên bản** = VBHN + văn bản gốc + văn bản sửa đổi được hợp nhất.

## Theo loại văn bản

| Loại | Số VB |
|---|---|
| Thông tư | 21 |
| Nghị định | 18 |
| Luật | 15 |
| Bộ luật | 9 |
| Văn bản hợp nhất | 5 |
| Chỉ thị | 4 |
| Công văn | 4 |
| Thông báo | 2 |
| Quyết định | 2 |

## Họ phiên bản (5)

| VBHN | Văn bản gốc | Văn bản sửa đổi |
|---|---|---|
| 83/2026/VBHN-TT-BXD | 03/2020/TT-BXD | 09/2025/TT-BXD |
| 10/2026/VBHN-NĐ-BNV | 170/2025/NĐ-CP | 300/2026/NĐ-CP |
| 21/VBHN-BTC | 19/2021/TT-BTC | 46/2024/TT-BTC, 40/2025/TT-BTC |
| 114/VBHN-VPQH | 48/2024/QH15 | 90/2025/QH15, 149/2025/QH15, 09/2026/QH16 |
| 56/VBHN-BCT | 72/2010/QĐ-TTg | 230/2026/NĐ-CP, 12/2019/QĐ-TTg |

## Tiêu đề Điều bị vỡ — trước và sau chuẩn hoá

- **Kỳ vọng**: số Điều theo cây cấu trúc do vbpl.vn biên tập (nguồn độc lập với bộ phân đoạn B); văn bản không có cây thì lấy dãy số Điều liên tục 1, 2, … bằng regex lỏng.
- **Bắt được**: dòng khớp đúng regex tiêu đề của phương pháp B `^Điều\s+(\d+)\s*[.．:]?\s*(.*)$`, không nằm trong khối trích dẫn.
- **Trước chuẩn hoá** = text crawl kiểu thông thường `get_text("\n")` (mỗi thẻ HTML một dòng); **sau** = text đã chuẩn hoá (`crawl/chuan_hoa.py`).

| Nhóm | VB có Điều | Điều kỳ vọng | Vỡ trước | Tỷ lệ trước | Vỡ sau | Tỷ lệ sau | VB còn vỡ |
|---|---|---|---|---|---|---|---|
| Luật, Bộ luật | 20 | 4581 | 0 | 0.00% | 0 | 0.00% | 0 |
| Nghị định, Thông tư | 35 | 1013 | 30 | 2.96% | 0 | 0.00% | 0 |
| Sửa đổi, bổ sung | 10 | 124 | 0 | 0.00% | 0 | 0.00% | 0 |
| Văn bản hợp nhất | 5 | 132 | 0 | 0.00% | 0 | 0.00% | 0 |
| **Tổng** | **70** | **5850** | **30** | **0.51%** | **0** | **0.00%** | 0 |

Nguồn số Điều kỳ vọng: cay_vbpl = 69 VB, regex_long = 1 VB.

Ví dụ tiêu đề vỡ trong text thô (dòng ⏎ là chỗ bị xuống dòng):

- 364/2026/NĐ-CP — Điều 5: `Điều ⏎ 5. ⏎ Tập sự hành nghề luật sư để trở thành luật sư công`
- 10/2026/TT-BTP — Điều 1: `Điều ⏎ 1. ⏎ Phạm`
- 65/2026/TT-BXD — Điều 4: `Điều ⏎ 4. ⏎ Quy định chuyển tiếp`
- 48/2026/TT-BCT — Điều 11: `Điều ⏎ 11. Hồ sơ, quy trình phân giao hạn ngạch thuế quan nhập khẩu theo phương thức xét duyệt hồ sơ ⏎ 1. Hồ sơ đề nghị phân giao hạn ngạch thuế quan nhập khẩu theo phương thức xét duyệt hồ sơ quy địn`

Trên **toàn bộ 212 văn bản ứng viên đã tải** (không chỉ tập chọn): 10892 Điều kỳ vọng; vỡ trước **30 (0.28%)** ở 4 VB, sau **0 (0.00%)**. Các văn bản gốc có tiêu đề vỡ được đưa hết vào tập chọn (nhãn `tieu_de_vo`).

## "Điều" nằm trong khối trích dẫn (văn bản sửa đổi)

Văn bản sửa đổi trích nguyên văn điều mới của luật bị sửa trong ngoặc kép, ví dụ `"Điều 4. … "`. Regex của B coi các dòng này là tiêu đề Điều thật → sinh **Điều giả**.

- 1/10 văn bản sửa đổi có dòng "Điều N" trong khối trích dẫn; tổng **1** dòng (so với 124 Điều thật của chính các văn bản này).
- Dòng mở đầu bằng dấu nháy `"Điều N …` (điều của văn bản bị sửa được trích nguyên văn): **100** dòng ở 7/10 VB. Regex của B không khớp các dòng này (vì có dấu nháy đứng trước) nên chúng không thành Điều giả, nhưng nội dung điều được trích nằm lẫn trong Điều của văn bản sửa đổi — dữ liệu cho nhược điểm 5 (nhiều phiên bản).

## Phần đã bỏ khi chuẩn hoá (data/clean/ so với data/clean_full/)

- Dòng "Căn cứ …/Theo đề nghị …" ở đầu: 246 dòng (68 VB)
- Nơi nhận: 605 dòng; khối chữ ký: 252 dòng (73 VB)
- Khối Nơi nhận/chữ ký nằm GIỮA văn bản (quyết định ban hành kèm quy chế, khối xác thực VBHN): 1 khối
- Trong đó Phụ lục (mẫu đơn, bảng biểu sau chữ ký): 82.990 từ (16 VB) — không thuộc phạm vi thực nghiệm
- Văn bản không có Phần/Chương/Điều (công văn, chỉ thị…): KHÔNG bỏ dòng "Căn cứ" vì ở đây nó là nội dung.
