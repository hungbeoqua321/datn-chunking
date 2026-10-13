"""Test các phép chấm trên dữ liệu giả có đáp án biết trước."""
from eval.cham import (bootstrap_hieu, cat_theo_tu, do_phu, du_trong_mot_chunk, giao, holm, mcnemar, mrr, recall_k,
                       tim_tuong_duong)

G = {"doc_id": "d", "start": 100, "end": 200}


def c(a, b, doc="d", n=None):
    return {"doc_id": doc, "start": a, "end": b, "n_words": n or (b - a) // 5}


def test_giao_chong_nhau():
    assert giao(100, 200, [(50, 120), (110, 150), (190, 300)]) == 60


def test_do_phu_va_recall():
    assert do_phu(G, [c(0, 150)]) == 0.5
    assert do_phu(G, [c(150, 400), c(0, 120)]) == 0.7
    assert do_phu(G, [c(100, 200, doc="khac")]) == 0
    kq = [c(500, 600), c(0, 140), c(140, 300)]
    assert recall_k([G], kq, 1) == 0 and recall_k([G], kq, 2) == 0 and recall_k([G], kq, 3) == 1
    assert mrr([G], kq) == 1 / 3


def test_nhieu_don_vi_du_ca():
    g2 = {"doc_id": "d", "start": 300, "end": 350}
    kq = [c(90, 210), c(1000, 1100), c(290, 360)]
    assert recall_k([G, g2], kq, 2) == 0 and recall_k([G, g2], kq, 2, chi_so=True) == 0.5
    assert recall_k([G, g2], kq, 3) == 1 and mrr([G, g2], kq) == 1 / 3
    assert du_trong_mot_chunk([G, g2], kq, 3) == 0 and du_trong_mot_chunk([G, g2], [c(0, 400)], 1) == 1


def test_tuong_duong_va_tim():
    td = {0: [{"doc_id": "vbhn", "start": 10, "end": 110}]}
    assert recall_k([G], [c(0, 120, doc="vbhn")], 1, td=td) == 1
    van_ban = {"goc": "Điều 5. Mức phạt\n1. Phạt tiền từ 1.000.000 đồng đến 2.000.000 đồng đối với hành vi vi phạm quy định.",
               "vbhn": "Điều 5. Mức phạt[3]\n1. Phạt tiền từ 1.000.000 đồng đến 2.000.000 đồng đối với hành vi vi phạm quy định."}
    g = {"doc_id": "goc", "start": 17, "end": len(van_ban["goc"])}
    r = tim_tuong_duong(g, van_ban)
    assert r and r[0]["doc_id"] == "vbhn" and van_ban["vbhn"][r[0]["start"]:r[0]["end"]].startswith("1. Phạt tiền")


def test_recall_theo_ngan_sach_tu():
    kq = [c(0, 50, n=200), c(100, 200, n=200), c(300, 310, n=10)]
    assert len(cat_theo_tu(kq, 300)) == 1                # chunk thứ 2 không vừa → dừng, không cắt dở
    assert len(cat_theo_tu(kq, 410)) == 3 and do_phu(G, cat_theo_tu(kq, 400)) == 1.0


def test_bootstrap_va_kiem_dinh():
    a = [0.0] * 50 + [1.0] * 50
    b = [1.0] * 100
    h, lo, hi = bootstrap_hieu(a, b, nhom=["x"] * 100)
    assert h == 0.5 and lo > 0.3 and hi < 0.7
    h, lo, hi = bootstrap_hieu([1.0, 0.0] * 50, [0.0, 1.0] * 50)
    assert h == 0 and lo < 0 < hi
    assert mcnemar(a, b) < 1e-10 and mcnemar(a, a) == 1.0
    assert holm({"x": 0.01, "y": 0.04, "z": 0.03}) == {"x": 0.03, "z": 0.06, "y": 0.06}
