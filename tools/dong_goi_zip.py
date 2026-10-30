"""Đóng gói bộ dữ liệu thành 2 tệp zip cho release `du-lieu` (Windows bấm đúp là mở, Linux dùng `unzip`).

    python tools/dong_goi_zip.py --ra ../datn-du-lieu
    python tools/dong_goi_zip.py --ra ../datn-du-lieu --chi pdf.zip    # chỉ đóng lại một gói, giữ dòng sha256 gói kia

  docs.zip   dữ liệu dạng văn bản để chạy đồ án:
             data/raw, data/clean, data/clean_full, data/manifest.csv, data/ung_vien.jsonl,
             data/thong_ke_chuan_hoa.jsonl, data/chunks/, data/index/<tên>/
             (KHÔNG có data/index/cache.f32, cache.keys — bộ đệm lúc dựng, truy hồi không đọc)
  pdf.zip    bản PDF gốc (scan có dấu đỏ) cho thử nghiệm OCR: ocr/data/pdf/*.pdf + ocr/data/manifest_pdf.csv

Đường dẫn trong zip dùng "/" và bắt đầu bằng data/ hoặc ocr/, giải nén tại gốc repo là đúng chỗ.
Ghi kèm SHA256SUMS.txt.
"""
import argparse
import hashlib
import zipfile
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
GOI = {
    "docs.zip": ["data/raw", "data/clean", "data/clean_full", "data/manifest.csv", "data/ung_vien.jsonl",
                 "data/thong_ke_chuan_hoa.jsonl", "data/chunks", "data/index"],
    "pdf.zip": ["ocr/data/pdf", "ocr/data/manifest_pdf.csv"],
}
BO_QUA = {"cache.f32", "cache.keys"}


def tep(muc: str) -> list[Path]:
    p = GOC / muc
    return [p] if p.is_file() else sorted(x for x in p.rglob("*") if x.is_file() and x.name not in BO_QUA)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ra", required=True, help="thư mục ghi các tệp zip")
    ap.add_argument("--chi", nargs="*", choices=list(GOI), help="chỉ đóng các gói này")
    a = ap.parse_args()
    ra = Path(a.ra)
    ra.mkdir(parents=True, exist_ok=True)
    cu = ra / "SHA256SUMS.txt"
    giu = {l.split()[1]: l for l in cu.read_text().splitlines() if l.strip()} if cu.exists() else {}
    tong = []
    for ten, muc in GOI.items():
        if a.chi and ten not in a.chi:
            if ten in giu:
                tong.append(giu[ten])
            continue
        z = ra / ten
        n = 0
        with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as f:
            for m in muc:
                for p in tep(m):
                    f.write(p, p.relative_to(GOC).as_posix())
                    n += 1
        h = hashlib.sha256(z.read_bytes()).hexdigest()
        tong.append(f"{h}  {ten}")
        print(f"{ten}: {n} tệp, {z.stat().st_size / 1e6:.0f} MB  {h}")
    (ra / "SHA256SUMS.txt").write_text("\n".join(tong) + "\n")


if __name__ == "__main__":
    main()
