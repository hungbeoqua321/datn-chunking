# Quét "bản cũ gây nhiễu" trong bộ câu hỏi đánh giá

Báo cáo phương pháp, kết quả và **giới hạn** của bước rà soát nhiễu phiên bản văn bản
trong bộ câu hỏi (`eval/questions.draft.jsonl`, 181 câu). Chạy 2026-10-15.

> Đây là **bước chẩn đoán trước pilot**, không phải kết quả truy hồi. Con số truy hồi
> thật (mỗi phương pháp lấy trúng bản cũ bao nhiêu lần) chỉ có sau khi chạy pilot.

---

## 1. Vấn đề

Kho văn bản chứa **cả bản cũ lẫn bản mới** của cùng một quy định, ở hai dạng:

| Dạng | Cặp | Trong `cap_tuong_duong.csv`? |
|---|---|---|
| Luật bị thay thế | 15/1999↔100/2015 (BLHS), 10/2012↔45/2019 (BLLĐ), 42-LCT↔95/2015 (BLHH) | **Không** |
| Văn bản hợp nhất | gốc ↔ VBHN (5 họ: 03/2020, 19/2021, 48/2024, 170/2025, 72/2010) | Có |

Khi gold nằm ở **bản mới** mà kho vẫn còn **bản cũ nội dung gần giống**, hệ thống có thể
truy hồi trúng bản cũ. Việc trúng bản nào phụ thuộc **thứ tự chunk**, không phụ thuộc
**cách phân đoạn** — tức là nhiễu nằm **trong chính độ đo**, không phải lỗi của phương pháp
phân đoạn nào. Vì vậy: **giữ kho nguyên**, chỉ gắn cờ và **báo cáo tách**.

## 2. Phương pháp

### 2.1 Lượt 1 — trùng từ vựng (3-gram), đã loại
Với mỗi đơn vị gold, tính độ chứa `|G ∩ U| / |G|` giữa tập 3-gram từ của gold (`G`) và của
đơn vị khớp nhất trong văn bản cũ (`U`). Ngưỡng 0,9 = GIỐNG; 0,6–0,9 = KHÁC ÍT.

**Chỉ bắt được 3/7 câu** người duyệt đã chỉ ra. 4 câu còn lại cùng **chủ đề** nhưng đã viết
lại bằng chữ khác (q007 chứa 0,13; q060 0,16/0,28; q097 0,30/0,54; q206 0,46) → độ đo
từ vựng mù với diễn đạt lại. **Bỏ cách này.**

### 2.2 Lượt 2 — tương đồng embedding (đang dùng)
Dùng chính mô hình nhúng của hệ thống (`halong_embedding`, mean-pooling, chuẩn hoá L2,
cosine = tích vô hướng). Với mỗi câu hỏi `q`:

```
sim_moi = cos( q , đoạn gold ở BẢN MỚI )
sim_cu  = max  cos( q , u )   với u chạy khắp khoản/điều của VĂN BẢN CŨ tương ứng
margin  = sim_moi − sim_cu
```

`margin < 0` ⇒ **có đơn vị bản cũ gần câu hỏi hơn cả gold** ⇒ truy hồi có thể lấy nhầm.
Gold nhiều đơn vị (xuyen_khoan, dan_chieu) lấy **margin nhỏ nhất** (bảo thủ).

Tập con = `margin < 0,05` **∪** 7 câu người duyệt chỉ định. Kết quả: **21/25 câu ứng viên**.

### 2.3 Tách làm hai tập con — không gộp
| Tập con | Số câu | Ý nghĩa |
|---|---|---|
| `phien_ban_co_y` | 10 | Họ VBHN, **có trong bảng tương đương** → margin âm là **đề bài**, không phải lỗi |
| `ban_cu_nhieu` | 11 | Luật bị thay thế, **ngoài bảng tương đương** → nhiễu thật |

Hai tập **báo cáo riêng**, không cộng dồn — vì bản chất khác nhau hoàn toàn.

## 3. Kết quả

### 3.1 `ban_cu_nhieu` — nhiễu thật (11 câu)

| qid | nhóm | margin | cặp bản mới ↔ bản cũ |
|---|---|---:|---|
| q100 | dan_chieu | **−0,293** | 95/2015 Đ284 ↔ 42-LCT Đ179 |
| q069 | xuyen_khoan | **−0,184** | 45/2019 Đ107k2 ↔ 10/2012 Đ107 |
| q060 | xuyen_khoan | **−0,136** | 45/2019 Đ185k5 ↔ 10/2012 Đ199 |
| q058 | xuyen_khoan | −0,093 | 100/2015 Đ313k5 ↔ 15/1999 Đ240k1 |
| q097 | dan_chieu | −0,078 | 95/2015 Đ162 ↔ 42-LCT Đ61 |
| q206 | don_gian | −0,031 | 45/2019 Đ75k1 ↔ 10/2012 Đ73k1 |
| q016 | don_gian | −0,014 | 100/2015 Đ19k2 ↔ 15/1999 Đ314k2 |
| q041 | don_gian | −0,011 | 100/2015 Đ361k1 ↔ 15/1999 Đ287k1 |
| q064 | xuyen_khoan | +0,003 | 100/2015 Đ260k5 ↔ 15/1999 Đ202k1 |
| q005 | don_gian | +0,005 | 45/2019 Đ46k1 ↔ 10/2012 Đ48k1 |
| q007 | don_gian | +0,106 | 95/2015 Đ174k4 ↔ 42-LCT Đ94 |

7 câu người duyệt chỉ định: q005, q007, q016, q060, q069, q097, q206.
Embedding **xác nhận 6/7** (margin ≤ +0,005). Riêng **q007 (+0,106)** độ đo **không**
đồng ý — giữ trong tập con theo quyết định của người duyệt, và ghi rõ chỗ bất đồng này.

**Quét phát hiện thêm 4 câu ngoài danh sách ban đầu:** q041, q058, q064, q100 —
trong đó q100 là ca nặng nhất toàn bộ (−0,293).

### 3.2 `phien_ban_co_y` — họ VBHN (10 câu)

q045 (−0,106), q049 (−0,133), q053 (−0,093), q051 (−0,089), q047 (−0,067),
q055 (−0,063), q046 (−0,049), q054 (−0,018), q048 (−0,012), q052 (+0,026).

Margin âm dày đặc ở họ 170/2025↔10/2026-VBHN là **dự kiến**: VBHN giữ nguyên số
Điều/khoản và phần lớn nguyên văn của văn bản gốc.

### 3.3 Dữ liệu
- `eval/quet_ban_cu_embedding.json` — margin từng câu.
- Mỗi câu trong tập con mang `tap_con` + `ban_cu_chi_tiet` (cặp, margin, sim_moi, sim_cu).

---

## 4. Nhược điểm của phương pháp

Liệt kê đầy đủ để người đọc báo cáo tự đánh giá độ tin cậy.

**4.1 Đo trên ĐƠN VỊ, không phải trên CHUNK.** Truy hồi thật so câu hỏi với *chunk*; quét
này so với *khoản/điều*. Mỗi phương pháp A/C/D/B cắt chunk khác nhau nên mức cạnh tranh
thật khác nhau. Đây là **xấp xỉ không phụ thuộc phương pháp** — ưu điểm (công bằng giữa
các phương pháp) đồng thời là nhược điểm (không phải con số thật của bất kỳ phương pháp nào).

**4.2 Chỉ so với MỘT văn bản cũ ghép cặp.** Không quét toàn kho. Một đơn vị gây nhiễu nằm
ở văn bản thứ ba, không cùng họ phiên bản, sẽ **không bị phát hiện**.

**4.3 Ngưỡng 0,05 là tuỳ chọn.** Không hiệu chuẩn từ dữ liệu. Các câu quanh ngưỡng
(q064 +0,003, q005 +0,005, q052 +0,026) vào/ra tập con chỉ vì vài phần nghìn.

**4.4 Độ mịn đơn vị bỏ sót `điểm`.** Chỉ duyệt `khoan` và `dieu` ở phía bản cũ. Một *điểm*
gần giống nằm trong khoản dài có thể bị pha loãng và không nổi lên.

**4.5 Cắt 512 token.** Mô hình nhúng có `max_seq_length = 512`; điều dài bị cắt đuôi khi
nhúng, nên `sim_cu` của các điều dài tính trên phần đầu — có thể **thấp giả tạo**.

**4.6 Gold trung lập là mảnh câu.** Với câu trung lập, gold là một span cắt giữa khoản;
nhúng một mảnh không tương đương nhúng một chunk trọn. `sim_moi` của nhóm này kém ổn định.

**4.7 Gộp nhiều đơn vị gold bằng `min`.** Chọn margin nhỏ nhất là bảo thủ (dễ gắn cờ),
nhưng làm mất thông tin: không phân biệt "một đơn vị rất rủi ro" với "mọi đơn vị hơi rủi ro".

**4.8 Độ đo bất đồng với người duyệt ít nhất 1 ca.** q007 margin +0,106 nhưng người duyệt
vẫn xếp là không an toàn. Nên coi quét này là **bộ lọc gợi ý**, không phải nhãn đúng/sai.

**4.9 Dự đoán rủi ro, không đo rủi ro.** Margin nói "bản cũ cạnh tranh", không nói
"thực tế đã lấy nhầm". Con số thật phải lấy từ pilot: với mỗi phương pháp, đếm số lần
chunk trả về thuộc văn bản cũ thay vì bản mới, **báo cáo riêng cho hai tập con**.

**4.10 Ranh giới hai tập con dựa vào bảng cặp liệt kê tay.** `cap_tuong_duong.csv` do người
lập; một họ phiên bản bị bỏ sót sẽ bị xếp nhầm sang `ban_cu_nhieu`.

---

## 5. Việc chưa làm

- **Chưa chạy pilot.** Đây là điểm dừng theo quy trình.
- Khi chạy đánh giá: mỗi phương pháp báo cáo **hai dòng riêng** — số lần truy hồi trúng
  bản cũ ở `ban_cu_nhieu` và ở `phien_ban_co_y`. Con số đi vào báo cáo **như một kết quả**,
  không dùng để loại câu hỏi.
