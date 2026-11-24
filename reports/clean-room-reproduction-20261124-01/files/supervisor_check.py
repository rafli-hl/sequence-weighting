"""Supervisor's check of the clean-room run: frozen hashes, file times against the freeze, and the transcript's tool calls."""
import datetime, hashlib, json, re, sys
from pathlib import Path

R = Path(sys.argv[1]); T = Path(sys.argv[2]); BS = chr(92)
fz = (R / 'FREEZE.txt').read_text(encoding='utf-8')
rows = [(h, rel.replace(BS, '/')) for h, rel in re.findall(r'^([0-9a-f]{64}) \*?(\S+)$', fz, re.M)]
bad = []; newest = 0
for h, rel in rows:
    p = R / rel
    if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest() != h: bad.append(rel)
    else: newest = max(newest, p.stat().st_mtime)
ts = lambda t: datetime.datetime.fromtimestamp(t, datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
print(f'{len(rows)} files named in FREEZE.txt; not matching now: {bad}')
print(f'newest frozen file last written {ts(newest)}; FREEZE.txt last written {ts((R / "FREEZE.txt").stat().st_mtime)}')
pub = [p for p in sorted((R / 'phase2').rglob('*')) if p.name in ('POINTS.csv', 'MATCHED.csv', 'FITS.csv', 'ANALYSIS.json')]
print('published tables on disk:', [(p.name, ts(p.stat().st_mtime), hashlib.sha256(p.read_bytes()).hexdigest()[:16]) for p in pub])

calls = []
for line in T.read_text(encoding='utf-8', errors='replace').splitlines():
    try: row = json.loads(line)
    except ValueError: continue
    msg = row.get('message') or {}
    content = msg.get('content') if isinstance(msg, dict) else None
    if not isinstance(content, list): continue
    for part in content:
        if isinstance(part, dict) and part.get('type') == 'tool_use':
            calls.append((row.get('timestamp', ''), part.get('name'), json.dumps(part.get('input'), ensure_ascii=False).replace(BS + BS, '/')))
print(len(calls), 'tool calls:', {n: sum(1 for c in calls if c[1] == n) for n in sorted({c[1] for c in calls})})
flags = {
    'drive D:': r'(?i)\bd:/|/mnt/d/|"/d/| /d/',
    "the owner's clone, Downloads or another Temp folder": r'(?i)rafli/sequence-weighting|Downloads|swa21|Temp/n8-',
    'git clone': r'git\s+(-c\s+\S+\s+)?clone',
    'a search tool without a path inside the working folder': None,
    'web search or web fetch tools': None,
}
for name, pat in flags.items():
    if name.startswith('a search tool'): hits = [c for c in calls if c[1] in ('Grep', 'Glob') and 'Temp/n7cr' not in c[2]]
    elif name.startswith('web search'): hits = [c for c in calls if c[1] in ('WebSearch', 'WebFetch')]
    else: hits = [c for c in calls if re.search(pat, c[2])]
    print(f'  {name}: {len(hits)}')
    for h in hits[:8]: print(f'      {h[0][11:19]} {h[1]}: {h[2][:260]}')
urls = {}
for c in calls:
    for u in re.findall(r'https?://[^\s"\']+', c[2]): urls.setdefault(u.rstrip('.,)'), c[0])
print('URLs in tool calls, with the time of their first use:')
for u, t in sorted(urls.items(), key=lambda x: x[1]): print('  ', t[11:19], u)
gh = [c for c in calls if re.search(r'\bgh\s', c[2])]
print('gh commands:')
for c in gh: print('  ', c[0][11:19], re.findall(r'gh\s[^;&|"]{0,140}', c[2])[:3])
