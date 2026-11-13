"""Sizes and weight distributions of the exposure-matched sets of the 11 November post-hoc analysis.

Post hoc, 13 November 2026; descriptive, tests nothing. The sets follow posthoc_exposure.py, section 3: for k = 1, 2, 3,
768 at epoch 2 + k/4 uses the sequences trained in quarters <= k of each of epochs 1-3, and 512 at epoch 3 those
trained in quarters >= 5 - k. Batch orders are regenerated from the seeds as in text_engine.orders.

Usage:  python reports/readme-revision-20261113-01/matched_set_weights.py path/to/n7-loss-arrays
Needs NumPy and PyTorch (the versions in tools/requirements-posthoc.txt reproduce the orders).
"""
import json, sys
from pathlib import Path
import numpy as np
import torch

bundle = Path(sys.argv[1]); man = json.loads((bundle / "MANIFEST.json").read_text(encoding="utf-8"))
N, Q = 16384, 4096
worst, sizes = {}, {}
print("draw  k   whole-draw median log10 w   512 set: n, median   768 set: n, median")
for d in sorted(man["draws"]):
    W = np.frombuffer((bundle / man["draws"][d]["weights"]["path"]).read_bytes(), "<f4").astype(np.float64)
    seed = man["draws"][d]["seeds"]["adapt_order_seed"]
    qtr = np.zeros((4, N), np.int64)
    for e in range(4):
        order = torch.randperm(N, generator=torch.Generator().manual_seed(999 + seed + e + 1)).numpy()
        qtr[e, order] = np.arange(N) // Q + 1
    a, b, c, _ = qtr
    whole = np.median(np.log10(W))
    for k in (1, 2, 3):
        s512 = (a >= 5 - k) & (b >= 5 - k) & (c >= 5 - k)
        s768 = (a <= k) & (b <= k) & (c <= k)
        m512, m768 = np.median(np.log10(W[s512])), np.median(np.log10(W[s768]))
        print(f"{d}   {k}   {whole:+.3f}                    {int(s512.sum()):5d}, {m512:+.3f}        {int(s768.sum()):5d}, {m768:+.3f}")
        worst[k] = max(worst.get(k, 0.0), abs(m512 - whole), abs(m768 - whole))
        sizes.setdefault(k, []).extend([int(s512.sum()), int(s768.sum())])
for k in (1, 2, 3):
    print(f"k = {k}: set sizes {min(sizes[k])}-{max(sizes[k])}; largest |median log10 w (set) - median log10 w (draw)| = {worst[k]:.3f}")
