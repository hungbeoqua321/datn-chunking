# Phương pháp D — Semantic Chunking: nguồn, công thức, thử nghiệm, nhược điểm, cách khắc phục

Báo cáo về baseline thứ ba của đề cương: phân đoạn theo ngữ nghĩa. Code: `chunking/semantic.py`.

> **CẬP NHẬT 16/10/2026 — đã sửa ba lỗi cài đặt và chạy lại.** Mọi số trong mục 3 là số SAU khi sửa.
> Các mục 4.2, 4.3, 4.4, 4.9 nay ghi rõ trạng thái *ĐÃ SỬA* kèm số trước/sau.
Số liệu đo trên **80 văn bản** (`data/manifest.csv`), seed 0.

---

## 1. Dùng phương pháp nào, của ai

**Tên:** Semantic Chunking — biến thể **ngưỡng phân vị** (percentile breakpoint).

**Nguồn:** lớp `SemanticChunker` của **LangChain** (`langchain_experimental.text_splitter`).
Tài liệu LangChain ghi rõ lớp này lấy từ notebook của **Greg Kamradt**
(Level 4 — Semantic Chunking). Tham số mặc định `breakpoint_threshold_type="percentile"`,
`breakpoint_threshold_amount=95`. Các kiểu ngưỡng khác mà thư viện có:
`standard_deviation`, `interquartile`, `gradient`.

### 📎 Repo / mã nguồn đã tham khảo — bấm vào để mở

| Nguồn | Đường dẫn |
|---|---|
| **Repo gốc của phương pháp** (Greg Kamradt) | [github.com/FullStackRetrieval-com/RetrievalTutorials](https://github.com/FullStackRetrieval-com/RetrievalTutorials) |
| **Notebook đúng chỗ mô tả Level 4** | [5_Levels_Of_Text_Splitting.ipynb](https://github.com/FullStackRetrieval-com/RetrievalTutorials/blob/main/tutorials/LevelsOfTextSplitting/5_Levels_Of_Text_Splitting.ipynb) |
| **Mã nguồn `SemanticChunker`** (bảng `BREAKPOINT_DEFAULTS`, hàm percentile) | [langchain-experimental/.../text_splitter.py](https://github.com/langchain-ai/langchain-experimental/blob/main/libs/experimental/langchain_experimental/text_splitter.py) |
| **Tài liệu API `SemanticChunker`** | [python.langchain.com — API reference](https://python.langchain.com/api_reference/experimental/text_splitter/langchain_experimental.text_splitter.SemanticChunker.html) |

*(Mọi đường dẫn trên đã kiểm HTTP 200 ngày 16/10/2026.)*

> **Tính chất nguồn:** đây là **mã thư viện + notebook hướng dẫn**, KHÔNG phải công trình
> bình duyệt. Mọi nhận xét dưới đây phải đóng khung là *"hạn chế quan sát được khi áp lên
> VBQPPL tiếng Việt"*, không được viết thành "phản biện công trình đã công bố".

## 2. Công thức

Cho văn bản tách thành dãy câu `s₁…sₙ` (bộ tách của phương pháp C).

**(1) Nhúng câu.** `vᵢ = E(sᵢ)`, với `E` = `halong_embedding`, vector đã chuẩn hoá L2 (‖vᵢ‖ = 1).

**(2) Khoảng cách hai câu liền nhau** (cosine = tích vô hướng vì đã chuẩn hoá):

```
dᵢ = 1 − vᵢ · vᵢ₊₁        i = 1 … n−1
```

**(3) Ngưỡng theo phân vị — tính RIÊNG trong từng văn bản:**

```
τ = percentile₉₅( { d₁ , … , dₙ₋₁ } )
```

**(4) Ranh giới:** đặt ranh giới sau câu `i` với mọi `i` thoả `dᵢ > τ`.
Đoạn = khoảng giữa hai ranh giới liên tiếp.

**(5) Ràng buộc kích thước — phần LUẬN VĂN TỰ THÊM, không có trong bản gốc**
(để so sánh công bằng với A/B/C, vốn bị chặn 50–350 từ):
- đoạn > 350 từ: cắt tiếp tại `argmax dᵢ` bên trong, đệ quy đến khi ≤ 350;
  **ngoại lệ:** đoạn chỉ gồm *một* câu thì giữ nguyên dù dài bao nhiêu;
- đoạn < 50 từ: gộp sang hàng xóm có ranh giới "gần nghĩa hơn" (`d` nhỏ hơn),
  nếu tổng ≤ **385** (= 350 cộng biên độ gộp); không gộp được thì để nguyên.
  ⇒ **trần thiết kế thực tế của D là 385 từ**, không phải 350 — xem mục 3.1.

### 2.1 Sai lệch so với bản gốc (quan trọng khi viết báo cáo)

| | LangChain `SemanticChunker` | D của luận văn |
|---|---|---|
| Đơn vị đem nhúng | **Cụm 3 câu** `sᵢ₋₁+sᵢ+sᵢ₊₁` (`buffer_size=1`) | **Cụm 3 câu** — ĐÃ SỬA (trước: từng câu rời) |
| Ràng buộc kích thước | Không (chỉ `min_chunk_size` ở bản mới) | Có, sàn 50 — trần 385 (350 + biên độ gộp) |
| Ngưỡng | percentile 95 | percentile 95 (giống) |

**ĐÃ SỬA 16/10/2026** — nay nhúng cụm 3 câu đúng bản gốc. Trước đó, nhúng **từng câu rời** làm dãy `dᵢ` **nhiễu hơn hẳn** so với bản gốc: một câu ngắn
("Điều 5.", "a) …") có vector rất lệch so với câu bên cạnh, sinh ranh giới giả.
Bản gốc gộp 3 câu chính là để làm trơn dãy khoảng cách. Giữ nguyên sai lệch này rồi kết luận D kém sẽ là **cài sai một phương pháp rồi chê chính nó** — nên đã sửa
trước khi lấy số chính thức. Chi phí nhúng tăng 3 lần (khoảng 1,1 giờ lên 3 giờ máy).

## 3. Đã thử nghiệm ra cái gì

Chạy trên 80 văn bản, so với ba phương pháp còn lại (số từ tính trên phần nội dung):

| Phương pháp | Số chunk | Trung vị từ | Max từ | Min từ | Vượt 512 token | Ký tự không phủ |
|---|---:|---:|---:|---:|---:|---:|
| A — 300 từ cố định | 5.172 | 300 | 300 | 6 | 6 (0,1%) | 0 |
| C — dấu câu | 5.640 | 281 | 300 | 10 | 5 (0,1%) | 0 |
| **D — ngữ nghĩa** | **7.673** | **199** | **385** | **25** | **7 (0,1%)** | **0** |
| B — cấu trúc | 12.718 | 97 | 372 | 3 | 44 (0,3%) | 0 |

### Thành quả
- **Chạy được trên toàn kho, không mất ký tự nào** (ký tự không phủ = 0) và **không có
  fallback** (0,0%) — tức thuật toán áp được cho mọi nhóm văn bản, kể cả văn bản không chia Điều.
- **Hầu như không vượt trần nhúng:** chỉ 5/7.718 chunk (0,1%) quá 512 token — thấp ngang A và C,
  tốt hơn B (44 chunk). Nghĩa là gần như toàn bộ nội dung chunk thực sự được mô hình đọc.
- **Nằm giữa A và B về độ mịn** (trung vị 198 từ, so với A 300 và B 97): đúng vai trò một
  baseline trung gian giữa "cắt mù theo độ dài" và "cắt theo cấu trúc".
- Ràng buộc kích thước (sàn 50, trần 385) do luận văn thêm **có tác dụng**: kéo trung vị từ phân bố tự do về
  dải so sánh được với A/C, nhờ đó bốn phương pháp đọ được trên cùng ngân sách từ.

## 3.1 Ràng buộc kích thước: ba loại vượt trần, và chiều sàn ngược lại

**Trần thiết kế của từng phương pháp** — ghi đúng con số thực tế, không ghi 350 rồi để max 385 bên cạnh:

| Phương pháp | Trần thiết kế | Dài nhất đo được | Vượt trần | Loại |
|---|---:|---:|---:|---|
| A | 300 | 300 | 0 | — |
| C | 300 | 300 | 0 | — (đã sửa) |
| B | 350 | 372 | 16 (0,13%) | ① đơn vị pháp lý thật |
| **D** | **385** | **385** | **205 (2,7%)** | ③ thiết kế cho phép |

**Ba loại vượt trần, bản chất khác hẳn nhau — không được gộp chung:**

**① Đơn vị pháp lý thật (B).** 16 chunk là một Điều trọn vẹn, vượt nhiều nhất 22 từ vì dòng tiêu đề
Chương/Mục được gắn vào đầu chunk nhưng không tính vào ngưỡng. Cắt đôi để ép trần sẽ phá chính định
nghĩa của B, nên **miễn trừ có chủ đích**, đếm và ghi chú.

**② Lỗi bộ tách câu (C, và D trước khi sửa).** Một khoản gồm nhiều điểm bị bộ tách nhận nhầm thành
một "câu" dài hơn trần, rồi để đứng nguyên. Đây **là lỗi**, không phải miễn trừ: đơn vị vượt trần
không có thật. Đã cắt bằng cửa sổ cố định — C từ 413 về 300, D từ 413 về trong trần.

**③ Thiết kế cho phép (D sau khi sửa).** 205 chunk trong dải 350–385 là **hệ quả có chủ ý** của biên
độ gộp: cho phép nhỉnh hơn trần một ít để hấp thụ các đoạn dưới sàn. Đây không phải vi phạm chính
sách mà là ràng buộc đã được định nghĩa như vậy — nên trần thực tế của D là **385**, và mọi so sánh
phải dùng con số đó.

### Chiều sàn: D bị ép, B thì không — và vì sao

| Phương pháp | Ngắn nhất | Chunk dưới 50 từ | Tỉ lệ | Có ép sàn? |
|---|---:|---:|---:|---|
| A | 6 | 16 | 0,3% | không |
| C | 10 | 6 | 0,1% | không |
| **D** | **25** | **5** | **0,1%** | **có — gộp, biên độ tới 385** |
| **B** | **3** | **2.781** | **21,9%** | **không** |

Hai cách xử lý trái ngược nhau, nhưng **cùng một lập luận: đơn vị pháp lý thật thì không đụng vào**.

- **D bị ép sàn** vì một đoạn 17 từ do D cắt ra **không phải đơn vị gì cả** — nó là mẩu vụn sinh ra
  từ chỗ ngưỡng phân vị rơi trúng, nên gộp lại là sửa một sản phẩm thừa của thuật toán.
- **B không bị ép sàn** dù có tới 2.781 chunk (21,9%) dưới 50 từ, ngắn nhất 3 từ, vì các chunk đó là
  **điểm và khoản có thật** — ví dụ Điều 151 khoản 2 điểm d và điểm đ của Bộ luật Hàng hải. Gộp chúng
  vào điểm bên cạnh sẽ tạo ra một chunk không ứng với đơn vị pháp lý nào, tức là phá đúng cái tính
  chất làm nên B.

**Hệ quả cần nói thẳng trong báo cáo:** baseline D đang được **nới trần rộng hơn chính phương pháp
đề xuất B** — 385 từ so với 372, và 2,7% số chunk vượt trần so với 0,13%. Nếu B vẫn thắng thì thắng
trong điều kiện ràng buộc chặt hơn đối thủ; nếu B thua thì không thể đổ cho ràng buộc.

## 4. Nhược điểm (kèm số đo)

**4.1 Ngưỡng phân vị đo ĐỘ DÀI chứ không đo ngữ nghĩa.**
`percentile₉₅` theo định nghĩa luôn chọn ~5% số chỗ nối làm ranh giới, **bất kể văn bản có
thật sự chuyển ý hay không**. Văn bản đồng nhất vẫn bị cắt; văn bản nhiều chủ đề lại bị cắt
thiếu. Số chunk trở thành hàm của số câu, không phải của nội dung. **Đây là khiếm khuyết lõi
của percentile**, không phải lỗi cài đặt.

**4.2 ✅ ĐÃ SỬA — nhúng từng câu rời (sai lệch ở §2.1) làm dãy khoảng cách nhiễu**, sinh ranh giới giả ở
các câu ngắn kiểu nhãn — rất nhiều trong VBQPPL.

**4.3 ✅ ĐÃ SỬA — trần thủng: max 413, nay 385.** Nguyên nhân ở code:
đoạn chỉ gồm một câu thì trả nguyên (`i1 - i0 == 1`). VBQPPL đầy câu liệt kê dài hơn 350 từ.

**4.4 ✅ ĐÃ SỬA — sàn thủng: min 17, nay 25**, chỉ còn **5 chunk** dưới sàn 50. Đổi lại, **205 chunk (2,7%) nằm trong dải 350–385** do biên độ gộp; không chunk nào vượt 385.

**4.5 Bộ tách câu không hợp văn bản luật.** Chỉ cắt ở `. ? !`; `a) b) đ)` và `;` không phải
ranh giới, nên một khoản nhiều điểm thành **một "câu" khổng lồ**, hỏng luôn bước (1)–(4).

**4.6 Chi phí bất đối xứng.** Phải nhúng **mọi câu của toàn kho** trước khi cắt
(`semantic.chuan_bi`, có chốt chặn 4 giờ). A và C gần như miễn phí. Chi phí này phải được
ghi vào bảng so sánh, nếu không thì so sánh không công bằng về mặt vận hành.

**4.7 Phụ thuộc mô hình nhúng.** Ranh giới là hàm của `halong_embedding`; đổi mô hình là ra
bộ chunk khác. **Không tái lập được giữa các mô hình** — khác hẳn A/B/C vốn tất định.

**4.8 Mù cấu trúc pháp lý.** Ranh giới có thể rơi giữa một khoản, tách quy tắc khỏi ngoại lệ
— đúng thứ mà nhóm câu hỏi `xuyen_khoan` đang đo.

**4.9 ✅ ĐÃ SỬA — văn bản ngắn thì phân vị vô nghĩa.** Nay văn bản dưới 20 câu rơi về cách gom của C (`fallback=True`): **6 văn bản**, sinh 8 chunk.

## 5. Cách khắc phục

### 5.1 Sửa được ngay, không đổi bản chất phương pháp
| Nhược điểm | Cách sửa |
|---|---|
| 4.3 trần 413 từ | Câu đơn > 350 từ thì cắt tiếp bằng cửa sổ cố định kiểu A, thay vì nhả chunk quá khổ |
| 4.4 sàn 17 từ | Cho phép gộp vượt 350 một biên độ nhỏ, hoặc ghi nhận và báo số chunk còn dưới sàn |
| 4.5 tách câu | Thêm `a) b) đ)` và `;` cấp điểm làm ranh giới câu — **sửa một chỗ, cải thiện cả C lẫn D** |
| 4.9 văn bản ngắn | Dưới N câu thì rơi về C, không tính phân vị |
| 4.2 nhiễu | Nhúng **cụm 3 câu** (`buffer_size=1`) đúng như bản gốc LangChain, để làm trơn dãy `dᵢ` |

### 5.2 Chữa đúng bệnh 4.1 — thay cái lõi
- Dùng kiểu ngưỡng khác mà thư viện đã có: `standard_deviation`, `interquartile`, `gradient`.
- Hoặc **hiệu chuẩn một ngưỡng tuyệt đối** trên tập giữ riêng rồi áp chung toàn kho. Khi đó
  số chunk phản ánh **nội dung**, không phản ánh **độ dài** — đúng mục tiêu của phân đoạn ngữ nghĩa.

### 5.3 Không "sửa", mà báo cáo như một kết quả
- **4.6 chi phí** và **4.7 phụ thuộc mô hình**: không khắc phục được trong khuôn khổ phương pháp;
  phải ghi thẳng vào phần so sánh như một chi phí/rủi ro của D.

### 5.4 Hướng cải tiến đề xuất (KHÔNG gọi là D)
Lai cấu trúc: chỉ cho phép ranh giới ngữ nghĩa tại những chỗ **không cắt giữa một khoản**
(ngữ nghĩa *bên trong* cấu trúc). Đây là cải tiến đề xuất cho phần kết luận — **không được
thay vào D giữa chừng**, vì sẽ làm mất baseline đang so sánh.

---

## 6. Tài liệu tham khảo

1. Greg Kamradt, *The 5 Levels of Text Splitting for Retrieval* — Level 4: Semantic Chunking.
   Repo: [FullStackRetrieval-com/RetrievalTutorials](https://github.com/FullStackRetrieval-com/RetrievalTutorials) ·
   Notebook: [tutorials/LevelsOfTextSplitting/5_Levels_Of_Text_Splitting.ipynb](https://github.com/FullStackRetrieval-com/RetrievalTutorials/blob/main/tutorials/LevelsOfTextSplitting/5_Levels_Of_Text_Splitting.ipynb)
2. LangChain, `langchain_experimental.text_splitter.SemanticChunker` —
   [tài liệu API](https://python.langchain.com/api_reference/experimental/text_splitter/langchain_experimental.text_splitter.SemanticChunker.html) ·
   [mã nguồn trên GitHub](https://github.com/langchain-ai/langchain-experimental/blob/main/libs/experimental/langchain_experimental/text_splitter.py) ·
   [mã nguồn bản v0.3 (có hàm percentile, bảng `BREAKPOINT_DEFAULTS`)](https://reference.langchain.com/v0.3/python/_modules/langchain_experimental/text_splitter.html)
3. LangChain v0.2 — [tài liệu `SemanticChunker` bản cũ](https://python.langchain.com/v0.2/api_reference/experimental/text_splitter/langchain_experimental.text_splitter.SemanticChunker.html)
   (bản này **chưa có** `gradient` và `min_chunk_size` — dùng để đối chiếu khi ghi số hiệu phiên bản).

> Kiểm lại số hiệu phiên bản `langchain-experimental` thực sự cài khi trích dẫn: bản v0.2
> chưa có `gradient` và `min_chunk_size`; mặc định `percentile = 95` lấy theo bảng
> `BREAKPOINT_DEFAULTS` trong mã nguồn.
