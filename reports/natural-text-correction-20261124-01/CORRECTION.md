# Correction to the record, 24 November 2026

**Status:** issued by the owner. It follows the audit of version 2.1 ([`AUDIT.md`](../audit-20261124-01/AUDIT.md),
post hoc and AI-made) and the clean-room reproduction of N7's analysis
([`README.md`](../clean-room-reproduction-20261124-01/README.md)).
**Scope:** it corrects two statements of the [23 November correction](../natural-text-correction-20261123-01/CORRECTION.md)
and one of the README, and states two points of N7's analysis that its protocol left unwritten. It does not edit any
historical file, change any registered number or label, or report any new run. No figure of the 23 November
correction changes.

## 1. The later bracket end and S4 (the audit's A2 and E5)

The 23 November correction, §1, said: "Reading every draw at its later end gives the smallest mean contrast, but not
the smallest lower t limit". That is true of P1 and S1. **It is false for S4:** over the 64 combinations of bracket
ends, S4's lowest lower t limit is reached with every draw at its later end.

| Step | All later ends: lower limit | Lowest lower limit over 64 combinations | Reached at |
|---|---|---|---|
| P1 | +0.00216 | +0.0000764 | m01 at the earlier end, the others later |
| S1 | +0.00099 | −0.0000507 | m02 at the earlier end, the others later |
| S4 | −0.00027 | −0.000268 | every draw at the later end: the same reading |

P1's lower limit is above 0 in all 64 combinations. S1's is at or below 0 in 1 of them, and S4's in 5.

**What changes:**
- Read the sentence as "for P1 and S1, reading every draw at its later end gives the smallest mean contrast but not
  the smallest lower t limit; for S4 it gives both". `README.md` and `METHODS.md` now say so. `METHODS.md` had set S4's
  −0.000268 "against" −0.00027, which is one number at two precisions.
- The README's limitation 4 said "S4's sign depends on this". S4's mean is above 0 in all 64 combinations (lowest
  +0.01043). What depends on the bracket end is whether an interval excludes 0: S4's under five combinations, and S1's
  under one.

**Reproduced by:** the audit's `a1_envelope.py` and `c04_n7_check.py`, and N8's `test_on_n7.py`.

## 2. The zero at k = 1 (the audit's A3)

The 23 November correction, §3, gave the largest total-variation distance between the two exposure-matched sets'
joint distributions over quarter cells as 0.000, 0.037 and 0.037 at k = 1, 2 and 3. **The 0.000 is zero by
construction:** at k = 1 each pass has one quarter, so there is one cell. The balance figure the external audit gave
at k = 1 was the largest marginal Kolmogorov–Smirnov distance, 0.119, which the 23 November correction left out. It
reproduces (0.11920, draw m02, the second pass), with 0.034 and 0.018 at k = 2 and 3. `METHODS.md` now gives it.

## 3. Two points the protocol does not fix (the clean-room reproduction)

A separate AI session implemented N7's analysis from the protocol, the technical note and the released losses, and
logged where the written specification did not decide the computation. Two of those points matter enough to state:

- **Tied weights.** The estimator sorts sequences by weight with a stable sort, so tied weights keep their sequence
  order and get consecutive ranks. N7's six draws have 3, 4, 1, 1, 1 and 1 surplus tied weights. Ranking ties by the
  empirical CDF instead moves p\* by at most 8.8e-9.
- **Mean losses.** The mean training and validation losses, the gap and every matching target are the values in the
  worker's records (`train_loss`, `validation_loss`), not means recomputed from the arrays. The two agree within
  8.55e-7, the registered `records_against_arrays` figure. Using array means instead moves a matched value by at most
  6.8e-7 and an interpolation weight by at most 4.5e-5.

Neither can move a label: the interval limit nearest to 0 is S3's upper limit, −0.00114. `METHODS.md` now states
both.

## What does not change

No registered number, label, sealed file or historical file changes. The 23 November `CORRECTION.md` is not edited.
The other findings of the audit are handled as its [`README.md`](../audit-20261124-01/README.md) lists.

Living pages changed for this note: `README.md` (the note under the sensitivity table, and limitation 4) and
`METHODS.md` (§4, §5 and §6).
