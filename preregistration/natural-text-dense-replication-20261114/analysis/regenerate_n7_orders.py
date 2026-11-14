"""Regenerate N7's batch orders from the seeds in the loss-array bundle's MANIFEST.json, for test_on_n7.py (S-b only).

    python -I -B regenerate_n7_orders.py <BUNDLE> <NEW_OUT_DIR>        # needs PyTorch (CPU); N7 used 2.7.0

N7's engine drew epoch e's order as torch.randperm(n, generator=torch.Generator().manual_seed(999 + adapt_order_seed + e))
(text_engine.orders, epochs 1-4). Writes, per draw, <draw>.i64 (four rows of n sequence indices in training order, int64
little-endian) and <draw>-seed-plus-1.i64 (the same with the seed shifted by 1, a negative control), and ORDERS.json with
each file's SHA-256, each epoch's order SHA-256 (n8_analysis.order_sha256) and the PyTorch version. Whether these are the
orders that produced the losses is checked against the losses by test_on_n7.py.
"""
import hashlib, json, sys
from pathlib import Path

import numpy as np
import torch

N, EPOCHS = 16384, 4


def orders(seed):
    return np.stack([torch.randperm(N, generator=torch.Generator().manual_seed(999 + seed + e)).numpy() for e in range(1, EPOCHS + 1)]).astype('<i8')


def main(bundle, out):
    man = json.loads((bundle / 'MANIFEST.json').read_bytes()); out.mkdir(parents=False, exist_ok=False); index = {}
    for d in sorted(man['draws']):
        seed = man['draws'][d]['seeds']['adapt_order_seed']
        for suffix, s in (('', seed), ('-seed-plus-1', seed + 1)):
            o = orders(s); b = o.tobytes(); (out / f'{d}{suffix}.i64').write_bytes(b)
            index[f'{d}{suffix}'] = dict(file=f'{d}{suffix}.i64', bytes=len(b), sha256=hashlib.sha256(b).hexdigest(), seed=s,
                                         epoch_order_sha256=[hashlib.sha256(row.tobytes()).hexdigest() for row in o])
    meta = dict(torch=torch.__version__, numpy=np.__version__, n=N, epochs=EPOCHS, layout='rows = epochs 1-4; int64 little-endian sequence indices in training order', orders=index)
    (out / 'ORDERS.json').write_bytes((json.dumps(meta, indent=1) + '\n').encode('utf-8'))
    print(f'torch {torch.__version__}: wrote {len(index)} order files to {out}')


if __name__ == '__main__':
    if len(sys.argv) != 3: raise SystemExit(__doc__)
    main(Path(sys.argv[1]), Path(sys.argv[2]))
