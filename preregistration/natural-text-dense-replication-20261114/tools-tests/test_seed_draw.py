"""Native tests of N8's seed draw (tools/n8_seed_draw.py, tools/n8_post_draw.py), the pin-only revision (tools/apply_pins.py) and the seal
(tools/build_n8_subject.py), on the synthetic corpus of test_tools.py (Windows Python 3.12, -I -B; NumPy). No seed of the study is drawn:
every draw is in fixture mode, with deterministic entropy and FIXTURE approval ids, in scratch folders outside D:. Nothing under a real
work/runs folder is opened.

    python -I -B test_seed_draw.py <N7_SEALED_SOURCE> <SCRATCH_DIR outside D:>

- The real wiring: the draw's paths are the plan's; the pilot's log is a real PASS whose five seeds the study census finds, run on the
  subject kept in seal/pilot/, which differs from this source in four files only; PILOT_COMMAND.txt pinned that log's script and subject,
  with its approval id and seeds; N7's partition, N7's left-over count and the owner's count agree; DRAW_COMMAND.txt pinned the scripts,
  policy and subject the owner's draw recorded, and every post-draw check passed; the plan pins that draw, the seal records it as DRAWN,
  and HASHES.json matches every file it names.
- The guard, in a child process (an audit hook cannot be removed): the manifest may be read; any other open, listing, write, removal or
  mkdir under a work/runs path, and any process start, is stopped.
- The draw, end to end in a child process under the guard: a scratch closed record whose work/runs holds the synthetic corpus and a planted
  seed record that the census must not open, a planted seed outside it that the census must find, and a scratch study folder holding a
  copy of the source, the frozen policy, a pilot log and a count. Its registry, partition, post-draw checks, disclosure and receipt.
- Refusals before any claim: FIXTURE or malformed approval ids, a malformed or another subject, a missing pilot log, a pilot log outside
  the census, an unreadable file in the study folder, a second draw. A failing post-draw check leaves the draw standing; the
  disclosure-only path then runs once.
- The seal: the pending seal of the source as it stood before the draw (seal/pre-pin/) equals the real one; apply_pins sets five pins, the
  two README status lines and the owner script's two hours lines, which then equal the study's own; the drawn seal accepts that and
  refuses a plan, README, owner script or other source file changed beyond them, another registry pin, another policy pin and a changed
  pre-pin copy, and the pending seal refuses once the registry is drawn; apply_pins refuses a second revision and a fixture registry for
  the study source.
"""
import json, os, re, shutil, subprocess, sys
from pathlib import Path
from unittest.mock import patch

HERE = Path(__file__).resolve().parent; STUDY = HERE.parent; SRC = STUDY / 'source'
sys.path.insert(0, str(HERE))
import test_tools as tt                       # the synthetic corpus, the fixture patches, the earlier partitions; its imports set the paths
from test_tools import check, refuses, results, sha, shaf
import fewepoch_plan as fp, peak_data, n7_matched_data, matched_plan as mp, matched_data as md, matched_registry as mr, count_fresh_pool as cfp
import n8_seed_draw as sd, n8_post_draw as pdd, apply_pins as aps, build_n8_subject as bs

PILOT_SEEDS = dict(init_seed=1111111111, weight_seed=2222222222, pretrain_order_seed=3333333333, adapt_order_seed=3999999999, benchmark_seed=123456789)   # fixture values only
PLANTED = dict(found=4000000001, hidden=4000000003)
REG_FILES = ['DISCLOSURE_FIGURES.md', 'DRAW.json', 'DRAW_CLAIM.json', 'EXCLUSIONS.json', 'PARTITION.json', 'REGISTRY.json', 'REGISTRY_AND_PARTITION_CHECK.json', 'SEED_DRAW_RECEIPT.json', 'SEED_REGISTRY_POLICY.md']


# ------------------------------------------------------------------ the real wiring (read only)
def real_wiring():
    print('--- the real wiring (nothing drawn, nothing written)')
    check("the draw's paths are the plan's: the manifest, the registry folder, the study folder and the closed record", sd.MANIFEST == mr.ROOT / fp.CORPUS / 'CORPUS_MANIFEST.json' and sd.REG_DIR == sd.STUDY / mp.REGISTRY['directory']
          and sd.STUDY == mr.STUDY == pdd.STUDY and sd.ROOT == mr.ROOT and sd.SRC == SRC and sd.PILOT_LOG == pdd.PILOT_LOG)
    log_raw = pdd.PILOT_LOG.read_bytes(); log = json.loads(log_raw); seeds = set(log['seeds'].values()); found, prov = mr.study_census(mr.STUDY)
    check("the pilot's log: a real PASS, and the study census finds its five seeds", log['status'] == 'PASS' and log['fixture'] is False and len(seeds) == 5 and seeds <= found and prov['unreadable_count'] == 0,
          f"log {sha(log_raw)[:16]}; census {len(found)} values from {prov['json_files_with_values']} files")
    kept = STUDY / 'seal/pilot/SOURCE_SUBJECT.json'; old = {f['path']: f['sha256'] for f in json.loads(kept.read_bytes())['files']}; now = {f['path']: f['sha256'] for f in json.loads((SRC / 'SOURCE_SUBJECT.json').read_bytes())['files']}
    differ = sorted(p for p in now if now[p] != old.get(p))
    check("the pilot ran on the subject kept in seal/pilot/, which differs from this source in four files only (pins, hours, README)", shaf(kept) == log['source_subject_sha256'] and set(old) == set(now)
          and differ == ['MATCHED_OWNER_RUN.ps1', 'README.md', 'matched_plan.py', 'matched_registry.py'], str(differ))
    command = (STUDY / 'PILOT_COMMAND.txt').read_text(encoding='utf-8'); pinned = dict(re.findall(r'"\$(?:study|src)\\([^"]+)" -Algorithm SHA256\)\.Hash\.ToLower\(\) -ne \'([0-9a-f]{64})\'', command))
    args = dict(re.findall(r'--([a-z-]+) (\S+)', command.split('n8_pilot.py ', 1)[1].splitlines()[0]))
    check('PILOT_COMMAND.txt pinned the pilot script and subject its log records, and passed its approval id and seeds', pinned == {'tools\\n8_pilot.py': log['pilot_sha256'], 'SOURCE_SUBJECT.json': log['source_subject_sha256']}
          and args.pop('approval-id') == log['approval_id'] and args.pop('expected-subject') == log['source_subject_sha256'] and {k.replace('-', '_'): int(v) for k, v in args.items()} == log['seeds'])
    n7_raw = pdd.N7_PARTITION.read_bytes(); left = json.loads(pdd.N7_CHECK.read_bytes())['left_over_articles']; counted = json.loads(pdd.COUNT.read_bytes())['n8_fresh_pool']
    check("N7's PARTITION.json equals its pin; N7's left-over articles equal the owner's count of the fresh pool", sha(n7_raw) == md.N7_PARTITION_SHA256 and left == counted['fresh_articles'],
          f"{counted['fresh_articles']:,} articles, {counted['fresh_sequences']:,} sequences")
    reg_dir = sd.REG_DIR; receipt = json.loads((reg_dir / 'SEED_DRAW_RECEIPT.json').read_bytes()); checked = json.loads((reg_dir / 'REGISTRY_AND_PARTITION_CHECK.json').read_bytes()); pre = shaf(STUDY / 'seal/pre-pin/SOURCE_SUBJECT.json')
    command = (STUDY / 'DRAW_COMMAND.txt').read_text(encoding='utf-8'); pinned = dict(re.findall(r'"\$(?:study|src|reg)\\([^"]+)" -Algorithm SHA256\)\.Hash\.ToLower\(\) -ne \'([0-9a-f]{64})\'', command))
    dargs = dict(re.findall(r'--([a-z-]+) (\S+)', next(ln for ln in command.splitlines() if 'n8_seed_draw.py" --' in ln)))
    check("DRAW_COMMAND.txt pinned the scripts, policy and subject the draw's receipt records, with its approval id; the hook stopped nothing; all 16 post-draw checks passed",
          pinned == {'tools\\n8_seed_draw.py': receipt['draw_script_sha256'], 'tools\\n8_post_draw.py': receipt['disclosure_script_sha256'], 'SEED_REGISTRY_POLICY.md': mr.POLICY_SHA256, 'SOURCE_SUBJECT.json': pre}
          and receipt['draw_script_sha256'] == shaf(sd.__file__) and receipt['disclosure_script_sha256'] == shaf(pdd.__file__) and receipt['source_subject_sha256'] == pre
          and dargs == {'approval-id': receipt['approval_id'], 'expected-subject': pre} and receipt['guard']['stopped_at'] is None and receipt['post_draw_all_pass'] is True and checked['all_pass'] and len(checked['checks']) == 16,
          f"receipt {shaf(reg_dir / 'SEED_DRAW_RECEIPT.json')[:16]}")
    sealed = json.loads((SRC / 'SOURCE_SUBJECT.json').read_bytes())['seed_registry_and_partition']
    check('the plan pins the drawn registry and partition, and the seal records them as DRAWN', mp.pins_set() and sealed['status'] == 'DRAWN' and (mp.REGISTRY['registry_sha256'], mp.REGISTRY['exclusions_sha256'], mp.REGISTRY['draw_sha256'],
          mp.PARTITION_SHA256, mp.REGISTRY['approval_id']) == (shaf(reg_dir / 'REGISTRY.json'), shaf(reg_dir / 'EXCLUSIONS.json'), shaf(reg_dir / 'DRAW.json'), shaf(reg_dir / 'PARTITION.json'), receipt['approval_id'])
          == (sealed['registry_sha256'], sealed['exclusions_sha256'], sealed['draw_sha256'], sealed['partition_sha256'], sealed['approval_id']))
    import write_hashes as wh; said = []
    with patch('builtins.print', lambda *a, **k: said.append(' '.join(map(str, a)))): code = wh.check()
    check('HASHES.json matches every file it names', code == 0, ' / '.join(said)[:200])


# ------------------------------------------------------------------ the fixture world
class World:
    """The synthetic corpus under a scratch closed record's work/runs, the earlier fixture partitions and the fixture count."""
    def __init__(self, scratch):
        self.scratch = scratch; self.closed = scratch / 'closed'; corpus = self.closed / 'work/runs/natural-text-corpus-fixture'
        self.man, self.digest, self.fix = tt.make_corpus(corpus); self.manifest = corpus / 'CORPUS_MANIFEST.json'
        (self.closed / 'reports/fixture').mkdir(parents=True); (self.closed / 'reports/fixture/SEEDS.json').write_text(json.dumps(dict(seed=PLANTED['found'])), encoding='utf-8')
        (self.closed / 'work/runs/hidden').mkdir(parents=True); (self.closed / 'work/runs/hidden/SEEDS.json').write_text(json.dumps(dict(seed=PLANTED['hidden'])), encoding='utf-8')
        regs = tt.registries(); seeds = {k: v['partition_seed'] for k, v in regs.items()}
        with tt.Fixture(self.fix):
            self.pins, n5, n6, n7a = tt.earlier_partitions(self.man, regs); n7 = n7_matched_data.partition(self.man, n5 | n6, regs['n7']['partition_seed'])
            self.count = cfp.count(self.man, seeds, self.pins, cfp.pool_record(peak_data.fresh_pool(self.man, n5 | n6)))
        self.n7_file = scratch / 'n7-fixture/PARTITION.json'; self.n7_file.parent.mkdir(); self.n7_file.write_bytes(n7_matched_data.encoded(n7)); self.left_over = n7['left_over_articles']

    def study(self, name, count=None):
        s = self.scratch / name; (s / bs.REGISTRY_DIR).mkdir(parents=True); (s / 'pilot').mkdir(); (s / 'data-count').mkdir(); shutil.copytree(SRC, s / 'source')
        for f in bs.PRE_PIN_COPIES + ('SOURCE_SUBJECT.json',): shutil.copyfile(STUDY / bs.PRE_PIN / f, s / 'source' / f)     # the source as it stood before the draw
        shutil.copyfile(STUDY / bs.REGISTRY_DIR / 'SEED_REGISTRY_POLICY.md', s / bs.REGISTRY_DIR / 'SEED_REGISTRY_POLICY.md')
        (s / 'pilot/PILOT_LOG.json').write_text(json.dumps(dict(status='PASS', fixture=True, seeds=PILOT_SEEDS)), encoding='utf-8')
        (s / 'data-count/FRESH_POOL_COUNT.json').write_text(json.dumps(count or self.count), encoding='utf-8')
        return s

    def kwargs(self, s, label):
        draw = dict(entropy=tt.entropy_for(label), root=self.closed, fixture=True, manifest_sha256=self.digest, fewepoch_partition_sha256=self.pins['few'], peak_partition_sha256=self.pins['peak'],
                    n7_partition_sha256=self.pins['n7'], study=s)
        disclose = dict(few_pin=self.pins['few'], peak_pin=self.pins['peak'], n7_pin=self.pins['n7'], manifest_sha256=self.digest, fixture=True, expected_fresh=self.left_over, n7_partition=self.n7_file,
                        count=s / 'data-count/FRESH_POOL_COUNT.json', pilot_log=s / 'pilot/PILOT_LOG.json', study=s)
        return dict(manifest=self.manifest, reg_dir=s / bs.REGISTRY_DIR, src=s / 'source', pilot_log=s / 'pilot/PILOT_LOG.json', draw_kwargs=draw, disclose_kwargs=disclose)

    def config(self, s, subject):
        return dict(manifest=str(self.manifest), study=str(s), subject=subject, fix=self.fix, closed=str(self.closed), pins=self.pins, digest=self.digest, n7_file=str(self.n7_file), left_over=self.left_over)


def from_config(cfg):
    """The World's kwargs, rebuilt in a child process from its config."""
    w = World.__new__(World); w.closed, w.manifest, w.digest, w.fix, w.pins, w.n7_file, w.left_over = Path(cfg['closed']), Path(cfg['manifest']), cfg['digest'], cfg['fix'], cfg['pins'], Path(cfg['n7_file']), cfg['left_over']
    return w


def listing(d): return {p.name: shaf(p) for p in sorted(Path(d).iterdir())}


# ------------------------------------------------------------------ child processes
def child_guard(scratch):
    runs = Path(scratch) / 'work/runs/corpus'; runs.mkdir(parents=True); m = runs / 'CORPUS_MANIFEST.json'; m.write_text('{}'); other = runs / 'OTHER.json'; other.write_text('{}')
    log = sd.install_guard(m); res = {}
    def attempt(name, fn):
        try: fn(); res[name] = 'allowed'
        except sd.RuleBroken: res[name] = 'stopped'
        except Exception as e: res[name] = type(e).__name__
    attempt('read the manifest', lambda: m.read_bytes())
    attempt('read the manifest by an upper-case, backslash path', lambda: open(str(m).upper().replace('/', '\\'), 'rb').close())
    attempt('read another file under work/runs', lambda: other.read_bytes())
    attempt('another file by an upper-case path', lambda: open(str(other).upper(), 'rb').close())
    attempt('list work/runs', lambda: os.listdir(runs.parent))
    attempt('scan a folder under work/runs', lambda: list(os.scandir(runs)))
    attempt('open the manifest to append', lambda: open(m, 'ab').close())
    attempt('remove a file under work/runs', lambda: os.remove(other))
    attempt('make a folder under work/runs', lambda: os.mkdir(runs / 'new'))
    attempt('write a file outside work/runs', lambda: (Path(scratch) / 'outside.json').write_text('{}'))
    attempt('start a process', lambda: subprocess.run(['cmd.exe', '/c', 'echo'], capture_output=True))
    print('GUARD ' + json.dumps(dict(results=res, log=log)))
    return 0


def child_draw(config):
    cfg = json.loads(Path(config).read_bytes()); w = from_config(cfg); s = Path(cfg['study'])
    log = sd.install_guard(cfg['manifest'])
    try:
        with tt.Fixture(cfg['fix']): return sd.run('FIXTURE-N8-DRAW', log, cfg['subject'], **w.kwargs(s, 'n8-draw-fixture'))
    except sd.RuleBroken as e:
        print(f'STOPPED by the rule on work/runs/: {e}'); return 2


# ------------------------------------------------------------------ the tests
def guard_checks(scratch):
    print('--- the guard (child process)')
    r = subprocess.run([sys.executable, '-I', '-B', __file__, '--child-guard', str(scratch / 'guard')], capture_output=True, text=True, timeout=300)
    line = next((ln for ln in r.stdout.splitlines() if ln.startswith('GUARD ')), None); got = json.loads(line[6:]) if line else {}; res = got.get('results', {})
    allowed = {'read the manifest', 'read the manifest by an upper-case, backslash path', 'write a file outside work/runs'}
    check('the manifest may be read (by any spelling of its path); every other touch of work/runs, and a process start, is stopped', r.returncode == 0 and len(res) == 11
          and all(v == ('allowed' if k in allowed else 'stopped') for k, v in res.items()) and got['log']['manifest_reads'] == 2, str(res) if r.returncode == 0 else r.stderr[-300:])


def draw_checks(n7, world):
    print('--- the draw, end to end under the guard (child process)')
    s = world.study('study-draw'); subject = bs.seal(n7, tt.CLOSED, study=s)
    check('the pending seal of the source as it stood before the draw equals the real pending seal, and keeps its copies in seal/pre-pin/', subject == shaf(STUDY / bs.PRE_PIN / 'SOURCE_SUBJECT.json')
          and sorted(p.name for p in (s / bs.PRE_PIN).iterdir()) == ['MATCHED_OWNER_RUN.ps1', 'README.md', 'SOURCE_SUBJECT.json', 'matched_plan.py'], subject[:16])
    cfg = world.scratch / 'child-draw.json'; cfg.write_text(json.dumps(world.config(s, subject)), encoding='utf-8')
    r = subprocess.run([sys.executable, '-I', '-B', __file__, '--child-draw', str(cfg)], capture_output=True, text=True, timeout=1200)
    reg_dir = s / bs.REGISTRY_DIR; names = sorted(p.name for p in reg_dir.iterdir())
    check('the draw exits 0, and writes the registry, partition, checks, disclosure and receipt, and nothing else', r.returncode == 0 and names == REG_FILES, (r.stdout + r.stderr)[-400:] if r.returncode else f'{len(names)} files')
    if r.returncode != 0 or names != REG_FILES: return s, subject
    receipt = json.loads((reg_dir / 'SEED_DRAW_RECEIPT.json').read_bytes()); checked = json.loads((reg_dir / 'REGISTRY_AND_PARTITION_CHECK.json').read_bytes())
    check('the receipt: the hook stopped nothing, the manifest was read and nothing else under work/runs, every post-draw check passed', receipt['guard']['stopped_at'] is None and receipt['guard']['manifest_reads'] >= 3
          and receipt['post_draw_all_pass'] is True and receipt['source_subject_sha256'] == subject and receipt['draw_script_sha256'] == shaf(sd.__file__) and receipt['disclosure_script_sha256'] == shaf(pdd.__file__),
          f"manifest reads {receipt['guard']['manifest_reads']}")
    failed = [k for k, v in checked['checks'].items() if not v['ok']]
    check('the post-draw record: every check passes, the fresh-pool and left-over checks among them', checked['all_pass'] and not failed and len(checked['checks']) == 16, f"{len(checked['checks'])} checks; failed {failed}")
    ex = json.loads((reg_dir / 'EXCLUSIONS.json').read_bytes()); reg = json.loads((reg_dir / 'REGISTRY.json').read_bytes())
    check("the census found the seed planted outside work/runs and never read the one inside it; the pilot's five seeds are excluded", PLANTED['found'] in ex['values'] and PLANTED['hidden'] not in ex['values']
          and set(PILOT_SEEDS.values()) <= set(ex['values']) and ex['provenance']['study_census']['root'] == str(s), f"{len(ex['values'])} exclusions")
    values = [reg['partition_seed']] + [g[k] for g in reg['groups'] for k in mr.ROLES] + [reg['benchmark']['benchmark_seed']]
    check('98 distinct role values, none of them excluded', len(values) == 98 == len(set(values)) and not set(values) & set(ex['values']) and [g['group'] for g in reg['groups']] == list(md.GROUPS))
    labels = ('Dry run of the exclusions, before any claim', "The pilot's five seeds are among the exclusions", 'All post-draw checks PASS', 'and nothing else. Receipt')
    check('the console shows the dry run, the pilot seeds excluded, the checks and the receipt, in that order', all(x in r.stdout for x in labels) and [r.stdout.index(x) for x in labels] == sorted(r.stdout.index(x) for x in labels))
    log = dict(manifest_reads=0, stopped_at=None); before = listing(reg_dir)
    with tt.Fixture(world.fix): ok, why = refuses(lambda: sd.run('FIXTURE-N8-DRAW', log, subject, **world.kwargs(s, 'n8-draw-again')), SystemExit, 'already drawn')
    check('a second draw is refused, and changes nothing in the registry folder', ok and listing(reg_dir) == before, why)
    other = world.scratch / 'other-pilot/PILOT_LOG.json'; other.parent.mkdir(); other.write_text(json.dumps(dict(seeds=dict(PILOT_SEEDS, init_seed=1234567))), encoding='utf-8')
    copy = world.scratch / 'registry-copy'; shutil.copytree(reg_dir, copy)
    with tt.Fixture(world.fix): rec = pdd.run(copy, world.manifest, **dict(world.kwargs(s, 'unused')['disclose_kwargs'], pilot_log=other), out=lambda *a: None)
    failed = [k for k, v in rec['checks'].items() if not v['ok']]
    check('the post-draw checks fail, on a copy of the registry, if a pilot seed is not among the exclusions', len(failed) == 1 and failed[0].startswith('98 distinct values'), str(failed)[:120])
    return s, subject


def refusal_checks(world, subject):
    print('--- refusals before any claim')
    for name, argv, text in (('a FIXTURE approval id', ['--approval-id', 'FIXTURE-N8-X', '--expected-subject', subject], 'never FIXTURE'),
                             ('a malformed approval id', ['--approval-id', 'OWNER-2026111-X', '--expected-subject', subject], 'OWNER-YYYYMMDD'),
                             ('a malformed subject', ['--approval-id', 'OWNER-00000000-TEST', '--expected-subject', 'abc'], 'must be a SHA-256')):
        ok, why = refuses(lambda: sd.main(argv), SystemExit, text); check(f'the command line refuses {name} before the hook', ok, why)
    s = world.study('study-refusals'); reg_dir = s / bs.REGISTRY_DIR; log = dict(manifest_reads=0, stopped_at=None); kw = world.kwargs(s, 'n8-refusals')
    elsewhere = world.scratch / 'elsewhere/PILOT_LOG.json'; elsewhere.parent.mkdir(); shutil.copyfile(s / 'pilot/PILOT_LOG.json', elsewhere)
    untouched = lambda: sorted(p.name for p in reg_dir.iterdir()) == ['SEED_REGISTRY_POLICY.md']
    with tt.Fixture(world.fix):
        for name, fn, text in (('another subject', lambda: sd.run('FIXTURE-N8-X', log, '0' * 64, **kw), 'differs from the one given'),
                               ('a missing pilot log', lambda: sd.run('FIXTURE-N8-X', log, subject, **dict(kw, pilot_log=s / 'pilot/NONE.json')), 'log is missing')):
            ok, why = refuses(fn, SystemExit, text); check(f'the draw refuses {name}, and claims nothing', ok and untouched(), why)
        (s / 'pilot/PILOT_LOG.json').unlink()                     # the log now lies only outside the study folder, where the census cannot see its seeds
        ok, why = refuses(lambda: sd.run('FIXTURE-N8-X', log, subject, **dict(kw, pilot_log=elsewhere)), SystemExit, "do not hold the pilot's five seeds")
        check('the draw refuses a pilot log outside the census, and claims nothing', ok and untouched(), why)
        shutil.copyfile(elsewhere, s / 'pilot/PILOT_LOG.json'); (s / 'data-count/BROKEN.json').write_text('{not json', encoding='utf-8')
        ok, why = refuses(lambda: sd.run('FIXTURE-N8-X', log, subject, **kw), SystemExit, 'could not read 1 file')
        check('the draw refuses an unreadable file in the study folder, and claims nothing', ok and untouched(), why)
        (s / 'data-count/BROKEN.json').unlink(); auth = s / 'source/AUTHORIZATION.json'; kept = auth.read_bytes(); auth.write_bytes(kept.replace(b'"enabled": false', b'"enabled": true'))
        ok, why = refuses(lambda: sd.run('FIXTURE-N8-X', log, subject, **kw), SystemExit, 'must be the disabled one')
        check('the draw refuses an enabled AUTHORIZATION.json, which the subject binds by hash, and claims nothing', ok and untouched() and auth.read_bytes() != kept, why); auth.write_bytes(kept)


def failing_check(world, subject):
    print('--- a failing post-draw check, then the disclosure-only path')
    wrong = json.loads(json.dumps(world.count)); wrong['n8_fresh_pool']['fresh_sequences'] += 1
    s = world.study('study-failing', count=wrong); reg_dir = s / bs.REGISTRY_DIR; log = dict(manifest_reads=0, stopped_at=None); said = []
    with tt.Fixture(world.fix): code = sd.run('FIXTURE-N8-FAIL', log, subject, **dict(world.kwargs(s, 'n8-failing'), out=said.append))
    checked = json.loads((reg_dir / 'REGISTRY_AND_PARTITION_CHECK.json').read_bytes()); receipt = json.loads((reg_dir / 'SEED_DRAW_RECEIPT.json').read_bytes())
    failed = [k for k, v in checked['checks'].items() if not v['ok']]
    check("a count that differs from the pool fails one check: exit 3, the draw stands, the receipt records the failure", code == 3 and (reg_dir / 'REGISTRY.json').is_file() and receipt['post_draw_all_pass'] is False
          and len(failed) == 1 and failed[0].startswith("the fresh pool equals the owner's count"), str(failed))
    kw = world.kwargs(s, 'unused'); kw = dict(manifest=kw['manifest'], reg_dir=kw['reg_dir'], src=kw['src'], disclose_kwargs=kw['disclose_kwargs'])
    ok, why = refuses(lambda: sd.disclosure_only('FIXTURE-N8-FAIL', log, subject, **kw), SystemExit, 'it stands')
    check('the disclosure-only path refuses while a check record exists', ok, why)
    (reg_dir / 'REGISTRY_AND_PARTITION_CHECK.json').unlink(); (s / 'data-count/FRESH_POOL_COUNT.json').write_text(json.dumps(world.count), encoding='utf-8')
    with tt.Fixture(world.fix): code = sd.disclosure_only('FIXTURE-N8-FAIL', log, subject, **dict(kw, out=said.append))
    check('with no check record it runs once, with no draw, under a receipt of its own', code == 0 and json.loads((reg_dir / 'REGISTRY_AND_PARTITION_CHECK.json').read_bytes())['all_pass']
          and (reg_dir / 'SEED_DRAW_RECEIPT-disclosure-only.json').is_file())


def seal_checks(n7, world, s):
    print('--- the pin-only revision and the seal')
    reg_dir = s / bs.REGISTRY_DIR; src = s / 'source'
    ok, why = refuses(lambda: bs.seal(n7, tt.CLOSED, study=s), SystemExit, 'The registry is drawn')
    check('the pending seal refuses once the registry is drawn', ok, why)
    plan_before, readme_before = (src / 'matched_plan.py').read_bytes(), (src / 'README.md').read_bytes(); said = []
    pins, diff = aps.revise(src=src, reg_dir=reg_dir, out=said.append)
    plus = [ln for ln in diff.splitlines() if ln.startswith('+') and not ln.startswith('+++')]; minus = [ln for ln in diff.splitlines() if ln.startswith('-') and not ln.startswith('---')]
    check('apply_pins changes five plan lines (None to the pins), the two README status lines and the two hours lines of the owner script, nothing else',
          len(plus) == len(minus) == 9 and sum(bool(re.search(r'= ?None[,)]?$', ln.rstrip())) for ln in minus) == 5 and sum('$hours=' in ln or '$m.hours' in ln for ln in minus) == sum('$hours=' in ln or '$m.hours' in ln for ln in plus) == 2
          and pins['partition_sha256'] == shaf(reg_dir / 'PARTITION.json') and bs.unpinned((src / 'matched_plan.py').read_text(encoding='utf-8')).encode('utf-8') == plan_before, f'{len(plus)} lines')
    check("the revised README and owner script equal the study's own", all((src / f).read_bytes() == (SRC / f).read_bytes() for f in ('README.md', 'MATCHED_OWNER_RUN.ps1')))
    subject = bs.seal(n7, tt.CLOSED, study=s); sealed = json.loads((src / 'SOURCE_SUBJECT.json').read_bytes())['seed_registry_and_partition']
    check('the seal accepts the revision as pin-only, and records the registry as DRAWN with its pins', sealed['status'] == 'DRAWN' and sealed['registry_sha256'] == pins['registry_sha256'] and sealed['partition_sha256'] == pins['partition_sha256']
          and sealed['approval_id'] == 'FIXTURE-N8-DRAW', subject[:16])
    ok, why = refuses(lambda: aps.revise(src=src, reg_dir=reg_dir, out=said.append), SystemExit, 'already pins')
    check('apply_pins refuses a second revision', ok, why)
    with patch.object(aps, 'STUDY', s):
        ok, why = refuses(lambda: aps.revise(src=s / 'source', reg_dir=reg_dir, out=said.append), SystemExit, 'only a real registry')
    check('apply_pins refuses a fixture registry for the study source (the scratch study standing in for it)', ok, why)
    def mutated(k, name, edit):
        t = world.scratch / f'seal-{k}'; shutil.copytree(s, t); p = t / 'source' / name; p.write_bytes(edit(p.read_bytes().decode('utf-8')).encode('utf-8')); return t
    for k, (name, edit, text) in enumerate((('matched_plan.py', lambda x: x.replace('RATE = 1e-4', 'RATE = 3e-4'), 'the plan differs beyond its pins'),
                                            ('README.md', lambda x: x + 'One more line.\n', 'the README differs beyond its status lines'),
                                            ('MATCHED_OWNER_RUN.ps1', lambda x: x.replace('$free -lt 3GB', '$free -lt 2GB'), 'the owner script differs beyond its hours'),
                                            ('matched_worker.py', lambda x: x + '# one more line\n', "Not a pin-only revision: ['MATCHED_OWNER_RUN.ps1', 'README.md', 'matched_plan.py', 'matched_worker.py']"),
                                            ('matched_plan.py', lambda x: x.replace(pins['registry_sha256'], '0' * 64), 'does not pin this registry'),
                                            ('matched_registry.py', lambda x: x.replace(mr.POLICY_SHA256, '1' * 64), 'must both pin the frozen seed policy'),
                                            ('../seal/pre-pin/README.md', lambda x: x + 'One more line.\n', 'differ from the pending seal'))):
        t = mutated(k, name, edit); ok, why = refuses(lambda: bs.seal(n7, tt.CLOSED, study=t), SystemExit, text)
        check(f"the seal refuses {name.replace('../', '')} changed ({text})", ok, why)


def main(n7, scratch):
    if str(scratch.resolve()).lower().startswith('d:'): raise SystemExit('The scratch folder must be outside D:')
    scratch.mkdir(parents=True, exist_ok=False)
    print(f"python {sys.version.split()[0]}; N8 source subject {shaf(SRC / 'SOURCE_SUBJECT.json')[:16]}; policy {mr.POLICY_SHA256[:16]}")
    real_wiring(); guard_checks(scratch)
    world = World(scratch); s, subject = draw_checks(n7, world); refusal_checks(world, subject); failing_check(world, subject); seal_checks(n7, world, s)
    print(f'{sum(results)} passed, {len(results) - sum(results)} failed')
    return 0 if all(results) else 1


if __name__ == '__main__':
    if len(sys.argv) == 3 and sys.argv[1] == '--child-guard': raise SystemExit(child_guard(sys.argv[2]))
    if len(sys.argv) == 3 and sys.argv[1] == '--child-draw': raise SystemExit(child_draw(sys.argv[2]))
    if len(sys.argv) != 3: raise SystemExit(__doc__)
    raise SystemExit(main(Path(sys.argv[1]), Path(sys.argv[2])))
