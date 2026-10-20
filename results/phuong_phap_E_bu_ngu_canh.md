# Phương pháp E — bù ngữ cảnh cho mảnh con khi cắt theo cấu trúc

Đóng góp đề xuất của đồ án. Code: `chunking/hybrid.py`. So trực tiếp với B, **không sửa B**.

> B là baseline của bảng chính theo đề cương, và gần trùng repo DSC 2026
> (Điều → khoản → điểm → cửa sổ cố định). Giữ nguyên B chính là giữ bản gốc để đối chứng,
> nên E nằm ở file riêng. **E tắt hết công tắc cho ra chunk trùng khít B** trên cả 80 văn bản
> (12.718/12.718 chunk, trùng cả ranh giới lẫn tiền tố) — đây là bất biến được test tự động giữ.

---

## 1. B còn thiếu gì — dư địa đo được

Ba con số dưới đây là lý do E tồn tại. Chúng được đo trên chính kho 80 văn bản, **không phụ thuộc
vào việc E thắng hay thua** ở bước đánh giá truy hồi.

| Dư địa | Số đo | Nghĩa là |
|---|---:|---|
| Chunk con **mất câu dẫn phần thân** | **2.013 / 12.718 = 16%** | mảnh bị cắt rời khỏi câu quy định phạm vi áp dụng |
| Chunk phải **rơi về cửa sổ cố định** | **252 / 12.718 = 2,0%** | chỗ duy nhất B cắt mù, không bám cấu trúc |
| Số từ nằm trong đơn vị phải cắt mù | **58.791 / 1.540.178 = 3,8%** | **dư địa của phân đoạn ngữ nghĩa trên VBQPPL** |

Con số **3,8%** đáng ghi vào báo cáo như một kết quả riêng: trên văn bản quy phạm pháp luật,
cấu trúc Điều–khoản–điểm đã tự chia nhỏ tới mức **96,2% số từ không cần tới phân đoạn ngữ nghĩa**.
Dư địa cho hướng ngữ nghĩa vì thế rất hẹp — một kết luận có giá trị kể cả khi E không thắng.

Chi tiết dư địa câu dẫn: chỉ **45/1.140 Điều bị tách (4%)** có câu dẫn phần thân, và **307 khoản**
có câu dẫn trước danh sách điểm. Lưu ý: mọi chunk con của B **đã mang `Điều N. <tên điều>` trong
tiền tố**, và tiền tố nằm trong chuỗi đem nhúng — nên E **không** lặp lại tên Điều (vô ích), chỉ
lặp phần **thân** câu dẫn vốn bị mất.

## 2. Ba thành phần, bốn công tắc

| Công tắc | Thành phần | Phạm vi tác động |
|---|---|---|
| `dan_dieu` | (1a) chép câu dẫn thân của **Điều** vào mọi chunk con | 45 Điều |
| `dan_khoan` | (1b) chép câu dẫn của **khoản** vào mọi chunk điểm | 307 khoản |
| `nhan_manh` | (2) nhãn **"(phần i/n)"** cho mọi đơn vị bị tách | mọi đơn vị nhiều mảnh |
| `semantic` | (3) tầng cuối cắt **ngữ nghĩa có chặn** thay cửa sổ cố định | 107 đơn vị |

Mỗi công tắc bật tắt riêng để đo đóng góp từng phần so với B.

**Ràng buộc của (3):** ranh giới ngữ nghĩa **không bao giờ vượt ra ngoài đơn vị pháp lý đang cắt**
— chỉ được cắt bên trong một Điều/khoản/điểm. Ngưỡng lấy phân vị 95 của các khoảng cách **trong
phạm vi đơn vị đó** (khác D, vốn tính trên toàn văn bản); đơn vị quá ngắn để lấy phân vị thì cắt ở
chỗ khoảng cách lớn nhất. Mỗi mảnh vẫn theo chính sách trần sàn đang áp (50–385 từ).

**Văn bản không có Điều** rơi về **cửa sổ cố định, giống hệt B** — để E chỉ khác B đúng ở ba thành
phần trên, không thêm biến thứ hai.

**Hai biến thể câu bản lề** (câu nằm đúng chỗ đổi ý thuộc mảnh nào): `E-duoi` cho nó xuống mảnh
dưới, `E-tren` giữ nó ở mảnh trên. Cài đối xứng, không ưu ái bên nào.

## 3. Thống kê chunk theo từng tổ hợp công tắc

80 văn bản, seed 0. Cột "chunk có dẫn" = số chunk được chép thêm câu dẫn; "% dẫn" = phần trăm độ dài
chunk bị câu dẫn chép lại chiếm.

| Cấu hình | Chunk | T.vị | Max | Min | <50 từ | >350 từ | Ký tự mất | Chunk có dẫn | % dẫn |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **B (gốc)** | 12.718 | 97 | 372 | 3 | 2.781 | 16 | 0 | 0 | 0,0 |
| E tắt hết | 12.718 | 97 | 372 | 3 | 2.781 | 16 | 0 | 0 | 0,0 |
| + dẫn Điều | 12.718 | 97 | 372 | 3 | 2.781 | 16 | 0 | 471 | 0,4 |
| + dẫn khoản | 12.718 | 97 | 372 | 3 | 2.781 | 16 | 0 | 1.419 | 2,0 |
| + nhãn mảnh | 12.718 | 97 | 372 | 3 | 2.781 | 16 | 0 | 0 | 0,0 |
| + semantic (duoi) | 12.753 | 97 | 381 | 3 | 2.779 | 28 | 0 | 0 | 0,0 |
| + semantic (tren) | 12.753 | 97 | 381 | 3 | 2.779 | 28 | 0 | 0 | 0,0 |
| **E đầy đủ (duoi)** | **12.753** | 97 | **381** | 3 | 2.779 | **28** | **0** | **1.881** | **2,4** |
| **E đầy đủ (tren)** | **12.753** | 97 | **381** | 3 | 2.779 | **28** | **0** | **1.881** | **2,4** |

Đọc bảng:

- **E tắt hết trùng khít B** — xác nhận ba tầng đầu chép đúng, mọi khác biệt về sau đều do công tắc.
- **(1a) và (1b) không đổi ranh giới**, chỉ thêm chữ vào thân chunk: cộng lại 1.881 chunk, chiếm
  **2,4%** độ dài. Chi phí ngữ cảnh rất rẻ so với lượng ngữ nghĩa bù được.
- **(2) nhãn mảnh không đổi số đo nào** vì chỉ thêm chữ vào tiền tố — phải đo bằng truy hồi, không
  đo được bằng thống kê chunk.
- **(3) semantic** làm số chunk tăng nhẹ (12.718 lên 12.753, +35) và dài nhất tăng 372 lên 381;
  số chunk dưới sàn giảm nhẹ (2.781 xuống 2.779). Số chunk vượt 350 tăng 16 lên 28, toàn bộ do
  biên độ gộp, không chunk nào vượt 385.
- **Không mất ký tự nào** ở mọi cấu hình.

### Phân bố số mảnh trên mỗi đơn vị bị tách

| Số mảnh | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 10 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Cửa sổ cố định (B) | 82 | 17 | 5 | 2 | — | 1 | — | — |
| Semantic có chặn (E) | 66 | 24 | 7 | 3 | 2 | — | 2 | 1 |

Semantic cắt **nhỏ và nhiều mảnh hơn** cửa sổ: số đơn vị chỉ tách đôi giảm từ 82 xuống 66, phần
chuyển sang nhóm 3 mảnh trở lên. Đây là hệ quả của việc ranh giới đặt theo chỗ đổi ý chứ không theo
mốc 300 từ.

### Hai biến thể câu bản lề khác nhau bao nhiêu

`E-duoi` và `E-tren` cho **cùng mọi số thống kê**, nhưng **không** cùng ranh giới:
**75 chunk khác nhau** (12.678/12.753 trùng), và **6/105 đơn vị bị tách có số mảnh khác nhau**.
Khác biệt nhỏ nhưng có thật, nên vẫn phải đo bằng truy hồi chứ không kết luận từ thống kê chunk.

## 4. Bộ câu hỏi riêng để đo E

Bộ chính 112 câu **không đo được E**: chỉ 16 câu chạm vùng mất câu dẫn và 2 câu chạm đơn vị tầng
cuối. Vì vậy dựng bộ riêng **`manh_con`, 30 câu**, báo cáo ở mục riêng, **không gộp vào bảng chính**:

- **15 câu** có gold trong tập 2.013 chunk mất câu dẫn — đo thành phần (1) và (2);
- **16 câu** có gold trong 107 đơn vị tầng cuối — đo thành phần (3);
- 1 câu thuộc cả hai tập; **12 câu gold trung lập**.

Báo cáo tách **hai bảng theo hai tập**, ghi rõ n của từng tập.

## 5. Những gì KHÔNG làm

- Không sửa A, B, C, D. Không thêm biến thể ngoài `E-tren` và `E-duoi`.
- Không dùng mô hình sinh để quyết định ranh giới — E tất định với một mô hình nhúng cho trước.
- Không mở rộng ngược lên Điều cha khi sinh câu trả lời (đó là việc của B+).
- Không hạ ngưỡng 350 riêng cho E (sẽ làm E khác B ở hai biến cùng lúc).
