"""Truy hồi dense + dựng ngữ cảnh cho mô hình sinh — GIỐNG HỆT nhau cho mọi phương pháp, chỉ khác tệp chunk.

- Truy hồi: nhúng câu hỏi (không tiền tố), cosine với ma trận chunk, lấy top-k.
- Ngữ cảnh sinh: KHÔNG cố định số khối — lấy CHUNK NGUYÊN theo thứ hạng (trong K_UNG_VIEN ứng viên) cho tới khi
  chunk kế tiếp không còn vừa ngân sách NGAN_SACH_NGU_CANH_TU từ (tính cả tiền tố: đó là chữ mô hình thật sự đọc).
  Không cắt dở chunk nào. Như nhau cho A, A+, B, B+ → mọi phương pháp được đưa cùng một lượng ngữ cảnh.
- B+: truy hồi trên chunk của B, rồi MỞ RỘNG mỗi chunk lên cả Điều cha (bỏ trùng Điều); Điều dài hơn phần ngân sách còn
  lại thì giữ một cửa sổ quanh đúng chunk trúng.
"""
import numpy as np

import cau_hinh as ch
from rag import chi_muc, nhung, sinh

TEP = {"A": "A_s0", "A+": "Acong_s0", "B": "B_s0", "B+": "B_s0", "A_H": "A_H_s0", "B-": "Btru_s0"}
_CACHE: dict[str, tuple] = {}
_VAN_BAN: dict[str, str] = {}


def nap(pp: str):
    ten = TEP.get(pp, pp)
    if ten not in _CACHE:
        _CACHE[ten] = chi_muc.nap(ten)
    return _CACHE[ten]


def vb(doc_id: str) -> str:
    if doc_id not in _VAN_BAN:
        _VAN_BAN[doc_id] = (ch.CLEAN / f"{doc_id}.txt").read_text()
    return _VAN_BAN[doc_id]


def nhung_cau_hoi(q: str) -> np.ndarray:
    return nhung.nhung([q])[0]


def tim(pp: str, q_vec: np.ndarray, k: int = 10) -> list[tuple[dict, float]]:
    m, cs = nap(pp)
    s = m @ q_vec
    top = np.argpartition(-s, min(k, len(s) - 1))[:k]
    top = top[np.argsort(-s[top])]
    return [(cs[i], float(s[i])) for i in top]


def _tien_to_dieu(c: dict) -> str:
    """Tiền tố tới cấp Điều (bỏ "> Khoản …", "> Điểm …") cho khối B+ đã mở rộng."""
    p = c["tien_to"].split(" > ")
    return " > ".join(x for x in p if not x.startswith(("Khoản ", "Điểm ")))


def ngu_canh(pp: str, ket_qua: list[tuple[dict, float]], ngan_sach: int = ch.NGAN_SACH_NGU_CANH_TU,
             k: int = ch.K_UNG_VIEN) -> list[dict]:
    """Danh sách khối {so_hieu, text, start, end, doc_id, chunk_id, mo_rong, bi_cat, so_tu} đưa cho mô hình sinh.

    Chỉ một trường hợp có cắt (bi_cat=True, ghi lại để báo cáo): B+ khi khối ĐẦU TIÊN là một Điều dài hơn cả ngân
    sách — giữ cửa sổ đúng `ngan_sach` từ quanh chunk trúng (thiết kế của B+, không phải cắt ngầm)."""
    khoi, da, con = [], set(), ngan_sach
    for c, _ in ket_qua[:k]:
        if pp == "B+" and c.get("dieu_start") is not None:
            key = (c["doc_id"], c["dieu_start"])
            if key in da:
                continue
            a, b = c["dieu_start"], c["dieu_end"]
            tt = _tien_to_dieu(c)
            t = vb(c["doc_id"])
            body, bi_cat = t[a:b], False
            n = len(tt.split()) + len(body.split())
            if n > con:
                if khoi:
                    break  # Điều kế tiếp không vừa → dừng (không cắt dở)
                # khối đầu: Điều dài hơn cả ngân sách → cửa sổ quanh chunk trúng, vừa đúng ngân sách
                tu = [(m.start() + a, m.end() + a) for m in __import__("re").finditer(r"\S+", body)]
                du = max(1, con - len(tt.split()))
                giua = next((i for i, (x, _) in enumerate(tu) if x >= c["start"]), 0)
                i0 = max(0, min(giua - du // 3, len(tu) - du))
                a, b = tu[i0][0], tu[min(len(tu), i0 + du) - 1][1]
                body, bi_cat = t[a:b], True
            da.add(key)
            text = tt + "\n" + body
            khoi.append({"so_hieu": c["so_hieu"], "text": text, "start": a, "end": b, "doc_id": c["doc_id"],
                         "chunk_id": c["chunk_id"], "mo_rong": True, "bi_cat": bi_cat, "so_tu": len(text.split())})
        else:
            n = len(c["text"].split())
            if n > con:
                break  # chunk kế tiếp không vừa ngân sách → dừng, không cắt dở
            khoi.append({"so_hieu": c["so_hieu"], "text": c["text"], "start": c["start"], "end": c["end"],
                         "doc_id": c["doc_id"], "chunk_id": c["chunk_id"], "mo_rong": False, "bi_cat": False,
                         "so_tu": n})
        con -= khoi[-1]["so_tu"]
        if con <= 0:
            break
    return khoi
