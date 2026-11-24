"""POST HOC audit script (area D). Builds a DUMMY study folder inside the auditor's scratch folder, with invented contents only
(no N8 data; every "loss" is the sentinel 6.283185), in the layout the sealed worker and owner script write, so that a scratch copy of
the published check_run.py can be exercised without touching the owner's drive D:. Three dummy runs: R1 COMPLETE, R2 FAILED in n06,
X2 COMPLETE (the retry of R2). Each carries the "known gap" of OPERATIONAL_NOTES.md (terminal inventory one file / 2,355 bytes over).

usage: python -I -B d02_dummy_study.py <clone> <scratch> [<dummy folder name> [refused]]
"""
import hashlib, json, os, shutil, sys
from pathlib import Path
import numpy as np

CLONE, SCRATCH = Path(sys.argv[1]), Path(sys.argv[2])
N8 = CLONE / 'preregistration' / 'natural-text-dense-replication-20261114'
STUDY = SCRATCH / (sys.argv[3] if len(sys.argv) > 3 else 'dummy-study')
REFUSED = len(sys.argv) > 4 and sys.argv[4] == 'refused'       # R1 only: one start refused by the sealed owner script before the claim
assert 'swa21' in str(STUDY) and 'scratch' in str(STUDY)
if STUDY.exists(): shutil.rmtree(STUDY)
(STUDY / 'runs').mkdir(parents=True); (STUDY / 'activations').mkdir()
shutil.copytree(N8 / 'source', STUDY / 'source')                      # the published sealed source, for the plan's constants
sys.path.insert(0, str(STUDY / 'source'))
import matched_plan as mp, text_plan as plan, fewepoch_plan as fp      # pure constants

SENTINEL = 6.283185
N, NV, POOL = 1024, plan.N_VALIDATION, 2048
SUBJECT = hashlib.sha256((N8 / 'source/SOURCE_SUBJECT.json').read_bytes()).hexdigest()
REG = json.loads((N8 / 'registry/n8-seed-registry/REGISTRY.json').read_bytes())
SEEDS = {r['group']: {k: v for k, v in r.items() if k != 'group'} for r in REG['groups']}
sha = lambda b: hashlib.sha256(b).hexdigest()
enc = lambda x: (json.dumps(x, sort_keys=True, indent=2) + '\n').encode()
CLOCK = [1_800_000_000_000_000_000]                                   # explicit, increasing mtimes (ns), so "written before" is well defined


def put(path, data):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True); path.write_bytes(data)
    CLOCK[0] += 1_000_000_000; os.utime(path, ns=(CLOCK[0], CLOCK[0])); return dict(bytes=len(data), sha256=sha(data))


def floats(count, value=SENTINEL): return np.full(count, value, dtype='<f4').tobytes()


def inputs_and_orders(run, d):
    rng = np.random.default_rng(SEEDS[d]['adapt_order_seed']); rows = [rng.permutation(N).astype('<i8').tobytes() for _ in range(mp.ORDER_EPOCHS)]
    of = put(run / d / mp.ORDER_FILE, b''.join(rows))
    put(run / d / 'INPUTS.json', enc(dict(seeds=SEEDS[d], n_train=N, widths=[512, 768], readouts=list(mp.READOUTS), weights=[1.0] * N,
                                          order_file=dict(path=f'{d}/{mp.ORDER_FILE}', **of), epoch_order_sha256=[sha(r) for r in rows])))


def e0(run, d, w, salt):
    st = put(run / d / f'w{w}' / 'E0.pt', (f'dummy state {d} {w} {salt}'.encode()) * 50)
    arr = put(run / d / f'w{w}' / 'E0.f32', floats(N + NV, SENTINEL + (1e-3 if salt else 0)))
    return dict(path=f'{d}/w{w}/E0.pt', **st), dict(path=f'{d}/w{w}/E0.f32', **arr)


def full_draw(run, d, salt=''):
    inputs_and_orders(run, d); pre, kept = {}, []
    upd = [fp.readout_update(e, N, plan.BATCH) for e in mp.READOUTS]; per = N // plan.BATCH
    for w in (768, 512):
        st, arr = e0(run, d, w, salt); kept.append(st)
        pre[str(w)] = dict(width=w, parameters=plan.parameters(w), state=st, E0_arrays=arr, pretraining_updates=plan.updates(POOL, plan.PRETRAIN['epochs']),
                           E0_train_loss=SENTINEL, E0_validation_loss=SENTINEL)
        a = put(run / d / f'w{w}' / mp.TAG / 'arrays.f32', floats(28 * (N + NV)))
        put(run / d / f'w{w}' / mp.TAG / 'record.json', enc(dict(stage=d, width=w, lr=1e-4, tag=mp.TAG, status='COMPLETE', n_train=N,
            readouts=[dict(epoch=e, update=u, train_loss=SENTINEL, validation_loss=SENTINEL) for e, u in zip(mp.READOUTS, upd)],
            epochs=[dict(epoch=i + 1, updates=x) for i, x in enumerate([per] * 3 + [upd[-1] - 3 * per])],
            arrays=dict(path=f'{d}/w{w}/{mp.TAG}/arrays.f32', **a), layout=dict(blocks=28, block_epochs=list(mp.READOUTS), train_rows=N, validation_rows=NV))))
    put(run / d / 'PRETRAINED.json', enc(pre))
    put(run / d / 'STATES_KEPT.json', enc(dict(kept=kept, kept_bytes=sum(x['bytes'] for x in kept), errors=[])))


def tree(root): return [p for p in Path(root).rglob('*') if p.is_file()]


def make(mode, done, active=None, first=None, salt=''):
    """One dummy run: `done` complete draws, then (FAILED) the draw it stopped in."""
    run, act = STUDY / 'runs' / f'n8-{mode.lower()}', STUDY / 'activations' / f'n8-{mode.lower()}'
    draws = list(mp.RUN_STAGES[mode]) if mode.startswith('R') else list(done); gated = done + ([active] if active else [])
    aid = f'OWNER-20991231-N8-{mode}-01'
    shutil.copytree(N8 / 'source', act); put(act / 'REGISTRY.json', (N8 / 'registry/n8-seed-registry/REGISTRY.json').read_bytes())
    approval = enc(dict(approval_id=aid, mode=mode, stages=draws, retry_of=mp.RETRY_OF.get(mode), fixture=False, user_text=f'DUMMY: I approve N8 Run {mode} under {aid}.'))
    put(act / 'APPROVAL_RECORD.json', approval)
    auth = dict(approval_id=aid, approval_record_sha256=sha(approval), fixture=False, mode=mode, stages=draws)
    if first is not None:
        raw = (first / 'TERMINAL.json').read_bytes(); put(act / 'FIRST_ATTEMPT_TERMINAL.json', raw); auth['first_attempt_terminal_sha256'] = sha(raw)
    put(act / 'AUTHORIZATION.json', enc(auth))
    put(act / 'OWNER_CLAIM.json', enc(dict(mode=mode, approval_id=aid, subject=SUBJECT, one_use=True)))
    pre = enc(dict(schema=1, stage='PRESTART', verdict='IDLE')); put(act / 'gpu-checks/PRESTART.json', pre)
    put(run / 'BENCHMARK.json', enc(dict(pool_n=POOL, caps=dict(feasible=True, stage_work_cap_seconds=3097))))
    put(run / 'gpu-checks/PRESTART.json', pre)
    if REFUSED and mode == 'R1':                                  # the sealed owner script's record of a refused start; the sealed worker copies it into the run folder (text_worker.prestart)
        ref = enc(dict(schema=1, stage='PRESTART', verdict='REFUSED')); put(act / 'gpu-checks/PRESTART-REFUSED-1.json', ref); put(run / 'gpu-checks/PRESTART-REFUSED-1.json', ref)
    receipts, closed, GAP, state = [], [0, 0], (2355, 1), None
    for d in gated:
        put(run / f'gpu-checks/{d}-REQUEST.json', enc(dict(schema=1, stage=d)))
        resp = enc(dict(schema=1, stage=d, verdict='IDLE')); put(act / f'gpu-checks/{d}-RESPONSE.json', resp); put(run / f'gpu-checks/{d}.json', resp)
        if d == active:
            inputs_and_orders(run, d); state, _ = e0(run, d, 768, ''); break
        full_draw(run, d, salt)
        fs = tree(run / d); closed = [closed[0] + sum(p.stat().st_size for p in fs), closed[1] + len(fs)]
        top = [p for p in run.iterdir() if p.is_file()] + tree(run / 'gpu-checks')
        e0cmp = None
        if first is not None:
            old = lambda w: first / d / f'w{w}' / 'E0.f32'
            e0cmp = {str(w): 'ABSENT' if not old(w).is_file() else 'SAME' if sha(old(w).read_bytes()) == sha((run / d / f'w{w}' / 'E0.f32').read_bytes()) else 'DIFFERENT' for w in (768, 512)}
        r = dict(stage=d, status='COMPLETE', trajectories=2, states_kept=2, state_errors=0, seconds=2700.0, closed_totals=list(closed), e0_against_first_attempt=e0cmp,
                 ledger_total=[closed[0] + sum(p.stat().st_size for p in top) + GAP[0], closed[1] + len(top) + GAP[1]])
        put(run / f'{d}-RECEIPT.json', enc(r)); receipts.append(r)
    fs = tree(run)
    t = dict(kind='n8', subject=SUBJECT, mode=mode, status='COMPLETE' if not active else 'FAILED', draws=draws, stages=receipts, startup=dict(decision='GO', reason='ALL_WIDTHS_WITHIN_LIMIT'),
             bindings={k: auth[k] for k in ('approval_id', 'approval_record_sha256', 'first_attempt_terminal_sha256') if k in auth}, n_train=N, arms={'768': [1e-4], '512': [1e-4]}, readouts=list(mp.READOUTS),
             benchmark=dict(path='BENCHMARK.json', bytes=(run / 'BENCHMARK.json').stat().st_size, sha256=sha((run / 'BENCHMARK.json').read_bytes())),
             stage_folders=sorted(gated), counted_as_attempt=True, elapsed_seconds=7500.0, inventory=dict(bytes=sum(p.stat().st_size for p in fs) + GAP[0], files=len(fs) + GAP[1]))
    if active:
        t.update(error=dict(type='RuntimeError', message='Sampled GPU limit'), active_stage=active,
                 states_on_failure=dict(benchmark=dict(deleted=[]), kept_in_active_stage=dict(kept=[state], kept_bytes=state['bytes'], errors=[])))
    put(run / 'TERMINAL.json', enc(t))
    (run / 'cache').mkdir(); CLOCK[0] += 1_000_000_000; os.utime(run / 'cache', ns=(CLOCK[0], CLOCK[0]))       # emptied just after the terminal was written
    put(act / 'POWER_LOG.jsonl', b'{"power":"AC"}\n'); put(act / 'WORKER_STDOUT.log', b'')
    put(act / 'WORKER_STDERR.log', b'' if not active else b'Traceback (most recent call last):\n  ...\nRuntimeError: Sampled GPU limit\n')
    put(act / 'OWNER_PROGRESS.log', b'2099-12-31 00:00:00  dummy progress line\n')
    gates = sorted(p.name for p in (act / 'gpu-checks').iterdir())
    put(act / 'OWNER_EXIT_RECEIPT.json', enc(dict(status='COMPLETE' if not active else 'FAILED', mode=mode, subject=SUBJECT, exit_observed=True, exit_code=0 if not active else 1, elapsed_seconds=8000.0,
        terminal_status=t['status'], terminal_sha256=sha((run / 'TERMINAL.json').read_bytes()), terminal_unreadable=False, terminal_outside_ledger=False, stop_reason=None,
        stage_folders=sorted(gated), counted_as_attempt=True, retry=mode.startswith('X'),
        gpu_gates=[dict(stage=d, verdict='IDLE', checks=1, off_ac_checks=0) for d in gated], gpu_check_files=[dict(name=n, sha256=sha((act / 'gpu-checks' / n).read_bytes())) for n in gates],
        power_during_run=dict(samples=10, off_ac_samples=0, changes=[]), power_log_sha256=sha((act / 'POWER_LOG.jsonl').read_bytes()))))
    return run


r1 = make('R1', ['n01', 'n02', 'n03'])
r2 = make('R2', ['n04', 'n05'], active='n06')
# X2 repeats n06 with the same seeds and orders; its new w768 E0 array differs from the one R2 left (salted), and R2 left no w512 array.
x2 = make('X2', ['n06'], first=r2, salt='retry')
print('dummy study at', STUDY)
for r in (r1, r2, x2): print(' ', r.name, len(tree(r)), 'files,', sum(p.stat().st_size for p in tree(r)), 'bytes')
print('sentinel loss value used everywhere:', SENTINEL)
