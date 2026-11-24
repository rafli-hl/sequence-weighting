"""POST HOC audit helper (area C). SYNTHETIC loss arrays on N8's grid, from fixed formulas; no N8 data. Used by c05 and c07."""
import math
import numpy as np

EP = [u / 1024 for u in (256, 512, 1024) + tuple(range(2048, 3584 + 1, 64))]      # N8's 28 readouts, written out independently
TAG = 'lr1e-04'


def make_draw(k, n, nv):
    """One draw: weights, two arms (E0, arrays, record) and four epochs of batch orders. 768 learns faster than 512, so 512's E3
    training loss is met by 768 near epoch 2.35."""
    i = np.arange(n); u = math.log(.01) + (math.log(10) - math.log(.01)) * (((i + 1) * 0.6180339887498949 + 0.137 * k) % 1.0)
    w = np.exp(u); w = (w / w.mean()).astype('<f4'); wf = w.astype(np.float64); arms = {}
    for width in (512, 768):
        wide = width == 768
        l0 = 6.0 + 0.3 * np.sin(1.7 * i + k) + (0.05 + 0.01 * math.sin(2.0 * k) if wide else 0.0)
        v0 = 6.3 + 0.2 * np.sin(0.9 * np.arange(nv) + k)
        e0 = np.concatenate([l0, v0]).astype('<f4'); blocks = []; readouts = []
        for e in EP:
            mean_gain = (1.15 + 0.34 * e + 0.012 * math.sin(1.3 * k)) if wide else (1.0 + 0.30 * e)
            q = (0.095 + 0.006 * e + 0.002 * math.sin(0.7 * k + 3 * e)) if wide else (0.10 + 0.004 * e + 0.002 * math.cos(0.5 * k))
            shape = wf ** q; gain = mean_gain * shape / shape.mean() + 0.2 * np.sin(3.1 * i + 5 * e + k + width / 100)
            tr = (l0 - gain).astype('<f4'); va = (v0 - 0.4 * e + 0.05 * e * e + (0.02 if wide else 0.0)).astype('<f4')
            blocks.append(np.concatenate([tr, va])); readouts.append(dict(epoch=e, update=round(e * n / 16), train_loss=float(tr.mean()), validation_loss=float(va.mean())))
        arms[(width, TAG)] = dict(e0=e0.tobytes(), arrays=np.concatenate(blocks).astype('<f4').tobytes(),
                                  record=dict(layout=dict(train_rows=n, validation_rows=nv, block_epochs=[0.25, 0.5, 1] + EP[3:]), readouts=readouts))
    order = np.stack([np.argsort(((np.arange(n) + 1) * (0.7548776662466927 + 0.01 * e) + 0.31 * k) % 1.0, kind='stable') for e in range(4)]).astype('<i8')
    return dict(weights=w.tolist(), arms=arms), order
