"""Tải các mô hình dùng trong thực nghiệm, ghim đúng revision và kiểm sha256.

    python tools/tai_mo_hinh.py            # tải mô hình nhúng + GGUF Q4_0
    python tools/tai_mo_hinh.py --q4km     # tải thêm bản Q4_K_M để so tốc độ
    python tools/tai_mo_hinh.py --force    # tải lại dù đã có

Mô hình lưu ở models/ (không đưa vào git).
"""
import argparse
import hashlib
import sys
from pathlib import Path

from huggingface_hub import hf_hub_download, snapshot_download

GOC = Path(__file__).resolve().parent.parent
THU_MUC = GOC / "models"

# Mô hình nhúng: repo cũ hiieu/halong_embedding đã chuyển sang contextboxai/halong_embedding.
NHUNG = {
    "repo": "contextboxai/halong_embedding",
    "revision": "b57776031035f70ed2030d2e35ecc533eb0f8f71",
    "sha256": {"model.safetensors": "2fd083778d8b1f54d7ad106d1e279b5e0f6f2f9f71ae095cf91107b6e54131ab"},
}
# Mô hình sinh: Qwen3-4B-Instruct-2507 (Apache-2.0), bản GGUF của unsloth.
SINH = {
    "repo": "unsloth/Qwen3-4B-Instruct-2507-GGUF",
    "revision": "a06e946bb6b655725eafa393f4a9745d460374c9",
    "tep": {
        "Qwen3-4B-Instruct-2507-Q4_0.gguf": "e0ba675d86ab277c61701c6793659b2ae801d95e3be791464c321e6fbf613be2",
        "Qwen3-4B-Instruct-2507-Q4_K_M.gguf": "3605803b982cb64aead44f6c1b2ae36e3acdb41d8e46c8a94c6533bc4c67e597",
    },
}


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for khoi in iter(lambda: f.read(1 << 20), b""):
            h.update(khoi)
    return h.hexdigest()


def kiem(p: Path, mong: str) -> None:
    thuc = sha256(p)
    if thuc != mong:
        sys.exit(f"SAI sha256 cho {p.name}: {thuc} != {mong}")
    print(f"  ok sha256 {p.name}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--q4km", action="store_true", help="tải thêm bản Q4_K_M để so tốc độ với Q4_0")
    ap.add_argument("--force", action="store_true", help="tải lại dù file đã có")
    a = ap.parse_args()

    THU_MUC.mkdir(exist_ok=True)
    dich = THU_MUC / "halong_embedding"
    if a.force or not (dich / "model.safetensors").exists():
        print("Tải mô hình nhúng", NHUNG["repo"], "@", NHUNG["revision"][:10])
        snapshot_download(NHUNG["repo"], revision=NHUNG["revision"], local_dir=dich)
    else:
        print("Đã có mô hình nhúng, bỏ qua (dùng --force để tải lại)")
    for ten, h in NHUNG["sha256"].items():
        kiem(dich / ten, h)

    can = ["Qwen3-4B-Instruct-2507-Q4_0.gguf"] + (["Qwen3-4B-Instruct-2507-Q4_K_M.gguf"] if a.q4km else [])
    for ten in can:
        p = THU_MUC / ten
        if a.force or not p.exists():
            print("Tải", ten)
            hf_hub_download(SINH["repo"], ten, revision=SINH["revision"], local_dir=THU_MUC)
        else:
            print("Đã có", ten, "— bỏ qua")
        kiem(p, SINH["tep"][ten])


if __name__ == "__main__":
    main()
