"""Draw the descriptive figures of METHODS.md: fitted p* across model size, training budget and sequence weight.

    python docs/make_results_figures.py [path/to/n7-loss-arrays]      # from the repository root

Every value comes from published files: N3's and N5's POINTS.csv (per-draw p* by width and readout), and, for the
gain-by-weight figure, the per-sequence losses in n7-loss-arrays-v1.zip (attached to the v1.2 release). Without the
bundle path, that figure is skipped. Writes docs/figures/<name>-light.png, <name>-dark.png and <name>.html
(interactive; the page loads plotly.js from a CDN). Intervals are 95% t intervals over draws.
"""
import csv, json, math, statistics as st, sys
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, LogNorm, Normalize
from matplotlib.cm import ScalarMappable
from scipy import stats
import plotly.graph_objects as go
from plotly.subplots import make_subplots

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "figures"
N3 = ROOT / "reports/natural-text-onerate-analysis-20261030-02/POINTS.csv"
N5 = ROOT / "reports/natural-text-fewepoch-analysis-20261103-01/POINTS.csv"
WIDTHS = [64, 96, 128, 192, 256, 384, 512, 768]


def params(width, layers=4, vocab=4096, length=128):
    """Exact parameter count of the model (text_plan.parameters in the sealed source)."""
    return layers * (12 * width * width + 13 * width) + (2 * vocab + length + 2) * width


THEMES = {
    "light": dict(bg="#ffffff", ink="#1f2328", ink2="#59636e", grid="#d1d9e0",
                  ramp=["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95", "#0d366b"],
                  w512="#2a78d6", w768="#eb6834"),
    "dark": dict(bg="#0d1117", ink="#e6edf3", ink2="#9198a1", grid="#3d444d",
                 ramp=["#184f95", "#256abf", "#3987e5", "#6da7ec", "#9ec5f4", "#cde2fb", "#eef5fd"],
                 w512="#3987e5", w768="#d95926"),
}
PLOTLY_RAMP = [[i / 6, c] for i, c in enumerate(THEMES["light"]["ramp"])]


def ci(x):
    x = list(x); n = len(x); m = st.mean(x); h = stats.t.ppf(.975, n - 1) * st.stdev(x) / math.sqrt(n)
    return m, m - h, m + h


def style(ax, T):
    ax.set_facecolor(T["bg"])
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    for s in ("left", "bottom"): ax.spines[s].set_color(T["grid"])
    ax.tick_params(colors=T["ink2"], labelsize=10, length=0, pad=6, which="both")
    ax.grid(color=T["grid"], linewidth=0.6, which="major"); ax.set_axisbelow(True)


def save(fig, name, mode):
    fig.savefig(OUT / f"{name}-{mode}.png", dpi=200, facecolor=fig.get_facecolor(), bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)


def table(path):
    rows = list(csv.DictReader(open(path, encoding="utf-8")))
    eps = sorted({float(r["epoch"]) for r in rows})
    stat = {(w, e): ci(float(r[f"p_{w}"]) for r in rows if float(r["epoch"]) == e) for w in WIDTHS for e in eps}
    return eps, stat, len({r["draw"] for r in rows})


STUDIES = [("N5 · WikiText-103 · learning rate 3e-4", N5), ("N3 · WikiText-2 · learning rate 3e-5", N3)]


# ---- 1. p* against model size, one line per training budget ---------------------------------------------------------
def fig_size(mode):
    T = THEMES[mode]; cmap = LinearSegmentedColormap.from_list("ramp", T["ramp"])
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.6), gridspec_kw=dict(wspace=0.32)); fig.patch.set_facecolor(T["bg"])
    x = [params(w) for w in WIDTHS]
    for ax, (title, path) in zip(axes, STUDIES):
        eps, S, nd = table(path); style(ax, T)
        norm = LogNorm(vmin=min(eps), vmax=max(eps))
        for e in eps:
            c = cmap(0.15 + 0.85 * norm(e))
            m = [S[(w, e)][0] for w in WIDTHS]; lo = [S[(w, e)][1] for w in WIDTHS]; hi = [S[(w, e)][2] for w in WIDTHS]
            ax.fill_between(x, lo, hi, color=c, alpha=0.18, linewidth=0)
            ax.plot(x, m, color=c, linewidth=2, marker="o", markersize=4, markeredgecolor=T["bg"], markeredgewidth=0.8)
        ax.set_xscale("log"); ax.set_xticks(x[::2] + [x[-1]], [f"{v / 1e6:.2g}M" for v in x[::2] + [x[-1]]])
        ax.minorticks_off()
        ax.set_xlabel("Parameters (width 64 → 768, depth 4)", color=T["ink2"], fontsize=10)
        ax.set_ylabel("p*", color=T["ink2"], fontsize=10)
        ax.set_title(f"{title} · {nd} draws", color=T["ink"], fontsize=11, loc="left")
        sm = ScalarMappable(norm=norm, cmap=LinearSegmentedColormap.from_list("r", [cmap(0.15 + 0.85 * norm(e)) for e in
                                                                                  np.geomspace(min(eps), max(eps), 64)]))
        cb = fig.colorbar(sm, ax=ax, pad=0.02, fraction=0.05); cb.outline.set_visible(False)
        cb.set_ticks(eps); cb.set_ticklabels([f"{e:g}" for e in eps]); cb.ax.minorticks_off()
        cb.ax.tick_params(colors=T["ink2"], labelsize=9, length=0); cb.set_label("epochs of weighted training", color=T["ink2"])
    fig.text(0.0, -0.06, "Lines: mean p* over draws at each readout; bands: 95% interval over draws. Fitted at evaluated readouts only.",
             color=T["ink2"], fontsize=9.5)
    save(fig, "pstar-vs-size", mode)


# ---- 1b. the same data transposed: p* against training time, one line per model size -------------------------------
def fig_training(mode):
    T = THEMES[mode]; cmap = LinearSegmentedColormap.from_list("ramp", T["ramp"])
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.6), gridspec_kw=dict(wspace=0.48)); fig.patch.set_facecolor(T["bg"])
    sizes = [params(w) for w in WIDTHS]; norm = LogNorm(vmin=min(sizes), vmax=max(sizes))
    for ax, (title, path) in zip(axes, STUDIES):
        eps, S, nd = table(path); style(ax, T)
        for w, n in zip(WIDTHS, sizes):
            c = cmap(0.15 + 0.85 * norm(n))
            ax.fill_between(eps, [S[(w, e)][1] for e in eps], [S[(w, e)][2] for e in eps], color=c, alpha=0.18, linewidth=0)
            ax.plot(eps, [S[(w, e)][0] for e in eps], color=c, linewidth=2, marker="o", markersize=4,
                    markeredgecolor=T["bg"], markeredgewidth=0.8)
        ax.set_xscale("log", base=2); ax.set_xticks(eps, [f"{e:g}" for e in eps]); ax.minorticks_off()
        ax.set_xlabel("Epochs of weighted training", color=T["ink2"], fontsize=10)
        ax.set_ylabel("p*", color=T["ink2"], fontsize=10)
        ax.set_title(f"{title} · {nd} draws", color=T["ink"], fontsize=11, loc="left")
        sm = ScalarMappable(norm=norm, cmap=LinearSegmentedColormap.from_list(
            "r", [cmap(0.15 + 0.85 * norm(v)) for v in np.geomspace(min(sizes), max(sizes), 64)]))
        cb = fig.colorbar(sm, ax=ax, pad=0.02, fraction=0.05); cb.outline.set_visible(False); cb.ax.minorticks_off()
        cb.set_ticks(sizes); cb.set_ticklabels([f"{w} · {n / 1e6:.2g}M" for w, n in zip(WIDTHS, sizes)])
        cb.ax.tick_params(colors=T["ink2"], labelsize=8, length=0); cb.set_label("width · parameters", color=T["ink2"])
    fig.text(0.0, -0.06, "Lines: mean p* over draws for each width; bands: 95% interval over draws. Fitted at evaluated readouts only.",
             color=T["ink2"], fontsize=9.5)
    save(fig, "pstar-vs-training", mode)


def html_size():
    fig = make_subplots(rows=1, cols=2, subplot_titles=[t for t, _ in STUDIES], horizontal_spacing=0.1)
    x = [params(w) for w in WIDTHS]
    for k, (title, path) in enumerate(STUDIES, start=1):
        eps, S, nd = table(path)
        for i, e in enumerate(eps):
            c = THEMES["light"]["ramp"][1 + round(5 * i / max(1, len(eps) - 1))]
            m = [S[(w, e)][0] for w in WIDTHS]
            err = [S[(w, e)][2] - S[(w, e)][0] for w in WIDTHS]
            fig.add_trace(go.Scatter(x=x, y=m, mode="lines+markers", name=f"{e:g} epochs", legendgroup=f"s{k}",
                                     line=dict(color=c), error_y=dict(type="data", array=err, thickness=1),
                                     customdata=WIDTHS, hovertemplate="width %{customdata}<br>%{x:.3s} parameters"
                                     "<br>p* %{y:.4f}<extra>" + f"{e:g} epochs" + "</extra>"), row=1, col=k)
        fig.update_xaxes(type="log", title="parameters", row=1, col=k); fig.update_yaxes(title="p*", row=1, col=k)
    fig.update_layout(template="plotly_white", title="p* against model size, by epochs of weighted training "
                      "(mean and 95% interval over 10 draws)")
    fig.write_html(OUT / "pstar-vs-size.html", include_plotlyjs="cdn")


# ---- 2. surface of p* over model size and training budget -----------------------------------------------------------
def fig_surface(mode):
    T = THEMES[mode]; cmap = LinearSegmentedColormap.from_list("ramp", T["ramp"])
    fig = plt.figure(figsize=(12, 5.4)); fig.patch.set_facecolor(T["bg"])
    for k, (title, path) in enumerate(STUDIES, start=1):
        eps, S, nd = table(path)
        X, Y = np.meshgrid(np.log10([params(w) for w in WIDTHS]), np.log2(eps))
        Z = np.array([[S[(w, e)][0] for w in WIDTHS] for e in eps])
        ax = fig.add_subplot(1, 2, k, projection="3d"); ax.set_facecolor(T["bg"])
        ax.plot_surface(X, Y, Z, cmap=cmap, linewidth=0.4, edgecolor=T["bg"], antialiased=True)
        ax.set_xticks(np.log10([params(w) for w in (64, 192, 512, 768)]), ["0.7M", "3.4M", "17M", "35M"])
        ax.set_yticks(np.log2(eps)[::2], [f"{e:g}" for e in eps[::2]])
        for lab, f in ((ax.set_xlabel, "parameters"), (ax.set_ylabel, "epochs"), (ax.set_zlabel, "mean p*")):
            lab(f, color=T["ink2"], labelpad=6)
        ax.tick_params(colors=T["ink2"], labelsize=8)
        for a in (ax.xaxis, ax.yaxis, ax.zaxis):
            a.set_pane_color(T["bg"]); a._axinfo["grid"]["color"] = T["grid"]
        ax.view_init(elev=24, azim=-128)
        ax.set_title(f"{title}\nmean of {nd} draws", color=T["ink"], fontsize=10.5)
    save(fig, "pstar-surface", mode)


def html_surface():
    fig = make_subplots(rows=1, cols=2, specs=[[{"type": "surface"}, {"type": "surface"}]],
                        subplot_titles=[t for t, _ in STUDIES])
    for k, (title, path) in enumerate(STUDIES, start=1):
        eps, S, nd = table(path)
        Z = [[S[(w, e)][0] for w in WIDTHS] for e in eps]
        fig.add_trace(go.Surface(x=[params(w) for w in WIDTHS], y=eps, z=Z, colorscale=PLOTLY_RAMP, showscale=k == 2,
                                 colorbar=dict(title="mean p*")), row=1, col=k)
        fig.update_scenes(dict(xaxis=dict(type="log", title="parameters"), yaxis=dict(type="log", title="epochs"),
                               zaxis=dict(title="mean p*")), row=1, col=k)
    fig.update_layout(template="plotly_white", title="Mean p* over model size and epochs of weighted training (10 draws each)")
    fig.write_html(OUT / "pstar-surface.html", include_plotlyjs="cdn")


# ---- 3. gain by sequence weight and training time, from N7's per-sequence losses ------------------------------------
N7_EPOCHS = [0.25, 0.5, 1, 2, 2.25, 2.5, 2.75, 3, 3.25, 3.5]


def gain_grid(bundle, width, tag, bins=16):
    man = json.load(open(bundle / "MANIFEST.json")); n = 16384
    edges = np.linspace(np.log10(0.01), np.log10(10), bins + 1)
    G = np.zeros((len(N7_EPOCHS), bins)); draws = sorted(man["draws"])
    for d in draws:
        w = np.fromfile(bundle / d / "weights.f32", "<f4")
        e0 = np.fromfile(bundle / d / f"w{width}" / "E0.f32", "<f4")[:n]
        a = np.fromfile(bundle / d / f"w{width}" / tag / "arrays.f32", "<f4").reshape(len(N7_EPOCHS), -1)[:, :n]
        b = np.clip(np.digitize(np.log10(w), edges) - 1, 0, bins - 1)
        for i in range(len(N7_EPOCHS)):
            g = e0 - a[i]
            G[i] += np.bincount(b, weights=g, minlength=bins) / np.bincount(b, minlength=bins)
    return (edges[:-1] + edges[1:]) / 2, G / len(draws), len(draws)


def fig_gain(bundle, mode):
    T = THEMES[mode]; cmap = LinearSegmentedColormap.from_list("ramp", T["ramp"])
    fig = plt.figure(figsize=(12, 5.4)); fig.patch.set_facecolor(T["bg"])
    for k, w in enumerate((512, 768), start=1):
        c, G, nd = gain_grid(bundle, w, "lr1e-04")
        X, Y = np.meshgrid(c, np.arange(len(N7_EPOCHS)))
        ax = fig.add_subplot(1, 2, k, projection="3d"); ax.set_facecolor(T["bg"])
        ax.plot_surface(X, Y, G, cmap=cmap, linewidth=0.3, edgecolor=T["bg"], antialiased=True, vmin=0, vmax=2.9)
        ax.set_xticks([-2, -1, 0, 1], ["0.01", "0.1", "1", "10"])
        ax.set_yticks(range(0, len(N7_EPOCHS), 2), [f"{e:g}" for e in N7_EPOCHS[::2]])
        for lab, f in ((ax.set_xlabel, "sequence weight w"), (ax.set_ylabel, "epochs (readout)"),
                       (ax.set_zlabel, "mean gain (nats)")):
            lab(f, color=T["ink2"], labelpad=6)
        ax.tick_params(colors=T["ink2"], labelsize=8)
        for a in (ax.xaxis, ax.yaxis, ax.zaxis):
            a.set_pane_color(T["bg"]); a._axinfo["grid"]["color"] = T["grid"]
        ax.view_init(elev=22, azim=-55); ax.set_zlim(0, 2.9)
        ax.set_title(f"N7 · width {w} ({params(w) / 1e6:.1f}M) · learning rate 1e-4\nmean of {nd} draws",
                     color=T["ink"], fontsize=10.5)
    save(fig, "gain-by-weight", mode)


def html_gain(bundle):
    fig = make_subplots(rows=1, cols=2, specs=[[{"type": "surface"}, {"type": "surface"}]],
                        subplot_titles=["N7 · width 512 · 1e-4", "N7 · width 768 · 1e-4"])
    for k, w in enumerate((512, 768), start=1):
        c, G, nd = gain_grid(bundle, w, "lr1e-04")
        fig.add_trace(go.Surface(x=10 ** c, y=list(range(len(N7_EPOCHS))), z=G, colorscale=PLOTLY_RAMP, cmin=0, cmax=2.9,
                                 showscale=k == 2, colorbar=dict(title="gain (nats)")), row=1, col=k)
        fig.update_scenes(dict(xaxis=dict(type="log", title="weight w"),
                               yaxis=dict(title="readout", tickvals=list(range(len(N7_EPOCHS))),
                                          ticktext=[f"{e:g}" for e in N7_EPOCHS]),
                               zaxis=dict(title="mean gain (nats)", range=[0, 2.9])), row=1, col=k)
    fig.update_layout(template="plotly_white", title="Mean per-sequence gain by weight and training time (N7, 6 draws)")
    fig.write_html(OUT / "gain-by-weight.html", include_plotlyjs="cdn")


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True); plt.rcParams["font.family"] = "DejaVu Sans"
    bundle = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    for mode in THEMES:
        fig_size(mode); fig_training(mode); fig_surface(mode)
        if bundle: fig_gain(bundle, mode)
    html_size(); html_surface()
    if bundle: html_gain(bundle)
    print("written:", ", ".join(sorted(p.name for p in OUT.glob("*") if p.stem.split("-")[0] in ("pstar", "gain"))))
