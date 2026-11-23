# Pre-registration: dense-readout replication of N7 on fresh WikiText-103 draws (N8, 14 November 2026)

This folder publishes the protocol, the sealed code and the seeds of one study **before any of its training runs**. It reopens the closed record for this study only. Its purpose is to let anyone check that the hypotheses, the analysis and the readings were fixed before any result existed.

## Status, 23 November 2026: training paused

- **Training is paused after 6 of 24 draws:** n01–n06, with n06 completed in the retry run X2. R3–R8 have not started.
- **No p\* has been computed or examined.** The per-sequence losses stay unpublished until the sealed analysis.
- **Resuming continues with R3** under the registered protocol. If fewer than 20 draws are ever completed, the
  registered INCOMPLETE rule applies (protocol section 6): no statistic and no label.
- **The operational events** of R1, R2 and X2 and the known gaps are in
  [`OPERATIONAL_NOTES.md`](OPERATIONAL_NOTES.md):
  - R1 completed;
  - R2 stopped in n06 when GPU memory in use outside the worker tripped the worker's guard (another app, as the owner
    reports);
  - X2 completed n06.

  None changes a registered file or is a protocol deviation.

## Status when published

- **No study data exists.** No activation has been built and no run of this study has started. No model has trained on any of its 24 draws, and no loss, gain or p\* of this study exists.
- **The seeds have been drawn,** once, by the owner, on 14 November 2026 (approval `OWNER-20261114-N8-SEEDS-01`). All 16 post-draw checks passed ([`registry/n8-seed-registry/REGISTRY_AND_PARTITION_CHECK.json`](registry/n8-seed-registry/REGISTRY_AND_PARTITION_CHECK.json)).
- **The source is sealed and disabled:** subject `9bdea3a9715b05393afe6713ddc696834dd344c3485c4e1a6ed0fa222f44bb6b`. After the draw, only the registry and partition pins, the source README's two status lines and the owner script's hours text changed; `tools/build_n8_subject.py` accepts nothing more against the pending seal kept in [`seal/pre-pin/`](seal/pre-pin/).
- **The pilot passed** on 13 November 2026: one draw, N7's m01 with throwaway seeds, ran through the N8 worker on the GPU and was then discarded ([`pilot/PILOT_LOG.json`](pilot/PILOT_LOG.json)). It read no loss and fitted no p\*. It ran on source subject `9743b179…` ([`seal/pilot/`](seal/pilot/)), which differs from the sealed source only in the pins of `matched_plan.py` and `matched_registry.py`, the hours in `MATCHED_OWNER_RUN.ps1` and the source README. Its five seeds are among the registry's exclusions.
- **The activation builder refuses** until the merge commit and tag of this registration are recorded in it. Runs come only after that.

## Notes after registration

- **15 November 2026, wording.** The registered protocol's title ("Protocol draft") and its sentence "This is a new study in a new record. It reuses N7's sealed code and recipe, and adds nothing to the closed `sequence-weighting` record" predate the decision to register N8 inside the reopened record. Its status line governs: "FINAL, 14 November 2026. Registered by the merge into `rafli-hl/sequence-weighting` and the tag `n8-registration`." The registered file is not edited.
- **15 November 2026, the registration recorded.** The merge commit `c6f98b26669f5d29f30c576b6d800c1fc82c98eb` (pull request #1, signed by GitHub) and the tag `n8-registration` are recorded in the activation builder. [`tools/build_n8_activation.py`](tools/build_n8_activation.py) here is that recorded builder, SHA-256 `c31fd4aa…`. It differs from the registered builder that `HASHES.json` names (`30765693…`) only in its two lines `EXPECTED_SUBJECT` and `PUBLIC_REGISTRATION`, as `HASHES.json`'s `activation_builder_note` says.
- **15 November 2026, operational: two empty folders before R1.** The first build of R1's activation stopped with `FileNotFoundError` at `target.mkdir()` in `tools/build_n8_activation.py`. The builder makes the activation folder but not its parent, `activations\`, which did not exist in the study folder. It stopped before writing anything: no activation, approval record or claim was made, and nothing ran. The worker likewise makes its run folder but not its parent, `runs\`, and its first admission check reads the free space of `runs\`. In a run, that check comes after the owner script's claim, and the owner script does not look for the folder. So the two empty folders `activations\` and `runs\` are created in the study folder before the build, and the owner's commands for each run check that both exist. A test on N7's test doubles reproduces the failure and the fix. No registered file changes, so this is not a protocol deviation.

## The question

In N7, at learning rate 1e-4, the contrast p\*(512) − p\*(768) was below 0 at equal updates and above 0 at equal training loss. Width 768 was read by interpolating between readouts a quarter epoch apart, and the equal-update result was fragile. N8 asks whether, on fresh draws and with readouts dense enough that interpolation hardly matters, the order of the two widths again differs between the two alignments.

- **H1, equal training loss:** p\*(512, E3) − p\*(768 at 512's E3 training loss) > 0.
- **H2, equal updates:** p\*(512, E3) − p\*(768, E3) < 0.

The reversal is called replicated only if both are confirmed. Each hypothesis is labelled from a two-sided 95% t interval over draws, and needs at least 20 of the 24 draws.

## Design

| | |
|---|---|
| **Corpus** | WikiText-103 (manifest `be911db7…`), less every article and text that N5, N6 and N7 assigned: 14,039 fresh articles, 582,603 sequences |
| **Draws** | 24 fresh draws, n01–n24, of 16,384 sequences each |
| **Models** | Depth 4, 4 heads, context 128, 4,096-token vocabulary; widths 512 and 768 (16.9 M and 34.7 M parameters) |
| **Rate** | 1e-4 only |
| **Training** | Each width pre-trained uniformly to E0, then weighted for 3.5 epochs (3,584 updates); both widths share a draw's tokens, weights and batch orders |
| **Readouts** | E0, E0.25, E0.5, E1, then every 64 updates from update 2,048 to 3,584 (28 in all) |
| **Matching** | H1: 768 read along its 25 readouts from E2 to E3.5, by linear interpolation of fitted p\* at 512's E3 training loss. H2: both widths at update 3,072 |
| **Runs** | R1–R8 of three draws each; a run that stops early is retried once, from scratch with the same seeds (X1–X8) |
| **Analysis** | [`analysis/n8_analysis.py`](analysis/n8_analysis.py), which reproduces N7's published numbers from its released losses |

Sensitivity and secondary analyses, the reading rules carried over from N7, power and the failure rules are in the protocol.

## Contents

| Path | What it is |
|---|---|
| [`N8-protocol-draft.md`](N8-protocol-draft.md) | The protocol: question, hypotheses, design, data, matching, analysis, sample size, stopping and failures, limits |
| [`CHANGES.md`](CHANGES.md) | Every change from N7's sealed source, hunk by hunk, each with the protocol section that justifies it |
| [`HASHES.json`](HASHES.json) | The hashes binding all of this, including files that are not published here |
| [`source/`](source/) | The sealed study source. `SOURCE_SUBJECT.json` lists every file's SHA-256, and its own SHA-256 is the source subject |
| [`registry/n8-seed-registry/`](registry/n8-seed-registry/) | The owner-run draw: frozen policy, claim, exclusions, entropy record, registry, partition, post-draw checks, disclosure figures and receipt |
| [`analysis/`](analysis/) | The analysis and its tests on N7's released losses and on synthetic data |
| [`tools/`](tools/) | The fresh-pool count, the pilot, the seed draw and its checks, the post-draw revision, the seal, the writers of `CHANGES.md` and `HASHES.json`, and the activation builder |
| [`source-tests/`](source-tests/), [`tools-tests/`](tools-tests/) | The tests of the source and the tools, on synthetic data and stand-ins |
| [`tests-retired/`](tests-retired/) | The pilot command's test, retired after its one use |
| [`pilot/PILOT_LOG.json`](pilot/PILOT_LOG.json) | The pilot's log: timings, memory, the start-up benchmark, the checks and its five seeds |
| [`PILOT_COMMAND.txt`](PILOT_COMMAND.txt) | The owner's command that ran the pilot: its hash checks, its GPU and power checks, and the pilot's command line with the approval id and the five throwaway seeds |
| [`data-count/FRESH_POOL_COUNT.json`](data-count/FRESH_POOL_COUNT.json) | The owner's count of the fresh pool, made before the draw |
| [`OPERATIONAL_NOTES.md`](OPERATIONAL_NOTES.md) | Dated operational events of the runs (R1, R2, X2), known gaps and precautions, copied from the study folder |
| [`check_run.py`](check_run.py) | The completeness check run after each run (`check_run.py R<k>` or `X<k>`): structure, sizes, counts and hashes, with an audit hook that confines it to that run's folders and refuses every write. It fits nothing and prints no loss value |
| [`X2_COMMAND.txt`](X2_COMMAND.txt) | The owner's command for the retry run X2: its hash and tag checks, R2's FAILED exit receipt and terminal, the build with the approval id and text, and the GPU memory check before the claim |
| [`RUN_COMMAND.ps1`](RUN_COMMAND.ps1) | The owner's command for R3–R8, not yet used: the approval checked before anything is read, the build checks, R<k−1>'s retry first if R<k−1> did not complete, and the GPU memory check before the claim. It mentions `R2_COMMAND.txt`, which is not published |
| [`seal/`](seal/) | `pilot/`: the source subject the pilot ran on. `pre-pin/`: the pending seal before the draw, with the three files the post-draw revision changed |
| `.gitattributes` | Keeps every file in this folder byte for byte: git converts no line endings here. Three sealed files, byte copies of N7's, have CRLF line endings |

**Not included, by design:** the corpus, which is not redistributed here; N7's loss arrays and regenerated batch orders, which the analysis tests read (N7's arrays are the v1.2 release's `n7-loss-arrays-v1.zip`); the owner's draw command, `DRAW_COMMAND.txt`, and its retired test, which hold a local home path. `HASHES.json` names each of them by hash. Paths inside the code refer to the original research machine and are not portable entry points. Of the operational files written after registration, only those that `OPERATIONAL_NOTES.md` cites are published: the notes themselves, `check_run.py`, `X2_COMMAND.txt` and `RUN_COMMAND.ps1`. The owner's commands for R1 and R2, and the tests of the commands and of `check_run.py`, are not published.

## How to verify

```sh
sha256sum source/SOURCE_SUBJECT.json   # 9bdea3a9715b05393afe6713ddc696834dd344c3485c4e1a6ed0fa222f44bb6b
python3 - <<'PY'
import json, hashlib, pathlib
sha = lambda p: hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
s = json.loads(pathlib.Path('source/SOURCE_SUBJECT.json').read_text())
print('changed sealed files:', [f['path'] for f in s['files'] if sha('source/' + f['path']) != f['sha256']])
h = json.loads(pathlib.Path('HASHES.json').read_text())
named = {'protocol': 'N8-protocol-draft.md', 'changes': 'CHANGES.md', 'seed_registry': 'registry/n8-seed-registry/REGISTRY.json',
         'partition': 'registry/n8-seed-registry/PARTITION.json', 'pilot_log': 'pilot/PILOT_LOG.json'}
print('differs from HASHES.json:', [k for k, p in named.items() if sha(p) != h[k + '_sha256']])
PY
```

## Scope and limits

Small models, one corpus family, one pair of widths at one rate, and no claim about larger scales. Equal training loss inside an epoch still leaves exposure unequal, so N8 cannot say whether 512 leads once exposure is also matched. Draws are treated as independent, although they share the validation set, the pre-training pool and the tokenizer. The protocol's section 9 lists what N8 cannot settle.
