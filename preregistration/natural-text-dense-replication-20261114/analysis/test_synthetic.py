"""Synthetic edge cases for n8_analysis.py: the t quantile, the reading rule, availability, INCOMPLETE and the joint label,
saturation, the sign test and the bracket envelope at N8's 24 draws.

    python -I -B test_synthetic.py

Synthetic values come from fixed formulas, not from a random generator. SciPy is used only if it is installed.
Exits 1 if any check fails.
"""
import itertools, math, statistics, sys, time, tracemalloc
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import n8_analysis as na

results = []
T95_N7 = {2: 4.302652730, 3: 3.182446305, 4: 2.776445105, 5: 2.570581836, 6: 2.446911851, 7: 2.364624252,
          8: 2.306004135, 9: 2.262157163, 10: 2.228138852, 11: 2.200985160}      # N7's text_analysis.T95, 9 decimals


def check(name, ok, detail=''):
    results.append(bool(ok)); print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f'  [{detail}]' if detail else ''))


def central(t, nu):
    """P(|T| <= t) in closed form for integer nu (Abramowitz and Stegun 26.7.3 and 26.7.4), independent of the incomplete beta."""
    th = math.atan(t / math.sqrt(nu)); s, c = math.sin(th), math.cos(th)
    if nu % 2:
        if nu == 1: return 2 * th / math.pi
        term = total = c
        for k in range(3, nu - 1, 2): term *= (k - 1) / k * c * c; total += term
        return 2 / math.pi * (th + s * total)
    term = total = 1.0
    for k in range(2, nu - 1, 2): term *= (k - 1) / k * c * c; total += term
    return s * total


def brute(ends, confidence=0.95):
    q = na.t_quantile(0.5 + confidence / 2, len(ends) - 1); low, up = math.inf, -math.inf
    for c in itertools.product(*ends):
        m = math.fsum(c) / len(c); h = q * statistics.stdev(c) / math.sqrt(len(c)); low = min(low, m - h); up = max(up, m + h)
    return low, up


def numpy_brute(ends, confidence=0.95, block=1 << 16):
    """Every combination directly: a bit matrix per block, np.std with ddof 1. A different route from bracket_envelope's split sums."""
    v = np.asarray(ends); n = len(v); q = na.t_quantile(0.5 + confidence / 2, n - 1); low, up = math.inf, -math.inf
    for start in range(0, 1 << n, block):
        idx = np.arange(start, min(start + block, 1 << n), dtype=np.int64); pick = ((idx[:, None] >> np.arange(n)) & 1).astype(bool)
        x = np.where(pick, v[:, 1], v[:, 0]); m = x.mean(axis=1); h = q * x.std(axis=1, ddof=1) / math.sqrt(n)
        low = min(low, float((m - h).min())); up = max(up, float((m + h).max()))
    return low, up


def synthetic_ends(n, spread=1.0):
    return [[0.008 + 0.006 * math.sin(1.3 * k + 0.2), 0.008 + 0.006 * math.sin(1.3 * k + 0.2) - spread * 0.004 * (1 + math.cos(0.7 * k))] for k in range(n)]


def t_quantiles():
    print('--- t quantile')
    worst = max(abs(central(na.t_quantile(prob, nu), nu) - (2 * prob - 1)) for nu in range(1, 61) for prob in (0.9, 0.95, 0.975, 0.995))
    check('closed-form integer-df CDF at the quantile, df 1-60, probabilities 0.9 to 0.995 (1e-13)', worst <= 1e-13, f'largest error {worst:.2g}')
    worst_p = max(abs((1 - na.p_two_sided(t, nu)) - central(t, nu)) for nu in range(1, 41) for t in (0.1, 0.7, 1.5, 2.1, 3.3, 6.0))
    check('two-sided p against the closed form, df 1-40 (1e-13)', worst_p <= 1e-13, f'largest error {worst_p:.2g}')
    worst_t = max(abs(na.t_quantile(0.975, df) - v) for df, v in T95_N7.items())
    check("N7's T95 table, df 2-11 (rounded to 9 decimals, so 5e-10)", worst_t <= 5e-10, f'largest difference {worst_t:.2g}')
    print('      df 19-23: ' + ', '.join(f'{df}: {na.t_quantile(0.975, df):.12f}' for df in range(19, 24)))
    try:
        from scipy import stats as sps
    except ImportError:
        print('SKIP  SciPy comparison: SciPy is not installed'); return
    worst_s = max(abs(na.t_quantile(0.975, df) - sps.t.ppf(0.975, df)) for df in range(1, 61))
    check('SciPy t.ppf(0.975), df 1-60 (1e-12)', worst_s <= 1e-12, f'largest difference {worst_s:.2g}')


def reading_rule():
    print('--- reading rule')
    r = na.read_along([(2, 4.25, 0.10), (2.25, 4.25, 0.11), (2.5, 4.20, 0.12)], 4.25)
    check('a flat interval holding the target is read at its earlier readout', r['status'] == 'READ' and r['between'] == [2, 2.25] and r['weight'] == 0.0 and r['read_at_readout'] == 2 and r['p_read'] == 0.10 and r['intervals_holding_the_target'] == 2, str({k: r[k] for k in ('between', 'weight', 'p_read', 'intervals_holding_the_target')}))
    r = na.read_along([(2, 4.30, 0.10), (2.25, 4.25, 0.11), (2.5, 4.25, 0.12), (2.75, 4.30, 0.13)], 4.25)
    check('a target equal to a readout value is held by the first interval that contains it', r['between'] == [2, 2.25] and r['weight'] == 1.0 and r['read_at_readout'] == 2.25 and r['p_read'] == 0.11 and r['intervals_holding_the_target'] == 3, str({k: r[k] for k in ('between', 'weight', 'p_read', 'intervals_holding_the_target')}))
    path = [(2, 4.30, 0.10), (2.25, 4.25, 0.11), (2.5, 4.20, 0.12)]
    for target in (4.31, 4.19):
        r = na.read_along(path, target)
        check(f'a target outside the path ({target}) is TARGET_OUTSIDE_PATH', r['status'] == 'TARGET_OUTSIDE_PATH' and r['intervals_holding_the_target'] == 0 and 'between' not in r and 'p_read' not in r, r['status'])
    path = [(2, 4.40, 0.10), (2.25, 4.30, 0.20), (2.5, 4.35, 0.30), (2.75, 4.20, 0.40), (3, 4.32, 0.50), (3.25, 4.10, 0.60)]
    r = na.read_along(path, 4.31)
    check('a non-monotone path: the first bracketing interval, and the count of all of them', r['between'] == [2, 2.25] and r['intervals_holding_the_target'] == 5 and abs(r['weight'] - 0.9) < 1e-12 and abs(r['p_read'] - 0.19) < 1e-12 and abs(r['read_at_readout'] - 2.225) < 1e-12,
          f"between {r['between']}, count {r['intervals_holding_the_target']}, p {r['p_read']:.4f}")
    r = na.read_along([(2, 4.30, None), (2.25, 4.25, 0.11), (2.5, 4.20, 0.12)], 4.27)
    check('an undefined p* at the bracket: UNDEFINED_FIT', r['status'] == 'UNDEFINED_FIT' and 'p_read' not in r, r['status'])
    r = na.read_along([(2, 4.30, 0.10), (2.25, 4.25, 0.11), (2.5, 4.20, None)], 4.27)
    check('an undefined p* off the bracket does not matter', r['status'] == 'READ', r['status'])
    per_d = {(512, 'x'): {3.0: dict(p=None, train=4.27)}, (768, 'x'): {2.0: dict(p=0.1, train=4.3), 2.25: dict(p=0.11, train=4.25)}}
    r = na.draw_row(per_d, (512, 'x'), (768, 'x'), 'matched', 'train', 3.0, (2.0, 2.25))
    check("an undefined p* of 512 at E3: UNDEFINED_FIT", r['status'] == 'UNDEFINED_FIT' and 'value' not in r, r['status'])


FIRST, SECOND, FINAL, PATH = na.PLAN['first'], na.PLAN['second'], na.PLAN['final'], na.PLAN['path']


def synthetic_study(n_outside=0, missing=(), undefined_768_final=0, h1_shift=0.004, h2_shift=-0.004):
    """24 draws on N8's grid. Along the path, 768's training loss falls and its p* rises linearly; 512's E3 target is read between
    E2.6 and E2.88, so no bracket touches E3, except in the first n_outside draws, where it lies below the path's end. H1 is h1_shift
    plus a smooth wiggle; H2 is h2_shift plus an alternating term whose mean over 24 draws is 0. In the last undefined_768_final draws,
    768's fit at E3 is undefined."""
    per = {}
    for k, d in enumerate(na.DRAWS):
        if d in missing: per[d] = None; continue
        r = 2.6 + 0.012 * k
        arm768 = {e: dict(p=0.09 + 0.01 * (e - 2), train=4.4 - 0.25 * (e - 2), validation=4.7, gap=0.3, saturated=False) for e in na.READOUTS}
        p512 = 0.09 + 0.01 * (r - 2) + h1_shift + 0.003 * math.sin(2.1 * k + 0.4)
        arm768[FINAL]['p'] = None if k >= 24 - undefined_768_final else p512 - h2_shift - 0.003 * (-1) ** k
        target = 4.0 if k < n_outside else 4.4 - 0.25 * (r - 2)
        arm512 = {e: dict(p=p512 if e == FINAL else 0.05, train=target if e == FINAL else 5.0, validation=4.7, gap=0.3, saturated=False) for e in na.READOUTS}
        per[d] = {FIRST: arm512, SECOND: arm768}
    return per


def availability_and_decision():
    print('--- availability and the decision (N8 grid, 24 draws, minimum 20)')
    check('plan grid: 28 readouts, a 25-readout path every 64 updates from 2,048 to 3,584, E3 on it',
          len(na.READOUTS) == 28 and len(PATH) == 25 and PATH[0] == 2.0 and PATH[-1] == 3.5 and FINAL in PATH and all(abs(b - a - 0.0625) < 1e-15 for a, b in zip(PATH, PATH[1:])),
          f'{len(na.READOUTS)} readouts, path {PATH[0]}..{PATH[-1]}, minimum {na.PLAN["min_draws"]} draws')
    quarters = [(2.0, 2.25, 3, 1), (2.25, 2.5, 3, 2), (2.5, 2.75, 3, 3), (2.75, 3.0, 3, 4), (3.0, 3.25, 4, 1), (3.25, 3.5, 4, 2)]
    steps = na.window_steps(PATH, na.PLAN['windows'])
    check("S-b windows: quarters; on N8's 64-update path the order check uses exactly the six quarter windows, none unaligned",
          na.PLAN['windows'] == 4 and steps == quarters and na.window_steps((2.0, 2.25, 2.5, 2.75, 3.0, 3.25, 3.5), 4) == quarters, f'{len(steps)} steps')
    out = na.decide(synthetic_study(n_outside=5)); h1 = out['statistics']['H1']
    check('19 of 24 available for H1: H1 UNAVAILABLE, REVERSAL_NOT_REPLICATED', len(h1['available']) == 19 and out['labels'] == dict(H1='UNAVAILABLE', H2='CONFIRMED') and out['joint'] == 'REVERSAL_NOT_REPLICATED' and 'interval' not in h1,
          f"labels {out['labels']}, {out['joint']}, TARGET_OUTSIDE_PATH {h1['unavailable_counts']['TARGET_OUTSIDE_PATH']}")
    out = na.decide(synthetic_study(n_outside=4)); h1 = out['statistics']['H1']
    check('20 of 24 available: both read, REVERSAL_REPLICATED', len(h1['available']) == 20 and out['labels'] == dict(H1='CONFIRMED', H2='CONFIRMED') and out['joint'] == 'REVERSAL_REPLICATED',
          f"H1 {h1['interval']['mean']:+.5f} [{h1['interval']['interval'][0]:+.5f}, {h1['interval']['interval'][1]:+.5f}], envelope over {h1['envelope']['combinations']} combinations")
    out = na.decide(synthetic_study(undefined_768_final=5)); h2 = out['statistics']['H2']
    check("an undefined 768 fit at E3 in 5 draws: H2 UNAVAILABLE (19 of 24), H1 unaffected", out['labels'] == dict(H1='CONFIRMED', H2='UNAVAILABLE') and h2['unavailable_counts']['UNDEFINED_FIT'] == 5 and out['joint'] == 'REVERSAL_NOT_REPLICATED', str(out['labels']))
    out = na.decide(synthetic_study(missing=('n01', 'n02', 'n03', 'n04', 'n05')))
    check('19 completed draws: INCOMPLETE, no statistic and no label', out['status'] == 'INCOMPLETE' and out['labels'] is None and out['joint'] is None and 'statistics' not in out, out['note'])
    out = na.decide(synthetic_study(missing=('n01', 'n02', 'n03', 'n04')))
    check('20 completed draws: read, failed draws counted as DRAW_MISSING for both', out['status'] == 'COMPLETE_WITH_FAILED_DRAWS' and all(s['unavailable_counts']['DRAW_MISSING'] == 4 for s in out['statistics'].values()) and out['joint'] == 'REVERSAL_REPLICATED', str(out['labels']))
    out = na.decide(synthetic_study(h2_shift=0.0))
    check('H2 interval including 0: INCONCLUSIVE, REVERSAL_NOT_REPLICATED', out['labels'] == dict(H1='CONFIRMED', H2='INCONCLUSIVE') and out['joint'] == 'REVERSAL_NOT_REPLICATED', str(out['labels']))
    out = na.decide(synthetic_study(h1_shift=-0.004, h2_shift=0.004))
    check('both on the wrong side: CONTRARY', out['labels'] == dict(H1='CONTRARY', H2='CONTRARY') and out['joint'] == 'REVERSAL_NOT_REPLICATED', str(out['labels']))


def saturation():
    print('--- saturation (fits at or above 7.999 refitted with the upper bound at 32)')
    n, nv = 400, 4
    w = np.array([math.exp(math.log(.01) + (math.log(10) - math.log(.01)) * (i + .5) / n) for i in range(n)]); w = (w / w.mean()).astype('<f4')

    def arm(g):
        e0 = np.concatenate([5.0 + g, np.full(nv, 5.0)]).astype('<f4'); arr = np.full(n + nv, 5.0, dtype='<f4')
        return dict(e0=e0.tobytes(), arrays=arr.tobytes(), record=dict(layout=dict(train_rows=n, validation_rows=nv, block_epochs=[3.0]), readouts=[dict(epoch=3.0, train_loss=5.0, validation_loss=5.0)]))

    shallow, steep, one = (na.arm_points(w.tolist(), arm(g))[3.0] for g in (0.5 * (w / w.max()) ** 0.5, 0.5 * (w / w.max()) ** 12, (np.arange(n) == n - 1) * 1.0))
    check('a fit below 7.999 is not refitted', shallow['p'] < na.P_UPPER and 'p32' not in shallow and not shallow['saturated'], f"p {shallow['p']:.4f}")
    check('gains rising as w^12: bound-8 fit at the bound, resolved at bound 32, not saturated', steep['p'] >= na.P_UPPER and steep['p32'] < 31.999 and not steep['saturated'], f"p {steep['p']}, at bound 32 {steep['p32']:.4f}")
    check('all gain on the heaviest sequence: unresolved at bound 32, SATURATED', one['p'] >= na.P_UPPER and one['saturated'], f"p {one['p']}, at bound 32 {one['p32']}")
    per = synthetic_study()
    per['n01'][SECOND][FINAL] = dict(per['n01'][SECOND][FINAL], p=8.0, p32=None, saturated=True)
    per['n02'][SECOND][FINAL] = dict(per['n02'][SECOND][FINAL], p=8.0, p32=9.5, saturated=False)
    h2 = na.decide(per)['statistics']['H2']; sat = h2['saturation']
    check('a saturated fit makes its draw unavailable (SATURATED); a resolved one stays, with its value at bound 32 reported',
          h2['unavailable'] == {'n01': 'SATURATED'} and h2['unavailable_counts']['SATURATED'] == 1 and sat['flagged'] == ['n01', 'n02'] and sat['saturated'] == ['n01']
          and abs(sat['values_at_bound_32']['n02'] - (h2['values']['n02'] + 8.0 - 9.5)) < 1e-12 and 'interval_at_bound_32' in sat, f"available {len(h2['available'])}")


def tests_and_intervals():
    print('--- sign test, leave-one-out, intervals')
    cases = [([1] * 6, (6, 0, 0, 0.03125)), ([1] * 5 + [0], (5, 0, 1, 0.0625)), ([1] * 5 + [-1], (5, 1, 0, 0.21875)), ([0, 0], (0, 0, 2, None))]
    for values, (pos, neg, zeros, p) in cases:
        s = na.sign_test(values)
        check(f'sign test {values}', (s['positive'], s['negative'], s['zeros']) == (pos, neg, zeros) and (s['p'] == p if p is None else abs(s['p'] - p) < 1e-15), f"p {s['p']}")
    vals = {f'd{k}': 0.01 + 0.004 * math.sin(k) for k in range(6)}; loo = na.leave_one_out(vals)
    direct = {d: na.t_interval([v for k, v in vals.items() if k != d]) for d in vals}
    check('leave-one-out intervals equal the interval of the remaining draws, df n - 2', all(loo[d]['interval'] == direct[d]['interval'] and loo[d]['df'] == 4 for d in vals))
    t = na.t_interval([0.003] * 4)
    check('a constant sample is degenerate, with a zero-width interval', t['degenerate'] and t['interval'][0] == t['interval'][1] == t['mean'], str(t['interval']))


def envelope():
    print('--- bracket envelope')
    worst = 0.0
    for n in (2, 3, 5, 10, 13):
        ends = synthetic_ends(n); env = na.bracket_envelope(ends); low, up = brute(ends)
        worst = max(worst, abs(env['min_lower'] - low), abs(env['max_upper'] - up))
    check('against itertools brute force, n = 2, 3, 5, 10, 13 (1e-12)', worst <= 1e-12, f'largest difference {worst:.2g}')
    ends = [[0.01 + 0.001 * k, 0.01 + 0.001 * k] for k in range(7)]; env = na.bracket_envelope(ends); t = na.t_interval([e[0] for e in ends])
    check('brackets of zero width: the envelope is the plain interval', abs(env['min_lower'] - t['interval'][0]) <= 1e-15 and abs(env['max_upper'] - t['interval'][1]) <= 1e-15)
    try:
        na.bracket_envelope([[0.1, 0.2]]); refused = False
    except ValueError:
        refused = True
    check('one draw is refused', refused)
    ends = synthetic_ends(24); tracemalloc.start(); t0 = time.perf_counter(); env = na.bracket_envelope(ends); took = time.perf_counter() - t0; peak = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
    check(f"24 draws: {env['combinations']:,} combinations in {took:.1f} s, peak traced memory {peak / 2 ** 20:.1f} MiB", env['combinations'] == 1 << 24 and peak < 256 * 2 ** 20,
          f"min lower {env['min_lower']:+.7f}, max upper {env['max_upper']:+.7f}")
    t0 = time.perf_counter(); low, up = numpy_brute(ends); took_b = time.perf_counter() - t0
    check('24 draws against a direct enumeration of all 2^24 combinations (1e-12)', abs(env['min_lower'] - low) <= 1e-12 and abs(env['max_upper'] - up) <= 1e-12,
          f'differences {abs(env["min_lower"] - low):.2g} / {abs(env["max_upper"] - up):.2g}; direct enumeration {took_b:.0f} s')
    check('the reported vertices give the reported limits', abs(env['at_min_lower']['interval'][0] - env['min_lower']) <= 1e-12 and abs(env['at_max_upper']['interval'][1] - env['max_upper']) <= 1e-12)
    v = np.asarray(ends); worst_in = math.inf; best_in = -math.inf; q = na.t_quantile(0.975, 23)
    for k in range(20000):
        lam = np.array([(0.5 + (k + 1) * (j + 1) * 0.6180339887498949) % 1.0 for j in range(24)]); x = v[:, 0] + lam * (v[:, 1] - v[:, 0])
        m = x.mean(); h = q * x.std(ddof=1) / math.sqrt(24); worst_in = min(worst_in, m - h); best_in = max(best_in, m + h)
    check('20,000 interior points stay inside the vertex extremes (concavity)', worst_in >= env['min_lower'] - 1e-15 and best_in <= env['max_upper'] + 1e-15,
          f'interior min lower {worst_in:+.7f}, max upper {best_in:+.7f}')


if __name__ == '__main__':
    print(f'numpy {np.__version__}, python {sys.version.split()[0]}')
    t_quantiles(); reading_rule(); availability_and_decision(); saturation(); tests_and_intervals(); envelope()
    print(f'{sum(results)} passed, {len(results) - sum(results)} failed')
    raise SystemExit(0 if all(results) else 1)
