"""Phương pháp C — phân đoạn theo dấu câu (baseline thứ hai của đề cương).

- Tách văn bản thành câu: mỗi dòng là ranh giới; trong một dòng, cắt sau dấu . ? ! (hoặc …) khi theo sau là khoảng
  trắng rồi một chữ HOA / chữ số / dấu mở nháy. Không cắt ở các chỗ dấu chấm không kết câu:
    * nhãn đầu dòng: "Điều 5.", "Chương II.", "Mục 1.", "1.", "1.1.", "a." (đánh số khoản, mục);
    * chữ viết tắt: "v.v.", "TP.", "ThS." …, chữ cái hoa đứng một mình (tên viết tắt "N. V. A");
    * dấu chấm không có khoảng trắng phía sau: "1.000.000", "vbpl.vn", "./." — và số hiệu như "12/2025/NĐ-CP",
      "05/2025/TT-BXD" vốn không chứa dấu chấm nên không bao giờ bị cắt ở giữa.
- Gom câu liên tiếp cho tới khi câu kế tiếp làm chunk vượt 300 từ thì cắt, không chồng lấn. Câu dài hơn 300 từ đứng
  một mình thành một chunk.
- Không nhìn cấu trúc, không gắn tiền tố; dieu_so/khoan_so để trống — giống A. Một seed (seed 0).
"""
import re

import cau_hinh as ch
from chunking.base import Chunk, Document

VIET_TAT = {"v.v", "TP", "Tp", "TS", "ThS", "Ths", "PGS", "GS", "BS", "KS", "CN", "TX", "St", "Nxb", "tr", "Th.S",
            "PGS.TS", "Q", "P"}
# nhãn ở đầu câu mà dấu chấm ngay sau nó không kết câu
RE_NHAN_DAU = re.compile(r"\s*\"?(?:(?:Điều|Chương|Mục|Phần|Tiểu mục)\s+[\dIVXLCDM]+[a-zđ]?|[IVXLCDM]+|\d+[a-zđ]?(?:\.\d+[a-zđ]?)*|[a-zđ])\.")
# nhãn mở bằng dấu nháy ở giữa câu (văn bản sửa đổi trích nguyên văn): ... như sau: "3. Nội dung", ... Điều 41 "Điều 41. Tên"
RE_NHAN_NHAY = re.compile(r"\"(?:Điều\s+\d+[a-zđ]?|Chương\s+[\dIVXLCDM]+|Mục\s+\d+|[IVXLCDM]+|\d+[a-zđ]?(?:\.\d+[a-zđ]?)*|[a-zđ])$")
# ứng viên kết câu: . ? ! … (có thể lặp, có thể kèm nháy/ngoặc đóng) rồi khoảng trắng
RE_KET = re.compile(r"(?:\.{3}|…|[.?!])+[\"')\]»”]*(?=\s)")


def _la_ket_cau(dong: str, m: re.Match, dau_cau: int = 0) -> bool:
    j = m.end()
    sau = dong[j:].lstrip()
    if not sau:
        return False  # cuối dòng: xuống dòng tự là ranh giới
    if not (sau[0].isupper() or sau[0].isdigit() or sau[0] in "\"'“«(["):
        return False
    if m.group(0)[0] != ".":
        return True  # ? ! … luôn kết câu khi theo sau là chữ hoa
    # từ đứng ngay trước dấu chấm
    i = m.start()
    tu = dong[:i].split()[-1] if dong[:i].split() else ""
    if tu in VIET_TAT or (len(tu) == 1 and tu.isupper()):
        return False
    nhan = RE_NHAN_DAU.match(dong, dau_cau)
    if nhan and nhan.end() == i + 1:
        return False  # dấu chấm của nhãn đầu câu ("Điều 5.", "1.") — kể cả khi tiêu đề nằm giữa dòng
    if RE_NHAN_NHAY.search(dong, 0, i):
        return False  # nhãn trích dẫn: như sau: "3. …  /  "Điều 41. …
    return True


def tach_cau(text: str) -> list[tuple[int, int]]:
    """Vị trí [đầu, cuối) của từng câu (đã bỏ khoảng trắng hai đầu). Hợp các câu phủ mọi ký tự không trắng."""
    ra = []
    vt = 0
    for dong in text.split("\n"):
        a = 0
        for m in RE_KET.finditer(dong):
            if _la_ket_cau(dong, m, a):
                ra.append((vt + a, vt + m.end()))
                a = m.end()
        ra.append((vt + a, vt + len(dong)))
        vt += len(dong) + 1
    # bỏ khoảng trắng hai đầu, bỏ câu rỗng
    sach = []
    for a, b in ra:
        s = text[a:b]
        if s.strip():
            sach.append((a + len(s) - len(s.lstrip()), b - (len(s) - len(s.rstrip()))))
    return sach


def gom(text: str, cau: list[tuple[int, int]], toi_da: int = ch.CUA_SO) -> list[tuple[int, int, int]]:
    """Gom câu liên tiếp thành chunk ≤ `toi_da` từ → [(start, end, số từ)]. Câu dài hơn `toi_da` đứng riêng."""
    ra, dau, cuoi, n = [], None, None, 0
    for a, b in cau:
        k = len(text[a:b].split())
        if dau is not None and n + k > toi_da:
            ra.append((dau, cuoi, n))
            dau, n = None, 0
        if dau is None:
            dau = a
        cuoi, n = b, n + k
    if dau is not None:
        ra.append((dau, cuoi, n))
    return ra


def chunk(doc: Document, seed: int = 0) -> list[Chunk]:
    ra = []
    for k, (a, b, n) in enumerate(gom(doc.text, tach_cau(doc.text))):
        ra.append(Chunk(chunk_id=f"C:{seed}:{doc.doc_id}:{k}", text=doc.text[a:b], doc_id=doc.doc_id,
                        so_hieu=doc.so_hieu, chuong=None, muc=None, dieu_so=None, dieu_ten=None, khoan_so=None,
                        diem=None, n_words=n, method="C", start=a, end=b, seed=seed))
    return ra
