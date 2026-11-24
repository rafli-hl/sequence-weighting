"""POST HOC audit script (auditor B): checks the power argument of N8-protocol-draft.md section 7 numerically. NumPy only.
It reads only N7's PUBLISHED per-draw contrasts (reports/natural-text-matched-analysis-20261105-01/MATCHED.csv) to recompute the
planning effects and SDs. It uses no N8 data and estimates no N8 result: every number below is a design calculation.

Power of the registered rule: a hypothesis is CONFIRMED if the two-sided 95% t interval lies entirely on the predicted side of 0,
i.e. T = sqrt(n) * mean / sd > t_{0.975, n-1} with the sign oriented to the prediction. Under normal draws T is noncentral t with
df = n - 1 and noncentrality d * sqrt(n), d = effect / SD.
  P(T > c) = E_V[ Phi(delta - c * sqrt(V / df)) ],  V ~ chi-square(df)        (exact; evaluated by quadrature)
and, independently, by Monte Carlo simulation of normal samples.
"""
import csv, math, sys
import numpy as np
REPO = sys.argv[1]

def phi(x): return 0.5 * (1.0 + np.vectorize(math.erf)(np.asarray(x, dtype=float) / math.sqrt(2.0)))

def t_cdf(t, df, m=200001):
    # integral of the t density by Simpson's rule on a transformed grid (u = atan(x/sqrt(df)))
    a = math.atan(t / math.sqrt(df)); u = np.linspace(-math.pi / 2, a, m)
    # density of U: f_T(x) dx with x = sqrt(df) tan u, dx = sqrt(df) sec^2 u du  ->  C * cos(u)^(df-1)
    c = math.exp(math.lgamma((df + 1) / 2) - math.lgamma(df / 2)) / math.sqrt(math.pi)
    y = c * np.cos(u) ** (df - 1); h = (u[-1] - u[0]) / (m - 1)
    return float(h / 3 * (y[0] + y[-1] + 4 * y[1:-1:2].sum() + 2 * y[2:-1:2].sum()))

def t_quantile(p, df):
    lo, hi = 0.0, 50.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if t_cdf(mid, df) < p: lo = mid
        else: hi = mid
    return (lo + hi) / 2

def nct_upper(c, df, delta, m=400001):
    # P(T > c) for noncentral t: integrate over S = sqrt(V/df), V ~ chi2(df).  density of S: 2 df s * f_chi2(df s^2)
    s = np.linspace(1e-9, 6.0, m)
    logf = math.log(2) + math.log(df) + np.log(s) + ((df / 2 - 1) * np.log(df * s * s) - df * s * s / 2 - (df / 2) * math.log(2) - math.lgamma(df / 2))
    y = np.exp(logf) * phi(delta - c * s); h = s[1] - s[0]
    return float(h / 3 * (y[0] + y[-1] + 4 * y[1:-1:2].sum() + 2 * y[2:-1:2].sum()))

def power(n, d): return nct_upper(t_quantile(0.975, n - 1), n - 1, d * math.sqrt(n))

def mc(n, d, reps=400000, seed=20261123):
    rng = np.random.default_rng(seed); x = rng.standard_normal((reps, n)) + d
    t = x.mean(axis=1) / (x.std(axis=1, ddof=1) / math.sqrt(n)); return float((t > t_quantile(0.975, n - 1)).mean())

# ---- the planning inputs, recomputed from N7's published per-draw values
rows = list(csv.DictReader(open(REPO + '/reports/natural-text-matched-analysis-20261105-01/MATCHED.csv', encoding='utf-8')))
def stat(name):
    v = np.array([float(r['value']) for r in rows if r['statistic'] == name and r['status'] == 'READ']); n = len(v)
    m, sd = v.mean(), v.std(ddof=1); q = t_quantile(0.975, n - 1); return n, m, sd, m - q * sd / math.sqrt(n), m + q * sd / math.sqrt(n)
print('check of my t quantiles: t(.975,5) = %.6f (2.570582), t(.975,23) = %.6f (2.068658), t(.975,7) = %.6f (2.364624)' % (t_quantile(0.975, 5), t_quantile(0.975, 23), t_quantile(0.975, 7)))
for name in ('P1', 'S3'):
    n, m, sd, lo, hi = stat(name); print(f'N7 {name}: n={n} mean={m:+.6f} sd={sd:.6f} interval=[{lo:+.6f}, {hi:+.6f}]  half effect={m / 2:+.6f}  d(full)={abs(m) / sd:.4f}  d(half)={abs(m) / 2 / sd:.4f}')
_, m1, s1, _, _ = stat('P1'); _, m2, s2, _, _ = stat('S3')

# ---- the protocol's planning values
E1, SD1, E2, SD2 = 0.00454, 0.00485, 0.00227, 0.00324
d1, d2 = E1 / SD1, E2 / SD2
print(f"\nprotocol's planning values: H1 d = {d1:.4f}, H2 d = {d2:.4f}")
print('draws | H1 exact (MC) | H2 exact (MC) | Bonferroni lower bound | protocol table')
table = {12: (0.84, 0.60, 0.44), 16: (0.94, 0.74, 0.68), 20: (0.98, 0.84, 0.82), 24: (0.99, 0.91, 0.90)}
for n in (12, 16, 20, 21, 22, 23, 24):
    p1, p2 = power(n, d1), power(n, d2)
    print(f'{n:5d} | {p1:.4f} ({mc(n, d1):.4f}) | {p2:.4f} ({mc(n, d2):.4f}) | {p1 + p2 - 1:.4f} | {table.get(n, "")}')
u1, u2 = abs(m1) / 2 / s1, abs(m2) / 2 / s2
print(f"\nsame table with the unrounded N7 values (H1 d = {u1:.4f}, H2 d = {u2:.4f}):")
for n in (12, 16, 20, 24):
    p1, p2 = power(n, u1), power(n, u2); print(f'{n:5d} | {p1:.4f} | {p2:.4f} | {p1 + p2 - 1:.4f}')
p1, p2 = power(8, 2 * u1), power(8, 2 * u2); print(f'    8 draws, full unrounded effects: H1 {p1:.4f}  H2 {p2:.4f}  lower bound {p1 + p2 - 1:.4f}')
f_ = (2 / 3) * 2 / 1.5; p1, p2 = power(24, f_ * u1), power(24, f_ * u2); print(f'   24 draws, two-thirds effects, SDs x 1.5, unrounded: H1 {p1:.4f}  H2 {p2:.4f}  lower bound {p1 + p2 - 1:.4f}')
print('\nfull N7 effects (protocol: 8 draws give joint power of at least 0.92):')
for n in (6, 7, 8):
    p1, p2 = power(n, 2 * d1), power(n, 2 * d2); print(f'  n={n}: H1 {p1:.4f}  H2 {p2:.4f}  lower bound {p1 + p2 - 1:.4f}')
print('two-thirds of N7 effects, SDs x 1.5 (protocol: 24 draws give a lower bound of 0.81):')
f = (2 / 3) * 2 / 1.5
for n in (20, 24):
    p1, p2 = power(n, f * d1), power(n, f * d2); print(f'  n={n}: H1 {p1:.4f}  H2 {p2:.4f}  lower bound {p1 + p2 - 1:.4f}')
print('\nnot in the protocol, for context (same rule, 24 and 20 draws):')
for label, k in (('half effects, SDs x 1.5', 1 / 1.5), ('half effects, SDs x 2', 0.5), ('one-third effects, N7 SDs', 2 / 3)):
    for n in (24, 20):
        p1, p2 = power(n, k * d1), power(n, k * d2); print(f'  {label:28s} n={n}: H1 {p1:.3f}  H2 {p2:.3f}  lower bound {max(p1 + p2 - 1, 0):.3f}  product (if independent) {p1 * p2:.3f}')
# chi-square 95% interval for a SD estimated from 6 draws (df 5): how uncertain the planning SD is
def chi2_cdf(x, df, m=200001):
    v = np.linspace(1e-12, x, m); y = np.exp((df / 2 - 1) * np.log(v) - v / 2 - (df / 2) * math.log(2) - math.lgamma(df / 2)); h = v[1] - v[0]
    return float(h / 3 * (y[0] + y[-1] + 4 * y[1:-1:2].sum() + 2 * y[2:-1:2].sum()))
def chi2_q(p, df):
    lo, hi = 1e-9, 100.0
    for _ in range(100):
        mid = (lo + hi) / 2
        if chi2_cdf(mid, df) < p: lo = mid
        else: hi = mid
    return (lo + hi) / 2
a, b = chi2_q(0.025, 5), chi2_q(0.975, 5)
print(f'\n95% interval for a true SD given an SD s estimated from 6 draws (normal draws): [{math.sqrt(5 / b):.3f} s, {math.sqrt(5 / a):.3f} s]')

# ---- false-positive rate of the joint rule on the boundary of the null (H1 true effect 0, H2 effect large): at most 2.5%
rng = np.random.default_rng(1); n = 24; reps = 400000; q = t_quantile(0.975, n - 1)
x = rng.standard_normal((reps, n)); y = rng.standard_normal((reps, n)) - 5.0
t1 = x.mean(1) / (x.std(1, ddof=1) / math.sqrt(n)); t2 = y.mean(1) / (y.std(1, ddof=1) / math.sqrt(n))
print(f'simulated P(both CONFIRMED | H1 effect = 0, H2 effect = -5 SD), n = 24: {float(((t1 > q) & (t2 < -q)).mean()):.4f}  (bound 0.025)')

# ---- the envelope claim: the lower t limit is concave in the contrasts, so its minimum over a box is at a vertex
rng = np.random.default_rng(7); worst = -math.inf
for trial in range(200):
    n = int(rng.integers(3, 9)); a = rng.normal(0, 1, n); b = a + rng.normal(0, 1, n); q = t_quantile(0.975, n - 1)
    def lower(v): return v.mean(-1) - q * v.std(-1, ddof=1) / math.sqrt(n)
    idx = np.arange(1 << n); pick = ((idx[:, None] >> np.arange(n)) & 1).astype(bool); vmin = lower(np.where(pick, b, a)).min()
    u = rng.random((20000, n)); imin = lower(a + u * (b - a)).min(); worst = max(worst, vmin - imin)
print(f'envelope: over 200 random boxes (3-8 draws), largest (vertex minimum of the lower limit minus the lowest of 20,000 sampled interior points): {worst:.3e} (<= 0 means no interior point was lower than the best vertex)')
