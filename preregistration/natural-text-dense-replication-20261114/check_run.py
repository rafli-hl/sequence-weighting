"""Completeness of one N8 run's outputs, R1-R8 or a retry run X1-X8 (Windows Python 3.12, -I -B; NumPy). Structure, sizes, counts and
hashes only: no p* is fitted, no contrast computed and no loss value printed; loss fields are read only to check that they exist and are
finite.

    python -I -B check_run.py <R1-R8 (or 1-8) or X1-X8> [--terminal <the SHA-256 the owner script printed>]

Before it imports anything but the standard library it installs an audit hook (read_only) that refuses to open or list anything outside
the run's two folders (activations\\n8-<run>, runs\\n8-<run>), the sealed source (for the plan's constants) and Python's own
installation, and refuses every write, process and network use. So it reads nothing under work/runs/ and nothing of any other run, but
for a retry run X<k>: R<k>'s terminal and R<k>'s folders of the draws X<k> repeats, which its activation lists (read just before).
A retry run X<k> (protocol section 8) is checked as a run of its draws, and against its first attempt: its activation holds R<k>'s
terminal byte for byte, R<k> did not complete, and its draws are those R<k> did not complete; each draw has the seeds and saved orders
R<k> wrote for it, if R<k> wrote them; and each receipt's comparison of the new E0 arrays with R<k>'s (SAME, DIFFERENT or ABSENT) is
recomputed from their SHA-256 and reported. It reads nothing else of R<k>.
Exit 0 when every check passes, 1 otherwise. The terminal's inventory check is strict. When it fails, the check reports whether the
difference is exactly the known operational gap of OPERATIONAL_NOTES.md: one file in the worker's temp folder (cache\\), counted by
every stage receipt's ledger and by the terminal, and deleted as the worker exited.
A FAILED run (protocol section 8): the draws its terminal records as complete are checked in full, as in a complete run. The draw it
failed in is checked against the terminal's record of what it left (its files among a draw's 12, its inputs and saved orders, every E0
state it kept); those files stay in place, and the retry run X<k> repeats the draw from scratch. Draws after it must have left nothing.
--study and --n-train are for the tests only (a scratch study on N7's test doubles).
"""
import os, sys

STUDY = r'D:\sequence-weighting-n8'
SUBJECT = '9bdea3a9715b05393afe6713ddc696834dd344c3485c4e1a6ed0fa222f44bb6b'
FLOOR = 3 * 2 ** 30                                      # every run after R1 is admitted with 3 GiB free (fewepoch_plan.LIMITS)
WRITE_FLAGS = os.O_WRONLY | os.O_RDWR | os.O_APPEND | os.O_CREAT | os.O_TRUNC
REFUSED = ('os.remove', 'os.rename', 'os.mkdir', 'os.rmdir', 'os.chmod', 'os.truncate', 'os.utime', 'os.link', 'os.symlink', 'os.system', 'os.startfile', 'os.kill',
           'shutil.copyfile', 'shutil.copymode', 'shutil.copystat', 'shutil.copytree', 'shutil.rmtree', 'shutil.move', 'shutil.chown',
           'shutil.make_archive', 'shutil.unpack_archive', 'webbrowser.open')


def read_only(roots):
    """Reads only under `roots` and Python's installation; no write, no process, no network. Irreversible for the process."""
    allowed = [os.path.normcase(os.path.abspath(r)).rstrip('\\/') for r in list(roots) + [sys.base_prefix, sys.prefix]]
    def inside(p):
        if isinstance(p, int): return True                                    # an already open descriptor
        p = os.path.normcase(os.path.abspath(os.fsdecode(p if p is not None else '.')))
        return any(p == a or p.startswith(a + os.sep) for a in allowed)
    def hook(event, args):
        if event == 'open':
            path, mode, flags = args
            if (mode and any(c in mode for c in 'wax+')) or (flags or 0) & WRITE_FLAGS: raise PermissionError(f'check_run.py writes nothing: {path}')
            if not inside(path): raise PermissionError(f'check_run.py reads only its run, its activation and the source: {path}')
        elif event in ('os.listdir', 'os.scandir', 'glob.glob'):
            if not inside(args[0]): raise PermissionError(f'check_run.py lists only its run, its activation and the source: {args[0]}')
        elif event in REFUSED or event.startswith(('subprocess.', 'socket.', 'os.exec', 'os.spawn', 'os.posix_spawn', 'os.fork', 'urllib.', 'http.', 'ftplib.', 'smtplib.')):
            raise PermissionError(f'check_run.py refuses {event}')
    sys.addaudithook(hook)


def roots(study, mode):
    """What the check of run `mode` may read: its two folders and the sealed source; for a retry run X<k>, also R<k>'s terminal and R<k>'s
    folders of the draws the X<k> activation lists (well-formed draw names only), and nothing else of R<k>."""
    import json, re
    run, act = os.path.join(study, 'runs', f'n8-{mode.lower()}'), os.path.join(study, 'activations', f'n8-{mode.lower()}')
    out = [run, act, os.path.join(STUDY, 'source')]
    if mode.startswith('X'):
        first = os.path.join(study, 'runs', f'n8-r{mode[1:]}'); out.append(os.path.join(first, 'TERMINAL.json'))
        try:
            with open(os.path.join(act, 'AUTHORIZATION.json'), 'rb') as f: stages = json.loads(f.read()).get('stages') or []
        except (OSError, ValueError, AttributeError): stages = []
        out += [os.path.join(first, d) for d in stages if isinstance(d, str) and re.fullmatch('n[0-9]{2}', d)]
    return out


def main(argv):
    import argparse, re
    ap = argparse.ArgumentParser(); ap.add_argument('run'); ap.add_argument('--terminal'); ap.add_argument('--study', default=STUDY); ap.add_argument('--n-train', type=int)
    a = ap.parse_args(argv)
    m = re.fullmatch('([RX]?)([1-8])', a.run.upper())
    if not m: raise SystemExit('The run must be R1-R8 (or 1-8) or a retry run X1-X8')
    mode = (m.group(1) or 'R') + m.group(2); study = os.path.abspath(a.study)
    read_only(roots(study, mode))
    sys.path.insert(0, os.path.join(STUDY, 'source'))
    return Check(study, mode, a.terminal, a.n_train).run_all()


class Check:
    def __init__(self, study, mode, terminal, n_train):
        global hashlib, json, math, re, shutil, Path, np, mp, plan, fp
        import hashlib, json, math, re, shutil
        from pathlib import Path
        import numpy as np
        import matched_plan as mp, text_plan as plan, fewepoch_plan as fp
        self.study, self.mode, self.k, self.retry, self.given = Path(study), mode, int(mode[1:]), mode.startswith('X'), terminal
        self.run, self.act, self.first = self.study / 'runs' / f'n8-{mode.lower()}', self.study / 'activations' / f'n8-{mode.lower()}', self.study / 'runs' / f'n8-r{mode[1:]}'
        self.draws = [] if self.retry else list(mp.RUN_STAGES[mode]); self.n = n_train or mp.N_TRAIN; self.nv = plan.N_VALIDATION; self.failed = []; self.passed = 0
        self.want = {'INPUTS.json', mp.ORDER_FILE, 'PRETRAINED.json', 'STATES_KEPT.json'} | {f'w{w}/{x}' for w in mp.WIDTHS for x in ('E0.f32', 'E0.pt', f'{mp.TAG}/arrays.f32', f'{mp.TAG}/record.json')}

    # ------------------------------------------------------------------ helpers
    def check(self, name, fn, key=None):
        try: ok, detail = fn()
        except Exception as e: ok, detail = False, f'{type(e).__name__}: {str(e)[:120]}'
        if ok: self.passed += 1
        else: self.failed.append(key or name)
        print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f'  [{detail}]' if detail else ''))

    sha = staticmethod(lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest())
    load = staticmethod(lambda p: json.loads(Path(p).read_bytes()))
    finite = staticmethod(lambda x: isinstance(x, (int, float)) and math.isfinite(x))
    files = staticmethod(lambda root: [p for p in Path(root).rglob('*') if p.is_file()])

    def get(self, p):
        """A record that may be missing or unreadable: None then, so the checks that read it fail instead of the whole check stopping."""
        try: return self.load(p)
        except Exception: return None

    # ------------------------------------------------------------------ the checks
    def run_all(self):
        k, mode = self.k, self.mode
        if not self.run.is_dir() or not (self.run / 'TERMINAL.json').is_file() or not (self.act / 'OWNER_EXIT_RECEIPT.json').is_file():
            print(f'=== Run {mode}\nFAIL  Run {mode} has not ended: no TERMINAL.json in {self.run} or no OWNER_EXIT_RECEIPT.json in {self.act}'); return 1
        self.t = t = self.load(self.run / 'TERMINAL.json'); self.rcpt = self.load(self.act / 'OWNER_EXIT_RECEIPT.json'); self.auth = self.load(self.act / 'AUTHORIZATION.json')
        if self.retry: self.draws = [d for d in self.auth.get('stages') or [] if isinstance(d, str)]       # checked against R<k>'s terminal (first_attempt)
        draws = self.draws
        print(f'=== Run {mode} ({", ".join(draws)}' + (f', the retry of Run R{k}' if self.retry else '') + '): completeness only; no p*, no contrast, no loss value')
        # A complete run: all its draws. A failed run: those its stage records give as complete (matched_worker.completed_draws), the draw it
        # failed in (active_stage), and the draws with a folder, whose GPU checks ran (stage_folders).
        self.complete = t.get('status') == 'COMPLETE'
        self.done = [s.get('stage') for s in t.get('stages') or [] if s.get('status') == 'COMPLETE']
        self.active = None if self.complete else t.get('active_stage')
        self.checked = draws if self.complete else self.done
        self.gated = draws if self.complete else list(t.get('stage_folders') or [])
        self.fate = 'failed in both attempts, reported as failed and excluded' if self.retry else f'left for the retry run X{k}'
        if not self.complete:
            e = t.get('error') or {}
            print(f"Run {mode} {t.get('status')} in {self.active} ({e.get('type')}: {e.get('message')}). Complete, checked in full: {', '.join(self.done) or 'none'}. "
                  f"Not complete, {self.fate}: {', '.join(d for d in draws if d not in self.done)}")
        self.terminal()
        if self.retry: self.first_attempt()
        self.each_draw(); self.receipts()
        try: gap = self.known_gap()
        except Exception as e: gap = dict(known=False, text=f'it could not be evaluated ({type(e).__name__}: {str(e)[:120]})')
        try: self.disk()
        except Exception as e: print(f'      disk use could not be measured ({type(e).__name__}: {str(e)[:120]})')
        print(f'{self.passed} passed, {len(self.failed)} failed')
        if 'inventory' in self.failed:
            print(('The inventory failure is the known operational gap (OPERATIONAL_NOTES.md): ' if gap['known'] else 'The inventory failure is NOT the known operational gap; report it: ') + gap['text'])
        others = [f for f in self.failed if f != 'inventory']
        if others: print(f'{len(others)} other failure(s): report them')
        if not self.complete: print(f"Run {mode} did not complete: {', '.join(self.done) or 'no draw'} complete; {', '.join(d for d in draws if d not in self.done)} {self.fate} (protocol section 8)")
        return 0 if not self.failed else 1

    def first_attempt(self):
        """A retry run X<k>: admitted on R<k>'s terminal, which its activation holds; its draws, those R<k> did not complete; each with R<k>'s
        seeds and saved orders for it, where R<k> wrote them."""
        k, first = self.k, self.first
        print(f'--- the first attempt, Run R{k}')
        def admitted():
            raw = (self.act / 'FIRST_ATTEMPT_TERMINAL.json').read_bytes(); ft = json.loads(raw); h = hashlib.sha256(raw).hexdigest()
            done = [s.get('stage') for s in ft.get('stages') or [] if s.get('status') == 'COMPLETE']
            ok = (raw == (first / 'TERMINAL.json').read_bytes() and h == self.auth['first_attempt_terminal_sha256'] == self.t['bindings']['first_attempt_terminal_sha256']
                  and ft['kind'] == 'n8' and ft['mode'] == f'R{k}' and ft['status'] != 'COMPLETE' and ft['subject'] == SUBJECT
                  and len(self.draws) > 0 and self.draws == [d for d in mp.RUN_STAGES[f'R{k}'] if d not in done] == self.t['draws'])
            return ok, f"R{k}'s terminal {h}, {ft['status']}; complete there: {', '.join(done) or 'none'}; repeated here: {', '.join(self.draws)}"
        self.check(f"FIRST_ATTEMPT_TERMINAL.json is R{k}'s terminal byte for byte, bound by the activation and this terminal; R{k} did not complete; "
                   f"this run's draws are those it did not complete", admitted)
        for d in self.draws:
            def same(d=d):
                if not (first / d / 'INPUTS.json').is_file(): return True, f'R{k} wrote no inputs for {d}'
                a, b = self.load(first / d / 'INPUTS.json'), self.load(self.run / d / 'INPUTS.json')
                return a['seeds'] == b['seeds'] and a['order_file']['sha256'] == b['order_file']['sha256'] and a['epoch_order_sha256'] == b['epoch_order_sha256'], b['order_file']['sha256'][:16]
            self.check(f"{d}: the same seeds and saved orders as R{k}'s {d}, where R{k} wrote them (protocol section 8: from scratch, with the same seeds)", same)

    def terminal(self):
        t, rcpt, auth, k, draws, mode = self.t, self.rcpt, self.auth, self.k, self.draws, self.mode
        print('--- the terminal')
        h = self.sha(self.run / 'TERMINAL.json')
        self.check("TERMINAL.json's SHA-256 equals the owner receipt's" + (' and the one given' if self.given else ''), lambda: (h == rcpt['terminal_sha256'] and (self.given is None or h == self.given.lower()), h))
        if self.complete:
            self.check(f'terminal: n8, COMPLETE, mode {mode}, the sealed subject, draws {", ".join(draws)}, no error, written through the ledger',
                       lambda: (t['kind'] == 'n8' and t['status'] == 'COMPLETE' and t['mode'] == mode and t['subject'] == SUBJECT and t['draws'] == draws and 'error' not in t
                                and 'terminal_outside_ledger' not in t and 'stage_folders_error' not in t, ''))
            self.check('terminal: start-up GO, every stage record COMPLETE, every draw folder there, counted as an attempt',
                       lambda: (t['startup']['decision'] == 'GO' and [s['stage'] for s in t['stages']] == draws and all(s['status'] == 'COMPLETE' for s in t['stages'])
                                and t['stage_folders'] == draws and t['counted_as_attempt'] is True, f"start-up {t['startup']['decision']} ({t['startup']['reason']})"))
        else:
            e = t.get('error') or {}
            self.check(f"terminal: n8, FAILED in {self.active} with its error recorded ({e.get('type')}: {e.get('message')}), mode {mode}, the sealed subject, draws {', '.join(draws)}, written through the ledger",
                       lambda: (t['kind'] == 'n8' and t['status'] == 'FAILED' and t['mode'] == mode and t['subject'] == SUBJECT and t['draws'] == draws and bool(e.get('type')) and bool(e.get('message'))
                                and 'terminal_outside_ledger' not in t and 'stage_folders_error' not in t, ''))
            self.check('terminal: start-up GO; the complete draws come first in run order, each stage record COMPLETE; it failed in the next draw; '
                       'draw folders for exactly these; counted as an attempt',
                       lambda: (t['startup']['decision'] == 'GO' and [s['stage'] for s in t['stages']] == self.done == draws[:len(self.done)] and len(self.done) < len(draws)
                                and self.active == draws[len(self.done)] and self.gated == sorted(self.done + [self.active]) and t['counted_as_attempt'] is True,
                                f"start-up {t['startup']['decision']} ({t['startup']['reason']}); complete {', '.join(self.done) or 'none'}; failed in {self.active}"))
        def bindings():
            rec = self.load(self.act / 'APPROVAL_RECORD.json'); aid = auth['approval_id']
            ok = (t['bindings'] == {x: auth[x] for x in t['bindings']} and t['bindings']['approval_id'] == aid and auth['approval_record_sha256'] == self.sha(self.act / 'APPROVAL_RECORD.json')
                  and re.fullmatch(rf'OWNER-[0-9]{{8}}-N8-{mode}-[0-9]{{2}}', aid) is not None and rec['approval_id'] == aid and rec['mode'] == mode and rec['stages'] == draws
                  and rec.get('retry_of') == (f'R{k}' if self.retry else None) and rec['fixture'] is False and auth['fixture'] is False
                  and re.search(rf'\bRun {mode}\b', rec['user_text']) is not None and aid in rec['user_text'])
            return ok, aid
        self.check(f"terminal's bindings equal the activation's; the approval id and its recorded text name Run {mode}" + (f', the retry of R{k}' if self.retry else ''), bindings)
        self.check(f"terminal: n_train {self.n:,}, arms 768 and 512 at 1e-4, the plan's 28 readouts",
                   lambda: (t['n_train'] == self.n and t['arms'] == {'768': [1e-4], '512': [1e-4]} and t['readouts'] == list(mp.READOUTS) and len(mp.READOUTS) == 28, ''))
        def bench():
            b = self.run / 'BENCHMARK.json'; B = self.load(b); self.pool_n = B['pool_n']
            return t['benchmark'] == dict(path='BENCHMARK.json', bytes=b.stat().st_size, sha256=self.sha(b)) and B['caps']['feasible'] is True, f"stage cap {B['caps']['stage_work_cap_seconds']} s"
        self.check('BENCHMARK.json is the one the terminal names; its caps were feasible', bench)
        def top():
            names = {p.name for p in self.run.iterdir()}; expected = {'BENCHMARK.json', 'TERMINAL.json', 'gpu-checks'} | set(self.gated) | {f'{d}-RECEIPT.json' for d in self.checked}
            gates = {p.name for p in (self.run / 'gpu-checks').iterdir()}; empty = [x for x in ('benchmark', 'cache') if (self.run / x).exists()]
            ok = names - {'benchmark', 'cache'} == expected and gates == {'PRESTART.json'} | {f'{d}{s}' for d in self.gated for s in ('-REQUEST.json', '.json')} and all(not any((self.run / x).rglob('*')) for x in empty)
            return ok, f"{len(names)} entries; {', '.join(x + chr(92) for x in empty) or 'no'} empty folders"
        self.check('the run folder holds only the expected entries' + ('' if self.complete else ' (a folder for each draw started, a receipt for each complete one)')
                   + '; its gate records are PRESTART and one request and one check per draw' + ('' if self.complete else ' started') + '; benchmark\\ and cache\\, if there, are empty', top)
        files = self.files(self.run); self.inv_now = (len(files) - 1, sum(p.stat().st_size for p in files if p.name != 'TERMINAL.json'))
        self.check("the terminal's inventory (files only, text_worker.Output.inventory) equals the run folder less TERMINAL.json itself",
                   lambda: (t['inventory']['files'] == self.inv_now[0] and t['inventory']['bytes'] == self.inv_now[1],
                            f"terminal {t['inventory']['bytes']:,} bytes in {t['inventory']['files']} files; now {self.inv_now[1]:,} in {self.inv_now[0]}"), key='inventory')

    def inputs_and_orders(self, d, D, inp):
        n = self.n
        self.check(f"{d}: INPUTS has the registry's seeds for {d}, n_train {n:,}, widths 512 and 768, the 28 readouts, {n:,} weights",
                   lambda: (inp['seeds'] == self.seeds[d] and inp['n_train'] == n and inp['widths'] == [512, 768] and inp['readouts'] == list(mp.READOUTS) and len(inp['weights']) == n, ''))
        def orders():
            raw = (D / mp.ORDER_FILE).read_bytes(); rows = [raw[i * n * 8:(i + 1) * n * 8] for i in range(mp.ORDER_EPOCHS)]
            perm = all(np.array_equal(np.sort(np.frombuffer(r, dtype='<i8')), np.arange(n)) for r in rows)
            return (len(raw) == mp.ORDER_EPOCHS * n * 8 and inp['order_file'] == dict(path=f'{d}/{mp.ORDER_FILE}', bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())
                    and [hashlib.sha256(r).hexdigest() for r in rows] == inp['epoch_order_sha256'] and perm), inp['order_file']['sha256'][:16]
        self.check(f"{d}: the saved orders: 4 epochs x {n:,} int64 indices, the file's and each epoch row's SHA-256 equal INPUTS', each row a permutation", orders)

    def each_draw(self):
        n, nv, k, want = self.n, self.nv, self.k, self.want
        print('--- each draw')
        upd = [fp.readout_update(e, n, plan.BATCH) for e in mp.READOUTS]; per_epoch = n // plan.BATCH; epochs = [per_epoch] * 3 + [fp.readout_update(mp.LAST_READOUT, n, plan.BATCH) - 3 * per_epoch]
        self.seeds = {row['group']: {x: v for x, v in row.items() if x != 'group'} for row in self.load(self.act / 'REGISTRY.json')['groups']}
        for d in self.checked:
            D = self.run / d
            self.check(f'{d}: exactly its 12 files, no partial state write', lambda: ((have := {p.relative_to(D).as_posix() for p in self.files(D)}) == want, f'{len(have)} files'))
            inp = self.get(D / 'INPUTS.json'); pre = self.get(D / 'PRETRAINED.json'); kept = self.get(D / 'STATES_KEPT.json')
            self.inputs_and_orders(d, D, inp)
            self.check(f'{d}: STATES_KEPT records exactly the two E0 states, no errors', lambda: (sorted(x['path'] for x in kept['kept']) == [f'{d}/w512/E0.pt', f'{d}/w768/E0.pt']
                                                                                             and kept['errors'] == [] and kept['kept_bytes'] == sum(x['bytes'] for x in kept['kept']), ''))
            for w in (768, 512):
                W = D / f'w{w}'; p = (pre or {}).get(str(w))
                def state(W=W, p=p, w=w):
                    st = W / 'E0.pt'; h = self.sha(st); kp = next(x for x in kept['kept'] if x['path'] == f'{d}/w{w}/E0.pt')
                    return kp == dict(path=f'{d}/w{w}/E0.pt', bytes=st.stat().st_size, sha256=h) and p['state'] == kp, f'{st.stat().st_size:,} bytes, {h[:16]}'
                self.check(f'{d} w{w}: E0 state kept; its bytes and SHA-256 equal STATES_KEPT and PRETRAINED', state)
                def e0(W=W, p=p, w=w):
                    b = (W / 'E0.f32').read_bytes()
                    return (len(b) == (n + nv) * 4 and p['E0_arrays'] == dict(path=f'{d}/w{w}/E0.f32', bytes=len(b), sha256=hashlib.sha256(b).hexdigest())
                            and bool(np.isfinite(np.frombuffer(b, dtype='<f4')).all()) and self.finite(p['E0_train_loss']) and self.finite(p['E0_validation_loss'])
                            and p['pretraining_updates'] == plan.updates(self.pool_n, plan.PRETRAIN['epochs']) and p['width'] == w and p['parameters'] == plan.parameters(w)), ''
                self.check(f'{d} w{w}: E0.f32 is {n:,} + {nv} float32 with the hash PRETRAINED gives, all finite; pre-training ran its updates', e0)
                rec = self.get(W / mp.TAG / 'record.json')
                self.check(f'{d} w{w}: record COMPLETE; 28 readouts at the plan\'s epochs and updates ({upd[0]:,} ... {upd[-1]:,}), each with finite losses; epochs of {", ".join(f"{x:,}" for x in epochs)} updates',
                           lambda rec=rec, w=w: (rec['status'] == 'COMPLETE' and rec['width'] == w and rec['lr'] == 1e-4 and rec['n_train'] == n and [r['epoch'] for r in rec['readouts']] == list(mp.READOUTS)
                                                 and [r['update'] for r in rec['readouts']] == upd and all(self.finite(r['train_loss']) and self.finite(r['validation_loss']) for r in rec['readouts'])
                                                 and [e['updates'] for e in rec['epochs']] == epochs, ''))
                def arrays(W=W, rec=rec, w=w):
                    b = (W / mp.TAG / 'arrays.f32').read_bytes(); L = rec['layout']
                    return (len(b) == 28 * (n + nv) * 4 and rec['arrays'] == dict(path=f'{d}/w{w}/{mp.TAG}/arrays.f32', bytes=len(b), sha256=hashlib.sha256(b).hexdigest())
                            and L['blocks'] == 28 and L['block_epochs'] == list(mp.READOUTS) and L['train_rows'] == n and L['validation_rows'] == nv
                            and bool(np.isfinite(np.frombuffer(b, dtype='<f4')).all())), f"{len(b):,} bytes, {rec['arrays']['sha256'][:16]}"
                self.check(f'{d} w{w}: arrays.f32 is 28 blocks of {n:,} + {nv} float32 with the hash its record gives, laid out as recorded, all finite', arrays)
        if self.active: self.partial(self.active)

    def partial(self, d):
        """The draw the run failed in: what it left, against the terminal's record of it. Its E0 losses are not read."""
        D = self.run / d; n, nv = self.n, self.nv
        have = {p.relative_to(D).as_posix() for p in self.files(D)} if D.is_dir() else set()
        self.check(f'{d}, the draw the run failed in: its files are among the 12 a draw writes, no partial write', lambda: (bool(have) and have <= self.want, f"{len(have)} files: {', '.join(sorted(have))}"))
        self.inputs_and_orders(d, D, self.get(D / 'INPUTS.json'))
        def states():
            rec = self.t['states_on_failure']['kept_in_active_stage']; listed = rec['kept']
            ok = (sorted(x['path'] for x in listed) == sorted(f'{d}/{p}' for p in have if p.endswith('/E0.pt')) and rec['errors'] == [] and rec['kept_bytes'] == sum(x['bytes'] for x in listed)
                  and all(x == dict(path=x['path'], bytes=(self.run / x['path']).stat().st_size, sha256=self.sha(self.run / x['path'])) for x in listed))
            return ok, '; '.join(f"{x['path']} {x['bytes']:,} bytes, {x['sha256'][:16]}" for x in listed) or 'none'
        self.check(f"{d}: every E0 state it left equals the terminal's states_on_failure record (bytes and SHA-256), no errors", states)
        e0 = sorted(p for p in have if p.endswith('/E0.f32'))
        self.check(f'{d}: each E0.f32 it left is {n:,} + {nv} float32', lambda: (all((D / p).stat().st_size == (n + nv) * 4 for p in e0), ', '.join(e0) or 'none'))

    def receipts(self):
        t, rcpt, k, draws, mode = self.t, self.rcpt, self.k, self.draws, self.mode
        print('--- the receipts')
        closed = [0, 0]
        for i, d in enumerate(self.checked):
            fs = self.files(self.run / d); closed = [closed[0] + sum(p.stat().st_size for p in fs), closed[1] + len(fs)]
            r = self.get(self.run / f'{d}-RECEIPT.json'); retry = 'a retry, with its E0 comparison' if self.retry else 'not a retry'
            self.check(f"{d}-RECEIPT: COMPLETE, 2 trajectories, 2 states kept, 0 state errors, {retry}; equals the terminal's stage record; its closed totals equal the draw folders now",
                       lambda r=r, i=i, c=list(closed): (r['stage'] == d and r['status'] == 'COMPLETE' and r['trajectories'] == 2 and r['states_kept'] == 2 and r['state_errors'] == 0
                                                         and (isinstance(r['e0_against_first_attempt'], dict) if self.retry else r['e0_against_first_attempt'] is None)
                                                         and r == t['stages'][i] and r['closed_totals'] == c, f"{r['seconds']:,.0f} s on the worker clock"))
            if self.retry:
                def e0(d=d, r=r):
                    # As matched_worker.e0_against_first_attempt: per width, widest first, ABSENT if R<k> left no E0 arrays, else SAME or DIFFERENT by SHA-256.
                    old = lambda w: self.first / d / f'w{w}' / 'E0.f32'
                    got = {str(w): 'ABSENT' if not old(w).is_file() else 'SAME' if self.sha(old(w)) == self.sha(self.run / d / f'w{w}' / 'E0.f32') else 'DIFFERENT' for w in sorted(mp.ARMS, reverse=True)}
                    return r['e0_against_first_attempt'] == got, ', '.join(f'w{w} {v}' for w, v in r['e0_against_first_attempt'].items())
                self.check(f"{d}-RECEIPT: its comparison of each width's new E0 arrays with R{k}'s {d} equals the one recomputed from their SHA-256 (SAME, DIFFERENT, or ABSENT where R{k} left none)", e0)
        claim = self.get(self.act / 'OWNER_CLAIM.json')
        self.check(f'OWNER_CLAIM: {mode}, the approval id, the sealed subject, one use', lambda: (claim['mode'] == mode and claim['approval_id'] == self.auth['approval_id'] and claim['subject'] == SUBJECT and claim['one_use'] is True, ''))
        elapsed = lambda: f"{rcpt['elapsed_seconds']:,.0f} s owner elapsed; worker clock {t['elapsed_seconds']:,.0f} s"
        retry = 'a retry' if self.retry else 'not a retry'
        if self.complete:
            self.check(f'OWNER_EXIT_RECEIPT: COMPLETE, exit observed, exit code 0, terminal COMPLETE and readable, every draw folder, counted, {retry}',
                       lambda: (rcpt['status'] == 'COMPLETE' and rcpt['exit_observed'] is True and rcpt['exit_code'] == 0 and rcpt['terminal_status'] == 'COMPLETE' and rcpt['terminal_unreadable'] is False
                                and rcpt['terminal_outside_ledger'] is False and rcpt['stage_folders'] == draws and rcpt['counted_as_attempt'] is True and rcpt['retry'] is self.retry and rcpt['mode'] == mode
                                and rcpt['subject'] == SUBJECT, elapsed()))
        else:
            self.check(f"OWNER_EXIT_RECEIPT: FAILED, exit observed, a nonzero exit code, terminal FAILED and readable, no GPU or power stop, the terminal's draw folders, counted, {retry}",
                       lambda: (rcpt['status'] == 'FAILED' and rcpt['exit_observed'] is True and rcpt['exit_code'] not in (0, None) and rcpt['terminal_status'] == 'FAILED' and rcpt['terminal_unreadable'] is False
                                and rcpt['terminal_outside_ledger'] is False and rcpt['stop_reason'] is None and rcpt['stage_folders'] == self.gated and rcpt['counted_as_attempt'] is True
                                and rcpt['retry'] is self.retry and rcpt['mode'] == mode and rcpt['subject'] == SUBJECT, f"exit code {rcpt['exit_code']}; " + elapsed()))
        def gates():
            names = sorted(p.name for p in (self.act / 'gpu-checks').iterdir()); listed = rcpt['gpu_check_files']
            ok = (sorted(x['name'] for x in listed) == names == sorted(['PRESTART.json'] + [f'{d}-RESPONSE.json' for d in self.gated]) and all(x['sha256'] == self.sha(self.act / 'gpu-checks' / x['name']) for x in listed)
                  and rcpt['power_log_sha256'] == self.sha(self.act / 'POWER_LOG.jsonl'))
            return ok, ', '.join(names)
        self.check("OWNER_EXIT_RECEIPT: its gate files' hashes equal the activation's gpu-checks; its power log hash equals POWER_LOG.jsonl", gates)
        pw = rcpt.get('power_during_run') or {}
        self.check('power during the run: on AC throughout, no change', lambda: (pw['off_ac_samples'] == 0 and not pw.get('changes'), f"{pw['samples']} readings"))
        self.check('the GPU check before each draw' + ('' if self.complete else ' started') + ' ended IDLE, none off AC',
                   lambda: ([g['stage'] for g in rcpt['gpu_gates']] == self.gated and all(g['verdict'] == 'IDLE' and g['off_ac_checks'] == 0 for g in rcpt['gpu_gates']),
                            ', '.join(f"{g['stage']} {g['verdict']} ({g['checks']})" for g in rcpt['gpu_gates'])))
        self.check("the run's gate records are byte copies of the activation's (prestart, and each draw's check)",
                   lambda: (self.sha(self.run / 'gpu-checks/PRESTART.json') == self.sha(self.act / 'gpu-checks/PRESTART.json') and all(self.sha(self.run / f'gpu-checks/{d}.json') == self.sha(self.act / f'gpu-checks/{d}-RESPONSE.json') for d in self.gated), ''))
        if self.complete:
            self.check("the worker's stdout and stderr logs are empty", lambda: ((self.act / 'WORKER_STDOUT.log').stat().st_size == 0 and (self.act / 'WORKER_STDERR.log').stat().st_size == 0, ''))
        else:
            def logs():
                last = [ln for ln in (self.act / 'WORKER_STDERR.log').read_text(encoding='utf-8').splitlines() if ln.strip()][-1]; e = t['error']
                return (self.act / 'WORKER_STDOUT.log').stat().st_size == 0 and last == f"{e['type']}: {e['message']}", f'stderr ends: {last[:80]}'
            self.check("the worker's stdout log is empty; its stderr log ends with the terminal's error (the traceback of the failure)", logs)
        def source():
            s = self.load(self.act / 'SOURCE_SUBJECT.json')
            return (self.sha(self.act / 'SOURCE_SUBJECT.json') == SUBJECT and all(self.sha(self.act / f['path']) == f['sha256'] for f in s['files'])
                    and not any(p.name == '__pycache__' for p in list(self.act.rglob('*')) + list(self.run.rglob('*')))), f"{len(s['files'])} files"
        self.check("the activation's source still matches the sealed subject; no bytecode folder in the activation or the run", source)
        print('      OWNER_PROGRESS.log:'); print('        ' + (self.act / 'OWNER_PROGRESS.log').read_text(encoding='utf-8').strip().replace('\n', '\n        '))

    def known_gap(self):
        """The known gap: the terminal's inventory exceeds the folder by one file; every stage receipt's ledger exceeds what was then on disk
        (the closed draw folders and the top-level files written before it) by the same file and bytes; cache\\ is now empty and was last
        changed after TERMINAL.json was written."""
        t, inv = self.t, self.t['inventory']; diff = (inv['files'] - self.inv_now[0], inv['bytes'] - self.inv_now[1])
        if diff == (0, 0): return dict(known=False, text='no difference')
        top = [p for p in self.run.iterdir() if p.is_file() and p.name != 'TERMINAL.json'] + [p for p in (self.run / 'gpu-checks').iterdir() if p.is_file()]
        ledgers, closed = [], [0, 0]
        for d in self.checked:
            fs = self.files(self.run / d); closed = [closed[0] + sum(p.stat().st_size for p in fs), closed[1] + len(fs)]
            r = self.load(self.run / f'{d}-RECEIPT.json'); when = (self.run / f'{d}-RECEIPT.json').stat().st_mtime_ns; before = [p for p in top if p.stat().st_mtime_ns < when]
            ledgers.append((r['ledger_total'][1] - closed[1] - len(before), r['ledger_total'][0] - closed[0] - sum(p.stat().st_size for p in before)))
        cache = self.run / 'cache'
        cache_ok = cache.is_dir() and not any(cache.iterdir()) and cache.stat().st_mtime_ns >= (self.run / 'TERMINAL.json').stat().st_mtime_ns
        lag = (cache.stat().st_mtime_ns - (self.run / 'TERMINAL.json').stat().st_mtime_ns) / 1e6 if cache.is_dir() else None
        known = diff[0] == 1 and diff[1] > 0 and bool(ledgers) and all(x == diff for x in ledgers) and cache_ok
        text = (f'{diff[0]} file, {diff[1]:,} bytes; every stage receipt\'s ledger carries the same ({"; ".join(f"{a} file, {b:,} bytes" for a, b in ledgers)}); '
                + (f'cache\\ is empty and was last changed {lag:,.0f} ms after TERMINAL.json' if cache.is_dir() else 'no cache\\ folder'))
        print(f'      inventory difference: {text}')
        return dict(known=known, text=text)

    def disk(self):
        print('--- disk')
        size = lambda root: sum(p.stat().st_size for p in self.files(root))
        run_b, act_b = size(self.run), size(self.act); states = sum(self.load(self.run / d / 'STATES_KEPT.json')['kept_bytes'] for d in self.checked)
        if self.active: states += self.t['states_on_failure']['kept_in_active_stage']['kept_bytes']
        du = shutil.disk_usage(self.study.anchor); later = 8 - self.k
        print(f'      runs\\n8-{self.mode.lower()}: {run_b:,} bytes ({run_b / 2**30:.3f} GiB), of which kept E0 states {states:,} ({states / 2**30:.3f} GiB)')
        print(f'      activations\\n8-{self.mode.lower()}: {act_b:,} bytes ({act_b / 2**20:.1f} MiB)')
        print(f'      {self.study.anchor} free: {du.free:,} bytes ({du.free / 2**30:.2f} GiB)')
        if self.complete and not self.retry:
            if later: print(f'      at this run\'s size, the {later} later run(s) leave about {(du.free - later * (run_b + act_b)) / 2**30:.2f} GiB free after R8 (floor {FLOOR / 2**30:.0f} GiB at each admission)')
        elif self.done:
            # A failed run, or a retry run: later runs of three draws at this run's size per complete draw (and, after a failed R<k>, its retry).
            folders = [size(self.run / d) for d in self.gated]; per_draw = sum(size(self.run / d) for d in self.done) / len(self.done); top = run_b - sum(folders); left = len(self.draws) - len(self.done)
            retry = left * per_draw + top + act_b if left and not self.retry else 0
            after = du.free - later * (3 * per_draw + top + act_b) - retry
            what = (f'the retry run X{self.k} ({left} draw(s)) and ' if retry else '') + f'the {later} later run(s)'
            if later or retry: print(f'      at {per_draw:,.0f} bytes per complete draw, {what} leave about {after / 2**30:.2f} GiB free after R8 (floor {FLOOR / 2**30:.0f} GiB at each admission)')


if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1:]))
