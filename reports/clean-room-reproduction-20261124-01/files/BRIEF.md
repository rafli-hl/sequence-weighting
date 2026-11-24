# Clean-room reproduction of N7's analysis

You are reproducing a published statistical analysis **independently**. You implement it yourself from its written
specification and its released data, **without looking at the original code or the published results**. Only once
your results are frozen do you compare them with the published ones. The value of this exercise depends entirely on
that separation, so follow the access rules exactly.

The study is N7 of the research record `rafli-hl/sequence-weighting` (release v2.1), a preregistered comparison of
how two Transformer widths (512 and 768) distribute their loss reduction across weighted training sequences. You
reproduce its analysis, not its training.

## 1. Access rules

**Phase 1 (implementation).** You may read only these:

| Source | Where |
|---|---|
| N7's protocol | https://raw.githubusercontent.com/rafli-hl/sequence-weighting/v2.1/preregistration/natural-text-matched-confirmation-20261104/sealed-source/PROTOCOL.md |
| The estimator's definition | Jane Street's technical note: https://blog.janestreet.com/a-study-of-sequence-weighting-at-scale/sequence-weighting-note.pdf |
| N7's released data | the asset `n7-loss-arrays-v1.zip` of release v1.2: `gh release download v1.2 --repo rafli-hl/sequence-weighting --pattern n7-loss-arrays-v1.zip` (SHA-256 `cbe26760e2062a4cf03307d779226fa6efce8cfcfbf57b2e092bd818af80b8a9`), including its own README and `MANIFEST.json` |

**Do not:**
- clone the repository;
- open any other file of it;
- open any `.py` file anywhere in it;
- read any page, issue, release note or search result that reports N7's numbers.

That includes `README.md`, `METHODS.md`, `CURRENT_CLAIMS.md`, `RESULT.md`, `ANALYSIS.json`, `POINTS.csv`,
`MATCHED.csv` and `FITS.csv`. If you see a number from N7's results by accident, say so in the report.

**Phase 2 (comparison),** only after the freeze in section 3. You may then fetch these:
- `https://raw.githubusercontent.com/rafli-hl/sequence-weighting/v2.1/reports/natural-text-matched-analysis-20261105-01/POINTS.csv`
- `.../MATCHED.csv`, `.../FITS.csv` and `.../ANALYSIS.json` in the same folder.

You still may not read the original code. Discrepancies are investigated from the specification and the data.

**Generally:**
- Do not push, open issues or post anything. You deliver a report and your code.
- Do not invent numbers, citations or results.

## 2. What to implement

From the protocol and the technical note, implement:

1. **The estimator p\*.**
   - Signed per-sequence gains from each model's own E0, at each readout.
   - The cumulative-discrepancy objective over sequences sorted by weight, minimised over the protocol's range of p.
   - The protocol's rules for undefined fits, bounds and ties.
   - Use any correct numerical method, and state which.
2. **Per-readout quantities:** for each draw (m01–m06), width, learning rate and readout, compute p\*, the mean
   training and validation losses, and the gap.
3. **Every registered statistic,** in its registered sequence:
   - the matched contrasts (the reading rule along 768's path, including its rules for bracketing, ties and
     unavailable draws);
   - the fixed-update contrasts;
   - the t intervals, sign tests and leave-one-draw-out intervals;
   - the availability rules and the labels.
4. **The registered diagnostics,** where the protocol defines them.

Use Python with NumPy only. You may use SciPy for t quantiles; otherwise implement them and say how.

**Specification log.** Wherever the protocol is ambiguous or silent, write down the question, the reading you chose
and why, before you see any published number. This log is a main result of the exercise.

## 3. Freeze before comparing

When the implementation is complete:
1. write all your outputs (per-readout table, per-draw contrasts, statistics, labels) to files;
2. compute the SHA-256 of each output file and of your code;
3. record the hashes and the time in the report, with the specification log.

After the freeze, do not change the frozen code or outputs. Any later change goes into a separate, clearly labelled
second pass, with its reason.

## 4. Compare

Compare your frozen outputs with the published tables:
- **All 240 fits:** the largest absolute difference in p\*, and every fit that differs by more than 1e-6.
- **Matched readings in `MATCHED.csv`:** status, bracket, weight and value, per draw and statistic.
- **Each registered statistic:** mean, interval, sign test, leave-one-draw-out results and label.

Classify each discrepancy as one of:
- **numerical:** below 1e-6, from a different optimiser or summation order;
- **specification ambiguity:** your documented reading differs from the original's;
- **error in your implementation;**
- **possible error in the published analysis.**

For the last category, give a minimal reproduction from the released data. Do not resolve a discrepancy by adopting
the published number without understanding it.

## 5. Report

Deliver one Markdown report with these parts:
1. **Summary** (at most 10 lines): do the published numbers reproduce from the specification and the data alone?
   Name any possible error in the published analysis.
2. **Provenance:** what you read and when, the bundle hash you verified, your environment, the frozen hashes, and
   any accidental exposure to results.
3. **Specification log:** every ambiguity and your reading.
4. **Comparison:** tables for the fits, matched readings and statistics, with the largest differences.
5. **Discrepancies,** each classified, with evidence.
6. **Code:** your complete code and the commands to run it.
7. **Limits:** this is a reproduction by an AI system, not an independent human replication, and it reproduces the
   analysis, not the training.

Write in plain, precise English.
