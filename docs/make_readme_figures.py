"""Draw the figures of README.md and METHODS.md from the published tables, in a light and a dark version.

    python docs/make_readme_figures.py      # from the repository root; needs matplotlib (3.11.2 for the published files)

Reads only published files: N4's and N5's POINTS.csv, N7's POINTS.csv and ANALYSIS.json, and the post-hoc RESULTS.json
of 11 November. Writes docs/figures/<name>-light.png and -dark.png. Intervals are 95% t intervals over draws.
"""
import csv, json, math, statistics as st
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs/figures"; OUT.mkdir(parents=True, exist_ok=True)
N4 = ROOT / "reports/natural-text-lateturn-analysis-20261031-01/POINTS.csv"
N5 = ROOT / "reports/natural-text-fewepoch-analysis-20261103-01/POINTS.csv"
N7 = ROOT / "reports/natural-text-matched-analysis-20261105-01"
PH = ROOT / "reports/natural-text-matched-assistant-posthoc-20261111-01/RESULTS.json"

THEMES = {
    "light": dict(bg="#ffffff", ink="#1f2328", ink2="#59636e", grid="#d1d9e0", zero="#818b98",
                  w512="#2a78d6", w768="#eb6834", mean="#1f2328",
                  ramp=["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95", "#0d366b"]),
    "dark": dict(bg="#0d1117", ink="#e6edf3", ink2="#9198a1", grid="#3d444d", zero="#656c76",
                 w512="#3987e5", w768="#d95926", mean="#e6edf3",
                 ramp=["#0d366b", "#184f95", "#256abf", "#3987e5", "#6da7ec", "#9ec5f4", "#cde2fb"]),
}


def ci(x):
    x = [v for v in x]; n = len(x); m = st.mean(x); h = stats.t.ppf(.975, n - 1) * st.stdev(x) / math.sqrt(n)
    return m, m - h, m + h


def fmt(v):
    return f"{v:+.4f}".replace("-", "\u2212")


def style(ax, T, grid_axis="y"):
    ax.set_facecolor(T["bg"])
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    for s in ("left", "bottom"): ax.spines[s].set_color(T["grid"])
    ax.tick_params(colors=T["ink2"], labelsize=10, length=0, pad=6)
    if grid_axis: ax.grid(axis=grid_axis, color=T["grid"], linewidth=0.6)
    ax.set_axisbelow(True)


def new(T, *a, **k):
    fig, axes = plt.subplots(*a, **k); fig.patch.set_facecolor(T["bg"]); return fig, axes


def save(fig, name, mode):
    fig.savefig(OUT / f"{name}-{mode}.png", dpi=200, facecolor=fig.get_facecolor(), bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)


# ---- data -------------------------------------------------------------------------------------------------------
def grid_means(path, widths):
    rows = list(csv.DictReader(open(path, encoding="utf-8")))
    eps = sorted({float(r["epoch"]) for r in rows})
    M = [[st.mean(float(r[f"p_{w}"]) for r in rows if float(r["epoch"]) == e) for e in eps] for w in widths]
    return eps, M, len({r["draw"] for r in rows})


P7 = {}
for r in csv.DictReader(open(N7 / "POINTS.csv", encoding="utf-8")):
    P7[(r["draw"], float(r["epoch"]), int(r["width"]), r["tag"])] = (float(r["p"]), float(r["train"]))
DRAWS = sorted({k[0] for k in P7}); EPOCHS = sorted({k[1] for k in P7})
A = json.load(open(N7 / "ANALYSIS.json", encoding="utf-8"))["statistics"]
V = json.load(open(PH, encoding="utf-8"))["values"]
vals = lambda s: [A[s]["values"][d] for d in sorted(A[s]["values"])]


# ---- 1. landscape: p* over width and training (two heatmaps) ------------------------------------------------------
def fig_landscape(mode):
    T = THEMES[mode]; cmap = LinearSegmentedColormap.from_list("seq", T["ramp"])
    panels = [(N5, [64, 96, 128, 192, 256, 384, 512, 768], "N5 · WikiText-103 · learning rate 3e-4"),
              (N4, [256, 384, 512, 768], "N4 · WikiText-2 · learning rate 3e-5")]
    fig, axes = new(T, 1, 2, figsize=(11, 4.1), gridspec_kw=dict(width_ratios=[5, 9], wspace=0.28))
    for ax, (path, widths, title) in zip(axes, panels):
        eps, M, nd = grid_means(path, widths)
        im = ax.imshow(M, origin="lower", aspect="auto", cmap=cmap)
        ax.set_xticks(range(len(eps)), [f"{e:g}" for e in eps]); ax.set_yticks(range(len(widths)), [str(w) for w in widths])
        for j in range(len(eps)):
            i = max(range(len(widths)), key=lambda k: M[k][j])
            ax.scatter([j], [i], s=150, facecolors="none", edgecolors=T["bg"], linewidths=3.2)
            ax.scatter([j], [i], s=150, facecolors="none", edgecolors=T["ink"], linewidths=1.4)
        style(ax, T, None); [s.set_visible(False) for s in ax.spines.values()]
        ax.set_xlabel("Epochs trained", color=T["ink2"], fontsize=9); ax.set_ylabel("Model width", color=T["ink2"], fontsize=9)
        ax.set_title(f"{title}\nmean p* over {nd} draws", color=T["ink"], fontsize=10, loc="left", pad=8)
        cb = fig.colorbar(im, ax=ax, fraction=0.05, pad=0.02); cb.outline.set_visible(False)
        cb.ax.tick_params(colors=T["ink2"], labelsize=8, length=0); cb.set_label("p*", color=T["ink2"], fontsize=9)
    fig.text(0.01, -0.04, "Ring: the width with the highest mean p* at each readout. Colour scales differ between panels.",
             color=T["ink2"], fontsize=9.5)
    save(fig, "landscape", mode)


# ---- 2. alignment: the same runs on two axes ----------------------------------------------------------------------
def arm(w, tag):
    out = []
    for e in EPOCHS:
        ps = [P7[(d, e, w, tag)][0] for d in DRAWS]; ls = [P7[(d, e, w, tag)][1] for d in DRAWS]
        out.append((e, st.mean(ls), *ci(ps)))
    return out


def fig_alignment(mode):
    T = THEMES[mode]
    fig, axes = new(T, 2, 2, figsize=(10, 7.4), gridspec_kw=dict(hspace=0.6, wspace=0.2))
    for row, (tag, lab, s_upd, s_loss) in enumerate([("lr1e-04", "1e-4", "S3", "P1"), ("lr3e-04", "3e-4", "S5", "S4")]):
        a5, a7 = arm(512, tag), arm(768, tag)
        loss512 = st.mean(P7[(d, 3.0, 512, tag)][1] for d in DRAWS)
        for col, ax in enumerate(axes[row]):
            style(ax, T)
            for a, w, c in ((a5, 512, T["w512"]), (a7, 768, T["w768"])):
                x = [r[0] if col == 0 else r[1] for r in a]
                ax.fill_between(x, [r[3] for r in a], [r[4] for r in a], color=c, alpha=0.18, linewidth=0)
                ax.plot(x, [r[2] for r in a], color=c, linewidth=2, marker="o", markersize=4,
                        markeredgecolor=T["bg"], markeredgewidth=1, label=f"width {w}")
                ax.annotate(f"{w}", (x[-1], a[-1][2]), xytext=(6, 0), textcoords="offset points",
                            color=T["ink"], fontsize=9, va="center")
            m, lo, hi = ci(vals(s_upd if col == 0 else s_loss))
            if col == 0:
                ax.axvline(3.0, color=T["ink2"], linestyle="--", linewidth=1)
                for b in (1, 2, 3): ax.axvline(b, color=T["grid"], linewidth=0.6, zorder=0)
                ax.set_xlabel("Epochs trained  (equal updates = same position on this axis)", color=T["ink2"], fontsize=9)
                head = f"Equal updates, epoch 3"
            else:
                ax.axvline(loss512, color=T["ink2"], linestyle="--", linewidth=1)
                ax.invert_xaxis()
                ax.set_xlabel("Training loss, nats  (further trained →)", color=T["ink2"], fontsize=9)
                head = f"Equal training loss, 512's loss at epoch 3"
            ax.set_title(f"Learning rate {lab} · {head}\np*(512) − p*(768) = {fmt(m)}  [{fmt(lo)}, {fmt(hi)}]",
                         color=T["ink"], fontsize=10.5, loc="left")
            ax.set_ylabel("p*" if col == 0 else "", color=T["ink2"], fontsize=9)
    h, l = axes[0][0].get_legend_handles_labels()
    leg = fig.legend(h, l, loc="upper center", ncol=2, frameon=False, bbox_to_anchor=(0.5, 1.0), fontsize=9)
    [t.set_color(T["ink"]) for t in leg.get_texts()]
    fig.text(0.01, 0.005, "N7, six draws. Lines: mean p*; bands: 95% interval over draws. Dashed line: where the registered "
             "comparison reads the two widths.\nRight: x is each width's mean training loss at a readout.",
             color=T["ink2"], fontsize=9.5)
    save(fig, "alignment", mode)


# ---- 3. the registered result, draw by draw -----------------------------------------------------------------------
def fig_paired(mode):
    T = THEMES[mode]
    fig, axes = new(T, 1, 2, figsize=(9, 3.8), sharey=True, gridspec_kw=dict(wspace=0.08))
    for ax, (lab, s_upd, s_loss) in zip(axes, [("1e-4", "S3", "P1"), ("3e-4", "S5", "S4")]):
        style(ax, T); ax.axhline(0, color=T["zero"], linewidth=1)
        u, l = vals(s_upd), vals(s_loss)
        for a, b in zip(u, l): ax.plot([0, 1], [a, b], color=T["grid"], linewidth=1.2, zorder=1)
        ax.scatter([0] * 6, u, s=36, color=T["ink2"], edgecolors=T["bg"], linewidths=1, zorder=3)
        ax.scatter([1] * 6, l, s=36, color=T["ink2"], edgecolors=T["bg"], linewidths=1, zorder=3)
        for x, v in ((0.16, u), (1.16, l)):
            m, lo, hi = ci(v); ax.errorbar([x], [m], yerr=[[m - lo], [hi - m]], fmt="o", color=T["mean"],
                                           markersize=5, capsize=3, linewidth=1.4, zorder=4)
        ax.set_xticks([0, 1], ["Equal updates", "Equal training loss"]); ax.set_xlim(-0.35, 1.45)
        ax.set_title(f"Learning rate {lab}", color=T["ink"], fontsize=10)
    axes[0].set_ylabel("p*(512) − p*(768)", color=T["ink2"], fontsize=9)
    fig.text(0.01, -0.05, "N7. Dots: six draws, joined by draw. Black: mean and 95% interval over draws.",
             color=T["ink2"], fontsize=9.5)
    save(fig, "result", mode)


# ---- 4. every estimate in one place -------------------------------------------------------------------------------
def fig_estimates(mode):
    T = THEMES[mode]
    rows = [
        ("Registered, confirmed (N7)", None, None),
        ("P1 · 1e-4 · equal training loss", vals("P1"), True),
        ("S1 · 1e-4 · equal train–validation gap", vals("S1"), True),
        ("S3 · 1e-4 · equal updates", vals("S3"), True),
        ("S4 · 3e-4 · equal training loss", vals("S4"), True),
        ("S5 · 3e-4 · equal updates", vals("S5"), True),
        ("Post hoc, descriptive", None, None),
        ("P1 · 768 read at the later bracket end", V["registered_later_end|P1"], False),
        ("S4 · 768 read at the later bracket end", V["registered_later_end|S4"], False),
        ("Each width at its better rate · equal updates", V["better_rate|equal_updates|3.0"], False),
        ("Each width at its better rate · equal training loss", V["better_rate|equal_loss"], False),
        ("1e-4 · exposure-matched sequences · 768 at 2.25", V["matched|lr1e-04|k1|every"], False),
        ("1e-4 · exposure-matched sequences · 768 at 2.5", V["matched|lr1e-04|k2|every"], False),
        ("1e-4 · exposure-matched sequences · 768 at 2.75", V["matched|lr1e-04|k3|every"], False),
        ("3e-4 · exposure-matched sequences · 768 at 2.25", V["matched|lr3e-04|k1|every"], False),
        ("3e-4 · exposure-matched sequences · 768 at 2.5", V["matched|lr3e-04|k2|every"], False),
        ("3e-4 · exposure-matched sequences · 768 at 2.75", V["matched|lr3e-04|k3|every"], False),
    ]
    fig, ax = new(T, figsize=(8.2, 6.8)); style(ax, T, "x")
    n = len(rows); ax.axvline(0, color=T["zero"], linewidth=1)
    ticks, labels, heads = [], [], []
    for i, (lab, v, reg) in enumerate(rows):
        y = n - 1 - i; ticks.append(y); labels.append(lab)
        if v is None: heads.append(len(labels) - 1); continue
        m, lo, hi = ci(v)
        ax.scatter(v, [y] * len(v), s=10, color=T["ink2"], alpha=0.55, zorder=2, linewidths=0)
        ax.plot([lo, hi], [y, y], color=T["w512"], linewidth=2, zorder=3, solid_capstyle="round")
        ax.scatter([m], [y], s=46, zorder=4, color=T["w512"] if reg else T["bg"], edgecolors=T["w512"], linewidths=1.6)
        ax.text(1.01, y, fmt(m), color=T["ink2"], fontsize=10, va="center", ha="left", transform=ax.get_yaxis_transform())
    ax.set_yticks(ticks, labels)
    for k, tl in enumerate(ax.get_yticklabels()):
        tl.set_color(T["ink"]); tl.set_fontsize(10.5)
        if k in heads: tl.set_fontweight("bold")
    ax.set_xlim(-0.045, 0.04); ax.set_ylim(-0.8, n - 0.2)
    ax.spines["left"].set_visible(False)
    ax.set_xlabel("p*(512) − p*(768)", color=T["ink2"], fontsize=9)
    fig.text(0.0, -0.03, "Bar: mean and 95% interval over six draws (unadjusted); grey dots: the draws.\nFilled: registered "
             "before the runs; hollow: post hoc.", color=T["ink2"], fontsize=9.5)
    save(fig, "estimates", mode)


# ---- 5. exposure: sequences trained this epoch vs the rest -----------------------------------------------------------
def fig_exposure(mode):
    T = THEMES[mode]
    fig, axes = new(T, 1, 2, figsize=(9, 3.6), sharey=True, gridspec_kw=dict(wspace=0.08))
    ticks = [0.25, 0.5, 2.25, 2.5, 2.75, 3.25, 3.5]
    for ax, (tag, lab) in zip(axes, [("lr1e-04", "1e-4"), ("lr3e-04", "3e-4")]):
        style(ax, T); ax.axhline(0, color=T["zero"], linewidth=1)
        for k, (w, c) in enumerate(((512, T["w512"]), (768, T["w768"]))):
            xs = [i + (k - 0.5) * 0.18 for i in range(len(ticks))]
            for x, e in zip(xs, ticks):
                m, lo, hi = ci(V[f"seen_minus_unseen|{w}|{tag}|{e:g}"])
                ax.plot([x, x], [lo, hi], color=c, linewidth=2, solid_capstyle="round")
                ax.scatter([x], [m], s=30, color=c, edgecolors=T["bg"], linewidths=1, zorder=3,
                           label=f"width {w}" if e == ticks[0] else None)
        ax.set_xticks(range(len(ticks)), [f"{e:g}" for e in ticks])
        ax.set_xlabel("Readout (epochs)", color=T["ink2"], fontsize=9)
        ax.set_title(f"Learning rate {lab}", color=T["ink"], fontsize=10)
    axes[0].set_ylabel("p*(trained this epoch) − p*(not yet)", color=T["ink2"], fontsize=9)
    leg = axes[1].legend(frameon=False, fontsize=9, loc="upper right"); [t.set_color(T["ink"]) for t in leg.get_texts()]
    fig.text(0.01, -0.05, "N7, post hoc. Within one model and readout: sequences already trained in the current epoch minus "
             "the rest. Mean and 95% interval over six draws.", color=T["ink2"], fontsize=9.5)
    save(fig, "exposure", mode)


if __name__ == "__main__":
    plt.rcParams["font.family"] = "DejaVu Sans"; plt.rcParams["axes.unicode_minus"] = True
    for mode in THEMES:
        fig_landscape(mode); fig_alignment(mode); fig_paired(mode); fig_estimates(mode); fig_exposure(mode)
    print("written:", ", ".join(sorted(p.name for p in OUT.glob("*.png"))))
