#!/usr/bin/env python
"""Phase 2, SECOND PASS (after the freeze, labelled as such): evidence for classifying the discrepancies.

Imports the frozen module code/n7_repro.py unchanged; writes nothing into the frozen folders.

Usage: python -I -B second_pass_checks.py <code folder> <bundle folder> <published folder>
"""
import csv
import json
import math
import os
import sys

import numpy as np

sys.path.insert(0, sys.argv[1])
import n7_repro as R  # noqa: E402

BUNDLE, PUB = sys.argv[2], sys.argv[3]
data, _ = R.load_bundle(BUNDLE)
with open(os.path.join(PUB, "FITS.csv"), encoding="utf-8", newline="") as f:
    fits = list(csv.DictReader(f))
with open(os.path.join(PUB, "ANALYSIS.json"), encoding="utf-8") as f:
    pub = json.load(f)
with open(os.path.join(PUB, "MATCHED.csv"), encoding="utf-8", newline="") as f:
    matched = list(csv.DictReader(f))

# ---- 1. Where does the remaining difference in p* come from?
print("1. Stationarity of the published p* under each tie reading (all 240 fits)")
fitters = {}
rows = []
for r in fits:
    draw, width, tag, epoch = r["draw"], int(r["width"]), r["tag"], float(r["epoch"])
    k = R.READOUTS.index(epoch)
    dw = data[draw]["widths"][width]
    gain = (dw["E0"][:R.N_TRAIN] - dw["arms"][tag]["arrays"][k][:R.N_TRAIN]).astype(np.float64)
    p_pub = float(r["p"])
    out = {"key": (draw, width, tag, epoch), "p_pub": p_pub, "neg_frac": float((gain < 0).mean()),
           "neg_frac_pub": float(r["negative_fraction"]), "J0_pub": float(r["J0"]), "obj_pub": float(r["objective"])}
    for ties in ("ordinal", "ecdf"):
        if (draw, ties) not in fitters:
            fitters[(draw, ties)] = R.Fitter(data[draw]["weights"], ties)
        ft = fitters[(draw, ties)]
        gt = (gain / gain.sum())[ft.order]
        mine = ft.fit(gain)
        j_pub, dj_pub = ft.exact(gt, p_pub)
        h = 1e-4
        curv = (ft.exact(gt, p_pub + h)[1] - ft.exact(gt, p_pub - h)[1]) / (2 * h)
        out[ties] = {"p_mine": mine["p"], "dp": mine["p"] - p_pub, "newton_step_from_pub": -dj_pub / curv,
                     "J_at_pub": j_pub, "J_at_mine": mine["objective"], "dJ_at_mine": ft.exact(gt, mine["p"])[1],
                     "dJ_at_pub": dj_pub, "J0": ft.exact(gt, 0.0)[0]}
    rows.append(out)
for ties in ("ordinal", "ecdf"):
    dps = np.array([r[ties]["dp"] for r in rows])
    newt = np.array([r[ties]["newton_step_from_pub"] for r in rows])
    relobj = np.array([r[ties]["J_at_pub"] / r["obj_pub"] - 1 for r in rows])
    relj0 = np.array([r[ties]["J0"] / r["J0_pub"] - 1 for r in rows])
    excess = np.array([r[ties]["J_at_pub"] - r[ties]["J_at_mine"] for r in rows])
    print("  ties=%-7s max|p_mine - p_pub| = %.3e ; max|(p_mine - p_pub) - Newton step from p_pub| = %.3e ; "
          "max|dJ/dp at mine| = %.2e ; max|dJ/dp at published| = %.2e"
          % (ties, np.abs(dps).max(), np.abs(dps - newt).max(), max(abs(r[ties]["dJ_at_mine"]) for r in rows),
             max(abs(r[ties]["dJ_at_pub"]) for r in rows)))
    print("                max rel |J(p_pub) (my evaluation) / published objective - 1| = %.3e ; max rel |J(0) / published J0 - 1| = %.3e ; "
          "fits where J(p_pub) < J(p_mine): %d (min excess %.2e, max %.2e)"
          % (np.abs(relobj).max(), np.abs(relj0).max(), int((excess < 0).sum()), excess.min(), excess.max()))
print("  negative_fraction: max |mine - published| = %.3e" % max(abs(r["neg_frac"] - r["neg_frac_pub"]) for r in rows))

# ---- 2. Tie order: is the published objective the stable-sort ordinal one?
print("2. Tie order check (objective at the published p, three orderings of tied weights), one fit per draw at E3, 512, 1e-4")
for draw in R.DRAWS:
    w = data[draw]["weights"].astype(np.float64)
    r = next(x for x in rows if x["key"] == (draw, 512, "lr1e-04", 3.0))
    dw = data[draw]["widths"][512]
    gain = (dw["E0"][:R.N_TRAIN] - dw["arms"]["lr1e-04"]["arrays"][7][:R.N_TRAIN]).astype(np.float64)
    gt = gain / gain.sum()

    def obj(order, p, idx=None):
        b = np.exp(p * np.log(w[order]))
        b /= b.sum()
        c = np.cumsum(gt[order] - b)
        return float(np.dot(c[:-1], c[:-1])) / w.size
    stable = np.argsort(w, kind="stable")
    rev = np.lexsort((-np.arange(w.size), w))      # ties in reverse sequence order
    n_tied = int(w.size - np.unique(w).size)
    print("  %s: tied surplus values %d ; rel diff to published objective: stable %.2e, reversed ties %.2e, ecdf %.2e"
          % (draw, n_tied, obj(stable, r["p_pub"]) / r["obj_pub"] - 1, obj(rev, r["p_pub"]) / r["obj_pub"] - 1,
             r["ecdf"]["J_at_pub"] / r["obj_pub"] - 1))

# ---- 3. The published t critical value and the t-test p-values (not registered in the protocol)
print("3. t quantile: mine %.15f, published %s, difference %.2e" % (R.t_crit(5), pub["statistics"]["P1"]["interval"]["t_critical"],
                                                                     R.t_crit(5) - pub["statistics"]["P1"]["interval"]["t_critical"]))
for s in ("P1", "S1", "S3", "S4", "S5"):
    pi = pub["statistics"][s]["interval"]
    t = pi["mean"] / pi["se"]
    p2 = 2 * (1 - R.t_cdf(abs(t), pi["df"]))
    print("   %s: published t-test p = %.12g ; recomputed two-sided p = %.12g ; published se - sd/sqrt(n) = %.1e"
          % (s, pi["p"], p2, pi["se"] - pi["sd"] / math.sqrt(pi["n"])))

# ---- 4. Internal consistency of the published tables
bad = 0
for r in matched:
    row = pub["statistics"][r["statistic"]]["rows"][r["draw"]]
    for col, key in (("value", "value"), ("p_read", "p_read"), ("p_first", "p_first"), ("target", "target"), ("weight", "weight"),
                     ("read_at_readout", "read_at_readout")):
        a = r[col]
        b = row.get(key)
        if (a == "") != (b is None) or (a != "" and float(a) != float(b)):
            bad += 1
    if r["status"] != row["status"]:
        bad += 1
print("4. MATCHED.csv against ANALYSIS.json rows: %d rows, %d cell mismatches" % (len(matched), bad))
# recompute every published interval from the published per-draw values
worst = 0.0
for s, st in pub["statistics"].items():
    if "interval" not in st:
        continue
    v = [st["values"][d] for d in st["available"]]
    ti = R.t_interval(v)
    worst = max(worst, abs(ti["mean"] - st["interval"]["mean"]), abs(ti["ci_low"] - st["interval"]["interval"][0]),
                abs(ti["ci_high"] - st["interval"]["interval"][1]), abs(ti["sd"] - st["interval"]["sd"]))
    for d, lo in st["leave_one_out"].items():
        rest = [st["values"][x] for x in st["available"] if x != d]
        tj = R.t_interval(rest)
        worst = max(worst, abs(tj["mean"] - lo["mean"]), abs(tj["ci_low"] - lo["interval"][0]), abs(tj["ci_high"] - lo["interval"][1]))
print("   published intervals and leave-one-out intervals recomputed from the published per-draw values: max |diff| = %.2e" % worst)

# ---- 5. Size of the loss-source ambiguity on each matched value (record losses vs array means), same fits
print("5. Effect of the loss source alone (ordinal fits; array means minus record values), per matched statistic and draw")
for step, name, kind, rate, var, expected in R.STATISTICS:
    if kind != "matched":
        continue
    line = []
    for draw in R.DRAWS:
        vals = {}
        for src in ("array", "record"):
            def loss(width, epoch):
                k = R.READOUTS.index(epoch)
                arm = data[draw]["widths"][width]["arms"][rate]
                if src == "array":
                    tr = float(arm["arrays"][k][:R.N_TRAIN].astype(np.float64).mean())
                    va = float(arm["arrays"][k][R.N_TRAIN:].astype(np.float64).mean())
                else:
                    tr = arm["record"]["readouts"][k]["train_loss"]
                    va = arm["record"]["readouts"][k]["validation_loss"]
                return {"train": tr, "val": va, "gap": va - tr}[var]
            rd = R.matched_reading(loss(512, 3), [loss(768, e) for e in R.PATH], R.PATH)
            if not rd["held"]:
                vals[src] = None
                continue
            pa = next(x for x in rows if x["key"] == (draw, 768, rate, float(rd["lo"])))["ordinal"]["p_mine"]
            pb = next(x for x in rows if x["key"] == (draw, 768, rate, float(rd["hi"])))["ordinal"]["p_mine"]
            p5 = next(x for x in rows if x["key"] == (draw, 512, rate, 3.0))["ordinal"]["p_mine"]
            vals[src] = p5 - (pa + rd["weight"] * (pb - pa))
        line.append("%s %s" % (draw, "n/a" if vals["array"] is None else "%.2e" % (vals["array"] - vals["record"])))
    print("   %s %-10s %s" % (step, name, "  ".join(line)))
