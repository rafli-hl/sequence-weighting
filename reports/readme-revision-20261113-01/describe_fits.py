"""Descriptive summary of N7's 240 published fits (FITS.csv). Post hoc, 13 November 2026; tests nothing.

Usage, from the repository root:  python reports/readme-revision-20261113-01/describe_fits.py
Needs the standard library only.
"""
import csv, statistics as st
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
rows = list(csv.DictReader(open(ROOT / "reports/natural-text-matched-analysis-20261105-01/FITS.csv", encoding="utf-8")))
p = [float(r["p"]) for r in rows if r["p"]]
ratio = [float(r["objective"]) / float(r["J0"]) for r in rows if r["p"]]
neg = [float(r["negative_fraction"]) for r in rows]
total = [float(r["total_gain"]) for r in rows]
print(f"fits: {len(rows)}; defined: {len(p)}; undefined reasons: {sorted({r['reason'] for r in rows if r['reason']}) or 'none'}")
print(f"at the lower bound: {sum(r['lower'] == 'True' for r in rows)}; at the upper bound: {sum(r['upper'] == 'True' for r in rows)}")
print(f"fitted exponent: {min(p):.4f} to {max(p):.4f}")
print(f"objective at the fit / objective at p = 0: median {st.median(ratio):.3f}, range {min(ratio):.3f} to {max(ratio):.3f}")
print(f"fraction of sequences with negative gain: {min(neg):.4f} to {max(neg):.4f}")
print(f"total gain (nats, summed over 16,384 sequences): smallest {min(total):.0f}")
