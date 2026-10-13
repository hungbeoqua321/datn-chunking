"""Chọn tập văn bản cuối cùng theo hạn ngạch của đề (sau khi đã tải và chuẩn hoá) → data/manifest.csv.

Hạn ngạch (tối thiểu, theo đề):
  luat         ≥ 20  Luật/Bộ luật có bố cục Chương (văn bản gốc, không phải văn bản sửa đổi)
  nd_tt        ≥ 30  Nghị định, Thông tư (gốc)                       — chia đều 15 + 15
  khong_dieu   ≥ 10  văn bản KHÔNG có "Điều" (Công văn, Chỉ thị, Thông báo, …)
  dieu_dai     ≥ 10  văn bản có ít nhất một Điều > 1500 từ (nhãn chồng lên các nhóm trên; không tính văn bản sửa đổi)
  sua_doi      ≥ 10  văn bản sửa đổi, bổ sung văn bản khác
  (thêm)            mọi văn bản gốc có tiêu đề Điều vỡ khi crawl thô (ca khó của nhược điểm 2)
  vbhn         ≥ 5   văn bản hợp nhất — mỗi VBHN kéo theo cả "họ": văn bản gốc + các văn bản sửa đổi được hợp nhất

Mọi lựa chọn ngẫu nhiên dùng seed cố định (SEED) nên chạy lại ra đúng tập cũ. Văn bản không có số hiệu bị loại
(không trích dẫn được). Mỗi văn bản có đúng một `nhom` chính; `dieu_dai` và `ho` là nhãn phụ.

    python -m crawl.chon_van_ban           # ghi data/manifest.csv (bỏ qua nếu đã có)
    python -m crawl.chon_van_ban --force
"""
import argparse
import csv
import json
import random
import re

import cau_hinh as ch
from crawl.thu_thap import RE_SUA_DOI, UNG_VIEN, quan_he

SEED = 2026
HAN_NGACH = {"luat": 20, "nd": 15, "tt": 15, "khong_dieu": 10, "dieu_dai": 10, "sua_doi": 10, "vbhn": 5}
COT = ["id", "so_hieu", "loai_van_ban", "nhom", "dieu_dai", "tieu_de_vo", "ho", "vai_trong_ho", "ngay_ban_hanh",
       "co_quan_ban_hanh", "trich_yeu", "url_nguon", "hieu_luc", "so_tu", "so_dieu", "dieu_dai_nhat", "ly_do"]


def nap() -> dict[str, dict]:
    tk = {d["id"]: d for d in map(json.loads, (ch.DATA / "thong_ke_chuan_hoa.jsonl").read_text().splitlines())}
    uv = {d["id"]: d for d in map(json.loads, UNG_VIEN.read_text().splitlines()) if d}
    ds = {}
    for doc_id, t in tk.items():
        m = json.loads((ch.RAW / f"{doc_id}.json").read_text())
        so = (m.get("so_hieu") or "").strip()
        if not m.get("co_noi_dung") or not so or so.lower() in ("không số", "khong so"):
            continue
        ds[doc_id] = {**m, **t, "nhom_tim": (uv.get(doc_id) or {}).get("nhom_tim"),
                      "sua_doi": bool(RE_SUA_DOI.search(m.get("trich_yeu") or "")),
                      "co_dieu": t["so_dieu"] > 0 or (t["sau"]["ky_vong"] or 0) > 0}
    return ds


def chon(ds: dict[str, dict]) -> list[dict]:
    rng = random.Random(SEED)
    da: dict[str, dict] = {}

    def them(d: dict, nhom: str, ly_do: str, ho: str = "", vai: str = "") -> None:
        if d["id"] not in da:
            da[d["id"]] = {**d, "nhom": nhom, "ly_do": ly_do, "ho": ho, "vai_trong_ho": vai}

    # 1) họ phiên bản: VBHN có đủ văn bản thành viên (gốc + sửa đổi) đã tải được
    ho_ok = []
    for v in sorted((d for d in ds.values() if d["loai_van_ban"] == "Văn bản hợp nhất"), key=lambda d: d["id"]):
        tv = quan_he(v["id"]).get("Hợp nhất", [])
        if 2 <= len(tv) <= 4 and all(t["id"] in ds for t in tv):
            tv = [ds[t["id"]] for t in tv]
            # họ "sạch": đúng một văn bản gốc, còn lại đều là văn bản sửa đổi (loại họ có QĐ đính chính …)
            if sum(not t["sua_doi"] for t in tv) == 1:
                ho_ok.append((v, tv))
    rng.shuffle(ho_ok)
    # ưu tiên có ít nhất một họ của Luật (VBHN của Văn phòng Quốc hội)
    ho_ok.sort(key=lambda h: not any(t["loai_van_ban"] in ("Luật", "Bộ luật") for t in h[1]))
    for v, tv in ho_ok[:HAN_NGACH["vbhn"]]:
        them(v, "vbhn", "VBHN có đủ văn bản được hợp nhất", ho=v["id"], vai="hop_nhat")
        for t in sorted(tv, key=lambda d: d["ngay_ban_hanh"]):
            vai = "sua_doi" if t["sua_doi"] else "goc"
            them(t, "sua_doi" if t["sua_doi"] else ("luat" if t["loai_van_ban"] in ("Luật", "Bộ luật") else "nd_tt"),
                 f"thành viên họ {v['so_hieu']}", ho=v["id"], vai=vai)

    # 2) văn bản sửa đổi, bổ sung (bù cho đủ hạn ngạch, ưu tiên có cả Luật)
    sd = [d for d in ds.values() if d["sua_doi"] and d["co_dieu"] and d["id"] not in da
          and d["loai_van_ban"] in ("Luật", "Bộ luật", "Nghị định", "Thông tư")]
    rng.shuffle(sd)
    sd.sort(key=lambda d: d["loai_van_ban"] not in ("Luật", "Bộ luật"))
    can = HAN_NGACH["sua_doi"] - sum(1 for d in da.values() if d["nhom"] == "sua_doi")
    for d in sd[:max(0, can)]:
        them(d, "sua_doi", "tiêu đề có 'sửa đổi, bổ sung'")

    # 3) Luật/Bộ luật gốc có Chương
    lu = [d for d in ds.values() if d["loai_van_ban"] in ("Luật", "Bộ luật") and not d["sua_doi"]
          and d["co_chuong"] and d["so_dieu"] >= 10 and d["id"] not in da]
    rng.shuffle(lu)
    can = HAN_NGACH["luat"] - sum(1 for d in da.values() if d["nhom"] == "luat")
    for d in lu[:max(0, can)]:
        them(d, "luat", "Luật/Bộ luật gốc có bố cục Chương")

    # 4) Nghị định, Thông tư gốc
    for loai, k in (("Nghị định", "nd"), ("Thông tư", "tt")):
        ung = [d for d in ds.values() if d["loai_van_ban"] == loai and not d["sua_doi"] and d["so_dieu"] >= 3
               and d["id"] not in da]
        rng.shuffle(ung)
        can = HAN_NGACH[k] - sum(1 for d in da.values() if d["nhom"] == "nd_tt" and d["loai_van_ban"] == loai)
        for d in ung[:max(0, can)]:
            them(d, "nd_tt", f"{loai} gốc")

    # 4b) ca khó "tiêu đề Điều vỡ khi crawl thô" (đề yêu cầu tập dữ liệu có đủ ca khó): lấy hết văn bản gốc
    #     Luật/NĐ/TT có tiêu đề vỡ trong text thô — chúng hiếm (vài văn bản) nên chọn ngẫu nhiên dễ bỏ sót.
    for d in sorted(ds.values(), key=lambda d: d["id"]):
        if (d["truoc"]["thieu"] > 0 and not d["sua_doi"] and d["id"] not in da
                and d["loai_van_ban"] in ("Luật", "Bộ luật", "Nghị định", "Thông tư")):
            them(d, "luat" if d["loai_van_ban"] in ("Luật", "Bộ luật") else "nd_tt",
                 f"tiêu đề Điều vỡ khi crawl thô ({d['truoc']['thieu']}/{d['truoc']['ky_vong']})")

    # 5) văn bản không có "Điều"
    #    lấy xoay vòng theo loại văn bản để không dồn hết vào một loại (Chỉ thị, Công văn, Thông báo, …)
    theo_loai: dict[str, list[dict]] = {}
    for d in sorted(ds.values(), key=lambda d: d["id"]):
        if not d["co_dieu"] and d["so_tu"] >= 200 and d["id"] not in da:
            theo_loai.setdefault(d["loai_van_ban"], []).append(d)
    for g in theo_loai.values():
        rng.shuffle(g)
    con = HAN_NGACH["khong_dieu"]
    while con and any(theo_loai.values()):
        for k in sorted(theo_loai):
            if con and theo_loai[k]:
                d = theo_loai[k].pop()
                them(d, "khong_dieu", f"{d['loai_van_ban']} không chia Điều")
                con -= 1

    # 6) nhãn "Điều dài" (> 1500 từ) — không tính văn bản sửa đổi (Điều 1 của chúng dài vì trích nguyên văn).
    #    Thiếu thì bổ sung thêm văn bản gốc có Điều dài từ phần ứng viên còn lại.
    def dem_dai() -> int:
        return sum(1 for d in da.values() if d["so_dieu_tren_1500"] > 0 and d["vai_trong_ho"] != "sua_doi"
                   and d["nhom"] != "sua_doi")

    them_dai = [d for d in ds.values() if d["so_dieu_tren_1500"] > 0 and not d["sua_doi"] and d["id"] not in da
                and d["loai_van_ban"] in ("Luật", "Bộ luật", "Nghị định", "Thông tư")]
    rng.shuffle(them_dai)
    while dem_dai() < HAN_NGACH["dieu_dai"] and them_dai:
        d = them_dai.pop()
        them(d, "luat" if d["loai_van_ban"] in ("Luật", "Bộ luật") else "nd_tt", "bổ sung cho nhóm Điều dài")
    ra = []
    for d in da.values():
        d["dieu_dai"] = d["so_dieu_tren_1500"] > 0 and d["nhom"] != "sua_doi"
        d["tieu_de_vo"] = d["truoc"]["thieu"] > 0
        ra.append(d)
    return sorted(ra, key=lambda d: (d["nhom"], d["loai_van_ban"], d["ngay_ban_hanh"], d["so_hieu"]))


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    if ch.MANIFEST.exists() and not a.force:
        print("Đã có", ch.MANIFEST, "— dùng --force để chọn lại")
        return
    ra = chon(nap())
    with open(ch.MANIFEST, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COT, extrasaction="ignore")
        w.writeheader()
        for d in ra:
            w.writerow({k: d.get(k, "") for k in COT})
    dem = {}
    for d in ra:
        dem[d["nhom"]] = dem.get(d["nhom"], 0) + 1
    print(f"{len(ra)} văn bản →", ch.MANIFEST, dem, "| Điều dài:", sum(d["dieu_dai"] for d in ra),
          "| họ phiên bản:", len({d['ho'] for d in ra if d['ho']}))
    thieu = {k: v for k, v in {"luat": 20, "nd_tt": 30, "khong_dieu": 10, "sua_doi": 10, "vbhn": 5}.items()
             if dem.get(k, 0) < v}
    if sum(d["dieu_dai"] for d in ra) < 10:
        thieu["dieu_dai"] = 10
    if thieu:
        print("CẢNH BÁO — chưa đủ hạn ngạch:", thieu)


if __name__ == "__main__":
    main()
