
## 5. Commands that matter, with their output

All run in the clone `C:\Users\rafli\AppData\Local\Temp\swa21\d\repo` (Git Bash), read-only.

**History and tags** (`git log --all --date=iso-strict --format='%h %p | A:%ad | C:%cd | %an / %cn | %G? | %s'`):

```
30548db c1a2380 | A:2026-11-23T12:09:20+07:00 | C:2026-11-23T12:09:20+07:00 | rafli-hl / rafli-hl | N | Version 2.1: N8 paused
c1a2380 88ac496 | A:2026-11-23T12:05:02+07:00 | C:2026-11-23T12:05:02+07:00 | rafli-hl / rafli-hl | N | N8 paused after 6 of 24 draws
88ac496 c6f98b2 | A:2026-11-15T01:44:07+07:00 | C:2026-11-15T01:44:07+07:00 | rafli-hl / rafli-hl | N | Version 2.0: N8 registration notes and recorded builder
c6f98b2 fee55ea aaafa2e | A:2026-11-15T01:19:19+07:00 | C:2026-11-15T01:19:19+07:00 | rafli-hl / GitHub | E | Merge pull request #1 from rafli-hl/n8-registration
aaafa2e fee55ea | A:2026-11-15T01:17:02+07:00 | C:2026-11-15T01:17:02+07:00 | rafli-hl / rafli-hl | N | Register N8: dense-readout replication of N7
fee55ea 320359b | A:2026-11-13T12:54:48+07:00 | C:2026-11-13T12:54:48+07:00 | rafli-hl / rafli-hl | N | Revise README and add METHODS.md (documentation only; no result changed
320359b c4ae0e1 | A:2026-11-13T01:32:39+07:00 | C:2026-11-13T01:32:39+07:00 | rafli-hl / GitHub | E | Add files via upload
c4ae0e1  | A:2026-11-12T17:13:56+07:00 | C:2026-11-12T17:13:56+07:00 | rafli-hl / rafli-hl | N | Research record, version 1.2
```

(`E` means the signature could not be checked locally for want of the key; the supervising session checks it through the API.) `git cat-file -t` of `refs/tags/n8-registration`, `v2.0`, `v2.1` and `v1.2` gives `commit` for each: all four tags are lightweight.

**GitHub, server-side times** (`gh api repos/rafli-hl/sequence-weighting/pulls/1 --jq '{…}'`):

```
{"base_ref":"main","changed_files":81,"closed_at":"2026-11-14T18:19:20Z","commits":1,"created_at":"2026-11-14T18:17:44Z","head_ref":"n8-registration","head_sha":"aaafa2ed180c3c5c4c136f16fc3e7ef9a9515126","merge_commit_sha":"c6f98b26669f5d29f30c576b6d800c1fc82c98eb","merged":true,"merged_at":"2026-11-14T18:19:20Z","merged_by":"rafli-hl","number":1,"state":"closed"}
```

`gh api 'repos/rafli-hl/sequence-weighting/activity?per_page=100' --jq '.[] | {ref, activity_type, timestamp, before: .before[0:7], after: .after[0:7], actor: .actor.login}'`:

```
{"activity_type":"push","actor":"rafli-hl","after":"30548db","before":"c1a2380","ref":"refs/heads/main","timestamp":"2026-11-23T05:09:33Z"}
{"activity_type":"push","actor":"rafli-hl","after":"c1a2380","before":"88ac496","ref":"refs/heads/main","timestamp":"2026-11-23T05:05:16Z"}
{"activity_type":"push","actor":"rafli-hl","after":"88ac496","before":"c6f98b2","ref":"refs/heads/main","timestamp":"2026-11-14T18:44:16Z"}
{"activity_type":"branch_deletion","actor":"rafli-hl","after":"0000000","before":"aaafa2e","ref":"refs/heads/n8-registration","timestamp":"2026-11-14T18:36:37Z"}
{"activity_type":"pr_merge","actor":"rafli-hl","after":"c6f98b2","before":"fee55ea","ref":"refs/heads/main","timestamp":"2026-11-14T18:19:20Z"}
{"activity_type":"branch_creation","actor":"rafli-hl","after":"aaafa2e","before":"0000000","ref":"refs/heads/n8-registration","timestamp":"2026-11-14T18:17:18Z"}
{"activity_type":"push","actor":"rafli-hl","after":"fee55ea","before":"320359b","ref":"refs/heads/main","timestamp":"2026-11-13T05:56:18Z"}
{"activity_type":"push","actor":"rafli-hl","after":"320359b","before":"c4ae0e1","ref":"refs/heads/main","timestamp":"2026-11-12T18:32:41Z"}
{"activity_type":"force_push","actor":"rafli-hl","after":"c4ae0e1","before":"a5c4a00","ref":"refs/heads/main","timestamp":"2026-11-12T10:17:29Z"}
{"activity_type":"branch_creation","actor":"rafli-hl","after":"a5c4a00","before":"0000000","ref":"refs/heads/main","timestamp":"2026-11-09T09:26:06Z"}
```

Branches, releases, artifacts, tag (`gh api` GET):

```
== branches
{"name":"main","sha":"30548dbb789b2a117486fdf6f9ab9added680172"}
== releases
{"assets":[],"created_at":"2026-11-23T05:09:20Z","name":"v2.1","published_at":"2026-11-23T05:10:47Z","tag_name":"v2.1","target_commitish":"main"}
{"assets":[],"created_at":"2026-11-14T18:44:07Z","name":"v2.0","published_at":"2026-11-14T18:45:38Z","tag_name":"v2.0","target_commitish":"main"}
{"assets":[{"created_at":"2026-11-12T10:25:50Z","name":"n7-loss-arrays-v1.zip","size":14577377}],"created_at":"2026-11-12T10:13:56Z","name":"v1.2","published_at":"2026-11-12T10:25:53Z","tag_name":"v1.2","target_commitish":"main"}
== actions artifacts
{"names":[],"total_count":0}
== git/ref/tags/n8-registration
{"ref":"refs/tags/n8-registration","sha":"c6f98b26669f5d29f30c576b6d800c1fc82c98eb","type":"commit"}
== releases/tags/n8-registration
{"message":"Not Found", … "status":"404"}
== wiki: git ls-remote https://github.com/rafli-hl/sequence-weighting.wiki.git
remote: Repository not found.
```

**What changed in the N8 folder since registration** (`git diff --name-status c6f98b2 30548db -- preregistration/natural-text-dense-replication-20261114`):

```
A	preregistration/natural-text-dense-replication-20261114/OPERATIONAL_NOTES.md
M	preregistration/natural-text-dense-replication-20261114/README.md
A	preregistration/natural-text-dense-replication-20261114/RUN_COMMAND.ps1
A	preregistration/natural-text-dense-replication-20261114/X2_COMMAND.txt
A	preregistration/natural-text-dense-replication-20261114/check_run.py
M	preregistration/natural-text-dense-replication-20261114/tools/build_n8_activation.py
```

The builder at registration (`git diff c6f98b2 88ac496 -- …/tools/build_n8_activation.py`, the two changed lines, cut at 100 characters):

```
-EXPECTED_SUBJECT = None                                  # PENDING: the sealed subject, set when the source is se
-PUBLIC_REGISTRATION = None                               # PENDING: dict(url, merge_commit, tag, source_subject_s
+EXPECTED_SUBJECT = '9bdea3a9715b05393afe6713ddc696834dd344c3485c4e1a6ed0fa222f44bb6b'   # the sealed subject, re
+PUBLIC_REGISTRATION = {'url': 'https://github.com/rafli-hl/sequence-weighting/pull/1', 'merge_commit': 'c6f98b26
```

`git show c6f98b2:…/tools/build_n8_activation.py | sha256sum` → `30765693bd8bb4929ba060c193a610ecc987413d0c83b8035c6a9044228471d3`, the hash `HASHES.json` names.

**The same-day revision of the notes** (`git diff c1a2380 30548db -- …/OPERATIONAL_NOTES.md`, the changed lines):

```
-X2's row comes from file sizes, the terminal and the n06 receipt. `check_run.py X2`, which also reads every data file to hash it, had not been run by 23 November 2026.
+`check_run.py X2`, run on 23 November 2026, confirms X2's row (Events, 16 November).
+  - `check_run.py X2` (run on 23 November 2026): 31 passed, 1 failed, the failure being the known gap above.
+    - n06 passes every check of a complete draw, its arrays' hashes, layout and finiteness included.
+    - Against R2: X2's copy of R2's terminal is byte for byte the one R2 wrote, and n06 has the same seeds and saved orders as R2's n06 (orders `19c09770…`).
+    - The receipt's E0 comparison recomputes exactly from the arrays' SHA-256.
```

and of the README's table row (`git diff c1a2380 30548db -- …/README.md`):

```
-| [`OPERATIONAL_NOTES.md`](OPERATIONAL_NOTES.md) | Dated operational events of the runs (R1, R2, X2), known gaps and precautions, copied from the study folder. It names the owner's run commands and the completeness check, `check_run.py`, which are not published |
+| [`OPERATIONAL_NOTES.md`](OPERATIONAL_NOTES.md) | Dated operational events of the runs (R1, R2, X2), known gaps and precautions, copied from the study folder |
```

`git diff 88ac496 c1a2380 -- …/README.md` adds the line beginning `+- **15 November 2026, operational: two empty folders before R1.**`; it is not in the README at 88ac496 (v2.0). `grep -n "c1a2380" PUBLICATION_NOTES.md` prints nothing.

**No N8 run output in the tree** (`git ls-tree -r --name-only HEAD | grep -i -E "n8-[rx][0-9]|/n[0-9]{2}/|/n[0-9]{2}-RECEIPT|TERMINAL\.json|arrays\.f32|E0\.f32|record\.json|PRETRAINED|OWNER_EXIT|\.f32$|\.i64$|\.pt$|\.npy$|\.npz$" | grep -v -E "^work/|^outputs/|^reports/|preregistration/natural-text-(matched|peak)"`): no output. `grep -rIn -E "n8-r[0-9]|n8-x[0-9]|sequence-weighting-n8"` outside the N8 folder: no output.

**No reason for the pause on any living page** (`grep -n -i "pause\|resum" README.md CURRENT_CLAIMS.md METHODS.md NATURAL_TEXT_STUDIES.md DATA_AVAILABILITY.md PUBLICATION_NOTES.md CITATION.cff reports/README.md reports/natural-text-correction-20261123-01/CORRECTION.md`, cut at 110 characters):

```
README.md:8:N7: its protocol and sealed source were registered publicly before any of its runs. Its training was paused on
README.md:17:**N8, paused on 23 November 2026.**
README.md:20:- Resuming continues with R3 under the registered protocol. If fewer than 20 draws are ever completed, the regi
CURRENT_CLAIMS.md:223:That is not a restriction on anyone else. N8's training was paused on 23 November 2026 after 6 of its 2
CURRENT_CLAIMS.md:225:examined. Resuming continues with R3 under the registered protocol; if fewer than 20 draws are ever comp
NATURAL_TEXT_STUDIES.md:191:**N8, paused on 23 November 2026.**
NATURAL_TEXT_STUDIES.md:194:- Resuming continues with R3 under the registered protocol. If fewer than 20 draws are ever comple
PUBLICATION_NOTES.md:29:## 23 November 2026: version 2.1, N8 paused; corrections of 23 November
PUBLICATION_NOTES.md:44:    tokenizer result; N8's pause.
PUBLICATION_NOTES.md:47:  - `README.md`: N8's pause; a note under the sensitivity table; the familywise caveat; matched recency
PUBLICATION_NOTES.md:49:  - `NATURAL_TEXT_STUDIES.md`: the audit, the correction, matched recency windows and N8's pause. No livi
PUBLICATION_NOTES.md:52:- **N8 paused.** Training is paused on 23 November 2026 after 6 of 24 draws (n01–n06; n06 completed in
PUBLICATION_NOTES.md:56:  - Resuming continues with R3 under the registered protocol. If fewer than 20 draws are ever completed
PUBLICATION_NOTES.md:81:tagged `n8-registration`. It has no results yet; its runs and their pause are in the entry of 23 Novemb
```

**Pre-pin against sealed, line by line** (`diff` of `seal/pre-pin/<file>` and `source/<file>`): `matched_plan.py` differs in lines 32–36 only (four `None` pins and `PARTITION_SHA256 = None` become the drawn values); `MATCHED_OWNER_RUN.ps1` in lines 17 and 78 only (the hours text); `README.md` in lines 3 and 25 only (the two status lines).

**The clone is unchanged:** `git status --porcelain | wc -l` → `0`; `find . -name __pycache__ -not -path './.git/*' | wc -l` → `0`; `git rev-parse HEAD` → `30548dbb789b2a117486fdf6f9ab9added680172`.
