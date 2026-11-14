# Seed registry policy: dense-readout replication (N8) on fresh WikiText-103 draws

**Frozen:** 14 Nov 2026, before any seed of this study is drawn. The registry tool (`source/matched_registry.py` in the N8 study folder) pins this file's SHA-256 and refuses a draw if it differs. Adapted from N7's policy (`reports/natural-text-matched-seed-registry-20261104-01/SEED_REGISTRY_POLICY.md` in the closed record, SHA-256 `323b5ae4…`); the changes are listed below.

**Roles (98 values):**
- `partition_seed`;
- for each of the 24 fresh draws n01–n24: `init_seed`, `weight_seed`, `pretrain_order_seed`, `adapt_order_seed`;
- `benchmark_seed` (the start-up benchmark of every run, R1–R8 and X1–X8).

No tuning group: no new rate is chosen.

**Mechanics (N7's, unchanged):**
- one exclusive claim, then a single draw of 1,024 bytes of operating-system entropy, read as 256 little-endian uint32 candidates;
- deterministic ordered acceptance: a candidate is accepted if it is more than 2,048 away from every excluded value and from every value already accepted, until 98 are accepted; fewer than 98 stops the registry, with no redraw;
- the registry re-derives exactly from its own draw and exclusion bytes (`validate`).

**Which seeds are excluded:**
- every earlier registry's values and exclusion list: the v0128 lists, the capacity ladder, S, the natural-text ladder used by N1 and N3 and by their first attempts, N4, N5, N6 and N7;
- a census of saved JSON records in the closed record, which never enters a folder whose path holds `work/runs`, at any depth (the owner's rule of 4 Nov 2026);
- a census of saved JSON records in the N8 study folder. It must find the folder and read every JSON file it walks there, or the draw refuses before its claim. This census excludes the pilot's five seeds, which `pilot/PILOT_LOG.json` records (protocol section 4).

A census counts every integer from 0 to 2^32 − 1 that it finds under a key whose name contains "seed", "stream", "schedule" or "corpus".

**Changed from N7's policy:**
- 98 roles for n01–n24, in place of 26 for m01–m06;
- N7's registry is one more exclusion source, and N7's m01–m06 articles are out (below);
- the census also walks the N8 study folder, which must exist and be read in full.

**Bindings:**
- the draw requires the WikiText-103 corpus manifest, which must equal the few-epoch study's pin (`be911db7…`) and validate under the sealed corpus rules;
- it requires the few-epoch (N5), peak (N6) and N7 registries and partitions, which must equal their pins;
- it requires an owner approval id (OWNER-YYYYMMDD-..., never FIXTURE);
- the claim and the registry record the approval id and the hash of every registry-source file.

**Which articles are fresh** (`matched_data.fresh_pool`, sealed with this policy). Start from the eligible training articles, those the corpus manifest does not exclude:
1. **Assigned articles are out:** every article the few-epoch partition assigned to t00 or d01–d10, every article the peak partition assigned to c01–c06, and every article N7's partition assigned to m01–m06, including the ones behind unused sequences. They are re-derived with the sealed `fewepoch_data.partition`, `peak_data.partition` and N7's `matched_data.partition` (a byte copy, `n7_matched_data.py`), each against its pin.
2. **Text duplicates of assigned articles are out:** every remaining article whose full text (`text_sha256` in the manifest) equals that of an assigned article.
3. **Repeats inside the pool are out:** every copy of any text that occurs more than once among what remains, so no two fresh draws can share a full text.

The owner's count of 13 November (`data-count/FRESH_POOL_COUNT.json`) found 14,039 fresh articles and 582,603 sequences. 24 draws of 16,384 need 393,216 sequences, and 401,064 suffice whatever the shuffle.

N1, N3, N4 and the first attempts of N1 and N3 drew WikiText-2 articles, and the corpus manifest excludes every article equal by title or text to a WikiText-2 article. So none of them can contribute an article. S is synthetic. The pilot drew N7's m01, which rule 1 removes.

**Partition rule** (`matched_data.partition`, sealed with this policy):
- the fresh articles are sorted by index, then shuffled with `random.Random(partition_seed)`;
- they are assigned whole, in that order, to n01, ..., n24, each draw until it holds at least 16,384 sequences;
- each draw uses its first 16,384 sequences in assignment order.

The rule depends only on per-article sequence counts, text hashes and the four partition seeds, so it is outcome-blind.

**Written by the draw** in `registry/n8-seed-registry/`: `DRAW_CLAIM.json`, `EXCLUSIONS.json`, `DRAW.json`, `PARTITION.json` and `REGISTRY.json`, which records the partition's hash. The partition is written here so that it can be checked without opening `work/runs/`. The owner-run draw script then adds its post-draw checks (`REGISTRY_AND_PARTITION_CHECK.json`), the disclosure figures (`DISCLOSURE_FIGURES.md`) and its receipt (`SEED_DRAW_RECEIPT.json`).

**What this does not remove:** exact token sequences and 64-token runs that recur outside identical full texts, and articles that share a title with an assigned article but not its text. The validation set, the pre-training pool and the tokenizer stay those of the earlier natural-text studies.
