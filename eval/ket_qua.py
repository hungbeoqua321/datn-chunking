"""Phân loại kết quả của một lần sinh — DÙNG CHUNG cho mọi bảng kết quả.

Ba hạng mục, loại trừ nhau, cộng lại đúng bằng cỡ mẫu:

  dat       — mô hình trả lời được, có nội dung để chấm
  tu_choi   — mô hình nói "không đủ căn cứ": một kết quả HỢP LỆ, không phải lỗi
  cat_tran  — câu trả lời chạm trần MAX_TOKENS nên DỞ DANG (rag.sinh.LoiCat)

`cat_tran` KHÔNG bị loại khỏi mẫu. Loại nó đi là làm đẹp số liệu: câu bị cắt là câu phương
pháp đó không trả lời nổi trong ngân sách đã khoá, và ngân sách là một phần của thiết kế thí
nghiệm chứ không phải tai nạn. Vì vậy nó đứng thành MỘT CỘT RIÊNG trong mọi bảng, không gộp
vào "đạt" và cũng không gộp vào "từ chối".

Mọi bảng kết quả lấy tên cột và cách đếm từ đây, để ba hạng mục không bao giờ lệch nhau giữa
các bảng.
"""
import collections

from eval import trich_dan

LOAI = ("dat", "tu_choi", "cat_tran")
TEN = {"dat": "đạt", "tu_choi": "từ chối", "cat_tran": "cắt trần"}


def phan_loai(r: dict) -> str:
    """Hạng mục của một dòng câu trả lời."""
    if r.get("cat_tran"):
        return "cat_tran"
    return "tu_choi" if trich_dan.tu_choi(r.get("tra_loi") or "") else "dat"


def dem(rows: list[dict], khoa: str) -> dict[str, dict[str, int]]:
    """Đếm theo (giá trị của `khoa`) × hạng mục. Mọi hạng mục đều có mặt, kể cả khi bằng 0."""
    ra: dict[str, dict[str, int]] = {}
    for r in rows:
        ra.setdefault(r[khoa], dict.fromkeys(LOAI, 0))[phan_loai(r)] += 1
    return ra


def bang(rows: list[dict], khoa: str, tieu_de: str = "biến thể") -> str:
    """Bảng markdown: một dòng mỗi giá trị của `khoa`, một cột mỗi hạng mục."""
    d = dem(rows, khoa)
    L = [f"| {tieu_de} | " + " | ".join(TEN[k] for k in LOAI) + " | tổng |",
         "|---|" + "---|" * (len(LOAI) + 1)]
    for k in sorted(d):
        v = d[k]
        L.append(f"| {k} | " + " | ".join(str(v[x]) for x in LOAI) + f" | {sum(v.values())} |")
    tong = collections.Counter()
    for v in d.values():
        tong.update(v)
    L.append("| **tổng** | " + " | ".join(f"**{tong[x]}**" for x in LOAI)
             + f" | **{sum(tong.values())}** |")
    return "\n".join(L)
