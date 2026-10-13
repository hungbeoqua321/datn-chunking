"""Đo tốc độ nhúng của halong_embedding trên CPU (3 luồng) với các đoạn ~300 từ thật (Bộ luật Lao động).

    python tools/do_toc_do_nhung.py
"""
import argparse, html as H, re, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bs4 import BeautifulSoup
import cau_hinh as ch
from rag import nhung

argparse.ArgumentParser(description=__doc__).parse_args()
s = BeautifulSoup(Path("/home/ubuntu/.claude/jobs/1409c164/tmp/blld.html").read_text(), "lxml")
for t in s(["style", "script"]): t.decompose()
tu = H.unescape(s.get_text(" ")).split()
doan = [" ".join(tu[i:i + 300]) for i in range(0, len(tu) - 300, 300)][:96]
m = nhung.nap(so_luong=3)
tok = [len(m.tokenizer(d)["input_ids"]) for d in doan]
nhung.nhung(doan[:8])  # làm nóng
t0 = time.monotonic(); nhung.nhung(doan); dt = time.monotonic() - t0
dong = ["# Tốc độ nhúng (halong_embedding, CPU 3 luồng, batch 16)", "",
        f"- {len(doan)} đoạn × 300 từ (Bộ luật Lao động), trung bình {sum(tok)/len(tok):.0f} token/đoạn "
        f"(min {min(tok)}, max {max(tok)}); {sum(t > 512 for t in tok)}/{len(tok)} đoạn vượt 512 token",
        f"- {dt:.1f} giây ⇒ **{len(doan)/dt:.2f} đoạn/giây**, {sum(min(t,512) for t in tok)/dt:.0f} token/giây"]
(ch.RESULTS / "buoc1/toc_do_nhung.md").write_text("\n".join(dong) + "\n")
print("\n".join(dong))
