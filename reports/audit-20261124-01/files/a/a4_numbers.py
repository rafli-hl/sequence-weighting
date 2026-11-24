"""POST HOC, descriptive (auditor A). Numbers quoted on the living pages, recomputed from published tables.
Standard library. Usage: python a4_numbers.py <repo root>
"""
import csv, json, math, statistics as st, sys
from pathlib import Path

root = Path(sys.argv[1]); T5 = 2.5705818356363
A = root / 'reports/natural-text-matched-analysis-20261105-01'
M = list(csv.DictReader(open(A / 'MATCHED.csv', encoding='utf-8')))


def ci(v, t=T5):
    m, h = st.mean(v), t * st.stdev(v) / math.sqrt(len(v)); return f'{m:+.5f} [{m - h:+.5f}, {m + h:+.5f}], {sum(x > 0 for x in v)}/{len(v)} above 0'


for s in ('P1', 'S1', 'S3', 'S4', 'S5', 'S2'):
    rows = [r for r in M if r['statistic'] == s]; v = [float(r['value']) for r in rows if r['status'] == 'READ']
    pos = [float(r['read_at_readout']) for r in rows if r['status'] == 'READ']
    print(f'{s}: {ci(v) if len(v) >= 5 else "only %d draws read" % len(v)}; read at {min(pos):.3f}-{max(pos):.3f}; values {", ".join("%+.5f" % x for x in v)}')
    if s in ('P1', 'S1', 'S4'): print('    brackets:', ', '.join(f"{r['draw']} {r['between_low']}-{r['between_high']}" for r in rows))
J = json.loads((A / 'ANALYSIS.json').read_bytes())
print('ANALYSIS.json top-level keys:', list(J)[:20])
p512 = [float(r['p_first']) for r in M if r['statistic'] == 'P1']; p768 = [float(r['p_read']) for r in M if r['statistic'] == 'P1']
print(f'mean p*(512, E3, 1e-4) {st.mean(p512):.4f}; 768 where read in P1: {min(p768):.4f}-{max(p768):.4f}')
loo = {}
for s in ('P1', 'S1', 'S3', 'S4', 'S5'):
    v = [float(r['value']) for r in M if r['statistic'] == s]; out = []
    T4 = 2.7764451051978            # t(0.975, df = 4)
    for i in range(6):
        w = v[:i] + v[i + 1:]; m, h = st.mean(w), T4 * st.stdev(w) / math.sqrt(5); out.append((m - h, m + h))
    loo[s] = out
    print(f'{s} leave-one-out intervals: ' + '; '.join(f'm0{i + 1} [{a:+.5f}, {b:+.5f}]{"*" if a <= 0 <= b else ""}' for i, (a, b) in enumerate(out)))
R = json.loads((root / 'reports/natural-text-matched-assistant-posthoc-20261111-01/RESULTS.json').read_bytes())['values']
for key in [f'matched|{tag}|k{k}|every' for tag in ('lr1e-04', 'lr3e-04') for k in (1, 2, 3)] + [k for k in R if k.startswith('better_rate')][:8]:
    v = R[key]
    if isinstance(v, list) and len(v) == 6 and all(isinstance(x, (int, float)) for x in v): print(f'{key}: {ci(v)}')
    else: print(f'{key}: {str(v)[:150]}')
