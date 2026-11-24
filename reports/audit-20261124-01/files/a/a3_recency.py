"""POST HOC, descriptive (auditor A). F3 of the 23 November correction WITHOUT PyTorch.

The batch orders are not published; the record regenerates them with torch.randperm (text_engine.orders: epoch e's order
is torch.randperm(n, generator=torch.Generator().manual_seed(999 + adapt_order_seed + e))). This script EMULATES that call
with a pure-Python MT19937 (32-bit seed, init_genrand) and the swap loop I recall from PyTorch's CPU randperm
(for i in 0..n-2: z = next_u32 % (n - i); swap r[i], r[i + z]).  The emulation is my reconstruction, not PyTorch itself, so it
is validated three ways before use: (1) MT19937 test vectors and NumPy's legacy MT19937; (2) the 36 published set sizes in
reports/readme-revision-20261113-01/OUTPUT.txt and the 18 published per-draw loss differences in the 11 November RESULTS.json;
(3) the losses: sequences the order says were trained in a quarter lose more loss in it (and a seed shifted by 1 does not).
Usage: python a3_recency.py <repo root> <bundle dir>
"""
import itertools, json, re, sys
from pathlib import Path

import numpy as np

root, bundle = Path(sys.argv[1]), Path(sys.argv[2])
N, U, B = 16384, 1024, 16


class MT:
    def __init__(self, seed):
        s = [seed & 0xFFFFFFFF]
        for i in range(1, 624): s.append((1812433253 * (s[-1] ^ (s[-1] >> 30)) + i) & 0xFFFFFFFF)
        self.s, self.i = s, 624

    def twist(self):
        s = self.s
        for k in range(624):
            y = (s[k] & 0x80000000) | (s[(k + 1) % 624] & 0x7FFFFFFF)
            s[k] = s[(k + 397) % 624] ^ (y >> 1) ^ (0x9908B0DF if y & 1 else 0)
        self.i = 0

    def u32(self):
        if self.i >= 624: self.twist()
        y = self.s[self.i]; self.i += 1
        y ^= y >> 11; y ^= (y << 7) & 0x9D2C5680; y ^= (y << 15) & 0xEFC60000; y ^= y >> 18
        return y & 0xFFFFFFFF


def randperm(n, seed):
    g = MT(seed); r = list(range(n))
    for i in range(n - 1):
        z = g.u32() % (n - i)
        r[i], r[i + z] = r[i + z], r[i]
    return np.array(r, dtype=np.int64)


# (1) the generator itself
g = MT(5489); first = g.u32(); [g.u32() for _ in range(9998)]; tenk = g.u32()
print(f'MT19937 seed 5489: first output {first} (standard 3499211612), 10000th {tenk} (standard 4123659995)')
rs = np.random.RandomState(2419856979); g = MT(2419856979)
print('equals NumPy legacy MT19937 raw 32-bit stream for seed 2419856979 (2,000 outputs):',
      [g.u32() for _ in range(2000)] == [int(x) for x in rs.randint(0, 2**32, size=2000, dtype=np.uint64)])

man = json.loads((bundle / 'MANIFEST.json').read_bytes()); draws = sorted(man['draws'])
print('order seeds 999 + adapt_order_seed + e stay below 2^32:', all(man['draws'][d]['seeds']['adapt_order_seed'] + 999 + 4 < 2**32 for d in draws))


def arm(d, width, tag):
    a = man['draws'][d]['widths'][str(width)]; rec = json.loads((bundle / a['arms'][tag]['record']['path']).read_bytes())
    arr = np.frombuffer((bundle / a['arms'][tag]['arrays']['path']).read_bytes(), '<f4').reshape(-1, N + 512)
    e0 = np.frombuffer((bundle / a['E0']['path']).read_bytes(), '<f4')
    return [float(x) for x in rec['layout']['block_epochs']], arr, e0


def pos_of(orders):
    pos = np.empty_like(orders)
    for e in range(orders.shape[0]): pos[e, orders[e]] = np.arange(N)
    return pos


orders, ctrl = {}, {}
for d in draws:
    seed = man['draws'][d]['seeds']['adapt_order_seed']
    orders[d] = np.stack([randperm(N, 999 + seed + e) for e in (1, 2, 3, 4)])
    ctrl[d] = np.stack([randperm(N, 999 + seed + 1 + e) for e in (1, 2, 3, 4)])

# (3) the losses: trained-minus-untrained loss change per quarter window, emulated orders and the seed + 1 control
steps = [(0.0, 0.25, 1, 1), (0.25, 0.5, 1, 2), (2.0, 2.25, 3, 1), (2.25, 2.5, 3, 2), (2.5, 2.75, 3, 3), (2.75, 3.0, 3, 4), (3.0, 3.25, 4, 1), (3.25, 3.5, 4, 2)]
for name, O in (('emulated orders', orders), ('seed + 1 control', ctrl)):
    gaps = []
    for d in draws:
        q = pos_of(O[d]) // (N // 4) + 1
        for width in (512, 768):
            for tag in ('lr1e-04', 'lr3e-04'):
                ep, arr, e0 = arm(d, width, tag)
                for t0, t1, e, k in steps:
                    a0 = e0[:N] if t0 == 0.0 else arr[ep.index(t0), :N]
                    dl = arr[ep.index(t1), :N].astype(np.float64) - a0.astype(np.float64); tr = q[e - 1] == k
                    gaps.append(dl[tr].mean() - dl[~tr].mean())
    print(f'loss change, trained minus untrained in the quarter ({name}; {len(gaps)} arm-windows): mean {np.mean(gaps):+.4f}, range {min(gaps):+.4f} to {max(gaps):+.4f} nats')

# (2) published set sizes (13 November) and per-draw loss differences on the sets (11 November RESULTS.json)
pub = {}
for line in (root / 'reports/readme-revision-20261113-01/OUTPUT.txt').read_text(encoding='utf-8').splitlines():
    m = re.match(r'^(m0\d)\s+(\d)\s+\S+\s+(\d+),\s*\S+\s+(\d+),', line)
    if m: pub[(m.group(1), int(m.group(2)))] = (int(m.group(3)), int(m.group(4)))
res = json.loads((root / 'reports/natural-text-matched-assistant-posthoc-20261111-01/RESULTS.json').read_bytes())['values']
size_ok, worst_loss, out = 0, 0.0, {}
for k in (1, 2, 3):
    ages, tvs, sizes = [], [], []
    for di, d in enumerate(draws):
        pos = pos_of(orders[d])[:3]; quarter = pos // (N // 4) + 1; rank = pos // B + 1
        m5 = np.all(quarter >= 5 - k, axis=0); m7 = np.all(quarter <= k, axis=0)
        size_ok += (int(m5.sum()), int(m7.sum())) == pub[(d, k)]; sizes += [int(m5.sum()), int(m7.sum())]
        ep5, a5, _ = arm(d, 512, 'lr1e-04'); ep7, a7, _ = arm(d, 768, 'lr1e-04')
        mine = float(a5[ep5.index(3.0), :N][m5].astype(np.float64).mean() - a7[ep7.index(2 + k / 4), :N][m7].astype(np.float64).mean())
        worst_loss = max(worst_loss, abs(mine - res[f'matched|lr1e-04|k{k}|loss_every'][di]))
        for e in range(3):          # age of pass e in updates before the readout: 512 at update 3072, 768 at 2048 + 256 k
            ages.append(((3072 - (e * U + rank[e][m5])).mean() - (2048 + 256 * k - (e * U + rank[e][m7])).mean(), d, e + 1))
        cells = list(itertools.product(range(1, k + 1), repeat=3))
        q5, q7 = quarter[:, m5] - (4 - k), quarter[:, m7]
        h5 = np.array([np.all(q5 == np.array(c)[:, None], axis=0).mean() for c in cells]); h7 = np.array([np.all(q7 == np.array(c)[:, None], axis=0).mean() for c in cells])
        tvs.append((float(np.abs(h5 - h7).sum() / 2), d))
    worst = max(ages, key=lambda x: abs(x[0])); tv = max(tvs)
    print(f'k = {k}: set sizes {min(sizes)}-{max(sizes)}; largest |mean age difference| {abs(worst[0]):.5f} updates (draw {worst[1]}, pass {worst[2]}, signed {worst[0]:+.5f}); '
          f'largest joint quarter-cell TV {tv[0]:.5f} (draw {tv[1]}; {k ** 3} cell{"s" if k > 1 else ""}); mean |age difference| over 18 draw-passes {np.mean([abs(a[0]) for a in ages]):.3f}; '
          f'window width {256 * k} updates')
print(f'published set sizes reproduced: {size_ok} of 18 (draw, k) pairs; largest difference from the 18 published loss_every values: {worst_loss:.2e}')
