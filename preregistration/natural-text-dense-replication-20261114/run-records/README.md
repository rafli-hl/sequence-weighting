# N8: run records of R1, R2 and X2

Byte copies of the records that the sealed worker and the sealed owner script wrote for the three runs made so far.
**None holds a loss value.** They were published on 24 November 2026 so that the statements in
[`OPERATIONAL_NOTES.md`](../OPERATIONAL_NOTES.md) can be checked, among them that every run followed the registration.

Before copying, every JSON file was scanned: no key in any of them contains "loss", and none holds a long numeric list.

## What is here, per run (`r1/`, `r2/`, `x2/`)

| Path | Written by | What it holds |
|---|---|---|
| `run/TERMINAL.json` | worker | Status, mode, draws, bindings, stage records, start-up decision, memory peaks, counts, inventory. Its SHA-256 is the terminal hash the notes quote |
| `run/<draw>-RECEIPT.json` | worker | One per completed draw: status, seconds, counts, memory peaks, ledger totals, and for a retry the SAME, DIFFERENT or ABSENT verdict on each width's E0 arrays |
| `run/BENCHMARK.json` | worker | The start-up benchmark: timings, memory peaks, the start-up decision and the time caps |
| `run/gpu-checks/` | worker | Its copy of the pre-start check, and per draw its request (with the worker's own device-memory reading) and the verdict it received |
| `activation/APPROVAL_RECORD.json`, `AUTHORIZATION.json` | builder | The owner's approval id and text, the builder's SHA-256, the public registration it records (merge commit and tag), and the bindings |
| `activation/OWNER_CLAIM.json`, `OWNER_EXIT_RECEIPT.json` | owner script | The one-use claim, and at exit: status, exit code, elapsed time, the terminal's SHA-256, the GPU and power checks |
| `activation/OWNER_PROGRESS.log.txt` | owner script | Its progress lines (`OWNER_PROGRESS.log`, renamed only because this repository ignores `*.log`) |
| `activation/gpu-checks/` | owner script | The Windows `nvidia-smi` check before the claim, and before each draw |
| `x2/activation/FIRST_ATTEMPT_TERMINAL.json` | builder | R2's terminal, on which the retry was admitted; byte for byte `r2/run/TERMINAL.json` |

## What they show

| Run | Approval record built (local, +07:00) | Pre-start check began (UTC) | Builder | Terminal SHA-256 |
|---|---|---|---|---|
| R1 | 2026-11-15 01:59:55 | 2026-11-14T19:00:20Z | `c31fd4aa…` | `4ffead3f…4c68`, COMPLETE |
| R2 | 2026-11-15 13:59:34 | 2026-11-15T06:59:48Z | `c31fd4aa…` | `2a02e957…7fe8`, FAILED in n06 |
| X2 | 2026-11-16 12:32:31 | 2026-11-16T05:32:40Z | `c31fd4aa…` | `f92644a3…1606`, COMPLETE |

- **Every run follows the registration.** The merge commit `c6f98b2` is dated 2026-11-14T18:19:19Z. R1's approval
  record was built 40 minutes later, by the recorded builder, and names that merge commit; its pre-start check began
  at 19:00:20Z.
- **Each terminal binds its approval record,** and each exit receipt gives its terminal's SHA-256.
- **The worker's own memory readings** (`wsl_device_used_bytes` in each `-REQUEST.json`) sit beside the Windows
  readings of the same check, for anyone who wants to see what the worker's guard measures.

## What is not here

Everything that holds a loss stays unpublished until the sealed analysis has run: the per-sequence arrays
(`E0.f32`, `arrays.f32`), each arm's `record.json` and each draw's `PRETRAINED.json` (mean losses), and the kept E0
states. Also not here: the draws' `INPUTS.json` and saved orders, the power logs, the worker's output logs, and the
copies of the sealed source and registries that each activation holds.

Paths inside the records are those of the machine the runs were made on.
