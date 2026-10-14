"""Kiểm tra tự động TRƯỚC KHI CHỐT bộ câu hỏi — chỉ GẮN CỜ, không xoá câu nào.

  xuyen_khoan: hai đoạn gold có thật là quan hệ QUY TẮC – NGOẠI LỆ không (đoạn loai_tru có nêu ngoại lệ, giới hạn hay
               trường hợp loại trừ của chính quy tắc ở đoạn dieu_kien không)?
  dan_chieu  : câu hỏi có trả lời ĐẦY ĐỦ được chỉ bằng đoạn NGUỒN không (nếu được → không cần đoạn ĐÍCH → sai ý đồ nhóm)?
  dan_chieu  : (máy móc, không dùng mô hình) đáp án nháp đã nằm gần trọn trong đoạn NGUỒN → gắn cờ (kiem_nguon_chua_dap_an)
  mọi nhóm   : gold nằm ở BẢN CŨ trong khi bản mới cũng có trong kho (BLHS 1999↔2015, BLLĐ 2012↔2019, BLHH 1990↔2015,
               văn bản gốc↔VBHN) — so nội dung đoạn gold với đơn vị khớp nhất của bản mới (tất định, không dùng mô hình).

Giám khảo là chính mô hình sinh tại chỗ (llama-server, temperature 0), mỗi lần gọi qua rag.sinh.goi (ghi nhật ký token,
dừng nếu bị cắt). Đây là bộ lọc gắn cờ để người duyệt chú ý, không phải nhãn đúng/sai cuối cùng — mô hình 4B có thể nhầm.
Kết quả lưu đệm theo (qid, nội dung câu hỏi, gold) trong eval/kiem_tra.json: sửa câu hỏi thì câu đó được kiểm lại.

    python -m eval.kiem_tra                 # kiểm các câu trong eval/questions.draft.jsonl, ghi cờ vào bản nháp
    (eval.duyet --chot cũng gọi kiem_tra() trên các câu GIỮ sau khi bạn sửa)
"""
import argparse
import hashlib
import json

import cau_hinh as ch
from chunking.base import nap_van_ban
from rag import sinh

KQ = ch.GOC / "eval/kiem_tra.json"
NHAP = ch.GOC / "eval/questions.draft.jsonl"
SCHEMA = {"type": "object", "properties": {"dat": {"type": "boolean"}, "ly_do": {"type": "string"}},
          "required": ["dat", "ly_do"]}
HE_THONG = "Bạn là chuyên gia pháp luật Việt Nam, đánh giá chặt chẽ, chỉ dựa trên đoạn văn bản được cung cấp. Trả lời JSON."


def _tin_nhan(x: dict, docs) -> list[dict]:
    t = {g.get("vai"): docs[g["doc_id"]].text[g["start"]:g["end"]] for g in x["gold"]}
    if x["loai"] == "xuyen_khoan":
        nd = (f"ĐOẠN A:\n{t.get('dieu_kien', '')}\n\nĐOẠN B:\n{t.get('loai_tru', '')}\n\n"
              "Đoạn B có nêu một NGOẠI LỆ, GIỚI HẠN hoặc TRƯỜNG HỢP LOẠI TRỪ áp dụng cho CHÍNH quy tắc ở đoạn A không "
              "(tức là muốn áp dụng đúng quy tắc ở đoạn A thì phải biết đoạn B)? Hai quy định song song, độc lập, hoặc "
              "đoạn B chỉ là ngoại lệ của một quy định khác thì trả lời false.\n"
              'Trả về JSON {"dat": true/false, "ly_do": "một câu"}.')
    else:
        nd = (f"CÂU HỎI: {x['question']}\n\nĐOẠN NGUỒN:\n{t.get('nguon', '')}\n\n"
              "Chỉ dựa vào ĐOẠN NGUỒN (không được đọc văn bản mà đoạn này dẫn chiếu tới), có trả lời ĐẦY ĐỦ và CỤ THỂ "
              "câu hỏi được không? Nếu đoạn nguồn chỉ nói \"theo quy định tại Điều …\" mà nội dung cần trả lời nằm ở "
              "điều được dẫn chiếu thì trả lời false.\n"
              'Trả về JSON {"dat": true/false, "ly_do": "một câu"}.')
    return [{"role": "system", "content": HE_THONG}, {"role": "user", "content": nd}]


# bản cũ → bản mới cùng có trong kho (ngoài các họ văn bản gốc → văn bản hợp nhất lấy từ manifest)
THAY_THE = {"15/1999/QH10": "100/2015/QH13", "10/2012/QH13": "45/2019/QH14", "42-LCT/HĐNN8": "95/2015/QH13"}


def kiem_ban_cu(ds: list[dict]) -> dict[str, str]:
    """{qid: cờ} cho câu có gold ở bản cũ mà bản mới cũng trong kho. Với mỗi đơn vị gold (trừ câu dẫn): tìm đơn vị nhỏ
    nhất của bản mới chứa nhiều 3-gram từ của gold nhất; độ chứa ≥ 0,9 → GIỐNG, 0,6–0,9 → KHÁC ÍT, < 0,6 → KHÁC NHIỀU
    hoặc không còn trong bản mới (máy không phân biệt được hai trường hợp này — đọc tay)."""
    import re
    import unicodedata

    from eval.don_vi import chi_muc

    docs = {d.doc_id: d for d in nap_van_ban()}
    theo_sh = {d.so_hieu: d for d in docs.values()}
    cap = dict(THAY_THE)
    for d in docs.values():
        if d.meta.get("vai_trong_ho") == "goc":
            vb = next((x for x in docs.values() if x.meta.get("ho") == d.meta.get("ho")
                       and x.meta.get("vai_trong_ho") == "hop_nhat"), None)
            if vb:
                cap[d.so_hieu] = vb.so_hieu

    def ng(s: str) -> set:
        w = re.sub(r"\[\d+\]|[^\w]+", " ", unicodedata.normalize("NFC", s).lower()).split()
        return {tuple(w[i:i + 3]) for i in range(max(1, len(w) - 2))}

    from eval.cham import ban_tuong_duong, doc_cap

    bang = doc_cap()
    vb = {k: d.text for k, d in docs.items()}
    sh = {k: d.so_hieu for k, d in docs.items()}
    dv_cap = {k: [u for t in ("dieu", "khoan", "diem") for u in chi_muc(d)[t]] for k, d in docs.items() if d.so_hieu in bang}
    dv: dict[str, list] = {}
    ra = {}
    for x in ds:
        phan = []
        for g in x["gold"]:
            if g["so_hieu"] not in cap or g.get("vai") == "dan":
                continue
            if not x.get("phien_ban") and ban_tuong_duong(g, vb, sh, dv_cap, bang):
                continue  # đã có bản tương đương theo bảng cặp liệt kê tay → lấy trúng bản mới vẫn được tính
            moi = cap[g["so_hieu"]]
            if moi not in dv:
                cm = chi_muc(theo_sh[moi])
                dv[moi] = [(u, ng(theo_sh[moi].text[u.start:u.end]), u.end - u.start)
                           for t in ("diem", "khoan", "dieu") for u in cm[t]]
            G = ng(docs[g["doc_id"]].text[g["start"]:g["end"]])
            c, _, u = max(((len(G & U) / max(1, len(G)), -n, u) for u, U, n in dv[moi]), key=lambda v: (round(v[0], 2), v[1]))
            kl = "GIỐNG" if c >= 0.9 else "KHÁC ÍT" if c >= 0.6 else "KHÁC NHIỀU hoặc không còn"
            nh = f"Điều {u.dieu}" + (f" khoản {u.khoan}" if u.khoan else "") + (f" điểm {u.diem}" if u.diem else "")
            phan.append(f"{g['so_hieu']} Điều {g['dieu']} ↔ {moi} {nh}: {kl} (chứa {c:.2f})")
        if phan:
            ra[x["qid"]] = "gold ở BẢN CŨ, bản mới cũng có trong kho — " + "; ".join(phan)
    return ra


def kiem_nguon_chua_dap_an(ds: list[dict], nguong: float = 0.6) -> dict[str, str]:
    """dan_chieu — kiểm tra MÁY MÓC (không dùng mô hình): đoạn nguồn một mình có chứa đáp án không. Đo tỉ lệ cặp từ liền
    nhau (đã chuẩn hoá) của đáp án nháp nằm trong đoạn nguồn và trong đoạn đích; gắn cờ khi ≥ `nguong` đáp án đã có trong
    nguồn và đoạn đích không đóng góp nhiều hơn. Giới hạn: dựa vào đáp án nháp của mô hình — câu hỏi sửa tay mà đáp án
    nháp không còn khớp thì kết quả không còn ý nghĩa (khi đó dựa vào kiểm tra bằng giám khảo)."""
    import re
    import unicodedata

    docs = {d.doc_id: d for d in nap_van_ban()}

    def cap_tu(s: str) -> set:
        w = re.sub(r"[^\w]+", " ", unicodedata.normalize("NFC", s).lower()).split()
        return {(a, b) for a, b in zip(w, w[1:])}

    ra = {}
    for x in ds:
        if x["loai"] != "dan_chieu":
            continue
        A = cap_tu(x.get("dap_an_nhap") or "")
        if not A:
            ra[x["qid"]] = "không có đáp án nháp để kiểm"
            continue
        t = {g.get("vai"): cap_tu(docs[g["doc_id"]].text[g["start"]:g["end"]]) for g in x["gold"]}
        n, dch = len(A & t.get("nguon", set())) / len(A), len(A & t.get("dich", set())) / len(A)
        if n >= nguong and dch <= n:
            ra[x["qid"]] = (f"đoạn nguồn một mình đã chứa {n:.0%} đáp án nháp (đoạn đích {dch:.0%}) — "
                            "câu hỏi có thể không cần đọc điều được dẫn chiếu")
    return ra


def _khoa(x: dict) -> str:
    return hashlib.sha1(json.dumps([x["qid"], x["loai"], x.get("question"), x["gold"]], ensure_ascii=False,
                                   sort_keys=True).encode()).hexdigest()


def kiem_tra(ds: list[dict]) -> dict[str, dict]:
    """{qid: {"loai", "dat", "ly_do", "co"}} cho các câu xuyen_khoan / dan_chieu trong ds. `co` = chuỗi cờ hoặc ""."""
    docs = {d.doc_id: d for d in nap_van_ban()}
    dem = json.loads(KQ.read_text()) if KQ.exists() else {}
    cl = sinh.client()
    ra = {}
    try:
        for x in ds:
            if x["loai"] not in ("xuyen_khoan", "dan_chieu"):
                continue
            k = _khoa(x)
            if k not in dem:
                r, _ = sinh.goi(_tin_nhan(x, docs), {"qid": x["qid"], "bien_the": "kiem_tra_truoc_chot", "seed": 0,
                                                     "so_khoi": len(x["gold"]), "so_tu_ngu_canh": 0}, cl,
                                model=sinh.tham_so()["model"], temperature=0, seed=42, max_tokens=200,
                                extra_body={"cache_prompt": False},
                                response_format={"type": "json_schema", "json_schema": {"name": "kiem_tra", "schema": SCHEMA}})
                try:
                    o = json.loads(r.choices[0].message.content)
                except json.JSONDecodeError:
                    o = {"dat": None, "ly_do": "giám khảo trả về không phải JSON"}
                dem[k] = {"qid": x["qid"], "loai": x["loai"], "dat": o.get("dat"), "ly_do": o.get("ly_do", "")}
                KQ.write_text(json.dumps(dem, ensure_ascii=False, indent=1))
                print(x["qid"], x["loai"], dem[k]["dat"], dem[k]["ly_do"][:100], flush=True)
            v = dict(dem[k])
            if x["loai"] == "xuyen_khoan":  # đạt = có quan hệ quy tắc–ngoại lệ
                v["co"] = "" if v["dat"] else f"hai gold không phải quan hệ quy tắc–ngoại lệ ({v['ly_do']})"
            else:                           # dat = trả lời được chỉ bằng nguồn → KHÔNG đạt ý đồ dan_chieu
                v["co"] = f"trả lời được chỉ bằng đoạn nguồn ({v['ly_do']})" if v["dat"] else ""
            if v["dat"] is None:
                v["co"] = "giám khảo không trả lời được — xem tay"
            ra[x["qid"]] = v
    finally:
        sinh.xuat_thong_ke_token()
    return ra


def main() -> None:
    argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter).parse_args()
    ds = [json.loads(x) for x in NHAP.read_text().splitlines() if x.strip()]
    kq = kiem_tra(ds)
    bc = kiem_ban_cu(ds)
    nc = kiem_nguon_chua_dap_an(ds)
    for x in ds:
        x["nguon_chua_dap_an"] = nc.get(x["qid"], "")
        if x["qid"] in kq:
            x["kiem_tra"] = kq[x["qid"]]["co"]
        x["ban_cu"] = bc.get(x["qid"], "")
    tam = NHAP.with_suffix(".tmp")
    tam.write_text("\n".join(json.dumps(x, ensure_ascii=False) for x in ds) + "\n")
    tam.replace(NHAP)
    for loai in ("xuyen_khoan", "dan_chieu"):
        v = [kq[x["qid"]] for x in ds if x["loai"] == loai]
        print(f"{loai}: {sum(bool(y['co']) for y in v)}/{len(v)} câu bị gắn cờ")
    print(f"gold ở bản cũ: {len(bc)} câu")
    print(f"dan_chieu, đoạn nguồn một mình chứa đáp án (máy móc): {len(nc)}/{sum(x['loai'] == 'dan_chieu' for x in ds)} câu")


if __name__ == "__main__":
    main()
