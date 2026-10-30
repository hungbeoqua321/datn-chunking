"""Bước 3 — phân tích lỗi trích dẫn của B và E2 (bộ chính, 110 câu, lượt local GPU).

Đọc chi_tiet_cau.jsonl do eval.bang_day_du ghi, xếp mỗi câu SAI (đúng toàn phần mức Điều = 0) vào đúng MỘT thùng,
theo thứ tự ưu tiên:

  T6 cắt trần            chạm MAX_TOKENS
  T1 truy hồi hụt        gold không nằm trọn trong 50 ứng viên
  T2 ngoài ngân sách     có trong 50 ứng viên nhưng không vào ngữ cảnh 1.200 từ
  T5 từ chối sai         gold trong ngữ cảnh mà mô hình từ chối (từ chối được tách khỏi T3)
  T4 dẫn sai             có trích dẫn, ít nhất một trích dẫn không phải gold
  T3 có mà không dẫn     gold trong ngữ cảnh, không trích dẫn sai nhưng thiếu gold (không trích, hoặc trích thiếu)

Ví dụ: ngữ cảnh dựng lại bằng truy_hoi.ngu_canh, so chunk_id với bản đã sinh (lệch thì DỪNG).

    python -m eval.phan_tich_loi        # → <KET_QUA_DIR>/phan_tich_loi.md
"""
import collections
import json
import time

import cau_hinh as ch
from chunking.base import nap_van_ban
from eval import cham, don_vi, trich_dan
from eval.cham_trich_dan import _SH_CHUNK, nap_so_hieu_chunk
from eval.chay_truy_hoi import _td_cho
from eval.sinh_day_du import PP_CHINH
from rag import truy_hoi
from rag.kiem_chi_muc import chot_chan

PPS = ["B", "E2"]
THUNG = {"T1": "truy hồi hụt", "T2": "ngoài ngân sách", "T3": "có mà không dẫn", "T4": "dẫn sai",
         "T5": "từ chối sai", "T6": "cắt trần"}
NHOM = ["don_gian", "dieu_dai", "xuyen_khoan", "khong_co_dieu", "dan_chieu"]


def thung(y: dict) -> str | None:
    if y["dieu_toan_phan"] == 1:
        return None
    if y["hang_muc"] == "cat_tran":
        return "T6"
    if y["trong_50"] < 1:
        return "T1"
    if y["trong_ngu_canh"] < 1:
        return "T2"
    if y["hang_muc"] == "tu_choi":
        return "T5"
    if y["co_trich"] and y["dieu_chinh_xac"] < 1:
        return "T4"
    return "T3"


def trich(r: dict) -> list[tuple]:
    mac_dinh = _SH_CHUNK.get((r.get("chunk_id") or [None])[0])
    return trich_dan.boc(r["tra_loi"] or "", mac_dinh=mac_dinh,
                         cho_phep_khong_dieu=any(g.get("dieu") is None for g in r["gold"]))


def khoa_gold(r):
    return {(trich_dan.khoa_tu_chuoi(g["so_hieu"]), g.get("dieu")) for g in r["gold"]}


def loai_t4(y, r) -> str:
    if any(g.get("dieu") is None for g in r["gold"]):
        return "bịa Điều cho văn bản không chia Điều"
    if y["dieu_phu"] == 1:
        return "dẫn thừa (đủ gold, thêm Điều khác)"
    g = khoa_gold(r)
    if any(d == gd and sh != gsh for sh, d, _, _ in trich(r) for gsh, gd in g):
        return "đúng số Điều, sai văn bản (bản hợp nhất / bản khác)"
    return "dẫn nhầm Điều"


def loai_t1(y) -> str:
    """Gold nhiều đơn vị là 'đủ cả' → một đơn vị hụt là hụt cả câu; tách: hụt hẳn / hụt một phần."""
    return "hụt một phần gold (≥ 1 đơn vị đã vào 50 ứng viên)" if y["hang_dau"] else "không đơn vị gold nào vào 50 ứng viên"


def cuu_duoc(y, r) -> dict:
    """Câu sẽ ĐÚNG nếu áp một cách sửa — ước lượng trên chính câu trả lời đã sinh (cận trên, không chạy lại)."""
    g = khoa_gold(r)
    t = list(dict.fromkeys((sh, d) for sh, d, _, _ in trich(r)))
    sh_gold = {sh for sh, _ in g}
    return {
        # văn bản không chia Điều: nếu chỉ ghi số hiệu (bỏ số Điều bịa) thì có đúng không
        "bo_dieu_bia": any(d is None for _, d in g) and bool(t) and {sh for sh, _ in t} == sh_gold,
        # chỉ giữ trích dẫn ĐẦU TIÊN
        "chi_dau": bool(t) and len(g) == 1 and t[0] in g,
        # chỉ giữ trích dẫn thuộc văn bản của khối đầu ngữ cảnh / văn bản gold — dùng cho dẫn thừa khác văn bản
        "loc_van_ban": bool(t) and {x for x in t if x[0] in sh_gold} == g and len(t) > len(g),
    }


def rut_gon(s: str, n: int) -> str:
    w = " ".join(s.split()).split(" ")
    return " ".join(w[:n]) + (" …" if len(w) > n else "")


def main() -> None:
    t0 = time.monotonic()
    idxs = sorted({truy_hoi.TEP.get(PP_CHINH[p], PP_CHINH[p]) for p in PPS})
    chot_chan(idxs)
    nap_so_hieu_chunk(idxs)
    ct = [json.loads(l) for l in open(ch.RESULTS / "chi_tiet_cau.jsonl", encoding="utf-8")]
    ct = {(y["qid"], y["pp"]): y for y in ct if y["bo"] == "chinh" and y["pp"] in PPS}
    tl = {(y["qid"], y["pp"]): y for y in map(json.loads, open(ch.RESULTS / "pilot_tra_loi.jsonl", encoding="utf-8"))}
    hoi = {x["qid"]: x for x in map(json.loads, open(ch.GOC / "eval/questions.jsonl", encoding="utf-8"))}
    qids = sorted(hoi)

    T = {k: thung(y) for k, y in ct.items()}
    md = ["# Phân tích lỗi trích dẫn — B và E2 (bộ chính 110 câu, lượt local GPU)", "",
          "Nguồn: `chi_tiet_cau.jsonl`, `pilot_tra_loi.jsonl` cùng thư mục (bước 1–2). Câu *sai* = đúng toàn phần mức "
          "Điều bằng 0. Mỗi câu sai vào đúng một thùng, xét theo thứ tự T6 → T1 → T2 → T5 → T4 → T3 (lỗi đầu chuỗi "
          "trước: đã không truy hồi được thì không xét trích dẫn). Bộ bóc trích dẫn là regex đã chốt (khớp 0,825 với "
          "120 nhãn tay), không sửa.", "",
          "| thùng | định nghĩa |", "|---|---|",
          "| T1 truy hồi hụt | gold không nằm trọn trong 50 ứng viên |",
          "| T2 ngoài ngân sách | có trong 50 ứng viên nhưng không vào ngữ cảnh 1.200 từ |",
          "| T3 có mà không dẫn | gold trong ngữ cảnh, không trích sai, nhưng thiếu gold |",
          "| T4 dẫn sai | có ít nhất một trích dẫn không phải gold |",
          "| T5 từ chối sai | gold trong ngữ cảnh mà mô hình từ chối |",
          "| T6 cắt trần | chạm 384 token |", "",
          "## 1. Bảng đếm", "",
          "| thùng | " + " | ".join(PPS) + " |", "|---|" + "---:|" * len(PPS)]
    for t in ["đúng"] + list(THUNG):
        md.append(f"| {t if t == 'đúng' else t + ' ' + THUNG[t]} | " + " | ".join(
            str(sum(1 for q in qids if (T[(q, p)] or "đúng") == t)) for p in PPS) + " |")
    md += ["", "### Theo nhóm (B / E2)", "",
           "| nhóm | n | " + " | ".join(THUNG) + " |", "|---|---:|" + "---|" * len(THUNG)]
    for g in NHOM:
        qs = [q for q in qids if hoi[q]["loai"] == g]
        md.append(f"| {g} | {len(qs)} | " + " | ".join(
            " / ".join(str(sum(1 for q in qs if T[(q, p)] == t)) for p in PPS) for t in THUNG) + " |")

    # T4 tách nhỏ
    md += ["", "### T4 tách nhỏ", "", "| loại | " + " | ".join(PPS) + " |", "|---|" + "---:|" * len(PPS)]
    l4 = {p: collections.Counter(loai_t4(ct[(q, p)], tl[(q, p)]) for q in qids if T[(q, p)] == "T4") for p in PPS}
    for k in sorted({k for c in l4.values() for k in c}):
        md.append(f"| {k} | " + " | ".join(str(l4[p][k]) for p in PPS) + " |")
    tu_doan = {p: sum(1 for q in qids if T[(q, p)] == "T4" and ct[(q, p)]["so_dieu_ngoai_ngu_canh"] > 0) for p in PPS}
    md.append(f"| *trong đó có ≥ 1 Điều không hề có trong ngữ cảnh (tự đoán)* | "
              + " | ".join(str(tu_doan[p]) for p in PPS) + " |")

    md += ["", "### T1 tách nhỏ", "", "| loại | " + " | ".join(PPS) + " |", "|---|" + "---:|" * len(PPS)]
    l1 = {p: collections.Counter(loai_t1(ct[(q, p)]) for q in qids if T[(q, p)] == "T1") for p in PPS}
    for k in sorted({k for c in l1.values() for k in c}):
        md.append(f"| {k} | " + " | ".join(str(l1[p][k]) for p in PPS) + " |")

    # B ↔ E2: câu chuyển thùng
    chuyen = collections.Counter((T[(q, "B")] or "đúng", T[(q, "E2")] or "đúng") for q in qids
                                 if T[(q, "B")] != T[(q, "E2")])
    md += ["", "### Câu đổi thùng giữa B và E2", "", "| B → E2 | số câu |", "|---|---:|"]
    md += [f"| {a} → {b} | {n} |" for (a, b), n in chuyen.most_common()]

    # ---- ví dụ
    docs = nap_van_ban()
    van_ban = {d.doc_id: d.text for d in docs}
    so_hieu = {d.doc_id: d.so_hieu for d in docs}
    cap = cham.doc_cap()
    dv = {d.doc_id: (lambda ci: ci["dieu"] + ci["khoan"] + ci["diem"] + ci["doan"])(don_vi.chi_muc(d))
          for d in docs if d.so_hieu in cap}
    md += ["", "## 2. Ví dụ thật — 3 câu mỗi thùng", "",
           "Ngữ cảnh rút gọn: mỗi khối = số hiệu + 30 từ đầu; ★ = khối chạm gold (độ phủ ≥ τ = 0,5). "
           "Lý do: tự động từ số liệu, kèm nhận xét đọc tay."]
    vec = {}
    for t in THUNG:
        ung = [(q, p) for p in PPS for q in qids if T[(q, p)] == t]
        # ưu tiên đa dạng: xen kẽ B và E2, khác qid, khác nhóm
        chon, da_q, da_nhom = [], set(), collections.Counter()
        for q, p in sorted(ung, key=lambda k: (da_nhom[hoi[k[0]]["loai"]], k[1] != "B", k[0])):
            if q in da_q or len(chon) == 3:
                continue
            chon.append((q, p)); da_q.add(q); da_nhom[hoi[q]["loai"]] += 1
        md += ["", f"### {t} — {THUNG[t]} ({len(ung)} lượt: "
               + ", ".join(f"{p} {sum(1 for _, pp in ung if pp == p)}" for p in PPS) + ")"]
        if not chon:
            md.append("\n*(không có câu nào)*")
        for q, p in chon:
            x, y, r = hoi[q], ct[(q, p)], tl[(q, p)]
            if q not in vec:
                vec[q] = truy_hoi.nhung_cau_hoi(x["question"])
            idx = PP_CHINH[p]
            kq_d = truy_hoi.tim(idx, vec[q], k=ch.K_UNG_VIEN)
            khoi = truy_hoi.ngu_canh(idx, kq_d, ngan_sach=ch.NGAN_SACH_NGU_CANH_TU, k=ch.K_UNG_VIEN)
            if [b["chunk_id"] for b in khoi] != r["chunk_id"]:
                raise SystemExit(f"LỆCH NGỮ CẢNH {q}/{p} — DỪNG.")
            td = _td_cho(x["gold"], van_ban, so_hieu, dv, cap, bool(x.get("phien_ban")))
            sao = [any(cham.do_phu(g, [b], td.get(j)) >= cham.TAU for j, g in enumerate(x["gold"])) for b in khoi]
            tr = trich(r)
            gold = "; ".join(f"{g['so_hieu']} Điều {g['dieu']}" + (f" khoản {g['khoan']}" if g.get("khoan") else "")
                             if g.get("dieu") else f"{g['so_hieu']} (không chia Điều)" for g in x["gold"])
            ly = {"T1": f"chunk gold đầu tiên ở hạng {y['hang_dau'] or '> 50'}; độ phủ gold trong 50 ứng viên "
                        f"{y['trong_50']:.2f}",
                  "T2": f"chunk gold đầu tiên ở hạng {y['hang_dau'] or '— (gold rải nhiều chunk, không chunk nào ≥ τ)'}; "
                        f"ngữ cảnh {y['so_khoi']} khối / "
                        f"{y['so_tu_ngu_canh']} từ đã đầy trước khi tới",
                  "T6": "chạm 384 token khi đang trả lời",
                  "T5": f"gold ở khối #{sao.index(True) + 1 if True in sao else '?'} nhưng mô hình từ chối",
                  }.get(t, f"gold ở khối #{sao.index(True) + 1 if True in sao else '?'} / {len(khoi)}; "
                           f"độ phủ {y['dieu_phu']:.2f}, độ chính xác {y['dieu_chinh_xac']:.2f}"
                        + (f"; {loai_t4(y, r)}" if t == "T4" else "")
                        + (f"; {y['so_dieu_ngoai_ngu_canh']} Điều trích không có trong ngữ cảnh"
                           if y["so_dieu_ngoai_ngu_canh"] else ""))
            md += ["", f"**{q} · {p} · {x['loai']}** — {x['question']}", "",
                   f"- gold: {gold}",
                   "- ngữ cảnh: " + " ‖ ".join(f"{'★' if s else ''}#{i + 1} [{b['so_hieu']}] {rut_gon(b['text'], 30)}"
                                                for i, (b, s) in enumerate(zip(khoi, sao))),
                   f"- trả lời: {rut_gon(r['tra_loi'] or '(rỗng)', 80)}",
                   f"- trích bóc được: " + (", ".join(f"Điều {d}" + (f" khoản {k}" if k else "") if d else "(chỉ số hiệu)"
                                                    for _, d, k, _ in tr) or "(không có)"),
                   f"- lý do: {ly}"]

    # ---- cải tiến
    cuu = {p: collections.Counter() for p in PPS}
    for p in PPS:
        for q in qids:
            if T[(q, p)] in ("T3", "T4"):
                for k, v in cuu_duoc(ct[(q, p)], tl[(q, p)]).items():
                    cuu[p][k] += v
    dem = {p: collections.Counter(T[(q, p)] for q in qids) for p in PPS}
    hd_t2 = {p: sorted((ct[(q, p)]["hang_dau"] or 999) for q in qids if T[(q, p)] == "T2") for p in PPS}
    md += ["", "## 3. Số liệu cho bảng cải tiến", "",
           "Ước lượng *trên chính câu trả lời đã sinh* (không chạy lại) — là cận trên vì đổi lời nhắc có thể làm hỏng câu "
           "đang đúng.", "",
           "| đo | " + " | ".join(PPS) + " |", "|---|" + "---:|" * len(PPS),
           "| T4 văn bản không chia Điều: bỏ số Điều bịa thì đúng | " + " | ".join(str(cuu[p]["bo_dieu_bia"]) for p in PPS) + " |",
           "| T3/T4: chỉ giữ trích dẫn đầu tiên thì đúng (gold 1 đơn vị) | " + " | ".join(str(cuu[p]["chi_dau"]) for p in PPS) + " |",
           "| T3/T4: bỏ trích dẫn của văn bản không phải gold thì đúng | " + " | ".join(str(cuu[p]["loc_van_ban"]) for p in PPS) + " |",
           "| T2: hạng chunk gold đầu tiên (999 = gold rải nhiều chunk, không chunk nào ≥ τ) | " + " | ".join(str(hd_t2[p]) for p in PPS) + " |",
           "| T1 / T5 / T6 | " + " | ".join(f"{dem[p]['T1']} / {dem[p]['T5']} / {dem[p]['T6']}" for p in PPS) + " |"]
    sai_e2 = [q for q in qids if T[(q, "B")] is None and T[(q, "E2")] == "T4"]
    t2_gan = {p: sum(1 for h in hd_t2[p] if h <= 6) for p in PPS}
    md += ["", "## 4. Nhận xét (đọc tay các ví dụ trên)", "",
           f"- **T4 là thùng lớn nhất** (B {dem['B']['T4']}, E2 {dem['E2']['T4']}), và gần một nửa không phải lỗi hiểu "
           f"luật: ở nhóm `khong_co_dieu` mô hình **bịa số Điều** cho văn bản vốn không chia Điều (thông báo, chỉ thị) — "
           f"q139 \"Điều 5 khoản 2 của 05/TB-VPCP\". Nội dung trả lời thường đúng; chỉ cần bỏ số Điều là khớp gold "
           f"({cuu['B']['bo_dieu_bia']} câu B, {cuu['E2']['bo_dieu_bia']} câu E2). Đây là lý do cả 8 phương pháp đều "
           "0,000 ở nhóm này (bảng 2 của metrics_trich_dan.md).",
           "- **Dẫn thừa**: mô hình dẫn thêm Điều ở văn bản khác có trong ngữ cảnh (q003 dẫn cả Điều 467 BLTTHS và "
           "Điều 387 BLTTDS bên cạnh Điều 139 Luật TCTAND đúng). Tiêu chí chính *khớp hoàn toàn* phạt mọi trích dẫn thừa (cột phụ *đủ gold* thì không).",
           f"- **E2 thua B chủ yếu vì mở rộng Điều**: {len(sai_e2)} câu B đúng mà E2 rơi vào T4, gần hết là *dẫn nhầm "
           "Điều*. Khối mở rộng lên cả Điều dài làm ngữ cảnh còn 1–2 khối; nhãn \"Điều N\" chỉ ở đầu khối nên mô hình "
           "gán khoản sang Điều khác hoặc lấy số khoản làm số Điều (q120: gold Điều 89 khoản 6 → E2 dẫn \"Điều 6\"; "
           "q039: Điều 46 khoản 3 → \"Điều 3 khoản 3\"). Đây là vấn đề *nhãn trong ngữ cảnh*, không phải truy hồi "
           "(R@5 của E2 = B).",
           "- **Đúng số Điều, sai văn bản**: dẫn bản khác của cùng văn bản. Từ 30/10 bảng cặp tương đương được áp ở tầng "
           "trích dẫn, nên q010 (dẫn 83/2026/VBHN-TT-BXD thay 03/2020/TT-BXD, cùng Điều 2 khoản 1) nay tính là đúng; "
           "các ca còn lại ở thùng này là câu phiên bản (không áp bảng cặp) hoặc cặp văn bản ngoài bảng.",
           "- **T1 đều là hụt một phần** gold nhiều đơn vị: một đơn vị vào 50 ứng viên, đơn vị kia (thường là đích dẫn "
           "chiếu, nhóm `dan_chieu`) thì không. Riêng q127 (và q122, cùng dạng): gold có một đơn vị cấp Điều mà span là "
           "**câu dẫn** \"Trong Luật này, các từ ngữ dưới đây được hiểu như sau:\" (12 từ, KHÔNG phải cả Điều — bản trước "
           "ghi sai, xem `results/nhat_ky_sua_loi.md` 30/10). Câu dẫn nằm trong chunk \"Điều 3 … Khoản 1\", chunk đó "
           "đứng hạng 779 (q122: 2.156) nên không vào 50 ứng viên.",
           f"- **T2**: chunk gold đầu tiên ở hạng ≤ 6 ở {t2_gan['B']}/{dem['B']['T2']} câu B — phần lớn là gold nhiều "
           "đơn vị, một đơn vị đã vào ngữ cảnh, đơn vị kia nằm ngoài 1.200 từ.",
           "- **T5, T6 nhỏ**. q021 cắt trần ở cả 8 phương pháp (câu trả lời liệt kê dài, chạm 384 token) — lỗi của câu "
           "hỏi chứ không của phương pháp.",
           "", "## 5. Cải tiến — xếp theo số câu kỳ vọng cứu được", "",
           "Số câu: cận trên ước trên câu trả lời đã sinh (mục 3), B / E2. Regex chấm **không đổi**. Sau khi duyệt "
           "(30/10): giữ #1, #2, #3 làm thử nghiệm ở bước 4 (`results/local_gpu/thu_them.md`, mỗi mục có kiểm soát chạy "
           "cùng lượt); #6 xử lý bằng sửa bộ chấm; **bỏ** bốn đề xuất cũ: chỉ dẫn đơn vị trực tiếp trả lời (dẫn thừa), "
           "E3 + rerank, MAX_TOKENS 512, lời nhắc bớt thận trọng.", "",
           "| # | thùng | cách sửa | câu kỳ vọng (B / E2) | chi phí | rủi ro với tính công bằng | trạng thái |",
           "|---:|---|---|---|---|---|---|",
           f"| 1 | T4 bịa Điều | Lời nhắc P1: \"đoạn không có 'Điều' thì chỉ ghi số hiệu, không tự đặt số Điều\" "
           f"| ≤ {cuu['B']['bo_dieu_bia']} / ≤ {cuu['E2']['bo_dieu_bia']} | 1 dòng lời nhắc; sinh lại cả 8 phương pháp "
           "| Trung bình: C và D sẽ bớt *tự đoán* — báo trước/sau P1 cho C và D ở nhóm `khong_co_dieu` "
           "| thử nghiệm 4.5: P1 × 8 phương pháp, kiểm soát lời nhắc gốc cùng lượt |",
           f"| 2 | T4 dẫn nhầm sau mở rộng | Tầng sinh: gắn lại nhãn \"(Điều N khoản k)\" ở đầu mỗi khoản trong khối mở "
           f"rộng (không đụng chuỗi nhúng) | 0 / ≤ {len(sai_e2)} | ~20 dòng ở `truy_hoi.ngu_canh` "
           "| Thấp: biến thể riêng E2n, E2 không đổi | thử nghiệm 4.5: E2n so với kiểm soát E2 |",
           f"| 3 | T2 ngoài ngân sách | Ngân sách 600 / 1.200 / 1.800 / 2.400 từ | ≤ {dem['B']['T2']} / ≤ {dem['E2']['T2']} "
           "| 2.400 từ vượt n_ctx 4096 → nâng n_ctx 8192 **chỉ cho lượt 2.400 từ** | Thấp nếu mọi phương pháp cùng ngân "
           "sách | thử nghiệm 4.2 |",
           "| 6 | T4 sai văn bản | Áp bảng cặp tương đương **đã chốt** (`eval/cap_tuong_duong.csv`) ở tầng trích dẫn như "
           "tầng truy hồi; câu phiên bản không áp | đã áp: B +1, E2 +1 (q010) | 0 | Thấp: luật tương đương có từ trước, đã "
           "ghi trong `eval/cham.py` là dùng cho cả hai tầng; trước 30/10 tầng trích dẫn bỏ sót — đây là sửa lỗi cài đặt, "
           "không phải luật mới | đã làm (`results/nhat_ky_sua_loi.md`) |"]
    md += ["", f"Thời gian chạy: {time.monotonic() - t0:.0f} s."]
    (ch.RESULTS / "phan_tich_loi.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
