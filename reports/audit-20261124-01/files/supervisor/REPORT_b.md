**Delivery note.** `FINDINGS.md` was not written: the Write tool refused it ("Subagents should return findings as text, not write report files"), and I did not work around that. The full report is below; please save it to `C:\Users\rafli\AppData\Local\Temp\swa21\b\scratch\FINDINGS.md` if the file is needed. My scripts and their outputs are in that scratch folder (`b1_source_diff.py`, `b2_power.py`, `b3_registry.py`, `b4_n7_loo.py`, each with a `.out` file; `all_hashes.txt`).

# Auditor B: the N8 registration package (area B, plus area F items met on the way)

Audited: `preregistration/natural-text-dense-replication-20261114/` at tag `v2.1` (commit `30548dbb789b2a117486fdf6f9ab9added680172`), against tag `n8-registration` (commit `c6f98b26669f5d29f30c576b6d800c1fc82c98eb`) and N7's sealed source. Paths are relative to the repository root unless they start with `N8/`, which stands for `preregistration/natural-text-dense-replication-20261114/`. Line numbers are at commit `30548db`.

**Summary.** No registered number, label, hash, seed, partition or source file of N8 was found to be wrong.
- `CHANGES.md` is exactly the real difference from N7's sealed source: 61 hunks, and applying them to N7's files reproduces N8's files byte for byte.
- The seed registry re-derives from its own draw and exclusions, the partition is disjoint from N7's, the pilot log matches every figure in the protocol's section 7, and the power table reproduces.
- The builder change after registration is exactly two lines, and no other registered file changed.
- The findings are gaps, not errors. The registered analysis has no entry point for N8's own run folders (N7's sealed analysis had one). The protocol's failure rules are silent on a run that leaves no terminal and on when the study ends. All three can be settled by a dated note before any p\* is computed.

## 1. Findings

| ID | Area | Severity | Finding | Evidence | Status | Fix type |
|---|---|---|---|---|---|---|
| B1 | B | Major (a gap, not an error; see the note under the table) | **The registered analysis has no loader or driver for N8's own run folders.** `analysis/n8_analysis.py` is a library whose entry `analyse(per, data, plan, orders)` takes already-assembled inputs. Nothing registered says how `data` and `orders` are built from `runs\n8-r<k>` and `runs\n8-x<k>`: what makes a draw "completed" or "failed", which attempt's arrays are read for a retried draw (n06 exists in R2 and X2), which binding checks refuse or drop a draw, and what files the analysis writes. N7's sealed analysis registered all of this (`load`, with terminal, pin, receipt-against-terminal, array-hash and layout checks, and a `__main__` that wrote `ANALYSIS.json`, `POINTS.csv`, `FITS.csv`, `MATCHED.csv`). N8 dropped that file and did not replace those parts. | `N8/analysis/n8_analysis.py:16` ("Inputs. data[d] is None for a failed draw, or dict(weights=[...], arms=…"), `:562` (`def analyse(per, data, plan=PLAN, orders=None)`); it has no `__main__`, and a grep of `N8/analysis/*.py` for `RECEIPT`, `TERMINAL`, `n8-r`, `runs/`, `def load` finds only the three test/regeneration `__main__` blocks (section 5). `N8/HASHES.json:31-36` lists 4 analysis files and `:37-47` 9 tools; `N8/tools/write_hashes.py:26-27` hashes every file under `analysis/` and `tools/`, so no loader existed there at registration. N7: `preregistration/natural-text-matched-confirmation-20261104/sealed-source/matched_analysis.py:61` (`def load(runs, pins=…)`), `:413` (`if __name__ == '__main__':`); `sealed-source/PROTOCOL.md:205` ("The analysis: `matched_analysis.py` on M1 and M2, once both have ended with a terminal, with the results report's layout frozen first"). `N8/CHANGES.md:37` ("**Dropped** `matched_analysis.py` … N7's analysis; N8's is `analysis/n8_analysis.py` (§6)"). | VERIFIED | Dated note before the analysis, publishing the loader/driver with its SHA-256 before any p\* is computed (section 3) |
| B2 | B | Minor (protocol gap; has not occurred) | **The failure rules do not cover a run that leaves no terminal.** Section 8 admits a retry "only on its first run's terminal record", and the builder enforces it. The worker writes `TERMINAL.json` only from its `finally` block. A killed process, a WSL or machine crash, or a refusal after the owner script's claim but before the worker's `try` therefore leaves none; the run's activation is then consumed and its retry cannot be built. The protocol does not say what such a run's draws are: failed and excluded (three draws lost per event; two events can make the study INCOMPLETE), or the subject of a recorded deviation. It also does not say whether a draw with a COMPLETE receipt but no terminal counts. Two readers could count different draws from the same folders. N7's protocol had an explicit rule. A related leftover: N8's terminal still records `counted_as_attempt`, the field of N7's counting rule, which N8's protocol does not have (a start-up stop is retried as X<k> in N8). | `N8/N8-protocol-draft.md:178-182`; `N8/tools/build_n8_activation.py:96` ("Run {first} left no terminal, so it admits no retry"); `N8/source/matched_worker.py:309-312` (raises before the `try` at `:316`), `:362-374` (`finally:` … `out.json('TERMINAL.json', status)`), `:371` (`status['counted_as_attempt'] = …`); `N8/source/MATCHED_OWNER_RUN.ps1:55` ("One-use attempt consumed; no retry"). N7: `sealed-source/PROTOCOL.md:220` ("A run that leaves no terminal, because WSL died or the machine crashed, counts for nothing, whatever receipts are on disk. A draw counts only through a terminal's stage records."), `:207-209` (counting rule). | VERIFIED | Dated note before R3 |
| B3 | B | Minor (protocol gap) | **The stopping rule does not say when the study ends or when the one analysis runs.** "No look at any p\* before all 24 draws are complete" cannot be met literally once a draw has failed twice. Nothing says when a paused study is closed as INCOMPLETE (the README's "if fewer than 20 draws are ever completed" has no end point). N7 registered "once both have ended with a terminal, with the results report's layout frozen first"; N8 has no counterpart. This does not inflate the false-positive rate (INCOMPLETE gives no label), but it leaves the timing of the analysis to a later choice. | `N8/N8-protocol-draft.md:176` ("**Fixed sample.** 24 draws, no interim analysis, and no look at any p\* before all 24 draws are complete."), `:103-106`; `N8/README.md:9-10`; N7 `sealed-source/PROTOCOL.md:205`. | VERIFIED | Dated note before R3 |
| B4 | B | Minor | **The recorded builder differs from the registered one in exactly two lines, as disclosed, but those lines carry two things the disclosures do not mention.** (a) `PUBLIC_REGISTRATION` has a sixth key, `pr_record_sha256` = `e8d92b7e…f381`. The registered line's own comment did not list it ("dict(url, merge_commit, tag, source_subject_sha256, pilot_log_sha256)"), and it names a file that is not published and is not named in `HASHES.json`, the README or `PUBLICATION_NOTES.md`. (b) Both comments cite `registration/apply_registration.py`, which is not published. Neither changes behaviour: the code reads only `merge_commit`, `tag`, `source_subject_sha256` and `pilot_log_sha256`, and copies the whole dict into each `APPROVAL_RECORD.json`. | `git diff n8-registration v2.1 -- N8/tools/build_n8_activation.py` (section 5: 2 lines removed, 2 added); `N8/tools/build_n8_activation.py:30-31`, `:47`, `:53-54`, `:142`; `git grep` for `e8d92b7e`, `pr_record` and `apply_registration` (section 5); `N8/README.md:31`; `PUBLICATION_NOTES.md:90-94`; `N8/HASHES.json:144`. | VERIFIED | Doc-only (name the PR record and the tool, or publish them) |
| B5 | B | Minor | **Some hunks of `CHANGES.md` are justified by documents that are not published, although the protocol says each change is "justified by a section of this protocol".** Hunks 29 and 55 cite only "brief, item "paths"". Hunks 50, 58 and 60 cite nothing (they rename N7 to N8 or list files). Hunks 15, 18, 22 and 40 add "Gate 2 review", and hunks 49 and 54 "the owner's decision of 14 Nov 2026", to a section number. I read all 61: these are paths, names, messages, the study-folder census and kept states. None touches the model, optimiser, loss, weights, batch order or evaluation. | `N8/N8-protocol-draft.md:197-198`; `N8/CHANGES.md:3` (""brief" is the owner's task brief for N8"), `:523`, `:936`, `:877`, `:974`, `:1005`, `:333`, `:369`, `:417`, `:712`, `:859`, `:926`; `b1_source_diff.py` output (section 4). | VERIFIED | Doc-only |
| B6 | B | Minor | **A README note dated 15 November was first published on 23 November, and `PUBLICATION_NOTES.md` says the README "keeps" it.** The note "15 November 2026, operational: two empty folders before R1" is absent from the README at `v2.0` and first appears in commit `c1a2380`. No registered file is affected; the publication date of the note is not stated. | `git show v2.0:N8/README.md \| grep -c 'two empty folders'` → 0; at `c1a2380` and `v2.1` → 1; `N8/README.md:32`; `PUBLICATION_NOTES.md:68` ("keeps the note of 15 November on the two empty folders"). | VERIFIED | Doc-only |
| B7 | B | Minor | **The protocol's pilot summary gives the worker's own GPU memory but not the figure the guard acts on.** Section 7 reports "PyTorch reserved at most 1.42 GiB". The registered pilot log also records the device-wide sample the guard uses: 2,386,349,260 bytes against a limit of 2,684,354,560, which is 284 MiB of headroom and depends on other apps. R2 later failed on exactly this guard. The margin was in the registered data but not in the protocol's feasibility argument. | `N8/N8-protocol-draft.md:170`; `N8/pilot/PILOT_LOG.json` (`stage.guard_peaks.device_used_sampled` = 2386349260); `N8/OPERATIONAL_NOTES.md:57-59`; `b3_registry.py` output, last lines. | VERIFIED | A matter for N8's result report (state the margin with the pilot figures) |
| B8 | B | Suggestion | **Three statements about registered material cannot be checked from the public files.** (a) That the partition equals the sealed rule's output for `partition_seed` 1258837015: the corpus manifest (`be911db7…`) is not published. (b) That the pilot's source subject `9743b179…` differs from the sealed source "only in the pins … the hours … and the source README": only the hashes of the pilot's versions are published, so I can confirm which four files differ, not how. (c) Bound record `LR_SELECTION.json` (`fa760ba0…`) is not in the repository (inherited from N6 and N7). | (a) `N8/registry/n8-seed-registry/REGISTRY_AND_PARTITION_CHECK.json` asserts it; `DATA_AVAILABILITY.md:62`. (b) `N8/README.md:25`; `b3_registry.py` output: "pilot subject -> sealed subject: ['MATCHED_OWNER_RUN.ps1', 'README.md', 'matched_plan.py', 'matched_registry.py']". (c) `N8/source/SOURCE_SUBJECT.json:6`; no file with that hash among the 1,430 tracked files. | UNVERIFIED; (a) needs the manifest's per-article sequence counts and text hashes, (b) needs the four pilot-subject files, (c) needs the record | Doc-only |
| B9 | B | Suggestion | **Three points of wording for the eventual result report.** (a) The joint label is REVERSAL_NOT_REPLICATED whenever both hypotheses are not CONFIRMED, including when one is INCONCLUSIVE or UNAVAILABLE. The report should give the two component labels beside it and not present that case as evidence of no reversal. (b) "No multiplicity correction is needed" holds for the joint claim (I simulated 0.0249 at the boundary of the null). A single hypothesis reported "as it stands" is controlled at 2.5% on its own, and the chance that at least one of the two is confirmed in error can reach 5%. (c) Section 8 says a retry "reports how each width's new E0 losses compare with the first attempt's". The sealed code reports only SAME, DIFFERENT or ABSENT by SHA-256, and nothing registered computes a size. | `N8/N8-protocol-draft.md:84-90`, `:31-32`, `:181`; `N8/analysis/n8_analysis.py:411-422`; `e0_against_first_attempt` in `N8/source/matched_worker.py` (hunk 42, `N8/CHANGES.md:756`); `b2_power.py` output. | VERIFIED | A matter for N8's result report |
| B10 | B | Suggestion | **The README table counts 28 readouts while listing 29 items.** "E0, E0.25, E0.5, E1, then every 64 updates from update 2,048 to 3,584 (28 in all)": the 28 excludes E0, as the protocol's "28 readouts per arm instead of 10" does. | `N8/README.md:52`; `N8/N8-protocol-draft.md:42`, `:154`; `N8/source/matched_plan.py:64`. | VERIFIED | Doc-only |
| F-b1 | F | Minor | **Dates in the record mix UTC and local time without saying so.** The merge is 2026-11-14T18:19:19Z, which is 15 November 01:19:19 at +07:00; the living pages date the registration "14 November 2026". The `v2.0` release, 26 minutes later (18:45:38Z), is dated "15 November". The seed draw's "14 November" is local (receipt `finished_local` 2026-11-14 01:09:29). Run events are in local time, and R1 has no clock time in `OPERATIONAL_NOTES.md`. So the registration and R1 fall on the same local date, and their order cannot be read from the published dates alone. It follows from the design (the recorded builder holds the merge hash, and each terminal binds its approval record), which only the unpublished run records can show. | `git log`: `c6f98b2 2026-11-15T01:19:19+07:00`, `88ac496 2026-11-15T01:44:07+07:00`; GitHub PR #1 `merged_at 2026-11-14T18:19:20Z`; release v2.0 `published_at 2026-11-14T18:45:38Z` (section 5); `README.md:11`, `CURRENT_CLAIMS.md:221`, `NATURAL_TEXT_STUDIES.md:187`, `reports/README.md:34`; `PUBLICATION_NOTES.md:78`, `:99`; `N8/registry/n8-seed-registry/SEED_DRAW_RECEIPT.json`; `N8/OPERATIONAL_NOTES.md:49-53`. | VERIFIED (that R1 started after the merge is UNVERIFIED on public files; R1's claim time or its `APPROVAL_RECORD.json` would verify it) | Doc-only |
| F-b2 | F | Suggestion (for auditor D) | **The guard's highest device-wide reading is the same to the byte in the pilot and in every completed draw.** It is 2,386,349,260 bytes on 13 November (pilot) and, per the notes, in n01–n05 and in X2's n06. With the worker's own peak constant at 1,522,532,352 bytes, the memory in use outside the worker would be the same 863,816,908 bytes at each draw's peak on four days. I cannot tell from public files whether this is a fixed overhead or a sign that the guard's reading does not always follow other apps. It bears on how much the 600 MiB start check protects. | `N8/pilot/PILOT_LOG.json` (`stage.guard_peaks`); `N8/OPERATIONAL_NOTES.md:59-60`, `:72`. | UNVERIFIED (the per-draw `peaks` in the run receipts, and a controlled reading with a second GPU app open, would verify it) | A matter for N8's result report |

**Note on B1's severity.** I rate it Major because the folder's stated purpose is "to let anyone check that the hypotheses, the analysis and the readings were fixed before any result existed" (`N8/README.md:3`), and for the step from run folders to the analysis inputs that is not yet supported. Calibration: with every draw COMPLETE under a terminal, any reasonable loader gives the same inputs, so the labels are at risk only in edge cases (a receipt and terminal that disagree, a binding or hash that fails, a retried draw). It becomes a documentation matter once the loader is published with its hash before any p\* exists.

## 2. Rejected concerns: checked and found sound

- **`CHANGES.md` against the real diff.** My own byte comparison finds 24 files identical, 8 changed, 1 added and 2 dropped.
  - `CHANGES.md` lists the same 24, the same 7 changed files plus the regenerated `SOURCE_SUBJECT.json`, the added `n7_matched_data.py` (byte-equal to N7's `matched_data.py`) and the two dropped files, all with correct hash prefixes.
  - Applying its 61 hunks as a patch to N7's files reproduces N8's seven files byte for byte. An independent `difflib` diff with one line of context equals the listed hunks.
  - There are 61 notes, numbered 1–61, one per hunk, and no line-ending change in any changed file.
- **Each change against the section it cites.** I read all 61 hunks. The substantive ones follow from the cited sections:
  - readouts and one rate (§3; `READOUTS` gives updates 256, 512, 1,024 and 2,048–3,584 in steps of 64, 28 in all), and the match path (§5, §6);
  - N7's articles excluded, N7's registry pinned and the study-folder census (§4);
  - saved orders, kept E0 states and the 8 GB check before R1 (§3);
  - R1–R8 and X1–X8, with admission on the first attempt's terminal (§8).
  
  The training and evaluation code is in files that are byte copies of N7's, or in lines of `matched_worker.py` that no hunk touches. The model has no dropout and batch orders come from seeded generators (`N8/source/text_engine.py:53`), so denser readouts do not alter training.
- **`SOURCE_SUBJECT.json`.** Its SHA-256 is `9bdea3a9…`, and its 31 listed files match in bytes and hash.
  - The only unlisted files are itself and `AUTHORIZATION.json`, which `disabled_authorization_sha256` binds.
  - Its changed, dropped, new and byte-copy lists equal my diff, and its five registry and partition hashes equal the published files.
  - N7's sealed-source folder hashes to N7's subject `7ef133ad…`.
- **`HASHES.json`.** All 17 single-file hashes and all grouped hashes equal the published files, except the two disclosed cases: the builder (`c31fd4aa…` now, `30765693…` registered) and `tests-retired/test_draw_command.py` (named, not published). Every hash prefix quoted in the protocol, the two READMEs and `CHANGES.md` prose matches a hash I can compute.
- **Seed registry.** I re-derived it with my own code from `DRAW.json` (1,024 bytes, 256 little-endian uint32) and `EXCLUSIONS.json` (4,370 values).
  - The 98 role values equal `REGISTRY.json`; the first 98 candidates were all accepted.
  - The nearest exclusion is 37,913 away and the nearest other role 112,876, as the check record says.
  - The pilot's five seeds, and every role value and exclusion list of N7, N6, N5 and the three other published registries, are in N8's exclusions.
  - The claim, registry, receipt and check record agree with each other and with the sealed source's 13 registry-source hashes.
- **Partition.** It has 24 groups n01–n24, each of 16,384 distinct sequences, 393,216 in all.
  - It uses 9,500 articles, none shared between groups; 9,500 + 4,539 left over = 14,039.
  - It has no article or sequence in common with N7's published partition (2,412 articles, 98,304 sequences).
  - Per-draw counts equal `DISCLOSURE_FIGURES.md` and the check record.
  - Its hash equals the pin in `source/matched_plan.py`, the registry, the receipt and `HASHES.json`.
- **Protocol numbers.**
  - 24 × 16,384 = 393,216, and 393,216 + 24 × 327 = 401,064 ≤ 582,603.
  - The fresh pool is 14,039 articles and 582,603 sequences in the count file, the registry and the partition; 13,511 = 11,099 + 2,412.
  - Kept states come to 4.62 GiB; 48 × 28 = 1,344 and 24 × 10 = 240.
- **Pilot log against section 7.** Every figure matches:
  - 43.6 s (22.0 + 21.6), 2,528 s per draw, cap 3,097 s;
  - 867 s (55 / 242 / 570) and 1,660 s (101 / 462 / 1,097), evaluation share 0.68;
  - 7,629 s measured and 7,186 s projected, 1.42 GiB, about 17 h for eight runs.
  
  The log holds no loss and no p\*, and its seeds equal those in `PILOT_COMMAND.txt`.
- **Seals.** From the pending seal to the sealed subject, exactly `matched_plan.py` (five pin lines), `README.md` (two status lines) and `MATCHED_OWNER_RUN.ps1` (the hours text, two lines) changed, as the README says. The draw ran on the pending seal `9209b566…`.
- **Power argument (post hoc check).** Exact noncentral-t power and a simulation agree with the table.

  | Draws | H1 | H2 | Joint lower bound |
  |---|---|---|---|
  | 12 | 0.84 | 0.60 | 0.44 |
  | 16 | 0.94 | 0.74 | 0.68 |
  | 20 | 0.98 | 0.84 | 0.82 |
  | 24 | 0.99 | 0.91 | 0.90 |

  - With the protocol's rounded inputs H2 at 16 draws is 0.7453; with N7's unrounded values it is 0.7445, which is the table's 0.74.
  - Full effects at 8 draws give 0.917 ("at least 0.92" is that figure rounded). Two-thirds effects with SDs × 1.5 at 24 draws give 0.806 (0.81).
  - The planning effects and SDs are N7's published values halved (P1 +0.009088, SD 0.004845; S3 −0.004542, SD 0.003245).
  - For context, not in the protocol: an SD from six draws is uncertain by a factor of 0.62 to 2.45, and at half effects with SDs × 1.5 the lower bound falls to 0.43.
- **Statements in sections 1 and 6.**
  - S3's interval includes 0 without m03 or without m05 (published N7 values).
  - The lower t limit is concave in the contrasts, so its minimum over the box of brackets is at a vertex (also checked on 200 random boxes).
  - N7's P1 read width 768 at epochs 2.19–2.48, inside N8's path from 2.0 to 3.5.
  - N7's p\* values are near 0.10, far from the saturation bound. So the lower-case "saturated" in the availability rule (line 79) against the SATURATED rule (lines 92–95) is not a practical ambiguity, and the registered code settles it.
- **After registration.** The folder's tree is identical at the PR commit `aaafa2e` and the merge `c6f98b2` (74 files).
  - Between the merge and `v2.1` only `README.md` (additions, and one paragraph extended) and `tools/build_n8_activation.py` (two lines) changed, and four files were added.
  - No file that `HASHES.json` or `SOURCE_SUBJECT.json` binds changed other than the builder.
  - PR #1's `merge_commit_sha` is `c6f98b2`, GitHub reports its signature valid, and `n8-registration` points at it (a lightweight tag).
- **`write_hashes.py --check`.** I did not run it. From its code (`:20`, `:34`) it reads `DRAW_COMMAND.txt`, which is not published, so on the public copy it should stop with `FileNotFoundError` before comparing anything. My `b3_registry.py` is an equivalent on the published files.

## 3. To settle before N8 resumes

1. **The analysis entry point (B1).** A dated note, and the loader/driver published with its SHA-256 before any p\* is computed, ideally before R3. It can be tested without reading a loss, on the worker's test doubles. It needs to fix:
   - the criterion for a completed draw (for example a COMPLETE receipt that agrees with the terminal's stage records, as N7's `load` required);
   - which run a retried draw is read from;
   - which failed binding, hash or layout check refuses the analysis and which makes a draw failed;
   - where the weights and the orders are read from;
   - the files the analysis writes.
2. **A run with no terminal (B2).** A dated note saying whether its draws are failed and excluded, whether receipts without a terminal count, and whether anything other than X<k> may repeat them. If the answer departs from section 8, it is a deviation and should be called one.
3. **The end of the study (B3).** A dated note saying that the single analysis runs once every draw is complete or has failed twice, and on what dated declaration, made before any p\* is computed, a study that is not resumed is closed as INCOMPLETE.
4. **For the supervising session.** F-b1 (state the merge time with its zone, and R1's claim time) and F-b2 (the constant guard reading) belong with area D's check of the runs.

## 4. Scripts I wrote (all post hoc; all read only the clone)

Sources are in `C:\Users\rafli\AppData\Local\Temp\swa21\b\scratch\`; they are not reproduced here. Command for each: `"C:\Users\rafli\AppData\Local\Programs\Python\Python312\python.exe" -I -B -X utf8 <script> "C:/Users/rafli/AppData/Local/Temp/swa21/b/repo"`. Full outputs are beside them as `*.out`.

### `b1_source_diff.py` (post hoc): N8 `source/` against N7 `sealed-source/`, `SOURCE_SUBJECT.json`, and `CHANGES.md` applied as a patch

```
N7 sealed-source files: 34 | N8 source files: 33
identical: 24
changed  : ['AUTHORIZATION.json', 'MATCHED_OWNER_RUN.ps1', 'README.md', 'SOURCE_SUBJECT.json', 'matched_data.py', 'matched_plan.py', 'matched_registry.py', 'matched_worker.py']
added    : ['n7_matched_data.py']
dropped  : ['PROTOCOL.md', 'matched_analysis.py']
  added n7_matched_data.py sha b634f4b74157d127 byte-equal to N7 file(s): ['matched_data.py']

SOURCE_SUBJECT.json sha256: 9bdea3a9715b05393afe6713ddc696834dd344c3485c4e1a6ed0fa222f44bb6b
files listed: 31 | mismatching bytes/sha: []
in source/ but not listed: ['AUTHORIZATION.json', 'SOURCE_SUBJECT.json']
listed but not in source/: []
changed_from_n7 (subject): ['matched_plan.py', 'matched_data.py', 'matched_registry.py', 'matched_worker.py', 'MATCHED_OWNER_RUN.ps1', 'README.md'] | equals my changed minus unlisted: True
dropped_from_n7 (subject): ['matched_analysis.py', 'PROTOCOL.md'] | equals mine: True
new_files (subject): ['n7_matched_data.py'] | equals mine: True
byte_copies_of_n7_source keys equal my identical set (minus unlisted): True | values: {'7ef133ad0120d0852c93ebe65f020718f51cebbf75abd43c29f89cdec8674f56'}
N7 SOURCE_SUBJECT.json sha256: 7ef133ad0120d0852c93ebe65f020718f51cebbf75abd43c29f89cdec8674f56
disabled_authorization_sha256 matches source/AUTHORIZATION.json: True | AUTHORIZATION.json: {'enabled': False, 'execution_ready': False, 'note': 'Sealed disabled source of the dense-readout replication (N8); activations are built per run by the pinned builder after owner approval and after the public registration is merged.'}
  subject draw_sha256 == sha256(DRAW.json): True
  subject exclusions_sha256 == sha256(EXCLUSIONS.json): True
  subject partition_sha256 == sha256(PARTITION.json): True
  subject policy_sha256 == sha256(SEED_REGISTRY_POLICY.md): True
  subject registry_sha256 == sha256(REGISTRY.json): True
  bound record reports/natural-text-fewepoch-seed-registry-20261101-01/REGISTRY.json: MATCH
  bound record reports/natural-text-matched-analysis-20261105-01/ANALYSIS.json: MATCH
  bound record reports/natural-text-matched-seed-registry-20261104-01/REGISTRY.json: ABSENT in clone
  bound record reports/natural-text-peak-analysis-approval-20261103-01/pinned-records/LR_SELECTION.json: ABSENT in clone
  bound record reports/natural-text-peak-seed-registry-20261103-01/REGISTRY.json: ABSENT in clone
N7 subject lists 32 files; N7 files mismatching their own subject: [] | N7 unlisted: ['AUTHORIZATION.json', 'SOURCE_SUBJECT.json']

CHANGES.md sha256: 73f72f3a11e5045ac79e30332743186009bfefdd8ada0d6a42a33f02928edd77 | CR bytes in it: 0
CHANGES Unchanged lists 24 files; my identical set has 24
  listed as unchanged but not identical: []
  identical but not listed as unchanged: []
  hash prefixes wrong: []
CHANGES Added: [('n7_matched_data.py', 'b634f4b74157d127')] | Dropped: [('matched_analysis.py', '2108f0b287a0b355'), ('PROTOCOL.md', 'adf006ba144efccb')] | Regenerated: ['SOURCE_SUBJECT.json']
  added hash prefix ok: n7_matched_data.py True
  dropped hash prefix ok (N7 file): matched_analysis.py True
  dropped hash prefix ok (N7 file): PROTOCOL.md True
CHANGES per-file sections: ['matched_plan.py', 'matched_data.py', 'matched_registry.py', 'matched_worker.py', 'MATCHED_OWNER_RUN.ps1', 'AUTHORIZATION.json', 'README.md']
  equals my changed set minus SOURCE_SUBJECT.json: True
matched_plan.py: fenced blocks 6, hunks 6, +40/-60 lines | patch(N7)==N8 bytes: True | my difflib(n=1) hunks identical to listed: True | (CRLF,LF) N7 (0, 89) N8 (0, 69)
matched_data.py: fenced blocks 7, hunks 7, +21/-18 lines | patch(N7)==N8 bytes: True | my difflib(n=1) hunks identical to listed: True | (CRLF,LF) N7 (0, 62) N8 (0, 65)
matched_registry.py: fenced blocks 14, hunks 14, +46/-26 lines | patch(N7)==N8 bytes: True | my difflib(n=1) hunks identical to listed: True | (CRLF,LF) N7 (0, 228) N8 (0, 248)
matched_worker.py: fenced blocks 20, hunks 20, +111/-66 lines | patch(N7)==N8 bytes: True | my difflib(n=1) hunks identical to listed: True | (CRLF,LF) N7 (0, 342) N8 (0, 387)
MATCHED_OWNER_RUN.ps1: fenced blocks 10, hunks 10, +31/-15 lines | patch(N7)==N8 bytes: True | my difflib(n=1) hunks identical to listed: True | (CRLF,LF) N7 (0, 110) N8 (0, 126)
AUTHORIZATION.json: fenced blocks 1, hunks 1, +1/-1 lines | patch(N7)==N8 bytes: True | my difflib(n=1) hunks identical to listed: True | (CRLF,LF) N7 (0, 5) N8 (0, 5)
README.md: fenced blocks 3, hunks 3, +15/-16 lines | patch(N7)==N8 bytes: True | my difflib(n=1) hunks identical to listed: True | (CRLF,LF) N7 (0, 26) N8 (0, 25)
numbered notes: 61 | consecutive 1..N: True | total hunks: 61
notes citing no protocol section, brief, gate review or owner decision:
  50. [MATCHED_OWNER_RUN.ps1] Names N8.
  58. [AUTHORIZATION.json] Names N8; still disabled.
  60. [README.md] Lists N8's changed, new, dropped and byte-copied files.
```

The two registries shown as "ABSENT in clone" are published under `preregistration/…/seed-registry/REGISTRY.json` with the bound hashes (`bee57882…`, `0e8b0528…`). `LR_SELECTION.json` is not in the repository (B8c).

### `b2_power.py` (post hoc): the power argument, NumPy only; uses N7's published per-draw values and no N8 data

```
check of my t quantiles: t(.975,5) = 2.570582 (2.570582), t(.975,23) = 2.068658 (2.068658), t(.975,7) = 2.364624 (2.364624)
N7 P1: n=6 mean=+0.009088 sd=0.004845 interval=[+0.004004, +0.014172]  half effect=+0.004544  d(full)=1.8759  d(half)=0.9379
N7 S3: n=6 mean=-0.004542 sd=0.003245 interval=[-0.007947, -0.001137]  half effect=-0.002271  d(full)=1.3999  d(half)=0.6999

protocol's planning values: H1 d = 0.9361, H2 d = 0.7006
draws | H1 exact (MC) | H2 exact (MC) | Bonferroni lower bound | protocol table
   12 | 0.8389 (0.8388) | 0.5997 (0.6001) | 0.4386 | (0.84, 0.6, 0.44)
   16 | 0.9377 (0.9373) | 0.7453 (0.7451) | 0.6830 | (0.94, 0.74, 0.68)
   20 | 0.9776 (0.9781) | 0.8441 (0.8440) | 0.8217 | (0.98, 0.84, 0.82)
   21 | 0.9828 (0.9828) | 0.8628 (0.8623) | 0.8457 | 
   22 | 0.9869 (0.9872) | 0.8795 (0.8798) | 0.8664 | 
   23 | 0.9900 (0.9900) | 0.8944 (0.8944) | 0.8844 | 
   24 | 0.9924 (0.9925) | 0.9076 (0.9074) | 0.9000 | (0.99, 0.91, 0.9)

same table with the unrounded N7 values (H1 d = 0.9379, H2 d = 0.6999):
   12 | 0.8403 | 0.5988 | 0.4392
   16 | 0.9385 | 0.7445 | 0.6830
   20 | 0.9780 | 0.8434 | 0.8215
   24 | 0.9926 | 0.9070 | 0.8996
    8 draws, full unrounded effects: H1 0.9943  H2 0.9220  lower bound 0.9163
   24 draws, two-thirds effects, SDs x 1.5, unrounded: H1 0.9743  H2 0.8311  lower bound 0.8055

full N7 effects (protocol: 8 draws give joint power of at least 0.92):
  n=6: H1 0.9509  H2 0.7820  lower bound 0.7330
  n=7: H1 0.9826  H2 0.8679  lower bound 0.8505
  n=8: H1 0.9942  H2 0.9225  lower bound 0.9166
two-thirds of N7 effects, SDs x 1.5 (protocol: 24 draws give a lower bound of 0.81):
  n=20: H1 0.9415  H2 0.7524  lower bound 0.6939
  n=24: H1 0.9739  H2 0.8318  lower bound 0.8057

not in the protocol, for context (same rule, 24 and 20 draws):
  half effects, SDs x 1.5      n=24: H1 0.833  H2 0.592  lower bound 0.425  product (if independent) 0.493
  half effects, SDs x 1.5      n=20: H1 0.754  H2 0.509  lower bound 0.263  product (if independent) 0.384
  half effects, SDs x 2        n=24: H1 0.594  H2 0.376  lower bound 0.000  product (if independent) 0.223
  half effects, SDs x 2        n=20: H1 0.511  H2 0.318  lower bound 0.000  product (if independent) 0.163
  one-third effects, N7 SDs    n=24: H1 0.833  H2 0.592  lower bound 0.425  product (if independent) 0.493
  one-third effects, N7 SDs    n=20: H1 0.754  H2 0.509  lower bound 0.263  product (if independent) 0.384

95% interval for a true SD given an SD s estimated from 6 draws (normal draws): [0.624 s, 2.453 s]
simulated P(both CONFIRMED | H1 effect = 0, H2 effect = -5 SD), n = 24: 0.0249  (bound 0.025)
envelope: over 200 random boxes (3-8 draws), largest (vertex minimum of the lower limit minus the lowest of 20,000 sampled interior points): -7.093e-03 (<= 0 means no interior point was lower than the best vertex)
```

### `b3_registry.py` (post hoc): `HASHES.json`, seed registry, partition, fresh-pool count, pins, seals, pilot log

52 of 52 checks passed. The three "pre-pin -> sealed" entries are my summaries of the diff lines the script printed; everything else is exact, and the full text is in `b3_registry.out`.

```
PASS  HASHES.json: 17 single-file hashes equal the published files  [[]]
PASS  HASHES.json: grouped file hashes equal the published files, except those listed  [differ: [('tools/build_n8_activation.py', 'c31fd4aa')]; named but not published: ['tests-retired/test_draw_command.py']]
      HASHES.json keys ending _sha256 with no published file checked above: ['draw_command_sha256', 'corpus_manifest_sha256', 'n7_partition_sha256']
      published files bound neither by HASHES.json nor by SOURCE_SUBJECT.json: ['.gitattributes', 'HASHES.json', 'OPERATIONAL_NOTES.md', 'README.md', 'RUN_COMMAND.ps1', 'X2_COMMAND.txt', 'check_run.py', 'source/AUTHORIZATION.json']
PASS  DRAW.json: 1,024 bytes of entropy
PASS  my re-derivation of the 98 role values from DRAW.json and EXCLUSIONS.json equals REGISTRY.json  [candidates used up to index 97; rejected before that: 0]
PASS  98 distinct values, each more than 2,048 from every exclusion and from each other  [nearest exclusion 37913, nearest other role 112876; the check record says 37913 and 112876]
PASS  registry decisions list equals my accept/reject sequence
PASS  registry binds its own draw, exclusions, policy and partition
PASS  exclusions: 4,370 values, sorted, unique; provenance union_values agrees
PASS  the pilot's five seeds are all in EXCLUSIONS.json  [{'adapt_order_seed': 90809628, 'benchmark_seed': 578352808, 'init_seed': 1188503724, 'pretrain_order_seed': 46458185, 'weight_seed': 1894175819}]
PASS  N7: every role value (26), every census-rule value of its REGISTRY.json (26) and its exclusion list (4316) are in N8's exclusions  [registry sha bee57882; nearest N8 role value to one of its values: 3876906]
PASS  N6: every role value (26), every census-rule value of its REGISTRY.json (26) and its exclusion list (not published) are in N8's exclusions  [registry sha 0e8b0528; nearest N8 role value to one of its values: 618034]
PASS  capacity-shift-followup-seed-registry-20261027-01: every role value (0), every census-rule value of its REGISTRY.json (61) and its exclusion list (4046) are in N8's exclusions  [registry sha 00f3ab61; nearest N8 role value to one of its values: 37913]
PASS  natural-text-fewepoch-seed-registry-20261101-01: every role value (46), every census-rule value of its REGISTRY.json (46) and its exclusion list (4236) are in N8's exclusions  [registry sha 75db913d; nearest N8 role value to one of its values: 88404]
PASS  natural-text-ladder-seed-registry-20261028-01: every role value (46), every census-rule value of its REGISTRY.json (46) and its exclusion list (4158) are in N8's exclusions  [registry sha 8ce7d597; nearest N8 role value to one of its values: 540657]
PASS  natural-text-lateturn-seed-registry-20261031-01: every role value (18), every census-rule value of its REGISTRY.json (18) and its exclusion list (4209) are in N8's exclusions  [registry sha b9b6a882; nearest N8 role value to one of its values: 2983161]
PASS  N8's registry pins N7's registry and partition as published
PASS  claim and registry: registry-source hashes equal the sealed source files (13 files)
PASS  receipt: registry, partition, draw script and disclosure script hashes
PASS  receipt: the draw ran on the pending seal kept in seal/pre-pin  [2026-11-14 01:09:29]
PASS  post-draw check record: 16 checks, all ok
PASS  partition: 24 groups n01-n24 in order, n = 16,384
PASS  each group: exactly 16,384 distinct sequences
PASS  groups are disjoint by sequence (393,216 distinct) and by article  [9500 articles in all; left over 4539; sum 14039]
      partition pool record: {'assigned_articles': 13511, 'eligible_articles': 27859, 'fresh_articles': 14039, 'fresh_sequences': 582603, 'removed_repeats_inside_the_pool': 215, 'removed_text_duplicates_of_assigned': 94, 'sets_of_repeats_inside_the_pool': 107, 'unused_articles': 14348}
PASS  articles used + left over = 14,039 fresh articles
PASS  no N8 article or sequence is in N7's published partition  [N7: 2412 articles, 98304 sequences, left over 14039]
      N6: no PARTITION.json published; not checked
PASS  N7's left-over articles (14,039) equal N8's fresh pool size
PASS  DISCLOSURE_FIGURES.md: articles and sequences per draw equal the partition
PASS  check record: articles and sequences per draw equal the partition
PASS  each group's sequences form at most as many consecutive runs as it has articles  [runs 361-418]
PASS  fresh pool: count file = registry record = 14,039 articles and 582,603 sequences
PASS  24 x 16,384 = 393,216; + 24 x (328 - 1) = 401,064 <= 582,603
PASS  count: assigned 13,511 = 11,099 (N5, N6) + 2,412 (N7); N7 pool 16,451 - 2,412 = 14,039
PASS  N7's published partition holds 2,412 articles in m01-m06  [2412]
PASS  count tool hash and source hashes agree with HASHES.json and the sealed source
PASS  matched_plan.py pins: policy, registry, exclusions, draw, partition
PASS  matched_registry.py POLICY_SHA256 and N7_REGISTRY_SHA256; matched_data.py N7_PARTITION_SHA256
PASS  builder (v2.1): EXPECTED_SUBJECT, and PUBLIC_REGISTRATION subject and pilot-log hash
      N8-protocol-draft.md: 5 hash prefixes quoted; not matching any hash I can compute from published files: []
      README.md: 6 hash prefixes quoted; not matching any hash I can compute from published files: []
      source/README.md: 2 hash prefixes quoted; not matching any hash I can compute from published files: []
      CHANGES.md: 2 hash prefixes quoted; not matching any hash I can compute from published files: []
      files whose hash differs, pilot subject -> pending seal : ['MATCHED_OWNER_RUN.ps1', 'README.md', 'matched_plan.py', 'matched_registry.py']
      files whose hash differs, pending seal -> sealed subject: ['MATCHED_OWNER_RUN.ps1', 'README.md', 'matched_plan.py']
      files whose hash differs, pilot subject -> sealed subject: ['MATCHED_OWNER_RUN.ps1', 'README.md', 'matched_plan.py', 'matched_registry.py']
PASS  pending seal -> sealed: exactly matched_plan.py, README.md and MATCHED_OWNER_RUN.ps1
PASS  pilot subject -> sealed: exactly matched_plan.py, matched_registry.py, MATCHED_OWNER_RUN.ps1 and README.md (as the README says)
PASS  the pre-pin copies are the files the pending seal lists
PASS  the pilot log names the pilot subject and the pilot tool
      --- pre-pin -> sealed: matched_plan.py       [summary: 5 lines; registry_sha256, exclusions_sha256, draw_sha256, approval_id and PARTITION_SHA256 go from None to their values]
      --- pre-pin -> sealed: README.md             [summary: 2 lines; "This package has not run…" and "SEALED_DISABLED…"]
      --- pre-pin -> sealed: MATCHED_OWNER_RUN.ps1 [summary: 2 lines; $hours='about 2.1' -> 'about 2.3 h wall time (2.1 h on the worker clock)', and the start message]
      SOURCE_SUBJECT pins_pending: pilot True, pre-pin True, sealed False
      SOURCE_SUBJECT status: pilot 'SEALED_DISABLED', pre-pin 'SEALED_DISABLED', sealed 'SEALED_DISABLED'
      SOURCE_SUBJECT has_run: pilot False, pre-pin False, sealed False
      SOURCE_SUBJECT runtime_authorized: pilot False, pre-pin False, sealed False
PASS  pilot log vs protocol section 7: benchmark 43.6 s (22.0 + 21.6)
PASS  pilot log vs protocol section 7: per draw 2,528 s = 42.1 min, cap 3,097 s
PASS  pilot log vs protocol section 7: width 512: 867 s; 55 / 242 / 570
PASS  pilot log vs protocol section 7: width 768: 1,660 s; 101 / 462 / 1,097
PASS  pilot log vs protocol section 7: evaluation about two thirds
PASS  pilot log vs protocol section 7: run of three: 7,629 s measured, 7,186 s projected; both under 21,600 s
PASS  pilot log vs protocol section 7: PyTorch reserved at most 1.42 GiB
PASS  pilot log vs protocol section 7: eight runs: about 17 h on the worker clock
PASS  pilot log vs protocol section 7: 28 readouts per record; 12 files; orders 524,288 bytes = 4 epochs x 16,384 x 8
PASS  pilot log vs protocol section 7: status PASS, real, no loss read, no p* fitted, run folder deleted
PASS  pilot log vs protocol section 7: the pilot's draw is N7's m01, none of it in N8's fresh pool
      evaluation share 0.682; device-wide GPU memory sampled by the guard, peak 2,386,349,260 bytes = 2.222 GiB; guard limit 2.5 GiB = 2,684,354,560; headroom 284 MiB
      kept E0 states: (67,497,092 + 138,986,628) x 24 = 4,955,609,280 bytes = 4.62 GiB (protocol: about 4.6 GiB)

52 of 52 checks passed
```

### `b4_n7_loo.py` (post hoc, descriptive, N7's published `MATCHED.csv`)

```
S3: all six: -0.004542 [-0.007947, -0.001137]
   without m01: -0.004870 [-0.009234, -0.000506]  includes 0: False
   without m02: -0.005423 [-0.008787, -0.002059]  includes 0: False
   without m03: -0.004173 [-0.008498, +0.000153]  includes 0: True
   without m04: -0.004884 [-0.009235, -0.000533]  includes 0: False
   without m05: -0.004318 [-0.008758, +0.000121]  includes 0: True
   without m06: -0.003584 [-0.006693, -0.000474]  includes 0: False
P1: all six: +0.009088 [+0.004004, +0.014172]
   without m01: +0.008564 [+0.002079, +0.015050]  includes 0: False
   without m02: +0.008859 [+0.002179, +0.015540]  includes 0: False
   without m03: +0.009272 [+0.002576, +0.015968]  includes 0: False
   without m04: +0.008098 [+0.002276, +0.013921]  includes 0: False
   without m05: +0.008832 [+0.002163, +0.015501]  includes 0: False
   without m06: +0.010901 [+0.008217, +0.013586]  includes 0: False
P1 read_at_readout (epochs): [2.249, 2.39, 2.302, 2.189, 2.231, 2.476] -> N8 path covers epochs 2.0 to 3.5
```

## 5. Commands that matter, with exact output

Run in `C:\Users\rafli\AppData\Local\Temp\swa21\b\repo`; `D` = `preregistration/natural-text-dense-replication-20261114`.

**The builder at the registration tag against `v2.1`** (`git diff n8-registration v2.1 -- $D/tools/build_n8_activation.py`; the only hunk):

```
@@ -27,8 +27,8 @@ from pathlib import Path
 ROOT = Path(r'D:\sequence-weighting-research')          # the closed record: earlier registries and the corpus, read only
 STUDY = Path(r'D:\sequence-weighting-n8')
 SOURCE = STUDY / 'source'
-EXPECTED_SUBJECT = None                                  # PENDING: the sealed subject, set when the source is sealed (step 6)
-PUBLIC_REGISTRATION = None                               # PENDING: dict(url, merge_commit, tag, source_subject_sha256, pilot_log_sha256), after the merge
+EXPECTED_SUBJECT = '9bdea3a9715b05393afe6713ddc696834dd344c3485c4e1a6ed0fa222f44bb6b'   # the sealed subject, recorded by registration/apply_registration.py
+PUBLIC_REGISTRATION = {'url': 'https://github.com/rafli-hl/sequence-weighting/pull/1', 'merge_commit': 'c6f98b26669f5d29f30c576b6d800c1fc82c98eb', 'tag': 'n8-registration', 'source_subject_sha256': '9bdea3a9715b05393afe6713ddc696834dd344c3485c4e1a6ed0fa222f44bb6b', 'pilot_log_sha256': '251d0951e30250afa16cb998b06550358c09234d8a24c45166b08d0642347db6', 'pr_record_sha256': 'e8d92b7ec779ca63015ea857500ab887dd3d89611680e3fa8d4e5aa11e36f381'}   # recorded by registration/apply_registration.py
 PILOT_LOG = STUDY / 'pilot' / 'PILOT_LOG.json'
```

**Builder hashes** (`git show <ref>:$D/tools/build_n8_activation.py | sha256sum` for `n8-registration`, `v2.0`, `v2.1`):

```
30765693bd8bb4929ba060c193a610ecc987413d0c83b8035c6a9044228471d3 *-
c31fd4aa32873a1d025621f06bcc66e289c16ad86f64612c00dad76b1fd62904 *-
c31fd4aa32873a1d025621f06bcc66e289c16ad86f64612c00dad76b1fd62904 *-
```

**The folder across commits** (`git ls-tree -r --name-only <ref> -- $D | wc -l`, `git rev-parse <ref>:$D`, `git diff --name-status`):

```
aaafa2e: 74 files; tree aef1502c3be2c342cf9b2558514a0e17220b48e1
n8-registration: 74 files; tree aef1502c3be2c342cf9b2558514a0e17220b48e1
v2.0: 74 files; tree a1caf8f9deec0cbe35b65ca1bf8d24159b298cde
v2.1: 78 files; tree b55841f249d82bf983f3cc2150c1980688bf4d99
--- c6f98b2 vs v2.0 (folder):
M	preregistration/natural-text-dense-replication-20261114/README.md
M	preregistration/natural-text-dense-replication-20261114/tools/build_n8_activation.py
--- v2.0 vs v2.1 (folder):
A	preregistration/natural-text-dense-replication-20261114/OPERATIONAL_NOTES.md
M	preregistration/natural-text-dense-replication-20261114/README.md
A	preregistration/natural-text-dense-replication-20261114/RUN_COMMAND.ps1
A	preregistration/natural-text-dense-replication-20261114/X2_COMMAND.txt
A	preregistration/natural-text-dense-replication-20261114/check_run.py
```

`git diff c6f98b2 v2.1 -- $D/README.md | grep -E "^-[^-]"` shows one removed line: the "Not included, by design" paragraph, replaced by the same paragraph with two sentences added.

**The README note of B6:**

```
v2.0 README mentions 'two empty folders': 0
c1a2380 README mentions: 1
v2.1: 1
```

**Tags, commit times and GitHub (read-only GET requests):**

```
refs/tags/n8-registration commit c6f98b26669f5d29f30c576b6d800c1fc82c98eb  2026-11-15T01:19:19+07:00
refs/tags/v1.2 commit c4ae0e143526214b97d9740ee911997b45076413  2026-11-12T17:13:56+07:00
refs/tags/v2.0 commit 88ac49683770b147ee580285d640fcde517d36c3  2026-11-15T01:44:07+07:00
refs/tags/v2.1 commit 30548dbb789b2a117486fdf6f9ab9added680172  2026-11-23T12:09:20+07:00
{"base":"main","changed_files":81,"commits":1,"created_at":"2026-11-14T18:17:44Z","head":"aaafa2ed180c3c5c4c136f16fc3e7ef9a9515126","merge_commit_sha":"c6f98b26669f5d29f30c576b6d800c1fc82c98eb","merged":true,"merged_at":"2026-11-14T18:19:20Z","number":1,"state":"closed","title":"Register N8: dense-readout replication of N7"}
{"committer":"GitHub","date":"2026-11-14T18:19:19Z","reason":"valid","sha":"c6f98b26669f5d29f30c576b6d800c1fc82c98eb","verified":true,"verified_at":"2026-11-14T18:19:20Z"}
{"assets":[],"created_at":"2026-11-23T05:09:20Z","name":"v2.1","published_at":"2026-11-23T05:10:47Z","tag_name":"v2.1","target_commitish":"main"}
{"assets":[],"created_at":"2026-11-14T18:44:07Z","name":"v2.0","published_at":"2026-11-14T18:45:38Z","tag_name":"v2.0","target_commitish":"main"}
{"assets":[{"name":"n7-loss-arrays-v1.zip","size":14577377}],"created_at":"2026-11-12T10:13:56Z","name":"v1.2","published_at":"2026-11-12T10:25:53Z","tag_name":"v1.2","target_commitish":"main"}
```

**Search behind B1** (`grep -n -E "RECEIPT|TERMINAL|n8-r|runs/|runs\\\\|def load|__main__|argparse|sys.argv" analysis/*.py`, run in the N8 folder):

```
analysis/regenerate_n7_orders.py:37:if __name__ == '__main__':
analysis/regenerate_n7_orders.py:38:    if len(sys.argv) != 3: raise SystemExit(__doc__)
analysis/regenerate_n7_orders.py:39:    main(Path(sys.argv[1]), Path(sys.argv[2]))
analysis/test_on_n7.py:243:if __name__ == '__main__':
analysis/test_on_n7.py:244:    if len(sys.argv) != 4: raise SystemExit(__doc__)
analysis/test_on_n7.py:245:    raise SystemExit(main(Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])))
analysis/test_synthetic.py:212:if __name__ == '__main__':
```

**Searches behind B4** (summarised, not verbatim output):
- `git grep -n -I "e8d92b7e"` and `git grep -n -I "pr_record"` each match only `$D/tools/build_n8_activation.py:31`.
- `git grep -n -I "apply_registration"` matches `$D/tools/build_n8_activation.py:30` and `:31`, and one unrelated line, `preregistration/natural-text-matched-confirmation-20261104/HASHES.json:32`.

**Not done.** I did not run `verify_publication.py`, `write_hashes.py --check`, the analysis tests or any repository code (left to the supervising session). I opened nothing outside the clone, the scratch folder and the brief, changed nothing in the clone, and computed nothing from N8 data.