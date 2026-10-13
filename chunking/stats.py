"""Thống kê chunk của từng phương pháp → results/buoc3/thong_ke_chunk.md + .json

Cho mỗi phương pháp (seed 0) — đúng yêu cầu của đề: tổng số chunk, trung vị / lớn nhất / nhỏ nhất số từ, tỷ lệ
chunk rơi vào fallback, số văn bản bị mất chunk (phải = 0). Thêm: % chunk vượt 512 token (đếm bằng tokenizer
thật của halong_embedding, trên đúng chuỗi đem nhúng = tiền tố + nội dung) — phần vượt bị CẮT khi nhúng;
số từ tiền tố trung bình; độ phủ văn bản (ký tự không trắng thuộc ít nhất một chunk).

    python -m chunking.stats
"""
import argparse
import json
import re
import statistics as st

import cau_hinh as ch
from chunking.base import doc_jsonl, nap_van_ban
from chunking.chay import PHUONG_PHAP, ten_tep

RA = ch.RESULTS / "buoc3"
RE_DONG_NHAY = re.compile(r'"[.;,:]*(\s*\./\.)?$')


def khoi_trich_dan_doc_lap(text: str) -> list[tuple[int, int]]:
    """Dò khối trích dẫn nguyên văn theo cách KHÁC với structural.dong_trich_dan (để kiểm chéo): mở ở dòng bắt đầu bằng
    dấu " (hoặc có ': "' với số dấu nháy lẻ), đóng ở dòng kết thúc bằng "[.;,:]* (có thể ngay dòng mở), cắt ở tiêu đề Điều
    kế tiếp của văn bản (số = Điều trước + 1). Trả [(đầu, cuối)) theo vị trí ký tự."""
    from chunking.structural import RE_DIEU, _dong
    ra, mo, dieu = [], None, 0
    for a, b, x in _dong(text):
        st_ = x.strip()
        m = RE_DIEU.match(st_)
        if mo is not None and m and int(m.group(1)) == dieu + 1:
            ra.append((mo, a))
            mo = None
        if mo is None:
            if m:
                dieu = int(m.group(1))
            if st_.startswith('"') or (': "' in st_ and st_.count('"') % 2):
                if st_.startswith('"') and len(st_) > 1 and RE_DONG_NHAY.search(st_):
                    ra.append((a, b))
                else:
                    mo = a
        elif RE_DONG_NHAY.search(st_):
            ra.append((mo, b))
            mo = None
    if mo is not None:
        ra.append((mo, len(text)))
    return ra


def don_vi_theo_cay(doc) -> tuple[dict[tuple, tuple[int, int]], set] | None:
    """Đáp án ĐỘC LẬP với B: vị trí thật của từng (Điều, khoản, điểm) lấy từ cây cấu trúc vbpl.vn (data/raw/<id>.cay.json).
    Node có dòng đầu nội dung → tìm tuần tự trong text sạch (đầu dòng). Node chỉ có tham chiếu ("$2" — nội dung nằm ở
    gói khác của luồng RSC) thì không định vị được. Trả ({nhãn: (đầu, cuối)} cho đơn vị biết chắc cả đầu lẫn cuối,
    tập mọi nhãn có trong cây)."""
    import ast
    import unicodedata
    p = ch.RAW / f"{doc.doc_id}.cay.json"
    if not p.exists():
        return None
    cay = json.loads(p.read_text())
    t = doc.text
    dau_dong = [0] + [i + 1 for i, x in enumerate(t) if x == "\n"]
    nut = []  # (cấp, nhãn, vị trí)
    vt = 0

    def chuan(x: str) -> str:
        x = unicodedata.normalize("NFC", x).replace("\u00d0", "Đ")
        for a, b in (("“", '"'), ("”", '"'), ("‘", "'"), ("’", "'")):
            x = x.replace(a, b)
        return " ".join(x.split())

    def di(n, dieu=None, khoan=None):
        nonlocal vt
        lv = n.get("level")
        nd = n.get("content") or {}
        if isinstance(nd, str):
            try:
                nd = ast.literal_eval(nd)
            except (ValueError, SyntaxError):
                nd = {}
        nd = nd.get("content", "") if isinstance(nd, dict) else ""
        dong1 = chuan(re.split(r"<br\s*/?>", nd)[0])[:40]
        m = re.match(r"^(?:Điều|Khoản|Điểm)\s+(\d+[a-zđ]?|[a-zđ])\b", n.get("title") or "")
        so = m.group(1) if m else None
        if lv == "Article":
            dieu, khoan, nhan = so, None, (so, None, None)
        elif lv == "Clause":
            khoan, nhan = so, (dieu, so, None)
        elif lv == "Point":
            nhan = (dieu, khoan, so)
        else:
            nhan = None
        if nhan:
            i = None
            if dong1 and not dong1.startswith("$"):
                i = next((a for a in dau_dong if a >= vt and chuan(t[a:a + 80]).startswith(dong1)), None)
            nut.append((nhan, i))
            if i is not None:
                vt = i + 1
        for c in n.get("children") or []:
            di(c, dieu, khoan)

    for n in (cay if isinstance(cay, list) else [cay]):
        di(n)
    # cuối của mỗi đơn vị = đầu của đơn vị kế tiếp cùng cấp hoặc cấp cao hơn
    cap = lambda k: 3 - sum(x is None for x in k)
    ra = {}
    for j, (k, a) in enumerate(nut):
        sau = next(((k2, a2) for k2, a2 in nut[j + 1:] if cap(k2) <= cap(k)), (None, len(t)))
        if a is not None and sau[1] is not None:
            ra[k] = (a, sau[1])
    return ra, {k for k, _ in nut}


def kiem_nhan_theo_cay(docs, cs, nhom: str = "sua_doi") -> dict:
    """Tỉ lệ chunk gán nhãn SAI so với cây vbpl.vn: nhãn (Điều, khoản, điểm) của chunk không có trong cây, hoặc đơn vị thật
    đó không chồng lên chunk. Chỉ xét chunk có nhãn Điều; nhãn có trong cây nhưng không định vị được → "không kiểm"."""
    vb = {d.doc_id: d for d in docs if d.nhom == nhom}
    dv = {k: don_vi_theo_cay(d) for k, d in vb.items()}
    tong = sai = khong_kiem = 0
    vi_du = []
    for c in cs:
        if c.doc_id not in vb or c.dieu_so is None or not dv[c.doc_id] or not dv[c.doc_id][1]:
            continue
        nhan_dieu = c.tien_to.split("> Điều ", 1)[1].split(".")[0].split(" ")[0] if "> Điều " in c.tien_to else str(c.dieu_so)
        k = (nhan_dieu, None if c.khoan_so is None else str(c.khoan_so), c.diem)
        vi_tri, co = dv[c.doc_id]
        cha = (k[0], k[1], None) if k[2] else (k[0], None, None)
        cay_du = k == cha or any(x[:2] == cha[:2] and x != cha and (k[2] is None or x[2]) for x in co)
        if (k in co and k not in vi_tri) or (k not in co and not cay_du):
            khong_kiem += 1  # có trong cây nhưng không định vị được, hoặc cây thiếu cấp con của Điều/khoản cha
            continue
        tong += 1
        sp = vi_tri.get(k)
        if sp is None or not (sp[0] < c.end and c.start < sp[1]):
            sai += 1
            if len(vi_du) < 3:
                vi_du.append(f"{c.so_hieu} — {c.tien_to.split(' > ', 1)[-1]}: {vb[c.doc_id].text[c.start:c.start + 70]}")
    return {"tong": tong, "sai": sai, "ti_le": sai / tong if tong else 0.0, "khong_kiem": khong_kiem, "vi_du": vi_du}


def kiem_nhan_trich_dan(docs, cs) -> dict:
    """Văn bản sửa đổi: số chunk có nhãn (Điều / khoản / điểm) lấy từ một dòng NẰM TRONG khối trích dẫn — tức nhãn của
    điều khoản được trích, không phải của văn bản đang xét."""
    from chunking.structural import RE_DIEM, RE_DIEU, RE_KHOAN, _dong
    vb = {d.doc_id: d for d in docs if d.nhom == "sua_doi"}
    tong = sai = 0
    vi_du = []
    for c in cs:
        if c.doc_id not in vb or c.dieu_start is None:
            continue
        tong += 1
        t = vb[c.doc_id].text
        khoi = khoi_trich_dan_doc_lap(t)
        trong = lambda v: any(a < v < b or a == v for a, b in khoi)
        dong = [(a, x) for a, _, x in _dong(t) if c.dieu_start <= a < c.end]
        nguon = [next((a for a, x in dong if RE_DIEU.match(x)), None)]
        if c.khoan_so is not None:
            nguon.append(next((a for a, x in reversed(dong) if (m := RE_KHOAN.match(x)) and m.group(1) == str(c.khoan_so)), None))
        if c.diem is not None:
            nguon.append(next((a for a, x in reversed(dong) if (m := RE_DIEM.match(x)) and m.group(1) == c.diem), None))
        if any(v is not None and trong(v) for v in nguon):
            sai += 1
            if len(vi_du) < 3:
                vi_du.append(f"{c.so_hieu} — {c.tien_to.split(' > ', 1)[-1]}")
    return {"tong": tong, "sai": sai, "ti_le": sai / tong if tong else 0.0, "vi_du": vi_du}


def so(n) -> str:
    return f"{n:,.0f}".replace(",", ".")


def do_phu(docs, cs) -> tuple[int, int]:
    """(số ký tự không trắng của toàn tập, số ký tự không trắng KHÔNG thuộc chunk nào)."""
    theo = {}
    for c in cs:
        theo.setdefault(c.doc_id, []).append((c.start, c.end))
    tong = thieu = 0
    for d in docs:
        co = bytearray(len(d.text))
        for a, b in theo.get(d.doc_id, []):
            co[a:b] = b"\x01" * (b - a)
        for i, x in enumerate(d.text):
            if not x.isspace():
                tong += 1
                thieu += not co[i]
    return tong, thieu


def main() -> None:
    argparse.ArgumentParser(description=__doc__).parse_args()
    from transformers import AutoTokenizer

    tok = AutoTokenizer.from_pretrained(str(ch.MO_HINH_NHUNG))
    docs = nap_van_ban()
    nhom = {d.doc_id: d.nhom for d in docs}
    bang, js = [], {}
    for pp in PHUONG_PHAP:
        if not ten_tep(pp, 0).exists():
            print("chưa có:", ten_tep(pp, 0).name)  # D chỉ có sau khi đã nhúng câu
            continue
        cs = doc_jsonl(ten_tep(pp, 0))
        n = [c.n_words for c in cs]
        ntok = [len(x) for x in tok([c.text for c in cs], add_special_tokens=True)["input_ids"]]
        mat = len({d.doc_id for d in docs} - {c.doc_id for c in cs})
        tong, thieu = do_phu(docs, cs)
        tt = [len(c.tien_to.split()) for c in cs]
        r = {"so_chunk": len(cs), "trung_vi_tu": st.median(n), "max_tu": max(n), "min_tu": min(n),
             "tb_tu": sum(n) / len(n), "ti_le_fallback": sum(c.fallback for c in cs) / len(cs),
             "vb_mat_chunk": mat, "vuot_512": sum(t > 512 for t in ntok), "ti_le_vuot_512": sum(t > 512 for t in ntok) / len(cs),
             "trung_vi_token": st.median(ntok), "max_token": max(ntok), "tb_tu_tien_to": sum(tt) / len(tt),
             "ky_tu_khong_phu": thieu, "ky_tu_tong": tong,
             "chunk_duoi_50_tu": sum(x < 50 for x in n)}
        if pp == "B":
            r["theo_nhom_fallback"] = {g: f"{sum(c.fallback for c in cs if nhom[c.doc_id] == g)}/"
                                          f"{sum(1 for c in cs if nhom[c.doc_id] == g)}" for g in sorted(set(nhom.values()))}
            r["tang"] = {"ca_dieu": sum(c.dieu_so is not None and c.khoan_so is None for c in cs),
                         "khoan": sum(c.khoan_so is not None and c.diem is None for c in cs),
                         "diem": sum(c.diem is not None for c in cs),
                         "ngoai_dieu": sum(c.dieu_so is None and not c.fallback for c in cs),
                         "fallback": sum(c.fallback for c in cs)}
        js[pp] = r
        bang.append(f"| {pp} | {so(r['so_chunk'])} | {r['trung_vi_tu']:.0f} | {r['max_tu']} | {r['min_tu']} | "
                    f"{r['ti_le_fallback']:.1%} | {mat} | {r['vuot_512']} ({r['ti_le_vuot_512']:.1%}) | "
                    f"{r['tb_tu_tien_to']:.0f} | {thieu} |")
    # độ dao động theo seed (số chunk)
    # nhãn Điều/khoản/điểm của B: đối chiếu cây cấu trúc vbpl.vn (độc lập) + bộ dò khối trích dẫn mở/đóng
    b0c = doc_jsonl(ten_tep("B", 0))
    nhan = {g: kiem_nhan_theo_cay(docs, b0c, g) for g in ("luat", "nd_tt", "sua_doi", "vbhn")}
    trich = kiem_nhan_trich_dan(docs, b0c)
    seeds = {pp: {s: len(doc_jsonl(ten_tep(pp, s))) for s in sd} for pp, (_, sd) in PHUONG_PHAP.items() if len(sd) > 1}
    # B chỉ được nhúng một lần: bằng chứng là các seed chỉ khác seed 0 ở cửa sổ fallback
    b0 = {c.text for c in doc_jsonl(ten_tep("B", 0))}
    b_khac = {}
    for s in ch.SEEDS:
        cs = doc_jsonl(ten_tep("B", s))
        k = [c for c in cs if c.text not in b0]
        b_khac[s] = {"so_chunk": len(cs), "trung_seed0": len(cs) - len(k), "khac": len(k), "khac_fallback": sum(c.fallback for c in k)}
    b = js["B"]
    L = ["# Thống kê chunk (bước 3)", "",
         f"Tập: {len(docs)} văn bản (`data/manifest.csv`). Seed 0 = cửa sổ bắt đầu từ từ đầu tiên (đúng đề).", "",
         "| Phương pháp | Số chunk | Trung vị từ | Max từ | Min từ | Fallback | VB mất chunk | Vượt 512 token | Từ tiền tố TB | Ký tự không phủ |",
         "|---|---|---|---|---|---|---|---|---|---|", *bang, "",
         "- **Số từ** tính trên phần nội dung (không tính tiền tố). **Vượt 512 token**: đếm bằng tokenizer của "
         "halong_embedding trên chuỗi đem nhúng (tiền tố + nội dung) — phần vượt bị cắt mất khi nhúng.",
         "- **Ký tự không phủ** = ký tự không trắng của văn bản không thuộc chunk nào (phải = 0: không để mất văn bản).",
         "- C (theo dấu câu) và D (theo ngữ nghĩa) là hai baseline của đề cương, cùng họ không nhìn cấu trúc với A; chỉ đo truy hồi.",
         "- A+, A_H, B− là đối chứng chỉ đo truy hồi; B+ dùng chính chunk của B.",
         f"- B: ngưỡng {ch.DIEU_TOI_DA} từ đo từ dòng \"Điều N\"; dòng tiêu đề Chương/Mục đứng ngay trước được gắn vào đầu "
         "chunk (để không mất ký tự nào) nhưng không tính vào ngưỡng — vì vậy số từ lớn nhất của B có thể nhỉnh hơn ngưỡng.", "",
         "## B theo tầng", "",
         f"- Cả Điều (≤ {ch.DIEU_TOI_DA} từ): {so(b['tang']['ca_dieu'])} chunk; tách theo khoản: {so(b['tang']['khoan'])}; "
         f"tách tiếp theo điểm: {so(b['tang']['diem'])}; ngoài Điều (phần đầu văn bản, chú thích VBHN): "
         f"{so(b['tang']['ngoai_dieu'])}; fallback (văn bản không có Điều): {b['tang']['fallback']}.",
         f"- Chunk dưới 50 từ: B {so(b['chunk_duoi_50_tu'])} ({b['chunk_duoi_50_tu'] / b['so_chunk']:.1%}) — so với A "
         f"{js['A']['chunk_duoi_50_tu']} (chỉ là đuôi văn bản). Đây là dữ liệu cho nhược điểm 6 (chunk quá nhỏ mất ngữ cảnh).",
         "- Fallback theo nhóm (chunk fallback / tổng chunk của nhóm): "
         + ", ".join(f"{g}: {v}" for g, v in b["theo_nhom_fallback"].items()), "",
         "## Số chunk theo seed", "", "| Phương pháp | " + " | ".join(f"seed {s}" for s in (0,) + ch.SEEDS) + " |",
         "|---|" + "---|" * (1 + len(ch.SEEDS))]
    L += [f"| {pp} | " + " | ".join(so(v) for v in d.values()) + " |" for pp, d in seeds.items()]
    L += ["", f"- **B không phụ thuộc seed:** số chunk qua 4 seed chỉ lệch {max(seeds['B'].values()) - min(seeds['B'].values())} "
          f"trên {so(seeds['B'][0])}; " + "; ".join(f"seed {s}: {so(v['trung_seed0'])}/{so(v['so_chunk'])} chunk trùng nguyên văn "
          f"seed 0, {v['khac']} chunk khác ({v['khac_fallback']}/{v['khac']} là cửa sổ fallback của văn bản không có Điều)"
          for s, v in b_khac.items()) + ". Vì vậy B và B− chỉ nhúng một lần (seed 0).",
          "- **A trần** chạy 4 seed, chỉ đo truy hồi (không sinh câu trả lời), để chứng minh dịch điểm bắt đầu cửa sổ "
          "chỉ là nhiễu. A+, A_H, B−, B+ và khâu sinh: một seed (0)."]
    L += ["", "## Nhãn Điều/khoản/điểm của B có đúng không", "",
          "Đối chiếu với cây cấu trúc của chính vbpl.vn (`data/raw/<id>.cay.json`, độc lập với regex của B): chunk sai "
          "khi đơn vị nó mang nhãn không tồn tại trong cây hoặc không chồng lên chunk. Chunk có nhãn mà cây thiếu node "
          "(node chỉ là tham chiếu \"$n\", hoặc cây không có cấp con) ghi là không kiểm được.", "",
          "| Nhóm | Sai / kiểm được | Tỉ lệ sai | Không kiểm được |", "|---|---|---|---|"]
    L += [f"| {g} | {r['sai']} / {r['tong']} | {r['ti_le']:.1%} | {r['khong_kiem']} |" for g, r in nhan.items()]
    L += ["", f"- Văn bản sửa đổi, đo bằng bộ dò khối trích dẫn mở/đóng (cách thứ hai): {trich['sai']}/{trich['tong']} "
          f"chunk ({trich['ti_le']:.1%}) có nhãn lấy từ dòng nằm trong trích dẫn.",
          "- B bỏ qua dòng nằm trong khối trích dẫn nguyên văn khi dò Điều/khoản/điểm (chunking/structural.py, "
          "dong_trich_dan). Trước khi sửa: sửa đổi 35,7% theo cây, 52,0% theo bộ dò mở/đóng (commit trước)."]
    RA.mkdir(parents=True, exist_ok=True)
    (RA / "thong_ke_chunk.md").write_text("\n".join(L) + "\n")
    (RA / "thong_ke_chunk.json").write_text(json.dumps({"seed0": js, "theo_seed": seeds, "b_khac_seed0": b_khac, "nhan_theo_cay": nhan, "nhan_trich_dan": trich}, ensure_ascii=False, indent=1))
    print("\n".join(L))


if __name__ == "__main__":
    main()
