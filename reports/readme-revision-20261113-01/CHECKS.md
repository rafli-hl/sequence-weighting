# Checks run on the revised copy, 13 November 2026

Run on Linux with Python 3.13, NumPy 2.5.3 and PyTorch 2.7.0, against the v1.2 loss-array bundle
(`n7-loss-arrays-v1.zip`, SHA-256 `cbe26760…b8a9`). The CI workflows use Python 3.12 and were not run for this revision.

| Check | Command | Result |
|---|---|---|
| Files against the manifest; local Markdown links | `python tools/verify_publication.py` | 1,346 manifest rows, all exact; 0 missing; 0 unlisted; 511 local links, 0 broken |
| Estimator fixture | `python outputs/sequence-weighting-pilot/core_checks.py` (in a temporary copy) | `status: passed`; exponents 0, 0.5, 1 and 2 recovered within 1e-11; quadratic-form equivalence error 4.9e-20 |
| README example, as written in `README.md` and in the `verify` workflow | the Python block of "Reproducing the results" | `P1 = +0.00909 [+0.00400, +0.01417], n = 6`, both copies |
| README example, edge cases | the example's `read_768` on constructed inputs | a flat interval holding the target reads its earlier readout; a target outside the path returns `None`; a target held only by a later interval is read there |
| p\* from the per-sequence losses | `python tools/verify_n7_losses.py n7-loss-arrays` | 66 bundle files match; 240 fits, largest difference from `POINTS.csv` 2.9e-9; largest loss difference 8.6e-7; P1, S1, S3, S4, S5 match `ANALYSIS.json`; PASS |
| Post-hoc exposure analysis | `python tools/verify_posthoc.py n7-loss-arrays` | 268 published values, 268 reproduced, largest difference 0; PASS |
| Math, diagrams and images | `README.md` and `METHODS.md` rendered to PDF with KaTeX and Mermaid | 0 KaTeX errors; the Mermaid diagram renders; 0 broken images |
| Section anchors | links with `#` in the edited pages, checked against their headings | 9 checked, 0 broken |
| Workflow syntax | `.github/workflows/verify.yml` parsed as YAML | parses |

Every number quoted in the revised pages was checked against `ANALYSIS.json`, `MATCHED.csv`, `POINTS.csv`,
`FITS.csv`, `CURRENT_CLAIMS.md` or the follow-up audit before it was written. No discrepancy with a published value was
found, so no correction was needed. The figure scripts were rerun; their PNG and HTML bytes differ between runs and
environments (embedded metadata and identifiers), so the files in `docs/figures/` are the ones listed in the manifest.
