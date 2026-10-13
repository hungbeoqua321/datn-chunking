"""Các phép chấm dùng chung (thuần Python, test được bằng dữ liệu giả).

Độ phủ gold: cov_k(G) = |G ∩ ∪ span(top-k chunk cùng văn bản)| / |G| (theo VỊ TRÍ KÝ TỰ của phần nội dung,
không tính tiền tố). Span của chunk chỉ tính tới chỗ mô hình nhúng THỰC SỰ đọc (end_nhung: chunk dài hơn 512 token bị
cắt đuôi khi nhúng — phần đuôi đó không thể giúp chunk được truy hồi nên không được tính là "đã lấy về").
Bản tương đương E(G): đoạn trùng nội dung ở văn bản khác CÙNG SỐ HIỆU (không bao giờ là bản cũ/bản sửa đổi của một
văn bản khác); câu hỏi về phiên bản thì tắt hẳn → lấy trúng bản đã hết hiệu lực không bao giờ được tính là đúng.
"""
import math
import random
import re
from collections import defaultdict

TAU = 0.5


# ── độ phủ ──────────────────────────────────────────────────────────────────
def giao(a: int, b: int, spans: list[tuple[int, int]]) -> int:
    """Số ký tự của [a, b) nằm trong hợp các khoảng `spans` (các khoảng có thể chồng nhau)."""
    s = sorted((max(a, x), min(b, y)) for x, y in spans if min(b, y) > max(a, x))
    tong, cuoi = 0, a
    for x, y in s:
        x = max(x, cuoi)
        if y > x:
            tong += y - x
            cuoi = y
    return tong


def do_phu(gold: dict, chunks: list[dict], tuong_duong: list[dict] | None = None) -> float:
    """cov của MỘT đơn vị gold với tập chunk (mỗi chunk có doc_id, start, end)."""
    theo_vb = defaultdict(list)
    for c in chunks:
        theo_vb[c["doc_id"]].append((c["start"], c.get("end_nhung", c["end"])))
    tot = 0.0
    for g in [gold] + list(tuong_duong or []):
        n = g["end"] - g["start"]
        if n > 0:
            tot = max(tot, giao(g["start"], g["end"], theo_vb.get(g["doc_id"], [])) / n)
    return tot


def recall_k(golds: list[dict], ket_qua: list[dict], k: int, tau: float = TAU, td: dict | None = None,
             chi_so: bool = False) -> float:
    """Gold nhiều đơn vị: 'đủ cả' (mọi đơn vị đạt τ) → 1/0. chi_so=True: trả tỉ lệ đơn vị đạt τ (trung bình)."""
    top = ket_qua[:k]
    dat = [do_phu(g, top, (td or {}).get(i)) >= tau for i, g in enumerate(golds)]
    return sum(dat) / len(dat) if chi_so else float(all(dat))


def mrr(golds: list[dict], ket_qua: list[dict], k: int = 10, tau: float = TAU, td: dict | None = None) -> float:
    """1/r*, r* = hạng nhỏ nhất mà top-r đạt 'đủ cả' τ; 0 nếu không đạt trong top-k."""
    for r in range(1, min(k, len(ket_qua)) + 1):
        if recall_k(golds, ket_qua, r, tau, td) == 1.0:
            return 1.0 / r
    return 0.0


def so_tu_doc(c: dict) -> int:
    """Số từ mô hình thật sự đọc của một chunk = tiền tố + nội dung (tiền tố chiếm ngân sách thật khi gửi cho mô hình)."""
    return len(c["text"].split()) if "text" in c else max(1, c.get("n_words", 1))


def cat_theo_tu(ket_qua: list[dict], ngan_sach: int) -> list[dict]:
    """Recall@W: lấy CHUNK NGUYÊN theo thứ hạng cho tới khi chunk kế tiếp làm vượt `ngan_sach` từ thì dừng — đếm CẢ
    tiền tố, giống hệt cách dựng ngữ cảnh cho mô hình sinh. Chunk đầu tiên luôn được lấy (chunk A+ 316 từ, D tới 350 từ
    vẫn có mặt ở W = 300)."""
    ra, con = [], ngan_sach
    for c in ket_qua:
        n = so_tu_doc(c)
        if n > con and ra:
            break
        ra.append(c)
        con -= n
    return ra


def du_trong_mot_chunk(golds: list[dict], ket_qua: list[dict], k: int, nguong: float = 0.9) -> float:
    """Mọi đơn vị gold nằm trọn (≥ 90%) trong CÙNG một chunk thuộc top-k (độ đo này thiên về B — ghi rõ)."""
    return float(any(all(do_phu(g, [c]) >= nguong for g in golds) for c in ket_qua[:k]))


# ── gold tương đương ở văn bản khác ─────────────────────────────────────────
def _chuan(s: str) -> tuple[str, list[int]]:
    """Chuẩn hoá để so khớp (bỏ ký hiệu chú thích [n], dấu nháy, gộp khoảng trắng, chữ thường) + bảng vị trí gốc."""
    ra, vt, trang = [], [], False
    i = 0
    while i < len(s):
        m = re.match(r"\[\d+\]", s[i:])
        if m:
            i += m.end()
            continue
        c = s[i]
        if c in "\"'":
            i += 1
            continue
        if c.isspace():
            if not trang and ra:
                ra.append(" ")
                vt.append(i)
            trang = True
        else:
            ra.append(c.lower())
            vt.append(i)
            trang = False
        i += 1
    return "".join(ra), vt


def _ngram(s: str, n: int = 5) -> set:
    return {s[i:i + n] for i in range(max(0, len(s) - n + 1))}


def tim_tuong_duong(gold: dict, van_ban: dict[str, str], so_hieu: dict[str, str], phien_ban: bool = False,
                    nguong: float = 0.8, _cache: dict = {}) -> list[dict]:  # noqa: B006
    """Các đoạn ở văn bản KHÁC nhưng CÙNG SỐ HIỆU với gold, có độ chứa 5-gram ký tự ≥ nguong (neo bằng 60 ký tự
    đầu/giữa/cuối). Câu hỏi phiên bản (phien_ban=True) → không có bản tương đương."""
    if phien_ban:
        return []
    g, _ = _chuan(van_ban[gold["doc_id"]][gold["start"]:gold["end"]])
    if len(g) < 40:
        return []
    ng = _ngram(g)
    neo = {g[:60], g[len(g) // 2:len(g) // 2 + 60], g[-60:]}
    ra = []
    for doc_id, t in van_ban.items():
        if doc_id == gold["doc_id"] or so_hieu.get(doc_id) != so_hieu.get(gold["doc_id"]):
            continue
        if doc_id not in _cache:
            _cache[doc_id] = _chuan(t)
        tc, vt = _cache[doc_id]
        for n in neo:
            j = tc.find(n)
            if j < 0:
                continue
            off = g.find(n)
            a = max(0, j - off)
            b = min(len(tc), a + len(g))
            ng2 = _ngram(tc[a:b])
            if ng and len(ng & ng2) / len(ng) >= nguong:
                ra.append({"doc_id": doc_id, "start": vt[a], "end": vt[b - 1] + 1})
                break
    return ra


# ── thống kê ────────────────────────────────────────────────────────────────
def bootstrap_hieu(a: list[float], b: list[float], nhom: list[str] | None = None, lan: int = 1000,
                   seed: int = 2026, cum: list[str] | None = None) -> tuple[float, float, float]:
    """Bootstrap GHÉP CẶP cho hiệu trung bình b − a → (hiệu, CI95 dưới, CI95 trên) — percentile.
    nhom: lấy mẫu lại phân tầng theo nhóm câu hỏi. cum: lấy mẫu lại theo cụm (văn bản) thay vì theo câu."""
    rng = random.Random(seed)
    d = [y - x for x, y in zip(a, b)]
    n = len(d)
    hieu = sum(d) / n
    if cum:
        theo = defaultdict(list)
        for i, c in enumerate(cum):
            theo[c].append(i)
        cums = list(theo.values())
    elif nhom:
        theo = defaultdict(list)
        for i, g in enumerate(nhom):
            theo[g].append(i)
    mau = []
    for _ in range(lan):
        if cum:
            idx = [i for c in (rng.choice(cums) for _ in cums) for i in c]
        elif nhom:
            idx = [rng.choice(ids) for ids in theo.values() for _ in ids]
        else:
            idx = [rng.randrange(n) for _ in range(n)]
        mau.append(sum(d[i] for i in idx) / len(idx))
    mau.sort()
    return hieu, mau[int(0.025 * lan)], mau[min(lan - 1, int(math.ceil(0.975 * lan)) - 1)]


def mcnemar(a: list[float], b: list[float]) -> float:
    """p-value McNemar chính xác (hai phía) cho hai dãy nhị phân ghép cặp."""
    b01 = sum(1 for x, y in zip(a, b) if x < 0.5 <= y)
    b10 = sum(1 for x, y in zip(a, b) if y < 0.5 <= x)
    n = b01 + b10
    if n == 0:
        return 1.0
    k = min(b01, b10)
    p = sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n
    return min(1.0, 2 * p)


def holm(p: dict[str, float]) -> dict[str, float]:
    """Hiệu chỉnh Holm–Bonferroni."""
    ds = sorted(p.items(), key=lambda x: x[1])
    m, ra, cao = len(ds), {}, 0.0
    for i, (k, v) in enumerate(ds):
        cao = max(cao, min(1.0, (m - i) * v))
        ra[k] = cao
    return ra
