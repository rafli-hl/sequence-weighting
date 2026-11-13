# Current claims

**As of 12 November 2026; wording revised 13 November 2026, with no claim, number or label changed.** This page states what the project currently claims, in one place. It is maintained for the
publication copy and replaces nothing: the historical records it cites keep their original wording and bytes. Where
this page and an older summary differ, this page is current.

The claims were first set out in [`RESPONSE.md` §5](reports/adversarial-review-response-20261104-01/RESPONSE.md) on
4 November, updated for N7 in
[`CLAIMS_4_AND_5_STATUS.md`](reports/adversarial-review-response-note-20261106-01/CLAIMS_4_AND_5_STATUS.md) on
6 November, and corrected in [`CORRECTION.md`](reports/natural-text-correction-20261109-01/CORRECTION.md) on
9 November. On 11 November a post-hoc analysis of N7's per-sequence losses (`REPORT.md` in
[`natural-text-matched-assistant-posthoc-20261111-01`](reports/natural-text-matched-assistant-posthoc-20261111-01/))
and a second [correction](reports/natural-text-correction-20261111-01/CORRECTION.md) narrowed how C4 and C5 can be
read. On 12 November a [follow-up audit](reports/follow-up-audit-20261112-01/REPORT.md) of the earlier studies and of
alternative explanations led to a third [correction](reports/natural-text-correction-20261112-01/CORRECTION.md): C1–C3
are reworded and qualified, the registered outcomes that did not confirm are listed, and C4 gains a power figure and
three disclosures. No label changed. Every contrast below is p\*(narrower width) − p\*(wider width), with a two-sided 95% t
interval over draws.

## Scope of every claim

Decoder-only Transformers of depth 4, at most 34.7 M parameters, trained on a synthetic task, WikiText-2 or
WikiText-103, with constant learning rates. In every comparison below the widths share one rate. No rate was tuned
on the draws analysed, but each natural-text rate was selected by validation loss on a tuning draw: 3e-5 for widths
128–384 only, 3e-4 as the best mean over eight widths, and 1e-4 as the best of five rates for width 768. No width's
best rate is located. None of the claims concerns the models, scale or regime of the reference study, and none is a
scaling law, a capacity mechanism, a new estimator or a practical benefit of weighting.

A sequence's influence on training depends on its batch. Every natural-text model was trained on batches of 16 with
the loss $\frac{1}{16}\sum_i w_i \ell_i$, which is not divided by the batch's weight sum, and with the norm of the
summed gradient clipped at 1. In N7 clipping was active on 92–99% of updates. Clipping rescales the whole update, so a
sequence's step depends on its batch-mates' weights and gradients; this is not the same as normalising the weights by
their batch sum. In N7 a sequence's loss falls faster with its own weight and slower with the summed weight of its 15
batch-mates, by similar amounts (post hoc;
[follow-up audit](reports/follow-up-audit-20261112-01/REPORT.md), AA-2). p\* describes this recipe. Both widths in
every comparison share it; the record does not estimate how much it shapes the level of p\* or the contrasts.

## The estimator

**E1. p\* is the estimator of the reference study's technical note.** The project fits p\* with the objective defined
in [An Estimator for the Effective Sequence Weight Exponent](https://blog.janestreet.com/a-study-of-sequence-weighting-at-scale/sequence-weighting-note.pdf),
the technical note accompanying [the reference study](https://blog.janestreet.com/a-study-of-sequence-weighting-at-scale/).
The note minimises dᵀKd with K = min(rᵢ, rⱼ) over p ≥ 0, where d is the difference between normalised gains and
normalised wᵖ. The implementation
([`core.py`](preregistration/natural-text-matched-confirmation-20261104/sealed-source/vendor/core.py)) computes the
equivalent mean squared cumulative discrepancy along ascending weight ranks. Its choices beyond the note:

| Choice | Value |
|---|---|
| Range of p | [0, 8]; a fit at the upper bound is refitted with the bound raised to 32 in a sensitivity analysis |
| Search | grid of step 0.05, then 50 ternary steps within the neighbouring cells; best of that point and the two ends |
| Gains | signed: loss before weighted training (E0) minus loss at the readout, per sequence |
| Guards | undefined if the weights are constant or the total gain is at most 1e-10 |
| Tied weights | ranked in their original sequence order (a stable sort) |

The equivalence and the recovery of known exponents are tested by
[`core_checks.py`](outputs/sequence-weighting-pilot/core_checks.py). **Interpretation:** p\* is the best-fitting
non-negative exponent under this objective. A fit of 0 does not show that gains are independent of the weights; gains
that fall with the weight also fit at 0. Gains need not follow a power of the weight: in N7 at epoch 3 the mean gain
is nearly flat over the lower half of the weights and rises over the upper half, where p\* is about 0.20, against 0.015
on the lower half and 0.10 overall (post hoc; follow-up audit, AA-6). The level of p\* depends on the weight range; the
signs of N7's contrasts do not, though P1's and S4's intervals include 0 on the lower half alone.

## The losses

**Training loss**, the quantity P1 and S4 are matched on, is measured at each readout, straight after that readout's
update, in a separate evaluation pass (model in evaluation mode, no gradients; the model has no dropout). For each
training sequence (16,384 in N5–N7) it takes the mean next-token negative log-likelihood over the sequence's 128
targets, in nats; the training loss is the unweighted mean over sequences, so the training weights are not applied.
**Validation loss** is the same mean over the validation sequences (512 in N5–N7), and the **gap** is validation loss minus training loss. A
sequence's **gain** at a readout is its loss before weighted training (E0) minus its loss at the readout. Source:
`losses` and `evaluate` in
[`text_engine.py`](preregistration/natural-text-matched-confirmation-20261104/sealed-source/text_engine.py) and the
readout loop in
[`matched_worker.py`](preregistration/natural-text-matched-confirmation-20261104/sealed-source/matched_worker.py);
the evaluation functions are the same in every natural-text study.

## Claims

**C1. Synthetic task and late WikiText-2 training: the peak moves to smaller widths.** On the synthetic task, the
width of peak p\* moves smaller from epoch 15 to 40: −0.796 doublings of width per doubling of epochs [−0.982,
−0.609], 12/12 corpora. In 19 of 59 defined corpus-epoch points the largest fit is at the estimator's bound (33 of 472
fits), and the direction and window were first seen on an earlier ladder whose results were already known. On
WikiText-2 at 3e-5 over widths 256–768, the highest-p\* width is 768, the top of the ladder, at epoch 8, and 384 at
epoch 32, in 4/4 draws (a shift of at least +0.909 doublings [+0.864, +0.954]; with four draws the exact sign test
gives p = 0.125). That shift follows from C2 and is not a separate confirmation, and it is a lower bound, because the
epoch-8 peak is at the top of the ladder. *Status:* sealed by hash within the project before the runs, not publicly preregistered. Same sign as the reference
study's epoch finding; not a reproduction of it. *Scope:* the movement is not monotone (on WikiText-2 the highest-p\*
width is 512 at epochs 1–2 and 24); N1 detected no shift over widths 64–384 with per-width rates; and over three
epochs on WikiText-103 the peak moves the other way (see the registered outcomes below).

**C2. At epoch 32 of WikiText-2 training, p\* falls with width over 384–768.** At 3e-5, a rate selected only for
widths 128–384, p\* falls with width at epoch 32, 28 epochs past the validation minimum: −0.1886 per doubling of width
[−0.2083, −0.1688], 4/4 (N4's P1). *Status:* sealed by hash within the project before the runs, not publicly preregistered. It is confirmed at this one readout:
N4's P2, the same slope at epoch 24, was INCONCLUSIVE, and at epochs 4–16 the slope is positive. *Alignment:* equal
epochs. The order also holds with 768 read at 384's epoch-32 gap, and for each width's highest p\* over all readouts
(post hoc; follow-up audit, EA-10). *Not excluded:* memorisation saturation. From 512 to 768 the total gain at epoch 32
rises by 44% while p\* × total gain stays flat, and the train–validation gap at 768 is about 3.9 nats (post hoc; AA-4).

**C3. The train–validation gap alone does not determine p\*.** N5's registered statistic M, p\* at 768 minus p\* at
384 at matched gap, is −0.0066 [−0.0076, −0.0055], 0/10 positive. It reads each width by linear interpolation between
readouts up to a whole epoch apart, the rule that biases N6's matched figures (C4), and its sign is not robust to that:
with 768 read at the higher end of each bracket it is +0.0015 [+0.0003, +0.0027] (post hoc). The two widths are also
read at different points of training: 384 about 0.44 epoch later than 768 at the same gap, and a curve in which p\*
depends on the epoch alone predicts M as −0.0067. A curve with no width effect gives the same label in 96–99% of the
protocol's fixture replicates, so M does not show capacity beyond memorisation, although its sealed label reads
CAPACITY_BEYOND_MEMORIZATION. *Status:* sealed by hash within the project before the runs, as M; not publicly preregistered. *Support without interpolation*
(post hoc, N5): at epoch 2 at 3e-4, widths 512 and 768 have the same gap (768 − 512: +0.0004 [−0.0047, +0.0055]) and
p\* differs by −0.0092 [−0.0112, −0.0072], 0/10 positive. The claim rests on that comparison as much as on M.

**C4. At epoch 3 and 1e-4, widths 512 and 768 are ordered one way at equal updates and the other way at equal overall
training loss; at 3e-4 the order is the same on both.** On six fresh WikiText-103 draws (N7), with 512 read at
epoch 3. The table is the registered result; how far it can be read as a reversal between the widths is narrowed
below.

| Learning rate | Comparison | Contrast | Status and qualification |
|---|---|---|---|
| 1e-4 | equal training loss (P1, primary) | +0.00909 [+0.00400, +0.01417], 6/6 | Preregistered publicly, confirmed. Stays above 0 with 768 read at the later end of each interpolation bracket (+0.00702 [+0.00216, +0.01189], 5/6), if p\* stays between bracketing readouts. A comparison of whole-set p\* in which 768 is read at epochs 2.19–2.48: see "How to read C4" |
| 1e-4 | equal train–validation gap (S1) | +0.00808 [+0.00487, +0.01130], 6/6 | Confirmed. Later bracket end: +0.00399 [+0.00099, +0.00699], 5/6 |
| 1e-4 | equal updates, equivalently equal tokens (S3) | −0.00454 [−0.00795, −0.00114], 0/6 | Confirmed, at epoch 3. The interval spans 0 when draw m03 or m05 is left out. By readout, the contrast is above 0 at epochs 0.25–1 and below 0 only from epoch 2.5 |
| 3e-4 | equal training loss (S4) | +0.01394 [+0.00893, +0.01896], 6/6 | Confirmed under the registered interpolation. **At the later bracket end the interval includes 0** (+0.01043 [−0.00027, +0.02113]). One draw decides this: m06, read at epoch 3.083 |
| 3e-4 | equal updates (S5) | +0.01382 [+0.01116, +0.01648], 6/6 | Confirmed |
| 1e-4 | equal validation loss (S2) | — | Unavailable: three draws had a reading, five were needed |

Equal updates means equal tokens seen under the shared batch and context settings; it is not equal compute or equal
time. Equal training loss is a different comparison, not an adjustment that isolates width: it also removes faster
learning, which width causes, and it compares the widths at different points within an epoch. All six P1 contrasts are
positive, so the exact two-sided sign test gives p = 0.031; one of them is +0.00002.

P1's power was planned from N6's spread (sd 0.0025) and the effect that selected the hypothesis (+0.0132), and the
protocol called that estimate likely flattering. N7's P1 has sd 0.0048, 1.9 times the planning value, and mean
+0.0091, 0.69 times the planning effect. The protocol's least favourable case, half the effect with the sd at its
upper 95% limit, gave power 0.703 with six draws. Gains are measured from each width's own loss before weighted
training (E0), and 768's E0 is 0.037 nats higher than 512's on average. Lowering 768's gains by that offset raises its
p\* by +0.0028 [+0.0012, +0.0044] and P1 becomes +0.0062 [−0.0001, +0.0126], 5/6 (post hoc; follow-up audit, AA-3).

**How to read C4: the post-hoc analyses of 11 November.** These are descriptive and were not registered. They move no
label, their intervals are not adjusted for the number of comparisons, and they were made and checked by AI models
only. Their script and exact output are in
[`natural-text-matched-assistant-posthoc-20261111-01`](reports/natural-text-matched-assistant-posthoc-20261111-01/).

- **Exposure differs at equal training loss.** P1 reads 768 at epochs 2.19–2.48, where it has trained on 19–48% of
  the training set a third time; 512 at epoch 3 has trained on all of it. p\* depends on this: within one model,
  sequences already trained in the current epoch have p\* higher by 0.050–0.084 than those not yet trained in it, at
  every readout inside an epoch from epoch 2 (20 of 20 arm-readouts, 6/6 draws each).
- **On exposure-matched sequences at 1e-4, the lead of 512 is not seen.** For 512 at epoch 3 against 768 at epochs
  2.25, 2.5 and 2.75, on sequences matched for the timing of all three passes, the contrasts are −0.0035
  [−0.0258, +0.0189] (4/6), −0.0048 [−0.0121, +0.0026] (2/6) and −0.0051 [−0.0109, +0.0008] (2/6). Each interval
  includes 0. The whole-set contrasts at the same readouts, +0.0100, +0.0040 and −0.0003, exceed them by +0.0135
  [−0.0076, +0.0345], +0.0088 [+0.0032, +0.0143] and +0.0047 [+0.0014, +0.0081]; with a Bonferroni adjustment over
  the six exposure-matched comparisons the last two intervals include 0. Matching only the most recent pass is not
  enough: it is biased towards 768. "Not seen" is not "absent": for an effect of P1's size, the comparison nearest to
  equal loss (768 at epoch 2.25, about 250 sequences per draw) has power 0.14, and those at 2.5 and 2.75, where 512 is
  behind in loss on the matched sets, 0.72 and 0.88. Within 768 at 1e-4, p\* on exposure-matched sets barely changes
  from epoch 2.5 or 2.75 to epoch 3 (+0.0006 [−0.0043, +0.0055] and +0.0002 [−0.0028, +0.0032]), while whole-set p\*
  rises by +0.0085 and +0.0042: over those readouts, the rise of whole-set p\* is the changing mix of exposure (post
  hoc; follow-up audit, AA-1 and AA-7).
- **At 3e-4 the lead of 512 is seen on exposure-matched sequences:** +0.0126 [−0.0099, +0.0351], +0.0126
  [+0.0049, +0.0204] and +0.0129 [+0.0072, +0.0187], close to S5.
- **With each width at its better rate of the two, there is no reversal.** At epoch 3, 512 has the lower validation
  loss at 3e-4 and 768 at 1e-4; at 1e-4, 512's training loss is 0.134 nats behind its own 3e-4 arm, and 768's differs
  by 0.005. 512 at 3e-4 against 768 at 1e-4 gives +0.01184 [+0.00789, +0.01578], 6/6, at equal updates and +0.01235
  [+0.00523, +0.01947], 5/6, at equal training loss; the second interval includes 0 at the later bracket end
  (+0.00518 [−0.00714, +0.01751]). N6's sealed secondary D3 gave the same order at equal updates (+0.0111
  [+0.0072, +0.0150]). The two arms differ in rate and in train–validation gap, so this is not a comparison of
  widths alone.
- **The larger rise of p\* after an epoch boundary** goes with the sequences not trained in that quarter. Their p\*
  falls by 0.011–0.024 per quarter inside an epoch but changes by only −0.007 to +0.002 in the first quarter after a
  boundary, while the quarter being trained gains 0.053–0.082 in every interval. The follow-up audit (AA-5; not
  re-checked by a second model) finds the step model-wide: compared at the same number of passes and time since
  training, sequences trained or not have a steeper gain–weight slope in the first quarter after a boundary than in
  other quarters, and the make-up of the untrained set does not explain it. The cause is not identified.
- **Validation loss** rises from epoch 3 to epoch 3.25 in every arm and draw (24 of 24; +0.022 to +0.046 nats by
  arm). Readings after epoch 3, which include S4's m06, lie past each arm's lowest validation readout. The registered
  check, which compares epochs 2 and 3, is unaffected.

*Narrowed:* P1 is confirmed as registered, as a statement about whole-set p\* at equal overall training loss. It is
not evidence that the narrower width has the higher p\* at equal training progress, because the models compared
differ in exposure and the lead is not seen where exposure is matched. The same applies to S1. *Not determined:*
whether 512 would lead at 1e-4 with training loss and exposure both matched. The matched sets differ in training loss
by 0.04–0.11 nats, and with 768 at epoch 2.25, the pair nearest to equal overall loss, the interval also contains
P1's value.

*Withdrawn:* "The 384→512 rise is mostly training progress" (`RESPONSE.md` §5, claim 4). Whether that rise is mostly
training progress is unresolved. *Qualified:* N6's matched figures interpolate across a whole epoch and are biased.
Where the wider model is the one interpolated, as in the figures that motivated N7, they are biased upward: on N7's
draws the same rule overstates P1 by about 0.006. Where 512 is the one interpolated (D1, and D2 and D3 matched on the
gap) they are biased downward, by less (see the
[12 November correction](reports/natural-text-correction-20261112-01/CORRECTION.md)).

**C5. Cross-width comparisons of p\* should state their alignment, including training exposure.** At epoch 3 and
1e-4, the contrasts at equal updates and at equal overall training loss have opposite signs for one pair of widths
(C4). *Status:* those two contrasts are confirmed. That the order of the widths reverses once training progress is
matched is not established: the equal-loss comparison leaves exposure unequal, and with each width at its better rate
of the two there is no reversal (post hoc; see C4). The recommendation is a judgement, and its novelty is conceded:
state how sizes are aligned, report more than one alignment, and, for readouts inside an epoch, state how many passes
the compared sequences have had and how recently. The earlier advice to "tune per width" is not tested and is not
part of the claim.

## Registered outcomes that did not confirm, or went the other way

The claims above rest on the registered outcomes that confirmed. These did not, and each is reported in its study's
own result. All figures reproduce from the published tables (follow-up audit, EA-3).

| Study | Registered outcome | Result | Bears on |
|---|---|---|---|
| N1, WikiText-2, widths 64–384, per-width rates | Primary A, peak shift | NO_DETECTED_SHIFT_CENSORED: all 70 peak locations at the 384 end of the ladder, slopes 0 | C1 |
| N1 | Primary B, interior peak | CONVEX: curvature +0.0611 [+0.0588, +0.0634], 10/10, so p\* dips rather than peaks inside the ladder | C1 |
| N3, WikiText-2, one rate (3e-5), 10 draws | Turn-down over 384–768, dip at one rate, tracking of memorisation | CONTINUES_RISING (+0.0220 [+0.0176, +0.0264]), NO_DIP_AT_ONE_RATE (+0.0428), TRACKS_MEMORIZATION (+0.9643); joint reading MEMORIZATION_PREDICTIONS_MET. These primaries average over epochs; C2's fall at epoch 32 was first seen as an N3 secondary | C2 |
| N4, WikiText-2, 4 fresh draws | P2, the turn-down slope at epoch 24 | INCONCLUSIVE: −0.0238 [−0.0479, +0.0003], predicted TURNS_DOWN. C2 is confirmed at epoch 32 only | C2 |
| N5, WikiText-103, 3 epochs, 10 draws | FALL, the slope of p\* on width over 384–768 at epoch 3 | CONTINUES_RISING: +0.0040 [+0.0010, +0.0069]. Not repeated on N6's draws (+0.0014 [−0.0013, +0.0041], 4/6) | C2 |
| N5 | Secondary: the peak location across readouts | MOVES_LARGER: +0.0237 doublings of width per doubling of readout [+0.0117, +0.0357], 10/10, opposite to C1's direction over these three epochs | C1 |
| N5 | M, matched gap | Sealed label CAPACITY_BEYOND_MEMORIZATION, read more narrowly in C3 | C3 |

## Open questions, and what would settle them

This record is closed: no further runs will be added to it. That is not a restriction on anyone else. Model states were
deleted, so each item that needs readouts needs a new study.

| Question | What would settle it | What would not |
|---|---|---|
| S4's dependence on interpolation | Readouts of 768 at 3e-4 inside epochs 3.0–3.25, where m06 is read (3.083). The other five draws are read at epochs 2.73–2.95 and stay positive at the later bracket end | Readouts inside epochs 2.0–2.25, which S4 does not use |
| Whether p\* stays between the readouts that bracket P1's readings | Readouts of 768 at 1e-4 inside epochs 2.0–2.5: three draws are bracketed by 2–2.25 and three by 2.25–2.5 | Readouts inside 2.0–2.25 alone |
| Whether 512 leads at 1e-4 when training loss and exposure are both matched | A design that matches both: for example a match at an epoch end, or draws large enough that sequences matched on every pass are numerous at the equal-loss point (about 250 per draw here) | Finer readouts. Equal overall training loss inside an epoch leaves exposure unequal however finely p\* is read |
| Whether 768's lead at equal updates at 1e-4 is an effect of width or of 512 training below its better rate | A registered comparison with the rate selected per width, on a grid of more than two rates | N7's cross-rate figures, which are post hoc and compare two rates only |
| S3's fragility when one draw is left out | More draws | — |
| S2, equal validation loss at 1e-4 | Unavailable in N7: three draws had a reading | — |
| Why p\* depends on recency, and why the gain–weight slope steps up in the first quarter after a boundary | Not addressed by any analysis here | — |
| How much batch-relative weighting under clipping shapes p\* | A registered comparison of clipping thresholds or batch sizes | Further analysis of N7, where every arm shares the recipe |

## What has been verified, and what has not

| Level | Status |
|---|---|
| Statistics from the published per-readout tables | Public. Every reported N7 statistic reproduces from `POINTS.csv`; see the example in [`README.md`](README.md#reproducing-the-results) |
| p\* from the per-sequence losses | Public for N7. The loss arrays are attached to the [v1.2 release](https://github.com/rafli-hl/sequence-weighting/releases/tag/v1.2), and `tools/verify_n7_losses.py` refits all 240 estimates with its own implementation (largest difference from `POINTS.csv` 2.9e-9) and recomputes the confirmed contrasts. An earlier AI audit (OpenAI Codex) reached the same result with separately written code |
| Post-hoc exposure analysis of 11 November | Public for N7. `posthoc_exposure.py` in [`natural-text-matched-assistant-posthoc-20261111-01`](reports/natural-text-matched-assistant-posthoc-20261111-01/) reproduces every figure from the same bundle and `POINTS.csv`. It needs PyTorch to regenerate the batch orders, which it checks against the losses. A second model (Claude Opus 5.5, the session supervising the check) recomputed the main figures with separate code, which is not published |
| Follow-up audit of 12 November | Public. Two fresh AI auditors (Claude Fable 5.2) audited the earlier studies and alternative explanations; their reports are in [`follow-up-audit-20261112-01`](reports/follow-up-audit-20261112-01/). The supervising session (Claude Opus 5.5) re-checked the main findings with separate code, `verify_findings.py`, which is published with its output; AA-5 was not re-checked |
| Training | Not reproducible from public files: model states, run folders and dataset rows are not published |

All reviews, audits and post-hoc analyses in this record were carried out by AI systems, not by independent human
reviewers. The independent review of 10 November, by a separate AI session (Claude Opus 5.5) that had no part in the
earlier work, is not part of the record; its points were used only where they could be checked against the published
files. See
[`AUDIT.md`](reports/full-audit-20261108-01/AUDIT.md) and [`README.md`](README.md#main-limitations).
