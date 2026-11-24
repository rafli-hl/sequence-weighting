"""POST HOC (auditor A). Local links and fragment anchors of the living pages. Standard library.
Usage: python a5_links.py <repo root>"""
import re, sys, urllib.parse
from pathlib import Path
root = Path(sys.argv[1])
pages = ['README.md', 'CURRENT_CLAIMS.md', 'METHODS.md', 'NATURAL_TEXT_STUDIES.md', 'DATA_AVAILABILITY.md', 'PUBLICATION_NOTES.md',
         'reports/README.md', 'outputs/README.md', 'preregistration/natural-text-dense-replication-20261114/README.md',
         'reports/natural-text-correction-20261123-01/CORRECTION.md', 'reports/external-audit-20261113-01/README.md']


def slug(h):   # GitHub's heading anchors: lower-case, drop punctuation except hyphen/underscore, spaces to hyphens
    h = re.sub(r'[`*]', '', h.strip()).lower()
    h = re.sub(r'[^\w\- ]', '', h, flags=re.UNICODE)
    return h.replace(' ', '-')


def anchors(p):
    out, seen = set(), {}
    for line in p.read_text(encoding='utf-8').splitlines():
        m = re.match(r'^(#{1,6})\s+(.*?)\s*$', line)
        if m:
            s = slug(m.group(2)); k = seen.get(s, 0); seen[s] = k + 1; out.add(s if k == 0 else f'{s}-{k}')
    return out


n = bad = ext = 0
for page in pages:
    p = root / page; text = p.read_text(encoding='utf-8')
    for m in re.finditer(r'\[[^\]]*\]\(([^)\s]+)\)|(?:src|srcset)="([^"]+)"', text):
        t = m.group(1) or m.group(2)
        if re.match(r'^[a-z]+://', t) or t.startswith('mailto:'): ext += 1; continue
        n += 1; path, _, frag = t.partition('#'); target = (p.parent / urllib.parse.unquote(path)).resolve() if path else p
        if not target.exists(): bad += 1; print(f'BROKEN {page}: {t}'); continue
        if frag and target.suffix == '.md' and frag not in anchors(target): bad += 1; print(f'BAD ANCHOR {page}: {t} (anchors: {sorted(anchors(target))[:40]})')
print(f'{n} local links and image sources checked on {len(pages)} pages; {bad} broken; {ext} external links not checked')
