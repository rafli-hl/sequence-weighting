# N8: dense-readout replication of N7. Protocol draft

**Status: FINAL, 14 November 2026. Registered by the merge into `rafli-hl/sequence-weighting` and the tag
`n8-registration`.** This is a new study in a new record. It reuses N7's sealed code and recipe, and adds nothing to the closed
`sequence-weighting` record.

## 1. Question

In N7, at learning rate 1e-4 and with width 512 read at epoch 3, the contrast p\*(512) − p\*(768) was:
- below 0 at equal updates (S3: −0.0045 [−0.0079, −0.0011]);
- above 0 at equal training loss (P1: +0.0091 [+0.0040, +0.0142]).

Two weaknesses limit that result:
1. **Interpolation.** Width 768 was read by interpolating between readouts a quarter epoch apart. A 13 November audit
   showed that under some combinations of bracket ends, S1's interval reaches 0 and P1's lower limit is barely above 0.
2. **Fragility at equal updates.** S3's interval includes 0 when either of two draws is left out.

N8 asks: **on fresh draws, with readouts dense enough that interpolation hardly matters, does the order of widths 512
and 768 at 1e-4 again differ between equal updates and equal training loss?**

N8 does not ask whether 512 leads once exposure is also matched. Equal training loss inside an epoch still leaves
exposure unequal. That needs a different design (section 9).

## 2. Hypotheses

Both are directional and both come from N7.

- **H1, equal training loss:** p\*(512, E3) − p\*(768 at 512's E3 training loss) > 0.
- **H2, equal updates:** p\*(512, E3) − p\*(768, E3) < 0.

**Reversal replicated** requires both H1 and H2 to be confirmed (section 6). If only one is confirmed, that is
reported as it stands, and the study does not call it a reversal.

## 3. Design

| Item | N8 | Change from N7 |
|---|---|---|
| Widths | 512, 768 | same |
| Learning rate | 1e-4 only | 3e-4 dropped: the reversal question concerns 1e-4 |
| Model, pre-training, optimiser, batch, clipping, loss, weights | as N7's sealed source | same |
| Weighted training | 3.5 epochs (3,584 updates) | same |
| Readouts | E0; epochs 0.25, 0.5, 1; then **every 64 updates from update 2,048 to 3,584** (epoch 2 to 3.5, 25 readouts) | denser: 64 updates instead of 256 |
| Draws | **24** fresh draws, n01–n24, of 16,384 sequences each | 6 → 24 (section 7) |
| Batch order | one permutation per epoch from each draw's order seed, shared by both widths | same rule |
| Evaluation | per-sequence loss on all training and validation sequences at every readout | same |
| Disk | about 4.6 GiB for the kept E0 states, plus the loss arrays and orders; at least 8 GB must be free before R1, and the owner script refuses to start R1 otherwise | new |
| Saved outputs | per-sequence loss arrays at every readout; each epoch's batch order, saved as little-endian int64 indices, with its SHA-256; E0 model states kept until the analysis is published | adds saved orders, order hashes and kept E0 states |

## 4. Data

- **Corpus.** N7's corpus (manifest `be911db7…`), with the tokenizer, validation set and pre-training pool of N6 and
  N7.
- **Fresh articles.** Exclusion rules as N7, plus every article N7 assigned to m01–m06. The owner's count of
  13 November (`data-count/FRESH_POOL_COUNT.json`) measured the fresh pool: **14,039 articles and 582,603
  sequences**. 24 draws of 16,384 need 393,216 sequences, and 401,064 suffice whatever the shuffle (the largest fresh
  article holds 328 sequences). The draw step must record the real count and stop if it falls short.
- **Partition.** As N7: sort the fresh indices, shuffle with the registry's partition seed, and assign whole articles
  until each draw holds 16,384 sequences.
- **Seeds.** A new registry, drawn once by the owner. It excludes every value in earlier registries and every seed
  recorded in a JSON file anywhere in the N8 study folder. The pilot therefore records its throwaway seeds in a JSON
  log.

## 5. Matching

- **Equal training loss (H1):** the target is 512's mean unweighted training loss at E3. 768 is read along its
  readouts from update 2,048 to 3,584 by linear interpolation of fitted p\* between the two readouts that bracket the
  target, 64 updates apart.
- **Reading rules (as N7).** Use the first bracketing interval in readout order. A flat interval holding the target
  is read at its earlier readout. A draw whose target falls outside the path is unavailable for H1, and the number of
  bracketing intervals is reported.
- **Equal updates (H2):** both widths at update 3,072. No interpolation.

## 6. Analysis

- **Unit.** The draw. Each contrast is computed within a draw.
- **Test.** For each hypothesis: a two-sided 95% t interval over draws; confirmed if the interval lies entirely on the
  predicted side of 0. An exact two-sided sign test is reported beside it.
- **Minimum.** H1 and H2 are each UNAVAILABLE with fewer than 20 of 24 draws available.
  - A draw is unavailable for H1 if its target lies outside 768's path or a fit it needs is undefined or saturated.
  - A draw is unavailable for H2 if either width's fit at update 3,072 is undefined or saturated.
  - A failed draw (section 8) is unavailable for both.
- **Path.** 768's matching path is all 25 readouts from update 2,048 to 3,584 inclusive (epoch 2 to 3.5).
- **Labels.**
  - Each hypothesis is labelled CONFIRMED if its interval lies entirely on the predicted side of 0; CONTRARY if
    entirely on the other side; INCONCLUSIVE if the interval includes 0; or UNAVAILABLE.
  - The joint label is REVERSAL_REPLICATED if both H1 and H2 are CONFIRMED, and REVERSAL_NOT_REPLICATED otherwise.
  - As in N7, "entirely" means beyond 0 by more than 1e-9.
- **Joint decision.** The reversal is confirmed only if both H1 and H2 are confirmed. Requiring both is an
  intersection-union test: no multiplicity correction is needed, and the chance of falsely declaring a reversal is
  at most 2.5%.
- **Rules carried over from N7.** Each is reported, and none gates a label unless stated:
  - **Saturation:** a fit at or above 7.999 is refitted with the upper bound at 32.
    - If the refit resolves, the label still uses the bound-8 value, as in N7, and the bound-32 values and interval are
      reported alongside.
    - An unresolved refit makes that draw SATURATED, and the draw is unavailable for the statistics that use it.
  - **NOT_OVERFIT:** per width, the interval of validation loss at E3 minus E2.
  - **Records against arrays:** each readout's recorded mean losses must match its arrays within 1e-3, or the readout
    is flagged.
- **Analysis environment.** The sealed analysis runs on native Windows Python 3.12.10 with NumPy 2.5.3. The estimator
  is a verbatim copy of N7's `vendor/core.exponent`. On N7, WSL (Python 3.12.3, NumPy 2.2.6) reproduced p\* to within
  8.8e-10, not bit for bit; no other platform has been measured. WSL is a cross-check only, and its comparisons use a
  tolerance of 1e-9 for p\* and for contrasts built from it.
- **Study status.**
  - COMPLETE: all 24 draws finished.
  - COMPLETE_WITH_FAILED_DRAWS: 20–23 finished.
  - INCOMPLETE: fewer than 20 finished; no statistic and no label.

**Registered sensitivity analyses.** These are reported, but they do not change the labels.

1. **Bracket envelope (the lesson of the 13 November audit).** Take each draw's 768 reading at either end of its
   bracket and enumerate all combinations. With 24 draws that is 2^24 ≈ 16.8 million. The lower t limit is concave in
   the contrasts, so its minimum is at a vertex; report the exact envelope of the lower and upper t limits. This
   bounds the effect of the reading rule, assuming p\* stays between the bracket readouts; it is not a calibrated
   interval.
2. **Leave-one-draw-out intervals** for H1 and H2.
3. **Starting offset.** H1 with 768's gains lowered, per draw, by that draw's mean difference in E0 training loss
   between the widths, then 768 refitted at the registered bracket ends with the registered weight. This is the
   computation of the 12 November follow-up audit (AA-3), now registered in advance.

**Registered secondary analyses (descriptive; no labels).**

- **S-a, equal improvement:** 768 read where its mean gain from its own E0 equals 512's at E3.
- **S-b, exposure windows:** the 11 November recency-window comparison of N7, applied to N8 with **quarter-epoch
  windows**: 768 is read at epochs 2.25, 2.5 and 2.75 against 512 at epoch 3, exactly as in N7. The denser readouts
  are not used for the windows, because 64-update windows would leave sets of 4–256 sequences.
  - Report each set's size and its recency balance: the mean age difference in updates, and the joint quarter-cell
    distance.
  - The sets are built from the batch orders the workers save (section 3).
- **S-c, fit diagnostics:** objective at the fit relative to its value at p = 0, maximum absolute cumulative
  discrepancy, and 16-bin gain residuals, for every fit.
- **S-d, path:** the contrast at every readout from epoch 2 to 3.5, with pointwise intervals.

## 7. Sample size

The effects observed in N7 are probably optimistic: six draws, and the effect chosen because it was found. The plan
therefore assumes **half of N7's effects at N7's between-draw SDs**:
- H1: effect +0.00454, SD 0.00485;
- H2: effect −0.00227, SD 0.00324.

With a two-sided t test at 5%:

| Draws | Power for H1 | Power for H2 | Lower bound on joint power |
|---|---|---|---|
| 12 | 0.84 | 0.60 | 0.44 |
| 16 | 0.94 | 0.74 | 0.68 |
| 20 | 0.98 | 0.84 | 0.82 |
| **24** | **0.99** | **0.91** | **0.90** |

At N7's full observed effects, 8 draws would already give joint power of at least 0.92. If the true effects are
two-thirds of N7's and the SDs 1.5 times larger, 24 draws give a lower bound of 0.81. The joint figure is the
Bonferroni lower bound P(H1) + P(H2) − 1; it assumes nothing about the dependence between H1 and H2.

**Compute.** N8 trains 48 arms: 24 draws × 2 widths at one rate. N7 trained 24 arms: 6 draws × 2 widths × 2 rates.
So N8 needs about twice N7's training. Evaluations rise more: 28 readouts per arm instead of 10, so 1,344 in all
instead of 240, about 5.6 times as many.

**Pilot (measured, 13 November).** One draw, N7's m01 (16,384 sequences) with throwaway seeds, ran through the N8
worker on the GPU and was then discarded (`pilot/PILOT_LOG.json`, SHA-256 `251d0951…`). Times are on the worker's
clock, which is the clock of the caps.
- **Start-up decision:** GO (ALL_WIDTHS_WITHIN_LIMIT), from a benchmark of 43.6 s (22.0 s at width 512, 21.6 s at
  width 768).
- **Per draw:** 2,528 s (42.1 min), within the cap of 3,097 s per draw that the worker sets for a run of three draws.
  - Width 512: 867 s. Pre-training and E0 took 55 s; weighted training 242 s; evaluation at its 28 readouts 570 s.
  - Width 768: 1,660 s. Pre-training and E0 took 101 s; weighted training 462 s; evaluation 1,097 s.
  - Evaluation takes about two thirds of the time.
- **Per run of three draws:** about 2.3 h wall time (2.1 h on the worker clock: 7,629 s, the benchmark and three
  draws at the pilot's time). The wall time applies the ratio seen in earlier runs on this machine, where Windows
  time ran 1.06–1.11 times the worker's. The benchmark projected 2.00 h on the worker clock (7,186 s). Both fit the
  6-hour cap, which is on the worker clock.
- **Memory:** PyTorch reserved at most 1.42 GiB of GPU memory, at width 768.
- **Schedule:** at the pilot's time, the eight runs R1–R8 take about 17 hours on the worker clock, about 18–19 hours
  of wall time.

## 8. Stopping, failures and deviations

- **Fixed sample.** 24 draws, no interim analysis, and no look at any p\* before all 24 draws are complete.
- **Runs.** The 24 draws are trained in eight runs, R1–R8, of three draws each, in registry order.
- **Failures.** A run that stops early can be retried once, as X1–X8.
  - A retry is admitted only on its first run's terminal record.
  - It repeats from scratch, with the same seeds, the draws that run did not finish.
  - It reports how each width's new E0 losses compare with the first attempt's.
  - A draw that fails in both attempts is reported as failed and excluded. Fewer than 20 completed draws makes the whole study INCOMPLETE, with no labels.
- **Deviations.** Any departure from this protocol is recorded with its date before the analysis runs, and listed in
  the result.

## 9. What N8 cannot settle

- **Exposure.** At equal training loss, 768 is read part-way through its third epoch. Only a design that matches
  exposure and loss together can separate the two; one candidate compares the widths only at epoch boundaries, with
  schedules set so that their losses meet there. That is a separate study.
- **Scope.** One pair of widths, one rate, one recipe and a small scale.
- **Independence.** The analysis code is written by the same project and checked by AI systems, not by independent
  people.

## 10. Before registration

1. **Make the N8 source.** Copy N7's sealed source and make only the changes listed in `CHANGES.md`, each justified by
   a section of this protocol.
2. **Write and test the analysis code on N7's released losses.** The code must reproduce every N7 number before it is
   sealed:
   - P1, S1, S3, S4 and S5 within 1e-6 of `ANALYSIS.json`;
   - every `MATCHED.csv` row within 1e-9;
   - all 240 refits within 1e-9 on the analysis environment;
   - the 64-combination envelope: P1 +0.0000764, S1 −0.0000507, S4 −0.000268.

   Done on 13 November (gate 1), including the sensitivity and secondary analyses. On N7 every check passes: 60/60
   on N7 and 37/37 synthetic, in both the registered environment and WSL.
3. **Run an engine check on one pilot draw that is then discarded:** time it, measure memory, and confirm that the
   orders and readouts are written.

   Done on 13 November (gate 4): PASS, on N7's m01 with throwaway seeds, then discarded (`pilot/PILOT_LOG.json`,
   SHA-256 `251d0951…`). The figures are in section 7.
4. **Have the owner draw the seed registry and run the partition**, then pin the partition hash.

   Done on 14 November: the owner's draw (OWNER-20261114-N8-SEEDS-01) passed all 16 post-draw checks; registry
   `7628c809…` and partition `15c1d598…`, pinned in `source/matched_plan.py` (sealed subject `9bdea3a9…`).
5. **Seal the protocol, source and registry by hash**, merge them publicly and tag. Only then train.