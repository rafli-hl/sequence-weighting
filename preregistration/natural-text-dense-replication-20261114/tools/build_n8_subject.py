"""Seal N8's study source (N8-protocol-draft.md). Native Python 3.12, -I -B. Derived from N7's build_matched_subject.py.

  python -I -B build_n8_subject.py <N7_SEALED_SOURCE> <CLOSED_RECORD_ROOT>      -> source/SOURCE_SUBJECT.json

N7_SEALED_SOURCE is preregistration/natural-text-matched-confirmation-20261104/sealed-source/ of the closed record (subject 7ef133ad...);
CLOSED_RECORD_ROOT holds the bound records under reports/. Both are only read. It refuses unless N7's source is its sealed subject, every
reused file is a byte copy of it, n7_matched_data.py is a byte copy of N7's matched_data.py, the source AUTHORIZATION.json is disabled,
the files are exactly the expected ones, and matched_registry.py and matched_plan.py both pin the frozen seed policy
(registry/n8-seed-registry/SEED_REGISTRY_POLICY.md). The subject binds the records the study depends on, and records the seed registry
and the partition:
- PENDING_OWNER_DRAW while the plan's registry pins are None. This pending seal refuses once the registry is drawn, and it keeps copies of
  SOURCE_SUBJECT.json, matched_plan.py, README.md and MATCHED_OWNER_RUN.ps1 in seal/pre-pin/;
- DRAWN, with their hashes, once the plan pins the drawn registry and partition, and only after the post-draw revision: against the
  pending seal in seal/pre-pin/ (whose copies must equal the hashes it records), only the plan's registry and partition pins, the README's
  two status lines and the owner script's hours line and start message (the owner's decision of 14 Nov 2026) changed, every bound record
  and the disabled authorization are as they were, and the draw ran on this registry source.
Nothing here opens anything under work/runs/.
"""
import hashlib, json, re, sys
from pathlib import Path

STUDY = Path(__file__).resolve().parents[1]
REGISTRY_DIR = 'registry/n8-seed-registry'
PRE_PIN = 'seal/pre-pin'
N7_SUBJECT = '7ef133ad0120d0852c93ebe65f020718f51cebbf75abd43c29f89cdec8674f56'
FROM_N7 = ('a1_download.py', 'a2_rows.py', 'acquire_common.py', 'acquire_plan.py', 'fewepoch_analysis.py', 'fewepoch_data.py', 'fewepoch_plan.py', 'fewepoch_registry.py', 'fewepoch_worker.py', 'peak_data.py',
           'text_analysis.py', 'text_data.py', 'text_engine.py', 'text_framework_setup.py', 'text_model.py', 'text_plan.py', 'text_registry.py', 'text_worker.py', 'wt103_corpus.py', 'vendor/core.py',
           'ORIGINAL_ENVIRONMENT.json', 'gpu_check.ps1', 'GPU_CHECK.json', 'power_gate.ps1')
CHANGED_FROM_N7 = ('matched_plan.py', 'matched_data.py', 'matched_registry.py', 'matched_worker.py', 'MATCHED_OWNER_RUN.ps1', 'README.md')
NEW = ('n7_matched_data.py',)                 # a byte copy of N7's matched_data.py
DROPPED_FROM_N7 = ('matched_analysis.py', 'PROTOCOL.md')
BOUND = ('reports/natural-text-fewepoch-seed-registry-20261101-01/REGISTRY.json', 'reports/natural-text-peak-seed-registry-20261103-01/REGISTRY.json',
         'reports/natural-text-matched-seed-registry-20261104-01/REGISTRY.json', 'reports/natural-text-peak-analysis-approval-20261103-01/pinned-records/LR_SELECTION.json',
         'reports/natural-text-matched-analysis-20261105-01/ANALYSIS.json')
PILOT = ("One pilot draw, on N7's m01 with throwaway seeds, ran on source subject `9743b179…`, which differs from this source only in the pins of `matched_plan.py` and "
         "`matched_registry.py`, the hours in `MATCHED_OWNER_RUN.ps1` and this README; it was then discarded (`../pilot/PILOT_LOG.json`).")
README_PENDING = ("**This package has not run.** No seed of this study has been drawn, no activation exists, and none of this study's draws has been trained. " + PILOT + " No data of this study exists.\n",
                  "**SEALED_DISABLED:** `AUTHORIZATION.json` is disabled. The seed policy is frozen (`../registry/n8-seed-registry/SEED_REGISTRY_POLICY.md`), and `matched_registry.py` and `matched_plan.py` pin it. "
                  "The seed registry and the partition do not exist yet, so their pins in `matched_plan.py` are PENDING and `SOURCE_SUBJECT.json` records them as PENDING_OWNER_DRAW. The worker and the builder refuse "
                  "real mode until a pin-only revision sets them.\n")
README_DRAWN = ("**This package has not run.** The seeds have been drawn by the owner, but no activation exists, and none of this study's draws has been trained. " + PILOT + " No loss, gain or p\\* of this study exists.\n",
                "**SEALED_DISABLED:** `AUTHORIZATION.json` is disabled. The seed policy is frozen, and the seed registry and the partition exist (`../registry/n8-seed-registry/`); `matched_plan.py` pins them, "
                "and `SOURCE_SUBJECT.json` records them as DRAWN. The builder still refuses real mode without the public registration of this subject.\n")
OWNER_PENDING = ("$hours='about 2.1'\n", "Write-Host ('Starting Run '+$mode+' ('+$m.hours+' hours; at most 6). ")
OWNER_DRAWN = ("$hours='about 2.3 h wall time (2.1 h on the worker clock)'\n", "Write-Host ('Starting Run '+$mode+' ('+$m.hours+'; at most 6 h on the worker clock). ")
PRE_PIN_COPIES = ('matched_plan.py', 'README.md', 'MATCHED_OWNER_RUN.ps1')
PLAN_PINS = (r"(?m)^( {16}registry_sha256=)'[0-9a-f]{64}'", r"(?m)^( {16}exclusions_sha256=)'[0-9a-f]{64}'", r"(?m)^( {16}draw_sha256=)'[0-9a-f]{64}'", r"(?m)^( {16}approval_id=)'[A-Z0-9-]+'",
             r"(?m)^(PARTITION_SHA256 = )'[0-9a-f]{64}'")
sha = lambda b: hashlib.sha256(b).hexdigest()


def policy_pin(src, reg_dir):
    """The frozen policy's hash, which matched_registry.py and matched_plan.py must both pin. Raises SystemExit otherwise."""
    if not (reg_dir / 'SEED_REGISTRY_POLICY.md').is_file(): raise SystemExit('The frozen seed policy is not in the registry folder')
    h = sha((reg_dir / 'SEED_REGISTRY_POLICY.md').read_bytes())
    in_tool = re.findall(r"(?m)^POLICY_SHA256 = '([0-9a-f]{64})'", (src / 'matched_registry.py').read_text(encoding='utf-8'))
    in_plan = re.findall(r"(?m)^ {16}policy_sha256='([0-9a-f]{64})',", (src / 'matched_plan.py').read_text(encoding='utf-8'))
    if in_tool != [h] or in_plan != [h]: raise SystemExit('matched_registry.py and matched_plan.py must both pin the frozen seed policy')
    return h


def unpinned(plan_text):
    """The plan with its registry and partition pins set back to None."""
    for pattern in PLAN_PINS: plan_text = re.sub(pattern, r'\g<1>None', plan_text)
    return plan_text


def revised(text, pending, drawn, what):
    """text with each pending line replaced by its drawn line; each pending line must occur exactly once."""
    for a, b in zip(pending, drawn):
        if text.count(a) != 1: raise SystemExit(f'The pending {what} does not hold its lines')
        text = text.replace(a, b)
    return text


def pin_only(src, reg, pre_pin, record):
    """The revision after the draw may change only the plan's registry and partition pins, the README's two status lines and the owner
    script's hours line and start message; every bound record and the disabled authorization stay as the pending seal has them; and the
    draw must have run on this registry source. Raises SystemExit otherwise."""
    if not (pre_pin / 'SOURCE_SUBJECT.json').is_file(): raise SystemExit('The pending seal is not kept, so a pin-only revision cannot be shown')
    old = json.loads((pre_pin / 'SOURCE_SUBJECT.json').read_bytes()); recorded = {f['path']: f['sha256'] for f in old['files']}
    if any(not (pre_pin / f).is_file() or sha((pre_pin / f).read_bytes()) != recorded[f] for f in PRE_PIN_COPIES): raise SystemExit('The copies in seal/pre-pin/ differ from the pending seal')
    changed = sorted(p for p, h in recorded.items() if sha((src / p).read_bytes()) != h)
    if changed != ['MATCHED_OWNER_RUN.ps1', 'README.md', 'matched_plan.py']: raise SystemExit(f'Not a pin-only revision: {changed}')
    if unpinned((src / 'matched_plan.py').read_text(encoding='utf-8')).encode('utf-8') != (pre_pin / 'matched_plan.py').read_bytes(): raise SystemExit('Not a pin-only revision: the plan differs beyond its pins')
    if revised((pre_pin / 'README.md').read_bytes().decode('utf-8'), README_PENDING, README_DRAWN, 'README').encode('utf-8') != (src / 'README.md').read_bytes():
        raise SystemExit('Not a pin-only revision: the README differs beyond its status lines')
    if revised((pre_pin / 'MATCHED_OWNER_RUN.ps1').read_bytes().decode('utf-8'), OWNER_PENDING, OWNER_DRAWN, 'owner script').encode('utf-8') != (src / 'MATCHED_OWNER_RUN.ps1').read_bytes():
        raise SystemExit('Not a pin-only revision: the owner script differs beyond its hours')
    moved = [p for p, h in old['bound_records'].items() if sha((record / p).read_bytes()) != h]
    if moved: raise SystemExit(f'Not a pin-only revision: a bound record changed: {moved}')
    if sha((src / 'AUTHORIZATION.json').read_bytes()) != old['disabled_authorization_sha256']: raise SystemExit('Not a pin-only revision: the authorization changed')
    differs = [f for f, h in reg['registry_source_sha256'].items() if sha((src / f).read_bytes()) != h]
    if differs: raise SystemExit(f'The draw ran on other registry source: {differs}')


def seal(n7, record, src=None, study=STUDY):
    src = study / 'source' if src is None else src; reg_dir, pre_pin = study / REGISTRY_DIR, study / PRE_PIN
    n7_raw = (n7 / 'SOURCE_SUBJECT.json').read_bytes()
    if sha(n7_raw) != N7_SUBJECT: raise SystemExit("N7's source subject differs")
    n7_files = {f['path']: f['sha256'] for f in json.loads(n7_raw)['files']}
    if any(sha((n7 / f).read_bytes()) != h for f, h in n7_files.items()): raise SystemExit("N7's sealed source differs from its subject")
    present = sorted(p.relative_to(src).as_posix() for p in src.rglob('*') if p.is_file())
    expected = sorted(FROM_N7 + CHANGED_FROM_N7 + NEW + ('AUTHORIZATION.json',))
    if sorted(set(present) - {'SOURCE_SUBJECT.json'}) != expected: raise SystemExit(f'Unexpected N8 source files: {sorted(set(present) ^ set(expected + ["SOURCE_SUBJECT.json"]))}')
    for f in FROM_N7:
        if (src / f).read_bytes() != (n7 / f).read_bytes() or sha((src / f).read_bytes()) != n7_files[f]: raise SystemExit('Not a byte copy of N7 source: ' + f)
    if (src / 'n7_matched_data.py').read_bytes() != (n7 / 'matched_data.py').read_bytes(): raise SystemExit("n7_matched_data.py is not a byte copy of N7's matched_data.py")
    for f in CHANGED_FROM_N7:
        if (src / f).read_bytes() == (n7 / f).read_bytes(): raise SystemExit('Listed as changed but identical to N7: ' + f)
    auth = (src / 'AUTHORIZATION.json').read_bytes(); a = json.loads(auth)
    if a.get('enabled') is not False or a.get('execution_ready') is not False: raise SystemExit('Source authorization must be disabled')
    policy = policy_pin(src, reg_dir); plan_text = (src / 'matched_plan.py').read_text(encoding='utf-8')
    pending = unpinned(plan_text) == plan_text; drawn = (reg_dir / 'REGISTRY.json').exists()
    if pending:
        if drawn: raise SystemExit('The registry is drawn: the plan must pin it, in a pin-only revision')
        if any((src / 'README.md').read_text(encoding='utf-8').count(line) != 1 for line in README_PENDING): raise SystemExit('The README does not hold the pending status lines')
        if any((src / 'MATCHED_OWNER_RUN.ps1').read_text(encoding='utf-8').count(line) != 1 for line in OWNER_PENDING): raise SystemExit('The owner script does not hold the pending hours lines')
        registry = dict(status='PENDING_OWNER_DRAW', policy_sha256=policy, registry_sha256=None, exclusions_sha256=None, draw_sha256=None, partition_sha256=None)
    else:
        if not drawn or not (reg_dir / 'PARTITION.json').exists(): raise SystemExit('The plan pins a registry, but the registry or its partition is not there')
        reg = json.loads((reg_dir / 'REGISTRY.json').read_bytes())
        registry = dict(status='DRAWN', policy_sha256=policy, registry_sha256=sha((reg_dir / 'REGISTRY.json').read_bytes()), exclusions_sha256=sha((reg_dir / 'EXCLUSIONS.json').read_bytes()),
                        draw_sha256=sha((reg_dir / 'DRAW.json').read_bytes()), partition_sha256=sha((reg_dir / 'PARTITION.json').read_bytes()), approval_id=reg['approval_id'])
        if reg.get('policy_sha256') != policy: raise SystemExit('The registry was drawn under another policy')
        for key in ('registry_sha256', 'exclusions_sha256', 'draw_sha256'):
            if re.findall(rf"(?m)^ {{16}}{key}='([0-9a-f]{{64}})'", plan_text) != [registry[key]]: raise SystemExit(f'The plan does not pin this registry ({key})')
        if re.findall(r"(?m)^ {16}approval_id='([A-Z0-9-]+)'", plan_text) != [registry['approval_id']] or re.findall(r"(?m)^PARTITION_SHA256 = '([0-9a-f]{64})'", plan_text) != [registry['partition_sha256']] \
                or reg.get('partition_sha256') != registry['partition_sha256']: raise SystemExit('The plan does not pin this approval id and partition')
        pin_only(src, reg, pre_pin, record)
    files = [dict(path=f, bytes=len((src / f).read_bytes()), sha256=sha((src / f).read_bytes())) for f in sorted(FROM_N7 + CHANGED_FROM_N7 + NEW)]
    subject = dict(schema=1, kind='dense-readout replication source, N8 (WikiText-103, widths 512 and 768 at 1e-4, 3.5 epochs, readouts every 64 updates from update 2,048 to 3,584; H1 and H2)',
                   files=files, byte_copies_of_n7_source={f: N7_SUBJECT for f in FROM_N7}, byte_copy_of_n7_matched_data=dict(path='n7_matched_data.py', n7_path='matched_data.py', n7_subject=N7_SUBJECT),
                   changed_from_n7=list(CHANGED_FROM_N7), new_files=list(NEW), dropped_from_n7=list(DROPPED_FROM_N7), disabled_authorization_sha256=sha(auth),
                   bound_records={p: sha((record / p).read_bytes()) for p in BOUND}, seed_registry_and_partition=registry, pins_pending=pending, status='SEALED_DISABLED', runtime_authorized=False, has_run=False)
    raw = (json.dumps(subject, sort_keys=True, indent=2) + '\n').encode('utf-8')
    (src / 'SOURCE_SUBJECT.json').write_bytes(raw)
    if pending:
        pre_pin.mkdir(parents=True, exist_ok=True)
        (pre_pin / 'SOURCE_SUBJECT.json').write_bytes(raw)
        for name in PRE_PIN_COPIES: (pre_pin / name).write_bytes((src / name).read_bytes())
    return sha(raw)


if __name__ == '__main__':
    if len(sys.argv) != 3: raise SystemExit(__doc__)
    print('subject', seal(Path(sys.argv[1]), Path(sys.argv[2])))
