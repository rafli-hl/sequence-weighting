# Audit: sequence-weighting record, version 2.1

**Date:** 23–24 November 2026. **Record audited:** `rafli-hl/sequence-weighting`, release `v2.1`, commit
`30548dbb789b2a117486fdf6f9ab9added680172`, and the v1.2 release asset `n7-loss-arrays-v1.zip`. Line numbers are at
that commit. `N8/` stands for `preregistration/natural-text-dense-replication-20261114/`.

**Who did it, and how independent it is.** All of it was done by AI systems (Claude Fable 5.2, Anthropic); it is not
human review and not a training replication.

- **The supervising session is not independent.** It prepared much of what the brief audits: the 23 November
  correction, `check_run.py`, the owner commands, `OPERATIONAL_NOTES.md`, the v2.1 edits to the living pages, and,
  earlier, N8's analysis code and source changes. Several findings below are errors in text or code it wrote (A1, A2,
  C1, C2, D4, D6, E1–E5, F-a1, F-d1).
- **Four fresh auditors** did the judgement work of the brief's section 4. Each was a separate session with no part
  in the earlier work, given the brief verbatim, its own clone at `v2.1` and no statement of what to expect. Their
  areas were A and E; B; C; D. Their reports are appendix 1, as returned.
- **The supervising session** ran the commands of the brief's section 3, re-read the lines each finding cites against
  its own clone, and merged the four reports. It dropped no finding. Where two auditors rated one thing differently,
  both ratings are given.
- **Public files only.** No file under the unpublished N8 run folders or the closed local record was opened for this
  audit, and no N8 result was estimated. Two facts from unpublished local records are quoted where they bear on a
  finding, and are marked as such (D1).
- **Read-only.** Nothing was pushed, opened or posted. GitHub was queried with GET requests. All five clones are
  unchanged (`git status --short`: 0 lines each).

## 1. Summary

1. **No registered number, label or N8 registration element was found to be wrong.** N7's published statistics, all
   240 fits, the 23 November correction's figures, N8's hashes, seed registry, partition and pilot figures reproduce.
2. **Major, C1: the registered N8 analysis has no entry point for N8's own data.** `n8_analysis.py` is a library on
   in-memory inputs. Nothing registered reads the run folders, decides which draws are complete, or picks the retry
   over the first attempt. N7's sealed analysis did. Settle this before any N8 loss is read.
3. **Major by the brief's definition (a check fails), F-a1:** `test_on_n7.py` gives 59 passed, 1 failed on public
   files with the documented install. It pins a file holding library version strings. No number is affected.
4. **The protocol is silent on three things:** a run that leaves no terminal (B2), when the study ends and the
   analysis runs (B3), and pauses (D2). N7's protocol had rules for the first two.
5. **That registration preceded R1 cannot be checked from public files (D1).** The merge commit is GitHub-signed, but
   R1 has a date only, the same local date as the merge.
6. **The 23 November correction's figures are right; two of its sentences are not.** Its general statement about the
   later bracket end is false for S4 (A2), and its revision after first publication is not disclosed (A1).
7. **The operational notes overstate what is known about GPU memory (D4),** and `check_run.py` would report two
   spurious failures after a refused start (F-d1).
8. **Living pages are stale about N8 (E1–E4):** one sentence still says the experiments "are closed again".
9. Nothing published allows an interim look at N8 results.

## 2. Checks run

Environments. **W:** Windows 11 (10.0.26300), Python 3.12.10, NumPy 2.5.3: the registered analysis environment.
**L:** Ubuntu 24.04.3 under WSL 2, Python 3.12.3, in a new virtual environment with NumPy 2.5.3 and PyTorch
2.7.0+cpu (CUDA not available to it). Git 2.45.1, GitHub CLI 2.87.3. Python ran with `-I -B` except where noted.

| Command | Environment | Exact result |
|---|---|---|
| `git -c core.autocrlf=false clone …`; `git checkout v2.1` | Git, Windows | `30548dbb789b2a117486fdf6f9ab9added680172`; 0 changed files |
| `python tools/verify_publication.py` | W | `manifest: 1429 rows; 1429 exact; 0 differ only in line endings; 0 mismatched; 0 missing; 0 published files not in the manifest` / `links: 567 local Markdown links checked; 0 known unavailable; 0 unexpected broken`; exit 0 |
| `python outputs/sequence-weighting-pilot/core_checks.py` | W, without `-I`, in a copy of the folder (it writes `CORE_CHECKS.json` beside itself) | `"status": "passed"`; exponents 0, 0.5, 1, 2 recovered as 0.0, 0.49999999999147443, 0.9999999999914743, 1.9999999999914744; quadratic-form error 4.912791094074942e-20; exit 0. With `-I` it stops at `ModuleNotFoundError: No module named 'core'`, because isolated mode leaves the script's folder off the path |
| `gh release download v1.2 --pattern n7-loss-arrays-v1.zip`; `unzip` | GitHub CLI, logged in | Exit 0. SHA-256 `cbe26760e2062a4cf03307d779226fa6efce8cfcfbf57b2e092bd818af80b8a9`, the README's pin; 68 files |
| `python tools/verify_n7_losses.py n7-loss-arrays` | W, and again in L | `bundle: 66 files match MANIFEST.json; 6 weight vectors match their runs' tensor hashes` / `fits: 240 refitted; largest \|p* - POINTS.csv\| = 2.90e-09; largest \|array mean - record\| = 8.55e-07` / P1, S1, S3, S4, S5 each `matches ANALYSIS.json` / `PASS`. Identical in both |
| `pip install --index-url https://download.pytorch.org/whl/cpu torch==2.7.0`; `pip install -r tools/requirements-posthoc.txt` | L | `3.12.3 numpy 2.5.3 torch 2.7.0+cpu cuda False` |
| `python tools/verify_posthoc.py n7-loss-arrays` | L | `ran with numpy 2.5.3, torch 2.7.0+cpu` / `keys: 268 published, 268 reproduced; 0 missing, 0 extra` / `largest difference: 0.00e+00` / `PASS` |
| `python N8/tools/write_hashes.py --check` | W | **Cannot run on public files.** `FileNotFoundError: … DRAW_COMMAND.txt`; exit 1 (S1) |
| Equivalent: `hashes_equivalent.py` (post hoc, appendix 2) | W | `38 named files match; 1 differ; 83 not published`. The one that differs is `tools/build_n8_activation.py` (published `c31fd4aa…`, `HASHES.json` `30765693…`), as `HASHES.json`'s own note says. Not published: `DRAW_COMMAND.txt`, `tests-retired/test_draw_command.py`, and 81 files of `inputs/`. `31 sealed files, 0 differ from SOURCE_SUBJECT.json`; subject `9bdea3a9…bb6b` |
| The 81 `inputs/` hashes against public material | W | `public bundle (v1.2 asset): 68 of 68 files equal the hashes HASHES.json names`. `orders regenerated here (torch 2.7.0+cpu, WSL): 12 of 13 files equal the hashes HASHES.json names; differing: ['inputs/n7-orders-v1/ORDERS.json']` |
| `python N8/analysis/regenerate_n7_orders.py n7-loss-arrays orders` | L | `torch 2.7.0+cpu: wrote 12 order files to orders`; exit 0 |
| `python N8/analysis/test_on_n7.py <repo> n7-loss-arrays orders` | W (registered environment) | **`59 passed, 1 failed`; exit 1.** `FAIL  regenerated orders (PyTorch 2.7.0+cpu): ORDERS.json pinned, files, per-epoch order_sha256, each row a permutation  [536bb5d050b9642f, 0 mismatches]` (F-a1). All other checks pass, among them the three envelope minima (+0.0000764, −0.0000507, −0.0002679), `240 refits of p* against POINTS.csv (1e-9)  [240 fits; largest \|p* difference\| 0]`, and S-b's balance (14.11545, 8.44744, 6.99420 updates; 0.00000, 0.03709, 0.03659) |
| The same | L (cross-check) | `59 passed, 1 failed`; the same one check. `largest \|p* difference\| 8.77e-10`, as the protocol's section 6 says of WSL |
| `python N8/analysis/test_synthetic.py` | W, and in L | `37 passed, 0 failed`; exit 0 (SciPy absent, so its one optional comparison is skipped) |
| `gh api repos/rafli-hl/sequence-weighting/commits/c6f98b2…` | GitHub API | `"verified":true`, `"reason":"valid"`, committer `GitHub <noreply@github.com>`, date `2026-11-14T18:19:19Z`, `verified_at 2026-11-14T18:19:20Z`, parents `fee55ea…` and `aaafa2e…`. Locally `git log --format=%G?` gives `E` (no key to check with) |
| `gh api …/git/refs/tags/n8-registration`; `…/pulls/1` | GitHub API | The tag is lightweight and points at `c6f98b2…`. PR #1: `merged: true`, `merged_at 2026-11-14T18:19:20Z`, `merge_commit_sha c6f98b2…` |
| `gh api …/releases` | GitHub API | `v2.1` published `2026-11-23T05:10:47Z` on `30548db`, no assets; `v2.0` `2026-11-14T18:45:38Z`, no assets; `v1.2` with `n7-loss-arrays-v1.zip` |

**Does the merge predate every N8 run record in `OPERATIONAL_NOTES.md`?** Signed: yes. Predates: not verifiable from
public files for R1 (finding D1). R2 (15 November, clock times 15:38–16:09) and X2 (16 November) fall after the merge
(15 November 01:19 at +07:00) under either reading of the time zone.

## 3. Findings

Critical: none. IDs keep each auditor's own numbering; "also" names the same finding in another auditor's report.
S1 is the supervising session's.

| ID | Area (A–F) | Severity | Finding | Evidence | Status | Fix type |
|---|---|---|---|---|---|---|
| C1 (also B1, D3) | C, B | **Major** (auditors B and C; auditor D rated its part Minor) | **The registered analysis has no entry point for N8's data.** `n8_analysis.py` takes in-memory `data` and `orders`. Nothing registered reads a run folder, decides which draws are completed or failed, chooses between a first attempt and its retry, checks arrays and orders against their recorded hashes, refuses to fit before the runs have ended, or writes outputs. N7's sealed analysis did each of these; `CHANGES.md` drops that file without replacing these parts. So the step from run folders to analysis inputs will be fixed by code written after registration, with six draws' data in existence. A concrete hazard: R2's n06 folder still holds a first-attempt `w768/E0.f32` that differs from X2's. No registered rule or number is wrong. With every draw COMPLETE under a terminal, any reasonable loader gives the same inputs; the risk is in edge cases. | `N8/analysis/n8_analysis.py:16–19` ("Inputs. data[d] is None for a failed draw, or dict(weights=[...], arms=…"), `:562` `def analyse(per, data, plan=PLAN, orders=None)`; no `__main__` and no file access in the file. N7: `…/sealed-source/matched_analysis.py:61` `def load(runs, pins=mw.PINS, …)`, `:413` `if __name__ == '__main__':`. `N8/CHANGES.md:37` "**Dropped** `matched_analysis.py` …: N7's analysis; N8's is `analysis/n8_analysis.py` (§6)". `N8/README.md:3`. `N8/OPERATIONAL_NOTES.md:63`, `:74`. Auditor C's `c05`: three draws passed as `None` with nothing saying they failed give `COMPLETE_WITH_FAILED_DRAWS` and labels; a failed draw omitted from the mapping makes `analyse()` raise `KeyError` | VERIFIED | Dated note, and a loader published with its SHA-256 and tests, before any N8 loss is read. The sealed file is not edited |
| F-a1 (also C3) | F, C | **Major by the brief's definition** (a check fails); no number is affected | **`test_on_n7.py` cannot reach 60 of 60 for a reader who follows the published instructions.** Its check at line 107 requires the SHA-256 of `ORDERS.json` to equal a pin. `regenerate_n7_orders.py` writes `torch.__version__` and `np.__version__` into that file. The pin is reproduced byte for byte only with `2.7.0+cu126` and `2.2.6`. With the documented CPU build and NumPy 2.5.3 the 12 order files are identical to those `HASHES.json` names, and the check still fails. The protocol's "60/60 on N7 … in both the registered environment and WSL" (section 10) therefore holds only with the registrant's version strings. | Section 2: `59 passed, 1 failed` in both environments, with real PyTorch 2.7.0+cpu. Supervisor: of 112 pairs of version strings tried, only `('2.7.0+cu126', '2.2.6')` reproduces `8ba4a3c2…`. Auditor A reached the same with orders from its own MT19937 code, without PyTorch (`a3c_orders_json.py`); with the pinned strings its run gives `60 passed, 0 failed`. `N8/analysis/regenerate_n7_orders.py:32`; `N8/analysis/test_on_n7.py:32`, `:107` | VERIFIED | Dated note naming the two strings, or publishing `inputs/n7-orders-v1/`. The registered test is not edited |
| B2 (also D9) | B, D | Minor (protocol gap; has not occurred) | **The failure rules do not cover a run that leaves no terminal.** A retry is admitted "only on its first run's terminal record", and the builder enforces it. The worker writes `TERMINAL.json` only from its `finally` block, so a killed process or a machine crash leaves none. The activation is then consumed and no retry can be built; `RUN_COMMAND.ps1` then stops every later run. The protocol does not say whether such a run's draws are failed, or whether a COMPLETE receipt without a terminal counts. N7's protocol had the rule. | `N8/N8-protocol-draft.md:178–182`; 0 matches for "no terminal" in it. `N8/tools/build_n8_activation.py:96`; `N8/source/matched_worker.py:362–374`; `N8/source/MATCHED_OWNER_RUN.ps1:55`. N7 `sealed-source/PROTOCOL.md:220` "**A run that leaves no terminal,** because WSL died or the machine crashed, counts for nothing, whatever receipts are on disk." Auditor D's `d05`: `STOPS … R2 EXIT_UNOBSERVED_NO_KILL, no X2` | VERIFIED | Dated note before R3 |
| B3 (also F-a3) | B | Minor (protocol gap) | **The stopping rule does not say when the study ends or when the one analysis runs.** "No look at any p\* before all 24 draws are complete" cannot be met literally once a draw has failed twice. A draw never attempted is not a failed draw, so stopping by choice at 20–23 draws is not a registered outcome, although the status rule would label it `COMPLETE_WITH_FAILED_DRAWS`. Nothing says when a study that is not resumed is closed as INCOMPLETE. This does not inflate the false-positive rate. | `N8/N8-protocol-draft.md:176`, `:103–106`, `:182`; `N8/README.md:9–10`. N7 `sealed-source/PROTOCOL.md:205` | VERIFIED | Dated note before R3 |
| D1 (also F-b1) | D | Minor | **That registration preceded R1 cannot be checked from public files.** The notes give R1 a date and no time, and that date is also the local date of the merge. The sealed design ties every run to the merge commit (the registered builder refuses; the recorded one writes the registration into each approval record, which each terminal binds), but those run records are unpublished. *From unpublished local records, read by the supervising session on 16 November and not public:* R1's pre-start GPU check began at 2026-11-14T19:00:20Z, 41 minutes after the merge. | `N8/OPERATIONAL_NOTES.md:49`, `:62` (no zone). `gh api …/pulls/1`: `merged_at 2026-11-14T18:19:20Z` = 15 November 01:19:20 at +07:00. `git diff c6f98b2 88ac496 -- N8/tools/build_n8_activation.py`: `PUBLIC_REGISTRATION = None` becomes the recorded value. Auditor D's `d01`: the three terminal hashes in the notes appear nowhere else in the repository, except R2's in `X2_COMMAND.txt` | VERIFIED (the gap). The order: PLAUSIBLE on public files | Doc-only: publish, for R1, R2 and X2, the records that hold no loss value (`TERMINAL.json`, stage receipts, `APPROVAL_RECORD.json`, `AUTHORIZATION.json`, `OWNER_EXIT_RECEIPT.json`, the gate records), and each run's start and end time with its zone |
| D2 | D | Minor | **The pause is disclosed without a reason and without a criterion for resuming.** The protocol is silent on pauses, so no stated rule is broken. But six draws' losses now sit unanalysed for an open period. "No p\* has been computed or examined" cannot be verified from files. | `N8/OPERATIONAL_NOTES.md:82–85`; `N8/README.md:5–10`; `PUBLICATION_NOTES.md:52–59`. 0 matches for "pause", "interrupt", "resum" in the protocol | VERIFIED (the omission) | Doc-only: a dated note with the reason, who decides to resume and on what, and that the decision uses no N8 data. Publishing the SHA-256 of every loss-bearing file of n01–n06 would fix the paused data |
| D4 (also B7, F-b2) | D | Minor | **The notes' account of GPU-memory headroom is not supported by the public numbers, and omits the tighter limit at start-up.** (a) The guard's peak reading is the same to the byte, 2,386,349,260, in the pilot and in all six completed draws, on four days, while the Windows readings in the same notes range over more than 100 MiB. In the pilot it exceeds the worker's reserved memory by the same 863,816,908 bytes at both widths. So "about that much more GPU memory in use during a draw, by anything, can stop the run" is not shown: what the reading tracks is not established. (b) The start-up benchmark gates the same reading at 2.25 GiB, 28.2 MiB above the pilot's peak. A start-up stop uses up the run, leaving the retry as the only attempt for three draws. (c) The protocol's section 7 reports the worker's own 1.42 GiB, not the figure the guard acts on. | `N8/pilot/PILOT_LOG.json`: 512 `cuda_reserved` 891289600, `device_used_sampled` 1755106508; 768 1522532352 and 2386349260; `fit_limit_bytes` 2415919104. 2,415,919,104 − 2,386,349,260 = 29,569,844. `N8/OPERATIONAL_NOTES.md:37`, `:57–59`, `:62`, `:71–72`. `N8/source/fewepoch_plan.py:77–78`; `N8/source/matched_worker.py:154–159`. `N8/N8-protocol-draft.md:170` | Numbers VERIFIED; what the reading measures UNVERIFIED | Doc-only: correct the two sentences and state the start-up margin. To settle what the reading measures, publish the paired readings the gate records hold (`wsl_device_used_bytes` beside the Windows `max_memory_used_mib`); they hold no loss value |
| A1 (also D6b) | A | Minor | **`CORRECTION.md` of 23 November was revised in place after its first public commit, and this is not disclosed.** `c1a2380` was pushed on its own (the `verify` workflow ran on it at 05:05:18Z). `30548db`, four minutes later, rewrote §3's "What changes" sentence and the closing list of pages. No number changed. `PUBLICATION_NOTES.md` names `c1a2380` nowhere. The same step changed `OPERATIONAL_NOTES.md` (from "`check_run.py X2` … had not been run" to its result) and the N8 README. The record's precedent is to disclose: the 9 November correction carries an "Amended" line. | `git log --stat -- reports/natural-text-correction-20261123-01/`; `grep -c c1a2380 PUBLICATION_NOTES.md` → 0; `reports/natural-text-correction-20261109-01/CORRECTION.md:5–6`; `git diff c1a2380 30548db -- N8/OPERATIONAL_NOTES.md` | VERIFIED | Doc-only: a dated line in `PUBLICATION_NOTES.md` |
| A2 | A | Minor | **The correction's general sentence is false for S4.** "Reading every draw at its later end gives the smallest mean contrast, but not the smallest lower t limit" (`CORRECTION.md`); "The later bracket end gives the lowest mean, not the lowest interval" (`README.md`); `METHODS.md` sets −0.000268 for S4 "against … −0.00027 with every draw at the later end". For S4 the all-later-end reading *is* the minimum over the 64 combinations: the two figures are one number at two precisions. The sentence holds for P1 and S1 only. The three envelope values themselves are correct. | `reports/natural-text-correction-20261123-01/CORRECTION.md:27–29`; `README.md:82`; `METHODS.md:222–224`. Auditor A's `a1_envelope.py`: S4 `-0.0002679 … at LLLLLL`; auditor C's `c04`: `ends at min lower [1, 1, 1, 1, 1, 1]` | VERIFIED | Doc-only |
| D6 (also B6) | D, E | Minor | **Entry dates are event dates, not publication dates.** The README note dated 15 November on the two folders is absent from v2.0 and first public on 23 November; `PUBLICATION_NOTES.md` says the README "keeps" it. R2's failure of 15 November was first public eight days later. The protocol's own requirement, recorded "before the analysis runs", is met. | `git show v2.0:N8/README.md \| grep -c "two empty folders"` → 0; `PUBLICATION_NOTES.md:68`; `N8/N8-protocol-draft.md:183–184` | VERIFIED | Doc-only |
| F-d1 | F, D | Minor | **`check_run.py`, as published, reports two extra failures for a sound run whose start the sealed owner script refused once.** The sealed script records a refused start as `PRESTART-REFUSED-<k>.json`, and the worker copies it into the run folder. The check expects the gate folders to hold `PRESTART.json` and the draws' records only. | `N8/source/MATCHED_OWNER_RUN.ps1:70–75`; `N8/source/text_worker.py:404`; `N8/source/matched_worker.py:318`; `N8/check_run.py:204–206`, `:311–312`. Auditor D, on a dummy run in its scratch folder: `52 passed, 3 failed … 2 other failure(s): report them` | VERIFIED on dummy data | Doc-only: revise the check (not a registered file) with a dated note |
| C2 | C | Minor | **Eight rule branches of the analysis are exercised by no registered test:** the 1e-9 margin; a saturated bracket fit making a draw unavailable for H1; H1's value at bound 32; the 1e-3 flag of records against arrays; NOT_OVERFIT's other two labels; S-d leaving out saturated fits; an undefined refit in the starting offset; the 7.999 threshold. No registered test runs `analyse()` from arrays on N8's own grid. On auditor C's constructed inputs the code is right in each case: this is a gap in the tests. | Auditor C's `c06`: eight one-line mutants leave all 30 checks of `test_synthetic.py`'s first five functions passing; three control mutants are caught. On N7 these branches never arise (largest p\* 0.1489) | VERIFIED | Doc-only: new dated test files beside the sealed ones |
| F-c1 | F, B | Minor | **The saturation rule is not N7's, though the protocol calls it "carried over from N7" and "as in N7".** In N7 an unresolved refit made the whole statistic SATURATED, and a side that differed at bound 32 made it SATURATION_SENSITIVE. In N8 an unresolved refit removes only that draw, and a resolved refit can never change a label. The code follows N8's text. | `N8/N8-protocol-draft.md:91–95`; N7 `sealed-source/PROTOCOL.md:128` | VERIFIED | Doc-only: a dated note |
| B4 | B | Minor | **The recorded builder differs from the registered one in exactly two lines, as disclosed, but they carry two undisclosed things:** a sixth key, `pr_record_sha256`, naming an unpublished file, and comments citing the unpublished `registration/apply_registration.py`. Neither changes behaviour. | `git diff n8-registration v2.1 -- N8/tools/build_n8_activation.py`; `:30–31`; `git grep pr_record` → that file only | VERIFIED | Doc-only |
| B5 | B | Minor | **Some hunks of `CHANGES.md` are justified by unpublished documents,** though the protocol says each change is "justified by a section of this protocol": hunks 29 and 55 cite only the owner's brief; 50, 58 and 60 cite nothing. All are paths, names and messages; none touches the model, optimiser, loss, weights, batch order or evaluation. | `N8/N8-protocol-draft.md:197–198`; `N8/CHANGES.md:3`, `:523`, `:936` | VERIFIED | Doc-only |
| E1 | E | Minor | **Stale status.** `NATURAL_TEXT_STUDIES.md:149`: "The experiments were reopened for N7 alone and are closed again." The same page, lines 187–197, says N8 is paused after 6 of 24 draws. | The lines cited | VERIFIED | Doc-only |
| E2 | E | Minor | **Stale page headers.** `CURRENT_CLAIMS.md:3` says "As of 12 November 2026; wording revised 13 November 2026, with no claim, number or label changed", but C3's wording, three numbers in C4's table and the training row changed on 23 November. `NATURAL_TEXT_STUDIES.md:1` is titled "27 October – 11 November 2026". | The lines cited | VERIFIED | Doc-only |
| E3 | E | Minor | **`DATA_AVAILABILITY.md` has not changed since 13 November and does not mention N8.** It lists "the public registrations of N6 and N7" and "the audits of 8 and 12 November 2026, and the corrections of 9, 11 and 12 November 2026". It does not list N8's run folders, loss arrays, saved orders or kept E0 states as unpublished. | `grep -c N8 DATA_AVAILABILITY.md` → 0; `:9–14` | VERIFIED | Doc-only |
| E4 | E | Minor | **Other lists of registrations omit N8.** `README.md:276` "Only N7 was publicly preregistered"; `README.md:303`; `METHODS.md:4`, `:23`; `NATURAL_TEXT_STUDIES.md:27`. The study tables in `METHODS.md` and `NATURAL_TEXT_STUDIES.md` have no N8 row. | The lines cited | VERIFIED | Doc-only |
| E5 | E | Minor | **`README.md:272`, "S4's sign depends on this", is wrong.** S4's mean is above 0 in all 64 combinations (lowest +0.01043). What depends on the bracket end is whether its interval excludes 0; after F1 that is also true of S1. | Auditor A's `a1_envelope.py` | VERIFIED | Doc-only |
| E6 | E | Minor | **Overstated caption.** `METHODS.md:362`: "Figure 6. Every estimate of the 512 − 768 contrast." The figure has 15 rows and omits estimates quoted on the living pages, among them S1 at the later end and the envelope minima. | `docs/make_readme_figures.py:170–190` | VERIFIED | Doc-only |
| S1 | B | Minor | **`write_hashes.py --check` cannot run on the published folder.** It hashes `DRAW_COMMAND.txt`, which is not published, and stops there. The README's own verification snippet covers six files. An equivalent over the published files finds only the disclosed difference. | Section 2 | VERIFIED | Doc-only: say so in the N8 README, or publish a check that skips unpublished files |
| A3 | A | Suggestion | F3's "0.000" at k = 1 is zero by construction: with one quarter per pass there is one joint cell. The audit's figure at k = 1 was a marginal KS distance of 0.11920, which reproduces and which the correction leaves out. N8's S-b will show the same. | `CORRECTION.md:84`; `METHODS.md:181–182`; `a3_recency.py`, `a3d_ks.py` | VERIFIED | Doc-only; and N8's result report |
| D5 (also B9c) | D | Suggestion | The retry's E0 comparison is reported only as SAME, DIFFERENT or ABSENT; the protocol says it "reports how each width's new E0 losses compare". The size of n06's w768 difference is deferred. | `N8/N8-protocol-draft.md:181`; `N8/source/matched_worker.py:288–296`; `N8/OPERATIONAL_NOTES.md:73–76` | VERIFIED | N8's result report |
| C4 | C | Suggestion | A hypothesis labelled UNAVAILABLE still gets per-draw values, a sign test and leave-one-draw-out intervals with a side. The protocol does not say what is then shown. | `N8/analysis/n8_analysis.py:395–396`; `c03` item 5 | VERIFIED | N8's result report; a dated note in advance |
| C5 | C | Suggestion | If a flat interval holds the target and its *later* fit is undefined, the code makes the draw unavailable, although the protocol reads a flat interval at its earlier readout. Copied from N7; very unlikely to arise. | `N8/analysis/n8_analysis.py:309`; `c03` item 3 | VERIFIED | N8's result report, if it arises |
| B9 | B | Suggestion | For the result report: give both component labels beside REVERSAL_NOT_REPLICATED; "no multiplicity correction is needed" holds for the joint claim only, and the chance that at least one hypothesis is confirmed in error can reach 5%. | `N8/N8-protocol-draft.md:84–90`, `:31–32`; `b2_power.py` (0.0249 at the boundary) | VERIFIED | N8's result report |
| B8 | B | Suggestion | Three statements cannot be checked from public files: that the partition is the sealed rule's output (the corpus manifest is unpublished); how the pilot's source differed (only hashes of its four changed files are public); the bound record `LR_SELECTION.json`. | `N8/README.md:25`; `N8/source/SOURCE_SUBJECT.json:6` | UNVERIFIED | Doc-only |
| D7 | D | Suggestion | The new GPU-memory check stops earlier than the sealed one and writes nothing, so a start it refuses leaves no record; the notes do not give its readings for X2. | `N8/X2_COMMAND.txt:55–72`; `N8/source/MATCHED_OWNER_RUN.ps1:70–75` | VERIFIED | Doc-only |
| D8 | D | Suggestion | The completeness results are not tied to a version of the check, and the commands of R1 and R2 are unpublished. The counts agree with the published version (55, 47, 32 checks). | `N8/OPERATIONAL_NOTES.md:53`, `:64`, `:78`; `N8/README.md:82`; `d03` | VERIFIED | Doc-only |
| F-a2 | F | Suggestion | N8's registration has no third-party archive: Software Heritage has neither the repository nor `c6f98b2` (HTTP 404, re-checked), and all tags are lightweight. GitHub's signature is the only independent evidence of its time. N6 and N7 cite archives. | `NATURAL_TEXT_STUDIES.md:31–51`; Software Heritage API | VERIFIED | Owner action, then doc-only |
| F-d2 | F | Suggestion | The margin under the per-draw time cap is not reported (R2's draws took 2,792 and 2,816 s; the pilot's cap was 3,097 s), and R2's owner-to-worker clock ratio, 1.036, is outside the 1.06–1.11 the protocol quotes. | `N8/OPERATIONAL_NOTES.md:51`, `:56`, `:70`; `N8/N8-protocol-draft.md:162`, `:166–168` | Arithmetic VERIFIED; the runs' caps UNVERIFIED | Doc-only |
| F-d3 | F | Suggestion | A pause can change the NVIDIA driver or the Windows build, which the sealed code neither refuses nor records. Contrasts are within a draw, so this would not favour a width. | `N8/source/text_framework_setup.py:15`, `:21`, `:28` | VERIFIED | Doc-only: record them per run |
| E7 | E | Suggestion | Dates mix UTC and local time without saying so: the merge (15 November 01:19 at +07:00) is dated "14 November", and the v2.0 release 26 minutes later "15 November". | `README.md:11`; `PUBLICATION_NOTES.md:78`, `:99` | VERIFIED | Doc-only |
| B10 | B | Suggestion | The N8 README counts "28 in all" readouts while listing 29 items; the 28 excludes E0. | `N8/README.md:52` | VERIFIED | Doc-only |
| F-d4 | F | Suggestion | The tag `n8-registration` is lightweight and carries no time of its own. | `git cat-file -t refs/tags/n8-registration` → `commit` | VERIFIED | Doc-only |

## 4. Rejected concerns: checked and found sound

**The 23 November correction.**
- **F1:** the three minima reproduce in three independent implementations (auditors A and C, and `test_on_n7.py`).
  P1's lower limit is above 0 in all 64 combinations, S1's is at or below 0 in exactly 1, S4's in 5. The concavity
  argument is right for both limits.
- **F2:** `gap_scale.py` runs and reproduces `GAP_SCALE.txt` byte for byte; auditor A's own computation agrees.
- **F3:** the maxima reproduce, with real PyTorch orders (section 2) and with auditor A's PyTorch-free orders.
- **F4:** N6's `POINTS.csv` and protocol have width 384 at 3e-4 only.
- No living page still says "the same gap", "for the timing" or "equally long ago".

**The registration package.**
- `CHANGES.md` is exactly the real difference from N7's sealed source: applying its 61 hunks to N7's files reproduces
  N8's byte for byte.
- The seed registry re-derives from its draw and exclusions. The partition has 24 disjoint groups of 16,384 and
  shares nothing with N7's.
- Every pilot figure in the protocol's section 7 matches the pilot log. The power table reproduces.
- The builder change is exactly two lines. No other registered file changed after the merge.

**The analysis code.**
- The estimator is a text-identical copy of N7's. All 240 N7 fits are bit-identical in the registered environment.
- The reading rule, t interval, 1e-9 margin, sign test, minimum of 20, labels, joint label and study status are
  implemented as section 6 states them.
- The 2^24 envelope is exact, and equals a direct enumeration.
- The tests' expected values come from independent sources, not from the code's own output.

**Conduct.**
- The retry was admitted, built and run as section 8 and the sealed code prescribe. It is a fresh run with the same
  seeds, not a continuation.
- The GPU-memory check cannot change which data exist. It runs before the sealed script and can only prevent a claim.
- No published command, and no sealed step between runs, reads a loss.
- `check_run.py` confines its reads and prints no loss value, tested on dummy runs with planted sentinels.
- The run-order rule in `RUN_COMMAND.ps1` does what the notes say.
- **Nothing published allows an interim look:** no N8 array, record or state is in the tree, the history, the
  releases or the pull request.

**Living pages.** Version 2.1, the date 23 November 2026 and N8's status agree on every page that states them and
with GitHub's release record. Numbers repeated across pages agree with each other and with the tables. All local
links resolve.

## 5. Before N8 resumes

None of these changes a registered rule or file. In order of weight:

1. **The loader (C1).** A dated note and a published, hashed loader with tests, before any N8 loss is read. It should
   fix: what makes a draw completed; that a retried draw is read wholly from its retry (n06 from X2); that nothing is
   fitted until every run and every due retry has ended; which hash checks refuse the analysis; and the output files.
2. **Three dated notes on what the protocol leaves open:** a run with no terminal (B2); when the study ends and the
   analysis runs, and that undone draws are not failed draws (B3); and the reason for the pause and the criterion for
   resuming (D2).
3. **Make the runs checkable (D1, D2).** Publish the run records that hold no loss value, each run's start and end
   time with its zone, and the SHA-256 of every loss-bearing file of n01–n06.
4. **GPU memory (D4).** Find out what the guard's reading measures before relying on a memory threshold, and state
   the 28 MiB start-up margin.
5. **The completeness check (F-d1, D7, D8).** Make it agree with refused-start records; give its SHA-256 with every
   result; record the new check's readings.
6. **The analysis tests (F-a1, C2, F-c1, C4).** A note on the `ORDERS.json` pin; dated tests for the eight untested
   branches; a note on the saturation rule and on what is read for an UNAVAILABLE hypothesis.
7. **Archive the registration with a third party (F-a2)** before more data exist.
8. **At the next publication:** A1, A2, D6, E1–E7, B4, B5, B10, S1.

## 6. New code

All of it is post hoc. Appendix 1 holds each auditor's report as returned, with its commands and outputs. Appendix 2
holds the source of every script the auditors and the supervising session wrote, each under its file name.

## 7. References

Verified by use in this audit:
- The repository at `30548dbb789b2a117486fdf6f9ab9added680172`; pull request #1; merge commit
  `c6f98b26669f5d29f30c576b6d800c1fc82c98eb`; releases v1.2, v2.0 and v2.1 (GitHub API, GET).
- `n7-loss-arrays-v1.zip`, SHA-256 `cbe26760e2062a4cf03307d779226fa6efce8cfcfbf57b2e092bd818af80b8a9`.
- https://blog.janestreet.com/a-study-of-sequence-weighting-at-scale/ returned HTTP 200 (auditor A). Its content was
  not inspected for this audit.

---

# Appendix 1. The four auditors' reports, as returned

Each is given as the auditor returned it; only the heading levels are lowered. For auditors A and D the fuller file each wrote is used; auditors B and C could not write a file, so their returned messages are used. Paths under the Temp folder `swa21` are the audit's working folders; the scripts and outputs they name are copied beside this report in `sequence_weighting_audit_2026-11-24_files`.

## Appendix 1A. Auditor A (areas A and E)

### Audit of record v2.1 (commit 30548db): areas A and E, with notes for F. Auditor A

Read-only audit of my clone at tag v2.1, the brief, and N7's public loss-array bundle. Every new calculation is **post hoc** and descriptive. No N8 result was estimated and no N8 data was read. GitHub and two public archives were queried with GET requests only.

#### Summary

1. No registered number, label or N8 registration element was found wrong in areas A and E.
2. Every figure in the 23 November correction reproduces with code I wrote: F1's minima (+0.0000764, −0.0000507, −0.000268), F2's scale, F3's maxima (14.11545, 8.44744, 6.99420 updates; 0.00000, 0.03709, 0.03659) and F4's arms.
3. F3 was verified without PyTorch. I generated the batch orders myself (section 4, "How I obtained batch orders"); the 12 order files are byte-identical by SHA-256 to those pinned in N8's `HASHES.json`.
4. **F-a1 (Major by the brief's definition, "a check fails"; no number affected).** `test_on_n7.py`, which the correction cites as reproducing F1 and F3, pins an index file whose bytes include the PyTorch and NumPy version strings of the machine that wrote it (`2.7.0+cu126`, `2.2.6`). With the published install lines (`2.7.0+cpu`, `2.5.3`) the same orders give 59 passed, 1 failed, exit 1.
5. **A1 (Minor).** `CORRECTION.md` was edited in place four minutes after its first public commit; neither the file nor `PUBLICATION_NOTES.md` says so.
6. **E1–E4 (Minor).** Living pages are stale about N8. One sentence still says the experiments "are closed again", and `DATA_AVAILABILITY.md` has not changed since 13 November.
7. Version 2.1, the date 23 November 2026 and N8's status agree on every page that states them, and with GitHub's release record.

#### 1. Findings

Paths are relative to the repository root at 30548db. "C" numbers refer to the commands in section 5, and script names to section 4.

| ID | Area | Severity | Finding | Evidence | Status | Fix type |
|---|---|---|---|---|---|---|
| A1 | A | Minor | The 23 November `CORRECTION.md` was revised in place after its first public commit, and this is not disclosed. c1a2380 was pushed on its own (the `verify` workflow ran on that push at 05:05:18Z) with the file at SHA-256 `05f5459c…`. 30548db, four minutes later, rewrote §3's "What changes" sentence and the closing "Living pages changed" list (`c043f501…`). The file has no amendment line. `PUBLICATION_NOTES.md` names c1a2380 nowhere and does not say the note was revised; its own 23 November entry was rewritten in place. The same step also changed `OPERATIONAL_NOTES.md` (from "`check_run.py X2` … had not been run by 23 November 2026" to its result), the N8 README, `README.md` and `NATURAL_TEXT_STUDIES.md`; the notes give only the final state. The record's precedent is to disclose: the 9 November correction says "**Amended 9 November 2026,** … Nothing else changed", and `PUBLICATION_NOTES.md:302` says "`CORRECTION.md` was amended in its local source and here". No number changed in the revision. | C1. Only trace, `PUBLICATION_NOTES.md:49–50`: 'No living page now says that the exposure-matched sets are matched "for the timing" of every pass.' Precedent: `reports/natural-text-correction-20261109-01/CORRECTION.md:5–6`. | VERIFIED | doc-only: a dated line in `PUBLICATION_NOTES.md` |
| A2 | A | Minor | The correction's general sentence is false for S4. `CORRECTION.md:27–29`: "Reading every draw at its later end gives the smallest mean contrast, but not the smallest lower t limit". `README.md:82`: "The later bracket end gives the lowest mean, not the lowest interval." `METHODS.md:222–224`: "Nor is it the least favourable reading for the interval: … −0.000268 for S4, against … −0.00027 with every draw at the later end." For S4 the all-later-end reading is the minimum over the 64 combinations (−0.0002679, all six draws at the later end). The two S4 figures set "against" each other are one number at two precisions. The sentence holds for P1 and S1 only. | `a1_envelope.py`, S4 block | VERIFIED | doc-only |
| A3 | A | Suggestion | F3's "0.000" at k = 1 is zero by construction: with one quarter per pass there is one joint cell. `CORRECTION.md:84` and `METHODS.md:181–182` list it beside 0.037 and 0.037 without saying so. The audit's balance figure at k = 1 was a marginal KS distance of 0.11920 (`AUDIT.md:61`), which reproduces (`a3d_ks.py`) and which the correction leaves out. N8's S-b `joint_cell_distance` at j = 1 will be 0 for the same reason. | `a3_recency.py`: "largest joint quarter-cell TV 0.00000 (… 1 cell)" | VERIFIED | doc-only; and a matter for N8's eventual result report |
| E1 | E | Minor | Stale status. `NATURAL_TEXT_STUDIES.md:149`: "The experiments were reopened for N7 alone and are closed again." Lines 187–197 of the same page, and every other page, say the record was reopened for N8 and that N8 is paused after 6 of 24 draws. `PUBLICATION_NOTES.md:116–117` says this page "no longer say[s] that no further runs will be added". | C2 | VERIFIED | doc-only |
| E2 | E | Minor | Stale page headers. `CURRENT_CLAIMS.md:3`: "**As of 12 November 2026; wording revised 13 November 2026, with no claim, number or label changed.**" C3's wording, three new numbers in C4's table and the training row changed on 23 November, and N8 paragraphs were added on 14 and 23 November. Its history paragraph (lines 7–18) ends at the 12 November correction. `NATURAL_TEXT_STUDIES.md:1` is titled "27 October – 11 November 2026" and its lines 3–5 end at 11 November; the page now runs to 23 November. | C2 | VERIFIED | doc-only |
| E3 | E | Minor | `DATA_AVAILABILITY.md` has not changed since 13 November and does not mention N8. Lines 9–10: "the public registrations of N6 and N7". Lines 13–14: "the audits of 8 and 12 November 2026, and the corrections of 9, 11 and 12 November 2026"; the 13 November audit and the 23 November correction are missing, although the notes of 13 November record that this list was then brought up to date. "What is not included" (lines 25–33) does not list N8's run folders, loss arrays or saved orders. Line 54, "the bundle holds no hash of them", is still true of the bundle, but N8's `HASHES.json` now pins hashes of N7's regenerated orders. | C2 | VERIFIED | doc-only |
| E4 | E | Minor | Other lists of registrations omit N8. `README.md:276`: "Only N7 was publicly preregistered", against `README.md:7–8`, where N8's "protocol and sealed source were registered publicly before any of its runs". `README.md:303`: "Public registrations of N6 and N7" for a folder that holds three. `METHODS.md:4`: "N7, the publicly preregistered study"; §1's table (lines 11–19) has no N8 row; `METHODS.md:23`: "the two public registrations". `NATURAL_TEXT_STUDIES.md:27`: "Two studies were also registered publicly"; its study table (lines 60–68) has no N8 row. | C2 | VERIFIED | doc-only |
| E5 | E | Minor | `README.md:271–272`, limitation 4: "The later-end readings are a sensitivity check, not a bound on the unobserved trajectory. S4's sign depends on this." S4's sign does not: its mean is above 0 in all 64 combinations (lowest +0.01043). What depends on the bracket end is whether its interval excludes 0. After F1 the same is true of S1 under one combination, which limitation 4 does not say. | `a1_envelope.py` | VERIFIED | doc-only |
| E6 | E | Minor | Overstated caption. `METHODS.md:362`: "**Figure 6.** Every estimate of the 512 − 768 contrast." The figure has 15 rows (`docs/make_readme_figures.py:170–190`; drawn 13 November). Estimates quoted on the living pages that it omits: S1 at the later bracket end (+0.00399 [+0.00099, +0.00699]), P1 with the E0 offset (+0.0062 [−0.0001, +0.0126]), P1 on the lower half of the weights (+0.0012 [−0.0009, +0.0032]), the better-rate contrast at the later end (+0.00518 [−0.00714, +0.01751]) and the 23 November envelope minima. | Image `docs/figures/estimates-light.png`, viewed | VERIFIED | doc-only (caption) |
| E7 | E | Suggestion | Dates mix clocks without saying so. N8's merge c6f98b2 is 2026-11-14T18:19:19Z (15 November, 01:19 +07:00) and is dated "14 November" (`README.md:11`, `reports/README.md:34`, `PUBLICATION_NOTES.md:99`). The v2.0 release, published 26 minutes later (2026-11-14T18:45:38Z), is dated "15 November 2026" (`PUBLICATION_NOTES.md:78`, `:95–96`). N8's run events are in local time. `NATURAL_TEXT_STUDIES.md:32–33` gives N6's and N7's merges in UTC. | C2 | VERIFIED | doc-only: give N8's merge time with its zone |
| F-a1 | F (bears on A and C) | Major by the brief's definition ("a check fails"); no number is affected | `test_on_n7.py` cannot pass for a reader who follows the published instructions. Its check at line 107 requires `sha(ORDERS.json) == ORDERS_SHA256` (`8ba4a3c2…`, also at `HASHES.json:142`). `regenerate_n7_orders.py` writes `torch.__version__` and `np.__version__` into that file. I rebuilt the pinned file byte for byte only with `2.7.0+cu126` and `2.2.6`, the protocol's WSL cross-check environment. The script's own usage line says "needs PyTorch (CPU)"; the README and the brief install the CPU build, which reports `2.7.0+cpu` (`AUDIT.md`: "ran with numpy 2.5.3, torch 2.7.0+cpu"), with NumPy 2.5.3. With identical order files and those two strings the test prints "FAIL  regenerated orders …" and "59 passed, 1 failed", exit 1; with the pinned strings, "60 passed, 0 failed", exit 0. The F1 and F3 checks pass in both runs. So the correction's "reproduced by `test_on_n7.py`" holds for the numbers, but "60 of 60" is reachable only on a machine that reports the registrant's version strings; a pass in the owner's WSL environment does not show that the public route passes. Limit of my evidence: I wrote the second `ORDERS.json` from the script's code and did not run the script under a CPU build of PyTorch. | `a3c_orders_json.py`, `a6_make_orders.py`, C3 | VERIFIED (mechanism and both runs); the CPU version string is taken from `AUDIT.md` | dated note stating the two strings, or publishing the order files (`inputs/n7-orders-v1/`); the registered test file is not to be edited |
| F-a2 | F (B, D) | Suggestion | N8's registration has no third-party archive. Software Heritage has no origin for the final repository and no revision c6f98b2; the Wayback CDX index has no capture of the repository page. For N6 and N7 the record cites both archives (`NATURAL_TEXT_STUDIES.md:31–51`). All four tags, `n8-registration` included, are lightweight: no tagger, date or signature. GitHub's signature on c6f98b2 is then the only independent evidence of when N8 was registered. | C2 | VERIFIED (Software Heritage, tags); PLAUSIBLE (Wayback: the query for PR #1's page timed out twice) | owner action, then doc-only |
| F-a3 | F (D) | Suggestion | No page says why training was paused, and the protocol has no provision for a pause (0 matches for "pause", "interrupt", "resum"). Section 8 fixes 24 draws. Section 6's status COMPLETE_WITH_FAILED_DRAWS covers 20–23 finished draws, where a failed draw is one that "fails in both attempts". The pages' sentence "If fewer than 20 draws are ever completed, the registered INCOMPLETE rule applies" is accurate, but leaves unsaid that a draw not yet attempted is not a failed draw, so stopping by choice at 20–23 is not a registered outcome. This is outside my assigned areas and is passed on. | C2; `N8-protocol-draft.md` §6 and §8 | VERIFIED (the texts) | doc-only: a dated note before R3 |

#### 2. Rejected concerns: checked and found sound

**The correction (A).**
- **F1.** All nine intervals in the table reproduce from `POINTS.csv` and `MATCHED.csv`. Minima over the 64 combinations: P1 +0.0000764 (m01 at the earlier end), S1 −0.0000507 (m02 at the earlier end, as the correction says), S4 −0.0002679. P1's lower limit is above 0 in all 64; S1's is at or below 0 in exactly 1; S4's in 5. The later end gives the lowest mean for all three, because 768's p\* rises in every bracket. The concavity argument is correct, and 200,000 random interior readings per statistic gave no lower limit below the vertex minimum.
- **F2.** `gap_scale.py` runs, and its output with LF line endings has the SHA-256 of `GAP_SCALE.txt` (`13b41f3d…`). My own recomputation gives the same interval, range and four slopes. A second descriptive scale agrees in size: across the ten draws at epoch 2, the p\* difference moves with the gap difference at +0.215 per nat (r = +0.55), and its value at zero gap difference is −0.0093. "About a tenth" stands. No living page still says "the same gap" for C3.
- **F3.** The three maxima and three distances reproduce to five decimals, as do the audit's KS figures. Set sizes are 226–272, 2,018–2,116 and 6,883–6,931. The mean absolute age difference over the 18 draw-passes is 4.2, 3.2 and 2.0 updates, in windows 256, 512 and 768 updates wide. No living page says "for the timing" or "equally long ago".
- **F4.** N6's `POINTS.csv` has width 384 at 3e-4 only, and 512 and 768 at both rates, on six draws. Its protocol's arm table agrees.
- **Quotations and side statements.** The sentences quoted from the 9 and 12 November corrections and from the old `METHODS.md` are exact. The tokenizer statement matches the audit's output and the pin at `acquire_plan.py:37`. The familywise statement matches N7's protocol (line 74) and its `HASHES.json` (lines 37–41).
- **Files.** `AUDIT.md` has the SHA-256 its README states (`9678f6cc…`). From v2.0 to v2.1 only living pages were modified and nine files added; no sealed or historical file changed.

**Living pages (E).**
- **Version and date.** "2.1" at `README.md:13`, `README.md:329` and `CITATION.cff:11`; 23 November 2026 at `README.md:13` and `CITATION.cff:16`. GitHub published v2.1 at 2026-11-23T05:10:47Z on 30548db.
- **N8's status** reads the same in `README.md`, `CURRENT_CLAIMS.md`, `NATURAL_TEXT_STUDIES.md` (lines 187–197), `PUBLICATION_NOTES.md`, the N8 README and the release notes: paused on 23 November after 6 of 24 draws, n06 completed in X2, R3–R8 not started, no p\* computed or examined.
- **Numbers repeated across pages** agree with each other and with the tables: the five registered contrasts and their leave-one-out readings, the later-end readings and counts, the read positions (2.19–2.48; m06 at 3.083; the other five at 2.73–2.95), P1's brackets (three and three), the six exposure-matched contrasts, the better-rate contrasts, the equal-updates sign by readout, the mean p\* of 0.103, the two parameter counts (recomputed from the architecture) and the update counts.
- **The README's example** prints `P1 = +0.00909 [+0.00400, +0.01417], n = 6`.
- **Links.** 314 local links and image sources on 11 pages resolve, fragment anchors included. The 12 external URLs on the living pages returned HTTP 200; their content was not inspected.
- **CI.** Both workflows succeeded on 30548db.
- **Considered and not raised:** v2.0 was released while the 13 November audit, which N8's protocol cites, was not yet in the tree (resolved in v2.1); local paths with the Windows user name in three new N8 files (disclosed at `PUBLICATION_NOTES.md:67`); the shorthand "exposure-matched", which now rests on the corrected definition in `METHODS.md` §5.

**Not verified by me.** The supervising session's checks of the brief's section 3. Whether PyTorch's CPU build writes exactly `2.7.0+cpu` on a reader's machine (taken from `AUDIT.md`). The content behind the external links.

#### 3. Before N8 resumes

1. **Nothing in areas A or E calls for a change to N8's registered analysis.** The constants N8's tests take from the 13 November audit reproduce independently.
2. **F-a1.** Decide how a reader is to reach "60 of 60": state the two version strings in a dated note, or publish the order files. The registered analysis is not affected.
3. **F-a3.** Record why training was paused, and that the 18 remaining draws will all be attempted. Do this before R3.
4. **F-a2.** Have the registration commit archived by a third party before more data or any analysis exists. This is the owner's action.
5. **Doc-only, at the next publication:** E1 first, then A1 and E2–E6.
6. **For the result report:** S-b's joint cell distance at j = 1 is 0 by construction (A3).

#### 4. New code (all post hoc) and exact output

Scripts are in `C:\Users\rafli\AppData\Local\Temp\swa21\a\scratch`, each with its output beside it as `.out`. `PY` is `C:\Users\rafli\AppData\Local\Programs\Python\Python312\python.exe -I -B` (Python 3.12.10, NumPy 2.5.3). `REPO` is my clone and `BUNDLE` is the extracted `n7-loss-arrays` folder.

##### How I obtained batch orders

- **I generated them, and read no order file from anywhere.** None is published, and I opened nothing outside my clone, my scratch folder, the bundle and the brief.
- **Inputs:** each draw's `adapt_order_seed` in the bundle's `MANIFEST.json`, and the sealed rule at `text_engine.py:52–53`: epoch e's order is `torch.randperm(n, generator=torch.Generator().manual_seed(999 + seed + e))`.
- **Tool:** my own pure-Python code in `a3_recency.py`, with no PyTorch. It is an MT19937 generator seeded with the 32-bit seed, followed by the swap loop of PyTorch's CPU `randperm` as I recall it: for i from 0 to n − 2, z is the next 32-bit output mod (n − i), and positions i and i + z are swapped.
- **Files written:** `a6_make_orders.py` wrote `orders_as_pinned\` and `orders_public_install\` in my scratch folder. Each holds 12 `.i64` files (six draws, and six with the seed shifted by 1) and an `ORDERS.json`, in the layout of `regenerate_n7_orders.py`. The two folders differ only in the version strings inside `ORDERS.json`.
- **Why I trust them:** the 12 files have the SHA-256 values that N8's `HASHES.json` pins for the registrant's PyTorch-generated files; they reproduce the 36 published set sizes and the 18 published per-draw losses exactly; and the losses separate trained from untrained sequences by −0.2257 nats on average, against +0.0001 for the shifted seed.
- **What this does not show:** I did not run PyTorch. That PyTorch 2.7.0 produces these orders rests on the hash identity with the registrant's pinned files.

##### `a1_envelope.py`

F1: the 64-combination envelope from N7's POINTS.csv and MATCHED.csv. Standard library, own t quantile.

SHA-256 `8518d76a94d7155ff2687647c2363241e2cbeb147ce35d17ece31ecb28d43942`. Command: `PY a1_envelope.py REPO`

~~~
t(0.975, df=5) = 2.5705818356363  (own bisection on the closed-form CDF)

== P1 (lr1e-04, matched on train) ==
  m01: bracket 2-2.25, weight 0.9959; p768 0.076656 -> 0.090136 (rises); contrast sealed +0.011705, earlier end +0.025130, later end +0.011650
  m02: bracket 2.25-2.5, weight 0.5615; p768 0.088761 -> 0.095095 (rises); contrast sealed +0.010231, earlier end +0.013788, later end +0.007454
  m03: bracket 2.25-2.5, weight 0.2071; p768 0.095407 -> 0.100937 (rises); contrast sealed +0.008166, earlier end +0.009311, later end +0.003780
  m04: bracket 2-2.25, weight 0.7561; p768 0.078456 -> 0.092275 (rises); contrast sealed +0.014037, earlier end +0.024485, later end +0.010666
  m05: bracket 2-2.25, weight 0.9251; p768 0.078437 -> 0.094538 (rises); contrast sealed +0.010368, earlier end +0.025263, later end +0.009162
  m06: bracket 2.25-2.5, weight 0.9029; p768 0.095226 -> 0.101309 (rises); contrast sealed +0.000021, earlier end +0.005512, later end -0.000570
  sealed (interpolated): +0.00909 [+0.00400, +0.01417], 6/6 above 0
  all later ends       : +0.00702 [+0.00216, +0.01189], 5/6 above 0
  all earlier ends     : +0.01725 [+0.00796, +0.02653], 6/6 above 0
  64 combinations: lowest lower limit +0.0000764 (mean +0.00927, upper +0.01846) at ELLLLL (draw order m01..m06; E earlier, L later)
    same combination with t = 2.5706: +0.0000763
    second lowest: +0.0002565 at ELLELL; combinations with lower limit <= 0: 0 of 64; highest lower limit +0.0079627
    lowest mean over the 64: +0.00702 at LLLLLL
    200,000 random interior readings: lowest lower limit +0.0008162 (vertex minimum +0.0000764)

== S1 (lr1e-04, matched on gap) ==
  m01: bracket 2.25-2.5, weight 0.2130; p768 0.090136 -> 0.096273 (rises); contrast sealed +0.010343, earlier end +0.011650, later end +0.005513
  m02: bracket 2.25-2.5, weight 0.1753; p768 0.088761 -> 0.095095 (rises); contrast sealed +0.012678, earlier end +0.013788, later end +0.007454
  m03: bracket 2.25-2.5, weight 0.3246; p768 0.095407 -> 0.100937 (rises); contrast sealed +0.007516, earlier end +0.009311, later end +0.003780
  m04: bracket 2.25-2.5, weight 0.9010; p768 0.092275 -> 0.097360 (rises); contrast sealed +0.006085, earlier end +0.010666, later end +0.005581
  m05: bracket 2.25-2.5, weight 0.1911; p768 0.094538 -> 0.101493 (rises); contrast sealed +0.007834, earlier end +0.009162, later end +0.002208
  m06: bracket 2.25-2.5, weight 0.2397; p768 0.095226 -> 0.101309 (rises); contrast sealed +0.004054, earlier end +0.005512, later end -0.000570
  sealed (interpolated): +0.00808 [+0.00487, +0.01130], 6/6 above 0
  all later ends       : +0.00399 [+0.00099, +0.00699], 5/6 above 0
  all earlier ends     : +0.01001 [+0.00709, +0.01294], 6/6 above 0
  64 combinations: lowest lower limit -0.0000507 (mean +0.00505, upper +0.01015) at LELLLL (draw order m01..m06; E earlier, L later)
    same combination with t = 2.5706: -0.0000508
    second lowest: +0.0002263 at EELLLL; combinations with lower limit <= 0: 1 of 64; highest lower limit +0.0070905
    lowest mean over the 64: +0.00399 at LLLLLL
    200,000 random interior readings: lowest lower limit +0.0004654 (vertex minimum -0.0000507)

== S4 (lr3e-04, matched on train) ==
  m01: bracket 2.75-3, weight 0.2042; p768 0.100862 -> 0.102674 (rises); contrast sealed +0.018293, earlier end +0.018663, later end +0.016851
  m02: bracket 2.75-3, weight 0.8043; p768 0.100989 -> 0.101997 (rises); contrast sealed +0.017070, earlier end +0.017880, later end +0.016873
  m03: bracket 2.75-3, weight 0.3845; p768 0.104627 -> 0.108042 (rises); contrast sealed +0.015546, earlier end +0.016859, later end +0.013444
  m04: bracket 2.5-2.75, weight 0.9280; p768 0.103107 -> 0.106906 (rises); contrast sealed +0.012925, earlier end +0.016450, later end +0.012651
  m05: bracket 2.75-3, weight 0.3352; p768 0.103096 -> 0.106238 (rises); contrast sealed +0.014874, earlier end +0.015927, later end +0.012785
  m06: bracket 3-3.25, weight 0.3314; p768 0.103894 -> 0.126254 (rises); contrast sealed +0.004944, earlier end +0.012355, later end -0.010005
  sealed (interpolated): +0.01394 [+0.00893, +0.01896], 6/6 above 0
  all later ends       : +0.01043 [-0.00027, +0.02113], 5/6 above 0
  all earlier ends     : +0.01636 [+0.01405, +0.01866], 6/6 above 0
  64 combinations: lowest lower limit -0.0002679 (mean +0.01043, upper +0.02113) at LLLLLL (draw order m01..m06; E earlier, L later)
    same combination with t = 2.5706: -0.0002679
    second lowest: -0.0002413 at LELLLL; combinations with lower limit <= 0: 5 of 64; highest lower limit +0.0140518
    lowest mean over the 64: +0.01043 at LLLLLL
    200,000 random interior readings: lowest lower limit -0.0001098 (vertex minimum -0.0002679)
~~~

##### `a2_gap.py`

F2: independent recomputation of the gap scale from N5's POINTS.csv, with one further descriptive scale.

SHA-256 `a65026d31f590248791552b5588c38aaff7a50ff37154dbea9a1887775c0083d`. Command: `PY a2_gap.py REPO`

~~~
readouts in N5 POINTS.csv: [0.25, 0.5, 1.0, 2.0, 3.0] | draws: 10 d01 .. d10
t(0.975, df=9) = 2.2621571627982
E2 gap 768-512:  +0.00039 [-0.00472, +0.00551]; draws -0.00925 to +0.01450; 4/10 above 0
E2 p*  768-512:  -0.00924 [-0.01123, -0.00724]; 0/10 above 0
width 512, E1->E2: mean of per-draw slopes 0.157 (draws 0.139 to 0.190); ratio of mean changes 0.156; gap change +0.132 to +0.161 nats
width 512, E2->E3: mean of per-draw slopes 0.185 (draws 0.172 to 0.195); ratio of mean changes 0.185; gap change +0.148 to +0.171 nats
width 768, E1->E2: mean of per-draw slopes 0.149 (draws 0.128 to 0.173); ratio of mean changes 0.149; gap change +0.117 to +0.145 nats
width 768, E2->E3: mean of per-draw slopes 0.167 (draws 0.150 to 0.184); ratio of mean changes 0.167; gap change +0.135 to +0.162 nats
slopes 0.149 to 0.185; upper limit 0.00551 nats -> 0.00082 to 0.00102 of p*; share of |p* difference| 0.089 to 0.110
  lower limit -0.00472 nats -> -0.00071 to -0.00087 of p* (the sign that would go with 768 having the lower p*)
  largest single-draw gap difference +0.01450 nats -> 0.00217 to 0.00268 of p*
across the 10 draws at E2: slope of (p* difference) on (gap difference) +0.215 per nat, r = +0.550; p* difference at zero gap difference (intercept) -0.00932
per draw (gap difference, p* difference): d01 -0.0045 -0.0106, d02 -0.0092 -0.0104, d03 +0.0064 -0.0037, d04 -0.0012 -0.0100, d05 -0.0056 -0.0085, d06 +0.0145 -0.0084, d07 -0.0011 -0.0133, d08 -0.0045 -0.0120, d09 +0.0066 -0.0061, d10 +0.0027 -0.0093
~~~

##### `a3_recency.py`

F3: the emulated batch orders, their validation, and the recency maxima.

SHA-256 `1c8a15d867f8a9a64b2aaf2ffa94e9ac36aabd8d492b29de83b338b53fbd615b`. Command: `PY a3_recency.py REPO BUNDLE`

~~~
MT19937 seed 5489: first output 3499211612 (standard 3499211612), 10000th 4123659995 (standard 4123659995)
equals NumPy legacy MT19937 raw 32-bit stream for seed 2419856979 (2,000 outputs): True
order seeds 999 + adapt_order_seed + e stay below 2^32: True
loss change, trained minus untrained in the quarter (emulated orders; 192 arm-windows): mean -0.2257, range -0.3467 to -0.1187 nats
loss change, trained minus untrained in the quarter (seed + 1 control; 192 arm-windows): mean +0.0001, range -0.0087 to +0.0123 nats
k = 1: set sizes 226-272; largest |mean age difference| 14.11545 updates (draw m02, pass 2, signed -14.11545); largest joint quarter-cell TV 0.00000 (draw m06; 1 cell); mean |age difference| over 18 draw-passes 4.207; window width 256 updates
k = 2: set sizes 2018-2116; largest |mean age difference| 8.44744 updates (draw m03, pass 3, signed +8.44744); largest joint quarter-cell TV 0.03709 (draw m03; 8 cells); mean |age difference| over 18 draw-passes 3.187; window width 512 updates
k = 3: set sizes 6883-6931; largest |mean age difference| 6.99420 updates (draw m04, pass 3, signed -6.99420); largest joint quarter-cell TV 0.03659 (draw m03; 27 cells); mean |age difference| over 18 draw-passes 1.981; window width 768 updates
published set sizes reproduced: 18 of 18 (draw, k) pairs; largest difference from the 18 published loss_every values: 0.00e+00
~~~

##### `a3b_order_hashes.py`

The emulated order files against the 12 hashes pinned in N8's HASHES.json.

SHA-256 `30a96285e5397be2cecd7a7c134aceac600b46d046c5ca343dfb22cbda176a17`. Command: `PY a3b_order_hashes.py REPO BUNDLE`

~~~
m01.i64: emulated 1454c34d6a9be84a..., pinned in HASHES.json 1454c34d6a9be84a...  MATCH
m01-seed-plus-1.i64: emulated c616d85dfc78f5df..., pinned in HASHES.json c616d85dfc78f5df...  MATCH
m02.i64: emulated 2dd2b964e1839d51..., pinned in HASHES.json 2dd2b964e1839d51...  MATCH
m02-seed-plus-1.i64: emulated 9453256699a44e46..., pinned in HASHES.json 9453256699a44e46...  MATCH
m03.i64: emulated cac1b23951790ca0..., pinned in HASHES.json cac1b23951790ca0...  MATCH
m03-seed-plus-1.i64: emulated f552dd02dcbdb99d..., pinned in HASHES.json f552dd02dcbdb99d...  MATCH
m04.i64: emulated 849eedd91be26e6e..., pinned in HASHES.json 849eedd91be26e6e...  MATCH
m04-seed-plus-1.i64: emulated 35e8815ecc62c3ed..., pinned in HASHES.json 35e8815ecc62c3ed...  MATCH
m05.i64: emulated 0bb27a61d12bc33e..., pinned in HASHES.json 0bb27a61d12bc33e...  MATCH
m05-seed-plus-1.i64: emulated cea25e11ea041f6b..., pinned in HASHES.json cea25e11ea041f6b...  MATCH
m06.i64: emulated 67d29a9c25d8cd21..., pinned in HASHES.json 67d29a9c25d8cd21...  MATCH
m06-seed-plus-1.i64: emulated ea2a16b25ed13468..., pinned in HASHES.json ea2a16b25ed13468...  MATCH
12 of 12 emulated order files are byte-identical to the pinned PyTorch-generated files
~~~

##### `a3c_orders_json.py`

Which version strings rebuild the pinned ORDERS.json (12 pairs tried).

SHA-256 `33476a78d2a2de64bfed98df02eb0f99e9ca8cd060bc2d1ced47af540599f96b`. Command: `PY a3c_orders_json.py REPO BUNDLE`

~~~
ORDERS.json rebuilt byte for byte (SHA-256 equals the pin 8ba4a3c2...): yes, with torch 2.7.0+cu126 and numpy 2.2.6
~~~

##### `a6_make_orders.py`

Writes the two order folders.

SHA-256 `51686ae563735bacbef75a996c02725d92d7fab3d6ccac23dd7917b8c70e4d34`. Command: `PY a6_make_orders.py BUNDLE orders_as_pinned 2.7.0+cu126 2.2.6 ; PY a6_make_orders.py BUNDLE orders_public_install 2.7.0+cpu 2.5.3`

~~~
wrote 12 order files to orders_as_pinned; ORDERS.json records torch 2.7.0+cu126, numpy 2.2.6; ORDERS.json SHA-256 8ba4a3c2e7906f65c6335ece7a785bfb37fe1b2904684959d388f589f2287eb1
wrote 12 order files to orders_public_install; ORDERS.json records torch 2.7.0+cpu, numpy 2.5.3; ORDERS.json SHA-256 536bb5d050b9642fa09d61cc65fd32a4725f32673289c6bf502eb668bc23b6e2
~~~

##### `a3d_ks.py`

The audit's KS balance figures, from the emulated orders.

SHA-256 `db1f9a514a9e85364eed6ec96c6088a649529e47c442e3f16cbb77e3eb6f57ce`. Command: `PY a3d_ks.py orders_as_pinned`

~~~
k = 1: largest marginal KS distance 0.11920 (m02 pass 2)
k = 2: largest marginal KS distance 0.03365 (m03 pass 3)
k = 3: largest marginal KS distance 0.01816 (m04 pass 3)
~~~

##### `a4_numbers.py`

Numbers quoted on the living pages, from MATCHED.csv and the 11 November RESULTS.json.

SHA-256 `0bad7f3828a3370ef19f92ed1fc381c031eab80e345c37fe8f5c08ccb4424b35`. Command: `PY a4_numbers.py REPO`

~~~
P1: +0.00909 [+0.00400, +0.01417], 6/6 above 0; read at 2.189-2.476; values +0.01171, +0.01023, +0.00817, +0.01404, +0.01037, +0.00002
    brackets: m01 2-2.25, m02 2.25-2.5, m03 2.25-2.5, m04 2-2.25, m05 2-2.25, m06 2.25-2.5
S1: +0.00808 [+0.00487, +0.01130], 6/6 above 0; read at 2.294-2.475; values +0.01034, +0.01268, +0.00752, +0.00608, +0.00783, +0.00405
    brackets: m01 2.25-2.5, m02 2.25-2.5, m03 2.25-2.5, m04 2.25-2.5, m05 2.25-2.5, m06 2.25-2.5
S3: -0.00454 [-0.00795, -0.00114], 0/6 above 0; read at 3.000-3.000; values -0.00290, -0.00014, -0.00639, -0.00283, -0.00566, -0.00933
S4: +0.01394 [+0.00893, +0.01896], 6/6 above 0; read at 2.732-3.083; values +0.01829, +0.01707, +0.01555, +0.01292, +0.01487, +0.00494
    brackets: m01 2.75-3, m02 2.75-3, m03 2.75-3, m04 2.5-2.75, m05 2.75-3, m06 3-3.25
S5: +0.01382 [+0.01116, +0.01648], 6/6 above 0; read at 3.000-3.000; values +0.01685, +0.01687, +0.01344, +0.01062, +0.01279, +0.01236
S2: only 3 draws read; read at 2.170-2.784; values +0.00611, +0.01414, -0.00571
ANALYSIS.json top-level keys: ['status', 'closed_by_failure', 'terminals', 'draws_available', 'arms', 'readouts', 'match_path', 'decision', 'sequence', 'statistics', 'readings', 'records_against_arrays', 'not_overfit', 'power_stated_in_advance', 'fit_bounds', 'losses', 'note', 'rate_effects', 'by_readout']
mean p*(512, E3, 1e-4) 0.1027; 768 where read in P1: 0.0889-0.1007
P1 leave-one-out intervals: m01 [+0.00208, +0.01505]; m02 [+0.00218, +0.01554]; m03 [+0.00258, +0.01597]; m04 [+0.00228, +0.01392]; m05 [+0.00216, +0.01550]; m06 [+0.00822, +0.01359]
S1 leave-one-out intervals: m01 [+0.00367, +0.01159]; m02 [+0.00429, +0.01005]; m03 [+0.00397, +0.01243]; m04 [+0.00446, +0.01251]; m05 [+0.00389, +0.01238]; m06 [+0.00565, +0.01214]
S3 leave-one-out intervals: m01 [-0.00923, -0.00051]; m02 [-0.00879, -0.00206]; m03 [-0.00850, +0.00015]*; m04 [-0.00924, -0.00053]; m05 [-0.00876, +0.00012]*; m06 [-0.00669, -0.00047]
S4 leave-one-out intervals: m01 [+0.00714, +0.01901]; m02 [+0.00703, +0.01960]; m03 [+0.00708, +0.02016]; m04 [+0.00755, +0.02074]; m05 [+0.00715, +0.02036]; m06 [+0.01318, +0.01830]
S5 leave-one-out intervals: m01 [+0.01036, +0.01607]; m02 [+0.01037, +0.01605]; m03 [+0.01039, +0.01741]; m04 [+0.01170, +0.01722]; m05 [+0.01058, +0.01748]; m06 [+0.01074, +0.01749]
matched|lr1e-04|k1|every: -0.00346 [-0.02582, +0.01890], 4/6 above 0
matched|lr1e-04|k2|every: -0.00476 [-0.01213, +0.00262], 2/6 above 0
matched|lr1e-04|k3|every: -0.00506 [-0.01094, +0.00083], 2/6 above 0
matched|lr3e-04|k1|every: +0.01258 [-0.00990, +0.03506], 5/6 above 0
matched|lr3e-04|k2|every: +0.01264 [+0.00486, +0.02042], 6/6 above 0
matched|lr3e-04|k3|every: +0.01292 [+0.00718, +0.01865], 6/6 above 0
better_rate|equal_updates|0.25: +0.02508 [+0.02200, +0.02816], 6/6 above 0
better_rate|loss|0.25: +0.05703 [+0.02344, +0.09062], 6/6 above 0
better_rate|equal_updates|0.5: +0.01755 [+0.01562, +0.01947], 6/6 above 0
better_rate|loss|0.5: +0.03324 [+0.00174, +0.06475], 5/6 above 0
better_rate|equal_updates|1.0: +0.01240 [+0.01095, +0.01385], 6/6 above 0
better_rate|loss|1.0: +0.01408 [-0.01483, +0.04298], 4/6 above 0
better_rate|equal_updates|2.0: +0.01147 [+0.00862, +0.01431], 6/6 above 0
better_rate|loss|2.0: +0.00231 [-0.02303, +0.02765], 4/6 above 0
~~~

##### `a5_links.py`

Local links and fragment anchors of 11 pages.

SHA-256 `4bfd8f16ca234f62dd160b6f4a944d4f6a8bbca05782998d1e42b65f5d2a4982`. Command: `PY a5_links.py REPO`

~~~
314 local links and image sources checked on 11 pages; 0 broken; 15 external links not checked
~~~

#### 5. Commands that matter, with exact output

Run in `REPO` unless stated.

##### C1. History of the correction (A1)

~~~
$ git log --format="%h %cd %s" --date=iso-strict --stat -- reports/natural-text-correction-20261123-01/
30548db 2026-11-23T12:09:20+07:00 Version 2.1: N8 paused

 reports/natural-text-correction-20261123-01/CORRECTION.md | 9 +++++----
 1 file changed, 5 insertions(+), 4 deletions(-)
c1a2380 2026-11-23T12:05:02+07:00 N8 paused after 6 of 24 draws

 .../CORRECTION.md                                  | 124 +++++++++++++++++++++
 .../GAP_SCALE.txt                                  |   9 ++
 .../gap_scale.py                                   |  40 +++++++
 3 files changed, 173 insertions(+)

$ git diff c1a2380 30548db -- reports/natural-text-correction-20261123-01/CORRECTION.md
diff --git a/reports/natural-text-correction-20261123-01/CORRECTION.md b/reports/natural-text-correction-20261123-01/CORRECTION.md
index b0ae40b..edcb8a2 100644
--- a/reports/natural-text-correction-20261123-01/CORRECTION.md
+++ b/reports/natural-text-correction-20261123-01/CORRECTION.md
@@ -85,9 +85,9 @@ largest total-variation distance between the sets' joint distributions over quar
 
 These are the audit's figures. `test_on_n7.py` reproduces them within 5e-6 from N7's regenerated batch orders.
 
-**What changes:** `METHODS.md` now says "matched recency windows" and gives these differences. C4 in
-`CURRENT_CLAIMS.md` says "in matched recency windows for all three passes" instead of "matched for the timing of all
-three passes".
+**What changes:** `METHODS.md` now says "matched recency windows" and gives these differences. `CURRENT_CLAIMS.md`
+(C4), `README.md` and `NATURAL_TEXT_STUDIES.md` say "in matched recency windows" for every pass instead of "matched for
+the timing" of every pass.
 
 ## 4. F4: N6's width 384, and the training statement
 
@@ -121,4 +121,5 @@ diagnostics) and F6 (estimator edge-case fixtures) are not adopted in this updat
 Living pages changed:
 - `CURRENT_CLAIMS.md`: C3, C4's table and exposure bullet, and the training row;
 - `METHODS.md`: §1's table, §5's exposure-matched comparison, §6 and §7;
-- `README.md`: the sensitivity table's note, the familywise rate and the training level.
+- `README.md`: the sensitivity table's note, the familywise rate, matched recency windows and the training level;
+- `NATURAL_TEXT_STUDIES.md`: matched recency windows.

$ git show c1a2380:reports/natural-text-correction-20261123-01/CORRECTION.md | sha256sum ; sha256sum reports/natural-text-correction-20261123-01/CORRECTION.md
05f5459c988f25ff77a6330e056e574da09bfa075fa9061ed2d91c74ed5359e2 *-
c043f501a9bb7963c57e41596b870e85e5cb1245d403328d833b3359981921cb *reports/natural-text-correction-20261123-01/CORRECTION.md

$ git grep -c "c1a2380" 30548db -- . ; git grep -n -i "amend\|revis" 30548db -- reports/natural-text-correction-20261123-01/CORRECTION.md   (no output: no match)

$ git diff --stat c1a2380 30548db
 CITATION.cff                                       |   4 +-
 NATURAL_TEXT_STUDIES.md                            |   4 +-
 PUBLICATION_MANIFEST.csv                           |  17 +-
 PUBLICATION_NOTES.md                               |  29 +-
 README.md                                          |   8 +-
 .../OPERATIONAL_NOTES.md                           |   6 +-
 .../README.md                                      |   7 +-
 .../RUN_COMMAND.ps1                                | 102 ++++++
 .../X2_COMMAND.txt                                 |  73 ++++
 .../check_run.py                                   | 379 +++++++++++++++++++++
 .../CORRECTION.md                                  |   9 +-
 11 files changed, 607 insertions(+), 31 deletions(-)

$ gh api -X GET "repos/rafli-hl/sequence-weighting/actions/runs?per_page=4" --jq ".workflow_runs[] | [.name, .head_sha[0:7], .event, .conclusion, .created_at] | @tsv"
verify-posthoc	30548db	release	success	2026-11-23T05:10:49Z
verify	30548db	release	success	2026-11-23T05:10:49Z
verify	30548db	push	success	2026-11-23T05:09:35Z
verify	c1a2380	push	success	2026-11-23T05:05:18Z
~~~

##### C2. Living pages, versions, dates, files changed, archives, tags, protocol (E1 to E7, F-a2, F-a3)

~~~
$ grep -n "closed again" NATURAL_TEXT_STUDIES.md ; sed -n "187,188p;191,192p" NATURAL_TEXT_STUDIES.md
149:The experiments were reopened for N7 alone and are closed again.
record was closed after N7; on 14 November 2026 it was reopened for one registered study, N8, a dense-readout
replication of N7 on fresh draws ([preregistration](preregistration/natural-text-dense-replication-20261114/README.md)), which has no results yet.
**N8, paused on 23 November 2026.**
- Training stopped after 6 of its 24 draws: n01–n06, with n06 completed in the retry run X2. R3–R8 have not started.

$ sed -n "3p" CURRENT_CLAIMS.md | cut -c1-120 ; sed -n "1p" NATURAL_TEXT_STUDIES.md
**As of 12 November 2026; wording revised 13 November 2026, with no claim, number or label changed.** This page states w
# Natural-text studies, 27 October – 11 November 2026

$ git log --format="%h %ad" --date=short -- DATA_AVAILABILITY.md ; grep -c "N8" DATA_AVAILABILITY.md ; sed -n "9,10p;13,14p" DATA_AVAILABILITY.md
fee55ea 2026-11-13
c4ae0e1 2026-11-12
0
- **Protocols and registrations.** Each study's protocol, amendments and seed registry, and the public registrations
  of N6 and N7.
- **Review records.** The adversarial review, the response to it, the owner's design decisions for the natural-text
  studies, the audits of 8 and 12 November 2026, and the corrections of 9, 11 and 12 November 2026.

$ grep -n "Only N7 was publicly\|Public registrations of N6 and N7\|sign depends" README.md | cut -c1-150 ; grep -n "the two public registrations" METHODS.md ; grep -n "Two studies were also registered publicly" NATURAL_TEXT_STUDIES.md ; ls preregistration
272:   readings are a sensitivity check, not a bound on the unobserved trajectory. S4's sign depends on this.
276:6. **Registration.** Only N7 was publicly preregistered. N6 was registered publicly after its data existed; the other
303:| `preregistration/` | Public registrations of N6 and N7, each with sealed source and seed registry |
23:How to check the two public registrations against the archived commits is in
27:Two studies were also registered publicly. N6 was registered only after its data existed (see
natural-text-dense-replication-20261114/
natural-text-matched-confirmation-20261104/
natural-text-peak-confirmation-20261103/

$ grep -n "version\|v2\.1\|date-released" CITATION.cff README.md | grep -i "2\.1\|version \|date-released" | cut -c1-140
CITATION.cff:11:version: "2.1"
CITATION.cff:16:date-released: 2026-11-23
README.md:13:[v2.1](https://github.com/rafli-hl/sequence-weighting/releases/tag/v2.1) (23 November 2026). The README
README.md:315:This repository starts from a single commit of the finished record (version 1.2). The record was built in an earlier
README.md:329:  version      = {2.1},

$ gh api -X GET repos/rafli-hl/sequence-weighting/releases --jq ".[] | [.tag_name, .created_at, .published_at] | @tsv"
v2.1	2026-11-23T05:09:20Z	2026-11-23T05:10:47Z
v2.0	2026-11-14T18:44:07Z	2026-11-14T18:45:38Z
v1.2	2026-11-12T10:13:56Z	2026-11-12T10:25:53Z

$ git log -3 --format="%h %ad %s" --date=iso-strict c6f98b2 ; git for-each-ref --format="%(refname) %(objecttype) %(objectname:short)" refs/tags
c6f98b2 2026-11-15T01:19:19+07:00 Merge pull request #1 from rafli-hl/n8-registration
aaafa2e 2026-11-15T01:17:02+07:00 Register N8: dense-readout replication of N7
fee55ea 2026-11-13T12:54:48+07:00 Revise README and add METHODS.md (documentation only; no result changed
refs/tags/n8-registration commit c6f98b2
refs/tags/v1.2 commit c4ae0e1
refs/tags/v2.0 commit 88ac496
refs/tags/v2.1 commit 30548db

$ git diff --name-status v2.0 v2.1
M	CITATION.cff
M	CURRENT_CLAIMS.md
M	METHODS.md
M	NATURAL_TEXT_STUDIES.md
M	PUBLICATION_MANIFEST.csv
M	PUBLICATION_NOTES.md
M	README.md
A	preregistration/natural-text-dense-replication-20261114/OPERATIONAL_NOTES.md
M	preregistration/natural-text-dense-replication-20261114/README.md
A	preregistration/natural-text-dense-replication-20261114/RUN_COMMAND.ps1
A	preregistration/natural-text-dense-replication-20261114/X2_COMMAND.txt
A	preregistration/natural-text-dense-replication-20261114/check_run.py
M	reports/README.md
A	reports/external-audit-20261113-01/AUDIT.md
A	reports/external-audit-20261113-01/README.md
A	reports/natural-text-correction-20261123-01/CORRECTION.md
A	reports/natural-text-correction-20261123-01/GAP_SCALE.txt
A	reports/natural-text-correction-20261123-01/gap_scale.py

$ curl -s "https://archive.softwareheritage.org/api/1/origin/https://github.com/rafli-hl/sequence-weighting/visits/?per_page=5"
{"exception":"NotFoundExc","reason":"Origin with url https://github.com/rafli-hl/sequence-weighting not found!"}
$ curl -s -o /dev/null -w "%{http_code}" "https://archive.softwareheritage.org/api/1/revision/c6f98b26669f5d29f30c576b6d800c1fc82c98eb/"
404
$ curl -s "http://web.archive.org/cdx/search/cdx?url=github.com/rafli-hl/sequence-weighting&limit=5&output=json&fl=timestamp,original,statuscode"
[]


$ grep -n -i -c "pause\|interrupt\|resum" preregistration/natural-text-dense-replication-20261114/N8-protocol-draft.md
0
~~~

##### C3. The record's `test_on_n7.py`, run twice on N7's public data (F-a1)

Command: `PY REPO/preregistration/natural-text-dense-replication-20261114/analysis/test_on_n7.py REPO BUNDLE <orders folder>`. Full outputs are in `test_on_n7_as_pinned.out` and `test_on_n7_public_install.out` (78 lines each). Apart from timing lines they differ only here (`<` pinned strings, `>` public-install strings):

~~~
49c49
< PASS  regenerated orders (PyTorch 2.7.0+cu126): ORDERS.json pinned, files, per-epoch order_sha256, each row a permutation  [8ba4a3c2e7906f65, 0 mismatches]
---
> FAIL  regenerated orders (PyTorch 2.7.0+cpu): ORDERS.json pinned, files, per-epoch order_sha256, each row a permutation  [536bb5d050b9642f, 0 mismatches]
70,71c70,71
< 60 passed, 0 failed
< exit 0
---
> 59 passed, 1 failed
> exit 1
~~~

The F1 and F3 lines, identical in both runs:

~~~
PASS  P1 envelope over 64 combinations: min lower +0.0000764, max upper +0.0274348  [vs brief 5.1e-09; vs itertools brute force 0 / 0]
PASS  S-b, 768 at E2.25: whole, last, every, losses against the 11 Nov RESULTS.json (1e-6); every-pass balance: sizes 226-272, mean age difference 14.11545, joint cell distance 0.00000 (13 Nov audit)  [largest value difference 1.1e-08]
PASS  S-b, 768 at E2.5: whole, last, every, losses against the 11 Nov RESULTS.json (1e-6); every-pass balance: sizes 2018-2116, mean age difference 8.44744, joint cell distance 0.03709 (13 Nov audit)  [largest value difference 2.2e-08]
PASS  S-b, 768 at E2.75: whole, last, every, losses against the 11 Nov RESULTS.json (1e-6); every-pass balance: sizes 6883-6931, mean age difference 6.99420, joint cell distance 0.03659 (13 Nov audit)  [largest value difference 2.2e-08]
PASS  S1 envelope over 64 combinations: min lower -0.0000507, max upper +0.0142363  [vs brief 4.1e-08; vs itertools brute force 0 / 0]
PASS  S4 envelope over 64 combinations: min lower -0.0002679, max upper +0.0243117  [vs brief 1.4e-07; vs itertools brute force 0 / 0]
~~~

##### C4. `gap_scale.py` (F2), the README example, and the state of the clone

~~~
$ PY reports/natural-text-correction-20261123-01/gap_scale.py > SCRATCH/gap_scale_rerun.out   (exit 0)
$ tr -d "\r" < SCRATCH/gap_scale_rerun.out | sha256sum ; sha256sum reports/natural-text-correction-20261123-01/GAP_SCALE.txt
13b41f3d7dc5818a6105fbf02376c277c2167b31bf8c873ec7ba6298f8ff36f3 *-
13b41f3d7dc5818a6105fbf02376c277c2167b31bf8c873ec7ba6298f8ff36f3 *reports/natural-text-correction-20261123-01/GAP_SCALE.txt
$ PY SCRATCH/readme_block.py   (README.md lines 205 to 226, unedited)
P1 = +0.00909 [+0.00400, +0.01417], n = 6
$ git status --porcelain | wc -l ; git rev-parse HEAD   (after all work)
0
30548dbb789b2a117486fdf6f9ab9added680172
~~~

## Appendix 1B. Auditor B (area B)

**Delivery note.** `FINDINGS.md` was not written: the Write tool refused it ("Subagents should return findings as text, not write report files"), and I did not work around that. The full report is below; please save it to `C:\Users\rafli\AppData\Local\Temp\swa21\b\scratch\FINDINGS.md` if the file is needed. My scripts and their outputs are in that scratch folder (`b1_source_diff.py`, `b2_power.py`, `b3_registry.py`, `b4_n7_loo.py`, each with a `.out` file; `all_hashes.txt`).

### Auditor B: the N8 registration package (area B, plus area F items met on the way)

Audited: `preregistration/natural-text-dense-replication-20261114/` at tag `v2.1` (commit `30548dbb789b2a117486fdf6f9ab9added680172`), against tag `n8-registration` (commit `c6f98b26669f5d29f30c576b6d800c1fc82c98eb`) and N7's sealed source. Paths are relative to the repository root unless they start with `N8/`, which stands for `preregistration/natural-text-dense-replication-20261114/`. Line numbers are at commit `30548db`.

**Summary.** No registered number, label, hash, seed, partition or source file of N8 was found to be wrong.
- `CHANGES.md` is exactly the real difference from N7's sealed source: 61 hunks, and applying them to N7's files reproduces N8's files byte for byte.
- The seed registry re-derives from its own draw and exclusions, the partition is disjoint from N7's, the pilot log matches every figure in the protocol's section 7, and the power table reproduces.
- The builder change after registration is exactly two lines, and no other registered file changed.
- The findings are gaps, not errors. The registered analysis has no entry point for N8's own run folders (N7's sealed analysis had one). The protocol's failure rules are silent on a run that leaves no terminal and on when the study ends. All three can be settled by a dated note before any p\* is computed.

#### 1. Findings

| ID | Area | Severity | Finding | Evidence | Status | Fix type |
|---|---|---|---|---|---|---|
| B1 | B | Major (a gap, not an error; see the note under the table) | **The registered analysis has no loader or driver for N8's own run folders.** `analysis/n8_analysis.py` is a library whose entry `analyse(per, data, plan, orders)` takes already-assembled inputs. Nothing registered says how `data` and `orders` are built from `runs\n8-r<k>` and `runs\n8-x<k>`: what makes a draw "completed" or "failed", which attempt's arrays are read for a retried draw (n06 exists in R2 and X2), which binding checks refuse or drop a draw, and what files the analysis writes. N7's sealed analysis registered all of this (`load`, with terminal, pin, receipt-against-terminal, array-hash and layout checks, and a `__main__` that wrote `ANALYSIS.json`, `POINTS.csv`, `FITS.csv`, `MATCHED.csv`). N8 dropped that file and did not replace those parts. | `N8/analysis/n8_analysis.py:16` ("Inputs. data[d] is None for a failed draw, or dict(weights=[...], arms=…"), `:562` (`def analyse(per, data, plan=PLAN, orders=None)`); it has no `__main__`, and a grep of `N8/analysis/*.py` for `RECEIPT`, `TERMINAL`, `n8-r`, `runs/`, `def load` finds only the three test/regeneration `__main__` blocks (section 5). `N8/HASHES.json:31-36` lists 4 analysis files and `:37-47` 9 tools; `N8/tools/write_hashes.py:26-27` hashes every file under `analysis/` and `tools/`, so no loader existed there at registration. N7: `preregistration/natural-text-matched-confirmation-20261104/sealed-source/matched_analysis.py:61` (`def load(runs, pins=…)`), `:413` (`if __name__ == '__main__':`); `sealed-source/PROTOCOL.md:205` ("The analysis: `matched_analysis.py` on M1 and M2, once both have ended with a terminal, with the results report's layout frozen first"). `N8/CHANGES.md:37` ("**Dropped** `matched_analysis.py` … N7's analysis; N8's is `analysis/n8_analysis.py` (§6)"). | VERIFIED | Dated note before the analysis, publishing the loader/driver with its SHA-256 before any p\* is computed (section 3) |
| B2 | B | Minor (protocol gap; has not occurred) | **The failure rules do not cover a run that leaves no terminal.** Section 8 admits a retry "only on its first run's terminal record", and the builder enforces it. The worker writes `TERMINAL.json` only from its `finally` block. A killed process, a WSL or machine crash, or a refusal after the owner script's claim but before the worker's `try` therefore leaves none; the run's activation is then consumed and its retry cannot be built. The protocol does not say what such a run's draws are: failed and excluded (three draws lost per event; two events can make the study INCOMPLETE), or the subject of a recorded deviation. It also does not say whether a draw with a COMPLETE receipt but no terminal counts. Two readers could count different draws from the same folders. N7's protocol had an explicit rule. A related leftover: N8's terminal still records `counted_as_attempt`, the field of N7's counting rule, which N8's protocol does not have (a start-up stop is retried as X<k> in N8). | `N8/N8-protocol-draft.md:178-182`; `N8/tools/build_n8_activation.py:96` ("Run {first} left no terminal, so it admits no retry"); `N8/source/matched_worker.py:309-312` (raises before the `try` at `:316`), `:362-374` (`finally:` … `out.json('TERMINAL.json', status)`), `:371` (`status['counted_as_attempt'] = …`); `N8/source/MATCHED_OWNER_RUN.ps1:55` ("One-use attempt consumed; no retry"). N7: `sealed-source/PROTOCOL.md:220` ("A run that leaves no terminal, because WSL died or the machine crashed, counts for nothing, whatever receipts are on disk. A draw counts only through a terminal's stage records."), `:207-209` (counting rule). | VERIFIED | Dated note before R3 |
| B3 | B | Minor (protocol gap) | **The stopping rule does not say when the study ends or when the one analysis runs.** "No look at any p\* before all 24 draws are complete" cannot be met literally once a draw has failed twice. Nothing says when a paused study is closed as INCOMPLETE (the README's "if fewer than 20 draws are ever completed" has no end point). N7 registered "once both have ended with a terminal, with the results report's layout frozen first"; N8 has no counterpart. This does not inflate the false-positive rate (INCOMPLETE gives no label), but it leaves the timing of the analysis to a later choice. | `N8/N8-protocol-draft.md:176` ("**Fixed sample.** 24 draws, no interim analysis, and no look at any p\* before all 24 draws are complete."), `:103-106`; `N8/README.md:9-10`; N7 `sealed-source/PROTOCOL.md:205`. | VERIFIED | Dated note before R3 |
| B4 | B | Minor | **The recorded builder differs from the registered one in exactly two lines, as disclosed, but those lines carry two things the disclosures do not mention.** (a) `PUBLIC_REGISTRATION` has a sixth key, `pr_record_sha256` = `e8d92b7e…f381`. The registered line's own comment did not list it ("dict(url, merge_commit, tag, source_subject_sha256, pilot_log_sha256)"), and it names a file that is not published and is not named in `HASHES.json`, the README or `PUBLICATION_NOTES.md`. (b) Both comments cite `registration/apply_registration.py`, which is not published. Neither changes behaviour: the code reads only `merge_commit`, `tag`, `source_subject_sha256` and `pilot_log_sha256`, and copies the whole dict into each `APPROVAL_RECORD.json`. | `git diff n8-registration v2.1 -- N8/tools/build_n8_activation.py` (section 5: 2 lines removed, 2 added); `N8/tools/build_n8_activation.py:30-31`, `:47`, `:53-54`, `:142`; `git grep` for `e8d92b7e`, `pr_record` and `apply_registration` (section 5); `N8/README.md:31`; `PUBLICATION_NOTES.md:90-94`; `N8/HASHES.json:144`. | VERIFIED | Doc-only (name the PR record and the tool, or publish them) |
| B5 | B | Minor | **Some hunks of `CHANGES.md` are justified by documents that are not published, although the protocol says each change is "justified by a section of this protocol".** Hunks 29 and 55 cite only "brief, item "paths"". Hunks 50, 58 and 60 cite nothing (they rename N7 to N8 or list files). Hunks 15, 18, 22 and 40 add "Gate 2 review", and hunks 49 and 54 "the owner's decision of 14 Nov 2026", to a section number. I read all 61: these are paths, names, messages, the study-folder census and kept states. None touches the model, optimiser, loss, weights, batch order or evaluation. | `N8/N8-protocol-draft.md:197-198`; `N8/CHANGES.md:3` (""brief" is the owner's task brief for N8"), `:523`, `:936`, `:877`, `:974`, `:1005`, `:333`, `:369`, `:417`, `:712`, `:859`, `:926`; `b1_source_diff.py` output (section 4). | VERIFIED | Doc-only |
| B6 | B | Minor | **A README note dated 15 November was first published on 23 November, and `PUBLICATION_NOTES.md` says the README "keeps" it.** The note "15 November 2026, operational: two empty folders before R1" is absent from the README at `v2.0` and first appears in commit `c1a2380`. No registered file is affected; the publication date of the note is not stated. | `git show v2.0:N8/README.md \| grep -c 'two empty folders'` → 0; at `c1a2380` and `v2.1` → 1; `N8/README.md:32`; `PUBLICATION_NOTES.md:68` ("keeps the note of 15 November on the two empty folders"). | VERIFIED | Doc-only |
| B7 | B | Minor | **The protocol's pilot summary gives the worker's own GPU memory but not the figure the guard acts on.** Section 7 reports "PyTorch reserved at most 1.42 GiB". The registered pilot log also records the device-wide sample the guard uses: 2,386,349,260 bytes against a limit of 2,684,354,560, which is 284 MiB of headroom and depends on other apps. R2 later failed on exactly this guard. The margin was in the registered data but not in the protocol's feasibility argument. | `N8/N8-protocol-draft.md:170`; `N8/pilot/PILOT_LOG.json` (`stage.guard_peaks.device_used_sampled` = 2386349260); `N8/OPERATIONAL_NOTES.md:57-59`; `b3_registry.py` output, last lines. | VERIFIED | A matter for N8's result report (state the margin with the pilot figures) |
| B8 | B | Suggestion | **Three statements about registered material cannot be checked from the public files.** (a) That the partition equals the sealed rule's output for `partition_seed` 1258837015: the corpus manifest (`be911db7…`) is not published. (b) That the pilot's source subject `9743b179…` differs from the sealed source "only in the pins … the hours … and the source README": only the hashes of the pilot's versions are published, so I can confirm which four files differ, not how. (c) Bound record `LR_SELECTION.json` (`fa760ba0…`) is not in the repository (inherited from N6 and N7). | (a) `N8/registry/n8-seed-registry/REGISTRY_AND_PARTITION_CHECK.json` asserts it; `DATA_AVAILABILITY.md:62`. (b) `N8/README.md:25`; `b3_registry.py` output: "pilot subject -> sealed subject: ['MATCHED_OWNER_RUN.ps1', 'README.md', 'matched_plan.py', 'matched_registry.py']". (c) `N8/source/SOURCE_SUBJECT.json:6`; no file with that hash among the 1,430 tracked files. | UNVERIFIED; (a) needs the manifest's per-article sequence counts and text hashes, (b) needs the four pilot-subject files, (c) needs the record | Doc-only |
| B9 | B | Suggestion | **Three points of wording for the eventual result report.** (a) The joint label is REVERSAL_NOT_REPLICATED whenever both hypotheses are not CONFIRMED, including when one is INCONCLUSIVE or UNAVAILABLE. The report should give the two component labels beside it and not present that case as evidence of no reversal. (b) "No multiplicity correction is needed" holds for the joint claim (I simulated 0.0249 at the boundary of the null). A single hypothesis reported "as it stands" is controlled at 2.5% on its own, and the chance that at least one of the two is confirmed in error can reach 5%. (c) Section 8 says a retry "reports how each width's new E0 losses compare with the first attempt's". The sealed code reports only SAME, DIFFERENT or ABSENT by SHA-256, and nothing registered computes a size. | `N8/N8-protocol-draft.md:84-90`, `:31-32`, `:181`; `N8/analysis/n8_analysis.py:411-422`; `e0_against_first_attempt` in `N8/source/matched_worker.py` (hunk 42, `N8/CHANGES.md:756`); `b2_power.py` output. | VERIFIED | A matter for N8's result report |
| B10 | B | Suggestion | **The README table counts 28 readouts while listing 29 items.** "E0, E0.25, E0.5, E1, then every 64 updates from update 2,048 to 3,584 (28 in all)": the 28 excludes E0, as the protocol's "28 readouts per arm instead of 10" does. | `N8/README.md:52`; `N8/N8-protocol-draft.md:42`, `:154`; `N8/source/matched_plan.py:64`. | VERIFIED | Doc-only |
| F-b1 | F | Minor | **Dates in the record mix UTC and local time without saying so.** The merge is 2026-11-14T18:19:19Z, which is 15 November 01:19:19 at +07:00; the living pages date the registration "14 November 2026". The `v2.0` release, 26 minutes later (18:45:38Z), is dated "15 November". The seed draw's "14 November" is local (receipt `finished_local` 2026-11-14 01:09:29). Run events are in local time, and R1 has no clock time in `OPERATIONAL_NOTES.md`. So the registration and R1 fall on the same local date, and their order cannot be read from the published dates alone. It follows from the design (the recorded builder holds the merge hash, and each terminal binds its approval record), which only the unpublished run records can show. | `git log`: `c6f98b2 2026-11-15T01:19:19+07:00`, `88ac496 2026-11-15T01:44:07+07:00`; GitHub PR #1 `merged_at 2026-11-14T18:19:20Z`; release v2.0 `published_at 2026-11-14T18:45:38Z` (section 5); `README.md:11`, `CURRENT_CLAIMS.md:221`, `NATURAL_TEXT_STUDIES.md:187`, `reports/README.md:34`; `PUBLICATION_NOTES.md:78`, `:99`; `N8/registry/n8-seed-registry/SEED_DRAW_RECEIPT.json`; `N8/OPERATIONAL_NOTES.md:49-53`. | VERIFIED (that R1 started after the merge is UNVERIFIED on public files; R1's claim time or its `APPROVAL_RECORD.json` would verify it) | Doc-only |
| F-b2 | F | Suggestion (for auditor D) | **The guard's highest device-wide reading is the same to the byte in the pilot and in every completed draw.** It is 2,386,349,260 bytes on 13 November (pilot) and, per the notes, in n01–n05 and in X2's n06. With the worker's own peak constant at 1,522,532,352 bytes, the memory in use outside the worker would be the same 863,816,908 bytes at each draw's peak on four days. I cannot tell from public files whether this is a fixed overhead or a sign that the guard's reading does not always follow other apps. It bears on how much the 600 MiB start check protects. | `N8/pilot/PILOT_LOG.json` (`stage.guard_peaks`); `N8/OPERATIONAL_NOTES.md:59-60`, `:72`. | UNVERIFIED (the per-draw `peaks` in the run receipts, and a controlled reading with a second GPU app open, would verify it) | A matter for N8's result report |

**Note on B1's severity.** I rate it Major because the folder's stated purpose is "to let anyone check that the hypotheses, the analysis and the readings were fixed before any result existed" (`N8/README.md:3`), and for the step from run folders to the analysis inputs that is not yet supported. Calibration: with every draw COMPLETE under a terminal, any reasonable loader gives the same inputs, so the labels are at risk only in edge cases (a receipt and terminal that disagree, a binding or hash that fails, a retried draw). It becomes a documentation matter once the loader is published with its hash before any p\* exists.

#### 2. Rejected concerns: checked and found sound

- **`CHANGES.md` against the real diff.** My own byte comparison finds 24 files identical, 8 changed, 1 added and 2 dropped.
  - `CHANGES.md` lists the same 24, the same 7 changed files plus the regenerated `SOURCE_SUBJECT.json`, the added `n7_matched_data.py` (byte-equal to N7's `matched_data.py`) and the two dropped files, all with correct hash prefixes.
  - Applying its 61 hunks as a patch to N7's files reproduces N8's seven files byte for byte. An independent `difflib` diff with one line of context equals the listed hunks.
  - There are 61 notes, numbered 1–61, one per hunk, and no line-ending change in any changed file.
- **Each change against the section it cites.** I read all 61 hunks. The substantive ones follow from the cited sections:
  - readouts and one rate (§3; `READOUTS` gives updates 256, 512, 1,024 and 2,048–3,584 in steps of 64, 28 in all), and the match path (§5, §6);
  - N7's articles excluded, N7's registry pinned and the study-folder census (§4);
  - saved orders, kept E0 states and the 8 GB check before R1 (§3);
  - R1–R8 and X1–X8, with admission on the first attempt's terminal (§8).
  
  The training and evaluation code is in files that are byte copies of N7's, or in lines of `matched_worker.py` that no hunk touches. The model has no dropout and batch orders come from seeded generators (`N8/source/text_engine.py:53`), so denser readouts do not alter training.
- **`SOURCE_SUBJECT.json`.** Its SHA-256 is `9bdea3a9…`, and its 31 listed files match in bytes and hash.
  - The only unlisted files are itself and `AUTHORIZATION.json`, which `disabled_authorization_sha256` binds.
  - Its changed, dropped, new and byte-copy lists equal my diff, and its five registry and partition hashes equal the published files.
  - N7's sealed-source folder hashes to N7's subject `7ef133ad…`.
- **`HASHES.json`.** All 17 single-file hashes and all grouped hashes equal the published files, except the two disclosed cases: the builder (`c31fd4aa…` now, `30765693…` registered) and `tests-retired/test_draw_command.py` (named, not published). Every hash prefix quoted in the protocol, the two READMEs and `CHANGES.md` prose matches a hash I can compute.
- **Seed registry.** I re-derived it with my own code from `DRAW.json` (1,024 bytes, 256 little-endian uint32) and `EXCLUSIONS.json` (4,370 values).
  - The 98 role values equal `REGISTRY.json`; the first 98 candidates were all accepted.
  - The nearest exclusion is 37,913 away and the nearest other role 112,876, as the check record says.
  - The pilot's five seeds, and every role value and exclusion list of N7, N6, N5 and the three other published registries, are in N8's exclusions.
  - The claim, registry, receipt and check record agree with each other and with the sealed source's 13 registry-source hashes.
- **Partition.** It has 24 groups n01–n24, each of 16,384 distinct sequences, 393,216 in all.
  - It uses 9,500 articles, none shared between groups; 9,500 + 4,539 left over = 14,039.
  - It has no article or sequence in common with N7's published partition (2,412 articles, 98,304 sequences).
  - Per-draw counts equal `DISCLOSURE_FIGURES.md` and the check record.
  - Its hash equals the pin in `source/matched_plan.py`, the registry, the receipt and `HASHES.json`.
- **Protocol numbers.**
  - 24 × 16,384 = 393,216, and 393,216 + 24 × 327 = 401,064 ≤ 582,603.
  - The fresh pool is 14,039 articles and 582,603 sequences in the count file, the registry and the partition; 13,511 = 11,099 + 2,412.
  - Kept states come to 4.62 GiB; 48 × 28 = 1,344 and 24 × 10 = 240.
- **Pilot log against section 7.** Every figure matches:
  - 43.6 s (22.0 + 21.6), 2,528 s per draw, cap 3,097 s;
  - 867 s (55 / 242 / 570) and 1,660 s (101 / 462 / 1,097), evaluation share 0.68;
  - 7,629 s measured and 7,186 s projected, 1.42 GiB, about 17 h for eight runs.
  
  The log holds no loss and no p\*, and its seeds equal those in `PILOT_COMMAND.txt`.
- **Seals.** From the pending seal to the sealed subject, exactly `matched_plan.py` (five pin lines), `README.md` (two status lines) and `MATCHED_OWNER_RUN.ps1` (the hours text, two lines) changed, as the README says. The draw ran on the pending seal `9209b566…`.
- **Power argument (post hoc check).** Exact noncentral-t power and a simulation agree with the table.

  | Draws | H1 | H2 | Joint lower bound |
  |---|---|---|---|
  | 12 | 0.84 | 0.60 | 0.44 |
  | 16 | 0.94 | 0.74 | 0.68 |
  | 20 | 0.98 | 0.84 | 0.82 |
  | 24 | 0.99 | 0.91 | 0.90 |

  - With the protocol's rounded inputs H2 at 16 draws is 0.7453; with N7's unrounded values it is 0.7445, which is the table's 0.74.
  - Full effects at 8 draws give 0.917 ("at least 0.92" is that figure rounded). Two-thirds effects with SDs × 1.5 at 24 draws give 0.806 (0.81).
  - The planning effects and SDs are N7's published values halved (P1 +0.009088, SD 0.004845; S3 −0.004542, SD 0.003245).
  - For context, not in the protocol: an SD from six draws is uncertain by a factor of 0.62 to 2.45, and at half effects with SDs × 1.5 the lower bound falls to 0.43.
- **Statements in sections 1 and 6.**
  - S3's interval includes 0 without m03 or without m05 (published N7 values).
  - The lower t limit is concave in the contrasts, so its minimum over the box of brackets is at a vertex (also checked on 200 random boxes).
  - N7's P1 read width 768 at epochs 2.19–2.48, inside N8's path from 2.0 to 3.5.
  - N7's p\* values are near 0.10, far from the saturation bound. So the lower-case "saturated" in the availability rule (line 79) against the SATURATED rule (lines 92–95) is not a practical ambiguity, and the registered code settles it.
- **After registration.** The folder's tree is identical at the PR commit `aaafa2e` and the merge `c6f98b2` (74 files).
  - Between the merge and `v2.1` only `README.md` (additions, and one paragraph extended) and `tools/build_n8_activation.py` (two lines) changed, and four files were added.
  - No file that `HASHES.json` or `SOURCE_SUBJECT.json` binds changed other than the builder.
  - PR #1's `merge_commit_sha` is `c6f98b2`, GitHub reports its signature valid, and `n8-registration` points at it (a lightweight tag).
- **`write_hashes.py --check`.** I did not run it. From its code (`:20`, `:34`) it reads `DRAW_COMMAND.txt`, which is not published, so on the public copy it should stop with `FileNotFoundError` before comparing anything. My `b3_registry.py` is an equivalent on the published files.

#### 3. To settle before N8 resumes

1. **The analysis entry point (B1).** A dated note, and the loader/driver published with its SHA-256 before any p\* is computed, ideally before R3. It can be tested without reading a loss, on the worker's test doubles. It needs to fix:
   - the criterion for a completed draw (for example a COMPLETE receipt that agrees with the terminal's stage records, as N7's `load` required);
   - which run a retried draw is read from;
   - which failed binding, hash or layout check refuses the analysis and which makes a draw failed;
   - where the weights and the orders are read from;
   - the files the analysis writes.
2. **A run with no terminal (B2).** A dated note saying whether its draws are failed and excluded, whether receipts without a terminal count, and whether anything other than X<k> may repeat them. If the answer departs from section 8, it is a deviation and should be called one.
3. **The end of the study (B3).** A dated note saying that the single analysis runs once every draw is complete or has failed twice, and on what dated declaration, made before any p\* is computed, a study that is not resumed is closed as INCOMPLETE.
4. **For the supervising session.** F-b1 (state the merge time with its zone, and R1's claim time) and F-b2 (the constant guard reading) belong with area D's check of the runs.

#### 4. Scripts I wrote (all post hoc; all read only the clone)

Sources are in `C:\Users\rafli\AppData\Local\Temp\swa21\b\scratch\`; they are not reproduced here. Command for each: `"C:\Users\rafli\AppData\Local\Programs\Python\Python312\python.exe" -I -B -X utf8 <script> "C:/Users/rafli/AppData/Local/Temp/swa21/b/repo"`. Full outputs are beside them as `*.out`.

##### `b1_source_diff.py` (post hoc): N8 `source/` against N7 `sealed-source/`, `SOURCE_SUBJECT.json`, and `CHANGES.md` applied as a patch

```
N7 sealed-source files: 34 | N8 source files: 33
identical: 24
changed  : ['AUTHORIZATION.json', 'MATCHED_OWNER_RUN.ps1', 'README.md', 'SOURCE_SUBJECT.json', 'matched_data.py', 'matched_plan.py', 'matched_registry.py', 'matched_worker.py']
added    : ['n7_matched_data.py']
dropped  : ['PROTOCOL.md', 'matched_analysis.py']
  added n7_matched_data.py sha b634f4b74157d127 byte-equal to N7 file(s): ['matched_data.py']

SOURCE_SUBJECT.json sha256: 9bdea3a9715b05393afe6713ddc696834dd344c3485c4e1a6ed0fa222f44bb6b
files listed: 31 | mismatching bytes/sha: []
in source/ but not listed: ['AUTHORIZATION.json', 'SOURCE_SUBJECT.json']
listed but not in source/: []
changed_from_n7 (subject): ['matched_plan.py', 'matched_data.py', 'matched_registry.py', 'matched_worker.py', 'MATCHED_OWNER_RUN.ps1', 'README.md'] | equals my changed minus unlisted: True
dropped_from_n7 (subject): ['matched_analysis.py', 'PROTOCOL.md'] | equals mine: True
new_files (subject): ['n7_matched_data.py'] | equals mine: True
byte_copies_of_n7_source keys equal my identical set (minus unlisted): True | values: {'7ef133ad0120d0852c93ebe65f020718f51cebbf75abd43c29f89cdec8674f56'}
N7 SOURCE_SUBJECT.json sha256: 7ef133ad0120d0852c93ebe65f020718f51cebbf75abd43c29f89cdec8674f56
disabled_authorization_sha256 matches source/AUTHORIZATION.json: True | AUTHORIZATION.json: {'enabled': False, 'execution_ready': False, 'note': 'Sealed disabled source of the dense-readout replication (N8); activations are built per run by the pinned builder after owner approval and after the public registration is merged.'}
  subject draw_sha256 == sha256(DRAW.json): True
  subject exclusions_sha256 == sha256(EXCLUSIONS.json): True
  subject partition_sha256 == sha256(PARTITION.json): True
  subject policy_sha256 == sha256(SEED_REGISTRY_POLICY.md): True
  subject registry_sha256 == sha256(REGISTRY.json): True
  bound record reports/natural-text-fewepoch-seed-registry-20261101-01/REGISTRY.json: MATCH
  bound record reports/natural-text-matched-analysis-20261105-01/ANALYSIS.json: MATCH
  bound record reports/natural-text-matched-seed-registry-20261104-01/REGISTRY.json: ABSENT in clone
  bound record reports/natural-text-peak-analysis-approval-20261103-01/pinned-records/LR_SELECTION.json: ABSENT in clone
  bound record reports/natural-text-peak-seed-registry-20261103-01/REGISTRY.json: ABSENT in clone
N7 subject lists 32 files; N7 files mismatching their own subject: [] | N7 unlisted: ['AUTHORIZATION.json', 'SOURCE_SUBJECT.json']

CHANGES.md sha256: 73f72f3a11e5045ac79e30332743186009bfefdd8ada0d6a42a33f02928edd77 | CR bytes in it: 0
CHANGES Unchanged lists 24 files; my identical set has 24
  listed as unchanged but not identical: []
  identical but not listed as unchanged: []
  hash prefixes wrong: []
CHANGES Added: [('n7_matched_data.py', 'b634f4b74157d127')] | Dropped: [('matched_analysis.py', '2108f0b287a0b355'), ('PROTOCOL.md', 'adf006ba144efccb')] | Regenerated: ['SOURCE_SUBJECT.json']
  added hash prefix ok: n7_matched_data.py True
  dropped hash prefix ok (N7 file): matched_analysis.py True
  dropped hash prefix ok (N7 file): PROTOCOL.md True
CHANGES per-file sections: ['matched_plan.py', 'matched_data.py', 'matched_registry.py', 'matched_worker.py', 'MATCHED_OWNER_RUN.ps1', 'AUTHORIZATION.json', 'README.md']
  equals my changed set minus SOURCE_SUBJECT.json: True
matched_plan.py: fenced blocks 6, hunks 6, +40/-60 lines | patch(N7)==N8 bytes: True | my difflib(n=1) hunks identical to listed: True | (CRLF,LF) N7 (0, 89) N8 (0, 69)
matched_data.py: fenced blocks 7, hunks 7, +21/-18 lines | patch(N7)==N8 bytes: True | my difflib(n=1) hunks identical to listed: True | (CRLF,LF) N7 (0, 62) N8 (0, 65)
matched_registry.py: fenced blocks 14, hunks 14, +46/-26 lines | patch(N7)==N8 bytes: True | my difflib(n=1) hunks identical to listed: True | (CRLF,LF) N7 (0, 228) N8 (0, 248)
matched_worker.py: fenced blocks 20, hunks 20, +111/-66 lines | patch(N7)==N8 bytes: True | my difflib(n=1) hunks identical to listed: True | (CRLF,LF) N7 (0, 342) N8 (0, 387)
MATCHED_OWNER_RUN.ps1: fenced blocks 10, hunks 10, +31/-15 lines | patch(N7)==N8 bytes: True | my difflib(n=1) hunks identical to listed: True | (CRLF,LF) N7 (0, 110) N8 (0, 126)
AUTHORIZATION.json: fenced blocks 1, hunks 1, +1/-1 lines | patch(N7)==N8 bytes: True | my difflib(n=1) hunks identical to listed: True | (CRLF,LF) N7 (0, 5) N8 (0, 5)
README.md: fenced blocks 3, hunks 3, +15/-16 lines | patch(N7)==N8 bytes: True | my difflib(n=1) hunks identical to listed: True | (CRLF,LF) N7 (0, 26) N8 (0, 25)
numbered notes: 61 | consecutive 1..N: True | total hunks: 61
notes citing no protocol section, brief, gate review or owner decision:
  50. [MATCHED_OWNER_RUN.ps1] Names N8.
  58. [AUTHORIZATION.json] Names N8; still disabled.
  60. [README.md] Lists N8's changed, new, dropped and byte-copied files.
```

The two registries shown as "ABSENT in clone" are published under `preregistration/…/seed-registry/REGISTRY.json` with the bound hashes (`bee57882…`, `0e8b0528…`). `LR_SELECTION.json` is not in the repository (B8c).

##### `b2_power.py` (post hoc): the power argument, NumPy only; uses N7's published per-draw values and no N8 data

```
check of my t quantiles: t(.975,5) = 2.570582 (2.570582), t(.975,23) = 2.068658 (2.068658), t(.975,7) = 2.364624 (2.364624)
N7 P1: n=6 mean=+0.009088 sd=0.004845 interval=[+0.004004, +0.014172]  half effect=+0.004544  d(full)=1.8759  d(half)=0.9379
N7 S3: n=6 mean=-0.004542 sd=0.003245 interval=[-0.007947, -0.001137]  half effect=-0.002271  d(full)=1.3999  d(half)=0.6999

protocol's planning values: H1 d = 0.9361, H2 d = 0.7006
draws | H1 exact (MC) | H2 exact (MC) | Bonferroni lower bound | protocol table
   12 | 0.8389 (0.8388) | 0.5997 (0.6001) | 0.4386 | (0.84, 0.6, 0.44)
   16 | 0.9377 (0.9373) | 0.7453 (0.7451) | 0.6830 | (0.94, 0.74, 0.68)
   20 | 0.9776 (0.9781) | 0.8441 (0.8440) | 0.8217 | (0.98, 0.84, 0.82)
   21 | 0.9828 (0.9828) | 0.8628 (0.8623) | 0.8457 | 
   22 | 0.9869 (0.9872) | 0.8795 (0.8798) | 0.8664 | 
   23 | 0.9900 (0.9900) | 0.8944 (0.8944) | 0.8844 | 
   24 | 0.9924 (0.9925) | 0.9076 (0.9074) | 0.9000 | (0.99, 0.91, 0.9)

same table with the unrounded N7 values (H1 d = 0.9379, H2 d = 0.6999):
   12 | 0.8403 | 0.5988 | 0.4392
   16 | 0.9385 | 0.7445 | 0.6830
   20 | 0.9780 | 0.8434 | 0.8215
   24 | 0.9926 | 0.9070 | 0.8996
    8 draws, full unrounded effects: H1 0.9943  H2 0.9220  lower bound 0.9163
   24 draws, two-thirds effects, SDs x 1.5, unrounded: H1 0.9743  H2 0.8311  lower bound 0.8055

full N7 effects (protocol: 8 draws give joint power of at least 0.92):
  n=6: H1 0.9509  H2 0.7820  lower bound 0.7330
  n=7: H1 0.9826  H2 0.8679  lower bound 0.8505
  n=8: H1 0.9942  H2 0.9225  lower bound 0.9166
two-thirds of N7 effects, SDs x 1.5 (protocol: 24 draws give a lower bound of 0.81):
  n=20: H1 0.9415  H2 0.7524  lower bound 0.6939
  n=24: H1 0.9739  H2 0.8318  lower bound 0.8057

not in the protocol, for context (same rule, 24 and 20 draws):
  half effects, SDs x 1.5      n=24: H1 0.833  H2 0.592  lower bound 0.425  product (if independent) 0.493
  half effects, SDs x 1.5      n=20: H1 0.754  H2 0.509  lower bound 0.263  product (if independent) 0.384
  half effects, SDs x 2        n=24: H1 0.594  H2 0.376  lower bound 0.000  product (if independent) 0.223
  half effects, SDs x 2        n=20: H1 0.511  H2 0.318  lower bound 0.000  product (if independent) 0.163
  one-third effects, N7 SDs    n=24: H1 0.833  H2 0.592  lower bound 0.425  product (if independent) 0.493
  one-third effects, N7 SDs    n=20: H1 0.754  H2 0.509  lower bound 0.263  product (if independent) 0.384

95% interval for a true SD given an SD s estimated from 6 draws (normal draws): [0.624 s, 2.453 s]
simulated P(both CONFIRMED | H1 effect = 0, H2 effect = -5 SD), n = 24: 0.0249  (bound 0.025)
envelope: over 200 random boxes (3-8 draws), largest (vertex minimum of the lower limit minus the lowest of 20,000 sampled interior points): -7.093e-03 (<= 0 means no interior point was lower than the best vertex)
```

##### `b3_registry.py` (post hoc): `HASHES.json`, seed registry, partition, fresh-pool count, pins, seals, pilot log

52 of 52 checks passed. The three "pre-pin -> sealed" entries are my summaries of the diff lines the script printed; everything else is exact, and the full text is in `b3_registry.out`.

```
PASS  HASHES.json: 17 single-file hashes equal the published files  [[]]
PASS  HASHES.json: grouped file hashes equal the published files, except those listed  [differ: [('tools/build_n8_activation.py', 'c31fd4aa')]; named but not published: ['tests-retired/test_draw_command.py']]
      HASHES.json keys ending _sha256 with no published file checked above: ['draw_command_sha256', 'corpus_manifest_sha256', 'n7_partition_sha256']
      published files bound neither by HASHES.json nor by SOURCE_SUBJECT.json: ['.gitattributes', 'HASHES.json', 'OPERATIONAL_NOTES.md', 'README.md', 'RUN_COMMAND.ps1', 'X2_COMMAND.txt', 'check_run.py', 'source/AUTHORIZATION.json']
PASS  DRAW.json: 1,024 bytes of entropy
PASS  my re-derivation of the 98 role values from DRAW.json and EXCLUSIONS.json equals REGISTRY.json  [candidates used up to index 97; rejected before that: 0]
PASS  98 distinct values, each more than 2,048 from every exclusion and from each other  [nearest exclusion 37913, nearest other role 112876; the check record says 37913 and 112876]
PASS  registry decisions list equals my accept/reject sequence
PASS  registry binds its own draw, exclusions, policy and partition
PASS  exclusions: 4,370 values, sorted, unique; provenance union_values agrees
PASS  the pilot's five seeds are all in EXCLUSIONS.json  [{'adapt_order_seed': 90809628, 'benchmark_seed': 578352808, 'init_seed': 1188503724, 'pretrain_order_seed': 46458185, 'weight_seed': 1894175819}]
PASS  N7: every role value (26), every census-rule value of its REGISTRY.json (26) and its exclusion list (4316) are in N8's exclusions  [registry sha bee57882; nearest N8 role value to one of its values: 3876906]
PASS  N6: every role value (26), every census-rule value of its REGISTRY.json (26) and its exclusion list (not published) are in N8's exclusions  [registry sha 0e8b0528; nearest N8 role value to one of its values: 618034]
PASS  capacity-shift-followup-seed-registry-20261027-01: every role value (0), every census-rule value of its REGISTRY.json (61) and its exclusion list (4046) are in N8's exclusions  [registry sha 00f3ab61; nearest N8 role value to one of its values: 37913]
PASS  natural-text-fewepoch-seed-registry-20261101-01: every role value (46), every census-rule value of its REGISTRY.json (46) and its exclusion list (4236) are in N8's exclusions  [registry sha 75db913d; nearest N8 role value to one of its values: 88404]
PASS  natural-text-ladder-seed-registry-20261028-01: every role value (46), every census-rule value of its REGISTRY.json (46) and its exclusion list (4158) are in N8's exclusions  [registry sha 8ce7d597; nearest N8 role value to one of its values: 540657]
PASS  natural-text-lateturn-seed-registry-20261031-01: every role value (18), every census-rule value of its REGISTRY.json (18) and its exclusion list (4209) are in N8's exclusions  [registry sha b9b6a882; nearest N8 role value to one of its values: 2983161]
PASS  N8's registry pins N7's registry and partition as published
PASS  claim and registry: registry-source hashes equal the sealed source files (13 files)
PASS  receipt: registry, partition, draw script and disclosure script hashes
PASS  receipt: the draw ran on the pending seal kept in seal/pre-pin  [2026-11-14 01:09:29]
PASS  post-draw check record: 16 checks, all ok
PASS  partition: 24 groups n01-n24 in order, n = 16,384
PASS  each group: exactly 16,384 distinct sequences
PASS  groups are disjoint by sequence (393,216 distinct) and by article  [9500 articles in all; left over 4539; sum 14039]
      partition pool record: {'assigned_articles': 13511, 'eligible_articles': 27859, 'fresh_articles': 14039, 'fresh_sequences': 582603, 'removed_repeats_inside_the_pool': 215, 'removed_text_duplicates_of_assigned': 94, 'sets_of_repeats_inside_the_pool': 107, 'unused_articles': 14348}
PASS  articles used + left over = 14,039 fresh articles
PASS  no N8 article or sequence is in N7's published partition  [N7: 2412 articles, 98304 sequences, left over 14039]
      N6: no PARTITION.json published; not checked
PASS  N7's left-over articles (14,039) equal N8's fresh pool size
PASS  DISCLOSURE_FIGURES.md: articles and sequences per draw equal the partition
PASS  check record: articles and sequences per draw equal the partition
PASS  each group's sequences form at most as many consecutive runs as it has articles  [runs 361-418]
PASS  fresh pool: count file = registry record = 14,039 articles and 582,603 sequences
PASS  24 x 16,384 = 393,216; + 24 x (328 - 1) = 401,064 <= 582,603
PASS  count: assigned 13,511 = 11,099 (N5, N6) + 2,412 (N7); N7 pool 16,451 - 2,412 = 14,039
PASS  N7's published partition holds 2,412 articles in m01-m06  [2412]
PASS  count tool hash and source hashes agree with HASHES.json and the sealed source
PASS  matched_plan.py pins: policy, registry, exclusions, draw, partition
PASS  matched_registry.py POLICY_SHA256 and N7_REGISTRY_SHA256; matched_data.py N7_PARTITION_SHA256
PASS  builder (v2.1): EXPECTED_SUBJECT, and PUBLIC_REGISTRATION subject and pilot-log hash
      N8-protocol-draft.md: 5 hash prefixes quoted; not matching any hash I can compute from published files: []
      README.md: 6 hash prefixes quoted; not matching any hash I can compute from published files: []
      source/README.md: 2 hash prefixes quoted; not matching any hash I can compute from published files: []
      CHANGES.md: 2 hash prefixes quoted; not matching any hash I can compute from published files: []
      files whose hash differs, pilot subject -> pending seal : ['MATCHED_OWNER_RUN.ps1', 'README.md', 'matched_plan.py', 'matched_registry.py']
      files whose hash differs, pending seal -> sealed subject: ['MATCHED_OWNER_RUN.ps1', 'README.md', 'matched_plan.py']
      files whose hash differs, pilot subject -> sealed subject: ['MATCHED_OWNER_RUN.ps1', 'README.md', 'matched_plan.py', 'matched_registry.py']
PASS  pending seal -> sealed: exactly matched_plan.py, README.md and MATCHED_OWNER_RUN.ps1
PASS  pilot subject -> sealed: exactly matched_plan.py, matched_registry.py, MATCHED_OWNER_RUN.ps1 and README.md (as the README says)
PASS  the pre-pin copies are the files the pending seal lists
PASS  the pilot log names the pilot subject and the pilot tool
      --- pre-pin -> sealed: matched_plan.py       [summary: 5 lines; registry_sha256, exclusions_sha256, draw_sha256, approval_id and PARTITION_SHA256 go from None to their values]
      --- pre-pin -> sealed: README.md             [summary: 2 lines; "This package has not run…" and "SEALED_DISABLED…"]
      --- pre-pin -> sealed: MATCHED_OWNER_RUN.ps1 [summary: 2 lines; $hours='about 2.1' -> 'about 2.3 h wall time (2.1 h on the worker clock)', and the start message]
      SOURCE_SUBJECT pins_pending: pilot True, pre-pin True, sealed False
      SOURCE_SUBJECT status: pilot 'SEALED_DISABLED', pre-pin 'SEALED_DISABLED', sealed 'SEALED_DISABLED'
      SOURCE_SUBJECT has_run: pilot False, pre-pin False, sealed False
      SOURCE_SUBJECT runtime_authorized: pilot False, pre-pin False, sealed False
PASS  pilot log vs protocol section 7: benchmark 43.6 s (22.0 + 21.6)
PASS  pilot log vs protocol section 7: per draw 2,528 s = 42.1 min, cap 3,097 s
PASS  pilot log vs protocol section 7: width 512: 867 s; 55 / 242 / 570
PASS  pilot log vs protocol section 7: width 768: 1,660 s; 101 / 462 / 1,097
PASS  pilot log vs protocol section 7: evaluation about two thirds
PASS  pilot log vs protocol section 7: run of three: 7,629 s measured, 7,186 s projected; both under 21,600 s
PASS  pilot log vs protocol section 7: PyTorch reserved at most 1.42 GiB
PASS  pilot log vs protocol section 7: eight runs: about 17 h on the worker clock
PASS  pilot log vs protocol section 7: 28 readouts per record; 12 files; orders 524,288 bytes = 4 epochs x 16,384 x 8
PASS  pilot log vs protocol section 7: status PASS, real, no loss read, no p* fitted, run folder deleted
PASS  pilot log vs protocol section 7: the pilot's draw is N7's m01, none of it in N8's fresh pool
      evaluation share 0.682; device-wide GPU memory sampled by the guard, peak 2,386,349,260 bytes = 2.222 GiB; guard limit 2.5 GiB = 2,684,354,560; headroom 284 MiB
      kept E0 states: (67,497,092 + 138,986,628) x 24 = 4,955,609,280 bytes = 4.62 GiB (protocol: about 4.6 GiB)

52 of 52 checks passed
```

##### `b4_n7_loo.py` (post hoc, descriptive, N7's published `MATCHED.csv`)

```
S3: all six: -0.004542 [-0.007947, -0.001137]
   without m01: -0.004870 [-0.009234, -0.000506]  includes 0: False
   without m02: -0.005423 [-0.008787, -0.002059]  includes 0: False
   without m03: -0.004173 [-0.008498, +0.000153]  includes 0: True
   without m04: -0.004884 [-0.009235, -0.000533]  includes 0: False
   without m05: -0.004318 [-0.008758, +0.000121]  includes 0: True
   without m06: -0.003584 [-0.006693, -0.000474]  includes 0: False
P1: all six: +0.009088 [+0.004004, +0.014172]
   without m01: +0.008564 [+0.002079, +0.015050]  includes 0: False
   without m02: +0.008859 [+0.002179, +0.015540]  includes 0: False
   without m03: +0.009272 [+0.002576, +0.015968]  includes 0: False
   without m04: +0.008098 [+0.002276, +0.013921]  includes 0: False
   without m05: +0.008832 [+0.002163, +0.015501]  includes 0: False
   without m06: +0.010901 [+0.008217, +0.013586]  includes 0: False
P1 read_at_readout (epochs): [2.249, 2.39, 2.302, 2.189, 2.231, 2.476] -> N8 path covers epochs 2.0 to 3.5
```

#### 5. Commands that matter, with exact output

Run in `C:\Users\rafli\AppData\Local\Temp\swa21\b\repo`; `D` = `preregistration/natural-text-dense-replication-20261114`.

**The builder at the registration tag against `v2.1`** (`git diff n8-registration v2.1 -- $D/tools/build_n8_activation.py`; the only hunk):

```
@@ -27,8 +27,8 @@ from pathlib import Path
 ROOT = Path(r'D:\sequence-weighting-research')          # the closed record: earlier registries and the corpus, read only
 STUDY = Path(r'D:\sequence-weighting-n8')
 SOURCE = STUDY / 'source'
-EXPECTED_SUBJECT = None                                  # PENDING: the sealed subject, set when the source is sealed (step 6)
-PUBLIC_REGISTRATION = None                               # PENDING: dict(url, merge_commit, tag, source_subject_sha256, pilot_log_sha256), after the merge
+EXPECTED_SUBJECT = '9bdea3a9715b05393afe6713ddc696834dd344c3485c4e1a6ed0fa222f44bb6b'   # the sealed subject, recorded by registration/apply_registration.py
+PUBLIC_REGISTRATION = {'url': 'https://github.com/rafli-hl/sequence-weighting/pull/1', 'merge_commit': 'c6f98b26669f5d29f30c576b6d800c1fc82c98eb', 'tag': 'n8-registration', 'source_subject_sha256': '9bdea3a9715b05393afe6713ddc696834dd344c3485c4e1a6ed0fa222f44bb6b', 'pilot_log_sha256': '251d0951e30250afa16cb998b06550358c09234d8a24c45166b08d0642347db6', 'pr_record_sha256': 'e8d92b7ec779ca63015ea857500ab887dd3d89611680e3fa8d4e5aa11e36f381'}   # recorded by registration/apply_registration.py
 PILOT_LOG = STUDY / 'pilot' / 'PILOT_LOG.json'
```

**Builder hashes** (`git show <ref>:$D/tools/build_n8_activation.py | sha256sum` for `n8-registration`, `v2.0`, `v2.1`):

```
30765693bd8bb4929ba060c193a610ecc987413d0c83b8035c6a9044228471d3 *-
c31fd4aa32873a1d025621f06bcc66e289c16ad86f64612c00dad76b1fd62904 *-
c31fd4aa32873a1d025621f06bcc66e289c16ad86f64612c00dad76b1fd62904 *-
```

**The folder across commits** (`git ls-tree -r --name-only <ref> -- $D | wc -l`, `git rev-parse <ref>:$D`, `git diff --name-status`):

```
aaafa2e: 74 files; tree aef1502c3be2c342cf9b2558514a0e17220b48e1
n8-registration: 74 files; tree aef1502c3be2c342cf9b2558514a0e17220b48e1
v2.0: 74 files; tree a1caf8f9deec0cbe35b65ca1bf8d24159b298cde
v2.1: 78 files; tree b55841f249d82bf983f3cc2150c1980688bf4d99
--- c6f98b2 vs v2.0 (folder):
M	preregistration/natural-text-dense-replication-20261114/README.md
M	preregistration/natural-text-dense-replication-20261114/tools/build_n8_activation.py
--- v2.0 vs v2.1 (folder):
A	preregistration/natural-text-dense-replication-20261114/OPERATIONAL_NOTES.md
M	preregistration/natural-text-dense-replication-20261114/README.md
A	preregistration/natural-text-dense-replication-20261114/RUN_COMMAND.ps1
A	preregistration/natural-text-dense-replication-20261114/X2_COMMAND.txt
A	preregistration/natural-text-dense-replication-20261114/check_run.py
```

`git diff c6f98b2 v2.1 -- $D/README.md | grep -E "^-[^-]"` shows one removed line: the "Not included, by design" paragraph, replaced by the same paragraph with two sentences added.

**The README note of B6:**

```
v2.0 README mentions 'two empty folders': 0
c1a2380 README mentions: 1
v2.1: 1
```

**Tags, commit times and GitHub (read-only GET requests):**

```
refs/tags/n8-registration commit c6f98b26669f5d29f30c576b6d800c1fc82c98eb  2026-11-15T01:19:19+07:00
refs/tags/v1.2 commit c4ae0e143526214b97d9740ee911997b45076413  2026-11-12T17:13:56+07:00
refs/tags/v2.0 commit 88ac49683770b147ee580285d640fcde517d36c3  2026-11-15T01:44:07+07:00
refs/tags/v2.1 commit 30548dbb789b2a117486fdf6f9ab9added680172  2026-11-23T12:09:20+07:00
{"base":"main","changed_files":81,"commits":1,"created_at":"2026-11-14T18:17:44Z","head":"aaafa2ed180c3c5c4c136f16fc3e7ef9a9515126","merge_commit_sha":"c6f98b26669f5d29f30c576b6d800c1fc82c98eb","merged":true,"merged_at":"2026-11-14T18:19:20Z","number":1,"state":"closed","title":"Register N8: dense-readout replication of N7"}
{"committer":"GitHub","date":"2026-11-14T18:19:19Z","reason":"valid","sha":"c6f98b26669f5d29f30c576b6d800c1fc82c98eb","verified":true,"verified_at":"2026-11-14T18:19:20Z"}
{"assets":[],"created_at":"2026-11-23T05:09:20Z","name":"v2.1","published_at":"2026-11-23T05:10:47Z","tag_name":"v2.1","target_commitish":"main"}
{"assets":[],"created_at":"2026-11-14T18:44:07Z","name":"v2.0","published_at":"2026-11-14T18:45:38Z","tag_name":"v2.0","target_commitish":"main"}
{"assets":[{"name":"n7-loss-arrays-v1.zip","size":14577377}],"created_at":"2026-11-12T10:13:56Z","name":"v1.2","published_at":"2026-11-12T10:25:53Z","tag_name":"v1.2","target_commitish":"main"}
```

**Search behind B1** (`grep -n -E "RECEIPT|TERMINAL|n8-r|runs/|runs\\\\|def load|__main__|argparse|sys.argv" analysis/*.py`, run in the N8 folder):

```
analysis/regenerate_n7_orders.py:37:if __name__ == '__main__':
analysis/regenerate_n7_orders.py:38:    if len(sys.argv) != 3: raise SystemExit(__doc__)
analysis/regenerate_n7_orders.py:39:    main(Path(sys.argv[1]), Path(sys.argv[2]))
analysis/test_on_n7.py:243:if __name__ == '__main__':
analysis/test_on_n7.py:244:    if len(sys.argv) != 4: raise SystemExit(__doc__)
analysis/test_on_n7.py:245:    raise SystemExit(main(Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])))
analysis/test_synthetic.py:212:if __name__ == '__main__':
```

**Searches behind B4** (summarised, not verbatim output):
- `git grep -n -I "e8d92b7e"` and `git grep -n -I "pr_record"` each match only `$D/tools/build_n8_activation.py:31`.
- `git grep -n -I "apply_registration"` matches `$D/tools/build_n8_activation.py:30` and `:31`, and one unrelated line, `preregistration/natural-text-matched-confirmation-20261104/HASHES.json:32`.

**Not done.** I did not run `verify_publication.py`, `write_hashes.py --check`, the analysis tests or any repository code (left to the supervising session). I opened nothing outside the clone, the scratch folder and the brief, changed nothing in the clone, and computed nothing from N8 data.

## Appendix 1C. Auditor C (area C)

### Audit of record v2.1 (commit 30548db): area C, N8's analysis code, and area F. Auditor C

**Two things about delivery first.**
- **`FINDINGS.md` was not written.** The Write tool refused it ("Subagents should return findings as text, not write report files"), and I did not work around that refusal with a shell command. This message is the whole report; please save it to `C:\Users\rafli\AppData\Local\Temp\swa21\c\scratch\FINDINGS.md` if you want the file.
- **Script sources are not pasted here** (47 KB). They are in the scratch folder, listed in section 4 with their SHA-256. Every command and its output is given below.

Scope: `preregistration/natural-text-dense-replication-20261114/analysis/` (`n8_analysis.py`, `test_on_n7.py`, `test_synthetic.py`, `regenerate_n7_orders.py`) against `N8-protocol-draft.md` sections 5, 6 and 8, and against N7's sealed source. `N8/` abbreviates `preregistration/natural-text-dense-replication-20261114/`, and `N7/` abbreviates `preregistration/natural-text-matched-confirmation-20261104/sealed-source/`. Names starting with `c0` are my scripts.

**Bottom line.** I found no rule of protocol sections 5 and 6 that `n8_analysis.py` implements wrongly, and no registered number or label that is wrong. On N7's published data the code reproduces the sealed statistics, every `MATCHED.csv` row, all 240 fits (bit for bit on this machine, which is the registered environment) and the three envelope values. The main finding is about what is not registered: the file is a library on in-memory inputs, and nothing registered reads N8's run folders (C1). The other findings are test-coverage gaps, one test pin that depends on version strings, and wording.

**Not verified by me.**
- `test_on_n7.py` was not run (no PyTorch here; the supervising session runs it).
- S-b's N7 figures are therefore not reproduced. I checked S-b's construction of its sets on synthetic orders only (c07).
- C3 is PLAUSIBLE: read, not executed.

#### 1. Findings

| ID | Area | Severity | Finding | Evidence | Status | Fix type |
|---|---|---|---|---|---|---|
| C1 | C | Major | **The registered analysis has no entry point for N8's data.** `n8_analysis.py` takes in-memory `data` and `orders`. Nothing registered reads a run folder, decides which draws are completed or failed, chooses between a first attempt and its retry, checks arrays and orders against recorded hashes, refuses to fit before all runs have ended, or writes outputs. N7's sealed analysis did each of these, and `CHANGES.md` drops that file without replacing these parts. The step from run folders to the analysis inputs will therefore be fixed by code written after registration, when six draws' data already exist. No registered rule or number is wrong; the gap is the layer in front of the rules. | `N8/analysis/n8_analysis.py:16-19`: "Inputs. data[d] is None for a failed draw, or dict(weights=[...], arms={(width, tag): dict(e0=bytes, arrays=bytes, record=dict)})". The file has no `__main__` and no file access (section 5, command 5). `:414`: `completed = [d for d in plan['draws'] if per.get(d) is not None]`. N7: `N7/matched_analysis.py:61-102` (`load`: terminal present, fixture refused, subject, receipts against the terminal, SHA-256 and size of E0 and arrays, layout, M2 admitted on M1) and `:413-421` (command line on run folders, four output files). `N8/CHANGES.md:37`: "**Dropped** `matched_analysis.py` ...: N7's analysis; N8's is `analysis/n8_analysis.py` (§6)." Protocol `:99` "The sealed analysis runs on native Windows Python 3.12.10", `:176` "no look at any p\* before all 24 draws are complete". `N8/README.md:3` "let anyone check that the hypotheses, the analysis and the readings were fixed before any result existed". Concrete hazard: `N8/OPERATIONAL_NOTES.md:63` R2 left n06's `w768/E0.f32` in place, and `:74` "w768 is DIFFERENT" from X2's. Reproduction, c05 items 2-4: three draws passed as None, with nothing saying they failed, give `COMPLETE_WITH_FAILED_DRAWS` and labels; a failed draw left out of the mapping instead of set to None makes `analyse()` raise `KeyError` at `:572`, although `decide()` labels the study. | VERIFIED | Dated correction: a dated note and a newly published, hashed loader with its tests, before any N8 loss is read. The sealed file is not edited. |
| C2 | C | Minor | **Eight rule branches are exercised by no registered test.** (1) the 1e-9 margin of "entirely"; (2) a saturated bracket fit making a draw unavailable for H1; (3) H1's value at bound 32; (4) the 1e-3 flag of records against arrays; (5) NOT_OVERFIT's other two labels; (6) S-d leaving out saturated fits; (7) an undefined refit in the starting offset; (8) the 7.999 threshold itself. Also, no registered test runs `analyse()` from arrays on N8's own grid (28 readouts, 24 draws). On my constructed inputs the code is right in every one of these cases, so this is a gap in the tests, not an error in the code. | c06 part A: one-line mutants M1-M8 of `n8_analysis.py` leave all 30 checks of `test_synthetic.py`'s first five functions passing; three control mutants are detected. c06 part B: on N7 the mutated branches never arise (largest p\* 0.1489, no undefined fit, records differ by at most 8.55e-07, both arms NOT_OVERFIT, nearest interval limit to 0 is 0.000121), so `test_on_n7.py` cannot detect them either. `N8/analysis/test_synthetic.py:164` tests saturation on H2 only; `test_on_n7.py:38` runs `analyse()` on N7's plan. The unmutated code on these branches: c03 items 2 and 4, c05 items 1 and 6, c08 items 1-4. | VERIFIED | Doc-only: new, dated test files beside the sealed ones before the analysis (my scripts can serve). |
| C3 | C | Minor | **One check of `test_on_n7.py` pins a hash that contains library version strings.** `regenerate_n7_orders.py` writes `torch.__version__` and `numpy.__version__` into `ORDERS.json`, and the test requires that file's SHA-256 to equal a pin. A reader who follows the documented route (the CPU build of PyTorch 2.7.0, whose version string ends in `+cpu`) would regenerate identical orders but a different `ORDERS.json`, so that check would fail with "0 mismatches": 59 of 60. The environments recorded in the record use `2.7.0+cu126`. | `N8/analysis/regenerate_n7_orders.py:32`: `meta = dict(torch=torch.__version__, numpy=np.__version__, ...)`; `:3` "needs PyTorch (CPU); N7 used 2.7.0". `N8/analysis/test_on_n7.py:32` `ORDERS_SHA256 = '8ba4a3c2...'`; `:107` the check needs `sha(raw) == ORDERS_SHA256 and bad == 0 and len(out) == 12`. `reports/natural-text-matched-assistant-posthoc-20261111-01/RESULTS.json:4` `"torch": "2.7.0+cu126"`; `tools/requirements-posthoc.txt` tells readers to install the CPU build. To verify: your run. If that check alone fails and prints "0 mismatches", this is confirmed; the twelve `.i64` files can then be compared with `N8/HASHES.json:130-141`, which names each by SHA-256. | PLAUSIBLE (read, not run) | Doc-only: a dated note naming the version strings behind the pin, or pointing to the per-file hashes. |
| C4 | C | Suggestion | **A hypothesis labelled UNAVAILABLE still gets inferential output.** With 19 of 24 draws available, H1 has no interval and no envelope, but the result holds its 19 per-draw values, the sign test and 19 leave-one-draw-out intervals (18 draws each, with a side). The starting offset, S-a and S-d are computed whatever the labels. The protocol says only that the hypothesis is UNAVAILABLE; it does not say what is then shown. | `N8/analysis/n8_analysis.py:395-396`: the leave-one-out line precedes `return dict(out, status='UNAVAILABLE')`. c03 item 5: "label UNAVAILABLE ... per-draw values: 19 ... leave-one-out intervals: 19", one entry with `'side': 'ABOVE'`. Protocol `:78`. | VERIFIED | A matter for N8's result report: say in advance, in a dated note, that these are not read for an UNAVAILABLE hypothesis. |
| C5 | C | Suggestion | **One corner where the code's output differs from the protocol's wording.** "A flat interval holding the target is read at its earlier readout" (protocol `:68-69`). If that interval's later fit is undefined or saturated, the code makes the draw unavailable, although the reading needs only the earlier fit. The same holds for any bracket end that carries zero weight. This is N7's behaviour, copied. It needs two exactly equal recorded losses and an undefined fit, so it is very unlikely to arise. | `N8/analysis/n8_analysis.py:309`: `if p0 is None or p1 is None: return dict(base, status='UNDEFINED_FIT')`. c03 item 3: path `[(2.0, 4.25, 0.10), (2.0625, 4.25, None), (2.125, 4.20, 0.12)]` with target 4.25 gives `'status': 'UNDEFINED_FIT', 'weight': 0.0, 'p_at_bracket': [0.1, None]`. | VERIFIED | A matter for N8's result report, only if it arises. |
| F-c1 | F (protocol wording, shared with B) | Minor | **The saturation rule is not N7's, though the protocol says it is "carried over from N7" and "as in N7".** In N7 an unresolved refit made the whole statistic SATURATED, and a side that differed at bound 32 made it SATURATION_SENSITIVE; neither was read. In N8 an unresolved refit removes only that draw, and a resolved refit can never change a label, even if the bound-32 interval falls on the other side. The code follows N8's text. On N7 no fit came near the bound (largest p\* 0.1489), so this is unlikely to matter. | Protocol `:91-95`: "Rules carried over from N7 ... If the refit resolves, the label still uses the bound-8 value, as in N7 ... An unresolved refit makes that draw SATURATED". `N7/PROTOCOL.md:128`: "An unresolved refit makes the statistic SATURATED, and a side that differs at bound 32 makes it SATURATION_SENSITIVE. Neither is read." `N7/matched_analysis.py:216-220`. c03 item 4 (the label uses the bound-8 value). | VERIFIED | Doc-only: a dated note that N8's saturation rule differs from N7's in these two points. |

#### 2. Rejected concerns: what I checked and found sound

**The estimator.**
- `exponent`, `exponent_upper` and `objective_at` are text-identical to `N7/vendor/core.py` and `N7/text_analysis.py` (c01).
- `read_along` differs from N7's in one word of its docstring; `_betacf`, `betai` and `side` are identical.
- N8's `source/vendor/core.py`, `source/text_analysis.py` and `source/fewepoch_analysis.py` are byte copies of N7's.
- Gains are subtracted in float32, as in N7. All 240 N7 fits are bit-identical to `POINTS.csv` in the registered environment (c04 item 1).

**Section 5, matching.**
- **H1 target:** 512's recorded mean training loss at E3 (`:317`). On N7 the record's mean and the array mean differ by at most 8.55e-07, far below any bracket's width, so using the record (as N7 did) is immaterial.
- **Path:** the 25 readouts from 2.0 to 3.5, equal as floats to the sealed plan's `READOUTS` (c05 item 0).
- **Reading rule:** first bracketing interval in readout order, a flat interval read at its earlier readout, a target outside the path unavailable, the count of bracketing intervals reported (c03 item 3, and all 36 rows of `MATCHED.csv` in c04).
- **What is interpolated:** p\*, linearly in the matched quantity (`:310`). The same bracket and weight are reused by the bound-32 value and the starting offset.
- **H2:** both widths at 3.0 (update 3,072), no interpolation (`:319`).

**Section 6, test and labels.**
- **t interval:** df n − 1, exact quantile by bisection. I checked it by integrating the t density numerically for df 19-23 (c03 item 1) and against N7's sealed intervals (differences below 1e-12, c04). The registered closed-form check covers df 1-60. My own interval with a hard-coded quantile agrees to 5e-18 on N8's grid (c05 item 1).
- **The 1e-9 margin:** a lower limit of 5e-10 gives INCONCLUSIVE and 2e-9 gives CONFIRMED; the same holds for H2's upper limit (c03 item 2).
- **Sign test:** exact, two-sided, zeros dropped; equal to N7's sealed p values.
- **Minimum of 20:** 19 available gives UNAVAILABLE and REVERSAL_NOT_REPLICATED (registered test; c03 item 5). Labels and the joint label are as written (`:404-422`).
- **Study status:** 24, 23 and 20 completed give COMPLETE, then COMPLETE_WITH_FAILED_DRAWS twice. 19 gives INCOMPLETE with no statistic and no label, and `analyse()` then returns only the environment, the plan and the decision (c03 item 6, c05 item 5).
- **Saturation, as N8's text states it:** only fits at or above 7.999 are refitted (7.9985 is not, 7.9995 is; c08 item 4). A resolved refit keeps the bound-8 value in the label and reports the bound-32 value with the registered weight. An unresolved one makes the draw unavailable for H1, or for both hypotheses if it is 512 at E3 (c03 item 4).
- **NOT_OVERFIT:** per width, E3 minus E2, three labels with the 1e-9 margin (c08 item 1).
- **Records against arrays:** flagged above 1e-3, not gating (c05 item 6).

**Sensitivity analyses.**
- **Envelope.** The lower limit, mean − q·sd/√n, is linear minus a seminorm, so it is concave and its minimum over the box of brackets is at a vertex. The upper limit is convex, so its maximum is at a vertex too. The argument is right for both limits as reported (minimum lower, maximum upper). The code enumerates all 2^n vertices, so the result is exact up to rounding.
  - The registered test's direct enumeration of all 2^24 agrees (differences 4.3e-19 and 0).
  - My own brute force on N7 gives P1 +0.00007639, S1 −0.00005074, S4 −0.00026786, equal to the 23 November correction's values.
  - Only H1 gets an envelope, over its available draws.
- **Leave-one-draw-out:** equal to N7's sealed values within 5e-13.
- **Starting offset:** the offset is mean E0 of 768 minus mean E0 of 512 over training rows; 768 is refitted at the registered bracket ends and read with the registered weight (`:426-439`). On N7 it gives +0.00625 [−0.00008, +0.01257], 5/6, against AA-3's printed +0.0062 [−0.0001, +0.0126], 5/6.

**Secondary analyses.**
- **S-a** reproduces the 13 November audit to 8 decimals, read positions included.
- **S-c** reproduces the audit's four diagnostics within 5e-9 over 240 fits.
- **S-d** equals `ANALYSIS.json`'s `by_readout` D4 exactly.
- **S-b:** the sets, sizes, age differences and joint cell distances equal my own construction, written from `posthoc_exposure.py` and the audit's code, on synthetic orders (c07). Windows are quarter epochs and the readouts are 2.25, 2.5 and 2.75, as registered.

**Tests.**
- Their expected values come from independent sources: N7's sealed outputs (four files, SHA-256 pinned and matching the clone), the 12 and 13 November audits' printed output, the 11 November `RESULTS.json`, a closed-form t distribution, hand-computed sign tests and two independent enumerations. I found no expected value taken from the code's own output.
- `test_on_n7.py` has 60 checks, and `test_synthetic.py` has 37 without SciPy (38 with it), as the protocol states.
- `test_synthetic.py` runs with NumPy alone: 37 passed, 0 failed, exit 0.

**Integrity.** The four analysis files match `HASHES.json`. Neither they nor the protocol changed between the tag `n8-registration` and v2.1.

**Choices the code makes where the protocol is silent.** None changes a label rule; they are listed so the result report can state them.
- The target and path values are the worker's recorded means, not array means.
- The bound-32 value refits only fits at or above 7.999 (N7 refitted every fit the draw used).
- The starting offset does not refit at bound 32, and drops a draw whose refit is undefined.
- S-a needs 2 draws, and S-d has no minimum.
- The envelope uses bound-8 values.

#### 3. To settle before N8 resumes, or before its analysis runs

Nothing in the analysis code needs to change before more draws are trained. The items below should be settled by dated notes, without editing a sealed file. Preferably that happens before R3, and in any case before anything other than `check_run.py` opens an N8 loss file.

1. **The loader (C1).** Publish and hash it with its tests. The note should state:
   - a draw's weights, E0, arrays, records and orders all come from one run folder;
   - a retried draw is read from its retry only (for n06 that is X2, never R2's leftover `w768/E0.f32`);
   - a draw is failed only when both attempts left it incomplete, and is passed as None, not omitted;
   - nothing is fitted until every run R1-R8, and every retry that is due, has its terminal;
   - arrays are checked against the SHA-256 in their records, and each order row against `INPUTS.json`'s `epoch_order_sha256` (`n8_analysis.order_sha256` gives the same hash);
   - which of N7's `load()` checks are kept, and what the output files are;
   - whether the run stops when `environment()['matches_registered']` is false, since the code only reports it.
2. **An unrun retry.** Say how a draw is classified if a run fails and its retry is never made. The code cannot tell "failed" from "not run" (c05 item 4).
3. **UNAVAILABLE (C4) and the flat-interval corner (C5).** One sentence each on what is read.
4. **Saturation wording (F-c1).**
5. **Tests for the branches of C2,** as new dated files, and the version strings behind the `ORDERS.json` pin (C3).

#### 4. Scripts I wrote (all post hoc)

All are in `C:\Users\rafli\AppData\Local\Temp\swa21\c\scratch`. Python is `C:\Users\rafli\AppData\Local\Programs\Python\Python312\python.exe -I -B` (3.12.10, NumPy 2.5.3, Windows; `n8_analysis.environment()` reports `matches_registered: True`). `<REPO>` is `C:/Users/rafli/AppData/Local/Temp/swa21/c/repo`, `<BUNDLE>` is `C:/Users/rafli/AppData/Local/Temp/swa21/bundle/n7-loss-arrays`, `<SCRATCH>` is the scratch folder. No script reads anything outside these three folders, and none reads N8 data. Each output is also saved there as `c0N_output.txt`.

| Script | SHA-256 | What it does |
|---|---|---|
| `c01_verbatim.py` | `6a125f68b83cb9a9ef8a25937d1919c44bb3925686fabf71928d41deb52d0da8` | Compares functions of `n8_analysis.py` with N7's sealed source |
| `c02_n7_refit.py` | `4aca7d22a58e7610be31784c325a8ac312d406be3941bb18ceecdc15c8064c0d` | Refits N7's 240 p\* from the bundle with `n8_analysis.points`; caches them in `c02_per.pkl` |
| `c03_constructed.py` | `cee273cde864b6be39731f8e2ae1a416229d892f11a68ecb483fcf2bf98fa334` | Constructed inputs, rule by rule |
| `c04_n7_check.py` | `caa0d10ce872394d221e433da68484f83d123c5ec695e42b48e7626eb1cb5b31` | `n8_analysis` on N7's published data against the sealed outputs and my own arithmetic (no S-b) |
| `c05_end_to_end.py` | `02910458f07bcf02b83f54fb49920e2cae4e2c72fb993a30129dc5f65abde20e` | `analyse()` on N8's grid with synthetic arrays; failed, absent and unrun draws |
| `c06_mutants.py` | `212e1161346d31ed985aa54cd2832b569c06f9727d0e07f086d273c80e0913b8` | Mutants of `n8_analysis.py` (written to `scratch/mutants/`) against `test_synthetic.py` |
| `c07_exposure_windows.py` | `7824c6c5422cee5563f962a6fb271bf82caa8121e51cfd5b3e20d61fb8e4b4f8` | S-b's sets on synthetic orders against my own construction |
| `c08_untested_branches.py` | `ed52d4e033c75705145028c1138ad292f35a013bf224af40bee86b743d96c051` | Four branches no registered test enters |
| `c_synth.py` | `001afc91aa850a086f965176aba2d80f05ff4e3c49ed4ff104d4d840047ebb7a` | Helper: synthetic arrays and orders on N8's grid, from fixed formulas |

##### c01: `python -I -B c01_verbatim.py <REPO>`

```
n8_analysis.py sha256 37b32fc547bb09f987f3131157f94ad171b5822b9d87d488bced3ae448f38538
exponent         vs N7 vendor/core.py         text identical: True; AST identical: True
exponent_upper   vs N7 text_analysis.py       text identical: True; AST identical: True
objective_at     vs N7 text_analysis.py       text identical: True; AST identical: True
read_along       vs N7 matched_analysis.py    text identical: False; AST identical: False
      --- N7
      +++ N8
      @@ -2 +2 @@
      -    """path_rows: (readout, value, p) in readout order along MATCH_PATH. The first interval whose two values hold the target gives the
      +    """path_rows: (readout, value, p) in readout order along the match path. The first interval whose two values hold the target gives the
_betacf          vs N7 fewepoch_analysis.py   text identical: True; AST identical: True
betai            vs N7 fewepoch_analysis.py   text identical: True; AST identical: True
p_two_sided      vs N7 fewepoch_analysis.py   text identical: False; AST identical: False
      --- N7
      +++ N8
      @@ -1 +1,3 @@
      -def p_two_sided(t, df): return betai(df / 2, 0.5, df / (df + t * t))
      +def p_two_sided(t, df):
      +    """P(|T| >= |t|) for Student's t with df degrees of freedom."""
      +    return betai(df / 2, 0.5, df / (df + t * t))
side             vs N7 matched_analysis.py    text identical: True; AST identical: True
sign_test        vs N7 matched_analysis.py    text identical: False; AST identical: False
      --- N7
      +++ N8
      @@ -2 +2 @@
      -    """The exact two-sided sign test; zeros are dropped. None if every value is zero."""
      +    """The exact two-sided sign test; zeros are dropped. p is None if every value is zero."""
      @@ -4,2 +4,2 @@
      -    if n == 0: return dict(positive=pos, negative=neg, p=None)
      -    return dict(positive=pos, negative=neg, p=min(1.0, 2 * math.fsum(math.comb(n, k) for k in range(min(pos, neg) + 1)) / 2 ** n))
      +    if n == 0: return dict(positive=pos, negative=neg, zeros=len(values), p=None)
      +    return dict(positive=pos, negative=neg, zeros=len(values) - n, p=min(1.0, 2 * math.fsum(math.comb(n, k) for k in range(min(pos, neg) + 1)) / 2 ** n))
draw_row         vs N7 matched_analysis.py    text identical: False; AST identical: False
      --- N7
      +++ N8
      @@ -1,5 +1,5 @@
      -def draw_row(per_d, spec):
      -    """One draw of one statistic: the reading of the second arm, and the contrast with the first arm at E3."""
      -    a, b = spec['first'], spec['second']; p_first = per_d[a][FINAL]['p']
      -    if spec['kind'] == 'matched':
      -        rows = [(e, per_d[b][e][spec['key']], per_d[b][e]['p']) for e in mp.MATCH_PATH]; r = read_along(rows, per_d[a][FINAL][spec['key']])
      +def draw_row(per_d, first, second, kind, key, final, path):
      +    """One draw of one contrast: the reading of the second arm, and p*(first, final) minus it (N7's draw_row)."""
      +    p_first = per_d[first][final]['p']
      +    if kind == 'matched':
      +        r = read_along([(e, per_d[second][e][key], per_d[second][e]['p']) for e in path], per_d[first][final][key])
      @@ -7 +7 @@
      -        p = per_d[b][FINAL]['p']; r = dict(status='READ', p_read=p, read_at_readout=FINAL) if p is not None else dict(status='UNDEFINED_FIT', read_at_readout=FINAL)
      +        p = per_d[second][final]['p']; r = dict(status='READ', p_read=p, read_at_readout=final) if p is not None else dict(status='UNDEFINED_FIT', read_at_readout=final)
leave_one_out    vs N7 matched_analysis.py    text identical: False; AST identical: False
      --- N7
      +++ N8
      @@ -1 +1 @@
      -def leave_one_out(values):
      +def leave_one_out(values, confidence=CONFIDENCE):
      @@ -5 +5,2 @@
      -        t = ta.tint([v for k, v in values.items() if k != d]); s = side(t); out[d] = dict(mean=t['mean'], interval=t['interval'], df=t['df'], side=s, excludes_zero=s != 'SPANS')
      +        t = t_interval([v for k, v in values.items() if k != d], confidence); s = side(t)
      +        out[d] = dict(mean=t['mean'], interval=t['interval'], df=t['df'], side=s, excludes_zero=s != 'SPANS')
fits_used        vs N7 matched_analysis.py    text identical: False; AST identical: False
      --- N7
      +++ N8
      @@ -1,4 +1,3 @@
      -def fits_used(spec, row):
      -    """The (arm, readout) fits a read draw uses."""
      -    second = [(spec['second'], e) for e in row['between']] if spec['kind'] == 'matched' else [(spec['second'], FINAL)]
      -    return [(spec['first'], FINAL)] + second
      +def fits_used(row, first, second, kind, final):
      +    """The (arm, readout) fits a draw's reading uses."""
      +    return [(first, final)] + [(second, e) for e in (row['between'] if kind == 'matched' else [final])]
N8 source/vendor/core.py byte-identical to N7 sealed-source/vendor/core.py: True f9320bae147f01bc
N8 source/text_analysis.py byte-identical to N7 sealed-source/text_analysis.py: True f53cf877b57ea424
N8 source/fewepoch_analysis.py byte-identical to N7 sealed-source/fewepoch_analysis.py: True fab5df60ab9d0acb
```

##### c02: `python -I -B c02_n7_refit.py <REPO> <BUNDLE> <SCRATCH>`

```
bundle files with a SHA-256 different from MANIFEST.json: 0
fitted m01, 30 s
fitted m02, 60 s
fitted m03, 92 s
fitted m04, 123 s
fitted m05, 157 s
fitted m06, 195 s
fits: 240 environment {'system': 'Windows', 'python': '3.12.10', 'numpy': '2.5.3', 'executable': 'C:\\Users\\rafli\\AppData\\Local\\Programs\\Python\\Python312\\python.exe', 'registered': {'system': 'Windows', 'python': '3.12.10', 'numpy': '2.5.3'}, 'matches_registered': True}
exit 0
```

##### c03: `python -I -B c03_constructed.py <REPO>`

```
=== 1. t quantile, df 19-23, against numerical integration of the t density (independent of the incomplete beta)
  df 19: quantile 2.093024054408; P(|T| <= q) by Simpson = 0.9500000000000 (want 0.95)
  df 20: quantile 2.085963447266; P(|T| <= q) by Simpson = 0.9500000000000 (want 0.95)
  df 21: quantile 2.079613844728; P(|T| <= q) by Simpson = 0.9500000000000 (want 0.95)
  df 22: quantile 2.073873067904; P(|T| <= q) by Simpson = 0.9500000000000 (want 0.95)
  df 23: quantile 2.068657610419; P(|T| <= q) by Simpson = 0.9500000000000 (want 0.95)
=== 2. "entirely" = beyond 0 by more than 1e-9 (H1 above, H2 below)
  margin 5e-10: H1 lower limit 5.000e-10 -> INCONCLUSIVE; H2 upper limit -5.000e-10 -> INCONCLUSIVE; joint REVERSAL_NOT_REPLICATED
  margin 2e-09: H1 lower limit 2.000e-09 -> CONFIRMED; H2 upper limit -2.000e-09 -> CONFIRMED; joint REVERSAL_REPLICATED
=== 3. reading rule
  target equal to a readout value, held first by a sloping interval: {'status': 'READ', 'between': [2.0, 2.0625], 'weight': 1.0, 'p_read': 0.11, 'intervals_holding_the_target': 3}
  flat first interval holding the target, its LATER fit undefined: {'status': 'UNDEFINED_FIT', 'between': [2.0, 2.0625], 'weight': 0.0, 'p_at_bracket': [0.1, None]}   | protocol wording expects: read at its earlier readout (p = 0.10)
  non-monotone path: {'status': 'READ', 'between': [2.0, 2.0625], 'weight': 0.5, 'p_read': 0.10500000000000001, 'intervals_holding_the_target': 3}
  target above / below every readout: ['TARGET_OUTSIDE_PATH', 'TARGET_OUTSIDE_PATH']
=== 4. saturation on the matched contrast (H1) and on 512 at E3 (no registered test exercises these branches)
  H1 unavailable: {'n02': 'SATURATED', 'n03': 'SATURATED'} | H2 unavailable: {'n03': 'SATURATED'}
  H1 n01 bound-8 value (label uses it): -1.5774999999999095 = p512 - (8 + w (p_hi - 8)) = -1.5774999999999095
  H1 n01 value at bound 32: -1.8774999999998934 = p512 - (9.5 + w (p_hi - 9.5)) = -1.8774999999998934
  H1 saturation flagged / saturated: ['n01', 'n02', 'n03'] ['n02', 'n03'] | interval at bound 32 present: True
  H2 saturation flagged / saturated: ['n03'] ['n03']
  labels: {'H1': 'INCONCLUSIVE', 'H2': 'CONFIRMED'} REVERSAL_NOT_REPLICATED | available H1 22 H2 23
=== 5. what an UNAVAILABLE hypothesis still emits (19 of 24 available)
  label UNAVAILABLE | joint REVERSAL_NOT_REPLICATED | keys: ['available', 'expected', 'first', 'key', 'kind', 'leave_one_out', 'min_draws', 'second', 'sign_test', 'status', 'unavailable', 'unavailable_counts', 'values']
  has interval: False | has envelope: False | per-draw values: 19 | sign test: {'positive': 19, 'negative': 0, 'zeros': 0, 'p': 3.814697265625e-06} | leave-one-out intervals: 19
  one leave-one-out entry: {'mean': 0.004044646897764879, 'interval': [0.00369032581727835, 0.004398967978251408], 'df': 17, 'side': 'ABOVE'}
=== 6. study status
  24 completed: status COMPLETE, labels {'H1': 'CONFIRMED', 'H2': 'CONFIRMED'}, joint REVERSAL_REPLICATED, statistics present: True
  23 completed: status COMPLETE_WITH_FAILED_DRAWS, labels {'H1': 'CONFIRMED', 'H2': 'CONFIRMED'}, joint REVERSAL_REPLICATED, statistics present: True
  20 completed: status COMPLETE_WITH_FAILED_DRAWS, labels {'H1': 'CONFIRMED', 'H2': 'CONFIRMED'}, joint REVERSAL_REPLICATED, statistics present: True
  19 completed: status INCOMPLETE, labels None, joint None, statistics present: False
  a draw absent from the mapping (not None): decide -> COMPLETE_WITH_FAILED_DRAWS {'n24': 'DRAW_MISSING'}
```

##### c04: `python -I -B c04_n7_check.py <REPO> <BUNDLE> <SCRATCH>`

The output has a second block headed "2. statistics from refits". It is identical, line for line, to the block from POINTS.csv below, so I give it once.

```
1. refits against POINTS.csv: 240 fits, largest |p* difference| 0; bit-identical in 240/240
   objective and J0 against FITS.csv: largest difference 0; fits at or above 7.999: 0; largest p* 0.1489
2. statistics from POINTS.csv: n8_analysis.contrast | auditor | ANALYSIS.json
   P1: +0.0090879 [+0.0040039, +0.0141720] ABOVE; vs auditor 7.2e-13; vs ANALYSIS.json 7.2e-13; sign 6/0 p 0.03125 (sealed 0.03125); leave-one-out vs sealed 4.8e-13
       envelope over 64 combinations: min lower +0.00007639 (auditor brute force +0.00007639; correction of 23 Nov +0.0000764), max upper +0.02743476 (auditor +0.02743476); ends at min lower [0, 1, 1, 1, 1, 1]
   S1: +0.0080848 [+0.0048733, +0.0112963] ABOVE; vs auditor 4.5e-13; vs ANALYSIS.json 4.5e-13; sign 6/0 p 0.03125 (sealed 0.03125); leave-one-out vs sealed 3e-13
       envelope over 64 combinations: min lower -0.00005074 (auditor brute force -0.00005074; correction of 23 Nov -0.0000507), max upper +0.01423631 (auditor +0.01423631); ends at min lower [1, 0, 1, 1, 1, 1]
   S3: -0.0045420 [-0.0079470, -0.0011370] BELOW; vs auditor 4.8e-13; vs ANALYSIS.json 4.8e-13; sign 0/6 p 0.03125 (sealed 0.03125); leave-one-out vs sealed 3.2e-13
   S4: +0.0139419 [+0.0089276, +0.0189563] ABOVE; vs auditor 7.1e-13; vs ANALYSIS.json 7.1e-13; sign 6/0 p 0.03125 (sealed 0.03125); leave-one-out vs sealed 4.7e-13
       envelope over 64 combinations: min lower -0.00026786 (auditor brute force -0.00026786; correction of 23 Nov -0.0002680), max upper +0.02431174 (auditor +0.02431174); ends at min lower [1, 1, 1, 1, 1, 1]
   S5: +0.0138212 [+0.0111616, +0.0164807] ABOVE; vs auditor 3.8e-13; vs ANALYSIS.json 3.8e-13; sign 6/0 p 0.03125 (sealed 0.03125); leave-one-out vs sealed 2.5e-13
   S2: UNAVAILABLE, available ['m02', 'm03', 'm06'] (auditor 3 readings; ANALYSIS.json UNAVAILABLE, ['m02', 'm03', 'm06']), reasons {'m01': 'TARGET_OUTSIDE_PATH', 'm04': 'TARGET_OUTSIDE_PATH', 'm05': 'TARGET_OUTSIDE_PATH'}
   MATCHED.csv: 36 rows, 0 mismatches of status, bracket or count, largest value difference 0
3. analyse() on N7 at 1e-4 (H1 = P1, H2 = S3), no orders
   decision COMPLETE {'H1': 'CONFIRMED', 'H2': 'CONFIRMED'} REVERSAL_REPLICATED | S_b: {'status': 'NOT_COMPUTED', 'reason': 'no batch orders given'}
   H1: +0.00909 [+0.00400, +0.01417] df 5 t 2.570581836
   H2: -0.00454 [-0.00795, -0.00114] df 5 t 2.570581836
   starting offset, contrast: +0.00625 [-0.00008, +0.01257], positive 5/6
   starting offset, change_in_768: +0.00284 [+0.00124, +0.00444], positive 5/6
   starting offset, offset: +0.03697 [+0.01634, +0.05760], positive 5/6
   auditor: contrast with the offset +0.00625 [-0.00008, +0.01257]   (AA-3 printed +0.0062 [-0.0001, +0.0126], 5/6)
   S-a: +0.01583581 [+0.01040960, +0.02126202]; positions 2.09092701 2.17570429 2.13578642 2.19158563 2.07568226 2.23352733   (13 Nov audit: +0.01583581 +0.01040960 +0.02126202; 2.09092701 2.17570429 2.13578642 2.19158563 2.07568226 2.23352733)
   S-c cumulative_rms: min/median/max 0.00476198 0.01443651 0.01914414; largest difference from the 13 Nov audit 2.4e-09; rows 240
   S-c cumulative_max_abs: min/median/max 0.00847085 0.02297270 0.02961557; largest difference from the 13 Nov audit 2.6e-09; rows 240
   S-c bin_max_abs: min/median/max 0.02492288 0.26589176 0.40357918; largest difference from the 13 Nov audit 3.1e-09; rows 240
   S-c bin_rms: min/median/max 0.01448940 0.12248159 0.18862965; largest difference from the 13 Nov audit 4.9e-09; rows 240
   S-d against ANALYSIS.json by_readout D4: values 0, intervals 6.5e-13
   NOT_OVERFIT: {'512|lr1e-04': ('NOT_OVERFIT', 'NOT_OVERFIT', 1.3622297734272593e-12), '768|lr1e-04': ('NOT_OVERFIT', 'NOT_OVERFIT', 1.089475731852474e-12)}
   records against arrays: 8.549686754122376e-07 flagged 0 | ANALYSIS.json 8.549686754122376e-07
   the result of analyse() serialises to JSON: yes
```

##### c05: `python -I -B c05_end_to_end.py <REPO>` (synthetic arrays; the labels below describe made-up data, not N8)

```
0. the plan against the sealed source plan, written out independently: readouts equal True | path 25 readouts 2.0 .. 3.5 | rate tag True | minimum 20 20 | draws 24
1. all 24 draws: COMPLETE {'H1': 'CONFIRMED', 'H2': 'INCONCLUSIVE'} REVERSAL_NOT_REPLICATED
   sections: {'sensitivity': ['envelope', 'leave_one_out', 'starting_offset'], 'secondary': ['S_a', 'S_b', 'S_c', 'S_d'], 'carried_over': ['not_overfit', 'records_against_arrays']}
   H1: n8_analysis +0.002740680 [+0.001844411, +0.003636948] df 23; auditor +0.002740680 [+0.001844411, +0.003636948] from 24 draws; largest difference 3.3e-18
   H2: n8_analysis -0.000763905 [-0.002204365, +0.000676554] df 23; auditor -0.000763905 [-0.002204365, +0.000676554] from 24 draws; largest difference 5e-18
   envelope: 16,777,216 combinations, min lower +0.0017045, max upper +0.0039313; H1 brackets 64 updates apart: True
   S-b steps: [2.25, 2.5, 2.75] | S-d readouts: 25 | S-c rows: 1344 | leave-one-out: {'H1': 24, 'H2': 24}
   serialises to JSON: yes
2. a failed draw given as None (n07):
   COMPLETE_WITH_FAILED_DRAWS {'H1': 'CONFIRMED', 'H2': 'INCONCLUSIVE'} REVERSAL_NOT_REPLICATED | H1 unavailable {'n07': 'DRAW_MISSING'} | NOT_OVERFIT n {'512|lr1e-04': 23, '768|lr1e-04': 23}
3. the same draw absent from the mapping (not None):
   analyse() raises KeyError 'n07' (decide() alone returns COMPLETE_WITH_FAILED_DRAWS)
4. three draws given as None although nothing says they failed (for example a run not yet made):
   COMPLETE_WITH_FAILED_DRAWS {'H1': 'CONFIRMED', 'H2': 'INCONCLUSIVE'} REVERSAL_NOT_REPLICATED -> the function labels whatever it is given; what counts as failed is decided by its caller
5. fewer than 20:
   ['decision', 'environment', 'plan'] INCOMPLETE None None
6. records against arrays: the recorded training loss of 768 at the first readout of n01's H1 bracket moved by +0.002 (arrays unchanged):
   flagged: [{'draw': 'n01', 'width': 768, 'tag': 'lr1e-04', 'epoch': 2.3125, 'difference': 0.001999713152646798}]
   n01 is still READ | weight 0.665644 -> 0.694162 | value 0.0041918739499680335 -> 0.004165970727503798 (the reading uses the record; the flag does not gate, as the protocol says)
7. NOT_OVERFIT labels: {'512|lr1e-04': 'NOT_OVERFIT', '768|lr1e-04': 'NOT_OVERFIT'} (validation falls from E2 to E3 by construction)
```

##### c06: `python -I -B c06_mutants.py <REPO> <BUNDLE> <SCRATCH>`

Each mutant is a one-line change written to `scratch/mutants/<name>/` beside a byte copy of `test_synthetic.py`; the clone is untouched. The test's first five functions are called (30 checks); its `envelope()` function is not, and no mutant touches the envelope or the quantile. In part B, the phrase about H2's envelope is left over from a mutant I removed and can be ignored.

```
PART A. test_synthetic.py (its first five functions, 30 checks) on mutants of n8_analysis.py
  M0 unmutated copy: SURVIVES (30 passed, 0 failed)
  M1 the 1e-9 margin dropped from side(): SURVIVES (30 passed, 0 failed)
  M2 H1 value at bound 32 ignores the interpolation weight: SURVIVES (30 passed, 0 failed)
  M3 a saturated fit makes a draw unavailable for H2 only, not for H1: SURVIVES (30 passed, 0 failed)
  M4 records flagged above 1e-2 instead of 1e-3: SURVIVES (30 passed, 0 failed)
  M5 NOT_OVERFIT: the labels OVERFIT and PLATEAU swapped: SURVIVES (30 passed, 0 failed)
  M6 S-d keeps saturated fits: SURVIVES (30 passed, 0 failed)
  M7 starting offset: an undefined refit is not set aside: SURVIVES (30 passed, 0 failed)
  M8 refit threshold 7.5 instead of 7.999: SURVIVES (30 passed, 0 failed)
  K1 control: unavailable at exactly the minimum: KILLED (the test aborts: KeyError: 'interval')
  K2 control: the last bracketing interval is read: KILLED (27 passed, 3 failed: a flat interval holding the target is read at its earlier readout  [{'between': [2.2; a target equal to a readout value is held by the first interval that contains it  [{; a non-monotone path: the first bracketing interval, and the count of all of them  [b)
  K3 control: a flat interval is read at its later readout: KILLED (29 passed, 1 failed: a flat interval holding the target is read at its earlier readout  [{'between': [2, )
PART B. on N7 with the unmutated module: do the mutated branches ever arise? (test_on_n7.py reads only N7)
  fits: 240; undefined: 0; largest p*: 0.1489 (M2, M3, M6, M8 need a fit of at least 7.5); saturated: 0
  lr1e-04: NOT_OVERFIT labels ['NOT_OVERFIT'] (M5 needs another label); records against arrays, largest difference 8.55e-07 (M4 needs one between 1e-3 and 1e-2); starting-offset rows ['READ'] (M7 needs UNDEFINED_FIT); H2 has an envelope: False (test_on_n7.py never looks for one)
  lr3e-04: NOT_OVERFIT labels ['NOT_OVERFIT'] (M5 needs another label); records against arrays, largest difference 8.55e-07 (M4 needs one between 1e-3 and 1e-2); starting-offset rows ['READ'] (M7 needs UNDEFINED_FIT); H2 has an envelope: False (test_on_n7.py never looks for one)
  interval limits examined: 106; nearest to 0: 0.000121 (M1 needs one within 1e-9 of 0)
```

##### c07: `python -I -B c07_exposure_windows.py <REPO>`

```
S-b on synthetic orders, 6 draws: largest difference between exposure_windows and the auditor, per-draw contrasts: {'whole': '0', 'last': '0', 'every': '0', 'loss_last': '0', 'loss_every': '0'}
  768 at E2.25: every-pass set sizes 25-41 equal: True; max |mean age difference| 0.65546 updates, difference 0; max joint quarter-cell distance 0.00000, difference 0
  768 at E2.5: every-pass set sizes 116-145 equal: True; max |mean age difference| 0.38345 updates, difference 0; max joint quarter-cell distance 0.04340, difference 0
  768 at E2.75: every-pass set sizes 398-440 equal: True; max |mean age difference| 0.23381 updates, difference 0; max joint quarter-cell distance 0.02584, difference 0
  order checks (synthetic losses do not depend on the orders, so about 0 is expected): {'n01': -0.0009, 'n02': -0.0012, 'n03': -0.0009, 'n04': -0.0009, 'n05': -0.0008, 'n06': -0.0013} | steps per draw {12}
```

##### c08: `python -I -B c08_untested_branches.py <REPO>`

```
1. NOT_OVERFIT: validation loss at E3 minus E2 per width, over the completed draws
   all falling: NOT_OVERFIT, interval [-3.449e-02, -2.851e-02], n 24
   all rising: OVERFIT, interval [+2.851e-02, +3.449e-02], n 24
   mixed: PLATEAU, interval [-4.313e-03, +4.313e-03], n 24
   falling, upper limit within 1e-9 of 0: PLATEAU, interval [-8.627e-04, -5.000e-10], n 24
2. S-d: a saturated fit drops its draw at that readout only
   draws at E2.5: 22 (n05 saturated and n07 undefined are out; n06, resolved at bound 32, stays with its bound-8 value -7.895 ) | draws at E2.5625: 24
3. starting offset: a refit that is undefined once the offset is taken off
   rows: {'n01': ('READ', 0.05), 'n02': ('UNDEFINED_FIT', 3.0591), 'n03': ('READ', 0.0424), 'n04': ('READ', 0.0472)} | draws in the contrast: 3 | draws in the offset summary: 4
4. the refit threshold: gains proportional to w^q, read through arm_points
   q = 7.9: p* = 7.900000; refitted at bound 32: False; saturated: False
   q = 7.9985: p* = 7.998500; refitted at bound 32: False; saturated: False
   q = 7.9995: p* = 7.999500; refitted at bound 32: True (p32 = 7.999500); saturated: False
   q = 8.0: p* = 8.000000; refitted at bound 32: True (p32 = 8.000000); saturated: False
   q = 9.0: p* = 8.000000; refitted at bound 32: True (p32 = 9.000000); saturated: False
```

#### 5. Commands that matter, with their output

**Command 1.** `python -I -B <REPO>/preregistration/natural-text-dense-replication-20261114/analysis/test_synthetic.py` (the registered test, unmodified, run from the clone; saved as `test_synthetic_output.txt`)

```
numpy 2.5.3, python 3.12.10
--- t quantile
PASS  closed-form integer-df CDF at the quantile, df 1-60, probabilities 0.9 to 0.995 (1e-13)  [largest error 9.8e-15]
PASS  two-sided p against the closed form, df 1-40 (1e-13)  [largest error 1.4e-14]
PASS  N7's T95 table, df 2-11 (rounded to 9 decimals, so 5e-10)  [largest difference 4.1e-10]
      df 19-23: 19: 2.093024054408, 20: 2.085963447266, 21: 2.079613844728, 22: 2.073873067904, 23: 2.068657610419
SKIP  SciPy comparison: SciPy is not installed
--- reading rule
PASS  a flat interval holding the target is read at its earlier readout  [{'between': [2, 2.25], 'weight': 0.0, 'p_read': 0.1, 'intervals_holding_the_target': 2}]
PASS  a target equal to a readout value is held by the first interval that contains it  [{'between': [2, 2.25], 'weight': 1.0, 'p_read': 0.11, 'intervals_holding_the_target': 3}]
PASS  a target outside the path (4.31) is TARGET_OUTSIDE_PATH  [TARGET_OUTSIDE_PATH]
PASS  a target outside the path (4.19) is TARGET_OUTSIDE_PATH  [TARGET_OUTSIDE_PATH]
PASS  a non-monotone path: the first bracketing interval, and the count of all of them  [between [2, 2.25], count 5, p 0.1900]
PASS  an undefined p* at the bracket: UNDEFINED_FIT  [UNDEFINED_FIT]
PASS  an undefined p* off the bracket does not matter  [READ]
PASS  an undefined p* of 512 at E3: UNDEFINED_FIT  [UNDEFINED_FIT]
--- availability and the decision (N8 grid, 24 draws, minimum 20)
PASS  plan grid: 28 readouts, a 25-readout path every 64 updates from 2,048 to 3,584, E3 on it  [28 readouts, path 2.0..3.5, minimum 20 draws]
PASS  S-b windows: quarters; on N8's 64-update path the order check uses exactly the six quarter windows, none unaligned  [6 steps]
PASS  19 of 24 available for H1: H1 UNAVAILABLE, REVERSAL_NOT_REPLICATED  [labels {'H1': 'UNAVAILABLE', 'H2': 'CONFIRMED'}, REVERSAL_NOT_REPLICATED, TARGET_OUTSIDE_PATH 5]
PASS  20 of 24 available: both read, REVERSAL_REPLICATED  [H1 +0.00393 [+0.00290, +0.00497], envelope over 1048576 combinations]
PASS  an undefined 768 fit at E3 in 5 draws: H2 UNAVAILABLE (19 of 24), H1 unaffected  [{'H1': 'CONFIRMED', 'H2': 'UNAVAILABLE'}]
PASS  19 completed draws: INCOMPLETE, no statistic and no label  [19 of 24 draws completed, fewer than 20: the study is INCOMPLETE and nothing is read.]
PASS  20 completed draws: read, failed draws counted as DRAW_MISSING for both  [{'H1': 'CONFIRMED', 'H2': 'CONFIRMED'}]
PASS  H2 interval including 0: INCONCLUSIVE, REVERSAL_NOT_REPLICATED  [{'H1': 'CONFIRMED', 'H2': 'INCONCLUSIVE'}]
PASS  both on the wrong side: CONTRARY  [{'H1': 'CONTRARY', 'H2': 'CONTRARY'}]
--- saturation (fits at or above 7.999 refitted with the upper bound at 32)
PASS  a fit below 7.999 is not refitted  [p 0.5000]
PASS  gains rising as w^12: bound-8 fit at the bound, resolved at bound 32, not saturated  [p 8.0, at bound 32 12.0000]
PASS  all gain on the heaviest sequence: unresolved at bound 32, SATURATED  [p 8.0, at bound 32 32.0]
PASS  a saturated fit makes its draw unavailable (SATURATED); a resolved one stays, with its value at bound 32 reported  [available 23]
--- sign test, leave-one-out, intervals
PASS  sign test [1, 1, 1, 1, 1, 1]  [p 0.03125]
PASS  sign test [1, 1, 1, 1, 1, 0]  [p 0.0625]
PASS  sign test [1, 1, 1, 1, 1, -1]  [p 0.21875]
PASS  sign test [0, 0]  [p None]
PASS  leave-one-out intervals equal the interval of the remaining draws, df n - 2
PASS  a constant sample is degenerate, with a zero-width interval  [[0.003, 0.003]]
--- bracket envelope
PASS  against itertools brute force, n = 2, 3, 5, 10, 13 (1e-12)  [largest difference 1.7e-18]
PASS  brackets of zero width: the envelope is the plain interval
PASS  one draw is refused
PASS  24 draws: 16,777,216 combinations in 0.5 s, peak traced memory 16.1 MiB  [min lower +0.0020124, max upper +0.0098573]
PASS  24 draws against a direct enumeration of all 2^24 combinations (1e-12)  [differences 4.3e-19 / 0; direct enumeration 7 s]
PASS  the reported vertices give the reported limits
PASS  20,000 interior points stay inside the vertex extremes (concavity)  [interior min lower +0.0029996, max upper +0.0089609]
37 passed, 0 failed
exit 0
```

**Commands 2-7**, run in the clone (saved as `cmd_output.txt`):

```
$ git rev-parse HEAD; git status --short | wc -l
30548dbb789b2a117486fdf6f9ab9added680172
0

$ sha256sum preregistration/natural-text-dense-replication-20261114/analysis/*
37b32fc547bb09f987f3131157f94ad171b5822b9d87d488bced3ae448f38538  analysis/n8_analysis.py
0d5a3661761f19b2b400163421b2d420673c1c769ee846a91131d9ae1ff55b72  analysis/regenerate_n7_orders.py
6f056cdb1e95e954559bb676709de3c7247313b8d5d628f06bb8c8b01ff6f161  analysis/test_on_n7.py
6e8ec084b07765f9b00b5dfa9c72719d7e7f2fb0c544c1b9666530b3e3bb1455  analysis/test_synthetic.py

$ sed -n 31,36p preregistration/natural-text-dense-replication-20261114/HASHES.json
  "analysis": {
    "analysis/n8_analysis.py": "37b32fc547bb09f987f3131157f94ad171b5822b9d87d488bced3ae448f38538",
    "analysis/regenerate_n7_orders.py": "0d5a3661761f19b2b400163421b2d420673c1c769ee846a91131d9ae1ff55b72",
    "analysis/test_on_n7.py": "6f056cdb1e95e954559bb676709de3c7247313b8d5d628f06bb8c8b01ff6f161",
    "analysis/test_synthetic.py": "6e8ec084b07765f9b00b5dfa9c72719d7e7f2fb0c544c1b9666530b3e3bb1455"
  },

$ git diff --stat n8-registration v2.1 -- preregistration/natural-text-dense-replication-20261114/analysis preregistration/natural-text-dense-replication-20261114/N8-protocol-draft.md | wc -l
0

$ grep -n -E "__main__|open\(|read_bytes|read_text|Path\(|os\.|import " preregistration/natural-text-dense-replication-20261114/analysis/n8_analysis.py
21:import hashlib
22:import math
23:import platform
24:import statistics
25:import sys
26:from functools import lru_cache
28:import numpy as np

$ grep -rl "n8_analysis" --include=*.py --include=*.ps1 --include=*.txt . (outside .git)
./preregistration/natural-text-dense-replication-20261114/analysis/regenerate_n7_orders.py
./preregistration/natural-text-dense-replication-20261114/analysis/test_on_n7.py
./preregistration/natural-text-dense-replication-20261114/analysis/test_synthetic.py
./preregistration/natural-text-dense-replication-20261114/seal/pre-pin/matched_plan.py
./preregistration/natural-text-dense-replication-20261114/source/matched_plan.py
./preregistration/natural-text-dense-replication-20261114/source-tests/test_n8_source.py
./preregistration/natural-text-dense-replication-20261114/tools/make_changes.py
./preregistration/natural-text-dense-replication-20261114/tools-tests/test_tools.py

$ grep -n -E "__main__|^def load" preregistration/natural-text-matched-confirmation-20261104/sealed-source/matched_analysis.py
61:def load(runs, pins=mw.PINS, subject=None, allow_fixture=False):
413:if __name__ == '__main__':
```

In the sixth command, only the three files under `analysis/` import the module; the other five name it in text.

**Command 8.** `sha256sum` of the inputs that `test_on_n7.py` pins. All four pins and the manifest pin match the clone and the bundle:

```
234434a34cf64d98e0d45cfe029bb37935207176fd996cafe85756956c7d860f  reports/natural-text-matched-analysis-20261105-01/POINTS.csv
86ea11d7210682375717d7eb67a58c74d806ad22dc57ec87ab9db4e836421e3b  reports/natural-text-matched-analysis-20261105-01/MATCHED.csv
a4af7bad78fdf9f4fe34317f73e6a1932fd0d29367b5da188b79ae73db95ce65  reports/natural-text-matched-analysis-20261105-01/ANALYSIS.json
b1cd03dec3a6e13ba2d82a6a95a48e99342ace8aaf4a0cdf1b36392fa8c7aa67  reports/natural-text-matched-analysis-20261105-01/FITS.csv
6f9c124787760b9b64e219bb55206bdc3f7f9b45774cb5eb82d4d528607b3698  n7-loss-arrays/MANIFEST.json
```

##### Conduct of this audit

- **I exceeded hard rule 4's limit on the 2^24 enumeration.** `decide()` computes H1's envelope whenever 24 draws are available, so my probes ran the split-sum enumeration over 2^24 combinations about 100 times: 5 in the registered test, 4 in c03, 4 in c05 (it ran twice) and about 88 in c06 (it ran twice, about 4 per mutant). Each takes about 0.5 s on one core, so about a minute of CPU in total. The 7-second direct enumeration ran once, inside the registered test. I noticed this only afterwards, and ran nothing with 24 draws after that.
- **The clone is unchanged:** `git status --short` is empty and there is no `__pycache__`. I wrote only in the scratch folder: the scripts, their outputs, `c02_per.pkl`, `cmd_output.txt` and `mutants/`.
- **I read nothing on drive D:** and nothing outside the three folders and the brief. No N8 data was read, and no N8 result was estimated; every label printed by c03, c05 and c08 describes made-up values.
- **GitHub was not contacted.**

## Appendix 1D. Auditor D (area D)

### Audit of the sequence-weighting record at v2.1 (30548db): area D, the conduct of N8 so far, with area F items

Auditor D of four. Public files only: my clone at `30548dbb789b2a117486fdf6f9ab9added680172`, read-only `git` and `gh api` GET requests, and the brief. Nothing on drive D: was opened, listed or searched. None of `check_run.py`, `X2_COMMAND.txt`, `RUN_COMMAND.ps1`, the builder, the worker or an owner script was run; where I tested logic I ran copies on dummy folders inside my scratch folder (section 4). The clone is unchanged (`git status --porcelain`: 0 lines; no `__pycache__`). I did not check the GitHub signature of `c6f98b2` (the supervising session does) and did not estimate any N8 result.

`N8/` below means `preregistration/natural-text-dense-replication-20261114/`. Line numbers are at commit 30548db.

#### 1. Findings

##### 1a. Summary

- **No Critical or Major finding in area D.** I found no registered number, label or registration element that is wrong, and no event that departs from a stated rule of the registered protocol without being disclosed.
- **R2's failure and the retry X2** follow protocol section 8 and the sealed code, as far as public files allow a check. The retry's registered report (each width's E0 comparison) is given: w768 DIFFERENT, w512 ABSENT.
- **The three published operational files do what the notes say.** Their pinned hashes match the published files. The run-order rule and the approval checks of `RUN_COMMAND.ps1` behave as described. A scratch copy of `check_run.py` (one line changed) on dummy runs performs exactly 55, 47 and 32 checks for a complete run, a run failed in its third draw and a one-draw retry: the notes report 54+1, 46+1 and 31+1. It confines its reads as described and printed no planted loss value.
- **Nothing published at v2.1 allows an interim look at N8 results** (tree, history, releases, branches, pull requests, artifacts).
- **The gaps are documentation gaps** (all Minor or Suggestion):
  - D1: that registration preceded R1 cannot be checked from public files. R1 has a date only, the same local date as the merge. The run-side evidence exists but is unpublished, although it holds no loss value.
  - D2: the pause has no stated reason and no stated criterion for resuming.
  - D3: no registered file says which attempt's files the analysis reads for a retried draw, or what makes a draw "completed".
  - D4: the notes' statement of GPU-memory headroom is not supported by the public pilot numbers, and it omits the 28 MiB margin at start-up.
  - F-d1: `check_run.py`, as published, reports two extra failures for a run whose start the sealed owner script refused once.

##### 1b. The five events against the registered protocol

| Event | What the protocol says | Handled as prescribed? | Disclosed? | A deviation not called one? |
|---|---|---|---|---|
| R1 parent folders (15 Nov) | Nothing. Section 10, step 5: "Seal the protocol, source and registry by hash, merge them publicly and tag. Only then train." | Yes. Two empty folders were made outside every sealed file. The builder writes nothing before `target.mkdir()` (`N8/tools/build_n8_activation.py:135–136`), so the failed first build left nothing. | Yes: `N8/README.md:32`, `N8/OPERATIONAL_NOTES.md:48`. First public on 23 November (D6). | No |
| R2 failed in n06; retry X2 (15–16 Nov) | Section 8, lines 178–182: one retry, "admitted only on its first run's terminal record", "repeats from scratch, with the same seeds, the draws that run did not finish", "reports how each width's new E0 losses compare with the first attempt's" | Yes, on the notes' account and by the sealed code path (builder `:94–102`; worker `source/matched_worker.py:64–73, 121–127, 288–296`). X2 repeated n06 only. | Yes: notes lines 54–81. The size of the E0 difference is deferred (D5). | No. The reading rule for the analysis is not registered (D3). |
| GPU-memory check before the claim (16 Nov) | Nothing. Owner commands are not registered files. | Not applicable. It runs before the sealed owner script and changes no sealed file. It is stricter than the sealed limit (600 against 658 MiB). It cannot remove or select data: without a claim nothing is consumed. | Yes: notes lines 26–38. Two effects are not stated (D7), and its rationale is weak (D4). | No |
| Run order (16 Nov) | Section 8, line 177: "in eight runs, R1–R8, of three draws each, in registry order". Silent on when a retry runs. | Yes. n06 was retried before any R3. `RUN_COMMAND.ps1:93–95` enforces it for R3–R8 (tested, section 4). | Yes: notes lines 40–44. | No. The sealed code itself enforces no order between runs (D9). |
| Pause (23 Nov) | Nothing on pauses. Line 176: "24 draws, no interim analysis, and no look at any p\* before all 24 draws are complete". Lines 104–106: fewer than 20 finished is INCOMPLETE. | The protocol sets no schedule, so a pause breaks no stated rule. | The fact and the commitments are on every living page. The reason is not given anywhere (D2). | No |

##### 1c. Findings table

| ID | Area | Severity | Finding | Evidence | Status | Fix type |
|---|---|---|---|---|---|---|
| D1 | D | Minor | **That registration preceded R1 cannot be checked from public files.** The notes give R1 a date and no time. That date is also the local date of the merge. R2's clock times carry no time zone. The sealed design does tie every run to the merge commit, but the files that would show it are unpublished. | `N8/OPERATIONAL_NOTES.md:49` "**15 November 2026, Run R1 COMPLETE.**"; line 62 "At 15:38:33 … 15:39:46 … 16:09:15" (no zone). `gh api …/pulls/1`: `"merged_at":"2026-11-14T18:19:20Z"`, which is 15 November 01:19:20 at +07:00. The registered builder had `PUBLIC_REGISTRATION = None` and refuses (`git diff c6f98b2 88ac496`; `N8/tools/build_n8_activation.py:53, 122–124`). The recorded builder writes `builder_sha256` and `public_registration` into `APPROVAL_RECORD.json` (`:141–144`), and the worker binds `approval_record_sha256` into `TERMINAL.json` (`N8/source/matched_worker.py:42, 314`). The notes give the three terminal hashes (lines 50, 55, 69); script d01 finds them nowhere else in the repository, except R2's in `X2_COMMAND.txt`. | VERIFIED (the gap). The order itself is PLAUSIBLE: R2 and X2 fall after the merge under either reading of the zone. | doc-only: publish, for R1, R2 and X2, `TERMINAL.json`, the stage receipts, `APPROVAL_RECORD.json`, `AUTHORIZATION.json`, `OWNER_EXIT_RECEIPT.json` and the `gpu-checks` records. By the sealed code none holds a loss value (section 1d). Add each run's start and end time with its zone. |
| D2 | D | Minor | **The pause is disclosed without a reason and without a criterion for resuming.** The protocol is silent on pauses, so this is not a departure from a stated rule. But six draws' losses now sit unanalysed for an open period, and the decision to resume is not tied to anything. "No p\* has been computed or examined" cannot be verified by anyone outside. | `N8/OPERATIONAL_NOTES.md:82–85`; `N8/README.md:5–10`; `PUBLICATION_NOTES.md:52–59`. A search of the living pages for "pause" and "resum" finds no reason (section 5). `N8/N8-protocol-draft.md:176` "**Fixed sample.** 24 draws, no interim analysis, and no look at any p\* before all 24 draws are complete." | VERIFIED (the omission). The no-look statement is UNVERIFIED and cannot be verified from files. | doc-only: a dated note with the reason, with who decides to resume and on what, and stating that the decision does not use N8 data. Publishing the SHA-256 of every loss-bearing file of n01–n06 now would fix the paused data. |
| D3 | D (touches C) | Minor | **No registered file says which attempt's files the analysis reads for a retried draw, or what makes a draw "completed".** The sealed analysis is a library that takes its data in memory. No N8 loader is registered. R2's n06 folder still holds a first-attempt `w768/E0.f32` and `E0.pt` beside X2's complete n06. | `N8/analysis/n8_analysis.py:16` "data[d] is None for a failed draw, or dict(weights=[...], arms={…})"; `:562` `def analyse(per, data, plan=PLAN, orders=None)`. The only loader in the folder is `N8/analysis/test_on_n7.py:85` `def load_bundle(bundle)`, for N7's bundle. `HASHES.json` lists four analysis files. Notes line 63: "**What n06 left, in place:** `INPUTS.json`, `ORDERS.i64`, `w768/E0.f32`, and the kept state `w768/E0.pt`". Protocol lines 180–182. | VERIFIED | doc-only now, and a matter for N8's result report: a dated note, before any p\* is computed, stating that n04 and n05 are read from `runs\n8-r2`, n06 wholly from `runs\n8-x2` (its E0 included), that nothing of R2's n06 enters the analysis, and that a draw is completed if its stage record is COMPLETE in the terminal its owner receipt names. Publish and hash the loader before it runs. |
| D4 | D | Minor | **The notes' account of GPU-memory headroom is not supported by the public numbers, and it omits the tighter limit at start-up.** (a) The guard's peak reading is the same to the byte in the pilot and in all six completed draws, across four runs on three days, while the Windows readings quoted in the same notes differ by more than 100 MiB. In the pilot the reading exceeds the worker's own reserved memory by the same 863,816,908 bytes at both widths. So the reading did not move one for one with other apps' memory, and "by anything" is not shown. (b) The start-up benchmark gates the same reading at 2.25 GiB, only 28.2 MiB above the pilot's peak. A start-up stop uses up the run, and the retry is then the only attempt left for all three draws. | (a) `N8/pilot/PILOT_LOG.json:9–10` (512: `cuda_reserved` 891289600, `device_used_sampled` 1755106508), `:30–31` and `:246–247` (768: 1522532352, 2386349260). Both differences are 863,816,908. Notes line 59 "In each of the five draws completed so far (n01–n05), its highest reading was 2,386,349,260 bytes"; line 72 the same for X2; lines 62 and 71: 484, 472, 324 and 377 MiB. Notes line 57 "samples the GPU memory used on the whole device"; line 37 "So about that much more GPU memory in use during a draw, by anything, can stop the run." (b) `N8/source/fewepoch_plan.py:77–78`; `N8/source/matched_worker.py:154–159, 339–340`; `PILOT_LOG.json:50` `"fit_limit_bytes": 2415919104`; 2,415,919,104 − 2,386,349,260 = 29,569,844 bytes. One-use: `N8/source/MATCHED_OWNER_RUN.ps1:55`. | Numbers VERIFIED. The reading that they do not track other apps' memory is PLAUSIBLE: the Windows readings are from before draws, not from the peak. | doc-only: correct the two sentences. To settle what the reading measures, publish the paired readings the gate records already hold for each draw: `wsl_device_used_bytes` in `<draw>-REQUEST.json` (`N8/source/text_worker.py:414`) beside the Windows `max_memory_used_mib` of the same check. They hold no loss value. |
| D5 | D | Suggestion | **The retry's E0 comparison is reported as registered, but only as SAME, DIFFERENT or ABSENT.** The notes defer its size because that needs the loss values. `check_run.py` compares the two attempts' seeds and order hashes, not the whole of `INPUTS.json`. | Protocol line 181 "It reports how each width's new E0 losses compare with the first attempt's."; `N8/source/matched_worker.py:288–296`; notes lines 73–76; `N8/check_run.py:161–165`. That bit-identical arrays were not expected was stated before X2: `DATA_AVAILABILITY.md:71`, added in fee55ea on 13 November; `N8/source/ORIGINAL_ENVIRONMENT.json:11` `"deterministic_algorithms": false`. | VERIFIED | A matter for N8's result report: give the size of the w768 E0 difference for n06. doc-only now: state whether R2's and X2's `n06/INPUTS.json` are byte-identical (their SHA-256; no loss value). |
| D6 | D (touches E) | Minor | **Entry dates are event dates, not publication dates, and one same-day revision is not disclosed.** (a) The README note dated 15 November on the two folders is absent from v2.0 and first public in c1a2380 on 23 November; `PUBLICATION_NOTES.md` says the README "keeps" it. (b) `OPERATIONAL_NOTES.md` was first published in c1a2380 saying `check_run.py X2` "had not been run by 23 November 2026", and the README said the check and the commands "are not published". Four minutes later v2.1 replaced both. The v2.1 entry does not mention the first version. (c) R2's failure of 15 November was first public eight days later. The protocol's own requirement is met: recorded "before the analysis runs". | `git diff 88ac496 c1a2380 -- N8/README.md` (the note is added); `PUBLICATION_NOTES.md:67–69` "keeps the note of 15 November on the two empty folders"; `git diff c1a2380 30548db -- N8/OPERATIONAL_NOTES.md N8/README.md` (section 5); GitHub activity: pushes at 2026-11-23T05:05:16Z and 05:09:33Z; no "c1a2380" in `PUBLICATION_NOTES.md`. Protocol lines 183–184. | VERIFIED | doc-only |
| D7 | D | Suggestion | **Two effects of the GPU-memory check are not stated.** (a) The sealed owner script records every start it refuses as `PRESTART-REFUSED-<k>.json`, which the worker copies into the run folder. The new check stops earlier, at a lower limit, and writes nothing. So a start refused for memory leaves no record from X2 on. (b) The notes give the owner script's readings for X2 but not the new check's five readings, nor whether it ever refused. | `N8/source/MATCHED_OWNER_RUN.ps1:70–75`; `N8/source/text_worker.py:404`; `N8/source/matched_worker.py:318`; `N8/X2_COMMAND.txt:55–72`; `N8/RUN_COMMAND.ps1:41–58`; `N8/source/GPU_CHECK.json:5`. Notes line 32 "**What it changes:** no sealed file, and nothing the worker or the owner script does."; line 71. | VERIFIED | doc-only: say so in the notes, and record the check's readings and refusals for each run. |
| D8 | D | Suggestion | **The completeness results cannot be tied to a version of the check, and the commands of R1 and R2 are unpublished.** The notes give pass counts, not the script's SHA-256 or its output. The published script contains failed-run and retry logic that cannot have been exercised before R2 failed. The counts do agree with the published version. `RUN_COMMAND.ps1` defines part of its checks by reference to the unpublished `R2_COMMAND.txt`. | Notes lines 53, 64, 78; `N8/README.md:82` "The owner's commands for R1 and R2, and the tests of the commands and of `check_run.py`, are not published."; `N8/RUN_COMMAND.ps1:15`; script d03: 55, 47 and 32 checks; published `check_run.py` SHA-256 `4df2aba5…9aa4`. | VERIFIED | doc-only: give the script's SHA-256 with each result; publish each run's check output (it prints no loss value) and the R1 and R2 commands. |
| D9 | D | Suggestion | **Registry order between runs is enforced only by the owner's commands, and one case has no rule.** The sealed builder, worker and owner script do not check that an earlier run ended. For R3–R8 the published command does. For R2 after R1 the command is unpublished. If a run leaves no terminal, for example after a power loss, the builder admits no retry and `RUN_COMMAND.ps1` then stops every later run; no registered rule says whether that run's draws with a COMPLETE receipt count as completed. | `N8/tools/build_n8_activation.py:103` `else: stages = list(mp.RUN_STAGES[mode])`, `:96` "left no terminal, so it admits no retry"; `N8/source/matched_worker.py:126`; `N8/RUN_COMMAND.ps1:93–95`; script d05: "STOPS … R2 EXIT_UNOBSERVED_NO_KILL, no X2". | VERIFIED (code). R2-after-R1 UNVERIFIED. | doc-only: a dated note for the no-terminal case, written before it can arise. |
| F-d1 | F | Minor | **`check_run.py`, as published, fails a sound run whose start the sealed owner script refused once.** The sealed script may refuse a start (GPU busy, or not on AC power), record it, and be run again. The worker copies the record into the run folder. The check expects the gate folders to hold `PRESTART.json` and the draws' records only, so it reports two failures beside the known gap and says "report them". The new memory check does not prevent this: it reads memory only, not utilization or power. | `N8/source/MATCHED_OWNER_RUN.ps1:70–75` ("Then run the same command again."); `N8/source/text_worker.py:404`; `N8/check_run.py:204–206, 311–312`. A scratch copy on a dummy R1 with one `PRESTART-REFUSED-1.json`: "52 passed, 3 failed … 2 other failure(s): report them" (section 4, d06). | VERIFIED on dummy data | doc-only: revise the check (it is not a registered file) with a dated note, or state in the notes that these two failures are expected after a refused start. |
| F-d2 | F | Suggestion | **The margin under the per-draw time cap is not reported, and one clock ratio is unexplained.** R2's draws took 2,792 and 2,816 s against the pilot's 2,528 s. If R2's cap was near the pilot's 3,097 s, n05 used 91% of it. A draw over its cap fails its run. Separately, owner time over worker time is 1.087 for R1 and 1.083 for X2 but 1.036 for R2, outside the 1.06–1.11 the protocol quotes. | Notes lines 51, 56, 70; protocol lines 162, 166–168; `N8/pilot/PILOT_LOG.json:84, 185`. Each run's cap is in its unpublished `BENCHMARK.json` (`N8/check_run.py:201` prints it). | Arithmetic VERIFIED. The caps of R1, R2 and X2 are UNVERIFIED. | doc-only: report each run's stage cap beside its draws' times. |
| F-d3 | F | Suggestion | **A pause can change the environment in ways the sealed code neither refuses nor records.** The worker pins Python, PyTorch, CUDA, cuDNN and the GPU's name, not the NVIDIA driver or the Windows build, and the gate records hold memory and utilization only. Contrasts are within a draw, so a change between runs would not favour a width, but it would not be visible either. | `N8/source/text_framework_setup.py:15, 21, 28`; `N8/source/gpu_check.ps1:23`; `N8/source/ORIGINAL_ENVIRONMENT.json` (no driver or OS field). | VERIFIED (not recorded) | doc-only: record the driver version and Windows build of R1, R2 and X2 if still known, and of each later run. |
| F-d4 | F | Suggestion | **The tag `n8-registration` carries no time of its own.** It is a lightweight tag, with no release. The time of the registration rests on the GitHub-signed merge commit and the pull request's `merged_at`, which is enough; the tag adds a name. Whether it was on GitHub before R1 cannot be checked. | `git cat-file -t refs/tags/n8-registration` → `commit`; `gh api …/git/ref/tags/n8-registration` → `"type":"commit"`; `gh api …/releases/tags/n8-registration` → 404. `N8/X2_COMMAND.txt:18–19` checks the tag before X2's build; R1's command is unpublished. | VERIFIED (lightweight). Its time is UNVERIFIED. | doc-only |

##### 1d. What in the notes can be checked from public files

| Statement in the notes | Checkable from public files? | Result, or what would have to be published |
|---|---|---|
| Limits and rules: guard 2,684,354,560 bytes; 658 MiB and 12% before the claim; memory recorded, not gated, before a draw; 600 MiB and five readings in the new check; retry before the next run | Yes | All match `fewepoch_plan.py:77, 84`, `GPU_CHECK.json:5, 7, 13`, `gpu_check.ps1:45, 60`, `X2_COMMAND.txt:55–71`, `RUN_COMMAND.ps1:93–95` |
| Arithmetic: 284 MiB; 1,060,714,088 bytes (1,012 MiB); 2,355 bytes | Yes | Correct: 298,005,300 / 2^20 = 284.2; 3,447,063,348 − 2,386,349,260 = 1,060,714,088; 634,105,445 − 634,103,090 = 2,355 |
| R1's folder holds 47 files besides `TERMINAL.json` | Yes, from the sealed layout | 1 + 3 receipts + 7 gate records + 3 × 12 = 47. The byte total is within 25,262 bytes of three draws at the pilot's public file sizes, the rest being the top-level JSON files |
| Guard peak 2,386,349,260 and reserved peak 1,522,532,352 in completed draws; `E0.pt` of 138,986,628 bytes | Corroborated | Equal to the public pilot's values (`PILOT_LOG.json:30–31, 156`) |
| A temp file in `cache\` during the run | Corroborated | `PILOT_LOG.json:53` `"cache_entries": 2` during the pilot's benchmark |
| `check_run.py` results 54+1, 46+1, 31+1 | The totals only | The published script performs 55, 47 and 32 checks (d03). The results need the run folders. Publishing each run's printed output would let them be read; it prints no loss value |
| The recheck 73 s after the first check before n06 | Consistent | 3 s settle + 10 readings 1 s apart + 60 s wait (`GPU_CHECK.json:6, 9, 11`) |
| Terminal hashes, approvals, times, GPU and power readings, what n06 left, the E0 verdicts, the cache timings | No | `TERMINAL.json`, the stage receipts, `BENCHMARK.json`, the run's and the activation's `gpu-checks`, `APPROVAL_RECORD.json`, `AUTHORIZATION.json`, `OWNER_CLAIM.json`, `OWNER_EXIT_RECEIPT.json`, `OWNER_PROGRESS.log`, `POWER_LOG.jsonl` and the two worker logs. By the code that writes them, none holds a loss value: `matched_worker.py:314, 337–338, 353–355, 359–360, 366–373`; `MATCHED_OWNER_RUN.ps1:112–117`; `gpu_check.ps1:40, 46`. `INPUTS.json`, `STATES_KEPT.json` and `ORDERS.i64` hold none either |
| Files that must stay unpublished until the analysis | — | `PRETRAINED.json` (E0 mean losses, `text_worker.py:264`), `record.json` (readout mean losses, `matched_worker.py:214`), `E0.f32`, `arrays.f32`, `E0.pt`. Their SHA-256 can be published |
| "A test on N7's test doubles reproduces the failure and the fix" (`N8/README.md:32`) | No | The test is unpublished (`N8/README.md:82`) |
| The pilot "differs from the sealed source only in the pins … the hours … and the source README" | At file level, yes | Four files differ between the two subjects, and no training code among them (d01). The pilot's versions of those four files are unpublished, so their content is UNVERIFIED. Pre-pin against sealed is verified line by line (section 5) |
| "No p\* has been computed or examined" | No | Cannot be shown from files. A published hash of the paused data and a stated reason for the pause are what can be added |

#### 2. Rejected concerns: checked and found sound

1. **The retry was admitted, built and run as registered.** The builder admits X2 only on R2's `TERMINAL.json`, with the same subject and inputs, a status other than COMPLETE and at least one draw to repeat, and requires R2's receipts to equal its stage records (`build_n8_activation.py:94–102`; `matched_worker.py:64–73`). The worker checks the same again and requires the activation to list exactly those draws (`:121–127`). `X2_COMMAND.txt` pins the recorded builder, the sealed subject, the pilot log, R2's FAILED exit receipt and R2's terminal hash (lines 11–14, 26–30).
2. **The retry is a fresh run with the same seeds, not a continuation.** A stage refuses an existing folder (`text_worker.py:135`). Pre-training reseeds from the registry's `init_seed` (`:247`), and so does each reload (`:236`). Orders and weights come from generators seeded per draw (`text_engine.py:53, 57`). The model has no dropout (`text_model.py`). So n06 does not depend on whether it ran third in R2 or first in X2. The worker reads R2's folder only to hash `E0.f32` (`matched_worker.py:288–296`).
3. **No published command, and no sealed step between runs, reads a loss.** `X2_COMMAND.txt` reads R2's exit receipt and hashes its terminal. `RUN_COMMAND.ps1` reads exit receipts' `status` only. The builder reads the terminal and the receipts' `status`. So a decision to start, retry or continue cannot be conditioned on results through these files.
4. **The GPU-memory check cannot change which data exist.** It runs before the sealed owner script, reads `nvidia-smi`, a performance counter and process names, writes nothing, and can only prevent a claim. The sealed script's own check still runs (`MATCHED_OWNER_RUN.ps1:68–75`).
5. **Pinned hashes match.** Builder `c31fd4aa…2904`, subject `9bdea3a9…bb6b` and pilot log `251d0951…7db6` in both commands equal the published files. All 31 sealed files match `SOURCE_SUBJECT.json` (d01).
6. **The run-order rule does what the notes say** (d05): R3's build stops without R2's exit receipt, stops when R2 is not COMPLETE and X2 has no exit receipt (also when X2 was built but never claimed), and proceeds when X2 has ended, COMPLETE or FAILED. The approval checks refuse a wrong run, a wrong or missing draw, a missing id and a second run named in the text.
7. **`check_run.py` confines its reads and prints no loss value** (d03, d04). Under its hook, opens and listings outside the run's two folders, the source and Python's installation are refused, including through `..`, `np.fromfile`, `np.memmap`, `os.open`, `glob` and a sibling folder with a similar name. For X2 it can also open R2's terminal and R2's n06 folder, and nothing else of R2. Writes, deletes, renames, processes and sockets are refused. A sentinel planted in every loss field and array of the dummy runs did not appear in its output, on sound or on corrupted data. Two limits, neither used by the script: metadata calls such as `os.stat` are not confined, and the hook is installed after one read of the activation's `AUTHORIZATION.json`, as its docstring says (`check_run.py:10`). It does read the loss arrays, to hash them and test that they are finite.
8. **The known inventory gap is described consistently.** The terminal's inventory is taken before `TERMINAL.json` is written and includes `cache\`, which is the worker's `TMPDIR` (`matched_worker.py:373–374`; `text_framework_setup.py:18`). The check's logic reports the gap only for exactly one file carried by every receipt's ledger (d03).
9. **The parent-folder account matches the code.** The builder makes the activation folder without its parent (`:136`). The worker reads the free space of the run folder's parent and makes the run folder without it (`matched_worker.py:310, 312`), after the owner script's claim (`MATCHED_OWNER_RUN.ps1:79`), and the owner script does not look for it. Without `runs\`, R1 would have failed after its claim and left no terminal, hence no retry.
10. **R2's failure matches the sealed guard.** The guard raises `Sampled GPU limit` when the device reading exceeds `gpu_sampled_bytes` (`text_worker.py:115–117`), on every forward pass through the pre-hook (`:238, 258`). Width 768 is a draw's first width (`matched_worker.py:268`). The worker's reserved peak did not rise, so the cause lay outside its own allocations, as the notes infer.
11. **Nothing published allows an interim look.** The tree holds no N8 run folder, array, record or state (section 5). Since registration the N8 folder gained four text files and changed `README.md` and the builder's two lines; nothing else. Releases v2.0 and v2.1 have no assets. The repository has one branch, one merged pull request, no other issue, no Actions artifact and no wiki. The notes publish statuses, times, memory readings, two hash prefixes and the E0 verdicts, from which no loss can be derived.
12. **The pilot and the seed draw precede the registration, and relate to it as the README says.** The pilot log's SHA-256 and the registry's pins are inside the registration commit. The pilot's five seeds are in `EXCLUSIONS.json` and none is a registry seed. The pilot ran N7's m01 (`"sequences_in_n8_fresh_pool": 0`), with `"loss_read": false`. The worker, engine and model files have the same hashes in the pilot's subject and the sealed one (d01). The pilot log has no time stamp of its own; its date is in its approval id.
13. **The history replacement of 12 November** (a force push seen in GitHub's activity log) is disclosed (`PUBLICATION_NOTES.md:166`) and precedes the registration.

#### 3. Before N8 resumes

In order of weight. None requires changing a registered rule or file.

1. **Fix the paused data and close D1.** Publish the SHA-256 of every loss-bearing file of n01–n06 and of what R2 left of n06. Publish the run records that hold no loss value (section 1d). The three terminal hashes already in the notes then become checkable, and each run can be shown to follow the merge commit.
2. **A dated note on the pause (D2):** its reason, who decides to resume and on what, and that the decision uses no N8 data.
3. **A dated note fixing how the analysis reads the runs (D3, D9),** before any p\* is computed: which folder each draw is read from, what "completed" means, that R2's n06 leftovers are not read, and what happens if a run leaves no terminal.
4. **Find out what the guard's reading measures before relying on a memory threshold (D4).** The paired readings are already in the gate records of seven draws. State the 28.2 MiB margin at start-up and the fact that a start-up stop leaves one attempt for three draws. The owner's commands are not registered and can be adjusted with a dated note; the sealed limits cannot.
5. **Make the completeness check agree with the sealed code's refused-start records (F-d1),** and give its SHA-256 with every result (D8).
6. **Record what the sealed code does not:** the new check's readings and refusals (D7), each run's stage cap beside its draws' times (F-d2), and the driver version and Windows build of each run (F-d3).

#### 4. Scripts I wrote (all post hoc), with their commands and output

All are in `C:\Users\rafli\AppData\Local\Temp\swa21\d\scratch`. They read only my clone and dummy folders they create in the scratch folder. The published `check_run.py` and `RUN_COMMAND.ps1` were never run: d03, d04 and d06 run a scratch copy of the check whose one changed line is `STUDY`, and d05 executes eleven and three lines taken unchanged from `RUN_COMMAND.ps1` with `$study` set to a dummy folder.

##### 4.1 `d01_hash_checks.py`: pinned hashes, the sealed source, the three subjects, the pilot seeds, the terminal hashes

Command:

```
"C:\Users\rafli\AppData\Local\Programs\Python\Python312\python.exe" -I -B d01_hash_checks.py "C:\Users\rafli\AppData\Local\Temp\swa21\d\repo"
```

Script:

```python
"""POST HOC audit script (area D). Reads only the auditor's clone. Checks:
 1. every hash pinned in X2_COMMAND.txt and RUN_COMMAND.ps1 against the published files;
 2. source/ against SOURCE_SUBJECT.json (path, bytes, sha256);
 3. which sealed files differ between the pilot's subject, the pre-pin subject and the sealed subject;
 4. the pilot's five seeds against the registry's exclusions and the registry's own seeds;
 5. the terminal hashes and other 64-hex strings in OPERATIONAL_NOTES.md: do they occur anywhere else in the repository?
"""
import hashlib, json, re, sys
from pathlib import Path
REPO = Path(sys.argv[1]); N8 = REPO / 'preregistration' / 'natural-text-dense-replication-20261114'
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()

print('== 1. hashes pinned in the owner commands')
pins = {'tools/build_n8_activation.py': 'c31fd4aa32873a1d025621f06bcc66e289c16ad86f64612c00dad76b1fd62904',
        'source/SOURCE_SUBJECT.json': '9bdea3a9715b05393afe6713ddc696834dd344c3485c4e1a6ed0fa222f44bb6b',
        'pilot/PILOT_LOG.json': '251d0951e30250afa16cb998b06550358c09234d8a24c45166b08d0642347db6'}
for name in ('X2_COMMAND.txt', 'RUN_COMMAND.ps1'):
    text = (N8 / name).read_text(encoding='utf-8')
    found = sorted(set(re.findall(r'\b[0-9a-f]{64}\b', text))); print(name, 'has', len(found), 'distinct 64-hex strings')
    for h in found:
        owner = [p for p, v in pins.items() if v == h]
        print('  ', h, '->', owner[0] + (' MATCHES published file' if sha(N8 / owner[0]) == h else ' DIFFERS from published file') if owner else 'not a published-file pin (see below)')
    print('   merge commit c6f98b26669f5d29f30c576b6d800c1fc82c98eb named:', 'c6f98b26669f5d29f30c576b6d800c1fc82c98eb' in text)
print('sha256 of the two commands and check_run.py as published:')
for name in ('X2_COMMAND.txt', 'RUN_COMMAND.ps1', 'check_run.py', 'OPERATIONAL_NOTES.md'): print('  ', name, sha(N8 / name))

print('== 2. source/ against SOURCE_SUBJECT.json')
subj = json.loads((N8 / 'source/SOURCE_SUBJECT.json').read_bytes())
bad = [f['path'] for f in subj['files'] if sha(N8 / 'source' / f['path']) != f['sha256'] or (N8 / 'source' / f['path']).stat().st_size != f['bytes']]
on_disk = sorted(p.relative_to(N8 / 'source').as_posix() for p in (N8 / 'source').rglob('*') if p.is_file())
listed = sorted(f['path'] for f in subj['files'])
print('   files listed', len(listed), '; changed:', bad, '; on disk but not listed:', sorted(set(on_disk) - set(listed)), '; listed but absent:', sorted(set(listed) - set(on_disk)))

print('== 3. subjects: pilot vs pre-pin vs sealed')
def table(p): return {f['path']: f['sha256'] for f in json.loads(Path(p).read_bytes())['files']}
sealed, pilot, prepin = table(N8 / 'source/SOURCE_SUBJECT.json'), table(N8 / 'seal/pilot/SOURCE_SUBJECT.json'), table(N8 / 'seal/pre-pin/SOURCE_SUBJECT.json')
print('   sha256 seal/pilot/SOURCE_SUBJECT.json  ', sha(N8 / 'seal/pilot/SOURCE_SUBJECT.json'))
print('   sha256 seal/pre-pin/SOURCE_SUBJECT.json', sha(N8 / 'seal/pre-pin/SOURCE_SUBJECT.json'))
for a, b, name in ((pilot, sealed, 'pilot -> sealed'), (prepin, sealed, 'pre-pin -> sealed'), (pilot, prepin, 'pilot -> pre-pin')):
    print('  ', name, ': differing', sorted(k for k in set(a) & set(b) if a[k] != b[k]), '; only in first', sorted(set(a) - set(b)), '; only in second', sorted(set(b) - set(a)))
for n in ('MATCHED_OWNER_RUN.ps1', 'matched_plan.py', 'README.md'):
    print('   seal/pre-pin/' + n, 'equals the pre-pin subject entry:', sha(N8 / 'seal/pre-pin' / n) == prepin.get(n))

print('== 4. the pilot seeds')
log = json.loads((N8 / 'pilot/PILOT_LOG.json').read_bytes()); seeds = log['seeds']
ex = json.loads((N8 / 'registry/n8-seed-registry/EXCLUSIONS.json').read_bytes()); reg = json.loads((N8 / 'registry/n8-seed-registry/REGISTRY.json').read_bytes())
def ints(o):
    if isinstance(o, bool): return
    if isinstance(o, int): yield o
    elif isinstance(o, dict):
        for v in o.values(): yield from ints(v)
    elif isinstance(o, list):
        for v in o: yield from ints(v)
exs, regs = set(ints(ex)), set()
for g in reg['groups']: regs |= {v for k, v in g.items() if k != 'group' and isinstance(v, int)}
regs |= set(ints(reg.get('benchmark', {}))); regs.add(reg.get('partition_seed'))
print('   pilot seeds:', seeds)
print('   each in EXCLUSIONS.json:', {k: v in exs for k, v in seeds.items()})
print('   any among the registry seeds:', sorted(set(seeds.values()) & regs))
print('   pilot log keys with "loss":', [k for k in log if 'loss' in k.lower()], '; loss_read =', log.get('loss_read'), '; p_star_fitted =', log.get('p_star_fitted'), '; run_folder_deleted =', log.get('run_folder_deleted'))
print('   registry groups:', len(reg['groups']), [g['group'] for g in reg['groups']][:3], '...', reg['groups'][-1]['group'])

print('== 5. 64-hex strings of OPERATIONAL_NOTES.md elsewhere in the repository')
notes = (N8 / 'OPERATIONAL_NOTES.md').read_text(encoding='utf-8')
hexes = sorted(set(re.findall(r'\b[0-9a-f]{64}\b', notes)))
texts = {}
for p in REPO.rglob('*'):
    if p.is_file() and '.git' not in p.parts and p.stat().st_size < 20_000_000:
        try: texts[p.relative_to(REPO).as_posix()] = p.read_bytes()
        except OSError: pass
for h in hexes:
    where = sorted(k for k, b in texts.items() if h.encode() in b)
    print('  ', h, '->', where)
```

Output:

```
== 1. hashes pinned in the owner commands
X2_COMMAND.txt has 4 distinct 64-hex strings
   251d0951e30250afa16cb998b06550358c09234d8a24c45166b08d0642347db6 -> pilot/PILOT_LOG.json MATCHES published file
   2a02e9573e4009c066d43bbf9e7d25d588dc10bd763865828cc8e59007607fe8 -> not a published-file pin (see below)
   9bdea3a9715b05393afe6713ddc696834dd344c3485c4e1a6ed0fa222f44bb6b -> source/SOURCE_SUBJECT.json MATCHES published file
   c31fd4aa32873a1d025621f06bcc66e289c16ad86f64612c00dad76b1fd62904 -> tools/build_n8_activation.py MATCHES published file
   merge commit c6f98b26669f5d29f30c576b6d800c1fc82c98eb named: True
RUN_COMMAND.ps1 has 3 distinct 64-hex strings
   251d0951e30250afa16cb998b06550358c09234d8a24c45166b08d0642347db6 -> pilot/PILOT_LOG.json MATCHES published file
   9bdea3a9715b05393afe6713ddc696834dd344c3485c4e1a6ed0fa222f44bb6b -> source/SOURCE_SUBJECT.json MATCHES published file
   c31fd4aa32873a1d025621f06bcc66e289c16ad86f64612c00dad76b1fd62904 -> tools/build_n8_activation.py MATCHES published file
   merge commit c6f98b26669f5d29f30c576b6d800c1fc82c98eb named: True
sha256 of the two commands and check_run.py as published:
   X2_COMMAND.txt e6b5e05ba21445e92458d1fb28b897cef5132090329cb026fb4e6cbdf65c99ef
   RUN_COMMAND.ps1 5148dc07554c9685a60d6623b0096d8ccdb82bae8dc29941c9c4b7944e139f2e
   check_run.py 4df2aba506af47277599e411ddb988fdfc1dfa683695d16fb92f39b4110d9aa4
   OPERATIONAL_NOTES.md 99e3429a52331da44fa5b11f089cefbb5ada640698b692ab6b313af8531a9f4a
== 2. source/ against SOURCE_SUBJECT.json
   files listed 31 ; changed: [] ; on disk but not listed: ['AUTHORIZATION.json', 'SOURCE_SUBJECT.json'] ; listed but absent: []
== 3. subjects: pilot vs pre-pin vs sealed
   sha256 seal/pilot/SOURCE_SUBJECT.json   9743b179e3c2b809add53cfe6d706c189634e22b3776bec843a180f0675e6941
   sha256 seal/pre-pin/SOURCE_SUBJECT.json 9209b566d3a7a97b54b079aaea6ec5d72ab0e0178755e9b6c8260f980dc57986
   pilot -> sealed : differing ['MATCHED_OWNER_RUN.ps1', 'README.md', 'matched_plan.py', 'matched_registry.py'] ; only in first [] ; only in second []
   pre-pin -> sealed : differing ['MATCHED_OWNER_RUN.ps1', 'README.md', 'matched_plan.py'] ; only in first [] ; only in second []
   pilot -> pre-pin : differing ['MATCHED_OWNER_RUN.ps1', 'README.md', 'matched_plan.py', 'matched_registry.py'] ; only in first [] ; only in second []
   seal/pre-pin/MATCHED_OWNER_RUN.ps1 equals the pre-pin subject entry: True
   seal/pre-pin/matched_plan.py equals the pre-pin subject entry: True
   seal/pre-pin/README.md equals the pre-pin subject entry: True
== 4. the pilot seeds
   pilot seeds: {'adapt_order_seed': 90809628, 'benchmark_seed': 578352808, 'init_seed': 1188503724, 'pretrain_order_seed': 46458185, 'weight_seed': 1894175819}
   each in EXCLUSIONS.json: {'adapt_order_seed': True, 'benchmark_seed': True, 'init_seed': True, 'pretrain_order_seed': True, 'weight_seed': True}
   any among the registry seeds: []
   pilot log keys with "loss": ['loss_read'] ; loss_read = False ; p_star_fitted = False ; run_folder_deleted = True
   registry groups: 24 ['n01', 'n02', 'n03'] ... n24
== 5. 64-hex strings of OPERATIONAL_NOTES.md elsewhere in the repository
   2a02e9573e4009c066d43bbf9e7d25d588dc10bd763865828cc8e59007607fe8 -> ['preregistration/natural-text-dense-replication-20261114/OPERATIONAL_NOTES.md', 'preregistration/natural-text-dense-replication-20261114/X2_COMMAND.txt']
   4ffead3f0c46e7f16d789a3368c753013417a51b8c9b92261d8f9d65c22b4c68 -> ['preregistration/natural-text-dense-replication-20261114/OPERATIONAL_NOTES.md']
   f92644a3d989d4b221685f12cfe04518e56072221e3bb336240ba5c9ed931606 -> ['preregistration/natural-text-dense-replication-20261114/OPERATIONAL_NOTES.md']
```

##### 4.2 `d02_dummy_study.py`: a dummy study with invented contents (every "loss" is the sentinel 6.283185)

Command:

```
"C:\Users\rafli\AppData\Local\Programs\Python\Python312\python.exe" -I -B d02_dummy_study.py "C:\Users\rafli\AppData\Local\Temp\swa21\d\repo" "C:\Users\rafli\AppData\Local\Temp\swa21\d\scratch"
"C:\Users\rafli\AppData\Local\Programs\Python\Python312\python.exe" -I -B d02_dummy_study.py "C:\Users\rafli\AppData\Local\Temp\swa21\d\repo" "C:\Users\rafli\AppData\Local\Temp\swa21\d\scratch" dummy-study-refused refused
```

Script:

```python
"""POST HOC audit script (area D). Builds a DUMMY study folder inside the auditor's scratch folder, with invented contents only
(no N8 data; every "loss" is the sentinel 6.283185), in the layout the sealed worker and owner script write, so that a scratch copy of
the published check_run.py can be exercised without touching the owner's drive D:. Three dummy runs: R1 COMPLETE, R2 FAILED in n06,
X2 COMPLETE (the retry of R2). Each carries the "known gap" of OPERATIONAL_NOTES.md (terminal inventory one file / 2,355 bytes over).

usage: python -I -B d02_dummy_study.py <clone> <scratch> [<dummy folder name> [refused]]
"""
import hashlib, json, os, shutil, sys
from pathlib import Path
import numpy as np

CLONE, SCRATCH = Path(sys.argv[1]), Path(sys.argv[2])
N8 = CLONE / 'preregistration' / 'natural-text-dense-replication-20261114'
STUDY = SCRATCH / (sys.argv[3] if len(sys.argv) > 3 else 'dummy-study')
REFUSED = len(sys.argv) > 4 and sys.argv[4] == 'refused'       # R1 only: one start refused by the sealed owner script before the claim
assert 'swa21' in str(STUDY) and 'scratch' in str(STUDY)
if STUDY.exists(): shutil.rmtree(STUDY)
(STUDY / 'runs').mkdir(parents=True); (STUDY / 'activations').mkdir()
shutil.copytree(N8 / 'source', STUDY / 'source')                      # the published sealed source, for the plan's constants
sys.path.insert(0, str(STUDY / 'source'))
import matched_plan as mp, text_plan as plan, fewepoch_plan as fp      # pure constants

SENTINEL = 6.283185
N, NV, POOL = 1024, plan.N_VALIDATION, 2048
SUBJECT = hashlib.sha256((N8 / 'source/SOURCE_SUBJECT.json').read_bytes()).hexdigest()
REG = json.loads((N8 / 'registry/n8-seed-registry/REGISTRY.json').read_bytes())
SEEDS = {r['group']: {k: v for k, v in r.items() if k != 'group'} for r in REG['groups']}
sha = lambda b: hashlib.sha256(b).hexdigest()
enc = lambda x: (json.dumps(x, sort_keys=True, indent=2) + '\n').encode()
CLOCK = [1_800_000_000_000_000_000]                                   # explicit, increasing mtimes (ns), so "written before" is well defined


def put(path, data):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True); path.write_bytes(data)
    CLOCK[0] += 1_000_000_000; os.utime(path, ns=(CLOCK[0], CLOCK[0])); return dict(bytes=len(data), sha256=sha(data))


def floats(count, value=SENTINEL): return np.full(count, value, dtype='<f4').tobytes()


def inputs_and_orders(run, d):
    rng = np.random.default_rng(SEEDS[d]['adapt_order_seed']); rows = [rng.permutation(N).astype('<i8').tobytes() for _ in range(mp.ORDER_EPOCHS)]
    of = put(run / d / mp.ORDER_FILE, b''.join(rows))
    put(run / d / 'INPUTS.json', enc(dict(seeds=SEEDS[d], n_train=N, widths=[512, 768], readouts=list(mp.READOUTS), weights=[1.0] * N,
                                          order_file=dict(path=f'{d}/{mp.ORDER_FILE}', **of), epoch_order_sha256=[sha(r) for r in rows])))


def e0(run, d, w, salt):
    st = put(run / d / f'w{w}' / 'E0.pt', (f'dummy state {d} {w} {salt}'.encode()) * 50)
    arr = put(run / d / f'w{w}' / 'E0.f32', floats(N + NV, SENTINEL + (1e-3 if salt else 0)))
    return dict(path=f'{d}/w{w}/E0.pt', **st), dict(path=f'{d}/w{w}/E0.f32', **arr)


def full_draw(run, d, salt=''):
    inputs_and_orders(run, d); pre, kept = {}, []
    upd = [fp.readout_update(e, N, plan.BATCH) for e in mp.READOUTS]; per = N // plan.BATCH
    for w in (768, 512):
        st, arr = e0(run, d, w, salt); kept.append(st)
        pre[str(w)] = dict(width=w, parameters=plan.parameters(w), state=st, E0_arrays=arr, pretraining_updates=plan.updates(POOL, plan.PRETRAIN['epochs']),
                           E0_train_loss=SENTINEL, E0_validation_loss=SENTINEL)
        a = put(run / d / f'w{w}' / mp.TAG / 'arrays.f32', floats(28 * (N + NV)))
        put(run / d / f'w{w}' / mp.TAG / 'record.json', enc(dict(stage=d, width=w, lr=1e-4, tag=mp.TAG, status='COMPLETE', n_train=N,
            readouts=[dict(epoch=e, update=u, train_loss=SENTINEL, validation_loss=SENTINEL) for e, u in zip(mp.READOUTS, upd)],
            epochs=[dict(epoch=i + 1, updates=x) for i, x in enumerate([per] * 3 + [upd[-1] - 3 * per])],
            arrays=dict(path=f'{d}/w{w}/{mp.TAG}/arrays.f32', **a), layout=dict(blocks=28, block_epochs=list(mp.READOUTS), train_rows=N, validation_rows=NV))))
    put(run / d / 'PRETRAINED.json', enc(pre))
    put(run / d / 'STATES_KEPT.json', enc(dict(kept=kept, kept_bytes=sum(x['bytes'] for x in kept), errors=[])))


def tree(root): return [p for p in Path(root).rglob('*') if p.is_file()]


def make(mode, done, active=None, first=None, salt=''):
    """One dummy run: `done` complete draws, then (FAILED) the draw it stopped in."""
    run, act = STUDY / 'runs' / f'n8-{mode.lower()}', STUDY / 'activations' / f'n8-{mode.lower()}'
    draws = list(mp.RUN_STAGES[mode]) if mode.startswith('R') else list(done); gated = done + ([active] if active else [])
    aid = f'OWNER-20991231-N8-{mode}-01'
    shutil.copytree(N8 / 'source', act); put(act / 'REGISTRY.json', (N8 / 'registry/n8-seed-registry/REGISTRY.json').read_bytes())
    approval = enc(dict(approval_id=aid, mode=mode, stages=draws, retry_of=mp.RETRY_OF.get(mode), fixture=False, user_text=f'DUMMY: I approve N8 Run {mode} under {aid}.'))
    put(act / 'APPROVAL_RECORD.json', approval)
    auth = dict(approval_id=aid, approval_record_sha256=sha(approval), fixture=False, mode=mode, stages=draws)
    if first is not None:
        raw = (first / 'TERMINAL.json').read_bytes(); put(act / 'FIRST_ATTEMPT_TERMINAL.json', raw); auth['first_attempt_terminal_sha256'] = sha(raw)
    put(act / 'AUTHORIZATION.json', enc(auth))
    put(act / 'OWNER_CLAIM.json', enc(dict(mode=mode, approval_id=aid, subject=SUBJECT, one_use=True)))
    pre = enc(dict(schema=1, stage='PRESTART', verdict='IDLE')); put(act / 'gpu-checks/PRESTART.json', pre)
    put(run / 'BENCHMARK.json', enc(dict(pool_n=POOL, caps=dict(feasible=True, stage_work_cap_seconds=3097))))
    put(run / 'gpu-checks/PRESTART.json', pre)
    if REFUSED and mode == 'R1':                                  # the sealed owner script's record of a refused start; the sealed worker copies it into the run folder (text_worker.prestart)
        ref = enc(dict(schema=1, stage='PRESTART', verdict='REFUSED')); put(act / 'gpu-checks/PRESTART-REFUSED-1.json', ref); put(run / 'gpu-checks/PRESTART-REFUSED-1.json', ref)
    receipts, closed, GAP, state = [], [0, 0], (2355, 1), None
    for d in gated:
        put(run / f'gpu-checks/{d}-REQUEST.json', enc(dict(schema=1, stage=d)))
        resp = enc(dict(schema=1, stage=d, verdict='IDLE')); put(act / f'gpu-checks/{d}-RESPONSE.json', resp); put(run / f'gpu-checks/{d}.json', resp)
        if d == active:
            inputs_and_orders(run, d); state, _ = e0(run, d, 768, ''); break
        full_draw(run, d, salt)
        fs = tree(run / d); closed = [closed[0] + sum(p.stat().st_size for p in fs), closed[1] + len(fs)]
        top = [p for p in run.iterdir() if p.is_file()] + tree(run / 'gpu-checks')
        e0cmp = None
        if first is not None:
            old = lambda w: first / d / f'w{w}' / 'E0.f32'
            e0cmp = {str(w): 'ABSENT' if not old(w).is_file() else 'SAME' if sha(old(w).read_bytes()) == sha((run / d / f'w{w}' / 'E0.f32').read_bytes()) else 'DIFFERENT' for w in (768, 512)}
        r = dict(stage=d, status='COMPLETE', trajectories=2, states_kept=2, state_errors=0, seconds=2700.0, closed_totals=list(closed), e0_against_first_attempt=e0cmp,
                 ledger_total=[closed[0] + sum(p.stat().st_size for p in top) + GAP[0], closed[1] + len(top) + GAP[1]])
        put(run / f'{d}-RECEIPT.json', enc(r)); receipts.append(r)
    fs = tree(run)
    t = dict(kind='n8', subject=SUBJECT, mode=mode, status='COMPLETE' if not active else 'FAILED', draws=draws, stages=receipts, startup=dict(decision='GO', reason='ALL_WIDTHS_WITHIN_LIMIT'),
             bindings={k: auth[k] for k in ('approval_id', 'approval_record_sha256', 'first_attempt_terminal_sha256') if k in auth}, n_train=N, arms={'768': [1e-4], '512': [1e-4]}, readouts=list(mp.READOUTS),
             benchmark=dict(path='BENCHMARK.json', bytes=(run / 'BENCHMARK.json').stat().st_size, sha256=sha((run / 'BENCHMARK.json').read_bytes())),
             stage_folders=sorted(gated), counted_as_attempt=True, elapsed_seconds=7500.0, inventory=dict(bytes=sum(p.stat().st_size for p in fs) + GAP[0], files=len(fs) + GAP[1]))
    if active:
        t.update(error=dict(type='RuntimeError', message='Sampled GPU limit'), active_stage=active,
                 states_on_failure=dict(benchmark=dict(deleted=[]), kept_in_active_stage=dict(kept=[state], kept_bytes=state['bytes'], errors=[])))
    put(run / 'TERMINAL.json', enc(t))
    (run / 'cache').mkdir(); CLOCK[0] += 1_000_000_000; os.utime(run / 'cache', ns=(CLOCK[0], CLOCK[0]))       # emptied just after the terminal was written
    put(act / 'POWER_LOG.jsonl', b'{"power":"AC"}\n'); put(act / 'WORKER_STDOUT.log', b'')
    put(act / 'WORKER_STDERR.log', b'' if not active else b'Traceback (most recent call last):\n  ...\nRuntimeError: Sampled GPU limit\n')
    put(act / 'OWNER_PROGRESS.log', b'2099-12-31 00:00:00  dummy progress line\n')
    gates = sorted(p.name for p in (act / 'gpu-checks').iterdir())
    put(act / 'OWNER_EXIT_RECEIPT.json', enc(dict(status='COMPLETE' if not active else 'FAILED', mode=mode, subject=SUBJECT, exit_observed=True, exit_code=0 if not active else 1, elapsed_seconds=8000.0,
        terminal_status=t['status'], terminal_sha256=sha((run / 'TERMINAL.json').read_bytes()), terminal_unreadable=False, terminal_outside_ledger=False, stop_reason=None,
        stage_folders=sorted(gated), counted_as_attempt=True, retry=mode.startswith('X'),
        gpu_gates=[dict(stage=d, verdict='IDLE', checks=1, off_ac_checks=0) for d in gated], gpu_check_files=[dict(name=n, sha256=sha((act / 'gpu-checks' / n).read_bytes())) for n in gates],
        power_during_run=dict(samples=10, off_ac_samples=0, changes=[]), power_log_sha256=sha((act / 'POWER_LOG.jsonl').read_bytes()))))
    return run


r1 = make('R1', ['n01', 'n02', 'n03'])
r2 = make('R2', ['n04', 'n05'], active='n06')
# X2 repeats n06 with the same seeds and orders; its new w768 E0 array differs from the one R2 left (salted), and R2 left no w512 array.
x2 = make('X2', ['n06'], first=r2, salt='retry')
print('dummy study at', STUDY)
for r in (r1, r2, x2): print(' ', r.name, len(tree(r)), 'files,', sum(p.stat().st_size for p in tree(r)), 'bytes')
print('sentinel loss value used everywhere:', SENTINEL)
```

Output:

```
dummy study at C:\Users\rafli\AppData\Local\Temp\swa21\d\scratch\dummy-study
  n8-r1 48 files, 1237485 bytes
  n8-r2 39 files, 876138 bytes
  n8-x2 18 files, 414063 bytes
sentinel loss value used everywhere: 6.283185
```

Output:

```
dummy study at C:\Users\rafli\AppData\Local\Temp\swa21\d\scratch\dummy-study-refused
  n8-r1 49 files, 1237550 bytes
  n8-r2 39 files, 876138 bytes
  n8-x2 18 files, 414063 bytes
sentinel loss value used everywhere: 6.283185
```

##### 4.3 `d03_run_check_copy.py`: a scratch copy of check_run.py on the dummy runs: number of checks, and whether a loss value is printed

Command:

```
"C:\Users\rafli\AppData\Local\Programs\Python\Python312\python.exe" -I -B d03_run_check_copy.py "C:\Users\rafli\AppData\Local\Temp\swa21\d\repo" "C:\Users\rafli\AppData\Local\Temp\swa21\d\scratch"
```

Script:

```python
"""POST HOC audit script (area D). Makes a scratch copy of the published check_run.py whose ONLY change is the STUDY constant (pointed
at the dummy study in the auditor's scratch folder), then runs that copy on the three dummy runs and reports:
 - the number of checks it performs for a complete run of three draws, a run failed in its third draw, and a one-draw retry
   (to compare with the counts in OPERATIONAL_NOTES.md: 54+1, 46+1, 31+1);
 - whether the sentinel "loss" value planted in every loss field and array (6.283185) appears anywhere in its output;
 - the same on a corrupted copy of the dummy study (failure paths).
The published check_run.py is never run: only the copy, and only on the dummy folders.

usage: python -I -B d03_run_check_copy.py <clone> <scratch>
"""
import difflib, hashlib, re, shutil, subprocess, sys
from pathlib import Path

CLONE, SCRATCH = Path(sys.argv[1]), Path(sys.argv[2])
SRC = CLONE / 'preregistration' / 'natural-text-dense-replication-20261114' / 'check_run.py'
STUDY = SCRATCH / 'dummy-study'
COPY = SCRATCH / 'check_run_copy.py'
PY = sys.executable

text = SRC.read_bytes().decode('utf-8')
old = "STUDY = r'D:\\sequence-weighting-n8'"
assert text.count(old) == 1, text.count(old)
assert "'" not in str(STUDY)
new = text.replace(old, "STUDY = r'" + str(STUDY) + "'")
COPY.write_bytes(new.encode('utf-8'))
print('published check_run.py sha256:', hashlib.sha256(SRC.read_bytes()).hexdigest())
print('diff published -> scratch copy:')
for line in difflib.unified_diff(text.splitlines(), new.splitlines(), 'check_run.py', 'check_run_copy.py', lineterm='', n=0): print('   ', line)
print('other mentions of drive D: left in the copy (comments and messages only):', [ln.strip()[:80] for ln in new.splitlines() if re.search(r"D:\\\\", ln)])


def run(mode, study=STUDY, extra=()):
    p = subprocess.run([PY, '-I', '-B', str(COPY), mode, '--study', str(study), '--n-train', '1024', *extra], capture_output=True, text=True, encoding='utf-8')
    out = p.stdout + p.stderr
    passes, fails = len(re.findall(r'^PASS  ', out, re.M)), len(re.findall(r'^FAIL  ', out, re.M))
    return p.returncode, out, passes, fails


for mode in ('R1', 'R2', 'X2'):
    rc, out, passes, fails = run(mode)
    (SCRATCH / f'd03_check_{mode}.out').write_text(out, encoding='utf-8')
    summary = [ln for ln in out.splitlines() if re.search(r'passed, .* failed|inventory failure|did not complete', ln)]
    print(f'== {mode}: exit {rc}; PASS lines {passes}, FAIL lines {fails}, total checks {passes + fails}')
    for ln in summary: print('    ' + ln[:230])
    print('    failed checks:', [ln[6:90] for ln in out.splitlines() if ln.startswith('FAIL  ')])
    print('    sentinel 6.28 in output:', '6.28' in out, '| any float with 4+ decimals printed:', sorted(set(re.findall(r'\b\d+\.\d{4,}\b', out)))[:8])

# Failure paths: a corrupted copy of the dummy study (truncated arrays, a missing key, a non-finite mean, an unreadable record).
BAD = SCRATCH / 'dummy-study-corrupt'
if BAD.exists(): shutil.rmtree(BAD)
shutil.copytree(STUDY, BAD)
import json
r1 = BAD / 'runs' / 'n8-r1'
a = r1 / 'n01' / 'w768' / 'lr1e-04' / 'arrays.f32'; a.write_bytes(a.read_bytes()[:-3])
p = r1 / 'n01' / 'PRETRAINED.json'; j = json.loads(p.read_bytes()); del j['512']['E0_validation_loss']; p.write_bytes(json.dumps(j).encode())
p = r1 / 'n02' / 'w512' / 'lr1e-04' / 'record.json'; j = json.loads(p.read_bytes()); j['readouts'][3]['train_loss'] = float('nan'); p.write_bytes(json.dumps(j).encode())
p = r1 / 'n03' / 'w768' / 'lr1e-04' / 'record.json'; p.write_bytes(p.read_bytes()[:200])
p = r1 / 'n03' / 'w512' / 'E0.f32'; p.write_bytes(b'\x00' * 7)
rc, out, passes, fails = run('R1', BAD)
(SCRATCH / 'd03_check_R1_corrupt.out').write_text(out, encoding='utf-8')
print(f'== R1 on the corrupted dummy: exit {rc}; PASS {passes}, FAIL {fails}, total {passes + fails}')
print('    sentinel 6.28 in output:', '6.28' in out, '| "nan" in output:', 'nan' in out.lower(), '| floats with 4+ decimals:', sorted(set(re.findall(r'\b\d+\.\d{4,}\b', out)))[:8])
for ln in out.splitlines():
    if ln.startswith('FAIL  '): print('    ' + ln[:60] + ' ... ' + (ln[ln.rfind('['):][:150] if '[' in ln else ''))
```

Output:

```
published check_run.py sha256: 4df2aba506af47277599e411ddb988fdfc1dfa683695d16fb92f39b4110d9aa4
diff published -> scratch copy:
    --- check_run.py
    +++ check_run_copy.py
    @@ -25 +25 @@
    -STUDY = r'D:\sequence-weighting-n8'
    +STUDY = r'C:\Users\rafli\AppData\Local\Temp\swa21\d\scratch\dummy-study'
other mentions of drive D: left in the copy (comments and messages only): []
== R1: exit 1; PASS lines 54, FAIL lines 1, total checks 55
    54 passed, 1 failed
    The inventory failure is the known operational gap (OPERATIONAL_NOTES.md): 1 file, 2,355 bytes; every stage receipt's ledger carries the same (1 file, 2,355 bytes; 1 file, 2,355 bytes; 1 file, 2,355 bytes); cache\ is empty and was
    failed checks: ["the terminal's inventory (files only, text_worker.Output.inventory) equals the run f"]
    sentinel 6.28 in output: False | any float with 4+ decimals printed: []
== R2: exit 1; PASS lines 46, FAIL lines 1, total checks 47
    46 passed, 1 failed
    The inventory failure is the known operational gap (OPERATIONAL_NOTES.md): 1 file, 2,355 bytes; every stage receipt's ledger carries the same (1 file, 2,355 bytes; 1 file, 2,355 bytes); cache\ is empty and was last changed 1,000 m
    Run R2 did not complete: n04, n05 complete; n06 left for the retry run X2 (protocol section 8)
    failed checks: ["the terminal's inventory (files only, text_worker.Output.inventory) equals the run f"]
    sentinel 6.28 in output: False | any float with 4+ decimals printed: []
== X2: exit 1; PASS lines 31, FAIL lines 1, total checks 32
    PASS  FIRST_ATTEMPT_TERMINAL.json is R2's terminal byte for byte, bound by the activation and this terminal; R2 did not complete; this run's draws are those it did not complete  [R2's terminal 55153c35dd237412d7d35971bf5e80fa1b5f2
    31 passed, 1 failed
    The inventory failure is the known operational gap (OPERATIONAL_NOTES.md): 1 file, 2,355 bytes; every stage receipt's ledger carries the same (1 file, 2,355 bytes); cache\ is empty and was last changed 1,000 ms after TERMINAL.json
    failed checks: ["the terminal's inventory (files only, text_worker.Output.inventory) equals the run f"]
    sentinel 6.28 in output: False | any float with 4+ decimals printed: []
== R1 on the corrupted dummy: exit 1; PASS 45, FAIL 10, total 55
    sentinel 6.28 in output: False | "nan" in output: False | floats with 4+ decimals: []
    FAIL  the terminal's inventory (files only, text_worker.Outp ... [terminal 1,237,668 bytes in 48 files; now 1,223,541 in 47]
    FAIL  n01 w768: arrays.f32 is 28 blocks of 1,024 + 512 float ... [172,029 bytes, 1f7ebdc912ff1e94]
    FAIL  n01 w512: E0.f32 is 1,024 + 512 float32 with the hash  ... [KeyError: 'E0_validation_loss']
    FAIL  n02 w512: record COMPLETE; 28 readouts at the plan's e ... 
    FAIL  n03 w768: record COMPLETE; 28 readouts at the plan's e ... [TypeError: 'NoneType' object is not subscriptable]
    FAIL  n03 w768: arrays.f32 is 28 blocks of 1,024 + 512 float ... [TypeError: 'NoneType' object is not subscriptable]
    FAIL  n03 w512: E0.f32 is 1,024 + 512 float32 with the hash  ... 
    FAIL  n01-RECEIPT: COMPLETE, 2 trajectories, 2 states kept,  ... [2,700 s on the worker clock]
    FAIL  n02-RECEIPT: COMPLETE, 2 trajectories, 2 states kept,  ... [2,700 s on the worker clock]
    FAIL  n03-RECEIPT: COMPLETE, 2 trajectories, 2 states kept,  ... [2,700 s on the worker clock]
```

The full output of each dummy check is in `d03_check_R1.out`, `d03_check_R2.out`, `d03_check_X2.out` and `d03_check_R1_corrupt.out` in the scratch folder.

##### 4.4 `d04_hook_test.py`: the audit hook of check_run.py, through the scratch copy, on the dummy study

Command:

```
"C:\Users\rafli\AppData\Local\Programs\Python\Python312\python.exe" -I -B d04_hook_test.py "C:\Users\rafli\AppData\Local\Temp\swa21\d\scratch" X2
"C:\Users\rafli\AppData\Local\Programs\Python\Python312\python.exe" -I -B d04_hook_test.py "C:\Users\rafli\AppData\Local\Temp\swa21\d\scratch" R1   (below: the X2 output in full, then the R1 lines that differ in kind)
```

Script:

```python
"""POST HOC audit script (area D). Tests the audit hook of the published check_run.py (read_only + roots) on the DUMMY study in the
auditor's scratch folder, through the scratch copy check_run_copy.py (one line changed: STUDY). It installs the hook exactly as main()
does for mode X2, then tries reads, listings, writes, processes and network use inside and outside the allowed roots, and prints what
was allowed or refused. Nothing on drive D: is touched: every path is inside the scratch folder.

usage: python -I -B d04_hook_test.py <scratch> <mode>
"""
import importlib.util, os, sys
from pathlib import Path

SCRATCH, MODE = Path(sys.argv[1]), sys.argv[2]
STUDY = SCRATCH / 'dummy-study'
spec = importlib.util.spec_from_file_location('check_run_copy', SCRATCH / 'check_run_copy.py'); cr = importlib.util.module_from_spec(spec); spec.loader.exec_module(cr)
assert os.path.normcase(cr.STUDY) == os.path.normcase(str(STUDY))

# An outside file, a sibling folder whose name starts like an allowed root, both inside the scratch folder (made before the hook).
outside = SCRATCH / 'outside-root'; outside.mkdir(exist_ok=True); (outside / 'secret.f32').write_bytes(b'\x00' * 16)
sibling = STUDY / 'runs' / f'n8-{MODE.lower()}-other'; sibling.mkdir(exist_ok=True); (sibling / 'x.json').write_bytes(b'{}')

roots = cr.roots(str(STUDY), MODE)
print('roots for', MODE + ':'); [print('   ', os.path.relpath(r, SCRATCH)) for r in roots]
cr.read_only(roots)                                     # irreversible for this process, as in check_run.main()
import glob, json, shutil, socket, subprocess
import numpy as np                                      # imported after the hook, as check_run.py does
print('numpy imported under the hook:', np.__version__)

run, act = STUDY / 'runs' / f'n8-{MODE.lower()}', STUDY / 'activations' / f'n8-{MODE.lower()}'
r2, r1 = STUDY / 'runs' / 'n8-r2', STUDY / 'runs' / 'n8-r1'


def attempt(label, fn):
    try: fn(); print(f'  ALLOWED  {label}')
    except PermissionError as e: print(f'  REFUSED  {label}   [{str(e)[:70]}]')
    except Exception as e: print(f'  ERROR    {label}   [{type(e).__name__}: {str(e)[:70]}]')


print('-- reads inside the allowed roots')
attempt('open run TERMINAL.json', lambda: open(run / 'TERMINAL.json', 'rb').close())
attempt('open activation AUTHORIZATION.json', lambda: open(act / 'AUTHORIZATION.json', 'rb').close())
attempt('open source matched_plan.py', lambda: open(STUDY / 'source' / 'matched_plan.py', 'rb').close())
attempt('same path in upper case', lambda: open(str(run / 'TERMINAL.json').upper(), 'rb').close())
attempt('list the run folder (os.listdir)', lambda: os.listdir(run))
attempt('rglob the run folder', lambda: list(run.rglob('*')))
attempt('np.frombuffer of a run array via read_bytes', lambda: np.frombuffer(next(run.rglob('arrays.f32')).read_bytes(), dtype='<f4'))
print('-- the first attempt R2 (allowed only for X2: its terminal and the folders of the draws X2 repeats)')
attempt('open R2 TERMINAL.json', lambda: open(r2 / 'TERMINAL.json', 'rb').close())
attempt('open R2 n06/INPUTS.json (the draw X2 repeats)', lambda: open(r2 / 'n06' / 'INPUTS.json', 'rb').close())
attempt('open R2 n06/w768/E0.f32', lambda: open(r2 / 'n06' / 'w768' / 'E0.f32', 'rb').close())
attempt('open R2 n04/INPUTS.json (a draw X2 does not repeat)', lambda: open(r2 / 'n04' / 'INPUTS.json', 'rb').close())
attempt('open R2 n04/w768/lr1e-04/arrays.f32', lambda: open(r2 / 'n04' / 'w768' / 'lr1e-04' / 'arrays.f32', 'rb').close())
attempt('open R2 BENCHMARK.json', lambda: open(r2 / 'BENCHMARK.json', 'rb').close())
attempt('open R2 n04-RECEIPT.json', lambda: open(r2 / 'n04-RECEIPT.json', 'rb').close())
attempt('list R2 run folder', lambda: os.listdir(r2))
attempt('open activations/n8-r2/OWNER_EXIT_RECEIPT.json', lambda: open(STUDY / 'activations' / 'n8-r2' / 'OWNER_EXIT_RECEIPT.json', 'rb').close())
print('-- other runs and anything else')
attempt('open R1 TERMINAL.json', lambda: open(r1 / 'TERMINAL.json', 'rb').close())
attempt('open R1 array via np.fromfile', lambda: np.fromfile(r1 / 'n01' / 'w768' / 'lr1e-04' / 'arrays.f32', dtype='<f4'))
attempt('np.memmap of an R1 array', lambda: np.memmap(r1 / 'n01' / 'w768' / 'lr1e-04' / 'arrays.f32', dtype='<f4', mode='r'))
attempt('os.open(O_RDONLY) of an R1 array', lambda: os.close(os.open(r1 / 'n01' / 'w768' / 'E0.f32', os.O_RDONLY)))
attempt('open through ..\\ from the run folder', lambda: open(str(run) + '\\..\\n8-r1\\TERMINAL.json', 'rb').close())
attempt('open a file in a sibling folder n8-<run>-other', lambda: open(sibling / 'x.json', 'rb').close())
attempt('open a file outside the study', lambda: open(outside / 'secret.f32', 'rb').close())
attempt('list runs\\', lambda: os.listdir(STUDY / 'runs'))
attempt('os.scandir of the study folder', lambda: list(os.scandir(STUDY)))
attempt('os.walk of R1 (first step)', lambda: next(os.walk(r1, onerror=lambda e: (_ for _ in ()).throw(e))))
attempt('glob R1 arrays', lambda: glob.glob(str(r1 / '*' / '*' / '*' / 'arrays.f32')))
print('-- writes, processes, network')
attempt('open a run file for append', lambda: open(run / 'TERMINAL.json', 'ab').close())
attempt('create a file in the run folder', lambda: open(run / 'new.txt', 'w').close())
attempt('Path.write_bytes in the activation', lambda: (act / 'new.bin').write_bytes(b'x'))
attempt('os.remove a run file', lambda: os.remove(run / 'BENCHMARK.json'))
attempt('os.rename a run file', lambda: os.rename(run / 'BENCHMARK.json', run / 'B.json'))
attempt('os.mkdir in the run folder', lambda: os.mkdir(run / 'newdir'))
attempt('shutil.copyfile out of the run folder', lambda: shutil.copyfile(run / 'BENCHMARK.json', outside / 'copy.json'))
attempt('subprocess.run', lambda: subprocess.run(['cmd', '/c', 'echo', 'x'], capture_output=True))
attempt('os.system', lambda: os.system('echo x'))
attempt('socket.socket()', lambda: socket.socket().close())
print('-- not covered by the hook (no audit event carries a path that it checks): metadata only')
attempt('os.stat of an R1 array (size, times)', lambda: os.stat(r1 / 'n01' / 'w768' / 'lr1e-04' / 'arrays.f32'))
attempt('Path.exists / is_file outside the roots', lambda: (outside / 'secret.f32').is_file())
attempt('shutil.disk_usage of the drive', lambda: shutil.disk_usage(STUDY.anchor))
print('files in the run folder unchanged:', sorted(p.name for p in run.iterdir()))
```

Output:

```
roots for X2:
    dummy-study\runs\n8-x2
    dummy-study\activations\n8-x2
    dummy-study\source
    dummy-study\runs\n8-r2\TERMINAL.json
    dummy-study\runs\n8-r2\n06
numpy imported under the hook: 2.5.3
-- reads inside the allowed roots
  ALLOWED  open run TERMINAL.json
  ALLOWED  open activation AUTHORIZATION.json
  ALLOWED  open source matched_plan.py
  ALLOWED  same path in upper case
  ALLOWED  list the run folder (os.listdir)
  ALLOWED  rglob the run folder
  ALLOWED  np.frombuffer of a run array via read_bytes
-- the first attempt R2 (allowed only for X2: its terminal and the folders of the draws X2 repeats)
  ALLOWED  open R2 TERMINAL.json
  ALLOWED  open R2 n06/INPUTS.json (the draw X2 repeats)
  ALLOWED  open R2 n06/w768/E0.f32
  REFUSED  open R2 n04/INPUTS.json (a draw X2 does not repeat)   [check_run.py reads only its run, its activation and the source: C:\Use]
  REFUSED  open R2 n04/w768/lr1e-04/arrays.f32   [check_run.py reads only its run, its activation and the source: C:\Use]
  REFUSED  open R2 BENCHMARK.json   [check_run.py reads only its run, its activation and the source: C:\Use]
  REFUSED  open R2 n04-RECEIPT.json   [check_run.py reads only its run, its activation and the source: C:\Use]
  REFUSED  list R2 run folder   [check_run.py lists only its run, its activation and the source: C:\Use]
  REFUSED  open activations/n8-r2/OWNER_EXIT_RECEIPT.json   [check_run.py reads only its run, its activation and the source: C:\Use]
-- other runs and anything else
  REFUSED  open R1 TERMINAL.json   [check_run.py reads only its run, its activation and the source: C:\Use]
  REFUSED  open R1 array via np.fromfile   [check_run.py reads only its run, its activation and the source: C:\Use]
  REFUSED  np.memmap of an R1 array   [check_run.py reads only its run, its activation and the source: C:\Use]
  REFUSED  os.open(O_RDONLY) of an R1 array   [check_run.py reads only its run, its activation and the source: C:\Use]
  REFUSED  open through ..\ from the run folder   [check_run.py reads only its run, its activation and the source: C:\Use]
  REFUSED  open a file in a sibling folder n8-<run>-other   [check_run.py reads only its run, its activation and the source: C:\Use]
  REFUSED  open a file outside the study   [check_run.py reads only its run, its activation and the source: C:\Use]
  REFUSED  list runs\   [check_run.py lists only its run, its activation and the source: C:\Use]
  REFUSED  os.scandir of the study folder   [check_run.py lists only its run, its activation and the source: C:\Use]
  REFUSED  os.walk of R1 (first step)   [check_run.py lists only its run, its activation and the source: C:\Use]
  REFUSED  glob R1 arrays   [check_run.py lists only its run, its activation and the source: C:\Use]
-- writes, processes, network
  REFUSED  open a run file for append   [check_run.py writes nothing: C:\Users\rafli\AppData\Local\Temp\swa21\d]
  REFUSED  create a file in the run folder   [check_run.py writes nothing: C:\Users\rafli\AppData\Local\Temp\swa21\d]
  REFUSED  Path.write_bytes in the activation   [check_run.py writes nothing: C:\Users\rafli\AppData\Local\Temp\swa21\d]
  REFUSED  os.remove a run file   [check_run.py refuses os.remove]
  REFUSED  os.rename a run file   [check_run.py refuses os.rename]
  REFUSED  os.mkdir in the run folder   [check_run.py refuses os.mkdir]
  REFUSED  shutil.copyfile out of the run folder   [check_run.py refuses shutil.copyfile]
  REFUSED  subprocess.run   [check_run.py refuses subprocess.Popen]
  REFUSED  os.system   [check_run.py refuses os.system]
  REFUSED  socket.socket()   [check_run.py refuses socket.__new__]
-- not covered by the hook (no audit event carries a path that it checks): metadata only
  ALLOWED  os.stat of an R1 array (size, times)
  ALLOWED  Path.exists / is_file outside the roots
  ALLOWED  shutil.disk_usage of the drive
files in the run folder unchanged: ['BENCHMARK.json', 'TERMINAL.json', 'cache', 'gpu-checks', 'n06', 'n06-RECEIPT.json']
```

Output for R1 (selected lines):

```
roots for R1:
    dummy-study\runs\n8-r1
    dummy-study\activations\n8-r1
    dummy-study\source
  REFUSED  open R2 TERMINAL.json   [check_run.py reads only its run, its activation and the source: C:\Use]
  REFUSED  open R2 n06/INPUTS.json (the draw X2 repeats)   [check_run.py reads only its run, its activation and the source: C:\Use]
  ALLOWED  open R1 TERMINAL.json
  REFUSED  open a file outside the study   [check_run.py reads only its run, its activation and the source: C:\Use]
```

##### 4.5 `d05_run_order_test.ps1`: the run-order rule and the approval checks of RUN_COMMAND.ps1, on dummy folders (Windows PowerShell 5.1)

Command:

```
& 'C:\Users\rafli\AppData\Local\Temp\swa21\d\scratch\d05_run_order_test.ps1' -Clone 'C:\Users\rafli\AppData\Local\Temp\swa21\d\repo' -Scratch 'C:\Users\rafli\AppData\Local\Temp\swa21\d\scratch'
```

Script:

```powershell
# POST HOC audit script (area D). Tests two pieces of the published RUN_COMMAND.ps1 on DUMMY folders inside the auditor's scratch
# folder: (1) the run-order rule (its lines 93-95), (2) the approval checks (its lines 63-73). The lines are taken from the published
# file by line number and executed unchanged, with $study pointed at a dummy folder. RUN_COMMAND.ps1 itself is never run; nothing on
# drive D: is touched; no builder, git, nvidia-smi or owner script is called (those lines are not among the ones extracted).
param([Parameter(Mandatory=$true)][string]$Clone, [Parameter(Mandatory=$true)][string]$Scratch)
$ErrorActionPreference = 'Stop'
$published = Join-Path $Clone 'preregistration\natural-text-dense-replication-20261114\RUN_COMMAND.ps1'
$lines = [IO.File]::ReadAllLines($published)
$orderRule = ($lines[92..94] -join "`n")        # lines 93-95 (1-based)
$approval = ($lines[62..72] -join "`n")         # lines 63-73
foreach ($bad in 'D:\', 'git ', 'nvidia', 'python', 'MATCHED_OWNER_RUN', 'build_n8') { if ($orderRule.Contains($bad) -or $approval.Contains($bad)) { throw "extracted lines contain $bad" } }
'--- the extracted run-order lines (93-95), first 110 characters of each:'
$lines[92..94] | ForEach-Object { '    ' + $_.Substring(0, [Math]::Min(110, $_.Length)) }

$dummy = Join-Path $Scratch 'ps-dummy-study'
if (-not $dummy.Contains('swa21\d\scratch')) { throw 'dummy path is not in the scratch folder' }
function Reset-Dummy { if (Test-Path -LiteralPath $dummy) { Remove-Item -LiteralPath $dummy -Recurse -Force -Confirm:$false }; New-Item -ItemType Directory -Force -Path (Join-Path $dummy 'activations') | Out-Null }
function Put-Receipt([string]$mode, [string]$status) {
  $d = Join-Path $dummy ('activations\n8-' + $mode.ToLower()); New-Item -ItemType Directory -Force -Path $d | Out-Null
  [IO.File]::WriteAllText((Join-Path $d 'OWNER_EXIT_RECEIPT.json'), (@{status=$status; mode=$mode} | ConvertTo-Json), [Text.UTF8Encoding]::new($false))
}
function Test-Order([string]$label, [scriptblock]$setup) {
  Reset-Dummy; & $setup
  $study = $dummy; $k = 3; $prev = 2
  try { Invoke-Expression $orderRule; "  PROCEEDS  $label" } catch { $m = "$($_.Exception.Message)"; "  STOPS     $label   [" + $m.Substring(0, [Math]::Min(95, $m.Length)) + ']' }
}
'--- (1) run order, Build step of R3 (k = 3, the run before it is R2)'
Test-Order 'no exit receipt of R2' { }
Test-Order 'R2 FAILED, no exit receipt of X2' { Put-Receipt 'R2' 'FAILED' }
Test-Order 'R2 FAILED, X2 built but never claimed (activation folder, no exit receipt)' { Put-Receipt 'R2' 'FAILED'; New-Item -ItemType Directory -Force -Path (Join-Path $dummy 'activations\n8-x2') | Out-Null }
Test-Order 'R2 FAILED, X2 ended COMPLETE' { Put-Receipt 'R2' 'FAILED'; Put-Receipt 'X2' 'COMPLETE' }
Test-Order 'R2 FAILED, X2 ended FAILED' { Put-Receipt 'R2' 'FAILED'; Put-Receipt 'X2' 'FAILED' }
Test-Order 'R2 COMPLETE, no X2' { Put-Receipt 'R2' 'COMPLETE' }
Test-Order 'R2 STOPPED_AT_STARTUP, no X2' { Put-Receipt 'R2' 'STOPPED_AT_STARTUP' }
Test-Order 'R2 EXIT_UNOBSERVED_NO_KILL, no X2' { Put-Receipt 'R2' 'EXIT_UNOBSERVED_NO_KILL' }

function Test-Approval([string]$label, [string]$ApprovalId, [string]$ApprovalText) {
  $k = 3; $draws = @(1..3 | ForEach-Object { 'n{0:d2}' -f (3 * ($k - 1) + $_) })
  try { Invoke-Expression $approval; "  ACCEPTED  $label" } catch { $m = "$($_.Exception.Message)"; "  REFUSED   $label   [" + $m.Substring(0, [Math]::Min(80, $m.Length)) + ']' }
}
'--- (2) approval checks, Build step of R3 (draws n07, n08, n09)'
Test-Approval 'id and text name Run R3, n07-n09 and the id' 'OWNER-20991231-N8-R3-01' 'I approve N8 Run R3 (draws n07, n08, n09) under OWNER-20991231-N8-R3-01.'
Test-Approval 'no approval given' '' ''
Test-Approval 'id names R4' 'OWNER-20991231-N8-R4-01' 'I approve N8 Run R3 (draws n07, n08, n09) under OWNER-20991231-N8-R4-01.'
Test-Approval 'id date is not a date' 'OWNER-20991341-N8-R3-01' 'I approve N8 Run R3 (draws n07, n08, n09) under OWNER-20991341-N8-R3-01.'
Test-Approval 'text names a second run' 'OWNER-20991231-N8-R3-01' 'I approve N8 Run R3 and R4 (draws n07, n08, n09) under OWNER-20991231-N8-R3-01.'
Test-Approval 'text names a wrong draw' 'OWNER-20991231-N8-R3-01' 'I approve N8 Run R3 (draws n07, n08, n10) under OWNER-20991231-N8-R3-01.'
Test-Approval 'text lacks a draw' 'OWNER-20991231-N8-R3-01' 'I approve N8 Run R3 (draws n07, n08) under OWNER-20991231-N8-R3-01.'
Test-Approval 'text lacks the id' 'OWNER-20991231-N8-R3-01' 'I approve N8 Run R3 (draws n07, n08, n09).'
Test-Approval 'text has a double quote' 'OWNER-20991231-N8-R3-01' 'I approve N8 Run R3 (draws n07, n08, n09) "now" under OWNER-20991231-N8-R3-01.'
Reset-Dummy
```

Output:

```
--- the extracted run-order lines (93-95), first 110 characters of each:
    if (-not (Test-Path -LiteralPath "$study\activations\n8-r$prev\OWNER_EXIT_RECEIPT.json" -PathType Leaf)) { thr
    $before = Get-Content -LiteralPath "$study\activations\n8-r$prev\OWNER_EXIT_RECEIPT.json" -Raw -Encoding UTF8 
    if ($before.status -ne 'COMPLETE' -and -not (Test-Path -LiteralPath "$study\activations\n8-x$prev\OWNER_EXIT_R
--- (1) run order, Build step of R3 (k = 3, the run before it is R2)
  STOPS     no exit receipt of R2   [Run R2 has not ended: activations\n8-r2 has no OWNER_EXIT_RECEIPT.json. Runs go in registry ord]
  STOPS     R2 FAILED, no exit receipt of X2   [Run R2 did not complete (status FAILED) and its retry run X2 has not ended: activations\n8-x2 h]
  STOPS     R2 FAILED, X2 built but never claimed (activation folder, no exit receipt)   [Run R2 did not complete (status FAILED) and its retry run X2 has not ended: activations\n8-x2 h]
  PROCEEDS  R2 FAILED, X2 ended COMPLETE
  PROCEEDS  R2 FAILED, X2 ended FAILED
  PROCEEDS  R2 COMPLETE, no X2
  STOPS     R2 STOPPED_AT_STARTUP, no X2   [Run R2 did not complete (status STOPPED_AT_STARTUP) and its retry run X2 has not ended: activat]
  STOPS     R2 EXIT_UNOBSERVED_NO_KILL, no X2   [Run R2 did not complete (status EXIT_UNOBSERVED_NO_KILL) and its retry run X2 has not ended: ac]
--- (2) approval checks, Build step of R3 (draws n07, n08, n09)
  ACCEPTED  id and text name Run R3, n07-n09 and the id
  REFUSED   no approval given   [The Build step needs -ApprovalId and -ApprovalText. Nothing was built]
  REFUSED   id names R4   [The approval id must name Run R3: OWNER-<yyyymmdd>-N8-R3-<nn>. Nothing was built]
  REFUSED   id date is not a date   [The approval id's date is not a date: 20991341. Nothing was built]
  REFUSED   text names a second run   [The approval text must name Run R3, its draws n07, n08, n09 and the approval id,]
  REFUSED   text names a wrong draw   [The approval text must name Run R3, its draws n07, n08, n09 and the approval id,]
  REFUSED   text lacks a draw   [The approval text must name Run R3, its draws n07, n08, n09 and the approval id,]
  REFUSED   text lacks the id   [The approval text must name Run R3, its draws n07, n08, n09 and the approval id,]
  REFUSED   text has a double quote   [The approval text must not contain double quotes or backslashes (they do not rea]
```

##### 4.6 d06: the scratch copy of the check on a dummy R1 with one refused start (no new script)

Command:

```
"C:\Users\rafli\AppData\Local\Programs\Python\Python312\python.exe" -I -B check_run_copy.py R1 --study "C:\Users\rafli\AppData\Local\Temp\swa21\d\scratch\dummy-study-refused" --n-train 1024 > d06_check_R1_refused.out 2>&1; echo "exit $?"
grep -E "^FAIL|passed, .* failed|other failure|inventory failure" d06_check_R1_refused.out | cut -c1-330
```

Output:

```
exit 1
FAIL  the run folder holds only the expected entries; its gate records are PRESTART and one request and one check per draw; benchmark\ and cache\, if there, are empty  [10 entries; cache\ empty folders]
FAIL  the terminal's inventory (files only, text_worker.Output.inventory) equals the run folder less TERMINAL.json itself  [terminal 1,237,733 bytes in 49 files; now 1,235,378 in 48]
FAIL  OWNER_EXIT_RECEIPT: its gate files' hashes equal the activation's gpu-checks; its power log hash equals POWER_LOG.jsonl  [PRESTART-REFUSED-1.json, PRESTART.json, n01-RESPONSE.json, n02-RESPONSE.json, n03-RESPONSE.json]
52 passed, 3 failed
The inventory failure is the known operational gap (OPERATIONAL_NOTES.md): 1 file, 2,355 bytes; every stage receipt's ledger carries the same (1 file, 2,355 bytes; 1 file, 2,355 bytes; 1 file, 2,355 bytes); cache\ is empty and was last changed 1,000 ms after TERMINAL.json
2 other failure(s): report them
```


#### 5. Commands that matter, with their output

All run in the clone `C:\Users\rafli\AppData\Local\Temp\swa21\d\repo` (Git Bash), read-only.

**History and tags** (`git log --all --date=iso-strict --format='%h %p | A:%ad | C:%cd | %an / %cn | %G? | %s'`):

```
30548db c1a2380 | A:2026-11-23T12:09:20+07:00 | C:2026-11-23T12:09:20+07:00 | rafli-hl / rafli-hl | N | Version 2.1: N8 paused
c1a2380 88ac496 | A:2026-11-23T12:05:02+07:00 | C:2026-11-23T12:05:02+07:00 | rafli-hl / rafli-hl | N | N8 paused after 6 of 24 draws
88ac496 c6f98b2 | A:2026-11-15T01:44:07+07:00 | C:2026-11-15T01:44:07+07:00 | rafli-hl / rafli-hl | N | Version 2.0: N8 registration notes and recorded builder
c6f98b2 fee55ea aaafa2e | A:2026-11-15T01:19:19+07:00 | C:2026-11-15T01:19:19+07:00 | rafli-hl / GitHub | E | Merge pull request #1 from rafli-hl/n8-registration
aaafa2e fee55ea | A:2026-11-15T01:17:02+07:00 | C:2026-11-15T01:17:02+07:00 | rafli-hl / rafli-hl | N | Register N8: dense-readout replication of N7
fee55ea 320359b | A:2026-11-13T12:54:48+07:00 | C:2026-11-13T12:54:48+07:00 | rafli-hl / rafli-hl | N | Revise README and add METHODS.md (documentation only; no result changed
320359b c4ae0e1 | A:2026-11-13T01:32:39+07:00 | C:2026-11-13T01:32:39+07:00 | rafli-hl / GitHub | E | Add files via upload
c4ae0e1  | A:2026-11-12T17:13:56+07:00 | C:2026-11-12T17:13:56+07:00 | rafli-hl / rafli-hl | N | Research record, version 1.2
```

(`E` means the signature could not be checked locally for want of the key; the supervising session checks it through the API.) `git cat-file -t` of `refs/tags/n8-registration`, `v2.0`, `v2.1` and `v1.2` gives `commit` for each: all four tags are lightweight.

**GitHub, server-side times** (`gh api repos/rafli-hl/sequence-weighting/pulls/1 --jq '{…}'`):

```
{"base_ref":"main","changed_files":81,"closed_at":"2026-11-14T18:19:20Z","commits":1,"created_at":"2026-11-14T18:17:44Z","head_ref":"n8-registration","head_sha":"aaafa2ed180c3c5c4c136f16fc3e7ef9a9515126","merge_commit_sha":"c6f98b26669f5d29f30c576b6d800c1fc82c98eb","merged":true,"merged_at":"2026-11-14T18:19:20Z","merged_by":"rafli-hl","number":1,"state":"closed"}
```

`gh api 'repos/rafli-hl/sequence-weighting/activity?per_page=100' --jq '.[] | {ref, activity_type, timestamp, before: .before[0:7], after: .after[0:7], actor: .actor.login}'`:

```
{"activity_type":"push","actor":"rafli-hl","after":"30548db","before":"c1a2380","ref":"refs/heads/main","timestamp":"2026-11-23T05:09:33Z"}
{"activity_type":"push","actor":"rafli-hl","after":"c1a2380","before":"88ac496","ref":"refs/heads/main","timestamp":"2026-11-23T05:05:16Z"}
{"activity_type":"push","actor":"rafli-hl","after":"88ac496","before":"c6f98b2","ref":"refs/heads/main","timestamp":"2026-11-14T18:44:16Z"}
{"activity_type":"branch_deletion","actor":"rafli-hl","after":"0000000","before":"aaafa2e","ref":"refs/heads/n8-registration","timestamp":"2026-11-14T18:36:37Z"}
{"activity_type":"pr_merge","actor":"rafli-hl","after":"c6f98b2","before":"fee55ea","ref":"refs/heads/main","timestamp":"2026-11-14T18:19:20Z"}
{"activity_type":"branch_creation","actor":"rafli-hl","after":"aaafa2e","before":"0000000","ref":"refs/heads/n8-registration","timestamp":"2026-11-14T18:17:18Z"}
{"activity_type":"push","actor":"rafli-hl","after":"fee55ea","before":"320359b","ref":"refs/heads/main","timestamp":"2026-11-13T05:56:18Z"}
{"activity_type":"push","actor":"rafli-hl","after":"320359b","before":"c4ae0e1","ref":"refs/heads/main","timestamp":"2026-11-12T18:32:41Z"}
{"activity_type":"force_push","actor":"rafli-hl","after":"c4ae0e1","before":"a5c4a00","ref":"refs/heads/main","timestamp":"2026-11-12T10:17:29Z"}
{"activity_type":"branch_creation","actor":"rafli-hl","after":"a5c4a00","before":"0000000","ref":"refs/heads/main","timestamp":"2026-11-09T09:26:06Z"}
```

Branches, releases, artifacts, tag (`gh api` GET):

```
== branches
{"name":"main","sha":"30548dbb789b2a117486fdf6f9ab9added680172"}
== releases
{"assets":[],"created_at":"2026-11-23T05:09:20Z","name":"v2.1","published_at":"2026-11-23T05:10:47Z","tag_name":"v2.1","target_commitish":"main"}
{"assets":[],"created_at":"2026-11-14T18:44:07Z","name":"v2.0","published_at":"2026-11-14T18:45:38Z","tag_name":"v2.0","target_commitish":"main"}
{"assets":[{"created_at":"2026-11-12T10:25:50Z","name":"n7-loss-arrays-v1.zip","size":14577377}],"created_at":"2026-11-12T10:13:56Z","name":"v1.2","published_at":"2026-11-12T10:25:53Z","tag_name":"v1.2","target_commitish":"main"}
== actions artifacts
{"names":[],"total_count":0}
== git/ref/tags/n8-registration
{"ref":"refs/tags/n8-registration","sha":"c6f98b26669f5d29f30c576b6d800c1fc82c98eb","type":"commit"}
== releases/tags/n8-registration
{"message":"Not Found", … "status":"404"}
== wiki: git ls-remote https://github.com/rafli-hl/sequence-weighting.wiki.git
remote: Repository not found.
```

**What changed in the N8 folder since registration** (`git diff --name-status c6f98b2 30548db -- preregistration/natural-text-dense-replication-20261114`):

```
A	preregistration/natural-text-dense-replication-20261114/OPERATIONAL_NOTES.md
M	preregistration/natural-text-dense-replication-20261114/README.md
A	preregistration/natural-text-dense-replication-20261114/RUN_COMMAND.ps1
A	preregistration/natural-text-dense-replication-20261114/X2_COMMAND.txt
A	preregistration/natural-text-dense-replication-20261114/check_run.py
M	preregistration/natural-text-dense-replication-20261114/tools/build_n8_activation.py
```

The builder at registration (`git diff c6f98b2 88ac496 -- …/tools/build_n8_activation.py`, the two changed lines, cut at 100 characters):

```
-EXPECTED_SUBJECT = None                                  # PENDING: the sealed subject, set when the source is se
-PUBLIC_REGISTRATION = None                               # PENDING: dict(url, merge_commit, tag, source_subject_s
+EXPECTED_SUBJECT = '9bdea3a9715b05393afe6713ddc696834dd344c3485c4e1a6ed0fa222f44bb6b'   # the sealed subject, re
+PUBLIC_REGISTRATION = {'url': 'https://github.com/rafli-hl/sequence-weighting/pull/1', 'merge_commit': 'c6f98b26
```

`git show c6f98b2:…/tools/build_n8_activation.py | sha256sum` → `30765693bd8bb4929ba060c193a610ecc987413d0c83b8035c6a9044228471d3`, the hash `HASHES.json` names.

**The same-day revision of the notes** (`git diff c1a2380 30548db -- …/OPERATIONAL_NOTES.md`, the changed lines):

```
-X2's row comes from file sizes, the terminal and the n06 receipt. `check_run.py X2`, which also reads every data file to hash it, had not been run by 23 November 2026.
+`check_run.py X2`, run on 23 November 2026, confirms X2's row (Events, 16 November).
+  - `check_run.py X2` (run on 23 November 2026): 31 passed, 1 failed, the failure being the known gap above.
+    - n06 passes every check of a complete draw, its arrays' hashes, layout and finiteness included.
+    - Against R2: X2's copy of R2's terminal is byte for byte the one R2 wrote, and n06 has the same seeds and saved orders as R2's n06 (orders `19c09770…`).
+    - The receipt's E0 comparison recomputes exactly from the arrays' SHA-256.
```

and of the README's table row (`git diff c1a2380 30548db -- …/README.md`):

```
-| [`OPERATIONAL_NOTES.md`](OPERATIONAL_NOTES.md) | Dated operational events of the runs (R1, R2, X2), known gaps and precautions, copied from the study folder. It names the owner's run commands and the completeness check, `check_run.py`, which are not published |
+| [`OPERATIONAL_NOTES.md`](OPERATIONAL_NOTES.md) | Dated operational events of the runs (R1, R2, X2), known gaps and precautions, copied from the study folder |
```

`git diff 88ac496 c1a2380 -- …/README.md` adds the line beginning `+- **15 November 2026, operational: two empty folders before R1.**`; it is not in the README at 88ac496 (v2.0). `grep -n "c1a2380" PUBLICATION_NOTES.md` prints nothing.

**No N8 run output in the tree** (`git ls-tree -r --name-only HEAD | grep -i -E "n8-[rx][0-9]|/n[0-9]{2}/|/n[0-9]{2}-RECEIPT|TERMINAL\.json|arrays\.f32|E0\.f32|record\.json|PRETRAINED|OWNER_EXIT|\.f32$|\.i64$|\.pt$|\.npy$|\.npz$" | grep -v -E "^work/|^outputs/|^reports/|preregistration/natural-text-(matched|peak)"`): no output. `grep -rIn -E "n8-r[0-9]|n8-x[0-9]|sequence-weighting-n8"` outside the N8 folder: no output.

**No reason for the pause on any living page** (`grep -n -i "pause\|resum" README.md CURRENT_CLAIMS.md METHODS.md NATURAL_TEXT_STUDIES.md DATA_AVAILABILITY.md PUBLICATION_NOTES.md CITATION.cff reports/README.md reports/natural-text-correction-20261123-01/CORRECTION.md`, cut at 110 characters):

```
README.md:8:N7: its protocol and sealed source were registered publicly before any of its runs. Its training was paused on
README.md:17:**N8, paused on 23 November 2026.**
README.md:20:- Resuming continues with R3 under the registered protocol. If fewer than 20 draws are ever completed, the regi
CURRENT_CLAIMS.md:223:That is not a restriction on anyone else. N8's training was paused on 23 November 2026 after 6 of its 2
CURRENT_CLAIMS.md:225:examined. Resuming continues with R3 under the registered protocol; if fewer than 20 draws are ever comp
NATURAL_TEXT_STUDIES.md:191:**N8, paused on 23 November 2026.**
NATURAL_TEXT_STUDIES.md:194:- Resuming continues with R3 under the registered protocol. If fewer than 20 draws are ever comple
PUBLICATION_NOTES.md:29:## 23 November 2026: version 2.1, N8 paused; corrections of 23 November
PUBLICATION_NOTES.md:44:    tokenizer result; N8's pause.
PUBLICATION_NOTES.md:47:  - `README.md`: N8's pause; a note under the sensitivity table; the familywise caveat; matched recency
PUBLICATION_NOTES.md:49:  - `NATURAL_TEXT_STUDIES.md`: the audit, the correction, matched recency windows and N8's pause. No livi
PUBLICATION_NOTES.md:52:- **N8 paused.** Training is paused on 23 November 2026 after 6 of 24 draws (n01–n06; n06 completed in
PUBLICATION_NOTES.md:56:  - Resuming continues with R3 under the registered protocol. If fewer than 20 draws are ever completed
PUBLICATION_NOTES.md:81:tagged `n8-registration`. It has no results yet; its runs and their pause are in the entry of 23 Novemb
```

**Pre-pin against sealed, line by line** (`diff` of `seal/pre-pin/<file>` and `source/<file>`): `matched_plan.py` differs in lines 32–36 only (four `None` pins and `PARTITION_SHA256 = None` become the drawn values); `MATCHED_OWNER_RUN.ps1` in lines 17 and 78 only (the hours text); `README.md` in lines 3 and 25 only (the two status lines).

**The clone is unchanged:** `git status --porcelain | wc -l` → `0`; `find . -name __pycache__ -not -path './.git/*' | wc -l` → `0`; `git rev-parse HEAD` → `30548dbb789b2a117486fdf6f9ab9added680172`.

---

# Appendix 2. Script sources (all post hoc)

Auditor D's scripts are printed in full in appendix 1D. The others follow, each with its SHA-256.

### `hashes_equivalent.py` (supervising session; SHA-256 `2e4d84fee64e03776c8ea2a59a66ec92e19e63af5d833212ebc791c61005eddb`)

~~~~python
"""Post hoc: every hash in N8's HASHES.json against the published file it names, where that file is published.
    python -I -B hashes_equivalent.py <N8 folder>"""
import hashlib, json, sys
from pathlib import Path
N = Path(sys.argv[1]); H = json.loads((N / 'HASHES.json').read_bytes())
sys.path.insert(0, str(N / 'tools')); sys.dont_write_bytecode = True
import write_hashes as wh
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
ok, differ, absent = [], [], []
for k, rel in wh.FILES.items():
    p = N / rel
    (absent if not p.is_file() else ok if sha(p) == H[f'{k}_sha256'] else differ).append((k, rel))
for g in wh.GROUPS:
    for rel, want in H[g].items():
        p = N / rel
        (absent if not p.is_file() else ok if sha(p) == want else differ).append((g, rel))
    extra = sorted(q.relative_to(N).as_posix() for q in (N / wh.GROUPS[g]).rglob('*') if q.is_file() and '__pycache__' not in q.parts and q.name != 'SOURCE_SUBJECT.json' and q.relative_to(N).as_posix() not in H[g]) if (N / wh.GROUPS[g]).is_dir() else []
    if extra: print('published but not in HASHES.json group', g, extra)
print(f'{len(ok)} named files match; {len(differ)} differ; {len(absent)} not published')
for k, rel in differ: print('  DIFFERS', k, rel, 'published', sha(N / rel)[:16], 'HASHES.json', (H.get(f'{k}_sha256') or H[k][rel])[:16])
for k, rel in absent: print('  NOT PUBLISHED', k, rel)
reg = json.loads((N / 'registry/n8-seed-registry/REGISTRY.json').read_bytes())
print('corpus_manifest, approval_id, n7_partition equal the registry:', all(H[k] == reg[k] for k in ('corpus_manifest_sha256', 'approval_id', 'n7_partition_sha256')))
s = json.loads((N / 'source/SOURCE_SUBJECT.json').read_bytes())
bad = [f['path'] for f in s['files'] if sha(N / 'source' / f['path']) != f['sha256'] or (N / 'source' / f['path']).stat().st_size != f['bytes']]
print(f"source subject {sha(N / 'source/SOURCE_SUBJECT.json')}; {len(s['files'])} sealed files, {len(bad)} differ from SOURCE_SUBJECT.json")
print('other keys in HASHES.json:', sorted(k for k in H if not k.endswith('_sha256') and k not in wh.GROUPS))
~~~~

### `a1_envelope.py` (auditor A; SHA-256 `8518d76a94d7155ff2687647c2363241e2cbeb147ce35d17ece31ecb28d43942`)

~~~~python
"""POST HOC, descriptive (auditor A). Recomputes the 23 November correction's F1 table from N7's published
POINTS.csv and MATCHED.csv only. Standard library. Usage: python a1_envelope.py <repo root>
"""
import csv, itertools, math, statistics as st, sys
from pathlib import Path

root = Path(sys.argv[1])
A = root / 'reports' / 'natural-text-matched-analysis-20261105-01'


def t_cdf_odd(t, nu):
    """Student t CDF for odd nu (closed form, Abramowitz & Stegun 26.7.3)."""
    th = math.atan(t / math.sqrt(nu))
    s, c = math.sin(th), math.cos(th)
    term, tot = c, c if nu > 1 else 0.0
    k = 1
    while 2 * k + 1 <= nu - 2:
        term *= (2 * k) / (2 * k + 1) * c * c
        tot += term
        k += 1
    a = 2 / math.pi * (th + s * tot) if nu > 1 else 2 / math.pi * th
    return 0.5 + a / 2


def t_q(p, nu):
    lo, hi = 0.0, 50.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if t_cdf_odd(mid, nu) < p: lo = mid
        else: hi = mid
    return (lo + hi) / 2


T5 = t_q(0.975, 5)
print(f't(0.975, df=5) = {T5:.13f}  (own bisection on the closed-form CDF)')

P = {}
for r in csv.DictReader(open(A / 'POINTS.csv', encoding='utf-8')):
    P[(r['draw'], float(r['epoch']), int(r['width']), r['tag'])] = r
M = [r for r in csv.DictReader(open(A / 'MATCHED.csv', encoding='utf-8'))]
RATE = {'P1': 'lr1e-04', 'S1': 'lr1e-04', 'S4': 'lr3e-04'}
KEY = {'P1': 'train', 'S1': 'gap', 'S4': 'train'}


def ci(v, t=T5):
    m, h = st.mean(v), t * st.stdev(v) / math.sqrt(len(v))
    return m, m - h, m + h


for stat in ('P1', 'S1', 'S4'):
    rows = [r for r in M if r['statistic'] == stat]
    assert len(rows) == 6 and all(r['status'] == 'READ' for r in rows)
    sealed, early, late, info = [], [], [], []
    for r in rows:
        d, lo, hi = r['draw'], float(r['between_low']), float(r['between_high'])
        p512 = float(P[(d, 3.0, 512, RATE[stat])]['p'])
        assert abs(p512 - float(r['p_first'])) < 1e-15
        plo, phi = (float(P[(d, e, 768, RATE[stat])]['p']) for e in (lo, hi))
        xlo, xhi = (float(P[(d, e, 768, RATE[stat])][KEY[stat]]) for e in (lo, hi))
        tgt = float(P[(d, 3.0, 512, RATE[stat])][KEY[stat]])
        assert abs(tgt - float(r['target'])) < 1e-12 and min(xlo, xhi) <= tgt <= max(xlo, xhi)
        w = (tgt - xlo) / (xhi - xlo)                   # my own interpolation weight, from the losses in POINTS.csv
        mine = p512 - (plo + w * (phi - plo))
        assert abs(mine - float(r['value'])) < 1e-12, (stat, d, mine, r['value'])
        sealed.append(float(r['value'])); early.append(p512 - plo); late.append(p512 - phi)
        info.append((d, lo, hi, plo, phi, w))
    print(f'\n== {stat} ({RATE[stat]}, matched on {KEY[stat]}) ==')
    for (d, lo, hi, plo, phi, w), s, e, l in zip(info, sealed, early, late):
        print(f'  {d}: bracket {lo:g}-{hi:g}, weight {w:.4f}; p768 {plo:.6f} -> {phi:.6f} ({"rises" if phi > plo else "FALLS"}); '
              f'contrast sealed {s:+.6f}, earlier end {e:+.6f}, later end {l:+.6f}')
    m, a, b = ci(sealed); print(f'  sealed (interpolated): {m:+.5f} [{a:+.5f}, {b:+.5f}], {sum(x > 0 for x in sealed)}/6 above 0')
    m, a, b = ci(late);   print(f'  all later ends       : {m:+.5f} [{a:+.5f}, {b:+.5f}], {sum(x > 0 for x in late)}/6 above 0')
    m, a, b = ci(early);  print(f'  all earlier ends     : {m:+.5f} [{a:+.5f}, {b:+.5f}], {sum(x > 0 for x in early)}/6 above 0')
    res = []
    for combo in itertools.product((0, 1), repeat=6):   # 0 = earlier end, 1 = later end
        v = [late[i] if c else early[i] for i, c in enumerate(combo)]
        m, a, b = ci(v)
        res.append((a, m, b, combo))
    res.sort()
    a, m, b, combo = res[0]
    print(f'  64 combinations: lowest lower limit {a:+.7f} (mean {m:+.5f}, upper {b:+.5f}) at '
          f'{"".join("L" if c else "E" for c in combo)} (draw order m01..m06; E earlier, L later)')
    a2 = ci([late[i] if c else early[i] for i, c in enumerate(combo)], t=2.5706)[1]
    print(f'    same combination with t = 2.5706: {a2:+.7f}')
    print(f'    second lowest: {res[1][0]:+.7f} at {"".join("L" if c else "E" for c in res[1][3])}; '
          f'combinations with lower limit <= 0: {sum(r[0] <= 0 for r in res)} of 64; '
          f'highest lower limit {res[-1][0]:+.7f}')
    means = sorted((r[1], r[3]) for r in res)
    print(f'    lowest mean over the 64: {means[0][0]:+.5f} at {"".join("L" if c else "E" for c in means[0][1])}')
    # random interior points of the box: is any lower limit below the vertex minimum? (concavity check, descriptive)
    import random
    rng = random.Random(20261123)
    worst = min(ci([early[i] + rng.random() * (late[i] - early[i]) for i in range(6)])[1] for _ in range(200000))
    print(f'    200,000 random interior readings: lowest lower limit {worst:+.7f} (vertex minimum {a:+.7f})')
~~~~

### `a2_gap.py` (auditor A; SHA-256 `a65026d31f590248791552b5588c38aaff7a50ff37154dbea9a1887775c0083d`)

~~~~python
"""POST HOC, descriptive (auditor A). Independent recomputation of the 23 November correction's F2 scale from N5's
published POINTS.csv. Standard library; own t quantile. Usage: python a2_gap.py <repo root>
"""
import csv, math, statistics as st, sys
from pathlib import Path

root = Path(sys.argv[1])
rows = list(csv.DictReader(open(root / 'reports/natural-text-fewepoch-analysis-20261103-01/POINTS.csv', encoding='utf-8')))
epochs = sorted({float(r['epoch']) for r in rows}); draws = sorted({r['draw'] for r in rows})
print('readouts in N5 POINTS.csv:', epochs, '| draws:', len(draws), draws[0], '..', draws[-1])
R = {(r['draw'], float(r['epoch'])): r for r in rows}
g = lambda d, e, w: float(R[(d, e)][f'gap_{w}']); p = lambda d, e, w: float(R[(d, e)][f'p_{w}'])


def t_cdf9(t):
    th = math.atan(t / 3.0); s, c = math.sin(th), math.cos(th)
    return 0.5 + (th + s * (c + 2 / 3 * c**3 + 8 / 15 * c**5 + 48 / 105 * c**7)) / math.pi


lo, hi = 0.0, 50.0
for _ in range(200):
    mid = (lo + hi) / 2
    lo, hi = (mid, hi) if t_cdf9(mid) < 0.975 else (lo, mid)
T9 = (lo + hi) / 2
print(f't(0.975, df=9) = {T9:.13f}')


def ci(v):
    m, h = st.mean(v), T9 * st.stdev(v) / math.sqrt(len(v)); return m, m - h, m + h


dg = [g(d, 2.0, 768) - g(d, 2.0, 512) for d in draws]
dp = [p(d, 2.0, 768) - p(d, 2.0, 512) for d in draws]
print('E2 gap 768-512:  %+.5f [%+.5f, %+.5f]; draws %+.5f to %+.5f; %d/10 above 0' % (*ci(dg), min(dg), max(dg), sum(x > 0 for x in dg)))
print('E2 p*  768-512:  %+.5f [%+.5f, %+.5f]; %d/10 above 0' % (*ci(dp), sum(x > 0 for x in dp)))
sl = {}
for w in (512, 768):
    for a, b in ((1.0, 2.0), (2.0, 3.0)):
        s = [(p(d, b, w) - p(d, a, w)) / (g(d, b, w) - g(d, a, w)) for d in draws]
        sl[(w, a, b)] = st.mean(s)
        dgap = [g(d, b, w) - g(d, a, w) for d in draws]
        print(f'width {w}, E{a:g}->E{b:g}: mean of per-draw slopes {st.mean(s):.3f} (draws {min(s):.3f} to {max(s):.3f}); '
              f'ratio of mean changes {st.mean([p(d, b, w) - p(d, a, w) for d in draws]) / st.mean(dgap):.3f}; gap change {min(dgap):+.3f} to {max(dgap):+.3f} nats')
smin, smax = min(sl.values()), max(sl.values())
m, a, b = ci(dg)
print(f'slopes {smin:.3f} to {smax:.3f}; upper limit {b:.5f} nats -> {b * smin:.5f} to {b * smax:.5f} of p*; share of |p* difference| {b * smin / abs(st.mean(dp)):.3f} to {b * smax / abs(st.mean(dp)):.3f}')
print(f'  lower limit {a:.5f} nats -> {a * smin:.5f} to {a * smax:.5f} of p* (the sign that would go with 768 having the lower p*)')
print(f'  largest single-draw gap difference {max(dg, key=abs):+.5f} nats -> {abs(max(dg, key=abs)) * smin:.5f} to {abs(max(dg, key=abs)) * smax:.5f} of p*')
# across draws at E2: does the 768-512 p* difference move with the gap difference? (descriptive)
mg, mp = st.mean(dg), st.mean(dp)
sxy = sum((x - mg) * (y - mp) for x, y in zip(dg, dp)); sxx = sum((x - mg) ** 2 for x in dg); syy = sum((y - mp) ** 2 for y in dp)
print(f'across the 10 draws at E2: slope of (p* difference) on (gap difference) {sxy / sxx:+.3f} per nat, r = {sxy / math.sqrt(sxx * syy):+.3f}; '
      f'p* difference at zero gap difference (intercept) {mp - sxy / sxx * mg:+.5f}')
print('per draw (gap difference, p* difference):', ', '.join(f'{d} {x:+.4f} {y:+.4f}' for d, x, y in zip(draws, dg, dp)))
~~~~

### `a3_recency.py` (auditor A; SHA-256 `1c8a15d867f8a9a64b2aaf2ffa94e9ac36aabd8d492b29de83b338b53fbd615b`)

~~~~python
"""POST HOC, descriptive (auditor A). F3 of the 23 November correction WITHOUT PyTorch.

The batch orders are not published; the record regenerates them with torch.randperm (text_engine.orders: epoch e's order
is torch.randperm(n, generator=torch.Generator().manual_seed(999 + adapt_order_seed + e))). This script EMULATES that call
with a pure-Python MT19937 (32-bit seed, init_genrand) and the swap loop I recall from PyTorch's CPU randperm
(for i in 0..n-2: z = next_u32 % (n - i); swap r[i], r[i + z]).  The emulation is my reconstruction, not PyTorch itself, so it
is validated three ways before use: (1) MT19937 test vectors and NumPy's legacy MT19937; (2) the 36 published set sizes in
reports/readme-revision-20261113-01/OUTPUT.txt and the 18 published per-draw loss differences in the 11 November RESULTS.json;
(3) the losses: sequences the order says were trained in a quarter lose more loss in it (and a seed shifted by 1 does not).
Usage: python a3_recency.py <repo root> <bundle dir>
"""
import itertools, json, re, sys
from pathlib import Path

import numpy as np

root, bundle = Path(sys.argv[1]), Path(sys.argv[2])
N, U, B = 16384, 1024, 16


class MT:
    def __init__(self, seed):
        s = [seed & 0xFFFFFFFF]
        for i in range(1, 624): s.append((1812433253 * (s[-1] ^ (s[-1] >> 30)) + i) & 0xFFFFFFFF)
        self.s, self.i = s, 624

    def twist(self):
        s = self.s
        for k in range(624):
            y = (s[k] & 0x80000000) | (s[(k + 1) % 624] & 0x7FFFFFFF)
            s[k] = s[(k + 397) % 624] ^ (y >> 1) ^ (0x9908B0DF if y & 1 else 0)
        self.i = 0

    def u32(self):
        if self.i >= 624: self.twist()
        y = self.s[self.i]; self.i += 1
        y ^= y >> 11; y ^= (y << 7) & 0x9D2C5680; y ^= (y << 15) & 0xEFC60000; y ^= y >> 18
        return y & 0xFFFFFFFF


def randperm(n, seed):
    g = MT(seed); r = list(range(n))
    for i in range(n - 1):
        z = g.u32() % (n - i)
        r[i], r[i + z] = r[i + z], r[i]
    return np.array(r, dtype=np.int64)


# (1) the generator itself
g = MT(5489); first = g.u32(); [g.u32() for _ in range(9998)]; tenk = g.u32()
print(f'MT19937 seed 5489: first output {first} (standard 3499211612), 10000th {tenk} (standard 4123659995)')
rs = np.random.RandomState(2419856979); g = MT(2419856979)
print('equals NumPy legacy MT19937 raw 32-bit stream for seed 2419856979 (2,000 outputs):',
      [g.u32() for _ in range(2000)] == [int(x) for x in rs.randint(0, 2**32, size=2000, dtype=np.uint64)])

man = json.loads((bundle / 'MANIFEST.json').read_bytes()); draws = sorted(man['draws'])
print('order seeds 999 + adapt_order_seed + e stay below 2^32:', all(man['draws'][d]['seeds']['adapt_order_seed'] + 999 + 4 < 2**32 for d in draws))


def arm(d, width, tag):
    a = man['draws'][d]['widths'][str(width)]; rec = json.loads((bundle / a['arms'][tag]['record']['path']).read_bytes())
    arr = np.frombuffer((bundle / a['arms'][tag]['arrays']['path']).read_bytes(), '<f4').reshape(-1, N + 512)
    e0 = np.frombuffer((bundle / a['E0']['path']).read_bytes(), '<f4')
    return [float(x) for x in rec['layout']['block_epochs']], arr, e0


def pos_of(orders):
    pos = np.empty_like(orders)
    for e in range(orders.shape[0]): pos[e, orders[e]] = np.arange(N)
    return pos


orders, ctrl = {}, {}
for d in draws:
    seed = man['draws'][d]['seeds']['adapt_order_seed']
    orders[d] = np.stack([randperm(N, 999 + seed + e) for e in (1, 2, 3, 4)])
    ctrl[d] = np.stack([randperm(N, 999 + seed + 1 + e) for e in (1, 2, 3, 4)])

# (3) the losses: trained-minus-untrained loss change per quarter window, emulated orders and the seed + 1 control
steps = [(0.0, 0.25, 1, 1), (0.25, 0.5, 1, 2), (2.0, 2.25, 3, 1), (2.25, 2.5, 3, 2), (2.5, 2.75, 3, 3), (2.75, 3.0, 3, 4), (3.0, 3.25, 4, 1), (3.25, 3.5, 4, 2)]
for name, O in (('emulated orders', orders), ('seed + 1 control', ctrl)):
    gaps = []
    for d in draws:
        q = pos_of(O[d]) // (N // 4) + 1
        for width in (512, 768):
            for tag in ('lr1e-04', 'lr3e-04'):
                ep, arr, e0 = arm(d, width, tag)
                for t0, t1, e, k in steps:
                    a0 = e0[:N] if t0 == 0.0 else arr[ep.index(t0), :N]
                    dl = arr[ep.index(t1), :N].astype(np.float64) - a0.astype(np.float64); tr = q[e - 1] == k
                    gaps.append(dl[tr].mean() - dl[~tr].mean())
    print(f'loss change, trained minus untrained in the quarter ({name}; {len(gaps)} arm-windows): mean {np.mean(gaps):+.4f}, range {min(gaps):+.4f} to {max(gaps):+.4f} nats')

# (2) published set sizes (13 November) and per-draw loss differences on the sets (11 November RESULTS.json)
pub = {}
for line in (root / 'reports/readme-revision-20261113-01/OUTPUT.txt').read_text(encoding='utf-8').splitlines():
    m = re.match(r'^(m0\d)\s+(\d)\s+\S+\s+(\d+),\s*\S+\s+(\d+),', line)
    if m: pub[(m.group(1), int(m.group(2)))] = (int(m.group(3)), int(m.group(4)))
res = json.loads((root / 'reports/natural-text-matched-assistant-posthoc-20261111-01/RESULTS.json').read_bytes())['values']
size_ok, worst_loss, out = 0, 0.0, {}
for k in (1, 2, 3):
    ages, tvs, sizes = [], [], []
    for di, d in enumerate(draws):
        pos = pos_of(orders[d])[:3]; quarter = pos // (N // 4) + 1; rank = pos // B + 1
        m5 = np.all(quarter >= 5 - k, axis=0); m7 = np.all(quarter <= k, axis=0)
        size_ok += (int(m5.sum()), int(m7.sum())) == pub[(d, k)]; sizes += [int(m5.sum()), int(m7.sum())]
        ep5, a5, _ = arm(d, 512, 'lr1e-04'); ep7, a7, _ = arm(d, 768, 'lr1e-04')
        mine = float(a5[ep5.index(3.0), :N][m5].astype(np.float64).mean() - a7[ep7.index(2 + k / 4), :N][m7].astype(np.float64).mean())
        worst_loss = max(worst_loss, abs(mine - res[f'matched|lr1e-04|k{k}|loss_every'][di]))
        for e in range(3):          # age of pass e in updates before the readout: 512 at update 3072, 768 at 2048 + 256 k
            ages.append(((3072 - (e * U + rank[e][m5])).mean() - (2048 + 256 * k - (e * U + rank[e][m7])).mean(), d, e + 1))
        cells = list(itertools.product(range(1, k + 1), repeat=3))
        q5, q7 = quarter[:, m5] - (4 - k), quarter[:, m7]
        h5 = np.array([np.all(q5 == np.array(c)[:, None], axis=0).mean() for c in cells]); h7 = np.array([np.all(q7 == np.array(c)[:, None], axis=0).mean() for c in cells])
        tvs.append((float(np.abs(h5 - h7).sum() / 2), d))
    worst = max(ages, key=lambda x: abs(x[0])); tv = max(tvs)
    print(f'k = {k}: set sizes {min(sizes)}-{max(sizes)}; largest |mean age difference| {abs(worst[0]):.5f} updates (draw {worst[1]}, pass {worst[2]}, signed {worst[0]:+.5f}); '
          f'largest joint quarter-cell TV {tv[0]:.5f} (draw {tv[1]}; {k ** 3} cell{"s" if k > 1 else ""}); mean |age difference| over 18 draw-passes {np.mean([abs(a[0]) for a in ages]):.3f}; '
          f'window width {256 * k} updates')
print(f'published set sizes reproduced: {size_ok} of 18 (draw, k) pairs; largest difference from the 18 published loss_every values: {worst_loss:.2e}')
~~~~

### `a3b_order_hashes.py` (auditor A; SHA-256 `30a96285e5397be2cecd7a7c134aceac600b46d046c5ca343dfb22cbda176a17`)

~~~~python
"""POST HOC (auditor A). Are the orders from my pure-Python emulation of torch.randperm byte-identical to the PyTorch-generated
orders that N8's registration pinned? Compares the SHA-256 of each emulated <draw>.i64 (four epoch rows, int64 little-endian, the
layout of analysis/regenerate_n7_orders.py) with the 12 hashes under inputs/n7-orders-v1/ in N8's HASHES.json.
Usage: python a3b_order_hashes.py <repo root> <bundle dir>"""
import hashlib, importlib.util, io, json, sys, contextlib
from pathlib import Path
import numpy as np

root, bundle = Path(sys.argv[1]), Path(sys.argv[2])
src = (Path(__file__).parent / 'a3_recency.py').read_text(encoding='utf-8')
ns = {}
exec(src.split('# (1) the generator itself')[0].replace('root, bundle = Path(sys.argv[1]), Path(sys.argv[2])', ''), ns)   # MT and randperm only
randperm = ns['randperm']
H = json.loads((root / 'preregistration/natural-text-dense-replication-20261114/HASHES.json').read_bytes())


def find(o, key):
    if isinstance(o, dict):
        if key in o: return o[key]
        for v in o.values():
            r = find(v, key)
            if r is not None: return r
    return None


man = json.loads((bundle / 'MANIFEST.json').read_bytes()); ok = 0
for d in sorted(man['draws']):
    seed = man['draws'][d]['seeds']['adapt_order_seed']
    for suffix, s in (('', seed), ('-seed-plus-1', seed + 1)):
        o = np.stack([randperm(16384, 999 + s + e) for e in (1, 2, 3, 4)]).astype('<i8')
        mine = hashlib.sha256(o.tobytes()).hexdigest(); pinned = find(H, f'inputs/n7-orders-v1/{d}{suffix}.i64')
        ok += mine == pinned; print(f'{d}{suffix}.i64: emulated {mine[:16]}..., pinned in HASHES.json {str(pinned)[:16]}...  {"MATCH" if mine == pinned else "DIFFERENT"}')
print(f'{ok} of 12 emulated order files are byte-identical to the pinned PyTorch-generated files')
~~~~

### `a3c_orders_json.py` (auditor A; SHA-256 `33476a78d2a2de64bfed98df02eb0f99e9ca8cd060bc2d1ced47af540599f96b`)

~~~~python
"""POST HOC (auditor A). Can ORDERS.json (the index regenerate_n7_orders.py writes, pinned in N8's HASHES.json and
test_on_n7.py as 8ba4a3c2...) be rebuilt byte for byte from the emulated orders? Its text includes the PyTorch and NumPy
version strings of the machine that wrote it, which are not published, so a few plausible strings are tried.
Usage: python a3c_orders_json.py <repo root> <bundle dir>"""
import hashlib, itertools, json, sys
from pathlib import Path
import numpy as np

root, bundle = Path(sys.argv[1]), Path(sys.argv[2])
ns = {}
exec((Path(__file__).parent / 'a3_recency.py').read_text(encoding='utf-8').split('# (1) the generator itself')[0]
     .replace('root, bundle = Path(sys.argv[1]), Path(sys.argv[2])', ''), ns)
randperm = ns['randperm']
PIN = '8ba4a3c2e7906f65c6335ece7a785bfb37fe1b2904684959d388f589f2287eb1'
N, EPOCHS = 16384, 4
man = json.loads((bundle / 'MANIFEST.json').read_bytes()); index = {}
for d in sorted(man['draws']):
    seed = man['draws'][d]['seeds']['adapt_order_seed']
    for suffix, s in (('', seed), ('-seed-plus-1', seed + 1)):
        o = np.stack([randperm(N, 999 + s + e) for e in range(1, EPOCHS + 1)]).astype('<i8'); b = o.tobytes()
        index[f'{d}{suffix}'] = dict(file=f'{d}{suffix}.i64', bytes=len(b), sha256=hashlib.sha256(b).hexdigest(), seed=s,
                                     epoch_order_sha256=[hashlib.sha256(row.tobytes()).hexdigest() for row in o])
hit = None
for t, n in itertools.product(('2.7.0+cu126', '2.7.0+cpu', '2.7.0'), ('2.5.3', '2.2.6', '2.3.5', '2.5.4')):
    meta = dict(torch=t, numpy=n, n=N, epochs=EPOCHS, layout='rows = epochs 1-4; int64 little-endian sequence indices in training order', orders=index)
    h = hashlib.sha256((json.dumps(meta, indent=1) + '\n').encode('utf-8')).hexdigest()
    if h == PIN: hit = (t, n)
print('ORDERS.json rebuilt byte for byte (SHA-256 equals the pin 8ba4a3c2...):', f'yes, with torch {hit[0]} and numpy {hit[1]}' if hit else 'no, for none of the 12 version-string pairs tried')
~~~~

### `a3d_ks.py` (auditor A; SHA-256 `db1f9a514a9e85364eed6ec96c6088a649529e47c442e3f16cbb77e3eb6f57ce`)

~~~~python
"""POST HOC (auditor A). The 13 November audit's other balance figure for F3: the largest two-sample Kolmogorov-Smirnov distance
between the two sets' ages of a pass (over draws and passes), from the emulated orders written by a6_make_orders.py.
Usage: python a3d_ks.py <orders dir>"""
import sys
from pathlib import Path
import numpy as np

d0 = Path(sys.argv[1]); N, U = 16384, 1024
for k in (1, 2, 3):
    worst = (0.0, None)
    for d in ('m01', 'm02', 'm03', 'm04', 'm05', 'm06'):
        o = np.frombuffer((d0 / f'{d}.i64').read_bytes(), '<i8').reshape(4, N)[:3]; pos = np.empty_like(o)
        for e in range(3): pos[e, o[e]] = np.arange(N)
        quarter, rank = pos // (N // 4) + 1, pos // 16 + 1
        m5, m7 = np.all(quarter >= 5 - k, axis=0), np.all(quarter <= k, axis=0)
        for e in range(3):
            a = np.sort(3072 - (e * U + rank[e][m5])); b = np.sort(2048 + 256 * k - (e * U + rank[e][m7])); grid = np.union1d(a, b)
            ks = float(np.abs(np.searchsorted(a, grid, side='right') / len(a) - np.searchsorted(b, grid, side='right') / len(b)).max())
            worst = max(worst, (ks, f'{d} pass {e + 1}'))
    print(f'k = {k}: largest marginal KS distance {worst[0]:.5f} ({worst[1]})')
~~~~

### `a4_numbers.py` (auditor A; SHA-256 `0bad7f3828a3370ef19f92ed1fc381c031eab80e345c37fe8f5c08ccb4424b35`)

~~~~python
"""POST HOC, descriptive (auditor A). Numbers quoted on the living pages, recomputed from published tables.
Standard library. Usage: python a4_numbers.py <repo root>
"""
import csv, json, math, statistics as st, sys
from pathlib import Path

root = Path(sys.argv[1]); T5 = 2.5705818356363
A = root / 'reports/natural-text-matched-analysis-20261105-01'
M = list(csv.DictReader(open(A / 'MATCHED.csv', encoding='utf-8')))


def ci(v, t=T5):
    m, h = st.mean(v), t * st.stdev(v) / math.sqrt(len(v)); return f'{m:+.5f} [{m - h:+.5f}, {m + h:+.5f}], {sum(x > 0 for x in v)}/{len(v)} above 0'


for s in ('P1', 'S1', 'S3', 'S4', 'S5', 'S2'):
    rows = [r for r in M if r['statistic'] == s]; v = [float(r['value']) for r in rows if r['status'] == 'READ']
    pos = [float(r['read_at_readout']) for r in rows if r['status'] == 'READ']
    print(f'{s}: {ci(v) if len(v) >= 5 else "only %d draws read" % len(v)}; read at {min(pos):.3f}-{max(pos):.3f}; values {", ".join("%+.5f" % x for x in v)}')
    if s in ('P1', 'S1', 'S4'): print('    brackets:', ', '.join(f"{r['draw']} {r['between_low']}-{r['between_high']}" for r in rows))
J = json.loads((A / 'ANALYSIS.json').read_bytes())
print('ANALYSIS.json top-level keys:', list(J)[:20])
p512 = [float(r['p_first']) for r in M if r['statistic'] == 'P1']; p768 = [float(r['p_read']) for r in M if r['statistic'] == 'P1']
print(f'mean p*(512, E3, 1e-4) {st.mean(p512):.4f}; 768 where read in P1: {min(p768):.4f}-{max(p768):.4f}')
loo = {}
for s in ('P1', 'S1', 'S3', 'S4', 'S5'):
    v = [float(r['value']) for r in M if r['statistic'] == s]; out = []
    T4 = 2.7764451051978            # t(0.975, df = 4)
    for i in range(6):
        w = v[:i] + v[i + 1:]; m, h = st.mean(w), T4 * st.stdev(w) / math.sqrt(5); out.append((m - h, m + h))
    loo[s] = out
    print(f'{s} leave-one-out intervals: ' + '; '.join(f'm0{i + 1} [{a:+.5f}, {b:+.5f}]{"*" if a <= 0 <= b else ""}' for i, (a, b) in enumerate(out)))
R = json.loads((root / 'reports/natural-text-matched-assistant-posthoc-20261111-01/RESULTS.json').read_bytes())['values']
for key in [f'matched|{tag}|k{k}|every' for tag in ('lr1e-04', 'lr3e-04') for k in (1, 2, 3)] + [k for k in R if k.startswith('better_rate')][:8]:
    v = R[key]
    if isinstance(v, list) and len(v) == 6 and all(isinstance(x, (int, float)) for x in v): print(f'{key}: {ci(v)}')
    else: print(f'{key}: {str(v)[:150]}')
~~~~

### `a5_links.py` (auditor A; SHA-256 `4bfd8f16ca234f62dd160b6f4a944d4f6a8bbca05782998d1e42b65f5d2a4982`)

~~~~python
"""POST HOC (auditor A). Local links and fragment anchors of the living pages. Standard library.
Usage: python a5_links.py <repo root>"""
import re, sys, urllib.parse
from pathlib import Path
root = Path(sys.argv[1])
pages = ['README.md', 'CURRENT_CLAIMS.md', 'METHODS.md', 'NATURAL_TEXT_STUDIES.md', 'DATA_AVAILABILITY.md', 'PUBLICATION_NOTES.md',
         'reports/README.md', 'outputs/README.md', 'preregistration/natural-text-dense-replication-20261114/README.md',
         'reports/natural-text-correction-20261123-01/CORRECTION.md', 'reports/external-audit-20261113-01/README.md']


def slug(h):   # GitHub's heading anchors: lower-case, drop punctuation except hyphen/underscore, spaces to hyphens
    h = re.sub(r'[`*]', '', h.strip()).lower()
    h = re.sub(r'[^\w\- ]', '', h, flags=re.UNICODE)
    return h.replace(' ', '-')


def anchors(p):
    out, seen = set(), {}
    for line in p.read_text(encoding='utf-8').splitlines():
        m = re.match(r'^(#{1,6})\s+(.*?)\s*$', line)
        if m:
            s = slug(m.group(2)); k = seen.get(s, 0); seen[s] = k + 1; out.add(s if k == 0 else f'{s}-{k}')
    return out


n = bad = ext = 0
for page in pages:
    p = root / page; text = p.read_text(encoding='utf-8')
    for m in re.finditer(r'\[[^\]]*\]\(([^)\s]+)\)|(?:src|srcset)="([^"]+)"', text):
        t = m.group(1) or m.group(2)
        if re.match(r'^[a-z]+://', t) or t.startswith('mailto:'): ext += 1; continue
        n += 1; path, _, frag = t.partition('#'); target = (p.parent / urllib.parse.unquote(path)).resolve() if path else p
        if not target.exists(): bad += 1; print(f'BROKEN {page}: {t}'); continue
        if frag and target.suffix == '.md' and frag not in anchors(target): bad += 1; print(f'BAD ANCHOR {page}: {t} (anchors: {sorted(anchors(target))[:40]})')
print(f'{n} local links and image sources checked on {len(pages)} pages; {bad} broken; {ext} external links not checked')
~~~~

### `a6_make_orders.py` (auditor A; SHA-256 `51686ae563735bacbef75a996c02725d92d7fab3d6ccac23dd7917b8c70e4d34`)

~~~~python
"""POST HOC (auditor A). Writes an ORDERS directory in the layout of N8's analysis/regenerate_n7_orders.py, from the pure-Python
emulation of torch.randperm in a3_recency.py (no PyTorch). The torch and numpy version strings that regenerate_n7_orders.py records in
ORDERS.json are given on the command line, because they are part of the bytes that test_on_n7.py pins.
Usage: python a6_make_orders.py <bundle dir> <new out dir> <torch version string> <numpy version string>"""
import hashlib, json, sys
from pathlib import Path
import numpy as np

bundle, out, tv, nv = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3], sys.argv[4]
ns = {}
exec((Path(__file__).parent / 'a3_recency.py').read_text(encoding='utf-8').split('# (1) the generator itself')[0]
     .replace('root, bundle = Path(sys.argv[1]), Path(sys.argv[2])', ''), ns)
randperm = ns['randperm']; N, EPOCHS = 16384, 4
man = json.loads((bundle / 'MANIFEST.json').read_bytes()); out.mkdir(parents=False, exist_ok=False); index = {}
for d in sorted(man['draws']):
    seed = man['draws'][d]['seeds']['adapt_order_seed']
    for suffix, s in (('', seed), ('-seed-plus-1', seed + 1)):
        o = np.stack([randperm(N, 999 + s + e) for e in range(1, EPOCHS + 1)]).astype('<i8'); b = o.tobytes(); (out / f'{d}{suffix}.i64').write_bytes(b)
        index[f'{d}{suffix}'] = dict(file=f'{d}{suffix}.i64', bytes=len(b), sha256=hashlib.sha256(b).hexdigest(), seed=s,
                                     epoch_order_sha256=[hashlib.sha256(row.tobytes()).hexdigest() for row in o])
meta = dict(torch=tv, numpy=nv, n=N, epochs=EPOCHS, layout='rows = epochs 1-4; int64 little-endian sequence indices in training order', orders=index)
raw = (json.dumps(meta, indent=1) + '\n').encode('utf-8'); (out / 'ORDERS.json').write_bytes(raw)
print(f'wrote {len(index)} order files to {out.name}; ORDERS.json records torch {tv}, numpy {nv}; ORDERS.json SHA-256 {hashlib.sha256(raw).hexdigest()}')
~~~~

### `readme_block.py` (auditor A; SHA-256 `4864632fb36a798ce2a8c2110cdeaf7d5da02885e0a1c97a5fa272463801da59`)

~~~~python
import csv, math, statistics as st

rows = csv.DictReader(open("reports/natural-text-matched-analysis-20261105-01/POINTS.csv"))
P = {(r["draw"], float(r["epoch"]), int(r["width"]), r["tag"]): r for r in rows}
draws, rate = sorted({k[0] for k in P}), "lr1e-04"
path = [e for e in sorted({k[1] for k in P}) if 2.0 <= e <= 3.5]

def read_768(target, d):  # 768's fitted p* where its training loss equals target
    pts = [(float(P[(d, e, 768, rate)]["train"]), float(P[(d, e, 768, rate)]["p"])) for e in path]
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        if min(x0, x1) <= target <= max(x0, x1):
            return y0 if x1 == x0 else y0 + (target - x0) / (x1 - x0) * (y1 - y0)
    return None  # target outside the path: the draw is unavailable

v = []
for d in draws:
    p768 = read_768(float(P[(d, 3.0, 512, rate)]["train"]), d)
    if p768 is not None:
        v.append(float(P[(d, 3.0, 512, rate)]["p"]) - p768)
assert len(v) >= 5, "fewer than five draws: P1 would be UNAVAILABLE"
half = 2.5706 * st.stdev(v) / math.sqrt(len(v))  # t(0.975, df = 5)
print(f"P1 = {st.mean(v):+.5f} [{st.mean(v) - half:+.5f}, {st.mean(v) + half:+.5f}], n = {len(v)}")
~~~~

### `b1_source_diff.py` (auditor B; SHA-256 `f378bf47d0a052b3004b514aee5adbe67df97c7b609dc6d476e3a31711b8c479`)

~~~~python
"""POST HOC audit script (auditor B). Reads only the clone at v2.1.
1. File-by-file comparison of N8 source/ against N7 sealed-source/ (SHA-256 over bytes).
2. SOURCE_SUBJECT.json against the files (bytes, sha256, coverage, lists).
3. CHANGES.md: 'Unchanged', 'Added', 'Dropped' lists against (1); every diff hunk in CHANGES.md applied as a patch to N7's file must
   reproduce N8's file byte for byte; and an independent difflib diff (n=1) must equal the hunks listed.
"""
import hashlib, json, re, sys, difflib
from pathlib import Path
REPO = Path(sys.argv[1])
N8 = REPO / 'preregistration/natural-text-dense-replication-20261114'
N7 = REPO / 'preregistration/natural-text-matched-confirmation-20261104/sealed-source'
sha = lambda b: hashlib.sha256(b).hexdigest()
def tree(root): return {p.relative_to(root).as_posix(): p.read_bytes() for p in sorted(root.rglob('*')) if p.is_file()}
a, b = tree(N7), tree(N8 / 'source')
same = sorted(k for k in a if k in b and a[k] == b[k]); changed = sorted(k for k in a if k in b and a[k] != b[k])
added = sorted(set(b) - set(a)); dropped = sorted(set(a) - set(b))
print('N7 sealed-source files:', len(a), '| N8 source files:', len(b))
print('identical:', len(same)); print('changed  :', changed); print('added    :', added); print('dropped  :', dropped)
for k in added:
    twins = [j for j in a if a[j] == b[k]]
    print(f'  added {k} sha {sha(b[k])[:16]} byte-equal to N7 file(s): {twins}')

# ---- 2. SOURCE_SUBJECT.json
raw = b['SOURCE_SUBJECT.json']; s = json.loads(raw)
print('\nSOURCE_SUBJECT.json sha256:', sha(raw))
listed = {f['path']: f for f in s['files']}
bad = [p for p, f in listed.items() if p not in b or len(b[p]) != f['bytes'] or sha(b[p]) != f['sha256']]
print('files listed:', len(listed), '| mismatching bytes/sha:', bad)
print('in source/ but not listed:', sorted(set(b) - set(listed)))
print('listed but not in source/:', sorted(set(listed) - set(b)))
print('changed_from_n7 (subject):', s['changed_from_n7'], '| equals my changed minus unlisted:', sorted(s['changed_from_n7']) == sorted(k for k in changed if k in listed))
print('dropped_from_n7 (subject):', s['dropped_from_n7'], '| equals mine:', sorted(s['dropped_from_n7']) == dropped)
print('new_files (subject):', s['new_files'], '| equals mine:', sorted(s['new_files']) == added)
print('byte_copies_of_n7_source keys equal my identical set (minus unlisted):', sorted(s['byte_copies_of_n7_source']) == sorted(k for k in same if k in listed), '| values:', set(s['byte_copies_of_n7_source'].values()))
print('N7 SOURCE_SUBJECT.json sha256:', sha(a['SOURCE_SUBJECT.json']))
print('disabled_authorization_sha256 matches source/AUTHORIZATION.json:', s['disabled_authorization_sha256'] == sha(b['AUTHORIZATION.json']), '| AUTHORIZATION.json:', json.loads(b['AUTHORIZATION.json']))
reg = N8 / 'registry/n8-seed-registry'
sr = s['seed_registry_and_partition']
for key, name in (('draw_sha256', 'DRAW.json'), ('exclusions_sha256', 'EXCLUSIONS.json'), ('partition_sha256', 'PARTITION.json'), ('policy_sha256', 'SEED_REGISTRY_POLICY.md'), ('registry_sha256', 'REGISTRY.json')):
    print(f'  subject {key} == sha256({name}):', sr[key] == sha((reg / name).read_bytes()))
for rel, h in s['bound_records'].items():
    p = REPO / rel
    print(f'  bound record {rel}:', 'MATCH' if p.is_file() and sha(p.read_bytes()) == h else ('ABSENT in clone' if not p.is_file() else 'DIFFERS'))
ns = json.loads(a['SOURCE_SUBJECT.json']); n7listed = {f['path']: f for f in ns['files']}
print('N7 subject lists', len(n7listed), 'files; N7 files mismatching their own subject:', [p for p, f in n7listed.items() if p not in a or sha(a[p]) != f['sha256']], '| N7 unlisted:', sorted(set(a) - set(n7listed)))

# ---- 3. CHANGES.md
ch = (N8 / 'CHANGES.md').read_bytes(); print('\nCHANGES.md sha256:', sha(ch), '| CR bytes in it:', ch.count(b'\r'))
text = ch.decode('utf-8'); lines = text.split('\n')
sections = {}; cur = None
for i, l in enumerate(lines):
    m = re.match(r'^## (.*)$', l)
    if m: cur = m.group(1); sections[cur] = []
    elif cur: sections[cur].append(l)
unch = dict(re.findall(r'^- `([^`]+)` `([0-9a-f]+)…`$', '\n'.join(sections['Unchanged']), flags=re.M))
print('CHANGES Unchanged lists', len(unch), 'files; my identical set has', len(same))
print('  listed as unchanged but not identical:', sorted(k for k in unch if k not in same))
print('  identical but not listed as unchanged:', sorted(k for k in same if k not in unch))
print('  hash prefixes wrong:', [k for k, h in unch.items() if k in b and not sha(b[k]).startswith(h)])
adr = '\n'.join(sections['Added, dropped and regenerated'])
print('CHANGES Added:', re.findall(r'\*\*Added\*\* `([^`]+)` `([0-9a-f]+)…`', adr), '| Dropped:', re.findall(r'\*\*Dropped\*\* `([^`]+)` `([0-9a-f]+)…`', adr), '| Regenerated:', re.findall(r'\*\*Regenerated\*\* `([^`]+)`', adr))
for k, h in re.findall(r'\*\*Added\*\* `([^`]+)` `([0-9a-f]+)…`', adr): print('  added hash prefix ok:', k, sha(b[k]).startswith(h))
for k, h in re.findall(r'\*\*Dropped\*\* `([^`]+)` `([0-9a-f]+)…`', adr): print('  dropped hash prefix ok (N7 file):', k, sha(a[k]).startswith(h))
filesecs = {k.strip('`'): v for k, v in sections.items() if k.startswith('`')}
print('CHANGES per-file sections:', list(filesecs)); print('  equals my changed set minus SOURCE_SUBJECT.json:', sorted(filesecs) == sorted(k for k in changed if k != 'SOURCE_SUBJECT.json'))
total_h = 0; notes = []
for name, body in filesecs.items():
    # parse the fenced diff blocks; each must be preceded by one numbered note
    hunks = []; i = 0
    while i < len(body):
        m = re.match(r'^\*\*(\d+)\.\*\* (.*)$', body[i])
        if m: notes.append((int(m.group(1)), name, m.group(2)))
        if body[i] == '```diff':
            j = i + 1; blk = []
            while body[j] != '```': blk.append(body[j]); j += 1
            hunks.append(blk); i = j
        i += 1
    old = a[name]; new = b[name]
    eol_old = (old.count(b'\r\n'), old.count(b'\n')); eol_new = (new.count(b'\r\n'), new.count(b'\n'))
    ol = old.decode('utf-8').split('\n'); nl = new.decode('utf-8').split('\n')
    # apply as a patch
    out = []; pos = 0; ok = True; nh = 0
    for blk in hunks:
        k = 0
        while k < len(blk):
            m = re.match(r'^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@', blk[k])
            if not m: ok = False; print('  unparsed line in block:', name, repr(blk[k][:80])); break
            nh += 1; o0 = int(m.group(1)); oc = int(m.group(2) or 1) if m.group(2) != '0' else 0; n0 = int(m.group(3)); nc = int(m.group(4) or 1) if m.group(4) != '0' else 0
            start = o0 - 1 if oc else o0
            if start < pos: ok = False; print('  hunk overlaps:', name, blk[k]); break
            out += ol[pos:start]; pos = start
            if len(out) != (n0 - 1 if nc else n0): ok = False; print('  new-side line number wrong:', name, blk[k], len(out) + 1)
            k += 1; seen_o = seen_n = 0
            while k < len(blk) and not blk[k].startswith('@@'):
                t, rest = blk[k][:1], blk[k][1:]
                if t == ' ':
                    if ol[pos] != rest: ok = False; print('  context mismatch', name, pos + 1)
                    out.append(rest); pos += 1; seen_o += 1; seen_n += 1
                elif t == '-':
                    if ol[pos] != rest: ok = False; print('  removed-line mismatch', name, pos + 1, repr(rest[:60]), repr(ol[pos][:60]))
                    pos += 1; seen_o += 1
                elif t == '+': out.append(rest); seen_n += 1
                elif blk[k].startswith('\\'): pass
                else: ok = False; print('  odd line', name, repr(blk[k][:60]))
                k += 1
            if (seen_o, seen_n) != (oc, nc): ok = False; print('  hunk counts wrong', name, (seen_o, seen_n), (oc, nc))
    out += ol[pos:]
    rebuilt = '\n'.join(out).encode('utf-8')
    total_h += nh
    # independent diff
    mine = [l.rstrip('\n') for l in difflib.unified_diff(old.decode('utf-8').splitlines(keepends=True), new.decode('utf-8').splitlines(keepends=True), n=1)][2:]
    theirs = [l for blk in hunks for l in blk]
    plus = sum(1 for l in theirs if l.startswith('+')); minus = sum(1 for l in theirs if l.startswith('-'))
    print(f'{name}: fenced blocks {len(hunks)}, hunks {nh}, +{plus}/-{minus} lines | patch(N7)==N8 bytes: {ok and rebuilt == new} | my difflib(n=1) hunks identical to listed: {mine == theirs} | (CRLF,LF) N7 {eol_old} N8 {eol_new}')
nums = [n for n, _, _ in notes]
print('numbered notes:', len(notes), '| consecutive 1..N:', nums == list(range(1, len(nums) + 1)), '| total hunks:', total_h)
cite = re.compile(r'§\s?\d+(?:\.\d+)?|brief|Gate 2 review|owner')
print('notes citing no protocol section, brief, gate review or owner decision:')
for n, name, t in notes:
    if not cite.search(t): print(f'  {n}. [{name}] {t}')
~~~~

### `b2_power.py` (auditor B; SHA-256 `937d1ae654360f88ddcccd14070a72d1ea5697799b9be984e7897c116b491124`)

~~~~python
"""POST HOC audit script (auditor B): checks the power argument of N8-protocol-draft.md section 7 numerically. NumPy only.
It reads only N7's PUBLISHED per-draw contrasts (reports/natural-text-matched-analysis-20261105-01/MATCHED.csv) to recompute the
planning effects and SDs. It uses no N8 data and estimates no N8 result: every number below is a design calculation.

Power of the registered rule: a hypothesis is CONFIRMED if the two-sided 95% t interval lies entirely on the predicted side of 0,
i.e. T = sqrt(n) * mean / sd > t_{0.975, n-1} with the sign oriented to the prediction. Under normal draws T is noncentral t with
df = n - 1 and noncentrality d * sqrt(n), d = effect / SD.
  P(T > c) = E_V[ Phi(delta - c * sqrt(V / df)) ],  V ~ chi-square(df)        (exact; evaluated by quadrature)
and, independently, by Monte Carlo simulation of normal samples.
"""
import csv, math, sys
import numpy as np
REPO = sys.argv[1]

def phi(x): return 0.5 * (1.0 + np.vectorize(math.erf)(np.asarray(x, dtype=float) / math.sqrt(2.0)))

def t_cdf(t, df, m=200001):
    # integral of the t density by Simpson's rule on a transformed grid (u = atan(x/sqrt(df)))
    a = math.atan(t / math.sqrt(df)); u = np.linspace(-math.pi / 2, a, m)
    # density of U: f_T(x) dx with x = sqrt(df) tan u, dx = sqrt(df) sec^2 u du  ->  C * cos(u)^(df-1)
    c = math.exp(math.lgamma((df + 1) / 2) - math.lgamma(df / 2)) / math.sqrt(math.pi)
    y = c * np.cos(u) ** (df - 1); h = (u[-1] - u[0]) / (m - 1)
    return float(h / 3 * (y[0] + y[-1] + 4 * y[1:-1:2].sum() + 2 * y[2:-1:2].sum()))

def t_quantile(p, df):
    lo, hi = 0.0, 50.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if t_cdf(mid, df) < p: lo = mid
        else: hi = mid
    return (lo + hi) / 2

def nct_upper(c, df, delta, m=400001):
    # P(T > c) for noncentral t: integrate over S = sqrt(V/df), V ~ chi2(df).  density of S: 2 df s * f_chi2(df s^2)
    s = np.linspace(1e-9, 6.0, m)
    logf = math.log(2) + math.log(df) + np.log(s) + ((df / 2 - 1) * np.log(df * s * s) - df * s * s / 2 - (df / 2) * math.log(2) - math.lgamma(df / 2))
    y = np.exp(logf) * phi(delta - c * s); h = s[1] - s[0]
    return float(h / 3 * (y[0] + y[-1] + 4 * y[1:-1:2].sum() + 2 * y[2:-1:2].sum()))

def power(n, d): return nct_upper(t_quantile(0.975, n - 1), n - 1, d * math.sqrt(n))

def mc(n, d, reps=400000, seed=20261123):
    rng = np.random.default_rng(seed); x = rng.standard_normal((reps, n)) + d
    t = x.mean(axis=1) / (x.std(axis=1, ddof=1) / math.sqrt(n)); return float((t > t_quantile(0.975, n - 1)).mean())

# ---- the planning inputs, recomputed from N7's published per-draw values
rows = list(csv.DictReader(open(REPO + '/reports/natural-text-matched-analysis-20261105-01/MATCHED.csv', encoding='utf-8')))
def stat(name):
    v = np.array([float(r['value']) for r in rows if r['statistic'] == name and r['status'] == 'READ']); n = len(v)
    m, sd = v.mean(), v.std(ddof=1); q = t_quantile(0.975, n - 1); return n, m, sd, m - q * sd / math.sqrt(n), m + q * sd / math.sqrt(n)
print('check of my t quantiles: t(.975,5) = %.6f (2.570582), t(.975,23) = %.6f (2.068658), t(.975,7) = %.6f (2.364624)' % (t_quantile(0.975, 5), t_quantile(0.975, 23), t_quantile(0.975, 7)))
for name in ('P1', 'S3'):
    n, m, sd, lo, hi = stat(name); print(f'N7 {name}: n={n} mean={m:+.6f} sd={sd:.6f} interval=[{lo:+.6f}, {hi:+.6f}]  half effect={m / 2:+.6f}  d(full)={abs(m) / sd:.4f}  d(half)={abs(m) / 2 / sd:.4f}')
_, m1, s1, _, _ = stat('P1'); _, m2, s2, _, _ = stat('S3')

# ---- the protocol's planning values
E1, SD1, E2, SD2 = 0.00454, 0.00485, 0.00227, 0.00324
d1, d2 = E1 / SD1, E2 / SD2
print(f"\nprotocol's planning values: H1 d = {d1:.4f}, H2 d = {d2:.4f}")
print('draws | H1 exact (MC) | H2 exact (MC) | Bonferroni lower bound | protocol table')
table = {12: (0.84, 0.60, 0.44), 16: (0.94, 0.74, 0.68), 20: (0.98, 0.84, 0.82), 24: (0.99, 0.91, 0.90)}
for n in (12, 16, 20, 21, 22, 23, 24):
    p1, p2 = power(n, d1), power(n, d2)
    print(f'{n:5d} | {p1:.4f} ({mc(n, d1):.4f}) | {p2:.4f} ({mc(n, d2):.4f}) | {p1 + p2 - 1:.4f} | {table.get(n, "")}')
u1, u2 = abs(m1) / 2 / s1, abs(m2) / 2 / s2
print(f"\nsame table with the unrounded N7 values (H1 d = {u1:.4f}, H2 d = {u2:.4f}):")
for n in (12, 16, 20, 24):
    p1, p2 = power(n, u1), power(n, u2); print(f'{n:5d} | {p1:.4f} | {p2:.4f} | {p1 + p2 - 1:.4f}')
p1, p2 = power(8, 2 * u1), power(8, 2 * u2); print(f'    8 draws, full unrounded effects: H1 {p1:.4f}  H2 {p2:.4f}  lower bound {p1 + p2 - 1:.4f}')
f_ = (2 / 3) * 2 / 1.5; p1, p2 = power(24, f_ * u1), power(24, f_ * u2); print(f'   24 draws, two-thirds effects, SDs x 1.5, unrounded: H1 {p1:.4f}  H2 {p2:.4f}  lower bound {p1 + p2 - 1:.4f}')
print('\nfull N7 effects (protocol: 8 draws give joint power of at least 0.92):')
for n in (6, 7, 8):
    p1, p2 = power(n, 2 * d1), power(n, 2 * d2); print(f'  n={n}: H1 {p1:.4f}  H2 {p2:.4f}  lower bound {p1 + p2 - 1:.4f}')
print('two-thirds of N7 effects, SDs x 1.5 (protocol: 24 draws give a lower bound of 0.81):')
f = (2 / 3) * 2 / 1.5
for n in (20, 24):
    p1, p2 = power(n, f * d1), power(n, f * d2); print(f'  n={n}: H1 {p1:.4f}  H2 {p2:.4f}  lower bound {p1 + p2 - 1:.4f}')
print('\nnot in the protocol, for context (same rule, 24 and 20 draws):')
for label, k in (('half effects, SDs x 1.5', 1 / 1.5), ('half effects, SDs x 2', 0.5), ('one-third effects, N7 SDs', 2 / 3)):
    for n in (24, 20):
        p1, p2 = power(n, k * d1), power(n, k * d2); print(f'  {label:28s} n={n}: H1 {p1:.3f}  H2 {p2:.3f}  lower bound {max(p1 + p2 - 1, 0):.3f}  product (if independent) {p1 * p2:.3f}')
# chi-square 95% interval for a SD estimated from 6 draws (df 5): how uncertain the planning SD is
def chi2_cdf(x, df, m=200001):
    v = np.linspace(1e-12, x, m); y = np.exp((df / 2 - 1) * np.log(v) - v / 2 - (df / 2) * math.log(2) - math.lgamma(df / 2)); h = v[1] - v[0]
    return float(h / 3 * (y[0] + y[-1] + 4 * y[1:-1:2].sum() + 2 * y[2:-1:2].sum()))
def chi2_q(p, df):
    lo, hi = 1e-9, 100.0
    for _ in range(100):
        mid = (lo + hi) / 2
        if chi2_cdf(mid, df) < p: lo = mid
        else: hi = mid
    return (lo + hi) / 2
a, b = chi2_q(0.025, 5), chi2_q(0.975, 5)
print(f'\n95% interval for a true SD given an SD s estimated from 6 draws (normal draws): [{math.sqrt(5 / b):.3f} s, {math.sqrt(5 / a):.3f} s]')

# ---- false-positive rate of the joint rule on the boundary of the null (H1 true effect 0, H2 effect large): at most 2.5%
rng = np.random.default_rng(1); n = 24; reps = 400000; q = t_quantile(0.975, n - 1)
x = rng.standard_normal((reps, n)); y = rng.standard_normal((reps, n)) - 5.0
t1 = x.mean(1) / (x.std(1, ddof=1) / math.sqrt(n)); t2 = y.mean(1) / (y.std(1, ddof=1) / math.sqrt(n))
print(f'simulated P(both CONFIRMED | H1 effect = 0, H2 effect = -5 SD), n = 24: {float(((t1 > q) & (t2 < -q)).mean()):.4f}  (bound 0.025)')

# ---- the envelope claim: the lower t limit is concave in the contrasts, so its minimum over a box is at a vertex
rng = np.random.default_rng(7); worst = -math.inf
for trial in range(200):
    n = int(rng.integers(3, 9)); a = rng.normal(0, 1, n); b = a + rng.normal(0, 1, n); q = t_quantile(0.975, n - 1)
    def lower(v): return v.mean(-1) - q * v.std(-1, ddof=1) / math.sqrt(n)
    idx = np.arange(1 << n); pick = ((idx[:, None] >> np.arange(n)) & 1).astype(bool); vmin = lower(np.where(pick, b, a)).min()
    u = rng.random((20000, n)); imin = lower(a + u * (b - a)).min(); worst = max(worst, vmin - imin)
print(f'envelope: over 200 random boxes (3-8 draws), largest (vertex minimum of the lower limit minus the lowest of 20,000 sampled interior points): {worst:.3e} (<= 0 means no interior point was lower than the best vertex)')
~~~~

### `b3_registry.py` (auditor B; SHA-256 `14e493eb98265da7e7fe0ba2fc76672811a8ab97ea7a2e09574673fd2c52f551`)

~~~~python
"""POST HOC audit script (auditor B). Reads only published files of the clone at v2.1; imports nothing from the repository.
Internal consistency of N8's HASHES.json, seed registry, partition, pilot log, seals and pins, re-derived with my own code.
"""
import hashlib, json, re, sys
from pathlib import Path
REPO = Path(sys.argv[1]); N8 = REPO / 'preregistration/natural-text-dense-replication-20261114'
N7 = REPO / 'preregistration/natural-text-matched-confirmation-20261104'; N6 = REPO / 'preregistration/natural-text-peak-confirmation-20261103'
REG = N8 / 'registry/n8-seed-registry'
sha = lambda b: hashlib.sha256(b).hexdigest()
J = lambda p: json.loads(Path(p).read_bytes())
ok_all = []
def check(name, ok, detail=''):
    ok_all.append(bool(ok)); print(('PASS  ' if ok else 'FAIL  ') + name + (f'  [{detail}]' if detail != '' else ''))

# ---------------------------------------------------------------- 1. HASHES.json against the files
h = J(N8 / 'HASHES.json')
single = dict(protocol_sha256='N8-protocol-draft.md', changes_sha256='CHANGES.md', sealed_source_subject_sha256='source/SOURCE_SUBJECT.json', pending_seal_before_the_draw_sha256='seal/pre-pin/SOURCE_SUBJECT.json',
              pilot_source_subject_sha256='seal/pilot/SOURCE_SUBJECT.json', seed_policy_sha256='registry/n8-seed-registry/SEED_REGISTRY_POLICY.md', seed_registry_sha256='registry/n8-seed-registry/REGISTRY.json',
              exclusions_sha256='registry/n8-seed-registry/EXCLUSIONS.json', draw_sha256='registry/n8-seed-registry/DRAW.json', draw_claim_sha256='registry/n8-seed-registry/DRAW_CLAIM.json',
              partition_sha256='registry/n8-seed-registry/PARTITION.json', registry_and_partition_check_sha256='registry/n8-seed-registry/REGISTRY_AND_PARTITION_CHECK.json',
              disclosure_figures_sha256='registry/n8-seed-registry/DISCLOSURE_FIGURES.md', seed_draw_receipt_sha256='registry/n8-seed-registry/SEED_DRAW_RECEIPT.json',
              fresh_pool_count_sha256='data-count/FRESH_POOL_COUNT.json', pilot_log_sha256='pilot/PILOT_LOG.json', pilot_command_sha256='PILOT_COMMAND.txt')
bad = [k for k, p in single.items() if sha((N8 / p).read_bytes()) != h[k]]
check('HASHES.json: 17 single-file hashes equal the published files', not bad, bad)
groups = ('pre_pin_copies', 'analysis', 'tools', 'source_tests', 'tools_tests', 'retired_tests')
diff, absent = [], []
for g in groups:
    for p, v in h[g].items():
        f = N8 / p
        if not f.is_file(): absent.append(p)
        elif sha(f.read_bytes()) != v: diff.append((p, sha(f.read_bytes())[:8]))
check('HASHES.json: grouped file hashes equal the published files, except those listed', diff == [('tools/build_n8_activation.py', 'c31fd4aa')] and absent == ['tests-retired/test_draw_command.py'], f'differ: {diff}; named but not published: {absent}')
unpub = [k for k in h if k.endswith('_sha256') and k not in single]
print('      HASHES.json keys ending _sha256 with no published file checked above:', unpub)
tracked = sorted(p.relative_to(N8).as_posix() for p in N8.rglob('*') if p.is_file())
named = set(single.values()) | {p for g in groups for p in h[g]}
subject_files = {'source/' + f['path'] for f in J(N8 / 'source/SOURCE_SUBJECT.json')['files']}
unbound = [p for p in tracked if p not in named and p not in subject_files]
print('      published files bound neither by HASHES.json nor by SOURCE_SUBJECT.json:', unbound)

# ---------------------------------------------------------------- 2. the seed draw, re-derived from the policy text
draw = J(REG / 'DRAW.json'); raw = bytes.fromhex(draw['entropy_hex']); ex = J(REG / 'EXCLUSIONS.json'); reg = J(REG / 'REGISTRY.json')
check('DRAW.json: 1,024 bytes of entropy', len(raw) == 1024 == draw['bytes'])
cands = [int.from_bytes(raw[4 * i:4 * i + 4], 'little') for i in range(256)]
excluded = sorted(set(ex['values'])); accepted = []
for c in cands:
    if len(accepted) == 98: break
    if all(abs(c - e) > 2048 for e in excluded) and all(abs(c - a) > 2048 for a in accepted): accepted.append(c)
roles = [('partition', 'partition_seed')] + [(f'n{i:02d}', r) for i in range(1, 25) for r in ('init_seed', 'weight_seed', 'pretrain_order_seed', 'adapt_order_seed')] + [('benchmark', 'benchmark_seed')]
mine = {}
for (slot, role), v in zip(roles, accepted): mine.setdefault(slot, {})[role] = v
theirs = {'partition': {'partition_seed': reg['partition_seed']}, 'benchmark': {'benchmark_seed': reg['benchmark']['benchmark_seed']}}
for row in reg['groups']: theirs[row['group']] = {k: v for k, v in row.items() if k != 'group'}
check('my re-derivation of the 98 role values from DRAW.json and EXCLUSIONS.json equals REGISTRY.json', len(accepted) == 98 and mine == theirs, f'candidates used up to index {cands.index(accepted[-1])}; rejected before that: {cands.index(accepted[-1]) + 1 - 98}')
vals = [v for s in theirs.values() for v in s.values()]
near_ex = min(min(abs(v - e) for e in excluded) for v in vals); near_other = min(abs(a - b) for i, a in enumerate(vals) for b in vals[i + 1:])
check('98 distinct values, each more than 2,048 from every exclusion and from each other', len(set(vals)) == 98 and near_ex > 2048 and near_other > 2048, f'nearest exclusion {near_ex}, nearest other role {near_other}; the check record says 37913 and 112876')
check('registry decisions list equals my accept/reject sequence', [d['value'] for d in reg['decisions'] if d['accepted']] == accepted and len(reg['decisions']) == 256)
check('registry binds its own draw, exclusions, policy and partition', (reg['draw_sha256'], reg['exclusions_sha256'], reg['policy_sha256'], reg['partition_sha256']) == (sha((REG / 'DRAW.json').read_bytes()), sha((REG / 'EXCLUSIONS.json').read_bytes()), sha((REG / 'SEED_REGISTRY_POLICY.md').read_bytes()), sha((REG / 'PARTITION.json').read_bytes())))
check('exclusions: 4,370 values, sorted, unique; provenance union_values agrees', len(ex['values']) == 4370 == ex['provenance']['union_values'] and ex['values'] == excluded)
pilot = J(N8 / 'pilot/PILOT_LOG.json')
check("the pilot's five seeds are all in EXCLUSIONS.json", all(v in set(excluded) for v in pilot['seeds'].values()) and len(pilot['seeds']) == 5, pilot['seeds'])
def text_values(r): return {r['partition_seed'], r['benchmark']['benchmark_seed']} | {v for row in r['groups'] for k, v in row.items() if k != 'group'}
def collect(value, under, out):
    # every integer 0..2^32-1 under a key whose name contains seed, stream, schedule or corpus (the policy's census rule)
    if isinstance(value, dict):
        for k, v in value.items(): collect(v, under or any(x in str(k).lower() for x in ('seed', 'stream', 'schedule', 'corpus')), out)
    elif isinstance(value, list):
        for v in value: collect(v, under, out)
    elif under and type(value) is int and 0 <= value < 2 ** 32: out.add(value)
exset = set(excluded)
for name, folder in (('N7', N7 / 'seed-registry'), ('N6', N6 / 'seed-registry')) + tuple((d.name, d) for d in sorted((REPO / 'reports').glob('*seed-registry*')) if (d / 'REGISTRY.json').is_file()):
    r = J(folder / 'REGISTRY.json'); tv = text_values(r) if 'groups' in r and 'partition_seed' in r else set(); cv = set(); collect(r, False, cv)
    e = set(J(folder / 'EXCLUSIONS.json')['values']) if (folder / 'EXCLUSIONS.json').is_file() else None
    check(f"{name}: every role value ({len(tv)}), every census-rule value of its REGISTRY.json ({len(cv)}) and its exclusion list ({'not published' if e is None else len(e)}) are in N8's exclusions",
          tv <= exset and cv <= exset and (e is None or e <= exset), 'registry sha ' + sha((folder / 'REGISTRY.json').read_bytes())[:8] + f'; nearest N8 role value to one of its values: {min(abs(a - b) for a in vals for b in (cv | tv))}')
check("N8's registry pins N7's registry and partition as published", reg['n7_registry_sha256'] == sha((N7 / 'seed-registry/REGISTRY.json').read_bytes()) and reg['n7_partition_sha256'] == sha((N7 / 'seed-registry/PARTITION.json').read_bytes()))
claim = J(REG / 'DRAW_CLAIM.json'); src = {f['path']: f['sha256'] for f in J(N8 / 'source/SOURCE_SUBJECT.json')['files']}
check('claim and registry: registry-source hashes equal the sealed source files (13 files)', claim['registry_source_sha256'] == reg['registry_source_sha256'] and all(src[k] == v for k, v in claim['registry_source_sha256'].items()) and len(claim['registry_source_sha256']) == 13)
rec = J(REG / 'SEED_DRAW_RECEIPT.json')
check('receipt: registry, partition, draw script and disclosure script hashes', (rec['registry_sha256'], rec['partition_sha256'], rec['draw_script_sha256'], rec['disclosure_script_sha256']) == (h['seed_registry_sha256'], h['partition_sha256'], h['tools']['tools/n8_seed_draw.py'], h['tools']['tools/n8_post_draw.py']))
check('receipt: the draw ran on the pending seal kept in seal/pre-pin', rec['source_subject_sha256'] == h['pending_seal_before_the_draw_sha256'] == sha((N8 / 'seal/pre-pin/SOURCE_SUBJECT.json').read_bytes()), rec['finished_local'])
chk = J(REG / 'REGISTRY_AND_PARTITION_CHECK.json')
check('post-draw check record: 16 checks, all ok', len(chk['checks']) == 16 and all(c['ok'] for c in chk['checks'].values()) and chk['all_pass'] is True)

# ---------------------------------------------------------------- 3. the partition
part = J(REG / 'PARTITION.json'); g = part['groups']
check('partition: 24 groups n01-n24 in order, n = 16,384', list(g) == [f'n{i:02d}' for i in range(1, 25)] and part['n'] == 16384)
check('each group: exactly 16,384 distinct sequences', all(len(v['sequences']) == 16384 == len(set(v['sequences'])) for v in g.values()))
allseq = [s for v in g.values() for s in v['sequences']]; allart = [a for v in g.values() for a in v['articles']]
check('groups are disjoint by sequence (393,216 distinct) and by article', len(set(allseq)) == 393216 == len(allseq) and len(set(allart)) == len(allart), f'{len(allart)} articles in all; left over {part["left_over_articles"]}; sum {len(allart) + part["left_over_articles"]}')
print('      partition pool record:', part['pool'])
check('articles used + left over = 14,039 fresh articles', len(allart) + part['left_over_articles'] == 14039 == reg['fresh_pool']['fresh_articles'] == part['pool'].get('fresh_articles', 14039))
for name, folder in (('N7', N7), ('N6', N6)):
    pf = folder / 'seed-registry/PARTITION.json'
    if not pf.is_file(): print(f'      {name}: no PARTITION.json published; not checked'); continue
    p7 = J(pf); a7 = {a for v in p7['groups'].values() for a in v['articles']}; s7 = {s for v in p7['groups'].values() for s in v['sequences']}
    check(f"no N8 article or sequence is in {name}'s published partition", not (set(allart) & a7) and not (set(allseq) & s7), f'{name}: {len(a7)} articles, {len(s7)} sequences, left over {p7.get("left_over_articles")}')
p7 = J(N7 / 'seed-registry/PARTITION.json')
check("N7's left-over articles (14,039) equal N8's fresh pool size", p7['left_over_articles'] == 14039)
fig = (REG / 'DISCLOSURE_FIGURES.md').read_text(encoding='utf-8'); rows = re.findall(r'^\| (n\d\d) \| (\d+) \| ([\d,]+) \|', fig, flags=re.M)
check('DISCLOSURE_FIGURES.md: articles and sequences per draw equal the partition', len(rows) == 24 and all(len(g[d]['articles']) == int(a) and len(g[d]['sequences']) == int(s.replace(',', '')) for d, a, s in rows))
det = chk['checks']['24 draws of exactly N sequences']['detail']
check('check record: articles and sequences per draw equal the partition', all(det[d] == dict(articles=len(g[d]['articles']), sequences=len(g[d]['sequences'])) for d in g))
# sequences are consecutive runs inside articles: the last article of a group may be cut
cut = {d: len(v['sequences']) for d, v in g.items()}
runs = {}
for d, v in g.items():
    s = v['sequences']; breaks = 1 + sum(1 for a, b in zip(s, s[1:]) if b != a + 1); runs[d] = breaks
check('each group\'s sequences form at most as many consecutive runs as it has articles', all(runs[d] <= len(g[d]['articles']) for d in g), f'runs {min(runs.values())}-{max(runs.values())}')

# ---------------------------------------------------------------- 4. the fresh-pool count and the protocol's numbers
fc = J(N8 / 'data-count/FRESH_POOL_COUNT.json')
check('fresh pool: count file = registry record = 14,039 articles and 582,603 sequences', fc['n8_fresh_pool'] == reg['fresh_pool'] and fc['n8_fresh_pool']['fresh_articles'] == 14039 and fc['n8_fresh_pool']['fresh_sequences'] == 582603)
check('24 x 16,384 = 393,216; + 24 x (328 - 1) = 401,064 <= 582,603', 24 * 16384 == 393216 == fc['sequences_needed'] and 393216 + 24 * (fc['largest_fresh_article_sequences'] - 1) == 401064 == fc['sequences_needed_whatever_the_shuffle'] and fc['largest_fresh_article_sequences'] == 328 and 401064 <= 582603)
check('count: assigned 13,511 = 11,099 (N5, N6) + 2,412 (N7); N7 pool 16,451 - 2,412 = 14,039', fc['assigned_articles'] == dict(all=13511, n5_and_n6=11099, n7=2412) and 11099 + 2412 == 13511 and fc['n7_pool_recount']['fresh_articles'] - 2412 == 14039)
a7 = {a for v in p7['groups'].values() for a in v['articles']}
check("N7's published partition holds 2,412 articles in m01-m06", len(a7) == 2412, len(a7))
check('count tool hash and source hashes agree with HASHES.json and the sealed source', fc['tool_sha256'] == h['tools']['tools/count_fresh_pool.py'] and all(src[k] == v for k, v in fc['source_sha256'].items()))

# ---------------------------------------------------------------- 5. pins in the sealed source, the builder and the prose
plan = (N8 / 'source/matched_plan.py').read_text(encoding='utf-8'); regpy = (N8 / 'source/matched_registry.py').read_text(encoding='utf-8'); datapy = (N8 / 'source/matched_data.py').read_text(encoding='utf-8')
pin = lambda text, key: re.search(key + r"\s*=\s*'([0-9a-f]{64})'", text).group(1)
check('matched_plan.py pins: policy, registry, exclusions, draw, partition', (pin(plan, 'policy_sha256'), pin(plan, 'registry_sha256'), pin(plan, 'exclusions_sha256'), pin(plan, 'draw_sha256'), pin(plan, 'PARTITION_SHA256')) == (h['seed_policy_sha256'], h['seed_registry_sha256'], h['exclusions_sha256'], h['draw_sha256'], h['partition_sha256']))
check('matched_registry.py POLICY_SHA256 and N7_REGISTRY_SHA256; matched_data.py N7_PARTITION_SHA256', pin(regpy, 'POLICY_SHA256') == h['seed_policy_sha256'] and pin(regpy, 'N7_REGISTRY_SHA256') == sha((N7 / 'seed-registry/REGISTRY.json').read_bytes()) and pin(datapy, 'N7_PARTITION_SHA256') == h['n7_partition_sha256'] == sha((N7 / 'seed-registry/PARTITION.json').read_bytes()))
b = (N8 / 'tools/build_n8_activation.py').read_text(encoding='utf-8')
check('builder (v2.1): EXPECTED_SUBJECT, and PUBLIC_REGISTRATION subject and pilot-log hash', "EXPECTED_SUBJECT = '" + h['sealed_source_subject_sha256'] in b and "'source_subject_sha256': '" + h['sealed_source_subject_sha256'] in b and "'pilot_log_sha256': '" + h['pilot_log_sha256'] in b)
prose = {'N8-protocol-draft.md': (N8 / 'N8-protocol-draft.md').read_text(encoding='utf-8'), 'README.md': (N8 / 'README.md').read_text(encoding='utf-8'), 'source/README.md': (N8 / 'source/README.md').read_text(encoding='utf-8'), 'CHANGES.md': (N8 / 'CHANGES.md').read_text(encoding='utf-8')}
known = {v for v in h.values() if isinstance(v, str) and re.fullmatch('[0-9a-f]{64}', v)} | {v for g_ in groups for v in h[g_].values()} | set(src.values()) | {sha((N8 / 'tools/build_n8_activation.py').read_bytes()), sha((N7 / 'sealed-source/SOURCE_SUBJECT.json').read_bytes()), 'c6f98b26669f5d29f30c576b6d800c1fc82c98eb'}
known |= {f['sha256'] for f in J(N7 / 'sealed-source/SOURCE_SUBJECT.json')['files']}
for name, text in prose.items():
    if name == 'CHANGES.md': text = '\n'.join(l for l in text.split('\n') if not l.startswith(('+', '-', ' ')))
    pref = set(re.findall(r'`([0-9a-f]{8,64})(?:…)?`', text))
    unmatched = sorted(p for p in pref if not any(k.startswith(p) for k in known))
    print(f'      {name}: {len(pref)} hash prefixes quoted; not matching any hash I can compute from published files: {unmatched}')

# ---------------------------------------------------------------- 6. the seals: pilot subject -> pending seal -> sealed subject
def files(p): return {f['path']: f['sha256'] for f in J(p)['files']}
s_pilot, s_pre, s_final = files(N8 / 'seal/pilot/SOURCE_SUBJECT.json'), files(N8 / 'seal/pre-pin/SOURCE_SUBJECT.json'), files(N8 / 'source/SOURCE_SUBJECT.json')
d1 = sorted(k for k in set(s_pilot) | set(s_pre) if s_pilot.get(k) != s_pre.get(k)); d2 = sorted(k for k in set(s_pre) | set(s_final) if s_pre.get(k) != s_final.get(k)); d3 = sorted(k for k in set(s_pilot) | set(s_final) if s_pilot.get(k) != s_final.get(k))
print('      files whose hash differs, pilot subject -> pending seal :', d1)
print('      files whose hash differs, pending seal -> sealed subject:', d2)
print('      files whose hash differs, pilot subject -> sealed subject:', d3)
check('pending seal -> sealed: exactly matched_plan.py, README.md and MATCHED_OWNER_RUN.ps1', d2 == ['MATCHED_OWNER_RUN.ps1', 'README.md', 'matched_plan.py'])
check('pilot subject -> sealed: exactly matched_plan.py, matched_registry.py, MATCHED_OWNER_RUN.ps1 and README.md (as the README says)', d3 == ['MATCHED_OWNER_RUN.ps1', 'README.md', 'matched_plan.py', 'matched_registry.py'])
check('the pre-pin copies are the files the pending seal lists', all(sha((N8 / 'seal/pre-pin' / k).read_bytes()) == s_pre[k] for k in ('MATCHED_OWNER_RUN.ps1', 'README.md', 'matched_plan.py')))
check("the pilot log names the pilot subject and the pilot tool", pilot['source_subject_sha256'] == h['pilot_source_subject_sha256'] and pilot['pilot_sha256'] == h['tools']['tools/n8_pilot.py'])
import difflib
for k in ('matched_plan.py', 'README.md', 'MATCHED_OWNER_RUN.ps1'):
    a = (N8 / 'seal/pre-pin' / k).read_text(encoding='utf-8').splitlines(); c = (N8 / 'source' / k).read_text(encoding='utf-8').splitlines()
    print(f'      --- pre-pin -> sealed: {k}')
    for l in difflib.unified_diff(a, c, n=0, lineterm=''):
        if l.startswith(('+', '-')) and not l.startswith(('+++', '---')): print('        ' + l[:230])
for key in ('pins_pending', 'status', 'has_run', 'runtime_authorized'):
    print(f'      SOURCE_SUBJECT {key}: pilot {J(N8 / "seal/pilot/SOURCE_SUBJECT.json").get(key)!r}, pre-pin {J(N8 / "seal/pre-pin/SOURCE_SUBJECT.json").get(key)!r}, sealed {J(N8 / "source/SOURCE_SUBJECT.json").get(key)!r}')
print('      seed_registry_and_partition: pilot', J(N8 / 'seal/pilot/SOURCE_SUBJECT.json').get('seed_registry_and_partition'), '| pre-pin', J(N8 / 'seal/pre-pin/SOURCE_SUBJECT.json').get('seed_registry_and_partition'))

# ---------------------------------------------------------------- 7. the pilot log against the protocol's section 7
t = pilot['stage']['timing']; r3 = pilot['run_of_three_draws']; bm = pilot['benchmark']['architectures']
w512 = t['w512/lr1e-04']['total_seconds'] + t['w512/pretraining and E0']['total_seconds']; w768 = t['w768/lr1e-04']['total_seconds'] + t['w768/pretraining and E0']['total_seconds']
ev = sum(x['evaluation_seconds'] for x in t.values())
facts = [('benchmark 43.6 s (22.0 + 21.6)', round(r3['benchmark_seconds'], 1) == 43.6 and round(bm['512']['seconds'], 1) == 22.0 and round(bm['768']['seconds'], 1) == 21.6),
         ('per draw 2,528 s = 42.1 min, cap 3,097 s', round(r3['measured_stage_seconds']) == 2528 and round(r3['measured_stage_seconds'] / 60, 1) == 42.1 and r3['stage_cap_seconds'] == 3097),
         ('width 512: 867 s; 55 / 242 / 570', (round(w512), round(t['w512/pretraining and E0']['total_seconds']), round(t['w512/lr1e-04']['training_seconds']), round(t['w512/lr1e-04']['evaluation_seconds'])) == (867, 55, 242, 570)),
         ('width 768: 1,660 s; 101 / 462 / 1,097', (round(w768), round(t['w768/pretraining and E0']['total_seconds']), round(t['w768/lr1e-04']['training_seconds']), round(t['w768/lr1e-04']['evaluation_seconds'])) == (1660, 101, 462, 1097)),
         ('evaluation about two thirds', 0.62 < ev / pilot['stage']['seconds'] < 0.72),
         ('run of three: 7,629 s measured, 7,186 s projected; both under 21,600 s', round(r3['measured_run_seconds']) == 7629 and round(r3['projected_run_seconds']) == 7186 and abs(r3['measured_run_seconds'] - (r3['benchmark_seconds'] + 3 * r3['measured_stage_seconds'])) < 1e-6),
         ('PyTorch reserved at most 1.42 GiB', round(pilot['stage']['guard_peaks']['cuda_reserved'] / 2 ** 30, 2) == 1.42),
         ('eight runs: about 17 h on the worker clock', round(8 * r3['measured_run_seconds'] / 3600) == 17),
         ('28 readouts per record; 12 files; orders 524,288 bytes = 4 epochs x 16,384 x 8', pilot['stage']['checks']['records_have_28_readouts'] == {'w512': True, 'w768': True} and pilot['stage']['checks']['files']['ORDERS.i64'] == 4 * 16384 * 8),
         ('status PASS, real, no loss read, no p* fitted, run folder deleted', pilot['status'] == 'PASS' and pilot['fixture'] is False and pilot['loss_read'] is False and pilot['p_star_fitted'] is False and pilot['run_folder_deleted'] is True),
         ("the pilot's draw is N7's m01, none of it in N8's fresh pool", pilot['data']['draw'] == "N7's m01" and pilot['data']['articles_in_n8_fresh_pool'] == 0 and pilot['data']['sequences_in_n8_fresh_pool'] == 0 and pilot['data']['articles'] == len(p7['groups']['m01']['articles']))]
for name, ok in facts: check('pilot log vs protocol section 7: ' + name, ok)
print(f'      evaluation share {ev / pilot["stage"]["seconds"]:.3f}; device-wide GPU memory sampled by the guard, peak {pilot["stage"]["guard_peaks"]["device_used_sampled"]:,} bytes = {pilot["stage"]["guard_peaks"]["device_used_sampled"] / 2 ** 30:.3f} GiB; guard limit 2.5 GiB = {int(2.5 * 2 ** 30):,}; headroom {(int(2.5 * 2 ** 30) - pilot["stage"]["guard_peaks"]["device_used_sampled"]) / 2 ** 20:.0f} MiB')
print(f'      kept E0 states: (67,497,092 + 138,986,628) x 24 = {(67497092 + 138986628) * 24:,} bytes = {(67497092 + 138986628) * 24 / 2 ** 30:.2f} GiB (protocol: about 4.6 GiB)')
print(f'\n{sum(ok_all)} of {len(ok_all)} checks passed')
~~~~

### `b4_n7_loo.py` (auditor B; SHA-256 `66edb5acbfdb5d6c139cf709a0b20f5fe9ed6377790b03f27775cc08c1fe1c04`)

~~~~python
"""POST HOC audit script (auditor B): descriptive check, on N7's PUBLISHED per-draw values (MATCHED.csv), of two statements in
N8-protocol-draft.md section 1: S3's leave-one-draw-out intervals, and the readouts at which N7's P1 read width 768."""
import csv, math, statistics, sys
T = {4: 2.7764451051977987, 5: 2.5705818366147395}
rows = list(csv.DictReader(open(sys.argv[1] + '/reports/natural-text-matched-analysis-20261105-01/MATCHED.csv', encoding='utf-8')))
for name in ('S3', 'P1'):
    v = {r['draw']: float(r['value']) for r in rows if r['statistic'] == name and r['status'] == 'READ'}
    m = statistics.fmean(v.values()); sd = statistics.stdev(v.values()); h = T[5] * sd / math.sqrt(6)
    print(f'{name}: all six: {m:+.6f} [{m - h:+.6f}, {m + h:+.6f}]')
    for d in v:
        w = [x for k, x in v.items() if k != d]; m = statistics.fmean(w); h = T[4] * statistics.stdev(w) / math.sqrt(5)
        print(f'   without {d}: {m:+.6f} [{m - h:+.6f}, {m + h:+.6f}]  includes 0: {m - h <= 0 <= m + h}')
print('P1 read_at_readout (epochs):', [round(float(r['read_at_readout']), 3) for r in rows if r['statistic'] == 'P1'], '-> N8 path covers epochs 2.0 to 3.5')
~~~~

### `c01_verbatim.py` (auditor C; SHA-256 `6a125f68b83cb9a9ef8a25937d1919c44bb3925686fabf71928d41deb52d0da8`)

~~~~python
"""POST HOC audit script (area C). Are the estimator pieces of n8_analysis.py verbatim copies of N7's sealed source?
Reads only the clone. Usage: python -I -B c01_verbatim.py <REPO>"""
import ast, hashlib, sys, difflib
from pathlib import Path
repo = Path(sys.argv[1])
N8 = repo / 'preregistration/natural-text-dense-replication-20261114'
N7 = repo / 'preregistration/natural-text-matched-confirmation-20261104/sealed-source'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
def seg(path, name):
    src = path.read_text(encoding='utf-8')
    for f in ast.walk(ast.parse(src)):
        if isinstance(f, ast.FunctionDef) and f.name == name: return ast.get_source_segment(src, f)
    raise KeyError(name)
def dump(path, name):
    src = path.read_text(encoding='utf-8')
    for f in ast.walk(ast.parse(src)):
        if isinstance(f, ast.FunctionDef) and f.name == name: return ast.dump(f)
mine = N8 / 'analysis/n8_analysis.py'
print('n8_analysis.py sha256', sha(mine))
for rel, name in (('vendor/core.py', 'exponent'), ('text_analysis.py', 'exponent_upper'), ('text_analysis.py', 'objective_at'),
                  ('matched_analysis.py', 'read_along'), ('fewepoch_analysis.py', '_betacf'), ('fewepoch_analysis.py', 'betai'),
                  ('fewepoch_analysis.py', 'p_two_sided'), ('matched_analysis.py', 'side'), ('matched_analysis.py', 'sign_test'),
                  ('matched_analysis.py', 'draw_row'), ('matched_analysis.py', 'leave_one_out'), ('matched_analysis.py', 'fits_used')):
    a, b = seg(N7 / rel, name), seg(mine, name)
    same_text = a == b; same_ast = dump(N7 / rel, name) == dump(mine, name)
    print(f'{name:16s} vs N7 {rel:22s} text identical: {same_text}; AST identical: {same_ast}')
    if not same_text:
        for line in difflib.unified_diff(a.splitlines(), b.splitlines(), 'N7', 'N8', lineterm='', n=0): print('      ' + line[:230])
for rel in ('vendor/core.py', 'text_analysis.py', 'fewepoch_analysis.py'):
    print(f'N8 source/{rel} byte-identical to N7 sealed-source/{rel}:', sha(N8 / 'source' / rel) == sha(N7 / rel), sha(N7 / rel)[:16])
~~~~

### `c02_n7_refit.py` (auditor C; SHA-256 `4aca7d22a58e7610be31784c325a8ac312d406be3941bb18ceecdc15c8064c0d`)

~~~~python
"""POST HOC audit script (area C). Refit N7's 240 p* from the public loss-array bundle with n8_analysis.points and cache them.
Reads only the clone and the bundle; writes c02_per.pkl in the scratch folder.
Usage: python -I -B c02_n7_refit.py <REPO> <BUNDLE> <SCRATCH>"""
import sys, json, pickle, time, hashlib
from pathlib import Path
sys.dont_write_bytecode = True
repo, bundle, scratch = (Path(x) for x in sys.argv[1:4])
sys.path.insert(0, str(repo / 'preregistration/natural-text-dense-replication-20261114/analysis'))
import numpy as np
import n8_analysis as na
man = json.loads((bundle / 'MANIFEST.json').read_bytes()); data = {}; bad = 0
for d, entry in man['draws'].items():
    wb = (bundle / entry['weights']['path']).read_bytes(); bad += hashlib.sha256(wb).hexdigest() != entry['weights']['sha256']
    arms = {}
    for wd, we in entry['widths'].items():
        e0 = (bundle / we['E0']['path']).read_bytes(); bad += hashlib.sha256(e0).hexdigest() != we['E0']['sha256']
        for tag, arm in we['arms'].items():
            arr = (bundle / arm['arrays']['path']).read_bytes(); bad += hashlib.sha256(arr).hexdigest() != arm['arrays']['sha256']
            arms[(int(wd), tag)] = dict(e0=e0, arrays=arr, record=json.loads((bundle / arm['record']['path']).read_bytes()))
    data[d] = dict(weights=np.frombuffer(wb, dtype='<f4').tolist(), arms=arms)
print('bundle files with a SHA-256 different from MANIFEST.json:', bad)
t0 = time.perf_counter()
per = na.points(data, sorted(data), progress=lambda d: print(f'fitted {d}, {time.perf_counter() - t0:.0f} s', flush=True))
pickle.dump(per, open(scratch / 'c02_per.pkl', 'wb'))
print('fits:', sum(len(pe) for pd in per.values() for pe in pd.values()), 'environment', na.environment())
~~~~

### `c03_constructed.py` (auditor C; SHA-256 `cee273cde864b6be39731f8e2ae1a416229d892f11a68ecb483fcf2bf98fa334`)

~~~~python
"""POST HOC audit script (area C). Constructed inputs for n8_analysis.py, rule by rule (protocol sections 5 and 6).
No N8 data is read: every value below comes from a fixed formula. Usage: python -I -B c03_constructed.py <REPO>"""
import sys, math, json, itertools, statistics
from pathlib import Path
sys.dont_write_bytecode = True
repo = Path(sys.argv[1])
sys.path.insert(0, str(repo / 'preregistration/natural-text-dense-replication-20261114/analysis'))
import numpy as np
import n8_analysis as na

FIRST, SECOND, FINAL = na.PLAN['first'], na.PLAN['second'], na.PLAN['final']
T23 = 2.0686576104190406          # t(0.975, 23); standard tables give 2.068658


def show(name, got, want=None):
    print(f'{name}: {got}' + ('' if want is None else f'   | protocol wording expects: {want}'))


def study(h1, h2, r=None):
    """24 draws on N8's grid. 768's training loss falls and its p* rises linearly along the path; 512's E3 target is met at readout r[k]."""
    per = {}
    for k, d in enumerate(na.DRAWS):
        rk = 2.3 + 0.01 * k if r is None else r[k]
        a768 = {e: dict(p=0.09 + 0.01 * (e - 2), train=4.4 - 0.25 * (e - 2), validation=4.7, gap=0.3, saturated=False) for e in na.READOUTS}
        p512 = 0.09 + 0.01 * (rk - 2) + h1[k]
        a768[FINAL]['p'] = p512 - h2[k]
        a512 = {e: dict(p=p512 if e == FINAL else 0.05, train=(4.4 - 0.25 * (rk - 2)) if e == FINAL else 5.0, validation=4.7, gap=0.3, saturated=False) for e in na.READOUTS}
        per[d] = {FIRST: a512, SECOND: a768}
    return per


print('=== 1. t quantile, df 19-23, against numerical integration of the t density (independent of the incomplete beta)')


def t_cdf_central(t, nu, steps=200000):
    c = math.exp(math.lgamma((nu + 1) / 2) - math.lgamma(nu / 2)) / math.sqrt(nu * math.pi); h = t / steps
    f = lambda x: c * (1 + x * x / nu) ** (-(nu + 1) / 2)
    s = f(0) + f(t) + 4 * sum(f((2 * i - 1) * h) for i in range(1, steps // 2 + 1)) + 2 * sum(f(2 * i * h) for i in range(1, steps // 2))
    return 2 * s * h / 3          # P(|T| <= t), Simpson


for df in range(19, 24):
    q = na.t_quantile(0.975, df); print(f'  df {df}: quantile {q:.12f}; P(|T| <= q) by Simpson = {t_cdf_central(q, df):.13f} (want 0.95)')

print('=== 2. "entirely" = beyond 0 by more than 1e-9 (H1 above, H2 below)')
a = 0.001; half = T23 * a / math.sqrt(23)          # alternating +-a: sd = a sqrt(24/23), half-width = t a / sqrt(23)
for margin in (5e-10, 2e-9):
    h1 = [half + margin + a * (-1) ** k for k in range(24)]; h2 = [-(half + margin) + a * (-1) ** k for k in range(24)]
    out = na.decide(study(h1, h2)); i1 = out['statistics']['H1']['interval']['interval']; i2 = out['statistics']['H2']['interval']['interval']
    print(f'  margin {margin:g}: H1 lower limit {i1[0]:.3e} -> {out["labels"]["H1"]}; H2 upper limit {i2[1]:.3e} -> {out["labels"]["H2"]}; joint {out["joint"]}')

print('=== 3. reading rule')
r = na.read_along([(2.0, 4.30, 0.10), (2.0625, 4.25, 0.11), (2.125, 4.25, None), (2.1875, 4.20, 0.13)], 4.25)
show('  target equal to a readout value, held first by a sloping interval', {k: r.get(k) for k in ('status', 'between', 'weight', 'p_read', 'intervals_holding_the_target')})
r = na.read_along([(2.0, 4.25, 0.10), (2.0625, 4.25, None), (2.125, 4.20, 0.12)], 4.25)
show('  flat first interval holding the target, its LATER fit undefined', {k: r.get(k) for k in ('status', 'between', 'weight', 'p_at_bracket')}, 'read at its earlier readout (p = 0.10)')
r = na.read_along([(2.0, 4.30, 0.10), (2.0625, 4.20, 0.11), (2.125, 4.28, 0.12), (2.1875, 4.10, 0.13)], 4.25)
show('  non-monotone path', {k: r.get(k) for k in ('status', 'between', 'weight', 'p_read', 'intervals_holding_the_target')})
print('  target above / below every readout:', [na.read_along([(2.0, 4.30, 0.10), (2.0625, 4.20, 0.11)], t)['status'] for t in (4.3000001, 4.1999999)])

print('=== 4. saturation on the matched contrast (H1) and on 512 at E3 (no registered test exercises these branches)')
h1 = [0.004 + 0.001 * math.sin(k) for k in range(24)]; h2 = [-0.004 + 0.001 * math.cos(k) for k in range(24)]
per = study(h1, h2); base = na.decide(per)
row = base['statistics']['H1']['rows']['n01']; lo, hi = row['between']; w = row['weight']
per['n01'][SECOND][lo] = dict(per['n01'][SECOND][lo], p=8.0, p32=9.5, saturated=False)              # resolved at bound 32
row2 = base['statistics']['H1']['rows']['n02']
per['n02'][SECOND][row2['between'][1]] = dict(per['n02'][SECOND][row2['between'][1]], p=8.0, p32=32.0, saturated=True)   # unresolved
per['n03'][FIRST][FINAL] = dict(per['n03'][FIRST][FINAL], p=8.0, p32=None, saturated=True)             # 512 at E3 unresolved
out = na.decide(per); s1, s2 = out['statistics']['H1'], out['statistics']['H2']
p512 = per['n01'][FIRST][FINAL]['p']; p_hi = per['n01'][SECOND][hi]['p']
print('  H1 unavailable:', s1['unavailable'], '| H2 unavailable:', s2['unavailable'])
print('  H1 n01 bound-8 value (label uses it):', s1['values']['n01'], '= p512 - (8 + w (p_hi - 8)) =', p512 - (8.0 + w * (p_hi - 8.0)))
print('  H1 n01 value at bound 32:', s1['saturation']['values_at_bound_32']['n01'], '= p512 - (9.5 + w (p_hi - 9.5)) =', p512 - (9.5 + w * (p_hi - 9.5)))
print('  H1 saturation flagged / saturated:', s1['saturation']['flagged'], s1['saturation']['saturated'], '| interval at bound 32 present:', 'interval_at_bound_32' in s1['saturation'])
print('  H2 saturation flagged / saturated:', s2['saturation']['flagged'], s2['saturation']['saturated'])
print('  labels:', out['labels'], out['joint'], '| available H1', len(s1['available']), 'H2', len(s2['available']))

print('=== 5. what an UNAVAILABLE hypothesis still emits (19 of 24 available)')
per = study(h1, h2)
for d in na.DRAWS[:5]: per[d][FIRST][FINAL]['train'] = 3.0          # target below the whole path
out = na.decide(per); s1 = out['statistics']['H1']
print('  label', out['labels']['H1'], '| joint', out['joint'], '| keys:', sorted(k for k in s1 if k != 'rows'))
print('  has interval:', 'interval' in s1, '| has envelope:', 'envelope' in s1, '| per-draw values:', len(s1['values']), '| sign test:', s1['sign_test'], '| leave-one-out intervals:', len(s1.get('leave_one_out', {})))
x = next(iter(s1['leave_one_out'].values())); print('  one leave-one-out entry:', {k: x[k] for k in ('mean', 'interval', 'df', 'side')})

print('=== 6. study status')
for missing in (0, 1, 4, 5):
    per = study(h1, h2)
    for d in na.DRAWS[:missing]: per[d] = None
    out = na.decide(per); print(f'  {24 - missing} completed: status {out["status"]}, labels {out["labels"]}, joint {out["joint"]}, statistics present: {"statistics" in out}')
per = study(h1, h2); del per['n24']; out = na.decide(per); print('  a draw absent from the mapping (not None): decide ->', out['status'], out['statistics']['H1']['unavailable'])
~~~~

### `c04_n7_check.py` (auditor C; SHA-256 `caa0d10ce872394d221e433da68484f83d123c5ec695e42b48e7626eb1cb5b31`)

~~~~python
"""POST HOC audit script (area C). n8_analysis.py on N7's published data, checked against N7's sealed outputs and against the
auditor's own arithmetic (hard-coded t quantile, itertools brute force, an independent reading rule). S-b needs batch orders
(PyTorch) and is not run here. Reads the clone, the bundle and c02_per.pkl (this auditor's cache of na.points on the bundle).
Usage: python -I -B c04_n7_check.py <REPO> <BUNDLE> <SCRATCH>"""
import sys, json, csv, math, pickle, itertools, statistics, hashlib
from pathlib import Path
sys.dont_write_bytecode = True
repo, bundle, scratch = (Path(x) for x in sys.argv[1:4])
sys.path.insert(0, str(repo / 'preregistration/natural-text-dense-replication-20261114/analysis'))
import numpy as np
import n8_analysis as na

A = repo / 'reports/natural-text-matched-analysis-20261105-01'
DRAWS = ('m01', 'm02', 'm03', 'm04', 'm05', 'm06'); LOW, HIGH = 'lr1e-04', 'lr3e-04'
PATH = (2.0, 2.25, 2.5, 2.75, 3.0, 3.25, 3.5); T5 = 2.570581836
sealed_json = json.loads((A / 'ANALYSIS.json').read_bytes()); sealed = sealed_json['statistics']
num = lambda s: None if s == '' else float(s)

# ---------------------------------------------------------------- inputs
csv_per = {d: {} for d in DRAWS}
for r in csv.DictReader((A / 'POINTS.csv').open(encoding='utf-8')):
    csv_per[r['draw']].setdefault((int(r['width']), r['tag']), {})[float(r['epoch'])] = dict(p=num(r['p']), train=float(r['train']), validation=float(r['validation']), gap=float(r['gap']), saturated=False)
per = pickle.load(open(scratch / 'c02_per.pkl', 'rb'))
worst = max(abs(per[d][a][e]['p'] - csv_per[d][a][e]['p']) for d in DRAWS for a in csv_per[d] for e in csv_per[d][a])
same = sum(per[d][a][e]['p'] == csv_per[d][a][e]['p'] for d in DRAWS for a in csv_per[d] for e in csv_per[d][a])
print(f'1. refits against POINTS.csv: 240 fits, largest |p* difference| {worst:.3g}; bit-identical in {same}/240')
fits = {(r['draw'], int(r['width']), r['tag'], float(r['epoch'])): r for r in csv.DictReader((A / 'FITS.csv').open(encoding='utf-8'))}
wo = max(max(abs(per[d][a][e]['objective'] - float(fits[(d, a[0], a[1], e)]['objective'])), abs(per[d][a][e]['J0'] - float(fits[(d, a[0], a[1], e)]['J0']))) for d in DRAWS for a in per[d] for e in per[d][a])
print(f'   objective and J0 against FITS.csv: largest difference {wo:.3g}; fits at or above 7.999: {sum(per[d][a][e]["p"] >= 7.999 for d in DRAWS for a in per[d] for e in per[d][a])}; largest p* {max(per[d][a][e]["p"] for d in DRAWS for a in per[d] for e in per[d][a]):.4f}')

# ---------------------------------------------------------------- the auditor's own reading rule and interval
def my_read(rows, target):
    count = sum(min(a[1], b[1]) <= target <= max(a[1], b[1]) for a, b in zip(rows, rows[1:]))
    for (e0, x0, p0), (e1, x1, p1) in zip(rows, rows[1:]):
        if min(x0, x1) <= target <= max(x0, x1):
            if x0 == x1: return p0, e0, e0, e1, count
            t = (target - x0) / (x1 - x0); return p0 + t * (p1 - p0), e0 + t * (e1 - e0), e0, e1, count
    return None, None, None, None, count


def my_ci(v, q=T5):
    m = sum(v) / len(v); sd = math.sqrt(sum((x - m) ** 2 for x in v) / (len(v) - 1)); h = q * sd / math.sqrt(len(v)); return m, m - h, m + h


SPECS = dict(P1=('matched', 'train', LOW), S1=('matched', 'gap', LOW), S3=('fixed', None, LOW), S4=('matched', 'train', HIGH), S5=('fixed', None, HIGH), S2=('matched', 'validation', LOW))
ENV = dict(P1=0.0000764, S1=-0.0000507, S4=-0.000268)
matched_rows = list(csv.DictReader((A / 'MATCHED.csv').open(encoding='utf-8')))
for source, pp in (('POINTS.csv', csv_per), ('refits', per)):
    print(f'2. statistics from {source}: n8_analysis.contrast | auditor | ANALYSIS.json')
    for name, (kind, key, tag) in SPECS.items():
        s = na.contrast(pp, DRAWS, (512, tag), (768, tag), kind, key, 3.0, PATH, 5, None, envelope=kind == 'matched')
        mine, ends = [], []
        for d in DRAWS:
            p1 = pp[d][(512, tag)][3.0]['p']
            if kind == 'fixed': mine.append(p1 - pp[d][(768, tag)][3.0]['p']); continue
            rows = [(e, pp[d][(768, tag)][e][key], pp[d][(768, tag)][e]['p']) for e in PATH]; pr, pos, e0, e1, cnt = my_read(rows, pp[d][(512, tag)][3.0][key])
            if pr is not None: mine.append(p1 - pr); ends.append((p1 - pp[d][(768, tag)][e0]['p'], p1 - pp[d][(768, tag)][e1]['p']))
        if s['status'] == 'UNAVAILABLE':
            print(f'   {name}: UNAVAILABLE, available {s["available"]} (auditor {len(mine)} readings; ANALYSIS.json {sealed[name]["status"]}, {sealed[name]["available"]}), reasons {s["unavailable"]}'); continue
        t = s['interval']; ref = sealed[name]['interval']; m = my_ci(mine)
        d_a = max(abs(x - y) for x, y in zip((t['mean'], *t['interval']), m)); d_s = max(abs(x - y) for x, y in zip((t['mean'], *t['interval']), (ref['mean'], *ref['interval'])))
        line = f'   {name}: {t["mean"]:+.7f} [{t["interval"][0]:+.7f}, {t["interval"][1]:+.7f}] {s["status"]}; vs auditor {d_a:.2g}; vs ANALYSIS.json {d_s:.2g}; sign {s["sign_test"]["positive"]}/{s["sign_test"]["negative"]} p {s["sign_test"]["p"]:.5f} (sealed {sealed[name]["sign_test"]["p"]:.5f})'
        loo = max(abs(x - y) for d in DRAWS for x, y in zip((s['leave_one_out'][d]['mean'], *s['leave_one_out'][d]['interval']), (sealed[name]['leave_one_out'][d]['mean'], *sealed[name]['leave_one_out'][d]['interval'])))
        line += f'; leave-one-out vs sealed {loo:.2g}'
        if kind == 'matched':
            lows = [my_ci(c)[1] for c in itertools.product(*ends)]; ups = [my_ci(c)[2] for c in itertools.product(*ends)]; env = s['envelope']
            line += f'\n       envelope over {env["combinations"]} combinations: min lower {env["min_lower"]:+.8f} (auditor brute force {min(lows):+.8f}; correction of 23 Nov {ENV[name]:+.7f}), max upper {env["max_upper"]:+.8f} (auditor {max(ups):+.8f}); ends at min lower {env["at_min_lower"]["ends"]}'
        print(line)
    bad = 0; worstm = 0.0
    for r in matched_rows:
        kind, key, tag = SPECS[r['statistic']]
        s = na.contrast(pp, DRAWS, (512, tag), (768, tag), kind, key, 3.0, PATH, 5, None)['rows'][r['draw']]
        bad += s['status'] != r['status']
        for f in ('target', 'weight', 'read_at_readout', 'p_first', 'p_read', 'value'):
            a, b = num(r[f]), s.get(f)
            if (a is None) != (b is None): bad += 1
            elif a is not None: worstm = max(worstm, abs(a - b))
        b = s.get('between') or [None, None]; bad += (num(r['between_low']), num(r['between_high'])) != (b[0], b[1])
        c = num(r['intervals_holding_the_target']); bad += (None if c is None else int(c)) != s.get('intervals_holding_the_target')
    print(f'   MATCHED.csv: {len(matched_rows)} rows, {bad} mismatches of status, bracket or count, largest value difference {worstm:.3g}')

# ---------------------------------------------------------------- analyse() on N7 at 1e-4, without orders
man = json.loads((bundle / 'MANIFEST.json').read_bytes()); data = {}
for d, entry in man['draws'].items():
    data[d] = dict(weights=np.frombuffer((bundle / entry['weights']['path']).read_bytes(), dtype='<f4').tolist(),
                   arms={(int(wd), tag): dict(e0=(bundle / we['E0']['path']).read_bytes(), arrays=(bundle / arm['arrays']['path']).read_bytes(), record=json.loads((bundle / arm['record']['path']).read_bytes()))
                         for wd, we in entry['widths'].items() for tag, arm in we['arms'].items()})
plan = dict(draws=DRAWS, first=(512, LOW), second=(768, LOW), final=3.0, previous=2.0, path=PATH, min_draws=5, min_completed=5, windows=4, updates_per_epoch=1024, batch=16)
res = na.analyse(per, data, plan, None); dec = res['decision']
print('3. analyse() on N7 at 1e-4 (H1 = P1, H2 = S3), no orders')
print('   decision', dec['status'], dec['labels'], dec['joint'], '| S_b:', res['secondary']['S_b'])
for h in ('H1', 'H2'):
    t = dec['statistics'][h]['interval']; print(f'   {h}: {t["mean"]:+.5f} [{t["interval"][0]:+.5f}, {t["interval"][1]:+.5f}] df {t["df"]} t {t["t_critical"]:.9f}')
so = res['sensitivity']['starting_offset']
for k in ('contrast', 'change_in_768', 'offset'):
    t = so[k]['interval']; print(f'   starting offset, {k}: {t["mean"]:+.5f} [{t["interval"][0]:+.5f}, {t["interval"][1]:+.5f}], positive {so[k]["sign_test"]["positive"]}/6')
# the auditor's own starting offset: float64 means, the sealed estimator on gains lowered by the offset
vals = []
for d in DRAWS:
    r = dec['statistics']['H1']['rows'][d]; n = 16384
    e05 = np.frombuffer(data[d]['arms'][(512, LOW)]['e0'], '<f4')[:n]; e07 = np.frombuffer(data[d]['arms'][(768, LOW)]['e0'], '<f4')[:n]
    arr7 = np.frombuffer(data[d]['arms'][(768, LOW)]['arrays'], '<f4').reshape(10, -1)[:, :n]; eps = [float(x) for x in data[d]['arms'][(768, LOW)]['record']['layout']['block_epochs']]
    off = float(e07.astype(np.float64).mean() - e05.astype(np.float64).mean())
    ps = [na.exponent(data[d]['weights'], ((e07 - arr7[eps.index(e)]).astype(np.float64) - off).tolist())['p'] for e in r['between']]
    vals.append(r['p_first'] - (ps[0] + r['weight'] * (ps[1] - ps[0])))
m = my_ci(vals); print(f'   auditor: contrast with the offset {m[0]:+.5f} [{m[1]:+.5f}, {m[2]:+.5f}]   (AA-3 printed +0.0062 [-0.0001, +0.0126], 5/6)')
sa = res['secondary']['S_a']; t = sa['interval']
print(f'   S-a: {t["mean"]:+.8f} [{t["interval"][0]:+.8f}, {t["interval"][1]:+.8f}]; positions ' + ' '.join(f'{sa["rows"][d]["read_at_readout"]:.8f}' for d in DRAWS) + '   (13 Nov audit: +0.01583581 +0.01040960 +0.02126202; 2.09092701 2.17570429 2.13578642 2.19158563 2.07568226 2.23352733)')
summ = res['secondary']['S_c']['summary']
for k, ref in (('cumulative_rms', (0.00476198, 0.01443651, 0.01914414)), ('cumulative_max_abs', (0.00847085, 0.02297270, 0.02961557)), ('bin_max_abs', (0.02492288, 0.26589176, 0.40357918)), ('bin_rms', (0.01448940, 0.12248159, 0.18862965))):
    print(f'   S-c {k}: min/median/max {summ[k]["min"]:.8f} {summ[k]["median"]:.8f} {summ[k]["max"]:.8f}; largest difference from the 13 Nov audit {max(abs(summ[k][x] - y) for x, y in zip(("min", "median", "max"), ref)):.2g}; rows {len(res["secondary"]["S_c"]["rows"])}')
wv = wi = 0.0
for e in PATH:
    key = f'E{int(e)}' if e == int(e) else f'E{e}'; ref = sealed_json['by_readout'][key]['contrasts']['D4']; mine = res['secondary']['S_d'][e]
    wv = max(wv, max(abs(mine['values'][x] - ref['values'][x]) for x in DRAWS)); wi = max(wi, max(abs(a - b) for a, b in zip((mine['interval']['mean'], *mine['interval']['interval']), (ref['interval']['mean'], *ref['interval']['interval']))))
print(f'   S-d against ANALYSIS.json by_readout D4: values {wv:.2g}, intervals {wi:.2g}')
no = res['carried_over']['not_overfit']
print('   NOT_OVERFIT:', {k: (v['label'], sealed_json['not_overfit']['arms'][k]['label'], max(abs(a - b) for a, b in zip(v['interval']['interval'], sealed_json['not_overfit']['arms'][k]['interval']['interval']))) for k, v in no.items()})
ra = res['carried_over']['records_against_arrays']; print('   records against arrays:', ra['max_absolute_difference'], 'flagged', len(ra['flagged']), '| ANALYSIS.json', sealed_json['records_against_arrays']['max_absolute_difference'])
json.dumps(res); print('   the result of analyse() serialises to JSON: yes')
~~~~

### `c05_end_to_end.py` (auditor C; SHA-256 `02910458f07bcf02b83f54fb49920e2cae4e2c72fb993a30129dc5f65abde20e`)

~~~~python
"""POST HOC audit script (area C). analyse() end to end on N8's own grid (24 draws, 28 readouts, a 25-readout path), on SYNTHETIC
loss arrays built from fixed formulas (256 training rows, 16 validation rows per draw; c_synth.py). No N8 data is read. The
registered tests never run analyse() on this grid: test_on_n7.py uses N7's 10 readouts and 6 draws, and test_synthetic.py calls
decide() on made-up fitted values. H1 and H2 are recomputed by the auditor with N7's sealed vendor/core.exponent, an own reading
rule and a hard-coded t quantile.
Usage: python -I -B c05_end_to_end.py <REPO>"""
import sys, math, json, copy, importlib.util
from pathlib import Path
sys.dont_write_bytecode = True
repo = Path(sys.argv[1])
sys.path.insert(0, str(repo / 'preregistration/natural-text-dense-replication-20261114/analysis'))
import numpy as np
import n8_analysis as na
sys.path.insert(0, str(Path(__file__).resolve().parent))
import c_synth
spec = importlib.util.spec_from_file_location('n7core', repo / 'preregistration/natural-text-matched-confirmation-20261104/sealed-source/vendor/core.py')
n7core = importlib.util.module_from_spec(spec); spec.loader.exec_module(n7core)

N, NV = 256, 16; EP = c_synth.EP; F, S = na.PLAN['first'], na.PLAN['second']; T23 = 2.0686576104190406
print('0. the plan against the sealed source plan, written out independently: readouts equal', list(na.READOUTS) == EP == [float(x) for x in (0.25, 0.5, 1) + tuple(2 + k / 16 for k in range(25))],
      '| path', len(na.PLAN['path']), 'readouts', na.PLAN['path'][0], '..', na.PLAN['path'][-1], '| rate tag', na.RATE_TAG == f'lr{1e-4:.0e}', '| minimum', na.PLAN['min_draws'], na.PLAN['min_completed'], '| draws', len(na.DRAWS))
PLAN = dict(na.PLAN, updates_per_epoch=N // 16)          # 16 updates per epoch at this toy size; everything else is the registered plan
data, orders = {}, {}
for k, d in enumerate(na.DRAWS): data[d], orders[d] = c_synth.make_draw(k, N, NV)
per = na.points(data)
res = na.analyse(per, data, PLAN, orders); dec = res['decision']
print('1. all 24 draws:', dec['status'], dec['labels'], dec['joint'])
print('   sections:', {k: sorted(v) for k, v in res.items() if k in ('sensitivity', 'secondary', 'carried_over')})

# the auditor's own H1 and H2
h1, h2 = [], []
for d in na.DRAWS:
    g = lambda width, e: (np.frombuffer(data[d]['arms'][(width, na.RATE_TAG)]['e0'], '<f4')[:N] - np.frombuffer(data[d]['arms'][(width, na.RATE_TAG)]['arrays'], '<f4').reshape(28, N + NV)[EP.index(e), :N]).tolist()
    rec = lambda width, e: next(x for x in data[d]['arms'][(width, na.RATE_TAG)]['record']['readouts'] if x['epoch'] == e)
    p512 = n7core.exponent(data[d]['weights'], g(512, 3.0))['p']; target = rec(512, 3.0)['train_loss']; path = [e for e in EP if e >= 2.0]
    for a, b in zip(path, path[1:]):
        x0, x1 = rec(768, a)['train_loss'], rec(768, b)['train_loss']
        if min(x0, x1) <= target <= max(x0, x1):
            p0, p1 = (n7core.exponent(data[d]['weights'], g(768, e))['p'] for e in (a, b)); t = 0.0 if x0 == x1 else (target - x0) / (x1 - x0); h1.append(p512 - (p0 + t * (p1 - p0))); break
    h2.append(p512 - n7core.exponent(data[d]['weights'], g(768, 3.0))['p'])
for name, mine in (('H1', h1), ('H2', h2)):
    m = sum(mine) / 24; sd = math.sqrt(sum((x - m) ** 2 for x in mine) / 23); half = T23 * sd / math.sqrt(24); t = dec['statistics'][name]['interval']
    print(f'   {name}: n8_analysis {t["mean"]:+.9f} [{t["interval"][0]:+.9f}, {t["interval"][1]:+.9f}] df {t["df"]}; auditor {m:+.9f} [{m - half:+.9f}, {m + half:+.9f}] from {len(mine)} draws; largest difference {max(abs(t["mean"] - m), abs(t["interval"][0] - m + half), abs(t["interval"][1] - m - half)):.2g}')
env = res['sensitivity']['envelope']; print(f'   envelope: {env["combinations"]:,} combinations, min lower {env["min_lower"]:+.7f}, max upper {env["max_upper"]:+.7f}; H1 brackets 64 updates apart: {all(abs(r["between"][1] - r["between"][0] - 0.0625) < 1e-12 for r in dec["statistics"]["H1"]["rows"].values())}')
sb = res['secondary']['S_b']; print('   S-b steps:', sorted(sb['steps']), '| S-d readouts:', len(res['secondary']['S_d']), '| S-c rows:', len(res['secondary']['S_c']['rows']), '| leave-one-out:', {h: len(v) for h, v in res['sensitivity']['leave_one_out'].items()})
json.dumps(res); print('   serialises to JSON: yes')

print('2. a failed draw given as None (n07):')
d2 = dict(data, n07=None); p2 = dict(per, n07=None); r2 = na.analyse(p2, d2, PLAN, orders)
print('  ', r2['decision']['status'], r2['decision']['labels'], r2['decision']['joint'], '| H1 unavailable', r2['decision']['statistics']['H1']['unavailable'], '| NOT_OVERFIT n', {k: v['interval']['n'] for k, v in r2['carried_over']['not_overfit'].items()})
print('3. the same draw absent from the mapping (not None):')
d3 = {k: v for k, v in data.items() if k != 'n07'}; p3 = {k: v for k, v in per.items() if k != 'n07'}
try:
    r3 = na.analyse(p3, d3, PLAN, orders); print('  ', r3['decision']['status'])
except Exception as e:
    print('   analyse() raises', type(e).__name__, e, '(decide() alone returns', na.decide(p3, PLAN)['status'] + ')')
print('4. three draws given as None although nothing says they failed (for example a run not yet made):')
p4 = dict(per, n22=None, n23=None, n24=None); r4 = na.decide(p4, PLAN); print('  ', r4['status'], r4['labels'], r4['joint'], '-> the function labels whatever it is given; what counts as failed is decided by its caller')
print('5. fewer than 20:')
p5 = dict(per, **{d: None for d in na.DRAWS[:5]}); r5 = na.analyse(p5, dict(data, **{d: None for d in na.DRAWS[:5]}), PLAN, orders); print('  ', sorted(r5), r5['decision']['status'], r5['decision']['labels'], r5['decision']['joint'])
print('6. records against arrays: the recorded training loss of 768 at the first readout of n01\'s H1 bracket moved by +0.002 (arrays unchanged):')
a = dec['statistics']['H1']['rows']['n01']; d6 = copy.deepcopy(data); k6 = EP.index(a['between'][0]); d6['n01']['arms'][S]['record']['readouts'][k6]['train_loss'] += 0.002
p6 = dict(per, n01={arm: na.arm_points(d6['n01']['weights'], x, diagnostics=False) for arm, x in d6['n01']['arms'].items()})
ra = na.records_against_arrays(p6); b = na.decide(p6, PLAN)['statistics']['H1']['rows']['n01']
print('   flagged:', ra['flagged']); print('   n01 is still', b['status'], '| weight', round(a['weight'], 6), '->', round(b['weight'], 6), '| value', a['value'], '->', b['value'], '(the reading uses the record; the flag does not gate, as the protocol says)')
print('7. NOT_OVERFIT labels:', {k: v['label'] for k, v in res['carried_over']['not_overfit'].items()}, '(validation falls from E2 to E3 by construction)')
~~~~

### `c06_mutants.py` (auditor C; SHA-256 `212e1161346d31ed985aa54cd2832b569c06f9727d0e07f086d273c80e0913b8`)

~~~~python
"""POST HOC audit script (area C). Which rules of n8_analysis.py does no registered test exercise?

Part A. One-line mutants of n8_analysis.py are written to the SCRATCH folder (the clone is not touched), each beside a byte copy of
the registered test_synthetic.py, and the test's own functions are called on the mutant: t_quantiles, reading_rule,
availability_and_decision, saturation, tests_and_intervals. Its sixth function, envelope(), is not called here, to avoid repeating
the 2^24 enumerations; no mutant below touches bracket_envelope or t_quantile. A mutant "survives" when all 30 checks still pass.
Three control mutants, which the tests should kill, show that the harness detects a broken rule.

Part B. For test_on_n7.py, which cannot run here (no PyTorch): the conditions under which the surviving mutants change anything
are evaluated on N7's published data with the UNMUTATED module. If none arises, test_on_n7.py cannot tell the mutant from the
original either, because the mutated branch is never entered on N7.

Usage: python -I -B c06_mutants.py <REPO> <BUNDLE> <SCRATCH>            (child mode: ... --child <mutant dir>)"""
import sys, json, pickle, shutil, subprocess, importlib.util
from pathlib import Path
sys.dont_write_bytecode = True

if '--child' in sys.argv:
    folder = Path(sys.argv[sys.argv.index('--child') + 1]); sys.path.insert(0, str(folder))
    spec = importlib.util.spec_from_file_location('ts', folder / 'test_synthetic.py'); ts = importlib.util.module_from_spec(spec)
    import io, contextlib
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            spec.loader.exec_module(ts)
            ts.t_quantiles(); ts.reading_rule(); ts.availability_and_decision(); ts.saturation(); ts.tests_and_intervals()
        failed = [line[6:90] for line in buf.getvalue().splitlines() if line.startswith('FAIL')]
        print(json.dumps(dict(passed=sum(ts.results), failed=len(ts.results) - sum(ts.results), names=failed)))
    except Exception as e:
        print(json.dumps(dict(error=f'{type(e).__name__}: {e}')))
    raise SystemExit(0)

repo, bundle, scratch = (Path(x) for x in sys.argv[1:4])
AN = repo / 'preregistration/natural-text-dense-replication-20261114/analysis'
src = (AN / 'n8_analysis.py').read_text(encoding='utf-8')
MUTANTS = [
    ('M0 unmutated copy', None, None),
    ('M1 the 1e-9 margin dropped from side()', "    if t['interval'][0] > EPS: return 'ABOVE'\n    if t['interval'][1] < -EPS: return 'BELOW'", "    if t['interval'][0] > 0.0: return 'ABOVE'\n    if t['interval'][1] < 0.0: return 'BELOW'"),
    ('M2 H1 value at bound 32 ignores the interpolation weight', "(r['weight'] if kind == 'matched' else 0.0)", "0.0"),
    ('M3 a saturated fit makes a draw unavailable for H2 only, not for H1', "for a, e in fits_used(r, first, second, kind, final)): r = dict(r, status='SATURATED')", "for a, e in fits_used(r, first, second, kind, final) if kind == 'fixed'): r = dict(r, status='SATURATED')"),
    ('M4 records flagged above 1e-2 instead of 1e-3', 'RECORD_LIMIT = 1e-3 ', 'RECORD_LIMIT = 1e-2 '),
    ('M5 NOT_OVERFIT: the labels OVERFIT and PLATEAU swapped', "'OVERFIT' if t['interval'][0] > EPS else 'PLATEAU'", "'PLATEAU' if t['interval'][0] > EPS else 'OVERFIT'"),
    ('M6 S-d keeps saturated fits', "per[d][a][e]['p'] is not None and not per[d][a][e].get('saturated', False) for a in", "per[d][a][e]['p'] is not None for a in"),
    ('M7 starting offset: an undefined refit is not set aside', 'if None in ps: rows[d]', 'if False: rows[d]'),
    ('M8 refit threshold 7.5 instead of 7.999', 'P_UPPER, S32_UPPER = 7.999, 32.0', 'P_UPPER, S32_UPPER = 7.5, 32.0'),
    ('K1 control: unavailable at exactly the minimum', "if len(available) < max(min_draws, 2): return dict(out, status='UNAVAILABLE')", "if len(available) <= max(min_draws, 2): return dict(out, status='UNAVAILABLE')"),
    ('K2 control: the last bracketing interval is read', '(e0, x0, p0), (e1, x1, p1) = hits[0]', '(e0, x0, p0), (e1, x1, p1) = hits[-1]'),
    ('K3 control: a flat interval is read at its later readout', 'w = 0.0 if x1 == x0 else', 'w = 1.0 if x1 == x0 else'),
]
print('PART A. test_synthetic.py (its first five functions, 30 checks) on mutants of n8_analysis.py')
root = scratch / 'mutants'
if root.exists(): shutil.rmtree(root)
for name, old, new in MUTANTS:
    folder = root / name.split()[0]; folder.mkdir(parents=True)
    if old is None: text = src
    else:
        if src.count(old) != 1: raise SystemExit(f'{name}: pattern found {src.count(old)} times')
        text = src.replace(old, new)
    (folder / 'n8_analysis.py').write_text(text, encoding='utf-8', newline='\n'); shutil.copyfile(AN / 'test_synthetic.py', folder / 'test_synthetic.py')
    out = subprocess.run([sys.executable, '-I', '-B', __file__, str(repo), str(bundle), str(scratch), '--child', str(folder)], capture_output=True, text=True)
    r = json.loads(out.stdout.strip().splitlines()[-1]) if out.stdout.strip() else dict(error=out.stderr[-300:])
    verdict = 'KILLED (the test aborts: ' + r['error'] + ')' if 'error' in r else ('SURVIVES' if r['failed'] == 0 else 'KILLED') + f" ({r['passed']} passed, {r['failed']} failed" + (': ' + '; '.join(r['names']) if r['failed'] else '') + ')'
    print(f'  {name}: {verdict}')

print('PART B. on N7 with the unmutated module: do the mutated branches ever arise? (test_on_n7.py reads only N7)')
sys.path.insert(0, str(AN))
import numpy as np
import n8_analysis as na
per = pickle.load(open(scratch / 'c02_per.pkl', 'rb')); DRAWS = tuple(sorted(per)); LOW, HIGH = 'lr1e-04', 'lr3e-04'; PATH = (2.0, 2.25, 2.5, 2.75, 3.0, 3.25, 3.5)
man = json.loads((bundle / 'MANIFEST.json').read_bytes()); data = {}
for d, entry in man['draws'].items():
    data[d] = dict(weights=np.frombuffer((bundle / entry['weights']['path']).read_bytes(), dtype='<f4').tolist(),
                   arms={(int(wd), tag): dict(e0=(bundle / we['E0']['path']).read_bytes(), arrays=(bundle / arm['arrays']['path']).read_bytes(), record=json.loads((bundle / arm['record']['path']).read_bytes()))
                         for wd, we in entry['widths'].items() for tag, arm in we['arms'].items()})
fits = [x for d in DRAWS for a in per[d] for x in per[d][a].values()]
print(f'  fits: {len(fits)}; undefined: {sum(x["p"] is None for x in fits)}; largest p*: {max(x["p"] for x in fits):.4f} (M2, M3, M6, M8 need a fit of at least 7.5); saturated: {sum(x["saturated"] for x in fits)}')
limits = []
for tag in (LOW, HIGH):
    plan = dict(draws=DRAWS, first=(512, tag), second=(768, tag), final=3.0, previous=2.0, path=PATH, min_draws=5, min_completed=5, windows=4, updates_per_epoch=1024, batch=16)
    res = na.analyse(per, data, plan, None)
    for s in list(res['decision']['statistics'].values()) + [res['secondary']['S_a']]:
        limits += s['interval']['interval'] + [x for v in s['leave_one_out'].values() for x in v['interval']]
    limits += [x for v in res['carried_over']['not_overfit'].values() for x in v['interval']['interval']]
    so = res['sensitivity']['starting_offset']
    print(f'  {tag}: NOT_OVERFIT labels {sorted(set(v["label"] for v in res["carried_over"]["not_overfit"].values()))} (M5 needs another label); records against arrays, largest difference {res["carried_over"]["records_against_arrays"]["max_absolute_difference"]:.3g} (M4 needs one between 1e-3 and 1e-2); '
          f'starting-offset rows {sorted(set(r["status"] for r in so["rows"].values()))} (M7 needs UNDEFINED_FIT); H2 has an envelope: {"envelope" in res["decision"]["statistics"]["H2"]} (test_on_n7.py never looks for one)')
for kind, key, tag in (('matched', 'gap', LOW), ('matched', 'validation', LOW)):
    s = na.contrast(per, DRAWS, (512, tag), (768, tag), kind, key, 3.0, PATH, 5, None, envelope=True)
    if 'interval' in s: limits += s['interval']['interval'] + [x for v in s['leave_one_out'].values() for x in v['interval']]
print(f'  interval limits examined: {len(limits)}; nearest to 0: {min(abs(x) for x in limits):.3g} (M1 needs one within 1e-9 of 0)')
~~~~

### `c07_exposure_windows.py` (auditor C; SHA-256 `7824c6c5422cee5563f962a6fb271bf82caa8121e51cfd5b3e20d61fb8e4b4f8`)

~~~~python
"""POST HOC audit script (area C). S-b (exposure_windows) on SYNTHETIC arrays and orders (6 draws, 1,024 training rows, 64 updates
per epoch; c_synth.py), against the auditor's own construction of the sets, written from the definitions in the post-hoc analysis of
11 November (posthoc_exposure.py, section 3) and the 13 November audit's recency code (ranks and quarters), with N7's sealed
vendor/core.exponent. The registered check of S-b is in test_on_n7.py and needs PyTorch, which this auditor does not have.
In the synthetic arrays the losses do not depend on the orders, so only the construction of the sets is checked here.
Usage: python -I -B c07_exposure_windows.py <REPO>"""
import sys, math, itertools, importlib.util
from pathlib import Path
sys.dont_write_bytecode = True
repo = Path(sys.argv[1])
sys.path.insert(0, str(repo / 'preregistration/natural-text-dense-replication-20261114/analysis')); sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
import n8_analysis as na
import c_synth
spec = importlib.util.spec_from_file_location('n7core', repo / 'preregistration/natural-text-matched-confirmation-20261104/sealed-source/vendor/core.py')
n7core = importlib.util.module_from_spec(spec); spec.loader.exec_module(n7core)

N, NV, U = 1024, 16, 64; DRAWS = na.DRAWS[:6]; EP = c_synth.EP
plan = dict(na.PLAN, draws=DRAWS, min_draws=5, min_completed=5, updates_per_epoch=U)
data, orders = {}, {}
for k, d in enumerate(DRAWS): data[d], orders[d] = c_synth.make_draw(k, N, NV)
per = na.points(data); sb = na.exposure_windows(per, data, orders, plan)


def arr(d, width): return np.frombuffer(data[d]['arms'][(width, c_synth.TAG)]['arrays'], '<f4').reshape(28, N + NV)[:, :N]
def e0(d, width): return np.frombuffer(data[d]['arms'][(width, c_synth.TAG)]['e0'], '<f4')[:N]
def fit(d, width, e, mask):
    w = np.asarray(data[d]['weights']); g = e0(d, width) - arr(d, width)[EP.index(e)]
    return n7core.exponent(w[mask].tolist(), g[mask].tolist())['p']


worst = dict(whole=0.0, last=0.0, every=0.0, loss_last=0.0, loss_every=0.0); bal = []
for k in (1, 2, 3):
    e7 = 2 + k / 4; step = sb['steps'][e7]; sizes, ages, tvs = [], [], []
    for d in DRAWS:
        ranks = np.empty((3, N), int)
        for e in range(3): ranks[e, orders[d][e]] = np.arange(N) // 16 + 1          # the update, within its epoch, at which a sequence is trained
        quarter = (ranks - 1) // (U // 4) + 1
        i5 = np.all(quarter >= 5 - k, axis=0); i7 = np.all(quarter <= k, axis=0); l5 = quarter[2] >= 5 - k; l7 = quarter[2] <= k
        mine = dict(whole=fit(d, 512, 3.0, np.ones(N, bool)) - fit(d, 768, e7, np.ones(N, bool)), last=fit(d, 512, 3.0, l5) - fit(d, 768, e7, l7), every=fit(d, 512, 3.0, i5) - fit(d, 768, e7, i7),
                    loss_last=arr(d, 512)[EP.index(3.0)][l5].astype(float).mean() - arr(d, 768)[EP.index(e7)][l7].astype(float).mean(),
                    loss_every=arr(d, 512)[EP.index(3.0)][i5].astype(float).mean() - arr(d, 768)[EP.index(e7)][i7].astype(float).mean())
        for key in worst: worst[key] = max(worst[key], abs(mine[key] - step['contrasts'][key]['values'][d]))
        sizes += [int(i5.sum()), int(i7.sum())]
        a5 = 3 * U - (ranks[:, i5] + np.arange(3)[:, None] * U); a7 = 2 * U + (U // 4) * k - (ranks[:, i7] + np.arange(3)[:, None] * U)
        ages += [abs(a5[e].mean() - a7[e].mean()) for e in range(3)]
        q5 = quarter[:, i5] - (4 - k); q7 = quarter[:, i7]; cells = list(itertools.product(range(1, k + 1), repeat=3))
        h5 = np.array([np.all(q5 == np.array(c)[:, None], axis=0).mean() for c in cells]); h7 = np.array([np.all(q7 == np.array(c)[:, None], axis=0).mean() for c in cells]); tvs.append(abs(h5 - h7).sum() / 2)
    b = step['balance']['every']
    bal.append((k, (b['size_min'], b['size_max']) == (min(sizes), max(sizes)), abs(b['max_abs_mean_age_difference'] - max(ages)), abs(b['max_joint_cell_distance'] - max(tvs)), min(sizes), max(sizes), max(ages), max(tvs)))
print('S-b on synthetic orders, 6 draws: largest difference between exposure_windows and the auditor, per-draw contrasts:', {k: f'{v:.2g}' for k, v in worst.items()})
for k, same, da, dt, s0, s1, ag, tv in bal:
    print(f'  768 at E{2 + k / 4}: every-pass set sizes {s0}-{s1} equal: {same}; max |mean age difference| {ag:.5f} updates, difference {da:.2g}; max joint quarter-cell distance {tv:.5f}, difference {dt:.2g}')
oc = sb['order_checks']; print('  order checks (synthetic losses do not depend on the orders, so about 0 is expected):', {d: round(v['mean'], 4) for d, v in oc.items()}, '| steps per draw', {v['steps'] for v in oc.values()})
~~~~

### `c08_untested_branches.py` (auditor C; SHA-256 `ed52d4e033c75705145028c1138ad292f35a013bf224af40bee86b743d96c051`)

~~~~python
"""POST HOC audit script (area C). Constructed inputs for four branches of n8_analysis.py that no registered test enters
(c06_mutants.py, M4-M8): the NOT_OVERFIT labels, S-d's exclusion of saturated fits, the starting offset's undefined refit, and the
7.999 refit threshold. Synthetic values from fixed formulas; no N8 data. decide() and analyse() are not called.
Usage: python -I -B c08_untested_branches.py <REPO>"""
import sys, math, copy
from pathlib import Path
sys.dont_write_bytecode = True
repo = Path(sys.argv[1])
sys.path.insert(0, str(repo / 'preregistration/natural-text-dense-replication-20261114/analysis')); sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
import n8_analysis as na
import c_synth

F, S = na.PLAN['first'], na.PLAN['second']
print('1. NOT_OVERFIT: validation loss at E3 minus E2 per width, over the completed draws')
for name, diffs in (('all falling', [-0.02 - 0.001 * k for k in range(24)]), ('all rising', [0.02 + 0.001 * k for k in range(24)]), ('mixed', [0.01 * (-1) ** k for k in range(24)]),
                    ('falling, upper limit within 1e-9 of 0', None)):
    if diffs is None:
        a = 0.001; half = na.t_quantile(0.975, 23) * a / math.sqrt(23); diffs = [-(half + 5e-10) + a * (-1) ** k for k in range(24)]
    per = {d: {arm: {2.0: dict(validation=4.7), 3.0: dict(validation=4.7 + diffs[k])} for arm in (F, S)} for k, d in enumerate(na.DRAWS)}
    out = na.not_overfit(per); x = out['512|lr1e-04']; print(f'   {name}: {x["label"]}, interval [{x["interval"]["interval"][0]:+.3e}, {x["interval"]["interval"][1]:+.3e}], n {x["interval"]["n"]}')

print('2. S-d: a saturated fit drops its draw at that readout only')
per = {d: {F: {e: dict(p=0.10 + 0.001 * k, saturated=False) for e in na.PLAN['path']}, S: {e: dict(p=0.09 + 0.002 * k, saturated=False) for e in na.PLAN['path']}} for k, d in enumerate(na.DRAWS)}
per['n05'][S][2.5] = dict(p=8.0, saturated=True); per['n06'][S][2.5] = dict(p=8.0, p32=9.0, saturated=False); per['n07'][F][2.5] = dict(p=None, saturated=False)
sd = na.path_contrasts(per); print('   draws at E2.5:', sd[2.5]['n'], '(n05 saturated and n07 undefined are out; n06, resolved at bound 32, stays with its bound-8 value', sd[2.5]['values']['n06'], ') | draws at E2.5625:', sd[2.5625]['n'])

print('3. starting offset: a refit that is undefined once the offset is taken off')
draws = na.DRAWS[:4]; data = {d: c_synth.make_draw(k, 256, 16)[0] for k, d in enumerate(draws)}; per = na.points(data)
h1 = na.contrast(per, draws, F, S, 'matched', 'train', 3.0, na.PLAN['path'], 2, 'ABOVE')
shifted = copy.deepcopy(data); arm = shifted['n02']['arms'][S]          # 768 of n02: E0 and every readout raised by 3 nats, so its gains are unchanged and the offset grows by 3
arm['e0'] = (np.frombuffer(arm['e0'], '<f4') + np.float32(3.0)).astype('<f4').tobytes(); arm['arrays'] = (np.frombuffer(arm['arrays'], '<f4') + np.float32(3.0)).astype('<f4').tobytes()
so = na.starting_offset(h1, shifted, dict(na.PLAN, draws=draws))
print('   rows:', {d: (r['status'], round(r['offset'], 4)) for d, r in so['rows'].items()}, '| draws in the contrast:', so['contrast']['n'], '| draws in the offset summary:', so['offset']['n'])

print('4. the refit threshold: gains proportional to w^q, read through arm_points')
n, nv = 400, 4
w = np.array([math.exp(math.log(.01) + (math.log(10) - math.log(.01)) * (i + .5) / n) for i in range(n)]); w = (w / w.mean()).astype('<f4'); wf = w.astype(np.float64)
for q in (7.9, 7.9985, 7.9995, 8.0, 9.0):
    g = (wf / wf.max()) ** q; e0 = np.concatenate([g, np.zeros(nv)]).astype('<f4'); arr = np.zeros(n + nv, dtype='<f4')          # gains = E0 - readout = g, exact in float32
    pt = na.arm_points(w.tolist(), dict(e0=e0.tobytes(), arrays=arr.tobytes(), record=dict(layout=dict(train_rows=n, validation_rows=nv, block_epochs=[3.0]), readouts=[dict(epoch=3.0, train_loss=0.0, validation_loss=0.0)])), diagnostics=False)[3.0]
    print(f'   q = {q}: p* = {pt["p"]:.6f}; refitted at bound 32: {"p32" in pt}' + (f' (p32 = {pt["p32"]:.6f})' if 'p32' in pt else '') + f'; saturated: {pt["saturated"]}')
~~~~

### `c_synth.py` (auditor C; SHA-256 `001afc91aa850a086f965176aba2d80f05ff4e3c49ed4ff104d4d840047ebb7a`)

~~~~python
"""POST HOC audit helper (area C). SYNTHETIC loss arrays on N8's grid, from fixed formulas; no N8 data. Used by c05 and c07."""
import math
import numpy as np

EP = [u / 1024 for u in (256, 512, 1024) + tuple(range(2048, 3584 + 1, 64))]      # N8's 28 readouts, written out independently
TAG = 'lr1e-04'


def make_draw(k, n, nv):
    """One draw: weights, two arms (E0, arrays, record) and four epochs of batch orders. 768 learns faster than 512, so 512's E3
    training loss is met by 768 near epoch 2.35."""
    i = np.arange(n); u = math.log(.01) + (math.log(10) - math.log(.01)) * (((i + 1) * 0.6180339887498949 + 0.137 * k) % 1.0)
    w = np.exp(u); w = (w / w.mean()).astype('<f4'); wf = w.astype(np.float64); arms = {}
    for width in (512, 768):
        wide = width == 768
        l0 = 6.0 + 0.3 * np.sin(1.7 * i + k) + (0.05 + 0.01 * math.sin(2.0 * k) if wide else 0.0)
        v0 = 6.3 + 0.2 * np.sin(0.9 * np.arange(nv) + k)
        e0 = np.concatenate([l0, v0]).astype('<f4'); blocks = []; readouts = []
        for e in EP:
            mean_gain = (1.15 + 0.34 * e + 0.012 * math.sin(1.3 * k)) if wide else (1.0 + 0.30 * e)
            q = (0.095 + 0.006 * e + 0.002 * math.sin(0.7 * k + 3 * e)) if wide else (0.10 + 0.004 * e + 0.002 * math.cos(0.5 * k))
            shape = wf ** q; gain = mean_gain * shape / shape.mean() + 0.2 * np.sin(3.1 * i + 5 * e + k + width / 100)
            tr = (l0 - gain).astype('<f4'); va = (v0 - 0.4 * e + 0.05 * e * e + (0.02 if wide else 0.0)).astype('<f4')
            blocks.append(np.concatenate([tr, va])); readouts.append(dict(epoch=e, update=round(e * n / 16), train_loss=float(tr.mean()), validation_loss=float(va.mean())))
        arms[(width, TAG)] = dict(e0=e0.tobytes(), arrays=np.concatenate(blocks).astype('<f4').tobytes(),
                                  record=dict(layout=dict(train_rows=n, validation_rows=nv, block_epochs=[0.25, 0.5, 1] + EP[3:]), readouts=readouts))
    order = np.stack([np.argsort(((np.arange(n) + 1) * (0.7548776662466927 + 0.01 * e) + 0.31 * k) % 1.0, kind='stable') for e in range(4)]).astype('<i8')
    return dict(weights=w.tolist(), arms=arms), order
~~~~
