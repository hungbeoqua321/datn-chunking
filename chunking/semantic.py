"""Phương pháp D — phân đoạn theo ngữ nghĩa (baseline thứ ba của đề cương).

1. Tách câu như C (chunking/sentence.py).
2. Nhúng từng câu bằng chính mô hình nhúng của pipeline (halong_embedding, vector đã chuẩn hoá L2).
3. Khoảng cách giữa hai câu liên tiếp = 1 − cosine. Đặt ranh giới ở các chỗ khoảng cách vượt phân vị 95 của các
   khoảng cách TRONG văn bản đó — ngưỡng theo phân vị, không lấy số cứng (cách làm của SemanticChunker, LangChain).
4. Ràng buộc kích thước để so được với các bộ khác:
   - đoạn > 350 từ: cắt tiếp tại khoảng cách lớn nhất bên trong, lặp tới khi ≤ 350 (một câu dài hơn 350 từ đứng riêng);
   - đoạn < 50 từ: gộp sang đoạn bên cạnh có ranh giới gần nghĩa hơn (khoảng cách nhỏ hơn) nếu tổng không vượt 350;
     không gộp được thì giữ nguyên (đếm trong thống kê).
5. Không gắn tiền tố, các trường cấu trúc để trống — giống A, C. Một seed.
"""
import numpy as np

from chunking.base import Chunk, Document
from chunking.sentence import tach_cau

PHAN_VI = 95
TOI_THIEU, TOI_DA = 50, 350
GIOI_HAN_GIAY = 4 * 3600  # nhúng câu dự kiến quá 4 giờ thì dừng, báo người dùng

_BANG: tuple | None = None  # (bộ đệm vector, {sha1: dòng})


def chuan_bi(docs: list[Document]) -> int:
    """Nhúng mọi câu của tập văn bản qua bộ đệm chung (rag.chi_muc) — chạy lại sẽ tiếp tục. Trả số câu khác nhau."""
    global _BANG
    from rag import chi_muc

    cau = sorted({d.text[a:b] for d in docs for a, b in tach_cau(d.text)})
    print(f"D: {len(cau)} câu khác nhau, {sum(len(c) for c in cau)} ký tự", flush=True)
    idx = chi_muc.nhung_bo_dem(cau, gioi_han_giay=GIOI_HAN_GIAY)
    bo = np.memmap(chi_muc.CACHE, dtype=np.float32, mode="r").reshape(-1, chi_muc.DIM)
    _BANG = (bo, idx)
    return len(cau)


def _vec_bo_dem(cau: list[str]) -> np.ndarray:
    from rag import chi_muc

    if _BANG is None:
        raise RuntimeError("chưa nhúng câu — gọi semantic.chuan_bi(docs) trước")
    bo, idx = _BANG
    return np.stack([bo[idx[chi_muc.sha(c)]] for c in cau])


def phan_doan(text: str, cau: list[tuple[int, int]], V: np.ndarray) -> list[tuple[int, int, int]]:
    """Các câu `cau` (vị trí) + vector từng câu `V` → [(start, end, số từ)] theo ngưỡng phân vị và ràng buộc 50–350 từ."""
    if not cau:
        return []
    n = [len(text[a:b].split()) for a, b in cau]
    kc = 1 - np.sum(V[:-1] * V[1:], axis=1)  # kc[i] = khoảng cách giữa câu i và câu i+1
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
                if sum(n[a0:a1]) <= TOI_DA:
                    doan[min(j, k)] = (a0, a1)
                    del doan[max(j, k)]
                    gop = True
                    break
            if gop:
                break
    return [(cau[i0][0], cau[i1 - 1][1], sum(n[i0:i1])) for i0, i1 in doan]


def chunk(doc: Document, seed: int = 0, vec=_vec_bo_dem) -> list[Chunk]:
    cau = tach_cau(doc.text)
    V = vec([doc.text[a:b] for a, b in cau]) if cau else np.zeros((0, 1))
    ra = []
    for k, (a, b, n) in enumerate(phan_doan(doc.text, cau, V)):
        ra.append(Chunk(chunk_id=f"D:{seed}:{doc.doc_id}:{k}", text=doc.text[a:b], doc_id=doc.doc_id,
                        so_hieu=doc.so_hieu, chuong=None, muc=None, dieu_so=None, dieu_ten=None, khoan_so=None,
                        diem=None, n_words=n, method="D", start=a, end=b, seed=seed))
    return ra
