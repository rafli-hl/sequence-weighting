# Audit brief: sequence-weighting record, version 2.1

You are an independent auditor of a published machine-learning research record. Work as a rigorous ML methods
reviewer, a statistician and a research software engineer. Find what is **wrong, unsupported, unclear, inconsistent
or unreproducible** in the record as it stands, and say what would fix each problem. You report; you do not edit.

**Repository:** https://github.com/rafli-hl/sequence-weighting (branch `main`, release `v2.1`, commit `30548db`).

## 1. What the record is

- **The question.** The record is a small-scale follow-up to Jane Street's
  [A study of sequence weighting at scale](https://blog.janestreet.com/a-study-of-sequence-weighting-at-scale/).
  When each training sequence carries a weight w in the loss, the fitted exponent p\* summarises how loss reduction
  is spread across weights. The record asks whether the order of two model widths in p\* depends on how they are
  aligned: at equal updates, or at equal training loss.
- **N1–N7** are completed studies. **N7** is the first study preregistered publicly before its runs. Its primary
  result is P1 = +0.0091 [+0.0040, +0.0142] at learning rate 1e-4 (label `REVERSAL_CONFIRMED`), with qualifications on
  exposure, interpolation and learning rate. The current position is in `CURRENT_CLAIMS.md`.
- **N8** is a dense-readout replication of N7.
  - **Design:** 24 fresh draws, widths 512 and 768 at 1e-4, readouts every 64 updates over epochs 2–3.5.
  - **Hypotheses:** two co-primaries, H1 (equal training loss, above 0) and H2 (equal updates, below 0).
  - **Registration:** publicly before any run, through PR #1, merged as the GitHub-signed commit `c6f98b2`, with
    the tag `n8-registration`.
  - **Folder:** `preregistration/natural-text-dense-replication-20261114/`.
  - **Status:** training is **paused** after 6 of 24 draws. No p\* of N8 has been computed, and N8's loss arrays are
    not published.
- **Corrections** are dated notes in `reports/`. Files whose hashes are cited elsewhere are never edited.

## 2. Rules

1. **Read-only.** Do not open pull requests or issues, push, or post anything. Deliver one Markdown report.
2. **Verify before you assert.** Every finding cites a file and line, a command and its output, or a quoted primary
   source. If you cannot check something, mark it **UNVERIFIED** and say what would verify it. Search the repository
   before calling anything missing.
3. **Respect the record.** Do not propose changing a registered hypothesis, rule, label or historical number. If you
   find an error, report it with a reproduction; the remedy is a dated correction.
4. **No new experiments.** You may run the published verification scripts, and write new **descriptive** analyses of
   published data, labelled **post hoc**. **Do not attempt to estimate any N8 result.** Its data is not published,
   and the protocol forbids interim looks.
5. **No fabrication.** Do not invent citations, numbers or results. Check every reference you give.
6. **Calibrate.** Do not call an inconclusive result evidence of no effect. Avoid "strong", "robust" and
   "significant" unless you define them.
7. **Don't re-raise what's already addressed** (section 5) unless you show the resolution is wrong or incomplete.

## 3. Run these checks

Use Python 3.12 if possible.

```bash
git -c core.autocrlf=false clone https://github.com/rafli-hl/sequence-weighting.git && cd sequence-weighting
git checkout v2.1
python tools/verify_publication.py
python outputs/sequence-weighting-pilot/core_checks.py
gh release download v1.2 --pattern n7-loss-arrays-v1.zip && unzip n7-loss-arrays-v1.zip
pip install numpy && python tools/verify_n7_losses.py n7-loss-arrays
pip install --index-url https://download.pytorch.org/whl/cpu torch==2.7.0
pip install -r tools/requirements-posthoc.txt && python tools/verify_posthoc.py n7-loss-arrays
```

For N8's registration folder:
- run its `write_hashes.py --check` or equivalent, and report whether `HASHES.json` matches;
- run N8's analysis tests against N7's published data, if they can run on public files (`test_on_n7.py`,
  `test_synthetic.py`);
- verify that the merge commit `c6f98b2` is GitHub-signed and predates every N8 run record mentioned in
  `OPERATIONAL_NOTES.md`.

Report each command's exact output. If something can't run on public files alone, say what it needs.

## 4. What to audit, in priority order

**A. The 23 November correction** (`reports/natural-text-correction-20261123-01/`). Check:
- F1, the bracket-envelope values: P1 +0.0000764, S1 −0.0000507, S4 −0.000268;
- F2, the gap-scale computation (`gap_scale.py`);
- F3, the recency-window wording and its maxima;
- F4, N6's width 384;
- whether every living page now agrees with the correction.

Note that `CORRECTION.md` was revised after its first commit, `c1a2380`, on the same day. Check whether
`PUBLICATION_NOTES.md` discloses that.

**B. The N8 registration package.**
- Does the protocol state its hypotheses, analysis, stopping rule, failure rules and power argument unambiguously?
  Look for gaps or internal contradictions. The protocol's title still says "draft", and one sentence predates the
  decision to register inside the reopened record; this is disclosed in the folder's README.
- `CHANGES.md` lists the differences from N7's sealed source. Spot-check that the sealed source differs from N7's
  only as listed, and that each change follows from the protocol.
- `HASHES.json`, the seed registry, the partition and the pilot log: are they internally consistent?
- The builder was changed after registration to record the merge and tag (`registration/`). Is that change exactly as
  disclosed, with no other effect?

**C. N8's analysis code** (`analysis/n8_analysis.py`). Does it implement the protocol exactly? Check:
- the reading rule, the t intervals and sign tests;
- the joint H1/H2 decision, availability and saturation rules;
- the 2^24 bracket envelope;
- the sensitivity analyses and S-a to S-d.

Do its tests reproduce N7's published numbers?

**D. Conduct of N8 so far** (`OPERATIONAL_NOTES.md` and the N8 README). Check each of these against the registered
protocol:
- the R1 parent-folder event;
- R2's failure and the retry X2;
- the GPU-memory precaution added to the owner commands;
- run order;
- the pause.

Is each event handled as the protocol prescribes, and disclosed fully? Is any event a protocol deviation that isn't
called one? Is anything published that would allow an interim look at N8 results?

**E. Living pages.** Check `README.md`, `CURRENT_CLAIMS.md`, `METHODS.md`, `NATURAL_TEXT_STUDIES.md`,
`DATA_AVAILABILITY.md`, `PUBLICATION_NOTES.md` and `CITATION.cff`:
- are N8's status and the version consistent across them?
- are any claims stale, numbers contradictory, links broken or captions overstated?

**F. Anything else material** that earlier audits missed, with evidence.

## 5. Already addressed (do not re-raise without new evidence)

- **The 13 November documentation revision:**
  - p\* is defined operationally, and the a + b·w^q example is given as conceptual only;
  - alignments are not described as equal progress;
  - the `REVERSAL_CONFIRMED` definition is explained, and the S3 and S4 sensitivities are shown;
  - exposure is treated as an alternative explanation;
  - clipping is described correctly;
  - the statistical caveats are stated, and what is interpolated is stated;
  - registration types are distinguished, and the reference study is credited;
  - five reproducibility levels are given.
- **The 13 November external audit's F1–F4,** handled by the 23 November correction. Its F5 and F6 are listed as not
  adopted.
- **Disclosed limitations:**
  - the scale (at most 34.7 M parameters) and the single recipe;
  - six draws in N7;
  - the familywise-rate simulation is unpublished;
  - reviews in the record were done by AI systems, with no independent human review or replication;
  - N8's results don't exist yet.

## 6. Report format

1. **Summary** (at most 10 lines): the most important findings, and whether any registered number, label or N8
   registration element appears to be wrong.
2. **Checks run:** a table of command, environment and exact result.
3. **Findings:** a table with these columns:

| ID | Area (A–F) | Severity | Finding | Evidence | Status | Fix type |
|---|---|---|---|---|---|---|

   - **Severity:**
     - Critical: a registered number, label or registration element is wrong.
     - Major: a claim is unsupported, a protocol deviation is undisclosed, or a check fails.
     - Minor: documentation.
     - Suggestion.
   - **Status:** VERIFIED, PLAUSIBLE or UNVERIFIED.
   - **Fix type:** doc-only, dated correction, post-hoc analysis, or a matter for N8's eventual result report.
4. **Rejected concerns:** what you checked and found sound.
5. **Before N8 resumes:** anything that should be settled before more draws are trained.
6. **New code:** every script you wrote, with its command and output, labelled post hoc.
7. **References:** verified only.

Write in plain, precise English. A short report of verified findings is better than a long one with guesses.
