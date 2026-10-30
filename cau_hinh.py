"""Hằng số và đường dẫn dùng chung cho mọi bước.

Mọi tham số của thực nghiệm nằm ở đây để báo cáo trích dẫn được đúng một chỗ.
Đổi tham số = đổi thực nghiệm: ghi lại lý do trong commit.
"""
import os
from pathlib import Path

GOC = Path(__file__).resolve().parent

# ── thư mục ──────────────────────────────────────────────────────────────
DATA = GOC / "data"
RAW = DATA / "raw"              # HTML gốc + metadata JSON tải về
CLEAN = DATA / "clean"          # text đã chuẩn hoá, đã bỏ "Căn cứ…" và nơi nhận/chữ ký
CLEAN_FULL = DATA / "clean_full"  # text đã chuẩn hoá, CHƯA bỏ gì (để đối chiếu)
# Thử nghiệm mở rộng đặt CHUNKS_DIR / INDEX_DIR sang thư mục riêng để không lẫn với chỉ mục gốc (kể cả bộ đệm).
CHUNKS = Path(os.environ.get("CHUNKS_DIR", DATA / "chunks"))  # chunk của từng phương pháp (jsonl)
INDEX = Path(os.environ.get("INDEX_DIR", DATA / "index"))     # vector nhúng (memmap)
RESULTS = Path(os.environ.get("KET_QUA_DIR", GOC / "results"))  # máy cá nhân: chạy tái lập ra thư mục riêng
MODELS = GOC / "models"
MANIFEST = DATA / "manifest.csv"

# ── phân đoạn ────────────────────────────────────────────────────────────
CUA_SO = 300        # A: cửa sổ cố định 300 từ, không chồng lấn
DIEU_TOI_DA = 350   # B: Điều/khoản dài hơn ngưỡng này thì tách tiếp
# Seed = độ lệch điểm bắt đầu cửa sổ cho mỗi văn bản (seed 0 = không lệch, đúng đề). Chỉ dùng ở hai chỗ:
#  - A trần: 4 seed (0 + SEEDS), CHỈ đo truy hồi, không sinh — chứng minh dịch cửa sổ chỉ là nhiễu;
#  - B: phân đoạn 4 seed CHỈ để đếm (B chỉ khác nhau ở cửa sổ fallback của văn bản không có Điều), nhúng một lần.
# Mọi thứ khác (A+, A_H, B−, B+) và toàn bộ khâu sinh câu trả lời: một seed (0), không ngoại lệ.
# Khoảng tin cậy lấy từ bootstrap 1000 lần trên tập câu hỏi — đó là nguồn nhiễu chính.
SEEDS = (1, 2, 3)

# ── truy hồi / sinh ──────────────────────────────────────────────────────
MO_HINH_NHUNG = MODELS / "halong_embedding"
NHUNG_REPO = "contextboxai/halong_embedding"   # trước đây là hiieu/halong_embedding
NHUNG_REVISION = "b57776031035f70ed2030d2e35ecc533eb0f8f71"
KS = (1, 3, 5, 10)           # trục 1: cố định số chunk k
NGAN_SACH_TU = (300, 600, 1200)  # trục 2: cố định ngân sách TỪ nội dung (Recall@W) — so công bằng giữa chunk to/nhỏ
# Ngữ cảnh đưa cho mô hình sinh: KHÔNG cố định số chunk (k=5 cho A ≈ 1.500 từ nhưng cho B chỉ ≈ 465 từ), mà lấy
# CHUNK NGUYÊN theo thứ hạng tới khi chunk kế tiếp không còn vừa CÙNG MỘT ngân sách từ (tính cả tiền tố — đó là chữ
# mô hình thật sự đọc). 1.200 từ ≈ 1.700 token: cộng prompt hệ thống + câu hỏi + 384 token trả lời vẫn dưới
# n_ctx = 4096 của llama-server (đo thử 40 ngữ cảnh ngẫu nhiên mỗi phương pháp: prompt lớn nhất 2.354 token, ở B).
# Mỗi lần gọi đều kiểm số token thật và dừng cả job nếu bị cắt — xem rag/sinh.py.
NGAN_SACH_NGU_CANH_TU = 1200
K_UNG_VIEN = 50            # số chunk ứng viên lấy ra để lấp ngân sách
PP_SINH = ("A", "B", "B+")  # sinh câu trả lời: 1 seed (seed 0), không ngoại lệ
MAX_TOKENS_TRA_LOI = 384

# ── đánh giá ─────────────────────────────────────────────────────────────
TAU = 0.5            # ngưỡng độ phủ gold để tính là "trúng" (độ nhạy: 0.9)
TAU_NHAY = 0.9
BOOTSTRAP = 1000
NGUONG_NHIEU = 0.01  # chênh lệch dưới mức này coi như nhiễu (theo đề)
