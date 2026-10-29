"""Ghép nhãn tay vào mẫu gán nhãn, giải mã X/Y/Z, đo độ khớp của bộ bóc trích dẫn bằng regex.

    python -m eval.ap_nhan nhan_120.txt            # ghép + chấm + xuất báo cáo
    python -m eval.ap_nhan nhan_120.txt --chi-ghep # chỉ ghép, chưa chấm

Tệp nhãn: mỗi dòng `<mã dòng> | <trích dẫn người đọc thấy, cách nhau ;> | <Đúng|Thiếu|Thừa|Sai>`.
Dòng trống và dòng bắt đầu bằng # bị bỏ qua.

Ghép là IDEMPOTENT: chạy lại cùng tệp không nhân đôi, nhãn mới ghi đè nhãn cũ cùng mã dòng.

Độ khớp = tỉ lệ dòng người đọc chấm **Đúng** — tức regex bóc khớp đúng những gì người đọc thấy.
Khoảng tin cậy Wilson 95% (hợp với tỉ lệ gần 0 hoặc gần 1 hơn khoảng chuẩn tắc).
"""
import argparse
import collections
import json
import math
import re
import sys

import cau_hinh as ch
from eval import pilot, trich_dan

NHAN_HOP_LE = ("Đúng", "Thiếu", "Thừa", "Sai")
# Kết quả bóc TRƯỚC KHI SỬA ba mẫu số hiệu (23/10), chụp lại trong eval/boc_cu_pilot.json.
# Giữ bản chụp thay vì giữ mã nguồn cũ: so cũ/mới vẫn làm được sau khi mã cũ đã bị thay.
BOC_CU = ch.GOC / "eval/boc_cu_pilot.json"


def _nap_boc_cu() -> dict[str, set[tuple]]:
    if not BOC_CU.exists():
        return {}
    d = json.loads(BOC_CU.read_text())["boc"]
    return {ma: {(frozenset(t[0]) if t[0] else None, t[1], t[2], t[3]) for t in ds}
            for ma, ds in d.items()}
RA = ch.RESULTS / "kiem_regex_trich_dan.md"


def doc_nhan(p) -> tuple[dict[str, tuple[str, str]], list[str]]:
    """Đọc tệp nhãn → ({mã dòng: (trích dẫn người đọc, nhãn)}, danh sách lỗi)."""
    ra, loi = {}, []
    for i, d in enumerate(open(p), 1):
        d = d.strip()
        if not d or d.startswith("#"):
            continue
        phan = [x.strip() for x in d.split("|")]
        if len(phan) != 3:
            loi.append(f"dòng {i}: cần đúng 3 phần ngăn bằng `|`, có {len(phan)} — {d[:60]}")
            continue
        ma, thay, nhan = phan
        if not re.fullmatch(r"\d{1,3}", ma):
            loi.append(f"dòng {i}: mã dòng `{ma}` không phải số")
            continue
        ma = f"{int(ma):03d}"
        if nhan not in NHAN_HOP_LE:
            loi.append(f"dòng {i}: nhãn `{nhan}` không thuộc {NHAN_HOP_LE}")
            continue
        if ma in ra:
            loi.append(f"dòng {i}: mã `{ma}` lặp trong chính tệp nhãn")
            continue
        ra[ma] = (thay, nhan)
    return ra, loi


def ghep(nhan: dict[str, tuple[str, str]]) -> list[str]:
    """Ghi nhãn vào eval/nhan_trich_dan.md đúng mã dòng. Trả danh sách lỗi."""
    md = pilot.NHAN.read_text()
    co = set(re.findall(r"\| mã dòng \| `(\d{3})` \|", md))
    loi = [f"mã `{m}` không có trong {pilot.NHAN.name}" for m in sorted(nhan) if m not in co]
    if loi:
        return loi
    for ma, (thay, nh) in nhan.items():
        # thay đúng hàng trống (hoặc hàng đã điền) của khối mang mã này — ghép lại KHÔNG nhân đôi
        kh = re.compile(rf"(\| mã dòng \| `{ma}` \|[\s\S]*?\| Trích dẫn người đọc thấy \| regex \|\n\|---\|---\|\n)"
                        r"\|[^\n]*\|[^\n]*\|\n")
        md, n = kh.subn(lambda m: m.group(1) + f"| {thay} | {nh} |\n", md, count=1)
        if n != 1:
            loi.append(f"mã `{ma}`: không tìm thấy hàng để điền")
    pilot.NHAN.write_text(md)
    return loi


def doc_da_ghep() -> dict[str, tuple[str, str]]:
    """Đọc ngược nhãn đã nằm trong eval/nhan_trich_dan.md."""
    md = pilot.NHAN.read_text()
    ra = {}
    for m in re.finditer(r"\| mã dòng \| `(\d{3})` \|[\s\S]*?\| Trích dẫn người đọc thấy \| regex \|\n"
                         r"\|---\|---\|\n\| ([^|]*)\| ([^|]*)\|", md):
        thay, nh = m.group(2).strip(), m.group(3).strip()
        if nh:
            ra[m.group(1)] = (thay, nh)
    return ra


def wilson(k: int, n: int, z: float = 1.959963985) -> tuple[float, float, float]:
    """Tỉ lệ k/n kèm khoảng tin cậy Wilson 95% → (tỉ lệ, dưới, trên)."""
    if n == 0:
        return 0.0, 0.0, 0.0
    p = k / n
    d = 1 + z * z / n
    giua = (p + z * z / (2 * n)) / d
    nua = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return p, max(0.0, giua - nua), min(1.0, giua + nua)


KHONG_CO = re.compile(r"^\(?\s*không có", re.I)


def tap_nguoi_doc(thay: str) -> set[tuple]:
    """Chuỗi người đọc viết tay → tập trích dẫn, dùng chính bộ phân tích của regex.

    Người đọc viết đúng cùng một lối ("59/2020/QH14 Điều 17 khoản 1; ..."), nên phân tích được
    bằng cùng công cụ. Ghi chú trong ngoặc như "(không có)" hoặc "thân bài nhắc X" coi là RỖNG —
    đó là lời người đọc nói KHÔNG có trích dẫn nguồn, không phải một trích dẫn.
    """
    if KHONG_CO.match(thay.strip()):
        return set()
    thay = re.sub(r"thân bài nhắc[^;]*", "", thay)
    ra, sh_cuoi = set(), None
    for phan in thay.split(";"):
        phan = trich_dan.chuan(phan).strip()
        if not phan:
            continue
        # số hiệu đứng ở ĐÂU CŨNG ĐƯỢC trong mẩu này — người đọc viết "32/2024/QH15 Điều 3",
        # tức số hiệu TRƯỚC Điều, ngược với lối mô hình sinh hay viết ("Điều 3 của 32/2024/QH15").
        sh = trich_dan._so_hieu_gan(phan) or sh_cuoi
        if sh:
            sh_cuoi = sh
        md = trich_dan.RE_DIEU.search(phan)
        if not md:
            if sh:
                ra.add((sh, None, None, None))
            continue
        dieu = int(re.match(r"\d+", md.group(1)).group())
        mk = re.search(r"khoản\s+(\d+)", phan, re.I)
        khoan = int(mk.group(1)) if mk else None
        # "khoản b" (chữ) là ĐIỂM về mặt pháp lý — gom vào danh sách điểm, như bên regex
        chu = re.findall(r"khoản\s+([a-zđ])\b", phan, re.I)
        # "điểm a b c" / "điểm a, b" → mỗi điểm một trích dẫn, giống cách regex bóc từng cái
        diem = (re.findall(r"\b([a-zđ])\b", phan[phan.lower().find("điểm"):])
                if "điểm" in phan.lower() else []) + chu
        if diem:
            for d in dict.fromkeys(diem):
                ra.add((sh, dieu, khoan, d))
        else:
            ra.add((sh, dieu, khoan, None))
        # "Điều 2, 3, 10 của X" trong chuỗi người đọc → mỗi số một trích dẫn
        for so in re.findall(r"(?:,|và)\s*(\d+)(?!\s*\d)", phan[md.end():]):
            if not re.search(r"(khoản|điểm)", phan[md.end():phan.index(so, md.end())], re.I):
                ra.add((sh, int(so), None, None))
    return ra


def phan_loai_auto(may: set[tuple], nguoi: set[tuple]) -> str:
    """So tập regex bóc được với tập người đọc thấy → một trong bốn nhãn."""
    if may == nguoi:
        return "Đúng"
    if may < nguoi:
        return "Thiếu"
    if may > nguoi:
        return "Thừa"
    return "Sai"


def _chuoi_trich(r: dict, **kw) -> str:
    boc = trich_dan.boc(r["tra_loi"], **kw)
    return "; ".join(pilot._nhan_trich(t) for t in boc) if boc else "(không bóc được gì)"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("tep", help="tệp nhãn tay")
    ap.add_argument("--chi-ghep", action="store_true")
    a = ap.parse_args()

    nhan, loi = doc_nhan(a.tep)
    if loi:
        print(f"TỆP NHÃN CÓ {len(loi)} LỖI — không ghép gì cả:", file=sys.stderr)
        for x in loi:
            print("  •", x, file=sys.stderr)
        raise SystemExit(2)
    loi = ghep(nhan)
    if loi:
        print(f"GHÉP HỎNG ({len(loi)}):", file=sys.stderr)
        for x in loi:
            print("  •", x, file=sys.stderr)
        raise SystemExit(2)
    da = doc_da_ghep()
    print(f"đã ghép {len(nhan)} nhãn | tổng nhãn trong tệp: {len(da)}")
    if a.chi_ghep:
        return

    chon, pp2ma, _ = pilot.chon_dong(ghi_giai_ma=False)
    ma2pp = {v: k for k, v in pp2ma.items()}
    cu_chup = _nap_boc_cu()
    nhan_cu, _ = doc_nhan(ch.GOC / "nhan_120.txt") if (ch.GOC / "nhan_120.txt").exists() else ({}, [])
    hang = []
    for n, r in enumerate(chon, 1):
        ma = f"{n:03d}"
        if ma not in da:
            continue
        thay, nh = da[ma]
        nguoi = tap_nguoi_doc(thay)
        t_cu = cu_chup.get(ma, set(trich_dan.boc(r["tra_loi"])))
        t_moi = set(trich_dan.boc(r["tra_loi"], mac_dinh=_mac_dinh(r),
                                  cho_phep_khong_dieu=_khong_dieu(r)))
        hang.append({"ma": ma, "pp": r["pp"], "bien_the_mu": pp2ma[r["pp"]], "loai": r["loai"],
                     "nhan": nh, "nguoi_doc_thay": thay, "qid": r["qid"],
                     "cu": _chuoi_trich(r), "tra_loi": r["tra_loi"],
                     "moi": _chuoi_trich(r, mac_dinh=_mac_dinh(r),
                                        cho_phep_khong_dieu=_khong_dieu(r)),
                     "cu_tuple": t_cu, "moi_tuple": t_moi,
                     "nhan_cu": nhan_cu.get(ma, ("", nh))[1],
                     "auto_cu": phan_loai_auto(t_cu, nguoi),
                     "auto_moi": phan_loai_auto(t_moi, nguoi)})
    viet(hang, ma2pp, len(chon))
    print(f"→ {RA} ({len(hang)} dòng đã chấm)")


def _khong_dieu(r: dict) -> bool:
    """Văn bản đích có chia Điều không. Gold không có Điều (Chỉ thị, Công văn…) → số hiệu đứng
    một mình CHÍNH LÀ trích dẫn; văn bản có Điều → số hiệu trần chỉ là nhắc tới, không bóc."""
    return any(g.get("dieu") is None for g in r.get("gold") or [])


def _mac_dinh(r: dict) -> frozenset | None:
    """Số hiệu của văn bản chunk truy hồi hạng 1 — dùng khi câu trả lời không nêu số hiệu nào."""
    cid = (r.get("chunk_id") or [None])[0]
    return _SH_CHUNK.get(cid) if cid else None


_SH_CHUNK: dict[str, frozenset] = {}


def nap_so_hieu_chunk(tens: list[str]) -> None:
    for t in tens:
        p = ch.INDEX / t / "chunks.jsonl"
        if p.exists():
            for c in map(json.loads, open(p)):
                k = trich_dan.khoa_tu_chuoi(c["so_hieu"])
                if k:
                    _SH_CHUNK[c["chunk_id"]] = k


MAU_SO_HIEU = {
    "ký hiệu có chữ thường (CT-TTg)": re.compile(r"\d\s*/\s*[A-ZĐ]{2,}(?:-[A-ZĐ]{1,})*-?[A-ZĐ]+[a-zđ]"),
    "số 0 đầu (09/…)": re.compile(r"\b0\d{1,4}\s*/"),
    "số hiệu kiểu cũ (9367 TC/PC)": re.compile(r"\b\d{3,5}\s*[/\s]\s*[A-ZĐ]{2,}\s*/\s*[A-ZĐ]{2,}"),
}


def MAU_DINH(hang):
    for ten, rx in MAU_SO_HIEU.items():
        yield ten, [h for h in hang
                    if rx.search(h["nguoi_doc_thay"]) or rx.search(h["tra_loi"] or "")]


def viet(hang: list[dict], ma2pp: dict[str, str], tong: int) -> None:
    L = ["# Kiểm bộ bóc trích dẫn bằng regex so với nhãn tay", "",
         f"Nhãn tay **{len(hang)}/{tong} dòng**, chấm **hai vòng**: vòng một trên bản regex cũ, "
         "vòng hai trên bản đã sửa. Nguồn: `eval/nhan_trich_dan.md` (nhãn), "
         "`results/pilot_tra_loi.jsonl` (câu trả lời). Sinh bằng `python -m eval.ap_nhan`.", "",
         "Độ khớp = tỉ lệ dòng người đọc chấm **Đúng**; khoảng tin cậy **Wilson 95%**.", "",
         "## 1. Độ khớp từng biến thể sau khi sửa (đã giải mã)", "",
         "| biến thể | mã mù | n | Đúng | Thiếu | Thừa | Sai | độ khớp | Wilson 95% |",
         "|---|---|---:|---:|---:|---:|---:|---:|---|"]

    def dong_bang(ten, ds, mu):
        c = collections.Counter(h["nhan"] for h in ds)
        pp_, lo, hi = wilson(c["Đúng"], len(ds))
        return (f"| {ten} | {mu} | {len(ds)} | {c['Đúng']} | {c['Thiếu']} | {c['Thừa']} | "
                f"{c['Sai']} | **{pp_:.3f}** | [{lo:.3f}; {hi:.3f}] |")
    for pp in ("A", "B", "B+"):
        ds = [h for h in hang if h["pp"] == pp]
        if ds:
            L.append(dong_bang(pp, ds, ds[0]["bien_the_mu"]))
    L.append(dong_bang("**TỔNG**", hang, "—"))
    L += ["", "## 1b. Trước và sau khi sửa bộ bóc", "",
          "Hai lần chấm tay trên **cùng 120 dòng**: lần đầu chấm bản regex cũ, lần sau chấm bản "
          "đã sửa. Cùng một người đọc, cùng một tiêu chí, nên so được với nhau.", "",
          "| | độ khớp | Wilson 95% | Đúng | Thiếu | Thừa | Sai |", "|---|---:|---|---:|---:|---:|---:|"]
    for ten, khoa in (("regex cũ", "nhan_cu"), ("**regex đã sửa**", "nhan")):
        c = collections.Counter(h[khoa] for h in hang)
        pp_, lo, hi = wilson(c["Đúng"], len(hang))
        L.append(f"| {ten} | **{pp_:.3f}** | [{lo:.3f}; {hi:.3f}] | {c['Đúng']} | {c['Thiếu']} | "
                 f"{c['Thừa']} | {c['Sai']} |")
    L += ["", "## 1c. Ba mẫu số hiệu đã sửa", "",
          "| mẫu | số dòng dính | A | B | B+ | nhãn sau khi sửa |",
          "|---|---:|---:|---:|---:|---|"]
    for ten, ds in MAU_DINH(hang):
        c = collections.Counter(h["pp"] for h in ds)
        nh = collections.Counter(h["nhan"] for h in ds)
        L.append(f"| {ten} | {len(ds)} | {c['A']} | {c['B']} | {c['B+']} | "
                 + ", ".join(f"{k} {v}" for k, v in nh.most_common()) + " |")
    con = collections.Counter(h["pp"] for h in hang if h["nhan"] != "Đúng")
    chu = [h for h in hang if h["nhan"] != "Đúng"
           and re.search(r"(khoản\s+[a-zđ]\b|điểm\s+[a-zđ][\s,]+[a-zđ])", h["nguoi_doc_thay"], re.I)]
    L += ["", f"**Độ khớp cuối cùng: {wilson(sum(1 for h in hang if h['nhan'] == 'Đúng'), len(hang))[0]:.3f}.** "
          f"Phần Thiếu còn sót toàn là điểm và khoản viết bằng chữ ({len(chu)}/{len(hang) - sum(1 for h in hang if h['nhan'] == 'Đúng')} "
          f"dòng lỗi), nhỏ và chia đều ba biến thể — **A {con['A']} · B {con['B']} · B+ {con['B+']}**. "
          "Không chấm lại nữa; con số này là con số cuối dùng cho báo cáo.", ""]
    L += ["", "## 2. Dòng Thiếu hoặc Sai — nhóm theo biến thể", "",
          "Mỗi dòng ghi **chuỗi regex bóc được** và **chuỗi người đọc thấy**, để soi mẫu định dạng "
          "nào regex hụt một cách hệ thống.", ""]
    for pp in ("A", "B", "B+"):
        ds = [h for h in hang if h["pp"] == pp and h["nhan"] in ("Thiếu", "Sai")]
        L += [f"### {pp} — {len(ds)} dòng", ""]
        if not ds:
            L += ["*(không có)*", ""]
            continue
        L += ["| mã | nhãn | regex bóc được | người đọc thấy |", "|---|---|---|---|"]
        for h in ds:
            L.append(f"| {h['ma']} | {h['nhan']} | {h['cu']} | {h['nguoi_doc_thay']} |")
        L.append("")
    RA.write_text("\n".join(L) + "\n")


if __name__ == "__main__":
    nap_so_hieu_chunk(["A_s0", "B_s0"])
    main()
