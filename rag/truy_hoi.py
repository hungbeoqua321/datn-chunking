"""Truy hồi dense + dựng ngữ cảnh cho mô hình sinh — GIỐNG HỆT nhau cho mọi phương pháp, chỉ khác tệp chunk.

- Truy hồi: nhúng câu hỏi (không tiền tố), cosine với ma trận chunk, lấy top-k.
- Ngữ cảnh sinh: KHÔNG cố định số khối — lấy CHUNK NGUYÊN theo thứ hạng (trong K_UNG_VIEN ứng viên) cho tới khi
  chunk kế tiếp không còn vừa ngân sách NGAN_SACH_NGU_CANH_TU từ (tính cả tiền tố: đó là chữ mô hình thật sự đọc).
  Không cắt dở chunk nào. Như nhau cho A, A+, B, B+ → mọi phương pháp được đưa cùng một lượng ngữ cảnh.
- B+: truy hồi trên chunk của B, rồi MỞ RỘNG mỗi chunk lên cả Điều cha (bỏ trùng Điều); Điều dài hơn phần ngân sách còn
  lại thì giữ một cửa sổ quanh đúng chunk trúng.
"""
import re

import numpy as np

import cau_hinh as ch
from rag import chi_muc, nhung, sinh

TEP = {"A": "A_s0", "A+": "Acong_s0", "B": "B_s0", "B+": "B_s0", "A_H": "A_H_s0", "B-": "Btru_s0",
       "C": "C_s0", "D": "D_s0",
       # E2: truy hồi trên chỉ mục "E chỉ semantic" (đã nhúng sẵn, KHÔNG nhúng gì mới); phần bù
       # ngữ cảnh làm ở TẦNG SINH, xem ngu_canh(). Kết quả truy hồi của E2 trùng Echi_s.
       "E2": "Echi_s_s0",
       # E3 = E2 + theo dẫn chiếu tường minh MỘT BƯỚC, kéo đơn vị đích vào ngay sau chunk dẫn.
       "E3": "Echi_s_s0",
       # E3b = E3 nhưng NỀN LÀ B: không mở rộng lên Điều cha, chỉ chunk truy hồi được cộng
       # các đơn vị đích kéo theo dẫn chiếu. Tách riêng tác động của việc theo dẫn chiếu
       # khỏi tác động của việc mở rộng khối.
       "E3b": "B_s0",
       # E2n (thăm dò, results/local_gpu/thu_them.md) = E2 nhưng trong khối đã mở rộng lên Điều, mỗi dòng
       # khoản được gắn lại nhãn "(Điều N khoản k)". Phân tích lỗi bước 3: E2 dẫn nhầm Điều ở 10 câu B
       # làm đúng, vì sau khi mở rộng nhãn Điều chỉ còn ở đầu khối dài.
       "E2n": "Echi_s_s0"}
# Phương pháp mở rộng khối lên cả Điều cha trước khi đưa cho mô hình sinh.
MO_RONG_DIEU = ("B+", "E2", "E3", "E2n")
_RE_KHOAN = re.compile(r"^(\d+)\.\s", re.M)
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


def _gan_nhan_khoan(body: str, dieu_so) -> str:
    """E2n: "1. Người nào…" → "(Điều 217 khoản 1) 1. Người nào…" cho mọi dòng khoản trong thân Điều."""
    if dieu_so is None:
        return body
    return _RE_KHOAN.sub(lambda m: f"(Điều {dieu_so} khoản {m.group(1)}) {m.group(0)}", body)


def _bu_ngu_canh_e2(c: dict, body: str) -> str:
    """Bù ngữ cảnh cho E2 — CHỈ ở tầng sinh, KHÔNG đụng chuỗi đem nhúng.

    Đặc tả sửa ngày 26/10: **chỉ chép câu dẫn của ĐIỀU, không chép câu dẫn của KHOẢN.**
    Bằng chứng: trên bộ manh_con, mọi cấu hình bật `dan_khoan` đều làm câu mc031 chạm trần
    MAX_TOKENS (5/5: Eduoi, Etren, Etat_d, Etat_n, Etat_s), còn mọi cấu hình tắt nó thì không
    (5/5: B, Etat_k, Echi_s, B+, E2). `dan_dieu` KHÔNG phân biệt được hai nhóm — Etat_d tắt dẫn
    Điều mà vẫn cắt. Câu dẫn khoản bị chép vào mọi chunk điểm nên phình ngữ cảnh; câu dẫn Điều
    chỉ có ở 45 Điều nên không.

    Trước đó (22/10) đã đo: chép câu dẫn vào CHUỖI NHÚNG làm hỏng truy hồi — mất 0,250 MRR trên
    tập mất câu dẫn. Bù ở tầng sinh tránh hẳn chuyện đó: vector không đổi, chỉ chữ mô hình đọc.

    Hàm chỉ chạy cho khối KHÔNG được mở rộng lên Điều cha. Đo thật trên 35 câu manh_con:
    **42/42 khối đều được mở rộng**, nên hàm này không chạy lần nào — câu dẫn Điều đã nằm sẵn
    trong thân Điều. Giữ lại để đúng đặc tả nếu dữ liệu đổi, không phải vì nó đang có tác dụng.
    """
    them = []
    if c.get("dieu_start") is not None:
        from chunking.hybrid import _cau_dan   # nhập tại chỗ: tránh vòng nhập rag ↔ chunking
        dan = _cau_dan(vb(c["doc_id"]), c["dieu_start"], c["start"])
        if dan and dan not in body:
            them.append(dan)                   # câu dẫn của ĐIỀU; câu dẫn của khoản: KHÔNG chép
    nhan = (f" (phần {c['vi_tri_manh']}/{c['tong_so_manh']})"
            if c.get("tong_so_manh") and c["tong_so_manh"] > 1 else "")
    if nhan:
        dong = body.split("\n", 1)
        body = dong[0] + nhan + ("\n" + dong[1] if len(dong) > 1 else "")
    return ("\n".join(them) + "\n" + body) if them else body


def ngu_canh(pp: str, ket_qua: list[tuple[dict, float]], ngan_sach: int = ch.NGAN_SACH_NGU_CANH_TU,
             k: int = ch.K_UNG_VIEN) -> list[dict]:
    """Danh sách khối {so_hieu, text, start, end, doc_id, chunk_id, mo_rong, bi_cat, so_tu} đưa cho mô hình sinh.

    Chỉ một trường hợp có cắt (bi_cat=True, ghi lại để báo cáo): B+ khi khối ĐẦU TIÊN là một Điều dài hơn cả ngân
    sách — giữ cửa sổ đúng `ngan_sach` từ quanh chunk trúng (thiết kế của B+, không phải cắt ngầm)."""
    khoi, da, con = [], set(), ngan_sach
    for c, _ in ket_qua[:k]:
        if pp in MO_RONG_DIEU and c.get("dieu_start") is not None:
            key = (c["doc_id"], c["dieu_start"])
            if key in da:
                continue
            a, b = c["dieu_start"], c["dieu_end"]
            tt = _tien_to_dieu(c)
            t = vb(c["doc_id"])
            body, bi_cat = t[a:b], False
            if pp == "E2n":
                body = _gan_nhan_khoan(body, c.get("dieu_so"))
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
                if pp == "E2n":  # nhãn làm cửa sổ dài thêm vài từ so với ngân sách — ghi trong so_tu
                    body = _gan_nhan_khoan(body, c.get("dieu_so"))
            da.add(key)
            text = tt + "\n" + body
            khoi.append({"so_hieu": c["so_hieu"], "text": text, "start": a, "end": b, "doc_id": c["doc_id"],
                         "chunk_id": c["chunk_id"], "mo_rong": True, "bi_cat": bi_cat, "so_tu": len(text.split())})
        else:
            body = c["text"]
            if pp in ("E2", "E3", "E2n"):
                body = _bu_ngu_canh_e2(c, body)
            n = len(body.split())
            if n > con:
                break  # chunk kế tiếp không vừa ngân sách → dừng, không cắt dở
            khoi.append({"so_hieu": c["so_hieu"], "text": body, "start": c["start"], "end": c["end"],
                         "doc_id": c["doc_id"], "chunk_id": c["chunk_id"], "mo_rong": False, "bi_cat": False,
                         "so_tu": n})
        con -= khoi[-1]["so_tu"]
        if pp in ("E3", "E3b"):
            # Đơn vị đích của dẫn chiếu đặt NGAY SAU chunk dẫn, và được ưu tiên hơn chunk hạng
            # thấp hơn: ta đang duyệt theo thứ hạng, nên đích của chunk thứ i vào trước chunk
            # thứ i+1. Không bao giờ cắt dở một đơn vị đích — không vừa thì bỏ cả.
            from rag import dan_chieu
            for d in dan_chieu.keo(khoi[-1]["text"], c["doc_id"], c.get("dieu_so")):
                if d["so_tu"] > con:
                    dan_chieu.THONG_KE["bo_vi_het_ngan_sach"] += 1
                    continue
                khoi.append({"so_hieu": d["so_hieu"], "text": d["text"], "start": d["start"],
                             "end": d["end"], "doc_id": d["doc_id"], "chunk_id": f"dc:{d['nhan']}",
                             "mo_rong": False, "bi_cat": False, "so_tu": d["so_tu"],
                             "dan_chieu": d["loai"]})
                con -= d["so_tu"]
        if con <= 0:
            break
    return khoi
