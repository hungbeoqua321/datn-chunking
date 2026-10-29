"""Chấm trích dẫn: so trích dẫn mô hình viết ra với gold.

    python -m eval.cham_trich_dan        # chấm cả bộ chính và manh_con

Bộ bóc đã được kiểm với nhãn tay 120 dòng, độ khớp **0,825** (xem
`results/kiem_regex_trich_dan.md`) — mọi con số dưới đây mang sẵn sai số đó.

Hai mức so khớp, báo cả hai:
  **Điều** — chỉ cần đúng số hiệu + số Điều;
  **khoản** — đúng cả khoản (gold không nêu khoản thì mức này bằng mức Điều).

Ba độ đo trên từng câu, rồi lấy trung bình:
  đúng toàn phần — tập trích dẫn phủ HẾT gold và không thừa đơn vị nào;
  độ phủ (recall) — tỉ lệ đơn vị gold được trích dẫn;
  độ chính xác (precision) — tỉ lệ trích dẫn trỏ đúng một đơn vị gold.

Câu **cắt trần** và câu **từ chối** vẫn nằm trong mẫu số (xem eval/ket_qua.py), vì không trích
dẫn được cũng là một kết quả.
"""
import argparse
import collections
import itertools
import csv
import json
import time

import cau_hinh as ch
from eval import ket_qua, trich_dan
from rag import truy_hoi

CSV_RA = ch.RESULTS / "metrics_trich_dan.csv"
MD_RA = ch.RESULTS / "metrics_trich_dan.md"
_SH_CHUNK: dict[str, frozenset] = {}


def nap_so_hieu_chunk(tens) -> None:
    for t in tens:
        p = ch.INDEX / t / "chunks.jsonl"
        if p.exists():
            for c in map(json.loads, open(p)):
                k = trich_dan.khoa_tu_chuoi(c["so_hieu"])
                if k:
                    _SH_CHUNK[c["chunk_id"]] = k


def khoa_gold(g: dict, muc: str) -> tuple:
    k = trich_dan.khoa_tu_chuoi(g["so_hieu"])
    if muc == "dieu" or g.get("khoan") is None:
        return (k, g.get("dieu"), None)
    return (k, g.get("dieu"), g.get("khoan"))


def khoa_trich(t: tuple, muc: str) -> tuple:
    sh, dieu, khoan, _ = t
    return (sh, dieu, None) if muc == "dieu" else (sh, dieu, khoan)


def cham_mot(r: dict, muc: str) -> dict:
    gold = {khoa_gold(g, muc) for g in r["gold"]}
    mac_dinh = _SH_CHUNK.get((r.get("chunk_id") or [None])[0])
    khong_dieu = any(g.get("dieu") is None for g in r["gold"])
    boc = trich_dan.boc(r.get("tra_loi") or "", mac_dinh=mac_dinh,
                        cho_phep_khong_dieu=khong_dieu)
    # ở mức Điều, gold không nêu khoản thì trích dẫn có khoản vẫn tính là trúng
    lay = {khoa_trich(t, muc) for t in boc}
    if muc == "khoan":
        g_khong_khoan = {k for k in gold if k[2] is None}
        lay |= {(sh, d, None) for sh, d, kh in lay if (sh, d, None) in g_khong_khoan}
    trung = lay & gold
    return {"phu": len(trung) / len(gold) if gold else 0.0,
            "chinh_xac": len(trung) / len(lay) if lay else 0.0,
            "toan_phan": float(bool(gold) and trung == gold and len(lay) == len(trung)),
            "co_trich": float(bool(lay))}


def cham_bo(rows: list[dict], khoa_pp: str) -> list[dict]:
    ra = []
    for pp in dict.fromkeys(r[khoa_pp] for r in rows):
        ds = [r for r in rows if r[khoa_pp] == pp]
        hm = collections.Counter(ket_qua.phan_loai(r) for r in ds)
        d = {"pp": pp, "n": len(ds), **{f"hm_{k}": hm[k] for k in ket_qua.LOAI}}
        for muc in ("dieu", "khoan"):
            diem = [cham_mot(r, muc) for r in ds]
            for k in ("toan_phan", "phu", "chinh_xac"):
                d[f"{muc}_{k}"] = sum(x[k] for x in diem) / len(diem)
        ra.append(d)
    return ra


def bang(ds: list[dict], tieu: str) -> list[str]:
    L = [f"| {tieu} | n | đạt | từ chối | cắt trần | đúng toàn phần | độ phủ | độ chính xác "
         "| đúng toàn phần (khoản) |",
         "|---|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for d in ds:
        L.append(f"| {d['pp']} | {d['n']} | {d['hm_dat']} | {d['hm_tu_choi']} | {d['hm_cat_tran']} "
                 f"| **{d['dieu_toan_phan']:.3f}** | {d['dieu_phu']:.3f} | {d['dieu_chinh_xac']:.3f} "
                 f"| {d['khoan_toan_phan']:.3f} |")
    return L


def _diem(rows, khoa, pp):
    ds = sorted([r for r in rows if r[khoa] == pp], key=lambda r: r["qid"])
    return [cham_mot(r, "dieu")["toan_phan"] for r in ds]


def kiem_dinh(chinh: list[dict], mc: list[dict]) -> list[str]:
    """McNemar ghép cặp trên "trích dẫn đúng toàn phần", hiệu chỉnh Holm trong từng bộ.

    McNemar hợp ở đây vì độ đo là nhị phân và hai phương pháp được chấm trên CÙNG câu hỏi —
    nó chỉ đếm các câu mà hai bên khác nhau, nên không bị nhiễu bởi những câu cả hai cùng
    đúng hoặc cùng sai. Holm chặn lạm phát sai số do so nhiều cặp một lúc.
    """
    from eval import cham
    L = ["", "## 4. Kiểm định — McNemar ghép cặp, hiệu chỉnh Holm", "",
         "Độ đo kiểm định là **trích dẫn đúng toàn phần** (nhị phân từng câu). Hiệu chỉnh Holm "
         "tính riêng trong từng bộ.", ""]
    for ten, rows, khoa, pps in (("Bộ chính, 110 câu", chinh, "pp", ("A", "B", "B+")),
                                 ("manh_con, 35 câu", mc, "cau_hinh",
                                  ("B", "B+", "Eduoi", "E2", "E3"))):
        co = [x for x in pps if any(r[khoa] == x for r in rows)]
        if len(co) < 2:
            continue
        d = {x: _diem(rows, khoa, x) for x in co}
        p = {f"{a} vs {b}": cham.mcnemar(d[a], d[b]) for a, b in itertools.combinations(co, 2)}
        h = cham.holm(p)
        L += [f"### {ten}", "", "| cặp | p (McNemar) | p sau Holm | kết luận ở mức 0,05 |",
              "|---|---:|---:|---|"]
        for k in sorted(p, key=lambda k: p[k]):
            L.append(f"| {k} | {p[k]:.3g} | {h[k]:.3g} | "
                     + ("**khác biệt có ý nghĩa**" if h[k] < 0.05 else "chưa kết luận được") + " |")
        L.append("")
    return L


def muc_e3(chinh: list[dict]) -> list[str]:
    """E3 trên 26 câu bộ chính — hai nhóm có dẫn chiếu tường minh. Nền là E2 (mở rộng lên Điều
    cha) cộng theo dẫn chiếu một bước; E3b là biến thể nền B, không mở rộng."""
    from eval import cham
    q26 = {r["qid"] for r in chinh if r["pp"] == "E3"}
    if not q26:
        return []
    QS = {x["qid"]: x for x in map(json.loads, open(ch.GOC / "eval/questions.jsonl"))}
    co = sorted({r["pp"] for r in chinh if r["pp"] in ("B", "B+", "E3", "E3b")})
    def cot(pp, loc=None):
        ds = sorted([r for r in chinh if r["pp"] == pp and r["qid"] in q26
                     and (loc is None or loc(r))], key=lambda r: r["qid"])
        return (ds, [cham_mot(r, "dieu")["toan_phan"] for r in ds],
                [1.0 if cham_mot(r, "dieu")["phu"] < 1 else 0.0 for r in ds],
                collections.Counter(ket_qua.phan_loai(r) for r in ds))
    def bs(a, b):
        h, lo, hi = cham.bootstrap_hieu(a, b)
        return f"{h:+.3f} [{lo:+.3f}; {hi:+.3f}]"
    L = ["", "## 3. E3 — theo dẫn chiếu tường minh, 26 câu bộ chính", "",
         "26 câu = 9 nhóm `dan_chieu` + 17 nhóm `xuyen_khoan`, đúng hai nhóm có dẫn chiếu để "
         "theo. **E3** nền E2 (mở rộng lên Điều cha), **E3b** nền B (không mở rộng).", ""]
    for ten, loc in (("Cả 26 câu", None),
                     ("Riêng 9 câu `dan_chieu`", lambda r: QS[r["qid"]]["loai"] == "dan_chieu")):
        L += [f"### {ten}", "",
              "| | n | đạt | từ chối | cắt trần | trích dẫn đúng | trả lời thiếu |",
              "|---|---:|---:|---:|---:|---:|---:|"]
        v = {}
        for pp in co:
            ds, td, thi, c = cot(pp, loc)
            if not ds:
                continue
            v[pp] = (td, thi)
            L.append(f"| {pp} | {len(ds)} | {c['dat']} | {c['tu_choi']} | {c['cat_tran']} "
                     f"| **{sum(td)/len(td):.3f}** | {sum(thi)/len(thi):.3f} |")
        L += ["", "| hiệu số | trích dẫn đúng | trả lời thiếu |", "|---|---|---|"]
        for a in ("B", "B+"):
            for b in ("E3", "E3b"):
                if a in v and b in v:
                    L.append(f"| {b} trừ {a} | {bs(v[a][0], v[b][0])} | {bs(v[a][1], v[b][1])} |")
        L.append("")
    return L


def chan_doan_e2(mc: list[dict]) -> list[str]:
    """E2 và B+ chỉ khác nhau ở CHỈ MỤC TRUY HỒI; cả hai đều mở rộng khối lên Điều cha trước khi
    sinh. Đo xem bước mở rộng có xoá sạch khác biệt do phân đoạn ngữ nghĩa tạo ra không."""
    d = {(x["qid"], x["cau_hinh"]): x for x in mc}
    qs = sorted({x["qid"] for x in mc})
    co = [q for q in qs if (q, "E2") in d and (q, "B+") in d]
    if not co:
        return []
    giong_tl = sum(1 for q in co if d[(q, "E2")]["tra_loi"] == d[(q, "B+")]["tra_loi"])
    giong_id = sum(1 for q in co if d[(q, "E2")]["chunk_id"] == d[(q, "B+")]["chunk_id"])
    giong_tu = sum(1 for q in co if d[(q, "E2")]["so_tu_ngu_canh"] == d[(q, "B+")]["so_tu_ngu_canh"])
    return [
        f"| | trùng / {len(co)} câu |", "|---|---:|",
        f"| chunk truy hồi được (`chunk_id`) | {giong_id} |",
        f"| số từ ngữ cảnh | {giong_tu} |",
        f"| **câu trả lời, giống từng ký tự** | **{giong_tl}** |", "",
        "Truy hồi khác nhau hoàn toàn — không câu nào trùng `chunk_id`, vì E2 đọc chỉ mục "
        f"`Echi_s_s0` còn B+ đọc `B_s0`. Nhưng **{giong_tl}/{len(co)} câu trả lời giống nhau từng "
        "ký tự**: cả hai đều mở rộng khối lên **Điều cha**, mà tập Điều cha thì trùng nhau, nên "
        "chữ đưa cho mô hình là một. Giải mã tham lam (temperature 0) cho ra đúng cùng câu.", "",
        "**Bước mở rộng lên Điều cha xoá sạch khác biệt do phân đoạn ngữ nghĩa tạo ra.** E2 như "
        "đang thiết kế không thể khác B+ một cách đo được — đây là giới hạn của thiết kế, không "
        "phải của dữ liệu.", ""]


def main() -> None:
    argparse.ArgumentParser(description=__doc__,
                            formatter_class=argparse.RawDescriptionHelpFormatter).parse_args()
    t0 = time.monotonic()
    nap_so_hieu_chunk(sorted(p.name for p in ch.INDEX.iterdir() if p.is_dir()))
    chinh = [json.loads(l) for l in open(ch.RESULTS / "pilot_tra_loi.jsonl") if l.strip()]
    mc_p = ch.RESULTS / "manh_con_tra_loi.jsonl"
    mc = [json.loads(l) for l in open(mc_p) if l.strip()] if mc_p.exists() else []
    # Mục 1 là bảng của CẢ 110 câu → chỉ A, B, B+. E3/E3b chỉ chạy 26 câu, để riêng ở mục 3,
    # trộn vào đây sẽ thành so sánh trên hai cỡ mẫu khác nhau.
    d_chinh = [x for x in cham_bo(chinh, "pp") if x["pp"] in ("A", "B", "B+")]
    CHON = ("B", "B+", "Eduoi", "E2", "E3")
    d_mc = [x for x in cham_bo(mc, "cau_hinh") if x["pp"] in CHON] if mc else []
    d_mc.sort(key=lambda x: CHON.index(x["pp"]))

    with open(CSV_RA, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["bo"] + list(d_chinh[0]))
        w.writeheader()
        for bo, ds in (("chinh", d_chinh), ("manh_con", d_mc)):
            for d in ds:
                w.writerow({"bo": bo, **d})

    L = [f"# Độ chính xác trích dẫn — {time.strftime('%Y-%m-%d %H:%M')}", "",
         "Sinh bằng `python -m eval.cham_trich_dan`. Số thô: `results/metrics_trich_dan.csv`.", "",
         "Bộ bóc trích dẫn đã kiểm với **nhãn tay 120 dòng, độ khớp 0,825** "
         "(`results/kiem_regex_trich_dan.md`) — mọi con số dưới đây mang sẵn sai số đó.", "",
         "*đúng toàn phần* = phủ hết gold, không thừa; *độ phủ* = tỉ lệ đơn vị gold được trích; "
         "*độ chính xác* = tỉ lệ trích dẫn trỏ đúng gold. Cột cuối là *đúng toàn phần* khi so "
         "tới cấp **khoản** thay vì chỉ cấp **Điều**.", "",
         "## 1. Bộ chính — 110 câu × 3 biến thể", ""] + bang(d_chinh, "biến thể")
    if d_mc:
        L += ["", "## 2. manh_con — 35 câu", ""] + bang(d_mc, "cấu hình")
        L += ["", "### Cắt trần — E2 cạnh B+", "",
              "Đặc tả E2 sửa ngày 26/10: chỉ chép câu dẫn của **Điều**, không chép câu dẫn của "
              "**khoản**. Lý do là mc031: mọi cấu hình bật `dan_khoan` đều chạm trần MAX_TOKENS "
              "ở câu đó (5/5), mọi cấu hình tắt nó thì không (5/5); `dan_dieu` không phân biệt "
              "được hai nhóm.", ""]
        cat = {x["cau_hinh"]: [y["qid"] for y in mc
                               if y["cau_hinh"] == x["cau_hinh"] and y.get("cat_tran")]
               for x in mc}
        L += ["| cấu hình | cắt trần | câu nào |", "|---|---:|---|"]
        for pp in ("B", "B+", "Eduoi", "E2"):
            ds = cat.get(pp, [])
            L.append(f"| {pp} | {len(ds)} | " + (", ".join(ds) if ds else "*(không có)*") + " |")
        L += ["", "E2 và B+ cùng **0 ca** — cả hai đều không chép câu dẫn khoản vào ngữ cảnh.", ""]
        L += ["", "### E2 trùng B+ — ghi lại như một kết quả âm", ""] + chan_doan_e2(mc)
    else:
        L += ["", "## 2. manh_con", "", "*(chưa có — E2 đang sinh)*"]
    L += kiem_dinh(chinh, mc) + muc_e3(chinh)
    MD_RA.write_text("\n".join(L) + "\n")
    print(f"→ {CSV_RA}\n→ {MD_RA}  ({time.monotonic()-t0:.0f}s)")
    for d in d_chinh + d_mc:
        print(f"  {d['pp']:7s} n={d['n']:3d}  đúng toàn phần={d['dieu_toan_phan']:.3f}  "
              f"phủ={d['dieu_phu']:.3f}  chính xác={d['dieu_chinh_xac']:.3f}")


if __name__ == "__main__":
    main()
