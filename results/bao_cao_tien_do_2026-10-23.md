# Báo cáo tiến độ đồ án tốt nghiệp — 23/10/2026

**Đề tài:** Nghiên cứu phương pháp phân đoạn văn bản quy phạm pháp luật cho bài toán RAG.

Em xin báo cáo thầy ba việc: chọn phương pháp nào, hơn phương pháp cũ bao nhiêu, và cải tiến gì
so với công trình đã có. Mọi con số trong báo cáo đều đọc ra từ file trong `results/`, em ghi tên
file nguồn ngay dưới từng bảng.

---

## Câu 1. Em chọn phương pháp nào, và vì sao

Đồ án so **bốn cách phân đoạn đã có**: cắt theo **số từ cố định** (A), cắt theo **dấu câu** (C),
cắt theo **ngữ nghĩa** (D, dùng `SemanticChunker` của LangChain), và cắt theo **cấu trúc điều
khoản** (B). Em chọn **B — cắt theo cấu trúc Điều → Khoản → Điểm — làm hướng chính**.

Lý do nằm ở đặc thù của văn bản quy phạm pháp luật, không phải ở kết quả đo. Bố cục VBQPPL
**do luật quy định** (Luật Ban hành VBQPPL), không phải do người soạn tự chọn, nên nó ổn định và
máy dò được. Quan trọng hơn: **điều, khoản, điểm chính là đơn vị viện dẫn** — người ta trích dẫn
"khoản 2 Điều 14", không ai trích "đoạn văn thứ ba". Một hệ hỏi đáp pháp luật phải trả lời kèm
căn cứ, nên ranh giới chunk trùng ranh giới viện dẫn là một lợi thế mang tính bản chất, chứ không
phải mẹo kỹ thuật.

| Ký hiệu | Cách cắt | Số chunk | Trung vị từ | Max từ |
|---|---|---:|---:|---:|
| **A** | cửa sổ cố định 300 từ, không chồng lấn (baseline) | 5.172 | 300 | 300 |
| **A+** | A + tiền tố `[Số hiệu] [Trích yếu]` (đối chứng) | 5.172 | 300 | 300 |
| **C** | theo dấu câu, gom tới 300 từ | 5.640 | 281 | 300 |
| **D** | theo ngữ nghĩa, phân vị 95 (LangChain) | 7.673 | 199 | 385 |
| **B** | Điều → Khoản → Điểm, quá 350 từ mới cắt tiếp | 12.718 | 97 | 372 |
| **B−** | chunk của B, bỏ tiền tố (đối chứng) | 12.718 | 97 | 372 |

*Nguồn: `results/buoc3/thong_ke_chunk.md`.* **B+** không có tệp chunk riêng — nó dùng chunk của B
rồi mở rộng lên Điều cha lúc sinh câu trả lời, nên không có dòng trong bảng này.

---

## Câu 2. Hơn phương pháp cũ bao nhiêu

Bảng chính, 110 câu hỏi, τ = 0,5. Cột hiệu số là **B trừ phương pháp đó**, kèm khoảng tin cậy
bootstrap ghép cặp 95% (1000 lần, phân tầng theo nhóm câu hỏi):

| Phương pháp | R@5 | R@1200 từ | MRR | B − pp (R@5) | B − pp (MRR) |
|---|---:|---:|---:|---|---|
| A (cửa sổ cố định) | 0,691 | 0,627 | 0,486 | **+0,100 [+0,036; +0,164]** | **+0,093 [+0,029; +0,153]** |
| C (dấu câu) | 0,754 | 0,746 | 0,564 | +0,036 [−0,018; +0,091] | +0,015 [−0,048; +0,084] |
| D (ngữ nghĩa) | 0,709 | 0,700 | 0,545 | **+0,082 [+0,009; +0,154]** | +0,034 [−0,033; +0,100] |
| **B (cấu trúc)** | **0,791** | **0,782** | **0,579** | — | — |

*Nguồn: `results/metrics_truy_hoi.csv`, sinh bằng `python -m eval.chay_truy_hoi` (39 giây).
In đậm = khoảng tin cậy không chứa 0.*

**Nhận xét 1 — B hơn A bao nhiêu.** B hơn A **+0,100 điểm R@5** và **+0,093 MRR**; cả hai khoảng
tin cậy **không chứa 0**, nên chênh lệch này không phải do may rủi của mẫu. Ở trục ngân sách từ
(R@1200) mức chênh còn lớn hơn: **+0,154 [+0,082; +0,227]**. So với D thì B hơn +0,082 R@5 (CI
không chứa 0), còn so với C thì **chưa kết luận được** — +0,036 với CI chứa 0.

**Nhận xét 2 — nhóm nào chênh lớn nhất, nhóm nào không chênh.** Chênh lớn nhất ở **điều dài**
(B 0,632 so với A 0,474 R@5; MRR **+0,184 [+0,020; +0,365]**) và **câu đơn giản** (R@5
**+0,140 [+0,020; +0,260]**) — đúng chỗ mà cắt mù theo 300 từ hay xé đôi một khoản. Hai nhóm
**không chênh**: `dan_chieu` (cả bốn phương pháp đều 0,333 — dẫn chiếu chéo chưa được xử lý,
xem Câu 3) và `khong_co_dieu` (**+0,000 [0,000; 0,000]** ở R@5).

Em xin nói rõ một chỗ em từng nghĩ sai: nhóm `khong_co_dieu` **không phải "bằng A theo định
nghĩa"**. Em kiểm lại trên dữ liệu — **47/47 chunk fallback của B trùng ranh giới A tuyệt đối**,
nhưng B có gắn thêm tiền tố `[số hiệu] [trích yếu]` còn A thì không, nên **chuỗi đem nhúng khác
nhau**. Hệ quả: R@5 bằng nhau đúng 0,000 (cùng tập chunk lọt top-5) nhưng thứ hạng lệch —
MRR −0,030 (CI chứa 0). Ngoài ra ở nhóm này **C tốt hơn B** (MRR −0,148), và nhóm `xuyen_khoan`
thì **B kém A rõ rệt về MRR: −0,161 [−0,342; −0,003]** — chunk B nhỏ nên một khoản lẻ dễ lên
hạng 1 trước khi đủ cả hai khoản mà câu hỏi cần.

**Nhận xét 3 — gold trung lập so với gold trùng ranh giới.** Đây là chỗ thầy có thể nghi B thắng
vì cách định nghĩa đáp án, nên em tách riêng. 34 câu có gold **trung lập** (span cắt cố ý không
trùng ranh giới điều khoản) và 76 câu gold **trùng ranh giới**:

| Tập gold | n | B − A (R@5) | B − A (MRR) |
|---|---:|---|---|
| trung lập | 34 | +0,118 [+0,000; +0,235] | **+0,171 [+0,052; +0,283]** |
| trùng ranh giới | 76 | **+0,092 [+0,013; +0,171]** | +0,058 [−0,012; +0,127] |

*Nguồn: `results/metrics_truy_hoi.csv`.*

Lợi thế của B **không biến mất** trên gold trung lập — thậm chí còn **lớn hơn** về MRR. Nên mức
hơn của B không giải thích được bằng việc đáp án được đặt trùng ranh giới mà B cắt.

Hai baseline còn lại đứng ở đâu so với A:

| Hiệu số | R@5 | R@1200 từ | MRR |
|---|---|---|---|
| C − A | +0,064 [−0,018; +0,136] | **+0,118 [+0,045; +0,191]** | **+0,078 [+0,005; +0,151]** |
| D − A | +0,018 [−0,064; +0,100] | +0,073 [−0,018; +0,164] | +0,059 [−0,012; +0,131] |

*Nguồn: `results/metrics_truy_hoi.csv`.* Cắt theo ngữ nghĩa (D) **không** hơn cửa sổ cố định một
cách đo được trên bộ này.

*Toàn bộ số trên là của tầng truy hồi.*

### Độ chính xác trích dẫn — đã có, cập nhật 28/10

Phần gán nhãn tay đã xong: **120 dòng**, hai vòng chấm, bộ bóc trích dẫn bằng regex đạt độ khớp
**0,825** với nhãn người đọc (`results/kiem_regex_trich_dan.md`). Mọi con số dưới đây mang sẵn
sai số đó.

| Phương pháp | đạt | từ chối | cắt trần | **trích dẫn đúng** | độ phủ | độ chính xác | hiệu số so với A [KTC] |
|---|---:|---:|---:|---:|---:|---:|---|
| A | 96 | 13 | 1 | **0,182** | 0,250 | 0,233 | — |
| **B** | 103 | 5 | 2 | **0,536** | 0,682 | 0,647 | +0,355 [+0,264; +0,436] |
| B+ | 100 | 9 | 1 | **0,445** | 0,559 | 0,528 | +0,264 [+0,173; +0,355] |

*Nguồn: `results/metrics_trich_dan.csv`.* Kiểm định McNemar ghép cặp, hiệu chỉnh Holm:
**A vs B p = 8,3 × 10⁻⁹** và **A vs B+ p = 2,2 × 10⁻⁶** — đều có ý nghĩa; **B vs B+ p = 0,053**,
chưa kết luận được.

**Đây là chỗ cắt theo cấu trúc ăn điểm rõ nhất.** B hơn A **gần ba lần** ở trích dẫn (0,536 so
với 0,182), trong khi ở truy hồi chỉ hơn 0,100 điểm R@5. Nghĩa là lợi ích của việc cắt trùng
ranh giới viện dẫn không nằm ở chỗ *tìm đúng chỗ* mà ở chỗ **viết đúng căn cứ** — đúng thứ một
hệ hỏi đáp pháp luật cần.

Tách theo nhóm, chênh lệch tập trung ở hai nhóm: **dieu_dai** (A 0,000 so với B 0,737) và
**xuyen_khoan** (A 0,118 so với B 0,765). Nhóm `khong_co_dieu` cả ba phương pháp đều **0,000** —
văn bản không chia Điều thì không có "Điều … khoản …" để trích.

Trên **gold trung lập** (34 câu, span cố ý không trùng ranh giới): A 0,206 · B 0,706 ·
B+ 0,559, hiệu B − A = **+0,500 [+0,353; +0,676]**. Lợi thế của B **không đến từ việc đáp án
được đặt trùng ranh giới mà B cắt**.

---

## Câu 3. Cải tiến gì so với repo mẫu

**B của đồ án gần trùng cách làm của repo DSC 2026** (Điều → khoản → cửa sổ cố định). Em chỉ thêm
**tầng điểm** và dùng **cửa sổ 300 từ thay vì 256**. Vì vậy **so E với B chính là so với repo** —
đây là lý do em giữ nguyên B không sửa, để nó đóng vai bản gốc.

Cải tiến của em gói trong **phương pháp E**, ba thành phần, xếp theo dư địa đo được trên kho:

**1. Lặp câu dẫn của Điều và khoản vào mọi mảnh con.** Khi một Điều bị cắt thành nhiều chunk, câu
dẫn phần thân — câu quy định phạm vi áp dụng — chỉ còn ở mảnh đầu, các mảnh sau mất ngữ cảnh.
Đo được: **2.013/12.718 chunk của B = 16%** rơi vào tình trạng này (45 Điều có câu dẫn thân, 307
khoản có câu dẫn trước danh sách điểm); E chép câu dẫn vào **1.881 chunk**. Repo không xử lý.

**2. Nhãn vị trí mảnh "(phần i/n)".** Mảnh thứ ba của một khoản hiện ra giống hệt mảnh thứ nhất,
mô hình không biết nó đang đọc đoạn giữa. E gắn nhãn vào tiền tố, áp cho **285 chunk** thuộc
**105 đơn vị bị tách**. Repo không có.

**3. Cắt ngữ nghĩa CÓ CHẶN ở tầng cuối.** Thay cửa sổ trượt bằng cắt theo ngữ nghĩa, nhưng ranh
giới **không bao giờ vượt ra ngoài đơn vị pháp lý đang cắt**. Tác động **107 đơn vị**, tương ứng
**58.791/1.540.178 từ = 3,8%** của kho. Repo dùng cửa sổ 256 từ.

*Nguồn: `results/phuong_phap_E_bu_ngu_canh.md`; số 285 và 1.881 đếm lại trực tiếp trên
`data/chunks/Eduoi_s0.jsonl`.*

**Dư địa thật sự rất hẹp, và em xin coi đó là một kết quả.** Cắt theo cấu trúc đã xử lý gọn
khoảng **84% kho**; phần E động vào là **16% còn lại**, và riêng hướng ngữ nghĩa chỉ còn **3,8%
số từ**. Nói cách khác: **96,2% số từ của VBQPPL không cần tới phân đoạn ngữ nghĩa** vì cấu trúc
điều khoản đã tự chia nhỏ tới mức đủ. Đây vừa là giới hạn của cải tiến, vừa là một kết luận có
giá trị cho đề tài.

### E so với B trên 35 câu `manh_con`

`manh_con` là bộ câu hỏi em dựng riêng, nhắm thẳng vào mảnh con — đáp án nằm ở mảnh bị tách khỏi
đơn vị cha. 15 câu thuộc tập **mất câu dẫn**, 21 câu thuộc tập **tầng cuối**.

| Cấu hình | R@5 (tất cả) | MRR − B, tập *mất câu dẫn* | MRR − B, tập *tầng cuối* |
|---|---:|---|---|
| B (= repo) | 0,629 | — | — |
| E đầy đủ (dưới) | 0,600 | **−0,250 [−0,422; −0,078]** | +0,126 [−0,045; +0,270] |
| E đầy đủ (trên) | 0,600 | **−0,250 [−0,422; −0,078]** | +0,138 [−0,030; +0,278] |
| E tắt dẫn Điều | 0,600 | **−0,217 [−0,378; −0,061]** | +0,102 [−0,052; +0,245] |
| **E tắt dẫn khoản** | **0,657** | −0,033 [−0,100; +0,000] | +0,126 [−0,045; +0,270] |
| E tắt nhãn mảnh | 0,600 | **−0,250 [−0,422; −0,078]** | +0,119 [−0,054; +0,270] |
| E tắt semantic | 0,571 | **−0,250 [−0,422; −0,078]** | +0,038 [−0,016; +0,115] |
| **E chỉ semantic** | **0,657** | +0,000 [+0,000; +0,000] | +0,095 [−0,058; +0,244] |

*Nguồn: `results/metrics_truy_hoi.csv`.*

**Nhận xét thật, kể cả khi bất lợi cho em: ở tầng truy hồi, E đầy đủ KHÔNG hơn B.** Đọc theo cột
thì thủ phạm hiện ra rất rõ: **mọi cấu hình bật `dẫn khoản` đều mất đúng −0,250 MRR** trên tập
*mất câu dẫn*, khoảng tin cậy không chứa 0; hai cấu hình **tắt `dẫn khoản`** thì mức mất về gần 0.
Trớ trêu là thành phần sinh ra để chữa đúng vấn đề "mất câu dẫn" lại làm hỏng truy hồi ở chính tập
đó. Giải thích em cho là hợp lý: chép cùng một câu dẫn vào mọi chunk điểm của một khoản làm các
chunk ấy **giống nhau hơn** trong không gian nhúng, nên điểm đúng khó nổi lên hạng đầu.

Thành phần **có dấu hiệu tốt** là **cắt ngữ nghĩa có chặn**: trên tập *tầng cuối* mọi cấu hình bật
semantic đều dương (+0,095 đến +0,138 MRR), và cấu hình *tắt semantic* là cấu hình kém nhất bảng
(R@5 0,571). Nhưng **mọi khoảng tin cậy ở tập này đều chứa 0** với n = 21, nên em **chưa dám kết
luận**. Thành phần **nhãn mảnh** chưa tách được tác động riêng.

Em xin lưu ý: đây là truy hồi. Ba thành phần của E nhằm giúp **mô hình sinh hiểu đúng mảnh con**,
nên phải đo ở tầng trích dẫn. Đã đo xong (28/10): trên 35 câu `manh_con`, B 0,257 · B+ 0,200 ·
E đầy đủ 0,286 · E2 0,200 · E3 0,200. **Không cặp nào khác biệt có ý nghĩa** — McNemar sau Holm
đều cho p = 1,000. Với n = 35 thì bộ này quá nhỏ để kết luận; đó là giới hạn em phải nói rõ.

### Nhược điểm của repo mà đồ án đã tái lập

Repo DSC 2026 tự nhận ba nhược điểm; em kiểm lại cả ba trên dữ liệu của mình. **Tiêu đề Điều bị
vỡ**: họ báo 62%, em đo trên nguồn vbpl.vn chỉ **30/5.850 = 0,51%** trước chuẩn hoá và **0,00%**
sau — tức đây là vấn đề **của nguồn dữ liệu**, không phải của phương pháp. **Nhãn Điều sai ở văn
bản sửa đổi**: em tái lập được **35,7%**, và sau khi thêm bước nhận diện khối trích dẫn nguyên văn
thì còn **1,5%** (4/272 chunk kiểm được). **Dẫn chiếu chéo** thì em **chưa xử lý** — kết quả nhóm
`dan_chieu` ở Câu 2 (cả bốn phương pháp 0,333) cho thấy đúng như vậy; em xin để sang chương 5.

*Nguồn: `results/buoc2/thong_ke_du_lieu.md`, `results/buoc3/thong_ke_chunk.md`.*

---

## Tiến độ so với lịch đề cương

| Tuần — kế hoạch | Thực tế |
|---|---|
| 1–2 tìm hiểu | xong |
| 3–4 dữ liệu | xong — 80 văn bản, 1,54 triệu từ, có kiểm tiêu đề vỡ |
| 5 câu hỏi | xong — 110 câu bộ chính, **thêm** 35 câu `manh_con` ngoài kế hoạch |
| 6–7 phân đoạn cơ bản | xong — A, A+, C, D |
| 8–9 phân đoạn cấu trúc | xong — B, B+, B−, A_H |
| 10 ghép hệ thống | xong — truy hồi + sinh, có chốt chặn chỉ mục tự động |
| 11 chạy thử | xong — pilot 240 câu trả lời |
| 12 so sánh và giao diện | **đang làm** — truy hồi xong, trích dẫn chờ gán nhãn tay |
| 13–14 viết báo cáo và slide | khung slide đã dựng; chương 4–5 chưa viết |

Phần **vượt kế hoạch**: phương pháp E và bộ `manh_con` (đóng góp riêng, không có trong đề cương),
cùng 330 + 280 = **610 câu trả lời** đã sinh. Phần **chậm**: chương 4 và 5.

## Ba góp ý lần trước, em đã xử lý

1. Đã đổi toàn bộ "phân chia" thành **"phân đoạn"** trong quyển và trong mã nguồn.
2. Phạm vi giữ đúng **hỏi đáp VBQPPL tiếng Việt**, không mở rộng sang loại văn bản khác.
3. Phần tổng quan đã trả lời "đã có phương pháp chưa, nhược điểm gì": có — **repo DSC 2026** — và
   em liệt kê ba nhược điểm họ tự nhận, kèm kết quả tái lập ở Câu 3.

## Việc còn lại

- **Gán nhãn tay 120 câu trả lời** để có độ chính xác trích dẫn (đây là nút thắt lớn nhất).
- Chạy nốt phần đánh giá sinh; phần sinh câu trả lời đã xong 610/610.
- Viết chương 4 (thực nghiệm) và chương 5 (hạn chế, hướng phát triển).
- Hoàn thiện slide bảo vệ.

## Em xin ý kiến thầy ba điều

1. **Chỉ tiêu bộ câu hỏi.** Sau vòng duyệt, ba nhóm không đạt chỉ tiêu ban đầu: `xuyen_khoan` còn
   **17**, `dan_chieu` còn **9**, `dieu_dai` còn **19**. Em hạ chỉ tiêu để **giữ chất lượng** thay
   vì bù cho đủ số bằng câu kém. Thầy cho em hỏi cách làm này có chấp nhận được không.
2. **Vị trí của E.** E có nên được trình bày là **đóng góp chính** của đồ án không, khi dư địa của
   nó chỉ là 16% kho và ở tầng truy hồi nó chưa hơn B?
3. **Hướng kết luận nếu E không thắng.** Nếu đo xong tầng trích dẫn mà E vẫn không hơn B một cách
   đo được, em kết luận **"cắt theo cấu trúc đã đủ cho phần lớn VBQPPL, dư địa cho hướng ngữ nghĩa
   rất hẹp — 3,8% số từ"** thì có được coi là một kết quả hợp lệ của đồ án không, hay thầy muốn em
   đổi hướng cải tiến?
