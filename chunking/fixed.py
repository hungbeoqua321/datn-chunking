"""Phương pháp A — phân đoạn theo kích thước cố định (baseline) và biến thể A+.

A : cửa sổ 300 từ, không chồng lấn; không nhìn nội dung, không nhìn cấu trúc; dieu_so/khoan_so để trống.
A+: A + tiền tố "[Số hiệu] [Trích yếu]" (đối chứng: tách phần lợi do tiêu đề văn bản khỏi phần lợi do cắt theo
    cấu trúc). Ranh giới giống hệt A.

Lý do 300 từ, không chồng lấn: các khảo sát thực nghiệm về chunking cho thấy đoạn 200–400 token không chồng lấn
ổn định hơn đoạn lớn kèm chồng lấn dày → baseline công bằng, không phải baseline dựng lên cho dễ thắng.
(300 từ tiếng Việt ≈ 350 token của halong_embedding — đo ở bước 1.)
"""
import cau_hinh as ch
from chunking.base import Chunk, Document, cua_so, do_lech, tien_to_van_ban


def chunk(doc: Document, seed: int = 0, co_tien_to: bool = False) -> list[Chunk]:
    ten = "A+" if co_tien_to else "A"
    tt = tien_to_van_ban(doc) if co_tien_to else ""
    ra = []
    for k, (a, b, n) in enumerate(cua_so(doc.text, 0, len(doc.text), ch.CUA_SO, do_lech(seed, doc.doc_id))):
        body = doc.text[a:b]
        ra.append(Chunk(chunk_id=f"{ten}:{seed}:{doc.doc_id}:{k}", text=(tt + "\n" + body) if tt else body,
                        doc_id=doc.doc_id, so_hieu=doc.so_hieu, chuong=None, muc=None, dieu_so=None, dieu_ten=None,
                        khoan_so=None, diem=None, n_words=n, method=ten, start=a, end=b, tien_to=tt, seed=seed))
    return ra


def chunk_a_cong(doc: Document, seed: int = 0) -> list[Chunk]:
    return chunk(doc, seed, co_tien_to=True)
