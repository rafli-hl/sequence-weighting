# Area 3 (second recomputation) — findings

Written 8 Nov 2026 by the orchestrating assistant from `compare_with_sealed_output.txt`, `robustness_checks_output.txt` and `RECOMPUTE_STATS2_OUTPUT.txt`. One new computation: `recompute_stats2_part2.py`, whose saved output was empty, re-run into `RECOMPUTE_STATS2_PART2_OUTPUT.txt` (reads `POINTS.csv`, `FITS.csv`, `MATCHED_PLANNING.json`, `RESULT.md`; fails in its last section on a key of its own JSON after sections A–G print).

## Held

- From `POINTS.csv` alone, with the protocol's matching rule and own t critical values (df 5: 2.5705818356363133), every statistic equals the sealed one: largest difference 7.2e-13 over means, limits and leave-one-out; per-draw rows and brackets identical; labels and `confirmed_through` S5 identical; `MATCHED.csv` rows differ by 0; NOT_OVERFIT intervals identical; by-readout contrasts to 6.5e-13; rate effects identical up to sign convention (`compare_with_sealed_output.txt`).
- E0 per draw recovered from `FITS.csv` (train + total_gain / 16,384) reproduces the sealed panel E0 (512 5.543738, 768 5.580711); gain-matched P1 +0.015836 [+0.010410, +0.021262], a rise of +0.0067 over the training-NLL match, as the protocol's §11 "about 0.006" says.

## Findings

- **S2-1 (major, reword).** Realized spread against the plan: P1 sd 0.004845 is 1.96× the planning sd 0.002477, and the realized mean 0.69× the planning effect (`robustness` §3). The study ran in the plan's pessimistic cell (0.703), while RESULT.md §2 still prints ">0.999". Report the realized spread beside the planning one.
- **S2-2 (minor, disclose).** Sign-test fragility: counting |value| < 1e-4 as a tie turns P1's 6/0 into 5/0/1, exact two-sided p 0.0625 (`robustness` §5).
- **S2-3 (minor, disclose).** Exposure: the matched 768 readings sit at phase 0.19–0.48 of epoch 3, 512's target at phase 1.0 (`robustness` §4, §6).
- **S2-4 (minor, disclose).** Three of six P1 brackets span the E2→E2.25 step, which carries 48–52 % of 768's whole E2→E3 rise (`robustness` §7).
- **S2-5 (note).** S2's UNAVAILABLE is a window effect: with 768's path extended to E1 (not the protocol) all six draws read, +0.01602 [+0.00155, +0.03050]; the protocol foresaw this (§6).
- **S2-6 (note, cite).** Phase sensitivity: reading 512 at E2.75, E3.25 or E3.5 instead of E3 keeps the training-NLL-matched contrast positive at both rates with 6/6 (`robustness` §2).
- **S2-7 (note).** Part 2 reproduces the protocol's power cells (0.703, 0.576 with N6's unrounded inputs; 0.698, 0.571 with the printed ones) and S2's availability figures (73/65/38/35 %); its spot check prints "MISMATCH" for P1/S1 from a p-value regex, not a differing number.

No blocker. S2-1 duplicates protocol P2-02.
