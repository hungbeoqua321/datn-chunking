"""Thử nhanh mô hình sinh trước khi chốt (bước 1): tốc độ thật + tuân thủ định dạng trích dẫn.

KHÔNG phải dữ liệu thực nghiệm. 10 câu hỏi viết tay về Bộ luật Lao động 45/2019/QH14 (lấy toàn văn từ vbpl.vn),
ngữ cảnh = Điều chứa đáp án + 2 Điều kế bên làm nhiễu, cộng 2 câu hỏi KHÔNG có trong ngữ cảnh
(mong đợi trả lời "Không đủ căn cứ").

    python tools/thu_mo_hinh.py --ra results/buoc1/thu_mo_hinh.md
"""
import argparse
import html as H
import json
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from bs4 import BeautifulSoup  # noqa: E402

import cau_hinh as ch  # noqa: E402
from crawl.vbpl import Vbpl  # noqa: E402
from eval.trich_dan import boc, khoa_tu_chuoi  # noqa: E402
from rag import sinh  # noqa: E402

SO_HIEU = "45/2019/QH14"
# (câu hỏi, Điều chứa đáp án) — None: không có trong ngữ cảnh
CAU = [
    ("Thời gian thử việc tối đa đối với công việc của người quản lý doanh nghiệp là bao lâu?", 25),
    ("Người lao động làm việc đủ 12 tháng cho một người sử dụng lao động được nghỉ hằng năm bao nhiêu ngày trong điều kiện bình thường?", 113),
    ("Thời giờ làm việc bình thường của người lao động tối đa là bao nhiêu giờ trong một ngày?", 105),
    ("Số giờ làm thêm của người lao động không được vượt quá bao nhiêu giờ trong một tháng?", 107),
    ("Lao động nữ được nghỉ thai sản trước và sau khi sinh con bao lâu?", 139),
    ("Hợp đồng lao động phải được giao kết theo những loại nào?", 20),
    ("Người lao động có quyền đơn phương chấm dứt hợp đồng lao động không cần báo trước trong những trường hợp nào?", 35),
    ("Người sử dụng lao động có trách nhiệm chi trả trợ cấp thôi việc cho người lao động đã làm việc thường xuyên từ bao lâu trở lên?", 46),
    ("Mức lương tối thiểu được xác lập theo đâu?", 91),
    ("Tuổi nghỉ hưu của người lao động trong điều kiện lao động bình thường được điều chỉnh theo lộ trình như thế nào?", 169),
    ("Thuế suất thuế giá trị gia tăng đối với hàng xuất khẩu là bao nhiêu?", None),
    ("Mức phạt khi vượt đèn đỏ đối với xe máy là bao nhiêu?", None),
]


def lay_dieu() -> dict[int, str]:
    tmp = Path("/home/ubuntu/.claude/jobs/1409c164/tmp/blld.html")
    if not tmp.exists():
        d = Vbpl().chi_tiet("139264")
        tmp.write_text(d["documentContent"]["content"])
    s = BeautifulSoup(tmp.read_text(), "lxml")
    for t in s(["style", "script"]):
        t.decompose()
    text = H.unescape(s.get_text("\n"))
    text = re.sub(r"[ \t ]+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n", text)
    phan = re.split(r"(?m)^\s*(?=Điều\s+\d+\s*\.)", text)
    dieu: dict[int, str] = {}
    for p in phan:
        m = re.match(r"Điều\s+(\d+)\s*\.", p)
        if m and int(m.group(1)) not in dieu:
            dieu[int(m.group(1))] = p.strip()[:3500]
    return dieu


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ra", default=str(ch.RESULTS / "buoc1/thu_mo_hinh.md"))
    a = ap.parse_args()
    dieu = lay_dieu()
    cl = sinh.client()
    model = sinh.tham_so()["model"]
    dong = [f"# Thử mô hình sinh `{model}` (không phải dữ liệu thực nghiệm)\n",
            "| # | Điều gold | Token vào | Token ra | Giây | Trích đúng Điều gold | Đúng dạng | Từ chối đúng |",
            "|---|---|---|---|---|---|---|---|"]
    chi_tiet = []
    tong = {"dung_dieu": 0, "dung_dang": 0, "tu_choi": 0, "n_co": 0, "n_khong": 0, "giay": 0.0}
    for i, (q, g) in enumerate(CAU, 1):
        if g is not None:
            ds = [g, g + 1, g + 2]
        else:
            ds = [10, 11, 12]
        khoi = [{"so_hieu": SO_HIEU, "text": dieu[n]} for n in ds if n in dieu]
        t0 = time.monotonic()
        r = sinh.tra_loi(q, khoi, cl)
        giay = time.monotonic() - t0
        ans = r["tra_loi"] or ""
        trich = boc(ans)
        k = khoa_tu_chuoi(SO_HIEU)
        # "đúng dạng" = có ít nhất một trích dẫn kèm số hiệu nguyên văn (chuỗi gốc xuất hiện trong câu trả lời)
        dung_dang = SO_HIEU in ans and any(t[0] == k for t in trich)
        dung_dieu = g is not None and any(t[1] == g and t[0] == k for t in trich)
        tu_choi = "Không đủ căn cứ" in ans
        tong["giay"] += giay
        if g is None:
            tong["n_khong"] += 1
            tong["tu_choi"] += tu_choi
        else:
            tong["n_co"] += 1
            tong["dung_dieu"] += dung_dieu
            tong["dung_dang"] += dung_dang
        u = r["usage"] or {}
        dong.append(f"| {i} | {g or '—'} | {u.get('prompt_tokens')} | {u.get('completion_tokens')} | {giay:.0f} | "
                    f"{'✓' if dung_dieu else ('' if g is None else '✗')} | {'✓' if dung_dang else '✗'} | "
                    f"{('✓' if tu_choi else '✗') if g is None else ''} |")
        chi_tiet.append({"q": q, "gold": g, "tra_loi": ans, "giay": round(giay, 1), "usage": u})
        print(i, g, f"{giay:.0f}s", "điều:", dung_dieu, "dạng:", dung_dang, "từ chối:", tu_choi, flush=True)
    dong += ["", f"- Trích đúng Điều gold: **{tong['dung_dieu']}/{tong['n_co']}**; đúng dạng "
             f"số hiệu chép nguyên văn \"{SO_HIEU}\": **{tong['dung_dang']}/{tong['n_co']}**; "
             f"từ chối đúng khi thiếu căn cứ: **{tong['tu_choi']}/{tong['n_khong']}**",
             f"- Thời gian trung bình: **{tong['giay'] / len(CAU):.0f} giây/câu**", "",
             "## Câu trả lời", ""]
    for c in chi_tiet:
        dong += [f"**{c['q']}** (gold: Điều {c['gold']})", "", "> " + c["tra_loi"].replace("\n", "\n> "), ""]
    Path(a.ra).parent.mkdir(parents=True, exist_ok=True)
    Path(a.ra).write_text("\n".join(dong))
    Path(a.ra).with_suffix(".json").write_text(json.dumps(chi_tiet, ensure_ascii=False, indent=1))
    print("→", a.ra)


if __name__ == "__main__":
    main()
