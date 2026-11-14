"""Native tests of N8's fresh-pool count, activation builder and pilot, and of the worker end to end (Windows Python 3.12, -I -B; NumPy).
No WSL, PyTorch, CUDA, GPU or seed draw of the study, and nothing under any work/runs folder is opened.

    python -I -B test_tools.py <SCRATCH_DIR outside D:>

- A synthetic corpus with the sealed manifest schema (the acquisition pins patched in this process, as N7's suite did; N patched to 256
  for N8, 64 for N6 and N7, N5's fill to 128), on which N5's, N6's and N7's partitions are re-derived from the real registries' seeds.
- The count, on that corpus, against an independent recount; its refusals.
- A fixture N8 registry, drawn by the sealed draw in fixture mode (a fixture policy, deterministic entropy, empty census roots).
- The builder: R1 and X1 activations built in fixture mode and admitted by the worker's own authorization; its refusals.
- The worker end to end on N7's NumPy doubles (the closed record's reports/): R1 with n02 made to fail in 768's arm, after its
  pre-training; X1 built on R1's terminal and run. Terminals, receipts, orders, kept states and the retry's E0 comparison are checked.
- The pilot on the doubles at small shapes: the log written first and kept, the run folder deleted, the seeds found by the registry's
  census, and a failing pilot that still keeps its seeds; its refusals.
What this cannot show: anything on real PyTorch and CUDA (the pilot is for that), and the count and partition on the real manifest.
"""
import hashlib, json, os, random, shutil, sys, threading, time
from pathlib import Path
from unittest.mock import patch

import numpy as np

HERE = Path(__file__).resolve().parent; STUDY = HERE.parent; SRC = STUDY / 'source'; TOOLS = STUDY / 'tools'
sys.path.insert(0, str(SRC)); sys.path.insert(1, str(SRC / 'vendor')); sys.path.insert(2, str(TOOLS))
import acquire_plan as ap, fewepoch_data, fewepoch_plan as fp, peak_data, n7_matched_data, text_plan as plan, text_worker as worker, wt103_corpus as wc
import matched_plan as mp, matched_data as md, matched_registry as mr, matched_worker as mw
import count_fresh_pool as cfp, build_n8_activation as bna, n8_pilot as pilot
CLOSED = Path(r'D:\sequence-weighting-research')
sys.path.insert(3, str(CLOSED / 'reports/natural-text-fewepoch-runa-package-20261102-02'))
import native_doubles as nd                                   # N7's NumPy doubles: never imported by source

sha = lambda b: hashlib.sha256(b).hexdigest()
shaf = lambda p: sha(Path(p).read_bytes())
results = []
N8_N = 256                                                    # dense readouts need N / 16 updates per epoch to be a multiple of 16


def check(name, ok, detail=''):
    results.append(bool(ok)); print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f'  [{detail}]' if detail else ''))


def refuses(fn, kind, text):
    try: fn()
    except kind as e: return text in str(e), str(e)[:140]
    except BaseException as e: return False, f'{type(e).__name__}: {str(e)[:140]}'
    return False, 'no refusal'


def entropy_for(label):
    def entropy(n):
        out, k = b'', 0
        while len(out) < n: out += hashlib.sha256(f'{label}:{k}'.encode()).digest(); k += 1
        return out[:n]
    return entropy


# ------------------------------------------------------------------ the synthetic corpus and the earlier partitions
def make_corpus(target, eligible=4200, lo=1, hi=5, copies=40):
    """The sealed manifest schema: 600 excluded one-sequence articles shuffled among `eligible` articles of lo..hi sequences, of which `copies`
    pairs share a full text. Tokens come from fixed generators. Returns (manifest, digest, acquisition pins)."""
    rng = random.Random('n8-fixture-corpus'); npr = np.random.default_rng(list(b'n8-fixture-tokens')); target.mkdir(parents=True); tok = b'{"fixture tokenizer": true}\n'; (target / 'tokenizer.json').write_bytes(tok)
    kinds = ['x'] * ap.WT2_TRAIN_ARTICLES + ['e'] * eligible; rng.shuffle(kinds); rows, first, found = [], 0, {}
    for i, kind in enumerate(kinds):
        s = 1 if kind == 'x' else rng.randint(lo, hi); rows.append(dict(index=i, first=first, sequences=s, tokens=s * plan.SEQ_TOKENS, title_sha256=sha(f'title-{i}'.encode()), text_sha256=sha(f'text-{i}'.encode()))); first += s
        if kind == 'x': found[str(len(found))] = i
    elig = [r for r, k in zip(rows, kinds) if k == 'e']; rng.shuffle(elig)
    for a, b in zip(elig[:copies], elig[copies:2 * copies]): b['text_sha256'] = a['text_sha256']
    def split(name, n):
        raw = npr.integers(0, plan.VOCAB, size=(n, plan.SEQ_TOKENS), dtype='<u2').tobytes(); (target / f'{name}.u16').write_bytes(raw); return raw
    tr, va, te = split('train', first), split('validation', 600), split('test', 2400); block = lambda n: [dict(index=k, first=k * 60, sequences=60, tokens=60 * plan.SEQ_TOKENS) for k in range(n // 60)]
    wt2 = sha(b'fixture natural-text manifest'); ex = sorted(found.values())
    manifest = dict(schema=3, kind=wc.KIND, seq_tokens=plan.SEQ_TOKENS, vocab=plan.VOCAB, approval_id='FIXTURE-N8-CORPUS', fixture=False, source_subject_sha256=fp.ACQUISITION_SUBJECT,
                    tokenizer=dict(file='tokenizer.json', sha256=sha(tok), library_version=plan.TOKENIZER['library_version'], settings=plan.TOKENIZER, source=dict(corpus=ap.WT2_CORPUS, manifest_sha256=wt2), retrained=False),
                    sources=dict(dataset=ap.DATASET, config=ap.CONFIG, revision=ap.REVISION), code_sha256={f: shaf(SRC / f) for f in wc.CODE_FILES},
                    splits=dict(train=dict(file='train.u16', bytes=len(tr), sha256=sha(tr), articles=rows, sequences=first), validation=dict(file='validation.u16', bytes=len(va), sha256=sha(va), articles=block(600), sequences=600),
                                test=dict(file='test.u16', bytes=len(te), sha256=sha(te), articles=block(2400), sequences=2400)),
                    wikitext2=dict(train_articles=ap.WT2_TRAIN_ARTICLES, train_articles_found_by_text=ap.WT2_TRAIN_ARTICLES, found_at=found),
                    exclusions=dict(rule='fixture', articles=ex, reasons={str(i): ['wikitext2_train_text'] for i in ex}, count=len(ex)), checks=dict(eligible_articles=eligible), interrupted_attempt_kept=None)
    raw = (json.dumps(manifest, sort_keys=True, indent=1) + '\n').encode('utf-8'); (target / 'CORPUS_MANIFEST.json').write_bytes(raw)
    return manifest, sha(raw), dict(WT2_MANIFEST_SHA256=wt2, TOKENIZER_SHA256=sha(tok), WT2_SPLIT_SHA256=dict(validation=sha(va), test=sha(te)))


class Fixture:
    """The patches every fixture call runs under: N, the acquisition pins, and (once drawn) the fixture policy."""
    def __init__(self, ap_pins, policy=None, n7_n=64): self.ap_pins, self.policy, self.n7_n = ap_pins, policy, n7_n
    def __enter__(self):
        self.ps = [patch.object(md, 'N_TRAIN', N8_N), patch.object(n7_matched_data, 'N_TRAIN', self.n7_n), patch.object(peak_data, 'N_TRAIN', 64), patch.object(fp, 'N_FILL', 128)]
        self.ps += [patch.object(ap, k, v) for k, v in self.ap_pins.items()]
        if self.policy: self.ps.append(patch.object(mr, 'POLICY_SHA256', self.policy))
        for p in self.ps: p.start()
        return self
    def __exit__(self, *a):
        for p in self.ps: p.stop()


def registries():
    out = {}
    for key, d in (('few', fp.REGISTRY['directory']), ('peak', mp.PEAK_REGISTRY['directory']), ('n7', mp.N7_REGISTRY['directory'])):
        out[key] = json.loads((CLOSED / d / 'REGISTRY.json').read_bytes())
    return out


def earlier_partitions(man, regs):
    few = fewepoch_data.partition(man, regs['few']['partition_seed']); n5 = {a for g in few['groups'].values() for a in g['articles']}
    peak = peak_data.partition(man, n5, regs['peak']['partition_seed']); n6 = {a for g in peak['groups'].values() for a in g['articles']}
    n7 = n7_matched_data.partition(man, n5 | n6, regs['n7']['partition_seed']); n7a = {a for g in n7['groups'].values() for a in g['articles']}
    pins = dict(few=sha(peak_data.encoded(few)), peak=sha(peak_data.encoded(peak)), n7=sha(n7_matched_data.encoded(n7)))
    return pins, n5, n6, n7a


# ------------------------------------------------------------------ the count
def count_checks(scratch, man, digest, fix):
    print('--- the fresh-pool count (step 3), on the synthetic corpus')
    regs = registries(); seeds = {k: v['partition_seed'] for k, v in regs.items()}
    with Fixture(fix):
        pins, n5, n6, n7a = earlier_partitions(man, regs)
        n7_pool = peak_data.fresh_pool(man, n5 | n6); recorded = cfp.pool_record(n7_pool)
        got = cfp.count(man, seeds, pins, recorded); direct = peak_data.fresh_pool(man, n5 | n6 | n7a)
        rows = {a['index']: a for a in man['splits']['train']['articles']}; largest = max(rows[i]['sequences'] for i in direct['articles'])
        bound = 24 * N8_N + 24 * (largest - 1)
        check('the count equals an independent recount of the pool less N5\'s, N6\'s and N7\'s articles and their text copies', got['n8_fresh_pool'] == cfp.pool_record(direct) and got['assigned_articles'] == dict(n5_and_n6=len(n5 | n6), n7=len(n7a), all=len(n5 | n6 | n7a)),
              f"{direct['fresh_articles']} articles, {direct['fresh_sequences']} sequences; removed {direct['removed_text_duplicates_of_assigned']} copies of assigned, {direct['removed_repeats_inside_the_pool']} repeats")
        check('feasibility whatever the shuffle: 24 x N + 24 x (largest article - 1)', got['sequences_needed_whatever_the_shuffle'] == bound and got['fits_whatever_the_shuffle'] == (direct['fresh_sequences'] >= bound) and got['largest_fresh_article_sequences'] == largest,
              f"needs {bound}, has {direct['fresh_sequences']}: fits {got['fits_whatever_the_shuffle']}")
        check("N7's pool recount matches its record, and N8's pool is N7's less N7's articles", got['n7_pool_matches_its_registry'] and got['n8_pool_is_n7_pool_less_n7_articles'])
        check("a record that differs from the recount is reported", cfp.count(man, seeds, pins, dict(recorded, fresh_sequences=recorded['fresh_sequences'] + 1))['n7_pool_matches_its_registry'] is False)
    ok, why = refuses(lambda: cfp.main(scratch / 'corpus' / 'CORPUS_MANIFEST.json', scratch / 'count-out'), SystemExit, 'differs from its pin')
    check('the command line refuses any manifest other than the pinned one, and writes nothing', ok and not (scratch / 'count-out').exists(), why)
    (scratch / 'count-exists').mkdir(); ok, why = refuses(lambda: cfp.main(scratch / 'corpus' / 'CORPUS_MANIFEST.json', scratch / 'count-exists'), SystemExit, 'output folder exists')
    check('it refuses an existing output folder before reading anything', ok, why)


# ------------------------------------------------------------------ the fixture registry
def draw_registry(scratch, man, digest, fix):
    reg_dir = scratch / 'registry'; reg_dir.mkdir(); policy = b'fixture N8 seed policy\n'; (reg_dir / 'SEED_REGISTRY_POLICY.md').write_bytes(policy)
    empty_root, empty_study = scratch / 'census-root-draw', scratch / 'census-study-draw'; empty_root.mkdir(); empty_study.mkdir(); regs = registries()
    with Fixture(fix):
        pins_e, n5, n6, n7a = earlier_partitions(man, regs)
        reg, _ = mr.draw(reg_dir, scratch / 'corpus' / 'CORPUS_MANIFEST.json', 'FIXTURE-N8-REG', entropy=entropy_for('n8-fixture-registry'), root=empty_root, fixture=True, policy_sha256=sha(policy),
                         manifest_sha256=digest, fewepoch_partition_sha256=pins_e['few'], peak_partition_sha256=pins_e['peak'], n7_partition_sha256=pins_e['n7'], study=empty_study)
    pins = dict(registry_sha256=shaf(reg_dir / 'REGISTRY.json'), exclusions_sha256=shaf(reg_dir / 'EXCLUSIONS.json'), draw_sha256=shaf(reg_dir / 'DRAW.json'), corpus_manifest_sha256=digest, partition_sha256=shaf(reg_dir / 'PARTITION.json'),
                fewepoch_registry_sha256=fp.REGISTRY['registry_sha256'], fewepoch_partition_sha256=pins_e['few'], peak_registry_sha256=mp.PEAK_REGISTRY['registry_sha256'], peak_partition_sha256=pins_e['peak'],
                n7_registry_sha256=mp.N7_REGISTRY['registry_sha256'], n7_partition_sha256=pins_e['n7'])
    print(f"--- fixture registry drawn: {len(reg['groups'])} groups, partition {pins['partition_sha256'][:16]}")
    return reg_dir, pins, sha(policy)


def inputs_for(reg_dir, corpus, first_attempt=None):
    return dict(registry=reg_dir, corpus=corpus, fewepoch_registry=CLOSED / fp.REGISTRY['directory'] / 'REGISTRY.json', peak_registry=CLOSED / mp.PEAK_REGISTRY['directory'] / 'REGISTRY.json',
                n7_registry=CLOSED / mp.N7_REGISTRY['directory'] / 'REGISTRY.json', first_attempt=first_attempt)


# ------------------------------------------------------------------ the worker on the doubles
def gpu_row(verdict='IDLE'): return dict(started_utc='fixture', context='boundary', utilization_mean_max_percent=1.0, memory_used_max_mib=None, samples=[dict(utc='fixture', memory_used_mib=600, memory_total_mib=4096, utilization_percent=0.0)],
                                         failed_samples=0, mean_utilization_percent=0.0, max_memory_used_mib=600, verdict=verdict, gpu_verdict=verdict, power=dict(utc='fixture', power='AC', battery_percent=80.0, scheme_guid=None, scheme_name='Turbo', error=None))


def write_verdict(act, stage, name=None):
    d = act / 'gpu-checks'; d.mkdir(parents=True, exist_ok=True); p = d / (name or f'{stage}-RESPONSE.json'); tmp = p.with_name(p.name + '.part')
    tmp.write_bytes(json.dumps(dict(schema=1, stage=stage, verdict='IDLE', checks=[gpu_row()])).encode()); os.replace(tmp, p)


def unix_resource(rss_bytes=300 * 2 ** 20):
    """A stand-in for the Unix-only resource module, which the guard's default memory reader imports; Windows has none. It reports a fixed
    peak RSS, so the guard's own limit check still runs."""
    m = __import__('types').ModuleType('resource'); m.RUSAGE_SELF = 0
    m.getrusage = lambda who: __import__('types').SimpleNamespace(ru_maxrss=rss_bytes // 1024)
    return patch.dict(sys.modules, {'resource': m})


def run_mode(act, out_root, corpus, pins, policy, fix, fail_stage=None):
    """matched_worker.run() on the doubles, with an owner-side responder for the GPU gates. fail_stage: 768's arm raises in that draw, after its pre-training."""
    write_verdict(act, 'PRESTART', 'PRESTART.json'); stop = threading.Event(); seen = set()
    def respond():
        while not stop.is_set():
            d = out_root / 'gpu-checks'
            for p in (sorted(d.glob('*-REQUEST.json')) if d.exists() else []):
                s = p.name[:-len('-REQUEST.json')]
                if s not in seen: seen.add(s); write_verdict(act, s)
            time.sleep(0.005)
    original = mw.Context.adapt_readouts
    def adapt(self, stage, width, *a, **k):
        if stage == fail_stage and width == 768: raise RuntimeError(f'fixture failure in {stage}, width 768')
        return original(self, stage, width, *a, **k)
    thread = threading.Thread(target=respond, daemon=True); thread.start(); err = None
    try:
        with Fixture(fix, policy), unix_resource(), patch.object(worker, 'GATE_POLL_SECONDS', 0.01), patch.object(mw.Context, 'adapt_readouts', adapt):
            code = mw.run(dependencies=nd.deps(nd.FakeCuda(), nd.text_engine_fake()), here=act, out_root=out_root, corpus_dir=corpus, pins=pins)
    except Exception as e: code, err = None, e
    finally: stop.set(); thread.join()
    return code, err, json.loads((out_root / 'TERMINAL.json').read_bytes())


def draw_files_ok(run, d):
    s = run / d; inputs = json.loads((s / 'INPUTS.json').read_bytes()); raw = (s / mp.ORDER_FILE).read_bytes(); size = 8 * N8_N
    rows = [np.frombuffer(raw[e * size:(e + 1) * size], dtype='<i8') for e in range(mp.ORDER_EPOCHS)]
    kept = json.loads((s / 'STATES_KEPT.json').read_bytes())
    return (inputs['epoch_order_sha256'] == [pilot_order_sha(r) for r in rows] and all(sorted(r.tolist()) == list(range(N8_N)) for r in rows)
            and sorted(x['path'] for x in kept['kept']) == [f'{d}/w512/E0.pt', f'{d}/w768/E0.pt'] and all((run / x['path']).is_file() for x in kept['kept'])
            and all(len(json.loads((s / f'w{w}/{mp.TAG}/record.json').read_bytes())['readouts']) == 28 for w in mp.WIDTHS))


def pilot_order_sha(row):
    sys.path.insert(0, str(STUDY / 'analysis')); import n8_analysis
    return n8_analysis.order_sha256(row)


def admit(act, corpus, pins, policy, fix):
    """The worker's own admission of an activation: its draws, or the refusal's text."""
    try:
        with Fixture(fix, policy): return mw.authorization(act, corpus, pins)[4]
    except PermissionError as e: return f'refused: {e}'


def builder_and_worker(scratch, man, digest, fix):
    print('--- the builder and the worker on the doubles')
    reg_dir, pins, policy = draw_registry(scratch, man, digest, fix); corpus = scratch / 'corpus'; subject = shaf(SRC / 'SOURCE_SUBJECT.json')
    acts, runs = scratch / 'activations', scratch / 'runs'; acts.mkdir(); runs.mkdir()
    with Fixture(fix, policy): r1 = bna.build('R1', acts / 'n8-r1', 'FIXTURE-N8-R1', 'fixture approval text', True, subject, source=SRC, pins=pins, inputs=inputs_for(reg_dir, corpus))
    auth = json.loads((acts / 'n8-r1' / 'AUTHORIZATION.json').read_bytes())
    admitted = admit(acts / 'n8-r1', corpus, pins, policy, fix)
    check('R1 built in fixture mode, and admitted by the worker with its three draws', r1['status'] == 'ARMED_UNUSED' and auth['stages'] == ['n01', 'n02', 'n03'] == admitted and auth['n7_registry_sha256'] == mp.N7_REGISTRY['registry_sha256'],
          f"{r1['stages']}; approval {r1['approval_record_sha256'][:16]}")
    code, err, term = run_mode(acts / 'n8-r1', runs / 'n8-r1', corpus, pins, policy, fix, fail_stage='n02')
    on_fail = term.get('states_on_failure', {}).get('kept_in_active_stage') or {}
    check('R1 on the doubles: n01 completes, n02 fails in 768\'s arm, the terminal is FAILED and keeps n02\'s 768 E0 state', isinstance(err, RuntimeError) and term['status'] == 'FAILED' and mw.completed_draws(term) == ['n01'] and term['draws'] == ['n01', 'n02', 'n03']
          and [x['path'] for x in on_fail.get('kept', [])] == ['n02/w768/E0.pt'] and term['kind'] == 'n8', f"{term['status']}: {term.get('error', {}).get('message')}")
    check("n01's files: orders with n8_analysis's hashes, both E0 states kept, 28 readouts per arm", draw_files_ok(runs / 'n8-r1', 'n01'))
    with Fixture(fix, policy): x1 = bna.build('X1', acts / 'n8-x1', 'FIXTURE-N8-X1', 'fixture approval text', True, subject, source=SRC, pins=pins, inputs=inputs_for(reg_dir, corpus, runs / 'n8-r1'))
    admitted = admit(acts / 'n8-x1', corpus, pins, policy, fix)
    check("X1 built on R1's terminal, for n02 and n03 only, and admitted by the worker", x1['stages'] == ['n02', 'n03'] == admitted and json.loads((acts / 'n8-x1' / 'AUTHORIZATION.json').read_bytes())['first_attempt_terminal_sha256'] == shaf(runs / 'n8-r1' / 'TERMINAL.json'))
    code, err, term = run_mode(acts / 'n8-x1', runs / 'n8-x1', corpus, pins, policy, fix)
    rec = {s['stage']: s['e0_against_first_attempt'] for s in term['stages']}
    check("X1 on the doubles completes n02 and n03; each receipt compares the new E0 losses with R1's", code == 0 and err is None and term['status'] == 'COMPLETE' and term['draws'] == ['n02', 'n03']
          and rec == {'n02': {'768': 'SAME', '512': 'ABSENT'}, 'n03': {'768': 'ABSENT', '512': 'ABSENT'}}, str(rec))
    check("X1's draws: orders with n8_analysis's hashes, both E0 states kept, 28 readouts per arm", draw_files_ok(runs / 'n8-x1', 'n02') and draw_files_ok(runs / 'n8-x1', 'n03'))
    print('--- the builder: refusals')
    with Fixture(fix, policy):
        for name, fn, text in (('a FIXTURE id in real mode', lambda: bna.build('R1', bna.TARGETS['R1'], 'FIXTURE-X', 't', False, subject), 'real approval'),
                               ('an unpinned builder', lambda: bna.build('R2', scratch / 'a2', 'FIXTURE-X', 't', True, None, pins=pins, inputs=inputs_for(reg_dir, corpus)), 'not pinned'),
                               ('a fixture target inside the study folder', lambda: bna.build('R2', bna.STUDY / 'activations-fixture', 'FIXTURE-X', 't', True, subject, source=SRC, pins=pins, inputs=inputs_for(reg_dir, corpus)), 'outside the study folder'),
                               ('an existing activation', lambda: bna.build('R1', acts / 'n8-r1', 'FIXTURE-X', 't', True, subject, source=SRC, pins=pins, inputs=inputs_for(reg_dir, corpus)), 'exists'),
                               ("a terminal that is not R1's (X1's own, complete)", lambda: bna.build('X1', scratch / 'x1b', 'FIXTURE-X', 't', True, subject, source=SRC, pins=pins, inputs=inputs_for(reg_dir, corpus, runs / 'n8-x1')), 'does not admit'),
                               ('a mode outside R1-R8 and X1-X8', lambda: bna.build('M1', scratch / 'm1', 'FIXTURE-X', 't', True, subject, pins=pins, inputs=inputs_for(reg_dir, corpus)), 'R1-R8 or X1-X8')):
            ok, why = refuses(fn, SystemExit, text); check(f'refuses {name}', ok, why)
        fake = scratch / 'r1-copy'; shutil.copytree(runs / 'n8-r1', fake, ignore=shutil.ignore_patterns('*.pt', '*.f32', 'cache')); (fake / 'n01-RECEIPT.json').unlink()
        ok, why = refuses(lambda: bna.build('X1', scratch / 'x1c', 'FIXTURE-X', 't', True, subject, source=SRC, pins=pins, inputs=inputs_for(reg_dir, corpus, fake)), SystemExit, 'receipts differ')
        check("refuses a first attempt whose receipts differ from its terminal", ok, why)
    good = scratch / 'PILOT_LOG.json'; good.write_bytes(json.dumps(dict(status='PASS', fixture=False, approval_id='pilot-00000000-00')).encode())
    ok1 = bna.pilot_log(good, dict(pilot_log_sha256=shaf(good))) == shaf(good)
    ok2, why = refuses(lambda: bna.pilot_log(good, dict(pilot_log_sha256='0' * 64)), SystemExit, 'does not name')
    bad = scratch / 'PILOT_FAIL.json'; bad.write_bytes(json.dumps(dict(status='FAIL', fixture=False, approval_id='pilot-00000000-00')).encode()); ok3, _ = refuses(lambda: bna.pilot_log(bad, dict(pilot_log_sha256=shaf(bad))), SystemExit, 'did not pass')
    fixture_log = scratch / 'PILOT_FIXTURE.json'; fixture_log.write_bytes(json.dumps(dict(status='PASS', fixture=True, approval_id='FIXTURE-PILOT')).encode()); ok4, _ = refuses(lambda: bna.pilot_log(fixture_log, dict(pilot_log_sha256=shaf(fixture_log))), SystemExit, 'not real')
    check("real mode needs a PASS, non-fixture pilot log (a pilot-YYYYMMDD-NN id) named by the public registration", ok1 and ok2 and ok3 and ok4, why)


# ------------------------------------------------------------------ the pilot on the doubles: N7's fixture m01 on the synthetic corpus
SEEDS = dict(init_seed=11, weight_seed=22, pretrain_order_seed=33, adapt_order_seed=44, benchmark_seed=55)      # fixture values for the doubles only


def pilot_fixture(scratch, man, digest, fix):
    """N7's fixture partition at N = 256 on the synthetic corpus, with the pilot's inputs and pins."""
    regs = registries()
    with Fixture(fix, n7_n=N8_N):
        pins_e, n5, n6, n7a = earlier_partitions(man, regs)
        n7 = n7_matched_data.partition(man, n5 | n6, regs['n7']['partition_seed']); pool = peak_data.fresh_pool(man, n5 | n6 | n7a)
    d = scratch / 'n7-registry-fixture'; d.mkdir(); raw = n7_matched_data.encoded(n7); (d / 'PARTITION.json').write_bytes(raw)
    pins = dict(corpus_manifest_sha256=digest, fewepoch_registry_sha256=fp.REGISTRY['registry_sha256'], peak_registry_sha256=mp.PEAK_REGISTRY['registry_sha256'], n7_registry_sha256=mp.N7_REGISTRY['registry_sha256'],
                fewepoch_partition_sha256=pins_e['few'], peak_partition_sha256=pins_e['peak'], n7_partition_sha256=sha(raw))
    inputs = dict(corpus=scratch / 'corpus', n7_partition=d / 'PARTITION.json', **{k: v for k, v in inputs_for(None, None).items() if k.endswith('_registry')})
    return n7, pool, n5 | n6 | n7a, inputs, pins


def pilot_checks(scratch, man, digest, fix):
    n7, pool, assigned, inputs, pins = pilot_fixture(scratch, man, digest, fix)
    with unix_resource(), Fixture(fix, n7_n=N8_N): pilot_checks_(scratch, man, n7, pool, assigned, inputs, pins)


def pilot_checks_(scratch, man, n7, pool, assigned, inputs, pins):
    print("--- the pilot on the doubles: N7's m01 (fixture, N = 256) through the worker's corpus loader")
    subject = shaf(SRC / 'SOURCE_SUBJECT.json'); study = scratch / 'pilot-study'; study.mkdir(); said = []
    deps = lambda **k: nd.deps(nd.FakeCuda(**k), nd.text_engine_fake())
    code = pilot.run_pilot('FIXTURE-PILOT-01', subject, SEEDS, dependencies=deps(), study=study, inputs=inputs, pins=pins, out=said.append)
    log = json.loads((study / 'pilot' / 'PILOT_LOG.json').read_bytes()); t = log.get('stage', {}).get('timing', {}); data = log.get('data', {})
    check('the pilot passes on the doubles: stage complete, every check held', code == 0 and log['status'] == 'PASS' and not log['stage']['problems'] and log['stage']['checks']['orders_written_with_hashes'] and log['stage']['checks']['e0_states_kept'],
          said[-1][:100] if said else '')
    check("the draw is N7's m01: every sequence in its articles, none in N8's pool, and the stage's INPUTS.json names it", data.get('status') == 'PASS' and data['sequences'] == data['distinct_sequences'] == N8_N and data['all_in_m01_articles']
          and data['sequences_in_n8_fresh_pool'] == 0 == data['articles_in_n8_fresh_pool'] and log['stage']['checks']['inputs_name_the_draw'] and log['shapes'] == dict(n=N8_N, validation=512, pool=2048),
          f"{data.get('articles')} articles; shapes {log.get('shapes')}; corpus read by the worker's loader")
    good = n7['groups']['m01']; seqs = list(good['sequences']); rows = {a['index']: a for a in man['splits']['train']['articles']}
    pool_seq = rows[pool['articles'][0]]['first']; other = n7['groups']['m02']['sequences'][0]
    for name, s, field in (("a sequence from N8's fresh pool", [pool_seq] + seqs[1:], 'sequences_in_n8_fresh_pool'), ("a sequence from N7's m02", [other] + seqs[1:], 'all_in_m01_articles'), ('a repeated sequence', [seqs[1]] + seqs[1:], 'distinct_sequences')):
        r = pilot.draw_record(man, good['articles'], s, assigned, pool, N8_N)
        check(f'the draw check fails on {name}', r['status'] == 'FAIL' and (r[field] if field == 'sequences_in_n8_fresh_pool' else not r[field] if field == 'all_in_m01_articles' else r[field] < N8_N), f"{field} = {r[field]}")
    check('the draw check passes on the draw itself', pilot.draw_record(man, good['articles'], seqs, assigned, pool, N8_N)['status'] == 'PASS')
    claimed = dict(pool, articles=list(pool['articles']) + [good['articles'][0]]); r = pilot.draw_record(man, good['articles'], seqs, assigned, claimed, N8_N)
    check("the draw check fails if N8's pool held an m01 article, though every sequence lies in m01", r['status'] == 'FAIL' and r['all_in_m01_articles'] and r['sequences_in_n8_fresh_pool'] > 0 and r['articles_in_n8_fresh_pool'] == 1,
          f"{r['sequences_in_n8_fresh_pool']} sequences, {r['articles_in_n8_fresh_pool']} article in the pool")
    fake = scratch / 'stage-check' / pilot.STAGE; fake.mkdir(parents=True); (fake / 'INPUTS.json').write_text(json.dumps(dict(articles=good['articles'][1:], sequence_indices_sha256='0' * 64)), encoding='utf-8')
    detail, problems = pilot.check_stage(scratch / 'stage-check', dict(n=N8_N, validation=512, pool=2048), {}, dict(n=N8_N, groups={pilot.STAGE: dict(articles=good['articles'], sequences=seqs)}))
    check("the stage check reports an INPUTS.json that names other articles or sequences", detail['inputs_name_the_draw'] is False and any('does not name' in str(p) for p in problems))
    check('timing per width: pre-training, and the arm split into training and evaluation (28 evaluations per arm)', sorted(t) == ['w512/lr1e-04', 'w512/pretraining and E0', 'w768/lr1e-04', 'w768/pretraining and E0']
          and all(t[f'w{w}/lr1e-04']['evaluations'] == 56 and abs(t[f'w{w}/lr1e-04']['training_seconds'] + t[f'w{w}/lr1e-04']['evaluation_seconds'] - t[f'w{w}/lr1e-04']['total_seconds']) < 1e-9 for w in mp.WIDTHS),
          f"evaluations per arm {[t[f'w{w}/lr1e-04']['evaluations'] for w in mp.WIDTHS]} (28 readouts x training and validation)")
    run = log.get('run_of_three_draws', {})
    check('peak memory per phase, the benchmark, and a run of three draws against the 6-hour cap are logged', all('peak_allocated_bytes' in v for v in t.values()) and log['benchmark']['decision'] == 'GO'
          and log['cap_of_a_run_of_three_draws']['stages'] == 3 and run.get('draws') == 3 and run['fits'] == log['three_draws_fit_a_run'] == (run['feasible_by_formula'] and run['measured_stage_within_cap'])
          and abs(run['projected_run_seconds'] - (run['benchmark_seconds'] + 3 * run['projected_stage_seconds'])) < 1e-9 and abs(run['measured_run_seconds'] - (run['benchmark_seconds'] + 3 * run['measured_stage_seconds'])) < 1e-9,
          f"projected run {run.get('projected_run_seconds', 0):.1f} s, from this draw {run.get('measured_run_seconds', 0):.1f} s (doubles), cap {run.get('stage_cap_seconds')} s per draw")
    names = {x['path'] for x in log['files_before_deletion']}
    check('the run folder is deleted; the log lists every file before deletion with its hash', log['run_folder_deleted'] and not (study / 'pilot' / 'run').exists() and sorted(p.name for p in (study / 'pilot').iterdir()) == ['PILOT_LOG.json']
          and {'pilot/ORDERS.i64', 'pilot/w768/E0.pt', 'pilot/w512/lr1e-04/arrays.f32'} <= names, f'{len(names)} files')
    check('the log records no loss and no p*', log['loss_read'] is False and log['p_star_fitted'] is False and 'loss' not in json.dumps(log.get('stage', {}).get('checks', {})).replace('loss_read', ''))
    excluded, _ = mr.exclusions(scratch / 'census-root', (), study)
    check("the registry's census finds all five pilot seeds in the log (protocol section 4)", set(SEEDS.values()) <= set(excluded))
    study2 = scratch / 'pilot-study-2'; study2.mkdir(); said = []
    code = pilot.run_pilot('FIXTURE-PILOT-02', subject, dict(SEEDS, init_seed=12), dependencies=deps(mem={768: 3 * 2 ** 30}), study=study2, inputs=inputs, pins=pins, out=said.append)
    log2 = json.loads((study2 / 'pilot' / 'PILOT_LOG.json').read_bytes())
    check('a pilot stopped by the start-up rule fails, deletes its run folder and keeps its seeds', code == 1 and log2['status'] == 'FAIL' and log2['benchmark']['decision'] == 'STOP' and log2['run_folder_deleted'] and log2['seeds']['init_seed'] == 12, log2['benchmark']['reason'])
    doctored = scratch / 'n7-doctored'; doctored.mkdir(); part = json.loads(Path(inputs['n7_partition']).read_bytes()); part['groups']['m01']['sequences'][0] = pool_seq
    (doctored / 'PARTITION.json').write_bytes(n7_matched_data.encoded(part)); study3 = scratch / 'pilot-study-3'; study3.mkdir(); said = []
    code = pilot.run_pilot('FIXTURE-PILOT-03', subject, dict(SEEDS, init_seed=13), dependencies=deps(), study=study3, inputs=dict(inputs, n7_partition=doctored / 'PARTITION.json'), pins=pins, out=said.append)
    log3 = json.loads((study3 / 'pilot' / 'PILOT_LOG.json').read_bytes())
    check("a changed N7 PARTITION.json is refused before any training, and the seeds are kept", code == 1 and log3['status'] == 'FAIL' and 'differs from its pin' in log3['error']['message'] and 'benchmark' not in log3 and not (study3 / 'pilot' / 'run').exists() and log3['seeds']['init_seed'] == 13, log3['error']['message'])
    for name, fn, text in (('a FIXTURE id on the real path', lambda: pilot.run_pilot('FIXTURE-X', subject, SEEDS, study=scratch / 'p3'), 'pilot-YYYYMMDD-NN'),
                           ('an approval id of another form on the real path', lambda: pilot.run_pilot('OWNER-00000000-X', subject, SEEDS, study=scratch / 'p3'), 'pilot-YYYYMMDD-NN'),
                           ('a well-formed id outside Linux', lambda: pilot.run_pilot('pilot-00000000-00', subject, SEEDS, study=scratch / 'p3'), 'Linux'),
                           ('test doubles without a FIXTURE id', lambda: pilot.run_pilot('NOT-A-FIXTURE', subject, SEEDS, dependencies=deps(), study=scratch / 'p3', inputs=inputs, pins=pins), 'need a FIXTURE id'),
                           ('test inputs without their pins', lambda: pilot.run_pilot('FIXTURE-X', subject, SEEDS, dependencies=deps(), study=scratch / 'p3', inputs=inputs), 'need their pins'),
                           ('repeated seeds', lambda: pilot.run_pilot('FIXTURE-X', subject, dict(SEEDS, weight_seed=11), dependencies=deps(), study=scratch / 'p3', inputs=inputs, pins=pins), 'five distinct'),
                           ('a missing seed', lambda: pilot.run_pilot('FIXTURE-X', subject, {k: v for k, v in SEEDS.items() if k != 'benchmark_seed'}, dependencies=deps(), study=scratch / 'p3', inputs=inputs, pins=pins), 'five distinct'),
                           ('another source subject', lambda: pilot.run_pilot('FIXTURE-X', '0' * 64, SEEDS, dependencies=deps(), study=scratch / 'p3', inputs=inputs, pins=pins), 'differs from the expected'),
                           ('an existing pilot folder', lambda: pilot.run_pilot('FIXTURE-X', subject, SEEDS, dependencies=deps(), study=study, inputs=inputs, pins=pins), 'runs once')):
        ok, why = refuses(fn, SystemExit, text); check(f'the pilot refuses {name}, writing nothing', ok and not (scratch / 'p3').exists(), why)


def main(scratch):
    if str(scratch.resolve()).lower().startswith('d:'): raise SystemExit('The scratch folder must be outside D:')
    scratch.mkdir(parents=True, exist_ok=False); (scratch / 'census-root').mkdir()
    print(f'numpy {np.__version__}, python {sys.version.split()[0]}; N8 source subject {shaf(SRC / "SOURCE_SUBJECT.json")[:16]}')
    man, digest, fix = make_corpus(scratch / 'corpus')
    count_checks(scratch, man, digest, fix); builder_and_worker(scratch, man, digest, fix); pilot_checks(scratch, man, digest, fix)
    print(f'{sum(results)} passed, {len(results) - sum(results)} failed')
    return 0 if all(results) else 1


if __name__ == '__main__':
    if len(sys.argv) != 2: raise SystemExit(__doc__)
    raise SystemExit(main(Path(sys.argv[1])))
