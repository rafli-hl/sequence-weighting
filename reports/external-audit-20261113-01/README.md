# External audit, 13 November 2026

**Status: post hoc and AI-made.** The audit was written by an AI reviewer (OpenAI Codex, as the report itself says),
not by independent human reviewers, and it is not a training replication. It audited the public record at commit
`fee55ea1486dedba51ae6b51cc2e3ba8eaa51401` and the v1.2 release's `n7-loss-arrays-v1.zip`. All of its new
calculations are post hoc and descriptive. It changes no registered number or label.

## Contents

| File | What it is |
|---|---|
| [`AUDIT.md`](AUDIT.md) | The audit report, filed byte for byte as received (received as `sequence_weighting_audit_2026-11-13.md`; SHA-256 `9678f6ccca3676e23f5b4cc853f68f10c9d89344db1f686aba653cf137251c13`) |

The auditor's scripts (`audit_numeric.py`, `audit_record.py`, `rebuild_tokenizer.py`) are printed inside the report,
in its section 6, with their outputs. They were not run for this record. File-and-line references in the report point
to commit `fee55ea`, not to the current pages.

## How its findings were handled

The [23 November correction](../natural-text-correction-20261123-01/CORRECTION.md) handles each finding.

| Finding | Severity (the audit's) | Handling |
|---|---|---|
| F1: the later bracket end is not the least favourable reading | Major | Corrected. The 64-combination envelope is reproduced by N8's [`test_on_n7.py`](../../preregistration/natural-text-dense-replication-20261114/analysis/test_on_n7.py) |
| F2: C3's gap difference does not establish equal gaps | Major | Corrected: "similar gap", with a descriptive scale computed from N5's `POINTS.csv` |
| F3: "every pass is equally long ago" is too strong | Minor | Reworded to "matched recency windows", with the largest differences in mean age |
| F4: N6's width 384 missing from the study table; the claims page's training statement | Minor | Added; the training row now follows the README's five levels |
| F5, F6: fit-residual diagnostics and estimator edge-case fixtures | Suggestion | Not adopted in this update |
| The tokenizer rebuilt from public files with its pinned SHA-256 | Finding of the audit | Recorded as the audit's result; not rerun here |
| The familywise-error simulation cannot be checked from public files | Finding of the audit | Recorded |
