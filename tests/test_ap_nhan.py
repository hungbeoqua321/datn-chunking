"""Ghép nhãn tay — ca mã sai, nhãn sai, và ghép hai lần không nhân đôi."""
import pytest

from eval import ap_nhan, pilot

KHOI = """## 007

| | |
|---|---|
| mã dòng | `007` |
| qid | `q001` |
| gold | X |

**Câu trả lời nguyên văn:**

> abc

| Trích dẫn người đọc thấy | regex |
|---|---|
|  |  |

---
"""


@pytest.fixture
def md(tmp_path, monkeypatch):
    p = tmp_path / "nhan.md"
    p.write_text(KHOI)
    monkeypatch.setattr(pilot, "NHAN", p)
    return p


def _tep(tmp_path, noi_dung):
    p = tmp_path / "nhan.txt"
    p.write_text(noi_dung)
    return p


def test_ma_khong_ton_tai_thi_KHONG_ghi_gi(md, tmp_path):
    nhan, loi = ap_nhan.doc_nhan(_tep(tmp_path, "999 | 1/2020/NĐ-CP Điều 1 | Đúng\n"))
    assert loi == []
    truoc = md.read_text()
    loi = ap_nhan.ghep(nhan)
    assert loi and "999" in loi[0]
    assert md.read_text() == truoc, "mã sai mà vẫn ghi vào tệp"


@pytest.mark.parametrize("nhan_xau", ["đúng", "OK", "Dung", "Thieu", ""])
def test_nhan_ngoai_bon_gia_tri_bi_tu_choi(tmp_path, nhan_xau):
    _, loi = ap_nhan.doc_nhan(_tep(tmp_path, f"007 | x | {nhan_xau}\n"))
    assert len(loi) == 1 and "không thuộc" in loi[0]


def test_sai_so_phan_va_ma_khong_phai_so(tmp_path):
    _, loi = ap_nhan.doc_nhan(_tep(tmp_path, "007 | thiếu cột\nabc | x | Đúng\n"))
    assert len(loi) == 2
    assert "3 phần" in loi[0] and "không phải số" in loi[1]


def test_ma_lap_trong_chinh_tep(tmp_path):
    _, loi = ap_nhan.doc_nhan(_tep(tmp_path, "007 | a | Đúng\n7 | b | Sai\n"))
    assert len(loi) == 1 and "lặp" in loi[0]


def test_ghep_hai_lan_khong_nhan_doi(md, tmp_path):
    nhan, _ = ap_nhan.doc_nhan(_tep(tmp_path, "007 | 1/2020/NĐ-CP Điều 1 | Đúng\n"))
    assert ap_nhan.ghep(nhan) == []
    mot = md.read_text()
    assert ap_nhan.ghep(nhan) == []
    assert md.read_text() == mot, "ghép lần hai làm đổi tệp"
    assert mot.count("1/2020/NĐ-CP Điều 1") == 1
    assert mot.count("| Trích dẫn người đọc thấy | regex |") == 1


def test_ghep_lai_nhan_khac_thi_GHI_DE_chu_khong_them_hang(md, tmp_path):
    ap_nhan.ghep(ap_nhan.doc_nhan(_tep(tmp_path, "007 | a | Đúng\n"))[0])
    ap_nhan.ghep(ap_nhan.doc_nhan(_tep(tmp_path, "007 | b | Sai\n"))[0])
    t = md.read_text()
    assert "| b | Sai |" in t and "| a | Đúng |" not in t
    assert t.count("---|---") == 2      # 1 bảng đầu khối + 1 bảng nhãn, không sinh thêm


def test_doc_lai_duoc_nhan_da_ghep(md, tmp_path):
    ap_nhan.ghep(ap_nhan.doc_nhan(_tep(tmp_path, "007 | a; b | Thiếu\n"))[0])
    assert ap_nhan.doc_da_ghep() == {"007": ("a; b", "Thiếu")}


@pytest.mark.parametrize("k, n, p", [(86, 120, 0.717), (40, 40, 1.0), (0, 40, 0.0)])
def test_wilson(k, n, p):
    ti, lo, hi = ap_nhan.wilson(k, n)
    assert abs(ti - p) < 1e-3
    assert 0.0 <= lo <= ti <= hi <= 1.0
    if 0 < k < n:
        assert lo > 0 and hi < 1
