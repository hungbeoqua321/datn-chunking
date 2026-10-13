"""Chuẩn hoá HTML gốc → text, trước khi phân đoạn (bước bắt buộc của đề).

Hai cách chuyển HTML → text được so sánh để đo "tiêu đề Điều bị vỡ":
  - THÔ  (trước chuẩn hoá): BeautifulSoup.get_text("\\n") — cách crawl phổ biến; mỗi thẻ (kể cả thẻ inline
          <b>, <span>, <a>) thành một dòng riêng, nên "Điều" và "12." nằm ở hai thẻ khác nhau sẽ bị tách dòng.
  - SẠCH (sau chuẩn hoá): chỉ xuống dòng ở thẻ khối (p, div, li, tr, h1–h6, br…), thẻ inline nối liền;
          rồi chuẩn hoá ký tự và gộp tiêu đề Điều bị ngắt dòng.

Các bước chuẩn hoá (theo đề):
  1. gộp dòng bị ngắt giữa chừng trong tiêu đề Điều ("Điều" | "12." | "Tên điều" → "Điều 12. Tên điều");
  2. \\r\\n → \\n, bỏ dòng trắng thừa, khoảng trắng kép, khoảng trắng không ngắt; nháy cong → nháy thẳng;
     Unicode NFC, Ð (U+00D0, Eth) → Đ (U+0110) — lỗi hay gặp trong HTML cũ làm regex "Điều" trượt;
  3. bỏ các dòng "Căn cứ …"/"Theo đề nghị …" ở đầu (trước Phần/Chương/Điều đầu tiên) và phần
     "Nơi nhận"/chữ ký ở cuối → data/clean/; bản chưa bỏ gì → data/clean_full/ để đối chiếu;
  4. đo tỷ lệ tiêu đề Điều bị vỡ trước/sau chuẩn hoá (so với số Điều kỳ vọng lấy từ cây cấu trúc do
     vbpl.vn biên tập — nguồn độc lập với bộ phân đoạn B; không có cây thì dùng dãy số Điều liên tục).

    python -m crawl.chuan_hoa            # chuẩn hoá mọi văn bản trong data/raw (bỏ qua file đã có)
    python -m crawl.chuan_hoa --force
"""
import argparse
import html as H
import json
import re
import unicodedata

from bs4 import BeautifulSoup, NavigableString

import cau_hinh as ch

THONG_KE = ch.DATA / "thong_ke_chuan_hoa.jsonl"

# Regex tiêu đề Điều của PHƯƠNG PHÁP B (đúng gợi ý của đề) — dùng để đếm "bắt được"
RE_TIEU_DE_B = re.compile(r"^Điều\s+(\d+)\s*[.．:]?\s*(.*)$", re.M)
# Regex lỏng (để dò Điều kỳ vọng khi không có cây cấu trúc)
RE_DIEU_LONG = re.compile(r"(?:^|\n)\s*Điều\s*\n?\s*(\d+)\s*[a-zđ]?\s*[.．:]", re.M)
RE_CAU_TRUC = re.compile(r"^(Phần|PHẦN|Chương|CHƯƠNG|Mục|MỤC)\s+([IVXLC\d]+|thứ\s+\S+)\b|^Điều\s+\d+", re.M)

KHOI = {"p", "div", "li", "tr", "h1", "h2", "h3", "h4", "h5", "h6", "table", "ul", "ol", "blockquote", "section",
        "article", "header", "footer", "pre", "td", "th", "dt", "dd"}
NHAY = str.maketrans({"“": '"', "”": '"', "„": '"', "«": '"', "»": '"',
                      "‘": "'", "’": "'", "‚": "'"})


def _soup(html: str) -> BeautifulSoup:
    s = BeautifulSoup(html, "lxml")
    for t in s(["style", "script", "noscript", "title", "head"]):
        t.decompose()
    return s


def _chu_thich_li(s: BeautifulSoup) -> None:
    """Chú thích VBHN dạng <li class="footnote-item" id="fn-N"> (số thứ tự do trình duyệt tự đánh, không có trong
    text) → một đoạn "[N] …" duy nhất; bỏ liên kết quay lại "↩"."""
    for a in s.select("a.footnote-backref"):
        a.decompose()
    for li in s.select("li.footnote-item"):
        m = re.match(r"fn-?(\d+)", li.get("id") or "")
        noi = " ".join(li.get_text(" ").replace("\u21a9", " ").split())
        p = s.new_tag("p")
        p.string = f"[{m.group(1)}] {noi}" if m else noi
        li.replace_with(p)


def text_tho(html: str) -> str:
    """Cách crawl ngây thơ (mốc 'trước chuẩn hoá'): mỗi thẻ một dòng, chỉ cắt khoảng trắng hai đầu dòng."""
    t = H.unescape(_soup(html).get_text("\n"))
    return "\n".join(x.strip() for x in t.replace("\r\n", "\n").split("\n") if x.strip())


def _chuan_ky_tu(s: str) -> str:
    s = unicodedata.normalize("NFC", s)
    s = s.replace("Ð", "Đ").replace("ð", "đ")  # Eth → Đ/đ
    s = s.translate(NHAY)
    s = re.sub(r"[   \t]", " ", s)
    s = re.sub(r"[​‌‍﻿]", "", s)
    return s


def text_khoi(html: str) -> str:
    """HTML → text: xuống dòng ở thẻ khối/br, thẻ inline nối liền."""
    s = _soup(html)
    _chu_thich_li(s)
    for br in s.find_all("br"):
        br.replace_with(NavigableString("\n"))
    for t in s.find_all(KHOI):
        t.insert_before(NavigableString("\n"))
        t.insert_after(NavigableString("\n"))
    t = H.unescape(s.get_text(""))
    t = t.replace("\r\n", "\n").replace("\r", "\n")
    return t


def gop_tieu_de(dong: list[str]) -> list[str]:
    """Gộp tiêu đề Điều bị ngắt dòng. Trả về danh sách dòng mới."""
    ra: list[str] = []
    i = 0
    while i < len(dong):
        x = dong[i]
        # "Điều" | "12." …  hoặc  "Điều 12" | "." …
        if re.fullmatch(r"Điều", x) and i + 1 < len(dong) and re.match(r"\d+", dong[i + 1]):
            dong[i + 1] = "Điều " + dong[i + 1]
            i += 1
            continue
        m = re.fullmatch(r"(Điều\s+\d+[a-zđ]?)\s*([.．:]?)", x)
        if m and i + 1 < len(dong):
            nx = dong[i + 1]
            if re.fullmatch(r"[.．:]", nx) and i + 2 < len(dong):  # "Điều 12" | "." | "Tên"
                nx = dong[i + 2]
                i += 1
            # dòng kế là tên điều (ngắn, không phải khoản "1." / điểm "a)" / Điều khác)
            if (nx and not re.match(r"(\d+[.)]|[a-zđ]\)|Điều\s+\d|Chương|CHƯƠNG|Mục|MỤC)", nx)
                    and len(nx.split()) <= 40):
                ra.append(f"{m.group(1)}. {nx}")
                i += 2
                continue
            ra.append(f"{m.group(1)}.")
            i += 1
            continue
        ra.append(x)
        i += 1
    return ra


RE_CHUONG = re.compile(r"^(Chương|CHƯƠNG|Mục|MỤC|Phần|PHẦN)\s+([IVXLC\d]+[a-z]?|thứ\s+\S+|THỨ\s+\S+)\.?$")
RE_DAU_DONG_DANH_SO = re.compile(r"^([a-zđ][).]|[ivx]+[).]|\d+[.)])\s")


def _in_hoa(x: str) -> bool:
    chu = [c for c in x if c.isalpha()]
    return bool(chu) and all(c.isupper() for c in chu)


def gop_dong(dong: list[str]) -> list[str]:
    """Gộp dòng bị thẻ <br> cắt giữa chừng (đề: "gộp các dòng bị ngắt giữa chừng").

    - tên Chương/Mục/Phần in hoa bị ngắt thành nhiều dòng → một dòng tên (dòng "Chương IV" vẫn đứng riêng);
    - dòng bắt đầu bằng chữ thường (không phải điểm "a)") nối vào dòng trước nếu dòng trước chưa kết thúc câu.
    """
    ra: list[str] = []
    i = 0
    while i < len(dong):
        x = dong[i]
        if RE_CHUONG.match(x) and i + 1 < len(dong) and _in_hoa(dong[i + 1]):
            ten, j = dong[i + 1], i + 2
            while (j < len(dong) and _in_hoa(dong[j]) and not RE_CHUONG.match(dong[j])
                   and not dong[j].startswith("Điều") and len(ten.split()) < 40):
                ten, j = ten + " " + dong[j], j + 1
            ra += [x, ten]
            i = j
            continue
        if (ra and x[:1].islower() and not RE_DAU_DONG_DANH_SO.match(x)
                and not re.search(r"[.;:!?]$", ra[-1]) and not RE_TIEU_DE_B.match(ra[-1])
                and not RE_CHUONG.match(ra[-1])):
            ra[-1] = ra[-1] + " " + x
            i += 1
            continue
        ra.append(x)
        i += 1
    return ra


def vung_chu_thich(dong: list[str]) -> int | None:
    """Chỉ số dòng bắt đầu danh sách chú thích cuối văn bản = đầu của dãy dòng "[n] …" (có dấu cách) đánh số
    TĂNG LIÊN TIẾP cuối cùng (có thể bắt đầu từ [2] nếu [1] nằm trong phần mở đầu). Ký hiệu chú thích trong thân
    văn bản (ví dụ "[17]Báo cáo …" đứng đầu đoạn, không có dấu cách) không tính."""
    ung = [(i, int(m.group(1))) for i, x in enumerate(dong) if (m := re.match(r"^\[(\d+)\]\s", x))]
    if not ung:
        return None
    k = len(ung) - 1
    while k > 0 and ung[k - 1][1] == ung[k][1] - 1:
        k -= 1
    return ung[k][0] if len(ung) - k >= 2 or ung[k][1] == 1 else None


def gop_chu_thich(dong: list[str]) -> list[str]:
    """Vùng chú thích VBHN ("[1] …" đến hết): các đoạn nối tiếp không đánh số gộp vào chú thích trước nó,
    để đoạn chú thích mở đầu bằng "Điều 2 của Luật …" không bị bộ phân đoạn tưởng là tiêu đề Điều."""
    dau = vung_chu_thich(dong)
    if dau is None:
        return dong
    ra = dong[:dau]
    for x in dong[dau:]:
        if RE_CHU_THICH.match(x) or not ra or RE_PHU_LUC.match(x):
            ra.append(x)
        elif RE_CHU_THICH.match(ra[-1]):
            ra[-1] += " " + x
        else:
            ra.append(x)
    return ra


def chuan_hoa(html: str) -> str:
    t = _chuan_ky_tu(text_khoi(html))
    t = re.sub(r"(?m)^(\s*)Điều(\d)", r"\1Điều \2", t)  # "Điều5." → "Điều 5."
    dong = [re.sub(r" {2,}", " ", x).strip() for x in t.split("\n")]
    dong = [x for x in dong if x and not re.fullmatch(r"[_\-–—=.…*~•·\s]+", x)]  # bỏ dòng kẻ trang trí
    dong = gop_tieu_de(dong)
    dong = gop_dong(dong)
    dong = gop_chu_thich(dong)
    return "\n".join(dong) + "\n"


# ── bỏ phần "Căn cứ" đầu văn bản và "Nơi nhận"/chữ ký cuối văn bản ──────────
RE_CAN_CU = re.compile(r"^(Căn cứ|Theo đề nghị|Xét đề nghị|Thực hiện|Theo đề xuất)\b", re.I)
RE_NOI_NHAN = re.compile(r"^Nơi nhận\s*:?", re.I)
RE_CHU_KY = re.compile(r"^(TM\.|T\.M\.|KT\.|K\.T\.|Q\.|TL\.|TUQ\.|TM |KT |\(?\[?Đã ký\]?\)?|\(ký\b|Chữ ký|"
                       r"XÁC THỰC VĂN BẢN HỢP NHẤT|CHỦ TỊCH|THỦ TƯỚNG|PHÓ THỦ TƯỚNG|BỘ TRƯỞNG|THỨ TRƯỞNG|"
                       r"CHỦ NHIỆM|PHÓ CHỦ NHIỆM|TỔNG KIỂM TOÁN|CHÁNH ÁN|VIỆN TRƯỞNG|THỐNG ĐỐC|PHÓ THỐNG ĐỐC|"
                       r"TỔNG GIÁM ĐỐC|GIÁM ĐỐC|CHÁNH VĂN PHÒNG|VỤ TRƯỞNG|CỤC TRƯỞNG|TỔNG CỤC TRƯỞNG|"
                       r"BỘ TRƯỞNG, CHỦ NHIỆM|PHÓ CHÁNH|CHÁNH THANH TRA)", re.I)
RE_KY_MANH = re.compile(r"^(TM\.|T\.M\.|KT\.|K\.T\.|TL\.|TUQ\.|Q\.\s?[A-ZĐ]|TM |KT )|"
                        r"^(CHỦ TỊCH QUỐC HỘI|XÁC THỰC VĂN BẢN HỢP NHẤT)\s*$")
RE_PHU_LUC = re.compile(r"^(PHỤ LỤC|Phụ lục|Mẫu số|MẪU SỐ)\b")
RE_CHU_THICH = re.compile(r"^\[\d+\]")  # chú thích cuối trang của VBHN: "[1] …"


def _la_ten_nguoi(x: str) -> bool:
    w = x.split()
    return 2 <= len(w) <= 5 and all(t[:1].isupper() for t in w) and not x.endswith((".", ":", ";"))


RE_MO_PHAN_MOI = re.compile(r"^(QUY CHẾ|QUY ĐỊNH|ĐIỀU LỆ|CHƯƠNG TRÌNH|KẾ HOẠCH|DANH MỤC|HƯỚNG DẪN|TIÊU CHUẨN|"
                            r"PHƯƠNG ÁN|CHIẾN LƯỢC|ĐỀ ÁN)\b|^(Chương|CHƯƠNG|Phần|PHẦN)\s+[IVXLC\d]")


def _loai_dong_cuoi(x: str, trong_noi_nhan: bool) -> str:
    if RE_NOI_NHAN.match(x):
        return "noi_nhan"
    if (RE_KY_MANH.match(x) or RE_CHU_KY.match(x) or _la_ten_nguoi(x) or re.match(r"^(Số|Hà Nội|TP\.)\b.*\d", x)
            or (_in_hoa(x) and len(x.split()) <= 8)):
        return "chu_ky"
    return "noi_nhan" if trong_noi_nhan else "khac"


def _dem(bo: dict, khoi: list[str]) -> None:
    trong = False
    for x in khoi:
        k = _loai_dong_cuoi(x, trong)
        trong = trong or k == "noi_nhan"
        bo["noi_nhan" if k in ("noi_nhan", "khac") and trong else "chu_ky" if k == "chu_ky" else "khac"] += 1


def bo_dau_cuoi(text: str, ky_vong: list[int] | None = None) -> tuple[str, dict]:
    """Bỏ "Căn cứ …" ở đầu, Nơi nhận / chữ ký / Phụ lục ở cuối (và khối chữ ký nằm GIỮA văn bản, ví dụ quyết định
    ban hành kèm quy chế). Trả (text đã bỏ, số dòng/từ đã bỏ theo từng loại)."""
    dong = text.rstrip("\n").split("\n")
    bo = {"can_cu": 0, "noi_nhan": 0, "chu_ky": 0, "khac": 0, "khoi_giua": 0, "phu_luc_tu": 0}
    # đầu: chỉ xét phần trước tiêu đề cấu trúc đầu tiên (Phần/Chương/Mục/Điều); bỏ từ dòng "Căn cứ" đầu tiên
    # đến dòng "Căn cứ/Theo đề nghị" cuối cùng (kể cả dòng kẹp giữa không mở đầu bằng "Căn cứ" do lỗi soạn thảo).
    # Văn bản không có cấu trúc thì KHÔNG bỏ gì (ở công văn, "Căn cứ …" thường là nội dung).
    dau = next((i for i, x in enumerate(dong) if RE_CAU_TRUC.match(x)), None)
    if dau is not None:
        cc = [i for i in range(dau) if RE_CAN_CU.match(dong[i])]
        if cc:
            bo["can_cu"] = cc[-1] - cc[0] + 1
            dong = dong[:cc[0]] + dong[cc[-1] + 1:]
    # tách vùng chú thích VBHN ("[1] …") ra trước để không bị cắt cùng phụ lục / chữ ký
    ct = vung_chu_thich(dong)
    chu_thich: list[str] = []
    if ct is not None:
        het = next((i for i in range(ct, len(dong)) if RE_PHU_LUC.match(dong[i]) and len(dong[i].split()) <= 12),
                   len(dong))
        chu_thich = [x for x in dong[ct:het] if RE_CHU_THICH.match(x)]
        dong = dong[:ct] + dong[het:]
    pl = phan_loai_tieu_de(dong, ky_vong)
    that = [i for i, _, t in pl if t]
    cuoi_dieu = max(that, default=0)
    # giữa văn bản: khối "Nơi nhận / XÁC THỰC VBHN / chữ ký" kẹp giữa hai phần (ví dụ quyết định 3 Điều + quy chế
    # kèm theo). Chỉ bỏ khi khối ngắn (≤ 30 dòng), không chứa tiêu đề Điều và kết thúc ngay trước phần mới.
    xoa: set[int] = set()
    for i in range(cuoi_dieu):
        x = dong[i]
        if i in xoa or not (RE_NOI_NHAN.match(x) or re.match(r"^XÁC THỰC VĂN BẢN HỢP NHẤT", x) or RE_KY_MANH.match(x)):
            continue
        a = i
        while a > 0 and a - 1 not in xoa and i - a < 4 and (_in_hoa(dong[a - 1]) or re.match(r"^Số\s*:", dong[a - 1])) \
                and not RE_TIEU_DE_B.match(dong[a - 1]) and not RE_CHUONG.match(dong[a - 1]):
            a -= 1
        b = next((j for j in range(i + 1, min(len(dong), i + 31)) if RE_MO_PHAN_MOI.match(dong[j])
                  or RE_TIEU_DE_B.match(dong[j])), None)
        if b is None or RE_TIEU_DE_B.match(dong[b]) and not any(RE_MO_PHAN_MOI.match(y) for y in dong[i:b]):
            continue
        khoi = dong[a:b]
        _dem(bo, khoi)
        bo["khoi_giua"] += 1
        xoa |= set(range(a, b))
    if xoa:
        cuoi_dieu -= sum(1 for k in xoa if k < cuoi_dieu)
        dong = [x for k, x in enumerate(dong) if k not in xoa]
    # cuối: cắt tại mốc kết thúc phần chính ĐẦU TIÊN sau tiêu đề Điều cuối cùng — "Nơi nhận", khối chữ ký,
    # hoặc tiêu đề Phụ lục/Mẫu số. (Phụ lục thường nằm SAU chữ ký và mỗi mẫu đơn trong phụ lục lại có "Nơi nhận"
    # riêng, nên lấy "Nơi nhận" cuối cùng là sai.) Phụ lục không thuộc phạm vi thực nghiệm: bỏ khỏi clean/,
    # vẫn còn ở clean_full/.
    cat = next((i for i in range(cuoi_dieu + 1, len(dong))
                if RE_NOI_NHAN.match(dong[i]) or RE_KY_MANH.match(dong[i])
                or (RE_PHU_LUC.match(dong[i]) and len(dong[i].split()) <= 12)), None)
    if cat is not None:
        sau = dong[cat:]
        p = next((i for i, x in enumerate(sau) if RE_PHU_LUC.match(x) and len(x.split()) <= 12), len(sau))
        bo["phu_luc_tu"] = sum(len(x.split()) for x in sau[p:])
        _dem(bo, sau[:p])
        dong = dong[:cat]
    # chữ ký liền sau nội dung (khi không có mốc mạnh): đi lùi bỏ dòng chức danh / "(Đã ký)" / tên người
    j = len(dong)
    while j > cuoi_dieu + 1 and (RE_CHU_KY.match(dong[j - 1]) or _la_ten_nguoi(dong[j - 1])
                                 or (_in_hoa(dong[j - 1]) and len(dong[j - 1].split()) <= 8)):
        j -= 1
    if 0 < len(dong) - j <= 12:
        bo["chu_ky"] += len(dong) - j
        dong = dong[:j]
    return "\n".join(dong + chu_thich) + "\n", bo


# ── đo tiêu đề Điều ─────────────────────────────────────────────────────────
def dieu_ky_vong(doc_id: str, text_full: str) -> tuple[list[int], str]:
    """Số Điều kỳ vọng: từ cây cấu trúc vbpl.vn; không có thì từ dãy số Điều liên tục (regex lỏng)."""
    pc = ch.RAW / f"{doc_id}.cay.json"
    if pc.exists():
        cay = json.loads(pc.read_text())
        so: list[int] = []

        def di(nut):
            for n in nut or []:
                if n.get("level") == "Article":
                    m = re.match(r"\s*Điều\s+(\d+)[a-zđ]?\s*([.．:]|$)", _chuan_ky_tu(n.get("title") or ""))
                    if m:
                        so.append(int(m.group(1)))
                di(n.get("children"))

        if isinstance(cay, list):
            di(cay)
        if so:
            return sorted(set(so)), "cay_vbpl"
    so = [int(x) for x in RE_DIEU_LONG.findall(text_full)]
    # dãy liên tục dài nhất bắt đầu từ 1 (bỏ các "Điều N" dẫn chiếu/trích dẫn lẻ tẻ)
    co, n = set(so), 0
    while n + 1 in co:
        n += 1
    return list(range(1, n + 1)), "regex_long"


def trong_ngoac(dong: list[str]) -> list[bool]:
    """Đánh dấu dòng nằm trong khối trích dẫn "…" (văn bản sửa đổi trích nguyên văn điều của luật bị sửa)."""
    # Theo số dấu nháy: mỗi dòng có số lẻ dấu " thì đảo trạng thái mở/đóng. Dòng mở khối (bắt đầu bằng ")
    # cũng tính là trong ngoặc. Đơn giản nhưng đủ cho cách trình bày của văn bản sửa đổi.
    ra, mo = [], False
    for x in dong:
        ra.append(mo or x.startswith('"'))
        if x.count('"') % 2 == 1:
            mo = not mo
    return ra


def phan_loai_tieu_de(dong: list[str], ky_vong: list[int] | None = None) -> list[tuple[int, int, bool]]:
    """Mọi dòng khớp regex tiêu đề của B → (chỉ số dòng, số Điều, là Điều THẬT của văn bản?).

    "Điều N" nằm trong khối trích dẫn (văn bản sửa đổi trích nguyên văn điều của luật bị sửa) là Điều GIẢ.
    Chỉ đếm dấu nháy thì dễ lệch (một dấu nháy lẻ làm mọi Điều sau đó bị coi là trong ngoặc), nên dùng thêm
    thứ tự: dòng không mở đầu bằng dấu nháy và mang đúng số Điều kế tiếp của văn bản (theo cây vbpl; không có
    cây thì là số liền sau Điều thật trước đó) là Điều thật — và nó đóng mọi khối trích dẫn đang mở.
    """
    kv = sorted(set(ky_vong or []))
    q = trong_ngoac(dong)
    ra, mo, vi_tri, truoc = [], False, 0, 0
    for i, x in enumerate(dong):
        m = RE_TIEU_DE_B.match(x)
        if m:
            n = int(m.group(1))
            ke = kv[vi_tri] if vi_tri < len(kv) else None
            dung_thu_tu = (n == ke) if kv else (n == truoc + 1)
            that = not x.startswith('"') and (dung_thu_tu or not (mo or q[i]))
            ra.append((i, n, that))
            if that:
                mo, truoc = False, n
                while vi_tri < len(kv) and kv[vi_tri] <= n:
                    vi_tri += 1
        if x.count('"') % 2 == 1:
            mo = not mo
    return ra


def do_tieu_de(text: str, ky_vong: list[int]) -> dict:
    """So khớp tiêu đề Điều mà regex của B bắt được với số Điều kỳ vọng.

    "Bắt được" đúng như B nhìn thấy: số Điều có ít nhất một dòng khớp RE_TIEU_DE_B (không xét trích dẫn).
    Riêng "Điều giả" = dòng khớp regex nhưng không phải Điều thật của văn bản (nằm trong khối trích dẫn).
    "Điều được trích" = dòng mở đầu bằng dấu nháy "Điều N … (regex của B không khớp, nên không thành Điều giả;
    nhưng nội dung điều được trích nằm lẫn trong Điều của văn bản sửa đổi — xem nhược điểm 5).
    """
    dong = text.split("\n")
    pl = phan_loai_tieu_de(dong, ky_vong)
    bat = {n for _, n, _ in pl}
    kv = set(ky_vong)
    return {"ky_vong": len(kv), "bat_duoc": len(kv & bat), "thieu": len(kv - bat),
            "ti_le_vo": (len(kv - bat) / len(kv)) if kv else None,
            "dieu_trong_ngoac": sum(1 for _, _, that in pl if not that),
            "dieu_duoc_trich": sum(1 for x in dong if re.match(r'^"\s*Điều\s+\d+', x)),
            "bat_ngoai_ky_vong": len(bat - kv)}


def thong_ke_dieu(text: str, ky_vong: list[int] | None = None) -> dict:
    """Số từ mỗi Điều (chỉ theo tiêu đề Điều thật, không tính Điều trong khối trích dẫn) + có Chương/Phần/Mục."""
    dong = text.split("\n")
    moc = [i for i, _, that in phan_loai_tieu_de(dong, ky_vong) if that]
    dai = [sum(len(x.split()) for x in dong[a:b]) for a, b in zip(moc, moc[1:] + [len(dong)])]
    return {"so_tu": len(text.split()), "so_dieu": len(dai), "dieu_dai_nhat": max(dai, default=0),
            "so_dieu_tren_1500": sum(d > 1500 for d in dai),
            "co_chuong": bool(re.search(r"(?m)^(Chương|CHƯƠNG)\s+[IVXLC\d]+", text)),
            "co_phan": bool(re.search(r"(?m)^(Phần|PHẦN)\s+(thứ|THỨ|[IVXLC\d]+)", text)),
            "co_muc": bool(re.search(r"(?m)^(Mục|MỤC)\s+\d+", text))}


def xu_ly(doc_id: str) -> dict:
    html = (ch.RAW / f"{doc_id}.html").read_text()
    full = chuan_hoa(html)
    kv, nguon = dieu_ky_vong(doc_id, full)
    sach, bo = bo_dau_cuoi(full, kv)
    (ch.CLEAN_FULL / f"{doc_id}.txt").write_text(full)
    (ch.CLEAN / f"{doc_id}.txt").write_text(sach)
    tho = _chuan_ky_tu(text_tho(html))  # mốc "trước": chỉ chuẩn hoá ký tự cho công bằng, không gộp dòng
    return {"id": doc_id, "nguon_ky_vong": nguon, "da_bo": bo,
            "truoc": do_tieu_de(tho, kv), "sau": do_tieu_de(full, kv), **thong_ke_dieu(sach, kv)}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    ch.CLEAN.mkdir(parents=True, exist_ok=True)
    ch.CLEAN_FULL.mkdir(parents=True, exist_ok=True)
    cu = {}
    if THONG_KE.exists() and not a.force:
        cu = {d["id"]: d for d in map(json.loads, THONG_KE.read_text().splitlines())}
    ra = []
    for ph in sorted(ch.RAW.glob("*.html")):
        doc_id = ph.stem
        if doc_id in cu and (ch.CLEAN / f"{doc_id}.txt").exists():
            ra.append(cu[doc_id])
            continue
        ra.append(xu_ly(doc_id))
    THONG_KE.write_text("\n".join(json.dumps(d, ensure_ascii=False) for d in ra) + "\n")
    tr = [d["truoc"] for d in ra if d["truoc"]["ky_vong"]]
    sa = [d["sau"] for d in ra if d["sau"]["ky_vong"]]
    kv = sum(x["ky_vong"] for x in tr)
    print(f"{len(ra)} văn bản; tiêu đề Điều kỳ vọng {kv}; vỡ trước {sum(x['thieu'] for x in tr)} "
          f"({sum(x['thieu'] for x in tr) / max(kv, 1):.2%}), sau {sum(x['thieu'] for x in sa)} "
          f"({sum(x['thieu'] for x in sa) / max(kv, 1):.2%})")


if __name__ == "__main__":
    main()
