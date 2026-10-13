"""Thống kê chunk của từng phương pháp → results/buoc3/thong_ke_chunk.md + .json

Cho mỗi phương pháp (seed 0) — đúng yêu cầu của đề: tổng số chunk, trung vị / lớn nhất / nhỏ nhất số từ, tỷ lệ
chunk rơi vào fallback, số văn bản bị mất chunk (phải = 0). Thêm: % chunk vượt 512 token (đếm bằng tokenizer
thật của halong_embedding, trên đúng chuỗi đem nhúng = tiền tố + nội dung) — phần vượt bị CẮT khi nhúng;
số từ tiền tố trung bình; độ phủ văn bản (ký tự không trắng thuộc ít nhất một chunk).

    python -m chunking.stats
"""
import argparse
import json
import statistics as st

import cau_hinh as ch
from chunking.base import doc_jsonl, nap_van_ban
from chunking.chay import PHUONG_PHAP, ten_tep

RA = ch.RESULTS / "buoc3"


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
    RA.mkdir(parents=True, exist_ok=True)
    (RA / "thong_ke_chunk.md").write_text("\n".join(L) + "\n")
    (RA / "thong_ke_chunk.json").write_text(json.dumps({"seed0": js, "theo_seed": seeds, "b_khac_seed0": b_khac}, ensure_ascii=False, indent=1))
    print("\n".join(L))


if __name__ == "__main__":
    main()
