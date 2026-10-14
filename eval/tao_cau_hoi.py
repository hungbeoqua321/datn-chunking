"""Bước 4 — sinh NHÁP bộ câu hỏi: chương trình chọn đơn vị gold, mô hình sinh (tại chỗ) chỉ viết câu hỏi.

Gold lấy từ chỉ mục cấu trúc độc lập (eval/don_vi.py), ghi bằng vị trí ký tự; mô hình chỉ thấy đoạn văn bản gold
(không thấy ranh giới chunk hay tiền tố của bất kỳ phương pháp nào) và được dặn KHÔNG nhắc số hiệu, số Điều/khoản.

  loai           số câu  cách chọn gold
  don_gian         50    20 khoản ngẫu nhiên + 20 đoạn TRUNG LẬP (1–3 câu liên tiếp ở vị trí ngẫu nhiên trong một
                         khoản, không theo ranh giới cấu trúc) + 10 điều khoản ĐÃ SỬA ĐỔI trong họ phiên bản
                         (gold = bản hiện hành trong VBHN; phien_ban_cu = bản cũ trong văn bản gốc)
  xuyen_khoan      30    cùng một Điều: khoản quy tắc (vai dieu_kien) + khoản ngoại lệ có cụm "trừ trường hợp",
                         "không áp dụng"… (vai loai_tru); ghi cụm từ khoá của khoản loại trừ
  dan_chieu        25    khoản NGUỒN có "quy định tại khoản k Điều N" + Điều/khoản ĐÍCH cùng văn bản
  dieu_dai         20    trong Điều > 1500 từ: câu dẫn của Điều (vai dan) + khoản/điểm đích nằm sâu bên trong
  khong_co_dieu    15    một đoạn của văn bản không chia Điều
Thêm ~10% câu dự phòng (du_phong=true) để thay câu bị loại khi duyệt.

GOLD TRUNG LẬP (trung_lap=true) — gold cố ý KHÔNG trùng ranh giới cấu trúc, để B không thắng chỉ vì đáp án được định
nghĩa đúng bằng ranh giới chunk của nó: 1–3 câu liên tiếp mà câu đầu KHÔNG phải đầu một Điều/khoản/điểm/đoạn, có thể
kéo sang khoản kế. Ít nhất 45/140 câu, rải theo nhóm (TRUNG_LAP); báo cáo lấy tập này làm số chính.
    python -m eval.tao_cau_hoi --trung-lap   # bổ sung gold trung lập vào eval/gold.draft.jsonl đang có (giữ câu đã nháp)

    python -m eval.tao_cau_hoi --chon      # chỉ chọn gold → eval/gold.draft.jsonl (không cần LLM)
    python -m eval.tao_cau_hoi             # chọn gold (nếu chưa có) + gọi LLM viết câu hỏi → eval/questions.draft.jsonl
                                           #   (tiếp tục được nếu bị dừng giữa chừng) + eval/questions.review.md
"""
import argparse
import json
import random
import re
import time

import cau_hinh as ch
from chunking.base import nap_van_ban, so_tu
from eval.don_vi import DonVi, chi_muc
from rag import sinh

SEED = 2026
SO_CAU = {"don_gian_khoan": 20, "don_gian_trung_lap": 20, "don_gian_phien_ban": 10, "xuyen_khoan": 30,
          "dan_chieu": 25, "dieu_dai": 20, "khong_co_dieu": 15}
DU_PHONG = 0.1
from eval.duyet import CAN, TRUNG_LAP  # noqa: E402  (chỉ tiêu dùng chung với bước duyệt)
GOLD = ch.GOC / "eval/gold.draft.jsonl"
NHAP = ch.GOC / "eval/questions.draft.jsonl"
DUYET = ch.GOC / "eval/questions.review.md"

RE_NGOAI_LE = re.compile(r"\b(trừ trường hợp|trừ các trường hợp|không áp dụng|ngoại trừ|không bao gồm|"
                         r"không phải|không được|được miễn|không thuộc)\b", re.I)
RE_DAN_CHIEU = re.compile(r"(?:quy định tại|theo quy định tại|nêu tại|tại)\s+(?:(?:các\s+)?điểm\s+[a-zđ](?:,\s*[a-zđ])*"
                          r"(?:\s+và\s+[a-zđ])?\s+)?(?:khoản\s+(\d+)\s+)?Điều\s+(\d+)\b(?!\s+(?:của\s+)?(?:Luật|Bộ luật|"
                          r"Nghị định|Thông tư|Pháp lệnh|Nghị quyết|Quyết định)\s+(?!này))", re.I)
RE_SUA = re.compile(r"(?:Sửa đổi, bổ sung|Sửa đổi|Bổ sung|Thay thế)\s+(?:(?:điểm\s+([a-zđ])\s+)?khoản\s+(\d+)\s+)?"
                    r"Điều\s+(\d+)\b[^\n]*(?:như sau|sau đây)\s*:?\s*$", re.I)


def doan(doc, u: DonVi) -> str:
    return doc.text[u.start:u.end]


def _gold(u: DonVi, vai: str | None = None, **kw) -> dict:
    g = {"doc_id": u.doc_id, "so_hieu": u.so_hieu, "dieu": u.dieu, "khoan": u.khoan, "diem": u.diem,
         "start": u.start, "end": u.end}
    if vai:
        g["vai"] = vai
    g.update(kw)
    return g


def _cau(text: str, a: int, b: int) -> list[tuple[int, int]]:
    """Các câu trong text[a:b] (tách ở '. ', '; ', ':' cuối dòng và xuống dòng)."""
    ra, s = [], a
    for m in re.finditer(r"(?<=[.;:])\s+|\n", text[a:b]):
        e = a + m.start()
        if e > s:
            ra.append((s, e))
        s = a + m.end()
    if s < b:
        ra.append((s, b))
    return [(x, y) for x, y in ra if text[x:y].strip()]


def _ban_cu(cm_goc: dict, dv: DonVi) -> DonVi | None:
    """Bản cũ của đơn vị VBHN `dv` = đơn vị CÙNG SỐ Điều/khoản/điểm trong văn bản gốc (VBHN giữ nguyên cách đánh số của
    văn bản gốc). Trước đây lấy số Điều từ dòng "Sửa đổi… Điều N" của văn bản sửa đổi → ghép sai 9/11 cặp."""
    loai = "diem" if dv.diem else "khoan" if dv.khoan is not None else "dieu"
    return next((u for u in cm_goc[loai] if u.dieu == dv.dieu and u.khoan == dv.khoan and u.diem == dv.diem), None)


def chon_gold() -> list[dict]:
    rng = random.Random(SEED)
    docs = {d.doc_id: d for d in nap_van_ban()}
    cm = {k: chi_muc(d) for k, d in docs.items()}
    nhom = {k: d.nhom for k, d in docs.items()}
    goc = [k for k in docs if nhom[k] in ("luat", "nd_tt")]
    ds: list[dict] = []

    def can(k: str) -> int:
        return round(SO_CAU[k] * (1 + DU_PHONG))

    def ghi(loai, gold, nguon, **kw):
        ds.append({"loai": loai, "gold": gold, "nguon_chon": nguon, **kw})

    # don_gian — khoản ngẫu nhiên (≤ 1 câu/văn bản)
    kh = [u for k in goc for u in cm[k]["khoan"] if 25 <= so_tu(doan(docs[k], u)) <= 150 and u.diem is None]
    rng.shuffle(kh)
    da = set()
    for u in kh:
        if len([x for x in ds if x["nguon_chon"] == "khoan"]) >= can("don_gian_khoan"):
            break
        if u.doc_id in da:
            continue
        da.add(u.doc_id)
        ghi("don_gian", [_gold(u)], "khoan")
    # don_gian — đoạn trung lập: 1–3 câu liên tiếp ở vị trí ngẫu nhiên trong một khoản (bỏ qua ranh giới cấu trúc)
    kh2 = [u for k in goc for u in cm[k]["khoan"] if so_tu(doan(docs[k], u)) >= 40]
    rng.shuffle(kh2)
    for u in kh2:
        if len([x for x in ds if x["nguon_chon"] == "trung_lap"]) >= can("don_gian_trung_lap"):
            break
        cau = _cau(docs[u.doc_id].text, u.start, u.end)[1:]  # bỏ câu đầu (thường chứa số khoản)
        if not cau:
            continue
        i = rng.randrange(len(cau))
        j = min(len(cau), i + rng.randint(1, 3))
        a, b = cau[i][0], cau[j - 1][1]
        if not 15 <= so_tu(docs[u.doc_id].text[a:b]) <= 90:
            continue
        ghi("don_gian", [_gold(DonVi(u.doc_id, u.so_hieu, u.dieu, u.khoan, None, a, b, u.b_parse_ok))], "trung_lap")
    # don_gian — điều khoản đã sửa đổi (họ phiên bản): dòng "Sửa đổi/Bổ sung/Thay thế … (khoản k) (Điều N)" ngay trước
    # một đoạn trích dẫn "…"; Điều N không ghi trên dòng thì lấy từ dòng cha gần nhất có "Điều N". Chỉ giữ đoạn mới
    # TÌM THẤY trong VBHN của họ (tức là thuộc văn bản gốc của họ, không phải luật khác cùng bị sửa).
    for vb in [d for d in docs.values() if d.nhom == "vbhn"]:
        ho = [d for d in docs.values() if d.meta.get("ho") == vb.doc_id]
        goc_ho = next((d for d in ho if d.meta.get("vai_trong_ho") == "goc"), None)
        if not goc_ho:
            continue
        for sd in [d for d in ho if d.meta.get("vai_trong_ho") == "sua_doi"]:
            dong = sd.text.split("\n")
            dieu_cha = None
            for i, x in enumerate(dong[:-1]):
                md = re.search(r"Điều\s+(\d+)\b", x)
                if md and re.search(r"Sửa đổi|Bổ sung|Thay thế|sửa đổi|bổ sung", x) and not x.startswith('"'):
                    dieu_cha = int(md.group(1))
                if not (re.search(r"(Sửa đổi|Bổ sung|Thay thế|sửa đổi|bổ sung|thay thế)", x) and dong[i + 1].startswith('"')):
                    continue
                mk = re.search(r"khoản\s+(\d+)", x)
                dieu = int(md.group(1)) if md else dieu_cha
                moi = dong[i + 1].strip('"').strip()
                if dieu is None or so_tu(moi) < 8:
                    continue
                mau = " ".join(moi.split()[:10])
                vt = vb.text.find(mau)
                if vt < 0:
                    continue
                dv = next((u for u in sorted(cm[vb.doc_id]["diem"] + cm[vb.doc_id]["khoan"] + cm[vb.doc_id]["dieu"],
                                             key=lambda u: u.end - u.start)
                           if u.start <= vt < u.end and 8 <= so_tu(doan(vb, u)) <= 600), None)
                cu = _ban_cu(cm[goc_ho.doc_id], dv) if dv else None
                if not dv or not cu:
                    continue
                if " ".join(doan(goc_ho, cu).split()[:10]) == mau:  # bản cũ giống bản mới → không phải sửa nội dung
                    continue
                ghi("don_gian", [_gold(dv)], "phien_ban", phien_ban=True, phien_ban_cu=[_gold(cu)], sua_boi=sd.so_hieu)
    pb = [x for x in ds if x["nguon_chon"] == "phien_ban"]
    rng.shuffle(pb)
    ds = [x for x in ds if x["nguon_chon"] != "phien_ban"] + pb[:can("don_gian_phien_ban")]
    # xuyen_khoan — khoản quy tắc + khoản ngoại lệ trong cùng Điều
    xk = []
    for k in goc:
        theo_dieu: dict[int, list[DonVi]] = {}
        for u in cm[k]["khoan"]:
            theo_dieu.setdefault(u.dieu, []).append(u)
        for dieu, ks in theo_dieu.items():
            if len(ks) < 2:
                continue
            for j in ks[1:]:
                tj = doan(docs[k], j)
                m = RE_NGOAI_LE.search(tj)
                if not m or not 10 <= so_tu(tj) <= 160:
                    continue
                ref = re.search(r"khoản\s+(\d+)\s+Điều này", tj)
                i = next((u for u in ks if ref and u.khoan == int(ref.group(1)) and u.khoan != j.khoan), ks[0])
                if i.khoan == j.khoan or not 12 <= so_tu(doan(docs[k], i)) <= 220:
                    continue
                cau = next((docs[k].text[a:b] for a, b in _cau(docs[k].text, j.start, j.end) if RE_NGOAI_LE.search(docs[k].text[a:b])), "")
                dieu_u = next(u for u in cm[k]["dieu"] if u.dieu == dieu and u.start <= i.start < u.end)
                xk.append(([_gold(i, "dieu_kien"), _gold(j, "loai_tru", cum=m.group(0), cau_loai_tru=cau.strip())],
                           so_tu(doan(docs[k], dieu_u)) > ch.DIEU_TOI_DA))
                break
    rng.shuffle(xk)
    # cân bằng: một nửa từ Điều bị B tách (> 350 từ), một nửa Điều B giữ nguyên
    chia = [g for g, c in xk if c][:can("xuyen_khoan") // 2 + 1]
    giu = [g for g, c in xk if not c][:can("xuyen_khoan") - len(chia)]
    for g in chia + giu:
        ghi("xuyen_khoan", g, "ngoai_le")
    # dan_chieu — nguồn trỏ tới Điều khác trong cùng văn bản
    dc = []
    for k in goc:
        for u in cm[k]["khoan"] + [x for x in cm[k]["dieu"] if not any(y.dieu == x.dieu for y in cm[k]["khoan"])]:
            t = doan(docs[k], u)
            if not 15 <= so_tu(t) <= 200:
                continue
            for m in RE_DAN_CHIEU.finditer(t):
                kd, nd = (int(m.group(1)) if m.group(1) else None), int(m.group(2))
                if nd == u.dieu or abs(nd - u.dieu) < 2:
                    continue
                dich = next((x for x in cm[k]["khoan"] if x.dieu == nd and x.khoan == kd), None) if kd else \
                    next((x for x in cm[k]["dieu"] if x.dieu == nd), None)
                if not dich or not 15 <= so_tu(doan(docs[k], dich)) <= 300:
                    continue
                dc.append([_gold(u, "nguon", cum=m.group(0)), _gold(dich, "dich")])
                break
    rng.shuffle(dc)
    da = {}
    for g in dc:
        if len([x for x in ds if x["loai"] == "dan_chieu"]) >= can("dan_chieu"):
            break
        if da.get(g[0]["doc_id"], 0) >= 2:
            continue
        da[g[0]["doc_id"]] = da.get(g[0]["doc_id"], 0) + 1
        ghi("dan_chieu", g, "dan_chieu")
    # dieu_dai — câu dẫn + đơn vị đích nằm sâu trong Điều > 1500 từ
    dd = []
    for k in goc:
        for u in cm[k]["dieu"]:
            t = doan(docs[k], u)
            if so_tu(t) <= 1500:
                continue
            con = [x for x in cm[k]["diem"] + cm[k]["khoan"] if x.dieu == u.dieu and u.start <= x.start < u.end
                   and x.start - u.start > 0.4 * (u.end - u.start) and 12 <= so_tu(doan(docs[k], x)) <= 200]
            if not con:
                continue
            x = rng.choice(con)
            g = [_gold(x, "dich")]
            cd = cau_dan(docs[k].text, cm[k], u, x)
            if cd:
                g.insert(0, _gold(_don_vi_span(cm[k], u, *cd), "dan"))
            dd.append(g)
    rng.shuffle(dd)
    da = {}
    for g in dd:
        if len([x for x in ds if x["loai"] == "dieu_dai"]) >= can("dieu_dai"):
            break
        if da.get(g[-1]["doc_id"], 0) >= 3:
            continue
        da[g[-1]["doc_id"]] = da.get(g[-1]["doc_id"], 0) + 1
        ghi("dieu_dai", g, "dieu_dai")
    # khong_co_dieu — một đoạn
    kd = [u for k in docs if nhom[k] == "khong_dieu" for u in cm[k]["doan"] if 20 <= so_tu(doan(docs[k], u)) <= 150]
    rng.shuffle(kd)
    da = {}
    for u in kd:
        if len([x for x in ds if x["loai"] == "khong_co_dieu"]) >= can("khong_co_dieu"):
            break
        if da.get(u.doc_id, 0) >= 2:
            continue
        da[u.doc_id] = da.get(u.doc_id, 0) + 1
        ghi("khong_co_dieu", [_gold(u)], "doan")
    # đánh số, đánh dấu dự phòng (phần vượt số câu của đề trong mỗi nhóm con)
    dem: dict[str, int] = {}
    ra = []
    for x in ds:
        k = {"khoan": "don_gian_khoan", "trung_lap": "don_gian_trung_lap", "phien_ban": "don_gian_phien_ban"}.get(
            x["nguon_chon"], x["loai"])
        dem[k] = dem.get(k, 0) + 1
        x["du_phong"] = dem[k] > SO_CAU[k]
        x["b_parse_ok"] = all(g.get("b_parse_ok", True) is not False for g in x["gold"])
        ra.append(x)
    for i, x in enumerate(ra, 1):
        x["qid"] = f"q{i:03d}"
    return ra


# ── gold trung lập ───────────────────────────────────────────────────────────
def _dau_don_vi(cm_doc: dict) -> set[int]:
    return {u.start for t in ("dieu", "khoan", "diem", "doan") for u in cm_doc.get(t, [])}


RE_CHI_NHAN = re.compile(r"^\s*(?:Điều\s+\d+[a-zđ]?\s*[.:]?|\d+[a-zđ]?\s*[.)]|[a-zđ]\))?\s*$")


def _la_dau(text: str, x: int, dau: set[int]) -> bool:
    """x là đầu một Điều/khoản/điểm/đoạn — kể cả khi trước x trên cùng dòng chỉ có nhãn ("7. ", "a) ", "Điều 5."), hoặc x
    là đầu dòng nội dung đầu tiên sau tiêu đề Điều."""
    ld = text.rfind("\n", 0, x) + 1
    if x in dau or (ld in dau and bool(RE_CHI_NHAN.match(text[ld:x]))):
        return True
    # dòng nội dung đầu tiên ngay sau dòng tiêu đề "Điều N." cũng là đầu Điều (B cắt chunk đúng tại đây)
    dong_truoc = text[text.rfind("\n", 0, max(0, ld - 1)) + 1:max(0, ld - 1)]
    return bool(re.match(r"\s*Điều\s+\d+", dong_truoc)) and not text[ld:x].strip()


def cau_dan(text: str, cm_doc: dict, dieu: DonVi, dich: DonVi | None) -> tuple[int, int] | None:
    """Câu dẫn cho gold nhóm dieu_dai: đích là điểm → phần dẫn của khoản chứa nó (trước điểm đầu tiên, vd "Người lao
    động có các quyền sau đây:"); ngược lại → dòng dẫn ngay sau tiêu đề Điều nếu dòng đó không phải khoản. Không có → None.
    (KHÔNG lấy tên Điều: tên Điều nằm ở dòng tiêu đề, không phải câu dẫn.)"""
    if dich is not None and dich.diem is not None:
        kh = next((k for k in cm_doc["khoan"] if k.dieu == dieu.dieu and k.start <= dich.start < k.end), None)
        d1 = min((d.start for d in cm_doc["diem"] if kh and kh.start <= d.start < kh.end), default=None)
        if kh and d1 and 3 <= so_tu(text[kh.start:d1]) <= 60:
            a, b = kh.start, d1
            while b > a and text[b - 1].isspace():
                b -= 1
            return a, b
    ld = text.find("\n", dieu.start) + 1  # dòng ngay sau dòng tiêu đề Điều
    if 0 < ld < dieu.end:
        le = text.find("\n", ld)
        le = dieu.end if le < 0 or le > dieu.end else le
        dong = text[ld:le]
        if dong.strip() and not re.match(r"\s*(\d+[a-zđ]?[.)]|[a-zđ]\))\s", dong) and 3 <= so_tu(dong) <= 60:
            return ld, le
    return None


RE_TIEU_DE = re.compile(r"^\s*(?:Chương|CHƯƠNG|Mục|MỤC|Phần|PHẦN|Tiểu mục|Điều)\s+\S+")


def _la_tieu_de(t: str) -> bool:
    """Dòng tiêu đề Chương/Mục/Phần/Điều, hoặc dòng viết hoa toàn bộ (tên chương) — không phải nội dung quy định."""
    t = t.strip()
    return bool(RE_TIEU_DE.match(t)) or (t == t.upper() and any(c.isalpha() for c in t))


def span_trung_lap(text: str, a: int, b: int, dau: set[int], rng, can: re.Pattern | None = None,
                   so_cau: tuple = (1, 3), tu: tuple = (15, 90), tranh: list = ()) -> tuple[int, int] | None:
    """1–3 CÂU TRỌN (tách bằng bộ tách câu của C: ở . ? ! và xuống dòng — không tách ở ; :) liên tiếp trong text[a:b],
    câu đầu KHÔNG phải đầu một Điều/khoản/điểm/đoạn và mở đầu bằng chữ hoa (không phải mảnh câu); không chứa dòng tiêu
    đề; không kết thúc bằng câu dẫn có dấu hai chấm; có thể kéo sang đơn vị kế. `can`: span phải chứa cụm khớp; `tranh`: các span đã dùng, không được chồng lên."""
    from chunking.sentence import tach_cau

    cau = [(a + x, a + y) for x, y in tach_cau(text[a:b])]
    ung = []
    for i, (x, _) in enumerate(cau):
        if _la_dau(text, x, dau) or not text[x].isupper() or _la_tieu_de(text[x:cau[i][1]]):
            continue
        for n in range(so_cau[0], so_cau[1] + 1):
            if i + n > len(cau) or _la_tieu_de(text[cau[i + n - 1][0]:cau[i + n - 1][1]]):
                break
            y = cau[i + n - 1][1]
            if text[x:y].rstrip().endswith(":"):
                continue  # kết thúc bằng câu dẫn "…sau đây:" mà không có nội dung đi kèm
            if tu[0] <= so_tu(text[x:y]) <= tu[1] and (can is None or can.search(text[x:y])) \
                    and not any(p < y and x < q for p, q in tranh):
                ung.append((x, y))
    return rng.choice(ung) if ung else None


def _don_vi_span(cm_doc: dict, u: DonVi, x: int, y: int) -> DonVi:
    """Đơn vị gold cho span [x, y): nhãn khoản/điểm nơi span BẮT ĐẦU (khoan_den ghi riêng nếu span kéo sang khoản kế)."""
    kh = next((k for k in cm_doc["khoan"] if k.dieu == u.dieu and k.start <= x < k.end), None)
    di = next((k for k in cm_doc["diem"] if k.dieu == u.dieu and k.start <= x < k.end), None)
    return DonVi(u.doc_id, u.so_hieu, u.dieu, kh.khoan if kh else None, di.diem if di else None, x, y, u.b_parse_ok)


def chon_trung_lap(da_co: list[dict]) -> list[dict]:
    """Gold trung lập cho cả 5 nhóm (TRUNG_LAP câu + ~10% dự phòng mỗi nhóm)."""
    rng = random.Random(SEED + 1)
    docs = {d.doc_id: d for d in nap_van_ban()}
    cm = {k: chi_muc(d) for k, d in docs.items()}
    dau = {k: _dau_don_vi(cm[k]) for k in docs}
    goc = sorted(k for k in docs if docs[k].nhom in ("luat", "nd_tt"))
    dung: dict[str, list] = {}
    for x in da_co:
        for g in x["gold"]:
            dung.setdefault(g["doc_id"], []).append((g["start"], g["end"]))
    ra: list[dict] = []

    def them(loai, gold, nguon, toi_da_vb=2):
        dk = gold[-1]["doc_id"]
        if sum(1 for x in ra if x["loai"] == loai and x["gold"][-1]["doc_id"] == dk) >= toi_da_vb:
            return False
        ra.append({"loai": loai, "gold": gold, "nguon_chon": nguon, "trung_lap": True})
        for g in gold:
            dung.setdefault(g["doc_id"], []).append((g["start"], g["end"]))
        return True

    def du(loai):
        return sum(x["loai"] == loai for x in ra) >= TRUNG_LAP[loai] + max(1, round(TRUNG_LAP[loai] * DU_PHONG))

    # don_gian: 1–3 câu trong một Điều, câu đầu không phải đầu đơn vị (có thể kéo sang khoản kế); ≤ 1 câu/văn bản
    dieu_ds = [(k, u) for k in goc for u in cm[k]["dieu"] if so_tu(doan(docs[k], u)) >= 60]
    rng.shuffle(dieu_ds)
    for k, u in dieu_ds:
        if du("don_gian"):
            break
        sp = span_trung_lap(docs[k].text, u.start, u.end, dau[k], rng, tranh=dung.get(k, []))
        if sp:
            them("don_gian", [_gold(_don_vi_span(cm[k], u, *sp))], "trung_lap", toi_da_vb=1)
    # xuyen_khoan: câu quy tắc (không phải câu đầu khoản) + câu ngoại lệ chứa cụm loại trừ (không phải câu đầu khoản)
    cap = []
    for k in goc:
        theo: dict[int, list[DonVi]] = {}
        for u in cm[k]["khoan"]:
            theo.setdefault(u.dieu, []).append(u)
        for dieu, ks in theo.items():
            for j in ks[1:]:
                tj = doan(docs[k], j)
                if RE_NGOAI_LE.search(tj):
                    ref = re.search(r"khoản\s+(\d+)\s+Điều này", tj)
                    i = next((u for u in ks if ref and u.khoan == int(ref.group(1)) and u.khoan != j.khoan), ks[0])
                    if i.khoan != j.khoan:
                        cap.append((k, i, j))
    rng.shuffle(cap)
    for k, i, j in cap:
        if du("xuyen_khoan"):
            break
        t = docs[k].text
        sj = span_trung_lap(t, j.start, j.end, dau[k], rng, can=RE_NGOAI_LE, so_cau=(1, 2), tu=(8, 90), tranh=dung.get(k, []))
        si = span_trung_lap(t, i.start, i.end, dau[k], rng, so_cau=(1, 2), tu=(8, 90), tranh=dung.get(k, []))
        if not (si and sj):
            continue
        m = RE_NGOAI_LE.search(t[sj[0]:sj[1]])
        them("xuyen_khoan", [_gold(_don_vi_span(cm[k], i, *si), "dieu_kien"),
                             _gold(_don_vi_span(cm[k], j, *sj), "loai_tru", cum=m.group(0), cau_loai_tru=t[sj[0]:sj[1]].strip())],
             "ngoai_le")
    # dan_chieu: câu nguồn chứa dẫn chiếu (không phải câu đầu khoản) + 1–3 câu trong đơn vị đích (không phải câu đầu)
    nguon = []
    for k in goc:
        for u in cm[k]["khoan"] + [x for x in cm[k]["dieu"] if not any(y.dieu == x.dieu for y in cm[k]["khoan"])]:
            for m in RE_DAN_CHIEU.finditer(doan(docs[k], u)):
                kd, nd = (int(m.group(1)) if m.group(1) else None), int(m.group(2))
                if nd == u.dieu or abs(nd - u.dieu) < 2:
                    continue
                dich = next((x for x in cm[k]["khoan"] if x.dieu == nd and x.khoan == kd), None) if kd else \
                    next((x for x in cm[k]["dieu"] if x.dieu == nd), None)
                if dich and so_tu(doan(docs[k], dich)) >= 25:
                    nguon.append((k, u, m.group(0), dich))
    rng.shuffle(nguon)
    for k, u, cum, dich in nguon:
        if du("dan_chieu"):
            break
        t = docs[k].text
        sn = span_trung_lap(t, u.start, u.end, dau[k], rng, can=re.compile(re.escape(cum)), so_cau=(1, 2), tu=(10, 90),
                            tranh=dung.get(k, []))
        sd = span_trung_lap(t, dich.start, dich.end, dau[k], rng, tranh=dung.get(k, []))
        if sn and sd:
            them("dan_chieu", [_gold(_don_vi_span(cm[k], u, *sn), "nguon", cum=cum), _gold(_don_vi_span(cm[k], dich, *sd), "dich")],
                 "dan_chieu")
    # dieu_dai: câu dẫn của Điều > 1500 từ + 1–3 câu nằm sâu bên trong (sau 40% chiều dài), không phải câu đầu đơn vị
    dd = []
    for k in goc:
        for u in cm[k]["dieu"]:
            if so_tu(doan(docs[k], u)) > 1500:
                dd.append((k, u))
    rng.shuffle(dd)
    for k, u in dd * 3:
        if du("dieu_dai"):
            break
        t = docs[k].text
        sd = span_trung_lap(t, u.start + int(0.4 * (u.end - u.start)), u.end, dau[k], rng, tranh=dung.get(k, []))
        if not sd:
            continue
        dv = _don_vi_span(cm[k], u, *sd)
        g = [_gold(dv, "dich")]
        cd = cau_dan(t, cm[k], u, dv)
        if cd and not (cd[0] < sd[1] and sd[0] < cd[1]):
            g.insert(0, _gold(_don_vi_span(cm[k], u, *cd), "dan"))
        them("dieu_dai", g, "dieu_dai", toi_da_vb=3)
    # khong_co_dieu: 1–3 câu bắt đầu giữa một đoạn (có thể kéo sang đoạn kế)
    kd = sorted(k for k in docs if docs[k].nhom == "khong_dieu")
    rng.shuffle(kd)
    for k in kd * 3:
        if du("khong_co_dieu"):
            break
        t = docs[k].text
        than = min((u.start for u in cm[k].get("doan", []) if so_tu(doan(docs[k], u)) >= 20
                    and not t[u.start:u.start + 10].lstrip().startswith(("V/v", "Số:", "Kính gửi"))), default=None)
        if than is None:  # bỏ phần đầu văn bản (cơ quan, số, V/v, nơi gửi): bắt đầu từ đoạn thân đầu tiên ≥ 20 từ
            continue
        sp = span_trung_lap(t, than, len(t), dau[k], rng, tu=(20, 90), tranh=dung.get(k, []))
        if sp:
            them("khong_co_dieu", [_gold(DonVi(k, docs[k].so_hieu, None, None, None, *sp))], "doan")
    for loai in TRUNG_LAP:
        if loai != "don_gian" and sum(x["loai"] == loai for x in ra) < TRUNG_LAP[loai]:
            print(f"CẢNH BÁO: {loai} chỉ có {sum(x['loai'] == loai for x in ra)} gold trung lập")
    return ra


def bo_sung_trung_lap() -> None:
    """Sửa cơ cấu eval/gold.draft.jsonl theo TRUNG_LAP mà KHÔNG đụng câu đã nháp: đánh dấu gold trung lập sẵn có, bỏ gold
    có nhãn lấy từ dòng trong khối trích dẫn (chưa nháp), cắt bớt gold cấu trúc thừa (chưa nháp), thêm gold trung lập mới."""
    from chunking.structural import dong_trich_dan

    ds = [json.loads(x) for x in GOLD.read_text().splitlines() if x.strip()]
    da_nhap = {json.loads(x)["qid"] for x in NHAP.read_text().splitlines() if x.strip()} if NHAP.exists() else set()
    docs = {d.doc_id: d for d in nap_van_ban()}
    cm = {k: chi_muc(d) for k, d in docs.items()}
    dau = {k: _dau_don_vi(cm[k]) for k in docs}
    trich = {k: dong_trich_dan(d.text) for k, d in docs.items()}
    giu = []
    for x in ds:
        if "trung_lap" not in x:
            x["trung_lap"] = x["nguon_chon"] == "trung_lap" and not any(
                _la_dau(docs[g["doc_id"]].text, g["start"], dau[g["doc_id"]]) for g in x["gold"])
        sai_nhan = any(docs[g["doc_id"]].text.rfind("\n", 0, g["start"]) + 1 in trich[g["doc_id"]]
                       for g in x["gold"] if g.get("khoan") is not None or g.get("diem") is not None)
        if sai_nhan and x["qid"] not in da_nhap:
            print("bỏ (nhãn lấy từ dòng trong khối trích dẫn):", x["qid"])
            continue
        if x.get("phien_ban"):  # bản cũ ghép theo số Điều/khoản của gold trong văn bản gốc (sửa lỗi ghép sai)
            g, c = x["gold"][0], x["phien_ban_cu"][0]
            cu = _ban_cu(cm[c["doc_id"]], DonVi(g["doc_id"], g["so_hieu"], g["dieu"], g["khoan"], g["diem"], g["start"], g["end"]))
            if cu:
                x["phien_ban_cu"] = [_gold(cu)]
        if x["loai"] == "dieu_dai":  # câu dẫn cũ là TÊN Điều (lỗi) → tính lại, kể cả câu đã nháp (nháp dùng câu dẫn đúng)
            d = docs[x["gold"][-1]["doc_id"]]
            dich = x["gold"][-1]
            u = next(v for v in cm[d.doc_id]["dieu"] if v.dieu == dich["dieu"] and v.start <= dich["start"] < v.end)
            dv = DonVi(d.doc_id, d.so_hieu, dich["dieu"], dich["khoan"], dich["diem"], dich["start"], dich["end"])
            cd = cau_dan(d.text, cm[d.doc_id], u, dv)
            x["gold"] = ([_gold(_don_vi_span(cm[d.doc_id], u, *cd), "dan")] if cd else []) + [dich]
        giu.append(x)
    moi = chon_trung_lap(giu)
    so = max(int(q[1:]) for q in {x["qid"] for x in giu} | da_nhap)  # qid mới không trùng qid nháp cũ
    for i, x in enumerate(moi, so + 1):
        x["qid"] = f"q{i:03d}"
        x["b_parse_ok"] = all(g.get("b_parse_ok", True) is not False for g in x["gold"])
    ra = []
    for loai in CAN:
        tl = [x for x in giu + moi if x["loai"] == loai and x["trung_lap"]]
        ct = [x for x in giu if x["loai"] == loai and not x["trung_lap"]]
        if loai == "don_gian":  # 10 phiên bản + TRUNG_LAP trung lập + phần còn lại là gold cấu trúc đã nháp
            pb = [x for x in giu if x["loai"] == loai and x["nguon_chon"] == "phien_ban"]
            ct = [x for x in giu if x["loai"] == loai and not x["trung_lap"] and x["nguon_chon"] != "phien_ban"]
            can_ct = CAN[loai] - TRUNG_LAP[loai] - SO_CAU["don_gian_phien_ban"]
            for n, x in enumerate(pb):
                x["du_phong"] = n >= SO_CAU["don_gian_phien_ban"]
            for n, x in enumerate(ct):
                x["du_phong"] = n >= can_ct
            for n, x in enumerate(tl):
                x["du_phong"] = n >= TRUNG_LAP[loai]
            ra += ct + tl + pb
            continue
        can_ct = CAN[loai] - TRUNG_LAP[loai]
        du_ct = can_ct + max(1, round(can_ct * DU_PHONG))
        ct = [x for x in ct if x["qid"] in da_nhap] + [x for x in ct if x["qid"] not in da_nhap]
        ct = ct[:max(du_ct, sum(x["qid"] in da_nhap for x in ct))]
        for n, x in enumerate(ct):
            x["du_phong"] = n >= can_ct
        for n, x in enumerate(tl):
            x["du_phong"] = n >= TRUNG_LAP[loai]
        ra += ct + tl
    GOLD.write_text("\n".join(json.dumps(x, ensure_ascii=False) for x in ra) + "\n")
    for loai in CAN:
        x = [y for y in ra if y["loai"] == loai]
        print(f"{loai:14s} tổng {len(x):3d} | GIỮ {sum(not y['du_phong'] for y in x):3d} "
              f"(trung lập {sum(not y['du_phong'] and y['trung_lap'] for y in x)}) | dự phòng {sum(y['du_phong'] for y in x)}")


def sua_cau_dan() -> None:
    """Tính lại câu dẫn (vai dan) cho MỌI gold nhóm dieu_dai — lần dựng lại cơ cấu từ bản sao lưu đã bỏ qua câu đã nháp
    nên tên Điều cũ quay lại gold (câu hỏi được nháp với câu dẫn đúng). Sửa cả gold.draft.jsonl lẫn questions.draft.jsonl."""
    docs = {d.doc_id: d for d in nap_van_ban()}
    cm = {}
    for tep in (GOLD, NHAP):
        ds = [json.loads(x) for x in tep.read_text().splitlines() if x.strip()]
        for x in ds:
            if x["loai"] != "dieu_dai":
                continue
            dich = x["gold"][-1]
            d = docs[dich["doc_id"]]
            cm.setdefault(d.doc_id, chi_muc(d))
            u = next(v for v in cm[d.doc_id]["dieu"] if v.dieu == dich["dieu"] and v.start <= dich["start"] < v.end)
            dv = DonVi(d.doc_id, d.so_hieu, dich["dieu"], dich["khoan"], dich["diem"], dich["start"], dich["end"])
            cd = cau_dan(d.text, cm[d.doc_id], u, dv)
            if cd and (cd[0] < dich["end"] and dich["start"] < cd[1]):
                cd = None
            x["gold"] = ([_gold(_don_vi_span(cm[d.doc_id], u, *cd), "dan")] if cd else []) + [dich]
        tam = tep.with_suffix(".tmp")
        tam.write_text("\n".join(json.dumps(x, ensure_ascii=False) for x in ds) + "\n")
        tam.replace(tep)


def sua_cuoi_gold() -> None:
    """Cắt các dòng tiêu đề Chương/Mục/Phần dính ở CUỐI đơn vị gold (lỗi cũ của chỉ mục don_vi) — gold.draft + bản nháp."""
    from eval.don_vi import bo_tieu_de_cuoi

    docs = {d.doc_id: d for d in nap_van_ban()}
    for tep in (GOLD, NHAP):
        ds = [json.loads(x) for x in tep.read_text().splitlines() if x.strip()]
        n = 0
        for x in ds:
            for g in x["gold"] + x.get("phien_ban_cu", []):
                b = bo_tieu_de_cuoi(docs[g["doc_id"]].text, g["start"], g["end"])
                n += b != g["end"]
                g["end"] = b
        tam = tep.with_suffix(".tmp")
        tam.write_text("\n".join(json.dumps(x, ensure_ascii=False) for x in ds) + "\n")
        tam.replace(tep)
        print(f"{tep.name}: cắt đuôi tiêu đề ở {n} đơn vị gold")


def thay_trung_lap_loi() -> None:
    """Thay các gold trung lập CHƯA ĐẠT luật hiện hành của span_trung_lap (vd kết thúc bằng câu dẫn "…sau đây:" — luật
    thêm sau khi sàng lọc lượt 1) bằng gold mới cùng nhóm, giữ nguyên mọi câu khác và cờ dự phòng của câu bị thay."""
    ds = [json.loads(x) for x in GOLD.read_text().splitlines() if x.strip()]
    docs = {d.doc_id: d for d in nap_van_ban()}
    loi = [x for x in ds if x.get("trung_lap") and any(docs[g["doc_id"]].text[g["start"]:g["end"]].rstrip().endswith(":")
                                                       for g in x["gold"] if g.get("vai") != "dan")]
    giu = [x for x in ds if x not in loi]
    moi = chon_trung_lap(giu)
    da_nhap = {json.loads(x)["qid"] for x in NHAP.read_text().splitlines() if x.strip()} if NHAP.exists() else set()
    so = max(int(q[1:]) for q in {x["qid"] for x in ds} | da_nhap)
    ra = list(giu)
    for x in loi:
        y = next(z for z in moi if z["loai"] == x["loai"])
        moi.remove(y)
        so += 1
        y.update(qid=f"q{so:03d}", du_phong=x["du_phong"],
                 b_parse_ok=all(g.get("b_parse_ok", True) is not False for g in y["gold"]))
        cuoi = max(i for i, z in enumerate(ra) if z["loai"] == x["loai"])
        ra.insert(cuoi + 1, y)
        print(f"thay {x['qid']} ({x['loai']}) → {y['qid']}")
    GOLD.write_text("\n".join(json.dumps(x, ensure_ascii=False) for x in ra) + "\n")


# ── viết câu hỏi bằng mô hình sinh ──────────────────────────────────────────
HE_THONG_NHAP = (
    "Bạn soạn câu hỏi kiểm tra cho hệ thống hỏi đáp pháp luật Việt Nam. Viết MỘT câu hỏi tự nhiên bằng tiếng Việt, "
    "như người dân hoặc cán bộ thực sự hỏi, mà câu trả lời nằm trong (các) đoạn văn bản được cung cấp.\n"
    "Bắt buộc:\n"
    "- KHÔNG nhắc số hiệu văn bản, KHÔNG nhắc số Điều, số khoản, số điểm.\n"
    "- Không chép nguyên văn cả câu của đoạn văn bản; diễn đạt lại bằng lời thường.\n"
    "- Có thể nêu lĩnh vực/đối tượng (ví dụ: người lao động, doanh nghiệp, công chức) để câu hỏi rõ nghĩa.\n"
    "- Trả lời ở dạng JSON: {\"cau_hoi\": \"...\", \"dap_an\": \"câu trả lời ngắn dựa trên đoạn văn bản\"}."
)
YEU_CAU = {
    "khoan": "Hỏi về một nội dung cụ thể trong đoạn văn bản.",
    "trung_lap": "Hỏi về đúng nội dung của đoạn trích này (không hỏi về phần khác).",
    "phien_ban": "Hỏi về quy định HIỆN HÀNH trong đoạn văn bản này.",
    "ngoai_le": ("Câu hỏi phải buộc người trả lời dùng CẢ HAI đoạn: đoạn QUY TẮC và đoạn NGOẠI LỆ. Ví dụ dạng: "
                 "\"…có được … không, nếu thuộc trường hợp …?\" — câu trả lời đúng phải nêu cả quy tắc lẫn ngoại lệ."),
    "dan_chieu": ("Đoạn NGUỒN dẫn chiếu sang đoạn ĐÍCH. Hỏi về nội dung của đoạn NGUỒN sao cho muốn trả lời đầy đủ "
                  "phải đọc thêm đoạn ĐÍCH (ví dụ: điều kiện, thủ tục, mức cụ thể nằm ở đoạn ĐÍCH)."),
    "dieu_dai": ("Đoạn ĐÍCH nằm sâu bên trong một điều rất dài; đoạn DẪN (nếu có) là câu dẫn của điều hoặc của khoản chứa "
                 "đoạn ĐÍCH. Hỏi về nội dung của đoạn ĐÍCH; nếu có đoạn DẪN thì câu hỏi phải nêu điều kiện/đối tượng "
                 "lấy từ đoạn DẪN để rõ nghĩa."),
    "doan": "Hỏi về một nội dung cụ thể trong đoạn văn bản (văn bản hành chính, không chia Điều).",
}
TEN_VAI = {"dieu_kien": "ĐOẠN QUY TẮC", "loai_tru": "ĐOẠN NGOẠI LỆ", "nguon": "ĐOẠN NGUỒN", "dich": "ĐOẠN ĐÍCH",
           "dan": "ĐOẠN DẪN"}
SCHEMA = {"type": "object", "properties": {"cau_hoi": {"type": "string"}, "dap_an": {"type": "string"}},
          "required": ["cau_hoi", "dap_an"]}


def tin_nhan(x: dict, docs) -> list[dict]:
    d0 = docs[x["gold"][0]["doc_id"]]
    phan = [f"Văn bản: {d0.trich_yeu}"]
    for g in x["gold"]:
        t = docs[g["doc_id"]].text[g["start"]:g["end"]]
        phan.append(f"{TEN_VAI.get(g.get('vai'), 'ĐOẠN VĂN BẢN')}:\n{' '.join(t.split()[:400])}")
    phan.append("Yêu cầu: " + YEU_CAU[x["nguon_chon"]])
    return [{"role": "system", "content": HE_THONG_NHAP}, {"role": "user", "content": "\n\n".join(phan)}]


def co_ro_ri(x: dict, docs) -> list[str]:
    q = x.get("question") or ""
    co = []
    if re.search(r"\b(Điều|khoản|điểm)\s+\d", q, re.I):
        co.append("nhắc số Điều/khoản")
    if any(g["so_hieu"] and g["so_hieu"].split("/")[0] in q and g["so_hieu"] in q for g in x["gold"]):
        co.append("nhắc số hiệu")
    t = " ".join(docs[g["doc_id"]].text[g["start"]:g["end"]] for g in x["gold"]).lower().split()
    tq = q.lower().split()
    if tq:
        trung = sum(w in set(t) for w in tq) / len(tq)
        x["ti_le_trung_tu"] = round(trung, 3)
        if trung > 0.85:
            co.append(f"trùng từ cao ({trung:.0%})")
    return co


def viet_cau_hoi(ds: list[dict]) -> None:
    docs = {d.doc_id: d for d in nap_van_ban()}
    cl = sinh.client()
    xong = {}
    if NHAP.exists():
        xong = {y["qid"]: y for y in map(json.loads, NHAP.read_text().splitlines()) if y.get("question")}
    t0 = time.monotonic()
    for i, x in enumerate(ds, 1):
        if x["qid"] in xong:
            x.update({k: xong[x["qid"]][k] for k in ("question", "dap_an_nhap", "co", "san_loc") if k in xong[x["qid"]]})
            continue
        # qua sinh.goi: ghi nhật ký token + DỪNG nếu bị cắt (một nháp bị cắt sẽ thành JSON hỏng mà không ai biết)
        tu = sum(len(docs[g["doc_id"]].text[g["start"]:g["end"]].split()) for g in x["gold"])
        r, _ = sinh.goi(tin_nhan(x, docs), {"qid": x["qid"], "bien_the": "nhap_cau_hoi", "seed": 0,
                                           "so_khoi": len(x["gold"]), "so_tu_ngu_canh": tu}, cl,
                        model=sinh.tham_so()["model"], temperature=0, seed=42, max_tokens=300,
                        extra_body={"cache_prompt": False},
                        response_format={"type": "json_schema", "json_schema": {"name": "cau_hoi", "schema": SCHEMA}})
        try:
            o = json.loads(r.choices[0].message.content)
        except json.JSONDecodeError:
            o = {"cau_hoi": r.choices[0].message.content.strip(), "dap_an": ""}
        x["question"], x["dap_an_nhap"] = o.get("cau_hoi", "").strip(), o.get("dap_an", "").strip()
        x["co"] = co_ro_ri(x, docs)
        luu(ds[:i] + [y for y in ds[i:] if y["qid"] in xong])
        dt = time.monotonic() - t0
        print(f"{x['qid']} {x['loai']:13} {dt / i:5.0f}s/câu  {x['question'][:90]}", flush=True)
    luu(ds)


def luu(ds: list[dict]) -> None:
    tam = NHAP.with_suffix(".tmp")
    tam.write_text("\n".join(json.dumps(x, ensure_ascii=False) for x in ds) + "\n")
    tam.replace(NHAP)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--chon", action="store_true", help="chỉ chọn gold, không gọi LLM")
    ap.add_argument("--force", action="store_true", help="chọn lại gold từ đầu (xoá nháp cũ)")
    ap.add_argument("--trung-lap", action="store_true", help="bổ sung gold trung lập vào gold.draft.jsonl đang có rồi dừng")
    ap.add_argument("--thay-trung-lap-loi", action="store_true", help="thay gold trung lập chưa đạt luật hiện hành rồi dừng")
    ap.add_argument("--sua-cau-dan", action="store_true", help="tính lại câu dẫn của nhóm dieu_dai rồi dừng")
    ap.add_argument("--sua-cuoi-gold", action="store_true", help="cắt dòng tiêu đề dính ở cuối đơn vị gold rồi dừng")
    a = ap.parse_args()
    if a.sua_cuoi_gold:
        sua_cuoi_gold()
        return
    if a.sua_cau_dan:
        sua_cau_dan()
        return
    if a.thay_trung_lap_loi:
        thay_trung_lap_loi()
        return
    if a.trung_lap:
        bo_sung_trung_lap()
        return
    if a.force or not GOLD.exists():
        ds = chon_gold()
        GOLD.write_text("\n".join(json.dumps(x, ensure_ascii=False) for x in ds) + "\n")
        if a.force and NHAP.exists():
            NHAP.unlink()
    ds = [json.loads(x) for x in GOLD.read_text().splitlines() if x.strip()]
    dem: dict[str, int] = {}
    for x in ds:
        k = x["loai"] + ("" if not x["du_phong"] else "+dự_phòng")
        dem[k] = dem.get(k, 0) + 1
    print(len(ds), "gold:", dem)
    if a.chon:
        return
    try:
        viet_cau_hoi(ds)
    finally:
        sinh.xuat_thong_ke_token()
    from eval.duyet import xuat_duyet
    xuat_duyet()


if __name__ == "__main__":
    main()
