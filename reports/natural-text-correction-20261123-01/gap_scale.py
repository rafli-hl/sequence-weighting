"""The scale behind the 23 November correction's F2, from N5's published POINTS.csv (post hoc, descriptive; standard library).

    python reports/natural-text-correction-20261123-01/gap_scale.py      # from the repository root

At epoch 2 (3e-4, ten draws): the gap and p* differences between widths 768 and 512, with 95% t intervals (df 9). Then,
within each of the two widths, the slope of p* on the train-validation gap between neighbouring readouts (E1 to E2,
E2 to E3) and across E1 to E3, per draw, and what a gap difference at the interval's upper limit corresponds to.
"""
import csv, hashlib, statistics as st
from pathlib import Path

POINTS = Path('reports/natural-text-fewepoch-analysis-20261103-01/POINTS.csv')
PINNED = '9a2baad33a711901098ffa365294a18eff6a6761d01293449d0b17cb576de026'
T9 = 2.2621571627409915                                  # two-sided 95% t quantile, df 9

raw = POINTS.read_bytes()
assert hashlib.sha256(raw).hexdigest() == PINNED, 'POINTS.csv differs from the published file'
rows = {(r['draw'], float(r['epoch'])): r for r in csv.DictReader(raw.decode('utf-8').splitlines())}
draws = sorted({d for d, _ in rows})
v = lambda d, e, k, w: float(rows[(d, e)][f'{k}_{w}'])


def interval(xs):
    m, h = st.mean(xs), T9 * st.stdev(xs) / len(xs) ** 0.5
    return f'{m:+.5f} [{m - h:+.5f}, {m + h:+.5f}]'


gap = [v(d, 2.0, 'gap', 768) - v(d, 2.0, 'gap', 512) for d in draws]
print(f'POINTS.csv {PINNED[:16]}..., {len(draws)} draws')
print(f'E2, 768 - 512: gap {interval(gap)} nats; p* {interval([v(d, 2.0, "p", 768) - v(d, 2.0, "p", 512) for d in draws])}; '
      f'draw gap differences {min(gap):+.5f} to {max(gap):+.5f}')
slopes = []
for w in (512, 768):
    for a, b in ((1.0, 2.0), (2.0, 3.0), (1.0, 3.0)):
        s = [(v(d, b, 'p', w) - v(d, a, 'p', w)) / (v(d, b, 'gap', w) - v(d, a, 'gap', w)) for d in draws]
        if b - a == 1.0: slopes.append(st.mean(s))
        print(f'width {w}, E{a:g} to E{b:g}: slope of p* on gap {st.mean(s):.3f} per nat (draws {min(s):.3f} to {max(s):.3f})')
upper = st.mean(gap) + T9 * st.stdev(gap) / len(gap) ** 0.5
print(f'neighbouring-readout slopes, means: {min(slopes):.3f} to {max(slopes):.3f} per nat; '
      f'a gap difference of {upper:.4f} nats (the upper limit) corresponds to {upper * min(slopes):.4f} to {upper * max(slopes):.4f} of p*')
