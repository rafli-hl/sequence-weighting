# Audit of the sequence-weighting record at v2.1 (30548db): area D, the conduct of N8 so far, with area F items

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

## 4. Scripts I wrote (all post hoc), with their commands and output

All are in `C:\Users\rafli\AppData\Local\Temp\swa21\d\scratch`. They read only my clone and dummy folders they create in the scratch folder. The published `check_run.py` and `RUN_COMMAND.ps1` were never run: d03, d04 and d06 run a scratch copy of the check whose one changed line is `STUDY`, and d05 executes eleven and three lines taken unchanged from `RUN_COMMAND.ps1` with `$study` set to a dummy folder.

### 4.1 `d01_hash_checks.py`: pinned hashes, the sealed source, the three subjects, the pilot seeds, the terminal hashes

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

### 4.2 `d02_dummy_study.py`: a dummy study with invented contents (every "loss" is the sentinel 6.283185)

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

### 4.3 `d03_run_check_copy.py`: a scratch copy of check_run.py on the dummy runs: number of checks, and whether a loss value is printed

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

### 4.4 `d04_hook_test.py`: the audit hook of check_run.py, through the scratch copy, on the dummy study

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

### 4.5 `d05_run_order_test.ps1`: the run-order rule and the approval checks of RUN_COMMAND.ps1, on dummy folders (Windows PowerShell 5.1)

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

### 4.6 d06: the scratch copy of the check on a dummy R1 with one refused start (no new script)

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


## 5. Commands that matter, with their output

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
