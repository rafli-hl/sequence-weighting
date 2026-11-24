"""Post hoc: every hash in N8's HASHES.json against the published file it names, where that file is published.
    python -I -B hashes_equivalent.py <N8 folder>"""
import hashlib, json, sys
from pathlib import Path
N = Path(sys.argv[1]); H = json.loads((N / 'HASHES.json').read_bytes())
sys.path.insert(0, str(N / 'tools')); sys.dont_write_bytecode = True
import write_hashes as wh
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
ok, differ, absent = [], [], []
for k, rel in wh.FILES.items():
    p = N / rel
    (absent if not p.is_file() else ok if sha(p) == H[f'{k}_sha256'] else differ).append((k, rel))
for g in wh.GROUPS:
    for rel, want in H[g].items():
        p = N / rel
        (absent if not p.is_file() else ok if sha(p) == want else differ).append((g, rel))
    extra = sorted(q.relative_to(N).as_posix() for q in (N / wh.GROUPS[g]).rglob('*') if q.is_file() and '__pycache__' not in q.parts and q.name != 'SOURCE_SUBJECT.json' and q.relative_to(N).as_posix() not in H[g]) if (N / wh.GROUPS[g]).is_dir() else []
    if extra: print('published but not in HASHES.json group', g, extra)
print(f'{len(ok)} named files match; {len(differ)} differ; {len(absent)} not published')
for k, rel in differ: print('  DIFFERS', k, rel, 'published', sha(N / rel)[:16], 'HASHES.json', (H.get(f'{k}_sha256') or H[k][rel])[:16])
for k, rel in absent: print('  NOT PUBLISHED', k, rel)
reg = json.loads((N / 'registry/n8-seed-registry/REGISTRY.json').read_bytes())
print('corpus_manifest, approval_id, n7_partition equal the registry:', all(H[k] == reg[k] for k in ('corpus_manifest_sha256', 'approval_id', 'n7_partition_sha256')))
s = json.loads((N / 'source/SOURCE_SUBJECT.json').read_bytes())
bad = [f['path'] for f in s['files'] if sha(N / 'source' / f['path']) != f['sha256'] or (N / 'source' / f['path']).stat().st_size != f['bytes']]
print(f"source subject {sha(N / 'source/SOURCE_SUBJECT.json')}; {len(s['files'])} sealed files, {len(bad)} differ from SOURCE_SUBJECT.json")
print('other keys in HASHES.json:', sorted(k for k in H if not k.endswith('_sha256') and k not in wh.GROUPS))
