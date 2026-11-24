"""POST HOC (auditor A). Are the orders from my pure-Python emulation of torch.randperm byte-identical to the PyTorch-generated
orders that N8's registration pinned? Compares the SHA-256 of each emulated <draw>.i64 (four epoch rows, int64 little-endian, the
layout of analysis/regenerate_n7_orders.py) with the 12 hashes under inputs/n7-orders-v1/ in N8's HASHES.json.
Usage: python a3b_order_hashes.py <repo root> <bundle dir>"""
import hashlib, importlib.util, io, json, sys, contextlib
from pathlib import Path
import numpy as np

root, bundle = Path(sys.argv[1]), Path(sys.argv[2])
src = (Path(__file__).parent / 'a3_recency.py').read_text(encoding='utf-8')
ns = {}
exec(src.split('# (1) the generator itself')[0].replace('root, bundle = Path(sys.argv[1]), Path(sys.argv[2])', ''), ns)   # MT and randperm only
randperm = ns['randperm']
H = json.loads((root / 'preregistration/natural-text-dense-replication-20261114/HASHES.json').read_bytes())


def find(o, key):
    if isinstance(o, dict):
        if key in o: return o[key]
        for v in o.values():
            r = find(v, key)
            if r is not None: return r
    return None


man = json.loads((bundle / 'MANIFEST.json').read_bytes()); ok = 0
for d in sorted(man['draws']):
    seed = man['draws'][d]['seeds']['adapt_order_seed']
    for suffix, s in (('', seed), ('-seed-plus-1', seed + 1)):
        o = np.stack([randperm(16384, 999 + s + e) for e in (1, 2, 3, 4)]).astype('<i8')
        mine = hashlib.sha256(o.tobytes()).hexdigest(); pinned = find(H, f'inputs/n7-orders-v1/{d}{suffix}.i64')
        ok += mine == pinned; print(f'{d}{suffix}.i64: emulated {mine[:16]}..., pinned in HASHES.json {str(pinned)[:16]}...  {"MATCH" if mine == pinned else "DIFFERENT"}')
print(f'{ok} of 12 emulated order files are byte-identical to the pinned PyTorch-generated files')
