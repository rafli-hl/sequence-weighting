# Area 5 — alternative explanations for N7's reversal: findings

Written 8 Nov 2026 by the orchestrating assistant from `ALT_RESULTS.txt` (§0–13) and `ALT_FOLLOWUP.txt`; the scripts read only the sealed outputs and N6's `POINTS.csv`. No new computation. The sealed statistics reproduce (§1).

- **AL-1 (major, reword).** Within-epoch non-linearity: the first quarter-epoch step in p\* exceeds every other quarter step in 48/48 arm-draws (ratios 2.9–5.0; §3). Three P1 readings sit in E2–E2.25. Reading 768 at the higher end of its bracket: P1 +0.00702 [+0.00216, +0.01189] 5/6 and S1 +0.00399 [+0.00099, +0.00699] 5/6 stay above 0; **S4 +0.01043 [−0.00027, +0.02113] spans 0** (m06 in the E3→E3.25 jump, +0.0224; §2). Report bracket-end sensitivity for every matched step.
- **AL-2 (major, concede).** Exposure phase: at the matched point 768 has revisited 19–48 % of the training set in epoch 3; 512 at E3 has revisited 100 % (§13). Validation NLL rises E3→E3.25 in 24/24 arm-draws (§3). corr(768's matched p\*, phase) = +0.79; 768's reading supplies 81 % of P1's variance (`ALT_FOLLOWUP` b, d). The two readings differ in phase as well as updates.
- **AL-3 (note, cite).** The reversal survives other anchorings: 768 anchored at E2.0, E2.25 or E2.5 with 512 read along its path gives +0.0190, +0.0105 [+0.0057, +0.0153], +0.0176, all 6/6; a sweep of common loss levels 4.21–4.32 gives 512 − 768 > 0 in 6/6 at every level (§4). This answers AL-2 as a full explanation.
- **AL-4 (minor, rebut).** Equal loss ≠ equal gain: 768's E0 is 0.037 nats higher. Matching on gain gives P1 +0.01584 [+0.01041, +0.02126] (the protocol's "about 0.006" rise holds); the E0 offset correlates −0.67 with P1, opposite to a dilution artefact (§5).
- **AL-5 (minor, concede).** Estimator mechanics: scale-invariant; a uniform extra 0.037 nats lowers p\* by ≈0.0027 (§6), which works against the reversal.
- **AL-6 (note).** Rate specificity: the rate effect on p\* at 512 is almost all progress (predicted −0.0182, observed −0.0164); S3 predicted from P1 and 768's within-epoch slope is −0.0043, observed −0.0045 (§7).
- **AL-7 (minor).** P1 skew −1.16 (W = 0.855, not rejected); bootstrap intervals exclude 0 for P1, S1, S4, S5 (§9).
- **AL-8 (minor, disclose).** S2-unavailable draws: mean P1 +0.0120 against +0.0061 (§8).
- **AL-9 (note).** Validation paths are non-monotone in 24/24 arm-draws (§11).

Ranking: AL-1 and AL-2 come first; AL-3 answers them from existing data. New runs needed: readouts inside E2.0–E2.25, and a match at an epoch end.
