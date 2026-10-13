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


class LoiCat(RuntimeError):
    """Có dấu hiệu dữ liệu bị cắt khi gọi mô hình sinh — phải DỪNG, không được ra số liệu từ lần gọi này."""


NHAT_KY = ch.RESULTS / "gen" / "nhat_ky_goi.jsonl"
_N_CTX: int | None = None


def client():
    from openai import OpenAI

    return OpenAI(base_url=os.environ["LLM_BASE_URL"], api_key=os.environ.get("LLM_API_KEY") or "khong-can",
                  timeout=900)


def tham_so() -> dict:
    """Tham số sinh cố định (ghi kèm mỗi câu trả lời trong cache)."""
    return {"model": os.environ["LLM_MODEL"], "temperature": 0, "seed": 42,
            "max_tokens": ch.MAX_TOKENS_TRA_LOI, "extra_body": {"cache_prompt": False}}


def n_ctx() -> int:
    """Cửa sổ ngữ cảnh THẬT của llama-server đang chạy (đọc từ /props, không giả định)."""
    global _N_CTX
    if _N_CTX is None:
        import requests

        base = os.environ["LLM_BASE_URL"].rstrip("/").removesuffix("/v1")
        p = requests.get(base + "/props", timeout=30).json()
        _N_CTX = int((p.get("default_generation_settings") or {}).get("n_ctx") or p.get("n_ctx"))
    return _N_CTX


def tra_loi(cau_hoi: str, khoi: list[dict], cl=None, nhan: dict | None = None) -> dict:
    """Gọi mô hình sinh MỘT lần, kiểm chặt việc cắt dữ liệu, ghi nhật ký số token thật.

    Dừng (LoiCat) khi:
      1. TRƯỚC khi gọi: số token prompt (đếm bằng tokenizer của chính mô hình) + max_tokens > n_ctx;
      2. SAU khi gọi: usage.prompt_tokens nhỏ hơn số token nội dung đã đếm (prompt bị cắt bớt ở phía server),
         hoặc prompt_tokens + completion_tokens chạm n_ctx;
      3. câu trả lời dừng vì hết max_tokens (finish_reason = "length") — thử lại MỘT lần với max_tokens gấp đôi nếu vẫn
         nằm trong n_ctx, vẫn bị cắt thì dừng.
    """
    import time

    cl = cl or client()
    ts = tham_so()
    tn = dung_tin_nhan(cau_hoi, khoi)
    noi_dung = sum(dem_token(m["content"]) for m in tn)  # chưa tính vài token khung chat template
    ctx = n_ctx()
    if noi_dung + ts["max_tokens"] > ctx:
        raise LoiCat(f"prompt {noi_dung} token + trả lời {ts['max_tokens']} > n_ctx {ctx} — sẽ bị cắt; giảm ngân sách")
    for lan in range(2):
        t0 = time.monotonic()
        r = cl.chat.completions.create(messages=tn, **ts)
        giay = time.monotonic() - t0
        u = r.usage
        ly_do = r.choices[0].finish_reason
        ghi = {"thoi_diem": time.strftime("%Y-%m-%dT%H:%M:%S"), **(nhan or {}), "lan": lan + 1,
               "prompt_tokens": u.prompt_tokens, "completion_tokens": u.completion_tokens, "token_noi_dung": noi_dung,
               "n_ctx": ctx, "max_tokens": ts["max_tokens"], "finish_reason": ly_do, "giay": round(giay, 1),
               "so_khoi": len(khoi), "ngu_canh_tu": sum(len(k["text"].split()) for k in khoi),
               "khoi_bi_cat": sum(bool(k.get("bi_cat")) for k in khoi)}
        NHAT_KY.parent.mkdir(parents=True, exist_ok=True)
        with open(NHAT_KY, "a") as f:
            f.write(json.dumps(ghi, ensure_ascii=False) + "\n")
        if u.prompt_tokens < noi_dung:
            raise LoiCat(f"server chỉ nhận {u.prompt_tokens}/{noi_dung} token prompt — prompt bị cắt: {ghi}")
        if u.prompt_tokens + u.completion_tokens >= ctx:
            raise LoiCat(f"chạm n_ctx {ctx} — có thể đã bị cắt: {ghi}")
        if ly_do == "length":
            if lan == 0 and u.prompt_tokens + 2 * ts["max_tokens"] < ctx:
                ts = {**ts, "max_tokens": 2 * ts["max_tokens"]}
                continue
            raise LoiCat(f"câu trả lời bị cắt vì hết max_tokens: {ghi}")
        return {"tra_loi": r.choices[0].message.content, "usage": u.model_dump(), "finish_reason": ly_do,
                "n_ctx": ctx, "token_noi_dung": noi_dung, "lan_goi": lan + 1,
                "tham_so": {k: v for k, v in ts.items() if k != "extra_body"}}
    raise LoiCat("không thể xảy ra")


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
