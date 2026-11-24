# Audit of version 2.1, 23–24 November 2026

**Status: post hoc and AI-made.** The audit was done by AI systems (Claude Fable 5.2), not by independent human
reviewers, and it is not a training replication. It audited the record at release v2.1, commit `30548db`.

**It is not fully independent.** Four fresh AI sessions, with no part in the earlier work, audited the correction of
23 November and the living pages, N8's registration package, N8's analysis code and the conduct of N8's runs. The
session that supervised them, ran the checks and merged their reports had itself prepared much of version 2.1. The
report says which findings concern that session's own work.

**Its result.** No registered number, label or N8 registration element was found to be wrong. It has two Major
findings and a list of documentation gaps.

## Contents

| Path | What it is |
|---|---|
| [`AUDIT.md`](AUDIT.md) | The report, byte for byte as written (as `sequence_weighting_audit_2026-11-24.md`; SHA-256 `d7c9b0cdce9579a607e74b0dfb82b7dbdb166b4f1372b1c9a23fff070bee575c`): summary, checks run, findings, the four auditors' reports as returned, and the source of every script |
| [`files/`](files/) | The owner's brief (`AUDIT_BRIEF.md`), each auditor's scripts and outputs (`a/`, `b/`, `c/`, `d/`) and the supervising session's outputs (`supervisor/`) |
| `.gitattributes` | Keeps every file here byte for byte |

**One redaction.** In [`files/supervisor/merge_commit.json`](files/supervisor/merge_commit.json), the saved GitHub
metadata of the registration's merge commit, the author's email address is replaced with `<REDACTED>`. Nothing else
in that file changed, and every other file here is as the audit left it. The address remains in the public commit
itself.

Paths inside the files are those of the machine the audit ran on. File-and-line references point to commit `30548db`,
not to the current pages.

## How its findings were handled

"24 November" means the changes recorded in [`PUBLICATION_NOTES.md`](../../PUBLICATION_NOTES.md) under that date.
"Open" means not handled yet: these wait for N8's loader and a dated amendment to its protocol, which must exist
before any N8 loss is read.

| Finding | Severity (the audit's) | Handling |
|---|---|---|
| C1: no registered entry point for N8's data | Major | **Open.** A loader, published and hashed with its tests, and a dated amendment |
| F-a1: `test_on_n7.py` gives 59 of 60 on public files | Major by the brief's definition | 24 November: a note in the N8 folder's README names the two version strings behind the pin. The registered test is not edited |
| B2, B3: a run with no terminal; when the study ends | Minor | **Open:** the amendment |
| D1: registration before R1 not checkable from public files | Minor | 24 November: the run records that hold no loss value are published, with each run's start time and zone |
| D2: the pause has no stated reason or criterion | Minor | 24 November for the reason: the pause statement now says "Paused at the owner's decision for reasons unrelated to the data; no N8 result has been computed or examined." It is the owner's statement, which public files cannot show. The criterion for resuming is **open** |
| D4: GPU-memory headroom overstated; start-up margin omitted | Minor | 24 November: `OPERATIONAL_NOTES.md` corrected; the paired readings are in the published gate records |
| A1, D6: revisions and first-publication dates not disclosed | Minor | 24 November: disclosed in `PUBLICATION_NOTES.md` |
| A2, A3, E5: the later bracket end and S4; the zero at k = 1 | Minor, Suggestion | 24 November: the [correction of 24 November](../natural-text-correction-20261124-01/CORRECTION.md) and the living pages |
| F-d1: `check_run.py` after a refused start | Minor | 24 November: stated in `OPERATIONAL_NOTES.md`. The check itself is **open** |
| C2: eight rule branches untested | Minor | **Open:** dated tests, with the loader |
| F-c1: the saturation rule is not N7's | Minor | **Open:** the amendment |
| B4, B5, B10, S1: the builder's sixth key; hunks citing the brief; "28 in all"; `write_hashes.py --check` | Minor, Suggestion | 24 November: the N8 folder's README |
| E1–E4, E6, E7: stale pages, lists without N8, a caption, time zones | Minor, Suggestion | 24 November: the living pages |
| D8: results not tied to a version of the check | Suggestion | 24 November: the check's SHA-256 is given with each result |
| D5, C4, C5, B9: matters for N8's result report | Suggestion | **Open,** for the result report |
| D7, F-d2, F-d3: the new check's readings; time caps; driver and Windows versions | Suggestion | 24 November for the caps (in the published `BENCHMARK.json` files and the notes). The rest is **open** |
| B8: three statements not checkable from public files | Suggestion | Unchanged |
| F-a2, F-d4: no third-party archive; the tag is lightweight | Suggestion | **Open:** the owner's action |
