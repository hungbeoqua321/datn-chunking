"""Chấm và lập bảng cho lượt chạy local (eval/sinh_day_du.py): truy hồi + trích dẫn, MỌI phương pháp.

    KET_QUA_DIR=results/local_gpu python -m eval.bang_day_du

Đọc  ch.RESULTS/pilot_tra_loi.jsonl (bộ chính, khoá "pp"), ch.RESULTS/manh_con_tra_loi.jsonl (khoá "cau_hinh").
Ghi  ch.RESULTS/metrics_truy_hoi.{md,csv}, ch.RESULTS/metrics_trich_dan.{md,csv},
     ch.RESULTS/chi_tiet_cau.jsonl — một dòng mỗi (bộ, câu, phương pháp): mọi điểm + cờ cho phân tích lỗi (bước 3).

Không chấm lại theo cách mới — dùng đúng các hàm đã chốt:
  truy hồi   eval.chay_truy_hoi._do (R@k, R@Wt, MRR; τ = 0,5; bảng cặp tương đương), K_UNG_VIEN 50
  trích dẫn  eval.cham_trich_dan.cham_mot (regex đã kiểm với 120 nhãn tay, độ khớp 0,825 — không sửa)
  hạng mục   eval.ket_qua.phan_loai (đạt / từ chối / cắt trần — cắt trần VẪN trong mẫu số)
  hiệu số    eval.cham.bootstrap_hieu (ghép cặp, 1000 lần, phân tầng theo nhóm câu hỏi)

Hai tầng truy hồi, báo cả hai:
  * xếp hạng chunk của chỉ mục — B+ trùng B, E2 / E3 trùng Echi_s, E3b trùng B ở tầng này (khác nhau ở bước dựng ngữ cảnh);
  * **gold trong ngữ cảnh** — gold có nằm trong các khối THỰC SỰ đưa cho mô hình (sau ngân sách 1200 từ, mở rộng Điều cha,
    kéo dẫn chiếu) hay không. Ngữ cảnh dựng lại tất định từ truy hồi, đối chiếu chunk_id với bản đã sinh — lệch là dừng.
"""
import collections
import csv
import json
import re
import time

import cau_hinh as ch
from chunking.base import nap_van_ban
from eval import cham, don_vi, ket_qua, trich_dan
from eval.cham_trich_dan import cham_mot, nap_so_hieu_chunk
from eval.chay_truy_hoi import BAN_CU_NHIEU, QUET_BAN_CU, _do, _td_cho
from eval.sinh_day_du import BO, PP_CHINH, PP_MANH_CON
from rag import truy_hoi
from rag.kiem_chi_muc import chot_chan

NHOM = ("don_gian", "dieu_dai", "xuyen_khoan", "khong_co_dieu", "dan_chieu")
DO_TH = ("R@1", "R@5", "R@10", "R@1200t", "MRR", "trong_50", "trong_ngu_canh")
TEN_TH = {"trong_50": "gold trong 50 ứng viên", "trong_ngu_canh": "gold trong ngữ cảnh"}
DO_TD = ("dieu_toan_phan", "dieu_du_gold", "khoan_toan_phan", "khoan_du_gold", "dieu_phu", "dieu_chinh_xac", "co_trich",
         "thieu")
TEN_TD = {"dieu_toan_phan": "**khớp hoàn toàn (Điều)**", "khoan_toan_phan": "khớp hoàn toàn (khoản)",
          "dieu_du_gold": "đủ gold (Điều)", "khoan_du_gold": "đủ gold (khoản)",
          "dieu_phu": "độ phủ", "dieu_chinh_xac": "độ chính xác", "co_trich": "có trích dẫn",
          "thieu": "trả lời thiếu"}
RE_DIEU = re.compile(r"Điều\s+(\d+[a-zđ]?)", re.I)


def _trich_dieu_ngoai_ngu_canh(r: dict, khoi: list[dict]) -> tuple[int, int]:
    """(số Điều được trích, số Điều được trích mà chuỗi 'Điều N' KHÔNG xuất hiện trong ngữ cảnh của đúng văn bản đó).
    Điều không có trong ngữ cảnh = mô hình tự đoán số Điều (chunk C, D không mang nhãn Điều)."""
    co = collections.defaultdict(set)
    for b in khoi:
        k = trich_dan.khoa_tu_chuoi(b["so_hieu"])
        co[k] |= {m.group(1).lower() for m in RE_DIEU.finditer(b["text"])}
    tat_ca = set().union(*co.values()) if co else set()
    trich = {(sh, str(d).lower()) for sh, d, _, _ in trich_dan.boc(r.get("tra_loi") or "") if d}
    ngoai = sum(1 for sh, d in trich if d not in (co.get(sh) if sh in co else tat_ca))
    return len(trich), ngoai


def cham_bo(ten, ds, tra_loi, pps, van_ban, so_hieu, dv, cap):
    ra = []
    for x in ds:
        td = _td_cho(x["gold"], van_ban, so_hieu, dv, cap, bool(x.get("phien_ban")))
        vec = truy_hoi.nhung_cau_hoi(x["question"])
        for pp, idx in pps.items():
            r = tra_loi.get((x["qid"], pp))
            if r is None:
                raise SystemExit(f"THIẾU câu trả lời {ten}/{x['qid']}/{pp} — bước 1 chưa xong, không lập bảng thiếu.")
            kq_d = truy_hoi.tim(idx, vec, k=ch.K_UNG_VIEN)
            kq = [c for c, _ in kq_d]
            khoi = truy_hoi.ngu_canh(idx, kq_d, ngan_sach=ch.NGAN_SACH_NGU_CANH_TU, k=ch.K_UNG_VIEN)
            if [b["chunk_id"] for b in khoi] != r["chunk_id"]:
                raise SystemExit(f"LỆCH NGỮ CẢNH {ten}/{x['qid']}/{pp}: dựng lại khác bản đã sinh — DỪNG.")
            d = _do(x["gold"], kq, td)
            d["trong_50"] = cham.recall_k(x["gold"], kq, ch.K_UNG_VIEN, td=td)
            d["trong_ngu_canh"] = cham.recall_k(x["gold"], khoi, 10 ** 9, td=td)
            # hạng của chunk đầu tiên chạm gold (≥ τ trên một đơn vị) — phục vụ phân tích lỗi
            d["hang_dau"] = next((i + 1 for i, c in enumerate(kq)
                                  if any(cham.do_phu(g, [c], td.get(j)) >= cham.TAU for j, g in enumerate(x["gold"]))),
                                 None)
            cd, ck = cham_mot(r, "dieu", td), cham_mot(r, "khoan", td)
            cd_cu = cham_mot(r, "dieu")   # trước sửa (1) — chỉ để đếm số câu đổi kết quả
            n_trich, n_ngoai = _trich_dieu_ngoai_ngu_canh(r, khoi)
            ra.append({"bo": ten, "qid": x["qid"], "pp": pp, "loai": x["loai"],
                       "trung_lap": bool(x.get("trung_lap")), "phien_ban": bool(x.get("phien_ban")),
                       "tap_mat_cau_dan": bool(x.get("tap_mat_cau_dan")), "tap_tang_cuoi": bool(x.get("tap_tang_cuoi")),
                       "hang_muc": ket_qua.phan_loai(r), **d,
                       "dieu_toan_phan": cd["toan_phan"], "dieu_phu": cd["phu"], "dieu_chinh_xac": cd["chinh_xac"],
                       "khoan_toan_phan": ck["toan_phan"], "co_trich": cd["co_trich"],
                       "dieu_du_gold": cd["du_gold"], "khoan_du_gold": ck["du_gold"],
                       "dieu_toan_phan_khong_td": cd_cu["toan_phan"], "dieu_du_gold_khong_td": cd_cu["du_gold"],
                       "thieu": 1.0 if cd["phu"] < 1 else 0.0,
                       "so_dieu_trich": n_trich, "so_dieu_ngoai_ngu_canh": n_ngoai,
                       "so_khoi": len(khoi), "so_tu_ngu_canh": r["so_tu_ngu_canh"],
                       "doc_top10": [c["doc_id"] for c in kq[:10]], "doc_ngu_canh": [b["doc_id"] for b in khoi]})
    return ra


def tb(rows, k):
    return sum(r[k] for r in rows) / len(rows) if rows else float("nan")


def bs(rows, a, b, k, phan_tang=True):
    """Hiệu b − a trên cùng tập câu, bootstrap ghép cặp 95%."""
    xa = sorted((r for r in rows if r["pp"] == a), key=lambda r: r["qid"])
    xb = sorted((r for r in rows if r["pp"] == b), key=lambda r: r["qid"])
    assert [r["qid"] for r in xa] == [r["qid"] for r in xb]
    if not xa:
        return (float("nan"),) * 3
    nh = [r["loai"] for r in xa] if phan_tang and len({r["loai"] for r in xa}) > 1 else None
    return cham.bootstrap_hieu([r[k] for r in xa], [r[k] for r in xb], nhom=nh)


def o(h):
    if h[0] != h[0]:
        return "—"
    s = f"{h[0]:+.3f} [{h[1]:+.3f}; {h[2]:+.3f}]"
    return f"**{s}**" if h[1] > 0 or h[2] < 0 else s


def tap_chinh(rows):
    t = {"tất cả": rows}
    for g in NHOM:
        t[f"nhóm {g}"] = [r for r in rows if r["loai"] == g]
    t["gold trung lập"] = [r for r in rows if r["trung_lap"]]
    t["gold trùng ranh giới"] = [r for r in rows if not r["trung_lap"]]
    return t


def tap_mc(rows):
    return {"tất cả": rows, "mất câu dẫn": [r for r in rows if r["tap_mat_cau_dan"]],
            "tầng cuối": [r for r in rows if r["tap_tang_cuoi"]]}


def n_cau(rows):
    return len({r["qid"] for r in rows})


def bang_diem(rows, pps, dos, ten_do, nhan="phương pháp"):
    L = [f"| {nhan} | n | " + " | ".join(ten_do.get(d, d) for d in dos) + " |",
         "|---|---:|" + "---:|" * len(dos)]
    for p in pps:
        x = [r for r in rows if r["pp"] == p]
        L.append(f"| {p} | {len(x)} | " + " | ".join(f"{tb(x, d):.3f}" for d in dos) + " |")
    return L


def bang_hieu(rows, pps, goc, dos, ten_do):
    L = [f"| hiệu (− {goc}) | " + " | ".join(ten_do.get(d, d) for d in dos) + " |", "|---|" + "---|" * len(dos)]
    for p in pps:
        if p != goc:
            L.append(f"| {p} − {goc} | " + " | ".join(o(bs(rows, goc, p, d)) for d in dos) + " |")
    return L


def bang_tap(taps, pps, do):
    L = ["| tập | n | " + " | ".join(pps) + " |", "|---|---:|" + "---:|" * len(pps)]
    for t, x in taps.items():
        L.append(f"| {t} | {n_cau(x)} | " + " | ".join(f"{tb([r for r in x if r['pp'] == p], do):.3f}" for p in pps)
                 + " |")
    return L


def bang_hang_muc(rows, pps, nhan="phương pháp"):
    L = [f"| {nhan} | n | đạt | từ chối | cắt trần | tỉ lệ từ chối |", "|---|---:|---:|---:|---:|---:|"]
    for p in pps:
        c = collections.Counter(r["hang_muc"] for r in rows if r["pp"] == p)
        n = sum(c.values())
        L.append(f"| {p} | {n} | {c['dat']} | {c['tu_choi']} | {c['cat_tran']} | {c['tu_choi'] / n:.3f} |")
    return L


def ban_cu(chinh_q, rows, so_hieu, pps):
    """Hai tập con bản cũ (như results/metrics_truy_hoi.md §3): số câu có chunk BẢN CŨ trong top-k / trong ngữ cảnh."""
    quet = {x["qid"]: x for x in json.load(open(QUET_BAN_CU, encoding="utf-8"))}
    sh2doc = collections.defaultdict(list)
    for d, s in so_hieu.items():
        sh2doc[s].append(d)
    ra = {}
    for ten, chon in (("ban_cu_nhieu", lambda x: x["qid"] in BAN_CU_NHIEU), ("phien_ban", lambda x: bool(x.get("phien_ban")))):
        cu = {}
        for x in (x for x in chinh_q if chon(x)):
            if x.get("phien_ban_cu"):
                cu[x["qid"]] = {g["doc_id"] for g in x["phien_ban_cu"]}
            else:
                s = quet.get(x["qid"], {}).get("cap", "")
                sh = s.split("↔")[-1].strip().split(" ")[0] if "↔" in s else ""
                cu[x["qid"]] = set(sh2doc.get(sh, []))
        ra[ten] = cu
    return ra


def main() -> None:
    t0 = time.monotonic()
    tat_ca_idx = sorted({truy_hoi.TEP.get(i, i) for pps in (PP_CHINH, PP_MANH_CON) for i in pps.values()})
    chot_chan(tat_ca_idx)
    nap_so_hieu_chunk(tat_ca_idx)
    docs = nap_van_ban()
    van_ban = {d.doc_id: d.text for d in docs}
    so_hieu = {d.doc_id: d.so_hieu for d in docs}
    cap = cham.doc_cap()
    dv = {}
    for d in docs:
        if d.so_hieu in cap:
            ci = don_vi.chi_muc(d)
            dv[d.doc_id] = ci["dieu"] + ci["khoan"] + ci["diem"] + ci["doan"]

    ket, cau = {}, {}
    for ten, (p_hoi, tep, khoa, pps) in BO.items():
        ds = sorted((json.loads(l) for l in open(p_hoi, encoding="utf-8") if l.strip()), key=lambda x: x["qid"])
        tl = {(y["qid"], y[khoa]): y for y in map(json.loads, open(ch.RESULTS / tep, encoding="utf-8"))}
        print(f"chấm {ten}: {len(ds)} câu × {len(pps)} …", flush=True)
        ket[ten] = cham_bo(ten, ds, tl, pps, van_ban, so_hieu, dv, cap)
        cau[ten] = ds
    with open(ch.RESULTS / "chi_tiet_cau.jsonl", "w", encoding="utf-8") as f:
        for ten in ket:
            for r in ket[ten]:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")

    C, M = ket["chinh"], ket["manh_con"]
    PC, PM = list(PP_CHINH), list(PP_MANH_CON)
    PM4 = ["B", "B+", "E2", "E3"]
    tc, tm = tap_chinh(C), tap_mc(M)
    giay = time.monotonic() - t0

    # ── CSV dạng dài ────────────────────────────────────────────────────────────
    for ten_tep, dos in (("metrics_truy_hoi.csv", DO_TH), ("metrics_trich_dan.csv", DO_TD)):
        with open(ch.RESULTS / ten_tep, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["loai_dong", "bo", "pp", "tap", "n", "do_do", "gia_tri", "ci_duoi", "ci_tren"])
            for bo, taps, pps in (("chinh", tc, PC), ("manh_con", tm, PM)):
                for t, x in taps.items():
                    for p in pps:
                        y = [r for r in x if r["pp"] == p]
                        for d in dos:
                            w.writerow(["diem", bo, p, t, len(y), d, round(tb(y, d), 4), "", ""])
                    for goc in (("A", "B") if bo == "chinh" else ("B",)):
                        for p in pps:
                            if p == goc:
                                continue
                            for d in dos:
                                h = bs(x, goc, p, d)
                                w.writerow(["hieu", bo, f"{p} − {goc}", t, n_cau(x), d,
                                            round(h[0], 4), round(h[1], 4), round(h[2], 4)])
            if ten_tep == "metrics_trich_dan.csv":
                for bo, rows, pps in (("chinh", C, PC), ("manh_con", M, PM)):
                    for p in pps:
                        c = collections.Counter(r["hang_muc"] for r in rows if r["pp"] == p)
                        for k in ket_qua.LOAI:
                            w.writerow(["hang_muc", bo, p, "tất cả", sum(c.values()), k, c[k], "", ""])

    dau = (f"Lượt chạy **local GPU** (RTX 2050, Qwen3-4B Q4_0 CUDA), {time.strftime('%Y-%m-%d %H:%M')}. "
           "Cấu hình sinh khoá như VPS: ngân sách 1200 từ, 50 ứng viên, 384 token, nhiệt độ 0, cùng lời nhắc. "
           "Sinh bằng `python -m eval.bang_day_du` từ `pilot_tra_loi.jsonl` / `manh_con_tra_loi.jsonl` cùng thư mục. "
           "Hiệu số: bootstrap ghép cặp 95% (1000 lần, phân tầng theo nhóm); **đậm** = khoảng tin cậy không chứa 0.")

    # ── metrics_truy_hoi.md ────────────────────────────────────────────────────
    L = [f"# Độ đo tầng truy hồi — local GPU", "", dau, "",
         "Hai tầng: *xếp hạng chunk* (R@k, R@1200t, MRR — B+ trùng B, E2/E3 trùng Echi_s ở tầng này) và "
         "*gold trong ngữ cảnh* (khối thật sự đưa cho mô hình sau ngân sách, mở rộng Điều, kéo dẫn chiếu). "
         "E = E đầy đủ (Eduoi).", "",
         f"## 1. Bộ chính — {n_cau(C)} câu × {len(PC)} phương pháp", ""] + bang_diem(C, PC, DO_TH, TEN_TH)
    L += ["", "### Hiệu so với A", ""] + bang_hieu(C, PC, "A", ("R@5", "R@1200t", "MRR", "trong_ngu_canh"), TEN_TH)
    L += ["", "### Hiệu so với B", ""] + bang_hieu(C, PC, "B", ("R@5", "R@1200t", "MRR", "trong_ngu_canh"), TEN_TH)
    for d in ("R@5", "trong_ngu_canh"):
        L += ["", f"## 2. Tách nhóm — {TEN_TH.get(d, d)}", ""] + bang_tap(tc, PC, d)
    L += ["", "### B − A theo từng tập (R@5 · gold trong ngữ cảnh)", "",
          "| tập | n | R@5 B − A | gold trong ngữ cảnh B − A |", "|---|---:|---|---|"]
    for t, x in tc.items():
        L.append(f"| {t} | {n_cau(x)} | {o(bs(x, 'A', 'B', 'R@5'))} | {o(bs(x, 'A', 'B', 'trong_ngu_canh'))} |")
    L += ["", f"## 3. manh_con — {n_cau(M)} câu × {len(PM)} cấu hình", ""] + bang_diem(M, PM, DO_TH, TEN_TH, "cấu hình")
    L += ["", "### Hiệu so với B", ""] + bang_hieu(M, PM, "B", ("R@5", "MRR", "trong_ngu_canh"), TEN_TH)
    L += ["", "### Theo tập con manh_con — gold trong ngữ cảnh", ""] + bang_tap(tm, PM, "trong_ngu_canh")
    bc = ban_cu(cau["chinh"], C, so_hieu, PC)
    L += ["", "## 4. Tập phiên bản và tập nhiễu bản cũ — số câu có chunk BẢN CŨ", "",
          "| tập | phương pháp | n | trong top-5 | trong top-10 | trong ngữ cảnh |", "|---|---|---:|---:|---:|---:|"]
    for ten, cu in bc.items():
        for p in PC:
            x = [r for r in C if r["pp"] == p and r["qid"] in cu]
            n5 = sum(any(d in cu[r["qid"]] for d in r["doc_top10"][:5]) for r in x)
            n10 = sum(any(d in cu[r["qid"]] for d in r["doc_top10"]) for r in x)
            nng = sum(any(d in cu[r["qid"]] for d in r["doc_ngu_canh"]) for r in x)
            L.append(f"| {ten} | {p} | {len(cu)} | {n5} | {n10} | {nng} |")
    L += ["", "`phien_ban`: bản cũ nằm trong bảng tương đương nên lấy về **không phải lỗi**. "
          "`ban_cu_nhieu`: bản cũ **ngoài** bảng tương đương — lấy về là nhiễu thật.", "",
          f"Thời gian chấm: {giay:.0f} s."]
    (ch.RESULTS / "metrics_truy_hoi.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    # ── metrics_trich_dan.md ───────────────────────────────────────────────────
    DT = ("dieu_toan_phan", "dieu_du_gold", "khoan_toan_phan", "khoan_du_gold", "dieu_phu", "dieu_chinh_xac", "co_trich")
    HT = ("dieu_toan_phan", "dieu_du_gold", "khoan_toan_phan", "dieu_phu")
    L = [f"# Độ chính xác trích dẫn — local GPU", "", dau, "",
         "Bộ bóc trích dẫn: regex đã chốt, kiểm với **120 nhãn tay, độ khớp 0,825** (`results/kiem_regex_trich_dan.md`) — "
         "mọi con số mang sẵn sai số đó. Câu **cắt trần** và **từ chối** vẫn nằm trong mẫu số.", "",
         "Hai tiêu chí, báo song song: **khớp hoàn toàn** (đủ mọi đơn vị gold và không trích thừa — tiêu chí chính) và "
         "*đủ gold* (đủ mọi đơn vị gold, cho phép trích thừa — tiêu chí phụ). Từ 30/10 trích dẫn trỏ vào **bản tương đương** "
         "theo bảng cặp đã chốt (`eval/cap_tuong_duong.csv`, cùng số Điều/khoản, nguyên văn giống hệt) được tính là trỏ "
         "vào gold, như ở tầng truy hồi; câu phiên bản không áp. Số câu đổi kết quả: mục 0.", "",
         f"## 1. Bộ chính — {n_cau(C)} câu × {len(PC)} phương pháp", ""] + bang_hang_muc(C, PC)
    L += [""] + bang_diem(C, PC, DT, TEN_TD)
    L += ["", "### 0. Số câu đổi kết quả do sửa bộ chấm ngày 30/10 (bộ chính, mức Điều)", "",
          "Sửa (1) = áp bảng cặp tương đương ở tầng trích dẫn. Sửa (2) = rà 19 câu `dieu_dai`: không câu nào có đơn vị "
          "gold lấy cả Điều → không sửa gold, 0 câu đổi (`results/nhat_ky_sua_loi.md`). Sửa (3) = thêm cột *đủ gold*: "
          "không đổi kết quả nào của cột chính; cột cuối đếm số câu *khớp hoàn toàn* = 0 mà *đủ gold* = 1.", "",
          "| phương pháp | sửa (1): 0 → 1 | sửa (1): 1 → 0 | sửa (2) | đủ gold nhưng không khớp hoàn toàn |",
          "|---|---:|---:|---:|---:|"]
    for p in PC:
        x = [r for r in C if r["pp"] == p]
        L.append(f"| {p} | {sum(r['dieu_toan_phan_khong_td'] == 0 and r['dieu_toan_phan'] == 1 for r in x)} "
                 f"| {sum(r['dieu_toan_phan_khong_td'] == 1 and r['dieu_toan_phan'] == 0 for r in x)} | 0 "
                 f"| {sum(r['dieu_du_gold'] == 1 and r['dieu_toan_phan'] == 0 for r in x)} |")
    L += ["", "### Hiệu so với A", ""] + bang_hieu(C, PC, "A", HT, TEN_TD)
    L += ["", "### Hiệu so với B", ""] + bang_hieu(C, PC, "B", HT, TEN_TD)
    L += ["", "### Kiểm định McNemar (khớp hoàn toàn, Điều), Holm trên 28 cặp", "",
          "| cặp | p | p sau Holm |", "|---|---:|---:|"]
    def day(p):
        return [r["dieu_toan_phan"] for r in sorted((r for r in C if r["pp"] == p), key=lambda r: r["qid"])]
    pv = {f"{a} vs {b}": cham.mcnemar(day(a), day(b)) for i, a in enumerate(PC) for b in PC[i + 1:]}
    ho = cham.holm(pv)
    for k in sorted(pv, key=pv.get):
        L.append(f"| {k} | {pv[k]:.3g} | {'**' if ho[k] < 0.05 else ''}{ho[k]:.3g}{'**' if ho[k] < 0.05 else ''} |")
    L += ["", "## 2. Tách nhóm — khớp hoàn toàn (Điều)", ""] + bang_tap(tc, PC, "dieu_toan_phan")
    L += ["", "### Tách nhóm — đủ gold (Điều), tiêu chí phụ", ""] + bang_tap(tc, PC, "dieu_du_gold")
    L += ["", "### B − A theo từng tập (Điều)", "", "| tập | n | B − A khớp hoàn toàn | B − A đủ gold |",
          "|---|---:|---|---|"]
    for t, x in tc.items():
        L.append(f"| {t} | {n_cau(x)} | {o(bs(x, 'A', 'B', 'dieu_toan_phan'))} | {o(bs(x, 'A', 'B', 'dieu_du_gold'))} |")
    L += ["", "### Hạng mục theo nhóm (đạt / từ chối / cắt trần)", "",
          "| nhóm | " + " | ".join(PC) + " |", "|---|" + "---|" * len(PC)]
    for g in NHOM:
        o_ = []
        for p in PC:
            c = collections.Counter(r["hang_muc"] for r in C if r["pp"] == p and r["loai"] == g)
            o_.append(f"{c['dat']}/{c['tu_choi']}/{c['cat_tran']}")
        L.append(f"| {g} | " + " | ".join(o_) + " |")
    xk = tc["nhóm xuyen_khoan"]
    L += ["", f"## 3. Trả lời thiếu ở `xuyen_khoan` ({n_cau(xk)} câu)", "",
          "*Trả lời thiếu* = độ phủ gold mức Điều < 1 (bỏ sót ít nhất một đơn vị gold), kể cả từ chối và cắt trần.", "",
          "| phương pháp | tỉ lệ thiếu | hiệu − B |", "|---|---:|---|"]
    for p in PC:
        L.append(f"| {p} | {tb([r for r in xk if r['pp'] == p], 'thieu'):.3f} | "
                 + ("—" if p == "B" else o(bs(xk, "B", p, "thieu"))) + " |")
    L += ["", f"## 4. manh_con — {n_cau(M)} câu", "", "### Bốn cột chính", ""] + bang_hang_muc(M, PM4, "cấu hình")
    L += [""] + bang_diem(M, PM4, DT, TEN_TD, "cấu hình")
    L += ["", "### Đủ 12 cấu hình (B + 7 cấu hình E + B+, E2, E3, E3b)", ""] + bang_hang_muc(M, PM, "cấu hình")
    L += [""] + bang_diem(M, PM, DT, TEN_TD, "cấu hình")
    L += ["", "### Hiệu so với B", ""] + bang_hieu(M, PM, "B", ("dieu_toan_phan", "dieu_du_gold", "khoan_toan_phan"),
                                                     TEN_TD)
    L += ["", "### Theo tập con manh_con — khớp hoàn toàn (Điều)", ""] + bang_tap(tm, PM, "dieu_toan_phan")
    L += ["", "### Theo tập con manh_con — đủ gold (Điều)", ""] + bang_tap(tm, PM, "dieu_du_gold")
    L += ["", "## 5. Tập phiên bản và tập nhiễu bản cũ — khớp hoàn toàn (Điều)", "",
          "| tập | n | " + " | ".join(PC) + " |", "|---|---:|" + "---:|" * len(PC)]
    for ten, cu in bc.items():
        x = [r for r in C if r["qid"] in cu]
        L.append(f"| {ten} | {n_cau(x)} | " + " | ".join(f"{tb([r for r in x if r['pp'] == p], 'dieu_toan_phan'):.3f}"
                                                        for p in PC) + " |")
    L += ["", "## 6. C và D ở tầng trích dẫn — mô hình có tự đoán số Điều không", "",
          "Chunk C (theo câu) và D (ngữ nghĩa) **không mang nhãn Điều**; số Điều chỉ có nếu chuỗi \"Điều N\" tình cờ nằm "
          "trong thân chunk. *Điều tự đoán* = Điều được trích mà chuỗi \"Điều N\" không xuất hiện ở đâu trong ngữ cảnh của "
          "đúng văn bản đó.", "",
          "| phương pháp | n | từ chối | tỉ lệ từ chối | câu có trích Điều | Điều được trích | Điều tự đoán | "
          "tỉ lệ tự đoán | khớp hoàn toàn (Điều) | đủ gold (Điều) | câu đúng ≥ 1 Điều gold |",
          "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for p in PC:
        x = [r for r in C if r["pp"] == p]
        tc_ = sum(r["so_dieu_trich"] for r in x)
        ng = sum(r["so_dieu_ngoai_ngu_canh"] for r in x)
        tu = sum(r["hang_muc"] == "tu_choi" for r in x)
        L.append(f"| {p} | {len(x)} | {tu} | {tu / len(x):.3f} | {sum(r['so_dieu_trich'] > 0 for r in x)} | {tc_} | {ng} | "
                 f"{(ng / tc_ if tc_ else 0):.3f} | {tb(x, 'dieu_toan_phan'):.3f} | {tb(x, 'dieu_du_gold'):.3f} "
                 f"| {sum(r['dieu_phu'] > 0 for r in x)} |")
    L += ["", f"Thời gian chấm: {giay:.0f} s."]
    (ch.RESULTS / "metrics_trich_dan.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"→ {ch.RESULTS}/metrics_truy_hoi.md, metrics_trich_dan.md, chi_tiet_cau.jsonl ({time.monotonic() - t0:.0f}s)")
    for p in PC:
        x = [r for r in C if r["pp"] == p]
        print(f"  {p:4s} R@5={tb(x, 'R@5'):.3f} ngữ cảnh={tb(x, 'trong_ngu_canh'):.3f} "
              f"trích dẫn đúng={tb(x, 'dieu_toan_phan'):.3f}")


if __name__ == "__main__":
    main()
