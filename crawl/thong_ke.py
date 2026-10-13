"""Thống kê tập dữ liệu đã chọn (data/manifest.csv) → results/buoc2/thong_ke_du_lieu.md + .json.

Gồm: số văn bản theo nhóm/loại, số từ, số Điều, Điều dài; tỷ lệ tiêu đề Điều bị vỡ trước/sau chuẩn hoá
(kèm ví dụ thật); số "Điều" nằm trong khối trích dẫn của văn bản sửa đổi; phần đã bỏ (Căn cứ, Nơi nhận,
chữ ký, Phụ lục). Mọi con số tính từ file, không viết tay.

    python -m crawl.thong_ke
"""
import argparse
import csv
import json
import re
import statistics as st

import cau_hinh as ch
from crawl.chuan_hoa import RE_TIEU_DE_B, _chuan_ky_tu, dieu_ky_vong, text_tho, trong_ngoac

RA = ch.RESULTS / "buoc2"
TEN_NHOM = {"luat": "Luật, Bộ luật", "nd_tt": "Nghị định, Thông tư", "khong_dieu": "Không có \"Điều\"",
            "sua_doi": "Sửa đổi, bổ sung", "vbhn": "Văn bản hợp nhất"}


def so(n: float) -> str:
    """Số kiểu Việt Nam: 1.234.567"""
    return f"{n:,.0f}".replace(",", ".")


def pct(a: int, b: int) -> str:
    return f"{a / b:.2%}" if b else "—"


def vi_du_vo(doc_id: str, toi_da: int = 2) -> list[dict]:
    """Tiêu đề Điều kỳ vọng mà regex của B không bắt được trên text THÔ — trích vài dòng quanh chỗ vỡ."""
    html = (ch.RAW / f"{doc_id}.html").read_text()
    tho = _chuan_ky_tu(text_tho(html))
    full = (ch.CLEAN_FULL / f"{doc_id}.txt").read_text()
    kv, _ = dieu_ky_vong(doc_id, full)
    bat = {int(m.group(1)) for x in tho.split("\n") if (m := RE_TIEU_DE_B.match(x))}  # khớp TỪNG DÒNG như bộ đếm
    ra = []
    dong = tho.split("\n")
    for so in sorted(set(kv) - bat)[:toi_da]:
        for i, x in enumerate(dong):
            ke = dong[i + 1] if i + 1 < len(dong) else ""
            if (x == "Điều" and re.match(rf"{so}\b", ke)) or re.fullmatch(rf"Điều\s+{so}\s*[.:]?", x):
                ra.append({"dieu": so, "doan": dong[i:i + 3]})
                break
    return ra


def main() -> None:
    argparse.ArgumentParser(description=__doc__).parse_args()
    tk = {d["id"]: d for d in map(json.loads, (ch.DATA / "thong_ke_chuan_hoa.jsonl").read_text().splitlines())}
    ds = list(csv.DictReader(open(ch.MANIFEST)))
    for d in ds:
        d.update(tk[d["id"]])
    RA.mkdir(parents=True, exist_ok=True)
    L = ["# Thống kê tập dữ liệu (bước 2)", "",
         f"Nguồn: vbpl.vn (CSDL quốc gia về pháp luật). Tập chọn: `data/manifest.csv` — **{len(ds)} văn bản**, "
         f"{so(sum(d['so_tu'] for d in ds))} từ (sau chuẩn hoá, đã bỏ Căn cứ/Nơi nhận/chữ ký/Phụ lục).", "",
         "## Theo nhóm", "",
         "| Nhóm | Số VB | Tổng từ | Trung vị từ/VB | Số Điều | VB có Chương | VB có Điều > 1500 từ |",
         "|---|---|---|---|---|---|---|"]
    for k, ten in TEN_NHOM.items():
        g = [d for d in ds if d["nhom"] == k]
        if not g:
            continue
        L.append(f"| {ten} | {len(g)} | {so(sum(d['so_tu'] for d in g))} | {so(st.median(d['so_tu'] for d in g))} | "
                 f"{so(sum(d['so_dieu'] for d in g))} | {sum(d['co_chuong'] for d in g)} | "
                 f"{sum(d['dieu_dai'] == 'True' for d in g)} |")
    L.append(f"| **Tổng** | **{len(ds)}** | **{so(sum(d['so_tu'] for d in ds))}** | {so(st.median(d['so_tu'] for d in ds))} | "
             f"{so(sum(d['so_dieu'] for d in ds))} | {sum(d['co_chuong'] for d in ds)} | "
             f"{sum(d['dieu_dai'] == 'True' for d in ds)} |")
    L += ["", "Nhãn phụ: **Điều dài** = có ít nhất một Điều > 1500 từ (không tính văn bản sửa đổi, vì Điều 1 của chúng "
          "dài do trích nguyên văn điều bị sửa); **họ phiên bản** = VBHN + văn bản gốc + văn bản sửa đổi được hợp nhất.", "",
          "## Theo loại văn bản", "", "| Loại | Số VB |", "|---|---|"]
    loai: dict[str, int] = {}
    for d in ds:
        loai[d["loai_van_ban"]] = loai.get(d["loai_van_ban"], 0) + 1
    L += [f"| {k} | {v} |" for k, v in sorted(loai.items(), key=lambda x: -x[1])]
    ho = sorted({d["ho"] for d in ds if d["ho"]})
    L += ["", f"## Họ phiên bản ({len(ho)})", "", "| VBHN | Văn bản gốc | Văn bản sửa đổi |", "|---|---|---|"]
    for h in ho:
        tv = [d for d in ds if d["ho"] == h]
        L.append(f"| {next(d['so_hieu'] for d in tv if d['vai_trong_ho'] == 'hop_nhat')} | "
                 f"{', '.join(d['so_hieu'] for d in tv if d['vai_trong_ho'] == 'goc')} | "
                 f"{', '.join(d['so_hieu'] for d in tv if d['vai_trong_ho'] == 'sua_doi')} |")

    # ── tiêu đề Điều bị vỡ ──
    co = [d for d in ds if d["truoc"]["ky_vong"]]
    kv = sum(d["truoc"]["ky_vong"] for d in co)
    vt, vs = sum(d["truoc"]["thieu"] for d in co), sum(d["sau"]["thieu"] for d in co)
    L += ["", "## Tiêu đề Điều bị vỡ — trước và sau chuẩn hoá", "",
          "- **Kỳ vọng**: số Điều theo cây cấu trúc do vbpl.vn biên tập (nguồn độc lập với bộ phân đoạn B); "
          "văn bản không có cây thì lấy dãy số Điều liên tục 1, 2, … bằng regex lỏng.",
          "- **Bắt được**: dòng khớp đúng regex tiêu đề của phương pháp B `^Điều\\s+(\\d+)\\s*[.．:]?\\s*(.*)$`, "
          "không nằm trong khối trích dẫn.",
          "- **Trước chuẩn hoá** = text crawl kiểu thông thường `get_text(\"\\n\")` (mỗi thẻ HTML một dòng); "
          "**sau** = text đã chuẩn hoá (`crawl/chuan_hoa.py`).", "",
          "| Nhóm | VB có Điều | Điều kỳ vọng | Vỡ trước | Tỷ lệ trước | Vỡ sau | Tỷ lệ sau | VB còn vỡ |",
          "|---|---|---|---|---|---|---|---|"]
    for k, ten in TEN_NHOM.items():
        g = [d for d in co if d["nhom"] == k]
        if not g:
            continue
        a, b = sum(d["truoc"]["ky_vong"] for d in g), sum(d["truoc"]["thieu"] for d in g)
        c = sum(d["sau"]["thieu"] for d in g)
        L.append(f"| {ten} | {len(g)} | {a} | {b} | {pct(b, a)} | {c} | {pct(c, a)} | "
                 f"{sum(d['sau']['thieu'] > 0 for d in g)} |")
    L.append(f"| **Tổng** | **{len(co)}** | **{kv}** | **{vt}** | **{pct(vt, kv)}** | **{vs}** | **{pct(vs, kv)}** | "
             f"{sum(d['sau']['thieu'] > 0 for d in co)} |")
    nguon = {}
    for d in co:
        nguon[d["nguon_ky_vong"]] = nguon.get(d["nguon_ky_vong"], 0) + 1
    L += ["", f"Nguồn số Điều kỳ vọng: {', '.join(f'{k} = {v} VB' for k, v in nguon.items())}."]
    vd = [(d, vi_du_vo(d["id"])) for d in co if d["truoc"]["thieu"]]
    vd = [(d, v) for d, v in vd if v][:4]
    if vd:
        L += ["", "Ví dụ tiêu đề vỡ trong text thô (dòng ⏎ là chỗ bị xuống dòng):", ""]
        for d, v in vd:
            for x in v[:1]:
                L.append(f"- {d['so_hieu']} — Điều {x['dieu']}: `{' ⏎ '.join(x['doan'])[:200]}`")
    # toàn bộ ứng viên đã tải (không chỉ tập chọn) — để thấy tần suất thật của lỗi khi crawl vbpl.vn
    tat = [d for d in tk.values() if d["truoc"]["ky_vong"]]
    a = sum(d["truoc"]["ky_vong"] for d in tat)
    b, c = sum(d["truoc"]["thieu"] for d in tat), sum(d["sau"]["thieu"] for d in tat)
    L += ["", f"Trên **toàn bộ {len(tk)} văn bản ứng viên đã tải** (không chỉ tập chọn): {a} Điều kỳ vọng; vỡ trước "
          f"**{b} ({pct(b, a)})** ở {sum(d['truoc']['thieu'] > 0 for d in tat)} VB, sau **{c} ({pct(c, a)})**. "
          "Các văn bản gốc có tiêu đề vỡ được đưa hết vào tập chọn (nhãn `tieu_de_vo`)."]
    con = [d for d in co if d["sau"]["thieu"]]
    if con:
        L += ["", "Văn bản còn tiêu đề vỡ sau chuẩn hoá: " + ", ".join(f"{d['so_hieu']} ({d['sau']['thieu']})" for d in con)]

    # ── Điều trong ngoặc trích dẫn (văn bản sửa đổi) ──
    sd = [d for d in ds if d["nhom"] == "sua_doi"]
    L += ["", "## \"Điều\" nằm trong khối trích dẫn (văn bản sửa đổi)", "",
          "Văn bản sửa đổi trích nguyên văn điều mới của luật bị sửa trong ngoặc kép, ví dụ "
          "`\"Điều 4. … \"`. Regex của B coi các dòng này là tiêu đề Điều thật → sinh **Điều giả**.", "",
          f"- {sum(d['sau']['dieu_trong_ngoac'] > 0 for d in sd)}/{len(sd)} văn bản sửa đổi có dòng \"Điều N\" "
          f"trong khối trích dẫn; tổng **{sum(d['sau']['dieu_trong_ngoac'] for d in sd)}** dòng "
          f"(so với {sum(d['sau']['ky_vong'] for d in sd)} Điều thật của chính các văn bản này).",
          f"- Dòng mở đầu bằng dấu nháy `\"Điều N …` (điều của văn bản bị sửa được trích nguyên văn): "
          f"**{sum(d['sau'].get('dieu_duoc_trich', 0) for d in sd)}** dòng ở "
          f"{sum(d['sau'].get('dieu_duoc_trich', 0) > 0 for d in sd)}/{len(sd)} VB. Regex của B không khớp các dòng này "
          "(vì có dấu nháy đứng trước) nên chúng không thành Điều giả, nhưng nội dung điều được trích nằm lẫn trong "
          "Điều của văn bản sửa đổi — dữ liệu cho nhược điểm 5 (nhiều phiên bản)."]

    # ── phần đã bỏ ──
    L += ["", "## Phần đã bỏ khi chuẩn hoá (data/clean/ so với data/clean_full/)", "",
          f"- Dòng \"Căn cứ …/Theo đề nghị …\" ở đầu: {sum(d['da_bo']['can_cu'] for d in ds)} dòng "
          f"({sum(d['da_bo']['can_cu'] > 0 for d in ds)} VB)",
          f"- Nơi nhận: {sum(d['da_bo']['noi_nhan'] for d in ds)} dòng; khối chữ ký: {sum(d['da_bo']['chu_ky'] for d in ds)} dòng "
          f"({sum((d['da_bo']['noi_nhan'] + d['da_bo']['chu_ky']) > 0 for d in ds)} VB)",
          f"- Khối Nơi nhận/chữ ký nằm GIỮA văn bản (quyết định ban hành kèm quy chế, khối xác thực VBHN): "
          f"{sum(d['da_bo'].get('khoi_giua', 0) for d in ds)} khối",
          f"- Trong đó Phụ lục (mẫu đơn, bảng biểu sau chữ ký): {so(sum(d['da_bo'].get('phu_luc_tu', 0) for d in ds))} từ "
          f"({sum(d['da_bo'].get('phu_luc_tu', 0) > 0 for d in ds)} VB) — không thuộc phạm vi thực nghiệm",
          "- Văn bản không có Phần/Chương/Điều (công văn, chỉ thị…): KHÔNG bỏ dòng \"Căn cứ\" vì ở đây nó là nội dung."]
    (RA / "thong_ke_du_lieu.md").write_text("\n".join(L) + "\n")
    (RA / "thong_ke_du_lieu.json").write_text(json.dumps(
        {"so_van_ban": len(ds), "tong_tu": sum(d["so_tu"] for d in ds), "dieu_ky_vong": kv, "vo_truoc": vt,
         "vo_sau": vs, "theo_van_ban": [{k: d[k] for k in ("id", "so_hieu", "nhom", "truoc", "sau", "so_tu", "so_dieu",
                                                            "dieu_dai_nhat", "da_bo")} for d in ds]},
        ensure_ascii=False, indent=1))
    print("→", RA / "thong_ke_du_lieu.md")


if __name__ == "__main__":
    main()
