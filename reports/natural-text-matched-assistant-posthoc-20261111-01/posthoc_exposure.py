"""Post-hoc, descriptive analyses of N7 by training exposure, from the v1.0 loss-array bundle and POINTS.csv.

    python reports/natural-text-matched-assistant-posthoc-20261111-01/posthoc_exposure.py PATH/TO/n7-loss-arrays [RESULTS.json]

Run from anywhere; needs NumPy and PyTorch (CPU). It prints a text report and, if a second argument is given, writes
the per-draw values behind every printed interval as JSON.

EVERYTHING HERE IS POST HOC. No statistic below was registered, none moves a sealed label, and no interval is adjusted
for the number of comparisons. Intervals are two-sided 95% t intervals over the six draws (df 5), as elsewhere in the
record.

What it does
  0. Checks: the bundle against its MANIFEST.json; a refit of all 240 estimates against POINTS.csv; the regenerated
     weights against the bundle; and the regenerated batch orders against the losses (the sequences an order says were
     trained in a quarter epoch are the ones whose loss fell in it; a shifted seed is the negative control).
  1. Seen and not-yet-seen sequences: at each readout inside an epoch, p* of the sequences already trained in the
     current epoch minus p* of those not yet trained in it.
  2. Fixed sets: over each quarter-epoch interval, p* of the sequences trained in that interval and of the others,
     before and after, and the whole-set change.
  3. Exposure-matched contrasts: 512 at epoch 3 against 768 at epoch 2.25, 2.5 and 2.75, (a) on the whole training
     set, (b) on sequences matched for the timing of the last pass only, (c) on sequences matched for the timing of
     every pass. Also the within-model effect of the timing of the second pass.
  4. Each width at its better rate: 512 at 3e-4 against 768 at 1e-4, from POINTS.csv.
  5. The equal-updates contrast 512 - 768 at every readout, from POINTS.csv.
  6. Where the matched readings of P1 and S4 fall, and the change of validation loss across each quarter epoch.

Batch orders. The loss arrays do not record which sequences were trained when. The sealed engine draws epoch e's order
as torch.randperm(n, generator=torch.Generator().manual_seed(999 + adapt_order_seed + e)) (text_engine.orders) and
trains on consecutive batches of 16 (matched_worker.adapt_readouts), so the readout at epoch (e - 1) + k/4 follows the
first 4096 k entries of epoch e's order. The seeds are in the bundle's MANIFEST.json. Check 0 fails loudly if the
installed PyTorch does not reproduce the orders that produced the losses.

"Quarter q of epoch e" below means positions [4096 (q - 1), 4096 q) of epoch e's order. Time is counted in quarter
epochs, T = 4 x epoch. The estimator is the sealed search (grid of step 0.05 on [0, 8], 50 ternary steps, best of that
point and the two ends), re-implemented here; it imports no project code.
"""
import csv, hashlib, json, math, random, sys
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
POINTS = ROOT / "reports/natural-text-matched-analysis-20261105-01/POINTS.csv"
DRAWS = ["m01", "m02", "m03", "m04", "m05", "m06"]
ARMS = [(512, "lr1e-04"), (768, "lr1e-04"), (512, "lr3e-04"), (768, "lr3e-04")]
LO, HI = "lr1e-04", "lr3e-04"
N, N_VAL, Q = 16384, 512, 4096
T975_5 = 2.570581836
PATH = [2.0, 2.25, 2.5, 2.75, 3.0, 3.25, 3.5]
RESULTS = {}


def sha(b):
    return hashlib.sha256(b).hexdigest()


def exponent(weights, gains):
    """p*: the sealed search on the mean squared cumulative discrepancy; ties ranked in sequence order."""
    w = np.asarray(weights, np.float64); g = np.asarray(gains, np.float64)
    assert w.max() - w.min() >= 1e-12 and g.sum() > 1e-10, "undefined fit"
    order = np.argsort(w, kind="stable")
    logw = np.log(w[order]); logw = logw - logw.max(); cg = np.cumsum(g[order] / g.sum())

    def objective(p):
        z = np.exp(p * logw)
        c = cg - np.cumsum(z) / z.sum()
        return float(np.dot(c, c) / len(c))

    grid = np.arange(161) / 20.0
    vals = np.empty(161)
    for s in range(0, 161, 23):
        z = np.exp(grid[s:s + 23, None] * logw[None, :])
        c = cg[None, :] - np.cumsum(z, 1) / z.sum(1, keepdims=True)
        vals[s:s + 23] = (c * c).mean(1)
    j = int(np.argmin(vals))
    lo, hi = float(grid[max(0, j - 1)]), float(grid[min(160, j + 1)])
    for _ in range(50):
        a, b = lo + (hi - lo) / 3, hi - (hi - lo) / 3
        if objective(a) < objective(b):
            hi = b
        else:
            lo = a
    return min([0.0, (lo + hi) / 2, 8.0], key=objective)


def interval(v):
    v = np.asarray(v, float); assert len(v) == 6
    m = float(v.mean()); h = T975_5 * float(v.std(ddof=1)) / math.sqrt(6)
    return m, m - h, m + h


def show(key, v, digits=4, count=True):
    """Format mean [95% interval] and the number of draws above 0; keep the per-draw values under `key`."""
    RESULTS[key] = [float(x) for x in v]
    m, lo, hi = interval(v)
    s = f"{m:+.{digits}f} [{lo:+.{digits}f}, {hi:+.{digits}f}]"
    return s + (f", {int(sum(x > 0 for x in v))}/6" if count else "")


class Arm:
    def __init__(self, bundle, man, d, width, tag):
        e = man["draws"][d]["widths"][str(width)]
        rec = json.loads((bundle / e["arms"][tag]["record"]["path"]).read_text(encoding="utf-8"))
        self.epochs = [float(x) for x in rec["layout"]["block_epochs"]]
        e0 = np.frombuffer((bundle / e["E0"]["path"]).read_bytes(), "<f4")
        arr = np.frombuffer((bundle / e["arms"][tag]["arrays"]["path"]).read_bytes(), "<f4").reshape(len(self.epochs), N + N_VAL)
        self.e0 = e0[:N]
        self.train = {ep: arr[k, :N] for k, ep in enumerate(self.epochs)}
        self.train[0.0] = self.e0
        self.val = {ep: arr[k, N:] for k, ep in enumerate(self.epochs)}

    def gain(self, ep):
        return (self.e0 - self.train[ep]).astype(np.float32)  # float32 subtraction, as in the sealed analysis

    def loss(self, ep, mask=None):
        x = self.train[ep].astype(np.float64)
        return float(x.mean() if mask is None else x[mask].mean())


def main(bundle, results_path=None):
    import torch
    bundle = Path(bundle); man = json.loads((bundle / "MANIFEST.json").read_text(encoding="utf-8"))
    print("POST-HOC ANALYSES OF N7 BY TRAINING EXPOSURE. Descriptive; nothing here was registered.")
    print(f"NumPy {np.__version__}; PyTorch {torch.__version__}. Contrasts are 512 minus 768; mean [95% t interval over 6 draws], draws above 0.")

    # ------------------------------------------------------------------ 0. checks
    print("\n0. CHECKS")
    files = 0
    for d, entry in man["draws"].items():
        refs = [entry["weights"]] + [x for wd in entry["widths"].values() for x in [wd["E0"]] + [y for arm in wd["arms"].values() for y in (arm["arrays"], arm["record"])]]
        for ref in refs:
            b = (bundle / ref["path"]).read_bytes()
            assert len(b) == ref["bytes"] and sha(b) == ref["sha256"], f"file differs from MANIFEST.json: {ref['path']}"
            files += 1
    print(f"  bundle: {files} files match MANIFEST.json")
    assert sorted(man["draws"]) == DRAWS

    arms = {(d, wd, tag): Arm(bundle, man, d, wd, tag) for d in DRAWS for wd, tag in ARMS}
    W = {d: np.frombuffer((bundle / man["draws"][d]["weights"]["path"]).read_bytes(), "<f4") for d in DRAWS}
    P = {}
    for r in csv.DictReader(open(POINTS, encoding="utf-8")):
        P[(r["draw"], float(r["epoch"]), int(r["width"]), r["tag"])] = dict(p=float(r["p"]), train=float(r["train"]), val=float(r["validation"]))

    FIT = {}
    worst = 0.0
    for (d, wd, tag), a in arms.items():
        for ep in a.epochs:
            FIT[(d, ep, wd, tag)] = exponent(W[d], a.gain(ep))
            worst = max(worst, abs(FIT[(d, ep, wd, tag)] - P[(d, ep, wd, tag)]["p"]))
    print(f"  refit: {len(FIT)} whole-set estimates; largest |p* - POINTS.csv| = {worst:.1e}")
    assert len(FIT) == 240 and worst < 1e-6

    for d in DRAWS:
        rng = random.Random(1000 + man["draws"][d]["seeds"]["weight_seed"])
        w = torch.tensor([math.exp(rng.uniform(math.log(.01), math.log(10))) for _ in range(N)], dtype=torch.float32)
        assert np.array_equal((w / w.mean()).numpy(), W[d]), f"regenerated weights differ: {d}"
    print("  weights: regenerated from weight_seed as text_engine.weights does; bit-identical to the bundle in 6/6 draws")

    def orders(d, shift=0):
        seed = man["draws"][d]["seeds"]["adapt_order_seed"] + shift
        return np.stack([torch.randperm(N, generator=torch.Generator().manual_seed(999 + seed + e)).numpy() for e in range(1, 5)])

    ORD = {d: orders(d) for d in DRAWS}
    # quarter of each sequence in each of the four epochs' orders: QTR[d][e - 1][i] in 1..4
    QTR = {}
    for d in DRAWS:
        q = np.zeros((4, N), np.int64)
        for e in range(4):
            q[e, ORD[d][e]] = np.arange(N) // Q + 1
        QTR[d] = q

    # the eight quarter-epoch intervals between consecutive readouts: (t0, t1, epoch, quarter trained in it)
    INTS = [(0.0, 0.25, 1, 1), (0.25, 0.5, 1, 2), (2.0, 2.25, 3, 1), (2.25, 2.5, 3, 2), (2.5, 2.75, 3, 3), (2.75, 3.0, 3, 4), (3.0, 3.25, 4, 1), (3.25, 3.5, 4, 2)]

    def separation(order_of, label):
        gaps = []
        for (t0, t1, e, q) in INTS:
            for d in DRAWS:
                trained = np.zeros(N, bool); trained[order_of[d][e - 1][(q - 1) * Q:q * Q]] = True
                for wd, tag in ARMS:
                    a = arms[(d, wd, tag)]
                    dl = a.train[t1].astype(np.float64) - a.train[t0].astype(np.float64)
                    gaps.append(dl[trained].mean() - dl[~trained].mean())
        gaps = np.array(gaps)
        print(f"  orders ({label}): loss change of the sequences the order says were trained in a quarter, minus that of the others: "
              f"mean {gaps.mean():+.4f} nats, range [{gaps.min():+.4f}, {gaps.max():+.4f}], below -0.05 in {int((gaps < -0.05).sum())}/{len(gaps)} (interval x draw x arm)")
        return gaps

    g = separation(ORD, "regenerated")
    g0 = separation({d: orders(d, 1) for d in DRAWS}, "negative control, seed + 1")
    assert (g < -0.05).all() and (np.abs(g0) < 0.02).all(), "the regenerated batch orders do not match the losses; check the PyTorch version"
    # the step falls exactly at the quarter's end: the last 256 sequences of the trained quarter against the first 256 after it
    edge = []
    for (t0, t1, e, q) in INTS:
        if q == 4:
            continue
        for d in DRAWS:
            o = ORD[d][e - 1]
            for wd, tag in ARMS:
                a = arms[(d, wd, tag)]; dl = a.train[t1].astype(np.float64) - a.train[t0].astype(np.float64)
                edge.append(dl[o[q * Q - 256:q * Q]].mean() - dl[o[q * Q:q * Q + 256]].mean())
    print(f"  orders: last 256 sequences trained in the quarter minus the first 256 after it: mean {np.mean(edge):+.4f} nats, below -0.05 in {int((np.array(edge) < -0.05).sum())}/{len(edge)}")

    def psub(d, wd, tag, ep, mask):
        return exponent(W[d][mask], arms[(d, wd, tag)].gain(ep)[mask])

    # ------------------------------------------------------------------ 1. seen and not-yet-seen
    print("\n1. SEEN AND NOT-YET-SEEN SEQUENCES")
    print("   p*(sequences already trained in the current epoch) - p*(sequences not yet trained in it), same model and readout.")
    for wd, tag in ARMS:
        print(f"  {wd} at {tag[2:]}:")
        for ep, e, k in [(0.25, 1, 1), (0.5, 1, 2), (2.25, 3, 1), (2.5, 3, 2), (2.75, 3, 3), (3.25, 4, 1), (3.5, 4, 2)]:
            v = []
            for d in DRAWS:
                seen = QTR[d][e - 1] <= k
                v.append(psub(d, wd, tag, ep, seen) - psub(d, wd, tag, ep, ~seen))
            print(f"    epoch {ep:<4} (seen {k}/4 of the set): {show(f'seen_minus_unseen|{wd}|{tag}|{ep}', v)}")

    # ------------------------------------------------------------------ 2. fixed sets
    print("\n2. FIXED SETS ACROSS EACH QUARTER-EPOCH INTERVAL")
    print("   T = the 4,096 sequences trained in the interval; O = the other 12,288. Mean p* before -> after, and the change with its interval.")
    print("   'boundary' marks the first quarter after an epoch boundary.")
    for wd, tag in ARMS:
        print(f"  {wd} at {tag[2:]}:")
        for (t0, t1, e, q) in INTS[2:]:
            whole, dT, dO, T0, T1, O0, O1 = [], [], [], [], [], [], []
            for d in DRAWS:
                T = QTR[d][e - 1] == q
                whole.append(FIT[(d, t1, wd, tag)] - FIT[(d, t0, wd, tag)])
                a0, a1, b0, b1 = psub(d, wd, tag, t0, T), psub(d, wd, tag, t1, T), psub(d, wd, tag, t0, ~T), psub(d, wd, tag, t1, ~T)
                T0.append(a0); T1.append(a1); O0.append(b0); O1.append(b1); dT.append(a1 - a0); dO.append(b1 - b0)
            key = f"{wd}|{tag}|{t0}-{t1}"
            print(f"    {t0:<4} -> {t1:<4}{' boundary' if q == 1 else '         '}: whole set {show('fixed|whole|' + key, whole, 4, False)} | "
                  f"T {np.mean(T0):.4f} -> {np.mean(T1):.4f}, {show('fixed|T|' + key, dT, 4, False)} | "
                  f"O {np.mean(O0):.4f} -> {np.mean(O1):.4f}, {show('fixed|O|' + key, dO, 4, False)}, falls in {int(sum(x < 0 for x in dO))}/6")
    print("   Excess of the whole-set rise in the first quarter after a boundary over the rise in the next quarter, and the same excess for T and for O:")
    for wd, tag in ARMS:
        for i1, i2 in [("2.0-2.25", "2.25-2.5"), ("3.0-3.25", "3.25-3.5")]:
            f = lambda s: np.array(RESULTS[f"fixed|{s}|{wd}|{tag}|{i1}"]) - np.array(RESULTS[f"fixed|{s}|{wd}|{tag}|{i2}"])
            print(f"    {wd} at {tag[2:]}, [{i1}] minus [{i2}]: whole set {show(f'excess|whole|{wd}|{tag}|{i1}', f('whole'), 4, False)}; "
                  f"T {show(f'excess|T|{wd}|{tag}|{i1}', f('T'), 4, False)}; O {show(f'excess|O|{wd}|{tag}|{i1}', f('O'), 4, False)}")

    # ------------------------------------------------------------------ 3. exposure-matched contrasts
    print("\n3. EXPOSURE-MATCHED CONTRASTS: 512 AT EPOCH 3 AGAINST 768 AT EPOCH 2 + k/4")
    print("   A sequence in quarters (a, b, c) of epochs 1-3 was trained at times a, 4 + b, 8 + c (quarter epochs).")
    print("   whole set    : all 16,384 sequences in both models (768 has trained on only k/4 of them a third time).")
    print("   last pass    : 768 on its quarters c <= k of epoch 3, 512 on its quarters c >= 5 - k: three passes each, and the same")
    print("                  time since the third pass; the timing of passes 1 and 2 is not matched.")
    print("   every pass   : 768 on sequences with a, b, c <= k, 512 on sequences with a, b, c >= 5 - k: the same time since each of")
    print("                  the three passes. The two models' sets are different sequences (about N (k/4)^3 each).")
    print("   k = 4 is the equal-updates comparison (S3 and S5): the same sequences, with identical exposure.")
    for tag in (LO, HI):
        print(f"  {tag[2:]}:")
        for k in (1, 2, 3, 4):
            ep7 = 2 + k / 4; rows = {x: [] for x in ("whole", "last", "every", "loss_whole", "loss_last", "loss_every", "n")}
            for d in DRAWS:
                a, b, c, _ = QTR[d]; a5, a7 = arms[(d, 512, tag)], arms[(d, 768, tag)]
                l5, l7 = c >= 5 - k, c <= k
                e5, e7 = l5 & (a >= 5 - k) & (b >= 5 - k), l7 & (a <= k) & (b <= k)
                rows["whole"].append(FIT[(d, 3.0, 512, tag)] - FIT[(d, ep7, 768, tag)])
                rows["last"].append(psub(d, 512, tag, 3.0, l5) - psub(d, 768, tag, ep7, l7))
                rows["every"].append(psub(d, 512, tag, 3.0, e5) - psub(d, 768, tag, ep7, e7))
                rows["loss_whole"].append(a5.loss(3.0) - a7.loss(ep7))
                rows["loss_last"].append(a5.loss(3.0, l5) - a7.loss(ep7, l7))
                rows["loss_every"].append(a5.loss(3.0, e5) - a7.loss(ep7, e7))
                rows["n"].append((int(e5.sum()), int(e7.sum())))
            key = f"matched|{tag}|k{k}"
            n5, n7 = np.mean([x[0] for x in rows["n"]]), np.mean([x[1] for x in rows["n"]])
            print(f"    768 at epoch {ep7:<4}: whole set  {show(key + '|whole', rows['whole'])}; training-loss difference {show(key + '|loss_whole', rows['loss_whole'], 3, False)}")
            if k < 4:
                print(f"                       last pass  {show(key + '|last', rows['last'])}; training-loss difference {show(key + '|loss_last', rows['loss_last'], 3, False)}")
                print(f"                       every pass {show(key + '|every', rows['every'])}; training-loss difference {show(key + '|loss_every', rows['loss_every'], 3, False)}; "
                      f"sequences per draw {n5:.0f} and {n7:.0f}")
                print(f"                       whole set minus every pass {show(key + '|whole_minus_every', np.array(rows['whole']) - np.array(rows['every']))}; "
                      f"last pass minus every pass {show(key + '|last_minus_every', np.array(rows['last']) - np.array(rows['every']))}")
    print("   Pooled over k = 1, 2, 3 within each draw (unweighted mean of the three contrasts):")
    for tag in (LO, HI):
        for s in ("whole", "last", "every", "whole_minus_every"):
            v = np.mean([RESULTS[f"matched|{tag}|k{k}|{s}"] for k in (1, 2, 3)], 0)
            print(f"    {tag[2:]} {s.replace('_', ' '):18s}: {show(f'matched|{tag}|pooled|{s}', v)}")
    print("   Within one model: does the timing of an earlier pass matter? Sequences trained a third time in quarter 1 of epoch 3,")
    print("   read at epoch 2.25: p*(second pass in quarters 3-4 of epoch 2) - p*(second pass in quarters 1-2 of epoch 2).")
    for wd, tag in ARMS:
        v = []
        for d in DRAWS:
            _, b, c, _ = QTR[d]
            v.append(psub(d, wd, tag, 2.25, (c == 1) & (b >= 3)) - psub(d, wd, tag, 2.25, (c == 1) & (b <= 2)))
        print(f"    {wd} at {tag[2:]}: {show(f'second_pass_late_minus_early|{wd}|{tag}', v)}")

    # ------------------------------------------------------------------ 4. each width at its better rate
    print("\n4. EACH WIDTH AT ITS BETTER RATE (from POINTS.csv): 512 AT 3e-4 AGAINST 768 AT 1e-4")
    print("   Rate effects at epoch 3, 1e-4 minus 3e-4 (as RESULT.md section 6c):")
    for wd in (512, 768):
        for name, f in (("training loss", "train"), ("validation loss", "val"), ("p*", "p")):
            v = [P[(d, 3.0, wd, LO)][f] - P[(d, 3.0, wd, HI)][f] for d in DRAWS]
            print(f"    {wd} {name:15s}: {show(f'rate_effect|{wd}|{f}', v)}")
    print("   So at epoch 3 the rate with the lower validation loss is 3e-4 for 512 and 1e-4 for 768 (of the two rates tested; neither")
    print("   width's best rate is located). 512's training loss is also lower at 3e-4; 768's hardly differs between the rates.")
    print("   Equal updates, 512 at 3e-4 minus 768 at 1e-4, at every readout:")
    for ep in [0.25, 0.5, 1.0] + PATH:
        v = [P[(d, ep, 512, HI)]["p"] - P[(d, ep, 768, LO)]["p"] for d in DRAWS]
        l = [P[(d, ep, 512, HI)]["train"] - P[(d, ep, 768, LO)]["train"] for d in DRAWS]
        print(f"    epoch {ep:<4}: p* {show(f'better_rate|equal_updates|{ep}', v, 5)}; training-loss difference {show(f'better_rate|loss|{ep}', l, 4, False)}")

    def matched(tag5, tag7, later_end=False):
        """The registered rule: 768's p* read by linear interpolation at the training loss 512 reaches at epoch 3, in the first
        bracket in readout order along epochs 2-3.5. later_end: 768 read at the later readout of that bracket instead."""
        out, where = [], []
        for d in DRAWS:
            tgt = P[(d, 3.0, 512, tag5)]["train"]
            pts = [(P[(d, e, 768, tag7)]["train"], P[(d, e, 768, tag7)]["p"], e) for e in PATH]
            for (x0, y0, e0), (x1, y1, e1) in zip(pts, pts[1:]):
                if min(x0, x1) <= tgt <= max(x0, x1):
                    t = (tgt - x0) / (x1 - x0)
                    out.append(P[(d, 3.0, 512, tag5)]["p"] - (y1 if later_end else y0 + t * (y1 - y0))); where.append(e0 + t * (e1 - e0)); break
        return out, where

    v, where = matched(HI, LO)
    print(f"   Equal training loss (the registered interpolation rule applied to this pair): {show('better_rate|equal_loss', v, 5)}")
    print("     768 read at epochs " + ", ".join(f"{d} {x:.3f}" for d, x in zip(DRAWS, where)))
    v, _ = matched(HI, LO, True)
    print(f"     with 768 read at the later end of each bracket: {show('better_rate|equal_loss_later_end', v, 5)}")

    # ------------------------------------------------------------------ 5. equal updates at every readout
    print("\n5. THE EQUAL-UPDATES CONTRAST 512 - 768 AT EVERY READOUT (from POINTS.csv; RESULT.md section 6a)")
    for ep in [0.25, 0.5, 1.0] + PATH:
        line = []
        for tag in (LO, HI):
            v = [P[(d, ep, 512, tag)]["p"] - P[(d, ep, 768, tag)]["p"] for d in DRAWS]
            m, lo, hi = interval(v)
            side = "above 0" if lo > 0 else "below 0" if hi < 0 else "includes 0"
            line.append(f"{tag[2:]} {show(f'equal_updates|{tag}|{ep}', v, 5)} ({side})")
        print(f"    epoch {ep:<4}: " + "; ".join(line))

    # ------------------------------------------------------------------ 6. where the matched readings fall; validation loss
    print("\n6. WHERE THE REGISTERED MATCHED READINGS FALL, AND VALIDATION LOSS BY QUARTER")
    for name, tag in (("P1 (1e-4)", LO), ("S4 (3e-4)", HI)):
        v, where = matched(tag, tag); u, _ = matched(tag, tag, True)
        print(f"  {name}: {show('registered|' + name[:2], v, 5)}; 768 read at epochs " + ", ".join(f"{d} {x:.3f}" for d, x in zip(DRAWS, where)))
        print(f"     per draw: " + ", ".join(f"{d} {x:+.5f}" for d, x in zip(DRAWS, v)))
        print(f"     later end of each bracket: {show('registered_later_end|' + name[:2], u, 5)}; per draw: " + ", ".join(f"{d} {x:+.5f}" for d, x in zip(DRAWS, u)))
    print("  Change of mean validation loss over each step between readouts (nats per token), from POINTS.csv:")
    for wd, tag in ARMS:
        cells = []
        for e0, e1 in zip(PATH, PATH[1:]):
            v = [P[(d, e1, wd, tag)]["val"] - P[(d, e0, wd, tag)]["val"] for d in DRAWS]
            RESULTS[f"validation_step|{wd}|{tag}|{e0}-{e1}"] = v
            cells.append(f"{e0}->{e1} {np.mean(v):+.4f} ({int(sum(x > 0 for x in v))}/6 rise)")
        print(f"    {wd} at {tag[2:]}: " + "; ".join(cells))
    for wd, tag in ARMS:
        v = [P[(d, 3.25, wd, tag)]["val"] - P[(d, 3.0, wd, tag)]["val"] for d in DRAWS]
        print(f"    {wd} at {tag[2:]}, epoch 3 -> 3.25: {show(f'validation_3_to_3.25|{wd}|{tag}', v)}")

    if results_path:
        Path(results_path).write_text(json.dumps(dict(
            note="Per-draw values (m01..m06) behind every interval printed by posthoc_exposure.py. Post hoc and descriptive.",
            numpy=np.__version__, torch=torch.__version__, values=RESULTS), indent=1) + "\n", encoding="utf-8")
    print("\nDONE")


if __name__ == "__main__":
    if len(sys.argv) not in (2, 3):
        sys.exit(__doc__)
    main(*sys.argv[1:])
