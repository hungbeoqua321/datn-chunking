"""Chốt chặn chỉ mục — phải DỪNG khi chỉ mục lệch tệp chunk.

Lỗi thật đã xảy ra: sau khi sửa cài đặt C và D, tệp chunk đổi nhưng `rag.chi_muc` bỏ qua vì chỉ mục
đã tồn tại, mà lệnh vẫn báo thành công. Suýt nữa pilot chấm C và D trên đúng bản lỗi vừa sửa.
"""
import json

import numpy as np
import pytest

import cau_hinh as ch
from rag import chi_muc, kiem_chi_muc
from rag.kiem_chi_muc import DIM, chot_chan, kiem


def _dung_kho(tmp_path, monkeypatch, cs_chunk, cs_index=None, n_vector=None):
    """Dựng một kho giả: data/chunks/T.jsonl + data/index/T/{chunks.jsonl,emb.f32}."""
    chunks, index = tmp_path / "chunks", tmp_path / "index"
    chunks.mkdir(); (index / "T").mkdir(parents=True)
    monkeypatch.setattr(ch, "CHUNKS", chunks)
    monkeypatch.setattr(ch, "INDEX", index)
    (chunks / "T.jsonl").write_text("".join(json.dumps(c, ensure_ascii=False) + "\n" for c in cs_chunk))
    ci = cs_chunk if cs_index is None else cs_index
    (index / "T" / "chunks.jsonl").write_text("".join(json.dumps(c, ensure_ascii=False) + "\n" for c in ci))
    n = len(ci) if n_vector is None else n_vector
    np.zeros((n, DIM), dtype=np.float32).tofile(index / "T" / "emb.f32")


def _cs(n, dau="nội dung"):
    return [{"chunk_id": f"T:{i}", "text": f"{dau} {i}"} for i in range(n)]


def test_khop_thi_khong_bao_loi(tmp_path, monkeypatch):
    _dung_kho(tmp_path, monkeypatch, _cs(5))
    assert kiem() == []
    chot_chan()          # không được ném


def test_bat_lech_so_chunk(tmp_path, monkeypatch):
    _dung_kho(tmp_path, monkeypatch, _cs(6), cs_index=_cs(5), n_vector=5)
    loi = kiem()
    assert len(loi) == 1 and "LỆCH SỐ CHUNK" in loi[0] and "--force" in loi[0]
    with pytest.raises(SystemExit):
        chot_chan()


def test_bat_lech_noi_dung_du_SO_DONG_BANG_NHAU(tmp_path, monkeypatch):
    """Ca quan trọng nhất: dựng lại chunk làm đổi nội dung mà số dòng không đổi —
    đếm dòng một mình sẽ LỌT, nên chốt chặn phải so vân nội dung."""
    _dung_kho(tmp_path, monkeypatch, _cs(5, "đã dựng lại"), cs_index=_cs(5, "bản cũ"))
    loi = kiem()
    assert len(loi) == 1 and "LỆCH NỘI DUNG" in loi[0]
    with pytest.raises(SystemExit):
        chot_chan()


def test_bat_lech_ma_tran_vector(tmp_path, monkeypatch):
    _dung_kho(tmp_path, monkeypatch, _cs(5), n_vector=4)
    loi = kiem()
    assert len(loi) == 1 and "LỆCH MA TRẬN VECTOR" in loi[0]


def test_bat_chua_nhung(tmp_path, monkeypatch):
    chunks, index = tmp_path / "chunks", tmp_path / "index"
    chunks.mkdir(); index.mkdir()
    monkeypatch.setattr(ch, "CHUNKS", chunks); monkeypatch.setattr(ch, "INDEX", index)
    (chunks / "T.jsonl").write_text(json.dumps({"chunk_id": "T:0", "text": "x"}) + "\n")
    loi = kiem()
    assert len(loi) == 1 and "CHƯA NHÚNG" in loi[0]


def test_bo_qua_tep_co_y_khong_nhung(tmp_path, monkeypatch):
    """B_s1..3 cố ý không nhúng → không bị báo lỗi, nhưng nêu đích danh thì vẫn kiểm."""
    chunks, index = tmp_path / "chunks", tmp_path / "index"
    chunks.mkdir(); index.mkdir()
    monkeypatch.setattr(ch, "CHUNKS", chunks); monkeypatch.setattr(ch, "INDEX", index)
    (chunks / "B_s1.jsonl").write_text(json.dumps({"chunk_id": "b", "text": "x"}) + "\n")
    assert kiem() == []                       # quét toàn bộ: bỏ qua
    assert "CHƯA NHÚNG" in kiem(["B_s1"])[0]  # nêu đích danh: vẫn kiểm


def test_chi_muc_bo_qua_tra_ve_False_va_in_BO_QUA(tmp_path, monkeypatch, capsys):
    """Thiếu --force thì phải nói rõ BỎ QUA và báo cho bên gọi biết, không im lặng."""
    _dung_kho(tmp_path, monkeypatch, _cs(3))
    assert chi_muc.dung("T", force=False) is False
    ra = capsys.readouterr().out
    assert "BỎ QUA" in ra and "--force" in ra and "XONG" not in ra


@pytest.mark.parametrize("vi_tri", [1, 2, 3, 7])
def test_bat_mot_chunk_o_QUANG_GIUA_doi_noi_dung(tmp_path, monkeypatch, vi_tri):
    """Chỉ MỘT chunk đổi nội dung, không nằm ở đầu / chính giữa / cuối.

    Băm ba điểm (đầu, giữa, cuối) sẽ LỌT ca này — đó là lý do vân nội dung băm toàn bộ chuỗi chunk
    theo thứ tự. Số dòng không đổi nên lớp đếm dòng cũng không bắt được.
    """
    goc = _cs(9)
    doi = [dict(c) for c in goc]
    doi[vi_tri]["text"] = "nội dung ĐÃ ĐỔI"
    _dung_kho(tmp_path, monkeypatch, doi, cs_index=goc)
    loi = kiem()
    assert len(loi) == 1 and "LỆCH NỘI DUNG" in loi[0], f"không bắt được chunk thứ {vi_tri}"
    with pytest.raises(SystemExit):
        chot_chan()


def test_bat_dao_cho_hai_chunk(tmp_path, monkeypatch):
    """Đảo thứ tự hai chunk: số dòng và tập nội dung y hệt, chỉ thứ tự khác — vẫn phải bắt,
    vì ma trận vector xếp theo đúng thứ tự dòng."""
    goc = _cs(9)
    doi = list(goc); doi[3], doi[5] = doi[5], doi[3]
    _dung_kho(tmp_path, monkeypatch, doi, cs_index=goc)
    loi = kiem()
    assert len(loi) == 1 and "LỆCH NỘI DUNG" in loi[0]
