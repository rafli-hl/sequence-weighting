# Natural-text studies, 27 October – 11 November 2026

This page indexes the synthetic follow-up and the natural-text studies that came after the Stage 10 record. It also
covers the adversarial review of their claims, the response, N7 (the confirmation study the review led to), the audit
of the whole record, the correction that followed it, and the post-hoc analysis and second correction of 11 November.

**Read these first.** The current claims, with their scope and qualifications, are in
[`CURRENT_CLAIMS.md`](CURRENT_CLAIMS.md). The final claims as first written are in [`RESPONSE.md` §5](reports/adversarial-review-response-20261104-01/RESPONSE.md),
and they supersede every earlier summary before `CURRENT_CLAIMS.md`. Claims 4 and 5 should be read with
[`CLAIMS_4_AND_5_STATUS.md`](reports/adversarial-review-response-note-20261106-01/CLAIMS_4_AND_5_STATUS.md), which
records what N7 changed, with the [correction of 9 November](reports/natural-text-correction-20261109-01/CORRECTION.md),
and with the [correction of 11 November](reports/natural-text-correction-20261111-01/CORRECTION.md), which narrows how
N7's result can be read.
Wording that the response retired is listed in
[`SUPERSEDED_WORDING.md`](reports/natural-text-evidence-chain-20261104-01/SUPERSEDED_WORDING.md).

## Scope

All models are decoder-only Transformers of depth 4 and width at most 768 (at most 34.7 M parameters), trained on a
4 GB laptop GPU. Each draw holds 0.2–2.1 M unique training tokens. The reference study's models span tens of millions
to hundreds of billions of parameters. This work is therefore a small-scale methodological study of the estimator p\*
under training-progress and learning-rate confounds, not a replication.

"Pre-registered" in these records means specified and sealed by hash within the project before the data existed;
such protocols were not public until the record was published, from 9 November 2026. [`METHODS.md`](METHODS.md)
tabulates how each study was registered.
Two studies were also registered publicly. N6 was registered only after its data existed (see
[PR #3](reports/natural-text-peak-result-20261103-01/pr3-gh-snapshot-20261104/) and
[`NOTE_PUBLIC_REGISTRATION_EDITS.md`](reports/natural-text-peak-result-20261103-01/NOTE_PUBLIC_REGISTRATION_EDITS.md)).
N7 was registered before any of its runs (see [PR #5](reports/github-pr-snapshots-20261111-01/pr5/)).
The two registrations entered the history of the repository where this record was built
(`rafli-hl/sequence-weighting-research`, now private) as merge commits signed by GitHub: `58240f0` (3 November 2026,
16:14 UTC) for N6 and `f3a2571` (5 November 2026, 04:44 UTC) for N7. That history, signatures included, is archived at
[Software Heritage](https://archive.softwareheritage.org/browse/origin/?origin_url=https://github.com/rafli-hl/sequence-weighting-research), where the commits are
[`swh:1:rev:58240f0e0e86a8d5514267c80ac7c30f19fb4076`](https://archive.softwareheritage.org/swh:1:rev:58240f0e0e86a8d5514267c80ac7c30f19fb4076;origin=https://github.com/rafli-hl/sequence-weighting-research)
and
[`swh:1:rev:f3a2571029f4a0b4d0dc2ee974338e13996e11d8`](https://archive.softwareheritage.org/swh:1:rev:f3a2571029f4a0b4d0dc2ee974338e13996e11d8;origin=https://github.com/rafli-hl/sequence-weighting-research).
Neither registration folder has changed since its commit. Software Heritage identifies a folder by its git tree hash,
so the check needs no access to the old repository: in a clone of this one,

```
git rev-parse HEAD:preregistration/natural-text-peak-confirmation-20261103     # 5e985c1c6fe5892d70c3dde104a172a237955663
git rev-parse HEAD:preregistration/natural-text-matched-confirmation-20261104  # a452a968ae265c4df265127bd1662da679bd0619
```

prints the hashes of the folders as they stand in those two archived commits, `swh:1:dir:5e985c1…` and
`swh:1:dir:a452a96…`. Copies of the GitHub pages of the pull requests the record cites are in
[`github-pr-snapshots-20261111-01`](reports/github-pr-snapshots-20261111-01/README.md) (PR #3 in
[`pr3-gh-snapshot-20261104`](reports/natural-text-peak-result-20261103-01/pr3-gh-snapshot-20261104/)), and the pages of
both registration pull requests are also saved in the Internet Archive's Wayback Machine
([PR #3](https://web.archive.org/web/2026/https://github.com/rafli-hl/sequence-weighting-research/pull/3), [PR #5](https://web.archive.org/web/2026/https://github.com/rafli-hl/sequence-weighting-research/pull/5)).
Sealed labels and readings are quoted exactly as written in their own records.

## The studies

The review and the response use the labels S, N1 and N3–N6. N2 was a memory probe of width 768 on 30 October, with an
engineering verdict and no scientific outcome (see the evidence chains); its records are not published. N7 was
designed after the review to test its strongest post-hoc finding.

| Label | Study | Protocol and sealed source | Result | Tables |
|---|---|---|---|---|
| S | Synthetic capacity-shift follow-up, 12 fresh corpora | [`PROTOCOL.md`](work/capacity-shift-followup-source-20261027-01/PROTOCOL.md) | [`REPORT.md`](reports/capacity-shift-followup-result-20261028-01/REPORT.md) | [`analysis`](reports/capacity-shift-followup-analysis-20261027-01/) |
| N1 | WikiText-2 width ladder, per-width learning rates | [`PROTOCOL.md`](work/natural-text-ladder-source-20261028-02/PROTOCOL.md); [`AMENDMENT_01.md`](reports/natural-text-ladder-amendment-20261028-01/AMENDMENT_01.md); [`LR_SELECTION.json`](reports/natural-text-ladder-lr-selection-20261028-01/LR_SELECTION.json) | [`REPORT.md`](reports/natural-text-ladder-analysis-20261029-01/REPORT.md); [exploratory note](reports/natural-text-ladder-exploratory-20261029-01/EXPLORATORY_NOTE.md) | [`sealed-analysis`](reports/natural-text-ladder-analysis-20261029-01/sealed-analysis/) |
| N3 | WikiText-2 one-rate extension, 10 draws, 32 epochs at 3e-5 | [`PROTOCOL.md`](work/natural-text-onerate-source-20261030-02/PROTOCOL.md) | [`RESULT.md`](reports/natural-text-onerate-result-20261031-01/RESULT.md) | [`analysis`](reports/natural-text-onerate-analysis-20261030-02/) |
| N4 | WikiText-2 late-turn confirmation, 4 fresh draws | [`PROTOCOL.md`](work/natural-text-lateturn-source-20261031-01/PROTOCOL.md) | [`RESULT.md`](reports/natural-text-lateturn-result-20261031-01/RESULT.md) | [`analysis`](reports/natural-text-lateturn-analysis-20261031-01/) |
| N5 | WikiText-103 few-epoch study, 10 fresh draws, 3 epochs | [`PROTOCOL.md`](work/natural-text-fewepoch-source-20261101-01/PROTOCOL.md) | [`RESULT.md`](reports/natural-text-fewepoch-result-20261103-01/RESULT.md); [descriptive section](reports/natural-text-fewepoch-descriptive-20261103-01/DESCRIPTIVE.md) | [`analysis`](reports/natural-text-fewepoch-analysis-20261103-01/) |
| N6 | WikiText-103 peak confirmation, 6 fresh draws, two rates | [Registration](preregistration/natural-text-peak-confirmation-20261103/README.md) (sealed source and seed registry) | [`RESULT.md`](reports/natural-text-peak-result-20261103-01/RESULT.md) | [`analysis`](reports/natural-text-peak-analysis-20261103-01/) |
| N7 | WikiText-103 matched-progress confirmation, 6 fresh draws, two rates, readouts every quarter epoch from epoch 2 | [Registration](preregistration/natural-text-matched-confirmation-20261104/README.md) (sealed source, seed registry, real-engine check), merged before any run | [`RESULT.md`](reports/natural-text-matched-result-20261105-01/RESULT.md), with its [verification](reports/natural-text-matched-result-20261105-01/RESULT_VERIFICATION.json) and an [assistant check](reports/natural-text-matched-result-20261105-01/ASSISTANT_CHECK.md); run records in `reports/natural-text-matched-run-checks-20261104-01/`; [post-hoc analysis by exposure](reports/natural-text-matched-assistant-posthoc-20261111-01/), not a sealed result | [`analysis`](reports/natural-text-matched-analysis-20261105-01/) |

Seed registries for S, N1, N4 and N5 are in `reports/*-seed-registry-*/` (`REGISTRY.json`, `SEED_REGISTRY_POLICY.md`,
the draw and its exclusions).

## Failed attempts

Two runs failed for operational reasons. Under an owner ruling, each was rerun as a new attempt on the same draws and
seeds. Neither failed attempt was analysed.

- **N1, Run B, attempt 1.** The run slowed and hit its per-draw time limit. A game started on the GPU during the run; the timing
  coincides, but the records cannot prove the cause.
  [`FAILURE_REPORT.md`](reports/natural-text-ladder-run-b-failure-20261028-01/FAILURE_REPORT.md). Its list of what
  was read is incomplete; the correction of record is
  [`DECISION.md`](reports/natural-text-ladder-owner-decisions-20261104-01/DECISION.md), and both should be cited
  together.
- **N3, attempt 1.** The charger was unplugged during a draw.
  [`FAILURE_REPORT.md`](reports/natural-text-onerate-failure-20261030-01/FAILURE_REPORT.md).

## Synthesis, review and response

- **Evidence chains.** [31 October](reports/natural-text-evidence-chain-20261031-01/EVIDENCE_CHAIN.md) and
  [4 November](reports/natural-text-evidence-chain-20261104-01/EVIDENCE_CHAIN.md), with the
  [superseded-wording note](reports/natural-text-evidence-chain-20261104-01/SUPERSEDED_WORDING.md).
- **Adversarial review.** [`REVIEW.md`](reports/adversarial-review-20261104-01/REVIEW.md): a read-only review by the
  project's assistant under an adversarial brief, with two recomputation scripts and their outputs. Its
  matched-progress figures are post hoc and interpolated between readouts.
- **Response.** [`RESPONSE.md`](reports/adversarial-review-response-20261104-01/RESPONSE.md): the disposition of every
  point (concede, reword, reanalysis or partial rebuttal) and the final claims in §5.
- **Owner decisions.** `reports/natural-text-ladder-owner-decisions-*/`: the design decisions the protocols cite;
  the 4 November record of the response's acceptance, a search incident and its ruling, and the closure of the
  experiments; and the 5–6 November records of N7's analysis and its aftermath. Some earlier N7 decision records they
  cite are not published.

## N7 and after

- **Claims 4 and 5 after N7.**
  [`CLAIMS_4_AND_5_STATUS.md`](reports/adversarial-review-response-note-20261106-01/CLAIMS_4_AND_5_STATUS.md): what N7
  confirmed, what it left unchanged, and its limitations.
- **Assistant recomputation.** [`RECOMPUTE.json`](reports/natural-text-matched-assistant-recompute-20261106-01/RECOMPUTE.json)
  recomputes N7's confirmed statistics from `POINTS.csv`, with a post-hoc bound on an epoch-boundary concern. It is
  not a sealed result, and it cannot check p\* itself, the losses, the pre-adaptation state or clipping.
- **Audit, 8 November.** [`AUDIT.md`](reports/full-audit-20261108-01/AUDIT.md): a read-only audit of the whole record
  in nine areas. It found no blocking problem: every hash link holds, and every N7 statistic reproduces from
  `POINTS.csv`. It ranks nine major findings, most of them about how results are worded. Findings for five of the
  areas are in `reports/full-audit-20261108-01/<area>/FINDINGS.md`, and the auditor's own re-checks are in
  `verify_orchestrator.py` and `VERIFY_ORCHESTRATOR.txt`. The audit was carried out by AI assistants of the same
  family as the rest of the work.
- **Correction, 9 November.** [`CORRECTION.md`](reports/natural-text-correction-20261109-01/CORRECTION.md): N6's
  matched figures are biased by coarse interpolation (upward where the wider model is the one interpolated, which
  includes the figures that motivated N7; see the 12 November correction); the sentence "The 384→512 rise is mostly training
  progress" in claim 4 is withdrawn; and N7's S4 label depends on interpolation.
- **Post-hoc analysis by exposure, 11 November.** `REPORT.md`, `posthoc_exposure.py` and its exact output, in
  [`natural-text-matched-assistant-posthoc-20261111-01`](reports/natural-text-matched-assistant-posthoc-20261111-01/).
  From N7's per-sequence losses and the batch orders regenerated from the sealed code, it compares sequences by when
  they were trained: seen and not-yet-seen sequences, fixed sets across each quarter epoch, and the two widths on
  sequences matched for the timing of every pass. From `POINTS.csv` it adds each width at its better rate and the
  equal-updates contrast at every readout. It is descriptive and not registered, and was made and checked by AI
  models only.
- **Correction, 11 November.** [`CORRECTION.md`](reports/natural-text-correction-20261111-01/CORRECTION.md): which
  readouts would settle S4 (inside epochs 3.0–3.25 at 3e-4, not 2.0–2.25); how P1 should be read given that the models
  it compares differ in exposure; the audit's claim that other anchorings answer the exposure concern, withdrawn; S3
  as a result at epoch 3; and the wording changed in the living pages.
- **Follow-up audit, 12 November.** [`REPORT.md`](reports/follow-up-audit-20261112-01/REPORT.md): two fresh AI
  auditors (Claude Fable 5.2) audited the studies before N7 and alternative explanations for the current claims, the
  two areas of the 8 November audit that no fresh auditor had finished. Their reports are filed as returned, and the
  supervising session re-checked the main findings with separate code (`verify_findings.py` and `OUTPUT.txt`).
- **Correction, 12 November.** [`CORRECTION.md`](reports/natural-text-correction-20261112-01/CORRECTION.md): the
  direction of the bias in N6's matched figures; a like-for-like S4 figure; C1–C3 reworded to carry their sources'
  qualifications; the registered outcomes that did not confirm, now listed in `CURRENT_CLAIMS.md`; and C4's power,
  E0-offset, multiplicity and batch-relative-weighting disclosures.

## Status

The experiments were reopened for N7 alone and are closed again.

N7's primary, P1, is **REVERSAL_CONFIRMED**, and that label stands. At learning rate 1e-4 on six fresh draws, p\* at
width 512 at epoch 3 is above p\* at 768 when 768 is read at the training loss 512 reaches at epoch 3 (+0.00909
[+0.00400, +0.01417], 6/6 positive). At the same number of updates, at epoch 3, 768 is above 512 (S3: −0.00454
[−0.00795, −0.00114], 0/6 positive). At 3e-4, 512 is above 768 on both axes (S4 and S5). S2, matched on validation
loss, is unavailable.

**What the post-hoc analysis of 11 November adds.** It is descriptive, not registered, and moves no label.

- P1 compares models with different training exposure: 768 is read at epochs 2.19–2.48, having trained on 19–48% of
  the set a third time. Within one model, sequences already trained in the current epoch have p\* higher by
  0.050–0.084 than those not yet trained in it.
- On sequences matched for the timing of every pass, the contrast at 1e-4 for 512 at epoch 3 against 768 at epochs
  2.25, 2.5 and 2.75 is −0.0035 [−0.0258, +0.0189], −0.0048 [−0.0121, +0.0026] and −0.0051 [−0.0109, +0.0008]: the
  lead of 512 is not seen, and every interval includes 0. At 3e-4 the matched contrasts are about +0.013.
- With each width at its better rate of the two (512 at 3e-4, 768 at 1e-4), 512 is above 768 at equal updates
  (+0.01184 [+0.00789, +0.01578], 6/6) and at equal training loss (+0.01235 [+0.00523, +0.01947], 5/6).
- At 1e-4 the equal-updates contrast is below 0 only from epoch 2.5; at epochs 0.25–1, 512 is above 768.

These are small models on one corpus family. N7 shows that, at epoch 3 and 1e-4, whole-set p\* orders the two widths
one way at equal updates and the other way at equal overall training loss. It does not show that the order of the
widths reverses once training progress is matched: the equal-loss comparison leaves exposure unequal, and the
opposite signs appear only at the rate at which 512 trains 0.134 nats behind its own 3e-4 arm. It does not show a
capacity mechanism, and nothing about the reference study's scale follows. Open limitations include:

- S3's fragility when one draw is left out;
- S4's dependence on interpolation. The draw that decides it, m06, is read at epoch 3.083, so readouts of 768 at 3e-4
  inside epochs 3.0–3.25 would settle it. Readouts inside epochs 2.0–2.25, which this page named until 11 November,
  would not;
- P1's interpolation, which rests on readouts bracketing epochs 2–2.25 in three draws and 2.25–2.5 in the other
  three;
- the unequal exposure of the models that the matched readings compare. Finer readouts would not settle this; a
  design that matches training loss and exposure together would. Whether 512 leads at 1e-4 under such a match is not
  determined;
- the learning rates: two were run, and no width's best rate is located.

[`CURRENT_CLAIMS.md`](CURRENT_CLAIMS.md#open-questions-and-what-would-settle-them) lists what would settle each. No
further runs will be added to this record; that is not a restriction on anyone else.

## Not included

See [`DATA_AVAILABILITY.md`](DATA_AVAILABILITY.md). In brief, these are not published:

- run folders, model states and dataset rows, and per-sequence arrays except N7's (attached to the v1.2 release);
- preparation and probe packages, and seed-package and approval folders;
- run and engine-check receipts, and owner console output. The exceptions are N7's two owner exit receipts and its
  run, input and analysis-claim records, which are published. N7's analysis exit receipt is withheld because it holds
  a home path.
- the duplicated analysis rerun inside S's result folder;
- the raw battery report and Windows power-event export from N3's failure diagnosis. The published
  [`DIAGNOSIS.json`](reports/natural-text-onerate-failure-20261030-01/DIAGNOSIS.json) of that failure does hold an
  extract of them: 47 power and update events from the day of the run, with battery readings;
- the 8 November audit's working files (its scripts, logs and copies of public files), and the 12 November auditors'
  scripts; the re-check of the 12 November findings is published.

Scripts in the published folders that read run directories need those original inputs.
