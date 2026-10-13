"""Kiểu dữ liệu và hàm dùng chung cho mọi phương pháp phân đoạn.

Interface chung (theo đề):  chunk(doc: Document) -> list[Chunk]

Ngoài các trường đề yêu cầu, mỗi Chunk ghi thêm VỊ TRÍ KÝ TỰ [start, end) của phần nội dung trong
data/clean/<doc_id>.txt. Đánh giá truy hồi so khớp gold theo vị trí ký tự, nên công bằng giữa phương pháp có
metadata Điều/khoản (B) và phương pháp không có (A) — không dựa vào metadata của chunk.
"""
import csv
import hashlib
import json
import random
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path

import cau_hinh as ch


@dataclass
class Document:
    doc_id: str
    so_hieu: str
    loai_van_ban: str
    trich_yeu: str
    text: str                      # data/clean/<doc_id>.txt
    nhom: str = ""
    meta: dict = field(default_factory=dict)


@dataclass
class Chunk:
    chunk_id: str
    text: str                      # đúng chuỗi đem đi nhúng = tien_to + nội dung
    doc_id: str
    so_hieu: str
    chuong: str | None
    muc: str | None
    dieu_so: int | None
    dieu_ten: str | None
    khoan_so: int | None
    diem: str | None
    n_words: int                   # số từ của phần NỘI DUNG (không tính tiền tố)
    method: str
    start: int                     # vị trí ký tự của nội dung trong text đã chuẩn hoá
    end: int
    fallback: bool = False         # B: văn bản không có "Điều" → rơi về cửa sổ cố định
    tien_to: str = ""              # tiền tố gắn trước nội dung (A+, A_H, B)
    seed: int = 0                  # seed độ lệch cửa sổ (0 = không lệch, đúng như đề)
    dieu_start: int | None = None  # B+: vị trí của cả Điều cha (để mở rộng khi sinh)
    dieu_end: int | None = None

    def dict(self) -> dict:
        return asdict(self)


def nap_van_ban(manifest: Path = ch.MANIFEST) -> list[Document]:
    ds = []
    for r in csv.DictReader(open(manifest)):
        ds.append(Document(doc_id=r["id"], so_hieu=r["so_hieu"], loai_van_ban=r["loai_van_ban"],
                           trich_yeu=r["trich_yeu"], text=(ch.CLEAN / f"{r['id']}.txt").read_text(),
                           nhom=r["nhom"], meta=r))
    return ds


RE_TU = re.compile(r"\S+")


def vi_tri_tu(text: str, a: int = 0, b: int | None = None) -> list[tuple[int, int]]:
    """Vị trí [đầu, cuối) của từng "từ" (chuỗi không chứa khoảng trắng) trong text[a:b]."""
    return [(m.start() + a, m.end() + a) for m in RE_TU.finditer(text[a:b if b is not None else len(text)])]


def so_tu(s: str) -> int:
    return len(s.split())


def do_lech(seed: int, doc_id: str, co: int = ch.CUA_SO) -> int:
    """Seed 0 → không lệch (đúng như đề: cửa sổ bắt đầu từ từ đầu tiên). Seed k > 0 → độ lệch U[1, co) cố định
    cho mỗi văn bản: cửa sổ đầu ngắn hơn, các cửa sổ sau đủ `co` từ."""
    if seed == 0:
        return 0
    h = int(hashlib.sha1(f"{seed}:{doc_id}".encode()).hexdigest(), 16)
    return random.Random(h).randrange(1, co)


def cua_so(text: str, a: int, b: int, co: int = ch.CUA_SO, lech: int = 0) -> list[tuple[int, int, int]]:
    """Cắt text[a:b] thành cửa sổ `co` từ không chồng lấn → [(start, end, số từ)]. `lech` > 0: cửa sổ đầu có
    `lech` từ. Vị trí trả về là vị trí ký tự trong toàn văn bản (từ đầu từ đầu tiên tới cuối từ cuối cùng)."""
    tu = vi_tri_tu(text, a, b)
    if not tu:
        return []
    moc = [0]
    if lech and lech < len(tu):
        moc.append(lech)
    while moc[-1] + co < len(tu):
        moc.append(moc[-1] + co)
    moc.append(len(tu))
    return [(tu[i][0], tu[j - 1][1], j - i) for i, j in zip(moc, moc[1:]) if j > i]


def tien_to_van_ban(doc: Document) -> str:
    return f"[{doc.so_hieu}] [{doc.trich_yeu}]"


def ghi_jsonl(p: Path, chunks: list[Chunk]) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    tam = p.with_suffix(".tmp")
    with open(tam, "w") as f:
        for c in chunks:
            f.write(json.dumps(c.dict(), ensure_ascii=False) + "\n")
    tam.replace(p)


def doc_jsonl(p: Path) -> list[Chunk]:
    return [Chunk(**json.loads(x)) for x in open(p) if x.strip()]
