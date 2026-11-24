"""POST HOC audit script (area D). Reads only the auditor's clone. Checks:
 1. every hash pinned in X2_COMMAND.txt and RUN_COMMAND.ps1 against the published files;
 2. source/ against SOURCE_SUBJECT.json (path, bytes, sha256);
 3. which sealed files differ between the pilot's subject, the pre-pin subject and the sealed subject;
 4. the pilot's five seeds against the registry's exclusions and the registry's own seeds;
 5. the terminal hashes and other 64-hex strings in OPERATIONAL_NOTES.md: do they occur anywhere else in the repository?
"""
import hashlib, json, re, sys
from pathlib import Path
REPO = Path(sys.argv[1]); N8 = REPO / 'preregistration' / 'natural-text-dense-replication-20261114'
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()

print('== 1. hashes pinned in the owner commands')
pins = {'tools/build_n8_activation.py': 'c31fd4aa32873a1d025621f06bcc66e289c16ad86f64612c00dad76b1fd62904',
        'source/SOURCE_SUBJECT.json': '9bdea3a9715b05393afe6713ddc696834dd344c3485c4e1a6ed0fa222f44bb6b',
        'pilot/PILOT_LOG.json': '251d0951e30250afa16cb998b06550358c09234d8a24c45166b08d0642347db6'}
for name in ('X2_COMMAND.txt', 'RUN_COMMAND.ps1'):
    text = (N8 / name).read_text(encoding='utf-8')
    found = sorted(set(re.findall(r'\b[0-9a-f]{64}\b', text))); print(name, 'has', len(found), 'distinct 64-hex strings')
    for h in found:
        owner = [p for p, v in pins.items() if v == h]
        print('  ', h, '->', owner[0] + (' MATCHES published file' if sha(N8 / owner[0]) == h else ' DIFFERS from published file') if owner else 'not a published-file pin (see below)')
    print('   merge commit c6f98b26669f5d29f30c576b6d800c1fc82c98eb named:', 'c6f98b26669f5d29f30c576b6d800c1fc82c98eb' in text)
print('sha256 of the two commands and check_run.py as published:')
for name in ('X2_COMMAND.txt', 'RUN_COMMAND.ps1', 'check_run.py', 'OPERATIONAL_NOTES.md'): print('  ', name, sha(N8 / name))

print('== 2. source/ against SOURCE_SUBJECT.json')
subj = json.loads((N8 / 'source/SOURCE_SUBJECT.json').read_bytes())
bad = [f['path'] for f in subj['files'] if sha(N8 / 'source' / f['path']) != f['sha256'] or (N8 / 'source' / f['path']).stat().st_size != f['bytes']]
on_disk = sorted(p.relative_to(N8 / 'source').as_posix() for p in (N8 / 'source').rglob('*') if p.is_file())
listed = sorted(f['path'] for f in subj['files'])
print('   files listed', len(listed), '; changed:', bad, '; on disk but not listed:', sorted(set(on_disk) - set(listed)), '; listed but absent:', sorted(set(listed) - set(on_disk)))

print('== 3. subjects: pilot vs pre-pin vs sealed')
def table(p): return {f['path']: f['sha256'] for f in json.loads(Path(p).read_bytes())['files']}
sealed, pilot, prepin = table(N8 / 'source/SOURCE_SUBJECT.json'), table(N8 / 'seal/pilot/SOURCE_SUBJECT.json'), table(N8 / 'seal/pre-pin/SOURCE_SUBJECT.json')
print('   sha256 seal/pilot/SOURCE_SUBJECT.json  ', sha(N8 / 'seal/pilot/SOURCE_SUBJECT.json'))
print('   sha256 seal/pre-pin/SOURCE_SUBJECT.json', sha(N8 / 'seal/pre-pin/SOURCE_SUBJECT.json'))
for a, b, name in ((pilot, sealed, 'pilot -> sealed'), (prepin, sealed, 'pre-pin -> sealed'), (pilot, prepin, 'pilot -> pre-pin')):
    print('  ', name, ': differing', sorted(k for k in set(a) & set(b) if a[k] != b[k]), '; only in first', sorted(set(a) - set(b)), '; only in second', sorted(set(b) - set(a)))
for n in ('MATCHED_OWNER_RUN.ps1', 'matched_plan.py', 'README.md'):
    print('   seal/pre-pin/' + n, 'equals the pre-pin subject entry:', sha(N8 / 'seal/pre-pin' / n) == prepin.get(n))

print('== 4. the pilot seeds')
log = json.loads((N8 / 'pilot/PILOT_LOG.json').read_bytes()); seeds = log['seeds']
ex = json.loads((N8 / 'registry/n8-seed-registry/EXCLUSIONS.json').read_bytes()); reg = json.loads((N8 / 'registry/n8-seed-registry/REGISTRY.json').read_bytes())
def ints(o):
    if isinstance(o, bool): return
    if isinstance(o, int): yield o
    elif isinstance(o, dict):
        for v in o.values(): yield from ints(v)
    elif isinstance(o, list):
        for v in o: yield from ints(v)
exs, regs = set(ints(ex)), set()
for g in reg['groups']: regs |= {v for k, v in g.items() if k != 'group' and isinstance(v, int)}
regs |= set(ints(reg.get('benchmark', {}))); regs.add(reg.get('partition_seed'))
print('   pilot seeds:', seeds)
print('   each in EXCLUSIONS.json:', {k: v in exs for k, v in seeds.items()})
print('   any among the registry seeds:', sorted(set(seeds.values()) & regs))
print('   pilot log keys with "loss":', [k for k in log if 'loss' in k.lower()], '; loss_read =', log.get('loss_read'), '; p_star_fitted =', log.get('p_star_fitted'), '; run_folder_deleted =', log.get('run_folder_deleted'))
print('   registry groups:', len(reg['groups']), [g['group'] for g in reg['groups']][:3], '...', reg['groups'][-1]['group'])

print('== 5. 64-hex strings of OPERATIONAL_NOTES.md elsewhere in the repository')
notes = (N8 / 'OPERATIONAL_NOTES.md').read_text(encoding='utf-8')
hexes = sorted(set(re.findall(r'\b[0-9a-f]{64}\b', notes)))
texts = {}
for p in REPO.rglob('*'):
    if p.is_file() and '.git' not in p.parts and p.stat().st_size < 20_000_000:
        try: texts[p.relative_to(REPO).as_posix()] = p.read_bytes()
        except OSError: pass
for h in hexes:
    where = sorted(k for k, b in texts.items() if h.encode() in b)
    print('  ', h, '->', where)
