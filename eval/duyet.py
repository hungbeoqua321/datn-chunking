"""Xuất bộ câu hỏi nháp ra file dễ đọc để DUYỆT TAY, và chốt bộ câu hỏi sau khi duyệt.

    python -m eval.duyet --xuat   # eval/questions.draft.jsonl → eval/questions.review.md
    python -m eval.duyet --chot   # đọc lại eval/questions.review.md (đã sửa tay) → eval/questions.jsonl

Cách duyệt trong questions.review.md — mỗi câu là một mục "## qXXX":
  - dòng "Trạng thái: GIỮ"  → sửa thành XOÁ để loại câu này (câu DỰ PHÒNG mặc định là DỰ PHÒNG: đổi thành GIỮ để dùng);
  - dòng "Câu hỏi: …"       → sửa trực tiếp nội dung câu hỏi (một dòng);
  - gold (trích đoạn văn bản) chỉ để đọc; nếu gold sai thì XOÁ câu đó.
Khi chốt, mỗi nhóm phải còn đủ số câu (50/18/12/20/15) và đủ số câu gold TRUNG LẬP (16/6/4/6/5 — gold cố ý không trùng
ranh giới khoản, là tập số chính của báo cáo); script báo nếu thiếu. Trước khi ghi, --chot chạy eval/kiem_tra.py trên các
câu GIỮ (đã sửa): quan hệ quy tắc–ngoại lệ (xuyen_khoan), trả lời được chỉ bằng đoạn nguồn (dan_chieu), gold ở bản cũ —
chỉ GẮN CỜ vào questions.jsonl và in danh sách, không xoá câu nào.
"""
import argparse
import json
import re

import cau_hinh as ch
from chunking.base import nap_van_ban

NHAP = ch.GOC / "eval/questions.draft.jsonl"
DUYET = ch.GOC / "eval/questions.review.md"
CHOT = ch.GOC / "eval/questions.jsonl"
# chỉ tiêu hạ ngày 14/10: xuyen_khoan 30 → 18, dan_chieu 25 → 12; tỉ lệ gold trung lập giữ ~32%
CAN = {"don_gian": 50, "xuyen_khoan": 18, "dan_chieu": 12, "dieu_dai": 20, "khong_co_dieu": 15}
TRUNG_LAP = {"don_gian": 16, "xuyen_khoan": 6, "dan_chieu": 4, "dieu_dai": 6, "khong_co_dieu": 5}
TEN_VAI = {"dieu_kien": "QUY TẮC", "loai_tru": "NGOẠI LỆ", "nguon": "NGUỒN", "dich": "ĐÍCH", "dan": "DẪN"}


def nhan(g: dict) -> str:
    if g.get("dieu") is None:
        return f"{g['so_hieu']} (đoạn)"
    s = f"Điều {g['dieu']}"
    if g.get("khoan") is not None:
        s += f" khoản {g['khoan']}"
    if g.get("diem"):
        s += f" điểm {g['diem']}"
    return f"{g['so_hieu']} {s}"


def xuat_duyet() -> None:
    docs = {d.doc_id: d for d in nap_van_ban()}
    ds = [json.loads(x) for x in NHAP.read_text().splitlines() if x.strip()]
    L = ["# Duyệt bộ câu hỏi đánh giá (nháp)", "",
         "Mỗi câu: sửa `Trạng thái:` (GIỮ / XOÁ; câu dự phòng đổi DỰ PHÒNG → GIỮ nếu muốn dùng) và sửa thẳng dòng "
         "`Câu hỏi:`. Xong chạy `python -m eval.duyet --chot`.", "",
         f"Tổng {len(ds)} câu nháp; cần giữ: " + ", ".join(f"{k} {v} (trung lập ≥ {TRUNG_LAP[k]})" for k, v in CAN.items())
         + ".", "",
         "**TRUNG LẬP** = gold cố ý KHÔNG trùng ranh giới cấu trúc (1–3 câu bắt đầu giữa khoản/điểm/đoạn, có thể vắt sang "
         "khoản kế) — tập số chính của báo cáo. Câu không ghi TRUNG LẬP có gold trùng ranh giới khoản (B có lợi thế cấu "
         "trúc), báo riêng. Câu DỰ PHÒNG: đổi thành GIỮ nếu muốn thay câu bị XOÁ cùng nhóm, cùng loại gold.", ""]
    if any(x.get("san_loc_co") is not None for x in ds):  # tóm tắt cờ sàng lọc (agent chỉ gắn cờ, không xoá câu nào)
        L += ["## Tóm tắt cờ sàng lọc tự động (chỉ để bạn biết xem kỹ chỗ nào — quyết định giữ/bỏ là của bạn)", "",
              "| Nhóm | Câu GIỮ (trung lập) | Không cờ | Gold đáng ngờ | Không trả lời được | Sai ý đồ nhóm | Mơ hồ | Lộ đáp án "
              "| Kiểm tra tự động | Gold ở bản cũ |",
              "|---|---|---|---|---|---|---|---|---|---|"]
        for k in CAN:
            g = [x for x in ds if x["loai"] == k and not x.get("du_phong")]
            dem = lambda t: sum(any(c.startswith(t) for c in x.get("san_loc_co") or []) for x in g)
            L.append(f"| {k} | {len(g)} ({sum(bool(x.get('trung_lap')) for x in g)}) | "
                     f"{sum(not x.get('san_loc_co') for x in g)} | {dem('gold đáng ngờ')} | {dem('KHÔNG trả lời')} | "
                     f"{dem('không đúng ý đồ')} | {dem('câu hỏi mơ hồ')} | {dem('lộ đáp án')} | "
                     f"{sum(bool(x.get('kiem_tra')) for x in g)} | {sum(bool(x.get('ban_cu')) for x in g)} |")
        L.append("")
    for x in ds:
        tt = "XOÁ" if x.get("xoa") else "DỰ PHÒNG" if x.get("du_phong") else "GIỮ"
        nguon = x["nguon_chon"]
        if nguon == "trung_lap" and not x.get("trung_lap"):
            nguon = "đầu khoản/điểm (không trung lập: span bắt đầu ngay đầu khoản hoặc điểm)"
        L += [f"## {x['qid']} · {x['loai']} · {nguon}" + (" · TRUNG LẬP" if x.get("trung_lap") else "")
              + (" · phiên bản" if x.get("phien_ban") else ""), "",
              f"Trạng thái: {tt}", f"Câu hỏi: {x.get('question', '')}", "",
              f"*Đáp án nháp của mô hình:* {x.get('dap_an_nhap', '')}", ""]
        if x.get("co"):
            L.append(f"**Cờ tự động:** {'; '.join(x['co'])}")
        if x.get("ban_cu"):
            L.append(f"**⚠ Bản cũ:** {x['ban_cu']}")
        if x.get("kiem_tra"):
            L.append(f"**⚠ Kiểm tra tự động:** {x['kiem_tra']}")
        if x.get("san_loc"):
            L.append(f"**Sàng lọc:** {x['san_loc']}")
        L.append("")
        for g in x["gold"]:
            t = docs[g["doc_id"]].text[g["start"]:g["end"]]
            vai = f" — {TEN_VAI.get(g.get('vai'), '')}" if g.get("vai") else ""
            L += [f"**Gold: {nhan(g)}{vai}**", ""] + ["> " + y for y in t.split("\n")][:40] + [""]
            if g.get("cau_loai_tru"):
                L += [f"*Câu ngoại lệ (dùng chấm 'trả lời thiếu'):* {g['cau_loai_tru']}", ""]
        for g in x.get("phien_ban_cu", []):
            t = docs[g["doc_id"]].text[g["start"]:g["end"]]
            L += [f"**Bản CŨ (đã bị {x.get('sua_boi')} sửa): {nhan(g)}**", ""] + ["> " + y for y in t.split("\n")][:20] + [""]
        L.append("---")
    DUYET.write_text("\n".join(L) + "\n")
    print("→", DUYET)


def chot() -> None:
    nhap = {x["qid"]: x for x in map(json.loads, NHAP.read_text().splitlines()) if x}
    ra, hien = [], None
    for dong in DUYET.read_text().split("\n"):
        m = re.match(r"^## (q\d+)\b", dong)
        if m:
            hien = dict(nhap[m.group(1)])
            ra.append(hien)
            continue
        if hien is None:
            continue
        if dong.startswith("Trạng thái:"):
            hien["trang_thai"] = dong.split(":", 1)[1].strip().upper()
        elif dong.startswith("Câu hỏi:"):
            hien["question"] = dong.split(":", 1)[1].strip()
    giu = [x for x in ra if x.get("trang_thai") in ("GIỮ", "GIU")]
    from eval.kiem_tra import kiem_ban_cu, kiem_tra
    kt, bc = kiem_tra(giu), kiem_ban_cu(giu)
    for x in giu:
        x["co_kiem_tra"] = [c for c in (kt.get(x["qid"], {}).get("co"), bc.get(x["qid"])) if c]
    co = [x for x in giu if x["co_kiem_tra"]]
    print(f"Kiểm tra tự động: {len(co)} câu GIỮ bị gắn cờ (không xoá) — xem trường co_kiem_tra:")
    for x in co:
        print(f"  {x['qid']} [{x['loai']}] " + " | ".join(c[:140] for c in x["co_kiem_tra"]))
    dem = {k: sum(x["loai"] == k for x in giu) for k in CAN}
    thieu = {k: f"{dem[k]}/{v}" for k, v in CAN.items() if dem[k] < v}
    if thieu:
        print("CHƯA ĐỦ số câu theo đề:", thieu, "— đổi thêm câu DỰ PHÒNG thành GIỮ")
    tl = {k: sum(x["loai"] == k and bool(x.get("trung_lap")) for x in giu) for k in CAN}
    thieu = {k: f"{tl[k]}/{v}" for k, v in TRUNG_LAP.items() if tl[k] < v}
    if thieu:
        print("CHƯA ĐỦ câu gold TRUNG LẬP:", thieu, "— đổi thêm câu DỰ PHÒNG có ghi TRUNG LẬP thành GIỮ")
    with open(CHOT, "w") as f:
        for x in giu:
            o = {"qid": x["qid"], "question": x["question"], "loai": x["loai"],
                 "gold": [{k: g.get(k) for k in ("so_hieu", "dieu", "khoan", "diem", "doc_id", "start", "end", "vai",
                                                 "cum", "cau_loai_tru") if g.get(k) is not None or k in ("dieu", "khoan")}
                          for g in x["gold"]],
                 "phien_ban": bool(x.get("phien_ban")), "phien_ban_cu": x.get("phien_ban_cu", []),
                 "nguon_chon": x["nguon_chon"], "trung_lap": bool(x.get("trung_lap")),
                 "co_kiem_tra": x["co_kiem_tra"],
                 "b_parse_ok": x.get("b_parse_ok", True)}
            f.write(json.dumps(o, ensure_ascii=False) + "\n")
    print(f"→ {CHOT}: {len(giu)} câu", dem, "| trung lập:", tl)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--xuat", action="store_true")
    ap.add_argument("--chot", action="store_true")
    ap.add_argument("--in", dest="in_qid", nargs="*", metavar="QID", help="in câu hỏi + nguyên văn gold (để kiểm)")
    a = ap.parse_args()
    if a.in_qid:
        docs = {d.doc_id: d for d in nap_van_ban()}
        for x in map(json.loads, NHAP.read_text().splitlines()):
            if x["qid"] in a.in_qid:
                print(f"=== {x['qid']} [{x['loai']}/{x['nguon_chon']}] CÂU HỎI: {x.get('question')}")
                print(f"    đáp án nháp: {x.get('dap_an_nhap')}")
                for g in x["gold"]:
                    print(f"--- GOLD {nhan(g)} vai={g.get('vai')}:\n{docs[g['doc_id']].text[g['start']:g['end']]}")
                for g in x.get("phien_ban_cu", []):
                    print(f"--- BẢN CŨ {nhan(g)}:\n{docs[g['doc_id']].text[g['start']:g['end']]}")
                print(f"--- văn bản: {docs[x['gold'][0]['doc_id']].trich_yeu}")
        raise SystemExit
    if a.xuat:
        xuat_duyet()
    if a.chot:
        chot()
    if not (a.xuat or a.chot):
        ap.print_help()
