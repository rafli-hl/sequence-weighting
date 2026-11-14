"""The pilot of N8 (N8-protocol-draft.md, section 10.3; the brief's step 4): one draw, both widths, through the N8 worker's start-up
benchmark and stage on the real engine, timed and measured, then deleted except a JSON log. Derived from N7's engine_check.py (its smoke
part).

  python -I -B n8_pilot.py --approval-id pilot-YYYYMMDD-NN --expected-subject <SHA-256> --init-seed <int> --weight-seed <int>
                           --pretrain-order-seed <int> --adapt-order-seed <int> --benchmark-seed <int>

Run by the owner in WSL, on the GPU, after the owner's go, on AC power with the lid open and no other GPU work. The five seeds are the
owner's throwaway set.

The draw is N7's m01: its 16,384 training sequences, from N7's PARTITION.json (the closed record's reports/, against its pin), read from
the sealed corpus by the worker's own loader (worker.load_corpus, every corpus file against its manifest), with the validation set and the
pre-training pool every run uses. N8's partition excludes m01, so the pilot trains on no sequence N8 can draw. Before any training the
pilot checks that every one of its sequences lies in an article of N7's m01 and that none lies in N8's fresh pool, re-derived with
matched_data from the three earlier registries.

In order:
1. Refusals before anything is written: the N8 source differs from the expected subject; an N8 activation or run exists (the pilot comes
   before the builder); the pilot folder exists; the seeds are not five distinct integers in [0, 2^32); the approval id.
2. pilot/PILOT_LOG.json is written first, with the seeds under "seeds", so that the registry's census excludes them whatever happens next
   (section 4). It is rewritten at the end.
3. The draw's checks above; then the start-up benchmark (matched_worker.startup_benchmark, 768 then 512) and its rule, and the time cap of
   a run of three draws (matched_worker.study_cap), as a run computes them.
4. One stage (matched_worker.stage) with the real engine, model, guard and output ledger under the run's limits. Each width's
   pre-training and arm are timed, evaluations between CUDA synchronisations, so training time is the arm's time less its evaluations;
   peak GPU memory is recorded per phase.
5. What the stage wrote, checked by name, size and hash: per width E0.pt, E0.f32 and its arm's record and arrays with 28 readouts;
   ORDERS.i64, each row a permutation, with its per-epoch hashes in INPUTS.json; STATES_KEPT.json. No loss value is read and no p* is
   fitted: records are reduced to statuses, epochs, updates and whether a field holds a number.
6. A run of three draws against the 6-hour cap: the projected run time from the benchmark (as the run's own cap formula uses it) and from
   this draw's measured time, the cap per draw, and whether three draws fit.
7. The run folder (pilot/run) is deleted. PILOT_LOG.json keeps the timings, memory, the benchmark and cap, the checks, and the name, size
   and hash of every file before deletion. PASS means the draw checks held, the stage completed and every check of its files held;
   whether three draws fit a run is reported beside it.
The functions take injected test doubles, inputs and pins for the native tests; the real path needs Linux and binds the real inputs.
"""
import argparse, hashlib, json, re, platform, shutil, struct, sys, time, traceback
sys.dont_write_bytecode = True
from pathlib import Path

STUDY = Path(__file__).resolve().parents[1]
SRC = STUDY / 'source'
sys.path.insert(0, str(SRC)); sys.path.insert(1, str(SRC / 'vendor'))
import text_plan as plan, text_worker as worker, wt103_corpus as wc
import fewepoch_plan as fp, fewepoch_worker as fw, matched_data as md, matched_plan as mp, matched_worker as mw

STAGE = 'pilot'
SEED_KEYS = ('init_seed', 'weight_seed', 'pretrain_order_seed', 'adapt_order_seed', 'benchmark_seed')
APPROVAL_ID = re.compile(r'^pilot-[0-9]{8}-[0-9]{2}$')
REAL_PINS = dict(corpus_manifest_sha256=fp.CORPUS_MANIFEST_SHA256, fewepoch_registry_sha256=fp.REGISTRY['registry_sha256'], peak_registry_sha256=mp.PEAK_REGISTRY['registry_sha256'],
                 n7_registry_sha256=mp.N7_REGISTRY['registry_sha256'], fewepoch_partition_sha256=fp.PARTITION_SHA256, peak_partition_sha256=md.PEAK_PARTITION_SHA256, n7_partition_sha256=md.N7_PARTITION_SHA256)
REAL_INPUTS = dict(corpus=mw.CORPUS, fewepoch_registry=mw.ROOT / fp.REGISTRY['directory'] / 'REGISTRY.json', peak_registry=mw.ROOT / mp.PEAK_REGISTRY['directory'] / 'REGISTRY.json',
                   n7_registry=mw.ROOT / mp.N7_REGISTRY['directory'] / 'REGISTRY.json', n7_partition=mw.ROOT / mp.N7_REGISTRY['directory'] / 'PARTITION.json')
sha = lambda b: hashlib.sha256(b).hexdigest()
encoded = lambda x: (json.dumps(x, sort_keys=True, indent=1, allow_nan=False) + '\n').encode('utf-8')


# ------------------------------------------------------------------ refusals
def check_approval(approval_id, dependencies):
    if not approval_id or not approval_id.strip(): raise SystemExit('An approval id is required')
    fixture = str(approval_id).upper().startswith('FIXTURE')
    if dependencies is None:
        if fixture or not APPROVAL_ID.match(str(approval_id)): raise SystemExit('The real path needs the owner\'s pilot approval id (pilot-YYYYMMDD-NN)')
        if not sys.platform.startswith('linux'): raise SystemExit('The real path needs the existing Linux owner (WSL)')
    elif not fixture: raise SystemExit('Injected test doubles need a FIXTURE id')


def check_seeds(seeds):
    values = [seeds.get(k) for k in SEED_KEYS]
    if sorted(seeds) != sorted(SEED_KEYS) or any(type(v) is not int or not 0 <= v < 2 ** 32 for v in values) or len(set(values)) != len(values):
        raise SystemExit('The pilot needs five distinct integer seeds in [0, 2^32): ' + ', '.join(SEED_KEYS))
    return dict(seeds)


def verify_source(expected):
    raw = (SRC / 'SOURCE_SUBJECT.json').read_bytes()
    if sha(raw) != expected: raise SystemExit('The N8 source subject differs from the expected one')
    for row in json.loads(raw)['files']:
        b = (SRC / row['path']).read_bytes()
        if len(b) != row['bytes'] or sha(b) != row['sha256']: raise SystemExit('Changed source ' + row['path'])
    return sorted(p.relative_to(SRC).as_posix() for p in SRC.rglob('*') if p.is_file())


def study_paths_absent():
    return not any((mw.STUDY / p).exists() for p in list(mp.ACTIVATIONS.values()) + list(mp.RUNS.values()))


# ------------------------------------------------------------------ the draw: N7's m01
def pilot_data(inputs, pins):
    """N7's m01, read from the sealed corpus by the worker's loader. Returns (corpus, partition, record); the record's status is PASS only if
    every input equals its pin, the draw holds N distinct sequences, all inside m01's articles, and none inside N8's fresh pool."""
    corpus_dir = Path(inputs['corpus']); man_raw = (corpus_dir / 'CORPUS_MANIFEST.json').read_bytes()
    if sha(man_raw) != pins['corpus_manifest_sha256']: raise RuntimeError('The corpus manifest differs from its pin')
    manifest = json.loads(man_raw); wc.validate_manifest(manifest, {f: sha((SRC / f).read_bytes()) for f in wc.CODE_FILES})
    if manifest.get('source_subject_sha256') != fp.ACQUISITION_SUBJECT or manifest.get('fixture') is not False: raise RuntimeError("Not the approved acquisition's corpus")
    regs = {}
    for key in ('fewepoch', 'peak', 'n7'):
        raw = Path(inputs[f'{key}_registry']).read_bytes()
        if sha(raw) != pins[f'{key}_registry_sha256']: raise RuntimeError(f'The {key} registry differs from its pin')
        regs[key] = json.loads(raw)
    part_raw = Path(inputs['n7_partition']).read_bytes()
    if sha(part_raw) != pins['n7_partition_sha256']: raise RuntimeError("N7's PARTITION.json differs from its pin")
    m01 = json.loads(part_raw)['groups']['m01']; seqs, arts = m01['sequences'], m01['articles']
    assigned = md.assigned_articles(manifest, regs['fewepoch']['partition_seed'], regs['peak']['partition_seed'], regs['n7']['partition_seed'], pins['fewepoch_partition_sha256'], pins['peak_partition_sha256'], pins['n7_partition_sha256'])
    pool = md.fresh_pool(manifest, assigned)
    rec = dict(draw_record(manifest, arts, seqs, assigned, pool, md.N_TRAIN), corpus_manifest_sha256=sha(man_raw), n7_partition_sha256=sha(part_raw))
    corpus = worker.load_corpus(manifest, corpus_dir) if rec['status'] == 'PASS' else None
    return corpus, dict(n=md.N_TRAIN, groups={STAGE: dict(articles=arts, sequences=seqs)}), rec


def draw_record(manifest, arts, seqs, assigned, pool, n):
    """The pilot draw against the corpus: N distinct sequences, all inside the draw's articles, those articles assigned to an earlier study,
    and no sequence or article inside N8's fresh pool. Status PASS or FAIL."""
    rows = {a['index']: a for a in manifest['splits']['train']['articles']}; span = lambda articles: {rows[a]['first'] + k for a in articles for k in range(rows[a]['sequences'])}
    rec = dict(draw="N7's m01", articles=len(arts), sequences=len(seqs), distinct_sequences=len(set(seqs)), all_in_m01_articles=set(seqs) <= span(arts), m01_articles_are_assigned=set(arts) <= set(assigned),
               sequences_in_n8_fresh_pool=len(set(seqs) & span(pool['articles'])), articles_in_n8_fresh_pool=len(set(arts) & set(pool['articles'])), n8_fresh_pool=dict(articles=pool['fresh_articles'], sequences=pool['fresh_sequences']))
    ok = len(seqs) == n == rec['distinct_sequences'] and rec['all_in_m01_articles'] and rec['m01_articles_are_assigned'] and rec['sequences_in_n8_fresh_pool'] == 0 and rec['articles_in_n8_fresh_pool'] == 0
    return dict(rec, status='PASS' if ok else 'FAIL')


# ------------------------------------------------------------------ the timed context
class Timed(mw.Context):
    """matched_worker.Context with clocks around each width's pre-training and arm, and around every evaluation (between CUDA
    synchronisations). Peak GPU memory is reset at the start of each phase and read at its end."""
    def __init__(self, *a, clock=time.monotonic):
        super().__init__(*a); self.clock = clock; self.timing = {}; self.phase = None

    def _cuda(self, name):
        f = getattr(self.torch.cuda, name, None)
        return f() if f is not None else None

    def _begin(self, key):
        self.phase = key; self.timing[key] = dict(evaluation_seconds=0.0, evaluations=0); self._cuda('synchronize'); self._cuda('reset_peak_memory_stats'); return self.clock()

    def _end(self, key, t0):
        self._cuda('synchronize'); t = self.timing[key]; t['total_seconds'] = self.clock() - t0; t['training_seconds'] = t['total_seconds'] - t['evaluation_seconds']
        t['peak_allocated_bytes'] = self._cuda('max_memory_allocated'); t['peak_reserved_bytes'] = self._cuda('max_memory_reserved'); self.phase = None

    def evaluate(self, model, tokens):
        self._cuda('synchronize'); t0 = self.clock(); result = super().evaluate(model, tokens); self._cuda('synchronize')
        if self.phase is not None: self.timing[self.phase]['evaluation_seconds'] += self.clock() - t0; self.timing[self.phase]['evaluations'] += 1
        return result

    def pretrain(self, stage, width, *a):
        key = f'w{width}/pretraining and E0'; t0 = self._begin(key)
        try: return super().pretrain(stage, width, *a)
        finally: self._end(key, t0)

    def adapt_readouts(self, stage, width, lr, tag, *a, **k):
        key = f'w{width}/{tag}'; t0 = self._begin(key)
        try: return super().adapt_readouts(stage, width, lr, tag, *a, **k)
        finally: self._end(key, t0)


# ------------------------------------------------------------------ checks of what the stage wrote
def record_shape(rec):
    """A record reduced to what the study's later steps rely on. No loss value leaves this function: only whether its field holds a number."""
    rows = rec.get('readouts') or []
    return dict(status=rec.get('status'), n_train=rec.get('n_train'), width=rec.get('width'), lr=rec.get('lr'), tag=rec.get('tag'), epochs=[r['epoch'] for r in rows], updates=[r['update'] for r in rows],
                validation_field_is_a_number=[isinstance(r.get('validation_loss'), float) for r in rows], train_field_is_a_number=[isinstance(r.get('train_loss'), float) for r in rows], epochs_recorded=len(rec.get('epochs') or []))


def check_stage(run_dir, shapes, counts, partition):
    d = Path(run_dir) / STAGE; n, nv, R = shapes['n'], shapes['validation'], len(mp.READOUTS); problems = []
    group = partition['groups'][STAGE]
    if (d / 'INPUTS.json').exists():
        inputs = json.loads((d / 'INPUTS.json').read_bytes())
        if inputs.get('articles') != group['articles'] or inputs.get('sequence_indices_sha256') != sha(json.dumps(group['sequences'][:n]).encode()): problems.append("INPUTS.json does not name the draw's articles and sequences")
    files = {p.relative_to(d).as_posix(): p.stat().st_size for p in d.rglob('*') if p.is_file()}
    want = {'INPUTS.json', 'PRETRAINED.json', 'STATES_KEPT.json', mp.ORDER_FILE} | {f'w{w}/{x}' for w in mp.WIDTHS for x in ('E0.pt', 'E0.f32', f'{mp.TAG}/record.json', f'{mp.TAG}/arrays.f32')}
    if set(files) != want: problems.append(dict(files_missing=sorted(want - set(files)), files_extra=sorted(set(files) - want)))
    shapes_ok = {}
    for w in mp.WIDTHS:
        if files.get(f'w{w}/E0.f32') != 4 * (n + nv): problems.append(f'w{w}/E0.f32 size')
        if files.get(f'w{w}/{mp.TAG}/arrays.f32') != 4 * R * (n + nv): problems.append(f'w{w}/{mp.TAG}/arrays.f32 size: 28 readouts expected')
        path = d / f'w{w}/{mp.TAG}/record.json'
        if path.exists():
            s = record_shape(json.loads(path.read_bytes())); want_shape = dict(status='COMPLETE', n_train=n, width=w, lr=mp.RATE, tag=mp.TAG, epochs=list(mp.READOUTS), updates=[fp.readout_update(e, n) for e in mp.READOUTS],
                                                                               validation_field_is_a_number=[True] * R, train_field_is_a_number=[True] * R, epochs_recorded=mp.ORDER_EPOCHS)
            shapes_ok[f'w{w}'] = s == want_shape
            if s != want_shape: problems.append(f'w{w} record shape: {s}')
    orders_ok = False
    if (d / mp.ORDER_FILE).exists() and (d / 'INPUTS.json').exists():
        raw = (d / mp.ORDER_FILE).read_bytes(); inputs = json.loads((d / 'INPUTS.json').read_bytes()); size = 8 * n
        rows = [raw[e * size:(e + 1) * size] for e in range(mp.ORDER_EPOCHS)]
        orders_ok = (len(raw) == mp.ORDER_EPOCHS * size and inputs.get('epoch_order_sha256') == [sha(r) for r in rows] and inputs.get('order_file') == dict(path=f'{STAGE}/{mp.ORDER_FILE}', bytes=len(raw), sha256=sha(raw))
                     and all(sorted(struct.unpack(f'<{n}q', r)) == list(range(n)) for r in rows))
        if not orders_ok: problems.append('ORDERS.i64: size, per-epoch hashes or permutations')
    kept = json.loads((d / 'STATES_KEPT.json').read_bytes()) if (d / 'STATES_KEPT.json').exists() else dict(kept=[], errors=['missing'])
    states_ok = sorted(x['path'] for x in kept['kept']) == sorted(f'{STAGE}/w{w}/E0.pt' for w in mp.WIDTHS) and not kept['errors'] and all(sha((Path(run_dir) / x['path']).read_bytes()) == x['sha256'] for x in kept['kept'] if (Path(run_dir) / x['path']).exists())
    if not states_ok: problems.append('E0 states not all kept with their hashes')
    c = mw.study_counts(n, shapes['pool']); A = sum(len(v) for v in mp.ARMS.values())
    if counts.get('updates') != len(mp.ARMS) * c['pre_updates'] + A * c['adapt_updates']: problems.append(f"update count {counts.get('updates')}")
    if c['files'] != len(want): problems.append('the sealed per-stage file count differs')
    if any(p.name.endswith('.part') for p in d.rglob('*')): problems.append('a partial file remains')
    return dict(files={k: files[k] for k in sorted(files)}, records_have_28_readouts=shapes_ok, orders_written_with_hashes=orders_ok, e0_states_kept=states_ok,
                inputs_name_the_draw=not any("INPUTS.json does not name" in str(p) for p in problems)), problems


def run_projection(results, caps, stage_seconds, draws=3):
    """A run of `draws` draws against the 6-hour cap: projected from the benchmark (the run's own cap formula) and from this draw's time."""
    bench = sum((r or {}).get('seconds', 0.0) for r in results.values()); cap = caps['stage_work_cap_seconds']
    out = dict(draws=draws, benchmark_seconds=bench, projected_stage_seconds=caps['projected_stage_seconds'], measured_stage_seconds=stage_seconds, stage_cap_seconds=cap,
               projected_run_seconds=bench + draws * caps['projected_stage_seconds'], measured_run_seconds=bench + draws * stage_seconds, overall_limit_seconds=fp.LIMITS['overall_seconds'],
               formula=caps['formula'], feasible_by_formula=bool(caps['feasible']), measured_stage_within_cap=stage_seconds <= cap)
    out['fits'] = out['feasible_by_formula'] and out['measured_stage_within_cap']
    return out


# ------------------------------------------------------------------ the pilot
def run_pilot(approval_id, expected, seeds, dependencies=None, study=STUDY, inputs=None, pins=None, clock=time.monotonic, out=print):
    check_approval(approval_id, dependencies); seeds = check_seeds(seeds); verify_source(expected)
    if (inputs is not None or pins is not None) and dependencies is None: raise SystemExit('The real path binds the real inputs and pins only')
    if (inputs is None) != (pins is None): raise SystemExit('Test inputs need their pins')
    inputs, pins = (REAL_INPUTS, REAL_PINS) if inputs is None else (inputs, pins)
    if not study_paths_absent(): raise SystemExit('An N8 activation or run exists; the pilot comes before the builder')
    pilot = Path(study) / 'pilot'; log, run_dir = pilot / 'PILOT_LOG.json', pilot / 'run'
    if pilot.exists(): raise SystemExit('The pilot folder exists; the pilot runs once')
    files_before = verify_source(expected); pilot.mkdir(parents=False)
    rec = dict(schema=1, kind="N8 pilot: one draw (N7's m01) through the N8 worker", approval_id=approval_id, fixture=dependencies is not None, seeds=seeds, source_subject_sha256=expected, pilot_sha256=sha(Path(__file__).read_bytes()),
               corpus_read=True, loss_read=False, p_star_fitted=False, status='STARTED')
    log.write_bytes(encoded(rec)); start = clock(); L = fp.LIMITS; saved = plan.LIMITS; output = None; problems = []
    try:
        corpus, partition, data = pilot_data(inputs, pins); rec['data'] = data
        out(f"Pilot draw: {data['sequences']} sequences of {data['articles']} m01 articles; all in m01: {data['all_in_m01_articles']}; in N8's pool: {data['sequences_in_n8_fresh_pool']}")
        if data['status'] != 'PASS': raise RuntimeError("The pilot draw is not N7's m01 alone, outside N8's pool")
        shapes = dict(n=partition['n'], validation=len(corpus['validation_indices']), pool=len(corpus['pool_indices'])); rec['shapes'] = shapes
        run_dir.mkdir(); plan.LIMITS = dict(L)
        output = worker.Output(run_dir, L['stage_storage_bytes'], L['stage_files'], L['storage_bytes'], L['total_files'])
        if dependencies is None:
            import text_framework_setup
            torch, engine, Model = text_framework_setup.setup(run_dir / 'cache')
        else: torch, engine, Model = dependencies
        rec.update(python=platform.python_version(), torch=str(torch.__version__))
        budget = worker.Budget(start + L['overall_seconds'] - 120, clock); guard = worker.Guard(budget, output, cuda=torch.cuda); output.guard = guard
        ctx = Timed(torch, engine, Model, guard, output, clock=clock)
        pool = engine.load_sequences(corpus['test'], corpus['pool_indices'])
        results, overheads, failure = mw.startup_benchmark(ctx, seeds['benchmark_seed'], pool, budget, clock)
        bench_states = fw.remove_states(run_dir, 'benchmark'); counted = [x for x in bench_states['deleted'] if x['path'].endswith('.pt')]
        output.top_bytes -= sum(x['bytes'] for x in counted); output.top_files -= len(counted)
        decision, reason = mw.startup_rule(results, failure); ctx.counts = {k: 0 for k in ctx.counts}
        bench = dict(architectures=results, overheads=overheads)
        caps = mw.study_cap(bench, len(mp.RUN_STAGES['R1']), shapes['n'], len(pool)) if decision == 'GO' else None
        rec['benchmark'] = dict(decision=decision, reason=reason, failure=failure, architectures=results, overheads=overheads, fit_limit_bytes=fp.FIT_LIMIT_BYTES)
        rec['cap_of_a_run_of_three_draws'] = caps
        out(f'Start-up benchmark: {decision} ({reason})')
        if decision != 'GO': raise RuntimeError(f'The start-up rule stops a run: {reason}')
        guard.peaks = {}; reset = getattr(torch.cuda, 'reset_peak_memory_stats', None)
        if reset is not None: reset()
        t0 = clock(); row = {k: seeds[k] for k in SEED_KEYS if k != 'benchmark_seed'}
        rows, states = mw.stage(ctx, STAGE, row, corpus, partition, shapes['n'])
        guard.full(); output.close_stage(); stage_seconds = clock() - t0
        detail, problems = check_stage(run_dir, shapes, ctx.counts, partition)
        rec['stage'] = dict(seconds=stage_seconds, adaptations=len(rows), counts=dict(ctx.counts), guard_peaks=dict(guard.peaks), guard_calls=dict(guard.calls), timing=ctx.timing, checks=detail, problems=problems)
        rec['run_of_three_draws'] = run_projection(results, caps, stage_seconds); rec['three_draws_fit_a_run'] = rec['run_of_three_draws']['fits']
        rec['status'] = 'FAIL' if problems else 'PASS'
        p = rec['run_of_three_draws']
        out(f"Stage: {'FAIL' if problems else 'PASS'} in {stage_seconds:.0f} s. A run of three draws: {p['projected_run_seconds'] / 3600:.2f} h projected from the benchmark, "
            f"{p['measured_run_seconds'] / 3600:.2f} h from this draw; cap {p['stage_cap_seconds']} s per draw; fits the 6-hour cap: {p['fits']}")
    except Exception as e:
        rec.update(status='FAIL', error=dict(type=type(e).__name__, message=str(e)[:400], traceback=traceback.format_exc()[-1500:]))
    finally:
        plan.LIMITS = saved
        if output is not None: output.stage = None; output.guard = None
    rec['files_before_deletion'] = [dict(path=p.relative_to(run_dir).as_posix(), bytes=p.stat().st_size, sha256=fw.sha_file(p)) for p in sorted(run_dir.rglob('*')) if p.is_file() and 'cache' not in p.relative_to(run_dir).parts] if run_dir.exists() else []
    shutil.rmtree(run_dir, ignore_errors=True); rec['run_folder_deleted'] = not run_dir.exists()
    rec.update(seconds=clock() - start, study_paths_absent=study_paths_absent())
    try: rec['source_files_unchanged'] = verify_source(expected) == files_before
    except SystemExit as e: rec['source_files_unchanged'] = False; rec['source_error'] = str(e)
    if not (rec['run_folder_deleted'] and rec['source_files_unchanged'] and rec['study_paths_absent']): rec['status'] = 'FAIL'
    raw = encoded(rec); log.write_bytes(raw)
    if rec.get('error'): out(f"Error: {rec['error']['type']}: {rec['error']['message']}")
    out(f"Pilot: {rec['status']} in {rec['seconds']:.0f} s. Log {log} sha256 {sha(raw)}")
    return 0 if rec['status'] == 'PASS' else 1


def main(argv=None):
    ap = argparse.ArgumentParser(); ap.add_argument('--approval-id', required=True); ap.add_argument('--expected-subject', required=True)
    for k in SEED_KEYS: ap.add_argument('--' + k.replace('_', '-'), type=int, required=True)
    a = ap.parse_args(argv)
    return run_pilot(a.approval_id, a.expected_subject, {k: getattr(a, k) for k in SEED_KEYS})


if __name__ == '__main__':
    raise SystemExit(main())
