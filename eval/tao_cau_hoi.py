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
                khoan = int(mk.group(1)) if mk else None
                cu = next((u for u in cm[goc_ho.doc_id]["khoan" if khoan else "dieu"]
                           if u.dieu == dieu and (khoan is None or u.khoan == khoan)), None)
                dv = next((u for u in sorted(cm[vb.doc_id]["diem"] + cm[vb.doc_id]["khoan"] + cm[vb.doc_id]["dieu"],
                                             key=lambda u: u.end - u.start)
                           if u.start <= vt < u.end and 8 <= so_tu(doan(vb, u)) <= 600), None)
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
            dau = _cau(docs[k].text, u.start, u.end)[:2]  # dòng tiêu đề + câu dẫn
            g = [_gold(x, "dich")]
            if len(dau) > 1 and so_tu(docs[k].text[dau[1][0]:dau[1][1]]) <= 60 and not re.match(r"\d+[.)]", docs[k].text[dau[1][0]:]):
                g.insert(0, _gold(DonVi(u.doc_id, u.so_hieu, u.dieu, None, None, dau[1][0], dau[1][1], u.b_parse_ok), "dan"))
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
    "dieu_dai": ("Đoạn DẪN là câu mở đầu của một điều rất dài; đoạn ĐÍCH là một khoản/điểm nằm sâu bên trong. Hỏi về "
                 "nội dung của đoạn ĐÍCH sao cho câu hỏi chỉ rõ nghĩa khi đặt trong ngữ cảnh của đoạn DẪN."),
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
            x.update({k: xong[x["qid"]][k] for k in ("question", "dap_an_nhap", "co")})
            continue
        r = cl.chat.completions.create(messages=tin_nhan(x, docs), model=sinh.tham_so()["model"], temperature=0,
                                       seed=42, max_tokens=300, extra_body={"cache_prompt": False},
                                       response_format={"type": "json_schema",
                                                        "json_schema": {"name": "cau_hoi", "schema": SCHEMA}})
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
    a = ap.parse_args()
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
    viet_cau_hoi(ds)
    from eval.duyet import xuat_duyet
    xuat_duyet()


if __name__ == "__main__":
    main()
