# Publication notes

This repository is a curated publication copy of a local research repository. These notes record how the copy was
made and how it has changed, newest first.

## General principles

- **Byte-identical copies.** Files are copied byte for byte from the local record, at their historical relative
  paths, with three kinds of exception:
  - personal home-directory prefixes replaced with `<LOCAL_USER_HOME>`;
  - links to unpublished files annotated as unavailable;
  - Markdown reports from the initial publication translated into English.

  The first two kinds are mapped in [`PUBLICATION_TRANSFORMATIONS.json`](PUBLICATION_TRANSFORMATIONS.json).
- **Root pages.** The root pages (`README.md`, `METHODS.md`, `NATURAL_TEXT_STUDIES.md`, `DATA_AVAILABILITY.md` and this file),
  the two folder maps (`reports/README.md`, `outputs/README.md`), `CURRENT_CLAIMS.md`, `CITATION.cff`, the licence
  files, the two workflows, and the files in `docs/` and `tools/` are written for the publication copy. The root pages
  replace the local operational pages.
- **Hashes.** [`PUBLICATION_MANIFEST.csv`](PUBLICATION_MANIFEST.csv) records the size and SHA-256 of every published
  file. Hashes quoted inside historical records describe the original local files.
- **Nothing is rerun.** Preparing a publication copy runs no experiment, training job, fixture or analysis. Checks
  are limited to syntax, imports, links and bounded scans for credentials and personal paths, which cannot guarantee
  that no private information remains. The exceptions are dated below: the automated checks of versions 1.0 and 1.1,
  which run the estimator fixture and refit published data, the post-hoc analysis of 11 November, and the re-check of
  the follow-up audit of 12 November, and the checks and two descriptive summaries of 13 November.
- **Licence.** From 9 November 2026: MIT for code; CC BY 4.0 for everything else (`LICENSE`, `LICENSE-CC-BY-4.0.md`).

## 13 November 2026: README and methods revised (documentation only, unreleased)

An editorial and scientific revision of the living pages. No study, registered rule, label, sealed file, historical
record or published number changed, and no hash cited elsewhere changed. Changes:

- **`README.md` restructured** as an entry point: the question; the main finding with its qualifications; N7's
  paired-contrast figure; the registered results with their sensitivity analyses (leave-one-draw-out, later bracket
  end, the E0 offset, weight range, exposure matching, learning rate); the setup and an operational definition of p\*;
  reproduction; five reproducibility levels; limitations; links. Removed or corrected: "the complete record" (some
  artefacts are not published); "every figure and number below is a measured result" (some values are interpolated or
  derived); "only the first kind is a test of a hypothesis"; "p\* grows over training at every size" (some paths dip
  or fall); "at every training budget" (now limited to the evaluated readouts); "a higher p\* than it started with"
  (now: last readout against first readout); "parameter counts are exact" beside rounded values (exact counts are now
  given); "only the width changes" (head dimension, embedding and feed-forward sizes change with width); a causal
  "which is why" in a post-hoc caption; and the "Strong" evidence label. The reference study's report that more epochs
  move the peak to smaller sizes is now credited to it, and the README no longer presents that pattern as a finding of
  this record.
- **`METHODS.md` added.** It gathers material moved out of the README, with corrections: each study's registration
  type; data, splits and overlap rules; the full model and training specification (exact parameter counts, weights
  rescaled to mean 1, clipping of the summed gradient, the original environment); the estimator, its guards, checks and
  interpretation; alignments and baselines; what is interpolated (fitted p\*, not losses); the statistics; a corrected
  comparison with the reference study; and the descriptive figures with corrected captions.
- **New descriptive summaries, post hoc.** `reports/readme-revision-20261113-01/` holds two scripts and their output:
  `describe_fits.py` summarises N7's `FITS.csv` (no fit undefined or at a bound; objective at the fit 2.9–7.6% of its
  value at p = 0; negative gains for at most 3.9% of sequences), and `matched_set_weights.py` gives the sizes and weight
  medians of the exposure-matched sets of 11 November. They test nothing and move no label.
- **`CURRENT_CLAIMS.md`:** the paragraph on batch-relative weighting now says that clipping rescales the summed gradient
  and is not equivalent to normalising weights by their batch sum; C1–C3's status reads "sealed by hash within the
  project before the runs, not publicly preregistered"; "No further runs are authorised" now says the record is closed
  and that this restricts no one else; a broken README anchor is fixed.
- **`NATURAL_TEXT_STUDIES.md`:** the same closing sentence, and a note that internally sealed protocols were not public
  until 9 November. **`DATA_AVAILABILITY.md`:** five reproducibility levels and the practical blockers to retraining
  (corpus files, launch guards, numerics); the list of review records now includes 12 November.
- **Figures.** `docs/make_results_figures.py` labels its footnote "Fitted at evaluated readouts only" instead of
  "Measured results", and spaces the panels of `pstar-vs-training` so that labels no longer overlap; its four figures
  were redrawn. The plotted values are unchanged.
- **The `verify` workflow** runs the README's example as now written, which follows the registered reading rule for
  flat intervals and unavailable draws; its output and assertion are unchanged apart from the added draw count.
- **Checks run** on this copy: `tools/verify_publication.py`, `core_checks.py`, the README example,
  `tools/verify_n7_losses.py` and `tools/verify_posthoc.py` on the v1.2 bundle. Results are in
  `reports/readme-revision-20261113-01/CHECKS.md`.

## 12 November 2026: version 1.2, prepared for the final repository

The record moves to its final repository, `rafli-hl/sequence-weighting`, which starts from a single commit of these
files; the repository where it was built, `rafli-hl/sequence-weighting-research`, becomes private, and its history is
archived at Software Heritage. Changes for the move, with no change to any finding:

- **Links.** Release links point to the v1.2 release of the final repository, which attaches the unchanged loss-array
  bundle (SHA-256 `cbe26760…b8a9`); clone URLs and `CITATION.cff` point to the final repository; links to pull
  requests in the living pages point to the copies in the record. Links in historical files are unchanged, and the
  README's new section "Where this record was built" says where each kind now leads.
- **Registrations.** `NATURAL_TEXT_STUDIES.md` no longer asks for `git diff` against commits this repository does not
  contain. It gives the archived commits' identifiers and the tree hashes that show both registration folders
  unchanged, which can be checked in a clone of the final repository.
- **Checks.** `verify` and `verify-posthoc` fetch the bundle from the v1.2 release and skip that step until the
  release exists; `verify` also runs when a release is published.
- **Version.** `CITATION.cff` and the README's citation are at version 1.2, dated 12 November 2026.

## 12 November 2026: follow-up audit and a third correction

- **Audit.** `reports/follow-up-audit-20261112-01/`: the reports of two fresh auditors (Claude Fable 5.2) on the
  studies before N7 and on alternative explanations, filed as returned except for local paths and one out-of-scope
  line; `REPORT.md`, which says how each finding was handled; and `verify_findings.py` with its exact output
  `OUTPUT.txt`, the supervising session's re-check from published tables and the N7 loss arrays. The auditors' own
  scripts are not published.
- **Correction.** `reports/natural-text-correction-20261112-01/CORRECTION.md`.
- **Living pages.** `CURRENT_CLAIMS.md`: C1–C3 reworded; a table of registered outcomes that did not confirm; the
  training loss defined; batch-relative weighting under clipping, P1's planned and realised power, the E0 offset, the
  power of the exposure-matched comparison and a multiplicity note added. `NATURAL_TEXT_STUDIES.md`: N2 described, the
  N1 failure cause hedged, the direction of N6's bias given, the new folders listed. `README.md` and
  `reports/README.md`: the new folders and a power caveat.
- **Origin.** These files were written for the publication copy and have no separate local source.

## 11 November 2026: pull-request snapshots and two small corrections

- **Snapshots.** `reports/github-pr-snapshots-20261111-01/` holds read-only copies of the GitHub API responses for
  pull requests #1, #4, #5 and #6, which the record cites, so that their pages survive a move of the repository.
  Pull request #5 is N7's public registration. Commit lists and PR #1's timeline are left out (see the folder's
  README); nothing in the copies is edited.
- **Licence file.** `LICENSE-CC-BY-4.0.md` says that WikiText text is under CC BY-SA 3.0 and GFDL, as the dataset
  metadata records.
- **Folder map.** `outputs/README.md` explains the historical name of `sequence-weighting-paper-track-v1`.
- **Origin.** These files were written for the publication copy and have no separate local source.

## 11 November 2026: corrections to the root pages and the publication verifier

Changes after the version 1.1 entry below, prepared by an AI assistant (Claude Fable 5.2) at the owner's request after
a read-through of the whole copy and its Git history. None changes a sealed file, a registered label or a reported
number, and no historical file is edited.

- **Verifier.** `tools/verify_publication.py` now checks the links of published Markdown files only, and in a copy
  without Git it counts as published only the files that `.gitignore` does not exclude, so environments, caches,
  fetched assets, run folders and the estimator fixture's output are not reported as unlisted. Before this,
  following the README (creating `.venv`, or running `core_checks.py` in place in a downloaded archive) could make the
  check fail. The checks of the published files themselves are unchanged.
- **README.** The BibTeX entry gives version 1.1, as `CITATION.cff` does. The layout table lists
  `tools/verify_posthoc.py` and the files of `work/` outside the sealed source folders, and describes `migration/`
  as what it is. The environment commands activate the environment they create. The heading of the earlier work no
  longer says Stages 1–10, since the section and `outputs/` also cover Stage 11 and v0129–v0136.
- **Third-party assets.** `README.md` and `DATA_AVAILABILITY.md` name the dataset (WikiText, `Salesforce/wikitext`)
  and the model (`EleutherAI/pythia-70m`) with their publications, and say that the dataset metadata records GFDL
  beside CC BY-SA 3.0.
- **Power events.** `NATURAL_TEXT_STUDIES.md` said that the battery and power-event records of N3's failure
  diagnosis are not published. The raw records are not, but the published `DIAGNOSIS.json` holds an extract of 47
  events; the page now says so.
- **Registrations.** `NATURAL_TEXT_STUDIES.md` names the two GitHub-signed merge commits that carry the public
  registrations of N6 and N7, and the command that shows the registration folders unchanged since then.
- **Metadata.** `PUBLICATION_TRANSFORMATIONS.json` now lists the 91 Markdown files of the initial publication that
  commit `a232fd7` reworded on 6 October, a few hours after they were first committed. They are among the reports
  described under "Initial publication" below, and no source hash is mapped for them; until now only two of them
  were listed.
- **Other.** `DATA_AVAILABILITY.md` says which fixture needs no environment; `docs/make_n7_figure.py` notes that
  it overwrites the published image; `.gitignore` covers editor and operating-system files and the fixture's output.
- **Not changed.** `CITATION.cff`, the licence files and `outputs/README.md`. Whether these changes belong to
  version 1.1 or to a later version is the owner's decision.

## 11 November 2026: version 1.1 (release, and an automated check of the post-hoc analysis)

Version 1.1 is the record as of this entry. It adds no study, changes no sealed file, registered label or reported
number, and edits no historical file. Relative to version 1.0 it contains the post-hoc analysis and the correction of
the entry below, and:

- **Automated check.** `tools/verify_posthoc.py` reruns `posthoc_exposure.py` on the loss-array bundle and compares
  every per-draw value with the published `RESULTS.json` (absolute tolerance 1e-6, as for the loss-array check); the script stops if the
  regenerated batch orders fail its checks against the losses. `tools/requirements-posthoc.txt` pins the versions
  used (NumPy 2.5.3, PyTorch 2.7.0). The workflow `.github/workflows/verify-posthoc.yml` runs it when the files it
  checks change, weekly, when a release is published, and on demand; it checks the bundle's SHA-256 before use.
- **Citation.** `CITATION.cff` gives version 1.1 and its date.
- **Loss arrays.** The bundle is unchanged. It is attached to the v1.1 release as well, with the same SHA-256
  (`cbe26760e2062a4cf03307d779226fa6efce8cfcfbf57b2e092bd818af80b8a9`), so each release is complete on its own.
- **Origin.** The new files were written for the publication copy and have no separate local source.

## 11 November 2026: post-hoc analysis by exposure, and a second correction

Changes after the v1.0 release, prepared by an AI assistant (Claude Fable 5.2) at the owner's request. None changes a
sealed file, a registered label or a reported number, and no historical file is edited.

- **Post-hoc analysis.** `reports/natural-text-matched-assistant-posthoc-20261111-01/` is added: `REPORT.md`, the
  script `posthoc_exposure.py`, its exact output `OUTPUT.txt` and the per-draw values `RESULTS.json`. The script
  reads the v1.0 loss-array bundle and N7's `POINTS.csv`. This is an exception to "nothing is rerun" above: a new
  analysis was run on published data for this entry. No model was trained and nothing under `work/runs/` was opened.
- **Correction.** `reports/natural-text-correction-20261111-01/CORRECTION.md` is added. It quotes each statement it
  corrects, in historical files and in the v1.0 text of the root pages.
- **Root pages.** `CURRENT_CLAIMS.md`, `NATURAL_TEXT_STUDIES.md`, `README.md`, `DATA_AVAILABILITY.md` and
  `reports/README.md` are updated. The main changes: which readouts would settle S4; P1 as a comparison of models
  with unequal training exposure; the comparison with each width at its better rate; S3 as a result at epoch 3; an
  accurate description of how the learning rates were chosen; and a list of open questions with what would settle
  each.
- **Origin.** The files were written for the publication copy and placed, byte for byte, in the owner's local
  record.
- **Not changed.** `CITATION.cff` still gives version 1.0 and its release date; whether these changes make a new
  version is the owner's decision. The automated check does not run the new script, which needs PyTorch.

## 9 November 2026: version 1.0 (licences, automated check, N7 loss arrays)

Under the owner's decisions of 9 November
([`OWNER_DECISIONS.md`](reports/natural-text-ladder-owner-decisions-20261109-01/OWNER_DECISIONS.md)):

- **Licences.** `LICENSE` (MIT, for code) and `LICENSE-CC-BY-4.0.md` (for everything else) are added, and
  `CITATION.cff` records both and the version.
- **Loss arrays.** N7's per-draw weights, 36 per-sequence loss arrays and 24 run records are attached to the v1.0
  release as `n7-loss-arrays-v1.zip`, outside the Git history. Every array matched the SHA-256 recorded by its run,
  and every weight vector matched its run's tensor hash. `tools/verify_n7_losses.py` refits all 240 estimates from
  the bundle and recomputes the confirmed contrasts. The rest of each run's inputs and every other run file stay
  local.
- **Automated check.** `.github/workflows/verify.yml` runs the manifest and link verifier, the estimator fixture and
  the README example on every change, and refits the N7 estimates from the release bundle once it exists.
- **Owner decisions.** The decision record is published byte-identical to its local source.

## 9 November 2026: corrections from an external audit

An audit by OpenAI's Codex of the public snapshot at `95ccaaf` and of the local record led to these changes. None
changes a sealed file, a registered label or a reported number.

- **Estimator attribution.** The README now identifies p\* as the estimator of the reference study's technical note,
  which the project's `core.py` implements, and qualifies the reading of a fit at p\* = 0. The earlier statement that
  the estimator was a reconstruction was wrong.
- **Current claims.** `CURRENT_CLAIMS.md` states every current claim with its scope, status and qualifications,
  including S4's dependence on interpolation next to its label.
- **Correction note.** `CORRECTION.md` was amended in its local source and here: N6's figures are called biased upward
  rather than upper bounds, and the exact sign test is given first. Its manifest row is updated.
- **Checking.** `tools/verify_publication.py` checks every file against the manifest, distinguishing line-ending
  changes from real mismatches, and checks every local Markdown link. The README and `DATA_AVAILABILITY.md` explain
  how to get the canonical bytes on Windows.
- **Figure.** `docs/n7_result.png`, drawn by `docs/make_n7_figure.py` from the published table, shows N7's per-draw
  contrasts in the README.
- **Metadata.** `PUBLICATION_TRANSFORMATIONS.json` lists the two later edits whose hashes differed from the initial
  record. `PUBLICATION_LINK_LIMITATIONS.json` and `PUBLICATION_DEPENDENCIES.json` state their scope. A reported broken
  link in an owner-decision record is quoted text inside inline code, not a link.

## 9 November 2026: navigation pages and citation metadata

- **Maps.** [`reports/README.md`](reports/README.md) maps the 69 report folders by study and kind, and
  [`outputs/README.md`](outputs/README.md) maps the earlier synthetic-task folders. Both are written for the publication
  copy, like the root pages. No folder is moved or renamed, because their paths and hashes are cited elsewhere.
- **Citation.** `CITATION.cff` adds GitHub's "Cite this repository" entry.
- **Root README.** The layout table now links the two maps and lists `CITATION.cff`.

## 9 November 2026: audit report, correction and root pages

- **Audit.** The report of the read-only audit of 8 November 2026 is added: `AUDIT.md`, the findings of the five
  areas that wrote them, and the auditor's re-check script with its output. The other four areas' findings exist only
  in the audit's workflow journal and are merged into `AUDIT.md`. The audit's roughly 600 working files are not
  published: scripts, logs, and copies of public files and pull-request records. The audit was carried out by AI
  assistants.
- **Correction.** A dated correction note, `reports/natural-text-correction-20261109-01/CORRECTION.md`, says how to
  read claims 4 and 5 and N7's S4 in the light of the audit. No earlier file is edited.
- **Root pages.** The four root pages are rewritten for clarity. The README now leads with the main result and
  includes a reproduction example, a limitations section, a statement of how the work was done, a citation entry and
  the licence status.
- **Byte-identical.** All added files are byte-identical to their local sources, and none needed redaction.

## 6 November 2026: N7 results

N7's results (22 files) were added in [PR #6](reports/github-pr-snapshots-20261111-01/pr6/). All are
byte-identical to their local sources except `reports/natural-text-matched-result-20261105-01/RESULT.md`, whose one
home-path prefix is redacted. Beyond the earlier selection, the files include:

- N7's two owner exit receipts, run verifications, input check and analysis claim;
- the report-layout, verifier and input-check scripts, because the results report names them by hash.

N7's analysis exit receipt is withheld because it holds a home path; `RESULT.md` names it by hash. Some decision
records and approval requests cited by the added files are not published.

## 5 November 2026: N7 registration

N7's protocol, sealed source, seed registry and real-engine check were registered in
[PR #5](reports/github-pr-snapshots-20261111-01/pr5/), merged before any of its runs.

## 4 November 2026: natural-text studies

248 files from the synthetic follow-up and the natural-text studies were added in
[PR #4](reports/github-pr-snapshots-20261111-01/pr4/), indexed in
[`NATURAL_TEXT_STUDIES.md`](NATURAL_TEXT_STUDIES.md). All are byte-identical, and a scan for personal home paths found
none. The selection keeps:

- sealed source packages, protocols, results, analysis tables and seed registries;
- failure reports, evidence chains, the adversarial review and its response;
- the owner's design decisions (`reports/natural-text-ladder-owner-decisions-*`).

The design decisions are an exception to the general exclusion of approvals. The protocols cite them, and the
4 November decision file is the correction of record for one failure report.

Excluded:

- preparation, probe, seed-package and approval folders;
- run and engine-check receipts, and owner console output;
- a duplicated analysis rerun;
- machine battery and power-event records.

References inside the added files to excluded material are left as written so that the files stay byte-identical.

## 3 November 2026: N6 registration

N6's sealed source and seed registry were registered in
[PR #3](reports/natural-text-peak-result-20261103-01/pr3-gh-snapshot-20261104/), after its data existed and before its
analysis. The manifest's original row order and CRLF line endings were kept.

## 6–8 October 2026: initial publication

The publication copy was prepared as a clean distribution, without the local repository's history. The local history
contains an archive larger than GitHub's file limit.

**Included:**

- source code, configuration, dependency locks and fixture code;
- protocols, reports and claim summaries;
- small CSV, JSON and figure evidence.

Some small duplicated source files and tables remain so that report and fixture references still resolve.

**Excluded:**

- large archives, checkpoints and raw data;
- generated fixture-attempt trees, caches and downloaded packages;
- private conversations and operational or approval receipts;
- active capacity-reader source packages.

Markdown reports originally written in Indonesian or mixed-language prose were translated into English for this copy.
Measurements, uncertainty, negative and undefined findings, citations, commands and archival status were preserved.
On 8 October the completed v0135 and v0136 results were catalogued
([PR #1](reports/github-pr-snapshots-20261111-01/pr1/)).
