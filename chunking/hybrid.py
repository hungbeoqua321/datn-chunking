"""Phương pháp E — bù ngữ cảnh cho mảnh con khi cắt theo cấu trúc (đóng góp của đồ án).

E KHÔNG sửa B. B là baseline của bảng chính và gần trùng repo DSC 2026 (Điều → khoản → điểm → cửa sổ
cố định); giữ nguyên B chính là giữ bản gốc để đối chứng. E là file riêng, so trực tiếp với B.

Ba tầng đầu giống hệt B. E thêm BA THÀNH PHẦN, mỗi thành phần một công tắc riêng để đo đóng góp từng
phần (xem `CongTac`):

  (1a) dan_dieu   — chép câu dẫn THÂN của Điều (phần trước khoản 1) vào mọi chunk con của Điều đó,
                    không chỉ chunk khoản đầu. Đo được: 45 Điều có câu dẫn thân, 503 chunk hưởng lợi.
  (1b) dan_khoan  — chép câu dẫn của khoản (phần trước danh sách điểm) vào mọi chunk điểm của khoản
                    đó. Đo được: 307 khoản, 1.510 chunk. Cộng với (1a) là 2.013 chunk ≈ 16% của B.
  (2)  nhan_manh  — đơn vị bị tách làm nhiều mảnh thì mỗi mảnh mang nhãn "(phần i/n)" trong tiền tố,
                    kèm trường vi_tri_manh / tong_so_manh.
  (3)  semantic   — tầng cuối: đơn vị pháp lý vẫn > 350 từ thì cắt theo NGỮ NGHĨA thay vì cửa sổ cố
                    định, nhưng CÓ CHẶN: ranh giới không bao giờ vượt ra ngoài đơn vị đang cắt.
                    Chỉ chạm 107 đơn vị (3,8% số từ, ~2% chunk của B).

Lưu ý tiền tố: mọi chunk con của B ĐÃ mang "Điều N. <tên điều>" trong tiền tố, và tiền tố nằm trong
chuỗi đem nhúng — nên (1) KHÔNG lặp lại tên Điều (vô ích), chỉ lặp phần THÂN câu dẫn vốn bị mất.

Văn bản không có "Điều" → cửa sổ cố định, fallback=True — GIỐNG HỆT B, để E chỉ khác B đúng ở ba
thành phần trên.

Ngưỡng semantic tính TRONG PHẠM VI đơn vị đang cắt (không phải toàn văn bản, khác D ở chỗ này).
Đơn vị quá ngắn để lấy phân vị thì cắt ở chỗ khoảng cách lớn nhất.

Hai biến thể chỉ khác nhau ở câu bản lề — câu nằm đúng chỗ đổi ý thuộc về mảnh nào:
    E-duoi : câu bản lề thuộc mảnh DƯỚI (ranh giới đặt TRƯỚC nó)
    E-tren : câu bản lề thuộc mảnh TRÊN (ranh giới đặt SAU nó)
Không ưu ái biến thể nào; chạy cả hai rồi so bằng cùng bộ độ đo.
"""
from dataclasses import dataclass

import numpy as np

import cau_hinh as ch
from chunking.base import Chunk, Document, cua_so, do_lech, so_tu, tien_to_van_ban, vi_tri_tu
from chunking.semantic import PHAN_VI, TOI_DA, TOI_THIEU, TRAN_GOP, cum_cau
from chunking.sentence import tach_cau
from chunking.structural import (RE_DIEM, RE_KHOAN, _cat_khoang, _chia, _moc, dong_trich_dan,
                                 phan_tich, tien_to_khoi)

# số khoảng cách tối thiểu để phân vị có nghĩa; ít hơn thì cắt ở chỗ xa nhất
IT_KHOANG_CACH = 10
# câu dẫn dài hơn ngần này thì không chép lại (chép vào sẽ nuốt mất chỗ của nội dung)
DAN_TOI_DA = 80


@dataclass
class CongTac:
    """Bật/tắt từng thành phần của E để đo đóng góp riêng so với B."""
    dan_dieu: bool = True
    dan_khoan: bool = True
    nhan_manh: bool = True
    semantic: bool = True
    ban_le: str = "duoi"        # "duoi" | "tren"

    def ten(self) -> str:
        if self.dan_dieu and self.dan_khoan and self.nhan_manh and self.semantic:
            return f"E-{self.ban_le}"
        b = "".join(k for k, v in (("d", self.dan_dieu), ("k", self.dan_khoan),
                                   ("n", self.nhan_manh), ("s", self.semantic)) if v)
        return f"E[{b or 'B'}]-{self.ban_le}" if self.semantic else f"E[{b or 'B'}]"


# ── tầng cuối: cắt ngữ nghĩa CÓ CHẶN trong phạm vi một đơn vị ────────────────
def phan_doan_trong_don_vi(text: str, a: int, b: int, V: np.ndarray, cau: list[tuple[int, int]],
                           ban_le: str) -> list[tuple[int, int, int]]:
    """Cắt [a, b) theo ngữ nghĩa, ranh giới KHÔNG BAO GIỜ ra ngoài [a, b).

    `cau` là các câu nằm trong [a, b); `V` là vector của CỤM 3 CÂU quanh từng câu (như D).
    Ngưỡng lấy phân vị 95 của các khoảng cách TRONG đơn vị này. Trả [(start, end, số từ)].
    """
    if not cau:
        return [(a, b, so_tu(text[a:b]))]
    n = [len(text[x:y].split()) for x, y in cau]
    if len(cau) == 1:
        return _cat_cua_so(text, cau[0][0], cau[0][1])
    kc = 1 - np.sum(V[:-1] * V[1:], axis=1)
    # đơn vị quá ngắn để lấy phân vị → chỉ chỗ xa nhất thành ranh giới
    nguong = np.percentile(kc, PHAN_VI) if len(kc) >= IT_KHOANG_CACH else float(kc.max()) - 1e-12
    buoc = 1 if ban_le == "duoi" else 2     # câu bản lề thuộc mảnh dưới / mảnh trên
    moc = {0, len(cau)}
    for i in range(len(kc)):
        if kc[i] > nguong:
            moc.add(min(i + buoc, len(cau)))
    moc = sorted(moc)
    doan = [(i, j) for i, j in zip(moc, moc[1:]) if j > i]

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
                p0, p1 = min(doan[j][0], i0), max(doan[j][1], i1)
                if sum(n[p0:p1]) <= TRAN_GOP:
                    doan[min(j, k)] = (p0, p1)
                    del doan[max(j, k)]
                    gop = True
                    break
            if gop:
                break
    ra: list[tuple[int, int, int]] = []
    for i0, i1 in doan:
        x, y, w = cau[i0][0], cau[i1 - 1][1], sum(n[i0:i1])
        if w > TOI_DA and i1 - i0 == 1:
            ra += _cat_cua_so(text, x, y)
        else:
            ra.append((x, y, w))
    return ra


def _cat_cua_so(text: str, a: int, b: int, toi_da: int = TOI_DA) -> list[tuple[int, int, int]]:
    tu = vi_tri_tu(text, a, b)
    ra = [(lo[0][0], lo[-1][1], len(lo)) for lo in (tu[i:i + toi_da] for i in range(0, len(tu), toi_da)) if lo]
    return ra or [(a, b, so_tu(text[a:b]))]


def _cau_dan(text: str, a: int, b: int) -> str:
    """Câu dẫn chép lại được: phần [a, b) đã bỏ khoảng trắng, không rỗng, không quá dài."""
    a, b = _cat_khoang(text, a, b)
    if a >= b:
        return ""
    s = text[a:b]
    return s if so_tu(s) <= DAN_TOI_DA else ""


def chuan_bi(docs: list[Document]) -> int:
    """Nhúng cụm 3 câu CHỈ của các đơn vị pháp lý phải dùng tầng semantic (107 đơn vị) — rẻ hơn D
    rất nhiều vì không đụng tới phần còn lại của kho."""
    from chunking import semantic
    from rag import chi_muc

    cum = set()
    for d in docs:
        for a, b in _don_vi_tang_cuoi(d):
            c = [(x, y) for x, y in tach_cau(d.text) if a <= x and y <= b]
            if c:
                cum.update(cum_cau(d.text, c))
    cum = sorted(cum)
    print(f"E: {len(cum)} cụm 3 câu của các đơn vị tầng cuối, {sum(len(c) for c in cum)} ký tự", flush=True)
    idx = chi_muc.nhung_bo_dem(cum, gioi_han_giay=semantic.GIOI_HAN_GIAY)
    bo = np.memmap(chi_muc.CACHE, dtype=np.float32, mode="r").reshape(-1, chi_muc.DIM)
    global _BANG
    _BANG = (bo, idx)
    return len(cum)


_BANG: tuple | None = None


def _vec_bo_dem(cs: list[str]) -> np.ndarray:
    from rag import chi_muc

    if _BANG is None:
        raise RuntimeError("chưa nhúng cụm câu — gọi hybrid.chuan_bi(docs) trước")
    bo, idx = _BANG
    return np.stack([bo[idx[chi_muc.sha(c)]] for c in cs])


def _don_vi_tang_cuoi(doc: Document) -> list[tuple[int, int]]:
    """Các đơn vị pháp lý vẫn > 350 từ sau ba tầng Điều/khoản/điểm — đúng chỗ B rơi về cửa sổ."""
    t = doc.text
    khoi = phan_tich(t)
    if not khoi:
        return []
    trich = dong_trich_dan(t)
    ra = []
    for k in khoi:
        if k.loai != "dieu":
            continue
        dd = k.dong_dieu if k.dong_dieu is not None else k.start
        if so_tu(t[dd:k.end]) <= ch.DIEU_TOI_DA:
            continue
        mk = _moc(t, k.start, k.end, RE_KHOAN, bo_dong_dau=True, trich=trich)
        if not mk:
            ra.append((k.start, k.end))
            continue
        for a, b, _ in _chia(t, k.start, k.end, mk):
            if so_tu(t[max(a, dd):b]) <= ch.DIEU_TOI_DA:
                continue
            md = _moc(t, max(a, dd), b, RE_DIEM, bo_dong_dau=True, trich=trich)
            if not md:
                ra.append((a, b))
                continue
            for x, y, _d in _chia(t, a, b, md):
                if so_tu(t[max(x, dd):y]) > ch.DIEU_TOI_DA:
                    ra.append((x, y))
    return ra


# ── dựng chunk ──────────────────────────────────────────────────────────────
def chunk(doc: Document, seed: int = 0, ct: CongTac | None = None, vec=None) -> list[Chunk]:
    ct = ct or CongTac()
    vec = vec or _vec_bo_dem
    ten = ct.ten()
    t = doc.text
    ra: list[Chunk] = []

    def them(a, b, k, khoan=None, diem=None, fallback=False, n=None, dan="", manh=None):
        a, b = _cat_khoang(t, a, b)
        if a >= b:
            return
        tt = tien_to_khoi(doc, k, khoan, diem) if k else tien_to_van_ban(doc)
        if manh and ct.nhan_manh and manh[1] > 1:
            tt += f" (phần {manh[0]}/{manh[1]})"
        than = t[a:b]
        if dan:
            than = dan + "\n" + than
        ra.append(Chunk(chunk_id=f"{ten}:{seed}:{doc.doc_id}:{len(ra)}", text=tt + "\n" + than,
                        doc_id=doc.doc_id, so_hieu=doc.so_hieu, chuong=k.chuong if k else None,
                        muc=k.muc if k else None, dieu_so=k.dieu_so if k else None,
                        dieu_ten=k.dieu_ten if k else None, khoan_so=khoan, diem=diem,
                        n_words=n if n is not None else so_tu(t[a:b]), method=ten, start=a, end=b,
                        fallback=fallback, tien_to=tt, seed=seed,
                        dieu_start=k.start if k and k.loai == "dieu" else None,
                        dieu_end=k.end if k and k.loai == "dieu" else None,
                        kem_theo=k.kem_theo if k else None,
                        vi_tri_manh=manh[0] if manh and manh[1] > 1 else None,
                        tong_so_manh=manh[1] if manh and manh[1] > 1 else None,
                        cau_dan_lap=dan))

    def cat_cuoi(a, b, k, khoan=None, diem=None, dan=""):
        """Tầng cuối: semantic có chặn (thành phần 3) hoặc cửa sổ cố định như B."""
        if ct.semantic:
            cau = [(x, y) for x, y in tach_cau(t) if a <= x and y <= b]
            if cau:
                V = vec(cum_cau(t, cau))
                mieng = phan_doan_trong_don_vi(t, a, b, V, cau, ct.ban_le)
            else:
                mieng = list(cua_so(t, a, b))
        else:
            mieng = list(cua_so(t, a, b))
        for i, (x, y, n) in enumerate(mieng, 1):
            them(x, y, k, khoan=khoan, diem=diem, n=n, dan=dan, manh=(i, len(mieng)))

    if not t.strip():
        tt = tien_to_van_ban(doc)
        ra.append(Chunk(chunk_id=f"{ten}:{seed}:{doc.doc_id}:0", text=tt + "\n" + doc.trich_yeu,
                        doc_id=doc.doc_id, so_hieu=doc.so_hieu, chuong=None, muc=None, dieu_so=None,
                        dieu_ten=None, khoan_so=None, diem=None, n_words=so_tu(doc.trich_yeu),
                        method=ten, start=0, end=0, tien_to=tt, seed=seed))
        return ra
    khoi = phan_tich(t)
    trich = dong_trich_dan(t)
    if not khoi:        # không có Điều → cửa sổ cố định, GIỐNG B
        for a, b, n in cua_so(t, 0, len(t), ch.CUA_SO, do_lech(seed, doc.doc_id)):
            them(a, b, None, fallback=True, n=n)
        return ra

    for k in khoi:
        if k.loai != "dieu":
            for a, b, n in cua_so(t, k.start, k.end):
                them(a, b, k, n=n)
            continue
        dd = k.dong_dieu if k.dong_dieu is not None else k.start
        if so_tu(t[dd:k.end]) <= ch.DIEU_TOI_DA:
            them(k.start, k.end, k)
            continue
        mk = _moc(t, k.start, k.end, RE_KHOAN, bo_dong_dau=True, trich=trich)
        if not mk:
            cat_cuoi(k.start, k.end, k)
            continue
        # (1a) câu dẫn THÂN của Điều: phần sau dòng "Điều N…" tới khoản 1
        ld = t.find("\n", dd) + 1
        dan_d = _cau_dan(t, ld, mk[0][0]) if (ct.dan_dieu and 0 < ld < mk[0][0]) else ""
        for i_k, (a, b, so_khoan) in enumerate(_chia(t, k.start, k.end, mk)):
            # mảnh khoản ĐẦU đã chứa sẵn câu dẫn của Điều (B gộp vào đó) → chỉ chép cho khoản 2 trở đi
            dd_k = dan_d if i_k > 0 else ""
            if so_tu(t[max(a, dd):b]) <= ch.DIEU_TOI_DA:
                them(a, b, k, khoan=int(so_khoan), dan=dd_k)
                continue
            md = _moc(t, max(a, dd), b, RE_DIEM, bo_dong_dau=True, trich=trich)
            if not md:
                cat_cuoi(a, b, k, khoan=int(so_khoan), dan=dd_k)
                continue
            # (1b) câu dẫn của khoản: phần trước điểm đầu tiên
            dan_k = _cau_dan(t, a, md[0][0]) if ct.dan_khoan else ""
            for i_d, (x, y, diem) in enumerate(_chia(t, a, b, md)):
                dan_x = "\n".join(s for s in (dd_k, dan_k if i_d > 0 else "") if s)
                if so_tu(t[max(x, dd):y]) <= ch.DIEU_TOI_DA:
                    them(x, y, k, khoan=int(so_khoan), diem=diem, dan=dan_x)
                else:
                    cat_cuoi(x, y, k, khoan=int(so_khoan), diem=diem, dan=dan_x)
    return ra
