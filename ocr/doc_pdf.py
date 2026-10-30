"""Trích chữ từ MỘT tệp PDF bất kỳ (tài liệu người dùng tải lên web) — chạy trong .venv-ocr.

Từng trang: có lớp chữ (> 50 ký tự) thì lấy luôn; không có (bản scan) thì OCR bằng Tesseract `vie`, bỏ dấu đỏ trước
— đúng cấu hình đã chọn ở ocr/ket_qua_ocr_so_sanh.md (mất 1,73% text chuẩn trên mẫu, 2,9 s/trang).

    python -m ocr.doc_pdf <tệp.pdf>     # in JSON: {"text", "so_trang", "trang_ocr", "giay"}
"""
import json
import sys
import time

import pymupdf

from ocr.quet import Tesseract, anh_trang, xam

NGUONG_LOP_CHU = 50


def doc(p: str) -> dict:
    t0 = time.monotonic()
    d = pymupdf.open(p)
    eng, trang, ocr = None, [], 0
    for t in d:
        s = t.get_text()
        if len(s.strip()) <= NGUONG_LOP_CHU:
            eng = eng or Tesseract(6)
            s = eng.doc(xam(anh_trang(t), "bo_do"))
            ocr += 1
        trang.append(s.replace("\r\n", "\n"))   # Tesseract trên Windows xuống dòng CRLF
    return {"text": "\n".join(trang), "so_trang": len(d), "trang_ocr": ocr, "giay": round(time.monotonic() - t0, 1)}


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(doc(sys.argv[1]), ensure_ascii=False))
