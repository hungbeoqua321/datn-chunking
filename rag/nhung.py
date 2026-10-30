"""Nạp mô hình nhúng halong_embedding và nhúng văn bản.

Kiểm tra cấu hình (đã đọc trong models/halong_embedding):
  - modules.json: Transformer → Pooling (mean) → Normalize  ⇒ vector đã chuẩn hoá L2, cosine = tích vô hướng
  - sentence_bert_config.json: max_seq_length = 512 (tính cả <s> </s>)
  - config_sentence_transformers.json: prompts rỗng ⇒ KHÔNG thêm tiền tố "query:" / "passage:" như họ e5

    python -m rag.nhung --kiem      # smoke test: tái hiện ví dụ trong model card
"""
import argparse
import json
import os

import numpy as np

import cau_hinh as ch

_MO_HINH = None


def nap(so_luong: int | None = None):
    """Nạp mô hình một lần. so_luong = số luồng torch (None: để mặc định)."""
    global _MO_HINH
    if _MO_HINH is None:
        import torch
        from sentence_transformers import SentenceTransformer

        if so_luong:
            torch.set_num_threads(so_luong)
        # Mặc định CPU như VPS; máy có GPU đặt NHUNG_DEVICE=cuda cho thử nghiệm mới (đổi điều kiện thực nghiệm)
        _MO_HINH = SentenceTransformer(str(ch.MO_HINH_NHUNG), device=os.environ.get("NHUNG_DEVICE", "cpu"))
    return _MO_HINH


def cau_hinh_mo_hinh() -> dict:
    """Đọc lại cấu hình từ đĩa để báo cáo (không giả định)."""
    d = ch.MO_HINH_NHUNG
    return {
        "modules": [m["type"].split(".")[-1] for m in json.loads((d / "modules.json").read_text())],
        "pooling": json.loads((d / "1_Pooling/config.json").read_text()),
        "max_seq_length": json.loads((d / "sentence_bert_config.json").read_text())["max_seq_length"],
        "prompts": json.loads((d / "config_sentence_transformers.json").read_text()).get("prompts", {}),
    }


def nhung(van_ban: list[str], batch: int = 16) -> np.ndarray:
    return nap().encode(van_ban, batch_size=batch, convert_to_numpy=True, normalize_embeddings=False,
                        show_progress_bar=False).astype(np.float32)


def kiem_tra() -> None:
    """Tái hiện ví dụ trong model card: thứ hạng phải khớp, vector phải có chuẩn 1."""
    q = "Bóng đá có lợi ích gì cho sức khỏe?"
    docs = [
        "Bóng đá giúp cải thiện sức khỏe tim mạch và tăng cường sức bền.",
        "Bóng đá là môn thể thao phổ biến nhất thế giới.",
        "Chơi bóng đá giúp giảm căng thẳng và cải thiện tâm lý.",
        "Bóng đá có thể giúp bạn kết nối với nhiều người hơn.",
        "Bóng đá không chỉ là môn thể thao mà còn là cách để giải trí.",
    ]
    # thứ hạng và điểm in trong model card
    mong_thu_tu = [0, 2, 4, 3, 1]
    mong_diem = [0.7318, 0.6623, 0.6102, 0.4988, 0.4828]
    vq, vd = nhung([q]), nhung(docs)
    diem = (vq @ vd.T).ravel()
    thu_tu = list(np.argsort(-diem))
    chuan = np.linalg.norm(vd, axis=1)
    print("cấu hình:", cau_hinh_mo_hinh())
    print("thứ hạng:", thu_tu, "điểm:", [round(float(diem[i]), 4) for i in thu_tu])
    assert thu_tu == mong_thu_tu, f"thứ hạng khác model card: {thu_tu}"
    assert np.allclose(chuan, 1, atol=1e-4), "vector chưa chuẩn hoá L2"
    lech = max(abs(float(diem[i]) - m) for i, m in zip(mong_thu_tu, mong_diem))
    assert lech < 0.01, f"điểm lệch model card {lech:.4f}"
    print(f"OK — khớp model card (lệch điểm lớn nhất {lech:.4f}), chuẩn L2 = 1")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--kiem", action="store_true", help="smoke test theo ví dụ của model card")
    a = ap.parse_args()
    os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
    if a.kiem:
        kiem_tra()
    else:
        ap.print_help()
