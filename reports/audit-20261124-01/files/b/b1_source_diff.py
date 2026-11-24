"""POST HOC audit script (auditor B). Reads only the clone at v2.1.
1. File-by-file comparison of N8 source/ against N7 sealed-source/ (SHA-256 over bytes).
2. SOURCE_SUBJECT.json against the files (bytes, sha256, coverage, lists).
3. CHANGES.md: 'Unchanged', 'Added', 'Dropped' lists against (1); every diff hunk in CHANGES.md applied as a patch to N7's file must
   reproduce N8's file byte for byte; and an independent difflib diff (n=1) must equal the hunks listed.
"""
import hashlib, json, re, sys, difflib
from pathlib import Path
REPO = Path(sys.argv[1])
N8 = REPO / 'preregistration/natural-text-dense-replication-20261114'
N7 = REPO / 'preregistration/natural-text-matched-confirmation-20261104/sealed-source'
sha = lambda b: hashlib.sha256(b).hexdigest()
def tree(root): return {p.relative_to(root).as_posix(): p.read_bytes() for p in sorted(root.rglob('*')) if p.is_file()}
a, b = tree(N7), tree(N8 / 'source')
same = sorted(k for k in a if k in b and a[k] == b[k]); changed = sorted(k for k in a if k in b and a[k] != b[k])
added = sorted(set(b) - set(a)); dropped = sorted(set(a) - set(b))
print('N7 sealed-source files:', len(a), '| N8 source files:', len(b))
print('identical:', len(same)); print('changed  :', changed); print('added    :', added); print('dropped  :', dropped)
for k in added:
    twins = [j for j in a if a[j] == b[k]]
    print(f'  added {k} sha {sha(b[k])[:16]} byte-equal to N7 file(s): {twins}')

# ---- 2. SOURCE_SUBJECT.json
raw = b['SOURCE_SUBJECT.json']; s = json.loads(raw)
print('\nSOURCE_SUBJECT.json sha256:', sha(raw))
listed = {f['path']: f for f in s['files']}
bad = [p for p, f in listed.items() if p not in b or len(b[p]) != f['bytes'] or sha(b[p]) != f['sha256']]
print('files listed:', len(listed), '| mismatching bytes/sha:', bad)
print('in source/ but not listed:', sorted(set(b) - set(listed)))
print('listed but not in source/:', sorted(set(listed) - set(b)))
print('changed_from_n7 (subject):', s['changed_from_n7'], '| equals my changed minus unlisted:', sorted(s['changed_from_n7']) == sorted(k for k in changed if k in listed))
print('dropped_from_n7 (subject):', s['dropped_from_n7'], '| equals mine:', sorted(s['dropped_from_n7']) == dropped)
print('new_files (subject):', s['new_files'], '| equals mine:', sorted(s['new_files']) == added)
print('byte_copies_of_n7_source keys equal my identical set (minus unlisted):', sorted(s['byte_copies_of_n7_source']) == sorted(k for k in same if k in listed), '| values:', set(s['byte_copies_of_n7_source'].values()))
print('N7 SOURCE_SUBJECT.json sha256:', sha(a['SOURCE_SUBJECT.json']))
print('disabled_authorization_sha256 matches source/AUTHORIZATION.json:', s['disabled_authorization_sha256'] == sha(b['AUTHORIZATION.json']), '| AUTHORIZATION.json:', json.loads(b['AUTHORIZATION.json']))
reg = N8 / 'registry/n8-seed-registry'
sr = s['seed_registry_and_partition']
for key, name in (('draw_sha256', 'DRAW.json'), ('exclusions_sha256', 'EXCLUSIONS.json'), ('partition_sha256', 'PARTITION.json'), ('policy_sha256', 'SEED_REGISTRY_POLICY.md'), ('registry_sha256', 'REGISTRY.json')):
    print(f'  subject {key} == sha256({name}):', sr[key] == sha((reg / name).read_bytes()))
for rel, h in s['bound_records'].items():
    p = REPO / rel
    print(f'  bound record {rel}:', 'MATCH' if p.is_file() and sha(p.read_bytes()) == h else ('ABSENT in clone' if not p.is_file() else 'DIFFERS'))
ns = json.loads(a['SOURCE_SUBJECT.json']); n7listed = {f['path']: f for f in ns['files']}
print('N7 subject lists', len(n7listed), 'files; N7 files mismatching their own subject:', [p for p, f in n7listed.items() if p not in a or sha(a[p]) != f['sha256']], '| N7 unlisted:', sorted(set(a) - set(n7listed)))

# ---- 3. CHANGES.md
ch = (N8 / 'CHANGES.md').read_bytes(); print('\nCHANGES.md sha256:', sha(ch), '| CR bytes in it:', ch.count(b'\r'))
text = ch.decode('utf-8'); lines = text.split('\n')
sections = {}; cur = None
for i, l in enumerate(lines):
    m = re.match(r'^## (.*)$', l)
    if m: cur = m.group(1); sections[cur] = []
    elif cur: sections[cur].append(l)
unch = dict(re.findall(r'^- `([^`]+)` `([0-9a-f]+)…`$', '\n'.join(sections['Unchanged']), flags=re.M))
print('CHANGES Unchanged lists', len(unch), 'files; my identical set has', len(same))
print('  listed as unchanged but not identical:', sorted(k for k in unch if k not in same))
print('  identical but not listed as unchanged:', sorted(k for k in same if k not in unch))
print('  hash prefixes wrong:', [k for k, h in unch.items() if k in b and not sha(b[k]).startswith(h)])
adr = '\n'.join(sections['Added, dropped and regenerated'])
print('CHANGES Added:', re.findall(r'\*\*Added\*\* `([^`]+)` `([0-9a-f]+)…`', adr), '| Dropped:', re.findall(r'\*\*Dropped\*\* `([^`]+)` `([0-9a-f]+)…`', adr), '| Regenerated:', re.findall(r'\*\*Regenerated\*\* `([^`]+)`', adr))
for k, h in re.findall(r'\*\*Added\*\* `([^`]+)` `([0-9a-f]+)…`', adr): print('  added hash prefix ok:', k, sha(b[k]).startswith(h))
for k, h in re.findall(r'\*\*Dropped\*\* `([^`]+)` `([0-9a-f]+)…`', adr): print('  dropped hash prefix ok (N7 file):', k, sha(a[k]).startswith(h))
filesecs = {k.strip('`'): v for k, v in sections.items() if k.startswith('`')}
print('CHANGES per-file sections:', list(filesecs)); print('  equals my changed set minus SOURCE_SUBJECT.json:', sorted(filesecs) == sorted(k for k in changed if k != 'SOURCE_SUBJECT.json'))
total_h = 0; notes = []
for name, body in filesecs.items():
    # parse the fenced diff blocks; each must be preceded by one numbered note
    hunks = []; i = 0
    while i < len(body):
        m = re.match(r'^\*\*(\d+)\.\*\* (.*)$', body[i])
        if m: notes.append((int(m.group(1)), name, m.group(2)))
        if body[i] == '```diff':
            j = i + 1; blk = []
            while body[j] != '```': blk.append(body[j]); j += 1
            hunks.append(blk); i = j
        i += 1
    old = a[name]; new = b[name]
    eol_old = (old.count(b'\r\n'), old.count(b'\n')); eol_new = (new.count(b'\r\n'), new.count(b'\n'))
    ol = old.decode('utf-8').split('\n'); nl = new.decode('utf-8').split('\n')
    # apply as a patch
    out = []; pos = 0; ok = True; nh = 0
    for blk in hunks:
        k = 0
        while k < len(blk):
            m = re.match(r'^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@', blk[k])
            if not m: ok = False; print('  unparsed line in block:', name, repr(blk[k][:80])); break
            nh += 1; o0 = int(m.group(1)); oc = int(m.group(2) or 1) if m.group(2) != '0' else 0; n0 = int(m.group(3)); nc = int(m.group(4) or 1) if m.group(4) != '0' else 0
            start = o0 - 1 if oc else o0
            if start < pos: ok = False; print('  hunk overlaps:', name, blk[k]); break
            out += ol[pos:start]; pos = start
            if len(out) != (n0 - 1 if nc else n0): ok = False; print('  new-side line number wrong:', name, blk[k], len(out) + 1)
            k += 1; seen_o = seen_n = 0
            while k < len(blk) and not blk[k].startswith('@@'):
                t, rest = blk[k][:1], blk[k][1:]
                if t == ' ':
                    if ol[pos] != rest: ok = False; print('  context mismatch', name, pos + 1)
                    out.append(rest); pos += 1; seen_o += 1; seen_n += 1
                elif t == '-':
                    if ol[pos] != rest: ok = False; print('  removed-line mismatch', name, pos + 1, repr(rest[:60]), repr(ol[pos][:60]))
                    pos += 1; seen_o += 1
                elif t == '+': out.append(rest); seen_n += 1
                elif blk[k].startswith('\\'): pass
                else: ok = False; print('  odd line', name, repr(blk[k][:60]))
                k += 1
            if (seen_o, seen_n) != (oc, nc): ok = False; print('  hunk counts wrong', name, (seen_o, seen_n), (oc, nc))
    out += ol[pos:]
    rebuilt = '\n'.join(out).encode('utf-8')
    total_h += nh
    # independent diff
    mine = [l.rstrip('\n') for l in difflib.unified_diff(old.decode('utf-8').splitlines(keepends=True), new.decode('utf-8').splitlines(keepends=True), n=1)][2:]
    theirs = [l for blk in hunks for l in blk]
    plus = sum(1 for l in theirs if l.startswith('+')); minus = sum(1 for l in theirs if l.startswith('-'))
    print(f'{name}: fenced blocks {len(hunks)}, hunks {nh}, +{plus}/-{minus} lines | patch(N7)==N8 bytes: {ok and rebuilt == new} | my difflib(n=1) hunks identical to listed: {mine == theirs} | (CRLF,LF) N7 {eol_old} N8 {eol_new}')
nums = [n for n, _, _ in notes]
print('numbered notes:', len(notes), '| consecutive 1..N:', nums == list(range(1, len(nums) + 1)), '| total hunks:', total_h)
cite = re.compile(r'§\s?\d+(?:\.\d+)?|brief|Gate 2 review|owner')
print('notes citing no protocol section, brief, gate review or owner decision:')
for n, name, t in notes:
    if not cite.search(t): print(f'  {n}. [{name}] {t}')
