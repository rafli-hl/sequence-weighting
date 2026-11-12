# Data availability and reproducibility

This page says what the repository contains, what it leaves out, and what can be reproduced from it.

## What is included

- **Source code.** Versioned Python and scripts for every study, including the sealed source of each natural-text
  study, at its historical relative path.
- **Protocols and registrations.** Each study's protocol, amendments and seed registry, and the public registrations
  of N6 and N7.
- **Results.** Compact CSV and JSON outputs of every sealed analysis (per-readout p\*, losses and fits), results
  reports and their verification records, failure reports, and figures with their backing tables.
- **Review records.** The adversarial review, the response to it, the owner's design decisions for the natural-text
  studies, the audit of 8 November 2026 (its report and findings), and the corrections of 9 and 11 November 2026.
- **Post-hoc analysis.** The analysis of N7 by training exposure of 11 November 2026: its report, script, exact output
  and per-draw values.
- **Asset metadata.** Pinned revisions, file names and hashes of the public model and tokenizer
  (`EleutherAI/pythia-70m`) and the WikiText dataset (`Salesforce/wikitext`), in `work/text-assets/provenance.json`,
  `model-metadata.json` and `dataset-metadata.json`.

[`PUBLICATION_MANIFEST.csv`](PUBLICATION_MANIFEST.csv) lists every published file with its size and SHA-256.

## What is not included

- Run folders (`work/runs/`), model states and optimiser states.
- Per-sequence loss arrays and training traces, except N7's, which are attached to the
  [v1.2 release](https://github.com/rafli-hl/sequence-weighting/releases/tag/v1.2) as `n7-loss-arrays-v1.zip`.
- Dataset rows, tokenizer and model weights, downloaded packages, installers and caches.
- Private conversations, host receipts and most approval and accounting records. The exceptions are listed in
  [`PUBLICATION_NOTES.md`](PUBLICATION_NOTES.md): the owner's design decisions for the natural-text studies, and N7's
  owner exit receipts, run verifications, input check and analysis claim. N7's analysis exit receipt is withheld
  because it holds a home path.
- The audit's working files: its scripts, logs and copies of public files.

No external hosting of datasets or checkpoints is offered.

## What can be reproduced

There are three levels of reproduction. The repository supports the first for every study, and the second for N7:

1. **Statistics from the published tables.** Every reported statistic can be recomputed from the per-readout tables.
2. **p\* from per-sequence losses.** N7's loss arrays, weights and run records are attached to the v1.2 release, and
   `tools/verify_n7_losses.py` refits all 240 of its estimates. The earlier studies' arrays are not published.
   The same bundle supports analyses of N7 by training exposure. The bundle does not record which sequences were
   trained when, but it holds each draw's seeds, and the sealed source gives the rule that turns them into batch
   orders. `reports/natural-text-matched-assistant-posthoc-20261111-01/posthoc_exposure.py` regenerates the orders
   with PyTorch, checks them against the losses, and reproduces the post-hoc analysis.
3. **Training.** This needs the datasets, model states and run folders, and the original hardware.


| Task | Possible from this repository |
|---|---|
| Read the code, protocols and reported outcomes | Yes |
| Recompute every reported statistic from the per-readout tables | Yes. See the example in [`README.md`](README.md#reproducing-the-results) |
| Run the self-contained mathematical fixtures, such as `outputs/sequence-weighting-pilot/core_checks.py` | Yes. `core_checks.py` needs only the standard library; fixtures that import PyTorch need the environment |
| Recompute p\* from per-sequence losses | For N7, yes: from the v1.2 release bundle with `tools/verify_n7_losses.py`. For the earlier studies, no |
| Recompute p\* for subsets of N7's sequences defined by when they were trained | Yes, with NumPy and PyTorch: `posthoc_exposure.py` regenerates the batch orders from the seeds in the bundle and stops if they do not match the losses. The orders are regenerated, not recorded: the bundle holds no hash of them. `tools/verify_posthoc.py` reruns the analysis with the versions pinned in `tools/requirements-posthoc.txt` and compares every per-draw value with `RESULTS.json`; the `verify-posthoc` workflow runs it |
| Retrain any model and reproduce a result bit for bit | No. Datasets must be fetched, and states, run folders and the original hardware are not available |

Scripts that read saved run directories need those original inputs. Some scripts also contain the original machine's
absolute paths and must be edited before use.

## Public assets and their terms

- **Dataset.** WikiText-2 and WikiText-103 (Merity, Xiong, Bradbury and Socher, *Pointer Sentinel Mixture Models*,
  ICLR 2017), text drawn from Wikipedia, fetched from the Hugging Face dataset `Salesforce/wikitext` at the pinned
  revision. Its metadata records CC-BY-SA-3.0 and GFDL.
- **Model.** `EleutherAI/pythia-70m` (Biderman et al., *Pythia: A Suite for Analyzing Large Language Models Across
  Training and Scaling*, ICML 2023), used with its tokenizer by Stage 1's public-text check. Its metadata records
  Apache-2.0. The natural-text studies train their own tokenizer and models on WikiText.

`work/fetch_text_assets.py` is the historical download helper for the model and WikiText-2. It reads the metadata
files above and uses `curl.exe`, so it is a Windows helper rather than a cross-platform installer. Check the current
upstream terms and attribution requirements before fetching or redistributing either asset; this repository grants no
licence to them.

## Checking the files

`python tools/verify_publication.py` compares every file with `PUBLICATION_MANIFEST.csv` and checks every local
Markdown link. On Windows, clone with `git -c core.autocrlf=false clone ...` first: Git's usual Windows setting
converts line endings, so most text files would otherwise differ from their recorded hashes. The script reports such
files separately from real mismatches.

## Provenance

Most files are byte-identical to their local source. The exceptions are of three kinds:

- a few narrative and JSON records in which a personal home-directory prefix was replaced with `<LOCAL_USER_HOME>`;
- a few pages in which links to unpublished files are annotated as unavailable;
- the Markdown reports of the initial publication, which were translated into English.

[`PUBLICATION_TRANSFORMATIONS.json`](PUBLICATION_TRANSFORMATIONS.json) records the source and publication SHA-256 for
the first two kinds. Hashes quoted inside historical records describe the original local files, not newly signed releases.

Links to files that are not published are shown as unavailable and listed in
[`PUBLICATION_LINK_LIMITATIONS.json`](PUBLICATION_LINK_LIMITATIONS.json). Literal references to missing files are
listed in [`PUBLICATION_DEPENDENCIES.json`](PUBLICATION_DEPENDENCIES.json). External links in historical records were
kept as written, without a fresh check.

Packaging implies nothing beyond the records themselves. It does not certify dataset independence, the global
optimality of any fit, the success of a new execution, or novelty. Signed gains, guards on non-positive gains, failed
gates and undefined estimates keep their original meaning.
