"""Independent re-check of the main findings of the follow-up audit of 12 November 2026 (post hoc, descriptive).

    python verify_findings.py <repository root> <unpacked n7-loss-arrays bundle>    -> OUTPUT.txt on stdout

Written by the supervising session (Claude Opus 5.5) separately from the auditors' code. It reads only published files:
N4's FITS.csv, N5's POINTS.csv, N7's ANALYSIS.json, the post-hoc RESULTS.json of 11 November, and the N7 loss-array
bundle attached to the v1.0 release. Needs NumPy, SciPy and PyTorch (CPU; PyTorch only to regenerate batch orders).
Intervals are two-sided 95% t intervals over draws, unadjusted unless stated.
"""
import csv, json, math, sys
from pathlib import Path
import numpy as np
import torch
from scipy import stats

ROOT, BUNDLE = Path(sys.argv[1]), Path(sys.argv[2])
sys.path.insert(0, str(ROOT / 'tools'))
from verify_n7_losses import exponent  # the record's own NumPy implementation of the estimator


def ci(x, t=None):
    x = np.asarray(x, float); n = len(x); t = t or stats.t.ppf(.975, n - 1)
    m = x.mean(); h = t * x.std(ddof=1) / math.sqrt(n)
    return f"{m:+.4f} [{m - h:+.4f}, {m + h:+.4f}], {int((x > 0).sum())}/{n} positive"


# --- EA-1: N5's M (768 - 384 at matched gap) and its sensitivity --------------------------------------------------
rows = list(csv.DictReader(open(ROOT / 'reports/natural-text-fewepoch-analysis-20261103-01/POINTS.csv')))
draws = sorted({r['draw'] for r in rows})


def path(d, w):
    rs = sorted((r for r in rows if r['draw'] == d), key=lambda r: float(r['epoch']))
    return [(float(r['epoch']), float(r[f'gap_{w}']), float(r[f'p_{w}'])) for r in rs]


def read(pth, level, mode):
    """First crossing of the gap level; p* by linear interpolation, or the higher or lower end of the bracket."""
    for (e0, g0, p0), (e1, g1, p1) in zip(pth, pth[1:]):
        if (g0 - level) * (g1 - level) <= 0 and g0 != g1:
            t = (level - g0) / (g1 - g0)
            p = {'lin': p0 + t * (p1 - p0), 'hi': max(p0, p1), 'lo': min(p0, p1)}[mode]
            return p, e0 + t * (e1 - e0)


M = {k: [] for k in ('registered', '768 at higher end', '384 at lower end', 'both')}
lead, pred = [], []
for d in draws:
    a, b = path(d, 384), path(d, 768)
    lo = max(min(g for _, g, _ in a), min(g for _, g, _ in b)); hi = min(max(g for _, g, _ in a), max(g for _, g, _ in b))
    lv = np.linspace(lo, hi, 101)
    for k, (ma, mb) in {'registered': ('lin', 'lin'), '768 at higher end': ('lin', 'hi'),
                        '384 at lower end': ('lo', 'lin'), 'both': ('lo', 'hi')}.items():
        M[k].append(np.mean([read(b, l, mb)[0] - read(a, l, ma)[0] for l in lv]))
    ea, pa = [e for e, _, _ in a], [p for _, _, p in a]
    lead.append(np.mean([read(a, l, 'lin')[1] - read(b, l, 'lin')[1] for l in lv]))
    pred.append(np.mean([np.interp(read(b, l, 'lin')[1], ea, pa) - np.interp(read(a, l, 'lin')[1], ea, pa) for l in lv]))
print('EA-1  N5, M = p*(768) - p*(384) at matched gap')
for k, v in M.items(): print(f'      {k:18s} {ci(v)}')
print(f'      epochs by which 384 is read later than 768 at equal gap: {ci(lead)}')
print(f'      M predicted by an epoch-only curve (each draw\'s own 384 path): {ci(pred)}')
print(f'      observed minus predicted: {ci(np.array(M["registered"]) - np.array(pred))}')
E2 = [r for r in rows if float(r['epoch']) == 2.0]
print(f'      epoch 2, gap 768 - 512: {ci([float(r["gap_768"]) - float(r["gap_512"]) for r in E2])}')
print(f'      epoch 2, p* 768 - 512:  {ci([float(r["p_768"]) - float(r["p_512"]) for r in E2])}')

# --- AA-4: N4 at epoch 32, total gain and p* x total gain ---------------------------------------------------------
fits = [x for x in csv.DictReader(open(ROOT / 'reports/natural-text-lateturn-analysis-20261031-01/FITS.csv')) if float(x['epoch']) == 32]
print('AA-4  N4 at epoch 32, mean over 4 draws: width, total gain, p* x total gain, p*')
for w in ('384', '512', '768'):
    s = [x for x in fits if x['width'] == w]
    print(f'      {w}  {np.mean([float(x["total_gain"]) for x in s]):7.0f}  '
          f'{np.mean([float(x["p"]) * float(x["total_gain"]) for x in s]):6.0f}  {np.mean([float(x["p"]) for x in s]):.3f}')

# --- AA-1 power and AA-7 multiplicity, from the stored post-hoc values --------------------------------------------
V = json.load(open(ROOT / 'reports/natural-text-matched-assistant-posthoc-20261111-01/RESULTS.json'))['values']
tc, tb = stats.t.ppf(.975, 5), stats.t.ppf(1 - .025 / 6, 5)
print('AA-1  every-pass matched contrasts: SE, power for an effect of +0.00909 (P1), effect detectable with 80% power')
print('AA-7  and Bonferroni intervals over the six every-pass comparisons (t = %.3f, df 5)' % tb)
for lr in ('lr1e-04', 'lr3e-04'):
    for k in (1, 2, 3):
        e = np.array(V[f'matched|{lr}|k{k}|every']); se = e.std(ddof=1) / math.sqrt(6)
        pw = 1 - stats.nct.cdf(tc, 5, .00909 / se) + stats.nct.cdf(-tc, 5, .00909 / se)
        d80 = next(x for x in np.arange(.0005, .1, .0001) if 1 - stats.nct.cdf(tc, 5, x / se) >= .8)
        print(f'      {lr} 768 at {2 + k / 4}: SE {se:.4f}, power {pw:.2f}, detectable {d80:.3f}; '
              f'every (Bonferroni) {ci(e, tb)}; whole minus every (Bonferroni) {ci(V[f"matched|{lr}|k{k}|whole_minus_every"], tb)}')

# --- AA-1 within-model, AA-3 E0 offset, AA-2 batch-relative weight, clipping ------------------------------------
man = json.load(open(BUNDLE / 'MANIFEST.json')); N, NV = 16384, 512
EP = [0.25, 0.5, 1, 2, 2.25, 2.5, 2.75, 3, 3.25, 3.5]


def load(d, w, lr):
    a = np.fromfile(BUNDLE / f'{d}/w{w}/{lr}/arrays.f32', '<f4').reshape(10, N + NV)[:, :N]
    return np.fromfile(BUNDLE / f'{d}/w{w}/E0.f32', '<f4')[:N], a


def order(d, e):
    s = man['draws'][d]['seeds']['adapt_order_seed']
    return torch.randperm(N, generator=torch.Generator().manual_seed(999 + s + e)).numpy()


def quarter(perm):
    q = np.empty(N, int); q[perm] = np.arange(N) // (N // 4) + 1; return q


P1rows = json.load(open(ROOT / 'reports/natural-text-matched-analysis-20261105-01/ANALYSIS.json'))['statistics']['P1']['rows']
res = {k: [] for k in ('within2', 'within3', 'whole2', 'whole3', 'P1', 'P1off', 'off')}
coef, clip = {512: [], 768: []}, []
for d in sorted(man['draws']):
    w = np.fromfile(BUNDLE / f'{d}/weights.f32', '<f4')
    perms = {e: order(d, e) for e in (1, 2, 3)}; Q = {e: quarter(p) for e, p in perms.items()}
    e05, a5 = load(d, 512, 'lr1e-04'); e07, a7 = load(d, 768, 'lr1e-04')
    fit = lambda e0, a, i, m=None: exponent(w if m is None else w[m], (e0 - a[i]) if m is None else (e0 - a[i])[m])
    for k in (2, 3):
        S7 = (Q[1] <= k) & (Q[2] <= k) & (Q[3] <= k); S5 = (Q[1] >= 5 - k) & (Q[2] >= 5 - k) & (Q[3] >= 5 - k)
        res[f'within{k}'].append(fit(e07, a7, EP.index(3), S5) - fit(e07, a7, EP.index(2 + k / 4), S7))
        res[f'whole{k}'].append(fit(e07, a7, EP.index(3)) - fit(e07, a7, EP.index(2 + k / 4)))
    r = P1rows[d]; i0, i1 = EP.index(r['between'][0]), EP.index(r['between'][1])
    q0, q1 = fit(e07, a7, i0), fit(e07, a7, i1)
    tw = next(t for t in (r['weight'], 1 - r['weight']) if abs((1 - t) * q0 + t * q1 - r['p_read']) < 1e-6)
    off = float(e07.mean() - e05.mean()); p5 = fit(e05, a5, EP.index(3))
    p7 = (1 - tw) * q0 + tw * q1; p7o = (1 - tw) * fit(e07 - off, a7, i0) + tw * fit(e07 - off, a7, i1)
    res['P1'].append(p5 - p7); res['P1off'].append(p5 - p7o); res['off'].append(p7o - p7)
    lw = np.log(w); mates = np.empty(N)
    for b in perms[3].reshape(-1, 16): mates[b] = np.log(w[b].sum() - w[b])
    for wd, a in ((512, a5), (768, a7)):
        X, Y = [], []
        for qq in range(1, 5):
            m = Q[3] == qq; Y.append(a[EP.index(2 + (qq - 1) / 4)][m] - a[EP.index(2 + qq / 4)][m])
            X.append(np.c_[np.ones(m.sum()), lw[m], mates[m], *(np.full(m.sum(), float(qq == j)) for j in (2, 3, 4))])
        coef[wd].append(np.linalg.lstsq(np.vstack(X), np.concatenate(Y), rcond=None)[0][1:3])
    for wd in (512, 768):
        for lr in ('lr1e-04', 'lr3e-04'):
            clip += [e['clip_fraction'] for e in json.load(open(BUNDLE / f'{d}/w{wd}/{lr}/record.json'))['epochs']]
print('AA-1  768 at 1e-4, within one model, exposure-matched sets: p*(epoch 3, late set) - p*(epoch 2+k/4, early set)')
print(f'      k = 2: {ci(res["within2"])}; whole set over the same readouts: {ci(res["whole2"])}')
print(f'      k = 3: {ci(res["within3"])}; whole set over the same readouts: {ci(res["whole3"])}')
print('AA-3  P1 recomputed:', ci(res['P1']))
print('      with 768\'s gains lowered by its mean E0 excess over 512:', ci(res['P1off']), '; change in 768\'s p*:', ci(res['off']))
print('AA-2  epoch-3 loss drop over the quarter in which a sequence is trained, on log own weight and log sum of its')
print('      15 batch-mates\' weights (quarter fixed effects), 1e-4:')
for wd, c in coef.items():
    c = np.array(c); print(f'      {wd}: own {ci(c[:, 0])}; batch-mates {ci(c[:, 1])}')
print(f'      fraction of updates clipped, per arm and epoch: {min(clip):.3f} to {max(clip):.3f} ({len(clip)} values)')

# --- AA-6: p* by weight range at epoch 3, and P1 and S4 on the lower half of the weights -------------------------
A = json.load(open(ROOT / 'reports/natural-text-matched-analysis-20261105-01/ANALYSIS.json'))['statistics']
half = {k: [] for k in ('p lower', 'p upper', 'p all', 'P1 lower', 'S4 lower', 'gain deciles')}
for d in sorted(man['draws']):
    w = np.fromfile(BUNDLE / f'{d}/weights.f32', '<f4'); lowm = w <= np.median(w)
    for stat, lr in (('P1', 'lr1e-04'), ('S4', 'lr3e-04')):
        e05, a5 = load(d, 512, lr); e07, a7 = load(d, 768, lr); r = A[stat]['rows'][d]
        f = lambda e0, a, i, m: exponent(w[m], (e0 - a[i])[m])
        i0, i1 = EP.index(r['between'][0]), EP.index(r['between'][1])
        allm = np.ones(N, bool); q0, q1 = f(e07, a7, i0, allm), f(e07, a7, i1, allm)
        tw = next(t for t in (r['weight'], 1 - r['weight']) if abs((1 - t) * q0 + t * q1 - r['p_read']) < 1e-6)
        half[f'{stat} lower'].append(f(e05, a5, EP.index(3), lowm) - ((1 - tw) * f(e07, a7, i0, lowm) + tw * f(e07, a7, i1, lowm)))
        if stat == 'P1':
            g = e05 - a5[EP.index(3)]
            half['p lower'].append(f(e05, a5, EP.index(3), lowm)); half['p upper'].append(f(e05, a5, EP.index(3), ~lowm))
            half['p all'].append(f(e05, a5, EP.index(3), allm))
            dec = np.digitize(w, np.quantile(w, np.linspace(.1, .9, 9)))
            half['gain deciles'].append([g[dec == j].mean() / g.mean() for j in range(10)])
print('AA-6  512 at 1e-4, epoch 3: p* on the lower half of the weights', ci(half['p lower']), '; upper half', ci(half['p upper']),
      '; all', ci(half['p all']))
print('      mean gain by weight decile, relative to the overall mean:', ' '.join(f'{x:.2f}' for x in np.mean(half['gain deciles'], 0)))
print('      on the lower half of the weights: P1', ci(half['P1 lower']), '; S4', ci(half['S4 lower']))

# --- EA-10 and C2's scope: N4 by epoch, and two other alignments at epoch 32 ------------------------------------
n4 = list(csv.DictReader(open(ROOT / 'reports/natural-text-lateturn-analysis-20261031-01/POINTS.csv')))
print('EA-10 N4 (WikiText-2, 3e-5): slope of p* on log2 width over 384-768 by epoch; mean gap at 768')
for e in sorted({float(r['epoch']) for r in n4}):
    rs = [r for r in n4 if float(r['epoch']) == e]
    print(f'      epoch {e:4g}: {ci([float(r["turn"]) for r in rs])}; gap at 768 {np.mean([float(r["gap_768"]) for r in rs]):.2f}')
at_gap, best = [], []
for d in sorted({r['draw'] for r in n4}):
    rs = sorted((r for r in n4 if r['draw'] == d), key=lambda r: float(r['epoch']))
    tgt = float(rs[-1]['gap_384']); g = [float(r['gap_768']) for r in rs]; p = [float(r['p_768']) for r in rs]
    i = next(i for i in range(len(g) - 1) if (g[i] - tgt) * (g[i + 1] - tgt) <= 0); t = (tgt - g[i]) / (g[i + 1] - g[i])
    at_gap.append(float(rs[-1]['p_384']) - (p[i] + t * (p[i + 1] - p[i])))
    best.append(max(float(r['p_384']) for r in rs) - max(float(r['p_768']) for r in rs))
print(f'      p*(384, epoch 32) - p*(768 read at that gap): {ci(at_gap)}')
print(f'      highest p* over readouts, 384 - 768: {ci(best)}')

# --- EA-5 and EA-6: direction of the bias of N6's coarse rule, measured on N7's draws ----------------------------
# N6's rule reads one arm at the other arm's epoch-3 value by linear interpolation between readouts 0.25, 0.5, 1, 2
# and 3 only; N7's own rule also uses the quarter readouts. Contrast = p*(first) - p*(second), as in the record.
pts = list(csv.DictReader(open(ROOT / 'reports/natural-text-matched-analysis-20261105-01/POINTS.csv')))
COARSE = [0.25, 0.5, 1.0, 2.0, 3.0]


def traj(d, w, tag, key, epochs=None):
    rs = sorted((r for r in pts if r['draw'] == d and r['width'] == str(w) and r['tag'] == tag), key=lambda r: float(r['epoch']))
    rs = [r for r in rs if float(r['epoch']) <= 3.0 and (epochs is None or float(r['epoch']) in epochs)]
    return [(float(r[key]), float(r['p'])) for r in rs]


def read_at(path_, target):
    for (v0, p0), (v1, p1) in zip(path_, path_[1:]):
        if (v0 - target) * (v1 - target) <= 0 and v0 != v1:
            return p0 + (target - v0) / (v1 - v0) * (p1 - p0)


def bias(first, second, key, read_first):
    """Coarse minus fine contrast, on the draws where both rules give a reading. read_first: the first arm is read."""
    co, fi = [], []
    for d in sorted({r['draw'] for r in pts}):
        fixed, moving = (second, first) if read_first else (first, second)
        e3 = [r for r in pts if r['draw'] == d and r['width'] == str(fixed[0]) and r['tag'] == fixed[1] and float(r['epoch']) == 3.0][0]
        tgt, pfix = float(e3[key]), float(e3['p'])
        c, f = read_at(traj(d, *moving, key, COARSE), tgt), read_at(traj(d, *moving, key, None), tgt)
        if c is None or f is None: continue
        co.append(c - pfix if read_first else pfix - c); fi.append(f - pfix if read_first else pfix - f)
    return len(co), ci(np.array(co) - np.array(fi)), ci(co), ci(fi)


print('EA-5  N6\'s coarse rule applied to N7: coarse minus fine contrast (n draws; then coarse and fine contrasts)')
for name, first, second, key, rf in (
        ('P1 type, 1e-4, training loss, 768 read', (512, 'lr1e-04'), (768, 'lr1e-04'), 'train', False),
        ('S4 type, 3e-4, training loss, 768 read', (512, 'lr3e-04'), (768, 'lr3e-04'), 'train', False),
        ('D2 type, 3e-4, gap, 512 read', (512, 'lr3e-04'), (768, 'lr3e-04'), 'gap', True),
        ('D3 type, 512@3e-4 - 768@1e-4, gap, 512 read', (512, 'lr3e-04'), (768, 'lr1e-04'), 'gap', True)):
    n, b, c, f = bias(first, second, key, rf); print(f'      {name}: n = {n}; bias {b}; coarse {c}; fine {f}')
