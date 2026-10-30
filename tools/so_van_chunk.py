"""So vân chunk của bản dựng lại với bản VPS — bước 0 của lượt chạy trên máy local.

Vân = rag.kiem_chi_muc._van_tay: sha1 của TOÀN BỘ chuỗi đem nhúng, đúng thứ tự (đổi một chunk là vân đổi).
Bản VPS có ở hai nơi, cả hai đều dựng trên VPS và tải về qua docs.zip:
  data/chunks/<t>.jsonl            tệp chunk
  data/index/<t>/chunks.jsonl      bản chép lúc nhúng
Ngoài vân còn so từng chunk (text + metadata) để chỉ ra chỗ lệch đầu tiên nếu có. Trường RỖNG ("" hoặc None) được coi như
không có: `cau_dan_lap`, `kem_theo`, `vi_tri_manh`, `tong_so_manh` thêm vào chunking/base.py cùng phương pháp E (3f66faf), sau khi VPS dựng chunk A/B/C, nên
bản VPS thiếu các trường đó còn bản mới ghi giá trị rỗng — cùng một nội dung.

    python tools/so_van_chunk.py thuc_nghiem/tai_lap_gpu/chunks [--ra thuc_nghiem/tai_lap_gpu/van_chunk.md]
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from rag.kiem_chi_muc import _doc, _van_tay  # noqa: E402

GOC = Path(__file__).resolve().parent.parent


def _chuan(cs: list[dict]) -> list[dict]:
    return [{k: v for k, v in c.items() if v not in ("", None)} for c in cs]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("moi", type=Path, help="thư mục chunk dựng lại")
    ap.add_argument("--ra", type=Path)
    a = ap.parse_args()
    dong, lech = [], 0
    for p in sorted(a.moi.glob("*.jsonl")):
        t = p.stem
        moi = _doc(p)
        vps = GOC / "data/chunks" / p.name
        idx = GOC / "data/index" / t / "chunks.jsonl"
        cu = _doc(vps) if vps.exists() else None
        v_moi = _van_tay(moi)
        v_cu = _van_tay(cu) if cu is not None else "—"
        v_idx = _van_tay(_doc(idx)) if idx.exists() else "—"
        khop_tron = cu is not None and _chuan(moi) == _chuan(cu)        # cả metadata (offset, nhãn) cũng phải trùng
        dau = ""
        if cu is not None and not khop_tron:
            lech += 1
            i = next((i for i, (x, y) in enumerate(zip(_chuan(moi), _chuan(cu))) if x != y), min(len(moi), len(cu)))
            dau = f"chunk đầu tiên lệch: #{i}"
        dong.append((t, len(moi), len(cu) if cu is not None else "—", v_moi, v_cu, v_idx,
                     "✅" if v_moi == v_cu else "❌", "✅" if khop_tron else ("❌ " + dau if cu is not None else "—")))
    hd = "| Tệp | Số chunk mới | Số chunk VPS | Vân mới | Vân VPS (data/chunks) | Vân VPS (data/index) | Vân khớp | Khớp cả metadata |"
    out = [hd, "|" + "---|" * 8] + ["| " + " | ".join(map(str, d)) + " |" for d in dong]
    s = "\n".join(out)
    print(s)
    print(f"\n{len(dong) - lech}/{len(dong)} tệp trùng tuyệt đối")
    if a.ra:
        a.ra.parent.mkdir(parents=True, exist_ok=True)
        a.ra.write_text(s + f"\n\n{len(dong) - lech}/{len(dong)} tệp trùng tuyệt đối (text + metadata từng chunk).\n")
    sys.exit(1 if lech else 0)


if __name__ == "__main__":
    main()
