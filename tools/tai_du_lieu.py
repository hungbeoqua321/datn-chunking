"""Tải bộ dữ liệu từ GitHub Release `du-lieu`, kiểm sha256 rồi giải nén đúng chỗ.

    python tools/tai_du_lieu.py                    # docs.zip (546 MB) — bắt buộc để chạy đồ án
    python tools/tai_du_lieu.py pdf                # pdf.zip (785 MB) — chỉ cho thử nghiệm OCR
    python tools/tai_du_lieu.py --tu ~/Downloads/docs.zip   # đã tải bằng trình duyệt/IDM: chỉ kiểm + giải nén

Mạng đứt giữa chừng thì cứ chạy lại lệnh — script tải TIẾP từ chỗ đã có (tệp .part trong data/_tai/),
không tải lại từ đầu. Chỉ dùng thư viện chuẩn của Python, không cần đăng nhập GitHub.
"""
import argparse
import hashlib
import sys
import time
import urllib.error
import urllib.request
import zipfile
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
URL = "https://github.com/hungbeoqua321/datn-chunking/releases/download/du-lieu/"
# tên gói -> (tệp, sha256, thư mục phải có sau khi giải nén)
GOI = {
    "docs": ("docs.zip", "ddc0b5a4848119515ce77a457cb871e9dd9883d3b52f382d065ae67d31ac4c25", "data/index"),
    "pdf": ("pdf.zip", "afd172a38243e199dc54defc278a232201c5306609646aa4f361af7ab85c61a8", "ocr/data/pdf"),
}
LAN_THU = 30


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for khoi in iter(lambda: f.read(1 << 20), b""):
            h.update(khoi)
    return h.hexdigest()


def tai(url: str, part: Path) -> None:
    """Tải về `part`, đứt thì nối tiếp bằng HTTP Range; thử lại tối đa LAN_THU lần."""
    for lan in range(1, LAN_THU + 1):
        da_co = part.stat().st_size if part.exists() else 0
        req = urllib.request.Request(url, headers={"User-Agent": "datn-chunking", "Range": f"bytes={da_co}-"})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                if r.status == 200 and da_co:      # server không nhận Range -> tải lại từ đầu
                    da_co = 0
                tong = da_co + int(r.headers.get("Content-Length", 0))
                with open(part, "ab" if da_co else "wb") as f:
                    t0, moc = time.time(), da_co
                    while khoi := r.read(1 << 20):
                        f.write(khoi)
                        da_co += len(khoi)
                        if time.time() - t0 >= 2 or da_co == tong:
                            toc = (da_co - moc) / max(time.time() - t0, 1e-9) / 1e6
                            print(f"\r  {da_co / 1e6:7.1f} / {tong / 1e6:.1f} MB  ({toc:.1f} MB/s)   ",
                                  end="", flush=True)
                            t0, moc = time.time(), da_co
            print()
            return
        except urllib.error.HTTPError as e:
            if e.code == 416:                      # đã tải đủ từ trước
                return
            loi = f"HTTP {e.code}"
        except (urllib.error.URLError, TimeoutError, ConnectionError, OSError) as e:
            loi = str(e)
        cho = min(5 * lan, 60)
        print(f"\n  mạng lỗi ({loi}) — thử lại lần {lan}/{LAN_THU} sau {cho} s, phần đã tải được giữ nguyên")
        time.sleep(cho)
    sys.exit("Tải không được sau nhiều lần thử. Chạy lại lệnh để tải tiếp, hoặc tải bằng trình duyệt rồi dùng --tu.")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("goi", nargs="*", choices=list(GOI), help="gói cần tải (mặc định: docs)")
    ap.add_argument("--tu", type=Path, help="dùng tệp zip đã tải sẵn thay vì tải")
    ap.add_argument("--force", action="store_true", help="giải nén lại dù dữ liệu đã có")
    ap.add_argument("--giu-zip", action="store_true", help="giữ tệp zip sau khi giải nén (mặc định xoá cho đỡ chật)")
    a = ap.parse_args()
    a.goi = a.goi or ["docs"]
    if a.tu and len(a.goi) != 1:
        sys.exit("--tu chỉ dùng với một gói")

    for ten in a.goi:
        tep, mong, dau_hieu = GOI[ten]
        if (GOC / dau_hieu).is_dir() and not a.force:
            print(f"Đã có {dau_hieu}/ — bỏ qua {tep} (dùng --force để giải nén lại)")
            continue
        if a.tu:
            zp = a.tu.expanduser()
        else:
            thu_muc = GOC / "data" / "_tai"
            thu_muc.mkdir(parents=True, exist_ok=True)
            zp, part = thu_muc / tep, thu_muc / (tep + ".part")
            if not zp.exists():
                print(f"Tải {tep} từ {URL + tep}")
                tai(URL + tep, part)
                part.replace(zp)

        print(f"Kiểm sha256 {zp.name} …")
        thuc = sha256(zp)
        if thuc != mong:
            if a.tu:
                sys.exit(f"SAI sha256 cho {zp.name}: {thuc} != {mong}\nTệp bị hỏng hoặc chưa tải xong — tải lại.")
            zp.unlink()
            sys.exit(f"SAI sha256 cho {zp.name}: {thuc} != {mong}\nTệp hỏng — đã xoá, chạy lại lệnh để tải lại.")
        print("  ok")

        print(f"Giải nén vào {GOC} …")
        with zipfile.ZipFile(zp) as z:
            for ten_tep in z.namelist():
                if ten_tep.startswith("/") or ".." in Path(ten_tep).parts:
                    sys.exit(f"Đường dẫn lạ trong zip: {ten_tep}")
            z.extractall(GOC)
        if not (GOC / dau_hieu).is_dir():
            sys.exit(f"Giải nén xong nhưng không thấy {dau_hieu}/ — báo lại người viết repo.")
        print(f"  xong: có {dau_hieu}/")
        if not a.tu and not a.giu_zip:
            zp.unlink()


if __name__ == "__main__":
    main()
