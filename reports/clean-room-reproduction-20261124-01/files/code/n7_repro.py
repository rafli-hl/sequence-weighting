#!/usr/bin/env python
"""Clean-room reproduction of the analysis of N7 (matched-progress confirmation).

Written from PROTOCOL.md (v2.1 sealed source), the Jane Street technical note and the released bundle
n7-loss-arrays-v1.zip only. NumPy only. See SPEC_LOG.md for every reading of the specification (Q1..Q33).

Usage:
    python -I -B n7_repro.py --bundle <path to n7-loss-arrays> --out <output folder> [--selftest]

Writes, for each of four variants (ties in {ecdf, ordinal} x losses in {arrays, record}):
    <out>/<variant>/per_readout.csv   one row per draw, width, rate, readout (240 rows)
    <out>/<variant>/matched.csv       one row per matched statistic and draw
    <out>/<variant>/contrasts.csv     one row per registered statistic and draw
    <out>/<variant>/analysis.json     statistics, sequence, labels, diagnostics, descriptives
The primary variant is ecdf_arrays.
"""
import argparse
import csv
import hashlib
import json
import math
import os
import sys

import numpy as np

N_TRAIN = 16384
N_VAL = 512
READOUTS = [0.25, 0.5, 1, 2, 2.25, 2.5, 2.75, 3, 3.25, 3.5]
PATH = [2, 2.25, 2.5, 2.75, 3, 3.25, 3.5]
E3 = 3
E2 = 2
DRAWS = ["m01", "m02", "m03", "m04", "m05", "m06"]
WIDTHS = [512, 768]
RATES = ["lr1e-04", "lr3e-04"]
BOUND = 8.0
REFIT_BOUND = 32.0
SAT_MARGIN = 0.001
GRID_STEP = 0.02
MIN_DRAWS = 5

# (step, name, kind, rate, matching variable, expected side)
STATISTICS = [
    ("P1", "D4m_train", "matched", "lr1e-04", "train", "above"),
    ("S1", "D4m_gap", "matched", "lr1e-04", "gap", "above"),
    ("S3", "D4_fixed_E3", "fixed", "lr1e-04", None, "below"),
    ("S4", "D2m_train", "matched", "lr3e-04", "train", "above"),
    ("S5", "D2_fixed_E3", "fixed", "lr3e-04", None, "above"),
    ("S2", "D4m_val", "matched", "lr1e-04", "val", "above"),
]


# ----------------------------------------------------------------------------------------------
# t distribution (no SciPy): regularised incomplete beta by Lentz's continued fraction
# ----------------------------------------------------------------------------------------------
def _betacf(a, b, x):
    tiny = 1e-300
    qab, qap, qam = a + b, a + 1.0, a - 1.0
    c = 1.0
    d = 1.0 - qab * x / qap
    if abs(d) < tiny:
        d = tiny
    d = 1.0 / d
    h = d
    for m in range(1, 10000):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        if abs(d) < tiny:
            d = tiny
        c = 1.0 + aa / c
        if abs(c) < tiny:
            c = tiny
        d = 1.0 / d
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        if abs(d) < tiny:
            d = tiny
        c = 1.0 + aa / c
        if abs(c) < tiny:
            c = tiny
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < 1e-16:
            return h
    raise RuntimeError("betacf did not converge")


def betai(a, b, x):
    if x <= 0.0:
        return 0.0
    if x >= 1.0:
        return 1.0
    front = math.exp(a * math.log(x) + b * math.log1p(-x) - (math.lgamma(a) + math.lgamma(b) - math.lgamma(a + b)))
    if x < (a + 1.0) / (a + b + 2.0):
        return front * _betacf(a, b, x) / a
    return 1.0 - front * _betacf(b, a, 1.0 - x) / b


def t_cdf(t, df):
    tail = 0.5 * betai(0.5 * df, 0.5, df / (df + t * t))
    return 1.0 - tail if t >= 0 else tail


def t_ppf(q, df):
    """Quantile for q > 0.5 by bisection on the CDF."""
    lo, hi = 0.0, 1.0
    while t_cdf(hi, df) < q:
        hi *= 2.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if t_cdf(mid, df) < q:
            lo = mid
        else:
            hi = mid
        if hi - lo < 1e-13:
            break
    return 0.5 * (lo + hi)


_TCRIT = {}


def t_crit(df):
    if df not in _TCRIT:
        _TCRIT[df] = t_ppf(0.975, df)
    return _TCRIT[df]


# ----------------------------------------------------------------------------------------------
# The estimator
# ----------------------------------------------------------------------------------------------
class Fitter:
    """p* = argmin over [0, bound] of d(p)' K d(p), K_ij = min(r_i, r_j), for one weight vector.

    ties = "ecdf":    r_i = #{j: w_j <= w_i} / N (tied weights share a rank)       [primary, Q4]
    ties = "ordinal": r_i = position in a stable ascending sort / N                [variant, Q4]
    In both cases J(p) = (1/N) * sum_k C[idx_k]^2 with C the cumulative sum of d in sorted order.
    """

    def __init__(self, weights_f32, ties):
        w = np.asarray(weights_f32).astype(np.float64)
        if not np.all(np.isfinite(w)) or np.any(w <= 0):
            raise ValueError("weights must be finite and positive")
        self.n = w.size
        self.order = np.argsort(w, kind="stable")
        ws = w[self.order]
        self.uniform = bool(ws[0] == ws[-1])
        lw = np.log(ws)
        self.lw = lw - lw[-1]
        new = np.empty(self.n, dtype=bool)
        new[0] = True
        new[1:] = ws[1:] != ws[:-1]
        self.n_distinct = int(new.sum())
        if ties == "ecdf":
            gid = np.cumsum(new) - 1
            ends = np.flatnonzero(np.append(new[1:], True))
            k = np.flatnonzero(gid >= 1)
            self.idx = ends[gid[k] - 1]
        elif ties == "ordinal":
            self.idx = np.arange(self.n - 1)
        else:
            raise ValueError(ties)
        self.ties = ties
        self._cache = {}

    def _basis(self, ps):
        e = np.exp(np.outer(ps, self.lw))
        b = e / e.sum(axis=1, keepdims=True)
        mu = (b * self.lw).sum(axis=1, keepdims=True)
        cb = np.cumsum(b, axis=1)[:, self.idx]
        dcb = np.cumsum(b * (self.lw - mu), axis=1)[:, self.idx]
        return cb, dcb

    def scan(self, gt, bound):
        """J and dJ/dp on the uniform grid (used only to find brackets)."""
        npts = int(round(bound / GRID_STEP)) + 1
        grid = np.linspace(0.0, bound, npts)
        cg = np.cumsum(gt)[self.idx]
        j = np.empty(npts)
        dj = np.empty(npts)
        chunk = 96
        for start in range(0, npts, chunk):
            sl = slice(start, min(start + chunk, npts))
            key = (bound, start)
            if bound == BOUND:
                if key not in self._cache:
                    self._cache[key] = self._basis(grid[sl])
                cb, dcb = self._cache[key]
            else:
                cb, dcb = self._basis(grid[sl])
            r = cg - cb
            j[sl] = np.einsum("ij,ij->i", r, r) / self.n
            dj[sl] = -2.0 * np.einsum("ij,ij->i", r, dcb) / self.n
        return grid, j, dj

    def exact(self, gt, p):
        """J(p) and dJ/dp at one p, from the cumulative sum of d itself."""
        e = np.exp(p * self.lw)
        b = e / e.sum()
        mu = float((b * self.lw).sum())
        c = np.cumsum(gt - b)[self.idx]
        dc = -np.cumsum(b * (self.lw - mu))[self.idx]
        return float(np.dot(c, c)) / self.n, 2.0 * float(np.dot(c, dc)) / self.n

    def fit(self, gain, bound=BOUND):
        """gain: float64 array in sequence order. Returns a dict; 'defined' False with a reason if undefined."""
        g = np.asarray(gain, dtype=np.float64)
        out = {"defined": False, "reason": "", "p": None, "objective": None, "bound": bound,
               "n_candidates": 0, "p_golden": None, "total_gain": None}
        if not np.all(np.isfinite(g)):
            out["reason"] = "nonfinite gain"
            return out
        total = float(g.sum())
        out["total_gain"] = total
        if not (total > 0.0):
            out["reason"] = "nonpositive total gain"
            return out
        if self.uniform:
            out["reason"] = "uniform weights"
            return out
        gt = (g / total)[self.order]
        grid, j, dj = self.scan(gt, bound)
        if not (np.all(np.isfinite(j)) and np.all(np.isfinite(dj))):
            out["reason"] = "nonfinite objective"
            return out
        last = grid.size - 1
        cands = []
        for k in range(grid.size):
            if k > 0 and j[k] > j[k - 1]:
                continue
            if k < last and j[k] > j[k + 1]:
                continue
            lo_i, hi_i = max(k - 1, 0), min(k + 1, last)
            br = None
            if lo_i < k and dj[lo_i] < 0.0 <= dj[k]:
                br = (grid[lo_i], grid[k])
            elif k < hi_i and dj[k] < 0.0 < dj[hi_i]:
                br = (grid[k], grid[hi_i])
            if br is not None:
                p = self._bisect(gt, br[0], br[1])
            elif k == 0 and dj[0] >= 0.0:
                p = 0.0
            elif k == last and dj[last] <= 0.0:
                p = float(bound)
            else:
                p = float(grid[k])
            cands.append((self.exact(gt, p)[0], p, (float(grid[lo_i]), float(grid[hi_i]))))
        cands.sort(key=lambda c: (c[0], c[1]))
        jbest, pbest, bracket = cands[0]
        out.update(defined=True, p=float(pbest), objective=float(jbest), n_candidates=len(cands),
                   p_golden=float(self._golden(gt, bracket[0], bracket[1])))
        return out

    def _bisect(self, gt, lo, hi):
        for _ in range(200):
            mid = 0.5 * (lo + hi)
            if self.exact(gt, mid)[1] < 0.0:
                lo = mid
            else:
                hi = mid
            if hi - lo < 1e-13:
                break
        return 0.5 * (lo + hi)

    def _golden(self, gt, a, b):
        """Independent cross-check: golden-section search on J itself."""
        invphi = (math.sqrt(5.0) - 1.0) / 2.0
        c = b - invphi * (b - a)
        d = a + invphi * (b - a)
        fc = self.exact(gt, c)[0]
        fd = self.exact(gt, d)[0]
        for _ in range(200):
            if b - a < 1e-10:
                break
            if fc < fd:
                b, d, fd = d, c, fc
                c = b - invphi * (b - a)
                fc = self.exact(gt, c)[0]
            else:
                a, c, fc = c, d, fd
                d = a + invphi * (b - a)
                fd = self.exact(gt, d)[0]
        return 0.5 * (a + b)


# ----------------------------------------------------------------------------------------------
# Loading
# ----------------------------------------------------------------------------------------------
def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def load_bundle(root):
    """Checks every file against MANIFEST.json and returns the raw arrays and records."""
    with open(os.path.join(root, "MANIFEST.json"), encoding="utf-8") as f:
        man = json.load(f)
    checked = 0

    def check(ent):
        nonlocal checked
        p = os.path.join(root, *ent["path"].split("/"))
        if os.path.getsize(p) != ent["bytes"] or sha256_file(p) != ent["sha256"]:
            raise RuntimeError("manifest mismatch: " + ent["path"])
        checked += 1
        return p

    data = {}
    for draw in sorted(man["draws"]):
        md = man["draws"][draw]
        if md["n_train"] != N_TRAIN or md["readouts"] != READOUTS:
            raise RuntimeError("unexpected layout in " + draw)
        w = np.fromfile(check(md["weights"]), dtype="<f4")
        if w.size != N_TRAIN:
            raise RuntimeError("weights size")
        dd = {"weights": w, "run": md["run"], "widths": {}}
        for width in WIDTHS:
            mw = md["widths"][str(width)]
            e0 = np.fromfile(check(mw["E0"]), dtype="<f4")
            if e0.size != N_TRAIN + N_VAL:
                raise RuntimeError("E0 size")
            dw = {"E0": e0, "arms": {}}
            for rate in RATES:
                ma = mw["arms"][rate]
                arr = np.fromfile(check(ma["arrays"]), dtype="<f4")
                if arr.size != len(READOUTS) * (N_TRAIN + N_VAL):
                    raise RuntimeError("arrays size")
                with open(check(ma["record"]), encoding="utf-8") as f:
                    rec = json.load(f)
                if rec["layout"]["block_epochs"] != READOUTS or rec["layout"]["train_rows"] != N_TRAIN \
                        or rec["layout"]["validation_rows"] != N_VAL or rec["width"] != width or rec["tag"] != rate \
                        or rec["stage"] != draw or [r["epoch"] for r in rec["readouts"]] != READOUTS:
                    raise RuntimeError("unexpected record in %s %s %s" % (draw, width, rate))
                dw["arms"][rate] = {"arrays": arr.reshape(len(READOUTS), N_TRAIN + N_VAL), "record": rec}
            dd["widths"][width] = dw
        data[draw] = dd
    return data, checked


# ----------------------------------------------------------------------------------------------
# Per-readout quantities (fits for both tie readings, losses from both sources)
# ----------------------------------------------------------------------------------------------
def compute_points(data, log=print):
    points = {}  # key (draw, width, rate, readout) -> dict
    e0 = {}
    for draw in sorted(data):
        dd = data[draw]
        fitters = {t: Fitter(dd["weights"], t) for t in ("ecdf", "ordinal")}
        for width in WIDTHS:
            dw = dd["widths"][width]
            e0_train = dw["E0"][:N_TRAIN]
            e0[(draw, width)] = {"train": float(e0_train.astype(np.float64).mean()),
                                 "val": float(dw["E0"][N_TRAIN:].astype(np.float64).mean())}
            for rate in RATES:
                arm = dw["arms"][rate]
                for k, epoch in enumerate(READOUTS):
                    block = arm["arrays"][k]
                    gain32 = e0_train - block[:N_TRAIN]          # float32 subtraction (Q1)
                    assert gain32.dtype == np.float32
                    gain = gain32.astype(np.float64)
                    rec = arm["record"]["readouts"][k]
                    pt = {
                        "draw": draw, "width": width, "rate": rate, "readout": epoch, "update": rec["update"],
                        "train_array": float(block[:N_TRAIN].astype(np.float64).mean()),
                        "val_array": float(block[N_TRAIN:].astype(np.float64).mean()),
                        "train_record": float(rec["train_loss"]),
                        "val_record": float(rec["validation_loss"]),
                        "fit": {t: fitters[t].fit(gain) for t in fitters},
                        "gain": gain,
                    }
                    points[(draw, width, rate, epoch)] = pt
            log("fitted %s w%d" % (draw, width))
        for f in fitters.values():
            f._cache.clear()
    return points, e0


# ----------------------------------------------------------------------------------------------
# Statistics helpers
# ----------------------------------------------------------------------------------------------
def side_of(lo, hi):
    if lo is None or hi is None:
        return "none"
    if lo > 0.0:
        return "above"
    if hi < 0.0:
        return "below"
    return "spans"


def t_interval(vals):
    n = len(vals)
    out = {"n": n, "mean": None, "sd": None, "df": None, "t_crit": None, "ci_low": None, "ci_high": None}
    if n >= 1:
        a = np.asarray(vals, dtype=np.float64)
        out["mean"] = float(a.mean())
    if n >= 2:
        sd = float(a.std(ddof=1))
        tc = t_crit(n - 1)
        half = tc * sd / math.sqrt(n)
        out.update(sd=sd, df=n - 1, t_crit=tc, ci_low=out["mean"] - half, ci_high=out["mean"] + half)
    out["side"] = side_of(out["ci_low"], out["ci_high"])
    return out


def sign_test(vals):
    pos = sum(1 for v in vals if v > 0)
    neg = sum(1 for v in vals if v < 0)
    zero = sum(1 for v in vals if v == 0)
    m = pos + neg
    if m == 0:
        p = 1.0 if vals else None
    else:
        k = min(pos, neg)
        p = min(1.0, 2.0 * sum(math.comb(m, i) for i in range(k + 1)) / 2.0 ** m)
    return {"positive": pos, "negative": neg, "zero": zero, "p_two_sided": p}


def leave_one_out(draws, vals, full_side):
    if len(vals) < 4:
        return None
    rows = []
    for i, d in enumerate(draws):
        rest = [v for j, v in enumerate(vals) if j != i]
        ti = t_interval(rest)
        rows.append({"dropped": d, "n": ti["n"], "mean": ti["mean"], "ci_low": ti["ci_low"],
                     "ci_high": ti["ci_high"], "side": ti["side"]})
    return {"intervals": rows,
            "min_ci_low": min(r["ci_low"] for r in rows),
            "max_ci_high": max(r["ci_high"] for r in rows),
            "all_on_full_side": all(r["side"] == full_side for r in rows)}


def status_of(step, side, n, expected):
    if n < MIN_DRAWS:
        return "UNAVAILABLE"
    if step == "P1":
        return {"above": "REVERSAL_CONFIRMED", "below": "NOT_REVERSED"}.get(side, "INCONCLUSIVE")
    if side == "spans":
        return "INCONCLUSIVE"
    return "CONFIRMED" if side == expected else "CONTRARY"


def matched_reading(target, values, epochs):
    """First closed interval in readout order whose two values hold the target (Q15..Q18)."""
    holds = [min(values[i], values[i + 1]) <= target <= max(values[i], values[i + 1])
             for i in range(len(values) - 1)]
    n_hold = sum(holds)
    if n_hold == 0:
        where = "below the path's minimum" if target < min(values) else "above the path's maximum"
        return {"held": False, "n_intervals": 0, "where": where}
    i = holds.index(True)
    a, b = values[i], values[i + 1]
    weight = 0.0 if a == b else (target - a) / (b - a)
    return {"held": True, "n_intervals": n_hold, "index": i, "lo": epochs[i], "hi": epochs[i + 1],
            "weight": weight, "position": epochs[i] + weight * (epochs[i + 1] - epochs[i])}


# ----------------------------------------------------------------------------------------------
# The analysis for one variant
# ----------------------------------------------------------------------------------------------
def analyse(data, points, e0, ties, losses):
    draws_present = sorted(data)

    def loss(draw, width, rate, epoch, var):
        pt = points[(draw, width, rate, epoch)]
        tr, va = pt["train_" + losses], pt["val_" + losses]
        return {"train": tr, "val": va, "gap": va - tr}[var]

    def fit(draw, width, rate, epoch):
        return points[(draw, width, rate, epoch)]["fit"][ties]

    refits = {}

    def refit(draw, width, rate, epoch):
        key = (draw, width, rate, epoch)
        if key not in refits:
            f = Fitter(data[draw]["weights"], ties)
            refits[key] = f.fit(points[key]["gain"], bound=REFIT_BOUND)
        return refits[key]

    def stat_draw(kind, rate, var, draw, pfun):
        """One draw's value for one statistic. pfun(draw, width, rate, epoch) -> fit dict."""
        row = {"draw": draw, "status": "AVAILABLE", "reason": "", "value": None, "fits_used": []}
        if draw not in data:
            row.update(status="UNAVAILABLE", reason="draw missing")
            return row
        f512 = pfun(draw, 512, rate, E3)
        row["p512_E3"] = f512["p"]
        if kind == "matched":
            target = loss(draw, 512, rate, E3, var)
            vals = [loss(draw, 768, rate, e, var) for e in PATH]
            rd = matched_reading(target, vals, PATH)
            row.update(target=target, path_values=vals, n_intervals=rd["n_intervals"])
            if not f512["defined"]:
                row.update(status="UNAVAILABLE", reason="undefined fit")
                return row
            if not rd["held"]:
                row.update(status="UNAVAILABLE", reason="target outside the path", where=rd["where"])
                return row
            fa, fb = pfun(draw, 768, rate, rd["lo"]), pfun(draw, 768, rate, rd["hi"])
            row.update(bracket_lo=rd["lo"], bracket_hi=rd["hi"], weight=rd["weight"], position=rd["position"],
                       p768_lo=fa["p"], p768_hi=fb["p"])
            if not (fa["defined"] and fb["defined"]):
                row.update(status="UNAVAILABLE", reason="undefined fit")
                return row
            read = fa["p"] + rd["weight"] * (fb["p"] - fa["p"])
            row.update(p768_read=read, value=f512["p"] - read,
                       fits_used=[(512, rate, E3), (768, rate, rd["lo"]), (768, rate, rd["hi"])])
        else:
            f768 = pfun(draw, 768, rate, E3)
            row["p768_E3"] = f768["p"]
            if not (f512["defined"] and f768["defined"]):
                row.update(status="UNAVAILABLE", reason="undefined fit")
                return row
            row.update(value=f512["p"] - f768["p"], fits_used=[(512, rate, E3), (768, rate, E3)])
        return row

    stats = {}
    matched_rows = []
    contrast_rows = []
    confirmed_so_far = True
    for step, name, kind, rate, var, expected in STATISTICS:
        rows = [stat_draw(kind, rate, var, d, fit) for d in DRAWS]
        avail = [r for r in rows if r["status"] == "AVAILABLE"]
        ds = [r["draw"] for r in avail]
        vals = [r["value"] for r in avail]
        ti = t_interval(vals)
        status = status_of(step, ti["side"], ti["n"], expected)
        counts = {"undefined fit": 0, "target outside the path": 0, "draw missing": 0}
        for r in rows:
            if r["status"] != "AVAILABLE":
                counts[r["reason"]] += 1
        # saturation (Q11)
        flagged = []
        for r in avail:
            hit = [k for k in r["fits_used"] if fit(r["draw"], *k)["p"] >= BOUND - SAT_MARGIN]
            if hit:
                flagged.append({"draw": r["draw"], "fits": [list(k) for k in hit]})
        sat = {"flagged": flagged, "label": None}
        if flagged:
            unresolved = False
            for fl in flagged:
                for k in fl["fits"]:
                    rf = refit(fl["draw"], *k)
                    if (not rf["defined"]) or rf["p"] >= REFIT_BOUND - SAT_MARGIN:
                        unresolved = True

            def pfun32(draw, width, rate_, epoch):
                f8 = fit(draw, width, rate_, epoch)
                if f8["defined"] and f8["p"] >= BOUND - SAT_MARGIN:
                    return refit(draw, width, rate_, epoch)
                return f8
            rows32 = [stat_draw(kind, rate, var, d, pfun32) for d in DRAWS]
            ti32 = t_interval([r["value"] for r in rows32 if r["status"] == "AVAILABLE"])
            sat.update(unresolved=unresolved, interval_at_32=ti32)
            if unresolved:
                sat["label"] = "SATURATED"
            elif ti32["side"] != ti["side"]:
                sat["label"] = "SATURATION_SENSITIVE"
        reached = confirmed_so_far
        label = status if reached else "NOT_READ"
        if sat["label"] and reached:
            label = sat["label"]
        is_confirmed = reached and sat["label"] is None and status in ("REVERSAL_CONFIRMED", "CONFIRMED")
        confirmed_so_far = confirmed_so_far and is_confirmed
        stats[step] = {
            "step": step, "name": name, "kind": kind, "rate": rate, "matched_on": var, "expected_side": expected,
            "n_available": ti["n"], "available_draws": ds,
            "unavailable": {r["draw"]: r["reason"] for r in rows if r["status"] != "AVAILABLE"},
            "unavailable_counts": counts,
            "values": {r["draw"]: r["value"] for r in rows},
            "mean": ti["mean"], "sd": ti["sd"], "df": ti["df"], "t_crit": ti["t_crit"],
            "ci_low": ti["ci_low"], "ci_high": ti["ci_high"], "side": ti["side"],
            "status": status, "reached": reached, "label": label,
            "sign_test": sign_test(vals), "leave_one_out": leave_one_out(ds, vals, ti["side"]),
            "saturation": sat,
        }
        for r in rows:
            contrast_rows.append([step, name, r["draw"], r["status"], r["reason"], r["value"]])
            if kind == "matched":
                matched_rows.append([step, name, var, rate, r["draw"], r["status"], r["reason"], r.get("target"),
                                     r.get("n_intervals"), r.get("bracket_lo"), r.get("bracket_hi"),
                                     r.get("weight"), r.get("position"), r.get("p768_lo"), r.get("p768_hi"),
                                     r.get("p768_read"), r.get("p512_E3"), r["value"], r.get("where", "")]
                                    + list(r.get("path_values", [None] * len(PATH))))

    # runs complete? (Q27)
    all_complete = len(draws_present) == len(DRAWS) and all(
        data[d]["widths"][w]["arms"][r]["record"]["status"] == "COMPLETE"
        for d in draws_present for w in WIDTHS for r in RATES)

    # records against arrays (Q29)
    worst = (0.0, None)
    for key, pt in points.items():
        for var in ("train", "val"):
            diff = abs(pt[var + "_record"] - pt[var + "_array"])
            if diff > worst[0]:
                worst = (diff, [key[0], key[1], key[2], key[3], var])
    rec_vs_arr = {"max_abs_difference": worst[0], "where": worst[1], "threshold": 0.001, "warning": worst[0] > 0.001}

    # NOT_OVERFIT (Q28)
    not_overfit = {}
    for width in WIDTHS:
        for rate in RATES:
            deltas = {d: loss(d, width, rate, E3, "val") - loss(d, width, rate, E2, "val") for d in draws_present}
            ti = t_interval(list(deltas.values()))
            if ti["n"] < MIN_DRAWS:
                lab = "UNAVAILABLE"
            else:
                lab = {"below": "NOT_OVERFIT", "above": "OVERFIT"}.get(ti["side"], "PLATEAU")
            not_overfit["w%d_%s" % (width, rate)] = {"delta": deltas, "n": ti["n"], "mean": ti["mean"],
                                                     "ci_low": ti["ci_low"], "ci_high": ti["ci_high"], "label": lab}
    for step, name, kind, rate, var, expected in STATISTICS:
        arms = ["w%d_%s" % (w, rate) for w in WIDTHS]
        stats[step]["arms_used"] = arms
        stats[step]["reading_prefixed"] = any(not_overfit[a]["label"] != "NOT_OVERFIT" for a in arms)

    # which row of section 7 applies
    p1, s1, s3 = stats["P1"], stats["S1"], stats["S3"]
    if not all_complete and p1["n_available"] < MIN_DRAWS:
        row7 = "A run did not complete, and P1 has fewer than 5 available draws"
    elif p1["label"] == "REVERSAL_CONFIRMED":
        if not s3["reached"]:
            row7 = "REVERSAL_CONFIRMED, with the sequence stopped before S3"
        elif s3["label"] == "CONFIRMED":
            row7 = "REVERSAL_CONFIRMED, with S3 reached and CONFIRMED"
        elif s3["label"] == "CONTRARY":
            row7 = "REVERSAL_CONFIRMED, with S3 reached and CONTRARY"
        else:
            row7 = "REVERSAL_CONFIRMED, with S3 reached and INCONCLUSIVE or unreadable"
    else:
        row7 = p1["label"]

    # descriptives (Q30)
    desc = {"fixed_update_by_readout": {}, "panel": {}, "rate_effect_at_E3": {}, "clipping": {}, "e0": {}}
    for rate in RATES:
        for epoch in READOUTS:
            vals, ds = [], []
            for d in draws_present:
                a, b = fit(d, 512, rate, epoch), fit(d, 768, rate, epoch)
                if a["defined"] and b["defined"]:
                    vals.append(a["p"] - b["p"])
                    ds.append(d)
            ti = t_interval(vals)
            desc["fixed_update_by_readout"]["%s_E%g" % (rate, epoch)] = {
                "values": dict(zip(ds, vals)), "n": ti["n"], "mean": ti["mean"], "ci_low": ti["ci_low"],
                "ci_high": ti["ci_high"], "side": ti["side"]}
    for width in WIDTHS:
        for rate in RATES:
            arm = "w%d_%s" % (width, rate)
            for epoch in READOUTS:
                ps = [fit(d, width, rate, epoch)["p"] for d in draws_present if fit(d, width, rate, epoch)["defined"]]
                desc["panel"]["%s_E%g" % (arm, epoch)] = {
                    "n_defined": len(ps),
                    "p_star": float(np.mean(ps)) if ps else None,
                    "train": float(np.mean([loss(d, width, rate, epoch, "train") for d in draws_present])),
                    "val": float(np.mean([loss(d, width, rate, epoch, "val") for d in draws_present])),
                    "gap": float(np.mean([loss(d, width, rate, epoch, "gap") for d in draws_present]))}
            clip = {}
            for d in draws_present:
                eps = data[d]["widths"][width]["arms"][rate]["record"]["epochs"]
                upd = sum(e["updates"] for e in eps)
                clip[d] = {"clip_fraction": sum(e["clip_fraction"] * e["updates"] for e in eps) / upd,
                           "gradient_norm_mean": sum(e["gradient_norm_mean"] * e["updates"] for e in eps) / upd,
                           "gradient_norm_max": max(e["gradient_norm_max"] for e in eps), "updates": upd}
            desc["clipping"][arm] = {"per_draw": clip,
                                     "clip_fraction_mean": float(np.mean([c["clip_fraction"] for c in clip.values()]))}
        vals, ds = [], []
        for d in draws_present:
            a, b = fit(d, width, "lr3e-04", E3), fit(d, width, "lr1e-04", E3)
            if a["defined"] and b["defined"]:
                vals.append(a["p"] - b["p"])
                ds.append(d)
        ti = t_interval(vals)
        desc["rate_effect_at_E3"]["w%d_3e-4_minus_1e-4" % width] = {
            "values": dict(zip(ds, vals)), "n": ti["n"], "mean": ti["mean"], "ci_low": ti["ci_low"],
            "ci_high": ti["ci_high"], "side": ti["side"]}
        desc["e0"]["w%d" % width] = {"per_draw": {d: e0[(d, width)] for d in draws_present},
                                     "train_mean": float(np.mean([e0[(d, width)]["train"] for d in draws_present])),
                                     "val_mean": float(np.mean([e0[(d, width)]["val"] for d in draws_present]))}

    fits = [points[k]["fit"][ties] for k in points]
    fit_summary = {
        "n_fits": len(fits), "n_defined": sum(1 for f in fits if f["defined"]),
        "n_at_upper": sum(1 for f in fits if f["defined"] and f["p"] >= BOUND - SAT_MARGIN),
        "n_at_lower": sum(1 for f in fits if f["defined"] and f["p"] <= SAT_MARGIN),
        "n_multiple_candidates": sum(1 for f in fits if f["defined"] and f["n_candidates"] > 1),
        "max_abs_bisection_minus_golden": max(abs(f["p"] - f["p_golden"]) for f in fits if f["defined"]),
        "p_min": min(f["p"] for f in fits if f["defined"]), "p_max": max(f["p"] for f in fits if f["defined"]),
    }
    analysis = {
        "variant": {"ties": ties, "losses": losses},
        "draws_present": draws_present, "runs": {d: data[d]["run"] for d in draws_present},
        "every_run_complete": all_complete,
        "sequence": [s[0] for s in STATISTICS],
        "labels": {s[0]: stats[s[0]]["label"] for s in STATISTICS},
        "statuses": {s[0]: stats[s[0]]["status"] for s in STATISTICS},
        "section7_row": row7,
        "statistics": stats,
        "records_against_arrays": rec_vs_arr,
        "not_overfit": not_overfit,
        "fit_summary": fit_summary,
        "descriptives": desc,
        "t_crit": {str(df): t_crit(df) for df in (2, 3, 4, 5)},
    }
    return analysis, matched_rows, contrast_rows


def fmt(v):
    if v is None:
        return ""
    if isinstance(v, bool):
        return "1" if v else "0"
    if isinstance(v, float):
        return repr(float(v))
    return str(v)


def write_csv(path, header, rows):
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(header)
        for r in rows:
            w.writerow([fmt(v) for v in r])


def write_variant(outdir, points, ties, losses, analysis, matched_rows, contrast_rows):
    os.makedirs(outdir, exist_ok=True)
    rows = []
    for draw in DRAWS:
        for width in WIDTHS:
            for rate in RATES:
                for epoch in READOUTS:
                    pt = points.get((draw, width, rate, epoch))
                    if pt is None:
                        continue
                    f = pt["fit"][ties]
                    tr, va = pt["train_" + losses], pt["val_" + losses]
                    rows.append([draw, width, rate, epoch, pt["update"], f["defined"], f["reason"], f["p"],
                                 f["objective"],
                                 f["defined"] and f["p"] <= SAT_MARGIN, f["defined"] and f["p"] >= BOUND - SAT_MARGIN,
                                 f["n_candidates"], f["p_golden"], f["total_gain"], tr, va, va - tr,
                                 pt["train_array"], pt["val_array"], pt["train_record"], pt["val_record"]])
    write_csv(os.path.join(outdir, "per_readout.csv"),
              ["draw", "width", "rate", "readout", "update", "defined", "reason", "p_star", "objective", "at_lower",
               "at_upper", "n_candidates", "p_star_golden", "total_gain", "train", "val", "gap", "train_array",
               "val_array", "train_record", "val_record"], rows)
    write_csv(os.path.join(outdir, "matched.csv"),
              ["step", "statistic", "matched_on", "rate", "draw", "status", "reason", "target", "n_intervals",
               "bracket_lo", "bracket_hi", "weight_on_later", "position", "p768_lo", "p768_hi", "p768_read",
               "p512_E3", "value", "where"] + ["path_E%g" % e for e in PATH], matched_rows)
    write_csv(os.path.join(outdir, "contrasts.csv"), ["step", "statistic", "draw", "status", "reason", "value"],
              contrast_rows)
    with open(os.path.join(outdir, "analysis.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(analysis, f, indent=1, sort_keys=True)
        f.write("\n")


# ----------------------------------------------------------------------------------------------
# Self-test
# ----------------------------------------------------------------------------------------------
def selftest():
    # t quantiles: closed forms for df 1 and 2, numerical integration for df 3..5
    q = 0.975
    assert abs(t_crit(1) - math.tan(math.pi * (q - 0.5))) < 1e-9
    assert abs(t_crit(2) - (2 * q - 1) / math.sqrt(2 * q * (1 - q))) < 1e-10
    for df in (3, 4, 5):
        tc = t_crit(df)
        x = np.linspace(0.0, tc, 200001)
        c = math.exp(math.lgamma((df + 1) / 2) - math.lgamma(df / 2)) / math.sqrt(df * math.pi)
        y = c * (1 + x * x / df) ** (-(df + 1) / 2)
        h = x[1] - x[0]
        integral = h / 3 * (y[0] + y[-1] + 4 * y[1:-1:2].sum() + 2 * y[2:-1:2].sum())
        assert abs(0.5 + integral - q) < 1e-10, (df, integral)
    # the cumulative-sum form of d'Kd against the explicit quadratic form, with ties
    rng = np.random.default_rng(12345)
    n = 300
    w = np.exp(rng.uniform(math.log(0.01), math.log(10), n)).astype(np.float32)
    w[10] = w[20]
    w[30] = w[40] = w[50]
    g = rng.normal(0.3, 1.0, n)
    for ties in ("ecdf", "ordinal"):
        f = Fitter(w, ties)
        w64 = w.astype(np.float64)
        if ties == "ecdf":
            r = np.array([(w64 <= x).sum() for x in w64]) / n
        else:
            r = np.empty(n)
            r[f.order] = np.arange(1, n + 1) / n
        kmat = np.minimum.outer(r, r)
        gt = g / g.sum()
        for p in (0.0, 0.37, 1.0, 2.5, 8.0):
            b = w64 ** p / (w64 ** p).sum()
            d = gt - b
            direct = float(d @ kmat @ d)
            j, dj = f.exact(gt[f.order], p)
            assert abs(direct - j) < 1e-12 * max(1.0, abs(direct)), (ties, p, direct, j)
            eps = 1e-6
            num = (f.exact(gt[f.order], p + eps)[0] - f.exact(gt[f.order], max(p - eps, 0.0))[0]) / (eps + min(eps, p))
            assert abs(num - dj) < 1e-5 * max(1.0, abs(dj)), (ties, p, num, dj)
        # recover a planted exponent: gains exactly proportional to w^1.7
        res = f.fit(w64 ** 1.7)
        assert res["defined"] and abs(res["p"] - 1.7) < 1e-9, res
        assert abs(res["p_golden"] - res["p"]) < 1e-6
        assert not f.fit(-np.abs(g))["defined"]
    assert not Fitter(np.ones(8, dtype=np.float32), "ecdf").fit(np.ones(8))["defined"]
    # matching rule
    r = matched_reading(1.5, [1.0, 2.0, 1.0, 2.0], [0, 1, 2, 3])
    assert r["index"] == 0 and r["n_intervals"] == 3 and abs(r["weight"] - 0.5) < 1e-15
    r = matched_reading(2.0, [1.0, 2.0, 3.0], [0, 1, 2])
    assert r["index"] == 0 and r["weight"] == 1.0 and r["n_intervals"] == 2
    r = matched_reading(2.0, [2.0, 2.0, 3.0], [0, 1, 2])
    assert r["index"] == 0 and r["weight"] == 0.0
    assert not matched_reading(5.0, [1.0, 2.0, 3.0], [0, 1, 2])["held"]
    # sign test
    assert abs(sign_test([1, 1, 1, 1, 1, 1])["p_two_sided"] - 2 / 64) < 1e-15
    assert abs(sign_test([1, 1, 1, 1, 1, -1])["p_two_sided"] - 14 / 64) < 1e-15
    print("selftest passed")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bundle", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        selftest()
    data, checked = load_bundle(args.bundle)
    print("bundle files verified against MANIFEST.json:", checked)
    points, e0 = compute_points(data)
    os.makedirs(args.out, exist_ok=True)
    for ties in ("ecdf", "ordinal"):
        for losses in ("array", "record"):
            name = "%s_%s" % (ties, "arrays" if losses == "array" else "record")
            analysis, matched_rows, contrast_rows = analyse(data, points, e0, ties, losses)
            write_variant(os.path.join(args.out, name), points, ties, losses, analysis, matched_rows, contrast_rows)
            print("wrote", name)
    print("done")


if __name__ == "__main__":
    main()
