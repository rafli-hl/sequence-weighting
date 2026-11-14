"""Analysis of N8, the dense-readout replication of N7 (standard library and NumPy), as N8-protocol-draft.md section 6.

- Decision: H1 (equal training loss, expected above 0) and H2 (equal updates, expected below 0) are co-primaries, each a two-sided
  95% t interval over draws, UNAVAILABLE with fewer than 20 available draws. REVERSAL_REPLICATED only if both are CONFIRMED.
  Fewer than 20 completed draws makes the study INCOMPLETE, with no labels.
- Registered sensitivity analyses: the bracket envelope, leave-one-draw-out intervals, the starting offset.
- Registered secondary analyses (descriptive): S-a equal improvement, S-b exposure windows, S-c fit diagnostics, S-d path.
- Carried over from N7 and reported: saturation (a fit at or above 7.999 refitted at bound 32), NOT_OVERFIT, records against
  arrays.

The estimator, exponent(), is a verbatim copy of N7's sealed vendor/core.exponent; exponent_upper() and objective_at() are
verbatim copies of N7's text_analysis.py. p* is reproducible bit for bit only on the same Python and libm; the registered
analysis environment is native Windows Python 3.12.10. Gains are signed per-sequence training-loss reductions from each
width's own E0, subtracted in float32 as N7's text_analysis.gains.

Inputs. data[d] is None for a failed draw, or dict(weights=[...], arms={(width, tag): dict(e0=bytes, arrays=bytes,
record=dict)}): the worker's E0 and readout arrays (little-endian float32; each block holds the training rows, then the
validation rows) and its record. orders[d], for S-b only, holds the draw's batch orders: an (epochs, n) integer array whose row
e - 1 lists the sequence indices of epoch e in training order. per = points(data) holds the fits.
"""
import hashlib
import math
import platform
import statistics
import sys
from functools import lru_cache

import numpy as np

# ------------------------------------------------------------------ the plan (protocol sections 3, 5 and 6)
DRAWS = tuple(f'n{i:02d}' for i in range(1, 25))
RATE_TAG = 'lr1e-04'
UPDATES_PER_EPOCH, BATCH = 1024, 16           # 16,384 sequences in batches of 16
READOUT_UPDATES = (256, 512, 1024) + tuple(range(2048, 3584 + 1, 64))
READOUTS = tuple(u / UPDATES_PER_EPOCH for u in READOUT_UPDATES)      # exact binary fractions: 2.0625 = 2112 / 1024
PLAN = dict(draws=DRAWS, first=(512, RATE_TAG), second=(768, RATE_TAG),
            final=3.0, previous=2.0,                                  # 512 is read at update 3,072; NOT_OVERFIT is E3 minus E2
            path=tuple(e for e in READOUTS if e >= 2.0),              # 25 readouts, updates 2,048 to 3,584
            min_draws=20, min_completed=20,
            windows=4,                                                # S-b: quarter-epoch windows, as N7 (protocol section 6)
            updates_per_epoch=UPDATES_PER_EPOCH, batch=BATCH)
CONFIDENCE = 0.95
EPS = 1e-9                                    # "entirely" on one side of 0: beyond it by more than EPS
P_UPPER, S32_UPPER = 7.999, 32.0              # saturation: a fit at or above P_UPPER is refitted with the upper bound at 32
RECORD_LIMIT = 1e-3                           # records against arrays
MIN_LEAVE_ONE_OUT = 4                         # the interval over the remaining draws needs df >= 2
BINS = 16                                     # S-c: equal-count weight bins
NO_READING = ('UNDEFINED_FIT', 'SATURATED', 'TARGET_OUTSIDE_PATH', 'DRAW_MISSING')
HYPOTHESES = dict(H1=dict(kind='matched', key='train', expected='ABOVE'), H2=dict(kind='fixed', key=None, expected='BELOW'))
REGISTERED_ENVIRONMENT = dict(system='Windows', python='3.12.10', numpy='2.5.3')


def environment():
    env = dict(system=platform.system(), python=platform.python_version(), numpy=np.__version__, executable=sys.executable)
    return dict(env, registered=REGISTERED_ENVIRONMENT, matches_registered=all(env[k] == v for k, v in REGISTERED_ENVIRONMENT.items()))


def order_sha256(order):
    """The SHA-256 of one epoch's batch order: its sequence indices in training order as little-endian int64."""
    return hashlib.sha256(np.ascontiguousarray(order, dtype='<i8').tobytes()).hexdigest()


# ------------------------------------------------------------------ the estimator (verbatim copy of N7's vendor/core.exponent)
def exponent(weights, gains):
    """Cumulative-discrepancy estimator, equivalent to d' K d for unique ranks.

    K_ij=min(r_i,r_j). Since sum(d)=0, cumulative prefix and suffix versions
    coincide. Sorting avoids materializing an N by N matrix.

    Tied weights (expected for float32 weights at N = 16,384; owner decision
    20261102-03): sorted() is stable, so tied entries keep ascending sequence
    index, their position in the draw's weight list. The equivalence holds with
    ties ranked in that order, and p is bit-for-bit reproducible for the same
    inputs on the same Python and libm.
    """
    w = [float(x) for x in weights]
    g = [float(x) for x in gains]
    if max(w) - min(w) < 1e-12:
        return {"p": None, "reason": "constant_weights"}
    if sum(g) <= 1e-10:
        return {"p": None, "reason": "nonpositive_total_gain"}
    order = sorted(range(len(w)), key=w.__getitem__)
    logw = [math.log(w[i]) for i in order]
    total_gain = sum(g)
    gn = [g[i] / total_gain for i in order]

    def objective(p):
        z = [p * x for x in logw]
        m = max(z)
        z = [math.exp(x - m) for x in z]
        total = sum(z)
        c = 0.0
        loss = 0.0
        for a, b in zip(gn, z):
            c += a - b / total
            loss += c * c
        return loss / len(w)

    grid = [i / 20 for i in range(161)]
    j = min(range(len(grid)), key=lambda i: objective(grid[i]))
    lo, hi = grid[max(0, j - 1)], grid[min(len(grid) - 1, j + 1)]
    for _ in range(50):
        a, b = lo + (hi - lo) / 3, hi - (hi - lo) / 3
        if objective(a) < objective(b):
            hi = b
        else:
            lo = a
    candidates = [0.0, (lo + hi) / 2, 8.0]
    p = min(candidates, key=objective)
    return {"p": p, "objective": objective(p), "at_upper_bound": p >= 7.999,
            "mean_gain": sum(g) / len(g)}


# ------------------------------------------------------------------ verbatim copies of N7's text_analysis.objective_at and exponent_upper
def objective_at(weights, gains, p):
    """Exact copy of core.exponent's objective (ascending-weight cumulative discrepancy)."""
    order = sorted(range(len(weights)), key=weights.__getitem__); total = sum(gains)
    logw = [math.log(weights[i]) for i in order]; gn = [gains[i] / total for i in order]
    z = [p * x for x in logw]; m = max(z); z = [math.exp(x - m) for x in z]; s = sum(z); c = loss = 0.0
    for a, b in zip(gn, z): c += a - b / s; loss += c * c
    return loss / len(weights)


def exponent_upper(weights, gains, upper):
    """vendor/core.exponent with search bound `upper` (shift_analysis.exponent_upper); identical to it at 8."""
    w = [float(x) for x in weights]
    g = [float(x) for x in gains]
    if max(w) - min(w) < 1e-12:
        return {"p": None, "reason": "constant_weights"}
    if sum(g) <= 1e-10:
        return {"p": None, "reason": "nonpositive_total_gain"}
    steps = int(round(upper * 20))
    if steps < 1 or abs(steps / 20 - upper) > 1e-12: raise ValueError('upper must be a positive multiple of 0.05')
    order = sorted(range(len(w)), key=w.__getitem__)
    logw = [math.log(w[i]) for i in order]
    total_gain = sum(g)
    gn = [g[i] / total_gain for i in order]

    def objective(p):
        z = [p * x for x in logw]
        m = max(z)
        z = [math.exp(x - m) for x in z]
        total = sum(z)
        c = 0.0
        loss = 0.0
        for a, b in zip(gn, z):
            c += a - b / total
            loss += c * c
        return loss / len(w)

    grid = [i / 20 for i in range(steps + 1)]
    j = min(range(len(grid)), key=lambda i: objective(grid[i]))
    lo, hi = grid[max(0, j - 1)], grid[min(len(grid) - 1, j + 1)]
    for _ in range(50):
        a, b = lo + (hi - lo) / 3, hi - (hi - lo) / 3
        if objective(a) < objective(b):
            hi = b
        else:
            lo = a
    candidates = [0.0, (lo + hi) / 2, float(upper)]
    p = min(candidates, key=objective)
    return {"p": p, "objective": objective(p), "at_upper_bound": p >= upper - 0.001,
            "mean_gain": sum(g) / len(g)}


# ------------------------------------------------------------------ fits and their diagnostics (S-c)
def fit_diagnostics(weights, gains, p, objective, j0, bins=BINS):
    """S-c for one fit: the objective at p* relative to its value at p = 0; the cumulative discrepancy between normalised gains and
    normalised powered weights in ascending weight order (its RMS and maximum absolute value); and the mean gain residual,
    observed minus sum(g) w^p / sum(w^p), in `bins` equal-count bins of ascending weight. Descriptive; no threshold."""
    w = np.asarray(weights, dtype=np.float64); g = np.asarray(gains, dtype=np.float64); order = np.argsort(w, kind='stable')
    lw = p * np.log(w[order]); z = np.exp(lw - lw.max()); z /= z.sum(); gs = g[order]; total = gs.sum()
    r = np.cumsum(gs / total - z); resid = [float((gs[b] - total * z[b]).mean()) for b in np.array_split(np.arange(len(gs)), bins)]
    return dict(objective_ratio=objective / j0 if j0 > 0 else None, cumulative_rms=float(np.sqrt(np.mean(r * r))), cumulative_max_abs=float(np.abs(r).max()),
                bin_residuals=resid, bin_max_abs=max(abs(x) for x in resid), bin_rms=math.sqrt(math.fsum(x * x for x in resid) / bins))


def arm_arrays(arm):
    """(E0, readout arrays as an (epochs, rows) view, training rows, epochs) of one arm's raw inputs."""
    lay = arm['record']['layout']; n, nv = lay['train_rows'], lay['validation_rows']; epochs = [float(e) for e in lay['block_epochs']]
    e0 = np.frombuffer(arm['e0'], dtype='<f4'); arr = np.frombuffer(arm['arrays'], dtype='<f4')
    if len(e0) != n + nv or len(arr) != len(epochs) * (n + nv): raise ValueError('array sizes differ from the record layout')
    return e0, arr.reshape(len(epochs), n + nv), n, epochs


def gains_at(arm, epoch):
    """Signed per-sequence training gains E0 -> epoch, in float32, as text_analysis.gains."""
    e0, arr, n, epochs = arm_arrays(arm); return e0[:n] - arr[epochs.index(float(epoch)), :n]


def arm_points(weights, arm, diagnostics=True):
    """One arm's readouts: {epoch: dict(p, reason, train, validation, gap, gain, array means, and, for a defined fit, objective,
    J0, the bound-32 refit if p >= P_UPPER, saturated, and the S-c diagnostics)}. train and validation are the record's mean losses;
    the gap is validation minus train (N7's gap_of); gain is the mean signed gain from E0."""
    e0, arr, n, epochs = arm_arrays(arm); by_epoch = {float(x['epoch']): x for x in arm['record']['readouts']}; out = {}
    if len(weights) != n: raise ValueError('weights differ from the record layout')
    for k, e in enumerate(epochs):
        gains = (e0[:n] - arr[k, :n]).tolist(); r = exponent(weights, gains); p = r.get('p'); x = by_epoch[e]
        pt = dict(p=p, reason=r.get('reason'), train=x['train_loss'], validation=x['validation_loss'], gap=x['validation_loss'] - x['train_loss'],
                  gain=math.fsum(gains) / n, array_train=math.fsum(arr[k, :n].tolist()) / n, array_validation=math.fsum(arr[k, n:].tolist()) / (arr.shape[1] - n), saturated=False)
        if p is not None:
            pt.update(objective=r['objective'], J0=objective_at(weights, gains, 0.0))
            if p >= P_UPPER:
                r32 = exponent_upper(weights, gains, S32_UPPER); pt['p32'] = r32.get('p'); pt['saturated'] = r32.get('p') is None or r32['p'] >= S32_UPPER - 0.001
            if diagnostics: pt['diagnostics'] = fit_diagnostics(weights, gains, p, pt['objective'], pt['J0'])
        out[e] = pt
    return out


def points(data, draws=None, progress=None):
    """per[d][(width, tag)][epoch] for every arm of every completed draw; per[d] = None for a failed draw."""
    per = {}
    for d in (draws or list(data)):
        dd = data.get(d)
        per[d] = None if dd is None else {arm: arm_points(dd['weights'], a) for arm, a in dd['arms'].items()}
        if progress: progress(d)
    return per


# ------------------------------------------------------------------ Student t (regularized incomplete beta, as N7's fewepoch_analysis)
def _betacf(a, b, x):
    qab, qap, qam = a + b, a + 1.0, a - 1.0; c, d = 1.0, 1.0 - qab * x / qap
    d = 1.0 / (d if abs(d) > 1e-300 else 1e-300); h = d
    for m in range(1, 1000):
        m2 = 2 * m; aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d; d = 1.0 / (d if abs(d) > 1e-300 else 1e-300); c = 1.0 + aa / c; c = c if abs(c) > 1e-300 else 1e-300; h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d; d = 1.0 / (d if abs(d) > 1e-300 else 1e-300); c = 1.0 + aa / c; c = c if abs(c) > 1e-300 else 1e-300; de = d * c; h *= de
        if abs(de - 1.0) < 1e-15: return h
    raise ArithmeticError('Incomplete beta did not converge')


def betai(a, b, x):
    if x <= 0: return 0.0
    if x >= 1: return 1.0
    bt = math.exp(math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b) + a * math.log(x) + b * math.log(1 - x))
    return bt * _betacf(a, b, x) / a if x < (a + 1) / (a + b + 2) else 1.0 - bt * _betacf(b, a, 1 - x) / b


def p_two_sided(t, df):
    """P(|T| >= |t|) for Student's t with df degrees of freedom."""
    return betai(df / 2, 0.5, df / (df + t * t))


@lru_cache(maxsize=None)
def t_quantile(prob, df):
    """The exact quantile q with P(T <= q) = prob, for 0.5 < prob < 1, by bisection on the incomplete beta to the last bit."""
    if not 0.5 < prob < 1 or df < 1: raise ValueError('t_quantile needs 0.5 < prob < 1 and df >= 1')
    tail = 2 * (1 - prob); lo, hi = 0.0, 1.0
    while p_two_sided(hi, df) > tail: lo, hi = hi, 2 * hi
    for _ in range(2000):
        mid = (lo + hi) / 2
        if mid <= lo or mid >= hi: break
        if p_two_sided(mid, df) > tail: lo = mid
        else: hi = mid
    return (lo + hi) / 2


# ------------------------------------------------------------------ intervals and tests
def t_interval(values, confidence=CONFIDENCE):
    """Mean, sd and the two-sided t interval (df n - 1, exact quantile); the t-test p of the mean; degenerate if sd <= EPS."""
    n = len(values)
    if n < 2: raise ValueError('a t interval needs at least 2 values')
    m = math.fsum(values) / n; sd = statistics.stdev(values); q = t_quantile(0.5 + confidence / 2, n - 1); se = sd / math.sqrt(n)
    degenerate = sd <= EPS; p = (0.0 if abs(m) > EPS else 1.0) if degenerate else p_two_sided(m / se, n - 1)
    return dict(n=n, df=n - 1, t_critical=q, mean=m, sd=sd, se=se, interval=[m - q * se, m + q * se], p=p, degenerate=degenerate,
                negative=sum(v < 0 for v in values), positive=sum(v > 0 for v in values))


def side(t):
    if t['interval'][0] > EPS: return 'ABOVE'
    if t['interval'][1] < -EPS: return 'BELOW'
    return 'SPANS'


def sign_test(values):
    """The exact two-sided sign test; zeros are dropped. p is None if every value is zero."""
    pos, neg = sum(v > 0 for v in values), sum(v < 0 for v in values); n = pos + neg
    if n == 0: return dict(positive=pos, negative=neg, zeros=len(values), p=None)
    return dict(positive=pos, negative=neg, zeros=len(values) - n, p=min(1.0, 2 * math.fsum(math.comb(n, k) for k in range(min(pos, neg) + 1)) / 2 ** n))


def leave_one_out(values, confidence=CONFIDENCE):
    """values: {draw: value}. The interval over the remaining draws, leaving out each draw in turn."""
    out = {}
    for d in values:
        t = t_interval([v for k, v in values.items() if k != d], confidence); s = side(t)
        out[d] = dict(mean=t['mean'], interval=t['interval'], df=t['df'], side=s, excludes_zero=s != 'SPANS')
    return out


def describe(values):
    """values: {draw: value}. The interval (if at least 2 values) and the sign test; descriptive."""
    v = list(values.values()); out = dict(n=len(v), values=values, sign_test=sign_test(v))
    if len(v) >= 2: out['interval'] = t_interval(v)
    return out


# ------------------------------------------------------------------ the reading rule (N7's matched_analysis.read_along, as written)
def read_along(path_rows, target):
    """path_rows: (readout, value, p) in readout order along the match path. The first interval whose two values hold the target gives the
    reading. Returns TARGET_OUTSIDE_PATH, or the bracket with UNDEFINED_FIT if a bracketing p* is undefined, or READ."""
    hits = [(a, b) for a, b in zip(path_rows, path_rows[1:]) if min(a[1], b[1]) <= target <= max(a[1], b[1])]
    values = [r[1] for r in path_rows]
    base = dict(target=target, path_min=min(values), path_max=max(values), intervals_holding_the_target=len(hits))
    if not hits: return dict(base, status='TARGET_OUTSIDE_PATH')
    (e0, x0, p0), (e1, x1, p1) = hits[0]; w = 0.0 if x1 == x0 else (target - x0) / (x1 - x0)
    base.update(between=[e0, e1], value_at_bracket=[x0, x1], weight=w, read_at_readout=e0 + w * (e1 - e0), p_at_bracket=[p0, p1])
    if p0 is None or p1 is None: return dict(base, status='UNDEFINED_FIT')
    return dict(base, status='READ', p_read=p0 + w * (p1 - p0))


def draw_row(per_d, first, second, kind, key, final, path):
    """One draw of one contrast: the reading of the second arm, and p*(first, final) minus it (N7's draw_row)."""
    p_first = per_d[first][final]['p']
    if kind == 'matched':
        r = read_along([(e, per_d[second][e][key], per_d[second][e]['p']) for e in path], per_d[first][final][key])
    else:
        p = per_d[second][final]['p']; r = dict(status='READ', p_read=p, read_at_readout=final) if p is not None else dict(status='UNDEFINED_FIT', read_at_readout=final)
    r = dict(r, p_first=p_first)
    if p_first is None and r['status'] == 'READ': r['status'] = 'UNDEFINED_FIT'
    if r['status'] == 'READ': r['value'] = p_first - r['p_read']
    return r


def fits_used(row, first, second, kind, final):
    """The (arm, readout) fits a draw's reading uses."""
    return [(first, final)] + [(second, e) for e in (row['between'] if kind == 'matched' else [final])]


# ------------------------------------------------------------------ the bracket envelope (registered sensitivity 1)
def bracket_envelope(ends, confidence=CONFIDENCE, block=1 << 18):
    """ends: per available draw, (contrast with 768 read at the bracket's first readout, at its second). Every one of the 2^n
    combinations of ends is enumerated; returns the minimum lower t limit and the maximum upper t limit, with the ends that give them.

    The lower limit, mean - q sd / sqrt(n), is concave in the values (the sd is a norm), so over the box of brackets its minimum is at a
    vertex; the upper limit is convex, so its maximum is too. Sums and sums of squares split over two halves of the draws: each half's
    2^(n/2) partial sums are tabulated once, and the full combinations are formed block by block as outer sums, never more than `block`
    at a time. Values are centred first; the sd does not depend on the shift.
    """
    v = np.asarray(ends, dtype=np.float64)
    if v.ndim != 2 or v.shape[1] != 2: raise ValueError('ends must be pairs')
    n = len(v)
    if n < 2: raise ValueError('the envelope needs at least 2 draws')
    q = t_quantile(0.5 + confidence / 2, n - 1); centre = float(v.mean()); v = v - centre; k = n // 2

    def half(part):
        idx = np.arange(1 << len(part), dtype=np.int64); pick = ((idx[:, None] >> np.arange(len(part), dtype=np.int64)) & 1).astype(bool)
        x = np.where(pick, part[:, 1], part[:, 0]); return x.sum(axis=1), (x * x).sum(axis=1)

    s_lo, q_lo = half(v[:k]); s_hi, q_hi = half(v[k:]); width = len(s_lo); rows = max(1, block // width)
    low = (math.inf, -1); up = (-math.inf, -1)
    for r0 in range(0, len(s_hi), rows):
        s = s_hi[r0:r0 + rows, None] + s_lo[None, :]; ss = q_hi[r0:r0 + rows, None] + q_lo[None, :]
        half_width = q * np.sqrt(np.maximum((ss - s * s / n) / (n - 1), 0.0)) / math.sqrt(n); mean = s / n
        lower = mean - half_width; i = int(np.argmin(lower))
        if lower.flat[i] < low[0]: low = (float(lower.flat[i]), ((r0 + i // width) << k) | (i % width))
        upper = mean + half_width; i = int(np.argmax(upper))
        if upper.flat[i] > up[0]: up = (float(upper.flat[i]), ((r0 + i // width) << k) | (i % width))

    def vertex(c):
        ends_used = [(c >> j) & 1 for j in range(n)]; vals = [float(v[j, b]) + centre for j, b in enumerate(ends_used)]
        t = t_interval(vals, confidence); return dict(ends=ends_used, mean=t['mean'], sd=t['sd'], interval=t['interval'])

    return dict(n=n, combinations=1 << n, t_critical=q, min_lower=low[0] + centre, max_upper=up[0] + centre,
                at_min_lower=vertex(low[1]), at_max_upper=vertex(up[1]))


# ------------------------------------------------------------------ contrasts
def contrast(per, draws, first, second, kind, key=None, final=3.0, path=PLAN['path'], min_draws=2, expected=None, envelope=False, confidence=CONFIDENCE):
    """A paired contrast over the draws: per-draw rows, availability and its reasons, the t interval and side, the sign test, the
    leave-one-draw-out intervals and, if asked, the bracket envelope. A draw whose reading uses a SATURATED fit is unavailable;
    fits at or above P_UPPER are listed with the contrast at bound 32. UNAVAILABLE with fewer than min_draws readings."""
    rows = {}
    for d in draws:
        if per.get(d) is None: rows[d] = dict(status='DRAW_MISSING'); continue
        r = draw_row(per[d], first, second, kind, key, final, path)
        if r['status'] == 'READ' and any(per[d][a][e].get('saturated', False) for a, e in fits_used(r, first, second, kind, final)): r = dict(r, status='SATURATED')
        rows[d] = r
    available = [d for d in draws if rows[d]['status'] == 'READ']; values = {d: rows[d]['value'] for d in available}
    out = dict(kind=kind, key=key, first=list(first), second=list(second), expected=expected, min_draws=min_draws, rows=rows, available=available,
               unavailable={d: rows[d]['status'] for d in draws if d not in available}, unavailable_counts={why: sum(rows[d]['status'] == why for d in draws) for why in NO_READING},
               values=values, sign_test=sign_test(list(values.values())))
    flagged = [d for d in draws if rows[d]['status'] in ('READ', 'SATURATED') and any(per[d][a][e]['p'] >= P_UPPER for a, e in fits_used(rows[d], first, second, kind, final))]
    if flagged:
        def p32(d, a, e):
            x = per[d][a][e]; return x.get('p32') if x['p'] >= P_UPPER else x['p']
        at32 = {}
        for d in flagged:
            r = rows[d]
            if r['status'] != 'READ': continue
            lo, hi = (r['between'] if kind == 'matched' else (final, final)); p_second = p32(d, second, lo) + (r['weight'] if kind == 'matched' else 0.0) * (p32(d, second, hi) - p32(d, second, lo))
            at32[d] = p32(d, first, final) - p_second
        out['saturation'] = dict(flagged=flagged, saturated=[d for d in flagged if rows[d]['status'] == 'SATURATED'], values_at_bound_32=dict(values, **at32))
    if len(available) >= MIN_LEAVE_ONE_OUT: out['leave_one_out'] = leave_one_out(values, confidence)
    if len(available) < max(min_draws, 2): return dict(out, status='UNAVAILABLE')
    t = t_interval(list(values.values()), confidence); out.update(interval=t, status=side(t))
    if flagged: out['saturation']['interval_at_bound_32'] = t_interval(list(out['saturation']['values_at_bound_32'].values()), confidence)
    if envelope:
        out['envelope'] = bracket_envelope([[rows[d]['p_first'] - rows[d]['p_at_bracket'][0], rows[d]['p_first'] - rows[d]['p_at_bracket'][1]] for d in available], confidence)
    return out


def label(stat):
    """CONFIRMED if the interval lies entirely on the expected side of 0, CONTRARY if on the other side, INCONCLUSIVE if it includes 0."""
    if stat['status'] == 'UNAVAILABLE': return 'UNAVAILABLE'
    if stat['status'] == 'SPANS': return 'INCONCLUSIVE'
    return 'CONFIRMED' if stat['status'] == stat['expected'] else 'CONTRARY'


def decide(per, plan=PLAN):
    """The registered decision. INCOMPLETE, with no statistic and no label, if fewer than min_completed draws completed; otherwise H1 and
    H2 with their labels, and REVERSAL_REPLICATED only if both are CONFIRMED."""
    completed = [d for d in plan['draws'] if per.get(d) is not None]; failed = [d for d in plan['draws'] if d not in completed]
    if len(completed) < plan['min_completed']:
        return dict(status='INCOMPLETE', completed=completed, failed=failed, labels=None, joint=None,
                    note=f"{len(completed)} of {len(plan['draws'])} draws completed, fewer than {plan['min_completed']}: the study is INCOMPLETE and nothing is read.")
    stats = {h: contrast(per, plan['draws'], plan['first'], plan['second'], s['kind'], s['key'], plan['final'], plan['path'], plan['min_draws'], s['expected'], envelope=h == 'H1')
             for h, s in HYPOTHESES.items()}
    labels = {h: label(s) for h, s in stats.items()}
    return dict(status='COMPLETE' if not failed else 'COMPLETE_WITH_FAILED_DRAWS', completed=completed, failed=failed, labels=labels,
                joint='REVERSAL_REPLICATED' if all(x == 'CONFIRMED' for x in labels.values()) else 'REVERSAL_NOT_REPLICATED', statistics=stats)


# ------------------------------------------------------------------ registered sensitivity 3: the starting offset
def starting_offset(h1, data, plan=PLAN):
    """H1 with 768's gains lowered by the draw's mean E0 excess over 512 (mean over training rows): 768 refitted at both ends of the
    draw's registered bracket and read with the registered weight. Also the change in 768's reading."""
    first, second = plan['first'], plan['second']; rows = {}
    for d in h1['available']:
        r = h1['rows'][d]; dd = data[d]; e01, _, n, _ = arm_arrays(dd['arms'][first]); e02, _, _, _ = arm_arrays(dd['arms'][second])
        offset = math.fsum(e02[:n].tolist()) / n - math.fsum(e01[:n].tolist()) / n
        fits = [exponent(dd['weights'], (gains_at(dd['arms'][second], e).astype(np.float64) - offset).tolist()) for e in r['between']]; ps = [f.get('p') for f in fits]
        if None in ps: rows[d] = dict(status='UNDEFINED_FIT', offset=offset, p_at_bracket=ps); continue
        p_off = ps[0] + r['weight'] * (ps[1] - ps[0])
        rows[d] = dict(status='READ', offset=offset, p_at_bracket=ps, at_upper_bound=any(p >= P_UPPER for p in ps), p_read=p_off, value=r['p_first'] - p_off, change=p_off - r['p_read'])
    read = [d for d in rows if rows[d]['status'] == 'READ']
    return dict(rows=rows, contrast=describe({d: rows[d]['value'] for d in read}), change_in_768=describe({d: rows[d]['change'] for d in read}),
                offset=describe({d: rows[d]['offset'] for d in rows}))


# ------------------------------------------------------------------ secondary analyses (descriptive; no labels)
def equal_improvement(per, plan=PLAN):
    """S-a: 768 read where its mean gain from its own E0 equals 512's at the final readout, by the registered reading rule."""
    return contrast(per, plan['draws'], plan['first'], plan['second'], 'matched', 'gain', plan['final'], plan['path'], 2, 'ABOVE')


def path_contrasts(per, plan=PLAN):
    """S-d: the equal-updates contrast at every readout of the path, with pointwise intervals (unadjusted)."""
    out = {}
    for e in plan['path']:
        vals = {d: per[d][plan['first']][e]['p'] - per[d][plan['second']][e]['p'] for d in plan['draws'] if per.get(d) is not None
                and all(per[d][a][e]['p'] is not None and not per[d][a][e].get('saturated', False) for a in (plan['first'], plan['second']))}
        out[e] = describe(vals)
    return out


def fit_table(per):
    """S-c: one row per fit with its diagnostics, and the minimum, median and maximum of each diagnostic over all defined fits."""
    rows = [dict(draw=d, width=a[0], tag=a[1], epoch=e, p=x['p'], saturated=x.get('saturated', False), **{k: v for k, v in (x.get('diagnostics') or {}).items() if k != 'bin_residuals'},
                 **{f'bin_{i + 1:02d}': v for i, v in enumerate((x.get('diagnostics') or {}).get('bin_residuals', []))})
            for d, pd in per.items() if pd is not None for a, pe in pd.items() for e, x in pe.items()]
    keys = ('objective_ratio', 'cumulative_rms', 'cumulative_max_abs', 'bin_max_abs', 'bin_rms')
    summary = {k: dict(min=float(np.min(v)), median=float(np.median(v)), max=float(np.max(v))) for k in keys for v in [[r[k] for r in rows if r.get(k) is not None]] if v}
    return dict(rows=rows, summary=summary)


def windows_of(order, n, windows, batch):
    """Per epoch row: each sequence's window (1..windows) and its update within the epoch (1..n / batch)."""
    pos = np.empty_like(order)
    for e in range(order.shape[0]): pos[e, order[e]] = np.arange(n)
    return pos // (n // windows) + 1, pos // batch + 1


def window_steps(path, windows):
    """The pairs of path readouts that open and close one window of an epoch: (t0, t1, epoch, window trained between them)."""
    steps = []
    for t0 in path:
        e = int(math.floor(t0)) + 1; k = (t0 - (e - 1)) * windows; t1 = next((x for x in path if abs(x - t0 - 1 / windows) < 1e-12), None)
        if t1 is not None and abs(k - round(k)) < 1e-9 and t1 <= e + 1e-12: steps.append((t0, t1, e, int(round(k)) + 1))
    return steps


def order_check(dd, order, plan=PLAN):
    """Do the orders match the losses? For each window of the path (window_steps), the training-loss change of the sequences the order
    says were trained in that window, minus that of the others (nats). Strongly negative everywhere if the orders are the ones used."""
    n = len(dd['weights']); win, _ = windows_of(order, n, plan['windows'], plan['batch']); gaps = []
    for t0, t1, e, q in window_steps(plan['path'], plan['windows']):
        trained = win[e - 1] == q
        for arm in (plan['first'], plan['second']):
            _, arr, _, epochs = arm_arrays(dd['arms'][arm]); dl = arr[epochs.index(t1), :n].astype(np.float64) - arr[epochs.index(t0), :n].astype(np.float64)
            gaps.append(float(dl[trained].mean() - dl[~trained].mean()))
    return dict(steps=len(gaps), mean=float(np.mean(gaps)), min=float(np.min(gaps)), max=float(np.max(gaps)))


def exposure_windows(per, data, orders, plan=PLAN):
    """S-b, the 11 November recency-window comparison of N7, with quarter-epoch windows as N7 (plan windows = 4). Epochs are cut into
    `windows` windows of n / windows consecutive sequences of the order. For j = 1 .. windows - 1, 512 at the final readout against 768
    at previous + j / windows, on (a) the whole set; (b) last pass: 768 on sequences in windows <= j of epoch 3, 512 on windows >= W + 1 - j;
    (c) every pass: the same condition in each of epochs 1-3. Per set: its size, p*, mean training loss, and its recency balance — the
    mean age of each pass (updates before the readout) of 512's set minus 768's, and the total-variation distance between the two sets'
    joint window cells over the matched passes (512's windows shifted by W - j)."""
    W, U, B = plan['windows'], plan['updates_per_epoch'], plan['batch']; first, second, final = plan['first'], plan['second'], plan['final']
    completed = [d for d in plan['draws'] if per.get(d) is not None]; out = dict(order_checks={}, steps={})
    cache = {}
    for d in completed:
        dd = data[d]; n = len(dd['weights']); order = np.asarray(orders[d]); win, rank = windows_of(order, n, W, B)
        out['order_checks'][d] = order_check(dd, order, plan); cache[d] = (dd, n, win, rank, np.asarray(dd['weights'], dtype=np.float64))
    for j in range(1, W):
        e2 = plan['previous'] + j / W; u1, u2 = round(final * U), round(e2 * U); vals = {k: {} for k in ('whole', 'last', 'every', 'loss_last', 'loss_every', 'whole_minus_every', 'last_minus_every')}
        sets = {}
        for d in completed:
            dd, n, win, rank, w = cache[d]; a, b, c = win[0], win[1], win[2]
            masks = dict(last=(c >= W + 1 - j, c <= j), every=((a >= W + 1 - j) & (b >= W + 1 - j) & (c >= W + 1 - j), (a <= j) & (b <= j) & (c <= j)))
            p1, p2 = per[d][first][final]['p'], per[d][second][e2]['p']
            if p1 is not None and p2 is not None: vals['whole'][d] = p1 - p2
            g1, g2 = gains_at(dd['arms'][first], final), gains_at(dd['arms'][second], e2)
            _, arr1, _, ep1 = arm_arrays(dd['arms'][first]); _, arr2, _, ep2 = arm_arrays(dd['arms'][second]); t1, t2 = arr1[ep1.index(final), :n], arr2[ep2.index(e2), :n]
            sets[d] = {}
            for name, (m1, m2) in masks.items():
                f1 = exponent(w[m1].tolist(), g1[m1].tolist()).get('p') if m1.sum() >= 2 else None
                f2 = exponent(w[m2].tolist(), g2[m2].tolist()).get('p') if m2.sum() >= 2 else None
                passes = (0, 1, 2) if name == 'every' else (2,)
                age = [float((u1 - (e * U + rank[e][m1])).mean() - (u2 - (e * U + rank[e][m2])).mean()) if m1.any() and m2.any() else None for e in range(3)]
                code1 = sum((win[e][m1] - (W - j) - 1) * j ** i for i, e in enumerate(passes)); code2 = sum((win[e][m2] - 1) * j ** i for i, e in enumerate(passes))
                h1 = np.bincount(code1, minlength=j ** len(passes)) / max(1, m1.sum()); h2 = np.bincount(code2, minlength=j ** len(passes)) / max(1, m2.sum())
                sets[d][name] = dict(size=[int(m1.sum()), int(m2.sum())], p=[f1, f2], loss=[float(t1[m1].astype(np.float64).mean()) if m1.any() else None, float(t2[m2].astype(np.float64).mean()) if m2.any() else None],
                                     mean_age_difference=age, joint_cell_distance=float(np.abs(h1 - h2).sum() / 2))
                if f1 is not None and f2 is not None: vals[name][d] = f1 - f2
                if m1.any() and m2.any(): vals[f'loss_{name}'][d] = sets[d][name]['loss'][0] - sets[d][name]['loss'][1]
            for x in ('whole', 'last'):
                if d in vals[x] and d in vals['every']: vals[f'{x}_minus_every'][d] = vals[x][d] - vals['every'][d]
        bal = {name: dict(size_min=min(min(sets[d][name]['size']) for d in sets), size_max=max(max(sets[d][name]['size']) for d in sets),
                          max_abs_mean_age_difference=max((abs(x) for d in sets for x in sets[d][name]['mean_age_difference'] if x is not None), default=None),
                          max_joint_cell_distance=max(sets[d][name]['joint_cell_distance'] for d in sets)) for name in ('last', 'every')}
        out['steps'][e2] = dict(j=j, readout_768=e2, contrasts={k: describe(v) for k, v in vals.items()}, balance=bal, per_draw=sets)
    return out


# ------------------------------------------------------------------ carried over from N7 (reported; not gating)
def not_overfit(per, plan=PLAN):
    """Per width: the interval of validation loss at the final readout minus the previous one. NOT_OVERFIT if entirely below 0."""
    completed = [d for d in plan['draws'] if per.get(d) is not None]; out = {}
    for arm in (plan['first'], plan['second']):
        t = t_interval([per[d][arm][plan['final']]['validation'] - per[d][arm][plan['previous']]['validation'] for d in completed])
        out[f'{arm[0]}|{arm[1]}'] = dict(interval=t, label='NOT_OVERFIT' if t['interval'][1] < -EPS else 'OVERFIT' if t['interval'][0] > EPS else 'PLATEAU')
    return out


def records_against_arrays(per):
    """Each readout's recorded mean losses against the means of its arrays; a readout differing by more than RECORD_LIMIT is flagged."""
    worst, flagged = 0.0, []
    for d, pd in per.items():
        for arm, pe in (pd or {}).items():
            for e, x in pe.items():
                diff = max(abs(x['array_train'] - x['train']), abs(x['array_validation'] - x['validation'])); worst = max(worst, diff)
                if diff > RECORD_LIMIT: flagged.append(dict(draw=d, width=arm[0], tag=arm[1], epoch=e, difference=diff))
    return dict(max_absolute_difference=worst, limit=RECORD_LIMIT, flagged=flagged)


# ------------------------------------------------------------------ the whole analysis
def analyse(per, data, plan=PLAN, orders=None):
    """The decision, then (unless INCOMPLETE) the registered sensitivity analyses, the secondary analyses and the carried-over checks.
    S-b needs the batch orders; without them it is reported as not computed."""
    result = dict(environment=environment(), plan={k: (list(v) if isinstance(v, tuple) else v) for k, v in plan.items()}, decision=decide(per, plan))
    if result['decision']['status'] == 'INCOMPLETE': return result
    h1 = result['decision']['statistics']['H1']
    result['sensitivity'] = dict(envelope=h1.get('envelope'), leave_one_out={h: s.get('leave_one_out') for h, s in result['decision']['statistics'].items()},
                                 starting_offset=starting_offset(h1, data, plan))
    result['secondary'] = dict(S_a=equal_improvement(per, plan), S_b=exposure_windows(per, data, orders, plan) if orders is not None else dict(status='NOT_COMPUTED', reason='no batch orders given'),
                               S_c=fit_table({d: per[d] for d in plan['draws'] if per.get(d) is not None}), S_d=path_contrasts(per, plan))
    result['carried_over'] = dict(not_overfit=not_overfit(per, plan), records_against_arrays=records_against_arrays({d: per[d] for d in plan['draws']}))
    return result
