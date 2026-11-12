# Follow-up audit, 12 November 2026: the studies before N7

**The auditor's report, saved by the supervising session.** The auditor could not write files, so it returned this report as a message. It is reproduced as returned, except that local paths to the auditor's working folder are replaced by "(not published)" and a line about folders outside the audit's scope is removed. Line numbers refer to the record at commit `3b4610d`. The auditor's scripts are not published; the main findings are re-checked independently in [`verify_findings.py`](verify_findings.py) ([`OUTPUT.txt`](OUTPUT.txt)), and how each finding was handled is in [`REPORT.md`](REPORT.md).

---

Fable 5.2 (claude-fable-5-2)

## Verdict

Every number behind C1, C2 and C3 reproduces from the published tables, registered outcomes were read as registered, and the hash links I could test hold; nothing is blocking. The problems are in the living pages' wording. C3 lacks the interpolation and exposure caveats the record applies to the same kind of matched reading in N7. C1 drops qualifiers that the governing RESPONSE §5 wording required. `CURRENT_CLAIMS.md` lists only the confirmations and omits the registered nulls and opposite-direction outcomes of N1, N3, N4-P2 and N5. The corrections' blanket "biased upward" for N6's matched figures has the wrong sign for 5 of the 12 cells.

Scripts are in the auditor's working folder (not published). My findings list was written to `MY_FINDINGS_BEFORE_READING_AUDIT.txt` in that folder before I opened the 8 November audit folder.

## Findings

No BLOCKING findings.

### MAJOR

**EA-1. C3 lacks the interpolation and exposure caveats applied elsewhere (`CURRENT_CLAIMS.md:60-62`; the 11 Nov correction's "What is not changed: Claims C1 to C3").**
- M reproduces: −0.0066 [−0.0076, −0.0055], 0/10 positive, t-test p = 1.76e−7 (`n5_check.py`).
- M reads each width by linear interpolation of p\* against the gap between readouts at E0.25, 0.5, 1, 2 and 3. 768 is read in the E1–E2 or E2–E3 bracket at 595 of 1,010 draw-levels, and 384 at 762.
- This is the rule the 9 Nov correction found biased by 0.003–0.006 on N7, which is the size of M itself.
- Bracket-end sensitivity, the one the record bolds for S4:

  | Reading | M |
  |---|---|
  | Registered (linear) | −0.0066 [−0.0076, −0.0055] |
  | 768 at the higher p\* of its bracket, 384 linear | +0.0015 [+0.0003, +0.0027], 8/10 positive |
  | 384 at the lower end, 768 linear | +0.0008 [−0.0002, +0.0018] |
  | Both least favourable | +0.0089 [+0.0077, +0.0100] |

  The brackets are wide, so this is a crude bound, but the sign is not protected.
- Exposure: 768 is read 0.2–0.6 epoch earlier than 384 at every level (for example E2.18 against E2.73). The 11 Nov correction says "the same reading applies to S1" (matched gap, N7) and does not extend it to M.
- The analysis RESPONSE §2 lists as "Not done" (`m_epochonly.py`): an epoch-only curve built from each draw's own 384 path predicts M = −0.0067 [−0.0073, −0.0062]. Observed minus predicted is +0.0002 [−0.0009, +0.0012]. M is entirely what the epoch confound predicts.
- The headline survives without interpolation, post hoc. At E2 at 3e-4, 512 and 768 have the same gap (768 − 512: +0.0004 [−0.0047, +0.0055]) and p\*(768) − p\*(512) = −0.0092 [−0.0112, −0.0072], 0/10. N6 shows the same pattern (gaps 0.4219 and 0.4226; D2 at E2 +0.0104).
- The matched-gap sign is pair-dependent: M(256,384) +0.0056, M(384,512) +0.0020, M(512,768) −0.0089, M(256,768) −0.0005 [−0.0012, +0.0002].
- Limited reassurance: an M-type statistic for 512 against 768 on N7 is unchanged by finer readouts (−0.00940 coarse, −0.00938 fine; `m_interp.py`). N7 has no 384, so the registered pair cannot be checked this way.
- Action: disclose and reword. Suggested: "**C3. The train–validation gap alone does not determine p\*.** Registered (N5): at matched gap, p\* at 768 is below p\* at 384 (M, −0.0066 [−0.0076, −0.0055], 10/10), read by linear interpolation between readouts up to a whole epoch apart. The sign is not robust to where in its bracket 768 is read (+0.0015 [+0.0003, +0.0027] at the higher end, post hoc), and the two widths are read at different epochs, so the exposure caveat of C4 applies. An epoch-only curve with no width effect gives the same label in 96–99% of fixture replicates and, fitted to these draws, predicts M = −0.0067; M shows nothing beyond the difference in epochs. Without interpolation (post hoc): at epoch 2, widths 512 and 768 have equal gap and p\* differs by −0.0092 [−0.0112, −0.0072], 0/10."

**EA-2. C1 is worded more strongly than RESPONSE §5 claim 1, which it says it summarises (`CURRENT_CLAIMS.md:51-54`).**
- Both numbers reproduce: S slope −0.796 [−0.982, −0.609], 12/12 negative; N4 P3 +0.9090 [+0.8641, +0.9539], 4/4 (`s_check.py`, `n4_check.py`).
- Dropped qualifiers:
  - P3 "is implied by P1, is not a separate confirmation, and is a bound because E8 is censored at the top rung". The E8 location is the ladder top (768) in 4/4 draws, so no E8 peak is located.
  - S's direction and window were first seen on the exposed ladder.
  - The WikiText-2 leg is given only as "4/4", whose exact two-sided sign test is p = 0.125. The t interval and units are omitted.
- The movement is not monotone. In N4 the highest-p\* width is 512 at E1–E2, 768 at E8–E12, 512 at E24 and 384 at E32.
- Opposite or null registered outcomes are not mentioned: N5's sealed secondary MOVES_LARGER (+0.0237 [+0.0117, +0.0357], 10/10) and N1's Primary A NO_DETECTED_SHIFT_CENSORED.
- Action: reword. Suggested: "On the synthetic task the width of peak p\* moves smaller from epoch 15 to 40 (−0.796 log2-width per doubling of epochs [−0.982, −0.609], 12/12 corpora; in 19 of 59 defined corpus-epoch points the largest fit is at the estimator's bound; direction and window first seen on an exposed ladder). On WikiText-2 at 3e-5 over widths 256–768, the highest-p\* width is the ladder top, 768, at epoch 8 and 384 at epoch 32 in 4/4 draws (shift ≥ +0.909 doublings [+0.864, +0.954]); this follows from C2, is not a separate confirmation, and is a bound. The movement is not monotone (512 at epochs 1–2), was not detected in N1 (widths 64–384, per-width rates), and runs the other way over 3 epochs on WikiText-103 (+0.0237 [+0.0117, +0.0357], secondary)."

**EA-3. `CURRENT_CLAIMS.md` omits registered outcomes that failed or went the other way (whole page; C1–C2 at `:51-58`).** The page "states what the project currently claims, in one place". All of the following reproduce (`n1n3.py`, `n4_check.py`, `n5_check.py`, `n6n7.py`) and are reported in their own study reports, but appear on no living page:
- N1 Primary A NO_DETECTED_SHIFT_CENSORED (all 70 locations at the 384 boundary, slopes 0) and Primary B CONVEX (curvature +0.0611 [+0.0588, +0.0634]). Sealed joint reading: "Neither finding is reproduced at this scale under this recipe."
- N3's three primaries: turn-down CONTINUES_RISING +0.0220 [+0.0176, +0.0264], NO_DIP +0.0428, TRACKS_MEMORIZATION +0.9643; joint MEMORIZATION_PREDICTIONS_MET. C2's E32 fall was first seen as an N3 secondary.
- N4 P2 (E24) INCONCLUSIVE, −0.0238 [−0.0479, +0.0003], predicted TURNS_DOWN. C2's fall is therefore confirmed at one readout only, and at E4–E16 the same slope is positive in 4/4.
- N5 FALL CONTINUES_RISING +0.0040 [+0.0010, +0.0069], not repeated on N6 (+0.0014 [−0.0013, +0.0041], 4/6).
- Action: disclose. Add a short "Registered outcomes that did not confirm, or went the other way" table to `CURRENT_CLAIMS.md` with these four rows, and change C2's heading to "At epoch 32 of WikiText-2 training, p\* falls with width over 384–768".

### MINOR

**EA-4. "19 of 59 defined fits at the estimator's bound" (`CURRENT_CLAIMS.md:52-53`).** The 59 are corpus-epoch points, each with 8 fits. 19 points have their largest fit at the bound, and 10 have two or more widths tied there. 33 of 472 fits are at the bound (`s_check.py`). Reword to "in 19 of 59 defined corpus-epoch points the largest fit is at the estimator's bound (33 of 472 fits)".

**EA-5. "N6's matched figures are biased upward" has the wrong sign for 5 of 12 cells.**
- Locations: 9 Nov `CORRECTION.md:20` and `:47`; `CURRENT_CLAIMS.md:122-123`; `NATURAL_TEXT_STUDIES.md:97-98`; `README.md:66`.
- The N6 rule reads whichever arm's E3 value lies on the other's path (`recompute_matched.py`). 768 or 384 is the interpolated arm in D2 train and validation, D4 (all three), and D3 train and validation; there the contrast is overstated. 512, the minuend, is the interpolated arm in D1 (all three), D2 gap and D3 gap; there under-reading 512 understates the contrast.
- Checked on N7 with the coarse rule against quarter-epoch readouts (`bias_dir.py`): D3-gap type −0.0015 [−0.0023, −0.0008], 0/6; D2-gap type −0.0006 (5 draws, includes 0).
- The correction's own §2 implies the downward direction for D1 (+0.0027 against an estimate near +0.011).
- Nothing substantive flips: "512 above 768 at 3e-4 matched on the gap" is strengthened, and D1's sentence is already withdrawn.
- Also undisclosed: the arm read varies within one contrast (D3 train: five draws read 768, c06 reads 512).
- Action: reword. Suggested for `CURRENT_CLAIMS.md`: "N6's matched figures interpolate across a whole epoch and are biased: upward where the wider model is the interpolated arm (D4, the figures that motivated N7), downward where 512 is (D1, and D2 and D3 matched on the gap)."

**EA-6. S4 "overstatement +0.0041" compares different draws (9 Nov `CORRECTION.md:40`).** +0.01806 is a five-draw mean under N6's rule; +0.01394 is the six-draw sealed mean. On the same five draws the fine rule gives +0.01574, so the overstatement is +0.0023 [+0.0008, +0.0039] (`bias_dir.py`). P1's +0.0059 and S1's +0.0032 are like for like and reproduce. Action: add the like-for-like figure in a future note.

**EA-7. "There is no N2" (`NATURAL_TEXT_STUDIES.md:39`).** Both evidence chains define N2 as the 768 memory probe of 30 October, "engineering only, no scientific primary". Reword: "N2 is a memory probe with no scientific outcome (see the evidence chains); its records are not published."

**EA-8. "A game was using the GPU" (`NATURAL_TEXT_STUDIES.md:60`).** The failure report says "The timing coincides, but the records cannot prove the cause." Reword: "The run hit its per-draw time cap; a game started on the GPU during the run, and the cause is not proven."

**EA-9. Units missing in C1 and C2 (`CURRENT_CLAIMS.md:52`, `:57`).** −0.796 is log2-width per doubling of epochs. −0.1886 is p\* per doubling of width (OLS over 384, 512, 768). Add the units.

### NOTE

**EA-10. C2 does not state its alignment, though C5 asks for it; it holds under two others (post hoc, `n4_matched.py`).**
- At E32 training NLL is 4.10, 3.48 and 2.54 at 384, 512 and 768.
- With 768 read at 384's E32 gap (about E16–E18): +0.0859 [+0.0621, +0.1096], 4/4, and +0.0802 [+0.0645, +0.0958] at the least favourable bracket end.
- Comparing each width's maximum over all readouts: 384 − 768 = +0.0802, 384 − 512 = +0.0205 [+0.0032, +0.0379], 512 − 768 = +0.0596, all 4/4. 384's maximum is at the last readout, so the first two are lower bounds.
- Optional: add "equal epochs; the order also holds at matched gap and for each width's maximum over readouts (post hoc)".

**EA-11. The "96–99%" fixture rate cannot be recomputed from the public copy.** It is quoted from N5 `PROTOCOL.md` §9; the planning record `FEWEPOCH_PLANNING_r2.json` is not published. The fixture uses assumed gap trajectories, as the protocol says. EA-1's measured-curve prediction is the reproducible counterpart.

**EA-12. Consistency of N6 and N7 at equal updates, by Welch test (`n6n7.py`).**

| Contrast | N6 | N7 | Welch p | Pooled, 12 draws |
|---|---|---|---|---|
| D4 / S3 | −0.0050 | −0.0045 | 0.82 | −0.0048 [−0.0069, −0.0026], 0/12 positive |
| D2 / S5 | +0.0158 | +0.0138 | 0.21 | — |
| D3 / cross-rate | +0.0111 | +0.0118 | 0.74 | — |

With N6's rule on both studies, matched training NLL gives +0.0132 and +0.0150 (p = 0.42). The pooled D4/S3 figure is not registered, but it bears on the leave-one-out fragility listed as an open limitation.

## Held

- **S:** primary −0.796 [−0.982, −0.609], sd 0.293, 12/12 negative. S32 −0.817 [−0.990, −0.644]. SD −0.794 [−0.966, −0.622] on 8 corpora. S_batch −0.851 [−0.934, −0.768]. 59 of 60 points defined, 19 flagged. An argmax-rung slope without the parabola gives −0.715 [−0.913, −0.518], 12/12.
- **N1:** 70 of 70 locations at the boundary; A slopes 0; curvature +0.0611.
- **N3:** three primaries and all nine by-epoch turn slopes reproduce.
- **N4:** P1 −0.1886 [−0.2083, −0.1688]; P3 +0.9090 [+0.8641, +0.9539]; P2 −0.0238 [−0.0479, +0.0003]; all nine by-epoch slopes match the stored `turn` column to 1e-15. P1 → P3 → P2 was read as registered. E32 p\* is monotone 384 > 512 > 768 in every draw.
- **N5:** M, FALL (p = 0.0133) and RISE +0.0275 [+0.0269, +0.0280] reproduce. The Holm labels are right. M's interval stays below 0 under every leave-one-out.
- **N6:**
  - D1 +0.0192 [+0.0179, +0.0204]; D2 +0.0158 [+0.0131, +0.0185]; D4 −0.0050 [−0.0090, −0.0010] (p = 0.0232); D3 +0.0111 [+0.0072, +0.0150].
  - D4 leave-one-out spans 0 without c02 or c05.
  - FALL +0.0014 [−0.0013, +0.0041], 4/6; M −0.0078 [−0.0102, −0.0053]; rate effects and by-readout table reproduce.
  - All 12 cells of RESPONSE §4 reproduce with the review's rule (`n6_matched_rule.py`).
- **N7 figures the record compares with N6:** P1 +0.00909, S1 +0.00808, S3 −0.00454, S4 +0.01394, S5 +0.01382. Later-end readings +0.00702, +0.00399 and +0.01043 [−0.00027, +0.02113]. N6's rule on N7 gives +0.01495, +0.01128 and +0.01806 (5 draws). Cross-rate +0.01184 and +0.01235 (later end +0.00518). 768 rate effect +0.00198 [−0.00128, +0.00524]. 512's training-loss deficit at 1e-4 is 0.134. Validation rises E3 → E3.25 in 24 of 24. First-quarter rises are 0.011–0.021 against 0.002–0.007.
- **Labels:** "preregistered within the project" is accurate for S's slope, N4 P1 and P3, and N5 M under Holm. N6 is correctly described as registered publicly only after its data existed; the PR #3 snapshot gives merge 2026-11-03T16:14:41Z, commit `58240f0…`.
- **Scope statements:** 3e-5 was selected for 128–384 only (grid lower edge). 3e-4 is the best mean over eight widths. 1e-4 is the best of five rates for 768 on t00. Token counts are 0.2–2.1 M and the largest model is 34.7 M parameters.
- **Hashes:** `ANALYSIS.json`, `POINTS.csv` and `FITS.csv` of N3–N6 match the hashes in their result reports. All files listed in the six `SOURCE_SUBJECT.json` (S, N1, N3, N4, N5, N6) match (129 files, 0 mismatches). `RESPONSE.md` and N6 `RESULT.md` match the hashes cited for them.
- **Disclosure:** failed attempts, the search incident, the second attempts on the same seeds, and the two preserved failed verifier runs are all disclosed. v0135 (gates failed) and v0136 (CALIBRATION_FAILED) are described accurately in the README.

## Comparison with the 8 November audit (`earlier/FINDINGS.md`)

| Its finding | My result |
|---|---|
| Held list | Confirmed for every statistic it names, including S32, SD and S_batch. "60 files byte-identical in public" I cannot check. Evidence-chain checks I read as stored PASS records (184 and 72 claims, 0 failures) and did not rerun. |
| E-1, N6 matched figures inflated | Confirmed on N7's draws (+0.01495, +0.01128, +0.01806). Addressed by the 9 Nov correction and `CURRENT_CLAIMS.md`. Two residues: the blanket "upper-biased" is wrong for the cells where 512 is read (EA-5; the audit's own D1 transfer goes upward, +0.0027 → ≈ +0.011), and S4's +0.0041 is not like for like (EA-6). I did not recompute the audit's transfers to N6 (≈ +0.0064 and so on); they are model-based. |
| E-2, N7 means outside N6's intervals for P1 and S4 | Confirmed. Addressed in the 9 Nov correction §1. |
| E-3, D2 matched on the gap reads the other arm | Confirmed: all six draws read 512. Not addressed: no page states the read direction per cell, and this is the root of EA-5. |
| E-4, 768 rate residual spans 0 on N7 | Confirmed. Already stated in `CLAIMS_4_AND_5_STATUS.md`; not carried into `CURRENT_CLAIMS.md`, which is acceptable. |
| E-5, public index names PR #5 and the reopening | Confirmed in the current page. |
| E-6, failure reports and DECISION public and consistent | Consistent, yes; identity with local files I cannot check. The index states the N1 cause more firmly than the report (EA-8). |

The 8 November audit did not raise EA-1, EA-2, EA-3, EA-4 or EA-7 to EA-10.

## Not checked

- Anything under `work/runs/`: p\* itself, per-sequence losses, E0 values, clipping and bound-32 refits for S and N1–N6. Their arrays are unpublished, so every recomputation starts from `POINTS.csv`.
- Whether protocols were sealed before data existed, beyond internal dates and the PR #3 snapshot. The copy is not a git repository, so the "`git diff` prints nothing" statements were not run.
- N7's registration and its PR #5 snapshot, as out of my area. Likewise the N7 per-sequence post-hoc figures (the exposure-matched contrasts and the 0.050–0.084 recency gap), which need the release bundle.
- The N5 planning fixtures (unpublished) and the audit's N6 transfer estimates.
- Stages 1–11 and v0129–v0134 beyond the two result records the README cites; no current claim rests on them.
- The evidence-chain check scripts were not rerun; some read run directories.
