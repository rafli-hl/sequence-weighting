# Correction to the record, 11 November 2026

**Status:** drafted on 11 Nov 2026 by an AI assistant (Claude Fable 5.2, Anthropic) at the owner's request, and
issued when the owner merged it into the public record. It follows a post-hoc analysis of N7's per-sequence losses (`REPORT.md` in
[`natural-text-matched-assistant-posthoc-20261111-01`](../natural-text-matched-assistant-posthoc-20261111-01/)) and an
independent review of the record on 10 Nov 2026 by a separate AI session (Claude Opus 5.5) that had no part in the
earlier work. The review is not part of this record; each of its points used here was checked against the published
files.
**Scope:** this note corrects statements in the record and says how some confirmed results should be read. It does not
edit any historical file, change any sealed label, or report any new run. Every new figure below is post hoc and
descriptive, and comes from the report above, where its script and exact output are filed.

**Files it qualifies.** Hashes are of the published files:

- `reports/natural-text-matched-result-20261105-01/RESULT.md`
  (`8e64cc2ca39e0602cb30e7beb86815372202f54ac249799e5b678e1b2de62f45`), sealed reading 4 and section 9.
- `reports/natural-text-matched-result-20261105-01/ASSISTANT_CHECK.md`
  (`daf5b5bfcd1831ff46fbfad11ba439dad340ca92b9f5d42ef7621ee2f42e4642`).
- `reports/adversarial-review-response-note-20261106-01/CLAIMS_4_AND_5_STATUS.md`
  (`99071bcc2fe0cb2e3766fce61255bff9ad47d0d4d928c552559f1a74e6035693`).
- `reports/full-audit-20261108-01/AUDIT.md` (`3829b25edcb078c2131255cd84ce865bd74cef8d8df409e963bbb5e11468506c`),
  finding M3, and `alternatives/FINDINGS.md`
  (`e78c5fd70201e8939f1f579f16d308c2fbc8ad1f808fe73a1380706a451a0705`), finding AL-3.
- `reports/adversarial-review-response-20261104-01/RESPONSE.md`
  (`d265bbffca504e7fad7cfba4864c2c338511bca0af7cfdaff5c631aa88600523`), claim 5 of section 5.
- The living pages `README.md`, `CURRENT_CLAIMS.md` and `NATURAL_TEXT_STUDIES.md` as released in v1.0. These pages
  are edited; section 6 lists the v1.0 wording that changed, so that no change to them is silent.

The correction of 9 November ([`CORRECTION.md`](../natural-text-correction-20261109-01/CORRECTION.md)) stands and is
not changed by this note.

## Summary

1. The statement that readouts inside epochs 2.0–2.25 would settle S4's dependence on interpolation is wrong. S4's
   doubtful draw is read at epoch 3.083, so the readouts that bear on it lie between epochs 3 and 3.25 at 3e-4. No
   finer readout settles the question of comparing different points within an epoch.
2. P1 stays REVERSAL_CONFIRMED as registered. Its reading as an ordering of the two widths at equal training progress
   is not supported: the models compared differ in training exposure, p\* depends on exposure, and on sequences
   matched for exposure no lead of 512 is seen at 1e-4.
3. The audit's statement that other anchorings answer the exposure concern is withdrawn. Every one of those
   anchorings compares whole sets with unequal exposure.
4. S3 holds at epoch 3. "768 is above 512 at equal updates at 1e-4" is not true of the first epoch.
5. "Comparing widths at equal updates or at equal training loss can reverse the p\* ordering" is narrowed. With each
   width at its better rate of the two tested there is no reversal.
6. Three statements in the v1.0 living pages were inaccurate and are corrected there.

## 1. Which readouts would settle S4

**The statements.**

- `NATURAL_TEXT_STUDIES.md` (v1.0), under "Status", after listing S3's fragility, S4's dependence on interpolation
  and the different points within an epoch at which the matched readings fall: "Readouts inside epochs 2.0–2.25 would
  settle the last two."
- `ASSISTANT_CHECK.md`: "only if p\* stays between the two readouts around it, and nothing inside E2.0–E2.25 can show
  that yet", and "with readouts inside E2.0–E2.25 as future work".
- `CLAIMS_4_AND_5_STATUS.md`: "with readouts inside E2.0–E2.25 as future work", and the same condition on the bound.
- `alternatives/FINDINGS.md`: "New runs needed: readouts inside E2.0–E2.25, and a match at an epoch end."

**What is wrong.** The first statement is wrong on both counts. The others concern P1 and are incomplete.

- *S4.* S4 is at 3e-4, and its six readings take 768 at epochs 2.801, 2.951, 2.846, 2.732, 2.834 and 3.083
  (`RESULT.md` section 3). With 768 read at the later end of each bracket, five draws stay positive (+0.0127 to
  +0.0169) and m06 becomes −0.01000; m06 alone makes the later-end interval include 0. m06's bracket is epochs 3 to
  3.25. Readouts of 768 at 3e-4 inside epochs 3.0–3.25 are therefore the ones that would settle S4. Readouts inside
  2.0–2.25 tell nothing about it. The correction of 9 November already named m06's bracket correctly; the index page
  did not follow it.
- *P1.* Three of P1's readings are bracketed by epochs 2 and 2.25 (m01, m04, m05) and three by epochs 2.25 and 2.5
  (m02, m03, m06). The draw that turns negative at the later end, m06 (−0.00057), is in the second group. Whether
  p\* stays between the bracketing readouts would need readouts of 768 at 1e-4 inside epochs 2.0–2.5, not only
  2.0–2.25. P1's later-end interval stays above 0, as reported.
- *Points within an epoch.* Finer readouts do not address this at all. It is a property of the comparison, not of
  the interpolation: see section 2.

A further fact bears on any reading after epoch 3. Mean validation loss rises from epoch 3 to epoch 3.25 in every arm
and draw (24 of 24; +0.022 to +0.046 nats by arm), as the audit noted. m06's S4 reading sets 512 at its lowest
validation readout against 768 just past its own. The registered check NOT_OVERFIT compares epochs 2 and 3 and is
unaffected.

**What changes.** Read "E2.0–E2.25" in the four files as: epochs 2.0–2.5 at 1e-4 for P1's interpolation, and epochs
3.0–3.25 at 3e-4 for S4's. Neither would settle the exposure question. `NATURAL_TEXT_STUDIES.md` and
`CURRENT_CLAIMS.md` now say this. The owner's decision of 6 November not to pursue further runs is unchanged, and no
run is authorised.

## 2. How P1 should be read

**The statements.**

- `RESULT.md`, sealed reading 4: "At fixed updates at E3 on these draws, 768 is above 512, so on these draws the
  comparison axis reverses the 512-768 ordering at 1e-4."
- `CLAIMS_4_AND_5_STATUS.md`: "The matched-progress reversal at 1e-4 is now a pre-registered, confirmed result", and,
  on the epoch boundary, "no cause is claimed".
- `README.md` (v1.0): "When the wider model is read at the training loss the narrower one reaches at epoch 3, the
  narrower model has the higher p\*."

**What stands.** All of it, as a statement of what was registered and measured. P1 compares p\* fitted on the whole
training set, with 768 read where its overall training loss equals 512's at epoch 3. It is +0.00909
[+0.00400, +0.01417], 6/6, it reproduces from the per-sequence losses, and its label is unchanged.

**What the post-hoc analysis adds** (`REPORT.md`, sections 1 to 3):

- At the matched point 768 has trained on 19% to 48% of the training set a third time; 512 at epoch 3 has trained
  on all of it. The audit reported this (M3).
- p\* depends on it. Within one model, sequences already trained in the current epoch have p\* higher by 0.050 to
  0.084 than those not yet trained in it, at every readout inside an epoch from epoch 2 (20 of 20 arm-readouts, 6/6
  draws each).
- For 512 at epoch 3 against 768 at epochs 2.25, 2.5 and 2.75, on sequences matched for the timing of all three
  passes, the contrasts at 1e-4 are −0.0035 [−0.0258, +0.0189], −0.0048 [−0.0121, +0.0026] and −0.0051
  [−0.0109, +0.0008]. Each interval includes 0. On the whole sets, the same pairs of readouts give +0.0100, +0.0040
  and −0.0003, which exceed the matched contrasts by +0.0135 [−0.0076, +0.0345], +0.0088 [+0.0032, +0.0143] and
  +0.0047 [+0.0014, +0.0081].
- At 3e-4 the matched contrasts are +0.0126 [−0.0099, +0.0351], +0.0126 [+0.0049, +0.0204] and +0.0129
  [+0.0072, +0.0187].

**What changes.** P1 should be stated as: "at 1e-4, whole-set p\* at 512 at epoch 3 is above whole-set p\* at 768
read at the same overall training loss." It should not be stated as showing that the narrower model has the higher
p\* at equal training progress, or that the order of the widths reverses once progress is matched. Equal overall
training loss inside an epoch leaves the two models with unequal exposure, and the lead of 512 is not seen where
exposure is matched.

**What does not follow.** The matched contrasts do not show that 768 leads, or that the widths are equal: the
intervals include 0, the matched sets differ in training loss by +0.04 to +0.11 nats, and with 768 at epoch 2.25,
the pair nearest to equal overall loss, the interval also contains P1's own value. Whether 512 would lead at 1e-4
with loss and exposure both matched is not determined by N7's data.

The same reading applies to S1, which matches the train–validation gap and takes 768 at epochs 2.29 to 2.48.

**On the epoch boundary.** The descriptions in `CLAIMS_4_AND_5_STATUS.md` and in section 1 of the correction of
9 November stand: whole-set p\* rises most in the first quarter after a boundary. The post-hoc analysis adds where
that comes from. The quarter being trained gains 0.053 to 0.082 in every interval, at a boundary or not. The
sequences not trained in the interval lose 0.011 to 0.024 inside an epoch, but change by only −0.007 to +0.002 in the
first quarter after a boundary. The cause is still not identified.

## 3. The audit's other anchorings do not answer the exposure concern

**The statements.**

- `alternatives/FINDINGS.md`, AL-3: "The reversal survives other anchorings: 768 anchored at E2.0, E2.25 or E2.5 with
  512 read along its path gives +0.0190, +0.0105 [+0.0057, +0.0153], +0.0176, all 6/6; a sweep of common loss levels
  4.21–4.32 gives 512 − 768 > 0 in 6/6 at every level (§4). This answers AL-2 as a full explanation." And: "AL-3
  answers them from existing data."
- `AUDIT.md`, M3: "A limitation to disclose, not a refutation: the reversal survives anchoring 768 at
  E2.0/E2.25/E2.5 and a sweep of common loss levels, 6/6 everywhere."

**What is wrong.** Each of those anchorings compares p\* on whole sets at equal overall training loss. At 1e-4,
768 reaches a given training loss about 0.6 to 0.8 of an epoch before 512 does over the range those anchorings
cover (panel means, `RESULT.md` section 6b), so each anchoring pairs models at different points within an epoch, with
unequal exposure. They repeat the comparison whose exposure
is in question; they do not control it. Their figures are not disputed, and they were not recomputed for this note.

**What changes.** "This answers AL-2 as a full explanation" and "AL-3 answers them from existing data" are withdrawn.
AL-2, the exposure concern, is not answered by AL-3; the analysis in section 2 is the one that addresses it. M3's
"a limitation to disclose, not a refutation" should be read with section 2: the registered result is not refuted,
and its reading as a reversal at matched progress is not supported.

## 4. S3 holds at epoch 3, not throughout training

**The statements.** `NATURAL_TEXT_STUDIES.md` (v1.0): "At a fixed number of updates, 768 is above 512 (S3: −0.00454
[−0.00795, −0.00114], 6/6)." `README.md` (v1.0): "At equal updates the wider model has the higher p\*."

**What is incomplete.** S3 is registered at epoch 3 and confirmed there. By readout (`RESULT.md` section 6a), the
equal-updates contrast at 1e-4 is above 0 at epochs 0.25, 0.5 and 1 (+0.0052 to +0.0055, 6/6 each), includes 0 at
epoch 2 (+0.00095 [−0.00118, +0.00309]) and at epoch 2.25 (−0.00227 [−0.00513, +0.00059]), and is below 0 from
epoch 2.5. In `NATURAL_TEXT_STUDIES.md` the count "6/6" was the number of negative draws, where the rest of the
record counts positive ones.

**What changes.** Both pages now say "at epoch 3", and give the count as 0/6 positive.

## 5. The reversal, and the learning rates

**The statements.**

- `RESPONSE.md` section 5, claim 5, as updated by `CLAIMS_4_AND_5_STATUS.md`: "Comparing widths at equal updates or
  at equal training loss can reverse the p\* ordering; cross-width p\* comparisons should report both, or tune per
  width." Status after N7: "Pre-registered and confirmed, for 512 and 768 at 1e-4, on these draws".
- `CLAIMS_4_AND_5_STATUS.md`: "The nearest case to tuning per width, D3 … Unchanged. D3 is not a step of N7."
- `CURRENT_CLAIMS.md` (v1.0), C5: "Comparing widths at equal updates or at equal training loss can reverse the p\*
  ordering, as C4 shows for one pair of widths at one rate."

**What the published tables add** (`REPORT.md` section 4; post hoc, from `POINTS.csv`):

- 1e-4 was chosen as 768's lowest validation loss of five rates on a tuning draw (N7 `PROTOCOL.md` section 3). On
  N7's draws at epoch 3, 768's validation loss is indeed lower at 1e-4 (by 0.021 nats), and 512's is lower at 3e-4
  (by 0.014). At 1e-4, 512's training loss is 0.134 nats behind its own 3e-4 arm; 768's differs by 0.005.
- With each width at its better rate of the two, 512 at 3e-4 against 768 at 1e-4, the contrast is +0.01184
  [+0.00789, +0.01578], 6/6, at equal updates at epoch 3 and +0.01235 [+0.00523, +0.01947], 5/6, at equal training
  loss under the registered interpolation rule. The second interval includes 0 with 768 read at the later end of
  each bracket (+0.00518 [−0.00714, +0.01751]).
- N6's sealed secondary D3 is the same equal-updates contrast on N6's draws: +0.0111 [+0.0072, +0.0150]. Its
  caveat, stated in advance, applies: the arms differ in rate, and in the train–validation gap.

**What changes.** The two registered contrasts at 1e-4, P1 and S3, have opposite signs; that stands. The
generalisation drawn from them is narrowed in three ways. The positive one compares models with unequal exposure
(section 2). The opposite signs appear at one of two rates, the one at which 512 trains markedly slower than at the
other. And with each width at its better rate of the two, 512 is above 768 at equal updates and at equal training
loss. "D3 is not a step of N7" remains true: the cross-rate figures here are post hoc, and "tune per width" is still
not a tested recommendation.

## 6. Wording corrected in the living pages

These pages are maintained for the publication copy and are edited in place. The v1.0 wording that this revision
replaces because it was wrong or overstated:

| Page (v1.0) | Wording | Correction |
|---|---|---|
| `NATURAL_TEXT_STUDIES.md` | "Readouts inside epochs 2.0–2.25 would settle the last two." | Wrong; section 1 |
| `NATURAL_TEXT_STUDIES.md` | "N7 shows that the comparison axis can reverse the p\* ordering of two widths at one learning rate." | Overstated; sections 2 and 5 |
| `NATURAL_TEXT_STUDIES.md` | "(S3: −0.00454 [−0.00795, −0.00114], 6/6)" | The count is 0/6 positive; section 4 |
| `README.md` | "At equal updates the wider model has the higher p\*. When the wider model is read at the training loss the narrower one reaches at epoch 3, the narrower model has the higher p\*." | Incomplete; sections 2 and 4 |
| `README.md` | "Learning rates. Rates are fixed per study, not tuned per width." | Inaccurate. N1 chose a rate per width on a tuning draw. In N5 to N7 each rate is shared by the widths compared, but the rates were selected on a tuning draw: 3e-4 by the mean over eight widths, and 1e-4 as the best of five for width 768 |
| `CURRENT_CLAIMS.md` | Scope: "with constant learning rates and no per-width tuning" | Inaccurate in the same way |
| `CURRENT_CLAIMS.md` | C4's title: "At 1e-4, the order of widths 512 and 768 depends on the comparison; at 3e-4 it does not." | Kept as the registered result, at epoch 3, with the reading of section 2 |
| `CURRENT_CLAIMS.md` | C5: "can reverse the p\* ordering, as C4 shows for one pair of widths at one rate" | Narrowed; section 5 |
| `README.md` | "Interpolation and epoch phase. … at 1e-4 the matched readings fall early in an epoch." | Replaced by the exposure limitation; section 2 |

## What is not changed

- Every sealed label, interval and reading of N7, and the fixed sequence that reached S5.
- Claims C1 to C3, and the correction of 9 November.
- S4's later-end sensitivity and S3's fragility when m03 or m05 is left out, as already reported.
- The closure of the experiments.

## How these figures were obtained

The figures of sections 2 and 5, and the readout positions and validation changes of sections 1 and 4, are printed by
[`posthoc_exposure.py`](../natural-text-matched-assistant-posthoc-20261111-01/posthoc_exposure.py), whose output is
filed as [`OUTPUT.txt`](../natural-text-matched-assistant-posthoc-20261111-01/OUTPUT.txt). It reads the v1.0
loss-array bundle and `POINTS.csv`, regenerates the batch orders from the sealed engine's rule and checks them
against the losses, and refits p\* with its own implementation. The share of the set that 768 has revisited at P1's
matched point (19% to 48%) is the fractional part of each reading's epoch in `RESULT.md` section 2. The audit's
anchoring figures in section 3 are quoted, not recomputed. The analysis was made and checked by AI models only; see
the report for who did what.
