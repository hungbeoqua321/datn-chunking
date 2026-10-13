"""Bộ chặn cắt dữ liệu khi gọi mô hình sinh: mọi dấu hiệu bị cắt phải DỪNG (LoiCat), không lặng lẽ trả lời."""
import json
from types import SimpleNamespace as NS

import pytest

from rag import sinh, truy_hoi


class ClientGia:
    def __init__(self, *ket):
        self.ket, self.lan = list(ket), 0
        self.chat = NS(completions=NS(create=self.create))

    def create(self, **kw):
        p, c, ly_do = self.ket[min(self.lan, len(self.ket) - 1)]
        self.lan += 1
        u = NS(prompt_tokens=p, completion_tokens=c, model_dump=lambda: {"prompt_tokens": p, "completion_tokens": c})
        return NS(usage=u, choices=[NS(finish_reason=ly_do, message=NS(content="Điều 1 của 1/2020/QH14"))])


@pytest.fixture(autouse=True)
def gia_lap(monkeypatch, tmp_path):
    monkeypatch.setenv("LLM_MODEL", "gia")
    monkeypatch.setattr(sinh, "dem_token", lambda s, base=None: 100)  # system + user = 200 token nội dung
    monkeypatch.setattr(sinh, "n_ctx", lambda: 1000)
    monkeypatch.setattr(sinh, "NHAT_KY", tmp_path / "nhat_ky.jsonl")
    monkeypatch.setattr(sinh, "THONG_KE_TOKEN", tmp_path / "thong_ke_token.md")


KHOI = [{"so_hieu": "1/2020/QH14", "text": "Điều 1. Nội dung."}]


def test_binh_thuong_ghi_nhat_ky():
    r = sinh.tra_loi("hỏi?", KHOI, ClientGia((230, 50, "stop")), nhan={"qid": "q1", "bien_the": "A", "seed": 0})
    assert r["usage"]["prompt_tokens"] == 230 and r["n_ctx"] == 1000
    d = json.loads(sinh.NHAT_KY.read_text())
    assert {k: d[k] for k in ("qid", "bien_the", "seed", "token_prompt", "token_tra_loi", "n_ctx", "ly_do_dung",
                              "so_khoi", "so_tu_ngu_canh")} == \
        {"qid": "q1", "bien_the": "A", "seed": 0, "token_prompt": 230, "token_tra_loi": 50, "n_ctx": 1000,
         "ly_do_dung": "stop", "so_khoi": 1, "so_tu_ngu_canh": 4}
    assert isinstance(d["thoi_gian_giay"], float)


def test_server_cat_prompt_thi_dung():
    with pytest.raises(sinh.LoiCat, match="prompt bị cắt"):
        sinh.tra_loi("hỏi?", KHOI, ClientGia((150, 50, "stop")))


def test_cham_n_ctx_thi_dung():
    with pytest.raises(sinh.LoiCat, match="n_ctx"):
        sinh.tra_loi("hỏi?", KHOI, ClientGia((900, 100, "stop")))


def test_vuot_truoc_khi_goi_thi_dung(monkeypatch):
    monkeypatch.setattr(sinh, "n_ctx", lambda: 500)  # 200 nội dung + 384 trả lời > 500
    with pytest.raises(sinh.LoiCat, match="sẽ bị cắt"):
        sinh.tra_loi("hỏi?", KHOI, ClientGia((230, 50, "stop")))


def test_tra_loi_bi_cat_thi_dung_ngay_khong_thu_lai(monkeypatch):
    monkeypatch.setattr(sinh, "n_ctx", lambda: 4096)
    cl = ClientGia((230, 384, "length"), (230, 50, "stop"))
    with pytest.raises(sinh.LoiCat, match="hết max_tokens"):
        sinh.tra_loi("hỏi?", KHOI, cl, nhan={"qid": "q2", "bien_the": "B", "seed": 0})
    assert cl.lan == 1  # không gọi lại lần thứ hai
    tk = sinh.THONG_KE_TOKEN.read_text()  # thống kê token được xuất cả khi job bị dừng
    assert "| B | 1 | 230 | 230 | 614 | 4096 | 3482 | 0 | 1 |" in tk


def test_ngu_canh_chi_lay_chunk_nguyen():
    def c(i, n, dieu=None):
        return ({"chunk_id": f"c{i}", "so_hieu": "x", "text": " ".join(["t"] * n), "start": i * 10, "end": i * 10 + 5,
                 "doc_id": "d", "tien_to": "", "dieu_start": dieu, "dieu_end": None}, 1.0)
    kq = [c(0, 300), c(1, 300), c(2, 300), c(3, 300), c(4, 300)]
    k = truy_hoi.ngu_canh("A", kq, ngan_sach=1200)
    assert len(k) == 4 and sum(x["so_tu"] for x in k) == 1200 and not any(x["bi_cat"] for x in k)
    k = truy_hoi.ngu_canh("A", kq, ngan_sach=1000)
    assert len(k) == 3  # chunk thứ 4 không vừa → dừng, không cắt dở
