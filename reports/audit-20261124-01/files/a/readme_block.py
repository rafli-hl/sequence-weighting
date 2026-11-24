import csv, math, statistics as st

rows = csv.DictReader(open("reports/natural-text-matched-analysis-20261105-01/POINTS.csv"))
P = {(r["draw"], float(r["epoch"]), int(r["width"]), r["tag"]): r for r in rows}
draws, rate = sorted({k[0] for k in P}), "lr1e-04"
path = [e for e in sorted({k[1] for k in P}) if 2.0 <= e <= 3.5]

def read_768(target, d):  # 768's fitted p* where its training loss equals target
    pts = [(float(P[(d, e, 768, rate)]["train"]), float(P[(d, e, 768, rate)]["p"])) for e in path]
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        if min(x0, x1) <= target <= max(x0, x1):
            return y0 if x1 == x0 else y0 + (target - x0) / (x1 - x0) * (y1 - y0)
    return None  # target outside the path: the draw is unavailable

v = []
for d in draws:
    p768 = read_768(float(P[(d, 3.0, 512, rate)]["train"]), d)
    if p768 is not None:
        v.append(float(P[(d, 3.0, 512, rate)]["p"]) - p768)
assert len(v) >= 5, "fewer than five draws: P1 would be UNAVAILABLE"
half = 2.5706 * st.stdev(v) / math.sqrt(len(v))  # t(0.975, df = 5)
print(f"P1 = {st.mean(v):+.5f} [{st.mean(v) - half:+.5f}, {st.mean(v) + half:+.5f}], n = {len(v)}")
