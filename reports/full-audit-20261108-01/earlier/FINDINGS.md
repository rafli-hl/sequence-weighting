# Area 7 — the earlier studies after N7: findings

Written 8 Nov 2026 by the orchestrating assistant from `RECOMPUTE_EARLIER.log`/`.json`, `PUBLIC_BLOB_CHECK.json` and `SPOTCHECK_EXTRA_OUTPUT.txt`. The one new computation was running `spotcheck_extra.py`, whose output had not been saved.

## Held

- RESPONSE §5 rows 1–3 reproduce from the result tables: S −0.796 [−0.982, −0.609] 12/12 (S32 −0.817, SD −0.794, S_batch −0.851); N4 P1 −0.1886 [−0.2083, −0.1688], P3 +0.9090; N5 M −0.0066 [−0.0076, −0.0055], FALL +0.0040 [+0.0010, +0.0069] 9/10; N6 D1 +0.0192, D2 +0.0158, D4 −0.0050 [−0.0090, −0.0010], FALL +0.0014 4/6, 768 rate effect +0.0047 [+0.0015, +0.0079]. Per-point recomputations match the stored columns to 0.
- Evidence chains: 184/184 and 72/72 claims pass their own check records.
- 60 earlier files are byte-identical in public; N6's fixed-update D4 and D2 agree with N7's S3 and S5.

## Findings

- **E-1 (major, reword).** N6's post-hoc matched figures are inflated by coarse interpolation. RESPONSE §4/§5 interpolate 768's p\* linearly between E2 and E3; N7's dense readouts show a first-quarter jump, so the line under-reads 768 near E2.3. On N7's own draws the coarse rule gives P1 +0.01495 (dense +0.00909), S1 +0.01128 (+0.00808), S4 +0.01806 (+0.01394). Applying N7's within-epoch shape to N6: D4 train +0.0132 → ≈ +0.0064, D4 gap +0.0101 → ≈ +0.0040, D2 train +0.0177 → ≈ +0.0164, D1 train +0.0027 → ≈ +0.0111 (the D1 transfer uses a 512/768 shape for a 384 arm). Reword claim 4; drop or mark unresolved "the 384→512 rise is mostly training progress"; the paper must say the N6 values are coarse and upper-biased.
- **E-2 (minor, reword).** N7's means lie outside N6's intervals for P1 (0.0091 < 0.0106) and S4 (0.0139 < 0.0147); ratios 0.69–0.90. The note states only the converse.
- **E-3 (minor, reword).** RESPONSE §4's D2 matched on the gap (+0.0132) is not reproduced by matching 768 on 512's target (no draw holds it); the review read the other arm. §4 should state the direction per cell.
- **E-4 (minor, reword).** Claim 5's "residual stays open" at 768 (+0.0047): N7 gives +0.0020 [−0.0013, +0.0052], spanning 0.
- **E-5 (note).** Public `NATURAL_TEXT_STUDIES.md` now names PR #5 and the reopening; no stale "only the peak confirmation" sentence remains.
- **E-6 (note).** Failure reports and the 4 Nov DECISION.md are public, identical and consistent.

No blocker. E-1 changes a published sentence.
