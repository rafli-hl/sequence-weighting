# Reports

This folder holds the records of the natural-text studies, the synthetic follow-up, and the review, audit,
corrections and post-hoc analysis that came after them. Folders keep their original names and contents, because many of their paths and
hashes are cited elsewhere in the record. This page is a map of them; the narrative index is
[`NATURAL_TEXT_STUDIES.md`](../NATURAL_TEXT_STUDIES.md).

## How folders are named

Folder names follow the pattern `<study>-<kind>-<date>-<n>`. `<date>` is the day the folder was created (YYYYMMDD,
2026), and `<n>` numbers the folders of the same kind made that day.

| Study prefix | Study | Label in the review |
|---|---|---|
| `capacity-shift-followup` | Synthetic capacity-shift follow-up | S |
| `natural-text-ladder` | WikiText-2 width ladder with per-width learning rates | N1 |
| `natural-text-onerate` | WikiText-2 one-rate extension | N3 |
| `natural-text-lateturn` | WikiText-2 late-turn confirmation | N4 |
| `natural-text-fewepoch` | WikiText-103 few-epoch study (width survey) | N5 |
| `natural-text-peak` | WikiText-103 peak confirmation (exploratory study) | N6 |
| `natural-text-matched` | WikiText-103 matched-progress confirmation | N7 |

| Kind | What it holds |
|---|---|
| `seed-registry` | The registry drawn once for the study: the draw, its claim record, exclusions and policy |
| `analysis` | The sealed analysis output: per-readout `POINTS.csv`, per-fit `FITS.csv` and `ANALYSIS.json` |
| `result` | The results report, with its verification record |
| `failure` | The report of a failed run and its diagnosis |
| `owner-decisions` | A dated record of the owner's decisions and instructions |
| `assistant-recompute`, `assistant-posthoc` | Work by an AI assistant after a sealed result: a recomputation, or a post-hoc analysis. Never a sealed result |
| `correction` | A dated note that corrects earlier statements without editing the files that made them |

Protocols and sealed source code are not in this folder. For S, N1 and N3–N5 they are in `work/*-source-*/`; for N6
and N7 they are in [`preregistration/`](../preregistration/).

## By study

**S: synthetic capacity-shift follow-up**
- [`capacity-shift-followup-seed-registry-20261027-01`](capacity-shift-followup-seed-registry-20261027-01/): seeds
- [`capacity-shift-followup-analysis-20261027-01`](capacity-shift-followup-analysis-20261027-01/): sealed analysis
- [`capacity-shift-followup-result-20261028-01`](capacity-shift-followup-result-20261028-01/): report
  ([`REPORT.md`](capacity-shift-followup-result-20261028-01/REPORT.md)), with the proposal for the natural-text ladder

**N1: WikiText-2 width ladder**
- [`natural-text-ladder-seed-registry-20261028-01`](natural-text-ladder-seed-registry-20261028-01/): seeds
- [`natural-text-ladder-amendment-20261028-01`](natural-text-ladder-amendment-20261028-01/): protocol amendment
- [`natural-text-ladder-lr-selection-20261028-01`](natural-text-ladder-lr-selection-20261028-01/): per-width learning
  rates chosen on the tuning draw
- [`natural-text-ladder-run-b-failure-20261028-01`](natural-text-ladder-run-b-failure-20261028-01/): failed attempt of
  Run B
- [`natural-text-ladder-analysis-20261029-01`](natural-text-ladder-analysis-20261029-01/): report and sealed analysis
- [`natural-text-ladder-exploratory-20261029-01`](natural-text-ladder-exploratory-20261029-01/): exploratory note

**N3: WikiText-2 one-rate extension**
- [`natural-text-onerate-failure-20261030-01`](natural-text-onerate-failure-20261030-01/): failed first attempt
- [`natural-text-onerate-analysis-20261030-02`](natural-text-onerate-analysis-20261030-02/): sealed analysis
- [`natural-text-onerate-result-20261031-01`](natural-text-onerate-result-20261031-01/): result

**N4: WikiText-2 late-turn confirmation**
- [`natural-text-lateturn-seed-registry-20261031-01`](natural-text-lateturn-seed-registry-20261031-01/): seeds
- [`natural-text-lateturn-analysis-20261031-01`](natural-text-lateturn-analysis-20261031-01/): sealed analysis
- [`natural-text-lateturn-result-20261031-01`](natural-text-lateturn-result-20261031-01/): result

**N5: WikiText-103 few-epoch study**
- [`natural-text-fewepoch-seed-registry-20261101-01`](natural-text-fewepoch-seed-registry-20261101-01/): seeds
- [`natural-text-fewepoch-analysis-20261103-01`](natural-text-fewepoch-analysis-20261103-01/): sealed analysis
- [`natural-text-fewepoch-result-20261103-01`](natural-text-fewepoch-result-20261103-01/): result
- [`natural-text-fewepoch-descriptive-20261103-01`](natural-text-fewepoch-descriptive-20261103-01/): descriptive section

**N6: WikiText-103 peak confirmation.** Its registration and seeds are in
[`preregistration/natural-text-peak-confirmation-20261103/`](../preregistration/natural-text-peak-confirmation-20261103/README.md).
- [`natural-text-peak-analysis-20261103-01`](natural-text-peak-analysis-20261103-01/): sealed analysis
- [`natural-text-peak-result-20261103-01`](natural-text-peak-result-20261103-01/): result, with a note on the edits
  made to its public registration

**N7: WikiText-103 matched-progress confirmation.** Its registration and seeds are in
[`preregistration/natural-text-matched-confirmation-20261104/`](../preregistration/natural-text-matched-confirmation-20261104/README.md).
- [`natural-text-matched-run-checks-20261104-01`](natural-text-matched-run-checks-20261104-01/): verification of both
  runs, the input check and the analysis claim
- [`natural-text-matched-m1-result-20261105-01`](natural-text-matched-m1-result-20261105-01/): record of the first run
- [`natural-text-matched-analysis-approval-20261105-01`](natural-text-matched-analysis-approval-20261105-01/): the
  report-layout, input-check and verifier scripts named by hash in the result
- [`natural-text-matched-analysis-20261105-01`](natural-text-matched-analysis-20261105-01/): sealed analysis
- [`natural-text-matched-result-20261105-01`](natural-text-matched-result-20261105-01/): result
  ([`RESULT.md`](natural-text-matched-result-20261105-01/RESULT.md)) and its verification
- [`natural-text-matched-assistant-recompute-20261106-01`](natural-text-matched-assistant-recompute-20261106-01/):
  recomputation of the confirmed statistics from `POINTS.csv`
- [`natural-text-matched-assistant-posthoc-20261111-01`](natural-text-matched-assistant-posthoc-20261111-01/):
  post-hoc analysis by training exposure, from the v1.0 loss-array bundle and `POINTS.csv`: `REPORT.md`, the script
  `posthoc_exposure.py`, its exact output `OUTPUT.txt` and the per-draw values `RESULTS.json`. Descriptive, not
  registered, and not a sealed result

## Review, audit and corrections

| Folder | Contents |
|---|---|
| [`natural-text-evidence-chain-20261031-01`](natural-text-evidence-chain-20261031-01/) | Evidence chain of 31 October |
| [`natural-text-evidence-chain-20261104-01`](natural-text-evidence-chain-20261104-01/) | Evidence chain of 4 November, with the superseded-wording note |
| [`adversarial-review-20261104-01`](adversarial-review-20261104-01/) | Adversarial review of the claims, with its recomputation scripts |
| [`adversarial-review-response-20261104-01`](adversarial-review-response-20261104-01/) | Response to the review and the final claims (§5) |
| [`adversarial-review-response-note-20261106-01`](adversarial-review-response-note-20261106-01/) | Status of claims 4 and 5 after N7 |
| [`full-audit-20261108-01`](full-audit-20261108-01/) | Read-only audit of the whole record |
| [`natural-text-correction-20261109-01`](natural-text-correction-20261109-01/) | Correction issued after the audit |
| [`github-pr-snapshots-20261111-01`](github-pr-snapshots-20261111-01/) | Copies of the GitHub API responses for pull requests #1, #4, #5 (N7's registration) and #6 |
| [`natural-text-correction-20261111-01`](natural-text-correction-20261111-01/) | Correction after the post-hoc analysis by exposure and an independent review: which readouts would settle S4, how P1 should be read, and the wording changed in the root pages |
| [`follow-up-audit-20261112-01`](follow-up-audit-20261112-01/) | Follow-up audit of the studies before N7 and of alternative explanations: two auditors' reports, an independent re-check (`verify_findings.py`, `OUTPUT.txt`) and how each finding was handled |
| [`natural-text-correction-20261112-01`](natural-text-correction-20261112-01/) | Correction after the follow-up audit: the direction of the bias in N6's matched figures, a like-for-like S4 figure, and the rewording of C1–C4 |

## Owner decisions

The 36 folders named `natural-text-ladder-owner-decisions-<date>-<n>` are dated records of the owner's decisions,
from 28 October to 9 November 2026. Despite the prefix, they cover all the natural-text studies, not only N1. The
protocols and reports cite them by path. Three are worth reading on their own:

- [`natural-text-ladder-owner-decisions-20261104-01`](natural-text-ladder-owner-decisions-20261104-01/): acceptance of
  the response to the review, the search incident and its ruling, the closure of the experiments, and the correction
  of record for N1's failure report.
- [`natural-text-ladder-owner-decisions-20261106-01`](natural-text-ladder-owner-decisions-20261106-01/): the
  decisions that followed N7's result.
- [`natural-text-ladder-owner-decisions-20261109-01`](natural-text-ladder-owner-decisions-20261109-01/): the licence,
  the publication of N7's loss arrays, and the v1.0 release.

Some decision records cited by these files are not published; see [`PUBLICATION_NOTES.md`](../PUBLICATION_NOTES.md).
