# Audit of record v2.1 (commit 30548db): areas A and E, with notes for F. Auditor A

Read-only audit of my clone at tag v2.1, the brief, and N7's public loss-array bundle. Every new calculation is **post hoc** and descriptive. No N8 result was estimated and no N8 data was read. GitHub and two public archives were queried with GET requests only.

## Summary

1. No registered number, label or N8 registration element was found wrong in areas A and E.
2. Every figure in the 23 November correction reproduces with code I wrote: F1's minima (+0.0000764, −0.0000507, −0.000268), F2's scale, F3's maxima (14.11545, 8.44744, 6.99420 updates; 0.00000, 0.03709, 0.03659) and F4's arms.
3. F3 was verified without PyTorch. I generated the batch orders myself (section 4, "How I obtained batch orders"); the 12 order files are byte-identical by SHA-256 to those pinned in N8's `HASHES.json`.
4. **F-a1 (Major by the brief's definition, "a check fails"; no number affected).** `test_on_n7.py`, which the correction cites as reproducing F1 and F3, pins an index file whose bytes include the PyTorch and NumPy version strings of the machine that wrote it (`2.7.0+cu126`, `2.2.6`). With the published install lines (`2.7.0+cpu`, `2.5.3`) the same orders give 59 passed, 1 failed, exit 1.
5. **A1 (Minor).** `CORRECTION.md` was edited in place four minutes after its first public commit; neither the file nor `PUBLICATION_NOTES.md` says so.
6. **E1–E4 (Minor).** Living pages are stale about N8. One sentence still says the experiments "are closed again", and `DATA_AVAILABILITY.md` has not changed since 13 November.
7. Version 2.1, the date 23 November 2026 and N8's status agree on every page that states them, and with GitHub's release record.

## 1. Findings

Paths are relative to the repository root at 30548db. "C" numbers refer to the commands in section 5, and script names to section 4.

| ID | Area | Severity | Finding | Evidence | Status | Fix type |
|---|---|---|---|---|---|---|
| A1 | A | Minor | The 23 November `CORRECTION.md` was revised in place after its first public commit, and this is not disclosed. c1a2380 was pushed on its own (the `verify` workflow ran on that push at 05:05:18Z) with the file at SHA-256 `05f5459c…`. 30548db, four minutes later, rewrote §3's "What changes" sentence and the closing "Living pages changed" list (`c043f501…`). The file has no amendment line. `PUBLICATION_NOTES.md` names c1a2380 nowhere and does not say the note was revised; its own 23 November entry was rewritten in place. The same step also changed `OPERATIONAL_NOTES.md` (from "`check_run.py X2` … had not been run by 23 November 2026" to its result), the N8 README, `README.md` and `NATURAL_TEXT_STUDIES.md`; the notes give only the final state. The record's precedent is to disclose: the 9 November correction says "**Amended 9 November 2026,** … Nothing else changed", and `PUBLICATION_NOTES.md:302` says "`CORRECTION.md` was amended in its local source and here". No number changed in the revision. | C1. Only trace, `PUBLICATION_NOTES.md:49–50`: 'No living page now says that the exposure-matched sets are matched "for the timing" of every pass.' Precedent: `reports/natural-text-correction-20261109-01/CORRECTION.md:5–6`. | VERIFIED | doc-only: a dated line in `PUBLICATION_NOTES.md` |
| A2 | A | Minor | The correction's general sentence is false for S4. `CORRECTION.md:27–29`: "Reading every draw at its later end gives the smallest mean contrast, but not the smallest lower t limit". `README.md:82`: "The later bracket end gives the lowest mean, not the lowest interval." `METHODS.md:222–224`: "Nor is it the least favourable reading for the interval: … −0.000268 for S4, against … −0.00027 with every draw at the later end." For S4 the all-later-end reading is the minimum over the 64 combinations (−0.0002679, all six draws at the later end). The two S4 figures set "against" each other are one number at two precisions. The sentence holds for P1 and S1 only. | `a1_envelope.py`, S4 block | VERIFIED | doc-only |
| A3 | A | Suggestion | F3's "0.000" at k = 1 is zero by construction: with one quarter per pass there is one joint cell. `CORRECTION.md:84` and `METHODS.md:181–182` list it beside 0.037 and 0.037 without saying so. The audit's balance figure at k = 1 was a marginal KS distance of 0.11920 (`AUDIT.md:61`), which reproduces (`a3d_ks.py`) and which the correction leaves out. N8's S-b `joint_cell_distance` at j = 1 will be 0 for the same reason. | `a3_recency.py`: "largest joint quarter-cell TV 0.00000 (… 1 cell)" | VERIFIED | doc-only; and a matter for N8's eventual result report |
| E1 | E | Minor | Stale status. `NATURAL_TEXT_STUDIES.md:149`: "The experiments were reopened for N7 alone and are closed again." Lines 187–197 of the same page, and every other page, say the record was reopened for N8 and that N8 is paused after 6 of 24 draws. `PUBLICATION_NOTES.md:116–117` says this page "no longer say[s] that no further runs will be added". | C2 | VERIFIED | doc-only |
| E2 | E | Minor | Stale page headers. `CURRENT_CLAIMS.md:3`: "**As of 12 November 2026; wording revised 13 November 2026, with no claim, number or label changed.**" C3's wording, three new numbers in C4's table and the training row changed on 23 November, and N8 paragraphs were added on 14 and 23 November. Its history paragraph (lines 7–18) ends at the 12 November correction. `NATURAL_TEXT_STUDIES.md:1` is titled "27 October – 11 November 2026" and its lines 3–5 end at 11 November; the page now runs to 23 November. | C2 | VERIFIED | doc-only |
| E3 | E | Minor | `DATA_AVAILABILITY.md` has not changed since 13 November and does not mention N8. Lines 9–10: "the public registrations of N6 and N7". Lines 13–14: "the audits of 8 and 12 November 2026, and the corrections of 9, 11 and 12 November 2026"; the 13 November audit and the 23 November correction are missing, although the notes of 13 November record that this list was then brought up to date. "What is not included" (lines 25–33) does not list N8's run folders, loss arrays or saved orders. Line 54, "the bundle holds no hash of them", is still true of the bundle, but N8's `HASHES.json` now pins hashes of N7's regenerated orders. | C2 | VERIFIED | doc-only |
| E4 | E | Minor | Other lists of registrations omit N8. `README.md:276`: "Only N7 was publicly preregistered", against `README.md:7–8`, where N8's "protocol and sealed source were registered publicly before any of its runs". `README.md:303`: "Public registrations of N6 and N7" for a folder that holds three. `METHODS.md:4`: "N7, the publicly preregistered study"; §1's table (lines 11–19) has no N8 row; `METHODS.md:23`: "the two public registrations". `NATURAL_TEXT_STUDIES.md:27`: "Two studies were also registered publicly"; its study table (lines 60–68) has no N8 row. | C2 | VERIFIED | doc-only |
| E5 | E | Minor | `README.md:271–272`, limitation 4: "The later-end readings are a sensitivity check, not a bound on the unobserved trajectory. S4's sign depends on this." S4's sign does not: its mean is above 0 in all 64 combinations (lowest +0.01043). What depends on the bracket end is whether its interval excludes 0. After F1 the same is true of S1 under one combination, which limitation 4 does not say. | `a1_envelope.py` | VERIFIED | doc-only |
| E6 | E | Minor | Overstated caption. `METHODS.md:362`: "**Figure 6.** Every estimate of the 512 − 768 contrast." The figure has 15 rows (`docs/make_readme_figures.py:170–190`; drawn 13 November). Estimates quoted on the living pages that it omits: S1 at the later bracket end (+0.00399 [+0.00099, +0.00699]), P1 with the E0 offset (+0.0062 [−0.0001, +0.0126]), P1 on the lower half of the weights (+0.0012 [−0.0009, +0.0032]), the better-rate contrast at the later end (+0.00518 [−0.00714, +0.01751]) and the 23 November envelope minima. | Image `docs/figures/estimates-light.png`, viewed | VERIFIED | doc-only (caption) |
| E7 | E | Suggestion | Dates mix clocks without saying so. N8's merge c6f98b2 is 2026-11-14T18:19:19Z (15 November, 01:19 +07:00) and is dated "14 November" (`README.md:11`, `reports/README.md:34`, `PUBLICATION_NOTES.md:99`). The v2.0 release, published 26 minutes later (2026-11-14T18:45:38Z), is dated "15 November 2026" (`PUBLICATION_NOTES.md:78`, `:95–96`). N8's run events are in local time. `NATURAL_TEXT_STUDIES.md:32–33` gives N6's and N7's merges in UTC. | C2 | VERIFIED | doc-only: give N8's merge time with its zone |
| F-a1 | F (bears on A and C) | Major by the brief's definition ("a check fails"); no number is affected | `test_on_n7.py` cannot pass for a reader who follows the published instructions. Its check at line 107 requires `sha(ORDERS.json) == ORDERS_SHA256` (`8ba4a3c2…`, also at `HASHES.json:142`). `regenerate_n7_orders.py` writes `torch.__version__` and `np.__version__` into that file. I rebuilt the pinned file byte for byte only with `2.7.0+cu126` and `2.2.6`, the protocol's WSL cross-check environment. The script's own usage line says "needs PyTorch (CPU)"; the README and the brief install the CPU build, which reports `2.7.0+cpu` (`AUDIT.md`: "ran with numpy 2.5.3, torch 2.7.0+cpu"), with NumPy 2.5.3. With identical order files and those two strings the test prints "FAIL  regenerated orders …" and "59 passed, 1 failed", exit 1; with the pinned strings, "60 passed, 0 failed", exit 0. The F1 and F3 checks pass in both runs. So the correction's "reproduced by `test_on_n7.py`" holds for the numbers, but "60 of 60" is reachable only on a machine that reports the registrant's version strings; a pass in the owner's WSL environment does not show that the public route passes. Limit of my evidence: I wrote the second `ORDERS.json` from the script's code and did not run the script under a CPU build of PyTorch. | `a3c_orders_json.py`, `a6_make_orders.py`, C3 | VERIFIED (mechanism and both runs); the CPU version string is taken from `AUDIT.md` | dated note stating the two strings, or publishing the order files (`inputs/n7-orders-v1/`); the registered test file is not to be edited |
| F-a2 | F (B, D) | Suggestion | N8's registration has no third-party archive. Software Heritage has no origin for the final repository and no revision c6f98b2; the Wayback CDX index has no capture of the repository page. For N6 and N7 the record cites both archives (`NATURAL_TEXT_STUDIES.md:31–51`). All four tags, `n8-registration` included, are lightweight: no tagger, date or signature. GitHub's signature on c6f98b2 is then the only independent evidence of when N8 was registered. | C2 | VERIFIED (Software Heritage, tags); PLAUSIBLE (Wayback: the query for PR #1's page timed out twice) | owner action, then doc-only |
| F-a3 | F (D) | Suggestion | No page says why training was paused, and the protocol has no provision for a pause (0 matches for "pause", "interrupt", "resum"). Section 8 fixes 24 draws. Section 6's status COMPLETE_WITH_FAILED_DRAWS covers 20–23 finished draws, where a failed draw is one that "fails in both attempts". The pages' sentence "If fewer than 20 draws are ever completed, the registered INCOMPLETE rule applies" is accurate, but leaves unsaid that a draw not yet attempted is not a failed draw, so stopping by choice at 20–23 is not a registered outcome. This is outside my assigned areas and is passed on. | C2; `N8-protocol-draft.md` §6 and §8 | VERIFIED (the texts) | doc-only: a dated note before R3 |

## 2. Rejected concerns: checked and found sound

**The correction (A).**
- **F1.** All nine intervals in the table reproduce from `POINTS.csv` and `MATCHED.csv`. Minima over the 64 combinations: P1 +0.0000764 (m01 at the earlier end), S1 −0.0000507 (m02 at the earlier end, as the correction says), S4 −0.0002679. P1's lower limit is above 0 in all 64; S1's is at or below 0 in exactly 1; S4's in 5. The later end gives the lowest mean for all three, because 768's p\* rises in every bracket. The concavity argument is correct, and 200,000 random interior readings per statistic gave no lower limit below the vertex minimum.
- **F2.** `gap_scale.py` runs, and its output with LF line endings has the SHA-256 of `GAP_SCALE.txt` (`13b41f3d…`). My own recomputation gives the same interval, range and four slopes. A second descriptive scale agrees in size: across the ten draws at epoch 2, the p\* difference moves with the gap difference at +0.215 per nat (r = +0.55), and its value at zero gap difference is −0.0093. "About a tenth" stands. No living page still says "the same gap" for C3.
- **F3.** The three maxima and three distances reproduce to five decimals, as do the audit's KS figures. Set sizes are 226–272, 2,018–2,116 and 6,883–6,931. The mean absolute age difference over the 18 draw-passes is 4.2, 3.2 and 2.0 updates, in windows 256, 512 and 768 updates wide. No living page says "for the timing" or "equally long ago".
- **F4.** N6's `POINTS.csv` has width 384 at 3e-4 only, and 512 and 768 at both rates, on six draws. Its protocol's arm table agrees.
- **Quotations and side statements.** The sentences quoted from the 9 and 12 November corrections and from the old `METHODS.md` are exact. The tokenizer statement matches the audit's output and the pin at `acquire_plan.py:37`. The familywise statement matches N7's protocol (line 74) and its `HASHES.json` (lines 37–41).
- **Files.** `AUDIT.md` has the SHA-256 its README states (`9678f6cc…`). From v2.0 to v2.1 only living pages were modified and nine files added; no sealed or historical file changed.

**Living pages (E).**
- **Version and date.** "2.1" at `README.md:13`, `README.md:329` and `CITATION.cff:11`; 23 November 2026 at `README.md:13` and `CITATION.cff:16`. GitHub published v2.1 at 2026-11-23T05:10:47Z on 30548db.
- **N8's status** reads the same in `README.md`, `CURRENT_CLAIMS.md`, `NATURAL_TEXT_STUDIES.md` (lines 187–197), `PUBLICATION_NOTES.md`, the N8 README and the release notes: paused on 23 November after 6 of 24 draws, n06 completed in X2, R3–R8 not started, no p\* computed or examined.
- **Numbers repeated across pages** agree with each other and with the tables: the five registered contrasts and their leave-one-out readings, the later-end readings and counts, the read positions (2.19–2.48; m06 at 3.083; the other five at 2.73–2.95), P1's brackets (three and three), the six exposure-matched contrasts, the better-rate contrasts, the equal-updates sign by readout, the mean p\* of 0.103, the two parameter counts (recomputed from the architecture) and the update counts.
- **The README's example** prints `P1 = +0.00909 [+0.00400, +0.01417], n = 6`.
- **Links.** 314 local links and image sources on 11 pages resolve, fragment anchors included. The 12 external URLs on the living pages returned HTTP 200; their content was not inspected.
- **CI.** Both workflows succeeded on 30548db.
- **Considered and not raised:** v2.0 was released while the 13 November audit, which N8's protocol cites, was not yet in the tree (resolved in v2.1); local paths with the Windows user name in three new N8 files (disclosed at `PUBLICATION_NOTES.md:67`); the shorthand "exposure-matched", which now rests on the corrected definition in `METHODS.md` §5.

**Not verified by me.** The supervising session's checks of the brief's section 3. Whether PyTorch's CPU build writes exactly `2.7.0+cpu` on a reader's machine (taken from `AUDIT.md`). The content behind the external links.

## 3. Before N8 resumes

1. **Nothing in areas A or E calls for a change to N8's registered analysis.** The constants N8's tests take from the 13 November audit reproduce independently.
2. **F-a1.** Decide how a reader is to reach "60 of 60": state the two version strings in a dated note, or publish the order files. The registered analysis is not affected.
3. **F-a3.** Record why training was paused, and that the 18 remaining draws will all be attempted. Do this before R3.
4. **F-a2.** Have the registration commit archived by a third party before more data or any analysis exists. This is the owner's action.
5. **Doc-only, at the next publication:** E1 first, then A1 and E2–E6.
6. **For the result report:** S-b's joint cell distance at j = 1 is 0 by construction (A3).

## 4. New code (all post hoc) and exact output

Scripts are in `C:\Users\rafli\AppData\Local\Temp\swa21\a\scratch`, each with its output beside it as `.out`. `PY` is `C:\Users\rafli\AppData\Local\Programs\Python\Python312\python.exe -I -B` (Python 3.12.10, NumPy 2.5.3). `REPO` is my clone and `BUNDLE` is the extracted `n7-loss-arrays` folder.

### How I obtained batch orders

- **I generated them, and read no order file from anywhere.** None is published, and I opened nothing outside my clone, my scratch folder, the bundle and the brief.
- **Inputs:** each draw's `adapt_order_seed` in the bundle's `MANIFEST.json`, and the sealed rule at `text_engine.py:52–53`: epoch e's order is `torch.randperm(n, generator=torch.Generator().manual_seed(999 + seed + e))`.
- **Tool:** my own pure-Python code in `a3_recency.py`, with no PyTorch. It is an MT19937 generator seeded with the 32-bit seed, followed by the swap loop of PyTorch's CPU `randperm` as I recall it: for i from 0 to n − 2, z is the next 32-bit output mod (n − i), and positions i and i + z are swapped.
- **Files written:** `a6_make_orders.py` wrote `orders_as_pinned\` and `orders_public_install\` in my scratch folder. Each holds 12 `.i64` files (six draws, and six with the seed shifted by 1) and an `ORDERS.json`, in the layout of `regenerate_n7_orders.py`. The two folders differ only in the version strings inside `ORDERS.json`.
- **Why I trust them:** the 12 files have the SHA-256 values that N8's `HASHES.json` pins for the registrant's PyTorch-generated files; they reproduce the 36 published set sizes and the 18 published per-draw losses exactly; and the losses separate trained from untrained sequences by −0.2257 nats on average, against +0.0001 for the shifted seed.
- **What this does not show:** I did not run PyTorch. That PyTorch 2.7.0 produces these orders rests on the hash identity with the registrant's pinned files.

### `a1_envelope.py`

F1: the 64-combination envelope from N7's POINTS.csv and MATCHED.csv. Standard library, own t quantile.

SHA-256 `8518d76a94d7155ff2687647c2363241e2cbeb147ce35d17ece31ecb28d43942`. Command: `PY a1_envelope.py REPO`

~~~
t(0.975, df=5) = 2.5705818356363  (own bisection on the closed-form CDF)

== P1 (lr1e-04, matched on train) ==
  m01: bracket 2-2.25, weight 0.9959; p768 0.076656 -> 0.090136 (rises); contrast sealed +0.011705, earlier end +0.025130, later end +0.011650
  m02: bracket 2.25-2.5, weight 0.5615; p768 0.088761 -> 0.095095 (rises); contrast sealed +0.010231, earlier end +0.013788, later end +0.007454
  m03: bracket 2.25-2.5, weight 0.2071; p768 0.095407 -> 0.100937 (rises); contrast sealed +0.008166, earlier end +0.009311, later end +0.003780
  m04: bracket 2-2.25, weight 0.7561; p768 0.078456 -> 0.092275 (rises); contrast sealed +0.014037, earlier end +0.024485, later end +0.010666
  m05: bracket 2-2.25, weight 0.9251; p768 0.078437 -> 0.094538 (rises); contrast sealed +0.010368, earlier end +0.025263, later end +0.009162
  m06: bracket 2.25-2.5, weight 0.9029; p768 0.095226 -> 0.101309 (rises); contrast sealed +0.000021, earlier end +0.005512, later end -0.000570
  sealed (interpolated): +0.00909 [+0.00400, +0.01417], 6/6 above 0
  all later ends       : +0.00702 [+0.00216, +0.01189], 5/6 above 0
  all earlier ends     : +0.01725 [+0.00796, +0.02653], 6/6 above 0
  64 combinations: lowest lower limit +0.0000764 (mean +0.00927, upper +0.01846) at ELLLLL (draw order m01..m06; E earlier, L later)
    same combination with t = 2.5706: +0.0000763
    second lowest: +0.0002565 at ELLELL; combinations with lower limit <= 0: 0 of 64; highest lower limit +0.0079627
    lowest mean over the 64: +0.00702 at LLLLLL
    200,000 random interior readings: lowest lower limit +0.0008162 (vertex minimum +0.0000764)

== S1 (lr1e-04, matched on gap) ==
  m01: bracket 2.25-2.5, weight 0.2130; p768 0.090136 -> 0.096273 (rises); contrast sealed +0.010343, earlier end +0.011650, later end +0.005513
  m02: bracket 2.25-2.5, weight 0.1753; p768 0.088761 -> 0.095095 (rises); contrast sealed +0.012678, earlier end +0.013788, later end +0.007454
  m03: bracket 2.25-2.5, weight 0.3246; p768 0.095407 -> 0.100937 (rises); contrast sealed +0.007516, earlier end +0.009311, later end +0.003780
  m04: bracket 2.25-2.5, weight 0.9010; p768 0.092275 -> 0.097360 (rises); contrast sealed +0.006085, earlier end +0.010666, later end +0.005581
  m05: bracket 2.25-2.5, weight 0.1911; p768 0.094538 -> 0.101493 (rises); contrast sealed +0.007834, earlier end +0.009162, later end +0.002208
  m06: bracket 2.25-2.5, weight 0.2397; p768 0.095226 -> 0.101309 (rises); contrast sealed +0.004054, earlier end +0.005512, later end -0.000570
  sealed (interpolated): +0.00808 [+0.00487, +0.01130], 6/6 above 0
  all later ends       : +0.00399 [+0.00099, +0.00699], 5/6 above 0
  all earlier ends     : +0.01001 [+0.00709, +0.01294], 6/6 above 0
  64 combinations: lowest lower limit -0.0000507 (mean +0.00505, upper +0.01015) at LELLLL (draw order m01..m06; E earlier, L later)
    same combination with t = 2.5706: -0.0000508
    second lowest: +0.0002263 at EELLLL; combinations with lower limit <= 0: 1 of 64; highest lower limit +0.0070905
    lowest mean over the 64: +0.00399 at LLLLLL
    200,000 random interior readings: lowest lower limit +0.0004654 (vertex minimum -0.0000507)

== S4 (lr3e-04, matched on train) ==
  m01: bracket 2.75-3, weight 0.2042; p768 0.100862 -> 0.102674 (rises); contrast sealed +0.018293, earlier end +0.018663, later end +0.016851
  m02: bracket 2.75-3, weight 0.8043; p768 0.100989 -> 0.101997 (rises); contrast sealed +0.017070, earlier end +0.017880, later end +0.016873
  m03: bracket 2.75-3, weight 0.3845; p768 0.104627 -> 0.108042 (rises); contrast sealed +0.015546, earlier end +0.016859, later end +0.013444
  m04: bracket 2.5-2.75, weight 0.9280; p768 0.103107 -> 0.106906 (rises); contrast sealed +0.012925, earlier end +0.016450, later end +0.012651
  m05: bracket 2.75-3, weight 0.3352; p768 0.103096 -> 0.106238 (rises); contrast sealed +0.014874, earlier end +0.015927, later end +0.012785
  m06: bracket 3-3.25, weight 0.3314; p768 0.103894 -> 0.126254 (rises); contrast sealed +0.004944, earlier end +0.012355, later end -0.010005
  sealed (interpolated): +0.01394 [+0.00893, +0.01896], 6/6 above 0
  all later ends       : +0.01043 [-0.00027, +0.02113], 5/6 above 0
  all earlier ends     : +0.01636 [+0.01405, +0.01866], 6/6 above 0
  64 combinations: lowest lower limit -0.0002679 (mean +0.01043, upper +0.02113) at LLLLLL (draw order m01..m06; E earlier, L later)
    same combination with t = 2.5706: -0.0002679
    second lowest: -0.0002413 at LELLLL; combinations with lower limit <= 0: 5 of 64; highest lower limit +0.0140518
    lowest mean over the 64: +0.01043 at LLLLLL
    200,000 random interior readings: lowest lower limit -0.0001098 (vertex minimum -0.0002679)
~~~

### `a2_gap.py`

F2: independent recomputation of the gap scale from N5's POINTS.csv, with one further descriptive scale.

SHA-256 `a65026d31f590248791552b5588c38aaff7a50ff37154dbea9a1887775c0083d`. Command: `PY a2_gap.py REPO`

~~~
readouts in N5 POINTS.csv: [0.25, 0.5, 1.0, 2.0, 3.0] | draws: 10 d01 .. d10
t(0.975, df=9) = 2.2621571627982
E2 gap 768-512:  +0.00039 [-0.00472, +0.00551]; draws -0.00925 to +0.01450; 4/10 above 0
E2 p*  768-512:  -0.00924 [-0.01123, -0.00724]; 0/10 above 0
width 512, E1->E2: mean of per-draw slopes 0.157 (draws 0.139 to 0.190); ratio of mean changes 0.156; gap change +0.132 to +0.161 nats
width 512, E2->E3: mean of per-draw slopes 0.185 (draws 0.172 to 0.195); ratio of mean changes 0.185; gap change +0.148 to +0.171 nats
width 768, E1->E2: mean of per-draw slopes 0.149 (draws 0.128 to 0.173); ratio of mean changes 0.149; gap change +0.117 to +0.145 nats
width 768, E2->E3: mean of per-draw slopes 0.167 (draws 0.150 to 0.184); ratio of mean changes 0.167; gap change +0.135 to +0.162 nats
slopes 0.149 to 0.185; upper limit 0.00551 nats -> 0.00082 to 0.00102 of p*; share of |p* difference| 0.089 to 0.110
  lower limit -0.00472 nats -> -0.00071 to -0.00087 of p* (the sign that would go with 768 having the lower p*)
  largest single-draw gap difference +0.01450 nats -> 0.00217 to 0.00268 of p*
across the 10 draws at E2: slope of (p* difference) on (gap difference) +0.215 per nat, r = +0.550; p* difference at zero gap difference (intercept) -0.00932
per draw (gap difference, p* difference): d01 -0.0045 -0.0106, d02 -0.0092 -0.0104, d03 +0.0064 -0.0037, d04 -0.0012 -0.0100, d05 -0.0056 -0.0085, d06 +0.0145 -0.0084, d07 -0.0011 -0.0133, d08 -0.0045 -0.0120, d09 +0.0066 -0.0061, d10 +0.0027 -0.0093
~~~

### `a3_recency.py`

F3: the emulated batch orders, their validation, and the recency maxima.

SHA-256 `1c8a15d867f8a9a64b2aaf2ffa94e9ac36aabd8d492b29de83b338b53fbd615b`. Command: `PY a3_recency.py REPO BUNDLE`

~~~
MT19937 seed 5489: first output 3499211612 (standard 3499211612), 10000th 4123659995 (standard 4123659995)
equals NumPy legacy MT19937 raw 32-bit stream for seed 2419856979 (2,000 outputs): True
order seeds 999 + adapt_order_seed + e stay below 2^32: True
loss change, trained minus untrained in the quarter (emulated orders; 192 arm-windows): mean -0.2257, range -0.3467 to -0.1187 nats
loss change, trained minus untrained in the quarter (seed + 1 control; 192 arm-windows): mean +0.0001, range -0.0087 to +0.0123 nats
k = 1: set sizes 226-272; largest |mean age difference| 14.11545 updates (draw m02, pass 2, signed -14.11545); largest joint quarter-cell TV 0.00000 (draw m06; 1 cell); mean |age difference| over 18 draw-passes 4.207; window width 256 updates
k = 2: set sizes 2018-2116; largest |mean age difference| 8.44744 updates (draw m03, pass 3, signed +8.44744); largest joint quarter-cell TV 0.03709 (draw m03; 8 cells); mean |age difference| over 18 draw-passes 3.187; window width 512 updates
k = 3: set sizes 6883-6931; largest |mean age difference| 6.99420 updates (draw m04, pass 3, signed -6.99420); largest joint quarter-cell TV 0.03659 (draw m03; 27 cells); mean |age difference| over 18 draw-passes 1.981; window width 768 updates
published set sizes reproduced: 18 of 18 (draw, k) pairs; largest difference from the 18 published loss_every values: 0.00e+00
~~~

### `a3b_order_hashes.py`

The emulated order files against the 12 hashes pinned in N8's HASHES.json.

SHA-256 `30a96285e5397be2cecd7a7c134aceac600b46d046c5ca343dfb22cbda176a17`. Command: `PY a3b_order_hashes.py REPO BUNDLE`

~~~
m01.i64: emulated 1454c34d6a9be84a..., pinned in HASHES.json 1454c34d6a9be84a...  MATCH
m01-seed-plus-1.i64: emulated c616d85dfc78f5df..., pinned in HASHES.json c616d85dfc78f5df...  MATCH
m02.i64: emulated 2dd2b964e1839d51..., pinned in HASHES.json 2dd2b964e1839d51...  MATCH
m02-seed-plus-1.i64: emulated 9453256699a44e46..., pinned in HASHES.json 9453256699a44e46...  MATCH
m03.i64: emulated cac1b23951790ca0..., pinned in HASHES.json cac1b23951790ca0...  MATCH
m03-seed-plus-1.i64: emulated f552dd02dcbdb99d..., pinned in HASHES.json f552dd02dcbdb99d...  MATCH
m04.i64: emulated 849eedd91be26e6e..., pinned in HASHES.json 849eedd91be26e6e...  MATCH
m04-seed-plus-1.i64: emulated 35e8815ecc62c3ed..., pinned in HASHES.json 35e8815ecc62c3ed...  MATCH
m05.i64: emulated 0bb27a61d12bc33e..., pinned in HASHES.json 0bb27a61d12bc33e...  MATCH
m05-seed-plus-1.i64: emulated cea25e11ea041f6b..., pinned in HASHES.json cea25e11ea041f6b...  MATCH
m06.i64: emulated 67d29a9c25d8cd21..., pinned in HASHES.json 67d29a9c25d8cd21...  MATCH
m06-seed-plus-1.i64: emulated ea2a16b25ed13468..., pinned in HASHES.json ea2a16b25ed13468...  MATCH
12 of 12 emulated order files are byte-identical to the pinned PyTorch-generated files
~~~

### `a3c_orders_json.py`

Which version strings rebuild the pinned ORDERS.json (12 pairs tried).

SHA-256 `33476a78d2a2de64bfed98df02eb0f99e9ca8cd060bc2d1ced47af540599f96b`. Command: `PY a3c_orders_json.py REPO BUNDLE`

~~~
ORDERS.json rebuilt byte for byte (SHA-256 equals the pin 8ba4a3c2...): yes, with torch 2.7.0+cu126 and numpy 2.2.6
~~~

### `a6_make_orders.py`

Writes the two order folders.

SHA-256 `51686ae563735bacbef75a996c02725d92d7fab3d6ccac23dd7917b8c70e4d34`. Command: `PY a6_make_orders.py BUNDLE orders_as_pinned 2.7.0+cu126 2.2.6 ; PY a6_make_orders.py BUNDLE orders_public_install 2.7.0+cpu 2.5.3`

~~~
wrote 12 order files to orders_as_pinned; ORDERS.json records torch 2.7.0+cu126, numpy 2.2.6; ORDERS.json SHA-256 8ba4a3c2e7906f65c6335ece7a785bfb37fe1b2904684959d388f589f2287eb1
wrote 12 order files to orders_public_install; ORDERS.json records torch 2.7.0+cpu, numpy 2.5.3; ORDERS.json SHA-256 536bb5d050b9642fa09d61cc65fd32a4725f32673289c6bf502eb668bc23b6e2
~~~

### `a3d_ks.py`

The audit's KS balance figures, from the emulated orders.

SHA-256 `db1f9a514a9e85364eed6ec96c6088a649529e47c442e3f16cbb77e3eb6f57ce`. Command: `PY a3d_ks.py orders_as_pinned`

~~~
k = 1: largest marginal KS distance 0.11920 (m02 pass 2)
k = 2: largest marginal KS distance 0.03365 (m03 pass 3)
k = 3: largest marginal KS distance 0.01816 (m04 pass 3)
~~~

### `a4_numbers.py`

Numbers quoted on the living pages, from MATCHED.csv and the 11 November RESULTS.json.

SHA-256 `0bad7f3828a3370ef19f92ed1fc381c031eab80e345c37fe8f5c08ccb4424b35`. Command: `PY a4_numbers.py REPO`

~~~
P1: +0.00909 [+0.00400, +0.01417], 6/6 above 0; read at 2.189-2.476; values +0.01171, +0.01023, +0.00817, +0.01404, +0.01037, +0.00002
    brackets: m01 2-2.25, m02 2.25-2.5, m03 2.25-2.5, m04 2-2.25, m05 2-2.25, m06 2.25-2.5
S1: +0.00808 [+0.00487, +0.01130], 6/6 above 0; read at 2.294-2.475; values +0.01034, +0.01268, +0.00752, +0.00608, +0.00783, +0.00405
    brackets: m01 2.25-2.5, m02 2.25-2.5, m03 2.25-2.5, m04 2.25-2.5, m05 2.25-2.5, m06 2.25-2.5
S3: -0.00454 [-0.00795, -0.00114], 0/6 above 0; read at 3.000-3.000; values -0.00290, -0.00014, -0.00639, -0.00283, -0.00566, -0.00933
S4: +0.01394 [+0.00893, +0.01896], 6/6 above 0; read at 2.732-3.083; values +0.01829, +0.01707, +0.01555, +0.01292, +0.01487, +0.00494
    brackets: m01 2.75-3, m02 2.75-3, m03 2.75-3, m04 2.5-2.75, m05 2.75-3, m06 3-3.25
S5: +0.01382 [+0.01116, +0.01648], 6/6 above 0; read at 3.000-3.000; values +0.01685, +0.01687, +0.01344, +0.01062, +0.01279, +0.01236
S2: only 3 draws read; read at 2.170-2.784; values +0.00611, +0.01414, -0.00571
ANALYSIS.json top-level keys: ['status', 'closed_by_failure', 'terminals', 'draws_available', 'arms', 'readouts', 'match_path', 'decision', 'sequence', 'statistics', 'readings', 'records_against_arrays', 'not_overfit', 'power_stated_in_advance', 'fit_bounds', 'losses', 'note', 'rate_effects', 'by_readout']
mean p*(512, E3, 1e-4) 0.1027; 768 where read in P1: 0.0889-0.1007
P1 leave-one-out intervals: m01 [+0.00208, +0.01505]; m02 [+0.00218, +0.01554]; m03 [+0.00258, +0.01597]; m04 [+0.00228, +0.01392]; m05 [+0.00216, +0.01550]; m06 [+0.00822, +0.01359]
S1 leave-one-out intervals: m01 [+0.00367, +0.01159]; m02 [+0.00429, +0.01005]; m03 [+0.00397, +0.01243]; m04 [+0.00446, +0.01251]; m05 [+0.00389, +0.01238]; m06 [+0.00565, +0.01214]
S3 leave-one-out intervals: m01 [-0.00923, -0.00051]; m02 [-0.00879, -0.00206]; m03 [-0.00850, +0.00015]*; m04 [-0.00924, -0.00053]; m05 [-0.00876, +0.00012]*; m06 [-0.00669, -0.00047]
S4 leave-one-out intervals: m01 [+0.00714, +0.01901]; m02 [+0.00703, +0.01960]; m03 [+0.00708, +0.02016]; m04 [+0.00755, +0.02074]; m05 [+0.00715, +0.02036]; m06 [+0.01318, +0.01830]
S5 leave-one-out intervals: m01 [+0.01036, +0.01607]; m02 [+0.01037, +0.01605]; m03 [+0.01039, +0.01741]; m04 [+0.01170, +0.01722]; m05 [+0.01058, +0.01748]; m06 [+0.01074, +0.01749]
matched|lr1e-04|k1|every: -0.00346 [-0.02582, +0.01890], 4/6 above 0
matched|lr1e-04|k2|every: -0.00476 [-0.01213, +0.00262], 2/6 above 0
matched|lr1e-04|k3|every: -0.00506 [-0.01094, +0.00083], 2/6 above 0
matched|lr3e-04|k1|every: +0.01258 [-0.00990, +0.03506], 5/6 above 0
matched|lr3e-04|k2|every: +0.01264 [+0.00486, +0.02042], 6/6 above 0
matched|lr3e-04|k3|every: +0.01292 [+0.00718, +0.01865], 6/6 above 0
better_rate|equal_updates|0.25: +0.02508 [+0.02200, +0.02816], 6/6 above 0
better_rate|loss|0.25: +0.05703 [+0.02344, +0.09062], 6/6 above 0
better_rate|equal_updates|0.5: +0.01755 [+0.01562, +0.01947], 6/6 above 0
better_rate|loss|0.5: +0.03324 [+0.00174, +0.06475], 5/6 above 0
better_rate|equal_updates|1.0: +0.01240 [+0.01095, +0.01385], 6/6 above 0
better_rate|loss|1.0: +0.01408 [-0.01483, +0.04298], 4/6 above 0
better_rate|equal_updates|2.0: +0.01147 [+0.00862, +0.01431], 6/6 above 0
better_rate|loss|2.0: +0.00231 [-0.02303, +0.02765], 4/6 above 0
~~~

### `a5_links.py`

Local links and fragment anchors of 11 pages.

SHA-256 `4bfd8f16ca234f62dd160b6f4a944d4f6a8bbca05782998d1e42b65f5d2a4982`. Command: `PY a5_links.py REPO`

~~~
314 local links and image sources checked on 11 pages; 0 broken; 15 external links not checked
~~~

## 5. Commands that matter, with exact output

Run in `REPO` unless stated.

### C1. History of the correction (A1)

~~~
$ git log --format="%h %cd %s" --date=iso-strict --stat -- reports/natural-text-correction-20261123-01/
30548db 2026-11-23T12:09:20+07:00 Version 2.1: N8 paused

 reports/natural-text-correction-20261123-01/CORRECTION.md | 9 +++++----
 1 file changed, 5 insertions(+), 4 deletions(-)
c1a2380 2026-11-23T12:05:02+07:00 N8 paused after 6 of 24 draws

 .../CORRECTION.md                                  | 124 +++++++++++++++++++++
 .../GAP_SCALE.txt                                  |   9 ++
 .../gap_scale.py                                   |  40 +++++++
 3 files changed, 173 insertions(+)

$ git diff c1a2380 30548db -- reports/natural-text-correction-20261123-01/CORRECTION.md
diff --git a/reports/natural-text-correction-20261123-01/CORRECTION.md b/reports/natural-text-correction-20261123-01/CORRECTION.md
index b0ae40b..edcb8a2 100644
--- a/reports/natural-text-correction-20261123-01/CORRECTION.md
+++ b/reports/natural-text-correction-20261123-01/CORRECTION.md
@@ -85,9 +85,9 @@ largest total-variation distance between the sets' joint distributions over quar
 
 These are the audit's figures. `test_on_n7.py` reproduces them within 5e-6 from N7's regenerated batch orders.
 
-**What changes:** `METHODS.md` now says "matched recency windows" and gives these differences. C4 in
-`CURRENT_CLAIMS.md` says "in matched recency windows for all three passes" instead of "matched for the timing of all
-three passes".
+**What changes:** `METHODS.md` now says "matched recency windows" and gives these differences. `CURRENT_CLAIMS.md`
+(C4), `README.md` and `NATURAL_TEXT_STUDIES.md` say "in matched recency windows" for every pass instead of "matched for
+the timing" of every pass.
 
 ## 4. F4: N6's width 384, and the training statement
 
@@ -121,4 +121,5 @@ diagnostics) and F6 (estimator edge-case fixtures) are not adopted in this updat
 Living pages changed:
 - `CURRENT_CLAIMS.md`: C3, C4's table and exposure bullet, and the training row;
 - `METHODS.md`: §1's table, §5's exposure-matched comparison, §6 and §7;
-- `README.md`: the sensitivity table's note, the familywise rate and the training level.
+- `README.md`: the sensitivity table's note, the familywise rate, matched recency windows and the training level;
+- `NATURAL_TEXT_STUDIES.md`: matched recency windows.

$ git show c1a2380:reports/natural-text-correction-20261123-01/CORRECTION.md | sha256sum ; sha256sum reports/natural-text-correction-20261123-01/CORRECTION.md
05f5459c988f25ff77a6330e056e574da09bfa075fa9061ed2d91c74ed5359e2 *-
c043f501a9bb7963c57e41596b870e85e5cb1245d403328d833b3359981921cb *reports/natural-text-correction-20261123-01/CORRECTION.md

$ git grep -c "c1a2380" 30548db -- . ; git grep -n -i "amend\|revis" 30548db -- reports/natural-text-correction-20261123-01/CORRECTION.md   (no output: no match)

$ git diff --stat c1a2380 30548db
 CITATION.cff                                       |   4 +-
 NATURAL_TEXT_STUDIES.md                            |   4 +-
 PUBLICATION_MANIFEST.csv                           |  17 +-
 PUBLICATION_NOTES.md                               |  29 +-
 README.md                                          |   8 +-
 .../OPERATIONAL_NOTES.md                           |   6 +-
 .../README.md                                      |   7 +-
 .../RUN_COMMAND.ps1                                | 102 ++++++
 .../X2_COMMAND.txt                                 |  73 ++++
 .../check_run.py                                   | 379 +++++++++++++++++++++
 .../CORRECTION.md                                  |   9 +-
 11 files changed, 607 insertions(+), 31 deletions(-)

$ gh api -X GET "repos/rafli-hl/sequence-weighting/actions/runs?per_page=4" --jq ".workflow_runs[] | [.name, .head_sha[0:7], .event, .conclusion, .created_at] | @tsv"
verify-posthoc	30548db	release	success	2026-11-23T05:10:49Z
verify	30548db	release	success	2026-11-23T05:10:49Z
verify	30548db	push	success	2026-11-23T05:09:35Z
verify	c1a2380	push	success	2026-11-23T05:05:18Z
~~~

### C2. Living pages, versions, dates, files changed, archives, tags, protocol (E1 to E7, F-a2, F-a3)

~~~
$ grep -n "closed again" NATURAL_TEXT_STUDIES.md ; sed -n "187,188p;191,192p" NATURAL_TEXT_STUDIES.md
149:The experiments were reopened for N7 alone and are closed again.
record was closed after N7; on 14 November 2026 it was reopened for one registered study, N8, a dense-readout
replication of N7 on fresh draws ([preregistration](preregistration/natural-text-dense-replication-20261114/README.md)), which has no results yet.
**N8, paused on 23 November 2026.**
- Training stopped after 6 of its 24 draws: n01–n06, with n06 completed in the retry run X2. R3–R8 have not started.

$ sed -n "3p" CURRENT_CLAIMS.md | cut -c1-120 ; sed -n "1p" NATURAL_TEXT_STUDIES.md
**As of 12 November 2026; wording revised 13 November 2026, with no claim, number or label changed.** This page states w
# Natural-text studies, 27 October – 11 November 2026

$ git log --format="%h %ad" --date=short -- DATA_AVAILABILITY.md ; grep -c "N8" DATA_AVAILABILITY.md ; sed -n "9,10p;13,14p" DATA_AVAILABILITY.md
fee55ea 2026-11-13
c4ae0e1 2026-11-12
0
- **Protocols and registrations.** Each study's protocol, amendments and seed registry, and the public registrations
  of N6 and N7.
- **Review records.** The adversarial review, the response to it, the owner's design decisions for the natural-text
  studies, the audits of 8 and 12 November 2026, and the corrections of 9, 11 and 12 November 2026.

$ grep -n "Only N7 was publicly\|Public registrations of N6 and N7\|sign depends" README.md | cut -c1-150 ; grep -n "the two public registrations" METHODS.md ; grep -n "Two studies were also registered publicly" NATURAL_TEXT_STUDIES.md ; ls preregistration
272:   readings are a sensitivity check, not a bound on the unobserved trajectory. S4's sign depends on this.
276:6. **Registration.** Only N7 was publicly preregistered. N6 was registered publicly after its data existed; the other
303:| `preregistration/` | Public registrations of N6 and N7, each with sealed source and seed registry |
23:How to check the two public registrations against the archived commits is in
27:Two studies were also registered publicly. N6 was registered only after its data existed (see
natural-text-dense-replication-20261114/
natural-text-matched-confirmation-20261104/
natural-text-peak-confirmation-20261103/

$ grep -n "version\|v2\.1\|date-released" CITATION.cff README.md | grep -i "2\.1\|version \|date-released" | cut -c1-140
CITATION.cff:11:version: "2.1"
CITATION.cff:16:date-released: 2026-11-23
README.md:13:[v2.1](https://github.com/rafli-hl/sequence-weighting/releases/tag/v2.1) (23 November 2026). The README
README.md:315:This repository starts from a single commit of the finished record (version 1.2). The record was built in an earlier
README.md:329:  version      = {2.1},

$ gh api -X GET repos/rafli-hl/sequence-weighting/releases --jq ".[] | [.tag_name, .created_at, .published_at] | @tsv"
v2.1	2026-11-23T05:09:20Z	2026-11-23T05:10:47Z
v2.0	2026-11-14T18:44:07Z	2026-11-14T18:45:38Z
v1.2	2026-11-12T10:13:56Z	2026-11-12T10:25:53Z

$ git log -3 --format="%h %ad %s" --date=iso-strict c6f98b2 ; git for-each-ref --format="%(refname) %(objecttype) %(objectname:short)" refs/tags
c6f98b2 2026-11-15T01:19:19+07:00 Merge pull request #1 from rafli-hl/n8-registration
aaafa2e 2026-11-15T01:17:02+07:00 Register N8: dense-readout replication of N7
fee55ea 2026-11-13T12:54:48+07:00 Revise README and add METHODS.md (documentation only; no result changed
refs/tags/n8-registration commit c6f98b2
refs/tags/v1.2 commit c4ae0e1
refs/tags/v2.0 commit 88ac496
refs/tags/v2.1 commit 30548db

$ git diff --name-status v2.0 v2.1
M	CITATION.cff
M	CURRENT_CLAIMS.md
M	METHODS.md
M	NATURAL_TEXT_STUDIES.md
M	PUBLICATION_MANIFEST.csv
M	PUBLICATION_NOTES.md
M	README.md
A	preregistration/natural-text-dense-replication-20261114/OPERATIONAL_NOTES.md
M	preregistration/natural-text-dense-replication-20261114/README.md
A	preregistration/natural-text-dense-replication-20261114/RUN_COMMAND.ps1
A	preregistration/natural-text-dense-replication-20261114/X2_COMMAND.txt
A	preregistration/natural-text-dense-replication-20261114/check_run.py
M	reports/README.md
A	reports/external-audit-20261113-01/AUDIT.md
A	reports/external-audit-20261113-01/README.md
A	reports/natural-text-correction-20261123-01/CORRECTION.md
A	reports/natural-text-correction-20261123-01/GAP_SCALE.txt
A	reports/natural-text-correction-20261123-01/gap_scale.py

$ curl -s "https://archive.softwareheritage.org/api/1/origin/https://github.com/rafli-hl/sequence-weighting/visits/?per_page=5"
{"exception":"NotFoundExc","reason":"Origin with url https://github.com/rafli-hl/sequence-weighting not found!"}
$ curl -s -o /dev/null -w "%{http_code}" "https://archive.softwareheritage.org/api/1/revision/c6f98b26669f5d29f30c576b6d800c1fc82c98eb/"
404
$ curl -s "http://web.archive.org/cdx/search/cdx?url=github.com/rafli-hl/sequence-weighting&limit=5&output=json&fl=timestamp,original,statuscode"
[]


$ grep -n -i -c "pause\|interrupt\|resum" preregistration/natural-text-dense-replication-20261114/N8-protocol-draft.md
0
~~~

### C3. The record's `test_on_n7.py`, run twice on N7's public data (F-a1)

Command: `PY REPO/preregistration/natural-text-dense-replication-20261114/analysis/test_on_n7.py REPO BUNDLE <orders folder>`. Full outputs are in `test_on_n7_as_pinned.out` and `test_on_n7_public_install.out` (78 lines each). Apart from timing lines they differ only here (`<` pinned strings, `>` public-install strings):

~~~
49c49
< PASS  regenerated orders (PyTorch 2.7.0+cu126): ORDERS.json pinned, files, per-epoch order_sha256, each row a permutation  [8ba4a3c2e7906f65, 0 mismatches]
---
> FAIL  regenerated orders (PyTorch 2.7.0+cpu): ORDERS.json pinned, files, per-epoch order_sha256, each row a permutation  [536bb5d050b9642f, 0 mismatches]
70,71c70,71
< 60 passed, 0 failed
< exit 0
---
> 59 passed, 1 failed
> exit 1
~~~

The F1 and F3 lines, identical in both runs:

~~~
PASS  P1 envelope over 64 combinations: min lower +0.0000764, max upper +0.0274348  [vs brief 5.1e-09; vs itertools brute force 0 / 0]
PASS  S-b, 768 at E2.25: whole, last, every, losses against the 11 Nov RESULTS.json (1e-6); every-pass balance: sizes 226-272, mean age difference 14.11545, joint cell distance 0.00000 (13 Nov audit)  [largest value difference 1.1e-08]
PASS  S-b, 768 at E2.5: whole, last, every, losses against the 11 Nov RESULTS.json (1e-6); every-pass balance: sizes 2018-2116, mean age difference 8.44744, joint cell distance 0.03709 (13 Nov audit)  [largest value difference 2.2e-08]
PASS  S-b, 768 at E2.75: whole, last, every, losses against the 11 Nov RESULTS.json (1e-6); every-pass balance: sizes 6883-6931, mean age difference 6.99420, joint cell distance 0.03659 (13 Nov audit)  [largest value difference 2.2e-08]
PASS  S1 envelope over 64 combinations: min lower -0.0000507, max upper +0.0142363  [vs brief 4.1e-08; vs itertools brute force 0 / 0]
PASS  S4 envelope over 64 combinations: min lower -0.0002679, max upper +0.0243117  [vs brief 1.4e-07; vs itertools brute force 0 / 0]
~~~

### C4. `gap_scale.py` (F2), the README example, and the state of the clone

~~~
$ PY reports/natural-text-correction-20261123-01/gap_scale.py > SCRATCH/gap_scale_rerun.out   (exit 0)
$ tr -d "\r" < SCRATCH/gap_scale_rerun.out | sha256sum ; sha256sum reports/natural-text-correction-20261123-01/GAP_SCALE.txt
13b41f3d7dc5818a6105fbf02376c277c2167b31bf8c873ec7ba6298f8ff36f3 *-
13b41f3d7dc5818a6105fbf02376c277c2167b31bf8c873ec7ba6298f8ff36f3 *reports/natural-text-correction-20261123-01/GAP_SCALE.txt
$ PY SCRATCH/readme_block.py   (README.md lines 205 to 226, unedited)
P1 = +0.00909 [+0.00400, +0.01417], n = 6
$ git status --porcelain | wc -l ; git rev-parse HEAD   (after all work)
0
30548dbb789b2a117486fdf6f9ab9added680172
~~~
