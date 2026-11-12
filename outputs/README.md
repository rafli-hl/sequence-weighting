# Outputs: earlier synthetic-task studies

This folder holds the project's earlier work, from late September to early October 2026, before the natural-text
studies in [`reports/`](../reports/README.md). It studies the estimator p\* and the weighting response on synthetic
tasks of the project's own design. Folders keep their original names and contents. Several hold source prepared for a
study that was never run; each folder's own README or protocol states its status, and inclusion here does not mean
that it ran.

**Start with** the [research note covering Stages 2–10](sequence-weighting-paper-track-v1/RESEARCH_NOTE.md), its
[claim audit](sequence-weighting-paper-track-v1/CLAIMS.md), and the
[figure catalogue](../figure/INDEX.md).

## Stages 1–11

| Folder | Study, as titled in its README |
|---|---|
| [`sequence-weighting-pilot`](sequence-weighting-pilot/) | Stage 1: local mechanism pilot. Also holds the core estimator, its fixtures (`core_checks.py`) and the environment lock |
| [`sequence-weighting-stage2`](sequence-weighting-stage2/) | Stage 2 (v0.3) |
| [`sequence-weighting-stage3`](sequence-weighting-stage3/) | Stage 3 (v0.4) |
| [`sequence-weighting-stage4`](sequence-weighting-stage4/) | Stage 4 (v0.5): controlled pretraining |
| [`sequence-weighting-stage5`](sequence-weighting-stage5/) | Stage 5 (v0.6): useful adaptation with epoch-0 selection |
| [`sequence-weighting-stage6`](sequence-weighting-stage6/) | Stage 6 (v0.7): selection stability |
| [`sequence-weighting-stage7`](sequence-weighting-stage7/) | Stage 7 (v0.8): CPU estimator validity |
| [`sequence-weighting-stage8`](sequence-weighting-stage8/) | Stage 8 (v0.9): fixed-input objective precision |
| [`sequence-weighting-stage9`](sequence-weighting-stage9/) | Stage 9 (v0.10) |
| [`sequence-weighting-stage10`](sequence-weighting-stage10/) | Stage 10: continuous-search agreement |
| [`sequence-weighting-stage11`](sequence-weighting-stage11/) | Stage 11 (v0.12): group-rule sharing |
| [`sequence-weighting-stage11-v0128`](sequence-weighting-stage11-v0128/) | Stage 11 v0128: one authorised preparation |
| [`sequence-weighting-paper-track-v1`](sequence-weighting-paper-track-v1/) | Research note, claim audit and literature review for Stages 2–10. The folder keeps its historical name, from the write-up track of October 2026, because other records cite its path |

## Diagnostics and later source packages (v0129–v0136)

| Folder | Study, as titled in its README or protocol |
|---|---|
| [`g1-clipping-diagnostic-v0129`](g1-clipping-diagnostic-v0129/) | G1 clipping diagnostic: protocol and source |
| [`g1-clipping-diagnostic-v0130`](g1-clipping-diagnostic-v0130/) | G1 clipping diagnostic, corrected; with its [decision record](g1-clipping-diagnostic-v0130/results/DECISION_RECORD.md) |
| [`sequence-weighting-weighting-contrast-v0131`](sequence-weighting-weighting-contrast-v0131/) | v0131: source-only handoff |
| [`sequence-weighting-factorial-v0132`](sequence-weighting-factorial-v0132/) | v0132: fresh factorial, source prepared |
| [`sequence-weighting-clipping-interaction-v0133-planning`](sequence-weighting-clipping-interaction-v0133-planning/) | v0133: proposed protocol |
| [`sequence-weighting-clipping-interaction-v0133`](sequence-weighting-clipping-interaction-v0133/) | v0133: clipping interaction, source candidate, not executed |
| [`sequence-weighting-clipping-interaction-v0133-r1`](sequence-weighting-clipping-interaction-v0133-r1/) | v0133-r1: import correction, not executed |
| [`sequence-weighting-gradient-alignment-v0134`](sequence-weighting-gradient-alignment-v0134/) | v0134: existing-checkpoint gradient panel, source candidate |
| [`sequence-weighting-preconditioning-v0135`](sequence-weighting-preconditioning-v0135/) | v0135: preconditioning; [result](sequence-weighting-preconditioning-v0135/results-fresh-preconditioning-v0135-20261005-01/RESULT_AND_DECISION_20261005.md): numerical audit passed, scientific gates failed |
| [`sequence-weighting-capacity-accounting-planning-20261005-01`](sequence-weighting-capacity-accounting-planning-20261005-01/) | Capacity-accounting plan manifest |
| [`v0136-planning`](v0136-planning/) | v0136: proposed protocol |
| [`sequence-weighting-compensation-calibration-v0136`](sequence-weighting-compensation-calibration-v0136/) | v0136: calibration; [result](sequence-weighting-compensation-calibration-v0136/results-fresh-compensation-calibration-v0136-20261005-01/RESULT_AND_DECISION_20261005.md): CALIBRATION_FAILED |

Historical READMEs in these folders contain the original machine's paths, approvals and run identifiers as context.
Their launch commands are not portable; see [`DATA_AVAILABILITY.md`](../DATA_AVAILABILITY.md).
