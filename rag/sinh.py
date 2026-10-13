"""Sinh câu trả lời từ ngữ cảnh truy hồi — GIỐNG HỆT nhau cho mọi phương pháp phân đoạn.

Gọi mô hình qua endpoint tương thích OpenAI (LLM_BASE_URL / LLM_API_KEY / LLM_MODEL trong .env).
Ở thực nghiệm này endpoint là llama-server chạy tại chỗ (tools/chay-llm.sh).

Các tham số cố định: temperature=0 (tham lam), seed cố định, max_tokens cố định, không cache prompt.
"""
import json
import os
from pathlib import Path

from dotenv import load_dotenv

import cau_hinh as ch

load_dotenv(ch.GOC / ".env")

# Prompt hệ thống: giống hệt cho A, A+, B, B+. Đổi prompt = đổi thực nghiệm.
HE_THONG = (
    "Bạn là trợ lý pháp lý. Chỉ được trả lời dựa trên các đoạn NGỮ CẢNH được cung cấp, "
    "không dùng hiểu biết bên ngoài.\n"
    "Quy tắc bắt buộc:\n"
    "1. Trả lời ngắn gọn, đúng trọng tâm câu hỏi, bằng tiếng Việt.\n"
    "2. Mỗi ý phải ghi căn cứ theo đúng dạng: \"Điều X khoản Y của <số hiệu văn bản>\" "
    "(không có khoản thì ghi \"Điều X của <số hiệu>\"; văn bản không chia Điều thì ghi \"<số hiệu>\"). "
    "Số hiệu chép NGUYÊN VĂN từ dòng [Nguồn: ...] của đoạn ngữ cảnh, không thêm tên loại văn bản, "
    "không đảo thứ tự (ví dụ đúng: \"Điều 5 khoản 2 của 12/2020/NĐ-CP\").\n"
    "3. Nếu ngữ cảnh không đủ để trả lời thì trả lời đúng một câu: "
    "\"Không đủ căn cứ trong ngữ cảnh được cung cấp.\" — không được tự suy đoán."
)


def dung_ngu_canh(khoi: list[dict]) -> str:
    """Mỗi khối: {so_hieu, text}. Dòng [Nguồn: số hiệu] là hằng số của pipeline cho mọi phương pháp."""
    return "\n\n".join(f"[Đoạn {i}] [Nguồn: {k['so_hieu']}]\n{k['text']}" for i, k in enumerate(khoi, 1))


def dung_tin_nhan(cau_hoi: str, khoi: list[dict]) -> list[dict]:
    return [
        {"role": "system", "content": HE_THONG},
        {"role": "user", "content": f"NGỮ CẢNH:\n{dung_ngu_canh(khoi)}\n\nCÂU HỎI: {cau_hoi}"},
    ]


def client():
    from openai import OpenAI

    return OpenAI(base_url=os.environ["LLM_BASE_URL"], api_key=os.environ.get("LLM_API_KEY") or "khong-can",
                  timeout=900)


def tham_so() -> dict:
    """Tham số sinh cố định (ghi kèm mỗi câu trả lời trong cache)."""
    return {"model": os.environ["LLM_MODEL"], "temperature": 0, "seed": 42,
            "max_tokens": ch.MAX_TOKENS_TRA_LOI, "extra_body": {"cache_prompt": False}}


def tra_loi(cau_hoi: str, khoi: list[dict], cl=None) -> dict:
    cl = cl or client()
    ts = tham_so()
    r = cl.chat.completions.create(messages=dung_tin_nhan(cau_hoi, khoi), **ts)
    return {"tra_loi": r.choices[0].message.content, "usage": r.usage.model_dump() if r.usage else None,
            "tham_so": {k: v for k, v in ts.items() if k != "extra_body"}}


def dem_token(van_ban: str, base: str | None = None) -> int:
    """Đếm token bằng tokenizer của chính mô hình sinh (POST /tokenize của llama-server)."""
    import requests

    base = (base or os.environ["LLM_BASE_URL"]).rstrip("/").removesuffix("/v1")
    r = requests.post(base + "/tokenize", json={"content": van_ban}, timeout=60)
    r.raise_for_status()
    return len(r.json()["tokens"])


def ghi_cache(p: Path, du_lieu: dict) -> None:
    """Ghi file tạm rồi đổi tên — dừng giữa chừng không để lại file hỏng."""
    p.parent.mkdir(parents=True, exist_ok=True)
    tam = p.with_suffix(".tmp")
    tam.write_text(json.dumps(du_lieu, ensure_ascii=False, indent=1))
    tam.replace(p)
