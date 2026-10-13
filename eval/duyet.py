"""Xuất bộ câu hỏi nháp ra file dễ đọc để DUYỆT TAY, và chốt bộ câu hỏi sau khi duyệt.

    python -m eval.duyet --xuat   # eval/questions.draft.jsonl → eval/questions.review.md
    python -m eval.duyet --chot   # đọc lại eval/questions.review.md (đã sửa tay) → eval/questions.jsonl

Cách duyệt trong questions.review.md — mỗi câu là một mục "## qXXX":
  - dòng "Trạng thái: GIỮ"  → sửa thành XOÁ để loại câu này (câu DỰ PHÒNG mặc định là DỰ PHÒNG: đổi thành GIỮ để dùng);
  - dòng "Câu hỏi: …"       → sửa trực tiếp nội dung câu hỏi (một dòng);
  - gold (trích đoạn văn bản) chỉ để đọc; nếu gold sai thì XOÁ câu đó.
Khi chốt, mỗi nhóm phải còn đủ số câu của đề (50/30/25/20/15); script báo nếu thiếu.
"""
import argparse
import json
import re

import cau_hinh as ch
from chunking.base import nap_van_ban

NHAP = ch.GOC / "eval/questions.draft.jsonl"
DUYET = ch.GOC / "eval/questions.review.md"
CHOT = ch.GOC / "eval/questions.jsonl"
CAN = {"don_gian": 50, "xuyen_khoan": 30, "dan_chieu": 25, "dieu_dai": 20, "khong_co_dieu": 15}
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
         f"Tổng {len(ds)} câu nháp; cần giữ: " + ", ".join(f"{k} {v}" for k, v in CAN.items()) + ".", ""]
    for x in ds:
        tt = "DỰ PHÒNG" if x.get("du_phong") else "GIỮ"
        L += [f"## {x['qid']} · {x['loai']} · {x['nguon_chon']}" + (" · phiên bản" if x.get("phien_ban") else ""), "",
              f"Trạng thái: {tt}", f"Câu hỏi: {x.get('question', '')}", "",
              f"*Đáp án nháp của mô hình:* {x.get('dap_an_nhap', '')}", ""]
        if x.get("co"):
            L.append(f"**Cờ tự động:** {'; '.join(x['co'])}")
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
    dem = {k: sum(x["loai"] == k for x in giu) for k in CAN}
    thieu = {k: f"{dem[k]}/{v}" for k, v in CAN.items() if dem[k] < v}
    if thieu:
        print("CHƯA ĐỦ số câu theo đề:", thieu, "— đổi thêm câu DỰ PHÒNG thành GIỮ")
    with open(CHOT, "w") as f:
        for x in giu:
            o = {"qid": x["qid"], "question": x["question"], "loai": x["loai"],
                 "gold": [{k: g.get(k) for k in ("so_hieu", "dieu", "khoan", "diem", "doc_id", "start", "end", "vai",
                                                 "cum", "cau_loai_tru") if g.get(k) is not None or k in ("dieu", "khoan")}
                          for g in x["gold"]],
                 "phien_ban": bool(x.get("phien_ban")), "phien_ban_cu": x.get("phien_ban_cu", []),
                 "nguon_chon": x["nguon_chon"], "b_parse_ok": x.get("b_parse_ok", True)}
            f.write(json.dumps(o, ensure_ascii=False) + "\n")
    print(f"→ {CHOT}: {len(giu)} câu", dem)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--xuat", action="store_true")
    ap.add_argument("--chot", action="store_true")
    a = ap.parse_args()
    if a.xuat:
        xuat_duyet()
    if a.chot:
        chot()
    if not (a.xuat or a.chot):
        ap.print_help()
