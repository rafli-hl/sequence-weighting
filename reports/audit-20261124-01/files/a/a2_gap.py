"""POST HOC, descriptive (auditor A). Independent recomputation of the 23 November correction's F2 scale from N5's
published POINTS.csv. Standard library; own t quantile. Usage: python a2_gap.py <repo root>
"""
import csv, math, statistics as st, sys
from pathlib import Path

root = Path(sys.argv[1])
rows = list(csv.DictReader(open(root / 'reports/natural-text-fewepoch-analysis-20261103-01/POINTS.csv', encoding='utf-8')))
epochs = sorted({float(r['epoch']) for r in rows}); draws = sorted({r['draw'] for r in rows})
print('readouts in N5 POINTS.csv:', epochs, '| draws:', len(draws), draws[0], '..', draws[-1])
R = {(r['draw'], float(r['epoch'])): r for r in rows}
g = lambda d, e, w: float(R[(d, e)][f'gap_{w}']); p = lambda d, e, w: float(R[(d, e)][f'p_{w}'])


def t_cdf9(t):
    th = math.atan(t / 3.0); s, c = math.sin(th), math.cos(th)
    return 0.5 + (th + s * (c + 2 / 3 * c**3 + 8 / 15 * c**5 + 48 / 105 * c**7)) / math.pi


lo, hi = 0.0, 50.0
for _ in range(200):
    mid = (lo + hi) / 2
    lo, hi = (mid, hi) if t_cdf9(mid) < 0.975 else (lo, mid)
T9 = (lo + hi) / 2
print(f't(0.975, df=9) = {T9:.13f}')


def ci(v):
    m, h = st.mean(v), T9 * st.stdev(v) / math.sqrt(len(v)); return m, m - h, m + h


dg = [g(d, 2.0, 768) - g(d, 2.0, 512) for d in draws]
dp = [p(d, 2.0, 768) - p(d, 2.0, 512) for d in draws]
print('E2 gap 768-512:  %+.5f [%+.5f, %+.5f]; draws %+.5f to %+.5f; %d/10 above 0' % (*ci(dg), min(dg), max(dg), sum(x > 0 for x in dg)))
print('E2 p*  768-512:  %+.5f [%+.5f, %+.5f]; %d/10 above 0' % (*ci(dp), sum(x > 0 for x in dp)))
sl = {}
for w in (512, 768):
    for a, b in ((1.0, 2.0), (2.0, 3.0)):
        s = [(p(d, b, w) - p(d, a, w)) / (g(d, b, w) - g(d, a, w)) for d in draws]
        sl[(w, a, b)] = st.mean(s)
        dgap = [g(d, b, w) - g(d, a, w) for d in draws]
        print(f'width {w}, E{a:g}->E{b:g}: mean of per-draw slopes {st.mean(s):.3f} (draws {min(s):.3f} to {max(s):.3f}); '
              f'ratio of mean changes {st.mean([p(d, b, w) - p(d, a, w) for d in draws]) / st.mean(dgap):.3f}; gap change {min(dgap):+.3f} to {max(dgap):+.3f} nats')
smin, smax = min(sl.values()), max(sl.values())
m, a, b = ci(dg)
print(f'slopes {smin:.3f} to {smax:.3f}; upper limit {b:.5f} nats -> {b * smin:.5f} to {b * smax:.5f} of p*; share of |p* difference| {b * smin / abs(st.mean(dp)):.3f} to {b * smax / abs(st.mean(dp)):.3f}')
print(f'  lower limit {a:.5f} nats -> {a * smin:.5f} to {a * smax:.5f} of p* (the sign that would go with 768 having the lower p*)')
print(f'  largest single-draw gap difference {max(dg, key=abs):+.5f} nats -> {abs(max(dg, key=abs)) * smin:.5f} to {abs(max(dg, key=abs)) * smax:.5f} of p*')
# across draws at E2: does the 768-512 p* difference move with the gap difference? (descriptive)
mg, mp = st.mean(dg), st.mean(dp)
sxy = sum((x - mg) * (y - mp) for x, y in zip(dg, dp)); sxx = sum((x - mg) ** 2 for x in dg); syy = sum((y - mp) ** 2 for y in dp)
print(f'across the 10 draws at E2: slope of (p* difference) on (gap difference) {sxy / sxx:+.3f} per nat, r = {sxy / math.sqrt(sxx * syy):+.3f}; '
      f'p* difference at zero gap difference (intercept) {mp - sxy / sxx * mg:+.5f}')
print('per draw (gap difference, p* difference):', ', '.join(f'{d} {x:+.4f} {y:+.4f}' for d, x, y in zip(draws, dg, dp)))
