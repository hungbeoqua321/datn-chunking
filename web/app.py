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
from fastapi.staticfiles import StaticFiles
from markdown_it import MarkdownIt

import cau_hinh as ch

R = ch.RESULTS
app = FastAPI(title="ĐATN — phân đoạn VBQPPL cho RAG", docs_url=None, redoc_url=None, openapi_url=None)
app.mount("/static", StaticFiles(directory=Path(__file__).parent / "static"), name="static")
MD = MarkdownIt("commonmark", {"html": False, "linkify": False}).enable("table")
VN = dt.timezone(dt.timedelta(hours=7))

CHUA_CO = {
    "bao_cao_so_sanh.md": "Chưa có báo cáo so sánh — bước 8 (viết báo cáo) chưa chạy.",
    "loi_phan_doan.md": "Chưa có bảng lỗi phân đoạn — bước 7 chưa chạy.",
    "metrics.csv": "Chưa có số liệu đánh giá — bước 5 (chạy đánh giá) chưa chạy.",
    "metrics.json": "Chưa có số liệu đánh giá — bước 5 (chạy đánh giá) chưa chạy.",
}

CSS = """
:root{--giay:#F5F7FA;--to:#FFFFFF;--muc:#17223A;--phu:#58627A;--ke:#D8DEE8;--son:#B3242B;--son-nhat:#F8E9EA;
--nen-ma:#EEF1F6;--chu:"Be Vietnam Pro",system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif;
--van:"Literata",Georgia,"Times New Roman",serif}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;font:16px/1.6 var(--chu);color:var(--muc);background:var(--giay);font-feature-settings:"tnum" 0}
a{color:var(--muc);text-decoration-color:var(--ke);text-underline-offset:3px}a:hover{text-decoration-color:var(--muc)}
:focus-visible{outline:2px solid var(--son);outline-offset:2px;border-radius:3px}
.dau-trang{background:var(--to);border-bottom:1px solid var(--ke)}
.dau-trang .trong{max-width:1240px;margin:0 auto;padding:14px 20px;display:flex;flex-wrap:wrap;gap:6px 28px;align-items:baseline}
.ten-de-tai{font-weight:600;font-size:15px;margin-right:auto;text-decoration:none}
.ten-de-tai span{color:var(--phu);font-weight:400}
.dau-trang nav{display:flex;flex-wrap:wrap;gap:4px 20px;font-size:15px}
.dau-trang nav a{text-decoration:none;color:var(--phu);padding:2px 0;border-bottom:2px solid transparent}
.dau-trang nav a:hover{color:var(--muc)}.dau-trang nav a[aria-current]{color:var(--muc);border-bottom-color:var(--son)}
main{max-width:1240px;margin:0 auto;padding:28px 20px 72px}
h1{font-size:1.75rem;line-height:1.25;font-weight:700;margin:0 0 .4em;letter-spacing:-.01em}
h2{font-size:1.25rem;line-height:1.3;font-weight:600;margin:2.2em 0 .6em}
h3{font-size:1.05rem;margin:1.6em 0 .4em}
.phu{color:var(--phu);font-size:14px}.loi{color:var(--son)}
/* trang đọc markdown (báo cáo, lỗi phân đoạn, kết quả từng bước) */
.doc{max-width:860px}.doc>p,.doc li,.doc blockquote{max-width:72ch}
.doc p,.doc li{font-family:var(--van);font-size:17px;line-height:1.7}
.doc table{border-collapse:collapse;margin:1.2em 0;font-size:14px;display:block;overflow-x:auto;max-width:100%;
background:var(--to);font-variant-numeric:tabular-nums}
.doc th,.doc td{border-bottom:1px solid var(--ke);padding:7px 12px;text-align:left;vertical-align:top}
.doc th{font-weight:600;border-bottom:2px solid var(--muc);white-space:nowrap}
.doc td:not(:first-child){white-space:nowrap}
.doc code{background:var(--nen-ma);padding:1px 5px;border-radius:4px;font-size:.88em}
.doc blockquote{margin:1em 0;padding:.2em 0 .2em 1em;border-left:3px solid var(--ke);color:var(--phu)}
.doc img{max-width:100%;height:auto;background:var(--to);border:1px solid var(--ke);border-radius:6px}
.lan-chay{display:inline-block;margin:0 0 1.6em;color:var(--phu);font-size:14px}
ul.ds-tep{list-style:none;padding:0;max-width:860px}ul.ds-tep li{padding:10px 0;border-bottom:1px solid var(--ke);
display:flex;flex-wrap:wrap;justify-content:space-between;gap:4px 16px}
@media(max-width:640px){main{padding:20px 16px 56px}h1{font-size:1.45rem}.doc p,.doc li{font-size:16px}}
@media(prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}
"""

TRANG_DIEU_HUONG = [("/", "Hỏi đáp"), ("/bao-cao", "Báo cáo so sánh"), ("/loi-phan-doan", "Lỗi phân đoạn"),
                    ("/ket-qua", "Kết quả từng bước"), ("/duyet", "Bộ câu hỏi"), ("/slide", "Slide bảo vệ"),
                    ("/api/tep", "Tải dữ liệu")]


def trang(tieu_de: str, than: str, duong_dan: str = "") -> HTMLResponse:
    nav = "".join(f'<a href="{u}"{" aria-current=page" if u == duong_dan else ""}>{t}</a>' for u, t in TRANG_DIEU_HUONG)
    return HTMLResponse(f'<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" '
                        f'content="width=device-width,initial-scale=1"><title>{html.escape(tieu_de)}</title>'
                        f'<link rel="stylesheet" href="/static/fonts/fonts.css"><style>{CSS}</style></head><body>'
                        f'<header class="dau-trang"><div class="trong"><a class="ten-de-tai" href="/">Phân đoạn văn bản '
                        f'quy phạm pháp luật cho RAG <span>— đồ án tốt nghiệp</span></a><nav aria-label="Điều hướng">{nav}'
                        f'</nav></div></header><main>{than}</main></body></html>')


def khong_co(ten: str) -> HTMLResponse:
    thong_bao = CHUA_CO.get(ten, f"Chưa có tệp {ten} — bước tạo ra nó chưa chạy.")
    r = trang("Chưa có kết quả", f'<h1>Chưa có kết quả</h1><p>{html.escape(thong_bao)}</p>'
                                 '<p class="phu">Các tệp đã có: <a href="/ket-qua">Kết quả từng bước</a>.</p>')
    r.status_code = 404
    return r


def thoi_diem(p: Path) -> str:
    return dt.datetime.fromtimestamp(p.stat().st_mtime, VN).strftime("%H:%M ngày %d/%m/%Y (giờ Việt Nam)")


def render_md(p: Path, tieu_de: str, goc_anh: str = "/bieu-do/", duong_dan: str = "") -> HTMLResponse:
    text = p.read_text()
    # ảnh trong markdown trỏ tới tệp png cùng thư mục → /bieu-do/<tên>.png
    text = re.sub(r"\]\((?:\./)?(?:results/)?([\w\-]+\.png)\)", lambda m: f"]({goc_anh}{m.group(1)})", text)
    than = (f'<span class="lan-chay">Số liệu của lần chạy lúc {thoi_diem(p)}, tệp '
            f'<a href="/tep/{html.escape(str(p.relative_to(R)))}">{html.escape(p.name)}</a></span>')
    return trang(tieu_de, f'<article class="doc">{MD.render(text)}{than}</article>', duong_dan)


# ── kết quả (chỉ đọc) ───────────────────────────────────────────────────────
@app.get("/healthz", response_class=PlainTextResponse)
def healthz():
    return "ok"


@app.get("/bao-cao", response_class=HTMLResponse)
def bao_cao():
    p = R / "bao_cao_so_sanh.md"
    return render_md(p, "Báo cáo so sánh", duong_dan="/bao-cao") if p.exists() else khong_co(p.name)


@app.get("/bao-cao.md")
def bao_cao_md():
    p = R / "bao_cao_so_sanh.md"
    if not p.exists():
        return PlainTextResponse(CHUA_CO[p.name], status_code=404)
    return PlainTextResponse(p.read_text(), media_type="text/plain; charset=utf-8")


@app.get("/loi-phan-doan", response_class=HTMLResponse)
def loi_phan_doan():
    p = R / "loi_phan_doan.md"
    return render_md(p, "Lỗi phân đoạn", duong_dan="/loi-phan-doan") if p.exists() else khong_co(p.name)


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
                 f'<span class="phu">{thoi_diem(p)}</span></li>' for p in ds)
    return trang("Kết quả từng bước", f'<h1>Kết quả từng bước</h1><p class="phu">Mọi bảng thống kê trong thư mục '
                                      f'kết quả, đọc thẳng từ đĩa ở mỗi lần mở trang.</p><ul class="ds-tep">{li}</ul>',
                 "/ket-qua")


@app.get("/ket-qua/{duong_dan:path}", response_class=HTMLResponse)
def ket_qua_tep(duong_dan: str):
    p = (R / duong_dan).resolve()
    if p.suffix != ".md" or R.resolve() not in p.parents or not p.exists() or p not in [x.resolve() for x in _ds_md()]:
        return khong_co(duong_dan)
    return render_md(p, p.stem, duong_dan="/ket-qua")


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
    if pp not in ("A", "A+", "B", "B+", "C", "D"):
        return JSONResponse({"loi": "Cách phân đoạn phải là A, C, D, B, B+ hoặc A+."}, status_code=400)
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
                         "trich": c["text"][len(c.get("tien_to") or ""):].strip()[:2500]}
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
    return trang("Hỏi đáp văn bản quy phạm pháp luật", (Path(__file__).parent / "static/hoi.html").read_text(), "/")


# ── bộ câu hỏi đang duyệt (chỉ đọc; sửa trong eval/questions.review.md) ───────
@app.get("/api/duyet")
def api_duyet():
    """Bộ câu hỏi nháp + trạng thái hiện tại trong file duyệt + cờ sàng lọc/kiểm tra + nguyên văn gold."""
    from chunking.base import nap_van_ban
    from eval.duyet import CAN, DUYET, NHAP, TRUNG_LAP, _doc_dong, nhan

    if not NHAP.exists():
        return JSONResponse({"loi": "Chưa có bộ câu hỏi nháp — bước 4 chưa chạy."}, status_code=404)
    docs = {d.doc_id: d for d in nap_van_ban()}
    tt = _doc_dong(DUYET.read_text()) if DUYET.exists() else {}
    ra = []
    for x in map(json.loads, NHAP.read_text().splitlines()):
        d = tt.get(x["qid"], {})
        ra.append({"qid": x["qid"], "loai": x["loai"], "trung_lap": bool(x.get("trung_lap")),
                   "phien_ban": bool(x.get("phien_ban")),
                   "trang_thai": d.get("Trạng thái") or ("XOÁ" if x.get("xoa") else "DỰ PHÒNG" if x.get("du_phong") else "GIỮ"),
                   "cau_hoi": d.get("Câu hỏi") or x.get("question", ""), "dap_an": x.get("dap_an_nhap", ""),
                   "co": (x.get("san_loc_co") or []) + (["kiểm tra tự động"] if x.get("kiem_tra") else [])
                         + (["nguồn đã chứa đáp án"] if x.get("nguon_chua_dap_an") else [])
                         + (["gold ở bản cũ"] if x.get("ban_cu") else []),
                   "ghi_chu": [v for v in (x.get("kiem_tra"), x.get("nguon_chua_dap_an"), x.get("ban_cu"), x.get("san_loc")) if v],
                   "gold": [{"nhan": nhan(g), "vai": g.get("vai"),
                             "text": docs[g["doc_id"]].text[g["start"]:g["end"]][:1500]} for g in x["gold"]]})
    return JSONResponse({"chi_tieu": CAN, "trung_lap": TRUNG_LAP, "cau": ra,
                         "thoi_diem": thoi_diem(DUYET) if DUYET.exists() else None})


@app.get("/duyet", response_class=HTMLResponse)
def trang_duyet():
    return trang("Bộ câu hỏi đánh giá", (Path(__file__).parent / "static/duyet.html").read_text(), "/duyet")


@app.get("/slide", response_class=HTMLResponse)
def trang_slide():
    """Slide bảo vệ (reveal.js). Trả NGUYÊN trang, không bọc khung site: deck phải chiếm trọn màn hình.
    In ra PDF: mở /slide?print-pdf rồi Ctrl+P → Save as PDF (xem README)."""
    return HTMLResponse((Path(__file__).parent / "static/slide.html").read_text())
