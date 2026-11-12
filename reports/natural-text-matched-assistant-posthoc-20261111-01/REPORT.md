# N7 by training exposure: a post-hoc analysis, 11 November 2026

**Status: post hoc and descriptive. This is not a sealed result.** Nothing in this report was registered. It reports
no new run, changes no sealed label, interval or reading, and adjusts no interval for the number of comparisons. Every
figure was computed after N7's outcomes, and the outcomes of earlier post-hoc looks at the same data, were known.

**Who did it.** An AI assistant, Claude Fable 5.2 (model ID `claude-fable-5-2`, Anthropic), made the analysis: first
on 10 November 2026, as an adversarial check, and again on 11 November, when it wrote the script filed here and ran it
for this report. A second model, Claude Opus 5.5 (the session supervising the check), recomputed the main figures with
separately written code on 10 and 11 November and obtained the same values to the printed digit; that code is not part
of this record. The script filed here reproduces the 10 November outputs to every printed digit. No human has checked
the analysis.

**What it reads.** The N7 loss-array bundle attached to the
[v1.0 release](https://github.com/rafli-hl/sequence-weighting-research/releases/tag/v1.0) (`n7-loss-arrays-v1.zip`;
its `MANIFEST.json` is `6f9c124787760b9b64e219bb55206bdc3f7f9b45774cb5eb82d4d528607b3698`) and
[`POINTS.csv`](../natural-text-matched-analysis-20261105-01/POINTS.csv)
(`234434a34cf64d98e0d45cfe029bb37935207176fd996cafe85756956c7d860f`). It opens nothing under `work/runs/`, and it
regenerates no loss by running a model.

| File | SHA-256 |
|---|---|
| [`posthoc_exposure.py`](posthoc_exposure.py) | `aa1f858267d2a6e759ede47e2a8b4ef1895fd7fedc89fe6059a6a526af96d26d` |
| [`OUTPUT.txt`](OUTPUT.txt), its exact output | `258ddd1b3523076b9bec4f42cb100fa83117621d456f70baadb805ec3a130962` |
| [`RESULTS.json`](RESULTS.json), the per-draw values behind every printed interval | `914490d1b6730c6a550462ce09d64710ab2982c1522e6faf1e95bd2b61de3a9c` |

To reproduce, with NumPy and PyTorch (CPU) installed and the bundle unpacked:

```sh
python reports/natural-text-matched-assistant-posthoc-20261111-01/posthoc_exposure.py path/to/n7-loss-arrays
```

The output filed here was produced with NumPy 2.5.3 and PyTorch 2.7.0 and is identical on a second run.

## Summary

Every contrast is p\*(512) − p\*(768), with a two-sided 95% t interval over the six draws (df 5) and the number of
draws above 0.

1. **Within one model, p\* depends on when a sequence was last trained.** At every readout inside an epoch from epoch
   2, the sequences already trained in the current epoch have p\* higher by 0.050 to 0.084 than those not yet trained
   in it (20 of 20 arm-readouts, 6/6 draws each).
2. **The larger rise of p\* after an epoch boundary goes with the sequences not trained in that quarter.** The
   quarter being trained gains 0.053 to 0.082 in every interval, boundary or not. The other sequences lose 0.011 to
   0.024 in quarters inside an epoch but change by only −0.007 to +0.002 in the first quarter after a boundary. The
   cause is not identified.
3. **At 1e-4, on sequences matched for the timing of every pass, the lead of 512 that P1 shows is not seen.** For 512
   at epoch 3 against 768 at epochs 2.25, 2.5 and 2.75, the matched contrasts are −0.0035 [−0.0258, +0.0189],
   −0.0048 [−0.0121, +0.0026] and −0.0051 [−0.0109, +0.0008]. Every interval includes 0. The whole-set contrasts for
   the same pairs of readouts are +0.0100, +0.0040 and −0.0003, and exceed the matched ones by +0.0135
   [−0.0076, +0.0345], +0.0088 [+0.0032, +0.0143] and +0.0047 [+0.0014, +0.0081]. At epoch 2.25, the pair nearest to
   equal overall training loss, the matched sets hold about 250 sequences and the interval is too wide to exclude
   P1's own value.
4. **At 3e-4 the lead of 512 remains on matched sequences:** +0.0126 [−0.0099, +0.0351], +0.0126 [+0.0049, +0.0204]
   and +0.0129 [+0.0072, +0.0187].
5. **With each width at its better rate of the two, 512 is above 768 on both axes.** 512 at 3e-4 against 768 at
   1e-4 gives +0.01184 [+0.00789, +0.01578], 6/6, at equal updates at epoch 3, and +0.01235 [+0.00523, +0.01947],
   5/6, at equal training loss. The second interval includes 0 when 768 is read at the later end of each bracket.
6. **At 1e-4 the equal-updates contrast is negative only late.** It is above 0 at epochs 0.25, 0.5 and 1, includes 0
   at epochs 2 and 2.25, and is below 0 from epoch 2.5.

P1 stays confirmed as registered: it is a statement about whole-set p\* at equal overall training loss, and it
reproduces. What changes is how it can be read. See [What this changes](#what-this-changes-in-the-claims).

## Method

### Batch orders

The loss arrays do not record which sequences were trained when. The sealed engine draws the order of epoch e as
`torch.randperm(n, generator=torch.Generator().manual_seed(999 + adapt_order_seed + e))`
([`text_engine.py`](../../preregistration/natural-text-matched-confirmation-20261104/sealed-source/text_engine.py),
`orders`) and trains on consecutive batches of 16
([`matched_worker.py`](../../preregistration/natural-text-matched-confirmation-20261104/sealed-source/matched_worker.py),
`adapt_readouts`). The readout at epoch (e − 1) + k/4 therefore follows the first 4,096 k entries of epoch e's
order. The seeds are in the bundle's `MANIFEST.json`. Every arm of a draw shares the order, so the two widths and
both rates see the same sequences at the same updates.

"Quarter q of epoch e" means positions 4,096 (q − 1) to 4,096 q − 1 of that order. Exposure is resolved to quarter
epochs, because that is the spacing of the readouts from epoch 2.

### Checks made by the script before any analysis

| Check | Result |
|---|---|
| Bundle files against `MANIFEST.json` | 66 of 66 match |
| Refit of all 240 whole-set estimates against `POINTS.csv` | Largest difference 1.3e-8 |
| Weights regenerated from `weight_seed` | Bit-identical to the bundle in 6/6 draws |
| Regenerated orders against the losses: loss change, over each of the 8 quarter-epoch intervals between readouts, of the sequences the order says were trained in it, minus that of the others | Mean −0.226 nats, range [−0.347, −0.119], in 192 of 192 interval × draw × arm cases |
| Negative control: the same with the order seed shifted by 1 | Mean +0.0001 nats, range [−0.009, +0.012] |
| Edge of the quarter: last 256 sequences trained in the quarter minus the first 256 after it | Mean −0.219 nats, below −0.05 in 168 of 168 |

The script stops if the installed PyTorch does not reproduce orders that pass these checks.

### Estimator and intervals

p\* is fitted with the sealed search (grid of step 0.05 on [0, 8], 50 ternary steps, best of that point and the two
ends), re-implemented in the script, on the gains of whichever set of sequences is named. A subset's p\* uses that
subset's weights and gains only. Intervals are t intervals over the six draws, as elsewhere in the record.

## Results

### 1. Seen and not-yet-seen sequences

p\* of the sequences already trained in the current epoch, minus p\* of those not yet trained in it, in the same
model at the same readout. Every interval is above 0 and every count is 6/6.

| Readout | 512 at 1e-4 | 768 at 1e-4 | 512 at 3e-4 | 768 at 3e-4 |
|---|---|---|---|---|
| Epoch 0.25 | +0.1475 [+0.1446, +0.1503] | +0.1343 [+0.1314, +0.1371] | +0.1977 [+0.1918, +0.2036] | +0.1769 [+0.1735, +0.1803] |
| Epoch 0.5 | +0.0956 [+0.0914, +0.0998] | +0.0865 [+0.0831, +0.0900] | +0.1152 [+0.1102, +0.1201] | +0.1027 [+0.0980, +0.1075] |
| Epoch 2.25 | +0.0605 [+0.0586, +0.0624] | +0.0657 [+0.0640, +0.0675] | +0.0828 [+0.0810, +0.0846] | +0.0841 [+0.0821, +0.0860] |
| Epoch 2.5 | +0.0543 [+0.0516, +0.0570] | +0.0591 [+0.0561, +0.0622] | +0.0730 [+0.0698, +0.0763] | +0.0718 [+0.0682, +0.0754] |
| Epoch 2.75 | +0.0502 [+0.0477, +0.0527] | +0.0541 [+0.0516, +0.0565] | +0.0659 [+0.0631, +0.0687] | +0.0632 [+0.0598, +0.0666] |
| Epoch 3.25 | +0.0557 [+0.0512, +0.0602] | +0.0616 [+0.0568, +0.0663] | +0.0763 [+0.0714, +0.0812] | +0.0780 [+0.0731, +0.0830] |
| Epoch 3.5 | +0.0505 [+0.0463, +0.0548] | +0.0556 [+0.0513, +0.0599] | +0.0686 [+0.0644, +0.0728] | +0.0681 [+0.0631, +0.0731] |

For scale, whole-set p\* at epoch 3 is 0.103 to 0.119, and the contrasts the study tests are 0.005 to 0.014. In the
first epoch the comparison is between sequences trained once and sequences never trained, so its two rows measure
something different.

### 2. Fixed sets across each quarter-epoch interval

T is the 4,096 sequences trained in the interval and O the other 12,288. The table gives the change of p\* over the
interval; "boundary" marks the first quarter after an epoch boundary.

| Arm | Interval | Whole set | T, trained in the interval | O, not trained in it | O falls in |
|---|---|---|---|---|---|
| 512 at 1e-4 | 2 → 2.25, boundary | +0.0114 [+0.0104, +0.0124] | +0.0558 [+0.0545, +0.0571] | −0.0050 [−0.0059, −0.0041] | 6/6 |
| | 2.25 → 2.5 | +0.0050 [+0.0042, +0.0057] | +0.0553 [+0.0545, +0.0562] | −0.0127 [−0.0132, −0.0121] | 6/6 |
| | 2.5 → 2.75 | +0.0040 [+0.0033, +0.0046] | +0.0571 [+0.0558, +0.0584] | −0.0137 [−0.0143, −0.0131] | 6/6 |
| | 2.75 → 3 | +0.0034 [+0.0027, +0.0040] | +0.0580 [+0.0566, +0.0595] | −0.0141 [−0.0148, −0.0133] | 6/6 |
| | 3 → 3.25, boundary | +0.0147 [+0.0131, +0.0162] | +0.0562 [+0.0542, +0.0581] | −0.0006 [−0.0017, +0.0004] | 4/6 |
| | 3.25 → 3.5 | +0.0058 [+0.0051, +0.0066] | +0.0534 [+0.0524, +0.0545] | −0.0107 [−0.0116, −0.0097] | 6/6 |
| 768 at 1e-4 | 2 → 2.25, boundary | +0.0146 [+0.0133, +0.0159] | +0.0626 [+0.0609, +0.0644] | −0.0033 [−0.0043, −0.0023] | 6/6 |
| | 2.25 → 2.5 | +0.0060 [+0.0053, +0.0067] | +0.0607 [+0.0589, +0.0625] | −0.0132 [−0.0137, −0.0127] | 6/6 |
| | 2.5 → 2.75 | +0.0043 [+0.0035, +0.0052] | +0.0621 [+0.0611, +0.0631] | −0.0148 [−0.0156, −0.0140] | 6/6 |
| | 2.75 → 3 | +0.0042 [+0.0033, +0.0051] | +0.0634 [+0.0620, +0.0648] | −0.0146 [−0.0154, −0.0138] | 6/6 |
| | 3 → 3.25, boundary | +0.0191 [+0.0169, +0.0212] | +0.0642 [+0.0615, +0.0669] | +0.0022 [+0.0008, +0.0037] | 0/6 |
| | 3.25 → 3.5 | +0.0068 [+0.0057, +0.0079] | +0.0588 [+0.0572, +0.0604] | −0.0114 [−0.0126, −0.0101] | 6/6 |
| 512 at 3e-4 | 2 → 2.25, boundary | +0.0170 [+0.0159, +0.0181] | +0.0770 [+0.0755, +0.0784] | −0.0062 [−0.0074, −0.0049] | 6/6 |
| | 2.25 → 2.5 | +0.0056 [+0.0049, +0.0063] | +0.0767 [+0.0753, +0.0781] | −0.0198 [−0.0205, −0.0192] | 6/6 |
| | 2.5 → 2.75 | +0.0040 [+0.0026, +0.0054] | +0.0805 [+0.0791, +0.0819] | −0.0217 [−0.0229, −0.0205] | 6/6 |
| | 2.75 → 3 | +0.0029 [+0.0018, +0.0040] | +0.0822 [+0.0803, +0.0840] | −0.0225 [−0.0234, −0.0215] | 6/6 |
| | 3 → 3.25, boundary | +0.0214 [+0.0195, +0.0234] | +0.0772 [+0.0749, +0.0794] | −0.0001 [−0.0013, +0.0011] | 3/6 |
| | 3.25 → 3.5 | +0.0069 [+0.0057, +0.0082] | +0.0740 [+0.0723, +0.0756] | −0.0169 [−0.0181, −0.0157] | 6/6 |
| 768 at 3e-4 | 2 → 2.25, boundary | +0.0162 [+0.0147, +0.0176] | +0.0772 [+0.0760, +0.0784] | −0.0073 [−0.0087, −0.0060] | 6/6 |
| | 2.25 → 2.5 | +0.0046 [+0.0038, +0.0054] | +0.0770 [+0.0742, +0.0798] | −0.0213 [−0.0219, −0.0208] | 6/6 |
| | 2.5 → 2.75 | +0.0023 [+0.0009, +0.0037] | +0.0789 [+0.0775, +0.0804] | −0.0235 [−0.0249, −0.0221] | 6/6 |
| | 2.75 → 3 | +0.0022 [+0.0013, +0.0032] | +0.0809 [+0.0792, +0.0825] | −0.0232 [−0.0240, −0.0223] | 6/6 |
| | 3 → 3.25, boundary | +0.0198 [+0.0179, +0.0218] | +0.0764 [+0.0737, +0.0790] | −0.0020 [−0.0033, −0.0006] | 5/6 |
| | 3.25 → 3.5 | +0.0054 [+0.0043, +0.0065] | +0.0741 [+0.0728, +0.0754] | −0.0190 [−0.0202, −0.0179] | 6/6 |

The whole-set rise in the first quarter after a boundary exceeds the rise in the next quarter by +0.006 to +0.015.
Across the same pairs of intervals, the rise of T differs by +0.0002 to +0.0054 and the change of O by +0.008 to
+0.017; O's excess is the larger in all eight arm-boundary cases (`OUTPUT.txt`, end of section 2). The three changes
are p\* of different sets, so they do not add up.

**What this does not show.** It does not identify why the sequences outside the trained quarter keep their p\* after
a boundary. The make-up of O differs between intervals: after a boundary a quarter of O was trained in the preceding
quarter epoch, and inside an epoch a third of it was. That difference is not controlled here.

### 3. Exposure-matched contrasts: 512 at epoch 3 against 768 at epoch 2 + k/4

A sequence in quarters (a, b, c) of the orders of epochs 1 to 3 was trained at times a, 4 + b and 8 + c, counted in
quarter epochs. Three comparisons use the same pair of readouts:

- **Whole set.** All 16,384 sequences in both models. 768 has trained on k/4 of them a third time; 512 on all.
- **Last pass matched.** 768 on its sequences with c ≤ k and 512 on its sequences with c ≥ 5 − k. Both sets have had
  three passes and the same times since the third. The timing of passes 1 and 2 is not matched: 768's are 4 − k
  quarters more recent.
- **Every pass matched.** 768 on sequences with a, b, c ≤ k and 512 on sequences with a, b, c ≥ 5 − k. The times
  since each of the three passes are then the same in both models. The sets are different sequences in the two
  models, about 16,384 (k/4)³ each.

At k = 4 the comparison is the equal-updates one (S3 and S5), on the same sequences with identical exposure.

**Learning rate 1e-4:**

| 768 read at | Whole set | Last pass matched | Every pass matched | Sequences per draw | Whole set minus every pass |
|---|---|---|---|---|---|
| Epoch 2.25 | +0.0100 [+0.0071, +0.0129], 6/6 | −0.0216 [−0.0262, −0.0169], 0/6 | −0.0035 [−0.0258, +0.0189], 4/6 | 247 and 252 | +0.0135 [−0.0076, +0.0345], 5/6 |
| Epoch 2.5 | +0.0040 [+0.0010, +0.0070], 5/6 | −0.0156 [−0.0198, −0.0113], 0/6 | −0.0048 [−0.0121, +0.0026], 2/6 | 2,045 and 2,057 | +0.0088 [+0.0032, +0.0143], 6/6 |
| Epoch 2.75 | −0.0003 [−0.0032, +0.0025], 3/6 | −0.0093 [−0.0127, −0.0060], 0/6 | −0.0051 [−0.0109, +0.0008], 2/6 | 6,904 and 6,901 | +0.0047 [+0.0014, +0.0081], 6/6 |
| Epoch 3 (S3) | −0.0045 [−0.0079, −0.0011], 0/6 | the same sequences | the same sequences | 16,384 | — |

Training loss of 512 minus that of 768, on the same sets (nats per token):

| 768 read at | Whole set | Last pass matched | Every pass matched |
|---|---|---|---|
| Epoch 2.25 | −0.012 [−0.038, +0.014] | +0.073 [+0.051, +0.095] | +0.036 [−0.026, +0.097] |
| Epoch 2.5 | +0.044 [+0.018, +0.070] | +0.099 [+0.070, +0.127] | +0.076 [+0.045, +0.106] |
| Epoch 2.75 | +0.099 [+0.072, +0.126] | +0.125 [+0.099, +0.150] | +0.113 [+0.091, +0.136] |
| Epoch 3 | +0.154 [+0.129, +0.179] | | |

**Learning rate 3e-4:**

| 768 read at | Whole set | Last pass matched | Every pass matched | Whole set minus every pass |
|---|---|---|---|---|
| Epoch 2.25 | +0.0229 [+0.0199, +0.0259], 6/6 | −0.0092 [−0.0148, −0.0036], 0/6 | +0.0126 [−0.0099, +0.0351], 5/6 | +0.0103 [−0.0110, +0.0317], 5/6 |
| Epoch 2.5 | +0.0183 [+0.0155, +0.0212], 6/6 | −0.0008 [−0.0052, +0.0035], 2/6 | +0.0126 [+0.0049, +0.0204], 6/6 | +0.0057 [−0.0004, +0.0118], 4/6 |
| Epoch 2.75 | +0.0160 [+0.0137, +0.0184], 6/6 | +0.0076 [+0.0043, +0.0109], 6/6 | +0.0129 [+0.0072, +0.0187], 6/6 | +0.0031 [−0.0005, +0.0067], 5/6 |
| Epoch 3 (S5) | +0.0138 [+0.0112, +0.0165], 6/6 | the same sequences | the same sequences | — |

At 3e-4 the training-loss differences on the every-pass sets are −0.093, −0.057 and −0.022.

**Reading these tables.**

- *The whole-set contrast at 1e-4 moves with how much of the set 768 has trained on a third time.* It falls from
  +0.0100 to −0.0045 as that share goes from 1/4 to 4/4. P1's six readings take 768 at epochs 2.19 to 2.48, where
  the share is 19% to 48%.
- *On sequences with the same exposure, the contrast at 1e-4 is about −0.004 to −0.005 at each of the three readouts,
  and at equal updates it is −0.0045.* The three matched intervals include 0, so the sign is not determined. What the
  data do not show is a lead of 512 on matched sequences.
- *The whole-set contrast exceeds the matched one.* The difference is above 0 in 6/6 draws with 768 at 2.5 and at
  2.75. With 768 at 2.25 it is +0.0135 with an interval that includes 0.
- *Matching only the last pass is biased towards 768,* by −0.018, −0.011 and −0.004 against matching every pass at
  1e-4 (the last two intervals exclude 0). The reason is in the last block of `OUTPUT.txt` section 3: within one
  model at epoch 2.25, among sequences trained a third time in the same quarter, p\* is higher by +0.011 to +0.015
  (6/6 in every arm) when the second pass fell in the later half of epoch 2 rather than the earlier half. Earlier
  passes matter, so a comparison "at equal passes and recency" must match all of them.
- *At 3e-4 the lead of 512 is there on matched sequences* and is close to the equal-updates value, +0.0138.

### 4. Each width at its better rate

At epoch 3 the rate with the lower validation loss is 3e-4 for 512 and 1e-4 for 768. The table gives each quantity
at 1e-4 minus the same quantity at 3e-4, at epoch 3:

| Width | Training loss | Validation loss | p\* |
|---|---|---|---|
| 512 | +0.1343 [+0.1289, +0.1397], 6/6 | +0.0142 [+0.0059, +0.0225], 6/6 | −0.0164 [−0.0173, −0.0154], 0/6 |
| 768 | +0.0052 [−0.0020, +0.0123], 5/6 | −0.0212 [−0.0323, −0.0100], 0/6 | +0.0020 [−0.0013, +0.0052], 5/6 |

These are the figures of `RESULT.md` section 6c. At 1e-4, width 512 trains 0.134 nats behind its own 3e-4 arm, and
768's training loss hardly differs between the rates. The rates were not chosen on these draws: 3e-4 had the lowest
mean validation loss over eight widths on a tuning draw, and 1e-4 was 768's lowest of five rates on that draw
(N7 `PROTOCOL.md` section 3). Only two rates were run, so neither width's best rate is located.

512 at 3e-4 minus 768 at 1e-4:

| Comparison | Contrast | Note |
|---|---|---|
| Equal updates, epoch 3 | +0.01184 [+0.00789, +0.01578], 6/6 | Training losses differ by +0.020 [−0.006, +0.045] |
| Equal updates, every other readout | +0.0115 to +0.0251, 6/6 at each of the nine | From epoch 1 to 3.25 the training losses are within 0.02 nats on average |
| Equal training loss, the registered interpolation rule applied to this pair | +0.01235 [+0.00523, +0.01947], 5/6 | 768 read at epochs 2.78 to 3.08; m06 is −0.00094 |
| The same, with 768 read at the later end of each bracket | +0.00518 [−0.00714, +0.01751], 4/6 | m02 and m06 are read after epoch 3 |

N6's sealed secondary D3 is the same contrast at equal updates on N6's draws, and gave the same order: +0.0111
[+0.0072, +0.0150] (N6 `RESULT.md` section 4). Its caveat, stated in advance there, applies here too: the two arms
differ in rate, and the train–validation gap at epoch 3 is larger for 512 at 3e-4 (+0.568) than for 768 at 1e-4
(+0.532), so a quantity that only tracked the gap would give the same sign.

At equal updates the two arms have seen the same sequences at the same times, and from epoch 1 their training losses
nearly coincide. Of the comparisons available in N7, this is the one in which updates, exposure and training loss
are closest to matched together. It is not a comparison at one learning rate.

### 5. The equal-updates contrast at every readout

From `POINTS.csv`; the values are those of `RESULT.md` section 6a.

| Readout | 1e-4 | Side | 3e-4 | Side |
|---|---|---|---|---|
| Epoch 0.25 | +0.00516 [+0.00391, +0.00641], 6/6 | above 0 | +0.00872 [+0.00630, +0.01114], 6/6 | above 0 |
| Epoch 0.5 | +0.00551 [+0.00437, +0.00665], 6/6 | above 0 | +0.00772 [+0.00563, +0.00980], 6/6 | above 0 |
| Epoch 1 | +0.00522 [+0.00388, +0.00657], 6/6 | above 0 | +0.00705 [+0.00570, +0.00840], 6/6 | above 0 |
| Epoch 2 | +0.00095 [−0.00118, +0.00309], 5/6 | includes 0 | +0.00958 [+0.00729, +0.01187], 6/6 | above 0 |
| Epoch 2.25 | −0.00227 [−0.00513, +0.00059], 1/6 | includes 0 | +0.01038 [+0.00769, +0.01307], 6/6 | above 0 |
| Epoch 2.5 | −0.00334 [−0.00638, −0.00030], 1/6 | below 0 | +0.01143 [+0.00859, +0.01427], 6/6 | above 0 |
| Epoch 2.75 | −0.00371 [−0.00661, −0.00081], 0/6 | below 0 | +0.01317 [+0.01006, +0.01628], 6/6 | above 0 |
| Epoch 3 (S3, S5) | −0.00454 [−0.00795, −0.00114], 0/6 | below 0 | +0.01382 [+0.01116, +0.01648], 6/6 | above 0 |
| Epoch 3.25 | −0.00895 [−0.01306, −0.00485], 0/6 | below 0 | +0.01542 [+0.01142, +0.01942], 6/6 | above 0 |
| Epoch 3.5 | −0.00990 [−0.01450, −0.00529], 0/6 | below 0 | +0.01698 [+0.01271, +0.02125], 6/6 | above 0 |

So "768 is above 512 at equal updates at 1e-4" holds at epoch 3, the registered readout, and from epoch 2.5. In the
first epoch 512 is above 768 at both rates.

### 6. Where the matched readings fall, and validation loss

| Step | 768 read at epoch (m01 to m06) | Contrast with 768 at the later end of each bracket, per draw |
|---|---|---|
| P1, 1e-4 | 2.249, 2.390, 2.302, 2.189, 2.231, 2.476 | +0.01165, +0.00745, +0.00378, +0.01067, +0.00916, −0.00057 |
| S4, 3e-4 | 2.801, 2.951, 2.846, 2.732, 2.834, 3.083 | +0.01685, +0.01687, +0.01344, +0.01265, +0.01279, −0.01000 |

- P1's brackets are epochs 2 to 2.25 for m01, m04 and m05, and 2.25 to 2.5 for m02, m03 and m06.
- S4's brackets are 2.5 to 2.75 for m04, 2.75 to 3 for m01, m02, m03 and m05, and 3 to 3.25 for m06. Only m06 turns
  negative at the later end, and it is the draw that makes S4's later-end interval include 0
  (+0.01043 [−0.00027, +0.02113], as in the correction of 9 November). **Readouts of 768 at 3e-4 between epochs 3 and
  3.25 are the ones that bear on S4. Readouts between epochs 2 and 2.25 do not.**
- Mean validation loss rises from epoch 3 to epoch 3.25 in every arm and every draw (24 of 24): +0.0217
  [+0.0150, +0.0284] and +0.0315 [+0.0209, +0.0421] for 512 and 768 at 1e-4, and +0.0464 [+0.0333, +0.0595] and
  +0.0416 [+0.0318, +0.0515] at 3e-4. It falls again by epoch 3.5 but stays above its epoch-3 value in every arm
  mean. m06's S4 reading therefore sets 512 at its lowest validation readout against 768 just past its own. The
  registered check NOT_OVERFIT compares epochs 2 and 3 and is unaffected.

## Limitations

- **Post hoc.** The questions were chosen after the results were known, several versions of the comparison were
  looked at on 10 November before this one was written down, and no interval is adjusted for that.
- **Matched sets are different sequences.** In section 3 the two models are fitted on disjoint random subsets, so
  the matched contrasts carry sampling noise that the whole-set and equal-updates contrasts do not. At k = 1 the sets
  hold about 250 sequences and the interval, [−0.026, +0.019], contains both the equal-updates value and P1's.
- **Exposure matched is not loss matched.** At 1e-4 the every-pass sets differ in training loss by +0.04 to +0.11
  nats (512 higher). No pair of readouts in N7 at 1e-4 matches overall training loss, every pass and enough
  sequences at once. Whether 512 would lead at 1e-4 with both loss and exposure matched is therefore not determined
  by these data.
- **A model-based estimate is not reproduced here.** The 10 November check also moved every three-pass sequence to a
  common exposure profile with an additive regression on the timing of each pass, which gave +0.0003
  [−0.0095, +0.0102] with 768 at epoch 2.25. It assumes the passes do not interact, an assumption that was not
  tested, and it is left out of the script and of the claims.
- **Quarter-epoch resolution.** Exposure is known to the quarter epoch, and P1's readings are interpolated between
  quarter-epoch readouts.
- **Equal loss is not equal gain,** as the protocol already says; nothing here matches gains.
- **Two rates, one corpus family, six draws** sharing a validation set, a pre-training pool and a tokenizer. "Better
  rate" means the better of two.
- **Batch orders are regenerated, not read.** They pass the checks above, but the bundle holds no recorded hash of
  them to compare with.
- **No mechanism.** Nothing here says why p\* depends on recency, or why the untrained sequences behave differently
  after a boundary.
- **Checked by models only.**

## What this changes in the claims

It moves no label. In [`CURRENT_CLAIMS.md`](../../CURRENT_CLAIMS.md) terms:

| Claim | Before | Now |
|---|---|---|
| P1 (C4) | Confirmed: at 1e-4, 512 is above 768 when 768 is read at 512's epoch-3 training loss | **Still confirmed as registered.** It is a statement about whole-set p\* at equal overall training loss. Its reading as a property of the two widths at equal training progress is not supported: at the matched point 768 has trained on 19–48% of the set a third time, p\* depends on that, and on sequences with matched exposure no lead of 512 is seen (intervals include 0) |
| S3 (C4) | Confirmed: at 1e-4, 768 is above 512 at equal updates | **Still confirmed, at epoch 3.** The sign holds from epoch 2.5; at epochs 0.25 to 1, 512 is above 768 |
| S4 (C4) | Confirmed under the registered interpolation; includes 0 at the later bracket end | Unchanged. The readouts that bear on it are 768's between epochs 3 and 3.25 at 3e-4. On exposure-matched sequences the lead of 512 at 3e-4 is +0.013 |
| "The comparison axis reverses the order at 1e-4" (C4, C5) | Confirmed for one pair of widths at one rate | **Narrowed.** The two registered contrasts have opposite signs. The positive one is not shown to survive matching exposure. With each width at its better rate of the two there is no reversal: 512 is above 768 on both axes. The opposite signs appear only at 1e-4, where 512 trains 0.134 nats behind its own 3e-4 arm |
| Recommendation (C5) | State the alignment; report more than one | Also state exposure: how many passes each compared sequence has had, and how recently. Equal overall training loss inside an epoch does not equalise it |
| "Readouts inside epochs 2.0–2.25 would settle" S4 and the within-epoch point | Stated in `NATURAL_TEXT_STUDIES.md` | **Wrong.** See the [correction of 11 November](../natural-text-correction-20261111-01/CORRECTION.md) |
