"""Ghi lại môi trường chạy thực nghiệm vào results/buoc1/moi_truong.md (để báo cáo trích dẫn).

    python tools/ghi_moi_truong.py
"""
import argparse
import importlib.metadata as md
import platform
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import cau_hinh as ch  # noqa: E402
from tools.tai_mo_hinh import NHUNG, SINH  # noqa: E402

GOI = ["torch", "sentence-transformers", "transformers", "huggingface_hub", "numpy", "pandas", "matplotlib",
       "pyarrow", "requests", "beautifulsoup4", "lxml", "openai", "fastapi", "uvicorn", "markdown-it-py", "pytest"]


def chay(lenh: str) -> str:
    try:
        return subprocess.run(lenh, shell=True, capture_output=True, text=True, timeout=30).stdout.strip()
    except Exception as e:  # noqa: BLE001
        return f"(lỗi: {e})"


def co_llama() -> str:
    """Các cờ trong tools/chay-llm.sh (phần sau tên chương trình), gộp thành một dòng."""
    s = (ch.GOC / "tools/chay-llm.sh").read_text().split('llama-server"', 1)[1]
    return " ".join(s.replace("\\\n", " ").split())


def main() -> None:
    argparse.ArgumentParser(description=__doc__).parse_args()
    llama = ch.GOC / "tools/llama.cpp"
    d = ["# Môi trường chạy thực nghiệm", "",
         f"- Máy: `{platform.machine()}`, CPU `{chay('lscpu | grep \"Model name\" | cut -d: -f2 | xargs')}`, "
         f"{chay('nproc')} nhân, RAM {chay('free -g | awk \"/Mem/ {print \\$2}\"')} GB, không GPU",
         f"- Hệ điều hành: {chay('. /etc/os-release; echo $PRETTY_NAME')}, glibc {platform.libc_ver()[1]}",
         f"- Python {platform.python_version()}", "",
         "## Thư viện", "", "| Gói | Phiên bản |", "|---|---|"]
    d += [f"| {g} | {md.version(g)} |" for g in GOI]
    d += ["", "## Mô hình", "",
          f"- Nhúng: `{NHUNG['repo']}` @ `{NHUNG['revision']}` (trước đây `hiieu/halong_embedding`); "
          f"model.safetensors sha256 `{NHUNG['sha256']['model.safetensors']}`",
          f"- Sinh: `{SINH['repo']}` @ `{SINH['revision']}`"]
    d += [f"  - `{t}` sha256 `{h}`" for t, h in SINH["tep"].items()]
    d += [f"- llama.cpp: tag `b11577`, commit `{chay(f'git -C {llama} rev-parse HEAD')}`, "
          "build `-DGGML_NATIVE=ON` (tools/build-llama.sh)",
          f"- Cờ llama-server: `{co_llama()}`"]
    p = ch.RESULTS / "buoc1/moi_truong.md"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("\n".join(d) + "\n")
    print("→", p)


if __name__ == "__main__":
    main()
