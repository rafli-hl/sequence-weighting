"""POST HOC (auditor A). Writes an ORDERS directory in the layout of N8's analysis/regenerate_n7_orders.py, from the pure-Python
emulation of torch.randperm in a3_recency.py (no PyTorch). The torch and numpy version strings that regenerate_n7_orders.py records in
ORDERS.json are given on the command line, because they are part of the bytes that test_on_n7.py pins.
Usage: python a6_make_orders.py <bundle dir> <new out dir> <torch version string> <numpy version string>"""
import hashlib, json, sys
from pathlib import Path
import numpy as np

bundle, out, tv, nv = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3], sys.argv[4]
ns = {}
exec((Path(__file__).parent / 'a3_recency.py').read_text(encoding='utf-8').split('# (1) the generator itself')[0]
     .replace('root, bundle = Path(sys.argv[1]), Path(sys.argv[2])', ''), ns)
randperm = ns['randperm']; N, EPOCHS = 16384, 4
man = json.loads((bundle / 'MANIFEST.json').read_bytes()); out.mkdir(parents=False, exist_ok=False); index = {}
for d in sorted(man['draws']):
    seed = man['draws'][d]['seeds']['adapt_order_seed']
    for suffix, s in (('', seed), ('-seed-plus-1', seed + 1)):
        o = np.stack([randperm(N, 999 + s + e) for e in range(1, EPOCHS + 1)]).astype('<i8'); b = o.tobytes(); (out / f'{d}{suffix}.i64').write_bytes(b)
        index[f'{d}{suffix}'] = dict(file=f'{d}{suffix}.i64', bytes=len(b), sha256=hashlib.sha256(b).hexdigest(), seed=s,
                                     epoch_order_sha256=[hashlib.sha256(row.tobytes()).hexdigest() for row in o])
meta = dict(torch=tv, numpy=nv, n=N, epochs=EPOCHS, layout='rows = epochs 1-4; int64 little-endian sequence indices in training order', orders=index)
raw = (json.dumps(meta, indent=1) + '\n').encode('utf-8'); (out / 'ORDERS.json').write_bytes(raw)
print(f'wrote {len(index)} order files to {out.name}; ORDERS.json records torch {tv}, numpy {nv}; ORDERS.json SHA-256 {hashlib.sha256(raw).hexdigest()}')
