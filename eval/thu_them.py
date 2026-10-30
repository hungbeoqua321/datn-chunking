"""Bước 4 — thử thêm nhờ GPU (THĂM DÒ, tách riêng, không trộn vào bảng chính) → results/local_gpu/thu_them.md

Mỗi thử nghiệm có cột KIỂM SOÁT là cấu hình gốc chạy lại cùng lượt, cùng server — không lấy số bước 1 ra so.

  seed      A và E (Eduoi) × 4 seed phân đoạn (0 = kiểm soát) ở cả tầng sinh          server 4B Q4_0, n_ctx 4096
  loi_nhac  B, E2 (kiểm soát) · B, E2 với lời nhắc "không tự đặt số Điều" (P1)
            · E2n (gắn lại nhãn khoản trong khối mở rộng) · E2n + P1                    server 4B Q4_0, n_ctx 4096
  mo_hinh   B, E3 × {4B Q4_0 (kiểm soát), 4B Q4_K_M (đối chứng lượng tử), 8B Q4_K_M}    ba server, n_ctx 4096
  ngan_sach B, E2 × ngân sách 600 / 1200 (kiểm soát) / 1800 / 2400 từ                   server 4B Q4_0, n_ctx 8192
  loc       B vs Bloc (bỏ cụm sáo khỏi chuỗi nhúng, giữ thân chunk) — chỉ truy hồi

    python -m eval.thu_them --dung-chunk          # Eduoi_s1..3, Bloc_s0 vào CHUNKS_DIR, rồi: python -m rag.chi_muc …
    python -m eval.thu_them --sinh seed loi_nhac  # chỉ các biến của server đang chạy; server sai cấu hình → DỪNG
    python -m eval.thu_them --cham
"""
import argparse
import collections
import json
import os
import re
import statistics as st
import time

import requests

import cau_hinh as ch
from chunking import hybrid
from chunking.base import ghi_jsonl, nap_van_ban
from chunking.chay import PHUONG_PHAP_E
from eval import cham, don_vi, ket_qua
from eval.bang_day_du import _trich_dieu_ngoai_ngu_canh, bs, o, tb
from eval.cham_trich_dan import cham_mot, nap_so_hieu_chunk
from eval.chay_truy_hoi import _do, _td_cho
from rag import sinh, truy_hoi
from rag.kiem_chi_muc import chot_chan
from rag.sinh import LoiCat

THU = ch.RESULTS / "thu_them"
MD_RA = ch.RESULTS / "thu_them.md"

# P1 = lời nhắc gốc + đúng một quy tắc (đề xuất 1 của phân tích lỗi, results/local_gpu/phan_tich_loi.md §5).
HE_THONG_P1 = sinh.HE_THONG + (
    "\n4. Chỉ ghi số Điều khi chính đoạn ngữ cảnh đó có chữ \"Điều X\". Đoạn không có \"Điều\" nào thì chỉ ghi "
    "\"<số hiệu>\", tuyệt đối không tự đặt số Điều.")
LOI_NHAC = {"goc": sinh.HE_THONG, "P1": HE_THONG_P1}

# Máy chủ: (tên tệp mô hình, n_ctx) — đọc từ /props của llama-server, lệch là DỪNG.
MAY = {"4b": ("Qwen3-4B-Instruct-2507-Q4_0.gguf", 4096), "4b_8k": ("Qwen3-4B-Instruct-2507-Q4_0.gguf", 8192),
       "4bkm": ("Qwen3-4B-Instruct-2507-Q4_K_M.gguf", 4096), "8b": ("Qwen3-8B-Q4_K_M.gguf", 4096)}


def _b(ten, pp, may="4b", ngan_sach=ch.NGAN_SACH_NGU_CANH_TU, loi_nhac="goc"):
    return {"ten": ten, "pp": pp, "may": may, "ngan_sach": ngan_sach, "loi_nhac": loi_nhac}


# Mỗi thử nghiệm: (biến kiểm soát, danh sách biến). Biến đầu tiên của mỗi nhóm so sánh là kiểm soát.
THU_NGHIEM = {
    "seed": [_b(f"A_s{s}", f"A_s{s}") for s in range(4)] + [_b(f"E_s{s}", f"Eduoi_s{s}") for s in range(4)],
    "loi_nhac": [_b("B", "B"), _b("E2", "E2"), _b("B·P1", "B", loi_nhac="P1"), _b("E2·P1", "E2", loi_nhac="P1"),
                 _b("E2n", "E2n"), _b("E2n·P1", "E2n", loi_nhac="P1")],
    "mo_hinh": [_b(f"{p}·{m}", p, may=m) for m in ("4b", "4bkm", "8b") for p in ("B", "E3")],
    "ngan_sach": [_b(f"{p}·{w}", p, may="4b_8k", ngan_sach=w) for p in ("B", "E2") for w in (600, 1200, 1800, 2400)],
}
KIEM_SOAT = {"seed": {"A": "A_s0", "E": "E_s0"}, "loi_nhac": {"B": "B", "E2": "E2"},
             "mo_hinh": {"B": "B·4b", "E3": "E3·4b"}, "ngan_sach": {"B": "B·1200", "E2": "E2·1200"}}
CUM_SAO = ("theo quy định của pháp luật", "trừ trường hợp", "của Luật này", "của Nghị định này")
RE_SAO = re.compile("|".join(re.escape(c) for c in CUM_SAO), re.I)


def _hoi():
    return sorted((json.loads(l) for l in open(ch.GOC / "eval/questions.jsonl", encoding="utf-8") if l.strip()),
                  key=lambda x: x["qid"])


def _nap(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()] if p.exists() else []


# ── dựng chunk ───────────────────────────────────────────────────────────────────────────────────────────────
def dung_chunk() -> None:
    docs = nap_van_ban()
    ct = PHUONG_PHAP_E["Eduoi"]
    can = [s for s in (1, 2, 3) if not (ch.CHUNKS / f"Eduoi_s{s}.jsonl").exists()]
    if can:
        hybrid.chuan_bi(docs)
    goc = {c["chunk_id"].split(":", 2)[2]: c["text"] for c in _nap(ch.CHUNKS / "Eduoi_s0.jsonl")}
    for s in can:
        cs = [c for d in docs for c in hybrid.chunk(d, s, ct)]
        ghi_jsonl(ch.CHUNKS / f"Eduoi_s{s}.jsonl", cs)
        khac = sum(goc.get(c.chunk_id.split(":", 2)[2]) != c.text for c in cs)
        print(f"Eduoi_s{s}.jsonl: {len(cs)} chunk, khác seed 0: {khac}", flush=True)
    p = ch.CHUNKS / "Bloc_s0.jsonl"
    if not p.exists():
        ra, doi, so_cum = [], 0, collections.Counter()
        for c in _nap(ch.CHUNKS / "B_s0.jsonl"):
            tt = c.get("tien_to") or ""
            than = c["text"][len(tt) + 1:] if tt and c["text"].startswith(tt + "\n") else c["text"]
            moi = re.sub(r"[ \t]{2,}", " ", RE_SAO.sub("", than))
            so_cum.update(m.group(0).lower() for m in RE_SAO.finditer(than))
            if moi != than:
                doi += 1
            # "text" = chuỗi ĐEM NHÚNG (đã lọc); thân gốc giữ ở "text_goc" — chỉ đo truy hồi, chấm theo start/end
            ra.append({**c, "chunk_id": c["chunk_id"].replace("B:", "Bloc:", 1),
                       "text": (tt + "\n" + moi) if tt else moi, "text_goc": c["text"]})
        p.write_text("".join(json.dumps(c, ensure_ascii=False) + "\n" for c in ra), encoding="utf-8")
        print(f"Bloc_s0.jsonl: {len(ra)} chunk, {doi} chunk có cụm sáo bị bỏ khỏi chuỗi nhúng; "
              f"số lần xuất hiện: {dict(so_cum)}", flush=True)


# ── sinh ─────────────────────────────────────────────────────────────────────────────────────────────────────
def may_dang_chay() -> str | None:
    base = os.environ["LLM_BASE_URL"].rstrip("/").removesuffix("/v1")
    p = requests.get(base + "/props", timeout=30).json()
    tep = os.path.basename(p.get("model_path", ""))
    n = (p.get("default_generation_settings") or {}).get("n_ctx") or p.get("n_ctx")
    return next((k for k, v in MAY.items() if v == (tep, n)), None)


def sinh_thu(ten_thu: list[str]) -> None:
    may = may_dang_chay()
    if may is None:
        raise SystemExit("server LLM không khớp cấu hình nào trong MAY — DỪNG")
    if may in ("8b",) and not os.environ.get("LLM_TAT_NGHI"):
        raise SystemExit("mô hình 8B là Qwen3 lai: phải đặt LLM_TAT_NGHI=1 — DỪNG")
    hoi = _hoi()
    viec = [(t, x, b) for t in ten_thu for b in THU_NGHIEM[t] if b["may"] == may for x in hoi]
    chot_chan(sorted({truy_hoi.TEP.get(b["pp"], b["pp"]) for _, _, b in viec}))
    THU.mkdir(parents=True, exist_ok=True)
    xong = {t: {(y["qid"], y["bien"]) for y in _nap(THU / f"{t}.jsonl")} for t in ten_thu}
    viec = [(t, x, b) for t, x, b in viec if (x["qid"], b["ten"]) not in xong[t]]
    print(f"server {may}: còn {len(viec)} lượt", flush=True)
    cl, t0, cat, theo = sinh.client(), time.monotonic(), [], collections.defaultdict(float)
    vec: dict[str, object] = {}
    for i, (t, x, b) in enumerate(viec, 1):
        if x["question"] not in vec:
            vec.clear()
            vec[x["question"]] = truy_hoi.nhung_cau_hoi(x["question"])
        kq = truy_hoi.tim(b["pp"], vec[x["question"]], k=ch.K_UNG_VIEN)
        khoi = truy_hoi.ngu_canh(b["pp"], kq, ngan_sach=b["ngan_sach"], k=ch.K_UNG_VIEN)
        t1, loi_cat = time.monotonic(), ""
        try:
            r = sinh.tra_loi(x["question"], khoi, cl, {"qid": x["qid"], "bien_the": f"thu_{t}_{b['ten']}", "seed": 0},
                             he_thong=LOI_NHAC[b["loi_nhac"]])
        except LoiCat as e:
            loi_cat, r = str(e), {"tra_loi": ""}
            cat.append((t, x["qid"], b["ten"]))
        theo[(t, b["ten"])] += time.monotonic() - t1
        dong = {"qid": x["qid"], "bien": b["ten"], **{k: b[k] for k in ("pp", "may", "ngan_sach", "loi_nhac")},
                "loai": x["loai"], "question": x["question"], "gold": x["gold"], "tra_loi": r["tra_loi"],
                "cat_tran": bool(loi_cat), "ly_do_cat": loi_cat, "so_khoi": len(khoi),
                "so_tu_ngu_canh": sum(len(k["text"].split()) for k in khoi), "chunk_id": [k["chunk_id"] for k in khoi],
                "token_prompt": (r.get("usage") or {}).get("prompt_tokens")}
        with open(THU / f"{t}.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps(dong, ensure_ascii=False) + "\n")
        print(f"  [{i}/{len(viec)}] {t} {x['qid']} {b['ten']}  {time.monotonic() - t1:.1f}s "
              f"(tb {(time.monotonic() - t0) / i:.1f}s)" + ("  ← CẮT TRẦN" if loi_cat else ""), flush=True)
    print(f"→ xong {len(viec)} lượt trong {time.monotonic() - t0:.0f}s. Cắt trần: {len(cat)} {cat}", flush=True)
    print("thời gian theo biến (s): " + json.dumps({f"{t}/{b}": round(s) for (t, b), s in theo.items()},
                                                   ensure_ascii=False), flush=True)


# ── chấm ─────────────────────────────────────────────────────────────────────────────────────────────────────
def _nen():
    docs = nap_van_ban()
    van_ban = {d.doc_id: d.text for d in docs}
    so_hieu = {d.doc_id: d.so_hieu for d in docs}
    cap = cham.doc_cap()
    dv = {}
    for d in docs:
        if d.so_hieu in cap:
            ci = don_vi.chi_muc(d)
            dv[d.doc_id] = ci["dieu"] + ci["khoan"] + ci["diem"] + ci["doan"]
    return van_ban, so_hieu, dv, cap


def cham_thu(t: str, hoi, nen) -> list[dict]:
    tl = {(y["qid"], y["bien"]): y for y in _nap(THU / f"{t}.jsonl")}
    ra, vecs = [], {}
    for x in hoi:
        td = _td_cho(x["gold"], *nen, bool(x.get("phien_ban")))
        vecs[x["qid"]] = v = truy_hoi.nhung_cau_hoi(x["question"])
        for b in THU_NGHIEM[t]:
            r = tl.get((x["qid"], b["ten"]))
            if r is None:
                raise SystemExit(f"THIẾU {t}/{x['qid']}/{b['ten']} — chưa sinh xong, không lập bảng thiếu.")
            kq_d = truy_hoi.tim(b["pp"], v, k=ch.K_UNG_VIEN)
            kq = [c for c, _ in kq_d]
            khoi = truy_hoi.ngu_canh(b["pp"], kq_d, ngan_sach=b["ngan_sach"], k=ch.K_UNG_VIEN)
            if [k["chunk_id"] for k in khoi] != r["chunk_id"]:
                raise SystemExit(f"LỆCH NGỮ CẢNH {t}/{x['qid']}/{b['ten']} — DỪNG.")
            d = _do(x["gold"], kq, td)
            d["trong_ngu_canh"] = cham.recall_k(x["gold"], khoi, 10 ** 9, td=td)
            cd, ck = cham_mot(r, "dieu"), cham_mot(r, "khoan")
            n_trich, n_ngoai = _trich_dieu_ngoai_ngu_canh(r, khoi)
            ra.append({"thu": t, "qid": x["qid"], "pp": b["ten"], "loai": x["loai"], **d,
                       "hang_muc": ket_qua.phan_loai(r), "dieu_toan_phan": cd["toan_phan"],
                       "khoan_toan_phan": ck["toan_phan"], "so_dieu_trich": n_trich, "so_dieu_ngoai": n_ngoai,
                       "so_tu_ngu_canh": r["so_tu_ngu_canh"], "token_prompt": r.get("token_prompt"),
                       "tra_loi": r["tra_loi"]})
    return ra


def cham_loc(hoi, nen) -> list[dict]:
    ra = []
    for x in hoi:
        td = _td_cho(x["gold"], *nen, bool(x.get("phien_ban")))
        v = truy_hoi.nhung_cau_hoi(x["question"])
        for ten, idx in (("B", "B_s0"), ("Bloc", "Bloc_s0")):
            kq_d = truy_hoi.tim(idx, v, k=ch.K_UNG_VIEN)
            kq = [c for c, _ in kq_d]
            d = _do(x["gold"], kq, td)
            d["trong_50"] = cham.recall_k(x["gold"], kq, ch.K_UNG_VIEN, td=td)
            # mô hình sinh đọc THÂN GỐC → ngân sách đếm trên text_goc, không trên chuỗi đã lọc
            goc_d = [({**c, "text": c.get("text_goc", c["text"])}, s) for c, s in kq_d]
            d["trong_ngu_canh"] = cham.recall_k(x["gold"], truy_hoi.ngu_canh("B", goc_d), 10 ** 9, td=td)
            d["top10"] = [c["chunk_id"].split(":", 1)[1] for c in kq[:10]]
            ra.append({"qid": x["qid"], "pp": ten, "loai": x["loai"], **d})
    return ra


def _hm(rows, p):
    c = collections.Counter(r["hang_muc"] for r in rows if r["pp"] == p)
    return f"{c['dat']}/{c['tu_choi']}/{c['cat_tran']}"


def _ngoai(rows, p):
    x = [r for r in rows if r["pp"] == p]
    n = sum(r["so_dieu_trich"] for r in x)
    return f"{sum(r['so_dieu_ngoai'] for r in x)}/{n}" if n else "—"


def bang_sinh(rows, pps, goc):
    L = ["| biến | n | R@5 | gold trong ngữ cảnh | đúng toàn phần (Điều) | đúng toàn phần (khoản) "
         "| đạt / từ chối / **cắt trần** | Điều tự đoán | từ ngữ cảnh TV | Δ Điều so với kiểm soát [95% CI] |",
         "|---|---:|---:|---:|---:|---:|---|---:|---:|---|"]
    for p in pps:
        x = [r for r in rows if r["pp"] == p]
        h = "*kiểm soát*" if p == goc else o(bs(rows, goc, p, "dieu_toan_phan"))
        L.append(f"| {p} | {len(x)} | {tb(x, 'R@5'):.3f} | {tb(x, 'trong_ngu_canh'):.3f} | {tb(x, 'dieu_toan_phan'):.3f} "
                 f"| {tb(x, 'khoan_toan_phan'):.3f} | {_hm(rows, p)} | {_ngoai(rows, p)} "
                 f"| {st.median(r['so_tu_ngu_canh'] for r in x):.0f} | {h} |")
    return L


def bang_nhom(rows, pps):
    nhom = ("don_gian", "dieu_dai", "xuyen_khoan", "khong_co_dieu", "dan_chieu")
    L = ["| nhóm | n | " + " | ".join(pps) + " |", "|---|---:|" + "---:|" * len(pps)]
    for g in nhom:
        x = [r for r in rows if r["loai"] == g]
        L.append(f"| {g} | {len({r['qid'] for r in x})} | "
                 + " | ".join(f"{tb([r for r in x if r['pp'] == p], 'dieu_toan_phan'):.3f}" for p in pps) + " |")
    return L


def _so_trung(rows, a, b):
    xa = {r["qid"]: r["tra_loi"] for r in rows if r["pp"] == a}
    return sum(xa[r["qid"]] == r["tra_loi"] for r in rows if r["pp"] == b)


def muc_seed(R) -> list[str]:
    L = ["## 1. Bốn seed phân đoạn cho A và E — ở cả tầng sinh", "",
         "Seed = độ lệch điểm bắt đầu cửa sổ mỗi văn bản (`chunking/base.do_lech`). Với A mọi chunk dịch; với E chỉ "
         "cửa sổ fallback của văn bản không có Điều dịch. Sinh tham lam, tất định trên GPU — mọi phương sai ở đây "
         "đến từ phân đoạn. Kiểm soát = seed 0 chạy lại cùng lượt.", ""]
    for g, pps in (("A", [f"A_s{s}" for s in range(4)]), ("E", [f"E_s{s}" for s in range(4)])):
        L += [f"### {g}", ""] + bang_sinh(R, pps, KIEM_SOAT["seed"][g]) + [""]
    L += ["### Phương sai giữa seed so với hiệu giữa phương pháp", "",
          "| | trung bình 4 seed | độ lệch chuẩn giữa seed | khoảng (min–max) | số câu đổi kết quả giữa các seed |",
          "|---|---:|---:|---|---:|"]
    gt = {}
    for g in ("A", "E"):
        pps = [f"{g}_s{s}" for s in range(4)]
        v = [tb([r for r in R if r["pp"] == p], "dieu_toan_phan") for p in pps]
        gt[g] = v
        theo_cau = collections.defaultdict(set)
        for r in R:
            if r["pp"] in pps:
                theo_cau[r["qid"]].add(r["dieu_toan_phan"])
        L.append(f"| {g} | {st.mean(v):.3f} | {st.stdev(v):.3f} | {min(v):.3f}–{max(v):.3f} "
                 f"| {sum(len(s) > 1 for s in theo_cau.values())}/110 |")
    h = bs(R, "A_s0", "E_s0", "dieu_toan_phan")
    L += ["", f"Hiệu E − A ở seed 0: {o(h)}. Hiệu theo từng cặp seed cùng chỉ số (E_s{{k}} − A_s{{k}}): "
          + ", ".join(f"s{k} {o(bs(R, f'A_s{k}', f'E_s{k}', 'dieu_toan_phan'))}" for k in range(4)) + ".", ""]
    return L


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dung-chunk", action="store_true")
    ap.add_argument("--sinh", nargs="*", choices=list(THU_NGHIEM))
    ap.add_argument("--cham", action="store_true")
    a = ap.parse_args()
    if a.dung_chunk:
        dung_chunk()
    if a.sinh:
        sinh_thu(a.sinh)
    if not a.cham:
        return
    t0 = time.monotonic()
    idx = sorted({truy_hoi.TEP.get(b["pp"], b["pp"]) for bs_ in THU_NGHIEM.values() for b in bs_} | {"Bloc_s0"})
    chot_chan(idx)
    nap_so_hieu_chunk(idx)
    hoi, nen = _hoi(), _nen()
    co = [t for t in THU_NGHIEM if (THU / f"{t}.jsonl").exists()]
    R = {t: cham_thu(t, hoi, nen) for t in co}
    with open(THU / "chi_tiet_cau.jsonl", "w", encoding="utf-8") as f:
        for t in R:
            for r in R[t]:
                f.write(json.dumps({k: v for k, v in r.items() if k != "tra_loi"}, ensure_ascii=False) + "\n")
    L = ["# Thử thêm nhờ GPU — THĂM DÒ, không trộn vào bảng chính", "",
         f"Lượt local GPU, {time.strftime('%Y-%m-%d %H:%M')}. Sinh và chấm: `python -m eval.thu_them`. 110 câu bộ chính. "
         "Mỗi thử nghiệm có cấu hình gốc chạy lại cùng lượt làm kiểm soát. Hiệu: bootstrap ghép cặp 95% (1000 lần, "
         "phân tầng theo nhóm); **đậm** = khoảng tin cậy không chứa 0. Cột *đạt / từ chối / cắt trần*: cắt trần vẫn "
         "nằm trong mẫu số (tính là sai). *Điều tự đoán* = số Điều được trích mà chuỗi \"Điều N\" không có trong ngữ "
         "cảnh của đúng văn bản đó / số Điều được trích.", ""]
    if "seed" in R:
        L += muc_seed(R["seed"])
    if "ngan_sach" in R:
        x = R["ngan_sach"]
        L += ["## 2. Quét ngân sách ngữ cảnh 600 / 1.200 / 1.800 / 2.400 từ — B và E2", "",
              "Server riêng n_ctx 8192 (bản sao `tools/chay-llm-gpu-8k.sh`, chỉ đổi `-c`), mọi ngân sách kể cả kiểm "
              "soát 1.200 chạy trên cùng server này.", ""]
        for g in ("B", "E2"):
            pps = [f"{g}·{w}" for w in (600, 1200, 1800, 2400)]
            L += [f"### {g}", ""] + bang_sinh(x, pps, KIEM_SOAT["ngan_sach"][g]) + ["", "Theo nhóm (Điều):", ""] \
                + bang_nhom(x, pps) + [""]
            tok = [r["token_prompt"] for r in x if r["pp"] == f"{g}·2400" and r["token_prompt"]]
            if tok:
                L += [f"Token prompt ở 2.400 từ: trung vị {st.median(tok):.0f}, lớn nhất {max(tok)}.", ""]
        L += ["### E2 − B ở từng ngân sách", "", "| ngân sách | E2 − B (Điều) |", "|---|---|"]
        L += [f"| {w} | {o(bs(x, f'B·{w}', f'E2·{w}', 'dieu_toan_phan'))} |" for w in (600, 1200, 1800, 2400)] + [""]
    if "mo_hinh" in R:
        x = R["mo_hinh"]
        L += ["## 3. Mô hình sinh lớn hơn — B và E3", "",
              "Kiểm soát: Qwen3-4B-Instruct-2507 Q4_0 (mô hình của bảng chính). Unsloth không phát hành Qwen3-8B bản "
              "Q4_0, nên 8B chạy Q4_K_M; thêm 4B Q4_K_M làm đối chứng lượng tử để tách tác động cỡ mô hình khỏi tác "
              "động cách lượng tử. Qwen3-8B là mô hình lai (có chế độ suy nghĩ), chạy với `enable_thinking=false`, "
              "cùng lời nhắc, nhiệt độ 0, 384 token. 8B không vừa 4 GB VRAM: một phần lớp chạy CPU.", ""]
        for g in ("B", "E3"):
            pps = [f"{g}·{m}" for m in ("4b", "4bkm", "8b")]
            L += [f"### {g}", ""] + bang_sinh(x, pps, KIEM_SOAT["mo_hinh"][g]) + ["", "Theo nhóm (Điều):", ""] \
                + bang_nhom(x, pps) + [""]
            L += [f"8B − 4B Q4_K_M (cùng lượng tử): {o(bs(x, f'{g}·4bkm', f'{g}·8b', 'dieu_toan_phan'))}", ""]
        dc = [r for r in x if r["loai"] == "dan_chieu"]
        L += ["### Nhóm dẫn chiếu riêng", "", "| biến | n | Điều | 8B − biến này |", "|---|---:|---:|---|"]
        for p in [f"{g}·{m}" for g in ("B", "E3") for m in ("4b", "4bkm", "8b")]:
            y = [r for r in dc if r["pp"] == p]
            g = p.split("·")[0]
            L.append(f"| {p} | {len(y)} | {tb(y, 'dieu_toan_phan'):.3f} | "
                     + ("—" if p.endswith("8b") else o(bs(dc, p, f"{g}·8b", "dieu_toan_phan", phan_tang=False))) + " |")
        L += [""]
    if True:  # loc: chỉ truy hồi, không cần sinh
        y = cham_loc(hoi, nen)
        dos = ("R@1", "R@5", "R@10", "MRR", "R@1200t", "trong_50", "trong_ngu_canh")
        L += ["## 4. Lọc cụm sáo khỏi chuỗi nhúng của B — chỉ truy hồi", "",
              "Bloc = chunk B, bỏ \"" + "\", \"".join(CUM_SAO) + "\" (không phân biệt hoa thường) khỏi CHUỖI ĐEM NHÚNG; "
              "tiền tố và vị trí chunk giữ nguyên. Kiểm soát B tính lại cùng lượt.", "",
              "| biến | n | " + " | ".join(dos) + " |", "|---|---:|" + "---:|" * len(dos)]
        for p in ("B", "Bloc"):
            z = [r for r in y if r["pp"] == p]
            L.append(f"| {p} | {len(z)} | " + " | ".join(f"{tb(z, d):.3f}" for d in dos) + " |")
        t10 = {r["qid"]: r["top10"] for r in y if r["pp"] == "B"}
        doi = sum(t10[r["qid"]] != r["top10"] for r in y if r["pp"] == "Bloc")
        L += ["", f"Số câu có top-10 khác B (thứ tự hoặc thành phần): {doi}/{len(t10)}."]
        L += ["", "| hiệu | " + " | ".join(dos) + " |", "|---|" + "---|" * len(dos),
              "| Bloc − B | " + " | ".join(o(bs(y, "B", "Bloc", d)) for d in dos) + " |", "",
              "Theo nhóm (R@5):", "", "| nhóm | n | B | Bloc | Bloc − B |", "|---|---:|---:|---:|---|"]
        for g in ("don_gian", "dieu_dai", "xuyen_khoan", "khong_co_dieu", "dan_chieu"):
            z = [r for r in y if r["loai"] == g]
            L.append(f"| {g} | {len(z) // 2} | {tb([r for r in z if r['pp'] == 'B'], 'R@5'):.3f} | "
                     f"{tb([r for r in z if r['pp'] == 'Bloc'], 'R@5'):.3f} | {o(bs(z, 'B', 'Bloc', 'R@5', False))} |")
        L += [""]
    if "loi_nhac" in R:
        x = R["loi_nhac"]
        L += ["## 5. Hai cải tiến từ phân tích lỗi — lời nhắc P1 và E2n", "",
              "P1 = lời nhắc gốc + quy tắc 4: *\"Chỉ ghi số Điều khi chính đoạn ngữ cảnh đó có chữ 'Điều X'. Đoạn không "
              "có 'Điều' nào thì chỉ ghi '<số hiệu>', tuyệt đối không tự đặt số Điều.\"* E2n = E2, mỗi dòng khoản trong "
              "khối đã mở rộng được gắn lại nhãn \"(Điều N khoản k)\" (nhãn tính vào ngân sách 1.200 từ). Bộ chấm "
              "không đổi.", ""]
        L += bang_sinh(x, ["B", "B·P1"], "B") + [""] + bang_sinh(x, ["E2", "E2·P1", "E2n", "E2n·P1"], "E2") + [""]
        L += ["Theo nhóm (Điều):", ""] + bang_nhom(x, ["B", "B·P1", "E2", "E2·P1", "E2n", "E2n·P1"]) + [""]
        L += [f"E2n·P1 − B: {o(bs(x, 'B', 'E2n·P1', 'dieu_toan_phan'))} · E2n − B: {o(bs(x, 'B', 'E2n', 'dieu_toan_phan'))}"
              f" · B·P1 − B: {o(bs(x, 'B', 'B·P1', 'dieu_toan_phan'))}", ""]
    # kiểm soát chạy lại có trùng bước 1 không (sinh trên GPU tất định)
    buoc1 = {(y["qid"], y["pp"]): y["tra_loi"] for y in _nap(ch.RESULTS / "pilot_tra_loi.jsonl")}
    L += ["## Kiểm soát chạy lại so với bước 1", "", "| thử nghiệm | biến kiểm soát | trùng từng ký tự với bước 1 |",
          "|---|---|---:|"]
    map1 = {"A_s0": "A", "E_s0": "E", "B": "B", "E2": "E2", "B·4b": "B", "E3·4b": "E3", "B·1200": "B", "E2·1200": "E2"}
    for t, ks in KIEM_SOAT.items():
        if t in R:
            for k in ks.values():
                x = [r for r in R[t] if r["pp"] == k]
                L.append(f"| {t} | {k} | {sum(buoc1.get((r['qid'], map1[k])) == r['tra_loi'] for r in x)}/{len(x)} |")
    L += ["", f"Chấm hết {time.monotonic() - t0:.0f} s."]
    MD_RA.write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()
