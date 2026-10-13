"""Web demo + xem kết quả thực nghiệm (FastAPI). Chạy: uvicorn web.app:app --host 127.0.0.1 --port 8081

Đường dẫn (theo đề):
  /                  trang hỏi đáp, công tắc A / A+ / B / B+, bảng chunk truy hồi kèm số hiệu/Điều/khoản
  /bao-cao           results/bao_cao_so_sanh.md render HTML (bảng kẻ khung, biểu đồ chèn đúng chỗ, thời điểm chạy)
  /bao-cao.md        markdown thô (text/plain) để copy vào Word
  /loi-phan-doan     results/loi_phan_doan.md render HTML
  /api/metrics       toàn bộ số liệu dạng JSON;  /api/metrics.csv  tải metrics.csv
  /bieu-do/<tên>.png biểu đồ;  /healthz  "ok"
Thêm: /ket-qua (mục lục, HTML), /ket-qua/<đường dẫn>.md (HTML), /api/tep (danh sách file JSON),
  /tep/<đường dẫn> (tải nguyên văn md/csv/json/png trong results/), POST /api/hoi (SSE).

Nhóm đường dẫn kết quả CHỈ ĐỌC, đọc file từ đĩa ở MỖI request (chạy lại thực nghiệm là web có số mới, không cần
restart); file chưa có thì trả 404 kèm câu tiếng Việt nói rõ bước nào chưa chạy.
"""
import asyncio
import csv
import datetime as dt
import html
import io
import json
import re
import time
from collections import defaultdict, deque
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, PlainTextResponse, StreamingResponse
from markdown_it import MarkdownIt

import cau_hinh as ch

R = ch.RESULTS
app = FastAPI(title="ĐATN — phân đoạn VBQPPL cho RAG", docs_url=None, redoc_url=None, openapi_url=None)
MD = MarkdownIt("commonmark", {"html": False, "linkify": False}).enable("table")
VN = dt.timezone(dt.timedelta(hours=7))

CHUA_CO = {
    "bao_cao_so_sanh.md": "Chưa có báo cáo so sánh — bước 8 (viết báo cáo) chưa chạy.",
    "loi_phan_doan.md": "Chưa có bảng lỗi phân đoạn — bước 7 chưa chạy.",
    "metrics.csv": "Chưa có số liệu đánh giá — bước 5 (chạy đánh giá) chưa chạy.",
    "metrics.json": "Chưa có số liệu đánh giá — bước 5 (chạy đánh giá) chưa chạy.",
}

CSS = """
:root{--chu:#1d2433;--nhat:#5b6475;--vien:#d5dae3;--nen:#ffffff;--nen2:#f5f7fa;--nhan:#0b5cad}
*{box-sizing:border-box}body{margin:0;font:16px/1.6 system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif;
color:var(--chu);background:var(--nen)}main{max-width:1100px;margin:0 auto;padding:24px 16px 64px}
header.dau{border-bottom:1px solid var(--vien);background:var(--nen2)}header.dau nav{max-width:1100px;margin:0 auto;
padding:10px 16px;display:flex;gap:18px;flex-wrap:wrap;font-size:15px}a{color:var(--nhan)}
h1{font-size:1.6em;line-height:1.3}h2{margin-top:2em;border-bottom:1px solid var(--vien);padding-bottom:.2em}
table{border-collapse:collapse;margin:1em 0;font-size:14px;display:block;overflow-x:auto;max-width:100%}
th,td{border:1px solid #9aa3b2;padding:5px 9px;text-align:left;vertical-align:top}th{background:#eef1f6}
tr:nth-child(even) td{background:#fafbfc}code{background:#f0f2f6;padding:1px 4px;border-radius:3px;font-size:.92em}
blockquote{margin:.6em 0;padding:.4em 1em;border-left:4px solid var(--vien);color:var(--nhat);background:var(--nen2)}
img{max-width:100%;height:auto;border:1px solid var(--vien)}.meta{color:var(--nhat);font-size:14px}
.o{display:flex;gap:8px;flex-wrap:wrap;align-items:center}textarea{width:100%;min-height:90px;font:inherit;padding:10px;
border:1px solid #9aa3b2;border-radius:6px}button{font:inherit;padding:8px 18px;border-radius:6px;border:1px solid var(--nhan);
background:var(--nhan);color:#fff;cursor:pointer}button:disabled{opacity:.5;cursor:wait}
.cong-tac label{border:1px solid #9aa3b2;border-radius:6px;padding:5px 12px;cursor:pointer;user-select:none}
.cong-tac input{margin-right:6px}#tra-loi{white-space:pre-wrap;background:var(--nen2);border:1px solid var(--vien);
border-radius:6px;padding:12px;min-height:3em}.loi{color:#a40000}
@media(max-width:640px){body{font-size:15px}th,td{padding:4px 6px}}
"""


def trang(tieu_de: str, than: str) -> HTMLResponse:
    nav = ('<header class="dau"><nav><a href="/">Hỏi đáp</a><a href="/bao-cao">Báo cáo so sánh</a>'
           '<a href="/loi-phan-doan">Lỗi phân đoạn</a><a href="/ket-qua">Kết quả từng bước</a>'
           '<a href="/api/metrics">API số liệu</a><a href="/api/tep">Tải file</a></nav></header>')
    return HTMLResponse(f'<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" '
                        f'content="width=device-width,initial-scale=1"><title>{html.escape(tieu_de)}</title>'
                        f'<style>{CSS}</style></head><body>{nav}<main>{than}</main></body></html>')


def khong_co(ten: str) -> HTMLResponse:
    thong_bao = CHUA_CO.get(ten, f"Chưa có tệp {ten} — bước tạo ra nó chưa chạy.")
    r = trang("Chưa có kết quả", f"<h1>Chưa có kết quả</h1><p>{html.escape(thong_bao)}</p>")
    r.status_code = 404
    return r


def thoi_diem(p: Path) -> str:
    return dt.datetime.fromtimestamp(p.stat().st_mtime, VN).strftime("%H:%M ngày %d/%m/%Y (giờ Việt Nam)")


def render_md(p: Path, tieu_de: str, goc_anh: str = "/bieu-do/") -> HTMLResponse:
    text = p.read_text()
    # ảnh trong markdown trỏ tới tệp png cùng thư mục → /bieu-do/<tên>.png
    text = re.sub(r"\]\((?:\./)?(?:results/)?([\w\-]+\.png)\)", lambda m: f"]({goc_anh}{m.group(1)})", text)
    than = f'<p class="meta">Số liệu của lần chạy lúc {thoi_diem(p)} · tệp <code>{html.escape(p.name)}</code></p>'
    return trang(tieu_de, than + MD.render(text))


# ── kết quả (chỉ đọc) ───────────────────────────────────────────────────────
@app.get("/healthz", response_class=PlainTextResponse)
def healthz():
    return "ok"


@app.get("/bao-cao", response_class=HTMLResponse)
def bao_cao():
    p = R / "bao_cao_so_sanh.md"
    return render_md(p, "Báo cáo so sánh") if p.exists() else khong_co(p.name)


@app.get("/bao-cao.md")
def bao_cao_md():
    p = R / "bao_cao_so_sanh.md"
    if not p.exists():
        return PlainTextResponse(CHUA_CO[p.name], status_code=404)
    return PlainTextResponse(p.read_text(), media_type="text/plain; charset=utf-8")


@app.get("/loi-phan-doan", response_class=HTMLResponse)
def loi_phan_doan():
    p = R / "loi_phan_doan.md"
    return render_md(p, "Lỗi phân đoạn") if p.exists() else khong_co(p.name)


@app.get("/api/metrics")
def api_metrics():
    pj, pc = R / "metrics.json", R / "metrics.csv"
    if pj.exists():
        o = json.loads(pj.read_text())
    elif pc.exists():
        o = {"metrics": list(csv.DictReader(io.StringIO(pc.read_text())))}
    else:
        return JSONResponse({"loi": CHUA_CO["metrics.csv"]}, status_code=404)
    o["thoi_diem"] = thoi_diem(pj if pj.exists() else pc)
    return JSONResponse(o)


@app.get("/api/metrics.csv")
def api_metrics_csv():
    p = R / "metrics.csv"
    if not p.exists():
        return PlainTextResponse(CHUA_CO["metrics.csv"], status_code=404)
    return FileResponse(p, media_type="text/csv; charset=utf-8", filename="metrics.csv")


@app.get("/bieu-do/{ten}")
def bieu_do(ten: str):
    if not re.fullmatch(r"[\w\-]+\.png", ten):
        return PlainTextResponse("Tên biểu đồ không hợp lệ.", status_code=404)
    p = next((x for x in (R / ten, *R.glob(f"*/{ten}")) if x.exists()), None)
    if not p:
        return PlainTextResponse(f"Chưa có biểu đồ {ten} — bước 8 (vẽ biểu đồ) chưa chạy.", status_code=404)
    return FileResponse(p, media_type="image/png")


def _ds_md() -> list[Path]:
    return sorted([p for p in R.rglob("*.md") if "gen" not in p.parts], key=lambda p: str(p))


@app.get("/ket-qua", response_class=HTMLResponse)
def ket_qua():
    ds = _ds_md()
    li = "".join(f'<li><a href="/ket-qua/{html.escape(str(p.relative_to(R)))}">{html.escape(str(p.relative_to(R)))}</a>'
                 f' <span class="meta">— {thoi_diem(p)}</span></li>' for p in ds)
    return trang("Kết quả từng bước", f"<h1>Kết quả từng bước</h1><p>Mọi tệp markdown trong <code>results/</code>, "
                                      f"đọc trực tiếp từ đĩa.</p><ul>{li}</ul>")


@app.get("/ket-qua/{duong_dan:path}", response_class=HTMLResponse)
def ket_qua_tep(duong_dan: str):
    p = (R / duong_dan).resolve()
    if p.suffix != ".md" or R.resolve() not in p.parents or not p.exists() or p not in [x.resolve() for x in _ds_md()]:
        return khong_co(duong_dan)
    return render_md(p, p.stem)


# ── tải file kết quả thô (để pull bằng curl/wget/script) ─────────────────────
DUOI_TAI = {".md": "text/plain; charset=utf-8", ".csv": "text/csv; charset=utf-8", ".txt": "text/plain; charset=utf-8",
            ".json": "application/json", ".jsonl": "application/x-ndjson", ".png": "image/png"}


def _ds_tai() -> dict[str, Path]:
    """{đường dẫn công khai: tệp} — mọi tệp trong results/ (trừ câu trả lời thô results/gen/, chỉ mở thống kê và nhật ký
    token) + bộ câu hỏi, gold và cờ sàng lọc trong eval/."""
    ra = {str(p.relative_to(R)): p for p in sorted(R.rglob("*")) if p.is_file() and p.suffix in DUOI_TAI
          and ("gen" not in p.parts or p.name in ("thong_ke_token.md", "nhat_ky_goi.jsonl"))
          and not p.name.startswith(".") and not p.name.endswith(".tmp")}
    for p in sorted((ch.GOC / "eval").glob("*")):
        if p.is_file() and p.suffix in DUOI_TAI and (p.name.startswith(("questions", "gold", "san_loc"))):
            ra[f"eval/{p.name}"] = p
    return ra


@app.get("/api/tep")
def api_tep():
    """Danh sách mọi file kết quả tải được: [{duong_dan, url, byte, thoi_diem}] — dùng để pull hàng loạt."""
    return JSONResponse([{"duong_dan": k, "url": f"/tep/{k}", "byte": p.stat().st_size, "thoi_diem": thoi_diem(p)}
                         for k, p in _ds_tai().items()])


@app.get("/tep/{duong_dan:path}")
def tep(duong_dan: str):
    """Tải nguyên văn một tệp (md, csv, json, jsonl, txt, png) — chỉ các tệp có trong /api/tep."""
    p = _ds_tai().get(duong_dan)
    if p is None:
        return PlainTextResponse(f"Không có tệp {duong_dan} (hoặc bước tạo ra nó chưa chạy). "
                                 "Danh sách tệp: /api/tep", status_code=404)
    return FileResponse(p, media_type=DUOI_TAI[p.suffix], filename=p.name if p.suffix != ".png" else None)


# ── hỏi đáp (POST /api/hoi, SSE) ────────────────────────────────────────────
_HANG = asyncio.Semaphore(1)        # mỗi lúc chỉ một lượt sinh (CPU)
_CHO = 0
_LUOT: dict[str, deque] = defaultdict(deque)
GIOI_HAN = [(60, 5), (3600, 30)]    # mỗi IP: 5 câu/phút, 30 câu/giờ


def _qua_gioi_han(ip: str) -> int | None:
    now = time.time()
    q = _LUOT[ip]
    while q and now - q[0] > 3600:
        q.popleft()
    for cua_so, toi_da in GIOI_HAN:
        if sum(1 for t in q if now - t <= cua_so) >= toi_da:
            return cua_so
    q.append(now)
    return None


def _cache_tra_loi(q: str, pp: str) -> dict | None:
    """Câu hỏi trùng câu trong bộ đánh giá → trả câu trả lời đã sinh sẵn (không chiếm CPU)."""
    pq = ch.GOC / "eval/questions.jsonl"
    if not pq.exists():
        return None
    for x in map(json.loads, pq.read_text().splitlines()):
        if x["question"].strip() == q.strip():
            p = R / "gen" / pp.replace("+", "cong") / f"{x['qid']}.json"
            if p.exists():
                return json.loads(p.read_text())
    return None


@app.post("/api/hoi")
async def api_hoi(request: Request):
    global _CHO
    try:
        body = await request.json()
    except Exception:  # noqa: BLE001
        return JSONResponse({"loi": "Yêu cầu không hợp lệ."}, status_code=400)
    q = str(body.get("cau_hoi", "")).strip()
    pp = str(body.get("phuong_phap", "B"))
    if pp not in ("A", "A+", "B", "B+"):
        return JSONResponse({"loi": "Phương pháp phải là A, A+, B hoặc B+."}, status_code=400)
    if not 3 <= len(q) <= 500:
        return JSONResponse({"loi": "Câu hỏi phải dài từ 3 đến 500 ký tự."}, status_code=400)
    ip = request.client.host if request.client else "?"
    cs = _qua_gioi_han(ip)
    if cs:
        return JSONResponse({"loi": f"Bạn hỏi quá nhanh — thử lại sau ít phút (giới hạn theo {cs // 60} phút)."},
                            status_code=429, headers={"Retry-After": str(min(cs, 600))})
    from rag import truy_hoi

    ten = truy_hoi.TEP[pp]
    if not (ch.INDEX / ten / "emb.f32").exists():
        return JSONResponse({"loi": "Chưa có chỉ mục vector — bước 5 (nhúng) chưa chạy."}, status_code=503)
    if _CHO >= 3:
        return JSONResponse({"loi": "Máy đang bận trả lời người khác — thử lại sau một phút."}, status_code=503,
                            headers={"Retry-After": "60"})

    async def luong():
        global _CHO
        _CHO += 1
        try:
            async with _HANG:
                t0 = time.monotonic()
                qv = await asyncio.to_thread(truy_hoi.nhung_cau_hoi, q)
                kq = await asyncio.to_thread(truy_hoi.tim, pp, qv, ch.K_UNG_VIEN)
                from rag import sinh

                khoi = await asyncio.to_thread(truy_hoi.ngu_canh, pp, kq)  # các khối thật sự đưa cho mô hình
                dung = {k["chunk_id"] for k in khoi}
                bang = [{"hang": i + 1, "diem": round(s, 4), "so_hieu": c["so_hieu"], "dieu": c.get("dieu_so"),
                         "khoan": c.get("khoan_so"), "diem_chu": c.get("diem"), "tien_to": c.get("tien_to", ""),
                         "trich": c["text"][len(c.get("tien_to") or ""):][:700]}
                        for i, (c, s) in enumerate(kq) if c["chunk_id"] in dung]
                yield f"event: chunks\ndata: {json.dumps(bang, ensure_ascii=False)}\n\n"
                cache = _cache_tra_loi(q, pp)
                if cache:
                    yield f"data: {json.dumps({'t': cache['tra_loi']}, ensure_ascii=False)}\n\n"
                    yield f"event: xong\ndata: {json.dumps({'giay': round(time.monotonic() - t0, 1), 'cache': True})}\n\n"
                    return
                cl = sinh.client()
                ts = sinh.tham_so()
                tn = sinh.dung_tin_nhan(q, khoi)
                noi_dung = await asyncio.to_thread(lambda: sum(sinh.dem_token(m["content"]) for m in tn))
                ctx = await asyncio.to_thread(sinh.n_ctx)
                if noi_dung + ts["max_tokens"] > ctx:  # cùng phép kiểm như khi đánh giá: không trả lời trên dữ liệu bị cắt
                    yield f"event: loi\ndata: {json.dumps({'loi': f'Ngữ cảnh {noi_dung} token vượt cửa sổ mô hình {ctx} — không trả lời.'}, ensure_ascii=False)}\n\n"
                    return
                stream = await asyncio.to_thread(lambda: cl.chat.completions.create(messages=tn, stream=True, **ts))
                it = iter(stream)
                ly_do = None
                while True:
                    if await request.is_disconnected():
                        stream.close()
                        return
                    part = await asyncio.to_thread(next, it, None)
                    if part is None:
                        break
                    d = part.choices[0].delta.content if part.choices else None
                    if part.choices and part.choices[0].finish_reason:
                        ly_do = part.choices[0].finish_reason
                    if d:
                        yield f"data: {json.dumps({'t': d}, ensure_ascii=False)}\n\n"
                yield (f"event: xong\ndata: {json.dumps({'giay': round(time.monotonic() - t0, 1), 'token_vao': noi_dung, 'n_ctx': ctx, 'bi_cat': ly_do == 'length'})}\n\n")
        except Exception as e:  # noqa: BLE001
            yield f"event: loi\ndata: {json.dumps({'loi': 'Lỗi khi trả lời: ' + type(e).__name__}, ensure_ascii=False)}\n\n"
        finally:
            _CHO -= 1

    return StreamingResponse(luong(), media_type="text/event-stream",
                             headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})


@app.get("/", response_class=HTMLResponse)
def trang_chu():
    return trang("Hỏi đáp VBQPPL — so sánh phân đoạn", (Path(__file__).parent / "static/hoi.html").read_text())
