"""Xếp hạng lại (rerank) ứng viên truy hồi bằng cross-encoder — THỬ NGHIỆM MỞ RỘNG, không thuộc thiết kế gốc.

Truy hồi dense lấy K_UNG_VIEN chunk, cross-encoder chấm lại từng cặp (câu hỏi, chunk) và xếp theo điểm đó.
Mặc định TẮT: mọi số trong results/ không dùng rerank. Bật trong thử nghiệm (thuc_nghiem/chay.py --rerank).

Hai mô hình, ghim revision như mô hình nhúng:
  bge     BAAI/bge-reranker-v2-m3          đa ngữ (XLM-R large, 568M), Apache-2.0
  aiteam  AITeamVN/Vietnamese_Reranker     tinh chỉnh từ bge-reranker-v2-m3 trên dữ liệu tiếng Việt, Apache-2.0

Thiết bị: RERANK_DEVICE (mặc định cuda nếu có, không thì cpu); fp16 trên GPU.

    python -m rag.rerank --tai               # tải cả hai mô hình về models/
    python -m rag.rerank --kiem bge          # thử một câu hỏi
"""
import argparse
import os

import cau_hinh as ch

MO_HINH = {
    "bge": {"repo": "BAAI/bge-reranker-v2-m3", "revision": "953dc6f6f85a1b2dbfca4c34a2796e7dde08d41e"},
    "aiteam": {"repo": "AITeamVN/Vietnamese_Reranker", "revision": "f536976248403314225d7fdfdbc87f0e9516a54e"},
}
DO_DAI_TOI_DA = 512   # token cho cả cặp (câu hỏi, chunk); chunk dài hơn bị cắt — như mô hình nhúng
_NAP: dict = {}


def thu_muc(ten: str):
    return ch.MODELS / f"reranker_{ten}"


def nap(ten: str):
    if ten not in _NAP:
        import torch
        from sentence_transformers import CrossEncoder

        dev = os.environ.get("RERANK_DEVICE") or ("cuda" if torch.cuda.is_available() else "cpu")
        m = CrossEncoder(str(thu_muc(ten)), max_length=DO_DAI_TOI_DA, device=dev)
        if dev == "cuda":
            m.model.half()
        _NAP[ten] = m
    return _NAP[ten]


def xep_lai(ten: str, cau_hoi: str, ung_vien: list[dict], lo: int = 16) -> list[tuple[dict, float]]:
    """Xếp lại danh sách chunk theo điểm cross-encoder (cao → thấp). Hoà điểm giữ thứ tự dense (sort ổn định)."""
    diem = nap(ten).predict([(cau_hoi, c["text"]) for c in ung_vien], batch_size=lo, show_progress_bar=False)
    thu_tu = sorted(range(len(ung_vien)), key=lambda i: -float(diem[i]))
    return [(ung_vien[i], float(diem[i])) for i in thu_tu]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--tai", action="store_true")
    ap.add_argument("--kiem", choices=list(MO_HINH))
    a = ap.parse_args()
    if a.tai:
        from huggingface_hub import snapshot_download
        for ten, m in MO_HINH.items():
            print("Tải", m["repo"], "@", m["revision"][:10])
            snapshot_download(m["repo"], revision=m["revision"], local_dir=thu_muc(ten),
                              allow_patterns=["*.json", "*.safetensors", "*.model", "*.txt"])
    if a.kiem:
        q = "Thời hạn của giấy phép lao động tối đa là bao lâu?"
        cs = [{"text": "Thời hạn của giấy phép lao động tối đa là 02 năm."},
              {"text": "Người lao động có quyền đơn phương chấm dứt hợp đồng lao động."}]
        for c, s in xep_lai(a.kiem, q, cs):
            print(f"{s:+.3f}  {c['text']}")


if __name__ == "__main__":
    main()
