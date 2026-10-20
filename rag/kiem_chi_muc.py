"""Chốt chặn: chỉ mục trong data/index/ phải khớp tệp chunk trong data/chunks/.

Phải chạy TRƯỚC MỌI LẦN ĐÁNH GIÁ. Lệch là DỪNG, không đánh giá.

Vì sao cần: `rag.chi_muc` bỏ qua tệp đã có chỉ mục nếu thiếu `--force`. Sau khi sửa cài đặt C và D,
tệp chunk đổi nhưng chỉ mục vẫn là bản cũ, mà lệnh chạy vẫn báo thành công — suýt nữa pilot chấm C
và D trên đúng bản lỗi vừa sửa. Đếm dòng một mình KHÔNG đủ: nếu số chunk tình cờ bằng nhau mà nội
dung đổi thì vẫn lọt, nên kiểm thêm vân nội dung và kích thước ma trận vector.

    python -m rag.kiem_chi_muc            # kiểm mọi tệp chunk, lệch thì mã thoát 1
    python -m rag.kiem_chi_muc A_s0 B_s0  # chỉ vài tệp

Trong mã đánh giá:
    from rag.kiem_chi_muc import chot_chan
    chot_chan()        # ném SystemExit nếu lệch
"""
import hashlib
import json
import sys

import cau_hinh as ch

DIM = 768
BYTE_MOI_VECTOR = DIM * 4

# Tệp chunk CỐ Ý không nhúng — phải liệt kê tường minh kèm lý do, không bỏ qua im lặng.
# B seed 1..3 chỉ dựng để ĐẾM, không nhúng: đã đo được B không phụ thuộc seed (4 seed lệch 6/12.718
# chunk, toàn bộ là cửa sổ fallback của văn bản không có Điều) — xem chunking/chay.py và
# results/buoc3/thong_ke_chunk.md. Nhúng thêm 3 bản gần như giống hệt là tốn máy vô ích.
KHONG_NHUNG = {
    "B_s1": "B không phụ thuộc seed — chỉ nhúng seed 0 (chunking/chay.py)",
    "B_s2": "B không phụ thuộc seed — chỉ nhúng seed 0 (chunking/chay.py)",
    "B_s3": "B không phụ thuộc seed — chỉ nhúng seed 0 (chunking/chay.py)",
}


def _van_tay(cs: list[dict]) -> str:
    """Vân nội dung: băm chuỗi ĐEM NHÚNG của MỌI chunk, theo đúng thứ tự.

    Trước đây chỉ băm ba điểm (đầu / giữa / cuối) cho rẻ, nhưng cách đó LỌT ca chỉ một chunk ở
    quãng giữa đổi nội dung — mà đó chính là kiểu lệch dễ xảy ra nhất khi dựng lại chunk. Băm toàn
    bộ tốn vài giây cho cả kho, rẻ hơn nhiều so với một lần đánh giá chấm trên chỉ mục sai.
    Thứ tự cũng được tính: đảo chỗ hai chunk là vân đổi.
    """
    h = hashlib.sha1()
    h.update(str(len(cs)).encode())
    for c in cs:
        h.update(b"\x00")                       # ngăn cách, tránh ghép chuỗi gây trùng giả
        h.update(c.get("text", "").encode())
    return h.hexdigest()[:16]


def _doc(p):
    return [json.loads(x) for x in open(p) if x.strip()]


def kiem(ten: list[str] | None = None) -> list[str]:
    """Trả danh sách mô tả lỗi; rỗng nghĩa là đạt."""
    ds = ten or sorted(p.stem for p in ch.CHUNKS.glob("*.jsonl"))
    loi = []
    for t in ds:
        if t in KHONG_NHUNG and (ten is None or t not in ten):
            continue        # cố ý không nhúng; vẫn kiểm nếu người dùng nêu đích danh
        src = ch.CHUNKS / f"{t}.jsonl"
        thu_muc = ch.INDEX / t
        if not src.exists():
            loi.append(f"{t}: KHÔNG CÓ tệp chunk {src}")
            continue
        if not (thu_muc / "chunks.jsonl").exists() or not (thu_muc / "emb.f32").exists():
            loi.append(f"{t}: CHƯA NHÚNG (thiếu {thu_muc}) — chạy `python -m rag.chi_muc {t}`")
            continue
        a, b = _doc(src), _doc(thu_muc / "chunks.jsonl")
        if len(a) != len(b):
            loi.append(f"{t}: LỆCH SỐ CHUNK — chunk {len(a)} vs chỉ mục {len(b)}; "
                       f"chạy `python -m rag.chi_muc --force {t}`")
            continue
        if _van_tay(a) != _van_tay(b):
            loi.append(f"{t}: LỆCH NỘI DUNG — cùng {len(a)} chunk nhưng nội dung khác "
                       f"(chunk đã dựng lại?); chạy `python -m rag.chi_muc --force {t}`")
            continue
        n_byte = (thu_muc / "emb.f32").stat().st_size
        if n_byte != len(b) * BYTE_MOI_VECTOR:
            loi.append(f"{t}: LỆCH MA TRẬN VECTOR — emb.f32 {n_byte} byte, cần "
                       f"{len(b) * BYTE_MOI_VECTOR} ({len(b)}×{DIM}×4)")
    return loi


def chot_chan(ten: list[str] | None = None) -> None:
    """Gọi ở ĐẦU mọi bước đánh giá. Lệch là dừng hẳn, không đánh giá tiếp."""
    loi = kiem(ten)
    if loi:
        print("CHỐT CHẶN CHỈ MỤC — DỪNG, KHÔNG ĐÁNH GIÁ:", file=sys.stderr)
        for x in loi:
            print("  •", x, file=sys.stderr)
        raise SystemExit(1)


def main() -> None:
    ten = sys.argv[1:] or None
    loi = kiem(ten)
    ds = ten or sorted(p.stem for p in ch.CHUNKS.glob("*.jsonl"))
    if loi:
        print("CHỐT CHẶN CHỈ MỤC — LỆCH:", file=sys.stderr)
        for x in loi:
            print("  •", x, file=sys.stderr)
        sys.exit(1)
    kiem_tra = [t for t in ds if t not in KHONG_NHUNG]
    print(f"chỉ mục khớp tệp chunk: {len(kiem_tra)}/{len(kiem_tra)} ({' '.join(kiem_tra)})")
    bo = [t for t in ds if t in KHONG_NHUNG]
    if bo:
        print(f"cố ý không nhúng ({len(bo)}): " + "; ".join(f"{t} — {KHONG_NHUNG[t]}" for t in bo))


if __name__ == "__main__":
    main()
