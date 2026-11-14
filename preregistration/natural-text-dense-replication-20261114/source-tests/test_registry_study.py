"""The registry's census of the study folder (protocol section 4) and the worker's list of kept states (section 3), on native Windows and in
WSL. No seed is drawn: every draw here is refused before its claim.

    python -I -B test_registry_study.py <SCRATCH_DIR outside D:>

- the study folder comes from matched_plan.STUDY_ROOT by OS, the same as the worker's, and is the real folder;
- the real study folder is read in full by the census (no file unreadable or skipped);
- a missing study folder, and a study folder with an unreadable JSON file, refuse the census and the draw, and the draw claims nothing;
- a readable folder's saved seeds are found;
- kept_states lists model states and partial state writes, and nothing else.
"""
import json, os, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent; SRC = HERE.parent / 'source'
sys.path.insert(0, str(SRC)); sys.path.insert(1, str(SRC / 'vendor'))
import matched_plan as mp, matched_registry as mr, matched_worker as mw

results = []


def check(name, ok, detail=''):
    results.append(bool(ok)); print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f'  [{detail}]' if detail else ''))


def refuses(fn, text):
    try: fn()
    except SystemExit as e: return text in str(e), str(e)[:150]
    except BaseException as e: return False, f'{type(e).__name__}: {str(e)[:150]}'
    return False, 'no refusal'


def main(scratch):
    if str(scratch.resolve()).replace('\\', '/').lower().startswith(('d:', '/mnt/d')): raise SystemExit('The scratch folder must be outside D:')
    scratch.mkdir(parents=True, exist_ok=False)
    system = 'posix' if os.name == 'posix' else 'nt'; print(f'{sys.platform}, python {sys.version.split()[0]}')
    check(f'the study folder by OS ({system}) is matched_plan.STUDY_ROOT, the same as the worker\'s, and exists', mr.STUDY == Path(mp.STUDY_ROOT[system]) == mw.STUDY and mr.STUDY.is_dir(), str(mr.STUDY))
    values, prov = mr.study_census(mr.STUDY)
    check('the real study folder is read in full by the census', prov['unreadable_count'] == 0, f"{prov['json_files_with_values']} JSON files with values, {len(values)} values, nothing unreadable")
    missing = scratch / 'no-such-study'; ok, why = refuses(lambda: mr.study_census(missing), 'does not exist'); check('a missing study folder refuses the census', ok, why)
    bad = scratch / 'bad-study'; bad.mkdir(); (bad / 'LOG.json').write_text(json.dumps(dict(seeds=dict(init_seed=4242))), encoding='utf-8'); (bad / 'BROKEN.json').write_text('{"seeds": [1, 2', encoding='utf-8')
    ok, why = refuses(lambda: mr.study_census(bad), 'could not read'); check('an unreadable JSON file in the study folder refuses the census', ok, why)
    good = scratch / 'good-study'; good.mkdir(); (good / 'LOG.json').write_text(json.dumps(dict(seeds=dict(init_seed=4242, weight_seed=4343))), encoding='utf-8')
    values, prov = mr.study_census(good); check('a readable folder\'s saved seeds are found', {4242, 4343} <= values and prov['unreadable_count'] == 0)
    for k, (name, study, text) in enumerate((('a missing study folder', missing, 'does not exist'), ('an unreadable study file', bad, 'could not read'))):
        reg = scratch / f'registry-{k}'; reg.mkdir(); (reg / 'SEED_REGISTRY_POLICY.md').write_text('fixture policy\n', encoding='utf-8')
        ok, why = refuses(lambda: mr.draw(reg, scratch / 'none.json', 'FIXTURE-N8-STUDY', entropy=lambda k: b'\0' * k, root=good, fixture=True, study=study), text)
        check(f'the draw refuses {name} and claims nothing', ok and sorted(p.name for p in reg.iterdir()) == ['SEED_REGISTRY_POLICY.md'], why)
    states = scratch / 'states'; (states / 'n01' / 'w768').mkdir(parents=True)
    for name, data in (('n01/w768/E0.pt', b'state'), ('n01/w768/E1.pt.part', b'partial'), ('n01/w768/E0.f32', b'arrays'), ('n01/notes.txt', b'text')): (states / name).write_bytes(data)
    kept = mw.kept_states(states, 'n01')
    check('kept_states lists model states and partial state writes, with their hashes, and nothing else', sorted(x['path'] for x in kept['kept']) == ['n01/w768/E0.pt', 'n01/w768/E1.pt.part'] and not kept['errors'] and kept['kept_bytes'] == 12,
          str([x['path'] for x in kept['kept']]))
    print(f'{sum(results)} passed, {len(results) - sum(results)} failed')
    return 0 if all(results) else 1


if __name__ == '__main__':
    if len(sys.argv) != 2: raise SystemExit(__doc__)
    raise SystemExit(main(Path(sys.argv[1])))
