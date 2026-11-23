# Correction to the record, 23 November 2026

**Status:** issued by the owner. It follows the external audit of 13 November 2026
([`AUDIT.md`](../external-audit-20261113-01/AUDIT.md)), which is post hoc and AI-made: an AI reviewer (OpenAI Codex)
audited the public record at commit `fee55ea`.
**Scope:** this note corrects statements in the record and says how some results should be read. It does not edit any
historical file, change any registered number or label, or report any new run. Every new figure below is post hoc and
descriptive. The F1 envelope and the F3 recency figures are reproduced by N8's
[`test_on_n7.py`](../../preregistration/natural-text-dense-replication-20261114/analysis/test_on_n7.py). The F2 scale
is computed by [`gap_scale.py`](gap_scale.py) from N5's published `POINTS.csv`, with its output in
[`GAP_SCALE.txt`](GAP_SCALE.txt).

## Summary

1. **F1.** The 9 November correction's "P1 and S1 stay above 0 under the least favourable reading" is wrong for S1, and
   P1's margin is minimal. The registered labels are unchanged.
2. **F2.** C3's gap difference does not establish equal gaps. "The same gap" becomes "a similar gap", with a
   descriptive scale.
3. **F3.** The exposure-matched sets have matched recency windows, not equal recencies.
4. **F4.** N6's width 384 at 3e-4 was missing from the study table in `METHODS.md`.
5. **Also recorded:** the audit's tokenizer rebuild, and that the simulation behind the "about 2.5%" familywise rate is
   unpublished.

## 1. F1: the later bracket end is not the least favourable reading

The [9 November correction](../natural-text-correction-20261109-01/CORRECTION.md), §3, read width 768 at the later end
of each draw's interpolation bracket and said that "P1 and S1 stay above 0 under the least favourable reading". Reading
every draw at its later end gives the smallest mean contrast, but not the smallest lower t limit: reading some draws at
the earlier end can shrink the spread over draws more than it raises the mean.

If p\* stays between the two readouts that bracket each draw's reading, each of the six draws can be read at either end:
2^6 = 64 combinations. The lower t limit is concave in the six contrasts, so its smallest value over that range is at
one of the 64.

| Step | Sealed (interpolated) | All later ends (9 November) | Lowest lower t limit over all 64 combinations |
|---|---|---|---|
| P1 | +0.00909 [+0.00400, +0.01417] | +0.00702 [+0.00216, +0.01189] | +0.0000764 |
| S1 | +0.00808 [+0.00487, +0.01130] | +0.00399 [+0.00099, +0.00699] | **−0.0000507** |
| S4 | +0.01394 [+0.00893, +0.01896] | +0.01043 [−0.00027, +0.02113] | −0.000268 |

For S1, the lowest limit reads draw m02 at the earlier end and the other five at the later end (the audit's §3.1).

**What changes:**
- The sentence "P1 and S1 stay above 0 under the least favourable reading" is wrong for S1: under one combination of
  bracket ends, S1's interval includes 0.
- P1's interval stays above 0 under every combination, but its lowest lower limit, +0.0000764, is barely above 0.
- These are envelopes of plug-in t limits, conditional on p\* staying between the bracketing readouts. They are not
  calibrated intervals.
- The registered labels, which use linear interpolation, are unchanged, and so are the all-later-end figures, which
  remain correct as a sensitivity reading.

**Reproduced by:** N8's analysis test, `test_on_n7.py`, which computes the envelope on N7's data, checks the three
values within 1e-6 against a brute-force enumeration (`ENVELOPE_MIN_LOWER`), and passed on 13 November (N8's protocol,
section 10, step 2: 60 of 60 checks on N7).

## 2. F2: C3's gap difference does not establish equal gaps

The [12 November correction](../natural-text-correction-20261112-01/CORRECTION.md), §3, and C3 in `CURRENT_CLAIMS.md`
said that at epoch 2 at 3e-4 in N5, widths 512 and 768 "have the same gap" (768 − 512: +0.0004 [−0.0047, +0.0055]).
An interval that contains 0 does not establish that the gaps are equal. The ten draws' gap differences range from
−0.0092 to +0.0145 nats.

**What changes:** C3 now says "a similar gap".

**A descriptive scale.** Near epoch 2, p\* rises by about 0.15–0.19 per nat of gap within either width. These are the
mean slopes over N5's ten draws between neighbouring readouts:
- width 512: 0.157 from epoch 1 to 2, and 0.185 from 2 to 3;
- width 768: 0.149 and 0.167.

At that rate, a gap difference at the interval's upper limit, 0.0055 nats, corresponds to 0.0008–0.0010 of p\*. That
is about a tenth of the p\* difference between the two widths at the same readout, −0.0092 [−0.0112, −0.0072].

This is a scale, not an equivalence test. The slope is taken along training, where the gap and training progress change
together, and no tolerance was set in advance.

## 3. F3: matched recency windows, not equal recencies

`METHODS.md` said that the exposure-matched sets of 11 November are chosen "so that every pass is equally long ago in
both". The sets are matched on recency windows: each pass of both sets falls in the same quarters of its epoch,
counted back from the readout. The realised ages differ.

At k = 1, 2 and 3, the largest difference between the two sets in the mean age of a pass is 14.1, 8.4 and 7.0
updates. This is the largest over draws and passes, in updates before the readout: 14.11545, 8.44744 and 6.99420. The
largest total-variation distance between the sets' joint distributions over quarter cells is 0.000, 0.037 and 0.037.

These are the audit's figures. `test_on_n7.py` reproduces them within 5e-6 from N7's regenerated batch orders.

**What changes:** `METHODS.md` now says "matched recency windows" and gives these differences. C4 in
`CURRENT_CLAIMS.md` says "in matched recency windows for all three passes" instead of "matched for the timing of all
three passes".

## 4. F4: N6's width 384, and the training statement

- **N6's width 384.** The study table in `METHODS.md` listed N6's widths as 512 and 768. N6 also trained width 384 at
  3e-4: it is in the arm table of its sealed protocol, and in its `POINTS.csv`, at 3e-4 only. The row now lists 384 at
  3e-4 beside 512 and 768 at both rates.
- **The training statement.** The audit also noted that the claims page put the inability to retrain down to the
  absence of model states and dataset rows, without the README's distinction between evaluating models and rebuilding
  and retraining. The claims page's training row now follows the README's five levels.

## 5. Also recorded

- **The tokenizer.** The audit reports that it rebuilt the tokenizer twice from the pinned public WikiText-2 training
  parquet, with the sealed code and `tokenizers` 0.21.4. Each rebuild gave 107,106 bytes with the pinned SHA-256
  `cd642ca2b78a76e880adf07efb425bd2db741248cbf537aed0538c9421cca146` (`acquire_plan.py`). This is the audit's result,
  and it was not rerun for this record. It removes one practical step from a retraining. The corpus files have not been
  rebuilt, and no retraining has been attempted.
- **The familywise rate.** The README and `METHODS.md` give N7's chance of any false confirmation as about 2.5%, from
  the protocol's simulation.
  - The simulation is in N7's planning and review records, which are not published; N7's `HASHES.json` names the review
    record by hash only. Its code, number of replicates and null configurations therefore cannot be checked from public
    files.
  - The audit adds that, for valid one-sided tests at 0.025 in a fixed order, the standard fixed-sequence argument
    bounds the rate without the simulation. That argument needs each test in the sequence to be valid.

## What does not change

No registered number, label, sealed file or historical file changes. The audit's suggestions F5 (fit-residual
diagnostics) and F6 (estimator edge-case fixtures) are not adopted in this update.

Living pages changed:
- `CURRENT_CLAIMS.md`: C3, C4's table and exposure bullet, and the training row;
- `METHODS.md`: §1's table, §5's exposure-matched comparison, §6 and §7;
- `README.md`: the sensitivity table's note, the familywise rate and the training level.
