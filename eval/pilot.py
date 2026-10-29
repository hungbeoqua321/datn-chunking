"""Pilot 80 câu × 3 biến thể (A, B, B+) — sinh câu trả lời rồi xuất file gán nhãn trích dẫn TAY.

Mục đích: đối chiếu bộ bóc trích dẫn bằng regex (eval/trich_dan.py) với nhãn người đọc, TRƯỚC khi
chạy sinh toàn bộ. Nếu regex hụt một mẫu định dạng nào đó một cách hệ thống thì mọi số về trích dẫn
sau này đều sai theo.

    python -m eval.pilot --sinh    # chạy truy hồi + sinh 240 câu trả lời -> results/pilot_tra_loi.jsonl
    python -m eval.pilot --xuat    # xuất eval/nhan_trich_dan.md (120 dòng) + eval/giai_ma_pilot.json
    python -m eval.pilot           # cả hai

Chốt theo cau_hinh, KHÔNG nhận tham số ghi đè: ngân sách 1200 từ, K_UNG_VIEN 50, MAX_TOKENS 384,
PP_SINH (A, B, B+).

LÀM MÙ: trong file gán nhãn, ba biến thể hiện ra là X, Y, Z gán ngẫu nhiên; bảng giải mã nằm riêng ở
eval/giai_ma_pilot.json và KHÔNG in vào file gán nhãn — người gán nhãn không được biết dòng nào của
phương pháp nào.
"""
import argparse
import collections
import json
import random
import re
import zlib
import time

import cau_hinh as ch
from eval import trich_dan
from rag import sinh, truy_hoi
from rag.kiem_chi_muc import chot_chan
from rag.sinh import LoiCat

SEED = 2026
SO_CAU_PILOT = 80
SO_DONG_NHAN = 120          # 40 mỗi biến thể; 120 dòng còn lại giữ làm dự trữ
CAU_HOI = ch.GOC / "eval/questions.jsonl"
TRA_LOI = ch.RESULTS / "pilot_tra_loi.jsonl"
NHAN = ch.GOC / "eval/nhan_trich_dan.md"
CHIA = ch.RESULTS / "gan_nhan"      # bản chẻ nhỏ để đọc qua web
SO_PHAN = 6
GIAI_MA = ch.GOC / "eval/giai_ma_pilot.json"
# phân tầng theo tỉ lệ, chốt cứng để tái lập được
TANG = {"don_gian": 36, "dieu_dai": 14, "xuyen_khoan": 12, "khong_co_dieu": 11, "dan_chieu": 7}


def chon_mau(ds: list[dict], chi_tieu: dict[str, int], seed: int) -> list[dict]:
    """Rút mẫu phân tầng, GIỮ TỈ LỆ gold trung lập trong từng tầng. Tất định theo seed."""
    rng = random.Random(seed)
    ra = []
    for nhom, can in chi_tieu.items():
        trong = [x for x in ds if x["loai"] == nhom]
        tl = sorted([x for x in trong if x.get("trung_lap")], key=lambda x: x["qid"])
        ct = sorted([x for x in trong if not x.get("trung_lap")], key=lambda x: x["qid"])
        can_tl = round(can * len(tl) / max(1, len(trong)))       # giữ tỉ lệ trung lập của tầng
        can_tl = min(can_tl, len(tl))
        can_ct = min(can - can_tl, len(ct))
        can_tl = min(can - can_ct, len(tl))
        rng.shuffle(tl); rng.shuffle(ct)
        ra += tl[:can_tl] + ct[:can_ct]
    return sorted(ra, key=lambda x: x["qid"])


def sinh_tra_loi(day_du: bool = False) -> None:
    """day_du=False: chỉ 80 câu mẫu pilot. day_du=True: CẢ bộ chính (110 câu) — bản chạy chính.

    Dù chạy kiểu nào cũng đọc lại results/pilot_tra_loi.jsonl và CHỈ sinh cặp (qid, biến thể) chưa
    có, nên bản chạy chính chỉ tốn thêm đúng phần ngoài pilot (30 câu × 3 = 90 cặp).
    """
    chot_chan()                       # chỉ mục phải khớp tệp chunk, lệch là dừng
    ds = [json.loads(l) for l in open(CAU_HOI) if l.strip()]
    mau = sorted(ds, key=lambda x: x["qid"]) if day_du else chon_mau(ds, TANG, SEED)
    print(f"mẫu pilot: {len(mau)} câu | " +
          str(dict(collections.Counter(x["loai"] for x in mau))), flush=True)
    print("  trung lập mỗi tầng: " +
          str({k: sum(1 for x in mau if x["loai"] == k and x.get("trung_lap")) for k in TANG}), flush=True)
    xong = {}
    if TRA_LOI.exists():
        xong = {(y["qid"], y["pp"]): y for y in map(json.loads, TRA_LOI.read_text().splitlines()) if y.get("tra_loi") or y.get("cat_tran")}
    cl = sinh.client()
    ra = list(xong.values())
    t0 = time.monotonic()
    tong = len(mau) * len(ch.PP_SINH)
    i = 0
    for x in mau:
        qv = truy_hoi.nhung_cau_hoi(x["question"])
        for pp in ch.PP_SINH:
            i += 1
            if (x["qid"], pp) in xong:
                continue
            kq = truy_hoi.tim(pp, qv, k=ch.K_UNG_VIEN)
            khoi = truy_hoi.ngu_canh(pp, kq, ngan_sach=ch.NGAN_SACH_NGU_CANH_TU, k=ch.K_UNG_VIEN)
            cat = ""
            try:
                r = sinh.tra_loi(x["question"], khoi, cl,
                                 {"qid": x["qid"], "bien_the": f"pilot_{pp}", "seed": 0})
            except LoiCat as e:
                # Chạm trần MAX_TOKENS → câu trả lời DỞ DANG. KHÔNG hạ trần, KHÔNG loại khỏi mẫu:
                # ghi lại thành hạng mục "cắt trần" (eval/ket_qua.py) và vẫn tính là đã làm, nên
                # cặp này có mặt trong mẫu số của mọi bảng. Xem results/nhat_ky_sua_loi.md.
                r, cat = {"tra_loi": ""}, str(e)
            ra.append({"qid": x["qid"], "pp": pp, "loai": x["loai"], "trung_lap": bool(x.get("trung_lap")),
                       "question": x["question"], "gold": x["gold"], "tra_loi": r["tra_loi"],
                       "cat_tran": bool(cat), "ly_do_cat": cat,
                       "so_khoi": len(khoi), "so_tu_ngu_canh": sum(len(k["text"].split()) for k in khoi),
                       "chunk_id": [k["chunk_id"] for k in khoi]})
            TRA_LOI.write_text("\n".join(json.dumps(y, ensure_ascii=False) for y in ra) + "\n")
            dt = time.monotonic() - t0
            print(f"  [{i}/{tong}] {x['qid']} {pp}  {dt / max(1, len(ra) - len(xong)):.0f}s/câu"
                  + ("  ← CẮT TRẦN" if cat else ""), flush=True)
    print(f"→ {TRA_LOI} ({len(ra)} câu trả lời)", flush=True)


def _nhan_gold(g: dict) -> str:
    s = f"{g['so_hieu']} Điều {g['dieu']}" if g.get("dieu") is not None else f"{g['so_hieu']} (đoạn)"
    if g.get("khoan") is not None:
        s += f" khoản {g['khoan']}"
    if g.get("diem"):
        s += f" điểm {g['diem']}"
    return s


def _hien_so_hieu(k) -> str:
    r"""Khoá số hiệu của eval.trich_dan là một frozenset các mẩu rời ({so, nam, ky_hieu}) —
    nó dùng để SO KHỚP, không phải để đọc. Dựng lại dạng `so/nam/KY` cho người gán nhãn.

    Thứ tự đã mất khi vào set nên phải suy ra: mẩu không toàn chữ số là ký hiệu, mẩu
    khớp (19|20)\d\d là năm, mẩu còn lại là số. Hai mẩu số cùng trông như năm thì
    KHÔNG đoán — in nguyên các mẩu, thà khó đọc còn hơn hiện sai số hiệu.
    """
    if not k:
        return "?"
    con = set(k)
    ky = sorted(x for x in con if not x.isdigit())
    con -= set(ky)
    nam = sorted(x for x in con if re.fullmatch(r"(19|20)\d\d", x))
    so = sorted(con - set(nam))
    if len(ky) == 1 and len(so) == 1 and len(nam) <= 1:
        return "/".join([so[0]] + nam + ky)
    if len(ky) == 1 and not so and len(nam) == 1:   # số hiệu không có năm, vd 2004/QH11
        return f"{nam[0]}/{ky[0]}"
    return " · ".join(sorted(k))                    # nhập nhằng: in nguyên, không đoán


def _nhan_trich(t: tuple) -> str:
    sh, dieu, khoan, diem = t
    p = [_hien_so_hieu(sh)]
    if dieu: p.append(f"Điều {dieu}")
    if khoan: p.append(f"khoản {khoan}")
    if diem: p.append(f"điểm {diem}")
    return " ".join(p)


def _chia_tang(tong: int) -> dict[str, int]:
    """Chia `tong` dòng cho 5 tầng theo tỉ lệ TANG, tổng phải ĐÚNG bằng `tong`.

    Làm tròn từng tầng rồi cộng lại thì lệch: 40 dòng theo tỉ lệ cho ra 18+7+6+6+4 = 41.
    Dùng phép chia lớn nhất phần dư (Hamilton): lấy phần nguyên trước, rồi phát nốt số
    dư cho các tầng có phần lẻ lớn nhất. Hoà thì ưu tiên tầng đông hơn, rồi theo tên —
    tất định, chạy lại ra đúng bảng cũ.
    """
    phan = {k: v * tong / SO_CAU_PILOT for k, v in TANG.items()}
    ra = {k: int(v) for k, v in phan.items()}
    thieu = tong - sum(ra.values())
    thu_tu = sorted(TANG, key=lambda k: (-(phan[k] - ra[k]), -TANG[k], k))
    for k in thu_tu[:thieu]:
        ra[k] += 1
    assert sum(ra.values()) == tong, ra
    return ra


def chon_dong(ghi_giai_ma: bool = True) -> tuple[list[dict], dict[str, str], int]:
    """Mẫu gán nhãn + bảng làm mù. TẤT ĐỊNH — mọi bản xuất phải gọi hàm này để mã dòng khớp nhau.

    Trả (danh sách dòng theo đúng thứ tự mã dòng 1..N, {pp: mã X/Y/Z}, số dòng dự trữ).
    """
    tat_ca = [json.loads(l) for l in open(TRA_LOI) if l.strip()]
    # Bỏ ca CẮT TRẦN khỏi mẫu gán nhãn: câu trả lời rỗng thì không có trích dẫn nào để người đọc
    # đối chiếu với regex, nên nó chiếm chỗ mà không cho thông tin. Đây CHỈ là loại khỏi mẫu gán
    # nhãn trích dẫn — trong mọi bảng kết quả, ca cắt trần vẫn đứng thành cột riêng (eval/ket_qua.py).
    rows = [r for r in tat_ca if not r.get("cat_tran")]
    rng = random.Random(SEED)
    # làm mù: A/B/B+ -> X/Y/Z ngẫu nhiên
    ma = list("XYZ"); rng.shuffle(ma)
    pp2ma = dict(zip(ch.PP_SINH, ma))
    if ghi_giai_ma:
        GIAI_MA.write_text(json.dumps({"ma_sang_pp": {v: k for k, v in pp2ma.items()},
                                       "pp_sang_ma": pp2ma, "seed": SEED}, ensure_ascii=False, indent=1))
    # 40 dòng mỗi biến thể, phân tầng theo 5 nhóm, tất định
    can_tang = _chia_tang(SO_DONG_NHAN // len(ch.PP_SINH))
    chon = []
    for pp in ch.PP_SINH:
        cua_pp = [r for r in rows if r["pp"] == pp]
        for nhom, can in can_tang.items():
            c = sorted([r for r in cua_pp if r["loai"] == nhom], key=lambda r: r["qid"])
            # crc32 chứ KHÔNG dùng hash(): hash() của chuỗi được ngẫu nhiên hoá theo từng tiến
            # trình (PYTHONHASHSEED), nên mẫu gán nhãn đổi mỗi lần chạy — nhãn gửi về theo mã dòng
            # sẽ ghép vào nhầm câu trả lời. Đã xảy ra thật, xem results/nhat_ky_sua_loi.md.
            rng2 = random.Random(SEED + zlib.crc32(nhom.encode()) % 1000)
            rng2.shuffle(c)
            chon += c[:can]
    rng.shuffle(chon)
    return chon, pp2ma, len(rows) - len(chon)


def xuat_nhan() -> None:
    chon, pp2ma, du_tru = chon_dong()
    bo = len([l for l in open(TRA_LOI) if l.strip()]) - du_tru - len(chon)
    if bo:
        print(f"   bỏ khỏi mẫu gán nhãn {bo} dòng cắt trần (câu trả lời rỗng, không có gì để đối chiếu)")
    rows = [1] * (len(chon) + du_tru)
    L = ["# Gán nhãn trích dẫn — pilot", "",
         f"**{len(chon)} dòng** cần gán nhãn tay (mỗi biến thể {len(chon)//len(ch.PP_SINH)} dòng, phân tầng theo 5 nhóm). "
         f"Còn {len(rows) - len(chon)} dòng giữ làm dự trữ.", "",
         "Ba biến thể hiện ra là **X, Y, Z** và đã được **làm mù** — bảng giải mã nằm ở "
         "`eval/giai_ma_pilot.json`, đừng mở trước khi gán nhãn xong.", "",
         "Với mỗi dòng, điền hai cột cuối:", "",
         "- **Trích dẫn người đọc thấy**: các trích dẫn bạn ĐỌC ĐƯỢC trong câu trả lời (ghi tay, kể cả khi regex bỏ sót).",
         "- **regex**: một trong bốn giá trị — **Đúng** (regex bóc khớp đúng những gì bạn thấy) · "
         "**Thiếu** (có trích dẫn mà regex không bóc được) · **Thừa** (regex bóc ra thứ không phải trích dẫn) · "
         "**Sai** (regex bóc nhưng sai số hiệu/Điều/khoản).", "", "---", ""]
    for n, r in enumerate(chon, 1):
        boc = trich_dan.boc(r["tra_loi"])
        L += [f"## {n:03d}", "",
              f"| | |", "|---|---|",
              f"| mã dòng | `{n:03d}` |",
              f"| qid | `{r['qid']}` |",
              f"| nhóm | {r['loai']}{' · trung lập' if r['trung_lap'] else ''} |",
              f"| biến thể | **{pp2ma[r['pp']]}** |",
              f"| gold | {' + '.join(_nhan_gold(g) for g in r['gold'])} |",
              f"| regex bóc được | {'; '.join(_nhan_trich(t) for t in boc) if boc else '*(không bóc được gì)*'} |",
              "", "**Câu trả lời nguyên văn:**", "", "> " + r["tra_loi"].strip().replace("\n", "\n> "), "",
              "| Trích dẫn người đọc thấy | regex |", "|---|---|", "|  |  |", "", "---", ""]
    NHAN.write_text("\n".join(L) + "\n")
    print(f"→ {NHAN} ({len(chon)} dòng) | giải mã: {GIAI_MA}")
    print("   phân bố:", dict(collections.Counter(f"{pp2ma[r['pp']]}/{r['loai']}" for r in chon)))


def xuat_chia() -> None:
    """Chẻ mẫu gán nhãn thành SO_PHAN tệp nhỏ để đọc qua web (mỗi lần tải được ~50k ký tự).

    Mã dòng GIỮ NGUYÊN như eval/nhan_trich_dan.md — cùng gọi chon_dong() nên thứ tự y hệt; nhờ
    vậy nhãn gửi về theo mã dòng ghép lại được. Mỗi tệp chỉ có bốn thứ: mã dòng (kèm mã biến thể
    đã làm mù), gold, trích dẫn regex bóc được, câu trả lời nguyên văn. Không chữ hướng dẫn, không
    ô trống — chữ thừa tốn chỗ tải.

    Chia đều ba biến thể: xếp theo (mã biến thể, mã dòng) rồi chia vòng tròn, nên mỗi tệp đúng
    SO_DONG_NHAN//SO_PHAN dòng và có đủ cả X, Y, Z.
    """
    chon, pp2ma, _ = chon_dong(ghi_giai_ma=False)
    dong = [(n, r) for n, r in enumerate(chon, 1)]
    dong.sort(key=lambda t: (pp2ma[t[1]["pp"]], t[0]))
    phan: list[list] = [[] for _ in range(SO_PHAN)]
    for i, d in enumerate(dong):
        phan[i % SO_PHAN].append(d)
    CHIA.mkdir(parents=True, exist_ok=True)
    for j, ds in enumerate(phan, 1):
        ds.sort(key=lambda t: t[0])
        L = [f"# Gán nhãn {j}/{SO_PHAN} — {len(ds)} dòng", ""]
        for n, r in ds:
            boc = trich_dan.boc(r["tra_loi"])
            L += [f"## {n:03d} · {pp2ma[r['pp']]}",
                  "gold: " + " + ".join(_nhan_gold(g) for g in r["gold"]),
                  "regex: " + ("; ".join(_nhan_trich(t) for t in boc) if boc else "(không bóc được gì)"),
                  "", "> " + r["tra_loi"].strip().replace("\n", "\n> "), ""]
        p = CHIA / f"phan_{j}.md"
        p.write_text("\n".join(L) + "\n")
        bt = collections.Counter(pp2ma[r["pp"]] for _, r in ds)
        print(f"→ {p}  {len(ds)} dòng, {len(p.read_text())} ký tự, "
              + " ".join(f"{k}={bt[k]}" for k in "XYZ"))


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--sinh", action="store_true")
    ap.add_argument("--day-du", action="store_true", help="bản chạy chính: cả 110 câu, không chỉ 80 câu pilot")
    ap.add_argument("--xuat", action="store_true")
    ap.add_argument("--chia", action="store_true", help=f"chẻ mẫu gán nhãn thành {SO_PHAN} tệp nhỏ trong results/gan_nhan/")
    a = ap.parse_args()
    if a.chia:
        xuat_chia()
        return
    if a.sinh or a.day_du or not a.xuat:
        sinh_tra_loi(day_du=a.day_du)
    if a.xuat or not a.sinh:
        xuat_nhan()


if __name__ == "__main__":
    main()
