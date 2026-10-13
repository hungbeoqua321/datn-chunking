"""Hằng số và đường dẫn dùng chung cho mọi bước.

Mọi tham số của thực nghiệm nằm ở đây để báo cáo trích dẫn được đúng một chỗ.
Đổi tham số = đổi thực nghiệm: ghi lại lý do trong commit.
"""
from pathlib import Path

GOC = Path(__file__).resolve().parent

# ── thư mục ──────────────────────────────────────────────────────────────
DATA = GOC / "data"
RAW = DATA / "raw"              # HTML gốc + metadata JSON tải về
CLEAN = DATA / "clean"          # text đã chuẩn hoá, đã bỏ "Căn cứ…" và nơi nhận/chữ ký
CLEAN_FULL = DATA / "clean_full"  # text đã chuẩn hoá, CHƯA bỏ gì (để đối chiếu)
CHUNKS = DATA / "chunks"        # chunk của từng phương pháp (jsonl)
INDEX = DATA / "index"          # vector nhúng (memmap)
RESULTS = GOC / "results"
MODELS = GOC / "models"
MANIFEST = DATA / "manifest.csv"

# ── phân đoạn ────────────────────────────────────────────────────────────
CUA_SO = 300        # A: cửa sổ cố định 300 từ, không chồng lấn
DIEU_TOI_DA = 350   # B: Điều/khoản dài hơn ngưỡng này thì tách tiếp
SEEDS = (1, 2, 3)   # seed = độ lệch điểm bắt đầu cửa sổ cho mỗi văn bản (xem README)

# ── truy hồi / sinh ──────────────────────────────────────────────────────
MO_HINH_NHUNG = MODELS / "halong_embedding"
NHUNG_REPO = "contextboxai/halong_embedding"   # trước đây là hiieu/halong_embedding
NHUNG_REVISION = "b57776031035f70ed2030d2e35ecc533eb0f8f71"
KS = (1, 3, 5, 10)
K_SINH = 5                 # số chunk tối đa đưa cho mô hình sinh
NGAN_SACH_NGU_CANH = 2000  # token (tokenizer của LLM), như nhau cho mọi phương pháp
MAX_TOKENS_TRA_LOI = 384

# ── đánh giá ─────────────────────────────────────────────────────────────
TAU = 0.5            # ngưỡng độ phủ gold để tính là "trúng" (độ nhạy: 0.9)
TAU_NHAY = 0.9
BOOTSTRAP = 1000
NGUONG_NHIEU = 0.01  # chênh lệch dưới mức này coi như nhiễu (theo đề)
