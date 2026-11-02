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


def dung_tin_nhan(cau_hoi: str, khoi: list[dict], he_thong: str = HE_THONG) -> list[dict]:
    return [
        {"role": "system", "content": he_thong},
        {"role": "user", "content": f"NGỮ CẢNH:\n{dung_ngu_canh(khoi)}\n\nCÂU HỎI: {cau_hoi}"},
    ]


class LoiCat(RuntimeError):
    """Có dấu hiệu dữ liệu bị cắt khi gọi mô hình sinh — phải DỪNG cả job, không được ra số liệu từ lần gọi này."""


NHAT_KY = ch.RESULTS / "gen" / "nhat_ky_goi.jsonl"
THONG_KE_TOKEN = ch.RESULTS / "gen" / "thong_ke_token.md"
_N_CTX: int | None = None


def client():
    from openai import OpenAI

    return OpenAI(base_url=os.environ["LLM_BASE_URL"], api_key=os.environ.get("LLM_API_KEY") or "khong-can",
                  timeout=900)


def tham_so() -> dict:
    """Tham số sinh cố định (ghi kèm mỗi câu trả lời trong cache).

    LLM_TAT_NGHI=1: tắt chế độ suy nghĩ của mô hình Qwen3 lai (bản 8B dùng ở thử nghiệm mô hình lớn hơn,
    results/local_gpu/thu_them.md) — bản 4B-Instruct-2507 không có chế độ này nên mặc định không gửi gì thêm."""
    extra = {"cache_prompt": False}
    if os.environ.get("LLM_TAT_NGHI"):
        extra["chat_template_kwargs"] = {"enable_thinking": False}
    return {"model": os.environ["LLM_MODEL"], "temperature": 0, "seed": 42,
            "max_tokens": ch.MAX_TOKENS_TRA_LOI, "extra_body": extra}


def n_ctx() -> int:
    """Cửa sổ ngữ cảnh THẬT của llama-server đang chạy: đọc /props, không có thì /v1/models — không hardcode."""
    global _N_CTX
    if _N_CTX is None:
        import requests

        base = os.environ["LLM_BASE_URL"].rstrip("/").removesuffix("/v1")
        p = requests.get(base + "/props", timeout=30).json()
        v = (p.get("default_generation_settings") or {}).get("n_ctx") or p.get("n_ctx")
        if not v:
            m = requests.get(base + "/v1/models", timeout=30).json()
            v = next((x.get("meta", {}).get("n_ctx") for x in m.get("data", [])), None)
        if not v:
            # KHÔNG phải LoiCat: LoiCat bị các script sinh ghi thành "cắt trần" (một kết quả hợp lệ trong mẫu). Không
            # đọc được trần là lỗi hạ tầng → phải dừng cả job (02/11: server chết, 26 lượt E3b bị ghi nhầm là cắt trần).
            raise RuntimeError("không đọc được n_ctx từ /props hay /v1/models — không chạy khi chưa biết trần ngữ cảnh")
        _N_CTX = int(v)
    return _N_CTX


def _dung(ly_do: str) -> None:
    xuat_thong_ke_token()
    raise LoiCat(ly_do)


def goi(tin_nhan: list[dict], nhan: dict, cl=None, **ts):
    """Gọi llama-server MỘT lần, ghi một dòng vào NHAT_KY, DỪNG (LoiCat) ngay khi có dấu hiệu bị cắt.

    `nhan`: qid, bien_the, seed, so_khoi, so_tu_ngu_canh (+ trường phụ tuỳ ý). Dừng khi:
      1. TRƯỚC khi gọi: token prompt (đếm bằng tokenizer của chính mô hình) + max_tokens > n_ctx;
      2. SAU khi gọi: token_prompt server báo nhỏ hơn số đã đếm (prompt bị cắt phía server);
      3. token_prompt + token_tra_loi chạm n_ctx;
      4. ly_do_dung (finish_reason) = "length" — không thử lại, dừng luôn.
    Trả (phản hồi, dòng nhật ký)."""
    import time

    cl = cl or client()
    ctx = n_ctx()
    dem = sum(dem_token(m["content"]) for m in tin_nhan)  # chưa tính vài token khung chat template
    if dem + ts["max_tokens"] > ctx:
        _dung(f"{nhan.get('bien_the')} {nhan.get('qid')}: prompt {dem} token + trả lời tối đa {ts['max_tokens']} "
              f"> n_ctx {ctx} — sẽ bị cắt; giảm ngân sách")
    t0 = time.monotonic()
    r = cl.chat.completions.create(messages=tin_nhan, **ts)
    u, ly_do = r.usage, r.choices[0].finish_reason
    ghi = {"qid": nhan.get("qid"), "bien_the": nhan.get("bien_the"), "seed": nhan.get("seed"),
           "token_prompt": u.prompt_tokens, "token_tra_loi": u.completion_tokens, "n_ctx": ctx, "ly_do_dung": ly_do,
           "so_khoi": nhan.get("so_khoi"), "so_tu_ngu_canh": nhan.get("so_tu_ngu_canh"),
           "thoi_gian_giay": round(time.monotonic() - t0, 1),
           **{k: v for k, v in nhan.items() if k not in ("qid", "bien_the", "seed", "so_khoi", "so_tu_ngu_canh")},
           "token_dem_truoc": dem, "max_tokens": ts["max_tokens"], "thoi_diem": time.strftime("%Y-%m-%dT%H:%M:%S")}
    NHAT_KY.parent.mkdir(parents=True, exist_ok=True)
    with open(NHAT_KY, "a") as f:
        f.write(json.dumps(ghi, ensure_ascii=False) + "\n")
    if u.prompt_tokens < dem:
        _dung(f"server chỉ nhận {u.prompt_tokens}/{dem} token prompt — prompt bị cắt: {ghi}")
    if u.prompt_tokens + u.completion_tokens >= ctx:
        _dung(f"chạm n_ctx {ctx} — có thể đã bị cắt: {ghi}")
    if ly_do == "length":
        _dung(f"câu trả lời bị cắt vì hết max_tokens: {ghi}")
    return r, ghi


def tra_loi(cau_hoi: str, khoi: list[dict], cl=None, nhan: dict | None = None, he_thong: str = HE_THONG) -> dict:
    """Sinh câu trả lời cho một câu hỏi từ các khối ngữ cảnh. `nhan` = {qid, bien_the, seed}.
    `he_thong` chỉ đổi ở thử nghiệm lời nhắc (eval/thu_them.py); mọi bảng chính dùng HE_THONG."""
    ts = tham_so()
    r, ghi = goi(dung_tin_nhan(cau_hoi, khoi, he_thong),
                 {**(nhan or {}), "so_khoi": len(khoi), "so_tu_ngu_canh": sum(len(k["text"].split()) for k in khoi),
                  "khoi_bi_cat": sum(bool(k.get("bi_cat")) for k in khoi)}, cl, **ts)
    return {"tra_loi": r.choices[0].message.content, "usage": r.usage.model_dump(), "finish_reason": ghi["ly_do_dung"],
            "n_ctx": ghi["n_ctx"], "token_dem_truoc": ghi["token_dem_truoc"],
            "tham_so": {k: v for k, v in ts.items() if k != "extra_body"}}


def xuat_thong_ke_token() -> None:
    """NHAT_KY → THONG_KE_TOKEN: theo từng biến thể — số lần gọi, trung vị/max token_prompt, max tổng, biên nhỏ nhất
    tới n_ctx, số lần chạm trần, số lần bị cắt (ly_do_dung = length)."""
    import statistics as st

    if not NHAT_KY.exists():
        return
    ds = [json.loads(x) for x in NHAT_KY.read_text().splitlines() if x.strip()]
    L = ["# Thống kê token các lần gọi mô hình sinh", "",
         f"Nguồn: `{str(NHAT_KY).removeprefix(str(ch.GOC) + '/')}` ({len(ds)} lần gọi). Chạm trần = token_prompt + token_tra_loi ≥ n_ctx; "
         "bị cắt = ly_do_dung là `length`. Hai cột này khác 0 nghĩa là job đã bị dừng ở lần gọi đó.", "",
         "| Biến thể | Lần gọi | token_prompt trung vị | token_prompt max | max prompt + trả lời | n_ctx | Biên nhỏ nhất tới trần "
         "| Chạm trần | Bị cắt | Số khối TV | Từ ngữ cảnh TV | Giây TV |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for bt in sorted({str(d.get("bien_the")) for d in ds}):
        x = [d for d in ds if str(d.get("bien_the")) == bt]
        tong = [d["token_prompt"] + d["token_tra_loi"] for d in x]
        L.append(f"| {bt} | {len(x)} | {st.median(d['token_prompt'] for d in x):.0f} | {max(d['token_prompt'] for d in x)} "
                 f"| {max(tong)} | {max(d['n_ctx'] for d in x)} | {min(d['n_ctx'] - t for d, t in zip(x, tong))} "
                 f"| {sum(t >= d['n_ctx'] for d, t in zip(x, tong))} | {sum(d['ly_do_dung'] == 'length' for d in x)} "
                 f"| {st.median(d.get('so_khoi') or 0 for d in x):.0f} | {st.median(d.get('so_tu_ngu_canh') or 0 for d in x):.0f} "
                 f"| {st.median(d['thoi_gian_giay'] for d in x):.0f} |")
    THONG_KE_TOKEN.parent.mkdir(parents=True, exist_ok=True)
    THONG_KE_TOKEN.write_text("\n".join(L) + "\n")


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


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser(description="Tiện ích của khâu sinh câu trả lời.")
    ap.add_argument("--thong-ke-token", action="store_true", help=f"xuất {THONG_KE_TOKEN.relative_to(ch.GOC)} từ nhật ký gọi")
    if ap.parse_args().thong_ke_token:
        xuat_thong_ke_token()
        print("→", THONG_KE_TOKEN)
