"""Phương pháp D — phân đoạn theo ngữ nghĩa (baseline thứ ba của đề cương).

1. Tách câu như C (chunking/sentence.py).
2. Nhúng **CỤM 3 CÂU** quanh mỗi câu (câu i−1, i, i+1) bằng chính mô hình nhúng của pipeline
   (halong_embedding, vector đã chuẩn hoá L2) — ĐÚNG như bản gốc `SemanticChunker` của LangChain
   (`buffer_size=1`). Trước đây bản này nhúng từng câu RỜI, làm dãy khoảng cách nhiễu hơn bản gốc;
   đã sửa để không rơi vào cảnh "cài sai một phương pháp rồi kết luận phương pháp đó kém".
3. Khoảng cách giữa hai cụm liên tiếp = 1 − cosine. Đặt ranh giới ở các chỗ khoảng cách vượt phân vị 95
   của các khoảng cách TRONG văn bản đó — ngưỡng theo phân vị, không lấy số cứng (cách làm của
   SemanticChunker, LangChain).
4. Ràng buộc kích thước để so được với các bộ khác:
   - đoạn > 350 từ: cắt tiếp tại khoảng cách lớn nhất bên trong, lặp tới khi ≤ 350;
     **một câu đơn dài hơn 350 từ thì cắt tiếp bằng CỬA SỔ CỐ ĐỊNH kiểu A** (trước đây để nguyên,
     làm thủng trần — đo được max 413 từ);
   - đoạn < 50 từ: gộp sang đoạn bên cạnh có ranh giới gần nghĩa hơn; cho phép tổng vượt trần một
     **biên độ nhỏ** (TRAN_GOP) để chunk tí hon được hấp thụ, thay vì bỏ mặc (trước đây min 17 từ).
     Không gộp được thì giữ nguyên (đếm trong thống kê).
5. Văn bản có **dưới 20 câu** thì phân vị 95 vô nghĩa (5 câu → 4 khoảng cách → p95 ≈ max): rơi về
   cách gom của C, chunk đánh dấu `fallback=True`.
6. Không gắn tiền tố, các trường cấu trúc để trống — giống A, C. Một seed.

CỐ Ý KHÔNG SỬA (quyết định của người hướng dẫn):
- Bộ tách câu vẫn chỉ cắt ở `. ? !` (không thêm "a) b) đ)" hay ";"). Việc đơn vị câu của văn bản luật
  không trùng câu ngữ pháp là một PHÁT HIỆN cần giữ, không phải lỗi cần vá; và C được đề cương định
  nghĩa là "cắt theo dấu câu".
- Không đổi kiểu ngưỡng sang standard_deviation / gradient (D là baseline, đổi lõi là mất baseline).
- Không cài bản lai cấu trúc–ngữ nghĩa (để ở hướng phát triển).
"""
import numpy as np

from chunking.base import Chunk, Document, vi_tri_tu
from chunking.sentence import tach_cau

PHAN_VI = 95
TOI_THIEU, TOI_DA = 50, 350
BUFFER = 1                      # bản gốc LangChain: nhúng cụm (i−1, i, i+1)
TRAN_GOP = int(TOI_DA * 1.1)    # 385 — biên độ nhỏ cho phép khi hấp thụ chunk dưới sàn
TOI_THIEU_CAU = 20              # dưới ngưỡng này thì phân vị vô nghĩa → rơi về C
GIOI_HAN_GIAY = 4 * 3600  # nhúng câu dự kiến quá 4 giờ thì dừng, báo người dùng

_BANG: tuple | None = None  # (bộ đệm vector, {sha1: dòng})


def cum_cau(text: str, cau: list[tuple[int, int]], buffer: int = BUFFER) -> list[str]:
    """Chuỗi đem nhúng cho từng câu = cụm (i−buffer … i+buffer) nối liền theo văn bản gốc."""
    n = len(cau)
    return [text[cau[max(0, i - buffer)][0]:cau[min(n - 1, i + buffer)][1]] for i in range(n)]


def _du_dai(cau: list) -> bool:
    return len(cau) >= TOI_THIEU_CAU


def chuan_bi(docs: list[Document]) -> int:
    """Nhúng mọi CỤM 3 CÂU của tập văn bản qua bộ đệm chung (rag.chi_muc) — chạy lại sẽ tiếp tục.
    Chỉ nhúng cụm của văn bản thật sự dùng D (≥ 20 câu); văn bản ngắn rơi về C nên không cần nhúng."""
    global _BANG
    from rag import chi_muc

    cum = set()
    for d in docs:
        c = tach_cau(d.text)
        if _du_dai(c):
            cum.update(cum_cau(d.text, c))
    cum = sorted(cum)
    print(f"D: {len(cum)} cụm {2 * BUFFER + 1} câu khác nhau, {sum(len(c) for c in cum)} ký tự", flush=True)
    idx = chi_muc.nhung_bo_dem(cum, gioi_han_giay=GIOI_HAN_GIAY)
    bo = np.memmap(chi_muc.CACHE, dtype=np.float32, mode="r").reshape(-1, chi_muc.DIM)
    _BANG = (bo, idx)
    return len(cum)


def _vec_bo_dem(cau: list[str]) -> np.ndarray:
    from rag import chi_muc

    if _BANG is None:
        raise RuntimeError("chưa nhúng cụm câu — gọi semantic.chuan_bi(docs) trước")
    bo, idx = _BANG
    return np.stack([bo[idx[chi_muc.sha(c)]] for c in cau])


def _cat_cua_so(text: str, a: int, b: int, toi_da: int = TOI_DA) -> list[tuple[int, int, int]]:
    """Một câu dài hơn trần: cắt thành các cửa sổ ≤ `toi_da` từ, kiểu A (không chồng lấn)."""
    tu = vi_tri_tu(text, a, b)
    ra = []
    for i in range(0, len(tu), toi_da):
        lo = tu[i:i + toi_da]
        ra.append((lo[0][0], lo[-1][1], len(lo)))
    return ra or [(a, b, len(text[a:b].split()))]


def phan_doan(text: str, cau: list[tuple[int, int]], V: np.ndarray) -> list[tuple[int, int, int]]:
    """Các câu `cau` (vị trí) + vector từng CỤM `V` → [(start, end, số từ)] theo ngưỡng phân vị và
    ràng buộc 50–350 từ (câu đơn quá dài cắt cửa sổ; gộp dưới sàn được phép tới TRAN_GOP)."""
    if not cau:
        return []
    n = [len(text[a:b].split()) for a, b in cau]
    kc = 1 - np.sum(V[:-1] * V[1:], axis=1)  # kc[i] = khoảng cách giữa cụm i và cụm i+1
    nguong = np.percentile(kc, PHAN_VI) if len(kc) else 0.0
    moc = [0] + [i + 1 for i in range(len(kc)) if kc[i] > nguong] + [len(cau)]
    doan = [(i, j) for i, j in zip(moc, moc[1:])]

    def tach(i0: int, i1: int) -> list[tuple[int, int]]:
        if sum(n[i0:i1]) <= TOI_DA or i1 - i0 == 1:
            return [(i0, i1)]
        j = i0 + 1 + int(np.argmax(kc[i0:i1 - 1]))
        return tach(i0, j) + tach(j, i1)

    doan = [x for d in doan for x in tach(*d)]
    gop = True
    while gop and len(doan) > 1:
        gop = False
        for k, (i0, i1) in enumerate(doan):
            if sum(n[i0:i1]) >= TOI_THIEU:
                continue
            ben = []
            if k > 0:
                ben.append((kc[i0 - 1], k - 1))
            if k + 1 < len(doan):
                ben.append((kc[i1 - 1], k + 1))
            for _, j in sorted(ben):
                a0, a1 = min(doan[j][0], i0), max(doan[j][1], i1)
                if sum(n[a0:a1]) <= TRAN_GOP:   # biên độ nhỏ: hấp thụ chunk tí hon
                    doan[min(j, k)] = (a0, a1)
                    del doan[max(j, k)]
                    gop = True
                    break
            if gop:
                break

    ra: list[tuple[int, int, int]] = []
    for i0, i1 in doan:
        a, b, w = cau[i0][0], cau[i1 - 1][1], sum(n[i0:i1])
        if w > TOI_DA and i1 - i0 == 1:     # câu đơn quá dài → cửa sổ cố định kiểu A
            ra += _cat_cua_so(text, a, b)
        else:
            ra.append((a, b, w))
    return ra


def chunk(doc: Document, seed: int = 0, vec=_vec_bo_dem) -> list[Chunk]:
    cau = tach_cau(doc.text)

    def lam(doan, fallback):
        return [Chunk(chunk_id=f"D:{seed}:{doc.doc_id}:{k}", text=doc.text[a:b], doc_id=doc.doc_id,
                      so_hieu=doc.so_hieu, chuong=None, muc=None, dieu_so=None, dieu_ten=None, khoan_so=None,
                      diem=None, n_words=n, method="D", start=a, end=b, seed=seed, fallback=fallback)
                for k, (a, b, n) in enumerate(doan)]

    if not _du_dai(cau):        # văn bản quá ngắn: phân vị vô nghĩa → gom như C
        from chunking import sentence
        return lam(sentence.gom(doc.text, cau), True)
    V = vec(cum_cau(doc.text, cau)) if cau else np.zeros((0, 1))
    return lam(phan_doan(doc.text, cau, V), False)
