"""Build the one-use activation of an N8 run, R1-R8, or retry run, X1-X8 (N8-protocol-draft.md, sections 8 and 10). Native Python 3.12, -I -B.
Derived from N7's build_matched_activation.py.

  python -I -B build_n8_activation.py --mode R1..R8|X1..X8 --approval-id <OWNER-...> --user-text <TEXT>
  python -I -B build_n8_activation.py --fixture ...      refuses: fixture mode reads only what its caller passes to build()

Real mode writes only the mode's activation folder (matched_plan.ACTIVATIONS, under the study folder), which must not exist. It refuses
while this builder is not pinned to the sealed subject (EXPECTED_SUBJECT), while the registry and partition pins are PENDING, while the
pilot's log is not a PASS, and while the public registration of the subject is not recorded here (PUBLIC_REGISTRATION: its merge commit,
tag and the pilot log's hash): runs come only after the registration is merged and tagged (section 10). It copies the sealed source,
every file checked, and writes:
- REGISTRY.json, EXCLUSIONS.json and DRAW.json, each equal to its pin, the registry re-derived from its draw;
- FEWEPOCH_REGISTRY.json, PEAK_REGISTRY.json and N7_REGISTRY.json, equal to the three earlier studies' pins;
- PARTITION.json, re-derived from the corpus manifest and the four registries, equal to its pin and to the draw's own PARTITION.json,
  its groups disjoint;
- for X<k>, FIRST_ATTEMPT_TERMINAL.json: R<k>'s terminal, which must admit the retry (matched_worker.check_first_attempt), with R<k>'s
  stage receipts equal to its stage records (section 8);
- APPROVAL_RECORD.json and an enabled, one-use AUTHORIZATION.json binding all of them, with the run's draws.
It refuses a FIXTURE approval id in real mode. Fixture mode needs a FIXTURE id, a target outside the study folder and the closed record,
and its inputs and pins from the caller, so it never falls through to the real inputs. Real mode reads the corpus, which lies in the
closed record's work/runs/, so only the owner runs it. Nothing is run here: the owner then runs MATCHED_OWNER_RUN.ps1 from the activation.
"""
import argparse, hashlib, json, re, sys, time
sys.dont_write_bytecode = True
from pathlib import Path

ROOT = Path(r'D:\sequence-weighting-research')          # the closed record: earlier registries and the corpus, read only
STUDY = Path(r'D:\sequence-weighting-n8')
SOURCE = STUDY / 'source'
EXPECTED_SUBJECT = None                                  # PENDING: the sealed subject, set when the source is sealed (step 6)
PUBLIC_REGISTRATION = None                               # PENDING: dict(url, merge_commit, tag, source_subject_sha256, pilot_log_sha256), after the merge
PILOT_LOG = STUDY / 'pilot' / 'PILOT_LOG.json'
sys.path.insert(0, str(SOURCE))
import fewepoch_plan as fp, matched_plan as mp, matched_data as md, matched_registry as mr, wt103_corpus as wc     # stdlib; the framework is never imported
import matched_worker as mw
sha = lambda b: hashlib.sha256(b).hexdigest()
encoded = lambda x: (json.dumps(x, sort_keys=True, indent=2) + '\n').encode('utf-8')
REGISTRY_FILES = ('REGISTRY.json', 'EXCLUSIONS.json', 'DRAW.json')
TARGETS = {m: STUDY / p for m, p in mp.ACTIVATIONS.items()}


def pilot_log(path, registration):
    """The pilot's log: PASS, real, and the one the public registration names. Returns its hash; raises SystemExit otherwise."""
    if not Path(path).is_file(): raise SystemExit('No pilot log: run the pilot first (step 4)')
    raw = Path(path).read_bytes(); r = json.loads(raw)
    if r.get('status') != 'PASS' or r.get('fixture') is not False or not re.fullmatch(r'pilot-[0-9]{8}-[0-9]{2}', str(r.get('approval_id', ''))): raise SystemExit('The pilot did not pass, or is not real')
    if registration.get('pilot_log_sha256') != sha(raw): raise SystemExit('The public registration does not name this pilot log')
    return sha(raw)


def registered(record, expected):
    """The public registration: merged and tagged, with its commit recorded, and of this subject. Raises SystemExit otherwise."""
    if not record or not re.fullmatch('[0-9a-f]{40}', str(record.get('merge_commit'))) or not record.get('tag'): raise SystemExit('The public registration is not recorded: an activation comes only after it is merged and tagged')
    if record.get('source_subject_sha256') != expected: raise SystemExit('The public registration is of another source subject: a changed subject needs a new registration')


def real_inputs(mode):
    first = STUDY / mp.RUNS[mp.RETRY_OF[mode]] if mode in mp.RETRY_MODES else None
    return dict(registry=STUDY / mp.REGISTRY['directory'], corpus=ROOT / mp.CORPUS, fewepoch_registry=ROOT / fp.REGISTRY['directory'] / 'REGISTRY.json', peak_registry=ROOT / mp.PEAK_REGISTRY['directory'] / 'REGISTRY.json',
                n7_registry=ROOT / mp.N7_REGISTRY['directory'] / 'REGISTRY.json', first_attempt=first)


def check_inputs(mode, pins, inputs, source_hashes, subject=None, real=False):
    """The inputs against the pins. Returns the bytes to copy, the bindings and the run's draws."""
    raw = {n: (Path(inputs['registry']) / n).read_bytes() for n in REGISTRY_FILES}
    if (sha(raw['REGISTRY.json']), sha(raw['EXCLUSIONS.json']), sha(raw['DRAW.json'])) != (pins['registry_sha256'], pins['exclusions_sha256'], pins['draw_sha256']): raise SystemExit('Registry files differ from their pins')
    try: registry = mr.validate(json.loads(raw['REGISTRY.json']), raw['EXCLUSIONS.json'], raw['DRAW.json'], pins['corpus_manifest_sha256'], pins['fewepoch_partition_sha256'], pins['peak_partition_sha256'], pins['n7_partition_sha256'])
    except ValueError as e: raise SystemExit('Registry does not re-derive: ' + str(e))
    man_raw = (Path(inputs['corpus']) / 'CORPUS_MANIFEST.json').read_bytes()
    if len({sha(man_raw), pins['corpus_manifest_sha256'], registry['corpus_manifest_sha256']}) != 1: raise SystemExit('Corpus manifest differs from its pin')
    manifest = json.loads(man_raw)
    try: wc.validate_manifest(manifest, source_hashes)
    except (ValueError, KeyError) as e: raise SystemExit('Corpus manifest differs from the pre-registration: ' + str(e))
    if manifest.get('source_subject_sha256') != fp.ACQUISITION_SUBJECT: raise SystemExit('Corpus was not made by the approved acquisition source')
    if real and manifest.get('fixture') is not False: raise SystemExit('A fixture corpus cannot be used by a real activation')
    for split, m in manifest['splits'].items():
        b = (Path(inputs['corpus']) / m['file']).read_bytes()
        if len(b) != m['bytes'] or sha(b) != m['sha256']: raise SystemExit('Corpus file differs from its manifest: ' + split)
    if sha((Path(inputs['corpus']) / 'tokenizer.json').read_bytes()) != manifest['tokenizer']['sha256']: raise SystemExit('Tokenizer differs from its manifest')
    few_raw, peak_raw, n7_raw = (Path(inputs[k]).read_bytes() for k in ('fewepoch_registry', 'peak_registry', 'n7_registry'))
    for name, got, key in (('few-epoch', few_raw, 'fewepoch_registry_sha256'), ('peak', peak_raw, 'peak_registry_sha256'), ('N7', n7_raw, 'n7_registry_sha256')):
        if sha(got) != pins[key]: raise SystemExit(f'The {name} registry differs from its pin')
    try: assigned = md.assigned_articles(manifest, json.loads(few_raw)['partition_seed'], json.loads(peak_raw)['partition_seed'], json.loads(n7_raw)['partition_seed'],
                                         pins['fewepoch_partition_sha256'], pins['peak_partition_sha256'], pins['n7_partition_sha256'])
    except ValueError as e: raise SystemExit('An earlier partition: ' + str(e))
    partition = md.partition(manifest, assigned, registry['partition_seed']); part_raw = encoded(partition)
    if sha(part_raw) != pins['partition_sha256'] or registry.get('partition_sha256') != pins['partition_sha256']: raise SystemExit('Partition differs from its pin')
    if (Path(inputs['registry']) / 'PARTITION.json').read_bytes() != part_raw: raise SystemExit("Partition differs from the draw's own PARTITION.json")
    try: md.disjoint(partition, manifest, assigned)
    except PermissionError as e: raise SystemExit('Partition: ' + str(e))
    files = dict(raw, **{'PARTITION.json': part_raw, 'FEWEPOCH_REGISTRY.json': few_raw, 'PEAK_REGISTRY.json': peak_raw, 'N7_REGISTRY.json': n7_raw})
    bindings = dict(registry_sha256=pins['registry_sha256'], exclusions_sha256=pins['exclusions_sha256'], draw_sha256=pins['draw_sha256'], partition_sha256=sha(part_raw), corpus_manifest_sha256=pins['corpus_manifest_sha256'],
                    fewepoch_registry_sha256=pins['fewepoch_registry_sha256'], peak_registry_sha256=pins['peak_registry_sha256'], n7_registry_sha256=pins['n7_registry_sha256'])
    if mode in mp.RETRY_MODES:
        run = Path(inputs['first_attempt']); first = mp.RETRY_OF[mode]
        if not (run / 'TERMINAL.json').is_file(): raise SystemExit(f'Run {first} left no terminal, so it admits no retry')
        t_raw = (run / 'TERMINAL.json').read_bytes(); t = json.loads(t_raw)
        try: stages = mw.check_first_attempt(t_raw, mode, {k: bindings[k] for k in mw.INPUT_KEYS}, subject)
        except PermissionError as e: raise SystemExit(str(e))
        receipts = [d for d in mp.RUN_STAGES[first] if (run / f'{d}-RECEIPT.json').is_file() and json.loads((run / f'{d}-RECEIPT.json').read_bytes()).get('status') == 'COMPLETE']
        if receipts != mw.completed_draws(t): raise SystemExit(f"Run {first}'s receipts differ from its terminal's stage records")
        files['FIRST_ATTEMPT_TERMINAL.json'] = t_raw; bindings['first_attempt_terminal_sha256'] = sha(t_raw)
    else: stages = list(mp.RUN_STAGES[mode])
    return files, bindings, stages


def outside(p):
    p = Path(p).resolve()
    return all(p != r.resolve() and r.resolve() not in p.parents for r in (ROOT, STUDY))


def build(mode, target, approval_id, user_text, fixture, expected, source=SOURCE, pins=None, inputs=None, pilot=PILOT_LOG):
    """pins and inputs: fixture only; real mode always binds the plan pins (matched_worker.PINS) and the real inputs."""
    if mode not in mp.MODES: raise SystemExit('Mode must be one of R1-R8 or X1-X8')
    if not approval_id or not user_text or not user_text.strip(): raise SystemExit('Owner approval id and exact text are required')
    if (pins is not None or inputs is not None) and not fixture: raise SystemExit('Real mode binds the plan pins only')
    if (pins is None) != (inputs is None): raise SystemExit('Fixture pins need their input files')
    if fixture:
        if not approval_id.startswith('FIXTURE') or not outside(target): raise SystemExit('Fixture mode needs a FIXTURE id and a target outside the study folder and the closed record')
        if inputs is None: raise SystemExit('Fixture mode reads no real input: the caller must pass its pins and input files to build()')
    elif approval_id.upper().startswith('FIXTURE') or Path(target).resolve() != TARGETS[mode].resolve(): raise SystemExit('Real activation must be the bound path with a real approval')
    if expected is None: raise SystemExit('The builder is not pinned to a sealed N8 subject')
    if not fixture and (any(v is None for v in mw.PINS.values()) or not mp.pins_set()): raise SystemExit('The registry and partition pins are PENDING')
    if not fixture: registered(PUBLIC_REGISTRATION, expected)
    raw = (source / 'SOURCE_SUBJECT.json').read_bytes()
    if sha(raw) != expected: raise SystemExit('The N8 source subject differs from the pinned one')
    files = json.loads(raw)['files']; hashes = {}
    for f in files:
        b = (source / f['path']).read_bytes()
        if len(b) != f['bytes'] or sha(b) != f['sha256']: raise SystemExit('Changed N8 source: ' + f['path'])
        hashes[f['path']] = f['sha256']
    pilot_sha = None if fixture else pilot_log(pilot, PUBLIC_REGISTRATION)
    copies, bindings, stages = check_inputs(mode, mw.PINS if pins is None else pins, real_inputs(mode) if inputs is None else inputs, hashes, expected, real=not fixture)
    target = Path(target)
    if target.exists(): raise SystemExit('One-use activation exists; no rebuild')
    target.mkdir()
    for f in files:
        (target / f['path']).parent.mkdir(parents=True, exist_ok=True); (target / f['path']).write_bytes((source / f['path']).read_bytes())
    (target / 'SOURCE_SUBJECT.json').write_bytes(raw)
    for name, b in copies.items(): (target / name).write_bytes(b)
    approval = dict(kind=f'N8 run approval (Run {mode})', mode=mode, stages=stages, retry_of=mp.RETRY_OF.get(mode), approval_id=approval_id, user_text=user_text, fixture=bool(fixture), source_subject_sha256=expected,
                    builder_sha256=sha(Path(__file__).read_bytes()), pilot_log_sha256=pilot_sha, public_registration=None if fixture else dict(PUBLIC_REGISTRATION), seed_registry=dict(mp.REGISTRY), bindings=bindings,
                    created_local=time.strftime('%Y-%m-%d %H:%M:%S'), owner_launches_only=True)
    approval_raw = encoded(approval); (target / 'APPROVAL_RECORD.json').write_bytes(approval_raw)
    auth = dict(enabled=True, execution_ready=True, one_use=True, mode=mode, stages=stages, fixture=bool(fixture), approval_id=approval_id, source_subject_sha256=expected, approval_record_sha256=sha(approval_raw), **bindings)
    (target / 'AUTHORIZATION.json').write_bytes(encoded(auth))
    return dict(status='ARMED_UNUSED', mode=mode, stages=stages, activation=str(target), source_subject_sha256=expected, approval_record_sha256=sha(approval_raw), owner_command=f"& '{target}\\MATCHED_OWNER_RUN.ps1' -ExpectedSubject '{expected}'")


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--mode', required=True); ap.add_argument('--approval-id', required=True); ap.add_argument('--user-text', required=True); ap.add_argument('--fixture', action='store_true')
    a = ap.parse_args()
    if a.fixture: raise SystemExit('Fixture mode reads no real input: tests call build() with their own pins and inputs')
    print(json.dumps(build(a.mode, TARGETS.get(a.mode, STUDY / 'invalid-mode'), a.approval_id, a.user_text, False, EXPECTED_SUBJECT), indent=1))
