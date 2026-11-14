"""Dense-readout replication, N8: the worker (Linux/CUDA; N8-protocol-draft.md). Derived from N7's matched_worker.py.

Disabled unless run from one of its one-use activations; the framework is imported lazily. It uses the sealed few-epoch and text
workers unchanged where it can (fewepoch_worker: Context, remove_states, draw_gate, classify, sha_file; text_worker: Budget, Guard,
Output, benchmark, prestart). Modes (from the activation's AUTHORIZATION.json): R1-R8, three draws each (n01-n24), and the retry runs
X1-X8. Per draw, each width is pre-trained once and adapted at 1e-4 (mp.ARMS), widest first, from its E0, for 3.5 epochs, with training
and validation per-sequence losses at E0.25, E0.5, E1 and every 64 updates from update 2,048 to 3,584 (protocol section 3). Each
width's E0 state is kept, and each epoch's batch order is written with its SHA-256 (protocol section 3). X<k> is admitted on R<k>'s
terminal under the same source subject and inputs, if that run did not complete, and repeats from scratch, with the same seeds, the
draws the terminal does not record as complete, counted from its stage records only (protocol section 8); it compares each repeated
width's E0 losses with the first attempt's, where those exist.
Unchanged from N7's worker: admission re-derives the registry and the partition and checks disjointness; the start-up benchmark runs
every width one at a time and stops the run before any training if a width exceeds 2.25 GiB; the cap is the same formula on this run's
exact counts, with one 30-minute gate wait reserved; a run over the 6-hour formula stops before any training; before every stage the
owner script's check covers the GPU and AC power; the counting rule (any stage folder makes the run counted); TERMINAL.json through the
ledger, or directly as a last resort with terminal_outside_ledger.
"""
import gc, json, math, os, shutil, sys, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import text_plan as plan
import text_worker as worker
import wt103_corpus
import fewepoch_plan as fp
import fewepoch_data as fd
import fewepoch_worker as fw
import matched_data as md
import matched_registry as mr
import matched_plan as mp

ROOT = worker.ROOT                            # the closed record's root: the corpus is read from it, and nothing is written there
STUDY = Path(mp.STUDY_ROOT['posix' if os.name == 'posix' else 'nt'])
ACTIVATIONS = {m: STUDY / p for m, p in mp.ACTIVATIONS.items()}
RUNS = {m: STUDY / p for m, p in mp.RUNS.items()}
CORPUS = ROOT / mp.CORPUS
KIND = 'n8'
PINS = dict(registry_sha256=mp.REGISTRY['registry_sha256'], exclusions_sha256=mp.REGISTRY['exclusions_sha256'], draw_sha256=mp.REGISTRY['draw_sha256'],
            corpus_manifest_sha256=fp.CORPUS_MANIFEST_SHA256, partition_sha256=mp.PARTITION_SHA256, fewepoch_registry_sha256=fp.REGISTRY['registry_sha256'], fewepoch_partition_sha256=fp.PARTITION_SHA256,
            peak_registry_sha256=mp.PEAK_REGISTRY['registry_sha256'], peak_partition_sha256=mp.PEAK_PARTITION_SHA256, n7_registry_sha256=mp.N7_REGISTRY['registry_sha256'], n7_partition_sha256=mp.N7_PARTITION_SHA256)
BINDING_KEYS = ('approval_id', 'approval_record_sha256', 'registry_sha256', 'exclusions_sha256', 'draw_sha256', 'partition_sha256', 'corpus_manifest_sha256', 'fewepoch_registry_sha256', 'peak_registry_sha256', 'n7_registry_sha256', 'first_attempt_terminal_sha256')
INPUT_KEYS = ('registry_sha256', 'partition_sha256', 'corpus_manifest_sha256')        # a retry must have been bound to its first attempt's inputs
sha, encoded = worker.sha, worker.encoded


def mode_of(here):
    m = json.loads((Path(here) / 'AUTHORIZATION.json').read_bytes()).get('mode')
    if m not in mp.MODES: raise PermissionError('DISABLED: no N8 approval')
    return m


# ------------------------------------------------------------------ admission
def completed_draws(terminal):
    """The draws a terminal records as complete, from each stage record's name and status. Operational records only: no outcome field is read."""
    return [s.get('stage') for s in terminal.get('stages') or [] if s.get('status') == 'COMPLETE']


def retry_stages(terminal):
    """The draws of a first-attempt run that its retry repeats: the run's draws, in run order, less those its terminal records as complete."""
    done = set(completed_draws(terminal)); return [d for d in mp.RUN_STAGES[terminal.get('mode')] if d not in done]


def check_first_attempt(raw, mode, bindings, subject):
    """X<k> is admitted on R<k>'s terminal: the same source subject and inputs, a run that did not complete, and at least one draw to repeat.
    Returns the draws to repeat. Nothing else about the run is weighed."""
    t = json.loads(raw)
    if t.get('kind') != KIND or t.get('mode') != mp.RETRY_OF.get(mode) or t.get('status') == 'COMPLETE': raise PermissionError(f'This terminal does not admit retry run {mode}')
    if t.get('subject') != subject: raise PermissionError('The first attempt ran under another source subject')
    if any((t.get('bindings') or {}).get(k) != bindings.get(k) for k in INPUT_KEYS): raise PermissionError('The first attempt was bound to other inputs')
    stages = retry_stages(t)
    if not stages: raise PermissionError('The first attempt left no draw to repeat')
    return stages


def authorization(here, corpus_dir=CORPUS, pins=PINS):
    """The one-use activation: enabled, a mode with its real path and a real approval, the sealed source unchanged, the approval record,
    the registry (re-derived from its own bytes), the WikiText-103 corpus manifest (sealed rules, the acquisition subject), the tokenizer,
    the few-epoch, peak and N7 registries, the partition (re-derived) and its disjointness; for a retry run, its first attempt's terminal,
    which must admit it. Returns the authorization, registry, manifest, partition and the run's draws (the activation must list the same)."""
    here = Path(here); a = json.loads((here / 'AUTHORIZATION.json').read_bytes()); mode = a.get('mode')
    if a.get('enabled') is not True or a.get('execution_ready') is not True or mode not in mp.MODES or a.get('one_use') is not True or not a.get('approval_id'):
        raise PermissionError('DISABLED: no N8 approval')
    if here.resolve() == ACTIVATIONS[mode].resolve() and (a.get('fixture') is not False or str(a['approval_id']).upper().startswith('FIXTURE')): raise PermissionError('Real activation needs a real approval')
    if any(v is None for v in pins.values()): raise PermissionError('A pin is not set (PENDING)')
    raw = (here / 'SOURCE_SUBJECT.json').read_bytes()
    if sha(raw) != a.get('source_subject_sha256'): raise PermissionError('Source subject differs from the authorization')
    if sha((here / 'APPROVAL_RECORD.json').read_bytes()) != a.get('approval_record_sha256'): raise PermissionError('Approval record binding')
    subject_hashes = {}
    for row in json.loads(raw)['files']:
        b = (here / row['path']).read_bytes()
        if len(b) != row['bytes'] or sha(b) != row['sha256']: raise PermissionError('Changed source ' + row['path'])
        subject_hashes[row['path']] = row['sha256']
    reg_raw, ex_raw, draw_raw = ((here / n).read_bytes() for n in ('REGISTRY.json', 'EXCLUSIONS.json', 'DRAW.json'))
    got = (sha(reg_raw), sha(ex_raw), sha(draw_raw))
    if got != (a.get('registry_sha256'), a.get('exclusions_sha256'), a.get('draw_sha256')) or got != (pins['registry_sha256'], pins['exclusions_sha256'], pins['draw_sha256']):
        raise PermissionError('Registry binding')
    try: registry = mr.validate(json.loads(reg_raw), ex_raw, draw_raw, pins['corpus_manifest_sha256'], pins['fewepoch_partition_sha256'], pins['peak_partition_sha256'], pins['n7_partition_sha256'])
    except ValueError as e: raise PermissionError('Registry does not re-derive from its draw: ' + str(e))
    man_raw = (Path(corpus_dir) / 'CORPUS_MANIFEST.json').read_bytes()
    if len({sha(man_raw), a.get('corpus_manifest_sha256'), registry['corpus_manifest_sha256'], pins['corpus_manifest_sha256']}) != 1: raise PermissionError('Corpus manifest binding')
    manifest = json.loads(man_raw)
    try: wt103_corpus.validate_manifest(manifest, subject_hashes)
    except (ValueError, KeyError) as e: raise PermissionError('Corpus manifest differs from the pre-registration: ' + str(e))
    if manifest.get('source_subject_sha256') != fp.ACQUISITION_SUBJECT or manifest.get('fixture') is not False: raise PermissionError('Corpus was not made by the approved acquisition')
    if sha((Path(corpus_dir) / 'tokenizer.json').read_bytes()) != manifest['tokenizer']['sha256']: raise PermissionError('Tokenizer binding')
    few_raw = (here / 'FEWEPOCH_REGISTRY.json').read_bytes()
    if sha(few_raw) != a.get('fewepoch_registry_sha256') or sha(few_raw) != pins['fewepoch_registry_sha256']: raise PermissionError('Few-epoch registry binding')
    peak_raw = (here / 'PEAK_REGISTRY.json').read_bytes()
    if sha(peak_raw) != a.get('peak_registry_sha256') or sha(peak_raw) != pins['peak_registry_sha256']: raise PermissionError('Peak registry binding')
    n7_raw = (here / 'N7_REGISTRY.json').read_bytes()
    if sha(n7_raw) != a.get('n7_registry_sha256') or sha(n7_raw) != pins['n7_registry_sha256']: raise PermissionError('N7 registry binding')
    part_raw = (here / 'PARTITION.json').read_bytes()
    if sha(part_raw) != a.get('partition_sha256') or sha(part_raw) != pins['partition_sha256']: raise PermissionError('Partition binding')
    try: assigned = md.assigned_articles(manifest, json.loads(few_raw)['partition_seed'], json.loads(peak_raw)['partition_seed'], json.loads(n7_raw)['partition_seed'],
                                         pins['fewepoch_partition_sha256'], pins['peak_partition_sha256'], pins['n7_partition_sha256'])
    except ValueError as e: raise PermissionError('Earlier partition: ' + str(e))
    partition = md.partition(manifest, assigned, registry['partition_seed'])
    if json.loads(part_raw) != json.loads(encoded(partition)): raise PermissionError('Partition does not re-derive from the corpus and the registry')
    md.disjoint(partition, manifest, assigned)
    if mode in mp.RETRY_MODES:
        ours = {k: a[k] for k in INPUT_KEYS}
        t_raw = (here / 'FIRST_ATTEMPT_TERMINAL.json').read_bytes()
        if sha(t_raw) != a.get('first_attempt_terminal_sha256'): raise PermissionError('First-attempt terminal binding')
        stages = check_first_attempt(t_raw, mode, ours, a['source_subject_sha256'])
    else: stages = list(mp.RUN_STAGES[mode])
    if a.get('stages') != stages: raise PermissionError("The activation's draws differ from the run's")
    return a, registry, manifest, partition, stages


# ------------------------------------------------------------------ start-up benchmark (no fallback; the few-epoch rule on this ladder)
def startup_benchmark(ctx, seed, pool, budget, clock):
    """text_worker.benchmark (sealed, unchanged) one width at a time in BENCH_WIDTHS order, each width with its own peaks (reset before
    it), all inside the 900 s benchmark budget. Stops at the first failing width."""
    t, g = ctx.torch, ctx.guard; start = clock(); results, overheads, failure = {}, None, None; saved = plan.WIDTHS
    g.budget = worker.Budget(min(budget.deadline, start + fp.LIMITS['benchmark_seconds']), clock)
    try:
        for w in mp.BENCH_WIDTHS:
            plan.WIDTHS = (w,); g.peaks = {}
            reset = getattr(t.cuda, 'reset_peak_memory_stats', None)
            if reset is not None: reset()
            t0 = clock()
            try: r = worker.benchmark(ctx, seed, fp.LIMITS['benchmark_seconds'], pool, clock)
            except Exception as e:
                failure = dict(width=w, kind=fw.classify(e), type=type(e).__name__, message=str(e)[:400], peaks=dict(g.peaks), seconds=clock() - t0); break
            results[str(w)] = dict(r['architectures'][str(w)], seconds=clock() - t0); overheads = r['overheads']
    finally:
        plan.WIDTHS = saved; g.budget = budget; gc.collect()
        empty = getattr(t.cuda, 'empty_cache', None)
        if empty is not None: empty()
    return results, overheads, failure


def startup_rule(results, failure, limit=fp.FIT_LIMIT_BYTES):
    for w in mp.BENCH_WIDTHS:
        if str(w) not in results: return 'STOP', f"FAILED_{(failure or {}).get('kind', 'INCOMPLETE')}_AT_{w}"
        pk_ = ((results[str(w)] or {}).get('peaks') or {}).get('device_used_sampled')
        if pk_ is None: return 'STOP', f'PEAK_MISSING_AT_{w}'
        if pk_ > limit: return 'STOP', f'PEAK_{w}_OVER_LIMIT'
    if failure is not None: return 'STOP', f"FAILED_{failure.get('kind')}_AT_{failure.get('width')}"
    return 'GO', 'ALL_WIDTHS_WITHIN_LIMIT'


def study_counts(n_train, n_pool, arms=None):
    """Exact per-stage counts of a layout {width: rates}: training and validation at every readout, arrays and a record per arm, and the
    draw's batch orders. Each arm runs update(E3.5) updates and starts ORDER_EPOCHS epochs."""
    arms = mp.ARMS if arms is None else arms; W = len(arms); A = sum(len(r) for r in arms.values()); R = len(mp.READOUTS); files = 4 + W * 2 + A * 2
    return dict(trajectories=A, adaptations_per_width={str(w): len(r) for w, r in arms.items()}, files=files, dirs=W + A, full_guards=2 + W + 2 * A, epoch_guards=W * plan.PRETRAIN['epochs'] + A * mp.ORDER_EPOCHS + files,
                pre_updates=plan.updates(n_pool, plan.PRETRAIN['epochs']), adapt_updates=fp.readout_update(mp.LAST_READOUT, n_train, plan.BATCH), e0_eval_batches=plan.eval_batches(n_train) + plan.eval_batches(plan.N_VALIDATION),
                readout_eval_batches=R * (plan.eval_batches(n_train) + plan.eval_batches(plan.N_VALIDATION)), e0_bytes=4 * (n_train + plan.N_VALIDATION), array_bytes=4 * R * (n_train + plan.N_VALIDATION),
                order_bytes=8 * mp.ORDER_EPOCHS * n_train, arrays=True)


def study_cap(benchmark, stages, n_train, n_pool, arms=None):
    """The few-epoch cap formula on this layout's exact counts, for a run of `stages` draws: cap = ceil(1.25 x projected + 120 s); feasible iff
    stages x (cap + 60) + 900 + 1,800 (one gate wait) <= 21,600 s."""
    arms = mp.ARMS if arms is None else arms; arch, o = benchmark['architectures'], benchmark['overheads']; c = study_counts(n_train, n_pool, arms)
    total = 30.0 + o['seconds_data_generation']
    fixed_write, per_byte = worker.write_model(arch)
    total += fixed_write + per_byte * c['order_bytes']
    for w, rates in arms.items():
        b = arch[str(w)]
        total += c['pre_updates'] * b['seconds_per_pretraining_update'] + c['e0_eval_batches'] * b['seconds_per_eval_batch'] + b['seconds_per_state_write'] + fixed_write + per_byte * c['e0_bytes']
        total += len(rates) * (b['seconds_per_state_reload'] + c['adapt_updates'] * b['seconds_per_update'] + c['readout_eval_batches'] * b['seconds_per_eval_batch'] + 2 * fixed_write + per_byte * (c['array_bytes'] + plan.RECORD_BYTES))
    total += c['full_guards'] * (o['seconds_per_full_guard'] + (c['files'] + c['dirs'] + o['cache_entries']) * o['seconds_per_inventory_entry'])
    total += c['epoch_guards'] * o['seconds_per_epoch_guard']
    L = fp.LIMITS; n = stages
    work = math.ceil(L['cap_multiplier'] * total + L['cap_fixed_seconds'])
    max_cap = (L['overall_seconds'] - L['benchmark_seconds'] - fp.GATE_RESERVE_SECONDS) / n - L['stage_slack_seconds']
    return dict(projected_stage_seconds=total, stage_work_cap_seconds=min(work, math.floor(max_cap)), feasible=work <= max_cap, stages=n, counts=c,
                formula=f"ceil({L['cap_multiplier']}*projected+{L['cap_fixed_seconds']}) <= {math.floor(max_cap)} s; {n}*(cap+{L['stage_slack_seconds']})+{L['benchmark_seconds']}+{fp.GATE_RESERVE_SECONDS} <= {L['overall_seconds']} s",
                write_model=dict(fixed_seconds=fixed_write, seconds_per_byte=per_byte))


# ------------------------------------------------------------------ adaptation to E3.5 with dense readouts
class Context(fw.Context):
    def adapt_readouts(self, stage, width, lr, tag, pre_result, seeds, data, weights, orders, arrays=True):
        """fewepoch_worker.Context.adapt_readouts, study path only, on this plan's readouts: a constant rate up to update(E3.5), the fourth
        epoch's batch order used as far as that, with training and validation per-sequence losses at every readout, written as arrays. The
        sealed adaptation step, evaluation and reload are used. A nonfinite update or evaluation fails closed."""
        if arrays is not True: raise ValueError('This study always writes arrays')
        t = self.torch; g = self.guard; name = f'{stage}/w{width}/{tag}'; n = len(data['train'])
        g.full()
        model, optimizer = self.load_adaptation_model(width, pre_result['state']['path'], pre_result['state_tensor_hashes'], seeds['init_seed'], lr)
        at = {fp.readout_update(e, n, plan.BATCH): e for e in mp.READOUTS}; last = fp.readout_update(mp.LAST_READOUT, n, plan.BATCH)
        blocks, readouts, epochs, update = [], [], [], 0
        for epoch in range(1, mp.ORDER_EPOCHS + 1):
            g.epoch(); model.train(); norms = []
            for ids in orders[epoch - 1].split(plan.BATCH):
                norms.append(self.adaptation_step(model, optimizer, data['train'], weights, ids)); update += 1; self.counts['updates'] += 1
                if update in at:
                    e = at[update]; va = self.evaluate(model, data['validation']); tr = self.evaluate(model, data['train'])
                    blocks.append(self.floats(tr) + self.floats(va))
                    readouts.append(dict(epoch=e, update=update, train_loss=float(tr.mean()), validation_loss=float(va.mean())))
                    model.train()
                if update == last: break
            epochs.append(dict(epoch=epoch, updates=len(norms), gradient_norm_mean=sum(norms) / len(norms), gradient_norm_max=max(norms), clip_fraction=sum(x > plan.ADAPT['clip'] for x in norms) / len(norms)))
        if update != last or any(int(s['step']) != last for s in optimizer.state.values()): raise RuntimeError('Adaptation updates')
        if [r['epoch'] for r in readouts] != list(mp.READOUTS): raise RuntimeError('Readouts')
        record = dict(stage=stage, width=width, lr=lr, tag=tag, status='COMPLETE', readouts=readouts, epochs=epochs, n_train=n)
        record['arrays'] = self.out.write(f'{name}/arrays.f32', b''.join(blocks))
        record['layout'] = dict(blocks=len(blocks), block_epochs=list(mp.READOUTS), train_rows=n, validation_rows=len(data['validation']),
                                order='per readout: train per-sequence loss, then validation per-sequence loss (little-endian float32)')
        self.out.json(f'{name}/record.json', record)
        del optimizer, model; t.cuda.empty_cache(); g.full()
        return dict(path=f'{name}/record.json', tag=tag, lr=lr, readouts=readouts, status='COMPLETE')


# ------------------------------------------------------------------ one stage
def inputs(ctx, d, seeds, corpus, partition, n):
    """fewepoch_worker.inputs on this partition, with ORDER_EPOCHS epochs of batch orders. text_engine.orders seeds each epoch on its own
    (999 + seed + epoch), so the first three epochs are what a 3-epoch draw would have."""
    e = ctx.engine
    idx = fd.sequences(dict(n_fill=partition['n'], groups=partition['groups']), d, n)
    data = dict(train=e.load_sequences(corpus['train'], idx), validation=e.load_sequences(corpus['validation'], corpus['validation_indices']))
    pool = e.load_sequences(corpus['test'], corpus['pool_indices'])
    weights = e.weights(seeds['weight_seed'], n); orders = e.orders(seeds['adapt_order_seed'], n, mp.ORDER_EPOCHS)
    pool_orders = e.orders(seeds['pretrain_order_seed'], len(pool), plan.PRETRAIN['epochs'])
    hashes = dict(train=e.tensor_hash(data['train']), validation=e.tensor_hash(data['validation']), pool=e.tensor_hash(pool),
                  weights=e.tensor_hash(weights), orders=e.tensor_hash(orders), pool_orders=e.tensor_hash(pool_orders))
    return idx, data, pool, weights, orders, pool_orders, hashes


def kept_states(out_root, rel):
    """Every model state (and partial state write) under out_root/rel, recorded by sha256 and size, and kept (protocol section 3); the files
    are those fewepoch_worker.remove_states would delete. Errors are recorded per file and never raised."""
    base = Path(out_root) / rel; kept, errors = [], []
    try: files = sorted(p for p in base.rglob('*') if p.is_file() and (p.name.endswith('.pt') or p.name.endswith('.pt.part'))) if base.exists() else []
    except Exception as e: return dict(kept=kept, errors=[dict(path=rel, stage='list', error=f'{type(e).__name__}: {str(e)[:200]}')])
    for p in files:
        name = p.relative_to(out_root).as_posix()
        try: kept.append(dict(path=name, bytes=p.stat().st_size, sha256=fw.sha_file(p)))
        except Exception as e: errors.append(dict(path=name, stage='hash', error=f'{type(e).__name__}: {str(e)[:200]}'))
    return dict(kept=kept, kept_bytes=sum(x['bytes'] for x in kept), errors=errors)


def order_rows(orders):
    """Each epoch's batch order as little-endian int64 sequence indices: the bytes of ORDER_FILE, one row per epoch."""
    return [o.detach().cpu().contiguous().numpy().astype('<i8').tobytes() for o in orders]


def stage(ctx, d, seeds, corpus, partition, n, arms=None):
    """One draw. The batch orders are written first, with each epoch's SHA-256. Widest first: pre-training, the width's arm from its E0,
    then the width's model state hashed and kept. A nonfinite update fails closed."""
    arms = mp.ARMS if arms is None else arms; e, out, g = ctx.engine, ctx.out, ctx.guard
    out.begin_stage(d); g.full()
    idx, data, pool, weights, orders, pool_orders, hashes = inputs(ctx, d, seeds, corpus, partition, n)
    order = sorted(arms, reverse=True)
    rows_bytes = order_rows(orders); order_file = out.write(f'{d}/{mp.ORDER_FILE}', b''.join(rows_bytes))
    out.json(f'{d}/INPUTS.json', dict(seeds=seeds, n_train=n, sequence_indices_sha256=sha(json.dumps(idx).encode()), articles=partition['groups'][d]['articles'], tensor_hashes=hashes,
                                      weights=[float(x) for x in weights.tolist()], arms={str(w): list(arms[w]) for w in order}, widths=sorted(arms), readouts=list(mp.READOUTS),
                                      order_file=order_file, epoch_order_sha256=[sha(r) for r in rows_bytes]))
    pretrained, rows, per_width = {}, [], {}
    for w in order:
        pretrained[w] = ctx.pretrain(d, w, seeds, pool, data, pool_orders)
        for r in arms[w]:
            res = ctx.adapt_readouts(d, w, r, fp.rate_tag(r), pretrained[w], seeds, data, weights, orders, arrays=True)
            rows.append(dict(width=w, lr=r, readouts=res['readouts'], status=res['status']))
        per_width[str(w)] = kept_states(out.root, f'{d}/w{w}')
    out.json(f'{d}/PRETRAINED.json', {str(w): v for w, v in pretrained.items()})
    if e.tensor_hash(weights) != hashes['weights'] or e.tensor_hash(orders) != hashes['orders'] or order_rows(orders) != rows_bytes: raise RuntimeError('Paired inputs changed')
    states = dict(per_width=per_width, kept=[x for v in per_width.values() for x in v['kept']], errors=[x for v in per_width.values() for x in v['errors']])
    states['kept_bytes'] = sum(x['bytes'] for x in states['kept'])
    out.json(f'{d}/STATES_KEPT.json', states)
    return rows, states


def e0_against_first_attempt(mode, d, out_root):
    """For a retry run: each width's new E0 losses against those its first attempt wrote for the draw, if it wrote them (the runs sit side
    by side). Reported, not gating."""
    if mode not in mp.RETRY_MODES: return None
    first = Path(out_root).parent / Path(mp.RUNS[mp.RETRY_OF[mode]]).name / d; out = {}
    for w in sorted(mp.ARMS, reverse=True):
        old, new = first / f'w{w}' / 'E0.f32', Path(out_root) / d / f'w{w}' / 'E0.f32'
        out[str(w)] = 'ABSENT' if not old.is_file() else 'SAME' if fw.sha_file(old) == fw.sha_file(new) else 'DIFFERENT'
    return out


# ------------------------------------------------------------------ entry
def run(dependencies=None, here=None, out_root=None, clock=time.monotonic, corpus_dir=CORPUS, pins=PINS):
    here = Path(here) if here is not None else HERE
    mode = mode_of(here)
    if dependencies is None and not (HERE.resolve() == here.resolve() == ACTIVATIONS[mode].resolve()):
        raise PermissionError('The worker runs only from its one-use activation')          # the code that runs is the hash-checked copy
    out_root = Path(out_root) if out_root is not None else RUNS[mode]
    a, registry, manifest, partition, stages = authorization(here, corpus_dir, pins)
    if a.get('fixture') is not False and dependencies is None: raise PermissionError('A fixture activation runs only with injected test doubles')
    L = fp.LIMITS; start = clock(); budget = worker.Budget(start + L['overall_seconds'] - 120, clock); n = partition['n']
    if out_root.exists(): raise FileExistsError('One-use run directory exists')
    if shutil.disk_usage(out_root.parent).free < L['admission_free_bytes']: raise RuntimeError('Admission free space')
    prestart_records = worker.prestart(here)
    out_root.mkdir()
    out = worker.Output(out_root, L['stage_storage_bytes'], L['stage_files'], L['storage_bytes'], L['total_files'])
    status = dict(kind=KIND, subject=a['source_subject_sha256'], mode=mode, status='STARTED', draws=list(stages), stages=[], bindings={k: a[k] for k in BINDING_KEYS if k in a}, n_train=n, arms={str(w): list(r) for w, r in mp.ARMS.items()}, readouts=list(mp.READOUTS))
    saved_limits = plan.LIMITS; guard = ctx = None; run_peaks = {}; code = 1
    try:
        plan.LIMITS = dict(L)
        for name, raw in prestart_records: out.write(f'{worker.GATE_DIR}/{name}', raw)
        if dependencies is None:
            import text_framework_setup
            torch, engine, Model = text_framework_setup.setup(out_root / 'cache')
        else: torch, engine, Model = dependencies
        guard = worker.Guard(budget, out, cuda=torch.cuda); out.guard = guard
        ctx = Context(torch, engine, Model, guard, out)
        corpus = worker.load_corpus(manifest, corpus_dir)
        pool = engine.load_sequences(corpus['test'], corpus['pool_indices'])
        results, overheads, failure = startup_benchmark(ctx, registry['benchmark']['benchmark_seed'], pool, budget, clock)
        bench_states = fw.remove_states(out_root, 'benchmark')
        counted = [x for x in bench_states['deleted'] if x['path'].endswith('.pt')]
        out.top_bytes -= sum(x['bytes'] for x in counted); out.top_files -= len(counted)
        bench_states['ledger_released'] = dict(bytes=sum(x['bytes'] for x in counted), files=len(counted))
        decision, reason = startup_rule(results, failure)
        bench_counts = dict(ctx.counts); ctx.counts = {k: 0 for k in ctx.counts}
        bench = dict(architectures=results, overheads=overheads)
        caps = study_cap(bench, len(stages), n, len(pool)) if decision == 'GO' else None
        status['startup'] = dict(decision=decision, reason=reason)
        status['benchmark'] = out.json('BENCHMARK.json', dict(benchmark=bench, failure=failure, startup=dict(decision=decision, reason=reason, fit_limit_bytes=fp.FIT_LIMIT_BYTES, guard_bytes=fp.GUARD_BYTES),
                                                              caps=caps, states=bench_states, benchmark_counts=bench_counts, guard_calls=dict(guard.calls), n_train=n, pool_n=len(pool)))
        if decision == 'STOP' or not caps['feasible']:
            status.update(status='STOPPED_AT_STARTUP', stop_reason=reason if decision == 'STOP' else 'STAGES_OVER_6_H'); return 1
        seeds = {row['group']: {k: v for k, v in row.items() if k != 'group'} for row in registry['groups']}
        device_used = lambda: (lambda free, total: total - free)(*torch.cuda.mem_get_info())
        for d in stages:
            fw.draw_gate(out, here, d, budget, device_used, clock)
            stage_start = clock(); guard.peaks = {}
            reset = getattr(torch.cuda, 'reset_peak_memory_stats', None)
            if reset is not None: reset()
            guard.budget = worker.Budget(min(budget.deadline, stage_start + caps['stage_work_cap_seconds']), clock)
            rows, states = stage(ctx, d, seeds[d], corpus, partition, n)
            guard.budget = budget
            guard.full(); out.close_stage()
            for k, v in guard.peaks.items(): run_peaks[k] = max(run_peaks.get(k, 0), v)
            receipt = dict(stage=d, status='COMPLETE', trajectories=len(rows), seconds=clock() - stage_start, counts=dict(ctx.counts), guard_calls=dict(guard.calls),
                           peaks=dict(guard.peaks), states_kept=len(states['kept']), state_errors=len(states['errors']), closed_totals=list(out.closed), ledger_total=list(out.ledger_total()),
                           e0_against_first_attempt=e0_against_first_attempt(mode, d, out_root))
            out.json(f'{d}-RECEIPT.json', receipt); status['stages'].append(receipt)
        status['status'] = 'COMPLETE'; code = 0
    except BaseException as error:
        status.update(status='FAILED', error=dict(type=type(error).__name__, message=str(error)[:400]), active_stage=out.stage)
        status['states_on_failure'] = dict(benchmark=fw.remove_states(out_root, 'benchmark'), kept_in_active_stage=kept_states(out_root, out.stage) if out.stage else None)
        raise
    finally:
        plan.LIMITS = saved_limits
        if guard is not None:
            for k, v in guard.peaks.items(): run_peaks[k] = max(run_peaks.get(k, 0), v)
        status.update(elapsed_seconds=clock() - start, counts=dict(ctx.counts) if ctx else {}, peaks=run_peaks)
        out.stage = None; out.guard = None
        try:
            try:
                status['stage_folders'] = sorted(d for d in stages if (out_root / d).is_dir())
                status['counted_as_attempt'] = bool(status['stage_folders'])
            except Exception as e: status['stage_folders_error'] = f'{type(e).__name__}: {str(e)[:200]}'
            size, files = out.inventory(); status['inventory'] = dict(bytes=size, files=files)
            out.json('TERMINAL.json', status)
        except BaseException as e:
            sys.stderr.write('Terminal publication failed: ' + repr(e)[:300] + '\n')
            try:
                status['terminal_outside_ledger'] = f'{type(e).__name__}: {str(e)[:200]}'
                with open(out_root / 'TERMINAL.json', 'xb') as f: f.write(encoded(status))
            except BaseException as e2: sys.stderr.write('Terminal last-resort write failed: ' + repr(e2)[:300] + '\n')
    return code


if __name__ == '__main__':
    if len(sys.argv) != 2 or sys.argv[1] != 'run': raise SystemExit('usage: matched_worker.py run')
    try: raise SystemExit(run())
    except PermissionError as e: sys.stderr.write(str(e) + '\n'); raise SystemExit(1)
