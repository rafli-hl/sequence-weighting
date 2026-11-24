# Audit of the sequence-weighting record at v2.1 (30548db): area D, the conduct of N8 so far, with area F items

The full report is at `C:\Users\rafli\AppData\Local\Temp\swa21\d\scratch\FINDINGS.md` (89 KB, 922 lines). This message is not identical to the file: sections 1–3 are the same text, but sections 4 and 5 are condensed here. The file has the full source of every script and every output in full.

Auditor D of four. Public files only: my clone at `30548dbb789b2a117486fdf6f9ab9added680172`, read-only `git` and `gh api` GET requests, and the brief. Nothing on drive D: was opened, listed or searched. None of `check_run.py`, `X2_COMMAND.txt`, `RUN_COMMAND.ps1`, the builder, the worker or an owner script was run; where I tested logic I ran copies on dummy folders inside my scratch folder (section 4). The clone is unchanged (`git status --porcelain`: 0 lines; no `__pycache__`). I did not check the GitHub signature of `c6f98b2` (the supervising session does) and did not estimate any N8 result.

`N8/` below means `preregistration/natural-text-dense-replication-20261114/`. Line numbers are at commit 30548db.

## 1. Findings

### 1a. Summary

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

### 1b. The five events against the registered protocol

| Event | What the protocol says | Handled as prescribed? | Disclosed? | A deviation not called one? |
|---|---|---|---|---|
| R1 parent folders (15 Nov) | Nothing. Section 10, step 5: "Seal the protocol, source and registry by hash, merge them publicly and tag. Only then train." | Yes. Two empty folders were made outside every sealed file. The builder writes nothing before `target.mkdir()` (`N8/tools/build_n8_activation.py:135–136`), so the failed first build left nothing. | Yes: `N8/README.md:32`, `N8/OPERATIONAL_NOTES.md:48`. First public on 23 November (D6). | No |
| R2 failed in n06; retry X2 (15–16 Nov) | Section 8, lines 178–182: one retry, "admitted only on its first run's terminal record", "repeats from scratch, with the same seeds, the draws that run did not finish", "reports how each width's new E0 losses compare with the first attempt's" | Yes, on the notes' account and by the sealed code path (builder `:94–102`; worker `source/matched_worker.py:64–73, 121–127, 288–296`). X2 repeated n06 only. | Yes: notes lines 54–81. The size of the E0 difference is deferred (D5). | No. The reading rule for the analysis is not registered (D3). |
| GPU-memory check before the claim (16 Nov) | Nothing. Owner commands are not registered files. | Not applicable. It runs before the sealed owner script and changes no sealed file. It is stricter than the sealed limit (600 against 658 MiB). It cannot remove or select data: without a claim nothing is consumed. | Yes: notes lines 26–38. Two effects are not stated (D7), and its rationale is weak (D4). | No |
| Run order (16 Nov) | Section 8, line 177: "in eight runs, R1–R8, of three draws each, in registry order". Silent on when a retry runs. | Yes. n06 was retried before any R3. `RUN_COMMAND.ps1:93–95` enforces it for R3–R8 (tested, section 4). | Yes: notes lines 40–44. | No. The sealed code itself enforces no order between runs (D9). |
| Pause (23 Nov) | Nothing on pauses. Line 176: "24 draws, no interim analysis, and no look at any p\* before all 24 draws are complete". Lines 104–106: fewer than 20 finished is INCOMPLETE. | The protocol sets no schedule, so a pause breaks no stated rule. | The fact and the commitments are on every living page. The reason is not given anywhere (D2). | No |

### 1c. Findings table

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

### 1d. What in the notes can be checked from public files

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

## 2. Rejected concerns: checked and found sound

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

## 3. Before N8 resumes

In order of weight. None requires changing a registered rule or file.

1. **Fix the paused data and close D1.** Publish the SHA-256 of every loss-bearing file of n01–n06 and of what R2 left of n06. Publish the run records that hold no loss value (section 1d). The three terminal hashes already in the notes then become checkable, and each run can be shown to follow the merge commit.
2. **A dated note on the pause (D2):** its reason, who decides to resume and on what, and that the decision uses no N8 data.
3. **A dated note fixing how the analysis reads the runs (D3, D9),** before any p\* is computed: which folder each draw is read from, what "completed" means, that R2's n06 leftovers are not read, and what happens if a run leaves no terminal.
4. **Find out what the guard's reading measures before relying on a memory threshold (D4).** The paired readings are already in the gate records of seven draws. State the 28.2 MiB margin at start-up and the fact that a start-up stop leaves one attempt for three draws. The owner's commands are not registered and can be adjusted with a dated note; the sealed limits cannot.
5. **Make the completeness check agree with the sealed code's refused-start records (F-d1),** and give its SHA-256 with every result (D8).
6. **Record what the sealed code does not:** the new check's readings and refusals (D7), each run's stage cap beside its draws' times (F-d2), and the driver version and Windows build of each run (F-d3).

## 4. Scripts I wrote (all post hoc): condensed here, full source and output in FINDINGS.md

All are in `C:\Users\rafli\AppData\Local\Temp\swa21\d\scratch`. They read only my clone and dummy folders they create in the scratch folder. Python is `"C:\Users\rafli\AppData\Local\Programs\Python\Python312\python.exe" -I -B`; `<clone>` and `<scratch>` are the two folders of the assignment.

**4.1 `d01_hash_checks.py <clone>`** — pinned hashes, the sealed source, the three subjects, the pilot seeds, the terminal hashes. Output (complete, long hashes shortened only where marked):

```
== 1. hashes pinned in the owner commands
X2_COMMAND.txt has 4 distinct 64-hex strings
   251d0951e30250afa16cb998b06550358c09234d8a24c45166b08d0642347db6 -> pilot/PILOT_LOG.json MATCHES published file
   2a02e9573e4009c066d43bbf9e7d25d588dc10bd763865828cc8e59007607fe8 -> not a published-file pin (see below)
   9bdea3a9715b05393afe6713ddc696834dd344c3485c4e1a6ed0fa222f44bb6b -> source/SOURCE_SUBJECT.json MATCHES published file
   c31fd4aa32873a1d025621f06bcc66e289c16ad86f64612c00dad76b1fd62904 -> tools/build_n8_activation.py MATCHES published file
   merge commit c6f98b26669f5d29f30c576b6d800c1fc82c98eb named: True
RUN_COMMAND.ps1 has 3 distinct 64-hex strings
   251d0951…7db6 -> pilot/PILOT_LOG.json MATCHES published file
   9bdea3a9…bb6b -> source/SOURCE_SUBJECT.json MATCHES published file
   c31fd4aa…2904 -> tools/build_n8_activation.py MATCHES published file
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
   2a02e957…7fe8 -> ['…/OPERATIONAL_NOTES.md', '…/X2_COMMAND.txt']
   4ffead3f…4c68 -> ['…/OPERATIONAL_NOTES.md']
   f92644a3…1606 -> ['…/OPERATIONAL_NOTES.md']
```

**4.2 `d02_dummy_study.py <clone> <scratch> [<folder> [refused]]`** — builds a dummy study with invented contents (every "loss" is the sentinel 6.283185; n_train 1,024): R1 COMPLETE, R2 FAILED in n06, X2 COMPLETE, each with the known inventory gap; the `refused` variant adds one `PRESTART-REFUSED-1.json` to R1. Output: `n8-r1 48 files, 1237485 bytes; n8-r2 39 files, 876138 bytes; n8-x2 18 files, 414063 bytes` (refused variant: `n8-r1 49 files, 1237550 bytes`).

**4.3 `d03_run_check_copy.py <clone> <scratch>`** — makes `check_run_copy.py` and runs it on the dummy runs. Output:

```
published check_run.py sha256: 4df2aba506af47277599e411ddb988fdfc1dfa683695d16fb92f39b4110d9aa4
diff published -> scratch copy:
    @@ -25 +25 @@
    -STUDY = r'D:\sequence-weighting-n8'
    +STUDY = r'C:\Users\rafli\AppData\Local\Temp\swa21\d\scratch\dummy-study'
other mentions of drive D: left in the copy (comments and messages only): []
== R1: exit 1; PASS lines 54, FAIL lines 1, total checks 55
    54 passed, 1 failed
    The inventory failure is the known operational gap (OPERATIONAL_NOTES.md): 1 file, 2,355 bytes; every stage receipt's ledger carries the same (…)
    sentinel 6.28 in output: False | any float with 4+ decimals printed: []
== R2: exit 1; PASS lines 46, FAIL lines 1, total checks 47
    46 passed, 1 failed
    Run R2 did not complete: n04, n05 complete; n06 left for the retry run X2 (protocol section 8)
    sentinel 6.28 in output: False | any float with 4+ decimals printed: []
== X2: exit 1; PASS lines 31, FAIL lines 1, total checks 32
    31 passed, 1 failed
    sentinel 6.28 in output: False | any float with 4+ decimals printed: []
== R1 on the corrupted dummy: exit 1; PASS 45, FAIL 10, total 55
    sentinel 6.28 in output: False | "nan" in output: False | floats with 4+ decimals: []
```

**4.4 `d04_hook_test.py <scratch> X2`** (and `R1`) — the audit hook, installed as `main()` installs it. Output for X2, condensed to verdicts:

```
roots for X2: dummy-study\runs\n8-x2, dummy-study\activations\n8-x2, dummy-study\source, dummy-study\runs\n8-r2\TERMINAL.json, dummy-study\runs\n8-r2\n06
numpy imported under the hook: 2.5.3
ALLOWED  open run TERMINAL.json / activation AUTHORIZATION.json / source matched_plan.py / same path in upper case / list and rglob the run folder
ALLOWED  open R2 TERMINAL.json / R2 n06/INPUTS.json / R2 n06/w768/E0.f32
REFUSED  open R2 n04/INPUTS.json / R2 n04 arrays.f32 / R2 BENCHMARK.json / R2 n04-RECEIPT.json / list R2 run folder / activations/n8-r2/OWNER_EXIT_RECEIPT.json
REFUSED  open R1 TERMINAL.json / np.fromfile, np.memmap, os.open of an R1 array / open through ..\ / sibling folder n8-<run>-other / a file outside the study
REFUSED  list runs\ / os.scandir of the study folder / os.walk of R1 / glob R1 arrays
REFUSED  append, create, Path.write_bytes, os.remove, os.rename, os.mkdir, shutil.copyfile, subprocess.run, os.system, socket.socket()
ALLOWED  os.stat of an R1 array (size, times) / Path.is_file outside the roots / shutil.disk_usage   (metadata only: not covered by the hook)
files in the run folder unchanged
```

For R1 the roots are its two folders and the source only; R2's terminal and n06 are then refused.

**4.5 `d05_run_order_test.ps1 -Clone <clone> -Scratch <scratch>`** (Windows PowerShell 5.1) — executes lines 93–95 and 63–73 of `RUN_COMMAND.ps1`, taken unchanged by line number, with `$study` set to a dummy folder. Output:

```
--- (1) run order, Build step of R3 (k = 3, the run before it is R2)
  STOPS     no exit receipt of R2   [Run R2 has not ended: activations\n8-r2 has no OWNER_EXIT_RECEIPT.json. Runs go in registry ord]
  STOPS     R2 FAILED, no exit receipt of X2   [Run R2 did not complete (status FAILED) and its retry run X2 has not ended: activations\n8-x2 h]
  STOPS     R2 FAILED, X2 built but never claimed (activation folder, no exit receipt)   [same message]
  PROCEEDS  R2 FAILED, X2 ended COMPLETE
  PROCEEDS  R2 FAILED, X2 ended FAILED
  PROCEEDS  R2 COMPLETE, no X2
  STOPS     R2 STOPPED_AT_STARTUP, no X2
  STOPS     R2 EXIT_UNOBSERVED_NO_KILL, no X2
--- (2) approval checks, Build step of R3 (draws n07, n08, n09)
  ACCEPTED  id and text name Run R3, n07-n09 and the id
  REFUSED   no approval given / id names R4 / id date is not a date / text names a second run / text names a wrong draw / text lacks a draw / text lacks the id / text has a double quote
```

**4.6 d06** (no new script): `check_run_copy.py R1 --study <scratch>\dummy-study-refused --n-train 1024`. Output (FAIL and summary lines):

```
exit 1
FAIL  the run folder holds only the expected entries; its gate records are PRESTART and one request and one check per draw; …  [10 entries; cache\ empty folders]
FAIL  the terminal's inventory (files only, text_worker.Output.inventory) equals the run folder less TERMINAL.json itself  [terminal 1,237,733 bytes in 49 files; now 1,235,378 in 48]
FAIL  OWNER_EXIT_RECEIPT: its gate files' hashes equal the activation's gpu-checks; its power log hash equals POWER_LOG.jsonl  [PRESTART-REFUSED-1.json, PRESTART.json, n01-RESPONSE.json, n02-RESPONSE.json, n03-RESPONSE.json]
52 passed, 3 failed
The inventory failure is the known operational gap (OPERATIONAL_NOTES.md): …
2 other failure(s): report them
```

## 5. Commands that matter (condensed; full output in FINDINGS.md)

All in the clone, read-only.

- `git log --all --date=iso-strict --format='%h %p | A:%ad | C:%cd | %an / %cn | %G? | %s'`:
  ```
  30548db c1a2380 | A:2026-11-23T12:09:20+07:00 | … | rafli-hl / rafli-hl | N | Version 2.1: N8 paused
  c1a2380 88ac496 | A:2026-11-23T12:05:02+07:00 | … | rafli-hl / rafli-hl | N | N8 paused after 6 of 24 draws
  88ac496 c6f98b2 | A:2026-11-15T01:44:07+07:00 | … | rafli-hl / rafli-hl | N | Version 2.0: N8 registration notes and recorded builder
  c6f98b2 fee55ea aaafa2e | A:2026-11-15T01:19:19+07:00 | … | rafli-hl / GitHub | E | Merge pull request #1 from rafli-hl/n8-registration
  aaafa2e fee55ea | A:2026-11-15T01:17:02+07:00 | … | rafli-hl / rafli-hl | N | Register N8: dense-readout replication of N7
  ```
  (`E`: the signature could not be checked locally for want of the key.) All four tags are lightweight (`git cat-file -t` → `commit`).
- `gh api repos/rafli-hl/sequence-weighting/pulls/1`: `"created_at":"2026-11-14T18:17:44Z"`, `"merged_at":"2026-11-14T18:19:20Z"`, `"merge_commit_sha":"c6f98b26669f5d29f30c576b6d800c1fc82c98eb"`, `"head_sha":"aaafa2ed180c3c5c4c136f16fc3e7ef9a9515126"`.
- `gh api 'repos/rafli-hl/sequence-weighting/activity?per_page=100'` (GitHub's own times): branch `n8-registration` created 2026-11-14T18:17:18Z; `pr_merge` to c6f98b2 at 18:19:20Z; branch deleted 18:36:37Z; push of 88ac496 at 18:44:16Z; push of c1a2380 at 2026-11-23T05:05:16Z; push of 30548db at 05:09:33Z; a `force_push` a5c4a00 → c4ae0e1 on 2026-11-12T10:17:29Z.
- Releases: v2.1 published 2026-11-23T05:10:47Z, assets `[]`; v2.0 published 2026-11-14T18:45:38Z, assets `[]`; v1.2 has `n7-loss-arrays-v1.zip` only. Branches: `main` only. Actions artifacts: `total_count 0`. Wiki repository: not found. `gh api …/git/ref/tags/n8-registration` → `"type":"commit"`; `…/releases/tags/n8-registration` → 404.
- `git diff --name-status c6f98b2 30548db -- N8`: `A OPERATIONAL_NOTES.md`, `M README.md`, `A RUN_COMMAND.ps1`, `A X2_COMMAND.txt`, `A check_run.py`, `M tools/build_n8_activation.py`.
- `git diff c6f98b2 88ac496 -- N8/tools/build_n8_activation.py`: `-EXPECTED_SUBJECT = None`, `-PUBLIC_REGISTRATION = None` become the recorded values; nothing else. `git show c6f98b2:N8/tools/build_n8_activation.py | sha256sum` → `30765693bd8bb4929ba060c193a610ecc987413d0c83b8035c6a9044228471d3`.
- `git diff c1a2380 30548db -- N8/OPERATIONAL_NOTES.md`:
  ```
  -X2's row comes from file sizes, the terminal and the n06 receipt. `check_run.py X2`, which also reads every data file to hash it, had not been run by 23 November 2026.
  +`check_run.py X2`, run on 23 November 2026, confirms X2's row (Events, 16 November).
  +  - `check_run.py X2` (run on 23 November 2026): 31 passed, 1 failed, the failure being the known gap above.
  (+ three sub-bullets)
  ```
  `git diff 88ac496 c1a2380 -- N8/README.md` adds the note "15 November 2026, operational: two empty folders before R1". `grep -n "c1a2380" PUBLICATION_NOTES.md` prints nothing.
- Tree search for N8 run output (`git ls-tree -r --name-only HEAD | grep -i -E "n8-[rx][0-9]|/n[0-9]{2}/|…|\.f32$|\.i64$|\.pt$|…"`, excluding the older studies' folders): no output. `grep -rIn -E "n8-r[0-9]|n8-x[0-9]|sequence-weighting-n8"` outside the N8 folder: no output.
- `grep -n -i "pause\|resum"` over the living pages: 14 lines, all stating the pause and the resumption rule; none gives a reason.
- `diff` of `seal/pre-pin/<file>` against `source/<file>`: `matched_plan.py` lines 32–36 only (the pins); `MATCHED_OWNER_RUN.ps1` lines 17 and 78 only (the hours text); `README.md` lines 3 and 25 only.
- Clone unchanged: `git status --porcelain | wc -l` → `0`; no `__pycache__`; `git rev-parse HEAD` → `30548dbb789b2a117486fdf6f9ab9added680172`.
