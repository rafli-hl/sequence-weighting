"""POST HOC audit script (area C). S-b (exposure_windows) on SYNTHETIC arrays and orders (6 draws, 1,024 training rows, 64 updates
per epoch; c_synth.py), against the auditor's own construction of the sets, written from the definitions in the post-hoc analysis of
11 November (posthoc_exposure.py, section 3) and the 13 November audit's recency code (ranks and quarters), with N7's sealed
vendor/core.exponent. The registered check of S-b is in test_on_n7.py and needs PyTorch, which this auditor does not have.
In the synthetic arrays the losses do not depend on the orders, so only the construction of the sets is checked here.
Usage: python -I -B c07_exposure_windows.py <REPO>"""
import sys, math, itertools, importlib.util
from pathlib import Path
sys.dont_write_bytecode = True
repo = Path(sys.argv[1])
sys.path.insert(0, str(repo / 'preregistration/natural-text-dense-replication-20261114/analysis')); sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
import n8_analysis as na
import c_synth
spec = importlib.util.spec_from_file_location('n7core', repo / 'preregistration/natural-text-matched-confirmation-20261104/sealed-source/vendor/core.py')
n7core = importlib.util.module_from_spec(spec); spec.loader.exec_module(n7core)

N, NV, U = 1024, 16, 64; DRAWS = na.DRAWS[:6]; EP = c_synth.EP
plan = dict(na.PLAN, draws=DRAWS, min_draws=5, min_completed=5, updates_per_epoch=U)
data, orders = {}, {}
for k, d in enumerate(DRAWS): data[d], orders[d] = c_synth.make_draw(k, N, NV)
per = na.points(data); sb = na.exposure_windows(per, data, orders, plan)


def arr(d, width): return np.frombuffer(data[d]['arms'][(width, c_synth.TAG)]['arrays'], '<f4').reshape(28, N + NV)[:, :N]
def e0(d, width): return np.frombuffer(data[d]['arms'][(width, c_synth.TAG)]['e0'], '<f4')[:N]
def fit(d, width, e, mask):
    w = np.asarray(data[d]['weights']); g = e0(d, width) - arr(d, width)[EP.index(e)]
    return n7core.exponent(w[mask].tolist(), g[mask].tolist())['p']


worst = dict(whole=0.0, last=0.0, every=0.0, loss_last=0.0, loss_every=0.0); bal = []
for k in (1, 2, 3):
    e7 = 2 + k / 4; step = sb['steps'][e7]; sizes, ages, tvs = [], [], []
    for d in DRAWS:
        ranks = np.empty((3, N), int)
        for e in range(3): ranks[e, orders[d][e]] = np.arange(N) // 16 + 1          # the update, within its epoch, at which a sequence is trained
        quarter = (ranks - 1) // (U // 4) + 1
        i5 = np.all(quarter >= 5 - k, axis=0); i7 = np.all(quarter <= k, axis=0); l5 = quarter[2] >= 5 - k; l7 = quarter[2] <= k
        mine = dict(whole=fit(d, 512, 3.0, np.ones(N, bool)) - fit(d, 768, e7, np.ones(N, bool)), last=fit(d, 512, 3.0, l5) - fit(d, 768, e7, l7), every=fit(d, 512, 3.0, i5) - fit(d, 768, e7, i7),
                    loss_last=arr(d, 512)[EP.index(3.0)][l5].astype(float).mean() - arr(d, 768)[EP.index(e7)][l7].astype(float).mean(),
                    loss_every=arr(d, 512)[EP.index(3.0)][i5].astype(float).mean() - arr(d, 768)[EP.index(e7)][i7].astype(float).mean())
        for key in worst: worst[key] = max(worst[key], abs(mine[key] - step['contrasts'][key]['values'][d]))
        sizes += [int(i5.sum()), int(i7.sum())]
        a5 = 3 * U - (ranks[:, i5] + np.arange(3)[:, None] * U); a7 = 2 * U + (U // 4) * k - (ranks[:, i7] + np.arange(3)[:, None] * U)
        ages += [abs(a5[e].mean() - a7[e].mean()) for e in range(3)]
        q5 = quarter[:, i5] - (4 - k); q7 = quarter[:, i7]; cells = list(itertools.product(range(1, k + 1), repeat=3))
        h5 = np.array([np.all(q5 == np.array(c)[:, None], axis=0).mean() for c in cells]); h7 = np.array([np.all(q7 == np.array(c)[:, None], axis=0).mean() for c in cells]); tvs.append(abs(h5 - h7).sum() / 2)
    b = step['balance']['every']
    bal.append((k, (b['size_min'], b['size_max']) == (min(sizes), max(sizes)), abs(b['max_abs_mean_age_difference'] - max(ages)), abs(b['max_joint_cell_distance'] - max(tvs)), min(sizes), max(sizes), max(ages), max(tvs)))
print('S-b on synthetic orders, 6 draws: largest difference between exposure_windows and the auditor, per-draw contrasts:', {k: f'{v:.2g}' for k, v in worst.items()})
for k, same, da, dt, s0, s1, ag, tv in bal:
    print(f'  768 at E{2 + k / 4}: every-pass set sizes {s0}-{s1} equal: {same}; max |mean age difference| {ag:.5f} updates, difference {da:.2g}; max joint quarter-cell distance {tv:.5f}, difference {dt:.2g}')
oc = sb['order_checks']; print('  order checks (synthetic losses do not depend on the orders, so about 0 is expected):', {d: round(v['mean'], 4) for d, v in oc.items()}, '| steps per draw', {v['steps'] for v in oc.values()})
