"""Thu thập ứng viên VBQPPL từ vbpl.vn: tìm theo loại → tải toàn văn HTML + metadata + cây cấu trúc.

Chỉ TẢI; việc chọn ra tập cuối (theo hạn ngạch của đề) làm ở crawl/chon_van_ban.py sau khi chuẩn hoá,
vì một số tiêu chí (có Chương không, có Điều trên 1500 từ không, có "Điều" không) phải đọc nội dung mới biết.

Mỗi văn bản <id> lưu trong data/raw/:
  <id>.html       nguyên văn documentContent.content (HTML gốc, chưa sửa gì)
  <id>.json       metadata: so_hieu, loai_van_ban, ngay_ban_hanh, co_quan_ban_hanh, trich_yeu, url_nguon,
                  hieu_luc (effStatus), hop_nhat (isConsolidatedDocument), ...
  <id>.cay.json   cây Phần/Chương/Mục/Điều/Khoản do vbpl.vn biên tập (nguồn độc lập để đếm Điều kỳ vọng)
  <id>.luoc_do.json  quan hệ với văn bản khác (chỉ tải cho VBHN, văn bản sửa đổi và văn bản gốc của họ)

    python -m crawl.thu_thap              # tìm + tải (bỏ qua file đã có)
    python -m crawl.thu_thap --force      # tải lại tất cả
    python -m crawl.thu_thap --chi-tim    # chỉ làm danh sách ứng viên (data/ung_vien.jsonl)
"""
import argparse
import json
import random
import re
import sys

import cau_hinh as ch
from crawl.vbpl import QUAN_HE, Vbpl, url_nguon

UNG_VIEN = ch.DATA / "ung_vien.jsonl"
SEED = 2026

# (nhóm, loại văn bản trên vbpl, số trang × 50 kết quả mới nhất)
NGUON = [
    ("luat", "Bộ luật", 1), ("luat", "Luật", 4),
    ("nd_tt", "Nghị định", 3), ("nd_tt", "Thông tư", 3),
    ("vbhn", "Văn bản hợp nhất", 3),
    ("khong_dieu", "Công văn", 2), ("khong_dieu", "Chỉ thị", 2), ("khong_dieu", "Thông báo", 1),
    ("khong_dieu", "Văn bản hành chính liên quan", 1), ("khong_dieu", "Văn bản khác", 1),
]
# số ứng viên tải về mỗi nhóm (nhiều hơn hạn ngạch để còn lọc theo nội dung)
TAI = {"luat_goc": 32, "nd_tt_goc": 70, "sua_doi": 18, "vbhn": 14, "khong_dieu": 30}
RE_SUA_DOI = re.compile(r"sửa đổi|bổ sung một số điều", re.I)


def tim_ung_vien(v: Vbpl) -> list[dict]:
    ds, da = [], set()
    for nhom, loai, so_trang in NGUON:
        for trang in range(1, so_trang + 1):
            r = v.tim(loai=loai, trang=trang, co=50)
            for it in r.get("items", []):
                if it["id"] in da:
                    continue
                da.add(it["id"])
                ds.append({"id": it["id"], "nhom_tim": nhom, "loai_van_ban": (it.get("docType") or {}).get("name"),
                           "so_hieu": it.get("docNum"), "trich_yeu": it.get("title"),
                           "ngay_ban_hanh": (it.get("issueDate") or "")[:10],
                           "hieu_luc": (it.get("effStatus") or {}).get("name"), "co_quan": it.get("agencyName")})
            print(f"  {loai} trang {trang}: tổng {r.get('total')}", flush=True)
    return ds


def luu_van_ban(v: Vbpl, doc_id: str, force: bool, luoc_do: bool = False) -> dict | None:
    pj, ph = ch.RAW / f"{doc_id}.json", ch.RAW / f"{doc_id}.html"
    if force or not (pj.exists() and ph.exists()):
        d = v.chi_tiet(doc_id)
        html = (d.get("documentContent") or {}).get("content") or ""
        meta = {
            "id": doc_id, "so_hieu": d.get("docNum"), "loai_van_ban": (d.get("docType") or {}).get("name"),
            "ngay_ban_hanh": (d.get("issueDate") or "")[:10], "co_quan_ban_hanh": d.get("agencyName"),
            "trich_yeu": d.get("title"), "url_nguon": url_nguon(doc_id),
            "hieu_luc": (d.get("effStatus") or {}).get("name"), "hieu_luc_tu": (d.get("effFrom") or "")[:10],
            "hieu_luc_den": (d.get("effTo") or "")[:10], "hop_nhat": bool(d.get("isConsolidatedDocument")),
            "html_cu": bool(d.get("isOld")), "co_noi_dung": bool(html.strip()), "nguon": "vbpl.vn",
            "nguoi_ky": [{"ten": i.get("personName"), "chuc_vu": i.get("jobTitleName")} for i in d.get("documentIssues") or []],
        }
        ch.RAW.mkdir(parents=True, exist_ok=True)
        ph.write_text(html)
        pj.write_text(json.dumps(meta, ensure_ascii=False, indent=1))
    meta = json.loads(pj.read_text())
    pc = ch.RAW / f"{doc_id}.cay.json"
    if force or not pc.exists():
        try:
            pc.write_text(json.dumps(v.cay(doc_id), ensure_ascii=False))
        except Exception as e:  # noqa: BLE001 — văn bản cũ có thể không có cây
            pc.write_text(json.dumps({"loi": str(e)}, ensure_ascii=False))
    if luoc_do:
        pl = ch.RAW / f"{doc_id}.luoc_do.json"
        if force or not pl.exists():
            o = v.luoc_do(doc_id)
            pl.write_text(json.dumps(o, ensure_ascii=False))
    return meta


def quan_he(doc_id: str) -> dict[str, list[dict]]:
    """{tên quan hệ: [{id, name}]} từ <id>.luoc_do.json."""
    pl = ch.RAW / f"{doc_id}.luoc_do.json"
    if not pl.exists():
        return {}
    o = json.loads(pl.read_text())
    return {QUAN_HE.get(int(k), k): vs for k, vs in (o.get("documentNamesByType") or {}).items()}


def bo_sung_khong_dieu(v: Vbpl, can: int) -> None:
    """Công văn trên vbpl.vn phần lớn chỉ có PDF (HTML rỗng) → lật thêm trang, tải tới khi đủ `can` văn bản
    Công văn / VB hành chính có toàn văn ≥ 300 từ và không có tiêu đề "Điều". Ghi thêm vào ung_vien.jsonl."""
    da = {json.loads(x)["id"] for x in UNG_VIEN.read_text().splitlines() if x.strip()}
    co = 0
    for loai in ("Công văn", "Văn bản hành chính liên quan", "Văn bản khác"):
        for trang in range(1, 16):
            r = v.tim(loai=loai, trang=trang, co=50)
            items = r.get("items", [])
            if not items:
                break
            for it in items:
                if co >= can:
                    return
                if it["id"] in da:
                    continue
                da.add(it["id"])
                with open(UNG_VIEN, "a") as f:
                    f.write(json.dumps({"id": it["id"], "nhom_tim": "khong_dieu",
                                        "loai_van_ban": (it.get("docType") or {}).get("name"), "so_hieu": it.get("docNum"),
                                        "trich_yeu": it.get("title"), "ngay_ban_hanh": (it.get("issueDate") or "")[:10],
                                        "hieu_luc": (it.get("effStatus") or {}).get("name"),
                                        "co_quan": it.get("agencyName")}, ensure_ascii=False) + "\n")
                m = luu_van_ban(v, it["id"], False)
                h = (ch.RAW / f"{it['id']}.html").read_text()
                chu = re.sub(r"<[^>]+>", " ", h)
                if m["co_noi_dung"] and len(chu.split()) >= 300 and not re.search(r">\s*Điều\s+\d+\s*[.:]", h):
                    co += 1
                    print(f"  +{co} {loai}: {m['so_hieu']} ({len(chu.split())} từ)", flush=True)
                else:  # không dùng được: xoá để không lẫn vào tập ứng viên
                    for duoi in (".html", ".json", ".cay.json"):
                        (ch.RAW / f"{it['id']}{duoi}").unlink(missing_ok=True)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--force", action="store_true", help="tìm và tải lại tất cả")
    ap.add_argument("--chi-tim", action="store_true", help="chỉ lập danh sách ứng viên")
    ap.add_argument("--bo-sung-khong-dieu", type=int, metavar="N", default=0,
                    help="tìm thêm Công văn / VB hành chính có toàn văn (đa số chỉ có PDF) cho đủ N văn bản")
    a = ap.parse_args()
    v = Vbpl()
    if a.bo_sung_khong_dieu:
        bo_sung_khong_dieu(v, a.bo_sung_khong_dieu)
        return
    if a.force or not UNG_VIEN.exists():
        print("Tìm ứng viên trên vbpl.vn …")
        ds = tim_ung_vien(v)
        UNG_VIEN.write_text("\n".join(json.dumps(x, ensure_ascii=False) for x in ds) + "\n")
    ds = [json.loads(x) for x in UNG_VIEN.read_text().splitlines() if x.strip()]
    print(f"{len(ds)} ứng viên trong {UNG_VIEN.name}")
    if a.chi_tim:
        return

    rng = random.Random(SEED)
    sua_doi = [x for x in ds if x["nhom_tim"] in ("luat", "nd_tt") and RE_SUA_DOI.search(x["trich_yeu"] or "")]
    goc_luat = [x for x in ds if x["nhom_tim"] == "luat" and x not in sua_doi]
    goc_ndtt = [x for x in ds if x["nhom_tim"] == "nd_tt" and x not in sua_doi]
    vbhn = [x for x in ds if x["nhom_tim"] == "vbhn"]
    khong = [x for x in ds if x["nhom_tim"] == "khong_dieu"]
    # Bộ luật luôn lấy hết (chỉ có ~17); phần còn lại bốc ngẫu nhiên có seed
    bo_luat = [x for x in goc_luat if x["loai_van_ban"] == "Bộ luật"]
    luat = bo_luat + rng.sample([x for x in goc_luat if x not in bo_luat], max(0, TAI["luat_goc"] - len(bo_luat)))
    nd = [x for x in goc_ndtt if x["loai_van_ban"] == "Nghị định"]
    tt = [x for x in goc_ndtt if x["loai_van_ban"] == "Thông tư"]
    ndtt = rng.sample(nd, min(len(nd), TAI["nd_tt_goc"] // 2)) + rng.sample(tt, min(len(tt), TAI["nd_tt_goc"] // 2))
    sd_luat = [x for x in sua_doi if x["nhom_tim"] == "luat"]
    sd = rng.sample(sd_luat, min(6, len(sd_luat)))
    sd += rng.sample([x for x in sua_doi if x not in sd], min(TAI["sua_doi"] - len(sd), len(sua_doi) - len(sd)))
    kd = rng.sample(khong, min(TAI["khong_dieu"], len(khong)))

    tai = [(x, False) for x in luat + ndtt + kd] + [(x, True) for x in sd]
    print(f"Tải {len(tai)} văn bản + {TAI['vbhn']} VBHN kèm họ (≤ 1 request/giây) …", flush=True)
    for i, (x, ld) in enumerate(tai, 1):
        m = luu_van_ban(v, x["id"], a.force, luoc_do=ld)
        if i % 10 == 0:
            print(f"  {i}/{len(tai)} {m['so_hieu']}", flush=True)

    # Họ phiên bản: VBHN + các văn bản được hợp nhất vào nó (gốc + sửa đổi). Ưu tiên họ nhỏ (2–4 văn bản).
    so_ho = 0
    for x in rng.sample(vbhn, len(vbhn)):
        if so_ho >= TAI["vbhn"]:
            break
        luu_van_ban(v, x["id"], a.force, luoc_do=True)
        thanh_vien = quan_he(x["id"]).get("Hợp nhất", [])
        if not 2 <= len(thanh_vien) <= 4:
            continue
        ok = True
        for tv in thanh_vien:
            m = luu_van_ban(v, tv["id"], a.force, luoc_do=True)
            ok &= bool(m and m["co_noi_dung"])
        if ok:
            so_ho += 1
            print(f"  họ {so_ho}: {x['so_hieu']} ← {[t['name'][:40] for t in thanh_vien]}", flush=True)
    print("Xong. Số file HTML:", len(list(ch.RAW.glob("*.html"))))


if __name__ == "__main__":
    sys.exit(main())
