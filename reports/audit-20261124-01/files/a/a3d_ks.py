"""POST HOC (auditor A). The 13 November audit's other balance figure for F3: the largest two-sample Kolmogorov-Smirnov distance
between the two sets' ages of a pass (over draws and passes), from the emulated orders written by a6_make_orders.py.
Usage: python a3d_ks.py <orders dir>"""
import sys
from pathlib import Path
import numpy as np

d0 = Path(sys.argv[1]); N, U = 16384, 1024
for k in (1, 2, 3):
    worst = (0.0, None)
    for d in ('m01', 'm02', 'm03', 'm04', 'm05', 'm06'):
        o = np.frombuffer((d0 / f'{d}.i64').read_bytes(), '<i8').reshape(4, N)[:3]; pos = np.empty_like(o)
        for e in range(3): pos[e, o[e]] = np.arange(N)
        quarter, rank = pos // (N // 4) + 1, pos // 16 + 1
        m5, m7 = np.all(quarter >= 5 - k, axis=0), np.all(quarter <= k, axis=0)
        for e in range(3):
            a = np.sort(3072 - (e * U + rank[e][m5])); b = np.sort(2048 + 256 * k - (e * U + rank[e][m7])); grid = np.union1d(a, b)
            ks = float(np.abs(np.searchsorted(a, grid, side='right') / len(a) - np.searchsorted(b, grid, side='right') / len(b)).max())
            worst = max(worst, (ks, f'{d} pass {e + 1}'))
    print(f'k = {k}: largest marginal KS distance {worst[0]:.5f} ({worst[1]})')
