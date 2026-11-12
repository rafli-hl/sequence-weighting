"""Step 3 of the reduced audit (8 Nov 2026): the orchestrator's own re-check of the major findings from a fresh angle, in
code of its own, from the primary records only (POINTS.csv of N7 and N6; PROTOCOL.md). Reads nothing under work/runs.
Writes VERIFY_ORCHESTRATOR.txt beside this file."""
import csv, math, re, statistics as st
from pathlib import Path
ROOT = Path(r'D:\sequence-weighting-research'); HERE = Path(__file__).resolve().parent
T5 = 2.5705818356363133  # t(0.975, 5)
def load(p):
    P = {}
    for r in csv.DictReader(open(p, encoding='utf-8', newline='')): P[(r['draw'], float(r['epoch']), int(r['width']), r['tag'])] = {k: float(r[k]) for k in ('p', 'train', 'gap', 'validation')}
    return P
def iv(v): m = st.mean(v); h = T5 * st.stdev(v) / math.sqrt(len(v)); return m, m - h, m + h, st.stdev(v)
def fmt(v): m, lo, hi, sd = iv(v); return f'{m:+.5f} [{lo:+.5f}, {hi:+.5f}] sd {sd:.5f} {sum(x > 0 for x in v)}>0/{sum(x < 0 for x in v)}<0'
def matched(P, draws, wide, narrow, rate, key, path, mode='linear'):
    """narrow's E3 value matched on wide's path; mode: linear | later | earlier (which end of the bracket)."""
    out, pos = [], {}
    for d in draws:
        tgt = P[(d, 3.0, narrow, rate)][key]; pts = [(e, P[(d, e, wide, rate)][key], P[(d, e, wide, rate)]['p']) for e in path]
        for (e0, x0, p0), (e1, x1, p1) in zip(pts, pts[1:]):
            if min(x0, x1) <= tgt <= max(x0, x1):
                w = 0.0 if x1 == x0 else (tgt - x0) / (x1 - x0); pr = p0 + w * (p1 - p0) if mode == 'linear' else (p1 if mode == 'later' else p0)
                out.append(P[(d, 3.0, narrow, rate)]['p'] - pr); pos[d] = (e0, e1, round(e0 + w * (e1 - e0), 3)); break
    return out, pos
lines = []
N7 = load(ROOT / 'reports/natural-text-matched-analysis-20261105-01/POINTS.csv'); D7 = sorted({k[0] for k in N7}); E7 = sorted({k[1] for k in N7}); dense = [e for e in E7 if 2.0 <= e <= 3.5]
lines.append('V1  S4 (3e-4, matched training NLL) with 768 read at each end of its bracket, N7 POINTS.csv, own code')
for mode in ('linear', 'earlier', 'later'):
    v, pos = matched(N7, D7, 768, 512, 'lr3e-04', 'train', dense, mode); lines.append(f'    {mode:8s} {fmt(v)}  brackets {pos}')
v, pos = matched(N7, D7, 768, 512, 'lr1e-04', 'train', dense, 'later'); lines.append(f'    P1 later  {fmt(v)}')
lines.append(f"    m06 at 3e-4: 512 E3 train {N7[('m06', 3.0, 512, 'lr3e-04')]['train']:.6f}; 768 train E3 {N7[('m06', 3.0, 768, 'lr3e-04')]['train']:.6f} E3.25 {N7[('m06', 3.25, 768, 'lr3e-04')]['train']:.6f}; 768 p* E3 {N7[('m06', 3.0, 768, 'lr3e-04')]['p']:.5f} E3.25 {N7[('m06', 3.25, 768, 'lr3e-04')]['p']:.5f}")
lines.append('V2  coarse (E2, E3 only) against dense interpolation, N7 draws, own code')
for name, rate, key in (('P1', 'lr1e-04', 'train'), ('S1', 'lr1e-04', 'gap'), ('S4', 'lr3e-04', 'train')):
    vd, _ = matched(N7, D7, 768, 512, rate, key, dense); vc, pc = matched(N7, D7, 768, 512, rate, key, [2.0, 3.0]); lines.append(f'    {name} dense {fmt(vd)} | coarse {fmt(vc)} (n={len(vc)}) | coarse minus dense of the mean {st.mean(vc) - st.mean(vd):+.5f}')
N6 = load(ROOT / 'reports/natural-text-peak-analysis-20261103-01/POINTS.csv'); D6 = sorted({k[0] for k in N6}); E6 = sorted({k[1] for k in N6}); lines.append(f'    N6 readouts {E6}; draws {D6}')
v6, p6 = matched(N6, D6, 768, 512, 'lr1e-04', 'train', [e for e in E6 if 2.0 <= e <= 3.0]); lines.append(f'    N6 D4 matched on train, E2-E3 linear: {fmt(v6)} positions {p6}')
steps = {}
for w in (512, 768):
    for rate in ('lr1e-04', 'lr3e-04'):
        ms = [st.mean(N7[(d, e, w, rate)]['p'] for d in D7) for e in dense]; steps[(w, rate)] = [round(b - a, 5) for a, b in zip(ms, ms[1:])]
lines.append(f'    N7 panel p* quarter steps E2->E3.5 per arm: {steps}')
lines.append('V4  realized spread of P1 against PROTOCOL.md section 10')
vp, _ = matched(N7, D7, 768, 512, 'lr1e-04', 'train', dense); lines.append(f'    P1 {fmt(vp)}; realized sd / 0.0025 = {st.stdev(vp) / 0.0025:.3f}; mean / 0.0132 = {st.mean(vp) / 0.0132:.3f}')
prot = (ROOT / 'work/natural-text-matched-source-20261104-01/PROTOCOL.md').read_text(encoding='utf-8')
sec10 = prot[prot.index('## 10.'):prot.index('## 11.')]
for ln in sec10.splitlines():
    if re.search(r'0\.0025|0\.0132|0\.703|0\.999|flattering|sd', ln): lines.append('    PROTOCOL 10: ' + ln.strip()[:260])
lines.append('V3  how train/validation are measured: the cited lines of the sealed code (read as text)')
for f, a, b in (('matched_worker.py', 190, 206), ('text_worker.py', 190, 210), ('text_engine.py', 40, 52), ('fewepoch_plan.py', 66, 76)):
    src = (ROOT / 'work/natural-text-matched-source-20261104-01' / f).read_text(encoding='utf-8').splitlines()
    for i in range(a - 1, min(b, len(src))): lines.append(f'    {f}:{i + 1}: {src[i][:200]}')
(HERE / 'VERIFY_ORCHESTRATOR.txt').write_text('\n'.join(lines) + '\n', encoding='utf-8'); print('\n'.join(lines))
