"""Reproduce the post-hoc exposure analysis of 11 November 2026 and compare it with the published values.

    python tools/verify_posthoc.py PATH/TO/n7-loss-arrays

Runs reports/natural-text-matched-assistant-posthoc-20261111-01/posthoc_exposure.py on the N7 loss-array bundle of
the v1.2 release, writing its per-draw values to a temporary file, and compares them with the published RESULTS.json:
the same keys, and every value within an absolute tolerance of 1e-6, as in tools/verify_n7_losses.py. Builds of the
same library versions on different machines can move a fit on a flat objective in its eighth decimal (1.4e-8 was seen
on GitHub's runner), far below any printed digit. The script itself stops, and this check fails,
if the regenerated batch orders do not pass its checks against the losses. Needs the versions pinned in
tools/requirements-posthoc.txt (PyTorch 2.7.0 regenerates the original orders).
"""
import json
import math
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FOLDER = ROOT / "reports/natural-text-matched-assistant-posthoc-20261111-01"
TOL = 1e-6


def main(bundle):
    published = json.loads((FOLDER / "RESULTS.json").read_text(encoding="utf-8"))["values"]
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "RESULTS.json"
        run = subprocess.run([sys.executable, "-I", str(FOLDER / "posthoc_exposure.py"), str(bundle), str(out)],
                             capture_output=True, text=True)
        if run.returncode != 0:
            print(run.stdout[-2000:], run.stderr[-4000:], sep="\n")
            sys.exit(f"posthoc_exposure.py exited with code {run.returncode}")
        fresh = json.loads(out.read_text(encoding="utf-8"))
    print(f"ran with numpy {fresh['numpy']}, torch {fresh['torch']}")
    values = fresh["values"]
    missing, extra = sorted(set(published) - set(values)), sorted(set(values) - set(published))
    worst, worst_key, bad = 0.0, None, []
    for key in sorted(set(published) & set(values)):
        a, b = published[key], values[key]
        if len(a) != len(b):
            bad.append(f"{key}: {len(a)} published values, {len(b)} reproduced")
            continue
        for x, y in zip(a, b):
            d = abs(x - y) if not (math.isnan(x) and math.isnan(y)) else 0.0
            if d > worst:
                worst, worst_key = d, key
            if not d <= TOL:
                bad.append(f"{key}: published {x!r}, reproduced {y!r}")
                break
    print(f"keys: {len(published)} published, {len(values)} reproduced; {len(missing)} missing, {len(extra)} extra")
    print(f"largest difference: {worst:.2e}" + (f" ({worst_key})" if worst_key else ""))
    for line in [f"missing: {k}" for k in missing[:10]] + [f"extra: {k}" for k in extra[:10]] + bad[:20]:
        print(" ", line)
    if missing or extra or bad:
        sys.exit("FAIL")
    print("PASS")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
