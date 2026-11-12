# Owner decisions, 9 November 2026: licence, loss-array bundle, release

Recorded by the assistant from the owner's answers in the session of 9 November 2026, after the external audit of
the public snapshot `95ccaaf` (its findings F02 and F10). The experiments remain closed; nothing here authorises a run.

## The decisions

1. **Licence.** The owner chose "MIT + CC-BY-4.0": MIT for code, CC BY 4.0 for reports, tables, figures and data.
2. **Loss arrays.** The owner chose "Yes, lift the rule for this": the rule that no assistant session opens anything
   under `work/runs/` is lifted for one purpose only, to read N7's per-draw `INPUTS.json`, `PRETRAINED.json`, the
   twelve `E0.f32` arrays, and the twenty-four `arrays.f32` arrays with their `record.json`, and to publish the
   weights, those arrays and records with a standalone verifier. The rule was introduced to protect blinding while
   experiments were open; all experiments are closed.
3. **Release.** The owner chose "Both": an automated check on GitHub, then a tagged release, v1.0.

## What was done under decision 2

- Read only the files named above, in `work/runs/natural-text-matched-m1-20261104-01/m01–m03/` and
  `work/runs/natural-text-matched-m2-20261104-01/m04–m06/`. No other file under `work/runs/` was opened.
- Before anything was published, the files were checked against the runs' own bindings: each `E0.f32` against the
  SHA-256 in its `PRETRAINED.json` (12/12), each `arrays.f32` against the SHA-256 in its `record.json` (24/24), and
  each draw's weights against the tensor hash recorded in its `INPUTS.json` (6/6).
- Published, as the release asset `n7-loss-arrays-v1.zip`: the six weight vectors (extracted from `INPUTS.json` as
  float32), the 36 loss arrays, the 24 run records, and a manifest. Not published: the rest of `INPUTS.json` (article
  identifiers, sequence indices), `PRETRAINED.json` (which lists deleted model-state hashes) and every other run file.

## Not authorised

Any run, any change to a sealed file or registered label, and opening any other file under `work/runs/`.
