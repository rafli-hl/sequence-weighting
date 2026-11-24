"""POST HOC audit script (area C). Which rules of n8_analysis.py does no registered test exercise?

Part A. One-line mutants of n8_analysis.py are written to the SCRATCH folder (the clone is not touched), each beside a byte copy of
the registered test_synthetic.py, and the test's own functions are called on the mutant: t_quantiles, reading_rule,
availability_and_decision, saturation, tests_and_intervals. Its sixth function, envelope(), is not called here, to avoid repeating
the 2^24 enumerations; no mutant below touches bracket_envelope or t_quantile. A mutant "survives" when all 30 checks still pass.
Three control mutants, which the tests should kill, show that the harness detects a broken rule.

Part B. For test_on_n7.py, which cannot run here (no PyTorch): the conditions under which the surviving mutants change anything
are evaluated on N7's published data with the UNMUTATED module. If none arises, test_on_n7.py cannot tell the mutant from the
original either, because the mutated branch is never entered on N7.

Usage: python -I -B c06_mutants.py <REPO> <BUNDLE> <SCRATCH>            (child mode: ... --child <mutant dir>)"""
import sys, json, pickle, shutil, subprocess, importlib.util
from pathlib import Path
sys.dont_write_bytecode = True

if '--child' in sys.argv:
    folder = Path(sys.argv[sys.argv.index('--child') + 1]); sys.path.insert(0, str(folder))
    spec = importlib.util.spec_from_file_location('ts', folder / 'test_synthetic.py'); ts = importlib.util.module_from_spec(spec)
    import io, contextlib
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            spec.loader.exec_module(ts)
            ts.t_quantiles(); ts.reading_rule(); ts.availability_and_decision(); ts.saturation(); ts.tests_and_intervals()
        failed = [line[6:90] for line in buf.getvalue().splitlines() if line.startswith('FAIL')]
        print(json.dumps(dict(passed=sum(ts.results), failed=len(ts.results) - sum(ts.results), names=failed)))
    except Exception as e:
        print(json.dumps(dict(error=f'{type(e).__name__}: {e}')))
    raise SystemExit(0)

repo, bundle, scratch = (Path(x) for x in sys.argv[1:4])
AN = repo / 'preregistration/natural-text-dense-replication-20261114/analysis'
src = (AN / 'n8_analysis.py').read_text(encoding='utf-8')
MUTANTS = [
    ('M0 unmutated copy', None, None),
    ('M1 the 1e-9 margin dropped from side()', "    if t['interval'][0] > EPS: return 'ABOVE'\n    if t['interval'][1] < -EPS: return 'BELOW'", "    if t['interval'][0] > 0.0: return 'ABOVE'\n    if t['interval'][1] < 0.0: return 'BELOW'"),
    ('M2 H1 value at bound 32 ignores the interpolation weight', "(r['weight'] if kind == 'matched' else 0.0)", "0.0"),
    ('M3 a saturated fit makes a draw unavailable for H2 only, not for H1', "for a, e in fits_used(r, first, second, kind, final)): r = dict(r, status='SATURATED')", "for a, e in fits_used(r, first, second, kind, final) if kind == 'fixed'): r = dict(r, status='SATURATED')"),
    ('M4 records flagged above 1e-2 instead of 1e-3', 'RECORD_LIMIT = 1e-3 ', 'RECORD_LIMIT = 1e-2 '),
    ('M5 NOT_OVERFIT: the labels OVERFIT and PLATEAU swapped', "'OVERFIT' if t['interval'][0] > EPS else 'PLATEAU'", "'PLATEAU' if t['interval'][0] > EPS else 'OVERFIT'"),
    ('M6 S-d keeps saturated fits', "per[d][a][e]['p'] is not None and not per[d][a][e].get('saturated', False) for a in", "per[d][a][e]['p'] is not None for a in"),
    ('M7 starting offset: an undefined refit is not set aside', 'if None in ps: rows[d]', 'if False: rows[d]'),
    ('M8 refit threshold 7.5 instead of 7.999', 'P_UPPER, S32_UPPER = 7.999, 32.0', 'P_UPPER, S32_UPPER = 7.5, 32.0'),
    ('K1 control: unavailable at exactly the minimum', "if len(available) < max(min_draws, 2): return dict(out, status='UNAVAILABLE')", "if len(available) <= max(min_draws, 2): return dict(out, status='UNAVAILABLE')"),
    ('K2 control: the last bracketing interval is read', '(e0, x0, p0), (e1, x1, p1) = hits[0]', '(e0, x0, p0), (e1, x1, p1) = hits[-1]'),
    ('K3 control: a flat interval is read at its later readout', 'w = 0.0 if x1 == x0 else', 'w = 1.0 if x1 == x0 else'),
]
print('PART A. test_synthetic.py (its first five functions, 30 checks) on mutants of n8_analysis.py')
root = scratch / 'mutants'
if root.exists(): shutil.rmtree(root)
for name, old, new in MUTANTS:
    folder = root / name.split()[0]; folder.mkdir(parents=True)
    if old is None: text = src
    else:
        if src.count(old) != 1: raise SystemExit(f'{name}: pattern found {src.count(old)} times')
        text = src.replace(old, new)
    (folder / 'n8_analysis.py').write_text(text, encoding='utf-8', newline='\n'); shutil.copyfile(AN / 'test_synthetic.py', folder / 'test_synthetic.py')
    out = subprocess.run([sys.executable, '-I', '-B', __file__, str(repo), str(bundle), str(scratch), '--child', str(folder)], capture_output=True, text=True)
    r = json.loads(out.stdout.strip().splitlines()[-1]) if out.stdout.strip() else dict(error=out.stderr[-300:])
    verdict = 'KILLED (the test aborts: ' + r['error'] + ')' if 'error' in r else ('SURVIVES' if r['failed'] == 0 else 'KILLED') + f" ({r['passed']} passed, {r['failed']} failed" + (': ' + '; '.join(r['names']) if r['failed'] else '') + ')'
    print(f'  {name}: {verdict}')

print('PART B. on N7 with the unmutated module: do the mutated branches ever arise? (test_on_n7.py reads only N7)')
sys.path.insert(0, str(AN))
import numpy as np
import n8_analysis as na
per = pickle.load(open(scratch / 'c02_per.pkl', 'rb')); DRAWS = tuple(sorted(per)); LOW, HIGH = 'lr1e-04', 'lr3e-04'; PATH = (2.0, 2.25, 2.5, 2.75, 3.0, 3.25, 3.5)
man = json.loads((bundle / 'MANIFEST.json').read_bytes()); data = {}
for d, entry in man['draws'].items():
    data[d] = dict(weights=np.frombuffer((bundle / entry['weights']['path']).read_bytes(), dtype='<f4').tolist(),
                   arms={(int(wd), tag): dict(e0=(bundle / we['E0']['path']).read_bytes(), arrays=(bundle / arm['arrays']['path']).read_bytes(), record=json.loads((bundle / arm['record']['path']).read_bytes()))
                         for wd, we in entry['widths'].items() for tag, arm in we['arms'].items()})
fits = [x for d in DRAWS for a in per[d] for x in per[d][a].values()]
print(f'  fits: {len(fits)}; undefined: {sum(x["p"] is None for x in fits)}; largest p*: {max(x["p"] for x in fits):.4f} (M2, M3, M6, M8 need a fit of at least 7.5); saturated: {sum(x["saturated"] for x in fits)}')
limits = []
for tag in (LOW, HIGH):
    plan = dict(draws=DRAWS, first=(512, tag), second=(768, tag), final=3.0, previous=2.0, path=PATH, min_draws=5, min_completed=5, windows=4, updates_per_epoch=1024, batch=16)
    res = na.analyse(per, data, plan, None)
    for s in list(res['decision']['statistics'].values()) + [res['secondary']['S_a']]:
        limits += s['interval']['interval'] + [x for v in s['leave_one_out'].values() for x in v['interval']]
    limits += [x for v in res['carried_over']['not_overfit'].values() for x in v['interval']['interval']]
    so = res['sensitivity']['starting_offset']
    print(f'  {tag}: NOT_OVERFIT labels {sorted(set(v["label"] for v in res["carried_over"]["not_overfit"].values()))} (M5 needs another label); records against arrays, largest difference {res["carried_over"]["records_against_arrays"]["max_absolute_difference"]:.3g} (M4 needs one between 1e-3 and 1e-2); '
          f'starting-offset rows {sorted(set(r["status"] for r in so["rows"].values()))} (M7 needs UNDEFINED_FIT); H2 has an envelope: {"envelope" in res["decision"]["statistics"]["H2"]} (test_on_n7.py never looks for one)')
for kind, key, tag in (('matched', 'gap', LOW), ('matched', 'validation', LOW)):
    s = na.contrast(per, DRAWS, (512, tag), (768, tag), kind, key, 3.0, PATH, 5, None, envelope=True)
    if 'interval' in s: limits += s['interval']['interval'] + [x for v in s['leave_one_out'].values() for x in v['interval']]
print(f'  interval limits examined: {len(limits)}; nearest to 0: {min(abs(x) for x in limits):.3g} (M1 needs one within 1e-9 of 0)')
