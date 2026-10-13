"""Nhúng chunk và lưu chỉ mục vector (numpy memmap, cosine = tích vô hướng vì vector đã chuẩn hoá L2).

Có bộ đệm dùng chung theo NỘI DUNG (sha1 của chuỗi đem nhúng): chunk giống hệt nhau giữa các seed / phương pháp
(ví dụ B seed 0..3 chỉ khác ở vài văn bản không có Điều; A+ và B trùng ở nhóm không có Điều) chỉ nhúng một lần.
Bộ đệm ghi nối tiếp theo từng lô nên dừng giữa chừng chạy lại sẽ tiếp tục.

  data/index/cache.f32 + cache.keys      bộ đệm vector (N × 768, float32) + sha1 từng dòng
  data/index/<tên>/emb.f32 + chunks.jsonl ma trận của một phương pháp/seed (thứ tự = thứ tự chunk)

    python -m rag.chi_muc A_s0 B_s0 ...    # dựng chỉ mục cho các tệp chunk (tên trong data/chunks/)
    python -m rag.chi_muc --tat-ca          # mọi tệp trong data/chunks/
"""
import argparse
import hashlib
import json
import os
import sys
import time

import numpy as np

import cau_hinh as ch

DIM = 768
CACHE = ch.INDEX / "cache.f32"
KEYS = ch.INDEX / "cache.keys"


def sha(s: str) -> str:
    return hashlib.sha1(s.encode()).hexdigest()


def _nap_cache() -> dict[str, int]:
    if not KEYS.exists():
        return {}
    keys = KEYS.read_text().split("\n")[:-1]
    n = os.path.getsize(CACHE) // (DIM * 4) if CACHE.exists() else 0
    keys = keys[:n]  # khoá chỉ hợp lệ nếu vector tương ứng đã ghi xong
    return {k: i for i, k in enumerate(keys)}


def nhung_bo_dem(van_ban: list[str], batch: int = 16, gioi_han_giay: float | None = None) -> dict[str, int]:
    """Đảm bảo mọi chuỗi đã có trong bộ đệm; trả {sha1: dòng}.

    `gioi_han_giay`: sau 2 phút đầu, nếu tổng thời gian dự kiến (ngoại suy theo số KÝ TỰ đã nhúng / giây — chuỗi được
    sắp từ ngắn tới dài nên ngoại suy theo số chuỗi sẽ đánh giá thấp) vượt giới hạn thì DỪNG, phần đã nhúng vẫn giữ."""
    from rag import nhung

    ch.INDEX.mkdir(parents=True, exist_ok=True)
    idx = _nap_cache()
    can = []
    da = set(idx)
    for t in van_ban:
        k = sha(t)
        if k not in da:
            da.add(k)
            can.append((k, t))
    if not can:
        return idx
    # sắp theo độ dài để lô đều nhau (nhanh hơn), ghi theo từng lô
    can.sort(key=lambda x: len(x[1]))
    nap = nhung.nap(so_luong=int(os.environ.get("SO_LUONG", "3")))
    t0, xong, ky_tu, tong_ky_tu = time.monotonic(), 0, 0, sum(len(t) for _, t in can)
    with open(CACHE, "ab") as fv, open(KEYS, "a") as fk:
        for i in range(0, len(can), batch * 8):
            lo = can[i:i + batch * 8]
            v = nap.encode([t for _, t in lo], batch_size=batch, convert_to_numpy=True,
                           show_progress_bar=False).astype(np.float32)
            fv.write(v.tobytes())
            fv.flush()
            fk.write("".join(k + "\n" for k, _ in lo))
            fk.flush()
            for k, _ in lo:
                idx[k] = len(idx)
            xong += len(lo)
            ky_tu += sum(len(t) for _, t in lo)
            dt = time.monotonic() - t0
            if gioi_han_giay and dt > 120 and dt + (tong_ky_tu - ky_tu) / (ky_tu / dt) > gioi_han_giay:
                raise RuntimeError(f"dự kiến {(dt + (tong_ky_tu - ky_tu) / (ky_tu / dt)) / 3600:.1f} h > giới hạn "
                                   f"{gioi_han_giay / 3600:.1f} h — DỪNG để báo người dùng ({xong}/{len(can)} đã nhúng)")
            print(f"  nhúng {xong}/{len(can)}  {xong / dt:.2f} chunk/s  còn ~{(len(can) - xong) / (xong / dt) / 60:.0f} phút",
                  flush=True)
    return idx


def cuoi_duoc_nhung(cs: list[dict]) -> list[int]:
    """Vị trí ký tự (trong văn bản) nơi phần ĐƯỢC NHÚNG của mỗi chunk kết thúc. Mô hình chỉ đọc 512 token đầu (tính cả
    <s></s>) của chuỗi tiền tố + nội dung; chunk dài hơn bị cắt đuôi → khi chấm độ phủ chỉ tính tới vị trí này."""
    from transformers import AutoTokenizer

    tok = AutoTokenizer.from_pretrained(str(ch.MO_HINH_NHUNG))
    ra = []
    for i in range(0, len(cs), 256):
        lo = cs[i:i + 256]
        enc = tok([c["text"] for c in lo], truncation=True, max_length=512, return_offsets_mapping=True)
        for c, om in zip(lo, enc["offset_mapping"]):
            het = max((b for _, b in om), default=0)  # ký tự cuối của token cuối cùng được giữ
            if het >= len(c["text"].rstrip()):
                ra.append(c["end"])  # không bị cắt
                continue
            dau_than = len(c["tien_to"]) + 1 if c.get("tien_to") else 0
            ra.append(min(c["end"], c["start"] + max(0, het - dau_than)))
    return ra


def _ghi_chunks(p, cs: list[dict]) -> None:
    for c, e in zip(cs, cuoi_duoc_nhung(cs)):
        c["end_nhung"] = e
    tam = p.with_suffix(".tmp")
    tam.write_text("".join(json.dumps(c, ensure_ascii=False) + "\n" for c in cs))
    tam.replace(p)


def dung(ten: str, force: bool = False) -> None:
    src = ch.CHUNKS / f"{ten}.jsonl"
    out = ch.INDEX / ten
    if (out / "emb.f32").exists() and not force:
        print("có rồi:", ten)
        return
    cs = [json.loads(x) for x in open(src) if x.strip()]
    print(f"{ten}: {len(cs)} chunk", flush=True)
    idx = nhung_bo_dem([c["text"] for c in cs])
    bo = np.memmap(CACHE, dtype=np.float32, mode="r").reshape(-1, DIM)
    m = np.stack([bo[idx[sha(c["text"])]] for c in cs])
    out.mkdir(parents=True, exist_ok=True)
    m.tofile(out / "emb.f32.tmp")
    _ghi_chunks(out / "chunks.jsonl", cs)
    (out / "emb.f32.tmp").replace(out / "emb.f32")
    print(f"→ {out} ({m.shape[0]}×{m.shape[1]})")


def nap(ten: str) -> tuple[np.ndarray, list[dict]]:
    d = ch.INDEX / ten
    cs = [json.loads(x) for x in open(d / "chunks.jsonl") if x.strip()]
    if cs and "end_nhung" not in cs[0]:  # chỉ mục dựng trước khi có end_nhung → bổ sung một lần
        _ghi_chunks(d / "chunks.jsonl", cs)
    m = np.fromfile(d / "emb.f32", dtype=np.float32).reshape(-1, DIM)
    assert m.shape[0] == len(cs), f"{ten}: lệch số dòng"
    return m, cs


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("ten", nargs="*")
    ap.add_argument("--tat-ca", action="store_true")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
    ds = a.ten or ([p.stem for p in sorted(ch.CHUNKS.glob("*.jsonl"))] if a.tat_ca else [])
    if not ds:
        ap.print_help()
        sys.exit(1)
    for t in ds:
        dung(t, a.force)


if __name__ == "__main__":
    main()
