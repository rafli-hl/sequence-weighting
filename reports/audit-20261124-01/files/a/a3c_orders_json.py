"""POST HOC (auditor A). Can ORDERS.json (the index regenerate_n7_orders.py writes, pinned in N8's HASHES.json and
test_on_n7.py as 8ba4a3c2...) be rebuilt byte for byte from the emulated orders? Its text includes the PyTorch and NumPy
version strings of the machine that wrote it, which are not published, so a few plausible strings are tried.
Usage: python a3c_orders_json.py <repo root> <bundle dir>"""
import hashlib, itertools, json, sys
from pathlib import Path
import numpy as np

root, bundle = Path(sys.argv[1]), Path(sys.argv[2])
ns = {}
exec((Path(__file__).parent / 'a3_recency.py').read_text(encoding='utf-8').split('# (1) the generator itself')[0]
     .replace('root, bundle = Path(sys.argv[1]), Path(sys.argv[2])', ''), ns)
randperm = ns['randperm']
PIN = '8ba4a3c2e7906f65c6335ece7a785bfb37fe1b2904684959d388f589f2287eb1'
N, EPOCHS = 16384, 4
man = json.loads((bundle / 'MANIFEST.json').read_bytes()); index = {}
for d in sorted(man['draws']):
    seed = man['draws'][d]['seeds']['adapt_order_seed']
    for suffix, s in (('', seed), ('-seed-plus-1', seed + 1)):
        o = np.stack([randperm(N, 999 + s + e) for e in range(1, EPOCHS + 1)]).astype('<i8'); b = o.tobytes()
        index[f'{d}{suffix}'] = dict(file=f'{d}{suffix}.i64', bytes=len(b), sha256=hashlib.sha256(b).hexdigest(), seed=s,
                                     epoch_order_sha256=[hashlib.sha256(row.tobytes()).hexdigest() for row in o])
hit = None
for t, n in itertools.product(('2.7.0+cu126', '2.7.0+cpu', '2.7.0'), ('2.5.3', '2.2.6', '2.3.5', '2.5.4')):
    meta = dict(torch=t, numpy=n, n=N, epochs=EPOCHS, layout='rows = epochs 1-4; int64 little-endian sequence indices in training order', orders=index)
    h = hashlib.sha256((json.dumps(meta, indent=1) + '\n').encode('utf-8')).hexdigest()
    if h == PIN: hit = (t, n)
print('ORDERS.json rebuilt byte for byte (SHA-256 equals the pin 8ba4a3c2...):', f'yes, with torch {hit[0]} and numpy {hit[1]}' if hit else 'no, for none of the 12 version-string pairs tried')
