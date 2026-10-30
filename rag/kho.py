"""Kho vector ĐỘC LẬP với chỉ mục của đồ án — dùng cho web: kho đầy đủ 212 văn bản và tài liệu người dùng tải lên.

Chỉ mục đồ án (data/index/, 80 văn bản, nhiều cách phân đoạn) KHÔNG bị đụng. Mỗi kho là một thư mục:

  data/kho/<tên>/chunks.jsonl   chunk (cắt theo B: Điều → Khoản → Điểm, tiền tố phân cấp)
  data/kho/<tên>/emb.f32        ma trận N × 768 float32, cùng thứ tự với chunks.jsonl
  data/kho/<tên>/tai_lieu.json  danh sách văn bản trong kho (id, tên, số hiệu, số trang, OCR, số chunk, thời gian)

  day_du   cả 212 văn bản đã tải từ vbpl.vn (data/clean) — 80 văn bản của đồ án + 132 ứng viên còn lại
  tai_len  tài liệu người dùng tải lên web (.txt, .md, .docx, .pdf — PDF scan được OCR, bỏ dấu đỏ)

Nhúng bằng đúng mô hình của đồ án (rag/nhung.py, thiết bị theo NHUNG_DEVICE). Tìm theo cosine, hoà điểm phá bằng
thứ tự trong kho (ổn định trên mọi nền tảng — xem thuc_nghiem/tai_lap/GHI_CHU.md).

    python -m rag.kho dung-day-du        # dựng kho day_du (bỏ qua nếu đã có; --force để dựng lại)
    python -m rag.kho them <tệp>...      # thêm tài liệu vào kho tai_len từ dòng lệnh
    python -m rag.kho ds                 # liệt kê tài liệu trong các kho
"""
import argparse
import datetime as dt
import html
import hashlib
import io
import json
import os
import re
import subprocess
import threading
import time
import zipfile
from pathlib import Path

import numpy as np

import cau_hinh as ch
from chunking import structural
from chunking.base import Document

GOC_KHO = Path(os.environ.get("KHO_DIR", ch.DATA / "kho"))
DIM = 768
DUOI_HOP_LE = (".txt", ".md", ".docx", ".pdf")
PY_OCR = ch.GOC / ".venv-ocr" / ("Scripts/python.exe" if os.name == "nt" else "bin/python")


class Kho:
    def __init__(self, ten: str):
        self.ten = ten
        self.thu_muc = GOC_KHO / ten
        self._khoa = threading.Lock()
        self._m: np.ndarray | None = None
        self._cs: list[dict] = []
        self._mtime: float | None | str = "chua_nap"   # khác mọi mtime, kể cả None (kho rỗng)

    # ── đọc ──────────────────────────────────────────────────────────────
    def _p(self, t: str) -> Path:
        return self.thu_muc / t

    def tai_lieu(self) -> list[dict]:
        p = self._p("tai_lieu.json")
        return json.loads(p.read_text()) if p.exists() else []

    def nap(self) -> tuple[np.ndarray, list[dict]]:
        """Nạp lại nếu tệp đổi (tài liệu vừa thêm/xoá ở tiến trình khác)."""
        p = self._p("emb.f32")
        mt = p.stat().st_mtime if p.exists() else None
        if mt != self._mtime:
            if mt is None:
                self._m, self._cs = np.zeros((0, DIM), np.float32), []
            else:
                self._m = np.fromfile(p, dtype=np.float32).reshape(-1, DIM)
                self._cs = [json.loads(l) for l in open(self._p("chunks.jsonl"), encoding="utf-8") if l.strip()]
                assert len(self._cs) == len(self._m), f"kho {self.ten}: {len(self._cs)} chunk ≠ {len(self._m)} vector"
            self._mtime = mt
        return self._m, self._cs

    def tim(self, q_vec: np.ndarray, k: int = 10) -> list[tuple[dict, float]]:
        m, cs = self.nap()
        if not len(cs):
            return []
        s = m @ q_vec
        thu_tu = np.lexsort((np.arange(len(s)), -s))[:k]   # điểm giảm dần, hoà thì theo thứ tự trong kho
        return [(cs[i], float(s[i])) for i in thu_tu]

    # ── ghi ──────────────────────────────────────────────────────────────
    def _ghi(self, m: np.ndarray, cs: list[dict], tl: list[dict]) -> None:
        self.thu_muc.mkdir(parents=True, exist_ok=True)
        for ten, viet in (("chunks.jsonl", lambda f: f.writelines(json.dumps(c, ensure_ascii=False) + "\n" for c in cs)),
                          ("tai_lieu.json", lambda f: f.write(json.dumps(tl, ensure_ascii=False, indent=1)))):
            tam = self._p(ten + ".tmp")
            with open(tam, "w", encoding="utf-8") as f:
                viet(f)
            tam.replace(self._p(ten))
        tam = self._p("emb.f32.tmp")
        m.astype(np.float32).tofile(tam)
        tam.replace(self._p("emb.f32"))   # ghi ma trận SAU CÙNG: mtime của nó báo cho nap() đọc lại cả bộ

    def them(self, docs: list[Document], thong_tin: list[dict]) -> list[dict]:
        """Cắt theo B, nhúng, nối vào kho. Văn bản đã có (cùng id) thì thay bản cũ."""
        from rag import nhung

        with self._khoa:
            m, cs = self.nap()
            tl = self.tai_lieu()
            moi_id = {d.doc_id for d in docs}
            giu = [i for i, c in enumerate(cs) if c["doc_id"] not in moi_id]
            m, cs = m[giu], [cs[i] for i in giu]
            tl = [x for x in tl if x["id"] not in moi_id]
            them_cs = []
            for d, tt in zip(docs, thong_tin):
                cd = [c.dict() for c in structural.chunk(d, 0)]
                for c in cd:   # không mở rộng lên Điều cha (B+): văn bản kho không nằm trong data/clean
                    c.pop("dieu_start", None), c.pop("dieu_end", None)
                    c["kho"] = self.ten
                them_cs += cd
                tl.append({**tt, "id": d.doc_id, "so_hieu": d.so_hieu, "ten": d.trich_yeu, "so_chunk": len(cd),
                           "so_tu": len(d.text.split())})
            t0 = time.monotonic()
            v = nhung.nhung([c["text"] for c in them_cs]) if them_cs else np.zeros((0, DIM), np.float32)
            giay = time.monotonic() - t0
            self._ghi(np.vstack([m, v]), cs + them_cs, tl)
            self._mtime = "chua_nap"
            for x in tl[-len(docs):]:
                x["giay_nhung"] = round(giay * x["so_chunk"] / max(1, len(them_cs)), 1)
            return tl[-len(docs):]

    def xoa(self, doc_id: str) -> bool:
        with self._khoa:
            m, cs = self.nap()
            tl = self.tai_lieu()
            if not any(x["id"] == doc_id for x in tl):
                return False
            giu = [i for i, c in enumerate(cs) if c["doc_id"] != doc_id]
            self._ghi(m[giu], [cs[i] for i in giu], [x for x in tl if x["id"] != doc_id])
            self._mtime = "chua_nap"
            return True


# ── đọc chữ từ tệp tải lên ───────────────────────────────────────────────
def doc_docx(du_lieu: bytes) -> str:
    """Chữ trong word/document.xml, mỗi đoạn <w:p> một dòng — không cần thư viện ngoài."""
    xml = zipfile.ZipFile(io.BytesIO(du_lieu)).read("word/document.xml").decode("utf-8")
    dong = []
    for p in re.findall(r"<w:p[ >].*?</w:p>", xml, flags=re.S):
        p = re.sub(r"<w:tab/>", "\t", p)
        dong.append("".join(re.findall(r"<w:t(?: [^>]*)?>([^<]*)</w:t>", p)))
    return html.unescape("\n".join(dong))


def doc_tep(ten_tep: str, du_lieu: bytes) -> dict:
    """{"text", "so_trang", "trang_ocr", "giay"} — PDF đi qua ocr/doc_pdf.py trong .venv-ocr."""
    duoi = Path(ten_tep).suffix.lower()
    t0 = time.monotonic()
    if duoi in (".txt", ".md"):
        for ma in ("utf-8-sig", "utf-16", "cp1258"):
            try:
                return {"text": du_lieu.decode(ma), "so_trang": 0, "trang_ocr": 0, "giay": 0}
            except UnicodeDecodeError:
                continue
        raise ValueError("Không đọc được bảng mã của tệp văn bản (cần UTF-8).")
    if duoi == ".docx":
        return {"text": doc_docx(du_lieu), "so_trang": 0, "trang_ocr": 0, "giay": round(time.monotonic() - t0, 1)}
    if duoi == ".pdf":
        if not PY_OCR.exists():
            raise RuntimeError("Chưa cài môi trường OCR (.venv-ocr) — xem docs/thuc-nghiem-mo-rong.md.")
        tam = GOC_KHO / "_tam" / (hashlib.sha1(du_lieu).hexdigest() + ".pdf")
        tam.parent.mkdir(parents=True, exist_ok=True)
        tam.write_bytes(du_lieu)
        try:
            r = subprocess.run([str(PY_OCR), "-W", "ignore", "-m", "ocr.doc_pdf", str(tam)], cwd=ch.GOC,
                               capture_output=True, env={**os.environ, "PYTHONUTF8": "1", "OMP_THREAD_LIMIT": "2"})
        finally:
            tam.unlink(missing_ok=True)
        if r.returncode:
            raise RuntimeError("OCR hỏng: " + r.stderr.decode("utf-8", "replace").strip().splitlines()[-1][:300])
        return json.loads(r.stdout.decode("utf-8"))
    raise ValueError(f"Chỉ nhận {', '.join(DUOI_HOP_LE)}.")


RE_SO_HIEU = re.compile(r"Số\s*(?:hiệu)?\s*:\s*([0-9][\w./\-–]*[\w])")


def tao_tai_lieu(ten_tep: str, du_lieu: bytes) -> tuple[Document, dict]:
    """Đọc chữ, đoán số hiệu từ dòng "Số: …" ở đầu văn bản (không có thì dùng tên tệp)."""
    r = doc_tep(ten_tep, du_lieu)
    text = re.sub(r"[ \t]+\n", "\n", r["text"]).strip()
    if len(text.split()) < 5:
        raise ValueError("Không lấy được chữ nào từ tệp (PDF ảnh quá mờ, hoặc tệp rỗng).")
    m = RE_SO_HIEU.search(text[:3000])
    so_hieu = m.group(1) if m else Path(ten_tep).stem
    did = "tl-" + hashlib.sha1(du_lieu).hexdigest()[:12]
    doc = Document(doc_id=did, so_hieu=so_hieu, loai_van_ban="", trich_yeu=Path(ten_tep).stem, text=text)
    tt = {"tep": ten_tep, "byte": len(du_lieu), "so_trang": r["so_trang"], "trang_ocr": r["trang_ocr"],
          "giay_doc": r["giay"], "luc": dt.datetime.now().isoformat(timespec="seconds")}
    return doc, tt


def dung_day_du(force: bool = False) -> None:
    """Kho day_du: mọi văn bản trong data/clean (212), metadata từ data/raw/<id>.json."""
    k = Kho("day_du")
    if k._p("emb.f32").exists() and not force:
        print(f"BỎ QUA: kho day_du đã có {len(k.tai_lieu())} văn bản (--force để dựng lại)")
        return
    if force and k.thu_muc.exists():
        for t in ("emb.f32", "chunks.jsonl", "tai_lieu.json"):
            k._p(t).unlink(missing_ok=True)
    import csv
    tam_muoi = {r["id"] for r in csv.DictReader(open(ch.MANIFEST))}
    docs, tt = [], []
    for p in sorted(ch.CLEAN.glob("*.txt")):
        meta = json.loads((ch.RAW / f"{p.stem}.json").read_text())
        docs.append(Document(doc_id=p.stem, so_hieu=meta["so_hieu"], loai_van_ban=meta.get("loai_van_ban", ""),
                             trich_yeu=meta.get("trich_yeu", ""), text=p.read_text()))
        tt.append({"tep": f"data/clean/{p.name}", "trong_80": p.stem in tam_muoi, "hieu_luc": meta.get("hieu_luc", "")})
    t0 = time.monotonic()
    k.them(docs, tt)
    m, cs = k.nap()
    print(f"kho day_du: {len(docs)} văn bản, {len(cs)} chunk, {time.monotonic() - t0:.0f}s")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="lenh", required=True)
    sub.add_parser("dung-day-du").add_argument("--force", action="store_true")
    sub.add_parser("them").add_argument("tep", nargs="+")
    sub.add_parser("ds")
    a = ap.parse_args()
    if a.lenh == "dung-day-du":
        dung_day_du(a.force)
    elif a.lenh == "them":
        k = Kho("tai_len")
        for t in a.tep:
            doc, tt = tao_tai_lieu(Path(t).name, Path(t).read_bytes())
            print(k.them([doc], [tt])[0])
    else:
        for ten in ("day_du", "tai_len"):
            tl = Kho(ten).tai_lieu()
            print(f"{ten}: {len(tl)} văn bản, {sum(x['so_chunk'] for x in tl)} chunk")
            for x in tl[-5:]:
                print(f"  {x['id']}  {x['so_hieu']}  {x.get('so_trang', 0)} trang  {x['so_chunk']} chunk")


if __name__ == "__main__":
    main()
