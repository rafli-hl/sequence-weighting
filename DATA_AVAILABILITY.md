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
  studies, the audits of 8 and 12 November 2026, and the corrections of 9, 11 and 12 November 2026.
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

Five levels, from the weakest to the strongest:

| Level | Possible from this repository | How, or what blocks it |
|---|---|---|
| 1. File integrity | Yes | `python tools/verify_publication.py` compares every file with `PUBLICATION_MANIFEST.csv` and checks every local Markdown link (see [Checking the files](#checking-the-files)) |
| 2. Statistics from the published tables | Yes, for every study | Each analysis folder's `POINTS.csv` holds per-draw, per-readout p\* and losses; N7's `MATCHED.csv` holds each draw's interpolation bracket. See the example in [`README.md`](README.md#reproducing-the-results) |
| 3. p\* from released per-sequence losses | N7 only | The v1.2 release bundle `n7-loss-arrays-v1.zip`; `tools/verify_n7_losses.py` refits all 240 estimates with NumPy. The earlier studies' per-sequence arrays are not published |
| 4. Losses from model evaluation | No | Each natural-text model state was hashed and then deleted during its run (each protocol's stage rule), and no model state of any study is published, so no model can be evaluated again |
| 5. Training from scratch | Not demonstrated | See below |

Level 3 also covers analyses of N7 by training exposure. The bundle does not record which sequences were trained when,
but it holds each draw's seeds, and the sealed source gives the rule that turns them into batch orders.
`reports/natural-text-matched-assistant-posthoc-20261111-01/posthoc_exposure.py` regenerates the orders with PyTorch,
stops if they do not match the losses, and reproduces the post-hoc analysis; `tools/verify_posthoc.py` reruns it with
the versions pinned in `tools/requirements-posthoc.txt` and compares every per-draw value with `RESULTS.json`. The
orders are regenerated, not recorded: the bundle holds no hash of them. Self-contained fixtures such as
`outputs/sequence-weighting-pilot/core_checks.py` need only the standard library; fixtures that import PyTorch need
the environment.

**Training from scratch.** Missing checkpoints do not by themselves prevent retraining: the protocols, sealed source,
hyperparameters, seed registries, article partitions (`PARTITION.json`) and the hashes of the data and tokenizer are
published, and WikiText is public. What stands in the way:

- **The corpus files.** The tokenizer, the corpus manifest and the tokenized sequence files are not published. They
  would have to be rebuilt from the pinned WikiText rows with the sealed acquisition code (it ran under WSL with
  `tokenizers` 0.21.4) and checked against the pinned hashes, for example the tokenizer's SHA-256 in
  `acquire_plan.py`.
- **The launch guards.** The sealed worker runs only from a one-use activation folder bound to an approval record and to
  the hashes of the original corpus manifest, registries and partition; the Windows launcher names the original
  machine's paths; and `text_framework_setup.py` refuses any Python, PyTorch, CUDA or cuDNN version or GPU model other
  than those in `ORIGINAL_ENVIRONMENT.json`. A retraining needs an adapted copy of this code, which would then no
  longer be the sealed source.
- **Numerics.** Deterministic algorithms were not enforced, so losses are not expected to be bit-identical even on the
  original hardware. A retraining would be a replication, compared with the published values within a tolerance that
  has not been set.

No one has attempted a retraining, and no runtime or memory figures beyond the original hardware are recorded.

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
