"""Recompute every N7 p* estimate from the per-sequence loss arrays, and the principal contrasts from those estimates.

    python tools/verify_n7_losses.py PATH/TO/n7-loss-arrays      # from the repository root; needs NumPy

The loss-array bundle (n7-loss-arrays-v1.zip) is attached to the repository's v1.2 release. This script:
  1. checks every file of the bundle against MANIFEST.json (sizes and SHA-256), and each weight vector against the
     tensor hash its run recorded;
  2. refits all 240 estimates (6 draws x 2 widths x 2 learning rates x 10 readouts) with its own NumPy implementation
     of the estimator: the sealed search (grid of step 0.05 on [0, 8], 50 ternary steps, best of that point and the two
     ends) applied to the mean squared cumulative discrepancy of the reference study's technical note, ties ranked by
     sequence order;
  3. compares the fits with reports/natural-text-matched-analysis-20261105-01/POINTS.csv (tolerance 1e-6), and the
     per-readout mean losses with the run records (tolerance 1e-5);
  4. recomputes the five confirmed contrasts from the refitted values and compares their means and intervals with
     ANALYSIS.json (tolerance 1e-6).
It imports nothing from the project's training or analysis code. It does not regenerate the losses by running models.
"""
import csv, hashlib, json, math, statistics as st, sys
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = ROOT / "reports/natural-text-matched-analysis-20261105-01"
T975 = {4: 2.776445105, 5: 2.570581836}
N_VAL = 512


def sha(b):
    return hashlib.sha256(b).hexdigest()


def exponent(weights, gains):
    """Return p*, or None if the fit is undefined."""
    w = np.asarray(weights, dtype=np.float64); g = np.asarray(gains, dtype=np.float64)
    if w.max() - w.min() < 1e-12 or g.sum() <= 1e-10:
        return None
    order = np.argsort(w, kind="stable")
    logw = np.log(w[order]); gn = g[order] / g.sum()

    def objective(p):
        z = np.exp(p * logw - (p * logw).max())
        c = np.cumsum(gn - z / z.sum())
        return float(np.dot(c, c) / len(c))

    grid = [i / 20 for i in range(161)]
    j = min(range(len(grid)), key=lambda i: objective(grid[i]))
    lo, hi = grid[max(0, j - 1)], grid[min(len(grid) - 1, j + 1)]
    for _ in range(50):
        a, b = lo + (hi - lo) / 3, hi - (hi - lo) / 3
        if objective(a) < objective(b):
            hi = b
        else:
            lo = a
    return min([0.0, (lo + hi) / 2, 8.0], key=objective)


def interval(v):
    m = st.mean(v); h = T975[len(v) - 1] * st.stdev(v) / math.sqrt(len(v))
    return m, m - h, m + h


def main(bundle):
    bundle = Path(bundle); man = json.loads((bundle / "MANIFEST.json").read_text(encoding="utf-8"))
    files = 0
    for d, entry in man["draws"].items():
        refs = [entry["weights"]] + [x for wd in entry["widths"].values() for x in [wd["E0"]] + [y for arm in wd["arms"].values() for y in (arm["arrays"], arm["record"])]]
        for ref in refs:
            b = (bundle / ref["path"]).read_bytes()
            assert len(b) == ref["bytes"] and sha(b) == ref["sha256"], f"file differs from MANIFEST.json: {ref['path']}"
            files += 1
        wb = (bundle / entry["weights"]["path"]).read_bytes(); n = len(wb) // 4
        h = hashlib.sha256(); h.update(str(((n,), "torch.float32")).encode()); h.update(wb)
        assert h.hexdigest() == entry["weights"]["bound_tensor_hash"], f"weights differ from the run's tensor hash: {d}"
    print(f"bundle: {files} files match MANIFEST.json; 6 weight vectors match their runs' tensor hashes")

    published = {}
    for r in csv.DictReader(open(ANALYSIS / "POINTS.csv", encoding="utf-8")):
        published[(r["draw"], float(r["epoch"]), int(r["width"]), r["tag"])] = r
    fits, worst_p, worst_loss = {}, 0.0, 0.0
    for d, entry in man["draws"].items():
        weights = np.frombuffer((bundle / entry["weights"]["path"]).read_bytes(), dtype="<f4")
        n = len(weights)
        for wd, wentry in entry["widths"].items():
            e0 = np.frombuffer((bundle / wentry["E0"]["path"]).read_bytes(), dtype="<f4")
            for tag, arm in wentry["arms"].items():
                rec = json.loads((bundle / arm["record"]["path"]).read_text(encoding="utf-8"))
                arr = np.frombuffer((bundle / arm["arrays"]["path"]).read_bytes(), dtype="<f4")
                for k, epoch in enumerate(rec["layout"]["block_epochs"]):
                    block = arr[k * (n + N_VAL):(k + 1) * (n + N_VAL)]
                    train, val = block[:n], block[n:]
                    gains = (e0[:n] - train).astype(np.float32)  # float32 subtraction, as in the sealed analysis
                    p = exponent(weights, gains)
                    pub = published[(d, float(epoch), int(wd), tag)]
                    worst_p = max(worst_p, abs(p - float(pub["p"])))
                    x = next(x for x in rec["readouts"] if x["epoch"] == epoch)
                    worst_loss = max(worst_loss, abs(float(train.astype(np.float64).mean()) - x["train_loss"]),
                                     abs(float(val.astype(np.float64).mean()) - x["validation_loss"]))
                    fits[(d, float(epoch), int(wd), tag)] = dict(p=p, train=x["train_loss"], gap=x["validation_loss"] - x["train_loss"])
    print(f"fits: {len(fits)} refitted; largest |p* - POINTS.csv| = {worst_p:.2e}; largest |array mean - record| = {worst_loss:.2e}")
    assert len(fits) == 240 and worst_p < 1e-6 and worst_loss < 1e-5

    draws = sorted(man["draws"]); path = [2.0, 2.25, 2.5, 2.75, 3.0, 3.25, 3.5]

    def matched(rate, key):
        out = []
        for d in draws:
            tgt = fits[(d, 3.0, 512, rate)][key]
            pts = [(fits[(d, e, 768, rate)][key], fits[(d, e, 768, rate)]["p"]) for e in path]
            for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
                if min(x0, x1) <= tgt <= max(x0, x1):
                    out.append(fits[(d, 3.0, 512, rate)]["p"] - (y0 + (tgt - x0) / (x1 - x0) * (y1 - y0))); break
        return out

    fixed = lambda rate: [fits[(d, 3.0, 512, rate)]["p"] - fits[(d, 3.0, 768, rate)]["p"] for d in draws]
    stats = {"P1": matched("lr1e-04", "train"), "S1": matched("lr1e-04", "gap"), "S3": fixed("lr1e-04"),
             "S4": matched("lr3e-04", "train"), "S5": fixed("lr3e-04")}
    sealed = json.loads((ANALYSIS / "ANALYSIS.json").read_text(encoding="utf-8"))["statistics"]
    for k, v in stats.items():
        m, lo, hi = interval(v); s = sealed[k]["interval"]
        assert len(v) == s["n"] and abs(m - s["mean"]) < 1e-6 and abs(lo - s["interval"][0]) < 1e-6 and abs(hi - s["interval"][1]) < 1e-6, k
        print(f"  {k}: {m:+.5f} [{lo:+.5f}, {hi:+.5f}], n = {len(v)}; matches ANALYSIS.json")
    print("PASS")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
