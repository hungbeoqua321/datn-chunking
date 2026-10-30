"""Chấm OCR: so ocr/data/ocr/<cấu hình>/<id>.txt với text chuẩn ocr/data/docs/<id>.txt.

  CER        khoảng cách Levenshtein ký tự / độ dài text chuẩn (gộp trên mọi văn bản: tổng lỗi / tổng ký tự)
  WER        như trên nhưng đơn vị là từ (tách theo khoảng trắng)
  CER_bo_dau CER sau khi bỏ dấu tiếng Việt ở cả hai bên — phần chênh với CER là lỗi do SAI DẤU
  CER_khong_chen (thay thế + xoá) / độ dài text chuẩn — bỏ lỗi CHÈN. Bản PDF gốc thường có thêm phụ lục, biểu
             mẫu, chữ ký số mà text chuẩn không có; CER thô tính hết những chữ đó là lỗi. Độ đo này trả lời:
             OCR khôi phục được bao nhiêu phần TEXT CHUẨN (cái RAG thật sự cần)

Chuẩn hoá trước khi so: Unicode NFC, bỏ ranh giới trang \\f, gộp mọi khoảng trắng thành một dấu cách.
Text chuẩn là data/clean_full (giữ cả quốc hiệu, "Căn cứ…", nơi nhận, chữ ký) nên phần chữ trên trang KHÔNG có
trong text chuẩn (số trang, chữ ký số, dấu giáp lai) bị tính là lỗi chèn — CER ở đây là cận trên, không phải
lỗi nhận dạng thuần.

Chỉ chấm các văn bản mà MỌI cấu hình đều đã OCR xong, để các cấu hình so trên cùng một tập.

    python -m ocr.danh_gia                 # → ocr/ket_qua_ocr.csv, ocr/ket_qua_ocr.md
"""
import argparse
import csv
import re
import unicodedata
from pathlib import Path

from rapidfuzz.distance import Levenshtein

GOC = Path(__file__).resolve().parent.parent
DOCS = GOC / "ocr" / "data" / "docs"
OCR = GOC / "ocr" / "data" / "ocr"
MANIFEST = GOC / "ocr" / "data" / "manifest_pdf.csv"
CSV_RA = GOC / "ocr" / "ket_qua_ocr.csv"
MD_RA = GOC / "ocr" / "ket_qua_ocr.md"


def chuan(s: str) -> str:
    return re.sub(r"\s+", " ", unicodedata.normalize("NFC", s.replace("\f", " "))).strip()


def bo_dau(s: str) -> str:
    s = unicodedata.normalize("NFD", s).replace("đ", "d").replace("Đ", "D")
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--cau-hinh", nargs="*", help="chỉ chấm các cấu hình này (mặc định: mọi thư mục)")
    ap.add_argument("--ra", default="ket_qua_ocr", help="tên tệp kết quả trong ocr/ (không đuôi)")
    a = ap.parse_args()
    global CSV_RA, MD_RA
    CSV_RA, MD_RA = GOC / "ocr" / f"{a.ra}.csv", GOC / "ocr" / f"{a.ra}.md"
    cau_hinh = sorted(p for p in OCR.iterdir() if p.is_dir() and (not a.cau_hinh or p.name in a.cau_hinh))
    chung = set.intersection(*({f.stem for f in p.glob("*.txt")} for p in cau_hinh))
    so_hieu = {r["id"]: r["so_hieu"] for r in csv.DictReader(open(MANIFEST))}
    dong, tong = [], {}
    for p in cau_hinh:
        tg = {}
        for f in sorted(p.glob("_thoi_gian*.csv")):
            for r in csv.DictReader(open(f)):
                tg.setdefault(r["id"], []).append(float(r["giay_render"]) + float(r["giay_ocr"]))
        t = tong.setdefault(p.name, {"loi_c": 0, "c": 0, "loi_w": 0, "w": 0, "loi_bd": 0, "trang": 0, "giay": 0.0})
        for i in sorted(chung):
            ref, hyp = chuan((DOCS / f"{i}.txt").read_text()), chuan((p / f"{i}.txt").read_text())
            lc = Levenshtein.distance(ref, hyp)
            lw = Levenshtein.distance(ref.split(), hyp.split())
            lbd = Levenshtein.distance(bo_dau(ref), bo_dau(hyp))
            op = Levenshtein.opcodes(ref, hyp)
            lkc = sum(max(i2 - i1, j2 - j1) if tag == "replace" else i2 - i1
                      for tag, i1, i2, j1, j2 in op if tag in ("replace", "delete"))
            dong.append({"cau_hinh": p.name, "id": i, "so_hieu": so_hieu.get(i, ""), "so_trang": len(tg[i]),
                         "ky_tu": len(ref), "ky_tu_ocr": len(hyp), "CER": round(lc / len(ref), 4),
                         "WER": round(lw / len(ref.split()), 4), "CER_bo_dau": round(lbd / len(ref), 4),
                         "CER_khong_chen": round(lkc / len(ref), 4),
                         "giay_moi_trang": round(sum(tg[i]) / len(tg[i]), 2)})
            t["loi_c"] += lc; t["c"] += len(ref); t["loi_w"] += lw; t["w"] += len(ref.split()); t["loi_bd"] += lbd
            t["loi_kc"] = t.get("loi_kc", 0) + lkc
            t["trang"] += len(tg[i]); t["giay"] += sum(tg[i])

    with open(CSV_RA, "w", newline="") as f:
        w = csv.DictWriter(f, list(dong[0]))
        w.writeheader()
        w.writerows(dong)
    md = ["# Chất lượng OCR trên bản scan gốc", "",
          f"{len(chung)} văn bản, {next(iter(tong.values()))['trang']} trang; mọi cấu hình chấm trên cùng tập này. "
          "CER/WER gộp (tổng lỗi / tổng độ dài text chuẩn). Chi tiết từng văn bản: `ocr/ket_qua_ocr.csv`.", "",
          "| Cấu hình | CER không tính chèn | CER | WER | CER bỏ dấu | Lỗi do dấu | Giây/trang |",
          "|---|---:|---:|---:|---:|---:|---:|"]
    for ten, t in sorted(tong.items(), key=lambda x: x[1]["loi_kc"] / x[1]["c"]):
        cer, cbd = t["loi_c"] / t["c"], t["loi_bd"] / t["c"]
        md.append(f"| {ten} | {t['loi_kc'] / t['c']:.2%} | {cer:.2%} | {t['loi_w'] / t['w']:.2%} | {cbd:.2%} | "
                  f"{cer - cbd:.2%} | {t['giay'] / t['trang']:.2f} |")
    md += ["", "CER ở đây là cận trên: số trang, dòng chữ ký số và chữ trong dấu giáp lai có trên bản scan nhưng "
           "không có trong text chuẩn nên bị tính là lỗi chèn."]
    MD_RA.write_text("\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    main()
