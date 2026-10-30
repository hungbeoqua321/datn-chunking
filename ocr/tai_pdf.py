"""Tải bản PDF GỐC (bản scan có dấu đỏ) của chính các văn bản trong data/manifest.csv để thử OCR.

Không crawl lại corpus: data/raw, data/clean… KHÔNG bị đụng tới. Chỉ ghi vào ocr/data/:

  ocr/data/pdf/<id>.pdf      bản PDF gốc vbpl.vn lưu kèm văn bản (trường documentContentFileName)
  ocr/data/docs/<id>.txt     text CHUẨN của cùng văn bản — chép nguyên từ data/clean_full (đáp án để đo CER;
                             clean_full giữ cả "Căn cứ…", nơi nhận, chữ ký — đúng những gì có trên bản scan)
  ocr/data/manifest_pdf.csv  id, số hiệu, tên file gốc, sha256, số trang, số trang có lớp text, ghi chú

Tên file lấy qua server action chi tiết (crawl/vbpl.py); file tải từ gateway của Bộ Tư pháp
(vbpl-bientap-gateway.moj.gov.vn — chỉ mở cho IP Việt Nam). Giữ ≤ 1 request/giây.

    python -m ocr.tai_pdf              # bỏ qua văn bản đã tải
    python -m ocr.tai_pdf --toi-da 20  # dừng khi đã có 20 PDF scan
"""
import argparse
import csv
import hashlib
import shutil
from pathlib import Path
from urllib.parse import quote

import cau_hinh as ch
from crawl import vbpl

THU_MUC = ch.GOC / "ocr" / "data"
PDF = THU_MUC / "pdf"
DOCS = THU_MUC / "docs"
MANIFEST = THU_MUC / "manifest_pdf.csv"
GATEWAY = "https://vbpl-bientap-gateway.moj.gov.vn/api/qtdc/public/doc/minio/buckets/vbpl"
COT = ["id", "so_hieu", "ten_goc", "sha256", "so_trang", "trang_co_text", "ghi_chu"]

# Client dò lại action id thì ghi ra ocr/data/, KHÔNG ghi vào data/raw (bản chụp phải giữ nguyên).
vbpl.TEP_ACTION = THU_MUC / "_actions.json"


def _so_trang(p: Path) -> tuple[int, int]:
    """(số trang, số trang có lớp text). Không có pymupdf thì trả (0, 0) — đếm lại ở bước OCR."""
    try:
        import pymupdf
    except ImportError:
        return 0, 0
    d = pymupdf.open(p)
    return len(d), sum(1 for t in d if len(t.get_text().strip()) > 50)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--toi-da", type=int, default=0, help="dừng khi đã có chừng này PDF (0: không giới hạn)")
    a = ap.parse_args()
    PDF.mkdir(parents=True, exist_ok=True)
    DOCS.mkdir(parents=True, exist_ok=True)
    if not vbpl.TEP_ACTION.exists() and (ch.RAW / "_actions.json").exists():
        shutil.copyfile(ch.RAW / "_actions.json", vbpl.TEP_ACTION)

    cu = {r["id"]: r for r in csv.DictReader(open(MANIFEST))} if MANIFEST.exists() else {}
    v = vbpl.Vbpl()
    for r in csv.DictReader(open(ch.MANIFEST)):
        if a.toi_da and sum(1 for x in cu.values() if x["sha256"]) >= a.toi_da:
            break
        i = r["id"]
        if i in cu and not cu[i]["ghi_chu"].startswith("lỗi"):   # lỗi mạng/server thì thử lại
            continue
        dong = {"id": i, "so_hieu": r["so_hieu"], "ten_goc": "", "sha256": "", "so_trang": 0,
                "trang_co_text": 0, "ghi_chu": ""}
        try:
            ten = v.chi_tiet(i).get("documentContentFileName") or ""
        except Exception as e:  # ghi lại, không dừng cả lượt vì một văn bản
            ten, dong["ghi_chu"] = "", f"lỗi chi_tiet: {e}"
        if not ten.lower().endswith(".pdf"):
            dong["ghi_chu"] = dong["ghi_chu"] or f"không có PDF gốc ({ten or 'trống'})"
        else:
            dong["ten_goc"] = ten
            v._cho()
            res = v.s.get(f"{GATEWAY}/{quote(i)}/{quote(ten)}/download", timeout=120,
                          headers={"Referer": vbpl.GOC_URL + "/"})
            if res.status_code != 200 or not res.content.startswith(b"%PDF"):
                dong["ghi_chu"] = f"tải hỏng: HTTP {res.status_code}"
            else:
                p = PDF / f"{i}.pdf"
                p.write_bytes(res.content)
                shutil.copyfile(ch.CLEAN_FULL / f"{i}.txt", DOCS / f"{i}.txt")
                dong["sha256"] = hashlib.sha256(res.content).hexdigest()
                dong["so_trang"], dong["trang_co_text"] = _so_trang(p)
        cu[i] = dong
        print(f"{i:40s} {dong['so_hieu']:22s} {dong['so_trang']:>3} trang  {dong['ghi_chu']}", flush=True)
        with open(MANIFEST, "w", newline="") as f:  # ghi lại sau mỗi văn bản: dừng giữa chừng vẫn tiếp được
            w = csv.DictWriter(f, COT)
            w.writeheader()
            w.writerows(cu.values())


if __name__ == "__main__":
    main()
