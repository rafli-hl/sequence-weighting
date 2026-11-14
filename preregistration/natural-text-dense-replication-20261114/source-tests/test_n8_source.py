"""Native tests of N8's source changes (Windows Python 3.12, -I -B; NumPy). No WSL, PyTorch, CUDA, GPU query, seed draw or training,
and nothing under any work/runs folder is opened.

    python -I -B test_n8_source.py <N7_SEALED_SOURCE> <SCRATCH_DIR outside D:>

What it covers, for each change in CHANGES.md:
- byte copies: every reused file equals N7's sealed copy, and n7_matched_data.py equals N7's matched_data.py;
- the plan: the readout grid and its update numbers, the arm, the runs and retry runs, and agreement with analysis/n8_analysis.py;
- the data: on a synthetic corpus (N patched down, as N7's suite did), N7's partition re-derived with N7's own function and added to the
  assigned articles; 24 disjoint groups; a wrong N7 pin refused;
- the registry: 98 roles derived in group order; N7's registry values and a value saved in the study folder are excluded; the plan and
  the registry tool pin the frozen policy; the draw and the admission check refuse any other policy;
- the worker: retry admission on first-attempt terminals; the per-stage counts and the cap; one stage on NumPy stand-ins writes the
  batch orders with hashes that n8_analysis.order_sha256 reproduces, and keeps both E0 states; the E0 comparison of a retry; refusals;
- the owner script: Windows PowerShell 5.1 refuses disabled, foreign and badly listed activations before claiming anything.
What it cannot show: the worker on real PyTorch and CUDA, and the partition on the real corpus manifest (steps 3 and 4).
"""
import hashlib, json, math, random, shutil, subprocess, sys, tempfile
from pathlib import Path
from unittest.mock import patch

import numpy as np

HERE = Path(__file__).resolve().parent; STUDY = HERE.parent; SRC = STUDY / 'source'
sys.path.insert(0, str(SRC)); sys.path.insert(1, str(SRC / 'vendor')); sys.path.insert(2, str(STUDY / 'analysis'))
import fewepoch_data, fewepoch_plan as fp, peak_data, n7_matched_data, text_plan, text_worker
import matched_plan as mp, matched_data as md, matched_registry as mr, matched_worker as mw
import n8_analysis as na

PS_EXE = r'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe'
FROM_N7 = ('a1_download.py', 'a2_rows.py', 'acquire_common.py', 'acquire_plan.py', 'fewepoch_analysis.py', 'fewepoch_data.py', 'fewepoch_plan.py', 'fewepoch_registry.py', 'fewepoch_worker.py', 'peak_data.py',
           'text_analysis.py', 'text_data.py', 'text_engine.py', 'text_framework_setup.py', 'text_model.py', 'text_plan.py', 'text_registry.py', 'text_worker.py', 'wt103_corpus.py', 'vendor/core.py',
           'ORIGINAL_ENVIRONMENT.json', 'gpu_check.ps1', 'GPU_CHECK.json', 'power_gate.ps1')
results = []
sha = lambda b: hashlib.sha256(b).hexdigest()


def check(name, ok, detail=''):
    results.append(bool(ok)); print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f'  [{detail}]' if detail else ''))


def refuses(fn, kind, text):
    try: fn()
    except kind as e: return text in str(e), str(e)[:120]
    except BaseException as e: return False, f'{type(e).__name__}: {str(e)[:120]}'
    return False, 'no refusal'


# ------------------------------------------------------------------ byte copies
def byte_copies(n7):
    print('--- byte copies of N7\'s sealed source')
    differ = [f for f in FROM_N7 if (SRC / f).read_bytes() != (n7 / f).read_bytes()]
    check(f'{len(FROM_N7)} reused files are byte copies of N7\'s sealed source', not differ, ', '.join(differ))
    check('n7_matched_data.py is a byte copy of N7\'s matched_data.py', (SRC / 'n7_matched_data.py').read_bytes() == (n7 / 'matched_data.py').read_bytes())
    check('matched_analysis.py and PROTOCOL.md are dropped', not (SRC / 'matched_analysis.py').exists() and not (SRC / 'PROTOCOL.md').exists())


# ------------------------------------------------------------------ plan
def plan_checks():
    print('--- the plan')
    ups = [fp.readout_update(e, mp.N_TRAIN, text_plan.BATCH) for e in mp.READOUTS]
    check('readouts: E0.25, E0.5, E1, then every 64 updates from update 2,048 to 3,584 (28)', ups == [256, 512, 1024] + list(range(2048, 3585, 64)) and len(mp.READOUTS) == 28, f'{ups[:4]} ... {ups[-1]}')
    check('readout updates and the match path equal n8_analysis.py\'s', tuple(ups) == na.READOUT_UPDATES and mp.MATCH_PATH == na.PLAN['path'] and mp.FINAL == na.PLAN['final'] and mp.PREVIOUS == na.PLAN['previous'])
    check('E3.5 is update 3,584, inside the 4 order epochs', fp.readout_update(mp.LAST_READOUT, mp.N_TRAIN) == 3584 <= mp.ORDER_EPOCHS * mp.N_TRAIN // text_plan.BATCH)
    check('one arm per width, at 1e-4 (tag equals the analysis\'s)', mp.ARMS == {768: (1e-4,), 512: (1e-4,)} and mp.TAG == na.RATE_TAG == 'lr1e-04')
    stages = [d for m in mp.RUN_MODES for d in mp.RUN_STAGES[m]]
    check('R1-R8 hold n01-n24 in order, three each; X<k> retries R<k>', stages == list(md.GROUPS) == list(na.DRAWS) and all(len(v) == 3 for v in mp.RUN_STAGES.values()) and mp.RETRY_OF == {f'X{k}': f'R{k}' for k in range(1, 9)})
    paths = list(mp.ACTIVATIONS.values()) + list(mp.RUNS.values())
    check('16 activations and 16 run folders, distinct, under the study folder, none under work/runs', len(set(paths)) == 32 and all('work/runs' not in p for p in paths) and str(mw.STUDY) == mp.STUDY_ROOT['nt'])
    reg_dir = STUDY / mp.REGISTRY['directory']; h = lambda n: sha((reg_dir / n).read_bytes()); policy = h('SEED_REGISTRY_POLICY.md')
    check("the plan and the registry tool pin the frozen seed policy; the plan pins the owner's drawn registry and partition, each equal to its file",
          mp.pins_set() and mp.REGISTRY['policy_sha256'] == mr.POLICY_SHA256 == policy and (mp.REGISTRY['registry_sha256'], mp.REGISTRY['exclusions_sha256'], mp.REGISTRY['draw_sha256'], mp.PARTITION_SHA256)
          == (h('REGISTRY.json'), h('EXCLUSIONS.json'), h('DRAW.json'), h('PARTITION.json')) and mp.REGISTRY['approval_id'] == json.loads((reg_dir / 'REGISTRY.json').read_bytes())['approval_id'],
          f"policy {policy[:16]}, registry {mp.REGISTRY['registry_sha256'][:16]}, partition {mp.PARTITION_SHA256[:16]}")


# ------------------------------------------------------------------ data
def manifest(n_articles=3000):
    """A synthetic corpus manifest with the fields the sealed partition functions read: excluded articles and planted text copies."""
    arts, first = [], 0
    for i in range(n_articles):
        s = 1 + (i * 7) % 5; text = f'article-{i}' if i % 37 else f'article-{i - 1}'      # every 37th article repeats the text of the one before it
        arts.append(dict(index=i, sequences=s, first=first, text_sha256=sha(text.encode()))); first += s
    return dict(exclusions=dict(articles=list(range(0, n_articles, 31))), splits=dict(train=dict(articles=arts)))


def data_checks():
    print('--- the data (synthetic corpus; N patched to 64, N5\'s fill to 128)')
    man = manifest(); seeds = dict(few=101, peak=202, n7=303, n8=404)      # fixture values for the synthetic corpus only
    with patch.object(fp, 'N_FILL', 128), patch.object(peak_data, 'N_TRAIN', 64), patch.object(n7_matched_data, 'N_TRAIN', 64), patch.object(md, 'N_TRAIN', 64):
        few = fewepoch_data.partition(man, seeds['few']); few_pin = sha(peak_data.encoded(few)); n5 = {a for g in few['groups'].values() for a in g['articles']}
        peak = peak_data.partition(man, n5, seeds['peak']); peak_pin = sha(peak_data.encoded(peak)); n6 = {a for g in peak['groups'].values() for a in g['articles']}
        n7 = n7_matched_data.partition(man, n5 | n6, seeds['n7']); n7_pin = sha(n7_matched_data.encoded(n7)); n7a = {a for g in n7['groups'].values() for a in g['articles']}
        assigned = md.assigned_articles(man, seeds['few'], seeds['peak'], seeds['n7'], few_pin, peak_pin, n7_pin)
        check("assigned articles = N5's, N6's and N7's partitions, each re-derived with its own sealed function", assigned == n5 | n6 | n7a and n7a and not (n7a & (n5 | n6)),
              f'{len(n5)} + {len(n6)} + {len(n7a)} articles')
        ok, why = refuses(lambda: md.assigned_articles(man, seeds['few'], seeds['peak'], seeds['n7'], few_pin, peak_pin, '0' * 64), ValueError, 'N7 partition differs')
        check('a wrong N7 pin is refused', ok, why)
        part = md.partition(man, assigned, seeds['n8']); d = md.disjoint(part, man, assigned); pool = part['pool']
        check('24 groups n01-n24 of N sequences, disjoint from every assigned article and its text', sorted(part['groups']) == list(md.GROUPS) and d == dict(articles=d['articles'], groups=24, n=64)
              and not ({a for g in part['groups'].values() for a in g['articles']} & n7a), f"{d['articles']} articles; pool {pool['fresh_articles']} fresh, {pool['removed_text_duplicates_of_assigned']} text copies of assigned and {pool['removed_repeats_inside_the_pool']} repeats removed")
        tiny = dict(man, splits=dict(train=dict(articles=man['splits']['train']['articles'][:400])))
        ok, why = refuses(lambda: md.partition(tiny, set(), seeds['n8']), ValueError, 'cannot fill 24 groups')
        check('a pool too small for 24 groups is refused', ok, why)


# ------------------------------------------------------------------ registry
def registry_checks(scratch):
    print('--- the registry')
    raw = b''.join(hashlib.sha256(f'fixture-entropy-{i}'.encode()).digest()[:4] for i in range(mr.CANDIDATES))
    draw_raw = mr.encoded(dict(entropy_hex=raw.hex(), bytes=len(raw), decoding='fixture'))
    partition_seed, groups, bench, decisions = mr.derive(draw_raw, [])
    check('98 roles derived from 256 candidates: partition, n01-n24 x 4 roles, benchmark', len(mr.ROLE_ORDER) == 98 and [g['group'] for g in groups] == list(md.GROUPS) and all(set(g) == {'group', *mr.ROLES} for g in groups) and 'benchmark_seed' in bench,
          f"{sum(x['accepted'] for x in decisions)} accepted")
    root, study = scratch / 'census-root', scratch / 'census-study'; root.mkdir(); (study / 'pilot').mkdir(parents=True)
    (study / 'pilot' / 'PILOT_LOG.json').write_text(json.dumps(dict(seeds=dict(init_seed=3141592653))), encoding='utf-8')
    excluded, prov = mr.exclusions(root, (), study)
    n7 = json.loads((mr.ROOT / mr.N7_DIRECTORY / 'REGISTRY.json').read_bytes())
    check("exclusions hold every N7 registry value and a seed saved in the study folder", mr.text_registry_values(n7) <= set(excluded) and 3141592653 in excluded and prov['study_census']['values'] == 1,
          f"{len(excluded)} values; N7 registry {sha((mr.ROOT / mr.N7_DIRECTORY / 'REGISTRY.json').read_bytes())[:16]}")
    reg_dir = scratch / 'registry'; reg_dir.mkdir(); (reg_dir / 'SEED_REGISTRY_POLICY.md').write_text('fixture policy\n', encoding='utf-8')
    ok, why = refuses(lambda: mr.draw(reg_dir, scratch / 'none.json', 'FIXTURE-N8-01', entropy=lambda k: raw, root=root, fixture=True, study=study), SystemExit, 'Policy differs')
    check('the draw refuses a policy that differs from the pinned one, and claims nothing', ok and sorted(p.name for p in reg_dir.iterdir()) == ['SEED_REGISTRY_POLICY.md'], why)
    fake = dict(status='FROZEN_DRAWN', groups=groups, corpus_manifest_sha256=fp.CORPUS_MANIFEST_SHA256, policy_sha256=sha(b'fixture policy\n'))
    ok, why = refuses(lambda: mr.validate(fake, b'{}', draw_raw), ValueError, 'frozen policy')
    check('admission refuses a registry bound to another policy', ok, why)


# ------------------------------------------------------------------ worker
def terminal(status, mode='R2', done=(), subject='S', inputs=None):
    return json.dumps(dict(kind='n8', mode=mode, status=status, subject=subject, bindings=inputs or dict(registry_sha256='r', partition_sha256='p', corpus_manifest_sha256='c'),
                           stages=[dict(stage=d, status='COMPLETE') for d in done])).encode()


def worker_admission():
    print('--- the worker: retry admission')
    ours = dict(registry_sha256='r', partition_sha256='p', corpus_manifest_sha256='c')
    check('a failed R2 after n04: X2 repeats n05 and n06', mw.check_first_attempt(terminal('FAILED', done=('n04',)), 'X2', ours, 'S') == ['n05', 'n06'])
    check('R2 stopped at start-up: X2 repeats all three', mw.check_first_attempt(terminal('STOPPED_AT_STARTUP'), 'X2', ours, 'S') == ['n04', 'n05', 'n06'])
    for name, raw, mode, text in (('a COMPLETE run', terminal('COMPLETE', done=('n04', 'n05', 'n06')), 'X2', 'does not admit'), ("another run's terminal", terminal('FAILED'), 'X3', 'does not admit'),
                                  ('another subject', terminal('FAILED', subject='T'), 'X2', 'another source subject'), ('other inputs', terminal('FAILED', inputs=dict(ours, partition_sha256='q')), 'X2', 'other inputs'),
                                  ('nothing left to repeat', terminal('FAILED', done=('n04', 'n05', 'n06')), 'X2', 'no draw to repeat'), ('an N7 terminal', terminal('FAILED').replace(b'"n8"', b'"matched"'), 'X2', 'does not admit')):
        ok, why = refuses(lambda: mw.check_first_attempt(raw, mode, ours, 'S'), PermissionError, text); check(f'retry refused on {name}', ok, why)


def worker_counts():
    print('--- the worker: counts and cap')
    c = mw.study_counts(mp.N_TRAIN, 10000)
    check('per stage: 2 trajectories, 12 files, 3,584 updates, 28 readouts of 528 evaluation batches, 512 KiB of orders',
          c['trajectories'] == 2 and c['files'] == 12 and c['adapt_updates'] == 3584 and c['readout_eval_batches'] == 28 * 528 and c['order_bytes'] == 524288 and c['array_bytes'] == 4 * 28 * 16896, str({k: c[k] for k in ('files', 'readout_eval_batches', 'array_bytes')}))
    arch = {str(w): dict(seconds_per_pretraining_update=0.01, seconds_per_eval_batch=0.004, seconds_per_state_write=0.5, seconds_per_state_reload=0.5, seconds_per_update=0.02) for w in mp.WIDTHS}
    bench = dict(architectures=arch, overheads=dict(seconds_data_generation=1.0, seconds_per_full_guard=0.05, seconds_per_inventory_entry=1e-4, cache_entries=10, seconds_per_epoch_guard=1e-3))
    with patch.object(text_worker, 'write_model', lambda a: (0.05, 1e-8)):
        three, one = mw.study_cap(bench, 3, mp.N_TRAIN, 10000), mw.study_cap(bench, 1, mp.N_TRAIN, 10000)
    check("the cap uses the run's own number of draws (3 for R<k>, fewer for a retry)", three['stages'] == 3 and one['stages'] == 1 and one['formula'] != three['formula'] and three['feasible'],
          f"stand-in timings: projected {three['projected_stage_seconds']:.0f} s per draw; cap {three['stage_work_cap_seconds']} s")
    state = 4 * (text_plan.parameters(512) + text_plan.parameters(768)); other = 2 * 4 * 28 * 16896 + 2 * 4 * 16896 + 524288 + 16384 * 22 + 4 * 2 ** 18
    check('both E0 states fit the stage quota with arrays, orders and records (estimate without torch.save overhead)', state + other < fp.LIMITS['stage_storage_bytes'],
          f'{(state + other) / 2 ** 20:.1f} MiB of {fp.LIMITS["stage_storage_bytes"] / 2 ** 20:.0f} MiB')


class T:
    """A NumPy stand-in for the few tensor methods stage() and inputs() call."""
    def __init__(self, a): self.a = np.asarray(a)
    def detach(self): return self
    def cpu(self): return self
    def contiguous(self): return self
    def numpy(self): return self.a
    def tolist(self): return self.a.tolist()
    def __iter__(self): return (T(x) for x in self.a)


class Engine:
    def load_sequences(self, split, idx): return list(idx)
    def weights(self, seed, n): return T(np.linspace(0.5, 1.5, n, dtype=np.float32))
    def orders(self, seed, n, epochs): return T(np.stack([np.random.default_rng(seed + e).permutation(n) for e in range(1, epochs + 1)]).astype(np.int64))
    def tensor_hash(self, x): return sha(np.ascontiguousarray(x.a if isinstance(x, T) else np.asarray(x)).tobytes())


class Guard:
    def full(self): pass
    def epoch(self): pass


class Ctx:
    def __init__(self, out): self.engine, self.out, self.guard = Engine(), out, Guard()
    def pretrain(self, stage, width, seeds, pool, data, pool_orders):
        return dict(state=self.out.write(f'{stage}/w{width}/E0.pt', f'state of {width}'.encode()), E0_arrays=self.out.write(f'{stage}/w{width}/E0.f32', np.full(4, width, '<f4').tobytes()))
    def adapt_readouts(self, stage, width, lr, tag, pre, seeds, data, weights, orders, arrays): return dict(readouts=[], status='COMPLETE')


def worker_stage(scratch):
    print('--- the worker: one stage on NumPy stand-ins')
    root = scratch / 'runs' / 'n8-x1'; root.mkdir(parents=True)
    out = text_worker.Output(root, fp.LIMITS['stage_storage_bytes'], fp.LIMITS['stage_files'], fp.LIMITS['storage_bytes'], fp.LIMITS['total_files'])
    n = 64; partition = dict(n=n, groups={'n02': dict(articles=[1], sequences=list(range(100, 100 + n)))}); corpus = dict(train='t', validation='v', test='p', validation_indices=[0], pool_indices=[0, 1])
    seeds = dict(init_seed=1, weight_seed=2, pretrain_order_seed=3, adapt_order_seed=4)        # fixture values for the stand-ins only
    rows, states = mw.stage(Ctx(out), 'n02', seeds, corpus, partition, n)
    inputs = json.loads((root / 'n02' / 'INPUTS.json').read_bytes()); raw = (root / 'n02' / mp.ORDER_FILE).read_bytes()
    orders = np.frombuffer(raw, dtype='<i8').reshape(mp.ORDER_EPOCHS, n); expect = Engine().orders(seeds['adapt_order_seed'], n, mp.ORDER_EPOCHS).a
    check('ORDERS.i64 holds the 4 epoch orders as little-endian int64, and INPUTS.json binds the file', np.array_equal(orders, expect) and inputs['order_file'] == dict(path=f'n02/{mp.ORDER_FILE}', bytes=len(raw), sha256=sha(raw)))
    check("INPUTS.json's per-epoch hashes are n8_analysis.order_sha256 of each order", inputs['epoch_order_sha256'] == [na.order_sha256(o) for o in orders])
    kept = json.loads((root / 'n02' / 'STATES_KEPT.json').read_bytes())
    check('both E0 states are kept and listed with their SHA-256; nothing is deleted', sorted(x['path'] for x in kept['kept']) == ['n02/w512/E0.pt', 'n02/w768/E0.pt']
          and all((root / x['path']).is_file() and sha((root / x['path']).read_bytes()) == x['sha256'] for x in kept['kept']) and not (root / 'n02' / 'STATES_DELETED.json').exists())
    first = scratch / 'runs' / 'n8-r1' / 'n02'
    (first / 'w768').mkdir(parents=True); (first / 'w768' / 'E0.f32').write_bytes(np.full(4, 768, '<f4').tobytes())
    (first / 'w512').mkdir(); (first / 'w512' / 'E0.f32').write_bytes(np.full(4, 0, '<f4').tobytes())
    got = mw.e0_against_first_attempt('X1', 'n02', root); shutil.rmtree(first / 'w512'); got2 = mw.e0_against_first_attempt('X1', 'n02', root)
    check("a retry compares each width's E0 losses with its first attempt's", got == {'768': 'SAME', '512': 'DIFFERENT'} and got2 == {'768': 'SAME', '512': 'ABSENT'} and mw.e0_against_first_attempt('R1', 'n02', root) is None, f'{got}, then {got2}')


def worker_refusals(scratch):
    print('--- the worker: refusals')
    ok, why = refuses(lambda: mw.run(), PermissionError, 'DISABLED'); check('the disabled source refuses to run', ok, why)
    act = scratch / 'activation'; act.mkdir()
    pending = dict(mw.PINS, registry_sha256=None)              # the plan's pins are set since the draw; a PENDING one is passed explicitly
    for name, auth, pins, text in (('an N7 mode', dict(enabled=True, execution_ready=True, mode='M1', one_use=True, approval_id='FIXTURE-N8'), mw.PINS, 'DISABLED'),
                                   ('a PENDING pin', dict(enabled=True, execution_ready=True, mode='R1', one_use=True, approval_id='FIXTURE-N8', fixture=True), pending, 'PENDING')):
        (act / 'AUTHORIZATION.json').write_text(json.dumps(auth), encoding='utf-8')
        ok, why = refuses(lambda: mw.authorization(act, pins=pins), PermissionError, text); check(f'admission refuses {name}', ok, why)


# ------------------------------------------------------------------ owner script
def owner_script(scratch):
    print('--- the owner script (Windows PowerShell 5.1)')
    for name, auth, text in (('a disabled activation', dict(enabled=False), 'DISABLED: no N8 approval'),
                             ('an N7 mode', dict(enabled=True, execution_ready=True, mode='M1'), 'Invalid activation'),
                             ("an X1 listing a draw outside R1", dict(enabled=True, execution_ready=True, mode='X1', stages=['n04']), 'Invalid activation: its draws'),
                             ('an R1 listing two of its three draws', dict(enabled=True, execution_ready=True, mode='R1', stages=['n01', 'n02']), 'Invalid activation: its draws'),
                             ('a valid X1 outside its activation folder', dict(enabled=True, execution_ready=True, mode='X1', stages=['n02'], one_use=True, approval_id='FIXTURE-N8', fixture=False), 'Invalid activation'),
                             ('a valid R1 outside its activation folder', dict(enabled=True, execution_ready=True, mode='R1', stages=['n01', 'n02', 'n03'], one_use=True, approval_id='FIXTURE-N8', fixture=False), 'Invalid activation')):
        d = Path(tempfile.mkdtemp(dir=scratch)); shutil.copyfile(SRC / 'MATCHED_OWNER_RUN.ps1', d / 'MATCHED_OWNER_RUN.ps1'); (d / 'AUTHORIZATION.json').write_text(json.dumps(auth), encoding='utf-8')
        r = subprocess.run([PS_EXE, '-NoProfile', '-NonInteractive', '-ExecutionPolicy', 'Bypass', '-File', str(d / 'MATCHED_OWNER_RUN.ps1'), '-ExpectedSubject', '0' * 64], capture_output=True, text=True, timeout=120)
        msg = (r.stderr + r.stdout).replace('\n', ' ')
        exact = 'its draws' in text or 'its draws' not in msg
        check(f'refuses {name}, claiming nothing', r.returncode != 0 and text in msg and exact and sorted(p.name for p in d.iterdir()) == ['AUTHORIZATION.json', 'MATCHED_OWNER_RUN.ps1'],
              next((ln.strip() for ln in (r.stderr or '').splitlines() if text.split(':')[0] in ln), '')[:90])


SPACE_PROBE = r"""
$ast=[System.Management.Automation.Language.Parser]::ParseFile('PATH_HERE',[ref]$null,[ref]$null)
$f=$ast.Find({param($n) $n -is [System.Management.Automation.Language.FunctionDefinitionAst] -and $n.Name -eq 'Get-AdmissionSpaceRefusal'},$true)
. ([scriptblock]::Create($f.Extent.Text))
$cases=@(@('R1',7.9GB),@('R1',8GB),@('R1',9GB),@('R1',2.9GB),@('R2',7.9GB),@('X1',7.9GB),@('R2',2.9GB),@('X1',2.9GB))
$out=@($cases|ForEach-Object{[ordered]@{mode=$_[0];free=[double]$_[1];refusal=(Get-AdmissionSpaceRefusal $_[0] $_[1])}})
ConvertTo-Json -InputObject $out -Compress
"""


def owner_disk_check():
    print('--- the owner script: disk check before R1 (protocol section 3)')
    path = SRC / 'MATCHED_OWNER_RUN.ps1'; text = path.read_text(encoding='utf-8')
    r = subprocess.run([PS_EXE, '-NoProfile', '-NonInteractive', '-Command', SPACE_PROBE.replace('PATH_HERE', str(path))], capture_output=True, text=True, timeout=120)
    rows = {(x['mode'], x['free']): x['refusal'] for x in json.loads(r.stdout)}; GB = 2 ** 30
    check('R1 is refused at 7.9 GB free and admitted at 8 GB (PowerShell GB = 2^30 bytes)', (rows[('R1', 7.9 * GB)] or '').startswith('Run R1 requires at least 8 GB') and rows[('R1', 8 * GB)] is None and rows[('R1', 9 * GB)] is None,
          f"7.9 GB: {rows[('R1', 7.9 * GB)]!r}; 8 GB: {rows[('R1', 8 * GB)]!r}")
    check('R1 below 3 GiB gets the 8 GB refusal; R2 and X1 at 7.9 GB are admitted; below 3 GiB every run is refused',
          (rows[('R1', 2.9 * GB)] or '').startswith('Run R1') and rows[('R2', 7.9 * GB)] is None and rows[('X1', 7.9 * GB)] is None and rows[('R2', 2.9 * GB)] == rows[('X1', 2.9 * GB)] == 'Admission requires at least 3 GiB free on D:')
    call = '$spaceRefusal=Get-AdmissionSpaceRefusal $mode ((Get-PSDrive D).Free)'
    check('the script calls the check with D:\'s free space, before its claim and before the GPU check', text.count(call) == 1 and text.index(call) < text.index('WriteAllText($claim') and text.index(call) < text.index("Invoke-GpuCheck $gpu 'prestart'")
          and text.index('if ($spaceRefusal) {throw $spaceRefusal}') > text.index(call))


def main(n7, scratch):
    if str(scratch.resolve()).lower().startswith('d:'): raise SystemExit('The scratch folder must be outside D:')
    scratch.mkdir(parents=True, exist_ok=False)
    print(f'numpy {np.__version__}, python {sys.version.split()[0]}')
    byte_copies(n7); plan_checks(); data_checks(); registry_checks(scratch); worker_admission(); worker_counts(); worker_stage(scratch); worker_refusals(scratch); owner_script(scratch); owner_disk_check()
    print(f'{sum(results)} passed, {len(results) - sum(results)} failed')
    return 0 if all(results) else 1


if __name__ == '__main__':
    if len(sys.argv) != 3: raise SystemExit(__doc__)
    raise SystemExit(main(Path(sys.argv[1]), Path(sys.argv[2])))
