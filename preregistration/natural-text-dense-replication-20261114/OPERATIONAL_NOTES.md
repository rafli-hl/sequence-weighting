# N8: operational notes for the results write-up

Dated operational events, known gaps and precautions of the runs. None changes a registered file, and none is a protocol deviation unless its entry says so. Completeness is checked after each run by `check_run.py <k>`, which reads only that run's two folders and the sealed source, fits nothing and prints no loss value. For a failed run it checks the complete draws in full, and the draw the run failed in against the terminal's record of what it left. For a retry run X<k> (`check_run.py X<k>`) it checks the retry's draws in full, and checks them against R<k>: the retry holds R<k>'s terminal, it repeats only the draws R<k> did not complete, with R<k>'s seeds and saved orders, and each receipt's comparison of the new E0 arrays with R<k>'s is recomputed. It reads nothing else of R<k>. The run records that hold no loss value are published in `run-records\` (24 November 2026).

## Known operational gaps

### The terminal's inventory counts one worker temp file (since R1)

- **What:** the worker's `TERMINAL.json` records an inventory of its run folder, taken just before the terminal is written. R1's records 48 files and 634,105,445 bytes. The run folder holds 47 files and 634,103,090 bytes besides `TERMINAL.json`. The difference is one file of 2,355 bytes.
- **Where it was:** in `runs\n8-r1\cache\`, the worker's temp folder (`TMPDIR`, which `text_framework_setup.py` points there).
  - Every stage receipt's ledger total carries the same 1 file and 2,355 bytes in its `cache\` term, from at least the end of n01.
  - `cache\` is now empty. It was last changed 31 ms after `TERMINAL.json` was written, and before the owner script wrote the worker's logs. So the file was deleted as the worker exited.
- **What it is not:** an output. Every data file is present and matches its recorded hash. Its name and contents are not known.
- **How it is handled:** `check_run.py` keeps its inventory check strict, so a run where this recurs fails that check. The check then reports whether the difference is exactly this gap: one file, the same in the terminal and in every stage receipt's ledger, with `cache\` empty and changed after the terminal. Anything else is reported as not the known gap.

| Run | Terminal less folder | Same in every stage receipt's ledger | `cache\` changed after the terminal | Known gap |
|---|---|---|---|---|
| R1 | 1 file, 2,355 bytes | yes | 31 ms after | yes |
| R2 | 1 file, 2,355 bytes | yes (n04 and n05; n06 has no receipt) | 90 ms after | yes |
| X2 | 1 file, 2,355 bytes | yes (n06) | 302 ms after | yes |

`check_run.py X2`, run on 23 November 2026, confirms X2's row (Events, 16 November).

## Operational precautions

### A GPU memory check before each claim (from X2 and R3; 16 November 2026)

- **Why:** another app's GPU memory stopped R2 in n06 (Events, 15 November).
- **What:** the owner's commands read the GPU memory used with `nvidia-smi` just before they call the owner script, which makes the claim. They are `X2_COMMAND.txt` (step 2) and `RUN_COMMAND.ps1` (`-Step Run`, R3–R8).
  - It takes five readings, 1 s apart. If any is over 600 MiB, nothing is claimed.
  - Either way, it lists the processes on the GPU, from `nvidia-smi`, with the dedicated GPU memory Windows counts for each, so the owner can close them.
- **What it changes:** no sealed file, and nothing the worker or the owner script does. It only queries `nvidia-smi` and a Windows performance counter.
  - The owner script's own check still runs before its claim. Under the sealed `GPU_CHECK.json` it refuses any reading over 658 MiB, or a mean utilization over 12%.
  - The checks before each draw are unchanged.
- **What it does not do:** it checks the start only.
  - Before each draw, the sealed check gates utilization, not memory. During a draw, only the worker's guard watches memory.
  - In every completed draw the guard's highest reading was 284 MiB under its limit.
  - GPU apps must stay closed until the run ends.
- **What the guard's reading measures is not established** (corrected on 24 November 2026, after the audit of version 2.1; the first version of this note said that about 284 MiB more GPU memory "in use during a draw, by anything, can stop the run", which the records do not show).
  - The guard's highest reading is the same to the byte, 2,386,349,260, in the pilot and in all six completed draws. In the start-up benchmarks it exceeds the worker's own reserved memory by the same 863,816,908 bytes at both widths.
  - Before each of the seven draws started, the worker's own reading was 918,342,860 bytes every time, while Windows `nvidia-smi` at the same checks read between 377 and 559 MiB (`run-records\`, the gate records). So over that range the worker's reading did not follow the memory Windows reported.
  - Yet in R2's n06 it rose by 1,012 MiB. So a threshold on the Windows reading at the start, such as the 600 MiB above, has not been shown to protect a draw.
- **The margin at start-up is smaller than the margin during a draw.** The start-up benchmark stops the run if the same reading exceeds 2,415,919,104 bytes (2.25 GiB), which is 28.2 MiB above the 2,386,349,260 it reached in each of the three benchmarks so far. A run stopped at start-up is used up, and its retry is then the one attempt left for its three draws.
- **A start refused by this check leaves no record.** The sealed owner script records each start it refuses (`PRESTART-REFUSED-<k>.json`). This check stops earlier and writes nothing, and its five readings are not saved. For X2 they were not noted; the owner script's own check, a moment later, read at most 324 MiB.

### One run at a time, a retry before the next run (owner, 16 November 2026)

- If a run R<k> does not complete, its retry X<k> runs before R<k+1>. So the draws stay in registry order (protocol section 8; n06 before n07), and no two runs overlap.
- `RUN_COMMAND.ps1` enforces it. R<k+1>'s build step reads R<k>'s exit receipt. Unless that receipt says COMPLETE, the build stops until X<k>'s exit receipt exists.
- For R3, the build therefore waits for X2 to end.

### A limitation of the completeness check (24 November 2026)

- `check_run.py` expects the gate folders to hold `PRESTART.json` and the draws' records only.
- If the sealed owner script refuses a start once (GPU busy, or not on AC power) and is then run again, it leaves a `PRESTART-REFUSED-<k>.json`, which the worker copies into the run folder. That is the sealed design, and the run is sound.
- For such a run the check, as published (`4df2aba5…`), reports two failures besides the known gap: the run folder's entries, and the exit receipt's gate files. They would be expected, not defects of the run. No run so far had a refused start. The check should be revised before R3.

## Events

- **15 November 2026, two empty folders before R1.** R1's first build stopped at `target.mkdir()` because `activations\` did not exist. Nothing was written or claimed. The empty folders `activations\` and `runs\` were created, and the owner's commands check both. Recorded in the published README's notes after registration.
- **15 November 2026, Run R1 COMPLETE.**
  - Approval `OWNER-20261115-N8-R1-01`; terminal `4ffead3f0c46e7f16d789a3368c753013417a51b8c9b92261d8f9d65c22b4c68`.
  - **It followed the registration.** The merge commit `c6f98b2` is dated 2026-11-14T18:19:19Z, which is 15 November 01:19:19 local time (+07:00). R1's approval record was built at 01:59:55 local time by the recorded builder (`c31fd4aa…`), and names that merge commit. The owner script's pre-start check began at 2026-11-14T19:00:20Z (02:00:20 local).
  - 8,225 s wall time, 7,568 s on the worker clock. Its draws took 2,491, 2,482 and 2,492 s, against a cap of 3,183 s per draw.
  - The power stayed on AC, and the three GPU checks were IDLE.
  - `check_run.py 1`: 54 passed, 1 failed, the failure being the known gap above. It was run with the check at SHA-256 `acfa48ee…`, before the check covered failed runs and retries; the published check (`4df2aba5…`) has the same 55 checks for a complete run.
- **15 November 2026, Run R2 FAILED in n06; n04 and n05 COMPLETE.**
  - Approval `OWNER-20261115-N8-R2-01`; terminal `2a02e9573e4009c066d43bbf9e7d25d588dc10bd763865828cc8e59007607fe8`. The owner script's exit receipt says FAILED, with worker exit code 1.
  - Its approval record was built at 13:59:34 local time on 15 November, and the pre-start check began at 2026-11-15T06:59:48Z (13:59:48 local). The clock times below are local, +07:00.
  - 7,770 s owner elapsed, 7,498 s on the worker clock. n04 and n05 took 2,792 s and 2,816 s on the worker clock, against a cap of 3,467 s per draw. The power stayed on AC.
  - **What stopped it.** The worker's guard samples the GPU memory used on the whole device (total less free, from `torch.cuda.mem_get_info`) at every update and forward pass. It stops the run above 2,684,354,560 bytes (2.5 GiB, `fewepoch_plan.GUARD_BYTES`).
    - In n06, at width 768 (a draw's first width), during an evaluation pass, it read 3,447,063,348 bytes and stopped with `RuntimeError: Sampled GPU limit`.
    - In each of the five draws completed so far (n01–n05), its highest reading was 2,386,349,260 bytes, 284 MiB under the limit. n06's reading was 1,060,714,088 bytes (1,012 MiB) above that.
    - The worker's own reserved GPU memory peaked at 1,522,532,352 bytes over the whole run, as in every completed draw. So the extra reading did not come from the worker's own allocations.
    - The owner reports that another app was using the GPU. The records do not show which, or how much memory it held (see "What the guard's reading measures is not established" above).
  - **The check before n06.** At 15:38:33 the owner script's check found the GPU BUSY on utilization: a mean of 13.8% against a limit of 12%, with 484 MiB in use (before a draw, memory is recorded, not gated). Its recheck at 15:39:46 was IDLE (10.4%; 472 MiB), and n06 started. The run stopped at 16:09:15, when `TERMINAL.json` was written.
  - **What n06 left, in place:** `INPUTS.json`, `ORDERS.i64`, `w768/E0.f32`, and the kept state `w768/E0.pt` (138,986,628 bytes, `efdb3733…`, as the terminal's `states_on_failure` records it). The retry's worker reads R2's run folder only to compare its new E0 arrays with the one left here (`w768/E0.f32`, by SHA-256, in `matched_worker.e0_against_first_attempt`), and reports the result in its n06 receipt.
  - `check_run.py 2`: 46 passed, 1 failed, the failure being the known gap above. n04 and n05 pass every check, and n06 matches the terminal's record of it. It was run with the check at SHA-256 `96808440…` on 16 November, and again with the published check (`4df2aba5…`) the same day, with the same result.
  - **Next, under protocol section 8:** n06 gets its one retry, Run X2, admitted on this terminal (`X2_COMMAND.txt`).
    - A dry check with the sealed `matched_worker.check_first_attempt` on this terminal admits X2, with n06 alone to repeat.
    - This is not a protocol deviation: section 8 provides the retry.
- **16 November 2026, Run X2 COMPLETE: n06 completed in the retry.**
  - Approval `OWNER-20261116-N8-X2-01`; terminal `f92644a3d989d4b221685f12cfe04518e56072221e3bb336240ba5c9ed931606`. It was admitted on R2's terminal `2a02e957…`, which its activation holds and its terminal binds.
  - Its approval record was built at 12:32:31 local time on 16 November, and the pre-start check began at 2026-11-16T05:32:40Z (12:32:40 local).
  - 3,010 s owner elapsed, 2,779 s on the worker clock; n06 took 2,683 s, against a cap of 3,294 s.
  - The owner script's check before its claim was IDLE, with at most 324 MiB in use. Its check before n06 was IDLE, at 377 MiB. The power stayed on AC.
  - The guard's highest reading in n06 was 2,386,349,260 bytes, as in every completed draw. The worker's logs are empty.
  - **E0 against R2's first attempt** (the n06 receipt):
    - w768 is DIFFERENT: R2 had left w768 E0 arrays for n06, and the retry's differ from them by SHA-256.
    - w512 is ABSENT: R2 left none.
    - This comparison is reported, not gating. Deterministic algorithms were not enforced, so bit-identical arrays were not expected. How much they differ is not examined here, since that needs the loss values.
  - The inventory shows the known gap above.
  - `check_run.py X2` (run on 23 November 2026, with the published check, `4df2aba5…`): 31 passed, 1 failed, the failure being the known gap above.
    - n06 passes every check of a complete draw, its arrays' hashes, layout and finiteness included.
    - Against R2: X2's copy of R2's terminal is byte for byte the one R2 wrote, and n06 has the same seeds and saved orders as R2's n06 (orders `19c09770…`).
    - The receipt's E0 comparison recomputes exactly from the arrays' SHA-256.
- **23 November 2026, training paused after 6 of 24 draws.**
  - n01–n06 are complete; n06 was completed in the retry X2. R3–R8 have not started.
  - Paused at the owner's decision for reasons unrelated to the data; no N8 result has been computed or examined. (This sentence was added on 24 November 2026.)
  - No p\* has been computed or examined, and the per-sequence losses stay unpublished until the sealed analysis.
  - Resuming continues with R3 under the registered protocol. If fewer than 20 draws are ever completed, the registered INCOMPLETE rule applies: no statistic and no label (protocol section 6).
- **24 November 2026, run records published; the audit of version 2.1.**
  - The records of R1, R2 and X2 that hold no loss value are published in `run-records\`: terminals, stage receipts, benchmarks, approval records, claims, exit receipts and the GPU and power check records. Every JSON file among them was scanned first: no key contains "loss".
  - The audit of version 2.1 found no registered number or label wrong. From it, this file was corrected (the guard's reading, the start-up margin) and extended (run times with their zone, time caps, the check's SHA-256 with each result, the check's limitation after a refused start).
  - **Still open before R3 or before any N8 loss is read:** a published loader for the run folders; a dated amendment to the protocol (a run that leaves no terminal, when the study ends, how tied weights are ranked, where mean losses are read from, the saturation rule's wording); the criterion for resuming; and the revised completeness check.
