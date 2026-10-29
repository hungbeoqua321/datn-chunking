"""Bước xuất file gán nhãn của pilot — hai lỗi đã làm hỏng lần chạy 21/10.

Cả hai chỉ lộ ra SAU khi sinh xong 240 câu trả lời (6h16m), vì `--xuat` chạy cuối cùng.
Test ở đây để lần sau hỏng là hỏng trong một phần nghìn giây.
"""
import pytest

from eval.pilot import SO_CAU_PILOT, TANG, _chia_tang, _hien_so_hieu, _nhan_trich


@pytest.mark.parametrize("khoa, mong", [
    (frozenset({"34", "2024", "QH15"}), "34/2024/QH15"),
    (frozenset({"254", "2026", "NĐ-CP"}), "254/2026/NĐ-CP"),
    (frozenset({"83", "2026", "VBHN-TT-BXD"}), "83/2026/VBHN-TT-BXD"),
    (frozenset({"21", "VBHN-BTC"}), "21/VBHN-BTC"),      # số hiệu không có năm
    (frozenset({"2004", "QH11"}), "2004/QH11"),          # số trông như năm, không có số riêng
    (None, "?"),
])
def test_dung_lai_so_hieu_tu_khoa_frozenset(khoa, mong):
    """Khoá số hiệu là frozenset dùng để SO KHỚP; in thẳng ra sẽ nổ TypeError.

    Đúng lỗi đã xảy ra: `" ".join([sh, ...])` với sh là frozenset →
    "sequence item 0: expected str instance, frozenset found".
    """
    assert _hien_so_hieu(khoa) == mong


def test_nhap_nhang_thi_in_nguyen_chu_khong_doan():
    """Hai mẩu số cùng trông như năm → không có cách nào biết đâu là số, đâu là năm.
    Thà in khó đọc còn hơn hiện sai số hiệu cho người gán nhãn."""
    ra = _hien_so_hieu(frozenset({"2015", "2019", "QH13"}))
    assert "·" in ra and all(x in ra for x in ("2015", "2019", "QH13"))


def test_nhan_trich_ghep_du_bon_cap():
    assert _nhan_trich((frozenset({"100", "2015", "QH13"}), 14, 5, "a")) \
        == "100/2015/QH13 Điều 14 khoản 5 điểm a"
    assert _nhan_trich((frozenset({"100", "2015", "QH13"}), None, None, None)) == "100/2015/QH13"


@pytest.mark.parametrize("tong", [30, 40, 60, 80])
def test_chia_tang_cong_lai_DUNG_bang_tong(tong):
    """Làm tròn từng tầng rồi cộng lại cho ra 41 chứ không phải 40 — file gán nhãn
    thừa 3 dòng so với bản đặc tả. Phép chia lớn nhất phần dư không bao giờ lệch."""
    ra = _chia_tang(tong)
    assert sum(ra.values()) == tong
    assert set(ra) == set(TANG)


def test_chia_tang_giu_dung_thu_tu_lon_nho():
    ra = _chia_tang(40)
    assert ra == {"don_gian": 18, "dieu_dai": 7, "xuyen_khoan": 6, "khong_co_dieu": 6, "dan_chieu": 3}
    # tầng đông hơn không bao giờ được ít dòng hơn tầng thưa hơn
    for a in TANG:
        for b in TANG:
            if TANG[a] > TANG[b]:
                assert ra[a] >= ra[b], (a, b, ra)


def test_chia_tang_tat_dinh():
    assert _chia_tang(40) == _chia_tang(40)


def test_chia_het_thi_dung_y_nguyen_ti_le():
    assert _chia_tang(SO_CAU_PILOT) == dict(TANG)


def test_ca_cat_tran_khong_vao_mau_gan_nhan(tmp_path, monkeypatch):
    """Câu trả lời rỗng thì không có trích dẫn nào để đối chiếu với regex — đưa vào chỉ tổ
    chiếm chỗ. Loại khỏi MẪU GÁN NHÃN không phải loại khỏi bảng kết quả (xem eval/ket_qua.py).

    Lỗi thật: sau khi bước 1 chạy xong, `--xuat` chạy lại và kéo 3 dòng q021 rỗng vào file.
    """
    import json

    import cau_hinh as ch
    from eval import pilot

    tl = tmp_path / "tl.jsonl"
    rows = [{"qid": f"q{i:03d}", "pp": pp, "loai": "don_gian", "trung_lap": False,
             "question": "x", "gold": [{"so_hieu": "1/2020/NĐ-CP", "dieu": 1}],
             "tra_loi": "" if i == 1 else f"Theo Điều {i} của 1/2020/NĐ-CP.",
             "cat_tran": i == 1}
            for i in range(1, 40) for pp in ch.PP_SINH]
    tl.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
    monkeypatch.setattr(pilot, "TRA_LOI", tl)
    monkeypatch.setattr(pilot, "NHAN", tmp_path / "nhan.md")
    monkeypatch.setattr(pilot, "GIAI_MA", tmp_path / "gm.json")
    pilot.xuat_nhan()
    ra = (tmp_path / "nhan.md").read_text()
    assert "`q001`" not in ra, "dòng cắt trần lọt vào mẫu gán nhãn"
