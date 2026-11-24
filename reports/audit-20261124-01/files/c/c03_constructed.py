"""POST HOC audit script (area C). Constructed inputs for n8_analysis.py, rule by rule (protocol sections 5 and 6).
No N8 data is read: every value below comes from a fixed formula. Usage: python -I -B c03_constructed.py <REPO>"""
import sys, math, json, itertools, statistics
from pathlib import Path
sys.dont_write_bytecode = True
repo = Path(sys.argv[1])
sys.path.insert(0, str(repo / 'preregistration/natural-text-dense-replication-20261114/analysis'))
import numpy as np
import n8_analysis as na

FIRST, SECOND, FINAL = na.PLAN['first'], na.PLAN['second'], na.PLAN['final']
T23 = 2.0686576104190406          # t(0.975, 23); standard tables give 2.068658


def show(name, got, want=None):
    print(f'{name}: {got}' + ('' if want is None else f'   | protocol wording expects: {want}'))


def study(h1, h2, r=None):
    """24 draws on N8's grid. 768's training loss falls and its p* rises linearly along the path; 512's E3 target is met at readout r[k]."""
    per = {}
    for k, d in enumerate(na.DRAWS):
        rk = 2.3 + 0.01 * k if r is None else r[k]
        a768 = {e: dict(p=0.09 + 0.01 * (e - 2), train=4.4 - 0.25 * (e - 2), validation=4.7, gap=0.3, saturated=False) for e in na.READOUTS}
        p512 = 0.09 + 0.01 * (rk - 2) + h1[k]
        a768[FINAL]['p'] = p512 - h2[k]
        a512 = {e: dict(p=p512 if e == FINAL else 0.05, train=(4.4 - 0.25 * (rk - 2)) if e == FINAL else 5.0, validation=4.7, gap=0.3, saturated=False) for e in na.READOUTS}
        per[d] = {FIRST: a512, SECOND: a768}
    return per


print('=== 1. t quantile, df 19-23, against numerical integration of the t density (independent of the incomplete beta)')


def t_cdf_central(t, nu, steps=200000):
    c = math.exp(math.lgamma((nu + 1) / 2) - math.lgamma(nu / 2)) / math.sqrt(nu * math.pi); h = t / steps
    f = lambda x: c * (1 + x * x / nu) ** (-(nu + 1) / 2)
    s = f(0) + f(t) + 4 * sum(f((2 * i - 1) * h) for i in range(1, steps // 2 + 1)) + 2 * sum(f(2 * i * h) for i in range(1, steps // 2))
    return 2 * s * h / 3          # P(|T| <= t), Simpson


for df in range(19, 24):
    q = na.t_quantile(0.975, df); print(f'  df {df}: quantile {q:.12f}; P(|T| <= q) by Simpson = {t_cdf_central(q, df):.13f} (want 0.95)')

print('=== 2. "entirely" = beyond 0 by more than 1e-9 (H1 above, H2 below)')
a = 0.001; half = T23 * a / math.sqrt(23)          # alternating +-a: sd = a sqrt(24/23), half-width = t a / sqrt(23)
for margin in (5e-10, 2e-9):
    h1 = [half + margin + a * (-1) ** k for k in range(24)]; h2 = [-(half + margin) + a * (-1) ** k for k in range(24)]
    out = na.decide(study(h1, h2)); i1 = out['statistics']['H1']['interval']['interval']; i2 = out['statistics']['H2']['interval']['interval']
    print(f'  margin {margin:g}: H1 lower limit {i1[0]:.3e} -> {out["labels"]["H1"]}; H2 upper limit {i2[1]:.3e} -> {out["labels"]["H2"]}; joint {out["joint"]}')

print('=== 3. reading rule')
r = na.read_along([(2.0, 4.30, 0.10), (2.0625, 4.25, 0.11), (2.125, 4.25, None), (2.1875, 4.20, 0.13)], 4.25)
show('  target equal to a readout value, held first by a sloping interval', {k: r.get(k) for k in ('status', 'between', 'weight', 'p_read', 'intervals_holding_the_target')})
r = na.read_along([(2.0, 4.25, 0.10), (2.0625, 4.25, None), (2.125, 4.20, 0.12)], 4.25)
show('  flat first interval holding the target, its LATER fit undefined', {k: r.get(k) for k in ('status', 'between', 'weight', 'p_at_bracket')}, 'read at its earlier readout (p = 0.10)')
r = na.read_along([(2.0, 4.30, 0.10), (2.0625, 4.20, 0.11), (2.125, 4.28, 0.12), (2.1875, 4.10, 0.13)], 4.25)
show('  non-monotone path', {k: r.get(k) for k in ('status', 'between', 'weight', 'p_read', 'intervals_holding_the_target')})
print('  target above / below every readout:', [na.read_along([(2.0, 4.30, 0.10), (2.0625, 4.20, 0.11)], t)['status'] for t in (4.3000001, 4.1999999)])

print('=== 4. saturation on the matched contrast (H1) and on 512 at E3 (no registered test exercises these branches)')
h1 = [0.004 + 0.001 * math.sin(k) for k in range(24)]; h2 = [-0.004 + 0.001 * math.cos(k) for k in range(24)]
per = study(h1, h2); base = na.decide(per)
row = base['statistics']['H1']['rows']['n01']; lo, hi = row['between']; w = row['weight']
per['n01'][SECOND][lo] = dict(per['n01'][SECOND][lo], p=8.0, p32=9.5, saturated=False)              # resolved at bound 32
row2 = base['statistics']['H1']['rows']['n02']
per['n02'][SECOND][row2['between'][1]] = dict(per['n02'][SECOND][row2['between'][1]], p=8.0, p32=32.0, saturated=True)   # unresolved
per['n03'][FIRST][FINAL] = dict(per['n03'][FIRST][FINAL], p=8.0, p32=None, saturated=True)             # 512 at E3 unresolved
out = na.decide(per); s1, s2 = out['statistics']['H1'], out['statistics']['H2']
p512 = per['n01'][FIRST][FINAL]['p']; p_hi = per['n01'][SECOND][hi]['p']
print('  H1 unavailable:', s1['unavailable'], '| H2 unavailable:', s2['unavailable'])
print('  H1 n01 bound-8 value (label uses it):', s1['values']['n01'], '= p512 - (8 + w (p_hi - 8)) =', p512 - (8.0 + w * (p_hi - 8.0)))
print('  H1 n01 value at bound 32:', s1['saturation']['values_at_bound_32']['n01'], '= p512 - (9.5 + w (p_hi - 9.5)) =', p512 - (9.5 + w * (p_hi - 9.5)))
print('  H1 saturation flagged / saturated:', s1['saturation']['flagged'], s1['saturation']['saturated'], '| interval at bound 32 present:', 'interval_at_bound_32' in s1['saturation'])
print('  H2 saturation flagged / saturated:', s2['saturation']['flagged'], s2['saturation']['saturated'])
print('  labels:', out['labels'], out['joint'], '| available H1', len(s1['available']), 'H2', len(s2['available']))

print('=== 5. what an UNAVAILABLE hypothesis still emits (19 of 24 available)')
per = study(h1, h2)
for d in na.DRAWS[:5]: per[d][FIRST][FINAL]['train'] = 3.0          # target below the whole path
out = na.decide(per); s1 = out['statistics']['H1']
print('  label', out['labels']['H1'], '| joint', out['joint'], '| keys:', sorted(k for k in s1 if k != 'rows'))
print('  has interval:', 'interval' in s1, '| has envelope:', 'envelope' in s1, '| per-draw values:', len(s1['values']), '| sign test:', s1['sign_test'], '| leave-one-out intervals:', len(s1.get('leave_one_out', {})))
x = next(iter(s1['leave_one_out'].values())); print('  one leave-one-out entry:', {k: x[k] for k in ('mean', 'interval', 'df', 'side')})

print('=== 6. study status')
for missing in (0, 1, 4, 5):
    per = study(h1, h2)
    for d in na.DRAWS[:missing]: per[d] = None
    out = na.decide(per); print(f'  {24 - missing} completed: status {out["status"]}, labels {out["labels"]}, joint {out["joint"]}, statistics present: {"statistics" in out}')
per = study(h1, h2); del per['n24']; out = na.decide(per); print('  a draw absent from the mapping (not None): decide ->', out['status'], out['statistics']['H1']['unavailable'])
