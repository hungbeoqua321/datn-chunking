"""Ba hình cho báo cáo so sánh (results/bao_cao_so_sanh.md) — PNG 150 dpi, số lấy thẳng từ chi_tiet_cau.jsonl.

  1. truy_hoi_bon_pp.png   — Recall@5, Recall@1200 từ, MRR của A, C, D, B (110 câu)
  2. trich_dan_theo_nhom.png — khớp hoàn toàn mức Điều theo năm nhóm, A / C / D / B / E
  3. thanh_phan_E.png      — tập manh_con 35 câu: R@5 và khớp hoàn toàn của B và bảy cấu hình E

Thanh sai số = khoảng tin cậy bootstrap 95% của trung bình (1000 lần, seed 0). Chạy:
    python -m eval.ve_hinh          (đọc KET_QUA_DIR, ghi vào <KET_QUA_DIR>/hinh/)
"""
from __future__ import annotations

import json
import random

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import matplotlib.ticker  # noqa: E402

import cau_hinh as ch  # noqa: E402

MAU = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4"]   # thứ tự cố định, đã qua validate_palette (light)
NEN, CHU, CHU2, LUOI = "#fcfcfb", "#0b0b0b", "#52514e", "#e4e3df"
NHOM = ("don_gian", "dieu_dai", "xuyen_khoan", "khong_co_dieu", "dan_chieu")
E_CAU_HINH = [("B", "B (mốc)"), ("Eduoi", "E đầy đủ (Eduoi)"), ("Etren", "E, câu bản lề lên trên"),
              ("Etat_d", "tắt dẫn Điều"), ("Etat_k", "tắt dẫn khoản"), ("Etat_n", "tắt nhãn mảnh"),
              ("Etat_s", "tắt semantic"), ("Echi_s", "chỉ semantic")]


def _ci(v: list[float], lan: int = 1000) -> tuple[float, float, float]:
    rng, n = random.Random(0), len(v)
    m = sorted(sum(rng.choices(v, k=n)) / n for _ in range(lan))
    return sum(v) / n, m[int(0.025 * lan)], m[int(0.975 * lan) - 1]


def _phong(ax) -> None:
    ax.set_facecolor(NEN)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(LUOI)
    ax.tick_params(colors=CHU2, labelsize=9)
    phay = matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:.1f}".replace(".", ","))
    ax.yaxis.set_major_formatter(phay)
    ax.xaxis.set_major_formatter(phay)
    ax.grid(axis="y", color=LUOI, linewidth=0.8)
    ax.set_axisbelow(True)


def _cot(ax, x, m, lo, hi, mau, rong, doc=False):
    ax.bar(x, m, rong, color=mau, edgecolor=NEN, linewidth=2)
    ax.errorbar(x, m, yerr=[[m - lo], [hi - m]], fmt="none", ecolor=CHU2, elinewidth=1, capsize=3)
    ax.text(x, hi + 0.015, f"{m:.3f}".replace(".", ","), ha="center", va="bottom", fontsize=7 if doc else 8,
            color=CHU, rotation=90 if doc else 0)


def main() -> None:
    ra = ch.RESULTS / "hinh"
    ra.mkdir(parents=True, exist_ok=True)
    rows = [json.loads(l) for l in open(ch.RESULTS / "chi_tiet_cau.jsonl", encoding="utf-8")]
    chinh = {(r["qid"], r["pp"]): r for r in rows if r["bo"] == "chinh"}
    mc = {(r["qid"], r["pp"]): r for r in rows if r["bo"] == "manh_con"}
    cot = lambda d, pp, k, loc=lambda r: True: [r[k] for (q, p), r in sorted(d.items()) if p == pp and loc(r)]  # noqa

    # 1. truy hồi bốn phương pháp — ba chỉ số, mỗi chỉ số một ô (không trộn thang)
    fig, axs = plt.subplots(1, 3, figsize=(10, 3.6), facecolor=NEN, sharey=True)
    for ax, (k, ten) in zip(axs, [("R@5", "Recall@5"), ("R@1200t", "Recall@1200 từ"), ("MRR", "MRR")]):
        _phong(ax)
        for i, pp in enumerate("ACDB"):
            _cot(ax, i, *_ci(cot(chinh, pp, k)), MAU[0] if pp == "B" else "#9fbfe8", 0.62)
        ax.set_xticks(range(4), list("ACDB"))
        ax.set_title(ten, fontsize=10, color=CHU, loc="left")
    axs[0].set_ylim(0, 1.0)
    fig.suptitle("Truy hồi trên 110 câu — A, C, D, B (thanh sai số: CI bootstrap 95%)", fontsize=11, color=CHU,
                 x=0.01, ha="left")
    fig.tight_layout()
    fig.savefig(ra / "truy_hoi_bon_pp.png", dpi=150, facecolor=NEN)
    plt.close(fig)

    # 2. trích dẫn theo nhóm — khớp hoàn toàn mức Điều
    pps = ["A", "C", "D", "B", "E"]
    fig, ax = plt.subplots(figsize=(12, 4.6), facecolor=NEN)
    _phong(ax)
    rong = 0.16
    for j, pp in enumerate(pps):
        for i, g in enumerate(NHOM):
            m, lo, hi = _ci(cot(chinh, pp, "dieu_toan_phan", lambda r, g=g: r["loai"] == g))
            _cot(ax, i + (j - 2) * rong, m, lo, hi, MAU[j], rong, doc=True)
    n = {g: sum(1 for (q, p), r in chinh.items() if p == "A" and r["loai"] == g) for g in NHOM}
    ax.set_xticks(range(len(NHOM)), [f"{g}\n(n={n[g]})" for g in NHOM])
    ax.set_ylim(0, 1.12)
    ax.set_ylabel("khớp hoàn toàn (Điều)", color=CHU2, fontsize=9)
    ax.legend([plt.Rectangle((0, 0), 1, 1, color=c) for c in MAU], pps, frameon=False, ncol=5, fontsize=9,
              loc="upper right", labelcolor=CHU)
    ax.set_title("Trích dẫn theo nhóm câu hỏi — khớp hoàn toàn mức Điều (CI bootstrap 95%)", fontsize=11,
                 color=CHU, loc="left")
    fig.tight_layout()
    fig.savefig(ra / "trich_dan_theo_nhom.png", dpi=150, facecolor=NEN)
    plt.close(fig)

    # 3. thành phần E trên manh_con — hai ô: R@5 và khớp hoàn toàn
    fig, axs = plt.subplots(1, 2, figsize=(11, 4.4), facecolor=NEN, sharey=True)
    for ax, (k, ten) in zip(axs, [("R@5", "Recall@5"), ("dieu_toan_phan", "khớp hoàn toàn (Điều)")]):
        _phong(ax)
        ax.grid(axis="y", visible=False)
        ax.grid(axis="x", color=LUOI, linewidth=0.8)
        for i, (pp, _) in enumerate(E_CAU_HINH):
            m, lo, hi = _ci(cot(mc, pp, k))
            y = len(E_CAU_HINH) - 1 - i
            ax.barh(y, m, 0.6, color=MAU[0] if pp == "B" else MAU[1], edgecolor=NEN, linewidth=2)
            ax.errorbar(m, y, xerr=[[m - lo], [hi - m]], fmt="none", ecolor=CHU2, elinewidth=1, capsize=3)
            ax.text(hi + 0.02, y, f"{m:.3f}".replace(".", ","), va="center", fontsize=8, color=CHU)
        ax.set_xlim(0, 1.05)
        ax.set_title(ten, fontsize=10, color=CHU, loc="left")
    axs[0].set_yticks(range(len(E_CAU_HINH)), [t for _, t in reversed(E_CAU_HINH)])
    fig.suptitle("Thành phần của E trên tập manh_con (35 câu) — so với B (CI bootstrap 95%)", fontsize=11,
                 color=CHU, x=0.01, ha="left")
    fig.tight_layout()
    fig.savefig(ra / "thanh_phan_E.png", dpi=150, facecolor=NEN)
    plt.close(fig)
    print(f"đã ghi 3 hình vào {ra}")


if __name__ == "__main__":
    main()
