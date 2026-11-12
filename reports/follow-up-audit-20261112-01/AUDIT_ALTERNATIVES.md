# Follow-up audit, 12 November 2026: alternative explanations

**The auditor's report, saved by the supervising session.** The auditor could not write files, so it returned this report as a message. It is reproduced as returned, except that local paths to the auditor's working folder are replaced by "(not published)" and a line about folders outside the audit's scope is removed. Line numbers refer to the record at commit `3b4610d`. The auditor's scripts are not published; the main findings are re-checked independently in [`verify_findings.py`](verify_findings.py) ([`OUTPUT.txt`](OUTPUT.txt)), and how each finding was handled is in [`REPORT.md`](REPORT.md).

---

Model: Fable 5.2 (`claude-fable-5-2`)

Everything I computed is post hoc and descriptive. Intervals are unadjusted two-sided 95% t intervals over the six draws unless I say otherwise. I ran no training and opened nothing under any `work/runs/` path.

## Verdict

No blocking problem: the living pages' wording on C4 and C5 is accurate, and every registered contrast holds its sign under every estimator and matching variant I tried. Three things are missing from the living pages and change how the claims read: the matched-sequence null has 14% power at the only readout where loss is roughly matched; gradient clipping makes the applied weight batch-relative; and p\* is close to a ratio of weight slope to mean gain, so several sign patterns come from the denominator. The epoch-boundary effect is not explained by which sequences are in the untrained set, and it is model-wide, which the current bullet does not say.

All scripts and outputs are in the auditor's working folder (not published). My baseline refit reproduces P1, S3, S4, S5 and the three every-pass matched contrasts to the printed digit.

## Findings

### MAJOR

**AA-1. The matched-sequence null at 1e-4 is a power problem where it matters, and a stronger statement is available.** (reword)
- **Tested:** power of the every-pass matched contrasts; subset sampling noise; a within-model version of the same comparison (`a5_power.py`, `a6_progress.py`).
- **Power for a true effect of P1's size (+0.00909):**

| 768 read at | SE | 80% detectable effect | Power for +0.00909 | Loss difference on matched sets |
|---|---|---|---|---|
| Epoch 2.25 | 0.0087 | 0.030 | 0.14 | +0.036 |
| Epoch 2.5 | 0.0029 | 0.010 | 0.72 | +0.076 |
| Epoch 2.75 | 0.0023 | 0.008 | 0.88 | +0.113 |

- **Source of the noise:** two random disjoint subsets of the same size in one model differ in p\* with SD 0.0155, 0.0050 and 0.0028; the observed between-draw SDs are 0.0213, 0.0070 and 0.0056. More than half of the variance at epochs 2.25 and 2.5 is subset sampling.
- **Within one model, p\* does not rise with training when exposure is held fixed.** p\*(epoch 3, late-exposure set) minus p\*(epoch 2 + k/4, early-exposure set), for 768 at 1e-4: +0.0006 [−0.0043, +0.0055] at k = 2 and +0.0002 [−0.0028, +0.0032] at k = 3. The whole-set rise over the same readouts is +0.0085 and +0.0042. All four arms agree. At k = 1 it is +0.0029 [−0.0195, +0.0252], uninformative.
- **The rate-by-width interaction survives matching intact:** matched contrast at 3e-4 minus at 1e-4 is +0.0160 [+0.0108, +0.0213], +0.0174 [+0.0145, +0.0203] and +0.0180 [+0.0149, +0.0210], all 6/6, against +0.0184 at equal updates. Subset noise cancels here because both rates use the same subsets.
- **How much it explains:** P1 minus S3 is 768's own whole-set rise from its read point to epoch 3 (+0.0136). From epoch 2.5 onward that rise is all exposure mix, within ±0.005. Between the read points (2.19–2.48) and 2.5 the data cannot say.
- **Living-page accuracy:** "is not seen" and "not determined" are accurate. "Indistinguishable" would not be. The pages give no power figure.
- **Suggested wording** for the C4 bullet: "On exposure-matched sequences at 1e-4 the lead of 512 is not seen, but the comparison nearest equal loss (768 at epoch 2.25, about 250 sequences) has 14% power for an effect of P1's size. At epochs 2.5 and 2.75 power is 72% and 88%, with 512 behind in loss by 0.08–0.11 nats. Within one model, p\* on exposure-matched sequences does not change measurably between epoch 2.5 and 3 (+0.0006 [−0.0043, +0.0055] for 768), while whole-set p\* rises by 0.0085."

**AA-2. Gradient clipping makes the applied weight relative to the batch.** (disclose)
- **Tested:** regression of each sequence's loss drop, over the quarter in which it is trained, on its own log weight and the log sum of its 15 batch-mates' weights (`a4_batch.py`).
- **Evidence:**

| Arm | Coefficient, own weight | Coefficient, batch-mates |
|---|---|---|
| 512 at 1e-4 | +0.085 | −0.099 |
| 768 at 1e-4 | +0.109 | −0.121 |
| 512 at 3e-4 | +0.135 | −0.147 |
| 768 at 3e-4 | +0.138 | −0.139 |

  The batch-mates coefficient is below 0 in 6/6 draws in every arm. For the same own weight, the loss drop is about 40% smaller in the heaviest-mates tercile (0.137 against 0.227 nats for 512 at 1e-4). Clipping is active on 93–99% of updates.
- **How much it explains:** the level of p\* (about 0.1) and its dependence on batch size 16 and clip 1.0. It does not explain the sign of any width contrast: both widths share the recipe.
- **Status in the record:** conceded on 4 November (`RESPONSE.md` §3.8) as "not quantified"; absent from `CURRENT_CLAIMS.md` and `README.md`. I rank this major because it bears on E1's reading for every text claim; it changes no sign, so minor is defensible.
- **Suggested wording** for "Scope of every claim": "Gradient clipping at norm 1 is active on 93–99% of updates, so the applied weight is relative to a sequence's batch of 16: a sequence's gain falls with its batch-mates' weights about as fast as it rises with its own (post hoc, N7). p\* here describes that recipe."

### MINOR

**AA-3. p\* is close to weight slope divided by mean gain, and the denominator drives some sign patterns.** (disclose)
- **Tested:** OLS slope of gain on log weight, and mean gain, per arm and readout; refits with a common E0 and with a uniform shift (`a1_estimator.py`, `a9_old_audit.py`).
- **At 1e-4, equal updates:** 768 has the larger absolute slope at every readout (epochs 1, 2, 3, 3.5; 0/6 each) and the larger mean gain. The p\* contrast changes sign over training only because the two ratios cross: at epoch 1 the log-slope contrast is −0.093 and log-gain −0.182; at epoch 3 they are −0.181 and −0.140.
- **At 3e-4:** 512 has the larger slope at every readout (6/6).
- **P1 and the E0 offset:** 768 starts 0.037 nats higher. Removing that uniform offset from 768's gains raises its p\* by +0.0028 [+0.0012, +0.0044], about a third of P1. With both widths' gains measured from a common per-sequence E0, P1 is +0.0061 [−0.0002, +0.0125], 5/6, and S3 is −0.0075 [−0.0118, −0.0033].
- **Suggested addition** to the S3 row: "On the absolute scale (nats per e-fold of weight) 768 is above 512 at 1e-4 at every readout; the early positive p\* contrast reflects 768's larger total gain." To the P1 row: "About 0.003 of P1 comes from 768's higher E0; with a common baseline the interval includes 0."

**AA-4. C2 and the WikiText-2 part of C1: memorisation saturation.** (disclose)
- **Tested:** p\* times total gain, as a proxy for absolute weight sensitivity, from N4's published `FITS.csv` (`a7_c2.py`). The proxy is rough at p\* of 0.3–0.5.
- **Evidence at epoch 32:** total gain rises 44% from 512 to 768 (3,315 to 4,774) while the proxy is flat (1,648 to 1,658); from 384 to 512 the proxy still rises (1,244 to 1,648). The train–validation gap at 768 is 3.9 nats.
- **How much it explains:** all of the 512→768 fall in p\*, and none of the 384→512 fall on this proxy.
- **Status:** `RESPONSE.md` §2 lists saturation as "not excluded"; `CURRENT_CLAIMS.md` does not carry it.
- **Suggested addition** to C2: "Memorisation saturation is not excluded: from 512 to 768 the total gain rises 44% while p\* × total gain is flat."

**AA-5. The epoch-boundary effect is not composition, not the denominator, and not confined to untrained sequences.** (reword)
- **Tested:** change of p\*, slope and mean gain per quarter, stratified by number of passes and quarters since the last pass (`a3_boundary.py`, `a3b_trained.py`).
- **Like-for-like, untrained sequences:** at the same passes and lag, the boundary quarter's change in p\* exceeds an inside quarter's by +0.005 to +0.020, 6/6 in every stratum and arm (512 at 1e-4: +0.0052 to +0.0121; 768 at 3e-4: +0.0084 to +0.0189). Two inside quarters compared the same way differ by at most 0.002.
- **It is in the absolute slope:** the slope difference is +0.006 to +0.026 while mean-gain differences are mixed in sign.
- **Trained sequences show it too:** at lag 1, the boundary quarter's slope gain exceeds the next quarter's by +0.007 to +0.022 (6/6 in every arm).
- **It coincides with** a stall or rise in validation loss (24 of 24 rise after epoch 3; 7 of 24 after epoch 2) and smaller training-loss progress.
- **Consequence:** matching sequences on pass timing does not match the model's phase within the epoch. Both matched sets have lived through the same number of boundary quarters, so I see no first-order bias, but I cannot quantify it further.
- **Mechanism:** not identified. The pattern is a step at the first quarter, not a gradient across quarters.
- **Suggested wording** for the bullet: "In the first quarter after an epoch boundary the weight slope of all sequences, trained or not, is higher by about 0.005–0.02 in p\* than in other quarters at the same number of passes and time since training. The make-up of the untrained set does not explain it. The cause is not identified."

**AA-6. The gain–weight relation is not a power law.** (disclose)
- **Tested:** mean gain by weight decile; p\* on weight sub-ranges (`a2_robust.py`).
- **Evidence at epoch 3:** normalised gain is flat over the lower half of weights (0.82–0.86) and rises only at the top (1.10, 1.30, 1.55). p\* is 0.015 on the bottom half and 0.20 on the top half, against 0.10 overall.
- **Effect on claims:** S3, S5 and S4 keep their sign and exclude 0 on every sub-range (S3 5/6 on two of them). P1 is positive on every sub-range, but on the bottom half its interval includes 0 (+0.0012 [−0.0009, +0.0032]), as does S4's there (+0.0020 [−0.0006, +0.0046]). The level of p\* depends on the weight range.

**AA-7. Multiplicity in the post-hoc matched comparisons.** (disclose)
- With Bonferroni over the six every-pass comparisons (t = 4.22 on df 5), "whole set minus every pass" at 1e-4 becomes +0.0088 [−0.0003, +0.0178] and +0.0047 [−0.0008, +0.0102]; both include 0. The 3e-4 matched lead at epoch 2.75 survives (+0.0129 [+0.0035, +0.0223]); at 2.5 it does not ([−0.0001, +0.0254]).
- The seen-versus-unseen difference (+0.05 to +0.08) survives any adjustment.
- The page says intervals are unadjusted; it should not quote those two differences as excluding 0 without that note beside them.

### NOTE

**AA-8. Per-draw variation tracks position and optimiser state.** P1 per draw correlates −0.86 with the epoch at which 768 is read (leave-one-out −0.63 to −0.99), as an exposure account predicts. S3 per draw correlates +0.95 with the 512-minus-768 difference in mean gradient norm at epoch 3 (+0.85 at 3e-4). Six points each, four correlations looked at (`a8_dose.py`, `a4_batch.py`).

**AA-9. Removing generic gain.** Subtracting each model's mean validation gain from its training gains triples p\* (about 0.30). S3 becomes −0.0074 [−0.0155, +0.0007], 1/6; P1 +0.0160 [+0.0046, +0.0274], 5/6; S5 and S4 stay above 0 (`a1_estimator.py`).

**AA-10. The record changed during the audit.** `NATURAL_TEXT_STUDIES.md` was edited on disk while I worked and now cites a "12 November correction" that is not in `reports/`. My reading of that page is of the earlier state plus the diff I saw (N2 description, N1 failure cause, interpolation-bias direction).

## Ruled out

- **Tie order:** reversing ties moves any of the 240 fits by at most 1.7e-8.
- **A few sequences or extreme weights:** dropping the top 1% or 5% of weights, the bottom 25%, or the 1% tails of E0 leaves S3 and S5 with the same sign and intervals excluding 0, and P1 and S4 positive with intervals excluding 0 on all of these. The bottom-half range is the exception, noted in AA-6 (P1 +0.0090, +0.0083, +0.0123, +0.0091 across the four trims).
- **Sequence sampling within a draw:** bootstrap SE of the per-draw contrast is 0.0004 (equal updates) and 0.0008 (equal loss), against between-draw SDs of 0.003 and 0.005.
- **Search range and non-positive gain:** no N7 fit is near a bound; the smallest total gain is 6,027.
- **Noise in the training-loss evaluation:** the model has no dropout, and the loss is evaluated on all 16,384 sequences.
- **Choice of whole-set matching axis at 1e-4:** every axis is positive.

| Axis | Contrast |
|---|---|
| Mean gain | +0.0158 [+0.0104, +0.0213], 6/6 |
| Weighted training loss (the objective) | +0.0072 [+0.0039, +0.0105], 6/6 |
| Weighted gain | +0.0096 [+0.0066, +0.0126], 6/6 |
| Median training loss | +0.0084 [+0.0025, +0.0143], 5/6 |
| Gap change from E0 | +0.0078 [+0.0046, +0.0110], 6/6 |

  None of these equalises exposure.
- **Interpolation inside an epoch:** predicting a mid readout from neighbours half an epoch apart errs by +0.0005 to +0.0012 in p\* inside epoch 3, so about a quarter of that at quarter spacing. Across a boundary the error is +0.003 to +0.009, which the later-bracket-end figures already bound (my P1 later end: +0.00702 [+0.00216, +0.01189], 5/6).
- **Boundary effect as lag composition or dilution by generic gain:** see AA-5.
- **Shared data order across widths:** the paired t interval over draws is valid for it; only the matched-set comparisons lose the pairing, which the report states.

## Comparison with the 8 November audit

I read `alternatives/FINDINGS.md` only after fixing my own list (`OWN_FINDINGS_BEFORE_READING_8NOV_AUDIT.txt` in the scratch folder).

| Finding | My result |
|---|---|
| AL-1, within-epoch non-linearity | Confirm. Later-end P1 reproduces exactly. Already on the living pages. AA-5 adds that the first-quarter step is model-wide. |
| AL-2, exposure phase | Confirm. Now central to C4. My correlation of P1 with read epoch is −0.86. |
| AL-3, other anchorings answer AL-2 | Numbers confirm (+0.0190, +0.0105 [+0.0057, +0.0153], +0.0176). Inference refuted: in every anchoring 512 has had 43 to over 100 points more third-pass exposure than 768. Already withdrawn on 11 November. |
| AL-4, equal loss is not equal gain | Confirm the figure (+0.01584 [+0.01041, +0.02126]). I did not check the −0.67 correlation. AA-3 qualifies the "rebut": with a common E0, P1's interval includes 0. |
| AL-5, a uniform 0.037 nats moves p\* by about 0.0027 | Magnitude confirmed (+0.0028). Direction refuted: the offset lowers 768's p\* at equal loss, so it adds to P1, not against it. |
| AL-6, rate effect at 512 is "almost all progress" | Not recomputed. Its prediction uses the within-epoch whole-set slope, which AA-1 shows is exposure mix from epoch 2.5, so "progress" there is not established. |
| AL-7, skew and bootstrap | Not recomputed. |
| AL-8, S2-unavailable draws | Confirm (+0.0120 against +0.0061). |
| AL-9, validation non-monotone | Confirm: rises from epoch 3 to 3.25 in 24 of 24. |

The 8 November audit did not cover AA-1 to AA-7.

## Not checked

- **C1 synthetic and C3:** no per-sequence data are published; the bound fits and the 96–99% fixture rate are already conceded on the living page.
- **The estimator on N1, N3, N5 and N6:** only N7's arrays are released. AA-2 and AA-6 are shown on N7 only.
- **Per-width rate selection:** the tuning draw's data are not in the bundle. On N7 itself "better rate of the two" holds at epoch 3, as the record states.
- **Optimiser state at equal loss** (768 has taken fewer AdamW steps) and the **shared pool, tokenizer and validation set:** not testable without new runs; both are disclosed.
- **Within-quarter exposure:** the losses resolve exposure only to the quarter. Position within the quarter matters (later-trained sequences drop 0.07–0.20 nats more) but is balanced in distribution between the matched sets.
- **Mechanism of the boundary effect and of recency:** characterised, not identified.
- **AL-6 and AL-7** of the earlier audit, as above.