"""POST HOC audit script (area C). analyse() end to end on N8's own grid (24 draws, 28 readouts, a 25-readout path), on SYNTHETIC
loss arrays built from fixed formulas (256 training rows, 16 validation rows per draw; c_synth.py). No N8 data is read. The
registered tests never run analyse() on this grid: test_on_n7.py uses N7's 10 readouts and 6 draws, and test_synthetic.py calls
decide() on made-up fitted values. H1 and H2 are recomputed by the auditor with N7's sealed vendor/core.exponent, an own reading
rule and a hard-coded t quantile.
Usage: python -I -B c05_end_to_end.py <REPO>"""
import sys, math, json, copy, importlib.util
from pathlib import Path
sys.dont_write_bytecode = True
repo = Path(sys.argv[1])
sys.path.insert(0, str(repo / 'preregistration/natural-text-dense-replication-20261114/analysis'))
import numpy as np
import n8_analysis as na
sys.path.insert(0, str(Path(__file__).resolve().parent))
import c_synth
spec = importlib.util.spec_from_file_location('n7core', repo / 'preregistration/natural-text-matched-confirmation-20261104/sealed-source/vendor/core.py')
n7core = importlib.util.module_from_spec(spec); spec.loader.exec_module(n7core)

N, NV = 256, 16; EP = c_synth.EP; F, S = na.PLAN['first'], na.PLAN['second']; T23 = 2.0686576104190406
print('0. the plan against the sealed source plan, written out independently: readouts equal', list(na.READOUTS) == EP == [float(x) for x in (0.25, 0.5, 1) + tuple(2 + k / 16 for k in range(25))],
      '| path', len(na.PLAN['path']), 'readouts', na.PLAN['path'][0], '..', na.PLAN['path'][-1], '| rate tag', na.RATE_TAG == f'lr{1e-4:.0e}', '| minimum', na.PLAN['min_draws'], na.PLAN['min_completed'], '| draws', len(na.DRAWS))
PLAN = dict(na.PLAN, updates_per_epoch=N // 16)          # 16 updates per epoch at this toy size; everything else is the registered plan
data, orders = {}, {}
for k, d in enumerate(na.DRAWS): data[d], orders[d] = c_synth.make_draw(k, N, NV)
per = na.points(data)
res = na.analyse(per, data, PLAN, orders); dec = res['decision']
print('1. all 24 draws:', dec['status'], dec['labels'], dec['joint'])
print('   sections:', {k: sorted(v) for k, v in res.items() if k in ('sensitivity', 'secondary', 'carried_over')})

# the auditor's own H1 and H2
h1, h2 = [], []
for d in na.DRAWS:
    g = lambda width, e: (np.frombuffer(data[d]['arms'][(width, na.RATE_TAG)]['e0'], '<f4')[:N] - np.frombuffer(data[d]['arms'][(width, na.RATE_TAG)]['arrays'], '<f4').reshape(28, N + NV)[EP.index(e), :N]).tolist()
    rec = lambda width, e: next(x for x in data[d]['arms'][(width, na.RATE_TAG)]['record']['readouts'] if x['epoch'] == e)
    p512 = n7core.exponent(data[d]['weights'], g(512, 3.0))['p']; target = rec(512, 3.0)['train_loss']; path = [e for e in EP if e >= 2.0]
    for a, b in zip(path, path[1:]):
        x0, x1 = rec(768, a)['train_loss'], rec(768, b)['train_loss']
        if min(x0, x1) <= target <= max(x0, x1):
            p0, p1 = (n7core.exponent(data[d]['weights'], g(768, e))['p'] for e in (a, b)); t = 0.0 if x0 == x1 else (target - x0) / (x1 - x0); h1.append(p512 - (p0 + t * (p1 - p0))); break
    h2.append(p512 - n7core.exponent(data[d]['weights'], g(768, 3.0))['p'])
for name, mine in (('H1', h1), ('H2', h2)):
    m = sum(mine) / 24; sd = math.sqrt(sum((x - m) ** 2 for x in mine) / 23); half = T23 * sd / math.sqrt(24); t = dec['statistics'][name]['interval']
    print(f'   {name}: n8_analysis {t["mean"]:+.9f} [{t["interval"][0]:+.9f}, {t["interval"][1]:+.9f}] df {t["df"]}; auditor {m:+.9f} [{m - half:+.9f}, {m + half:+.9f}] from {len(mine)} draws; largest difference {max(abs(t["mean"] - m), abs(t["interval"][0] - m + half), abs(t["interval"][1] - m - half)):.2g}')
env = res['sensitivity']['envelope']; print(f'   envelope: {env["combinations"]:,} combinations, min lower {env["min_lower"]:+.7f}, max upper {env["max_upper"]:+.7f}; H1 brackets 64 updates apart: {all(abs(r["between"][1] - r["between"][0] - 0.0625) < 1e-12 for r in dec["statistics"]["H1"]["rows"].values())}')
sb = res['secondary']['S_b']; print('   S-b steps:', sorted(sb['steps']), '| S-d readouts:', len(res['secondary']['S_d']), '| S-c rows:', len(res['secondary']['S_c']['rows']), '| leave-one-out:', {h: len(v) for h, v in res['sensitivity']['leave_one_out'].items()})
json.dumps(res); print('   serialises to JSON: yes')

print('2. a failed draw given as None (n07):')
d2 = dict(data, n07=None); p2 = dict(per, n07=None); r2 = na.analyse(p2, d2, PLAN, orders)
print('  ', r2['decision']['status'], r2['decision']['labels'], r2['decision']['joint'], '| H1 unavailable', r2['decision']['statistics']['H1']['unavailable'], '| NOT_OVERFIT n', {k: v['interval']['n'] for k, v in r2['carried_over']['not_overfit'].items()})
print('3. the same draw absent from the mapping (not None):')
d3 = {k: v for k, v in data.items() if k != 'n07'}; p3 = {k: v for k, v in per.items() if k != 'n07'}
try:
    r3 = na.analyse(p3, d3, PLAN, orders); print('  ', r3['decision']['status'])
except Exception as e:
    print('   analyse() raises', type(e).__name__, e, '(decide() alone returns', na.decide(p3, PLAN)['status'] + ')')
print('4. three draws given as None although nothing says they failed (for example a run not yet made):')
p4 = dict(per, n22=None, n23=None, n24=None); r4 = na.decide(p4, PLAN); print('  ', r4['status'], r4['labels'], r4['joint'], '-> the function labels whatever it is given; what counts as failed is decided by its caller')
print('5. fewer than 20:')
p5 = dict(per, **{d: None for d in na.DRAWS[:5]}); r5 = na.analyse(p5, dict(data, **{d: None for d in na.DRAWS[:5]}), PLAN, orders); print('  ', sorted(r5), r5['decision']['status'], r5['decision']['labels'], r5['decision']['joint'])
print('6. records against arrays: the recorded training loss of 768 at the first readout of n01\'s H1 bracket moved by +0.002 (arrays unchanged):')
a = dec['statistics']['H1']['rows']['n01']; d6 = copy.deepcopy(data); k6 = EP.index(a['between'][0]); d6['n01']['arms'][S]['record']['readouts'][k6]['train_loss'] += 0.002
p6 = dict(per, n01={arm: na.arm_points(d6['n01']['weights'], x, diagnostics=False) for arm, x in d6['n01']['arms'].items()})
ra = na.records_against_arrays(p6); b = na.decide(p6, PLAN)['statistics']['H1']['rows']['n01']
print('   flagged:', ra['flagged']); print('   n01 is still', b['status'], '| weight', round(a['weight'], 6), '->', round(b['weight'], 6), '| value', a['value'], '->', b['value'], '(the reading uses the record; the flag does not gate, as the protocol says)')
print('7. NOT_OVERFIT labels:', {k: v['label'] for k, v in res['carried_over']['not_overfit'].items()}, '(validation falls from E2 to E3 by construction)')
