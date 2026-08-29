"""
Regenerasi kedua figur makalah dari simulation_results.json.

Tidak menjalankan ulang simulasi apa pun -- hanya membaca hasil yang sudah ada,
jadi selesai dalam hitungan detik.

Pakai:
    python regenerate_figures.py                       # baca ./simulation_results.json
    python regenerate_figures.py path/ke/hasil.json    # atau tentukan sendiri
"""

import json
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# Nama tampilan HARUS sama persis dengan kolom "Scheme" di Tabel 2 naskah.
LABELS = {
    "pairs":        "Pairs",
    "residual":     "Residual",
    "wild":         "Wild (FHH)",
    "wild_nofs":    "Wild (FHH, no correction)",
    "wild_mammen":  "Wild (Mammen)",
    "wild_cluster": "Wild cluster",
    "adaptive":     "Adaptive",
}
MARKERS = {"pairs": "o", "residual": "s", "wild": "^", "wild_nofs": "<",
           "wild_mammen": "v", "wild_cluster": "D", "adaptive": "P"}
ORDER = ["pairs", "residual", "wild", "wild_nofs", "wild_mammen",
         "wild_cluster", "adaptive"]


def scenario_label(key):
    """'n250_tau0.05' -> 'n = 250\\ntau = 0.05' (dua baris, tanpa rotasi)."""
    n, tau = key.split("_tau")
    return f"$n = {n[1:]}$\n$\\tau = {float(tau):g}$"


def plot_var_ratio_vs_coverage(res, methods, path):
    fig, ax = plt.subplots(figsize=(7.5, 5.2))
    for m in methods:
        xs = [v[m]["var_ratio"] for v in res.values() if m in v]
        ys = [v[m]["coverage"] for v in res.values() if m in v]
        if xs:
            ax.scatter(xs, ys, label=LABELS.get(m, m), marker=MARKERS.get(m, "o"),
                       s=70, alpha=0.85, edgecolors="white", linewidths=0.6)
    ax.axhline(0.95, ls="--", c="grey", lw=1)
    ax.axvline(1.0, ls="--", c="grey", lw=1)
    ax.set_xscale("log")
    ax.set_xlabel("bootstrap variance / Monte Carlo variance (log scale)")
    ax.set_ylabel("empirical coverage")
    ax.set_ylim(0, 1.02)
    ax.grid(alpha=0.3, ls="--")
    # Legenda DI LUAR area plot, di bawah, supaya tidak menutupi titik mana pun.
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.16),
              ncol=3, fontsize=9, frameon=False)
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print("tersimpan:", path)


def plot_coverage(res, methods, path):
    keys = list(res.keys())
    fig, ax = plt.subplots(figsize=(10, 5.2))
    x = np.arange(len(keys))
    w = 0.8 / max(len(methods), 1)
    for i, m in enumerate(methods):
        ax.bar(x + i * w, [res[k].get(m, {}).get("coverage", np.nan) for k in keys],
               w, label=LABELS.get(m, m))
    ax.axhline(0.95, ls="--", c="black", lw=1.2)
    ax.set_xticks(x + 0.4 - w / 2)
    ax.set_xticklabels([scenario_label(k) for k in keys])
    ax.set_ylabel("empirical coverage")
    ax.set_ylim(0, 1.02)          # legenda kini di luar, jadi tidak perlu ruang ekstra
    ax.grid(axis="y", alpha=0.3, ls="--")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.10),
              ncol=4, fontsize=9, frameon=False)
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print("tersimpan:", path)


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else "simulation_results.json"
    with open(src) as f:
        res = json.load(f)
    present = [m for m in ORDER if any(m in v for v in res.values())]
    print("skema ditemukan:", ", ".join(LABELS[m] for m in present))
    plot_var_ratio_vs_coverage(res, present, "var_ratio_vs_coverage.png")
    plot_coverage(res, present, "coverage_by_scenario.png")


if __name__ == "__main__":
    main()
