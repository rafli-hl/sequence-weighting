# Correction to the final claims, 9 November 2026

**Status:** issued by the owner on 9 Nov 2026, following the read-only audit of 8 Nov 2026
([`AUDIT.md`](../full-audit-20261108-01/AUDIT.md), `3829b25edcb078c2131255cd84ce865bd74cef8d8df409e963bbb5e11468506c`).
**Amended 9 November 2026,** after an external audit: section 1 now calls N6's figures biased upward rather than
upper bounds, and the sign-test paragraph gives the exact test first. Nothing else changed.
**Scope:** this note corrects how two published claims should be read. It does not edit any earlier file, change any
sealed label, or report any new run. All figures below are post hoc and computed from published per-readout tables.

**Files it qualifies:**

- `reports/adversarial-review-response-20261104-01/RESPONSE.md`
  (`d265bbffca504e7fad7cfba4864c2c338511bca0af7cfdaff5c631aa88600523`), section 4 and claims 4 and 5 of section 5.
- `reports/adversarial-review-response-note-20261106-01/CLAIMS_4_AND_5_STATUS.md`
  (`99071bcc2fe0cb2e3766fce61255bff9ad47d0d4d928c552559f1a74e6035693`).
- `reports/natural-text-matched-result-20261105-01/RESULT.md`, the CONFIRMED label of S4.

## Summary

1. N6's matched-progress figures are biased upward. They were interpolated linearly across a whole epoch, and N7
   shows that p\* does not move linearly within an epoch.
2. The sentence "The 384→512 rise is mostly training progress (+0.0027 at matched training loss)" in claim 4 is
   withdrawn. Whether the rise is mostly training progress is unresolved.
3. N7's S4 keeps its sealed label, CONFIRMED, but that label depends on interpolating between readouts. P1 and S1 do not.

## 1. N6's matched figures are biased upward

N6 had readouts at epochs 0.25, 0.5, 1, 2 and 3. Section 4 of `RESPONSE.md` read one width at the other's epoch-3
training loss by interpolating linearly between epochs 2 and 3. N7 added readouts every quarter epoch from epoch 2 and
showed that in every arm p\* rises most in the first quarter after an epoch boundary. A straight line across a whole
epoch therefore reads the wider model too low just after the boundary, where the matched points fall, and overstates
the contrast.

Applying N6's rule to N7's own draws measures the size of the effect:

| N7 contrast | N6's rule (epochs 2 and 3 only) | N7's rule (quarter-epoch readouts) | Overstatement |
|---|---|---|---|
| P1: 1e-4, matched training NLL | +0.01495 | +0.00909 | +0.0059 |
| S1: 1e-4, matched gap | +0.01128 | +0.00808 | +0.0032 |
| S4: 3e-4, matched training NLL | +0.01806 (5 draws) | +0.01394 | +0.0041 |

For S4, one draw's target lies past epoch 3, so N6's rule reads only five draws. Extrapolating that draw instead gives
an overstatement of about +0.003.

**What changes:**

- The matched figures in section 4 of `RESPONSE.md`, and the "+0.0132, post hoc" in claim 4, should be read as biased
  upward, not as estimates. This is a diagnosis made on N7's draws; it does not establish a mathematical bound for
  N6's own, unobserved trajectories. The fixed-update figures (D2 and D4, the pre-registered ones) involve no interpolation and are
  unaffected.
- `CLAIMS_4_AND_5_STATUS.md` notes that each of N6's means lies inside N7's interval and that each N7 mean is closer to
  0. Both statements hold, and the second is at least partly due to the coarser rule. It should also be said that N7's
  means lie outside N6's intervals for P1 (+0.00909 against [+0.0106, +0.0158]) and S4 (+0.01394 against
  [+0.0147, +0.0206]).
- N7's own figures stand. N7's readouts bracket each matched point within a quarter epoch.

## 2. The 384→512 sentence in claim 4 is withdrawn

The figure +0.0027 in claim 4 is N6's D1 (512 − 384 at 3e-4) matched on training NLL. It was interpolated in the
same way as the figures above. N7 has no width 384, so the size of the bias for this contrast cannot be measured
directly. The audit's estimate, which borrows N7's within-epoch shape from widths 512 and 768, puts the corrected
figure near +0.011, against +0.0192 at fixed updates. That estimate is too indirect to stand in for the figure.

**What changes:** the sentence "The 384→512 rise is mostly training progress (+0.0027 at matched training loss)" is
withdrawn. Whether the rise from 384 to 512 at 3e-4 is mostly training progress is unresolved. The rest of claim 4 is
unchanged, read with section 1 of this note.

## 3. S4 depends on the interpolation

Each of N7's matched steps reads width 768 by linear interpolation between the two quarter-epoch readouts whose
training NLL brackets the target. If p\* stays between those readouts, the least favourable reading for a positive
contrast takes 768 at the later end of its bracket:

| Step | Sealed (interpolated) | Later end of each bracket | Draws > 0 |
|---|---|---|---|
| P1 | +0.00909 [+0.00400, +0.01417] | +0.00702 [+0.00216, +0.01189] | 5/6 |
| S1 | +0.00808 [+0.00487, +0.01130] | +0.00399 [+0.00099, +0.00699] | 5/6 |
| S4 | +0.01394 [+0.00893, +0.01896] | +0.01043 [−0.00027, +0.02113] | 5/6 |

In draw m06 at 3e-4, the target falls in 768's step from epoch 3 to 3.25, where p\* rises by +0.0224. S4's interval
then includes 0.

**What changes:** S4's label, CONFIRMED, stands as sealed, and so does the fixed sequence that reached S5. Any
statement of S4 should add that it depends on the interpolation. P1 and S1 stay above 0 under the least favourable
reading. P1's bound was already reported in `CLAIMS_4_AND_5_STATUS.md`.

## Also disclosed

- **Realised spread.** N7 was planned from N6's spread of P1 (sd 0.0025) and N6's effect (+0.0132), at which the
  power of P1 exceeded 0.999. On N7, P1's sd was 0.0048 (1.94 times the planning value) and its mean 0.69 times the
  planning effect. That is close to the protocol's most pessimistic cell, with power 0.703. The planning effect was
  itself one of the upper-biased figures of section 1.
- **Sign tests.** All six draws of P1 are positive, so the exact two-sided sign test gives p = 0.031. One of them is
  +0.00002, and one draw of S3 is −0.00014; counting such values as ties, a post-hoc convention, gives p = 0.0625. The
  labels rest on the t intervals, as the protocol specifies.

## How these figures were obtained

The section 1 and 3 figures were computed by the audit (`verify_orchestrator.py`, checks V1 and V2, output in
`VERIFY_ORCHESTRATOR.txt`, both in the audit folder). They were then recomputed independently from
`reports/natural-text-matched-analysis-20261105-01/POINTS.csv` in a separate session, and they match to the digits
shown. The realised spread is check V4 of the same script. The section 2 estimate is the audit's
(`earlier/FINDINGS.md`, finding E-1) and was not recomputed.
