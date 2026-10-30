"""Đóng gói data/ thành .zip (Windows bấm đúp là mở được) — cùng nội dung với các tệp .tar.* của release.

    python tools/dong_goi_zip.py --ra ../datn-release-zip

  datn-corpus.zip   data/raw, data/clean, data/clean_full, data/manifest.csv, data/ung_vien.jsonl,
                    data/thong_ke_chuan_hoa.jsonl
  datn-chunks.zip   data/chunks/
  datn-index.zip    data/index/<tên>/  (KHÔNG có cache.f32 / cache.keys — bộ đệm lúc dựng, truy hồi không đọc)

Đường dẫn trong zip dùng "/" và bắt đầu bằng data/, giải nén tại gốc repo là đúng chỗ. Ghi kèm SHA256SUMS-zip.txt.
"""
import argparse
import hashlib
import zipfile
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
GOI = {
    "datn-corpus.zip": ["data/raw", "data/clean", "data/clean_full", "data/manifest.csv", "data/ung_vien.jsonl",
                        "data/thong_ke_chuan_hoa.jsonl"],
    "datn-chunks.zip": ["data/chunks"],
    "datn-index.zip": ["data/index"],
}
BO_QUA = {"cache.f32", "cache.keys"}


def tep(muc: str) -> list[Path]:
    p = GOC / muc
    return [p] if p.is_file() else sorted(x for x in p.rglob("*") if x.is_file() and x.name not in BO_QUA)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ra", required=True, help="thư mục ghi các tệp zip")
    a = ap.parse_args()
    ra = Path(a.ra)
    ra.mkdir(parents=True, exist_ok=True)
    tong = []
    for ten, muc in GOI.items():
        z = ra / ten
        with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as f:
            for m in muc:
                for p in tep(m):
                    f.write(p, p.relative_to(GOC).as_posix())
        h = hashlib.sha256(z.read_bytes()).hexdigest()
        tong.append(f"{h}  {ten}")
        print(f"{ten}: {z.stat().st_size / 1e6:.0f} MB  {h}")
    (ra / "SHA256SUMS-zip.txt").write_text("\n".join(tong) + "\n")


if __name__ == "__main__":
    main()
