"""Validate n8_analysis.py on N7: reproduce N7's sealed statistics, every row of MATCHED.csv, the bracket envelope, and every
published N7 figure behind N8's registered sensitivity and secondary analyses.

    python -I -B test_on_n7.py <RECORD> <BUNDLE> <ORDERS>

RECORD is a checkout of the closed record (rafli-hl/sequence-weighting, v1.2); BUNDLE is the extracted n7-loss-arrays directory
of the v1.2 release; ORDERS is the output of regenerate_n7_orders.py. All are only read. N7's statistics are computed twice:
from POINTS.csv, and from p* refitted on the loss arrays with n8_analysis.exponent. Exits 1 if any check fails.

Reference figures, besides the sealed outputs:
- starting offset: the follow-up audit of 12 November (reports/follow-up-audit-20261112-01/OUTPUT.txt, AA-3), printed to 4 decimals;
- S-a and S-c: the audit of 13 November 2026 (its printed output, 8 decimals);
- S-b: the post-hoc analysis of 11 November (reports/natural-text-matched-assistant-posthoc-20261111-01/RESULTS.json), and the
  13 November audit's recency balance (5 decimals).
"""
import ast, csv, hashlib, itertools, json, math, statistics, sys, time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import n8_analysis as na

ANALYSIS_DIR = 'reports/natural-text-matched-analysis-20261105-01'
POSTHOC = 'reports/natural-text-matched-assistant-posthoc-20261111-01/RESULTS.json'
SEALED = 'preregistration/natural-text-matched-confirmation-20261104/sealed-source'
PINS = {f'{ANALYSIS_DIR}/POINTS.csv': '234434a34cf64d98e0d45cfe029bb37935207176fd996cafe85756956c7d860f',
        f'{ANALYSIS_DIR}/MATCHED.csv': '86ea11d7210682375717d7eb67a58c74d806ad22dc57ec87ab9db4e836421e3b',
        f'{ANALYSIS_DIR}/ANALYSIS.json': 'a4af7bad78fdf9f4fe34317f73e6a1932fd0d29367b5da188b79ae73db95ce65',
        f'{ANALYSIS_DIR}/FITS.csv': 'b1cd03dec3a6e13ba2d82a6a95a48e99342ace8aaf4a0cdf1b36392fa8c7aa67'}
MANIFEST_SHA256 = '6f9c124787760b9b64e219bb55206bdc3f7f9b45774cb5eb82d4d528607b3698'
ORDERS_SHA256 = '8ba4a3c2e7906f65c6335ece7a785bfb37fe1b2904684959d388f589f2287eb1'

# N7's plan (matched_plan.py) and its fixed sequence.
DRAWS = ('m01', 'm02', 'm03', 'm04', 'm05', 'm06')
LOW, HIGH = 'lr1e-04', 'lr3e-04'
FINAL, PATH, MIN_DRAWS = 3.0, (2.0, 2.25, 2.5, 2.75, 3.0, 3.25, 3.5), 5
N7_PLAN = {tag: dict(draws=DRAWS, first=(512, tag), second=(768, tag), final=FINAL, previous=2.0, path=PATH, min_draws=MIN_DRAWS, min_completed=MIN_DRAWS,
                     windows=4, updates_per_epoch=1024, batch=16) for tag in (LOW, HIGH)}
SPECS = dict(P1=('matched', 'train', LOW, 'ABOVE'), S1=('matched', 'gap', LOW, 'ABOVE'), S3=('fixed', None, LOW, 'BELOW'),
             S4=('matched', 'train', HIGH, 'ABOVE'), S5=('fixed', None, HIGH, 'ABOVE'), S2=('matched', 'validation', LOW, 'ABOVE'))
PUBLISHED = dict(P1=(0.00909, 0.00400, 0.01417), S1=(0.00808, 0.00487, 0.01130), S3=(-0.00454, -0.00795, -0.00114),
                 S4=(0.01394, 0.00893, 0.01896), S5=(0.01382, 0.01116, 0.01648))
ENVELOPE_MIN_LOWER = dict(P1=0.0000764, S1=-0.0000507, S4=-0.000268)
MATCHED_FIELDS = ('target', 'weight', 'read_at_readout', 'p_first', 'p_read', 'value')
OFFSET = dict(contrast=((0.0062, -0.0001, 0.0126), 5), change_in_768=((0.0028, 0.0012, 0.0044), 5))      # AA-3, 4 decimals
EQUAL_IMPROVEMENT = {LOW: ((0.01583581, 0.01040960, 0.02126202), (2.09092701, 2.17570429, 2.13578642, 2.19158563, 2.07568226, 2.23352733)),
                     HIGH: ((0.01648477, 0.01349573, 0.01947381), (2.60162681, 2.71524205, 2.65710198, 2.73668887, 2.64194972, 2.83445866))}
DIAGNOSTICS = dict(cumulative_rms=(0.00476198, 0.01443651, 0.01914414), cumulative_max_abs=(0.00847085, 0.02297270, 0.02961557),
                   bin_max_abs=(0.02492288, 0.26589176, 0.40357918), bin_rms=(0.01448940, 0.12248159, 0.18862965))
RECENCY = {1: (226, 272, 14.11545, 0.00000), 2: (2018, 2116, 8.44744, 0.03709), 3: (6883, 6931, 6.99420, 0.03659)}
POSTHOC_KEYS = ('whole', 'last', 'every', 'loss_last', 'loss_every', 'whole_minus_every', 'last_minus_every')

results = []


def check(name, ok, detail=''):
    results.append(bool(ok)); print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f'  [{detail}]' if detail else ''))


def sha(b): return hashlib.sha256(b).hexdigest()


def number(s): return None if s == '' else float(s)


def three(t): return (t['mean'], *t['interval'])


def diff3(a, b): return max(abs(x - y) for x, y in zip(a, b))


def stats_for(per):
    return {name: na.contrast(per, DRAWS, (512, tag), (768, tag), kind, key, FINAL, PATH, MIN_DRAWS, expected, envelope=kind == 'matched')
            for name, (kind, key, tag, expected) in SPECS.items()}


def points_from_csv(path):
    per = {d: {} for d in DRAWS}
    for r in csv.DictReader(path.open(encoding='utf-8')):
        per[r['draw']].setdefault((int(r['width']), r['tag']), {})[float(r['epoch'])] = dict(p=number(r['p']), train=float(r['train']), validation=float(r['validation']), gap=float(r['gap']), saturated=False)
    return per


def load_bundle(bundle):
    raw = (bundle / 'MANIFEST.json').read_bytes(); check('bundle MANIFEST.json SHA-256', sha(raw) == MANIFEST_SHA256, sha(raw)[:16])
    man = json.loads(raw); files = bad = 0; data = {}
    for d, entry in man['draws'].items():
        refs = [entry['weights']] + [x for wd in entry['widths'].values() for x in [wd['E0']] + [y for arm in wd['arms'].values() for y in (arm['arrays'], arm['record'])]]
        for ref in refs:
            b = (bundle / ref['path']).read_bytes(); files += 1; bad += len(b) != ref['bytes'] or sha(b) != ref['sha256']
        wb = (bundle / entry['weights']['path']).read_bytes(); h = hashlib.sha256(); h.update(str(((len(wb) // 4,), 'torch.float32')).encode()); h.update(wb)
        bad += h.hexdigest() != entry['weights']['bound_tensor_hash']
        data[d] = dict(weights=np.frombuffer(wb, dtype='<f4').tolist(),
                       arms={(int(wd), tag): dict(e0=(bundle / we['E0']['path']).read_bytes(), arrays=(bundle / arm['arrays']['path']).read_bytes(), record=json.loads((bundle / arm['record']['path']).read_bytes()))
                             for wd, we in entry['widths'].items() for tag, arm in we['arms'].items()})
    check("bundle files against MANIFEST.json, weights against the runs' tensor hashes", bad == 0 and files == 66, f'{files} files, 6 weight hashes, {bad} mismatches')
    return data


def load_orders(path):
    raw = (path / 'ORDERS.json').read_bytes(); meta = json.loads(raw); bad = 0; out = {}
    for key, x in meta['orders'].items():
        b = (path / x['file']).read_bytes(); o = np.frombuffer(b, dtype='<i8').reshape(meta['epochs'], meta['n'])
        bad += sha(b) != x['sha256'] or [na.order_sha256(row) for row in o] != x['epoch_order_sha256'] or any(sorted(row.tolist()) != list(range(meta['n'])) for row in o)
        out[key] = o
    check(f"regenerated orders (PyTorch {meta['torch']}): ORDERS.json pinned, files, per-epoch order_sha256, each row a permutation", sha(raw) == ORDERS_SHA256 and bad == 0 and len(out) == 12, f'{sha(raw)[:16]}, {bad} mismatches')
    return out


def compare_points(per, ref, fits):
    worst = dict(p=0.0, train=0.0, validation=0.0, gap=0.0); n = 0; obj = 0.0
    for d in DRAWS:
        for arm, eps in ref[d].items():
            for e, r in eps.items():
                x = per[d][arm][e]; n += 1; f = fits[(d, arm[0], arm[1], e)]
                for k in worst: worst[k] = max(worst[k], abs(x[k] - r[k]))
                obj = max(obj, abs(x['objective'] - f['objective']), abs(x['J0'] - f['J0']))
    check('240 refits of p* against POINTS.csv (1e-9)', n == 240 and worst['p'] <= 1e-9, f"{n} fits; largest |p* difference| {worst['p']:.3g}")
    check('record losses and gaps against POINTS.csv (exact)', worst['train'] == worst['validation'] == worst['gap'] == 0.0, ', '.join(f'{k} {worst[k]:.3g}' for k in ('train', 'validation', 'gap')))
    check('objective at p* and at p = 0 against FITS.csv (1e-9)', obj <= 1e-9, f'largest difference {obj:.3g}')


def compare_stats(source, stats, sealed, matched):
    print(f'--- statistics from {source}')
    for name, pub in PUBLISHED.items():
        t = stats[name]['interval']; ref = sealed[name]['interval']; d_pub = diff3(three(t), pub); d_seal = diff3(three(t), three(ref))
        check(f'{name} {t["mean"]:+.5f} [{t["interval"][0]:+.5f}, {t["interval"][1]:+.5f}], n = {t["n"]}, side {stats[name]["status"]}',
              d_pub <= 1e-5 and d_seal <= 1e-6 and t['n'] == ref['n'] and stats[name]['status'] == sealed[name]['status'], f'vs brief {d_pub:.2g}, vs ANALYSIS.json {d_seal:.2g}')
        s, rs = stats[name]['sign_test'], sealed[name]['sign_test']; lo1, lo2 = stats[name]['leave_one_out'], sealed[name]['leave_one_out']
        loo = max(diff3((lo1[d]['mean'], *lo1[d]['interval']), (lo2[d]['mean'], *lo2[d]['interval'])) for d in lo1)
        check(f'{name} sign test {s["positive"]}/{s["negative"]} p = {s["p"]:.5f}, t-test p, leave-one-out',
              (s['positive'], s['negative']) == (rs['positive'], rs['negative']) and abs(s['p'] - rs['p']) <= 1e-12 and abs(t['p'] - ref['p']) <= 1e-6 and loo <= 1e-6,
              f't-test p {t["p"]:.6f} vs {ref["p"]:.6f}; leave-one-out largest difference {loo:.2g}')
    s2 = stats['S2']
    check('S2 UNAVAILABLE; available m02, m03, m06; m01, m04, m05 TARGET_OUTSIDE_PATH',
          s2['status'] == 'UNAVAILABLE' and s2['available'] == ['m02', 'm03', 'm06'] and s2['unavailable'] == {d: 'TARGET_OUTSIDE_PATH' for d in ('m01', 'm04', 'm05')}, f"status {s2['status']}, available {s2['available']}")
    worst, bad, rows = 0.0, [], 0
    for r in matched:
        mine = stats[r['statistic']]['rows'][r['draw']]; rows += 1; between = mine.get('between') or [None, None]
        pairs = [(number(r[f]), mine.get(f)) for f in MATCHED_FIELDS] + [(number(r['between_low']), between[0]), (number(r['between_high']), between[1])]
        for a, b in pairs:
            if (a is None) != (b is None): bad.append(r['statistic'] + r['draw'])
            elif a is not None: worst = max(worst, abs(a - b))
        count = number(r['intervals_holding_the_target']); mc = mine.get('intervals_holding_the_target')
        if r['status'] != mine['status'] or (count is None) != (mc is None) or (count is not None and int(count) != mc): bad.append(r['statistic'] + r['draw'])
    check('every row of MATCHED.csv: status, bracket, weight, read position, interval count, values (1e-9)', rows == 36 and not bad and worst <= 1e-9,
          f'{rows} rows, largest difference {worst:.3g}' + (f', mismatches {bad}' if bad else ''))
    for name, want in ENVELOPE_MIN_LOWER.items():
        env = stats[name]['envelope']; rows_ = stats[name]['rows']
        ends = [[rows_[d]['p_first'] - rows_[d]['p_at_bracket'][0], rows_[d]['p_first'] - rows_[d]['p_at_bracket'][1]] for d in stats[name]['available']]
        q = na.t_quantile(0.975, len(ends) - 1); brute_low, brute_up = math.inf, -math.inf
        for c in itertools.product(*ends):
            m = math.fsum(c) / len(c); h = q * statistics.stdev(c) / math.sqrt(len(c)); brute_low = min(brute_low, m - h); brute_up = max(brute_up, m + h)
        check(f"{name} envelope over {env['combinations']} combinations: min lower {env['min_lower']:+.7f}, max upper {env['max_upper']:+.7f}",
              abs(env['min_lower'] - want) <= 1e-6 and abs(env['min_lower'] - brute_low) <= 1e-12 and abs(env['max_upper'] - brute_up) <= 1e-12,
              f'vs brief {abs(env["min_lower"] - want):.2g}; vs itertools brute force {abs(env["min_lower"] - brute_low):.2g} / {abs(env["max_upper"] - brute_up):.2g}')


def epoch_key(e): return f'E{int(e)}' if e == int(e) else f'E{e}'


def compare_analysis(res, per, data, orders, sealed_json, posthoc):
    sealed = sealed_json['statistics']; dec = res['decision']; h1, h2 = dec['statistics']['H1'], dec['statistics']['H2']
    print('--- the N8 analysis run on N7 at 1e-4 (H1 = P1, H2 = S3)')
    print(f"INFO  environment {res['environment']['system']} Python {res['environment']['python']} NumPy {res['environment']['numpy']}; matches the registered one: {res['environment']['matches_registered']}")
    ok = diff3(three(h1['interval']), three(sealed['P1']['interval'])) <= 1e-6 and diff3(three(h2['interval']), three(sealed['S3']['interval'])) <= 1e-6
    check(f"decision {dec['status']}: H1 {dec['labels']['H1']}, H2 {dec['labels']['H2']}, {dec['joint']}; intervals equal P1 and S3",
          ok and dec['status'] == 'COMPLETE' and dec['labels'] == dict(H1='CONFIRMED', H2='CONFIRMED') and dec['joint'] == 'REVERSAL_REPLICATED' and 'saturation' not in h1 and 'saturation' not in h2)
    loo = max(diff3((s['leave_one_out'][d]['mean'], *s['leave_one_out'][d]['interval']), (sealed[k]['leave_one_out'][d]['mean'], *sealed[k]['leave_one_out'][d]['interval'])) for s, k in ((h1, 'P1'), (h2, 'S3')) for d in DRAWS)
    check('leave-one-draw-out for H1 and H2 against ANALYSIS.json (1e-6)', loo <= 1e-6, f'largest difference {loo:.2g}')
    env = res['sensitivity']['envelope']; check('H1 envelope equals P1\'s', abs(env['min_lower'] - 0.0000764) <= 1e-6, f"min lower {env['min_lower']:+.7f}")
    so = res['sensitivity']['starting_offset']
    for key, (want, pos) in OFFSET.items():
        t = so[key]['interval']; d = diff3(three(t), want)
        check(f"starting offset, {key.replace('_', ' ')}: {t['mean']:+.4f} [{t['interval'][0]:+.4f}, {t['interval'][1]:+.4f}], {so[key]['sign_test']['positive']}/6 (AA-3, 4 decimals: 6e-5)",
              d <= 6e-5 and so[key]['sign_test']['positive'] == pos, f'largest difference {d:.2g}')
    off = so['offset']['interval']; print(f"INFO  mean E0 offset, 768 minus 512: {off['mean']:+.5f} [{off['interval'][0]:+.5f}, {off['interval'][1]:+.5f}]")
    for tag in (LOW, HIGH):
        sa = res['secondary']['S_a'] if tag == LOW else na.equal_improvement(per, N7_PLAN[HIGH]); (want, pos) = EQUAL_IMPROVEMENT[tag]
        t = sa['interval']; d = diff3(three(t), want); dp = max(abs(sa['rows'][x]['read_at_readout'] - y) for x, y in zip(DRAWS, pos))
        check(f"S-a at {tag[2:]}: {t['mean']:+.8f} [{t['interval'][0]:+.8f}, {t['interval'][1]:+.8f}], n = {t['n']} (13 Nov audit, 1e-8)", d <= 1e-8 and dp <= 1e-8 and t['n'] == 6,
              f'largest difference {d:.2g}; read positions {dp:.2g}')
    sb = res['secondary']['S_b']; oc = sb['order_checks']
    check('S-b orders against the losses: every step, trained window minus the others, below -0.05 nats', all(x['max'] < -0.05 for x in oc.values()),
          f"{sum(x['steps'] for x in oc.values())} draw-steps x 2 widths; mean {np.mean([x['mean'] for x in oc.values()]):+.4f}, largest {max(x['max'] for x in oc.values()):+.4f}")
    ctrl = [na.order_check(data[d], orders[f'{d}-seed-plus-1'], N7_PLAN[LOW]) for d in DRAWS]
    check('S-b negative control (seed + 1): every step within 0.02 nats of 0', all(max(abs(x['min']), abs(x['max'])) < 0.02 for x in ctrl), f"largest |gap| {max(max(abs(x['min']), abs(x['max'])) for x in ctrl):.4f}")
    for k in (1, 2, 3):
        step = sb['steps'][2 + k / 4]; worst = 0.0; missing = []
        for key in POSTHOC_KEYS:
            ref = posthoc[f'matched|{LOW}|k{k}|{key}']; mine = step['contrasts'][key]['values']
            if sorted(mine) != list(DRAWS): missing.append(key); continue
            worst = max(worst, max(abs(mine[d] - r) for d, r in zip(DRAWS, ref)))
        b = step['balance']['every']; size_min, size_max, age, tv = RECENCY[k]
        check(f"S-b, 768 at E{2 + k / 4}: whole, last, every, losses against the 11 Nov RESULTS.json (1e-6); every-pass balance: sizes {b['size_min']}-{b['size_max']}, "
              f"mean age difference {b['max_abs_mean_age_difference']:.5f}, joint cell distance {b['max_joint_cell_distance']:.5f} (13 Nov audit)",
              not missing and worst <= 1e-6 and (b['size_min'], b['size_max']) == (size_min, size_max) and abs(b['max_abs_mean_age_difference'] - age) <= 5e-6 and abs(b['max_joint_cell_distance'] - tv) <= 5e-6,
              f'largest value difference {worst:.2g}' + (f'; missing {missing}' if missing else ''))
    summ = res['secondary']['S_c']['summary']; d = max(diff3((summ[k]['min'], summ[k]['median'], summ[k]['max']), v) for k, v in DIAGNOSTICS.items())
    check(f"S-c over {len(res['secondary']['S_c']['rows'])} fits: min, median and max of four diagnostics against the 13 Nov audit (1e-8)", d <= 1e-8 and len(res['secondary']['S_c']['rows']) == 240, f'largest difference {d:.2g}')
    print('INFO  S-c objective ratio min/median/max ' + ' / '.join(f"{summ['objective_ratio'][x]:.6f}" for x in ('min', 'median', 'max')))
    worst_v = worst_i = 0.0
    for e in PATH:
        ref = sealed_json['by_readout'][epoch_key(e)]['contrasts']['D4']; mine = res['secondary']['S_d'][e]
        worst_v = max(worst_v, max(abs(mine['values'][x] - ref['values'][x]) for x in DRAWS)); worst_i = max(worst_i, diff3(three(mine['interval']), three(ref['interval'])))
    check('S-d at the 7 path readouts against ANALYSIS.json by_readout D4: values (1e-9, protocol section 6), intervals (1e-6)', worst_v <= 1e-9 and worst_i <= 1e-6, f'{worst_v:.2g}, {worst_i:.2g}')
    no = res['carried_over']['not_overfit']; d = max(diff3(three(no[k]['interval']), three(sealed_json['not_overfit']['arms'][k]['interval'])) for k in no)
    check(f"NOT_OVERFIT {', '.join(f'{k} {v['label']}' for k, v in no.items())} against ANALYSIS.json (1e-6)",
          d <= 1e-6 and all(no[k]['label'] == sealed_json['not_overfit']['arms'][k]['label'] for k in no), f'largest difference {d:.2g}')
    ra = res['carried_over']['records_against_arrays']
    check(f"records against arrays: largest difference {ra['max_absolute_difference']:.3g}, none flagged (ANALYSIS.json: exact)",
          ra['max_absolute_difference'] == sealed_json['records_against_arrays']['max_absolute_difference'] and not ra['flagged'])


def main(record, bundle, orders_dir):
    print(f'numpy {np.__version__}, python {sys.version.split()[0]}')
    for rel, want in PINS.items():
        got = sha((record / rel).read_bytes()); check(f'{rel} SHA-256', got == want, got[:16])
    posthoc_raw = (record / POSTHOC).read_bytes(); print(f'INFO  {POSTHOC} SHA-256 {sha(posthoc_raw)}')
    mine_src = Path(na.__file__).read_text(encoding='utf-8'); seg = lambda src, name: next(ast.get_source_segment(src, f) for f in ast.parse(src).body if isinstance(f, ast.FunctionDef) and f.name == name)
    for rel, name in (('vendor/core.py', 'exponent'), ('text_analysis.py', 'exponent_upper'), ('text_analysis.py', 'objective_at')):
        src = (record / SEALED / rel).read_text(encoding='utf-8')
        check(f'n8_analysis.{name} is a verbatim copy of the sealed {rel}', seg(src, name) == seg(mine_src, name), f'{rel} {sha((record / SEALED / rel).read_bytes())[:16]}')
    sealed_json = json.loads((record / ANALYSIS_DIR / 'ANALYSIS.json').read_bytes()); sealed = sealed_json['statistics']
    matched = list(csv.DictReader((record / ANALYSIS_DIR / 'MATCHED.csv').open(encoding='utf-8')))
    fits = {(r['draw'], int(r['width']), r['tag'], float(r['epoch'])): dict(objective=float(r['objective']), J0=float(r['J0'])) for r in csv.DictReader((record / ANALYSIS_DIR / 'FITS.csv').open(encoding='utf-8'))}
    check('t quantile, df 5, against the sealed T95 table (2.570581836)', abs(na.t_quantile(0.975, 5) - 2.570581836) <= 5e-10, f'{na.t_quantile(0.975, 5)!r}')
    csv_points = points_from_csv(record / ANALYSIS_DIR / 'POINTS.csv')
    compare_stats('POINTS.csv', stats_for(csv_points), sealed, matched)
    print('--- p* refitted from the loss arrays (about 0.7 s per fit)')
    data = load_bundle(bundle); t0 = time.perf_counter()
    per = na.points(data, DRAWS, progress=lambda d: print(f'      fitted {d}: 40 fits, {time.perf_counter() - t0:.0f} s elapsed'))
    compare_points(per, csv_points, {(d, w, t, e): v for (d, w, t, e), v in fits.items()})
    compare_stats('the refitted loss arrays', stats_for(per), sealed, matched)
    orders = load_orders(orders_dir); t0 = time.perf_counter()
    res = na.analyse(per, data, N7_PLAN[LOW], {d: orders[d] for d in DRAWS}); print(f'      analyse(): {time.perf_counter() - t0:.0f} s')
    compare_analysis(res, per, data, orders, sealed_json, json.loads(posthoc_raw)['values'])
    print(f'{sum(results)} passed, {len(results) - sum(results)} failed')
    return 0 if all(results) else 1


if __name__ == '__main__':
    if len(sys.argv) != 4: raise SystemExit(__doc__)
    raise SystemExit(main(Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])))
