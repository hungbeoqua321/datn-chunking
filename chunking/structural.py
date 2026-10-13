"""Phương pháp B — phân đoạn bám cấu trúc pháp lý (Điều → Khoản → Điểm), và các biến thể dùng chung bộ phân tích.

Tầng 1  tách theo "Điều N" — regex của đề: ^Điều\\s+(\\d+)\\s*[.．:]?\\s*(.*)$ (từng dòng); nhận cả trường hợp tên
        điều nằm ở dòng kế tiếp.
Tầng 2  Điều dài hơn 350 từ → tách theo khoản ^(\\d+)[.)]\\s ; khoản vẫn > 350 từ → tách theo điểm ^([a-zđ])\\)\\s ;
        cuối cùng mới rơi về cửa sổ cố định 300 từ. Phần dẫn trước khoản 1 (vd "Điều 5. Tên ⏎ Người lao động có
        quyền sau đây:") gộp vào chunk khoản đầu tiên; tương tự phần dẫn trước điểm a) gộp vào chunk điểm đầu.
Tầng 3  văn bản KHÔNG có "Điều" → cửa sổ 300 từ, fallback=True (giống hệt A+ cùng seed).
Tầng 0  văn bản rỗng → một chunk từ trích yếu (không để mất văn bản).

Mọi chunk của B mang tiền tố phân cấp, lặp lại ở MỌI chunk con của một Điều:
    [Số hiệu] [Trích yếu] > Chương X > Mục m > Điều N. Tên điều > Khoản k > Điểm a
Phần đầu văn bản trước Điều 1 (quốc hiệu, tên văn bản…) thành chunk riêng (cửa sổ, tiền tố văn bản); vùng chú
thích cuối của VBHN ("[1] …") cũng thành chunk riêng — không gộp vào Điều cuối.

Biến thể dùng chung bộ phân tích (đối chứng, chỉ đo truy hồi):
  B− : chunk của B nhưng KHÔNG gắn tiền tố;
  A_H: ranh giới cửa sổ của A + tiền tố phân cấp của Điều chứa từ đầu tiên của cửa sổ.
B+ dùng đúng chunk của B (mở rộng lên Điều cha xảy ra lúc sinh, nhờ dieu_start/dieu_end).
"""
import re
from dataclasses import dataclass

import cau_hinh as ch
from chunking.base import Chunk, Document, cua_so, do_lech, so_tu, tien_to_van_ban
from crawl.chuan_hoa import vung_chu_thich

RE_DIEU = re.compile(r"^Điều\s+(\d+)\s*[.．:]?\s*(.*)$")       # đúng gợi ý của đề
RE_KHOAN = re.compile(r"^(\d+)[.)]\s")
RE_DIEM = re.compile(r"^([a-zđ])\)\s")
RE_PHAN = re.compile(r"^(?:Phần|PHẦN)\s+(thứ\s+\S+|THỨ\s+\S+|[IVXLC\d]+)\b")
RE_CHUONG = re.compile(r"^(?:Chương|CHƯƠNG)\s+([IVXLC\d]+[a-z]?)\b")
RE_MUC = re.compile(r"^(?:Mục|MỤC)\s+(\d+|[IVXLC]+|[A-ZĐ])\b")


@dataclass
class Khoi:
    """Một đơn vị cấp Điều (hoặc phần đầu / chú thích) của văn bản."""
    loai: str               # "dieu" | "dau" | "chu_thich"
    start: int
    end: int
    dieu_so: int | None = None
    dieu_ten: str | None = None
    chuong: str | None = None
    muc: str | None = None
    dong_dieu: int | None = None   # vị trí dòng "Điều N" (khối có thể bắt đầu sớm hơn ở dòng tiêu đề Chương/Mục)
    nhan: str | None = None        # nhãn Điều đầy đủ, vd "51a" (dieu_so vẫn là số nguyên 51)


def _dong(text: str) -> list[tuple[int, int, str]]:
    ra, i = [], 0
    for x in text.split("\n"):
        ra.append((i, i + len(x), x))
        i += len(x) + 1
    return ra


def phan_tich(text: str) -> list[Khoi]:
    """Chia văn bản thành khối cấp Điều. Dòng tiêu đề Phần/Chương/Mục gắn vào ĐẦU Điều kế tiếp (để mọi ký tự đều
    thuộc một chunk) và cập nhật ngữ cảnh chương/mục cho tiền tố."""
    dong = _dong(text)
    ct = vung_chu_thich([x for _, _, x in dong])
    het_than = dong[ct][0] if ct is not None else len(text)
    khoi: list[Khoi] = []
    chuong = muc = None
    cho = None  # vị trí dòng tiêu đề Chương/Mục đang chờ gắn vào Điều kế tiếp
    dau_dieu = []
    for k, (a, b, x) in enumerate(dong):
        if a >= het_than:
            break
        if x.strip() in ("Chương", "CHƯƠNG", "Mục", "MỤC") and k + 1 < len(dong):
            x = x.strip() + " " + dong[k + 1][2]  # tiêu đề "Chương ⏎ VIII TÊN" bị ngắt dòng (chỉ để nhận dạng)
        if RE_PHAN.match(x) or RE_CHUONG.match(x) or RE_MUC.match(x):
            m = RE_CHUONG.match(x)
            if m:
                chuong, muc = m.group(1), None
            elif RE_MUC.match(x):
                muc = RE_MUC.match(x).group(1)
            else:
                chuong = muc = None
            cho = a if cho is None else cho
            continue
        m = RE_DIEU.match(x)
        if m:
            ten = m.group(2).strip()
            if not ten and k + 1 < len(dong):  # tên điều nằm ở dòng kế tiếp
                nx = dong[k + 1][2]
                if nx and not (RE_KHOAN.match(nx) or RE_DIEM.match(nx) or RE_DIEU.match(nx)):
                    ten = nx.strip()
            mh = re.match(r"^Điều\s+(\d+)([a-zđ])\s*[.．:]\s*(.*)$", x)  # "Điều 51a. Tên" (điều bổ sung)
            nhan = m.group(1)
            if mh:
                nhan, ten = mh.group(1) + mh.group(2), mh.group(3).strip()
            dau_dieu.append((cho if cho is not None else a, int(m.group(1)), ten, chuong, muc, a, nhan))
            cho = None
    if not dau_dieu:
        return []
    if dau_dieu[0][0] > 0:
        khoi.append(Khoi("dau", 0, dau_dieu[0][0]))
    for i, (a, n, ten, c, mu, dd, nhan) in enumerate(dau_dieu):
        b = dau_dieu[i + 1][0] if i + 1 < len(dau_dieu) else het_than
        khoi.append(Khoi("dieu", a, b, n, ten, c, mu, dd, nhan))
    if het_than < len(text):
        khoi.append(Khoi("chu_thich", het_than, len(text)))
    return khoi


def tien_to_khoi(doc: Document, k: Khoi, khoan: int | None = None, diem: str | None = None) -> str:
    p = [tien_to_van_ban(doc)]
    if k.loai == "chu_thich":
        p.append("Chú thích")
    if k.chuong:
        p.append(f"Chương {k.chuong}")
    if k.muc:
        p.append(f"Mục {k.muc}")
    if k.loai == "dieu":
        nh = k.nhan or k.dieu_so
        p.append(f"Điều {nh}. {k.dieu_ten}".rstrip(". ") if k.dieu_ten else f"Điều {nh}")
    if khoan is not None:
        p.append(f"Khoản {khoan}")
    if diem is not None:
        p.append(f"Điểm {diem}")
    return " > ".join(p)


def _moc(text: str, a: int, b: int, re_moc: re.Pattern, bo_dong_dau: bool) -> list[tuple[int, str]]:
    """Vị trí đầu các dòng khớp re_moc trong text[a:b] → [(vị trí, nhãn)]."""
    ra = []
    for s, _, x in _dong(text[a:b]):
        if bo_dong_dau and s == 0:
            continue
        m = re_moc.match(x)
        if m:
            ra.append((a + s, m.group(1)))
    return ra


def _chia(text: str, a: int, b: int, moc: list[tuple[int, str]]) -> list[tuple[int, int, str]]:
    """Cắt [a, b) tại các mốc; đoạn dẫn trước mốc đầu gộp vào đoạn đầu."""
    ra = []
    for i, (s, nhan) in enumerate(moc):
        e = moc[i + 1][0] if i + 1 < len(moc) else b
        ra.append((a if i == 0 else s, e, nhan))
    return ra


def _cat_khoang(text: str, a: int, b: int) -> tuple[int, int]:
    """Bỏ khoảng trắng hai đầu [a, b)."""
    while a < b and text[a].isspace():
        a += 1
    while b > a and text[b - 1].isspace():
        b -= 1
    return a, b


def chunk(doc: Document, seed: int = 0, co_tien_to: bool = True) -> list[Chunk]:
    ten = "B" if co_tien_to else "B-"
    t = doc.text
    ra: list[Chunk] = []

    def them(a, b, k: Khoi | None, khoan=None, diem=None, fallback=False, n=None):
        a, b = _cat_khoang(t, a, b)
        if a >= b:
            return
        tt = (tien_to_khoi(doc, k, khoan, diem) if k else tien_to_van_ban(doc)) if co_tien_to else ""
        body = t[a:b]
        ra.append(Chunk(chunk_id=f"{ten}:{seed}:{doc.doc_id}:{len(ra)}", text=(tt + "\n" + body) if tt else body,
                        doc_id=doc.doc_id, so_hieu=doc.so_hieu, chuong=k.chuong if k else None,
                        muc=k.muc if k else None, dieu_so=k.dieu_so if k else None,
                        dieu_ten=k.dieu_ten if k else None, khoan_so=khoan, diem=diem,
                        n_words=n if n is not None else so_tu(body), method=ten, start=a, end=b, fallback=fallback,
                        tien_to=tt, seed=seed, dieu_start=k.start if k and k.loai == "dieu" else None,
                        dieu_end=k.end if k and k.loai == "dieu" else None))

    # Tầng 0: văn bản rỗng
    if not t.strip():
        tt = tien_to_van_ban(doc) if co_tien_to else ""
        ra.append(Chunk(chunk_id=f"{ten}:{seed}:{doc.doc_id}:0", text=(tt + "\n" + doc.trich_yeu) if tt else doc.trich_yeu,
                        doc_id=doc.doc_id, so_hieu=doc.so_hieu, chuong=None, muc=None, dieu_so=None, dieu_ten=None,
                        khoan_so=None, diem=None, n_words=so_tu(doc.trich_yeu), method=ten, start=0, end=0,
                        tien_to=tt, seed=seed))
        return ra
    khoi = phan_tich(t)
    # Tầng 3: không có Điều → cửa sổ 300 từ (giống A+ cùng seed), đánh dấu fallback
    if not khoi:
        for a, b, n in cua_so(t, 0, len(t), ch.CUA_SO, do_lech(seed, doc.doc_id)):
            them(a, b, None, fallback=True, n=n)
        return ra
    for k in khoi:
        if k.loai != "dieu":  # phần đầu văn bản / chú thích VBHN: cửa sổ, không phải fallback
            for a, b, n in cua_so(t, k.start, k.end):
                them(a, b, k, n=n)
            continue
        # Tầng 1: cả Điều nếu ≤ 350 từ — đếm từ dòng "Điều N" (tiêu đề Chương/Mục gắn ở đầu khối chỉ để phủ hết
        # ký tự, không thuộc Điều nên không tính vào ngưỡng)
        dd = k.dong_dieu if k.dong_dieu is not None else k.start
        if so_tu(t[dd:k.end]) <= ch.DIEU_TOI_DA:
            them(k.start, k.end, k)
            continue
        # Tầng 2: tách theo khoản
        mk = _moc(t, k.start, k.end, RE_KHOAN, bo_dong_dau=True)
        if not mk:
            for a, b, n in cua_so(t, k.start, k.end):
                them(a, b, k, n=n)
            continue
        for a, b, so_khoan in _chia(t, k.start, k.end, mk):
            if so_tu(t[max(a, dd):b]) <= ch.DIEU_TOI_DA:
                them(a, b, k, khoan=int(so_khoan))
                continue
            md = _moc(t, max(a, dd), b, RE_DIEM, bo_dong_dau=True)
            if not md:
                for x, y, n in cua_so(t, a, b):
                    them(x, y, k, khoan=int(so_khoan), n=n)
                continue
            for x, y, diem in _chia(t, a, b, md):
                if so_tu(t[max(x, dd):y]) <= ch.DIEU_TOI_DA:
                    them(x, y, k, khoan=int(so_khoan), diem=diem)
                else:
                    for u, v, n in cua_so(t, x, y):
                        them(u, v, k, khoan=int(so_khoan), diem=diem, n=n)
    return ra


def chunk_b_tru(doc: Document, seed: int = 0) -> list[Chunk]:
    """B− : chunk của B, không tiền tố."""
    return chunk(doc, seed, co_tien_to=False)


def chunk_ah(doc: Document, seed: int = 0) -> list[Chunk]:
    """A_H: ranh giới cửa sổ của A (cùng seed) + tiền tố phân cấp của Điều chứa từ đầu cửa sổ."""
    khoi = phan_tich(doc.text)
    ra = []
    for i, (a, b, n) in enumerate(cua_so(doc.text, 0, len(doc.text), ch.CUA_SO, do_lech(seed, doc.doc_id))):
        k = next((x for x in khoi if x.start <= a < x.end), None)
        tt = tien_to_khoi(doc, k) if k else tien_to_van_ban(doc)
        body = doc.text[a:b]
        ra.append(Chunk(chunk_id=f"A_H:{seed}:{doc.doc_id}:{i}", text=tt + "\n" + body, doc_id=doc.doc_id,
                        so_hieu=doc.so_hieu, chuong=k.chuong if k else None, muc=k.muc if k else None,
                        dieu_so=k.dieu_so if k else None, dieu_ten=k.dieu_ten if k else None, khoan_so=None,
                        diem=None, n_words=n, method="A_H", start=a, end=b, tien_to=tt, seed=seed))
    return ra
