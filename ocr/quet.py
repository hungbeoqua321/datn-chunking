"""OCR bản PDF scan trong ocr/data/pdf → ocr/data/ocr/<engine>_<tien_xu_ly>/<id>.txt

Hai engine, hai cách tiền xử lý (để so sánh, không đoán):

  engine     tesseract  Tesseract 5 + vie (tessdata_best), CPU, --psm 6 ... đổi bằng --psm
             easyocr    EasyOCR "vi", GPU nếu có; ghép dòng theo toạ độ
  tiền xử lý goc       ảnh xám, không làm gì thêm
             bo_do     BỎ DẤU ĐỎ: điểm ảnh có sắc đỏ/hồng đủ đậm (HSV) tô trắng trước khi chuyển xám —
                       dấu đỏ và chữ ký số in màu đè lên chữ đen thì chữ đen vẫn còn

Mỗi trang render 300 dpi. Thời gian từng trang ghi vào <thư mục>/_thoi_gian.csv. File đã có thì bỏ qua.

    python -m ocr.quet --engine tesseract --tien-xu-ly bo_do
    python -m ocr.quet --engine easyocr --tien-xu-ly goc --chi 0034b890-7637-11f1-bf90-3df95518d6f5
"""
import argparse
import csv
import os
import subprocess
import tempfile
import time
from pathlib import Path

import cv2
import numpy as np
import pymupdf

GOC = Path(__file__).resolve().parent.parent
PDF = GOC / "ocr" / "data" / "pdf"
RA = GOC / "ocr" / "data" / "ocr"
TESSERACT = Path(os.environ.get("TESSERACT", GOC / "tools/tesseract-env/Library/bin/tesseract.exe"))
TESSDATA = Path(os.environ.get("TESSDATA_PREFIX", GOC / "tools/tesseract-env/share/tessdata"))
DPI = 300


def anh_trang(trang: pymupdf.Page) -> np.ndarray:
    pix = trang.get_pixmap(dpi=DPI, colorspace=pymupdf.csRGB)
    return np.frombuffer(pix.samples, np.uint8).reshape(pix.height, pix.width, 3).copy()


def bo_dau_do(rgb: np.ndarray) -> np.ndarray:
    """Tô trắng điểm ảnh đỏ/hồng. Ngưỡng bão hoà 60 giữ lại chữ đen/xám (S thấp) kể cả khi nằm dưới dấu."""
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
    do = (((hsv[..., 0] <= 12) | (hsv[..., 0] >= 155)) & (hsv[..., 1] >= 60) & (hsv[..., 2] >= 60))
    ra = rgb.copy()
    ra[do] = 255
    return ra


def xam(rgb: np.ndarray, tien_xu_ly: str) -> np.ndarray:
    if tien_xu_ly == "bo_do":
        rgb = bo_dau_do(rgb)
    return cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)


class Tesseract:
    def __init__(self, psm: int):
        self.psm = psm

    def doc(self, g: np.ndarray) -> str:
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "t.png"
            cv2.imwrite(str(p), g)
            r = subprocess.run([str(TESSERACT), str(p), "stdout", "--tessdata-dir", str(TESSDATA),
                                "-l", "vie", "--psm", str(self.psm),
                                "--dpi", str(DPI)], capture_output=True)
        if r.returncode:
            raise RuntimeError(r.stderr.decode("utf-8", "replace"))
        return r.stdout.decode("utf-8")


class EasyOcr:
    def __init__(self):
        import easyocr
        import torch
        self.r = easyocr.Reader(["vi"], gpu=torch.cuda.is_available(), verbose=False)

    def doc(self, g: np.ndarray) -> str:
        hop = self.r.readtext(g, detail=1, paragraph=False)
        # ghép theo dòng: các hộp có tâm dọc gần nhau (≤ nửa chiều cao) là một dòng, rồi xếp trái → phải
        hop = sorted(((min(p[1] for p in b), max(p[1] for p in b), min(p[0] for p in b), t) for b, t, _ in hop))
        dong, ra = [], []
        for y0, y1, x0, t in hop:
            if dong and (y0 + y1) / 2 - dong[-1][0] > (y1 - y0) / 2:
                ra.append(" ".join(x[2] for x in sorted(dong, key=lambda x: x[1])))
                dong = []
            dong.append(((y0 + y1) / 2, x0, t))
        if dong:
            ra.append(" ".join(x[2] for x in sorted(dong, key=lambda x: x[1])))
        return "\n".join(ra)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--engine", choices=("tesseract", "easyocr"), required=True)
    ap.add_argument("--tien-xu-ly", choices=("goc", "bo_do"), default="bo_do")
    ap.add_argument("--psm", type=int, default=6, help="chế độ phân trang của Tesseract (6: một khối văn bản)")
    ap.add_argument("--chi", nargs="*", metavar="ID", help="chỉ OCR các văn bản này")
    ap.add_argument("--phan", metavar="i/n", help="chỉ làm phần thứ i trong n phần (chạy song song n tiến trình; "
                    "Tesseract nên đặt OMP_THREAD_LIMIT=1)")
    a = ap.parse_args()

    ten = f"{a.engine}_{a.tien_xu_ly}" + (f"_psm{a.psm}" if a.engine == "tesseract" and a.psm != 6 else "")
    ra = RA / ten
    ra.mkdir(parents=True, exist_ok=True)
    ds = sorted(PDF.glob("*.pdf"))
    if a.chi:
        ds = [p for p in ds if p.stem in a.chi]
    tg = ra / "_thoi_gian.csv"
    if a.phan:
        i, n = map(int, a.phan.split("/"))
        ds = ds[i - 1::n]
        tg = ra / f"_thoi_gian_{i}.csv"     # mỗi tiến trình một tệp, không ghi chen nhau
    moi = not tg.exists()
    eng = Tesseract(a.psm) if a.engine == "tesseract" else EasyOcr()
    t_all = time.monotonic()
    with open(tg, "a", newline="") as f:
        w = csv.writer(f)
        if moi:
            w.writerow(["id", "trang", "giay_render", "giay_ocr"])
        for p in ds:
            dich = ra / f"{p.stem}.txt"
            if dich.exists():
                continue
            d, trang_ra = pymupdf.open(p), []
            for i, trang in enumerate(d):
                t0 = time.monotonic()
                g = xam(anh_trang(trang), a.tien_xu_ly)
                t1 = time.monotonic()
                trang_ra.append(eng.doc(g))
                w.writerow([p.stem, i + 1, round(t1 - t0, 3), round(time.monotonic() - t1, 3)])
            f.flush()
            dich.write_text("\n\f".join(trang_ra))   # \f: ranh giới trang
            print(f"{ten} {p.stem}: {len(d)} trang ({time.monotonic() - t_all:.0f}s)", flush=True)
    print(f"xong {ten}: {time.monotonic() - t_all:.0f}s")


if __name__ == "__main__":
    main()
