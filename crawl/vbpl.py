"""Client cho vbpl.vn — Cơ sở dữ liệu quốc gia về văn bản pháp luật (Bộ Tư pháp).

Trang vbpl.vn mới là ứng dụng Next.js. Dữ liệu không đi qua REST công khai mà qua
"server action": POST tới chính trang, header `Next-Action: <id 40 hex>`, thân là mảng
JSON tham số; phản hồi là luồng React Server Components (text/x-component).
Backend thật (vbpl-bientap-gateway.moj.gov.vn) chặn IP ngoài Việt Nam, còn server
Next.js của vbpl.vn thì gọi hộ được — nên đây là đường duy nhất lấy toàn văn từ VPS.

Action id gắn với bản build hiện tại của vbpl.vn và ĐỔI mỗi lần họ deploy lại, nên
không viết cứng: tự dò từ các chunk JS của trang rồi thử từng id với một văn bản đã biết.
Kết quả dò lưu ở data/raw/_actions.json kèm buildId; lỗi "action not found" thì dò lại.

robots.txt của vbpl.vn: Allow: /, chỉ cấm /api/ và /Pages/ — các POST ở đây đi vào
trang /van-ban/... nên không thuộc vùng cấm. Giữ ≤ 1 request/giây.

    python -m crawl.vbpl --chi-tiet 139264          # in metadata + số "Điều" của một văn bản
    python -m crawl.vbpl --tim "Luật" --loai Luật    # thử tìm kiếm
    python -m crawl.vbpl --do-lai                    # dò lại action id
"""
import argparse
import json
import re
import time
from pathlib import Path

import requests

import cau_hinh as ch

GOC_URL = "https://vbpl.vn"
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"
TEP_ACTION = ch.RAW / "_actions.json"
DOC_MAU = "139264"  # Bộ luật Lao động 45/2019/QH14 — dùng để thử action id

# id loại văn bản (bảng tra LoaiVanBan của vbpl.vn)
LOAI = {
    "Luật": "11025e19-2dd6-4165-85ad-ab6241186a1a",
    "Bộ luật": "404b68a7-8e71-4ee5-a6c0-07e59f35f824",
    "Nghị định": "0d08b84c-7de7-4800-8760-2a68265e7890",
    "Thông tư": "178c63a9-73ff-4fd4-9d91-18d690520090",
    "Quyết định": "0a5362e8-cdca-436e-96cd-979598df3b16",
    "Văn bản hợp nhất": "26b8a9ff-1b59-4c57-9605-f2ad4ed7c324",
    "Nghị quyết": "044d941c-40de-45b9-ae84-51f5a730bfe0",
    "Công văn": "ecc6bbe0-5d0c-4916-836b-bb2f8146249c",
    "Văn bản hành chính liên quan": "25fad6ae-78f6-4acd-a70e-da19032729af",
    "Văn bản khác": "39a344bd-d086-4fd9-880c-9ecefdb19a40",
    "Chỉ thị": "0045710b-eb54-4ce5-b511-76aa23f3021b",
    "Thông báo": "ed938c9b-e50d-42f8-80b9-e945f207bd04",
}
# mã quan hệ trong "lược đồ" văn bản (enum N8 trong JS của vbpl.vn)
QUAN_HE = {1: "Bãi bỏ", 3: "Căn cứ", 4: "Dẫn chiếu", 6: "Đính chính", 7: "Hợp nhất", 8: "Hướng dẫn áp dụng",
           9: "Quy định chi tiết", 10: "Sửa đổi, bổ sung", 12: "Thay thế", 13: "Bổ sung", 16: "Sửa đổi"}


class LoiAction(RuntimeError):
    pass


def doc_rsc(b: bytes) -> dict[str, str]:
    """Tách luồng React Server Components thành {id dòng: nội dung}.

    Dòng dạng `<id>:<json>\\n`; chuỗi dài đi riêng dạng `<id>:T<độ dài hex>,<text>` (text có thể
    chứa xuống dòng nên phải cắt theo số byte, không theo dòng).
    """
    hang: dict[str, str] = {}
    i = 0
    while i < len(b):
        j = b.find(b":", i)
        if j < 0:
            break
        rid = b[i:j].decode("utf-8", "replace")
        k = j + 1
        if b[k:k + 1] == b"T":
            c = b.index(b",", k)
            n = int(b[k + 1:c], 16)
            hang[rid] = b[c + 1:c + 1 + n].decode("utf-8")
            i = c + 1 + n
        else:
            e = b.find(b"\n", k)
            e = len(b) if e < 0 else e
            hang[rid] = b[k:e].decode("utf-8", "replace")
            i = e + 1
    return hang


class Vbpl:
    def __init__(self, nghi: float = 1.1):
        self.s = requests.Session()
        self.s.headers["User-Agent"] = UA
        self.nghi = nghi
        self._lan_cuoi = 0.0
        self.actions: dict = {}
        if TEP_ACTION.exists():
            self.actions = json.loads(TEP_ACTION.read_text())

    # ── HTTP lịch sự ─────────────────────────────────────────────────────
    def _cho(self) -> None:
        d = time.monotonic() - self._lan_cuoi
        if d < self.nghi:
            time.sleep(self.nghi - d)
        self._lan_cuoi = time.monotonic()

    def _get(self, url: str) -> str:
        self._cho()
        r = self.s.get(url, timeout=60)
        r.raise_for_status()
        return r.text

    def _action(self, aid: str, args: list, trang: str = "/van-ban/trung-uong") -> dict[str, str]:
        self._cho()
        r = self.s.post(GOC_URL + trang, data=json.dumps(args, ensure_ascii=False).encode(), timeout=120,
                        headers={"Next-Action": aid, "Content-Type": "text/plain;charset=UTF-8",
                                 "Accept": "text/x-component"})
        if r.status_code == 404 or "Server action not found" in r.text[:500]:
            raise LoiAction(f"action {aid} không còn (vbpl.vn đã deploy bản mới?)")
        r.raise_for_status()
        return doc_rsc(r.content)

    # ── dò action id ─────────────────────────────────────────────────────
    def do_action(self) -> dict:
        """Gom mọi id 40-hex trong các chunk JS của trang chi tiết + trang danh sách, rồi thử từng id."""
        ung_vien: set[str] = set()
        chunk_co_action: set[str] = set()
        for trang in (f"/van-ban/chi-tiet/{DOC_MAU}", "/van-ban/trung-uong"):
            html = self._get(GOC_URL + trang)
            for js in sorted(set(re.findall(r'/_next/static/chunks/[^"\']+\.js', html))):
                ids = set(re.findall(r'\("([0-9a-f]{40})"', self._get(GOC_URL + js)))
                if ids:
                    chunk_co_action.add(js.rsplit("/", 1)[-1])
                ung_vien |= ids
        # trang không lộ buildId; dùng tên (có hash) của các chunk chứa action làm "dấu vân tay" bản build
        build = ",".join(sorted(chunk_co_action))
        tim = {"pageNumber": 1, "pageSize": 1, "sortBy": "issueDate", "sortDirection": "desc", "groupVbpl": True,
               "agencyLevel": "TRUNG_UONG", "optionDoc": "all", "matchMode": "all_words", "docType": [LOAI["Luật"]]}
        ket = {"build": build, "chi_tiet": None, "tim": None, "cay": None, "luoc_do": None}
        for aid in sorted(ung_vien):
            if all(ket[k] for k in ("chi_tiet", "tim", "cay", "luoc_do")):
                break
            for vai, args in (("chi_tiet", [DOC_MAU]), ("tim", [tim]), ("cay", [DOC_MAU]), ("luoc_do", [DOC_MAU])):
                if ket[vai]:
                    continue
                try:
                    h = self._action(aid, args)
                    o = json.loads(h.get("1", "null"))
                except Exception:
                    continue
                if vai == "chi_tiet" and isinstance(o, dict) and o.get("docNum") and "documentContent" in o:
                    ket["chi_tiet"] = aid
                elif (vai == "tim" and isinstance(o, dict) and o.get("items")
                      and o["items"][0].get("docNum")
                      and (o["items"][0].get("docType") or {}).get("name") == "Luật"):
                    # phải đúng là tìm kiếm có lọc loại văn bản (có action khác cũng trả items/total)
                    ket["tim"] = aid
                elif (vai == "cay" and isinstance(o, list) and o and isinstance(o[0], dict)
                      and o[0].get("level") in ("Chapter", "Article", "Part", "Section")):
                    ket["cay"] = aid  # cây Phần/Chương/Mục/Điều/Khoản do vbpl.vn biên tập
                elif vai == "luoc_do" and isinstance(o, dict) and "documentNamesByType" in o:
                    ket["luoc_do"] = aid  # quan hệ với văn bản khác (sửa đổi, hợp nhất, ...)
        if not (ket["chi_tiet"] and ket["tim"]):
            raise LoiAction(f"không dò được action id: {ket}")
        ch.RAW.mkdir(parents=True, exist_ok=True)
        TEP_ACTION.write_text(json.dumps(ket, ensure_ascii=False, indent=1))
        self.actions = ket
        return ket

    def _goi(self, vai: str, args: list) -> dict:
        if not self.actions.get(vai):
            self.do_action()
        try:
            h = self._action(self.actions[vai], args)
        except LoiAction:
            self.do_action()  # dò lại đúng một lần
            h = self._action(self.actions[vai], args)
        o = json.loads(h.get("1", "null"))
        if o is None:
            raise RuntimeError("phản hồi rỗng")
        return o if vai != "chi_tiet" else self._noi_chuoi(o, h)

    @staticmethod
    def _noi_chuoi(o, hang: dict[str, str]):
        """Thay tham chiếu "$<id>" (chuỗi dài gửi riêng) bằng nội dung thật."""
        if isinstance(o, str) and re.fullmatch(r"\$[0-9a-f]+", o):
            return hang.get(o[1:], o)
        if isinstance(o, dict):
            return {k: Vbpl._noi_chuoi(v, hang) for k, v in o.items()}
        if isinstance(o, list):
            return [Vbpl._noi_chuoi(v, hang) for v in o]
        return o

    # ── API dùng ở các bước sau ──────────────────────────────────────────
    def chi_tiet(self, doc_id: str) -> dict:
        return self._goi("chi_tiet", [str(doc_id)])

    def cay(self, doc_id: str) -> list:
        """Cây cấu trúc do vbpl.vn biên tập — nguồn ĐỘC LẬP với bộ phân đoạn B (đếm Điều kỳ vọng)."""
        return self._goi("cay", [str(doc_id)])

    def luoc_do(self, doc_id: str) -> dict:
        return self._goi("luoc_do", [str(doc_id)])

    def tim(self, loai: str | None = None, tu_khoa: str | None = None, trang: int = 1, co: int = 50,
            theo_diem: bool = False) -> dict:
        p = {"pageNumber": trang, "pageSize": co, "sortBy": "issueDate", "sortDirection": "desc", "groupVbpl": True,
             "agencyLevel": "TRUNG_UONG", "optionDoc": "all", "matchMode": "all_words"}
        if loai:
            p["docType"] = [LOAI[loai]]
        if tu_khoa:
            p["keyword"] = tu_khoa
        if theo_diem:
            p["score"] = True
        return self._goi("tim", [p])


def url_nguon(doc_id: str) -> str:
    return f"{GOC_URL}/van-ban/chi-tiet/{doc_id}"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--chi-tiet", metavar="ID")
    ap.add_argument("--tim", metavar="TU_KHOA")
    ap.add_argument("--loai", choices=list(LOAI))
    ap.add_argument("--do-lai", action="store_true", help="dò lại action id")
    a = ap.parse_args()
    v = Vbpl()
    if a.do_lai:
        print(v.do_action())
    if a.chi_tiet:
        d = v.chi_tiet(a.chi_tiet)
        html = (d.get("documentContent") or {}).get("content") or ""
        print({k: d.get(k) for k in ("docNum", "title", "issueDate", "effStatus", "isConsolidatedDocument")})
        print("loại:", (d.get("docType") or {}).get("name"), "| cơ quan:", d.get("agencyName"))
        print("HTML:", len(html), "ký tự; số 'Điều N':", len(re.findall(r"Điều\s+\d+", html)))
    if a.tim or a.loai:
        r = v.tim(loai=a.loai, tu_khoa=a.tim, co=5, theo_diem=bool(a.tim))
        print("tổng:", r.get("total"))
        for it in r.get("items", []):
            print(" ", it.get("id"), it.get("docNum"), "|", (it.get("docType") or {}).get("name"), "|", (it.get("title") or "")[:80])


if __name__ == "__main__":
    main()
