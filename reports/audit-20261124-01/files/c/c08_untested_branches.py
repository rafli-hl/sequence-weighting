"""POST HOC audit script (area C). Constructed inputs for four branches of n8_analysis.py that no registered test enters
(c06_mutants.py, M4-M8): the NOT_OVERFIT labels, S-d's exclusion of saturated fits, the starting offset's undefined refit, and the
7.999 refit threshold. Synthetic values from fixed formulas; no N8 data. decide() and analyse() are not called.
Usage: python -I -B c08_untested_branches.py <REPO>"""
import sys, math, copy
from pathlib import Path
sys.dont_write_bytecode = True
repo = Path(sys.argv[1])
sys.path.insert(0, str(repo / 'preregistration/natural-text-dense-replication-20261114/analysis')); sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
import n8_analysis as na
import c_synth

F, S = na.PLAN['first'], na.PLAN['second']
print('1. NOT_OVERFIT: validation loss at E3 minus E2 per width, over the completed draws')
for name, diffs in (('all falling', [-0.02 - 0.001 * k for k in range(24)]), ('all rising', [0.02 + 0.001 * k for k in range(24)]), ('mixed', [0.01 * (-1) ** k for k in range(24)]),
                    ('falling, upper limit within 1e-9 of 0', None)):
    if diffs is None:
        a = 0.001; half = na.t_quantile(0.975, 23) * a / math.sqrt(23); diffs = [-(half + 5e-10) + a * (-1) ** k for k in range(24)]
    per = {d: {arm: {2.0: dict(validation=4.7), 3.0: dict(validation=4.7 + diffs[k])} for arm in (F, S)} for k, d in enumerate(na.DRAWS)}
    out = na.not_overfit(per); x = out['512|lr1e-04']; print(f'   {name}: {x["label"]}, interval [{x["interval"]["interval"][0]:+.3e}, {x["interval"]["interval"][1]:+.3e}], n {x["interval"]["n"]}')

print('2. S-d: a saturated fit drops its draw at that readout only')
per = {d: {F: {e: dict(p=0.10 + 0.001 * k, saturated=False) for e in na.PLAN['path']}, S: {e: dict(p=0.09 + 0.002 * k, saturated=False) for e in na.PLAN['path']}} for k, d in enumerate(na.DRAWS)}
per['n05'][S][2.5] = dict(p=8.0, saturated=True); per['n06'][S][2.5] = dict(p=8.0, p32=9.0, saturated=False); per['n07'][F][2.5] = dict(p=None, saturated=False)
sd = na.path_contrasts(per); print('   draws at E2.5:', sd[2.5]['n'], '(n05 saturated and n07 undefined are out; n06, resolved at bound 32, stays with its bound-8 value', sd[2.5]['values']['n06'], ') | draws at E2.5625:', sd[2.5625]['n'])

print('3. starting offset: a refit that is undefined once the offset is taken off')
draws = na.DRAWS[:4]; data = {d: c_synth.make_draw(k, 256, 16)[0] for k, d in enumerate(draws)}; per = na.points(data)
h1 = na.contrast(per, draws, F, S, 'matched', 'train', 3.0, na.PLAN['path'], 2, 'ABOVE')
shifted = copy.deepcopy(data); arm = shifted['n02']['arms'][S]          # 768 of n02: E0 and every readout raised by 3 nats, so its gains are unchanged and the offset grows by 3
arm['e0'] = (np.frombuffer(arm['e0'], '<f4') + np.float32(3.0)).astype('<f4').tobytes(); arm['arrays'] = (np.frombuffer(arm['arrays'], '<f4') + np.float32(3.0)).astype('<f4').tobytes()
so = na.starting_offset(h1, shifted, dict(na.PLAN, draws=draws))
print('   rows:', {d: (r['status'], round(r['offset'], 4)) for d, r in so['rows'].items()}, '| draws in the contrast:', so['contrast']['n'], '| draws in the offset summary:', so['offset']['n'])

print('4. the refit threshold: gains proportional to w^q, read through arm_points')
n, nv = 400, 4
w = np.array([math.exp(math.log(.01) + (math.log(10) - math.log(.01)) * (i + .5) / n) for i in range(n)]); w = (w / w.mean()).astype('<f4'); wf = w.astype(np.float64)
for q in (7.9, 7.9985, 7.9995, 8.0, 9.0):
    g = (wf / wf.max()) ** q; e0 = np.concatenate([g, np.zeros(nv)]).astype('<f4'); arr = np.zeros(n + nv, dtype='<f4')          # gains = E0 - readout = g, exact in float32
    pt = na.arm_points(w.tolist(), dict(e0=e0.tobytes(), arrays=arr.tobytes(), record=dict(layout=dict(train_rows=n, validation_rows=nv, block_epochs=[3.0]), readouts=[dict(epoch=3.0, train_loss=0.0, validation_loss=0.0)])), diagnostics=False)[3.0]
    print(f'   q = {q}: p* = {pt["p"]:.6f}; refitted at bound 32: {"p32" in pt}' + (f' (p32 = {pt["p32"]:.6f})' if 'p32' in pt else '') + f'; saturated: {pt["saturated"]}')
