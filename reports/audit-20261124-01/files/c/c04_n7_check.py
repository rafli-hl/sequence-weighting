"""POST HOC audit script (area C). n8_analysis.py on N7's published data, checked against N7's sealed outputs and against the
auditor's own arithmetic (hard-coded t quantile, itertools brute force, an independent reading rule). S-b needs batch orders
(PyTorch) and is not run here. Reads the clone, the bundle and c02_per.pkl (this auditor's cache of na.points on the bundle).
Usage: python -I -B c04_n7_check.py <REPO> <BUNDLE> <SCRATCH>"""
import sys, json, csv, math, pickle, itertools, statistics, hashlib
from pathlib import Path
sys.dont_write_bytecode = True
repo, bundle, scratch = (Path(x) for x in sys.argv[1:4])
sys.path.insert(0, str(repo / 'preregistration/natural-text-dense-replication-20261114/analysis'))
import numpy as np
import n8_analysis as na

A = repo / 'reports/natural-text-matched-analysis-20261105-01'
DRAWS = ('m01', 'm02', 'm03', 'm04', 'm05', 'm06'); LOW, HIGH = 'lr1e-04', 'lr3e-04'
PATH = (2.0, 2.25, 2.5, 2.75, 3.0, 3.25, 3.5); T5 = 2.570581836
sealed_json = json.loads((A / 'ANALYSIS.json').read_bytes()); sealed = sealed_json['statistics']
num = lambda s: None if s == '' else float(s)

# ---------------------------------------------------------------- inputs
csv_per = {d: {} for d in DRAWS}
for r in csv.DictReader((A / 'POINTS.csv').open(encoding='utf-8')):
    csv_per[r['draw']].setdefault((int(r['width']), r['tag']), {})[float(r['epoch'])] = dict(p=num(r['p']), train=float(r['train']), validation=float(r['validation']), gap=float(r['gap']), saturated=False)
per = pickle.load(open(scratch / 'c02_per.pkl', 'rb'))
worst = max(abs(per[d][a][e]['p'] - csv_per[d][a][e]['p']) for d in DRAWS for a in csv_per[d] for e in csv_per[d][a])
same = sum(per[d][a][e]['p'] == csv_per[d][a][e]['p'] for d in DRAWS for a in csv_per[d] for e in csv_per[d][a])
print(f'1. refits against POINTS.csv: 240 fits, largest |p* difference| {worst:.3g}; bit-identical in {same}/240')
fits = {(r['draw'], int(r['width']), r['tag'], float(r['epoch'])): r for r in csv.DictReader((A / 'FITS.csv').open(encoding='utf-8'))}
wo = max(max(abs(per[d][a][e]['objective'] - float(fits[(d, a[0], a[1], e)]['objective'])), abs(per[d][a][e]['J0'] - float(fits[(d, a[0], a[1], e)]['J0']))) for d in DRAWS for a in per[d] for e in per[d][a])
print(f'   objective and J0 against FITS.csv: largest difference {wo:.3g}; fits at or above 7.999: {sum(per[d][a][e]["p"] >= 7.999 for d in DRAWS for a in per[d] for e in per[d][a])}; largest p* {max(per[d][a][e]["p"] for d in DRAWS for a in per[d] for e in per[d][a]):.4f}')

# ---------------------------------------------------------------- the auditor's own reading rule and interval
def my_read(rows, target):
    count = sum(min(a[1], b[1]) <= target <= max(a[1], b[1]) for a, b in zip(rows, rows[1:]))
    for (e0, x0, p0), (e1, x1, p1) in zip(rows, rows[1:]):
        if min(x0, x1) <= target <= max(x0, x1):
            if x0 == x1: return p0, e0, e0, e1, count
            t = (target - x0) / (x1 - x0); return p0 + t * (p1 - p0), e0 + t * (e1 - e0), e0, e1, count
    return None, None, None, None, count


def my_ci(v, q=T5):
    m = sum(v) / len(v); sd = math.sqrt(sum((x - m) ** 2 for x in v) / (len(v) - 1)); h = q * sd / math.sqrt(len(v)); return m, m - h, m + h


SPECS = dict(P1=('matched', 'train', LOW), S1=('matched', 'gap', LOW), S3=('fixed', None, LOW), S4=('matched', 'train', HIGH), S5=('fixed', None, HIGH), S2=('matched', 'validation', LOW))
ENV = dict(P1=0.0000764, S1=-0.0000507, S4=-0.000268)
matched_rows = list(csv.DictReader((A / 'MATCHED.csv').open(encoding='utf-8')))
for source, pp in (('POINTS.csv', csv_per), ('refits', per)):
    print(f'2. statistics from {source}: n8_analysis.contrast | auditor | ANALYSIS.json')
    for name, (kind, key, tag) in SPECS.items():
        s = na.contrast(pp, DRAWS, (512, tag), (768, tag), kind, key, 3.0, PATH, 5, None, envelope=kind == 'matched')
        mine, ends = [], []
        for d in DRAWS:
            p1 = pp[d][(512, tag)][3.0]['p']
            if kind == 'fixed': mine.append(p1 - pp[d][(768, tag)][3.0]['p']); continue
            rows = [(e, pp[d][(768, tag)][e][key], pp[d][(768, tag)][e]['p']) for e in PATH]; pr, pos, e0, e1, cnt = my_read(rows, pp[d][(512, tag)][3.0][key])
            if pr is not None: mine.append(p1 - pr); ends.append((p1 - pp[d][(768, tag)][e0]['p'], p1 - pp[d][(768, tag)][e1]['p']))
        if s['status'] == 'UNAVAILABLE':
            print(f'   {name}: UNAVAILABLE, available {s["available"]} (auditor {len(mine)} readings; ANALYSIS.json {sealed[name]["status"]}, {sealed[name]["available"]}), reasons {s["unavailable"]}'); continue
        t = s['interval']; ref = sealed[name]['interval']; m = my_ci(mine)
        d_a = max(abs(x - y) for x, y in zip((t['mean'], *t['interval']), m)); d_s = max(abs(x - y) for x, y in zip((t['mean'], *t['interval']), (ref['mean'], *ref['interval'])))
        line = f'   {name}: {t["mean"]:+.7f} [{t["interval"][0]:+.7f}, {t["interval"][1]:+.7f}] {s["status"]}; vs auditor {d_a:.2g}; vs ANALYSIS.json {d_s:.2g}; sign {s["sign_test"]["positive"]}/{s["sign_test"]["negative"]} p {s["sign_test"]["p"]:.5f} (sealed {sealed[name]["sign_test"]["p"]:.5f})'
        loo = max(abs(x - y) for d in DRAWS for x, y in zip((s['leave_one_out'][d]['mean'], *s['leave_one_out'][d]['interval']), (sealed[name]['leave_one_out'][d]['mean'], *sealed[name]['leave_one_out'][d]['interval'])))
        line += f'; leave-one-out vs sealed {loo:.2g}'
        if kind == 'matched':
            lows = [my_ci(c)[1] for c in itertools.product(*ends)]; ups = [my_ci(c)[2] for c in itertools.product(*ends)]; env = s['envelope']
            line += f'\n       envelope over {env["combinations"]} combinations: min lower {env["min_lower"]:+.8f} (auditor brute force {min(lows):+.8f}; correction of 23 Nov {ENV[name]:+.7f}), max upper {env["max_upper"]:+.8f} (auditor {max(ups):+.8f}); ends at min lower {env["at_min_lower"]["ends"]}'
        print(line)
    bad = 0; worstm = 0.0
    for r in matched_rows:
        kind, key, tag = SPECS[r['statistic']]
        s = na.contrast(pp, DRAWS, (512, tag), (768, tag), kind, key, 3.0, PATH, 5, None)['rows'][r['draw']]
        bad += s['status'] != r['status']
        for f in ('target', 'weight', 'read_at_readout', 'p_first', 'p_read', 'value'):
            a, b = num(r[f]), s.get(f)
            if (a is None) != (b is None): bad += 1
            elif a is not None: worstm = max(worstm, abs(a - b))
        b = s.get('between') or [None, None]; bad += (num(r['between_low']), num(r['between_high'])) != (b[0], b[1])
        c = num(r['intervals_holding_the_target']); bad += (None if c is None else int(c)) != s.get('intervals_holding_the_target')
    print(f'   MATCHED.csv: {len(matched_rows)} rows, {bad} mismatches of status, bracket or count, largest value difference {worstm:.3g}')

# ---------------------------------------------------------------- analyse() on N7 at 1e-4, without orders
man = json.loads((bundle / 'MANIFEST.json').read_bytes()); data = {}
for d, entry in man['draws'].items():
    data[d] = dict(weights=np.frombuffer((bundle / entry['weights']['path']).read_bytes(), dtype='<f4').tolist(),
                   arms={(int(wd), tag): dict(e0=(bundle / we['E0']['path']).read_bytes(), arrays=(bundle / arm['arrays']['path']).read_bytes(), record=json.loads((bundle / arm['record']['path']).read_bytes()))
                         for wd, we in entry['widths'].items() for tag, arm in we['arms'].items()})
plan = dict(draws=DRAWS, first=(512, LOW), second=(768, LOW), final=3.0, previous=2.0, path=PATH, min_draws=5, min_completed=5, windows=4, updates_per_epoch=1024, batch=16)
res = na.analyse(per, data, plan, None); dec = res['decision']
print('3. analyse() on N7 at 1e-4 (H1 = P1, H2 = S3), no orders')
print('   decision', dec['status'], dec['labels'], dec['joint'], '| S_b:', res['secondary']['S_b'])
for h in ('H1', 'H2'):
    t = dec['statistics'][h]['interval']; print(f'   {h}: {t["mean"]:+.5f} [{t["interval"][0]:+.5f}, {t["interval"][1]:+.5f}] df {t["df"]} t {t["t_critical"]:.9f}')
so = res['sensitivity']['starting_offset']
for k in ('contrast', 'change_in_768', 'offset'):
    t = so[k]['interval']; print(f'   starting offset, {k}: {t["mean"]:+.5f} [{t["interval"][0]:+.5f}, {t["interval"][1]:+.5f}], positive {so[k]["sign_test"]["positive"]}/6')
# the auditor's own starting offset: float64 means, the sealed estimator on gains lowered by the offset
vals = []
for d in DRAWS:
    r = dec['statistics']['H1']['rows'][d]; n = 16384
    e05 = np.frombuffer(data[d]['arms'][(512, LOW)]['e0'], '<f4')[:n]; e07 = np.frombuffer(data[d]['arms'][(768, LOW)]['e0'], '<f4')[:n]
    arr7 = np.frombuffer(data[d]['arms'][(768, LOW)]['arrays'], '<f4').reshape(10, -1)[:, :n]; eps = [float(x) for x in data[d]['arms'][(768, LOW)]['record']['layout']['block_epochs']]
    off = float(e07.astype(np.float64).mean() - e05.astype(np.float64).mean())
    ps = [na.exponent(data[d]['weights'], ((e07 - arr7[eps.index(e)]).astype(np.float64) - off).tolist())['p'] for e in r['between']]
    vals.append(r['p_first'] - (ps[0] + r['weight'] * (ps[1] - ps[0])))
m = my_ci(vals); print(f'   auditor: contrast with the offset {m[0]:+.5f} [{m[1]:+.5f}, {m[2]:+.5f}]   (AA-3 printed +0.0062 [-0.0001, +0.0126], 5/6)')
sa = res['secondary']['S_a']; t = sa['interval']
print(f'   S-a: {t["mean"]:+.8f} [{t["interval"][0]:+.8f}, {t["interval"][1]:+.8f}]; positions ' + ' '.join(f'{sa["rows"][d]["read_at_readout"]:.8f}' for d in DRAWS) + '   (13 Nov audit: +0.01583581 +0.01040960 +0.02126202; 2.09092701 2.17570429 2.13578642 2.19158563 2.07568226 2.23352733)')
summ = res['secondary']['S_c']['summary']
for k, ref in (('cumulative_rms', (0.00476198, 0.01443651, 0.01914414)), ('cumulative_max_abs', (0.00847085, 0.02297270, 0.02961557)), ('bin_max_abs', (0.02492288, 0.26589176, 0.40357918)), ('bin_rms', (0.01448940, 0.12248159, 0.18862965))):
    print(f'   S-c {k}: min/median/max {summ[k]["min"]:.8f} {summ[k]["median"]:.8f} {summ[k]["max"]:.8f}; largest difference from the 13 Nov audit {max(abs(summ[k][x] - y) for x, y in zip(("min", "median", "max"), ref)):.2g}; rows {len(res["secondary"]["S_c"]["rows"])}')
wv = wi = 0.0
for e in PATH:
    key = f'E{int(e)}' if e == int(e) else f'E{e}'; ref = sealed_json['by_readout'][key]['contrasts']['D4']; mine = res['secondary']['S_d'][e]
    wv = max(wv, max(abs(mine['values'][x] - ref['values'][x]) for x in DRAWS)); wi = max(wi, max(abs(a - b) for a, b in zip((mine['interval']['mean'], *mine['interval']['interval']), (ref['interval']['mean'], *ref['interval']['interval']))))
print(f'   S-d against ANALYSIS.json by_readout D4: values {wv:.2g}, intervals {wi:.2g}')
no = res['carried_over']['not_overfit']
print('   NOT_OVERFIT:', {k: (v['label'], sealed_json['not_overfit']['arms'][k]['label'], max(abs(a - b) for a, b in zip(v['interval']['interval'], sealed_json['not_overfit']['arms'][k]['interval']['interval']))) for k, v in no.items()})
ra = res['carried_over']['records_against_arrays']; print('   records against arrays:', ra['max_absolute_difference'], 'flagged', len(ra['flagged']), '| ANALYSIS.json', sealed_json['records_against_arrays']['max_absolute_difference'])
json.dumps(res); print('   the result of analyse() serialises to JSON: yes')
