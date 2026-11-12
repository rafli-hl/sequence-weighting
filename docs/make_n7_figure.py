"""Draw the README's N7 figure from the published per-readout table, and check it against the sealed analysis.

    python docs/make_n7_figure.py      # from the repository root; needs matplotlib

It overwrites docs/n7_result.png. The image's bytes depend on the Matplotlib version (3.11.2 for the published file),
so a regenerated file can differ from the hash in PUBLICATION_MANIFEST.csv while showing the same figure.

For each draw and learning rate, p*(512) - p*(768) after three epochs is shown at equal updates and at equal
training loss (768 read along its own readouts at 512's epoch-3 training loss, the registered interpolation rule).
Lines join the two readings of the same draw.
"""
import csv, json, math, statistics as st
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
N7 = ROOT / "reports/natural-text-matched-analysis-20261105-01"
P = {}
for r in csv.DictReader(open(N7 / "POINTS.csv", encoding="utf-8")):
    P[(r["draw"], float(r["epoch"]), int(r["width"]), r["tag"])] = {k: float(r[k]) for k in ("p", "train")}
A = json.load(open(N7 / "ANALYSIS.json", encoding="utf-8"))["statistics"]
DRAWS = sorted({k[0] for k in P}); PATH = [e for e in sorted({k[1] for k in P}) if 2.0 <= e <= 3.5]


def equal_loss(d, rate):
    tgt = P[(d, 3.0, 512, rate)]["train"]
    pts = [(P[(d, e, 768, rate)]["train"], P[(d, e, 768, rate)]["p"]) for e in PATH]
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        if min(x0, x1) <= tgt <= max(x0, x1):
            return P[(d, 3.0, 512, rate)]["p"] - (y0 + (tgt - x0) / (x1 - x0) * (y1 - y0))


def equal_updates(d, rate):
    return P[(d, 3.0, 512, rate)]["p"] - P[(d, 3.0, 768, rate)]["p"]


DATA = {rate: ([equal_updates(d, rate) for d in DRAWS], [equal_loss(d, rate) for d in DRAWS]) for rate in ("lr1e-04", "lr3e-04")}
for rate, (upd, loss), (ku, kl) in zip(DATA, DATA.values(), (("S3", "P1"), ("S5", "S4"))):
    assert abs(st.mean(upd) - A[ku]["interval"]["mean"]) < 1e-12 and abs(st.mean(loss) - A[kl]["interval"]["mean"]) < 1e-12

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.facecolor": "#fafafa", "axes.edgecolor": "#555555", "axes.grid": True, "grid.color": "#e2e2e2",
                     "axes.axisbelow": True, "xtick.color": "#555555", "ytick.color": "#555555"})
fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.0), sharey=True)
for ax, (rate, (upd, loss)), title in zip(axes, DATA.items(), ("Learning rate 1e-4", "Learning rate 3e-4")):
    for u, l in zip(upd, loss):
        ax.plot([0, 1], [u, l], color="#9a9a9a", lw=0.8, zorder=2)
    ax.scatter([0] * 6, upd, s=22, color="#e5592f", zorder=3)
    ax.scatter([1] * 6, loss, s=22, color="#3a6fde", zorder=3)
    for x, v in ((0, upd), (1, loss)):
        m = st.mean(v); h = 2.570581836 * st.stdev(v) / math.sqrt(len(v))
        ax.errorbar(x + 0.12, m, yerr=h, fmt="o", ms=4, color="#222222", capsize=3, lw=1, zorder=4)
    ax.axhline(0, color="#555555", lw=0.8)
    ax.set_xticks([0, 1]); ax.set_xticklabels(["Equal updates", "Equal training loss"])
    ax.set_xlim(-0.4, 1.5); ax.set_title(title); ax.grid(axis="x", visible=False)
axes[0].set_ylabel("p*(512) − p*(768)")
fig.text(0.5, -0.02, "Dots: six draws, joined by draw. Black: mean and 95% t interval (df 5).", ha="center",
         fontsize=8, color="#555555")
fig.tight_layout()
fig.savefig(ROOT / "docs/n7_result.png", dpi=200, bbox_inches="tight")
print("written docs/n7_result.png; means match ANALYSIS.json")
