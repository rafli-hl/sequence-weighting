"""The owner-run seed draw of the dense-readout replication, N8 (N8-protocol-draft.md, section 4; the brief's step 5). Native Windows
Python 3.12, -I -B. One use; no redraw. Derived from N7's run_seed_draw.py.

  python.exe -I -B n8_seed_draw.py --approval-id <OWNER-YYYYMMDD-...> --expected-subject <sha256 of source/SOURCE_SUBJECT.json>

Under the closed record's work/runs/ it reads one file, the corpus manifest, by its exact path, and writes nothing there. An audit hook in
this process enforces that: any other open or listing of a path holding work/runs, or a mkdir, rename, link, remove or copy touching one,
stops the script, at any depth, and so does starting a process or opening a connection. The hook sees no stat-type call (is_file, exists)
and no open through ctypes; nothing the draw reaches opens a file that way. Everything that happens after the claim up to the entropy draw
runs once under the hook before any claim, so a breach or a missing file there stops the script with nothing claimed.

Steps: the hook; the N8 source against the subject given; the pilot's log; a dry run of the exclusions, whose census walks the closed
record (work/runs pruned) and the N8 study folder (read in full, or refused), and which must hold the pilot's five seeds;
matched_registry.draw, which checks the frozen policy against its pin, makes the one claim and the one entropy draw, and writes the
registry and the partition in registry/n8-seed-registry/; then the post-draw checks and disclosure (n8_post_draw.py), from the manifest
only; then SEED_DRAW_RECEIPT.json, with what the hook saw.

It prints hashes, the 98 seed values, article and sequence counts, check results and tie counts. No loss, gain or p* exists at this point,
and none is read.

If the draw stands and a later step fails or is interrupted, the script says so and exits non-zero. There is no redraw, and the next step
is the owner's decision. If the post-draw step left no check record, --disclosure-only runs it once, under the same hook, with no draw.
"""
import argparse, hashlib, json, os, platform, re, sys, time
sys.dont_write_bytecode = True
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = Path(r'D:\sequence-weighting-research'); STUDY = Path(r'D:\sequence-weighting-n8'); SRC = STUDY / 'source'; REG_DIR = STUDY / 'registry/n8-seed-registry'
MANIFEST = ROOT / 'work/runs/natural-text-corpus-wt103-20261101-01/CORPUS_MANIFEST.json'
PILOT_LOG = STUDY / 'pilot/PILOT_LOG.json'
APPROVAL_ID = re.compile(r'OWNER-[0-9]{8}-[A-Z0-9-]{2,60}')
WORK_RUNS = re.compile(r'/work/runs(/|$)')
PATH_EVENTS = ('open', 'os.listdir', 'os.scandir', 'glob.glob', 'os.mkdir', 'os.rename', 'os.link', 'os.symlink', 'os.remove', 'os.rmdir', 'os.truncate', 'os.chmod', 'os.utime', 'shutil.copyfile', 'shutil.copytree', 'shutil.move', 'shutil.rmtree')
NO_PROCESS_OR_NETWORK = ('subprocess.Popen', 'os.system', 'os.exec', 'os.spawn', 'os.posix_spawn', 'os.startfile', 'socket.connect', 'socket.getaddrinfo', 'urllib.Request')
WRITE_FLAGS = os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND
sha = lambda b: hashlib.sha256(b).hexdigest()
encoded = lambda x: (json.dumps(x, sort_keys=True, indent=2, allow_nan=False) + '\n').encode('utf-8')


class RuleBroken(BaseException):
    """Not an Exception, so that nothing on the way, such as the census's handling of unreadable files, can catch it."""


def norm(p): return os.path.abspath(os.fsdecode(p)).replace('\\', '/').lower()


def install_guard(allowed):
    """From here on, in this process, the one path under work/runs that may be touched is `allowed`, and only to read it. Returns the log the hook keeps."""
    allowed = norm(allowed); log = dict(manifest_reads=0, stopped_at=None)
    def hook(event, args):
        if event in NO_PROCESS_OR_NETWORK:
            log['stopped_at'] = event; raise RuleBroken(f'{event}: this script starts no process and opens no connection')
        if event in PATH_EVENTS:
            for a in args[:1 if event == 'open' else 2]:
                if not isinstance(a, (str, bytes, os.PathLike)): continue
                s = norm(a)
                if not WORK_RUNS.search(s): continue
                if event == 'open' and s == allowed and not set(str(args[1] or '')) & set('wax+') and not (args[2] or 0) & WRITE_FLAGS: log['manifest_reads'] += 1; continue
                log['stopped_at'] = f'{event} {s}'; raise RuleBroken(f'{event} of a path holding work/runs: {s}')
    sys.addaudithook(hook); return log


def verify_source(src, expected):
    """The N8 source against the subject given, every file, with nothing added and the authorization disabled."""
    if not re.fullmatch('[0-9a-f]{64}', str(expected)): raise SystemExit('No source subject to check against; nothing claimed')
    raw = (src / 'SOURCE_SUBJECT.json').read_bytes()
    if sha(raw) != expected: raise SystemExit('The source subject differs from the one given; nothing claimed')
    subject = json.loads(raw); want = {row['path']: row for row in subject['files']}
    for path, row in want.items():
        b = (src / path).read_bytes()
        if len(b) != row['bytes'] or sha(b) != row['sha256']: raise SystemExit('Changed source ' + path + '; nothing claimed')
    present = {p.relative_to(src).as_posix() for p in src.rglob('*') if p.is_file()}
    if present != set(want) | {'SOURCE_SUBJECT.json', 'AUTHORIZATION.json'}: raise SystemExit(f'Unexpected source files: {sorted(present ^ (set(want) | {"SOURCE_SUBJECT.json", "AUTHORIZATION.json"}))}; nothing claimed')
    auth = (src / 'AUTHORIZATION.json').read_bytes()
    if json.loads(auth).get('enabled') is not False or sha(auth) != subject['disabled_authorization_sha256']: raise SystemExit('The source authorization must be the disabled one the subject binds; nothing claimed')
    return subject


def import_paths(src):
    for p in (str(HERE), str(src / 'vendor'), str(src)):
        if p not in sys.path: sys.path.insert(0, p)


def post_draw(pdd, approval_id, log, manifest, reg_dir, expected_subject, registry_sha256, partition_sha256, receipt_name, disclose_kwargs, out):
    """The post-draw checks and disclosure, and the receipt. Whatever stops them, the draw stands and the receipt is written."""
    code = 0
    try:
        rec = pdd.run(reg_dir, manifest, out=out, **(disclose_kwargs or {}))
        if not rec['all_pass']: code = 3; out('A post-draw check failed. The draw stands, with no redraw; the next step is the owner decision.')
    except BaseException as e:
        rec = None; code = 3; out(f'The post-draw step stopped: {type(e).__name__}: {str(e)[:300]}. The draw stands, with no redraw; the next step is the owner decision.')
    receipt = dict(schema=1, purpose='The owner-run seed draw of N8: what ran, and what the hook saw', approval_id=approval_id, source_subject_sha256=expected_subject, draw_script_sha256=sha(Path(__file__).read_bytes()),
                   disclosure_script_sha256=sha((HERE / 'n8_post_draw.py').read_bytes()), corpus_manifest_path=str(manifest), guard=dict(log), registry_sha256=registry_sha256, partition_sha256=partition_sha256,
                   post_draw_all_pass=None if rec is None else rec['all_pass'], python=platform.python_version(), finished_local=time.strftime('%Y-%m-%d %H:%M:%S'))
    raw = encoded(receipt); (Path(reg_dir) / receipt_name).write_bytes(raw)
    out(f"Under work/runs/ the script read the manifest {log['manifest_reads']} times and nothing else. Receipt {sha(raw)}")
    return code


def disclosure_only(approval_id, log, expected_subject, manifest=MANIFEST, reg_dir=REG_DIR, src=SRC, disclose_kwargs=None, out=print):
    """The post-draw step, once, if the draw left no check record. No draw. A check record that exists stands, whether or not it passed."""
    verify_source(src, expected_subject); reg_dir = Path(reg_dir)
    if not (reg_dir / 'REGISTRY.json').is_file(): raise SystemExit('No registry exists; there is nothing to disclose')
    if (reg_dir / 'REGISTRY_AND_PARTITION_CHECK.json').exists(): raise SystemExit('The post-draw check record exists; it stands')
    import_paths(src); import n8_post_draw as pdd
    raw = (reg_dir / 'REGISTRY.json').read_bytes(); reg = json.loads(raw)
    if reg.get('approval_id') != approval_id: raise SystemExit('The registry is under another approval')
    name = 'SEED_DRAW_RECEIPT-disclosure-only.json' if (reg_dir / 'SEED_DRAW_RECEIPT.json').exists() else 'SEED_DRAW_RECEIPT.json'
    return post_draw(pdd, approval_id, log, manifest, reg_dir, expected_subject, sha(raw), reg['partition_sha256'], name, disclose_kwargs, out)


def run(approval_id, log, expected_subject, manifest=MANIFEST, reg_dir=REG_DIR, src=SRC, pilot_log=PILOT_LOG, draw_kwargs=None, disclose_kwargs=None, out=print):
    """Everything after the hook. The keyword arguments after expected_subject are for the native tests; the command line passes none of them."""
    verify_source(src, expected_subject); out(f'N8 source: {expected_subject}, every file checked')
    import_paths(src); import matched_registry as mr, n8_post_draw as pdd
    draw_kwargs = draw_kwargs or {}
    if not Path(pilot_log).is_file(): raise SystemExit("The pilot's log is missing, so its seeds cannot be shown excluded; nothing claimed")
    pilot_seeds = json.loads(Path(pilot_log).read_bytes())['seeds']
    values, prov = mr.exclusions(draw_kwargs.get('root', mr.ROOT), (), draw_kwargs.get('study', mr.STUDY)); sc = prov['study_census']
    out(f"Dry run of the exclusions, before any claim: {len(values)} values, {prov['census_values']} of them from the censuses: {prov['json_files_with_values']} files in the closed record "
        f"({prov['unreadable_count']} unreadable) and {sc['json_files_with_values']} in the study folder ({sc['unreadable_count']} unreadable); the hook stopped nothing.")
    missing = sorted(k for k, v in pilot_seeds.items() if v not in set(values))
    if len(pilot_seeds) != 5 or missing: raise SystemExit(f"The exclusions do not hold the pilot's five seeds (missing: {missing}); nothing claimed")
    out("The pilot's five seeds are among the exclusions.")
    reg, digest = mr.draw(reg_dir, manifest, approval_id, **draw_kwargs)
    out(json.dumps(dict(registry_sha256=digest, partition_seed=reg['partition_seed'], partition_sha256=reg['partition_sha256'], groups=reg['groups'], benchmark=reg['benchmark'], fresh_pool=reg['fresh_pool']), indent=1))
    return post_draw(pdd, approval_id, log, manifest, reg_dir, expected_subject, digest, reg['partition_sha256'], 'SEED_DRAW_RECEIPT.json', disclose_kwargs, out)


def main(argv=None):
    a = argparse.ArgumentParser(); a.add_argument('--approval-id', required=True); a.add_argument('--expected-subject', required=True); a.add_argument('--disclosure-only', action='store_true'); args = a.parse_args(argv)
    if not APPROVAL_ID.fullmatch(args.approval_id) or args.approval_id.upper().startswith('FIXTURE'): raise SystemExit('An owner approval id (OWNER-YYYYMMDD-..., never FIXTURE) is required; nothing claimed')
    if not re.fullmatch('[0-9a-f]{64}', args.expected_subject): raise SystemExit('The expected subject must be a SHA-256; nothing claimed')
    log = install_guard(MANIFEST)
    try: return disclosure_only(args.approval_id, log, args.expected_subject) if args.disclosure_only else run(args.approval_id, log, args.expected_subject)
    except RuleBroken as e:
        sys.stderr.write(f'STOPPED by the rule on work/runs/: {e}\n'); return 2


if __name__ == '__main__':
    raise SystemExit(main())
