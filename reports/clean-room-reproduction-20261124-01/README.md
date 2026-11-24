# Clean-room reproduction of N7's analysis, 24 November 2026

**What this is.** A reproduction of N7's *analysis* by a separate AI session (Claude Fable 5.2), written from the
protocol, the reference study's technical note and the released loss arrays, without the original code or the
published results. It is not a human replication and not an independent one: an AI session launched by the project
did it, on the owner's machine. It does not cover the training: the per-sequence losses are taken as released.

**Result.** All 240 fits agree with the published p\* within 8.7e-9. Every registered statistic, sign test,
leave-one-draw-out side and label reproduces. The session found no possible error in the published analysis.

## Blinding was imperfect

The session's starting context included a line of the project's memory index that named N7's labels: P1
REVERSAL_CONFIRMED, confirmed through S5, S2 UNAVAILABLE. It held no number. The session reported this itself, in the
report's section 2. The numerical agreement cannot come from that line. The session's choice of readings could in
principle have been influenced, although the two readings where it differs from the original were logged before any
fit was run.

## The freeze before the comparison is recorded

Times are UTC, on 23 November 2026 (24 November in local time, +07:00).

| Event | Time | Record |
|---|---|---|
| Protocol, technical note and bundle fetched | 18:02 | the report's section 2 |
| Specification log written, before any fit | 18:05 | [`files/SPEC_LOG.md`](files/SPEC_LOG.md) |
| Newest frozen file written | 18:12:20 | file times, checked by [`files/supervisor_check.py`](files/supervisor_check.py) |
| Freeze: SHA-256 of the code, the log and 16 output files | 18:12:32 | [`files/FREEZE.txt`](files/FREEZE.txt), SHA-256 `66b44eb3a545a310aadbd82957479017f15e9a381185a74ce8b790c3a35a232a` |
| First request for a published table | 18:12:40 | the session's tool calls, in the supervising session's note |

Afterwards the supervising session checked the 22 hashes in `FREEZE.txt`, the session's 42 tool calls (no path to any
copy of the repository, no clone, no search) and a rerun of the frozen code, which reproduced all 16 frozen output
files byte for byte. Its note is the report's second part.

## Two points the written specification does not fix

The session logged each before any fit, chose another reading than the original, and found the difference harmless:

- **Tied weights.** The original ranks them in stable sort order. An empirical-CDF reading moves p\* by at most
  8.8e-9.
- **Mean losses.** The original takes the mean training and validation losses, and the matching targets, from the
  worker's records. The array means differ from them by at most 8.55e-7, which moves a matched value by at most
  6.8e-7.

Neither can move a label. [`METHODS.md`](../../METHODS.md) now states both.

## Contents

| Path | What it is |
|---|---|
| [`REPORT.md`](REPORT.md) | The report, byte for byte as written (as `n7_clean_room_reproduction_2026-11-24.md`; SHA-256 `0c43ca76ecfa84e4d3a2b4e3ddfb05945df066a069c7ad233de887e51cdab389`): the session's report as returned, the supervising session's note, the specification log, the freeze record, the complete code and the instructions the session was given |
| [`files/`](files/) | The session's working files: `BRIEF.md` (the owner's brief), `SPEC_LOG.md`, `FREEZE.txt`, `code/n7_repro.py` (frozen), `out/` (the frozen outputs of four variants), `phase2/` (the comparison and its evidence, written after the freeze), and the supervising session's check, note and rerun |
| `.gitattributes` | Keeps every file here byte for byte, so the frozen hashes stay checkable |

**Left out:** what the session downloaded. Each can be fetched again and checked by hash.
- The protocol: [`PROTOCOL.md`](../../preregistration/natural-text-matched-confirmation-20261104/sealed-source/PROTOCOL.md),
  SHA-256 `adf006ba…dd23e`.
- The technical note, a third party's document: SHA-256 `f7728b89…d346` as fetched from the URL in the brief.
- The bundle: the v1.2 release's `n7-loss-arrays-v1.zip`, SHA-256 `cbe26760…b8a9`.
- The four published tables it compared with, in
  [`natural-text-matched-analysis-20261105-01`](../natural-text-matched-analysis-20261105-01/).

`rerun_supervisor.log` is published as `rerun_supervisor.log.txt`, with the same bytes. Paths inside the files are
those of the machine it ran on.
