"""In các khối số cho quyển — TỪ BỘ LOCAL (results/local_gpu), bộ VPS chỉ dùng để kiểm chứng tái lập.

Định dạng do người viết quyển chốt: dấu phẩy thập phân, ba chữ số, khoảng tin cậy [a; b], tên file nguồn dưới mỗi
khối, số chưa có ghi "chưa chạy".

    python -m eval.khoi_so            # → results/local_gpu/khoi_so.md (và in ra)

Khối 0 môi trường · 1 thống kê chunk · 2 bộ câu hỏi · 3 kiểm regex · 4 truy hồi 110 câu · 5 trích dẫn 110 câu ·
6 manh_con · 7 dẫn chiếu 26/9 câu · 8 nhiễu bản cũ · 9 thử thêm (bước 4).
"""
import collections
import json
import math
import statistics as st
from types import SimpleNamespace

import cau_hinh as ch
from chunking import hybrid
from chunking.base import nap_van_ban
from chunking.stats import do_phu
from eval import ap_nhan, cham, don_vi, pilot
from eval.bang_day_du import BO, ban_cu, bs, cham_bo, tb
from eval.cham_trich_dan import nap_so_hieu_chunk
from rag import dan_chieu, truy_hoi
from rag.kiem_chi_muc import chot_chan

RA = ch.RESULTS / "khoi_so.md"
CHUA = "chưa chạy"
NHOM = ("don_gian", "dieu_dai", "xuyen_khoan", "khong_co_dieu", "dan_chieu")
PP8 = ("A", "C", "D", "B", "B+", "E", "E2", "E3")


# ── định dạng ────────────────────────────────────────────────────────────────────────────────────────────────
def s3(x) -> str:
    if x is None or x != x:
        return CHUA
    return f"{x:.3f}".replace(".", ",")


def d3(x) -> str:
    return f"{x:+.3f}".replace(".", ",")


def ci(h) -> str:
    """Hiệu [a; b]; đậm khi khoảng tin cậy không chứa 0."""
    if h is None or h[0] != h[0]:
        return CHUA
    s = f"{d3(h[0])} [{d3(h[1])}; {d3(h[2])}]"
    return f"**{s}**" if h[1] > 0 or h[2] < 0 else s


def so(n) -> str:
    return f"{n:,}".replace(",", ".")


def pt(k, n) -> str:
    return f"{k / n * 100:.1f}%".replace(".", ",") if n else CHUA


def nguon(*ten) -> list[str]:
    return ["", "Nguồn: " + ", ".join(f"`{t}`" for t in ten), ""]


def hm(rows, p) -> str:
    c = collections.Counter(r["hang_muc"] for r in rows if r["pp"] == p)
    return f"{c['dat']} / {c['tu_choi']} / {c['cat_tran']}" if c else CHUA


def wilson(k, n, z=1.96):
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (c - h) / d, (c + h) / d


def _nap(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()] if p.exists() else []


# ── khối 1 ───────────────────────────────────────────────────────────────────────────────────────────────────
SAU_BO = {"A": "A_s0", "C": "C_s0", "D": "D_s0", "B (cũng là B+)": "B_s0", "E (Eduoi)": "Eduoi_s0",
          "E2 / E3 (Echi_s)": "Echi_s_s0"}


def khoi1(docs) -> list[str]:
    L = ["## Khối 1 — Thống kê chunk sáu phương pháp", "",
         "Sáu bộ chunk khác nhau đứng sau tám phương pháp sinh (B+ dùng chunk B; E3 dùng chunk Echi_s). 80 văn bản, "
         "seed 0. Số từ tính trên phần nội dung, không tính tiền tố. *Dưới sàn* = < 50 từ; *vượt trần* = > 350 từ "
         "(ngưỡng tách của B); *ký tự mất* = ký tự không trắng của văn bản không thuộc chunk nào.", "",
         "| phương pháp | số chunk | trung vị từ | dài nhất | ngắn nhất | dưới sàn | vượt trần | ký tự mất |",
         "|---|---:|---:|---:|---:|---:|---:|---:|"]
    for ten, tep in SAU_BO.items():
        cs = _nap(ch.CHUNKS / f"{tep}.jsonl")
        n = [c["n_words"] for c in cs]
        _, mat = do_phu(docs, [SimpleNamespace(**c) for c in cs])
        L.append(f"| {ten} | {so(len(cs))} | {st.median(n):.0f} | {max(n)} | {min(n)} "
                 f"| {so(sum(x < 50 for x in n))} | {so(sum(x > 350 for x in n))} | {so(mat)} |")
    n_tc = sum(len(hybrid._don_vi_tang_cuoi(d)) for d in docs)
    L += ["", "| chỉ số riêng | giá trị |", "|---|---:|",
          f"| số đơn vị tầng cuối của E (phải cắt ngữ nghĩa có chặn) | {so(n_tc)} |",
          "| số chunk B mất câu dẫn phần thân | 2.013 / 12.718 (15,8%) |",
          "| nhãn Điều sai của B, văn bản sửa đổi — trước / sau xử lý khối trích dẫn | 35,7% / 1,5% (4/272) |",
          "| nhãn Điều sai của B, VBHN — trước / sau xử lý văn bản kèm theo | 11,7% (43/368) / 3,2% (11/343) |",
          "| tiêu đề Điều vỡ khi crawl thô, 212 văn bản ứng viên — trước / sau chuẩn hoá | 30 / 10.892 (0,28%) / 0 |"]
    return L + nguon(*(f"{ch.CHUNKS.as_posix()}/{t}.jsonl" for t in SAU_BO.values()),
                     "results/phuong_phap_E_bu_ngu_canh.md §1", "results/buoc3/thong_ke_chunk.md",
                     "results/buoc2/thong_ke_du_lieu.md") \
        + ["Bộ chunk local trùng tuyệt đối bộ VPS (20/20 tệp, `thuc_nghiem/tai_lap_gpu/van_chunk.md`), nên các chỉ "
           "số mức kho ở bảng dưới lấy thẳng từ báo cáo dữ liệu.", ""]


# ── khối 2 ───────────────────────────────────────────────────────────────────────────────────────────────────
def khoi2(hoi, mc) -> list[str]:
    L = ["## Khối 2 — Bộ câu hỏi", "", "| nhóm | số câu | gold trung lập | gold trùng ranh giới |", "|---|---:|---:|---:|"]
    for g in NHOM:
        x = [q for q in hoi if q["loai"] == g]
        L.append(f"| {g} | {len(x)} | {sum(bool(q.get('trung_lap')) for q in x)} "
                 f"| {sum(not q.get('trung_lap') for q in x)} |")
    L.append(f"| **tổng** | **{len(hoi)}** | **{sum(bool(q.get('trung_lap')) for q in hoi)}** "
             f"| **{sum(not q.get('trung_lap') for q in hoi)}** |")
    from eval.chay_truy_hoi import BAN_CU_NHIEU
    q_ids = {q["qid"] for q in hoi}
    L += ["", "| bộ / tập con | số câu |", "|---|---:|",
          f"| manh_con (đo E) | {len(mc)} |",
          f"| manh_con — tập mất câu dẫn | {sum(bool(q.get('tap_mat_cau_dan')) for q in mc)} |",
          f"| manh_con — tập tầng cuối | {sum(bool(q.get('tap_tang_cuoi')) for q in mc)} |",
          f"| câu dính bản cũ — tập phiên bản (bản cũ trong bảng tương đương) | {sum(bool(q.get('phien_ban')) for q in hoi)} |",
          f"| câu dính bản cũ — tập nhiễu (bản cũ ngoài bảng tương đương) | {sum(q in q_ids for q in BAN_CU_NHIEU)} |"]
    return L + nguon("eval/questions.jsonl", "eval/manh_con.draft.jsonl", "eval/chay_truy_hoi.py (BAN_CU_NHIEU)")


# ── khối 3 ───────────────────────────────────────────────────────────────────────────────────────────────────
def khoi3() -> list[str]:
    cu, _ = ap_nhan.doc_nhan(ch.GOC / "nhan_120.txt")
    moi = {"A": (32, 7, 1, 0), "B": (34, 6, 0, 0), "B+": (33, 5, 1, 1)}  # vòng hai, results/kiem_regex_trich_dan.md
    import os
    luu = os.environ.get("KET_QUA_DIR")
    os.environ.pop("KET_QUA_DIR", None)          # nhãn gắn trên câu trả lời VPS (results/pilot_tra_loi.jsonl)
    try:
        import importlib
        importlib.reload(ch)
        chon, _, _ = pilot.chon_dong(ghi_giai_ma=False)
    finally:
        if luu is not None:
            os.environ["KET_QUA_DIR"] = luu
        importlib.reload(ch)
    dem = collections.defaultdict(collections.Counter)
    for i, r in enumerate(chon, 1):
        if f"{i:03d}" in cu:
            dem[r["pp"]][cu[f"{i:03d}"][1]] += 1
    L = ["## Khối 3 — Kiểm regex bóc trích dẫn", "",
         "**Dùng lại 120 nhãn** tay (40 dòng mỗi biến thể A, B, B+), gắn trên câu trả lời VPS; regex không đổi từ "
         "đó, lượt local chấm bằng đúng regex này. Độ khớp = tỉ lệ dòng người đọc chấm Đúng; khoảng tin cậy Wilson 95%.",
         "", "| biến thể | n | độ khớp trước sửa | Wilson 95% | độ khớp sau sửa | Wilson 95% |",
         "|---|---:|---:|---|---:|---|"]
    tc, tm = collections.Counter(), collections.Counter()
    for pp in ("A", "B", "B+"):
        c, (d, th, tu, sa) = dem[pp], moi[pp]
        n = sum(c.values())
        tc.update(c)
        tm.update({"Đúng": d, "Thiếu": th, "Thừa": tu, "Sai": sa})
        a, b = wilson(c["Đúng"], n)
        a2, b2 = wilson(d, n)
        L.append(f"| {pp} | {n} | {s3(c['Đúng'] / n)} | [{s3(a)}; {s3(b)}] | {s3(d / n)} | [{s3(a2)}; {s3(b2)}] |")
    n = sum(tc.values())
    a, b = wilson(tc["Đúng"], n)
    a2, b2 = wilson(tm["Đúng"], n)
    L.append(f"| **tổng** | {n} | **{s3(tc['Đúng'] / n)}** | [{s3(a)}; {s3(b)}] | **{s3(tm['Đúng'] / n)}** "
             f"| [{s3(a2)}; {s3(b2)}] |")
    L += ["", "Phân bố ba loại lỗi (trước sửa → sau sửa):", "", "| biến thể | Thiếu | Thừa | Sai |", "|---|---:|---:|---:|"]
    for pp in ("A", "B", "B+"):
        c, (_, th, tu, sa) = dem[pp], moi[pp]
        L.append(f"| {pp} | {c['Thiếu']} → {th} | {c['Thừa']} → {tu} | {c['Sai']} → {sa} |")
    L.append(f"| **tổng** | {tc['Thiếu']} → {tm['Thiếu']} | {tc['Thừa']} → {tm['Thừa']} | {tc['Sai']} → {tm['Sai']} |")
    return L + nguon("nhan_120.txt (vòng một)", "eval/nhan_trich_dan.md (vòng hai)", "results/kiem_regex_trich_dan.md")


# ── khối 4 ───────────────────────────────────────────────────────────────────────────────────────────────────
def khoi4(C) -> list[str]:
    D = ("R@5", "R@1200t", "MRR")
    L = ["## Khối 4 — Truy hồi, 110 câu", "", "| phương pháp | Recall@5 | Recall@1200 | MRR |", "|---|---:|---:|---:|"]
    for p in ("A", "C", "D", "B"):
        x = [r for r in C if r["pp"] == p]
        L.append(f"| {p} | " + " | ".join(s3(tb(x, d)) for d in D) + " |")
    L += ["", "| hiệu | Recall@5 | Recall@1200 | MRR |", "|---|---|---|---|"]
    for p in ("A", "C", "D"):
        L.append(f"| B − {p} | " + " | ".join(ci(bs(C, p, "B", d)) for d in D) + " |")
    L += ["", "Năm nhóm, A và B:", "", "| nhóm | n | R@5 A | R@5 B | B − A R@5 | R@1200 A | R@1200 B | B − A R@1200 "
          "| MRR A | MRR B |", "|---|---:|---:|---:|---|---:|---:|---|---:|---:|"]
    for g in NHOM:
        x = [r for r in C if r["loai"] == g]
        a, b = [r for r in x if r["pp"] == "A"], [r for r in x if r["pp"] == "B"]
        L.append(f"| {g} | {len(a)} | {s3(tb(a, 'R@5'))} | {s3(tb(b, 'R@5'))} | {ci(bs(x, 'A', 'B', 'R@5'))} "
                 f"| {s3(tb(a, 'R@1200t'))} | {s3(tb(b, 'R@1200t'))} | {ci(bs(x, 'A', 'B', 'R@1200t'))} "
                 f"| {s3(tb(a, 'MRR'))} | {s3(tb(b, 'MRR'))} |")
    L += ["", "| tập | n | " + " | ".join(f"R@5 {p}" for p in ("A", "C", "D", "B")) + " | B − A R@5 |",
          "|---|---:|---:|---:|---:|---:|---|"]
    for ten, f in (("gold trung lập", True), ("gold trùng ranh giới", False)):
        x = [r for r in C if bool(r["trung_lap"]) == f]
        L.append(f"| {ten} | {len(x) // len(PP8)} | "
                 + " | ".join(s3(tb([r for r in x if r["pp"] == p], "R@5")) for p in ("A", "C", "D", "B"))
                 + f" | {ci(bs(x, 'A', 'B', 'R@5'))} |")
    return L + nguon("results/local_gpu/chi_tiet_cau.jsonl", "results/local_gpu/metrics_truy_hoi.md")


# ── khối 5 ───────────────────────────────────────────────────────────────────────────────────────────────────
def khoi5(C) -> list[str]:
    L = ["## Khối 5 — Trích dẫn, 110 câu", "",
         "Hai tiêu chí: **khớp hoàn toàn** (chính — đủ gold, không trích thừa) và *đủ gold* (phụ — cho phép thừa), mức "
         "Điều. Cắt trần và từ chối nằm trong mẫu số.", "",
         "| phương pháp | khớp hoàn toàn | đủ gold | đạt / từ chối / cắt trần | − A khớp hoàn toàn | − A đủ gold "
         "| − B khớp hoàn toàn | − B đủ gold |", "|---|---:|---:|---|---|---|---|---|"]
    for p in PP8:
        x = [r for r in C if r["pp"] == p]
        L.append(f"| {p} | {s3(tb(x, 'dieu_toan_phan'))} | {s3(tb(x, 'dieu_du_gold'))} | {hm(C, p)} "
                 f"| {'—' if p == 'A' else ci(bs(C, 'A', p, 'dieu_toan_phan'))} "
                 f"| {'—' if p == 'A' else ci(bs(C, 'A', p, 'dieu_du_gold'))} "
                 f"| {'—' if p == 'B' else ci(bs(C, 'B', p, 'dieu_toan_phan'))} "
                 f"| {'—' if p == 'B' else ci(bs(C, 'B', p, 'dieu_du_gold'))} |")
    for do, ten in (("dieu_toan_phan", "khớp hoàn toàn"), ("dieu_du_gold", "đủ gold")):
        L += ["", f"Năm nhóm — {ten}:", "", "| nhóm | n | " + " | ".join(PP8) + " | B − A |",
              "|---|---:|" + "---:|" * len(PP8) + "---|"]
        tap = [(g, [r for r in C if r["loai"] == g]) for g in NHOM] + [("gold trung lập", [r for r in C if r["trung_lap"]])]
        for g, x in tap:
            L.append(f"| {g} | {len(x) // len(PP8)} | "
                     + " | ".join(s3(tb([r for r in x if r["pp"] == p], do)) for p in PP8)
                     + f" | {ci(bs(x, 'A', 'B', do))} |")
    xk = [r for r in C if r["loai"] == "xuyen_khoan"]
    L += ["", "Tỷ lệ trả lời thiếu ở `xuyen_khoan` (17 câu; thiếu = bỏ sót ≥ 1 đơn vị gold mức Điều, kể cả từ chối "
          "và cắt trần):", "", "| phương pháp | tỷ lệ thiếu | − B |", "|---|---:|---|"]
    for p in PP8:
        L.append(f"| {p} | {s3(tb([r for r in xk if r['pp'] == p], 'thieu'))} | "
                 + ("—" if p == "B" else ci(bs(xk, "B", p, "thieu"))) + " |")
    return L + nguon("results/local_gpu/chi_tiet_cau.jsonl", "results/local_gpu/metrics_trich_dan.md")


# ── khối 6 ───────────────────────────────────────────────────────────────────────────────────────────────────
def khoi6(M) -> list[str]:
    L = ["## Khối 6 — manh_con, 35 câu", "", "| cấu hình | R@5 | gold trong ngữ cảnh | khớp hoàn toàn | đủ gold "
         "| đạt / từ chối / cắt trần | − B khớp hoàn toàn |", "|---|---:|---:|---:|---:|---|---|"]
    for p in ("B", "B+", "E2", "E3"):
        x = [r for r in M if r["pp"] == p]
        L.append(f"| {p} | {s3(tb(x, 'R@5'))} | {s3(tb(x, 'trong_ngu_canh'))} | {s3(tb(x, 'dieu_toan_phan'))} "
                 f"| {s3(tb(x, 'dieu_du_gold'))} | {hm(M, p)} | {'—' if p == 'B' else ci(bs(M, 'B', p, 'dieu_toan_phan'))} |")
    E8 = ("B", "Eduoi", "Etren", "Etat_d", "Etat_k", "Etat_n", "Etat_s", "Echi_s")
    taps = (("tập mất câu dẫn", "tap_mat_cau_dan"), ("tập tầng cuối", "tap_tang_cuoi"))
    L += ["", "Tám cấu hình (B + bảy cấu hình E), tách hai tập — R@5 / gold trong ngữ cảnh / khớp hoàn toàn:", "",
          "| cấu hình | " + " | ".join(f"{t} (n={len({r['qid'] for r in M if r[k]})})" for t, k in taps)
          + " | cắt trần (35 câu) |", "|---|---|---|---:|"]
    for p in E8:
        o_ = []
        for _, k in taps:
            x = [r for r in M if r["pp"] == p and r[k]]
            o_.append(f"{s3(tb(x, 'R@5'))} / {s3(tb(x, 'trong_ngu_canh'))} / {s3(tb(x, 'dieu_toan_phan'))}")
        L.append(f"| {p} | " + " | ".join(o_) + f" | {sum(r['hang_muc'] == 'cat_tran' for r in M if r['pp'] == p)} |")
    cat = {p: sum(r["hang_muc"] == "cat_tran" for r in M if r["pp"] == p) for p in dict.fromkeys(r["pp"] for r in M)}
    L += ["", "Cắt trần theo cấu hình (35 câu): " + ", ".join(f"{p} {n}" for p, n in cat.items()) + "."]
    return L + nguon("results/local_gpu/chi_tiet_cau.jsonl (bo = manh_con)", "results/local_gpu/manh_con_tra_loi.jsonl")


# ── khối 7 ───────────────────────────────────────────────────────────────────────────────────────────────────
def khoi7(C, E3b, hoi) -> list[str]:
    q26 = [q for q in hoi if q["loai"] in ("dan_chieu", "xuyen_khoan")]
    tk = {}
    for pp in ("E3", "E3b"):
        dan_chieu.THONG_KE.clear()
        for q in q26:
            v = truy_hoi.nhung_cau_hoi(q["question"])
            truy_hoi.ngu_canh(pp, truy_hoi.tim(pp, v, k=ch.K_UNG_VIEN))
        tk[pp] = dict(dan_chieu.THONG_KE)
    R = [r for r in C if r["pp"] in ("B", "B+", "E3")] + E3b
    L = ["## Khối 7 — Dẫn chiếu: 26 câu (dan_chieu + xuyen_khoan) và 9 câu (dan_chieu)", "",
         "E3 = E2 (mở rộng lên Điều cha) + theo dẫn chiếu tường minh một bước; E3b = nền B, không mở rộng.", ""]
    for ten, loc in (("26 câu", ("dan_chieu", "xuyen_khoan")), ("9 câu `dan_chieu`", ("dan_chieu",))):
        x = [r for r in R if r["loai"] in loc]
        L += [f"### {ten}", "", "| phương pháp | n | khớp hoàn toàn | đủ gold | trả lời thiếu | đạt / từ chối / cắt trần "
              "| − B khớp hoàn toàn |", "|---|---:|---:|---:|---:|---|---|"]
        for p in ("B", "B+", "E3", "E3b"):
            y = [r for r in x if r["pp"] == p]
            if not y:
                L.append(f"| {p} | — | {CHUA} | {CHUA} | {CHUA} | {CHUA} | {CHUA} |")
                continue
            L.append(f"| {p} | {len(y)} | {s3(tb(y, 'dieu_toan_phan'))} | {s3(tb(y, 'dieu_du_gold'))} | {s3(tb(y, 'thieu'))} "
                     f"| {hm(x, p)} | {'—' if p == 'B' else ci(bs(x, 'B', p, 'dieu_toan_phan', phan_tang=len(loc) > 1))} |")
        L.append("")

    def g(pp, k):
        return sum(v for kk, v in tk[pp].items() if kk.endswith(k))
    L += ["Thống kê dẫn chiếu khi dựng ngữ cảnh cho 26 câu (đếm số lần, không phải số câu):", "",
          "| | theo được | không theo được | ngoài kho | bỏ vì hết ngân sách |", "|---|---:|---:|---:|---:|"]
    for pp in ("E3", "E3b"):
        L.append(f"| {pp} | {g(pp, '_theo_duoc')} | {g(pp, '_khong_thay')} | {tk[pp].get('khac_vb_ngoai_kho', 0)} "
                 f"| {tk[pp].get('bo_vi_het_ngan_sach', 0)} |")
    L += ["", "Chi tiết theo loại: " + "; ".join(f"{pp}: " + ", ".join(f"{k} {v}" for k, v in sorted(tk[pp].items()))
                                              for pp in tk)]
    return L + nguon("results/local_gpu/chi_tiet_cau.jsonl", "results/local_gpu/dan_chieu26/pilot_tra_loi.jsonl (E3b)",
                     "rag/dan_chieu.py (THONG_KE)")


# ── khối 8 ───────────────────────────────────────────────────────────────────────────────────────────────────
def khoi8(C, hoi, so_hieu) -> list[str]:
    bc = ban_cu(hoi, C, so_hieu, list(PP8))
    L = ["## Khối 8 — Nhiễu bản cũ", "",
         "Số câu có chunk của **bản cũ** trong top-5 / top-10. *Tập phiên bản*: bản cũ nằm trong bảng tương đương (lấy "
         "về không phải lỗi). *Tập nhiễu*: bản cũ ngoài bảng tương đương (lấy về là nhiễu thật).", "",
         "| tập | n | " + " | ".join(f"{p} top-5 / top-10" for p in ("A", "C", "D", "B")) + " |",
         "|---|---:|---|---|---|---|"]
    for ten, nhan in (("phien_ban", "tập phiên bản"), ("ban_cu_nhieu", "tập nhiễu")):
        cu = bc[ten]
        o_ = []
        for p in ("A", "C", "D", "B"):
            x = [r for r in C if r["pp"] == p and r["qid"] in cu]
            o_.append(f"{sum(any(d in cu[r['qid']] for d in r['doc_top10'][:5]) for r in x)} / "
                      f"{sum(any(d in cu[r['qid']] for d in r['doc_top10']) for r in x)}")
        L.append(f"| {nhan} | {len(cu)} | " + " | ".join(o_) + " |")
    return L + nguon("results/local_gpu/chi_tiet_cau.jsonl", "results/local_gpu/metrics_truy_hoi.md §4")


# ── khối 9 ───────────────────────────────────────────────────────────────────────────────────────────────────
def khoi9() -> list[str]:
    from eval.thu_them import KIEM_SOAT, PP8 as P8, THU_NGHIEM
    rows = _nap(ch.RESULTS / "thu_them" / "chi_tiet_cau.jsonl")
    T = collections.defaultdict(list)
    for r in rows:
        T[r["thu"]].append(r)
    L = ["## Khối 9 — Thử thêm (bước 4, thăm dò)", "",
         "Mỗi bảng có **kiểm soát** = cấu hình gốc chạy lại cùng lượt, cùng server. Hiệu so với kiểm soát: bootstrap ghép "
         "cặp 95%. Mức Điều.", ""]

    def bang(t, pps, goc, tieu):
        x = T.get(t, [])
        out = [f"### {tieu}", "", "| biến | khớp hoàn toàn | đủ gold | đạt / từ chối / cắt trần | Δ khớp hoàn toàn "
               "| Δ đủ gold |", "|---|---:|---:|---|---|---|"]
        for p in pps:
            y = [r for r in x if r["pp"] == p]
            if not y:
                out.append(f"| {p} | {CHUA} | {CHUA} | {CHUA} | {CHUA} | {CHUA} |")
                continue
            kc = " (kiểm soát)" if p == goc else ""
            out.append(f"| {p}{kc} | {s3(tb(y, 'dieu_toan_phan'))} | {s3(tb(y, 'dieu_du_gold'))} | {hm(x, p)} "
                       f"| {'—' if p == goc else ci(bs(x, goc, p, 'dieu_toan_phan'))} "
                       f"| {'—' if p == goc else ci(bs(x, goc, p, 'dieu_du_gold'))} |")
        return out + [""]
    L += bang("seed", [f"A_s{s}" for s in range(4)], "A_s0", "9.1 Seed — A")
    L += bang("seed", [f"E_s{s}" for s in range(4)], "E_s0", "9.1 Seed — E")
    for g in ("B", "E2"):
        L += bang("ngan_sach", [f"{g}·600", f"{g}·1200", f"{g}·1800"], f"{g}·1200", f"9.2 Ngân sách — {g}, n_ctx 4096")
        L += bang("ngan_sach", [f"{g}·1200·8k", f"{g}·2400·8k"], f"{g}·1200·8k",
                  f"9.2 Ngân sách — {g}, n_ctx 8192 (chỉ cho 2.400 từ)")
    for g in ("B", "E3"):
        L += bang("mo_hinh", [f"{g}·4b", f"{g}·4bkm", f"{g}·8b"], f"{g}·4b", f"9.3 Mô hình sinh — {g}")
    x = T.get("loi_nhac", [])
    L += ["### 9.4 Lời nhắc P1 — tám phương pháp, mỗi phương pháp so với kiểm soát lời nhắc gốc", "",
          "| phương pháp | khớp hoàn toàn gốc → P1 | Δ [95% CI] | đủ gold gốc → P1 | Δ [95% CI] | cắt trần gốc → P1 |",
          "|---|---|---|---|---|---|"]
    for p in P8:
        a, b = [r for r in x if r["pp"] == p], [r for r in x if r["pp"] == f"{p}·P1"]
        if not a or not b:
            L.append(f"| {p} | {CHUA} | {CHUA} | {CHUA} | {CHUA} | {CHUA} |")
            continue
        L.append(f"| {p} | {s3(tb(a, 'dieu_toan_phan'))} → {s3(tb(b, 'dieu_toan_phan'))} "
                 f"| {ci(bs(x, p, f'{p}·P1', 'dieu_toan_phan'))} | {s3(tb(a, 'dieu_du_gold'))} → {s3(tb(b, 'dieu_du_gold'))} "
                 f"| {ci(bs(x, p, f'{p}·P1', 'dieu_du_gold'))} | {sum(r['hang_muc'] == 'cat_tran' for r in a)} → "
                 f"{sum(r['hang_muc'] == 'cat_tran' for r in b)} |")
    L += [""]
    L += bang("loi_nhac", ["E2", "E2n", "B"], "E2", "9.5 E2n — so với kiểm soát E2 (dòng B để so thêm)")
    L += ["### 9.6 Lọc cụm sáo khỏi chuỗi nhúng của B — chỉ truy hồi", "",
          "Xem `results/local_gpu/thu_them.md` §4: Bloc − B = +0,000 ở R@1, R@5, R@10, R@1200, gold trong ngữ cảnh; "
          "MRR −0,001 [−0,005; +0,002].", ""]
    return L + nguon("results/local_gpu/thu_them/chi_tiet_cau.jsonl", "results/local_gpu/thu_them.md")


def main() -> None:
    import time
    t0 = time.monotonic()
    tat_ca = sorted({truy_hoi.TEP.get(i, i) for pps in (BO["chinh"][3], BO["manh_con"][3]) for i in pps.values()})
    chot_chan(tat_ca)
    nap_so_hieu_chunk(tat_ca)
    docs = nap_van_ban()
    so_hieu = {d.doc_id: d.so_hieu for d in docs}
    rows = _nap(ch.RESULTS / "chi_tiet_cau.jsonl")
    C = [r for r in rows if r["bo"] == "chinh"]
    M = [r for r in rows if r["bo"] == "manh_con"]
    hoi = sorted(_nap(ch.GOC / "eval/questions.jsonl"), key=lambda x: x["qid"])
    mc = _nap(ch.GOC / "eval/manh_con.draft.jsonl")
    # E3b: 26 câu, tệp riêng; chấm bằng đúng cham_bo của bảng chính
    p_e3b = ch.RESULTS / "dan_chieu26" / "pilot_tra_loi.jsonl"
    E3b = []
    if p_e3b.exists():
        tl = {(y["qid"], y["pp"]): y for y in _nap(p_e3b)}
        q26 = [q for q in hoi if (q["qid"], "E3b") in tl]
        if len(q26) == 26:
            van_ban = {d.doc_id: d.text for d in docs}
            cap = cham.doc_cap()
            dv = {}
            for d in docs:
                if d.so_hieu in cap:
                    c_ = don_vi.chi_muc(d)
                    dv[d.doc_id] = c_["dieu"] + c_["khoan"] + c_["diem"] + c_["doan"]
            E3b = cham_bo("chinh", q26, tl, {"E3b": "E3b"}, van_ban, so_hieu, dv, cap)
    L = ["# Khối số cho quyển — bộ local GPU", "",
         "Bộ số chính của quyển (`results/local_gpu`, RTX 2050, Qwen3-4B-Instruct-2507 Q4_0); bộ VPS chỉ dùng kiểm chứng "
         "tái lập. Dấu phẩy thập phân, ba chữ số; hiệu số: bootstrap ghép cặp 95% (1000 lần, phân tầng theo nhóm), "
         "**đậm** = khoảng tin cậy không chứa 0.", ""]
    L += khoi1(docs) + khoi2(hoi, mc) + khoi3() + khoi4(C) + khoi5(C) + khoi6(M) + khoi7(C, E3b, hoi) \
        + khoi8(C, hoi, so_hieu) + khoi9()
    L += [f"Sinh bằng `python -m eval.khoi_so` trong {time.monotonic() - t0:.0f} s."]
    RA.write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()
