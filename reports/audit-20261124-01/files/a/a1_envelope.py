"""POST HOC, descriptive (auditor A). Recomputes the 23 November correction's F1 table from N7's published
POINTS.csv and MATCHED.csv only. Standard library. Usage: python a1_envelope.py <repo root>
"""
import csv, itertools, math, statistics as st, sys
from pathlib import Path

root = Path(sys.argv[1])
A = root / 'reports' / 'natural-text-matched-analysis-20261105-01'


def t_cdf_odd(t, nu):
    """Student t CDF for odd nu (closed form, Abramowitz & Stegun 26.7.3)."""
    th = math.atan(t / math.sqrt(nu))
    s, c = math.sin(th), math.cos(th)
    term, tot = c, c if nu > 1 else 0.0
    k = 1
    while 2 * k + 1 <= nu - 2:
        term *= (2 * k) / (2 * k + 1) * c * c
        tot += term
        k += 1
    a = 2 / math.pi * (th + s * tot) if nu > 1 else 2 / math.pi * th
    return 0.5 + a / 2


def t_q(p, nu):
    lo, hi = 0.0, 50.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if t_cdf_odd(mid, nu) < p: lo = mid
        else: hi = mid
    return (lo + hi) / 2


T5 = t_q(0.975, 5)
print(f't(0.975, df=5) = {T5:.13f}  (own bisection on the closed-form CDF)')

P = {}
for r in csv.DictReader(open(A / 'POINTS.csv', encoding='utf-8')):
    P[(r['draw'], float(r['epoch']), int(r['width']), r['tag'])] = r
M = [r for r in csv.DictReader(open(A / 'MATCHED.csv', encoding='utf-8'))]
RATE = {'P1': 'lr1e-04', 'S1': 'lr1e-04', 'S4': 'lr3e-04'}
KEY = {'P1': 'train', 'S1': 'gap', 'S4': 'train'}


def ci(v, t=T5):
    m, h = st.mean(v), t * st.stdev(v) / math.sqrt(len(v))
    return m, m - h, m + h


for stat in ('P1', 'S1', 'S4'):
    rows = [r for r in M if r['statistic'] == stat]
    assert len(rows) == 6 and all(r['status'] == 'READ' for r in rows)
    sealed, early, late, info = [], [], [], []
    for r in rows:
        d, lo, hi = r['draw'], float(r['between_low']), float(r['between_high'])
        p512 = float(P[(d, 3.0, 512, RATE[stat])]['p'])
        assert abs(p512 - float(r['p_first'])) < 1e-15
        plo, phi = (float(P[(d, e, 768, RATE[stat])]['p']) for e in (lo, hi))
        xlo, xhi = (float(P[(d, e, 768, RATE[stat])][KEY[stat]]) for e in (lo, hi))
        tgt = float(P[(d, 3.0, 512, RATE[stat])][KEY[stat]])
        assert abs(tgt - float(r['target'])) < 1e-12 and min(xlo, xhi) <= tgt <= max(xlo, xhi)
        w = (tgt - xlo) / (xhi - xlo)                   # my own interpolation weight, from the losses in POINTS.csv
        mine = p512 - (plo + w * (phi - plo))
        assert abs(mine - float(r['value'])) < 1e-12, (stat, d, mine, r['value'])
        sealed.append(float(r['value'])); early.append(p512 - plo); late.append(p512 - phi)
        info.append((d, lo, hi, plo, phi, w))
    print(f'\n== {stat} ({RATE[stat]}, matched on {KEY[stat]}) ==')
    for (d, lo, hi, plo, phi, w), s, e, l in zip(info, sealed, early, late):
        print(f'  {d}: bracket {lo:g}-{hi:g}, weight {w:.4f}; p768 {plo:.6f} -> {phi:.6f} ({"rises" if phi > plo else "FALLS"}); '
              f'contrast sealed {s:+.6f}, earlier end {e:+.6f}, later end {l:+.6f}')
    m, a, b = ci(sealed); print(f'  sealed (interpolated): {m:+.5f} [{a:+.5f}, {b:+.5f}], {sum(x > 0 for x in sealed)}/6 above 0')
    m, a, b = ci(late);   print(f'  all later ends       : {m:+.5f} [{a:+.5f}, {b:+.5f}], {sum(x > 0 for x in late)}/6 above 0')
    m, a, b = ci(early);  print(f'  all earlier ends     : {m:+.5f} [{a:+.5f}, {b:+.5f}], {sum(x > 0 for x in early)}/6 above 0')
    res = []
    for combo in itertools.product((0, 1), repeat=6):   # 0 = earlier end, 1 = later end
        v = [late[i] if c else early[i] for i, c in enumerate(combo)]
        m, a, b = ci(v)
        res.append((a, m, b, combo))
    res.sort()
    a, m, b, combo = res[0]
    print(f'  64 combinations: lowest lower limit {a:+.7f} (mean {m:+.5f}, upper {b:+.5f}) at '
          f'{"".join("L" if c else "E" for c in combo)} (draw order m01..m06; E earlier, L later)')
    a2 = ci([late[i] if c else early[i] for i, c in enumerate(combo)], t=2.5706)[1]
    print(f'    same combination with t = 2.5706: {a2:+.7f}')
    print(f'    second lowest: {res[1][0]:+.7f} at {"".join("L" if c else "E" for c in res[1][3])}; '
          f'combinations with lower limit <= 0: {sum(r[0] <= 0 for r in res)} of 64; '
          f'highest lower limit {res[-1][0]:+.7f}')
    means = sorted((r[1], r[3]) for r in res)
    print(f'    lowest mean over the 64: {means[0][0]:+.5f} at {"".join("L" if c else "E" for c in means[0][1])}')
    # random interior points of the box: is any lower limit below the vertex minimum? (concavity check, descriptive)
    import random
    rng = random.Random(20261123)
    worst = min(ci([early[i] + rng.random() * (late[i] - early[i]) for i in range(6)])[1] for _ in range(200000))
    print(f'    200,000 random interior readings: lowest lower limit {worst:+.7f} (vertex minimum {a:+.7f})')
