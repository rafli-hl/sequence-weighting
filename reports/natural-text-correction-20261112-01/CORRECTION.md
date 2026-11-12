# Correction to the record, 12 November 2026

**Status:** drafted on 12 Nov 2026 by an AI assistant (Claude Opus 5.5, Anthropic) at the owner's request, and issued
when the owner merged it into the public record. It follows the follow-up audit of 12 Nov 2026
([`REPORT.md`](../follow-up-audit-20261112-01/REPORT.md)), in which two fresh AI auditors (Claude Fable 5.2) audited
the studies before N7 and alternative explanations for the current claims.
**Scope:** this note corrects statements in the record and says how some results should be read. It does not edit any
historical file, change any sealed label, or report any new run. Every new figure below is post hoc and descriptive;
each is reproduced by [`verify_findings.py`](../follow-up-audit-20261112-01/verify_findings.py), whose output is
[`OUTPUT.txt`](../follow-up-audit-20261112-01/OUTPUT.txt).

## Summary

1. N6's matched figures are biased in the direction set by which arm is interpolated, not always upward.
2. The S4 overstatement in the 9 November correction compares different draws; like for like it is +0.0023.
3. C1, C2 and C3 in `CURRENT_CLAIMS.md` are reworded to carry the qualifications of their sources, and the registered
   outcomes that did not confirm are now listed there.
4. C4 gains a power figure, the effect of the E0 offset, a multiplicity note and a power note for the
   exposure-matched comparison; the scope of every claim gains a note on batch-relative weighting.
5. Three statements in `NATURAL_TEXT_STUDIES.md` are corrected.

## 1. The direction of the bias in N6's matched figures

The [9 November correction](../natural-text-correction-20261109-01/CORRECTION.md), §1, says N6's matched figures are
"biased upward". N6's rule reads whichever arm's epoch-3 value lies on the other arm's path, by linear interpolation
between epochs 2 and 3. p\* rises most in the first quarter after an epoch boundary, so a straight line under-reads the
interpolated arm there. The contrast is p\*(512) − p\*(wider), so it is overstated when the wider arm is the one read,
and understated when 512 is.

Applying N6's rule to N7's draws (coarse minus quarter-epoch reading):

| Type of contrast | Arm read | Draws | Bias of N6's rule |
|---|---|---|---|
| P1: 1e-4, matched training loss | 768 | 6 | +0.0059 [+0.0049, +0.0069], 6/6 |
| S4: 3e-4, matched training loss | 768 | 5 | +0.0023 [+0.0008, +0.0039], 5/5 |
| D2: 3e-4, matched gap | 512 | 5 | −0.0005 [−0.0019, +0.0008], 1/5 |
| D3: 512 at 3e-4 − 768 at 1e-4, matched gap | 512 | 6 | −0.0015 [−0.0023, −0.0008], 0/6 |

**What changes:** read the 9 November correction's "biased upward" as "biased upward where the wider model is the arm
read, which includes D4, the figures that motivated N7; biased downward, by less, where 512 is the arm read (D1, and
D2 and D3 matched on the gap)". The withdrawn sentence about D1 stays withdrawn, and nothing confirmed changes sign:
the downward cells make 512's lead at matched gap slightly larger, not smaller. The arm read can also differ between
draws within one contrast.

## 2. The S4 overstatement compares different draws

The table in the 9 November correction gives S4's overstatement as +0.0041: +0.01806 under N6's rule, on five draws,
against +0.01394, the sealed mean over six. On the same five draws N7's own rule gives +0.0157, so the overstatement is
+0.0023 [+0.0008, +0.0039] (row 2 above). P1's +0.0059 and S1's +0.0032 compare the same draws and stand.

## 3. C1, C2 and C3

- **C1** dropped qualifiers that its source, `RESPONSE.md` §5 claim 1, carried: the WikiText-2 shift follows from C2,
  is not a separate confirmation, and is a lower bound because the epoch-8 peak is at the top of the ladder; and the
  synthetic direction and window were first seen on a ladder whose results were known. It now carries them, with
  units, the count of fits at the estimator's bound (33 of 472 fits, in 19 of 59 corpus-epoch points), and its scope:
  the movement is not monotone, N1 detected none, and N5's secondary moves the other way.
- **C2** now names its readout in its heading. N4's P2 at epoch 24 was INCONCLUSIVE, so the fall is confirmed at
  epoch 32 only. It also states its alignment (equal epochs, with two other alignments that give the same order) and
  that memorisation saturation is not excluded, as `RESPONSE.md` §2 already said.
- **C3** now says that its registered statistic, M, reads both widths by the same whole-epoch interpolation that
  biases N6's figures, and that M's sign flips when 768 is read at the higher end of its brackets (+0.0015
  [+0.0003, +0.0027]). The two widths are read about 0.44 epoch apart, and a p\* curve that depends on the epoch alone
  predicts M (−0.0067 against −0.0066). The claim itself is supported without interpolation: at epoch 2, widths 512
  and 768 have the same gap and p\* differs by −0.0092 [−0.0112, −0.0072], 0/10 positive.
- **Registered outcomes that did not confirm** (N1's primaries A and B, N3's three primaries, N4's P2, N5's FALL, and
  N5's secondary on the peak location) were reported in their own results but on no living page. They are now listed
  in `CURRENT_CLAIMS.md`.

## 4. C4 and the scope of every claim

- **Power.** P1's planned power assumed N6's sd (0.0025) and the effect that selected the hypothesis (+0.0132). N7's
  P1 had sd 0.0048 and mean +0.0091. This was in the 8 November audit (M5) and is now on the claims page.
- **E0 offset.** 768's loss before weighted training is 0.037 nats higher than 512's. Lowering 768's gains by that
  offset makes P1 +0.0062 [−0.0001, +0.0126], 5/6.
- **Exposure-matched comparison.** "The lead of 512 is not seen" stands, but the comparison nearest to equal loss has
  power 0.14 for an effect of P1's size, so it is not evidence of no difference. Within one model, p\* on
  exposure-matched sets barely changes from epoch 2.5 or 2.75 to epoch 3, while whole-set p\* rises.
- **Multiplicity.** With a Bonferroni adjustment over the six exposure-matched comparisons, the whole-set-minus-matched
  differences at 1e-4 include 0 at every readout.
- **Batch-relative weighting.** With the weighted loss averaged over batches of 16 and clipping active on 92–99% of
  updates, a sequence's loss drop grows with its own weight and shrinks, by a similar amount, with its batch-mates'
  summed weight. `RESPONSE.md` §3.8 conceded this as "not quantified"; it is now quantified for N7 and stated in the scope of
  every claim.
- **The training loss** that P1 and S4 match on is now defined on the claims page (8 November audit, M4).

## 5. `NATURAL_TEXT_STUDIES.md`

- "There is no N2" is replaced: N2 was a memory probe of width 768 on 30 October, with an engineering verdict only,
  as both evidence chains record.
- "A game was using the GPU" is replaced by what the failure report says: the run slowed and hit its per-draw time
  limit; a game started on the GPU during the run, and the records cannot prove the cause.
- The summary of the 9 November correction now gives the direction of the bias as in §1.
