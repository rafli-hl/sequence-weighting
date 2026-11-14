# Dense-readout replication (N8): disabled source

**This package has not run.** No seed of this study has been drawn, no activation exists, and none of this study's draws has been trained. One pilot draw, on N7's m01 with throwaway seeds, ran on source subject `9743b179…`, which differs from this source only in the pins of `matched_plan.py` and `matched_registry.py`, the hours in `MATCHED_OWNER_RUN.ps1` and this README; it was then discarded (`../pilot/PILOT_LOG.json`). No data of this study exists.

**Design:** `../N8-protocol-draft.md`. **Analysis:** `../analysis/n8_analysis.py`. **Every change from N7's sealed source:** `../CHANGES.md`.

## Files

**Changed from N7's sealed source** (subject `7ef133ad…`):
- `matched_plan.py`: the frozen constants: paths, pins, draws n01–n24 in runs R1–R8 and retry runs X1–X8, the arm at 1e-4, the readouts;
- `matched_data.py`: the fresh pool and partition, with N7's m01–m06 added to the assigned articles;
- `matched_registry.py`: the one-use registry tool, with N7's registry as one more exclusion source;
- `matched_worker.py`: the WSL/CUDA worker: the batch orders written with their hashes, E0 states kept, the retry runs;
- `MATCHED_OWNER_RUN.ps1`: the one-use owner entry of a run. It never runs from this directory;
- `AUTHORIZATION.json`, `README.md`.

**New:** `n7_matched_data.py`, a byte copy of N7's `matched_data.py`, which re-derives N7's partition.

**Dropped from N7's sealed source:** `matched_analysis.py` (N8's analysis is `../analysis/n8_analysis.py`) and `PROTOCOL.md` (N8's protocol is `../N8-protocol-draft.md`).

**Byte copies of N7's sealed source:** `peak_data.py`, `fewepoch_data.py`, `fewepoch_plan.py`, `fewepoch_registry.py`, `fewepoch_worker.py`, `fewepoch_analysis.py`, `wt103_corpus.py`, `acquire_plan.py`, `acquire_common.py`, `a1_download.py`, `a2_rows.py`, `text_data.py`, `text_plan.py`, `text_engine.py`, `text_worker.py`, `text_analysis.py`, `text_model.py`, `text_framework_setup.py`, `text_registry.py`, `vendor/core.py`, `ORIGINAL_ENVIRONMENT.json`, `gpu_check.ps1`, `GPU_CHECK.json`, `power_gate.ps1`.

## Status

**SEALED_DISABLED:** `AUTHORIZATION.json` is disabled. The seed policy is frozen (`../registry/n8-seed-registry/SEED_REGISTRY_POLICY.md`), and `matched_registry.py` and `matched_plan.py` pin it. The seed registry and the partition do not exist yet, so their pins in `matched_plan.py` are PENDING and `SOURCE_SUBJECT.json` records them as PENDING_OWNER_DRAW. The worker and the builder refuse real mode until a pin-only revision sets them.
