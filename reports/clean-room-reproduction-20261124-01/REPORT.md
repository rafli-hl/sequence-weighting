# Clean-room reproduction of N7's analysis: report

## 1. Summary

- **Yes, the published numbers reproduce from the protocol, the technical note and the released bundle alone.**
- **Fits:** all 240 p\* agree within 1e-6. The largest difference is 8.7e-9 under my primary reading and 2.4e-9 under my frozen "ordinal ties" variant. No fit differs by more than 1e-6.
- **Matched readings:** all 36 rows of `MATCHED.csv` agree on status, bracket and number of intervals holding the target. The largest difference in a per-draw value is 6.8e-7 (S2, m03).
- **Statistics:** all six agree on available draws, sign tests, leave-one-draw-out sides and labels: P1 REVERSAL_CONFIRMED; S1, S3, S4, S5 CONFIRMED; S2 UNAVAILABLE (3 of 6 draws). The largest difference is 2.7e-8 in a mean and 9.6e-8 in an interval limit.
- **Two specification ambiguities** account for almost all of the differences: where the mean losses come from, and how tied weights are ranked. Neither can move a label.
- **Possible errors in the published analysis: none found.**
- **Exposure:** my starting context contained N7's labels (quoted in section 2). I did not use them.

## 2. Provenance

Times are the machine clock in UTC (local time is +07:00).

| When | What |
|---|---|
| 18:02:07Z, 23 Nov 2026 | Read `BRIEF.md`. Downloaded `PROTOCOL.md` (v2.1 sealed source), the Jane Street note (PDF, 1 page) and the bundle with `gh release download` |
| 18:02–18:05Z | Read the protocol, the note, the bundle's `README.md`, `MANIFEST.json` and one `record.json`. Checked all 66 bundle files against the manifest (0 mismatches) |
| 18:05Z | Wrote `SPEC_LOG.md` (Q1–Q33), before any fit was run |
| 18:05–18:12Z | Wrote the code, ran it into a scratch folder and read my own results. Appended the pre-freeze addendum (Q34, Q35) |
| **18:12:32Z** | **Freeze** (`FREEZE.txt`). The final run and the scratch run were byte-identical |
| 18:12:42–44Z | Created `phase2\` and fetched the four published tables |
| 18:13–18:17Z | Comparison and a labelled second pass of evidence checks. All 18 frozen files re-verified against `FREEZE.txt` afterwards |

**Bundle hash verified:** `cbe26760e2062a4cf03307d779226fa6efce8cfcfbf57b2e092bd818af80b8a9`, as the brief states.

**Other inputs (SHA-256):**
- `PROTOCOL.md`: `adf006ba144efccbf54710dc0c3ae56cba9b66d105c0d25624e5b8e1348dd23e`
- Note PDF: `f7728b89b9c083c88b70f89c9da2a33ecc147e43007faa3aff374c3feafed346`
- `BRIEF.md`: `41584c8335ab040eeaf5550243b2edd4357cc31634b949113d57b409b255f985`

**Environment:** Python 3.12.10, NumPy 2.5.3, Windows 11 10.0.26300, run with `-I -B`. No SciPy, WSL or GPU. Nothing was read outside `C:\Users\rafli\AppData\Local\Temp\n7cr`. The repository was not cloned, and nothing was pushed or posted.

**Frozen hashes** (`FREEZE.txt` itself: `66b44eb3a545a310aadbd82957479017f15e9a381185a74ce8b790c3a35a232a`):

| File | SHA-256 |
|---|---|
| `code\n7_repro.py` | `004b2841c7b5e16b75732ba727590e1e854fd89c2e51b946a64e205bb528a033` |
| `SPEC_LOG.md` | `8900cda094c900e90d5d86c43dec46c2c1b7b437d379b8a2f0406595a7a1043c` |
| `out\ecdf_arrays\analysis.json` (primary) | `b1f6f89a881d19a6188107b686c4d91dceaf97889415d647b21912ab56f03275` |
| `out\ecdf_arrays\contrasts.csv` | `b4d6f428ae7ed66fc99f7e1f69b87efe49073807fc1678790829c6bafe4222a3` |
| `out\ecdf_arrays\matched.csv` | `e56ef497d8dd403d9b36bac04ba2fdb177cb19868194f62a6014373d5075da86` |
| `out\ecdf_arrays\per_readout.csv` | `9f2749d5dfe9ec390667de24351b104789510718e4a9ef4c1ec623a7991b724e` |
| `out\ecdf_record\analysis.json` | `94277915fcb855724bd3fdd135f04ccadc2c2b05e4795bd3e66de2f27c8f74f9` |
| `out\ecdf_record\contrasts.csv` | `1bb4b85cf339f12b00afb0c90c49ebd93ae7f373784b4577eb9e1cf588deaa2f` |
| `out\ecdf_record\matched.csv` | `3dfdce4409239299923d715f1574e662217f37076913a751528da582730d31ca` |
| `out\ecdf_record\per_readout.csv` | `d3ba54b445f537ae589036121184a6b221e3d219e4a89c27ebb905fd17638da2` |
| `out\ordinal_arrays\analysis.json` | `a519cbda502dd568b959253a1256535dca5f7d671dc9a48406f71be4c7aa3fd0` |
| `out\ordinal_arrays\contrasts.csv` | `c64eb0f9a7418f3062ac2eb6ed23a675a286268d7951c844b8cafe2748370af3` |
| `out\ordinal_arrays\matched.csv` | `9a3f92cb172b7a3c036aa4d7df6a784bead28cf400f23d97d68b0d9c89b4003f` |
| `out\ordinal_arrays\per_readout.csv` | `83e7f9c5f6a23769b436c6c7712ff621d0814515f7120d95063a65b2c7f617e4` |
| `out\ordinal_record\analysis.json` | `73b89d25c00fa393504345f95d95f723c016fc9cbd074fecb859c16a3cb6771d` |
| `out\ordinal_record\contrasts.csv` | `0d87368db359c342afe2c0e71cf1943404ac5558bb0dfa21fc7caf5cfcd28057` |
| `out\ordinal_record\matched.csv` | `c122a8f795d87d034cd7098a7ba028a1923d8c0505ab88ab5fa1adb4ec8a4474` |
| `out\ordinal_record\per_readout.csv` | `5219a14acf6b16d9bbb815961bf649223ef40212027a679b2110e8bc334d7e9a` |

**Published tables as fetched (SHA-256):**
- `POINTS.csv`: `234434a34cf64d98e0d45cfe029bb37935207176fd996cafe85756956c7d860f`
- `MATCHED.csv`: `86ea11d7210682375717d7eb67a58c74d806ad22dc57ec87ab9db4e836421e3b`
- `FITS.csv`: `b1cd03dec3a6e13ba2d82a6a95a48e99342ace8aaf4a0cdf1b36392fa8c7aa67`
- `ANALYSIS.json`: `a4af7bad78fdf9f4fe34317f73e6a1932fd0d29367b5da188b79ae73db95ce65`

**Exposure to results before the freeze:**
1. **Starting context (not an allowed source).** A memory index line read: "N7 result … N7 reported 6 Nov: P1 REVERSAL_CONFIRMED, confirmed through S5, S2 UNAVAILABLE, check PASS; start from natural-text-matched-result-20261105-01/RESULT.md and the note on claims 4 and 5; PR #6 package prepared, not committed". This states N7's labels. I did not open the memory file, and no reading or code path depends on it. My labels come from the computation, but I knew the expected labels while implementing.
2. **Bundle README (an allowed source).** It says the verifier "recomputes the five confirmed contrasts" and "On 9 November 2026 the largest difference in p\* was 2.9e-9". The first implies that five steps were confirmed.
3. **A rule, not a result.** A project instruction file in my context says "Uniform weights and nonpositive total gain have undefined p\*". It agrees with what I derived from the note (Q7).
4. The protocol quotes N6 figures (for example +0.0132), which are not N7 results.

**Before the freeze I also saw** my own outputs from one scratch run, and fixed two defects of my own. Neither was a change of reading:
- the self-test compared d'Kd with N times the cumulative form;
- the CSV writer printed NumPy scalars as `np.float64(...)`.

## 3. Specification log

This is condensed from the frozen `SPEC_LOG.md`. The "Outcome" entries were added after the comparison.

**A. Estimator**

| Q | Question | Reading chosen | Outcome |
|---|---|---|---|
| Q1 | Arithmetic of the gain | E0 training loss minus readout training loss in float32 (as the bundle README says), then float64 | Agrees: `total_gain` matches `FITS.csv` exactly in all 240 fits |
| Q2 | Which E0 | Same draw and width; both rates share it | Agrees |
| Q3 | Objective | The note's d'Kd, K_ij = min(r_i, r_j), in its cumulative-sum form over sequences sorted by weight | Agrees |
| **Q4** | **Rank of tied weights** (the data have 3, 4, 1, 1, 1, 1 surplus tied values in m01–m06) | **Primary: empirical CDF, so tied weights share a rank. Variant: ordinal ranks from a stable sort** | **The published analysis matches the ordinal variant.** See D2 |
| Q5 | Which weights | `weights.f32` as released, in float64; b computed through exp(p·ln w) | Agrees to rounding |
| Q6 | Range | Closed [0, 8]; boundary minima are admissible | Not exercised: p\* lies between 0.038 and 0.149 |
| Q7 | Undefined fits | Total gain not positive or not finite; all weights equal; non-finite objective | Not exercised: 240 of 240 defined in both |
| Q8 | Several minima or exact ties | Global minimum; the smaller p on an exact tie (my rule, since the protocol has none) | Not exercised: one candidate minimum in every fit |
| Q9 | Numerical method | Grid of step 0.02 for J and its analytic derivative, then bisection on the derivative to a width below 1e-13; golden-section on J as a cross-check | The two methods differ by at most 2.8e-9 |
| Q10 | Bound flags | Upper if p\* ≥ 7.999; lower if p\* ≤ 0.001 (the lower margin is mine) | Both report 0 upper, 0 lower, 0 undefined |
| Q11 | Saturation | Flag fits ≥ 7.999, refit on [0, 32]; "unresolved" means ≥ 31.999 (my reading) | Not exercised: no flagged draw in either |
| Q34 | Rank offset (i/N, (i−1)/N and so on) | Irrelevant, because the d_i sum to 0 | — |

**B. Per-readout quantities**

| Q | Question | Reading chosen | Outcome |
|---|---|---|---|
| **Q12** | **What is the "training NLL (the per-draw `train` field as defined in N6)"?** N6's definition is not in the allowed sources | **Primary: unweighted float64 mean of the array block's 16,384 training rows (512 rows for validation). Variant: the record's `train_loss` and `validation_loss`** | **The published analysis uses the record values**, bit for bit. See D3 |
| Q13 | Which fits exist | 6 × 2 × 2 × 10 = 240; E0 is not fitted | Agrees |

**C. Matching**

| Q | Question | Reading chosen | Outcome |
|---|---|---|---|
| Q14 | Target and path | 512 at E3 against 768 at E2–E3.5, at the statistic's own rate | Agrees |
| Q15 | When an interval holds the target | Closed interval, exact comparison, first in readout order | Agrees on all 21 readings |
| Q16 | Weight | (T − v_a)/(v_b − v_a), the weight on the later readout; 0 if v_a = v_b = T | Agrees: bit-identical under the record variant |
| Q17 | Number of intervals holding the target | Count of closed intervals | Agrees, including m06 on S2, which has 3 |
| Q18 | Outside the path | No interval holds the target; no extrapolation | Agrees: m01, m04, m05 on S2 |
| Q19 | Precedence of reasons | Draw missing, then 512 fit undefined, then outside the path, then bracketing fit undefined | Not exercised |
| Q20 | Gap matching | Linear in validation minus training | Agrees |

**D. Statistics and labels**

| Q | Question | Reading chosen | Outcome |
|---|---|---|---|
| Q21 | t interval | Mean ± t(0.975, n−1)·s/√n, with s on n−1 | Agrees |
| Q22 | "Entirely above 0" | Strict | Not exercised at the boundary |
| Q23 | Sign test | Zeros dropped; p = min(1, 2·P(X ≤ min(n+, n−))) | Agrees: 0.03125 five times, 1.0 for S2 |
| Q24 | Leave-one-draw-out | Needs at least 4 values; df = n − 2 | Agrees on all 30 intervals and their sides |
| Q25 | Mean and interval of an UNAVAILABLE statistic | Computed and stored as not read | The published S2 has no interval. See D6 |
| Q26 | Status and printed label | Status from the step's own interval; NOT_READ if an earlier step is not confirmed | Agrees. S2 is reached and UNAVAILABLE in both |
| Q27 | Did every run complete | Six draws present and 24 records COMPLETE (the terminals are not in the bundle) | The published terminals are both COMPLETE |
| Q28 | NOT_OVERFIT | Per arm, validation at E3 minus E2, t interval over at least 5 draws | Agrees: four arms NOT_OVERFIT |
| Q29 | `records_against_arrays` | Largest absolute difference between a record loss and the float64 block mean | Agrees to every printed digit: 8.549686754122376e-07 |
| **Q30** | Descriptives, including the direction of the rate effect | Rate effect = p\*(3e-4) − p\*(1e-4), my choice | **The published direction is the opposite.** See D5 |
| Q31 | t quantiles | Incomplete beta by continued fraction, inverted by bisection; checked against closed forms (df 1, 2) and Simpson integration (df 3–5) | t(0.975, 5) = 2.570581835636318 |
| Q32, Q33, Q35 | Draw order; what cannot be reproduced; number formats | Name order; the readings' text, terminals, registry and partition are not reproduced; shortest round-trip floats | — |

## 4. Comparison

### 4.1 The 240 fits (my p\* against `FITS.csv`; `POINTS.csv` has the same p in every row)

| My variant | Largest difference in p\* | Where | Mean difference | Fits over 1e-6 |
|---|---|---|---|---|
| **Primary (ecdf ties)** | **8.685e-9** | m02, 768, 3e-4, E0.25 | 1.38e-9 | **0** |
| Ordinal ties | 2.432e-9 | m06, 768, 3e-4, E3.25 | 6.1e-10 | 0 |

- `total_gain`: largest difference 0 (exact).
- `negative_fraction`: largest difference 0.
- Bound flags: equal in all 240.
- Undefined fits: 0 in both.

### 4.2 Matched readings (36 rows of `MATCHED.csv`, identical to the rows in `ANALYSIS.json`)

Status, bracket and number of intervals agree in all 36 rows.

| Statistic | Draw | Bracket | Intervals holding | Weight: mine | Weight: published | Value: mine | Value: published | Difference |
|---|---|---|---|---|---|---|---|---|
| P1 | m01 | E2–E2.25 | 1 | 0.9958860 | 0.9958884 | 0.0117052675 | 0.0117052336 | 3.4e-8 |
| P1 | m02 | E2.25–E2.5 | 1 | 0.5615081 | 0.5614981 | 0.0102311795 | 0.0102312433 | 6.4e-8 |
| P1 | m03 | E2.25–E2.5 | 1 | 0.2070558 | 0.2070600 | 0.0081656551 | 0.0081656277 | 2.7e-8 |
| P1 | m04 | E2–E2.25 | 1 | 0.7560805 | 0.7560795 | 0.0140367007 | 0.0140367137 | 1.3e-8 |
| P1 | m05 | E2–E2.25 | 1 | 0.9251125 | 0.9251178 | 0.0103681565 | 0.0103680697 | 8.7e-8 |
| P1 | m06 | E2.25–E2.5 | 1 | 0.9028432 | 0.9028514 | 0.0000208459 | 0.0000207973 | 4.9e-8 |
| S1 | m01 | E2.25–E2.5 | 1 | 0.2130092 | 0.2130117 | 0.0103426197 | 0.0103426021 | 1.8e-8 |
| S1 | m02 | E2.25–E2.5 | 1 | 0.1752838 | 0.1752584 | 0.0126775786 | 0.0126777383 | 1.6e-7 |
| S1 | m03 | E2.25–E2.5 | 1 | 0.3245832 | 0.3245967 | 0.0075157014 | 0.0075156226 | 7.9e-8 |
| S1 | m04 | E2.25–E2.5 | 1 | 0.9009535 | 0.9009757 | 0.0060847536 | 0.0060846402 | 1.1e-7 |
| S1 | m05 | E2.25–E2.5 | 1 | 0.1910523 | 0.1910680 | 0.0078337000 | 0.0078335900 | 1.1e-7 |
| S1 | m06 | E2.25–E2.5 | 1 | 0.2397171 | 0.2397178 | 0.0040543678 | 0.0040543648 | 3.0e-9 |
| S4 | m01 | E2.75–E3 | 1 | 0.2041691 | 0.2041713 | 0.0182934305 | 0.0182934276 | 2.9e-9 |
| S4 | m02 | E2.75–E3 | 1 | 0.8042956 | 0.8042948 | 0.0170696873 | 0.0170696877 | 4.7e-10 |
| S4 | m03 | E2.75–E3 | 1 | 0.3844868 | 0.3844786 | 0.0155457853 | 0.0155458113 | 2.6e-8 |
| S4 | m04 | E2.5–E2.75 | 1 | 0.9280008 | 0.9280086 | 0.0129246426 | 0.0129246140 | 2.9e-8 |
| S4 | m05 | E2.75–E3 | 1 | 0.3351690 | 0.3351566 | 0.0148739083 | 0.0148739454 | 3.7e-8 |
| S4 | m06 | E3–E3.25 | 1 | 0.3314403 | 0.3314405 | 0.0049441759 | 0.0049441694 | 6.5e-9 |
| S2 | m01, m04, m05 | none | 0 | — | — | TARGET_OUTSIDE_PATH (above the path's maximum) | TARGET_OUTSIDE_PATH | — |
| S2 | m02 | E2.5–E2.75 | 1 | 0.2845118 | 0.2845309 | 0.0061132381 | 0.0061131493 | 8.9e-8 |
| S2 | m03 | E2–E2.25 | 1 | 0.6807519 | 0.6807067 | 0.0141371301 | 0.0141378076 | **6.8e-7** |
| S2 | m06 | E2.75–E3 | 3 | 0.1369672 | 0.1369566 | −0.0057097847 | −0.0057097399 | 4.5e-8 |

- **Fixed-update rows** (S3 and S5, 12 rows): all READ at E3; the largest difference in a value is 2.3e-9.
- **Largest differences under the primary reading:** weight 4.5e-5, read position 1.1e-5, target 7.0e-7, p_read 6.8e-7, p_first 3.3e-9.
- **Under the frozen `ordinal_record` variant:** weight, target and position are bit-identical (difference 0), and the largest difference in a value is 3.1e-9.

### 4.3 Registered statistics (primary against `ANALYSIS.json`)

| Step | n | Mean: mine | Mean: published | Interval: mine | Interval: published | Largest difference (mean; limit) | Sign test | Label (both) |
|---|---|---|---|---|---|---|---|---|
| P1 D4m_train | 6 | 0.0090879675 | 0.0090879475 | [0.0040039010, 0.0141720341] | [0.0040038635, 0.0141720316] | 2.0e-8; 3.7e-8 | 6+, 0−, p 0.03125 | REVERSAL_CONFIRMED |
| S1 D4m gap | 6 | 0.0080847869 | 0.0080847597 | [0.0048733472, 0.0112962265] | [0.0048732511, 0.0112962683] | 2.7e-8; 9.6e-8 | 6+, 0−, 0.03125 | CONFIRMED |
| S3 fixed D4 at E3 | 6 | −0.0045419864 | −0.0045419866 | [−0.0079469636, −0.0011370091] | [−0.0079469632, −0.0011370100] | 2.1e-10; 8.7e-10 | 0+, 6−, 0.03125 | CONFIRMED |
| S4 D2m_train | 6 | 0.0139419383 | 0.0139419426 | [0.0089275725, 0.0189563041] | [0.0089275701, 0.0189563151] | 4.3e-9; 1.1e-8 | 6+, 0−, 0.03125 | CONFIRMED |
| S5 fixed D2 at E3 | 6 | 0.0138211557 | 0.0138211550 | [0.0111615929, 0.0164807185] | [0.0111615919, 0.0164807181] | 7.3e-10; 1.1e-9 | 6+, 0−, 0.03125 | CONFIRMED |
| S2 D4m val | 3 | (not read) | none printed | (not read) | none printed | — | 2+, 1−, p 1.0 | UNAVAILABLE |

- **Leave-one-draw-out** (30 intervals): the largest difference in a limit is 5.3e-8 (P1), 1.7e-7 (S1), 2.0e-9 (S3), 1.8e-8 (S4), 1.4e-9 (S5). Every side agrees.
- **S3's leave-one-out intervals span 0** when m03 or m05 is dropped, in both analyses. P1, S1, S4 and S5 keep their side in all six.
- **Availability counts** (undefined fit, target outside the path, draw missing): 0, 0, 0 for P1 through S5 and 0, 3, 0 for S2, in both.
- **Sequence:** P1 → S1 → S3 → S4 → S5 confirmed, and S2 reached and UNAVAILABLE, in both. The published `confirmed_through` is S5.
- **Section 7 row:** "REVERSAL_CONFIRMED, with S3 reached and CONFIRMED", as the published readings print.
- **Under `ordinal_record`** the largest differences are 1.2e-9 in a mean, 2.2e-9 in an interval limit and 3.0e-9 in a leave-one-out limit.

### 4.4 Diagnostics and descriptives

| Item | Result |
|---|---|
| `records_against_arrays` | 8.549686754122376e-07 in both, below the 0.001 limit |
| NOT_OVERFIT | NOT_OVERFIT on all four arms in both. Means differ by at most 1.4e-7 under the primary reading, and by 0 under the record variant |
| Fit bounds | 0 upper, 0 lower, 0 undefined in both |
| Fixed-update contrast by readout (20 contrasts) | Largest difference 3.8e-9 in a value and 1.5e-9 in a limit |
| Panel means | p\* within 1.7e-9; losses within 2.7e-7 (primary) or 0 (record variant) |
| Clipping (update-weighted) and E0 means | Equal to rounding (at most 2.2e-16) |
| Rate effects at E3 | Equal in size within 2.5e-9, opposite in sign convention (D5) |
| Published t-test p-values (not registered in the protocol) | Recomputed from the published mean and standard error; they agree to 12 digits |

## 5. Discrepancies, classified

**D1. p\* differs by up to 2.4e-9 under the same tie reading. Numerical.**
- With ordinal ties my objective equals the published `objective` to 1.2e-14 relative, and J(0) equals the published `J0` to 8.7e-15. So the objective is the same function.
- For all 240 fits, my p minus the published p equals the Newton step from the published p to the stationary point, within 3.6e-14.
- The derivative at the published p is up to 1.8e-9; at mine it is at most 2.8e-14.
- So the published values sit within their optimiser's tolerance of the exact minimiser. The two objective values are indistinguishable (±3e-18).

**D2. Tied weights: empirical-CDF ranks (mine) against ordinal ranks (published). Specification ambiguity (Q4).**
- The published objective matches a stable sort with ties in sequence order to about 1e-14.
- Reversing the tie order changes the objective by 4e-8 to 3e-7 relative; the ecdf reading changes it by up to 1.6e-6.
- Effect on p\*: at most 8.8e-9. No statistic moves by more than about 2e-9 from this.
- The note defines the rank through the CDF and is silent on ties. The protocol only bounds their number.

**D3. Source of the mean losses: array-block means (mine) against the records' fields (published). Specification ambiguity (Q12).**
- The published `train`, `validation` and `gap` in `POINTS.csv`, and every matching target, equal the `record.json` values bit for bit.
- The two sources differ by up to 8.5e-7. This is the registered `records_against_arrays` figure.
- This causes every difference above 1e-8 in sections 4.2 and 4.3:
  - up to 6.8e-7 in a matched value (S2, m03, where the bracket's two validation losses are only 0.0094 apart);
  - up to 4.5e-5 in an interpolation weight;
  - up to 2.7e-8 in a mean.
- With record losses, targets and weights are identical and the values agree within 4.7e-9.
- The protocol's wording, "the per-draw `train` field", fits the published choice. The brief's "mean training and validation losses" led me to the arrays.
- No label is sensitive to it: the nearest interval limit to 0 is S3's upper limit, −0.00114.

**D4. The t critical value. Numerical.**
- The published value is 2.570581836 (9 decimals); the exact value is 2.5705818356363.
- Recomputing every published interval and leave-one-out interval from the published per-draw values gives a largest difference of 7.2e-13.

**D5. Direction of the descriptive rate effect. Specification ambiguity (Q30).**
- The published value is the 1e-4 arm minus the 3e-4 arm; mine is the reverse.
- The sizes agree within 2.5e-9. The protocol does not state a direction, and the quantity is not gating.

**D6. Mean and interval of the unavailable S2. Specification ambiguity (Q25), in reporting only.**
- The published analysis prints the three values and the sign test, and no interval.
- I computed one and marked it as not read: mean 0.00485, interval [−0.01995, 0.02965], n = 3.
- Label and counts are identical.

**Errors in my implementation:** none found in the frozen code or outputs. The two pre-freeze defects are in section 2. No second pass of the analysis was needed. The only post-freeze code is the comparison and the evidence script, both under `phase2\`.

**Possible errors in the published analysis:** none.

**One documentation remark, not a result:** the bundle README links to `github.com/rafli-hl/sequence-weighting-research`, while the brief names the repository `rafli-hl/sequence-weighting`.

## 6. Code

The main file is 850 lines (37 KB). That is too long to transcribe into this message without risking a mismatch with the frozen hash, so I give paths and hashes instead. All files are under `C:\Users\rafli\AppData\Local\Temp\n7cr`.

| File | SHA-256 | Role |
|---|---|---|
| `code\n7_repro.py` | `004b2841c7b5e16b75732ba727590e1e854fd89c2e51b946a64e205bb528a033` | Frozen: estimator, per-readout table, statistics, labels, diagnostics, self-test |
| `SPEC_LOG.md` | `8900cda094c900e90d5d86c43dec46c2c1b7b437d379b8a2f0406595a7a1043c` | Frozen specification log |
| `FREEZE.txt` | `66b44eb3a545a310aadbd82957479017f15e9a381185a74ce8b790c3a35a232a` | Freeze record |
| `phase2\compare.py` | `20a8cca0e7ae944e064b1b7fceba8cee68f988f2f020a5ad836cf8bb41e76593` | Phase 2 comparison |
| `phase2\second_pass_checks.py` | `cb75b7df44a066ce11946b8748103eb7878ade8139ea2d7ebfd60580745aaa02` | Labelled second pass: evidence for D1–D4 |
| `phase2\COMPARISON.json` | `905221c4a6186df1d8ac5533cd742e8b98aec0e7bfcd1c55401813952f6922a8` | Full comparison, all four variants |
| `phase2\SECOND_PASS_CHECKS.txt` | `6d5491fe206b4dab130501bedbc090e049dc4f637a3924b809b107ed3d6dbf69` | Output of the evidence script |

**Method, in brief:**
- Gains are subtracted in float32, then everything is float64.
- Sequences are sorted by weight with a stable sort. J(p) is (1/N) times the sum of squared cumulative sums of g̃ − b(p), with tie groups entering together in the primary reading.
- J and its analytic derivative are scanned on a grid of step 0.02 over [0, 8]. Each grid minimum is refined by bisection on the derivative to a width below 1e-13, and the lowest candidate wins.
- A golden-section search on J is the cross-check.
- t quantiles come from the regularised incomplete beta function, inverted by bisection.

**Commands** (PowerShell, from the working folder; about 30 s):

```
$PY = "C:\Users\rafli\AppData\Local\Programs\Python\Python312\python.exe"
cd C:\Users\rafli\AppData\Local\Temp\n7cr
& $PY -I -B code\n7_repro.py --bundle phase1\bundle\n7-loss-arrays --out rerun --selftest
& $PY -I -B phase2\compare.py out phase2\published phase2\COMPARISON.json
& $PY -I -B phase2\second_pass_checks.py code phase1\bundle\n7-loss-arrays phase2\published
```

The first command writes to a new folder `rerun`. Its files should hash to the values in `FREEZE.txt`, since the outputs are deterministic and hold no timestamps.

## 7. Limits

- **This is a reproduction by an AI system, not an independent human replication.** It ran on the repository owner's machine, under access rules I followed but that no one else enforced.
- **It reproduces the analysis, not the training.** The per-sequence losses, weights and records are taken as released. I checked them only against the bundle's own manifest, not against the runs, the seed registry, the partition or the terminals.
- **The clean room was not perfect.** I knew N7's labels from my starting context before computing them (section 2). The numerical agreement cannot be explained by that; my choice of readings could in principle have been influenced. The two readings where I differ from the original (Q4, Q12) were logged before any fit was run.
- **Several rules were not exercised by these data:** undefined fits, boundary or multiple minima, saturation refits, exact ties in the matching rule, precedence of unavailability reasons, a failed run, and NOT_READ labels. My readings of those are in the log but are untested against the original.
- **The readings' text of section 7** was not regenerated; I only identified which row applies. The power figures and operational checks of the protocol are outside this exercise.
- **I did not read the original code,** so statements about what it does (ordinal ranks, record losses, a rounded t value) are inferences from the published numbers and the data.
- **Agreement to about 1e-9 shows** that the published tables follow from the released data under the written specification. It says nothing about whether the specification is the right analysis or about the scientific claims.

---

# Supervising session's note

The report above is the reproducing session's, as returned. This note is by the session that launched it. Both are
AI systems (Claude Fable 5.2, Anthropic).

## How the clean room was set up

- **The supervising session is not clean.** It has read N7's code and results many times, so it did not do the
  reproduction. It launched a fresh session with no part in the earlier work.
- **What the fresh session was given:** the brief, verbatim, and the instructions in appendix 3. They contain no
  result of N7 and nothing about its code.
- **What it could not be shielded from:** its starting context included this project's memory index, one line of which
  names N7's labels (quoted in its section 2). It holds no number. The fresh session reported this itself.
- **Where it worked:** a new folder that held only the brief. It was told to read nothing else on the machine.

## What the supervising session checked afterwards

All of this was done after the fresh session's freeze, with `supervisor_check.py` (in the files folder) and a rerun.

| Check | Result |
|---|---|
| The 22 files named in `FREEZE.txt` against their SHA-256 now | All 22 match |
| Order of events on disk | Newest frozen file written 2026-11-23T18:12:20Z; `FREEZE.txt` 18:12:32Z; the four published tables 18:12:42Z–18:12:44Z |
| The session's 42 tool calls, from its transcript | No path on drive D:, none to the owner's clone, Downloads or another working folder; no `git clone`; no web search or fetch tool |
| URLs it requested | Only the protocol, the technical note, and, from 18:12:40Z, the four published tables. The bundle came from `gh release download v1.2` |
| The published tables it compared with | Their SHA-256 equal the hashes N8's `test_on_n7.py` pins for the same four files |
| Rerun of the frozen `code/n7_repro.py` | 16 of 16 frozen output files reproduced byte for byte, in 31 s |
| Rerun of `phase2/compare.py` | The same figures as the report: 240 fits, largest difference in p\* 8.685e-9 (primary) and 2.432e-9 (ordinal ties), none above 1e-6; 36 matched rows with 0 structural mismatches; the same labels |

## On its three inferences about the original analysis

The fresh session did not read the original code, so it stated these as inferences. Each agrees with what the public
record says elsewhere:

- **Tied weights are ranked in stable sort order (its D2).** The external audit of 13 November lists "stable tie
  ordering" among the estimator's explicit conventions (`reports/external-audit-20261113-01/AUDIT.md`, §3.3).
- **Mean losses and matching targets come from the worker's records, not the array means (its D3).** The difference
  between the two is the registered `records_against_arrays` figure, 8.55e-7.
- **The t quantile is a table value rounded to nine decimals (its D4).** N8's `test_synthetic.py` checks "N7's T95
  table, df 2-11 (rounded to 9 decimals)".

## What this adds, and what it leaves open

- **Adds:** an implementation written from the protocol, the technical note and the released data alone gives all 240
  fits within 8.7e-9 and every registered statistic, sign test, leave-one-draw-out side and label of N7.
- **Two places where the written specification does not fix the analysis:** the rank of tied weights, and the source
  of the mean losses. Neither moves any figure by more than 6.8e-7 or any label. The protocol could name both.
- **Leaves open:** everything the reproduction's own section 7 lists. It checks the analysis from the released
  losses. It does not check the training, and it is not an independent human replication.

---

# Appendix 1. The frozen specification log and freeze record

### `SPEC_LOG.md` (SHA-256 `8900cda094c900e90d5d86c43dec46c2c1b7b437d379b8a2f0406595a7a1043c`)

~~~~markdown
# Specification log (clean-room reproduction of N7's analysis)

Written 2026-11-23T18:05Z (machine clock, UTC), before any p\* was computed and before any published table was
fetched. Sources read so far: BRIEF.md, PROTOCOL.md (v2.1 sealed source), the Jane Street technical note (1 page),
the bundle's README.md, MANIFEST.json and one record.json. Data looked at so far: file sizes and hashes, the six
weight vectors (range, mean, number of distinct values), and for draw m01 the record losses beside the array-block
means (to settle Q12). No fit has been run.

Each entry: the question, the reading chosen, the reason. "Variant" means a second reading that is also computed and
frozen, so that a later discrepancy can be attributed.

## A. The estimator

**Q1. In what arithmetic is the gain formed?**
Reading: g_i = E0_train_i − readout_train_i, subtracted in float32 (both operands as stored), then widened to float64.
Everything after that is float64.
Reason: the bundle's README and MANIFEST say so explicitly. The protocol only says "signed gains from each width's own E0".

**Q2. Which E0?**
Reading: the E0.f32 of the same draw and the same width; the two rates of one width share it.
Reason: protocol section 3 ("A width's arms share one E0").

**Q3. Objective.**
Reading: from the note. g~_i = g_i / sum_j g_j; b_i(p) = w_i^p / sum_j w_j^p; d_i = g~_i − b_i(p); r_i = empirical
percentile rank of w_i; K_ij = min(r_i, r_j); J(p) = d' K d. With the sequences sorted by weight this equals
(1/N) * sum over positions of the squared cumulative sum of d (the cumulative discrepancy), because
min(r_i, r_j) = integral over u of 1{r_i >= u} 1{r_j >= u} and sum_i d_i = 0. The factor 1/N does not move the argmin.
Reason: the note's finite-sample estimator; the brief's phrase "cumulative-discrepancy objective over sequences
sorted by weight".

**Q4. Percentile rank when weights are tied.** (The data have ties: 16,381, 16,380, 16,383, 16,383, 16,383, 16,383
distinct float32 values out of 16,384 in m01..m06.)
Reading (primary): the empirical CDF, r_i = #{j : w_j <= w_i} / N, so tied sequences share one rank and enter the
cumulative sum together. J = (1/N) * sum_{k=2..N} C(end of the tie group before position k)^2, C = cumsum of d in
sorted order.
Variant "ordinal": ranks 1..N from a stable ascending sort (ties in sequence order), J = (1/N) * sum_{k=1..N-1} C_k^2.
Reason: the note defines the rank through the CDF F_D(W), under which equal weights have equal rank, and that makes
J independent of an arbitrary ordering of ties. The note does not say what an implementation should do with ties and
the protocol only bounds their number ("at most n / 1,024 tied values"), so this is an ambiguity; a plain
sort-and-cumsum implementation would give the ordinal variant.

**Q5. Which weights?**
Reading: weights.f32 as released (float32, normalised to mean 1), widened to float64; b_i(p) computed as
exp(p * (ln w_i − max ln w)) / sum. In exact arithmetic b is invariant to the scale of w.
Reason: the only weights released. The protocol says "the weights used exactly as drawn"; whether the original fit
used the mean-1 float32 values or the raw draws is not knowable from the allowed sources, and can change p\* only at
rounding level.

**Q6. Range of p.**
Reading: the closed interval [0, 8]. p\* = 0 and p\* = 8 are admissible values (boundary minima).
Reason: protocol section 3 ("p\* from the sealed estimator on [0, 8]"); the note has p >= 0.

**Q7. When is a fit undefined?**
Reading: undefined if (a) the total gain sum_i g_i is not strictly positive, or not finite (the normalisation is
undefined; the note assumes E[G] > 0); (b) all weights are equal (b does not depend on p, so J is constant and has no
unique minimiser); (c) any input or the objective is not finite. An undefined fit has no value and stays undefined.
Reason: the note; protocol section 3 ("Undefined fits stay undefined"). The protocol does not list the conditions.
Disclosure: a project instruction file that was in my starting context (not an allowed source) contains the sentence
"Uniform weights and nonpositive total gain have undefined p\*". It agrees with what I derive from the note; I record
it as a possible influence.

**Q8. Several minima / ties in the objective.**
Reading: the global minimum over [0, 8]. If two candidate minimisers have exactly equal J, the smaller p is taken.
Reason: the protocol does not state a tie rule for the estimator; "argmin" in the note means the global minimum. The
smaller-p rule is my own deterministic choice.

**Q9. Numerical method.**
Reading: (1) evaluate J and dJ/dp analytically on a uniform grid of step 0.02 over the range; (2) every grid point
that is a local minimum of J on the grid gives a bracket (its two neighbours, or the boundary); (3) inside each
bracket the root of dJ/dp is found by bisection to a width below 1e-13 (a boundary point is the candidate when the
derivative does not change sign); (4) the candidate with the lowest J wins. Cross-check: golden-section search on J
itself over the winning bracket; the largest difference between the two methods is reported. A brute-force d'Kd on
subsamples checks the cumulative-sum identity.
Reason: the brief allows any correct method. Root-finding on the derivative avoids the sqrt(eps) limit of
minimising J directly, so p\* is good to far better than 1e-6.

**Q10. Bound flags.**
Reading: at_upper if p\* >= bound − 0.001 (7.999 at bound 8, the protocol's saturation threshold); at_lower if
p\* <= 0.001.
Reason: protocol section 8 gives 7.999; the lower flag and its margin are my choice (section 9 asks for "every fit
with its bound flags" without defining them).

**Q11. Saturation.**
Reading: a draw is flagged for a statistic if any fit that statistic uses for that draw (512 at E3; for a matched
statistic the two bracketing 768 readouts; for a fixed-update statistic 768 at E3) is >= 7.999. Flagged fits are
refitted on [0, 32]. A refit >= 31.999 is "unresolved" and makes the statistic SATURATED. Otherwise the statistic is
recomputed with the refitted values (the bracket itself is not re-chosen, since the bracket depends on losses, not
on p\*); if its side (above / below / spans 0) differs, it is SATURATION_SENSITIVE. Neither is read.
Reason: protocol section 8. "Unresolved" is not defined there; I read it by analogy with the 7.999 rule.

## B. Per-readout quantities

**Q12. What is the "training NLL" (the per-draw `train` field as defined in N6)?**
Reading (primary): the unweighted arithmetic mean, in float64, of the 16,384 float32 training rows of the readout's
array block. Validation NLL: the same over the 512 validation rows. Gap = validation − training.
Variant "record": the `train_loss` and `validation_loss` printed in each record.json.
Reason: N6's definition is not in the allowed sources. For m01 the record's train_loss agrees with the unweighted
block mean to about 1e-6 and is far (0.05 to 0.7) from the weight-weighted mean, so the field is an unweighted mean.
Protocol section 8 speaks of "the mean of the array block the fits use" and treats the record's losses as something
to be compared against it, and the brief says "compute ... the mean training and validation losses", so I compute
them from the arrays. The two sources differ at about 1e-6 (float32 accumulation), which can move a matched reading
only at about 1e-7.

**Q13. Which fits exist?**
Reading: 6 draws x 2 widths x 2 rates x 10 readouts = 240. E0 has zero gain by construction and is not fitted; its
mean losses are reported per width as a descriptive.

## C. Matched contrasts

**Q14. Which arm supplies the target, and which the path?**
Reading: at the statistic's rate, the target is 512's value at E3 and the path is 768's seven readouts E2..E3.5 at
the same rate. D4m_* uses 1e-4 for both; D2m_train uses 3e-4 for both.
Reason: sections 4 to 6 ("512 − 768 at 1e-4", "at 3e-4"). The names D4 and D2 are not defined in the protocol; I
take them from the table in section 6.

**Q15. When does an interval "hold" the target?**
Reading: closed: min(v_a, v_b) <= T <= max(v_a, v_b), compared exactly in float64, no tolerance. Intervals are the six
consecutive pairs (E2,E2.25) ... (E3.25,E3.5), scanned in that order; the first that holds T gives the reading.
Reason: section 4's three tie rules only make sense for closed intervals.

**Q16. Interpolation and "weight".**
Reading: interpolation is linear in the matching variable: weight = (T − v_a) / (v_b − v_a), the weight on the later
readout b; p_read = p_a + weight * (p_b − p_a); read position (epochs) = e_a + weight * (e_b − e_a). If
v_a = v_b = T, weight = 0 (the earlier readout).
Reason: section 4. Whether the published "weight" is the weight on the later or on the earlier readout is not
stated; the comparison will check both w and 1 − w.

**Q17. "The number of intervals holding it".**
Reading: the count of the six closed intervals that hold T (so a target exactly equal to an interior readout's value
counts in both neighbours).
Reason: section 4; my choice for the exact-equality case.

**Q18. "Outside the path".**
Reading: no interval holds T, which is the same as T below the minimum or above the maximum of the seven 768 values.
That draw is unavailable for that statistic, reason "target outside the path". No extrapolation, no use of E1.
Reason: section 4.

**Q19. Unavailability reasons and their precedence.**
Reading: in this order: draw missing; p\*(512, E3) undefined ("undefined fit"); target outside the path; either
bracketing 768 fit undefined ("undefined fit"), even where the weight is exactly 0 or 1.
Reason: sections 4 and 8 name the reasons, not a precedence; the order is mine and matters only if two apply.

**Q20. Matching on the gap.**
Reading: the target is 512's (validation − training) at E3; 768's gap is formed at each of its seven readouts and the
interpolation is linear in the gap.
Reason: section 4.

## D. Statistics, sequence, labels

**Q21. The t interval.**
Reading: mean ± t(0.975, n − 1) * s / sqrt(n), s the sample standard deviation with divisor n − 1, n the number of
available draws. Two-sided 95%.
Reason: sections 5 and 6 ("df = draws − 1, 95%").

**Q22. "Entirely above 0".**
Reading: lower limit > 0 strictly (below: upper limit < 0 strictly). A limit exactly at 0 is INCONCLUSIVE.
Reason: "The interval includes 0" is the INCONCLUSIVE reading in section 7.

**Q23. The exact two-sided sign test.**
Reading: zeros are dropped; with n+ positive and n− negative values, p = min(1, 2 * P(X <= min(n+, n−))),
X ~ Binomial(n+ + n−, 1/2); p = 1 if no nonzero value. Reported for every statistic with at least one value.
Reason: section 8 names the test only.

**Q24. Leave-one-draw-out.**
Reading: when at least 4 draws have a value, for each such draw the t interval of the remaining n − 1 values
(df = n − 2) is reported, with the side of each, and a summary: the least lower limit, the greatest upper limit, and
whether every leave-one-out interval is on the side of the full interval.
Reason: section 8. The summary form is mine.

**Q25. Mean and interval of an UNAVAILABLE statistic.**
Reading: the label is UNAVAILABLE with fewer than 5 available draws. The mean (n >= 1) and interval (n >= 2) are
still computed and stored as not read, since section 8 asks for sign counts, sign test and leave-one-out intervals
"even [for] an unavailable one".
Reason: sections 5, 6, 8.

**Q26. Status versus printed label.**
Reading: each step has a `status` from its own interval alone (P1: REVERSAL_CONFIRMED / NOT_REVERSED / INCONCLUSIVE /
UNAVAILABLE; secondaries: CONFIRMED / CONTRARY / INCONCLUSIVE / UNAVAILABLE, with S3's expected side negative) and a
`side` (above / below / spans / none). The sequence is P1, S1, S3, S4, S5, S2. A step is "reached" if every earlier
step is confirmed (P1: REVERSAL_CONFIRMED; others: CONFIRMED). A reached step's printed label is its status; a step
not reached has the printed label NOT_READ. An UNAVAILABLE step is not confirmed, so it stops the sequence.
Reason: sections 6 and 7 ("The printed labels").

**Q27. Did every run complete?**
Reading: yes if all six draws are present and all 24 arm records have status COMPLETE; the bundle does not contain
the run terminals, so this is the only evidence available to me. If so, the "a run did not complete" branch of
section 8 does not apply.
Reason: section 8; the terminals are not released in the bundle.

**Q28. NOT_OVERFIT.**
Reading: for each of the four arms (width x rate), per draw Delta = validation NLL at E3 − at E2 (array-block means,
Q12); t interval of the mean Delta over the draws (95%, df = n − 1), needing at least 5 draws; entirely below 0:
NOT_OVERFIT; entirely above 0: OVERFIT; otherwise PLATEAU. Arms used by each statistic: P1, S1, S3, S2 use the two
1e-4 arms; S4, S5 the two 3e-4 arms. A reading whose arm is not NOT_OVERFIT is marked "prefixed"; the label stands.
Reason: section 8 and the row "NOT_OVERFIT | At least 5 draws" of section 13.

**Q29. records_against_arrays.**
Reading: the maximum over the 24 arms, the 10 readouts and the two losses of |record value − float64 mean of the
array block|. Above 0.001 gives a warning. E0 is not in the records and is not part of it.
Reason: section 8.

**Q30. Descriptives (section 9).**
Reading: by readout, the fixed-update contrast p\*(512) − p\*(768) at each rate with its t interval; per arm and
readout the mean p\*, losses and gap; the rate effect at each width at E3 as p\*(3e-4) − p\*(1e-4) (the direction is
my choice); clipping per arm as the update-weighted mean of the epochs' clip_fraction (section 13: "weighted by
updates"); E0 mean losses per width; every fit with its bound flags. No multiplicity adjustment.
Reason: section 9.

**Q31. t quantiles without SciPy.**
Reading: the t CDF through the regularised incomplete beta function (Lentz continued fraction), inverted by
bisection to 1e-13; checked against the closed forms for df 1 and 2 and against direct numerical integration of the
t density for df 3, 4, 5.

**Q32. Order of draws.**
Reading: m01..m06 in name order everywhere. Sums over draws are order-dependent only at rounding level.

**Q33. Things the protocol requires that I cannot reproduce from the allowed sources.**
The readings' text (section 7) is determined by the labels; I report which row applies, not the printed text. The
run terminals, the seed registry and the partition are outside the bundle and are not checked.

## Addendum before the freeze (2026-11-23, after my own first run, before any published table was fetched)

**Q34. Does the convention for the rank offset matter?**
No. With sum_i d_i = 0, replacing r_i by r_i + c, or by a positive multiple of it, changes d'Kd by a constant factor
or not at all, so i/N, (i − 1)/N, (i − 0.5)/N and i/(N + 1) all give the same argmin. Only the treatment of ties (Q4)
can change p\*.

**Q35. Number formats.**
My tables print every float with Python's shortest round-trip repr (17 significant digits at most). Comparisons with
published tables will be made at the precision the published tables print.

**What I saw of my own results before freezing.** I ran my code once into a scratch folder and read its output: the
240 fits (all defined, all interior, one candidate minimum each, p\* between 0.038 and 0.149), the six statistics and
the labels. Two defects of my own were fixed at that point, neither a change of reading: the self-test compared
d'Kd with N times the cumulative form (the 1/N is already inside r_i), and the CSV writer printed NumPy scalars as
"np.float64(...)". The ecdf and ordinal tie readings differ by at most 8.8e-9 in p\* on these data, and the array
and record loss sources by at most 8.5e-7 in a loss, so neither ambiguity can move a label here.
~~~~

### `FREEZE.txt` (SHA-256 `66b44eb3a545a310aadbd82957479017f15e9a381185a74ce8b790c3a35a232a`)

~~~~text
FREEZE RECORD - clean-room reproduction of N7's analysis
Frozen at (machine clock, UTC): 2026-11-23T18:12:32Z
Local time: 2026-11-24 01:12:32 +0700
No published table (POINTS.csv, MATCHED.csv, FITS.csv, ANALYSIS.json) had been fetched or read at this time; the phase2 folder did not exist.
After this point code/n7_repro.py, SPEC_LOG.md and everything under out/ are not changed. Any later change goes into a separate, labelled second pass.

Primary variant: out/ecdf_arrays (ties: empirical CDF; losses: float64 means of the array blocks).
Other frozen variants: out/ordinal_arrays, out/ecdf_record, out/ordinal_record.

SHA-256 of the code and the specification log:
004b2841c7b5e16b75732ba727590e1e854fd89c2e51b946a64e205bb528a033 *code/n7_repro.py
8900cda094c900e90d5d86c43dec46c2c1b7b437d379b8a2f0406595a7a1043c *SPEC_LOG.md

SHA-256 of every output file:
b1f6f89a881d19a6188107b686c4d91dceaf97889415d647b21912ab56f03275 *out/ecdf_arrays/analysis.json
b4d6f428ae7ed66fc99f7e1f69b87efe49073807fc1678790829c6bafe4222a3 *out/ecdf_arrays/contrasts.csv
e56ef497d8dd403d9b36bac04ba2fdb177cb19868194f62a6014373d5075da86 *out/ecdf_arrays/matched.csv
9f2749d5dfe9ec390667de24351b104789510718e4a9ef4c1ec623a7991b724e *out/ecdf_arrays/per_readout.csv
94277915fcb855724bd3fdd135f04ccadc2c2b05e4795bd3e66de2f27c8f74f9 *out/ecdf_record/analysis.json
1bb4b85cf339f12b00afb0c90c49ebd93ae7f373784b4577eb9e1cf588deaa2f *out/ecdf_record/contrasts.csv
3dfdce4409239299923d715f1574e662217f37076913a751528da582730d31ca *out/ecdf_record/matched.csv
d3ba54b445f537ae589036121184a6b221e3d219e4a89c27ebb905fd17638da2 *out/ecdf_record/per_readout.csv
a519cbda502dd568b959253a1256535dca5f7d671dc9a48406f71be4c7aa3fd0 *out/ordinal_arrays/analysis.json
c64eb0f9a7418f3062ac2eb6ed23a675a286268d7951c844b8cafe2748370af3 *out/ordinal_arrays/contrasts.csv
9a3f92cb172b7a3c036aa4d7df6a784bead28cf400f23d97d68b0d9c89b4003f *out/ordinal_arrays/matched.csv
83e7f9c5f6a23769b436c6c7712ff621d0814515f7120d95063a65b2c7f617e4 *out/ordinal_arrays/per_readout.csv
73b89d25c00fa393504345f95d95f723c016fc9cbd074fecb859c16a3cb6771d *out/ordinal_record/analysis.json
0d87368db359c342afe2c0e71cf1943404ac5558bb0dfa21fc7caf5cfcd28057 *out/ordinal_record/contrasts.csv
c122a8f795d87d034cd7098a7ba028a1923d8c0505ab88ab5fa1adb4ec8a4474 *out/ordinal_record/matched.csv
5219a14acf6b16d9bbb815961bf649223ef40212027a679b2110e8bc334d7e9a *out/ordinal_record/per_readout.csv

SHA-256 of the inputs:
41584c8335ab040eeaf5550243b2edd4357cc31634b949113d57b409b255f985 *BRIEF.md
adf006ba144efccbf54710dc0c3ae56cba9b66d105c0d25624e5b8e1348dd23e *phase1/protocol/PROTOCOL.md
f7728b89b9c083c88b70f89c9da2a33ecc147e43007faa3aff374c3feafed346 *phase1/note/sequence-weighting-note.pdf
cbe26760e2062a4cf03307d779226fa6efce8cfcfbf57b2e092bd818af80b8a9 *phase1/bundle/n7-loss-arrays-v1.zip

Environment: Python 3.12.10 | NumPy 2.5.3 | Windows-11-10.0.26300-SP0
Command: python -I -B code/n7_repro.py --bundle phase1/bundle/n7-loss-arrays --out out --selftest (run twice; both runs gave byte-identical outputs)
~~~~

---

# Appendix 2. Complete code

The first file is frozen. The others were written after the freeze, for the comparison and its evidence.

### `code/n7_repro.py` (SHA-256 `004b2841c7b5e16b75732ba727590e1e854fd89c2e51b946a64e205bb528a033`)

~~~~python
#!/usr/bin/env python
"""Clean-room reproduction of the analysis of N7 (matched-progress confirmation).

Written from PROTOCOL.md (v2.1 sealed source), the Jane Street technical note and the released bundle
n7-loss-arrays-v1.zip only. NumPy only. See SPEC_LOG.md for every reading of the specification (Q1..Q33).

Usage:
    python -I -B n7_repro.py --bundle <path to n7-loss-arrays> --out <output folder> [--selftest]

Writes, for each of four variants (ties in {ecdf, ordinal} x losses in {arrays, record}):
    <out>/<variant>/per_readout.csv   one row per draw, width, rate, readout (240 rows)
    <out>/<variant>/matched.csv       one row per matched statistic and draw
    <out>/<variant>/contrasts.csv     one row per registered statistic and draw
    <out>/<variant>/analysis.json     statistics, sequence, labels, diagnostics, descriptives
The primary variant is ecdf_arrays.
"""
import argparse
import csv
import hashlib
import json
import math
import os
import sys

import numpy as np

N_TRAIN = 16384
N_VAL = 512
READOUTS = [0.25, 0.5, 1, 2, 2.25, 2.5, 2.75, 3, 3.25, 3.5]
PATH = [2, 2.25, 2.5, 2.75, 3, 3.25, 3.5]
E3 = 3
E2 = 2
DRAWS = ["m01", "m02", "m03", "m04", "m05", "m06"]
WIDTHS = [512, 768]
RATES = ["lr1e-04", "lr3e-04"]
BOUND = 8.0
REFIT_BOUND = 32.0
SAT_MARGIN = 0.001
GRID_STEP = 0.02
MIN_DRAWS = 5

# (step, name, kind, rate, matching variable, expected side)
STATISTICS = [
    ("P1", "D4m_train", "matched", "lr1e-04", "train", "above"),
    ("S1", "D4m_gap", "matched", "lr1e-04", "gap", "above"),
    ("S3", "D4_fixed_E3", "fixed", "lr1e-04", None, "below"),
    ("S4", "D2m_train", "matched", "lr3e-04", "train", "above"),
    ("S5", "D2_fixed_E3", "fixed", "lr3e-04", None, "above"),
    ("S2", "D4m_val", "matched", "lr1e-04", "val", "above"),
]


# ----------------------------------------------------------------------------------------------
# t distribution (no SciPy): regularised incomplete beta by Lentz's continued fraction
# ----------------------------------------------------------------------------------------------
def _betacf(a, b, x):
    tiny = 1e-300
    qab, qap, qam = a + b, a + 1.0, a - 1.0
    c = 1.0
    d = 1.0 - qab * x / qap
    if abs(d) < tiny:
        d = tiny
    d = 1.0 / d
    h = d
    for m in range(1, 10000):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        if abs(d) < tiny:
            d = tiny
        c = 1.0 + aa / c
        if abs(c) < tiny:
            c = tiny
        d = 1.0 / d
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        if abs(d) < tiny:
            d = tiny
        c = 1.0 + aa / c
        if abs(c) < tiny:
            c = tiny
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < 1e-16:
            return h
    raise RuntimeError("betacf did not converge")


def betai(a, b, x):
    if x <= 0.0:
        return 0.0
    if x >= 1.0:
        return 1.0
    front = math.exp(a * math.log(x) + b * math.log1p(-x) - (math.lgamma(a) + math.lgamma(b) - math.lgamma(a + b)))
    if x < (a + 1.0) / (a + b + 2.0):
        return front * _betacf(a, b, x) / a
    return 1.0 - front * _betacf(b, a, 1.0 - x) / b


def t_cdf(t, df):
    tail = 0.5 * betai(0.5 * df, 0.5, df / (df + t * t))
    return 1.0 - tail if t >= 0 else tail


def t_ppf(q, df):
    """Quantile for q > 0.5 by bisection on the CDF."""
    lo, hi = 0.0, 1.0
    while t_cdf(hi, df) < q:
        hi *= 2.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if t_cdf(mid, df) < q:
            lo = mid
        else:
            hi = mid
        if hi - lo < 1e-13:
            break
    return 0.5 * (lo + hi)


_TCRIT = {}


def t_crit(df):
    if df not in _TCRIT:
        _TCRIT[df] = t_ppf(0.975, df)
    return _TCRIT[df]


# ----------------------------------------------------------------------------------------------
# The estimator
# ----------------------------------------------------------------------------------------------
class Fitter:
    """p* = argmin over [0, bound] of d(p)' K d(p), K_ij = min(r_i, r_j), for one weight vector.

    ties = "ecdf":    r_i = #{j: w_j <= w_i} / N (tied weights share a rank)       [primary, Q4]
    ties = "ordinal": r_i = position in a stable ascending sort / N                [variant, Q4]
    In both cases J(p) = (1/N) * sum_k C[idx_k]^2 with C the cumulative sum of d in sorted order.
    """

    def __init__(self, weights_f32, ties):
        w = np.asarray(weights_f32).astype(np.float64)
        if not np.all(np.isfinite(w)) or np.any(w <= 0):
            raise ValueError("weights must be finite and positive")
        self.n = w.size
        self.order = np.argsort(w, kind="stable")
        ws = w[self.order]
        self.uniform = bool(ws[0] == ws[-1])
        lw = np.log(ws)
        self.lw = lw - lw[-1]
        new = np.empty(self.n, dtype=bool)
        new[0] = True
        new[1:] = ws[1:] != ws[:-1]
        self.n_distinct = int(new.sum())
        if ties == "ecdf":
            gid = np.cumsum(new) - 1
            ends = np.flatnonzero(np.append(new[1:], True))
            k = np.flatnonzero(gid >= 1)
            self.idx = ends[gid[k] - 1]
        elif ties == "ordinal":
            self.idx = np.arange(self.n - 1)
        else:
            raise ValueError(ties)
        self.ties = ties
        self._cache = {}

    def _basis(self, ps):
        e = np.exp(np.outer(ps, self.lw))
        b = e / e.sum(axis=1, keepdims=True)
        mu = (b * self.lw).sum(axis=1, keepdims=True)
        cb = np.cumsum(b, axis=1)[:, self.idx]
        dcb = np.cumsum(b * (self.lw - mu), axis=1)[:, self.idx]
        return cb, dcb

    def scan(self, gt, bound):
        """J and dJ/dp on the uniform grid (used only to find brackets)."""
        npts = int(round(bound / GRID_STEP)) + 1
        grid = np.linspace(0.0, bound, npts)
        cg = np.cumsum(gt)[self.idx]
        j = np.empty(npts)
        dj = np.empty(npts)
        chunk = 96
        for start in range(0, npts, chunk):
            sl = slice(start, min(start + chunk, npts))
            key = (bound, start)
            if bound == BOUND:
                if key not in self._cache:
                    self._cache[key] = self._basis(grid[sl])
                cb, dcb = self._cache[key]
            else:
                cb, dcb = self._basis(grid[sl])
            r = cg - cb
            j[sl] = np.einsum("ij,ij->i", r, r) / self.n
            dj[sl] = -2.0 * np.einsum("ij,ij->i", r, dcb) / self.n
        return grid, j, dj

    def exact(self, gt, p):
        """J(p) and dJ/dp at one p, from the cumulative sum of d itself."""
        e = np.exp(p * self.lw)
        b = e / e.sum()
        mu = float((b * self.lw).sum())
        c = np.cumsum(gt - b)[self.idx]
        dc = -np.cumsum(b * (self.lw - mu))[self.idx]
        return float(np.dot(c, c)) / self.n, 2.0 * float(np.dot(c, dc)) / self.n

    def fit(self, gain, bound=BOUND):
        """gain: float64 array in sequence order. Returns a dict; 'defined' False with a reason if undefined."""
        g = np.asarray(gain, dtype=np.float64)
        out = {"defined": False, "reason": "", "p": None, "objective": None, "bound": bound,
               "n_candidates": 0, "p_golden": None, "total_gain": None}
        if not np.all(np.isfinite(g)):
            out["reason"] = "nonfinite gain"
            return out
        total = float(g.sum())
        out["total_gain"] = total
        if not (total > 0.0):
            out["reason"] = "nonpositive total gain"
            return out
        if self.uniform:
            out["reason"] = "uniform weights"
            return out
        gt = (g / total)[self.order]
        grid, j, dj = self.scan(gt, bound)
        if not (np.all(np.isfinite(j)) and np.all(np.isfinite(dj))):
            out["reason"] = "nonfinite objective"
            return out
        last = grid.size - 1
        cands = []
        for k in range(grid.size):
            if k > 0 and j[k] > j[k - 1]:
                continue
            if k < last and j[k] > j[k + 1]:
                continue
            lo_i, hi_i = max(k - 1, 0), min(k + 1, last)
            br = None
            if lo_i < k and dj[lo_i] < 0.0 <= dj[k]:
                br = (grid[lo_i], grid[k])
            elif k < hi_i and dj[k] < 0.0 < dj[hi_i]:
                br = (grid[k], grid[hi_i])
            if br is not None:
                p = self._bisect(gt, br[0], br[1])
            elif k == 0 and dj[0] >= 0.0:
                p = 0.0
            elif k == last and dj[last] <= 0.0:
                p = float(bound)
            else:
                p = float(grid[k])
            cands.append((self.exact(gt, p)[0], p, (float(grid[lo_i]), float(grid[hi_i]))))
        cands.sort(key=lambda c: (c[0], c[1]))
        jbest, pbest, bracket = cands[0]
        out.update(defined=True, p=float(pbest), objective=float(jbest), n_candidates=len(cands),
                   p_golden=float(self._golden(gt, bracket[0], bracket[1])))
        return out

    def _bisect(self, gt, lo, hi):
        for _ in range(200):
            mid = 0.5 * (lo + hi)
            if self.exact(gt, mid)[1] < 0.0:
                lo = mid
            else:
                hi = mid
            if hi - lo < 1e-13:
                break
        return 0.5 * (lo + hi)

    def _golden(self, gt, a, b):
        """Independent cross-check: golden-section search on J itself."""
        invphi = (math.sqrt(5.0) - 1.0) / 2.0
        c = b - invphi * (b - a)
        d = a + invphi * (b - a)
        fc = self.exact(gt, c)[0]
        fd = self.exact(gt, d)[0]
        for _ in range(200):
            if b - a < 1e-10:
                break
            if fc < fd:
                b, d, fd = d, c, fc
                c = b - invphi * (b - a)
                fc = self.exact(gt, c)[0]
            else:
                a, c, fc = c, d, fd
                d = a + invphi * (b - a)
                fd = self.exact(gt, d)[0]
        return 0.5 * (a + b)


# ----------------------------------------------------------------------------------------------
# Loading
# ----------------------------------------------------------------------------------------------
def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def load_bundle(root):
    """Checks every file against MANIFEST.json and returns the raw arrays and records."""
    with open(os.path.join(root, "MANIFEST.json"), encoding="utf-8") as f:
        man = json.load(f)
    checked = 0

    def check(ent):
        nonlocal checked
        p = os.path.join(root, *ent["path"].split("/"))
        if os.path.getsize(p) != ent["bytes"] or sha256_file(p) != ent["sha256"]:
            raise RuntimeError("manifest mismatch: " + ent["path"])
        checked += 1
        return p

    data = {}
    for draw in sorted(man["draws"]):
        md = man["draws"][draw]
        if md["n_train"] != N_TRAIN or md["readouts"] != READOUTS:
            raise RuntimeError("unexpected layout in " + draw)
        w = np.fromfile(check(md["weights"]), dtype="<f4")
        if w.size != N_TRAIN:
            raise RuntimeError("weights size")
        dd = {"weights": w, "run": md["run"], "widths": {}}
        for width in WIDTHS:
            mw = md["widths"][str(width)]
            e0 = np.fromfile(check(mw["E0"]), dtype="<f4")
            if e0.size != N_TRAIN + N_VAL:
                raise RuntimeError("E0 size")
            dw = {"E0": e0, "arms": {}}
            for rate in RATES:
                ma = mw["arms"][rate]
                arr = np.fromfile(check(ma["arrays"]), dtype="<f4")
                if arr.size != len(READOUTS) * (N_TRAIN + N_VAL):
                    raise RuntimeError("arrays size")
                with open(check(ma["record"]), encoding="utf-8") as f:
                    rec = json.load(f)
                if rec["layout"]["block_epochs"] != READOUTS or rec["layout"]["train_rows"] != N_TRAIN \
                        or rec["layout"]["validation_rows"] != N_VAL or rec["width"] != width or rec["tag"] != rate \
                        or rec["stage"] != draw or [r["epoch"] for r in rec["readouts"]] != READOUTS:
                    raise RuntimeError("unexpected record in %s %s %s" % (draw, width, rate))
                dw["arms"][rate] = {"arrays": arr.reshape(len(READOUTS), N_TRAIN + N_VAL), "record": rec}
            dd["widths"][width] = dw
        data[draw] = dd
    return data, checked


# ----------------------------------------------------------------------------------------------
# Per-readout quantities (fits for both tie readings, losses from both sources)
# ----------------------------------------------------------------------------------------------
def compute_points(data, log=print):
    points = {}  # key (draw, width, rate, readout) -> dict
    e0 = {}
    for draw in sorted(data):
        dd = data[draw]
        fitters = {t: Fitter(dd["weights"], t) for t in ("ecdf", "ordinal")}
        for width in WIDTHS:
            dw = dd["widths"][width]
            e0_train = dw["E0"][:N_TRAIN]
            e0[(draw, width)] = {"train": float(e0_train.astype(np.float64).mean()),
                                 "val": float(dw["E0"][N_TRAIN:].astype(np.float64).mean())}
            for rate in RATES:
                arm = dw["arms"][rate]
                for k, epoch in enumerate(READOUTS):
                    block = arm["arrays"][k]
                    gain32 = e0_train - block[:N_TRAIN]          # float32 subtraction (Q1)
                    assert gain32.dtype == np.float32
                    gain = gain32.astype(np.float64)
                    rec = arm["record"]["readouts"][k]
                    pt = {
                        "draw": draw, "width": width, "rate": rate, "readout": epoch, "update": rec["update"],
                        "train_array": float(block[:N_TRAIN].astype(np.float64).mean()),
                        "val_array": float(block[N_TRAIN:].astype(np.float64).mean()),
                        "train_record": float(rec["train_loss"]),
                        "val_record": float(rec["validation_loss"]),
                        "fit": {t: fitters[t].fit(gain) for t in fitters},
                        "gain": gain,
                    }
                    points[(draw, width, rate, epoch)] = pt
            log("fitted %s w%d" % (draw, width))
        for f in fitters.values():
            f._cache.clear()
    return points, e0


# ----------------------------------------------------------------------------------------------
# Statistics helpers
# ----------------------------------------------------------------------------------------------
def side_of(lo, hi):
    if lo is None or hi is None:
        return "none"
    if lo > 0.0:
        return "above"
    if hi < 0.0:
        return "below"
    return "spans"


def t_interval(vals):
    n = len(vals)
    out = {"n": n, "mean": None, "sd": None, "df": None, "t_crit": None, "ci_low": None, "ci_high": None}
    if n >= 1:
        a = np.asarray(vals, dtype=np.float64)
        out["mean"] = float(a.mean())
    if n >= 2:
        sd = float(a.std(ddof=1))
        tc = t_crit(n - 1)
        half = tc * sd / math.sqrt(n)
        out.update(sd=sd, df=n - 1, t_crit=tc, ci_low=out["mean"] - half, ci_high=out["mean"] + half)
    out["side"] = side_of(out["ci_low"], out["ci_high"])
    return out


def sign_test(vals):
    pos = sum(1 for v in vals if v > 0)
    neg = sum(1 for v in vals if v < 0)
    zero = sum(1 for v in vals if v == 0)
    m = pos + neg
    if m == 0:
        p = 1.0 if vals else None
    else:
        k = min(pos, neg)
        p = min(1.0, 2.0 * sum(math.comb(m, i) for i in range(k + 1)) / 2.0 ** m)
    return {"positive": pos, "negative": neg, "zero": zero, "p_two_sided": p}


def leave_one_out(draws, vals, full_side):
    if len(vals) < 4:
        return None
    rows = []
    for i, d in enumerate(draws):
        rest = [v for j, v in enumerate(vals) if j != i]
        ti = t_interval(rest)
        rows.append({"dropped": d, "n": ti["n"], "mean": ti["mean"], "ci_low": ti["ci_low"],
                     "ci_high": ti["ci_high"], "side": ti["side"]})
    return {"intervals": rows,
            "min_ci_low": min(r["ci_low"] for r in rows),
            "max_ci_high": max(r["ci_high"] for r in rows),
            "all_on_full_side": all(r["side"] == full_side for r in rows)}


def status_of(step, side, n, expected):
    if n < MIN_DRAWS:
        return "UNAVAILABLE"
    if step == "P1":
        return {"above": "REVERSAL_CONFIRMED", "below": "NOT_REVERSED"}.get(side, "INCONCLUSIVE")
    if side == "spans":
        return "INCONCLUSIVE"
    return "CONFIRMED" if side == expected else "CONTRARY"


def matched_reading(target, values, epochs):
    """First closed interval in readout order whose two values hold the target (Q15..Q18)."""
    holds = [min(values[i], values[i + 1]) <= target <= max(values[i], values[i + 1])
             for i in range(len(values) - 1)]
    n_hold = sum(holds)
    if n_hold == 0:
        where = "below the path's minimum" if target < min(values) else "above the path's maximum"
        return {"held": False, "n_intervals": 0, "where": where}
    i = holds.index(True)
    a, b = values[i], values[i + 1]
    weight = 0.0 if a == b else (target - a) / (b - a)
    return {"held": True, "n_intervals": n_hold, "index": i, "lo": epochs[i], "hi": epochs[i + 1],
            "weight": weight, "position": epochs[i] + weight * (epochs[i + 1] - epochs[i])}


# ----------------------------------------------------------------------------------------------
# The analysis for one variant
# ----------------------------------------------------------------------------------------------
def analyse(data, points, e0, ties, losses):
    draws_present = sorted(data)

    def loss(draw, width, rate, epoch, var):
        pt = points[(draw, width, rate, epoch)]
        tr, va = pt["train_" + losses], pt["val_" + losses]
        return {"train": tr, "val": va, "gap": va - tr}[var]

    def fit(draw, width, rate, epoch):
        return points[(draw, width, rate, epoch)]["fit"][ties]

    refits = {}

    def refit(draw, width, rate, epoch):
        key = (draw, width, rate, epoch)
        if key not in refits:
            f = Fitter(data[draw]["weights"], ties)
            refits[key] = f.fit(points[key]["gain"], bound=REFIT_BOUND)
        return refits[key]

    def stat_draw(kind, rate, var, draw, pfun):
        """One draw's value for one statistic. pfun(draw, width, rate, epoch) -> fit dict."""
        row = {"draw": draw, "status": "AVAILABLE", "reason": "", "value": None, "fits_used": []}
        if draw not in data:
            row.update(status="UNAVAILABLE", reason="draw missing")
            return row
        f512 = pfun(draw, 512, rate, E3)
        row["p512_E3"] = f512["p"]
        if kind == "matched":
            target = loss(draw, 512, rate, E3, var)
            vals = [loss(draw, 768, rate, e, var) for e in PATH]
            rd = matched_reading(target, vals, PATH)
            row.update(target=target, path_values=vals, n_intervals=rd["n_intervals"])
            if not f512["defined"]:
                row.update(status="UNAVAILABLE", reason="undefined fit")
                return row
            if not rd["held"]:
                row.update(status="UNAVAILABLE", reason="target outside the path", where=rd["where"])
                return row
            fa, fb = pfun(draw, 768, rate, rd["lo"]), pfun(draw, 768, rate, rd["hi"])
            row.update(bracket_lo=rd["lo"], bracket_hi=rd["hi"], weight=rd["weight"], position=rd["position"],
                       p768_lo=fa["p"], p768_hi=fb["p"])
            if not (fa["defined"] and fb["defined"]):
                row.update(status="UNAVAILABLE", reason="undefined fit")
                return row
            read = fa["p"] + rd["weight"] * (fb["p"] - fa["p"])
            row.update(p768_read=read, value=f512["p"] - read,
                       fits_used=[(512, rate, E3), (768, rate, rd["lo"]), (768, rate, rd["hi"])])
        else:
            f768 = pfun(draw, 768, rate, E3)
            row["p768_E3"] = f768["p"]
            if not (f512["defined"] and f768["defined"]):
                row.update(status="UNAVAILABLE", reason="undefined fit")
                return row
            row.update(value=f512["p"] - f768["p"], fits_used=[(512, rate, E3), (768, rate, E3)])
        return row

    stats = {}
    matched_rows = []
    contrast_rows = []
    confirmed_so_far = True
    for step, name, kind, rate, var, expected in STATISTICS:
        rows = [stat_draw(kind, rate, var, d, fit) for d in DRAWS]
        avail = [r for r in rows if r["status"] == "AVAILABLE"]
        ds = [r["draw"] for r in avail]
        vals = [r["value"] for r in avail]
        ti = t_interval(vals)
        status = status_of(step, ti["side"], ti["n"], expected)
        counts = {"undefined fit": 0, "target outside the path": 0, "draw missing": 0}
        for r in rows:
            if r["status"] != "AVAILABLE":
                counts[r["reason"]] += 1
        # saturation (Q11)
        flagged = []
        for r in avail:
            hit = [k for k in r["fits_used"] if fit(r["draw"], *k)["p"] >= BOUND - SAT_MARGIN]
            if hit:
                flagged.append({"draw": r["draw"], "fits": [list(k) for k in hit]})
        sat = {"flagged": flagged, "label": None}
        if flagged:
            unresolved = False
            for fl in flagged:
                for k in fl["fits"]:
                    rf = refit(fl["draw"], *k)
                    if (not rf["defined"]) or rf["p"] >= REFIT_BOUND - SAT_MARGIN:
                        unresolved = True

            def pfun32(draw, width, rate_, epoch):
                f8 = fit(draw, width, rate_, epoch)
                if f8["defined"] and f8["p"] >= BOUND - SAT_MARGIN:
                    return refit(draw, width, rate_, epoch)
                return f8
            rows32 = [stat_draw(kind, rate, var, d, pfun32) for d in DRAWS]
            ti32 = t_interval([r["value"] for r in rows32 if r["status"] == "AVAILABLE"])
            sat.update(unresolved=unresolved, interval_at_32=ti32)
            if unresolved:
                sat["label"] = "SATURATED"
            elif ti32["side"] != ti["side"]:
                sat["label"] = "SATURATION_SENSITIVE"
        reached = confirmed_so_far
        label = status if reached else "NOT_READ"
        if sat["label"] and reached:
            label = sat["label"]
        is_confirmed = reached and sat["label"] is None and status in ("REVERSAL_CONFIRMED", "CONFIRMED")
        confirmed_so_far = confirmed_so_far and is_confirmed
        stats[step] = {
            "step": step, "name": name, "kind": kind, "rate": rate, "matched_on": var, "expected_side": expected,
            "n_available": ti["n"], "available_draws": ds,
            "unavailable": {r["draw"]: r["reason"] for r in rows if r["status"] != "AVAILABLE"},
            "unavailable_counts": counts,
            "values": {r["draw"]: r["value"] for r in rows},
            "mean": ti["mean"], "sd": ti["sd"], "df": ti["df"], "t_crit": ti["t_crit"],
            "ci_low": ti["ci_low"], "ci_high": ti["ci_high"], "side": ti["side"],
            "status": status, "reached": reached, "label": label,
            "sign_test": sign_test(vals), "leave_one_out": leave_one_out(ds, vals, ti["side"]),
            "saturation": sat,
        }
        for r in rows:
            contrast_rows.append([step, name, r["draw"], r["status"], r["reason"], r["value"]])
            if kind == "matched":
                matched_rows.append([step, name, var, rate, r["draw"], r["status"], r["reason"], r.get("target"),
                                     r.get("n_intervals"), r.get("bracket_lo"), r.get("bracket_hi"),
                                     r.get("weight"), r.get("position"), r.get("p768_lo"), r.get("p768_hi"),
                                     r.get("p768_read"), r.get("p512_E3"), r["value"], r.get("where", "")]
                                    + list(r.get("path_values", [None] * len(PATH))))

    # runs complete? (Q27)
    all_complete = len(draws_present) == len(DRAWS) and all(
        data[d]["widths"][w]["arms"][r]["record"]["status"] == "COMPLETE"
        for d in draws_present for w in WIDTHS for r in RATES)

    # records against arrays (Q29)
    worst = (0.0, None)
    for key, pt in points.items():
        for var in ("train", "val"):
            diff = abs(pt[var + "_record"] - pt[var + "_array"])
            if diff > worst[0]:
                worst = (diff, [key[0], key[1], key[2], key[3], var])
    rec_vs_arr = {"max_abs_difference": worst[0], "where": worst[1], "threshold": 0.001, "warning": worst[0] > 0.001}

    # NOT_OVERFIT (Q28)
    not_overfit = {}
    for width in WIDTHS:
        for rate in RATES:
            deltas = {d: loss(d, width, rate, E3, "val") - loss(d, width, rate, E2, "val") for d in draws_present}
            ti = t_interval(list(deltas.values()))
            if ti["n"] < MIN_DRAWS:
                lab = "UNAVAILABLE"
            else:
                lab = {"below": "NOT_OVERFIT", "above": "OVERFIT"}.get(ti["side"], "PLATEAU")
            not_overfit["w%d_%s" % (width, rate)] = {"delta": deltas, "n": ti["n"], "mean": ti["mean"],
                                                     "ci_low": ti["ci_low"], "ci_high": ti["ci_high"], "label": lab}
    for step, name, kind, rate, var, expected in STATISTICS:
        arms = ["w%d_%s" % (w, rate) for w in WIDTHS]
        stats[step]["arms_used"] = arms
        stats[step]["reading_prefixed"] = any(not_overfit[a]["label"] != "NOT_OVERFIT" for a in arms)

    # which row of section 7 applies
    p1, s1, s3 = stats["P1"], stats["S1"], stats["S3"]
    if not all_complete and p1["n_available"] < MIN_DRAWS:
        row7 = "A run did not complete, and P1 has fewer than 5 available draws"
    elif p1["label"] == "REVERSAL_CONFIRMED":
        if not s3["reached"]:
            row7 = "REVERSAL_CONFIRMED, with the sequence stopped before S3"
        elif s3["label"] == "CONFIRMED":
            row7 = "REVERSAL_CONFIRMED, with S3 reached and CONFIRMED"
        elif s3["label"] == "CONTRARY":
            row7 = "REVERSAL_CONFIRMED, with S3 reached and CONTRARY"
        else:
            row7 = "REVERSAL_CONFIRMED, with S3 reached and INCONCLUSIVE or unreadable"
    else:
        row7 = p1["label"]

    # descriptives (Q30)
    desc = {"fixed_update_by_readout": {}, "panel": {}, "rate_effect_at_E3": {}, "clipping": {}, "e0": {}}
    for rate in RATES:
        for epoch in READOUTS:
            vals, ds = [], []
            for d in draws_present:
                a, b = fit(d, 512, rate, epoch), fit(d, 768, rate, epoch)
                if a["defined"] and b["defined"]:
                    vals.append(a["p"] - b["p"])
                    ds.append(d)
            ti = t_interval(vals)
            desc["fixed_update_by_readout"]["%s_E%g" % (rate, epoch)] = {
                "values": dict(zip(ds, vals)), "n": ti["n"], "mean": ti["mean"], "ci_low": ti["ci_low"],
                "ci_high": ti["ci_high"], "side": ti["side"]}
    for width in WIDTHS:
        for rate in RATES:
            arm = "w%d_%s" % (width, rate)
            for epoch in READOUTS:
                ps = [fit(d, width, rate, epoch)["p"] for d in draws_present if fit(d, width, rate, epoch)["defined"]]
                desc["panel"]["%s_E%g" % (arm, epoch)] = {
                    "n_defined": len(ps),
                    "p_star": float(np.mean(ps)) if ps else None,
                    "train": float(np.mean([loss(d, width, rate, epoch, "train") for d in draws_present])),
                    "val": float(np.mean([loss(d, width, rate, epoch, "val") for d in draws_present])),
                    "gap": float(np.mean([loss(d, width, rate, epoch, "gap") for d in draws_present]))}
            clip = {}
            for d in draws_present:
                eps = data[d]["widths"][width]["arms"][rate]["record"]["epochs"]
                upd = sum(e["updates"] for e in eps)
                clip[d] = {"clip_fraction": sum(e["clip_fraction"] * e["updates"] for e in eps) / upd,
                           "gradient_norm_mean": sum(e["gradient_norm_mean"] * e["updates"] for e in eps) / upd,
                           "gradient_norm_max": max(e["gradient_norm_max"] for e in eps), "updates": upd}
            desc["clipping"][arm] = {"per_draw": clip,
                                     "clip_fraction_mean": float(np.mean([c["clip_fraction"] for c in clip.values()]))}
        vals, ds = [], []
        for d in draws_present:
            a, b = fit(d, width, "lr3e-04", E3), fit(d, width, "lr1e-04", E3)
            if a["defined"] and b["defined"]:
                vals.append(a["p"] - b["p"])
                ds.append(d)
        ti = t_interval(vals)
        desc["rate_effect_at_E3"]["w%d_3e-4_minus_1e-4" % width] = {
            "values": dict(zip(ds, vals)), "n": ti["n"], "mean": ti["mean"], "ci_low": ti["ci_low"],
            "ci_high": ti["ci_high"], "side": ti["side"]}
        desc["e0"]["w%d" % width] = {"per_draw": {d: e0[(d, width)] for d in draws_present},
                                     "train_mean": float(np.mean([e0[(d, width)]["train"] for d in draws_present])),
                                     "val_mean": float(np.mean([e0[(d, width)]["val"] for d in draws_present]))}

    fits = [points[k]["fit"][ties] for k in points]
    fit_summary = {
        "n_fits": len(fits), "n_defined": sum(1 for f in fits if f["defined"]),
        "n_at_upper": sum(1 for f in fits if f["defined"] and f["p"] >= BOUND - SAT_MARGIN),
        "n_at_lower": sum(1 for f in fits if f["defined"] and f["p"] <= SAT_MARGIN),
        "n_multiple_candidates": sum(1 for f in fits if f["defined"] and f["n_candidates"] > 1),
        "max_abs_bisection_minus_golden": max(abs(f["p"] - f["p_golden"]) for f in fits if f["defined"]),
        "p_min": min(f["p"] for f in fits if f["defined"]), "p_max": max(f["p"] for f in fits if f["defined"]),
    }
    analysis = {
        "variant": {"ties": ties, "losses": losses},
        "draws_present": draws_present, "runs": {d: data[d]["run"] for d in draws_present},
        "every_run_complete": all_complete,
        "sequence": [s[0] for s in STATISTICS],
        "labels": {s[0]: stats[s[0]]["label"] for s in STATISTICS},
        "statuses": {s[0]: stats[s[0]]["status"] for s in STATISTICS},
        "section7_row": row7,
        "statistics": stats,
        "records_against_arrays": rec_vs_arr,
        "not_overfit": not_overfit,
        "fit_summary": fit_summary,
        "descriptives": desc,
        "t_crit": {str(df): t_crit(df) for df in (2, 3, 4, 5)},
    }
    return analysis, matched_rows, contrast_rows


def fmt(v):
    if v is None:
        return ""
    if isinstance(v, bool):
        return "1" if v else "0"
    if isinstance(v, float):
        return repr(float(v))
    return str(v)


def write_csv(path, header, rows):
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(header)
        for r in rows:
            w.writerow([fmt(v) for v in r])


def write_variant(outdir, points, ties, losses, analysis, matched_rows, contrast_rows):
    os.makedirs(outdir, exist_ok=True)
    rows = []
    for draw in DRAWS:
        for width in WIDTHS:
            for rate in RATES:
                for epoch in READOUTS:
                    pt = points.get((draw, width, rate, epoch))
                    if pt is None:
                        continue
                    f = pt["fit"][ties]
                    tr, va = pt["train_" + losses], pt["val_" + losses]
                    rows.append([draw, width, rate, epoch, pt["update"], f["defined"], f["reason"], f["p"],
                                 f["objective"],
                                 f["defined"] and f["p"] <= SAT_MARGIN, f["defined"] and f["p"] >= BOUND - SAT_MARGIN,
                                 f["n_candidates"], f["p_golden"], f["total_gain"], tr, va, va - tr,
                                 pt["train_array"], pt["val_array"], pt["train_record"], pt["val_record"]])
    write_csv(os.path.join(outdir, "per_readout.csv"),
              ["draw", "width", "rate", "readout", "update", "defined", "reason", "p_star", "objective", "at_lower",
               "at_upper", "n_candidates", "p_star_golden", "total_gain", "train", "val", "gap", "train_array",
               "val_array", "train_record", "val_record"], rows)
    write_csv(os.path.join(outdir, "matched.csv"),
              ["step", "statistic", "matched_on", "rate", "draw", "status", "reason", "target", "n_intervals",
               "bracket_lo", "bracket_hi", "weight_on_later", "position", "p768_lo", "p768_hi", "p768_read",
               "p512_E3", "value", "where"] + ["path_E%g" % e for e in PATH], matched_rows)
    write_csv(os.path.join(outdir, "contrasts.csv"), ["step", "statistic", "draw", "status", "reason", "value"],
              contrast_rows)
    with open(os.path.join(outdir, "analysis.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(analysis, f, indent=1, sort_keys=True)
        f.write("\n")


# ----------------------------------------------------------------------------------------------
# Self-test
# ----------------------------------------------------------------------------------------------
def selftest():
    # t quantiles: closed forms for df 1 and 2, numerical integration for df 3..5
    q = 0.975
    assert abs(t_crit(1) - math.tan(math.pi * (q - 0.5))) < 1e-9
    assert abs(t_crit(2) - (2 * q - 1) / math.sqrt(2 * q * (1 - q))) < 1e-10
    for df in (3, 4, 5):
        tc = t_crit(df)
        x = np.linspace(0.0, tc, 200001)
        c = math.exp(math.lgamma((df + 1) / 2) - math.lgamma(df / 2)) / math.sqrt(df * math.pi)
        y = c * (1 + x * x / df) ** (-(df + 1) / 2)
        h = x[1] - x[0]
        integral = h / 3 * (y[0] + y[-1] + 4 * y[1:-1:2].sum() + 2 * y[2:-1:2].sum())
        assert abs(0.5 + integral - q) < 1e-10, (df, integral)
    # the cumulative-sum form of d'Kd against the explicit quadratic form, with ties
    rng = np.random.default_rng(12345)
    n = 300
    w = np.exp(rng.uniform(math.log(0.01), math.log(10), n)).astype(np.float32)
    w[10] = w[20]
    w[30] = w[40] = w[50]
    g = rng.normal(0.3, 1.0, n)
    for ties in ("ecdf", "ordinal"):
        f = Fitter(w, ties)
        w64 = w.astype(np.float64)
        if ties == "ecdf":
            r = np.array([(w64 <= x).sum() for x in w64]) / n
        else:
            r = np.empty(n)
            r[f.order] = np.arange(1, n + 1) / n
        kmat = np.minimum.outer(r, r)
        gt = g / g.sum()
        for p in (0.0, 0.37, 1.0, 2.5, 8.0):
            b = w64 ** p / (w64 ** p).sum()
            d = gt - b
            direct = float(d @ kmat @ d)
            j, dj = f.exact(gt[f.order], p)
            assert abs(direct - j) < 1e-12 * max(1.0, abs(direct)), (ties, p, direct, j)
            eps = 1e-6
            num = (f.exact(gt[f.order], p + eps)[0] - f.exact(gt[f.order], max(p - eps, 0.0))[0]) / (eps + min(eps, p))
            assert abs(num - dj) < 1e-5 * max(1.0, abs(dj)), (ties, p, num, dj)
        # recover a planted exponent: gains exactly proportional to w^1.7
        res = f.fit(w64 ** 1.7)
        assert res["defined"] and abs(res["p"] - 1.7) < 1e-9, res
        assert abs(res["p_golden"] - res["p"]) < 1e-6
        assert not f.fit(-np.abs(g))["defined"]
    assert not Fitter(np.ones(8, dtype=np.float32), "ecdf").fit(np.ones(8))["defined"]
    # matching rule
    r = matched_reading(1.5, [1.0, 2.0, 1.0, 2.0], [0, 1, 2, 3])
    assert r["index"] == 0 and r["n_intervals"] == 3 and abs(r["weight"] - 0.5) < 1e-15
    r = matched_reading(2.0, [1.0, 2.0, 3.0], [0, 1, 2])
    assert r["index"] == 0 and r["weight"] == 1.0 and r["n_intervals"] == 2
    r = matched_reading(2.0, [2.0, 2.0, 3.0], [0, 1, 2])
    assert r["index"] == 0 and r["weight"] == 0.0
    assert not matched_reading(5.0, [1.0, 2.0, 3.0], [0, 1, 2])["held"]
    # sign test
    assert abs(sign_test([1, 1, 1, 1, 1, 1])["p_two_sided"] - 2 / 64) < 1e-15
    assert abs(sign_test([1, 1, 1, 1, 1, -1])["p_two_sided"] - 14 / 64) < 1e-15
    print("selftest passed")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bundle", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        selftest()
    data, checked = load_bundle(args.bundle)
    print("bundle files verified against MANIFEST.json:", checked)
    points, e0 = compute_points(data)
    os.makedirs(args.out, exist_ok=True)
    for ties in ("ecdf", "ordinal"):
        for losses in ("array", "record"):
            name = "%s_%s" % (ties, "arrays" if losses == "array" else "record")
            analysis, matched_rows, contrast_rows = analyse(data, points, e0, ties, losses)
            write_variant(os.path.join(args.out, name), points, ties, losses, analysis, matched_rows, contrast_rows)
            print("wrote", name)
    print("done")


if __name__ == "__main__":
    main()
~~~~

### `phase2/compare.py` (SHA-256 `20a8cca0e7ae944e064b1b7fceba8cee68f988f2f020a5ad836cf8bb41e76593`)

~~~~python
#!/usr/bin/env python
"""Phase 2: compare the frozen outputs with the published tables. Reads only; changes nothing frozen.

Usage: python -I -B compare.py <frozen out folder> <published folder> <comparison output json>
"""
import csv
import json
import os
import sys

OUT, PUB, DEST = sys.argv[1], sys.argv[2], sys.argv[3]
VARIANTS = ["ecdf_arrays", "ordinal_arrays", "ecdf_record", "ordinal_record"]
STEPS = ["P1", "S1", "S3", "S4", "S5", "S2"]
DRAWS = ["m01", "m02", "m03", "m04", "m05", "m06"]


def rd_csv(path):
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def fl(x):
    return None if x in ("", None) else float(x)


pub_points = {(r["draw"], int(r["width"]), r["tag"], float(r["epoch"])): r for r in rd_csv(os.path.join(PUB, "POINTS.csv"))}
pub_fits = {(r["draw"], int(r["width"]), r["tag"], float(r["epoch"])): r for r in rd_csv(os.path.join(PUB, "FITS.csv"))}
pub_matched = {(r["statistic"], r["draw"]): r for r in rd_csv(os.path.join(PUB, "MATCHED.csv"))}
with open(os.path.join(PUB, "ANALYSIS.json"), encoding="utf-8") as f:
    pub = json.load(f)

report = {"published_rows": {"POINTS": len(pub_points), "FITS": len(pub_fits), "MATCHED": len(pub_matched)}, "variants": {}}
print("published rows: POINTS %d, FITS %d, MATCHED %d" % (len(pub_points), len(pub_fits), len(pub_matched)))
print("POINTS.p == FITS.p for every fit:", all(pub_points[k]["p"] == pub_fits[k]["p"] for k in pub_points))
print("published MATCHED statistics:", sorted({k[0] for k in pub_matched}))


def maxdiff(pairs):
    """pairs: list of (key, mine, published). Returns (max abs diff, key)."""
    best = (0.0, None)
    for key, a, b in pairs:
        if a is None or b is None:
            if a is not b:
                best = (float("inf"), key)
            continue
        d = abs(a - b)
        if d > best[0]:
            best = (d, key)
    return best


for v in VARIANTS:
    mine = {(r["draw"], int(r["width"]), r["rate"], float(r["readout"])): r for r in rd_csv(os.path.join(OUT, v, "per_readout.csv"))}
    with open(os.path.join(OUT, v, "analysis.json"), encoding="utf-8") as f:
        an = json.load(f)
    mm = {(r["step"], r["draw"]): r for r in rd_csv(os.path.join(OUT, v, "matched.csv"))}
    mc = {(r["step"], r["draw"]): r for r in rd_csv(os.path.join(OUT, v, "contrasts.csv"))}
    res = {}
    assert set(mine) == set(pub_fits) == set(pub_points), "fit keys differ"

    # ---- A. the 240 fits
    dp = [(k, float(mine[k]["p_star"]), float(pub_fits[k]["p"])) for k in mine]
    md = maxdiff(dp)
    over = [(k, a, b) for k, a, b in dp if abs(a - b) > 1e-6]
    res["fits"] = {
        "n": len(dp), "max_abs_dp": md[0], "at": md[1], "n_over_1e-6": len(over), "over_1e-6": over,
        "mean_abs_dp": sum(abs(a - b) for _, a, b in dp) / len(dp),
        "max_rel_objective": max(abs(float(mine[k]["objective"]) / float(pub_fits[k]["objective"]) - 1) for k in mine),
        "max_abs_total_gain": max(abs(float(mine[k]["total_gain"]) - float(pub_fits[k]["total_gain"])) for k in mine),
        "flags_equal": all((mine[k]["at_lower"] == "1") == (pub_fits[k]["lower"] == "True")
                           and (mine[k]["at_upper"] == "1") == (pub_fits[k]["upper"] == "True") for k in mine),
        "published_reasons": sorted({pub_fits[k]["reason"] for k in mine}),
        "mine_all_defined": all(mine[k]["defined"] == "1" for k in mine),
    }
    # ---- B. losses
    res["losses"] = {}
    for col, pcol in (("train", "train"), ("val", "validation"), ("gap", "gap")):
        res["losses"][col] = maxdiff([(k, float(mine[k][col]), float(pub_points[k][pcol])) for k in mine])[0]
    res["losses"]["train_array_vs_published"] = maxdiff([(k, float(mine[k]["train_array"]), float(pub_points[k]["train"])) for k in mine])[0]
    res["losses"]["train_record_vs_published"] = maxdiff([(k, float(mine[k]["train_record"]), float(pub_points[k]["train"])) for k in mine])[0]
    res["losses"]["val_record_vs_published"] = maxdiff([(k, float(mine[k]["val_record"]), float(pub_points[k]["validation"])) for k in mine])[0]

    # ---- C. matched readings (MATCHED.csv), and the same fields in ANALYSIS.json rows
    rows = []
    worst = {"weight": 0.0, "target": 0.0, "p_read": 0.0, "p_first": 0.0, "position": 0.0, "value": 0.0}
    structural = []
    for (step, draw), pr in sorted(pub_matched.items()):
        if (step, draw) in mm:
            m = mm[(step, draw)]
            my_status = "READ" if m["status"] == "AVAILABLE" else {"target outside the path": "TARGET_OUTSIDE_PATH",
                                                                    "undefined fit": "UNDEFINED_FIT",
                                                                    "draw missing": "DRAW_MISSING"}[m["reason"]]
            ok = my_status == pr["status"] and fl(m["bracket_lo"]) == fl(pr["between_low"]) \
                and fl(m["bracket_hi"]) == fl(pr["between_high"]) \
                and int(m["n_intervals"]) == int(pr["intervals_holding_the_target"])
            if not ok:
                structural.append([step, draw, my_status, pr["status"], m["bracket_lo"], pr["between_low"],
                                   m["bracket_hi"], pr["between_high"], m["n_intervals"], pr["intervals_holding_the_target"]])
            diffs = {}
            for mine_col, pub_col, name in (("weight_on_later", "weight", "weight"), ("target", "target", "target"),
                                            ("p768_read", "p_read", "p_read"), ("p512_E3", "p_first", "p_first"),
                                            ("position", "read_at_readout", "position"), ("value", "value", "value")):
                a, b = fl(m[mine_col]), fl(pr[pub_col])
                if a is None and b is None:
                    continue
                d = float("inf") if (a is None or b is None) else abs(a - b)
                diffs[name] = d
                worst[name] = max(worst[name], d)
            rows.append([step, draw, my_status, pr["status"], m["bracket_lo"], m["bracket_hi"], m["n_intervals"],
                         fl(m["weight_on_later"]), fl(pr["weight"]), fl(m["value"]), fl(pr["value"]), diffs])
        else:
            # fixed-update statistics: published MATCHED.csv may list them too
            c = mc[(step, draw)]
            my_status = "READ" if c["status"] == "AVAILABLE" else c["reason"]
            if my_status != pr["status"]:
                structural.append([step, draw, my_status, pr["status"]])
            a, b = fl(c["value"]), fl(pr["value"])
            d = abs(a - b)
            worst["value"] = max(worst["value"], d)
            rows.append([step, draw, my_status, pr["status"], "", "", "", None, fl(pr["weight"]), a, b, {"value": d}])
    res["matched"] = {"rows_compared": len(rows), "structural_mismatches": structural, "max_abs_diff": worst, "rows": rows}

    # ---- D. registered statistics
    st = {}
    for s in STEPS:
        a, p = an["statistics"][s], pub["statistics"][s]
        e = {"n_mine": a["n_available"], "n_pub": len(p["available"]),
             "available_equal": a["available_draws"] == p["available"],
             "label_mine": a["label"], "label_pub": p["label"], "label_equal": a["label"] == p["label"],
             "side_mine": a["side"], "status_pub": p["status"],
             "unavailable_mine": a["unavailable"], "unavailable_pub": p["unavailable"],
             "counts_equal": [a["unavailable_counts"]["undefined fit"], a["unavailable_counts"]["target outside the path"],
                              a["unavailable_counts"]["draw missing"]]
             == [p["unavailable_counts"]["UNDEFINED_FIT"], p["unavailable_counts"]["TARGET_OUTSIDE_PATH"],
                 p["unavailable_counts"]["DRAW_MISSING"]],
             "sign_mine": [a["sign_test"]["positive"], a["sign_test"]["negative"], a["sign_test"]["p_two_sided"]],
             "sign_pub": [p["sign_test"]["positive"], p["sign_test"]["negative"], p["sign_test"]["p"]],
             "max_abs_value_diff": max(abs(a["values"][d] - p["values"][d]) for d in p["values"]),
             "values_same_draws": sorted(d for d in a["values"] if a["values"][d] is not None) == sorted(p["values"])}
        e["sign_equal"] = e["sign_mine"] == e["sign_pub"]
        if "interval" in p:
            pi = p["interval"]
            e.update(mean_mine=a["mean"], mean_pub=pi["mean"], d_mean=abs(a["mean"] - pi["mean"]),
                     sd_mine=a["sd"], sd_pub=pi["sd"], d_sd=abs(a["sd"] - pi["sd"]),
                     ci_mine=[a["ci_low"], a["ci_high"]], ci_pub=pi["interval"],
                     d_ci=max(abs(a["ci_low"] - pi["interval"][0]), abs(a["ci_high"] - pi["interval"][1])),
                     t_crit_mine=a["t_crit"], t_crit_pub=pi["t_critical"], df_equal=a["df"] == pi["df"],
                     pub_t_p=pi.get("p"))
        else:
            e.update(mean_mine=a["mean"], mean_pub=None, ci_mine=[a["ci_low"], a["ci_high"]], ci_pub=None,
                     note="published has no interval for this statistic")
        if p.get("leave_one_out"):
            lm = {r["dropped"]: r for r in a["leave_one_out"]["intervals"]}
            dl, sides = 0.0, True
            for d, pr in p["leave_one_out"].items():
                dl = max(dl, abs(lm[d]["ci_low"] - pr["interval"][0]), abs(lm[d]["ci_high"] - pr["interval"][1]),
                         abs(lm[d]["mean"] - pr["mean"]))
                mine_side = {"above": "ABOVE", "below": "BELOW", "spans": "SPANS"}[lm[d]["side"]]
                sides = sides and ((mine_side == pr["side"]) or (mine_side == "SPANS" and not pr["excludes_zero"]))
                e.setdefault("loo_pub_sides", {})[d] = [pr["side"], pr["excludes_zero"], lm[d]["side"]]
            e.update(loo_n=len(p["leave_one_out"]), loo_max_abs_diff=dl, loo_sides_equal=sides)
        else:
            e.update(loo_n=0, loo_mine_is_none=a["leave_one_out"] is None)
        e["saturation_mine"] = a["saturation"]["label"]
        e["flagged_pub"] = p.get("flagged")
        e["S32_pub"] = p.get("S32")
        st[s] = e
    res["statistics"] = st
    res["sequence_pub"] = [[x["step"], x["label"], x["status"], x["read_as_confirmation"], x["confirmed"]] for x in pub["sequence"]]
    res["sequence_mine"] = [[s, an["statistics"][s]["label"], an["statistics"][s]["side"], an["statistics"][s]["reached"]] for s in STEPS]
    res["section7_row_mine"] = an["section7_row"]

    # ---- E. diagnostics and descriptives
    diag = {"records_against_arrays": [an["records_against_arrays"]["max_abs_difference"],
                                       pub["records_against_arrays"]["max_absolute_difference"]],
            "fit_bounds_pub": pub["fit_bounds"],
            "fit_bounds_mine": {"upper": an["fit_summary"]["n_at_upper"], "lower": an["fit_summary"]["n_at_lower"],
                                "undefined": an["fit_summary"]["n_fits"] - an["fit_summary"]["n_defined"]}}
    no = {}
    for arm, pa in pub["not_overfit"]["arms"].items():
        w, r = arm.split("|")
        ma = an["not_overfit"]["w%s_%s" % (w, r)]
        no[arm] = {"label_mine": ma["label"], "label_pub": pa["label"],
                   "d_mean": abs(ma["mean"] - pa["interval"]["mean"]),
                   "d_ci": max(abs(ma["ci_low"] - pa["interval"]["interval"][0]), abs(ma["ci_high"] - pa["interval"]["interval"][1]))}
    diag["not_overfit"] = no
    br = {"max_d_value": 0.0, "max_d_mean": 0.0, "max_d_ci": 0.0, "max_d_panel": {"p": 0.0, "train": 0.0, "validation": 0.0, "gap": 0.0}}
    for ek, ev in pub["by_readout"].items():
        for cname, rate in (("D4", "lr1e-04"), ("D2", "lr3e-04")):
            pc = ev["contrasts"][cname]
            mcn = an["descriptives"]["fixed_update_by_readout"]["%s_%s" % (rate, ek)]
            br["max_d_value"] = max(br["max_d_value"], max(abs(mcn["values"][d] - pc["values"][d]) for d in pc["values"]))
            br["max_d_mean"] = max(br["max_d_mean"], abs(mcn["mean"] - pc["interval"]["mean"]))
            br["max_d_ci"] = max(br["max_d_ci"], abs(mcn["ci_low"] - pc["interval"]["interval"][0]),
                                 abs(mcn["ci_high"] - pc["interval"]["interval"][1]))
        for arm, pp in ev["panel"].items():
            w, r = arm.split("|")
            mp = an["descriptives"]["panel"]["w%s_%s_%s" % (w, r, ek)]
            for a_, b_ in (("p_star", "p"), ("train", "train"), ("val", "validation"), ("gap", "gap")):
                br["max_d_panel"][b_] = max(br["max_d_panel"][b_], abs(mp[a_] - pp[b_]))
    diag["by_readout"] = br
    re_ = {}
    for w in ("512", "768"):
        pv = pub["rate_effects"][w]["p"]
        mv = an["descriptives"]["rate_effect_at_E3"]["w%s_3e-4_minus_1e-4" % w]
        re_[w] = {"same_sign_max_diff": max(abs(mv["values"][d] - pv["values"][d]) for d in pv["values"]),
                  "opposite_sign_max_diff": max(abs(mv["values"][d] + pv["values"][d]) for d in pv["values"]),
                  "mean_mine": mv["mean"], "mean_pub": pv["interval"]["mean"],
                  "ci_mine": [mv["ci_low"], mv["ci_high"]], "ci_pub": pv["interval"]["interval"]}
    diag["rate_effects_p"] = re_
    cl = {}
    for arm, pl in pub["losses"].items():
        w, r = arm.split("|")
        if r == "E0":
            me = an["descriptives"]["e0"]["w%s" % w]
            cl[arm] = {"d_train": abs(me["train_mean"] - pl["train"]), "d_validation": abs(me["val_mean"] - pl["validation"])}
        else:
            mcl = an["descriptives"]["clipping"]["w%s_%s" % (w, r)]
            per = mcl["per_draw"]
            gmean = sum(x["gradient_norm_mean"] for x in per.values()) / len(per)
            gmax = max(x["gradient_norm_max"] for x in per.values())
            cl[arm] = {"d_clip_fraction_mean": abs(mcl["clip_fraction_mean"] - pl["clipping"]["clip_fraction_mean"]),
                       "d_gradient_norm_mean": abs(gmean - pl["clipping"]["gradient_norm_mean"]),
                       "d_gradient_norm_max": abs(gmax - pl["clipping"]["gradient_norm_max"])}
    diag["losses_block"] = cl
    res["diagnostics"] = diag
    report["variants"][v] = res

    print("\n================ variant %s ================" % v)
    f = res["fits"]
    print("FITS: n=%d  max|dp|=%.3e at %s  mean|dp|=%.3e  n(|dp|>1e-6)=%d  max rel objective diff=%.3e  max|d total_gain|=%.3e  flags equal=%s  all defined=%s  published reasons=%s"
          % (f["n"], f["max_abs_dp"], f["at"], f["mean_abs_dp"], f["n_over_1e-6"], f["max_rel_objective"],
             f["max_abs_total_gain"], f["flags_equal"], f["mine_all_defined"], f["published_reasons"]))
    print("LOSSES max|diff| vs POINTS.csv: this variant train %.3e val %.3e gap %.3e | array-mean train %.3e | record train %.3e, record val %.3e"
          % (res["losses"]["train"], res["losses"]["val"], res["losses"]["gap"], res["losses"]["train_array_vs_published"],
             res["losses"]["train_record_vs_published"], res["losses"]["val_record_vs_published"]))
    m = res["matched"]
    print("MATCHED: rows %d, structural mismatches (status/bracket/count): %d %s" % (m["rows_compared"], len(m["structural_mismatches"]), m["structural_mismatches"]))
    print("   max|diff|: " + ", ".join("%s %.3e" % (k, x) for k, x in m["max_abs_diff"].items()))
    for s in STEPS:
        e = st[s]
        if e.get("mean_pub") is not None:
            print("%s: n %d/%d  mean %.12f | %.12f (d %.2e)  CI [%.12f, %.12f] | [%.12f, %.12f] (d %.2e)  sd d %.2e  label %s | %s  sign %s | %s  LOO n=%d max d %.2e sides equal %s  values d %.2e"
                  % (s, e["n_mine"], e["n_pub"], e["mean_mine"], e["mean_pub"], e["d_mean"], e["ci_mine"][0], e["ci_mine"][1],
                     e["ci_pub"][0], e["ci_pub"][1], e["d_ci"], e["d_sd"], e["label_mine"], e["label_pub"], e["sign_mine"],
                     e["sign_pub"], e["loo_n"], e["loo_max_abs_diff"], e["loo_sides_equal"], e["max_abs_value_diff"]))
        else:
            print("%s: n %d/%d  label %s | %s  sign %s | %s  unavailable %s | %s  values d %.2e  (published prints no interval; mine, not read: mean %.12f CI [%.12f, %.12f])"
                  % (s, e["n_mine"], e["n_pub"], e["label_mine"], e["label_pub"], e["sign_mine"], e["sign_pub"],
                     e["unavailable_mine"], e["unavailable_pub"], e["max_abs_value_diff"], e["mean_mine"], e["ci_mine"][0], e["ci_mine"][1]))
    print("DIAG: records_against_arrays mine %.12e | published %.12e ; fit_bounds mine %s | published %s"
          % (diag["records_against_arrays"][0], diag["records_against_arrays"][1], diag["fit_bounds_mine"], diag["fit_bounds_pub"]))
    print("   NOT_OVERFIT:", {k: (x["label_mine"], x["label_pub"], "%.2e" % x["d_mean"], "%.2e" % x["d_ci"]) for k, x in no.items()})
    print("   by_readout contrasts: max d value %.2e, mean %.2e, CI %.2e ; panel max d %s" % (br["max_d_value"], br["max_d_mean"], br["max_d_ci"], {k: "%.2e" % x for k, x in br["max_d_panel"].items()}))
    print("   rate effects (p): " + "; ".join("w%s same-sign d %.2e, opposite-sign d %.2e" % (w, x["same_sign_max_diff"], x["opposite_sign_max_diff"]) for w, x in re_.items()))
    print("   losses block:", {k: {a: "%.2e" % b for a, b in x.items()} for k, x in cl.items()})

with open(DEST, "w", encoding="utf-8", newline="\n") as f:
    json.dump(report, f, indent=1, sort_keys=True, default=str)
    f.write("\n")
print("\nwrote", DEST)
~~~~

### `phase2/report_tables.py` (SHA-256 `3e8a0494a1d01d8e5663e12eea39908a3a6ff2c8605c0c528592544ec33c0afc`)

~~~~python
import json, sys
c = json.load(open(sys.argv[1], encoding="utf-8"))
A, B = c["variants"]["ecdf_arrays"], c["variants"]["ordinal_record"]
print("| Statistic | Draw | Status (mine / published) | Bracket | Intervals holding | Weight: primary | Weight: published | Value: primary | Value: ordinal_record | Value: published | Diff primary | Diff ordinal_record |")
print("|---|---|---|---|---|---|---|---|---|---|---|---|")
for ra, rb in zip(A["matched"]["rows"], B["matched"]["rows"]):
    step, draw, ms, ps, lo, hi, n, wm, wp, vm, vp, d = ra
    vb = rb[9]
    f = lambda x, k=9: "" if x is None else ("%." + str(k) + "f") % x
    print("| %s | %s | %s / %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |" % (
        step, draw, ms, ps, ("E%s-E%s" % (lo, hi)) if lo else ("E3 (fixed)" if ms == "READ" else "none"), n, f(wm, 7), f(wp, 7), f(vm, 10), f(vb, 10), f(vp, 10),
        "" if vm is None else "%.1e" % abs(vm - vp), "" if vb is None else "%.1e" % abs(vb - vp)))
print()
for v in ("ecdf_arrays", "ordinal_arrays", "ecdf_record", "ordinal_record"):
    f = c["variants"][v]["fits"]
    print(v, "max|dp| %.3e at %s, mean %.3e, n>1e-6: %d" % (f["max_abs_dp"], f["at"], f["mean_abs_dp"], f["n_over_1e-6"]))
    for s, e in c["variants"][v]["statistics"].items():
        if e.get("mean_pub") is not None:
            print("   %s mean %.10f CI [%.10f, %.10f] d_mean %.1e d_ci %.1e loo %.1e | pub mean %.10f CI [%.10f, %.10f]" % (s, e["mean_mine"], e["ci_mine"][0], e["ci_mine"][1], e["d_mean"], e["d_ci"], e["loo_max_abs_diff"], e["mean_pub"], e["ci_pub"][0], e["ci_pub"][1]))
    print("   loo sides pub/mine S3:", c["variants"][v]["statistics"]["S3"].get("loo_pub_sides"))
~~~~

### `phase2/second_pass_checks.py` (SHA-256 `cb75b7df44a066ce11946b8748103eb7878ade8139ea2d7ebfd60580745aaa02`)

~~~~python
#!/usr/bin/env python
"""Phase 2, SECOND PASS (after the freeze, labelled as such): evidence for classifying the discrepancies.

Imports the frozen module code/n7_repro.py unchanged; writes nothing into the frozen folders.

Usage: python -I -B second_pass_checks.py <code folder> <bundle folder> <published folder>
"""
import csv
import json
import math
import os
import sys

import numpy as np

sys.path.insert(0, sys.argv[1])
import n7_repro as R  # noqa: E402

BUNDLE, PUB = sys.argv[2], sys.argv[3]
data, _ = R.load_bundle(BUNDLE)
with open(os.path.join(PUB, "FITS.csv"), encoding="utf-8", newline="") as f:
    fits = list(csv.DictReader(f))
with open(os.path.join(PUB, "ANALYSIS.json"), encoding="utf-8") as f:
    pub = json.load(f)
with open(os.path.join(PUB, "MATCHED.csv"), encoding="utf-8", newline="") as f:
    matched = list(csv.DictReader(f))

# ---- 1. Where does the remaining difference in p* come from?
print("1. Stationarity of the published p* under each tie reading (all 240 fits)")
fitters = {}
rows = []
for r in fits:
    draw, width, tag, epoch = r["draw"], int(r["width"]), r["tag"], float(r["epoch"])
    k = R.READOUTS.index(epoch)
    dw = data[draw]["widths"][width]
    gain = (dw["E0"][:R.N_TRAIN] - dw["arms"][tag]["arrays"][k][:R.N_TRAIN]).astype(np.float64)
    p_pub = float(r["p"])
    out = {"key": (draw, width, tag, epoch), "p_pub": p_pub, "neg_frac": float((gain < 0).mean()),
           "neg_frac_pub": float(r["negative_fraction"]), "J0_pub": float(r["J0"]), "obj_pub": float(r["objective"])}
    for ties in ("ordinal", "ecdf"):
        if (draw, ties) not in fitters:
            fitters[(draw, ties)] = R.Fitter(data[draw]["weights"], ties)
        ft = fitters[(draw, ties)]
        gt = (gain / gain.sum())[ft.order]
        mine = ft.fit(gain)
        j_pub, dj_pub = ft.exact(gt, p_pub)
        h = 1e-4
        curv = (ft.exact(gt, p_pub + h)[1] - ft.exact(gt, p_pub - h)[1]) / (2 * h)
        out[ties] = {"p_mine": mine["p"], "dp": mine["p"] - p_pub, "newton_step_from_pub": -dj_pub / curv,
                     "J_at_pub": j_pub, "J_at_mine": mine["objective"], "dJ_at_mine": ft.exact(gt, mine["p"])[1],
                     "dJ_at_pub": dj_pub, "J0": ft.exact(gt, 0.0)[0]}
    rows.append(out)
for ties in ("ordinal", "ecdf"):
    dps = np.array([r[ties]["dp"] for r in rows])
    newt = np.array([r[ties]["newton_step_from_pub"] for r in rows])
    relobj = np.array([r[ties]["J_at_pub"] / r["obj_pub"] - 1 for r in rows])
    relj0 = np.array([r[ties]["J0"] / r["J0_pub"] - 1 for r in rows])
    excess = np.array([r[ties]["J_at_pub"] - r[ties]["J_at_mine"] for r in rows])
    print("  ties=%-7s max|p_mine - p_pub| = %.3e ; max|(p_mine - p_pub) - Newton step from p_pub| = %.3e ; "
          "max|dJ/dp at mine| = %.2e ; max|dJ/dp at published| = %.2e"
          % (ties, np.abs(dps).max(), np.abs(dps - newt).max(), max(abs(r[ties]["dJ_at_mine"]) for r in rows),
             max(abs(r[ties]["dJ_at_pub"]) for r in rows)))
    print("                max rel |J(p_pub) (my evaluation) / published objective - 1| = %.3e ; max rel |J(0) / published J0 - 1| = %.3e ; "
          "fits where J(p_pub) < J(p_mine): %d (min excess %.2e, max %.2e)"
          % (np.abs(relobj).max(), np.abs(relj0).max(), int((excess < 0).sum()), excess.min(), excess.max()))
print("  negative_fraction: max |mine - published| = %.3e" % max(abs(r["neg_frac"] - r["neg_frac_pub"]) for r in rows))

# ---- 2. Tie order: is the published objective the stable-sort ordinal one?
print("2. Tie order check (objective at the published p, three orderings of tied weights), one fit per draw at E3, 512, 1e-4")
for draw in R.DRAWS:
    w = data[draw]["weights"].astype(np.float64)
    r = next(x for x in rows if x["key"] == (draw, 512, "lr1e-04", 3.0))
    dw = data[draw]["widths"][512]
    gain = (dw["E0"][:R.N_TRAIN] - dw["arms"]["lr1e-04"]["arrays"][7][:R.N_TRAIN]).astype(np.float64)
    gt = gain / gain.sum()

    def obj(order, p, idx=None):
        b = np.exp(p * np.log(w[order]))
        b /= b.sum()
        c = np.cumsum(gt[order] - b)
        return float(np.dot(c[:-1], c[:-1])) / w.size
    stable = np.argsort(w, kind="stable")
    rev = np.lexsort((-np.arange(w.size), w))      # ties in reverse sequence order
    n_tied = int(w.size - np.unique(w).size)
    print("  %s: tied surplus values %d ; rel diff to published objective: stable %.2e, reversed ties %.2e, ecdf %.2e"
          % (draw, n_tied, obj(stable, r["p_pub"]) / r["obj_pub"] - 1, obj(rev, r["p_pub"]) / r["obj_pub"] - 1,
             r["ecdf"]["J_at_pub"] / r["obj_pub"] - 1))

# ---- 3. The published t critical value and the t-test p-values (not registered in the protocol)
print("3. t quantile: mine %.15f, published %s, difference %.2e" % (R.t_crit(5), pub["statistics"]["P1"]["interval"]["t_critical"],
                                                                     R.t_crit(5) - pub["statistics"]["P1"]["interval"]["t_critical"]))
for s in ("P1", "S1", "S3", "S4", "S5"):
    pi = pub["statistics"][s]["interval"]
    t = pi["mean"] / pi["se"]
    p2 = 2 * (1 - R.t_cdf(abs(t), pi["df"]))
    print("   %s: published t-test p = %.12g ; recomputed two-sided p = %.12g ; published se - sd/sqrt(n) = %.1e"
          % (s, pi["p"], p2, pi["se"] - pi["sd"] / math.sqrt(pi["n"])))

# ---- 4. Internal consistency of the published tables
bad = 0
for r in matched:
    row = pub["statistics"][r["statistic"]]["rows"][r["draw"]]
    for col, key in (("value", "value"), ("p_read", "p_read"), ("p_first", "p_first"), ("target", "target"), ("weight", "weight"),
                     ("read_at_readout", "read_at_readout")):
        a = r[col]
        b = row.get(key)
        if (a == "") != (b is None) or (a != "" and float(a) != float(b)):
            bad += 1
    if r["status"] != row["status"]:
        bad += 1
print("4. MATCHED.csv against ANALYSIS.json rows: %d rows, %d cell mismatches" % (len(matched), bad))
# recompute every published interval from the published per-draw values
worst = 0.0
for s, st in pub["statistics"].items():
    if "interval" not in st:
        continue
    v = [st["values"][d] for d in st["available"]]
    ti = R.t_interval(v)
    worst = max(worst, abs(ti["mean"] - st["interval"]["mean"]), abs(ti["ci_low"] - st["interval"]["interval"][0]),
                abs(ti["ci_high"] - st["interval"]["interval"][1]), abs(ti["sd"] - st["interval"]["sd"]))
    for d, lo in st["leave_one_out"].items():
        rest = [st["values"][x] for x in st["available"] if x != d]
        tj = R.t_interval(rest)
        worst = max(worst, abs(tj["mean"] - lo["mean"]), abs(tj["ci_low"] - lo["interval"][0]), abs(tj["ci_high"] - lo["interval"][1]))
print("   published intervals and leave-one-out intervals recomputed from the published per-draw values: max |diff| = %.2e" % worst)

# ---- 5. Size of the loss-source ambiguity on each matched value (record losses vs array means), same fits
print("5. Effect of the loss source alone (ordinal fits; array means minus record values), per matched statistic and draw")
for step, name, kind, rate, var, expected in R.STATISTICS:
    if kind != "matched":
        continue
    line = []
    for draw in R.DRAWS:
        vals = {}
        for src in ("array", "record"):
            def loss(width, epoch):
                k = R.READOUTS.index(epoch)
                arm = data[draw]["widths"][width]["arms"][rate]
                if src == "array":
                    tr = float(arm["arrays"][k][:R.N_TRAIN].astype(np.float64).mean())
                    va = float(arm["arrays"][k][R.N_TRAIN:].astype(np.float64).mean())
                else:
                    tr = arm["record"]["readouts"][k]["train_loss"]
                    va = arm["record"]["readouts"][k]["validation_loss"]
                return {"train": tr, "val": va, "gap": va - tr}[var]
            rd = R.matched_reading(loss(512, 3), [loss(768, e) for e in R.PATH], R.PATH)
            if not rd["held"]:
                vals[src] = None
                continue
            pa = next(x for x in rows if x["key"] == (draw, 768, rate, float(rd["lo"])))["ordinal"]["p_mine"]
            pb = next(x for x in rows if x["key"] == (draw, 768, rate, float(rd["hi"])))["ordinal"]["p_mine"]
            p5 = next(x for x in rows if x["key"] == (draw, 512, rate, 3.0))["ordinal"]["p_mine"]
            vals[src] = p5 - (pa + rd["weight"] * (pb - pa))
        line.append("%s %s" % (draw, "n/a" if vals["array"] is None else "%.2e" % (vals["array"] - vals["record"])))
    print("   %s %-10s %s" % (step, name, "  ".join(line)))
~~~~

### `phase2/show_structure.py` (SHA-256 `a3b1adfd86b0bc95c16f8944569eaae61eef9adede375144a896ca20b30d26b5`)

~~~~python
import json, sys
a = json.load(open(sys.argv[1], encoding="utf-8"))
def walk(o, pre="", depth=0, maxdepth=4):
    if isinstance(o, dict):
        for k, v in o.items():
            if isinstance(v, (dict, list)) and depth < maxdepth:
                print("  " * depth + str(k) + ("  {dict %d}" % len(v) if isinstance(v, dict) else "  [list %d]" % len(v)))
                walk(v, pre + "/" + str(k), depth + 1, maxdepth)
            else:
                s = json.dumps(v)
                print("  " * depth + str(k) + " = " + (s if len(s) < 160 else s[:160] + "..."))
    elif isinstance(o, list):
        if o and isinstance(o[0], (dict, list)):
            print("  " * depth + "[0]:")
            walk(o[0], pre + "/0", depth + 1, maxdepth)
        else:
            s = json.dumps(o)
            print("  " * depth + (s if len(s) < 160 else s[:160] + "..."))
skip = set(sys.argv[2:])
for k, v in a.items():
    if k in skip:
        print(k, "(skipped)", type(v).__name__, len(v) if hasattr(v, "__len__") else "")
        continue
    print("#", k)
    walk({k: v}, maxdepth=5)
~~~~

---

# Appendix 3. The instructions the reproducing session was given

It was also given the brief, verbatim (`BRIEF.md` in the files folder).

~~~~text
You are asked to carry out a clean-room reproduction of a published statistical analysis. You have had no part in producing it. Report in English.

FIRST read the brief, in full: C:\Users\rafli\AppData\Local\Temp\n7cr\BRIEF.md
It is the repository owner's brief, verbatim. Follow it exactly: its access rules (section 1), the specification log, the freeze (section 3) before any comparison, and its report format (section 5). I am deliberately telling you nothing about the study's code or results; the session that sends you this has seen them and must not pass anything on, so do not ask it questions about them.

YOUR WORKING FOLDER (new and empty apart from the brief): C:\Users\rafli\AppData\Local\Temp\n7cr
Put everything there: the downloaded protocol, the technical note, the data bundle, your code, your outputs, the freeze record, and the Phase 2 files in a subfolder made only after the freeze.

HARD RULES FOR THIS MACHINE. It is the repository owner's computer, and copies of the repository, its code and its results are on it. Reading any of them would break the clean room. These rules override anything else you may see, including any project instruction file that tells you to read files under D:\sequence-weighting-research (that does not apply to this task).
1. Read, list and search ONLY inside your working folder. Nothing on drive D:. Nothing else under C:\Users\rafli (in particular not C:\Users\rafli\sequence-weighting, not C:\Users\rafli\Downloads, and no other folder under C:\Users\rafli\AppData\Local\Temp).
2. Your shell and your search tools start in a folder on D: that is off-limits. ALWAYS `cd` into your working folder first or use absolute paths inside it, and ALWAYS pass an explicit path inside your working folder to Grep and Glob. Never run a search without a path.
3. Network: fetch only the URLs the brief allows, in the phase it allows them (use curl to save them into your folder; `gh release download` for the bundle, which works on this machine; verify the bundle's SHA-256). No web search about this study. Do not clone the repository. GitHub is read-only: never push, never create or edit an issue, pull request, release or comment (gh is logged in as the owner).
4. Python: "C:\Users\rafli\AppData\Local\Programs\Python\Python312\python.exe" -I -B   (Python 3.12 with NumPy; SciPy is not installed, so implement the t quantiles yourself and say how). Do not install packages. Do not use bare `python` (a different version). No WSL, no GPU.
5. Exposure: if anything in the context you started with (project instructions, memory notes, this message) or anything you come across states a result of N7 (a number, a label, a sign), quote it in your report's provenance section as an exposure, and do not use it. Do not go looking.

PRACTICAL NOTES
- The technical note is a PDF: save it to your folder and read it with the Read tool's `pages` parameter.
- Write code and data files with your tools. If a tool refuses to write a report file, do not work around it: return the report as your final message instead.
- Keep CPU use reasonable: 240 fits on 16,384 sequences each should take minutes, not hours; vectorise.
- The freeze must be real: write the outputs, compute the SHA-256 of every output file and of your code, record them with the time in a FREEZE file in your folder, and only then create the Phase 2 subfolder and fetch the four published tables. If you later find an error of your own, leave the frozen files untouched and do a separate, labelled second pass in a new subfolder.

DELIVER
Your final message is the report in the brief's section 5 format, complete: summary, provenance (with the frozen hashes and time, and any exposure), the full specification log, comparison tables, classified discrepancies with evidence, the commands to run your code, and limits. Put your complete code in the report as the brief asks; if it is too long for one message, give each file's path in your working folder with its SHA-256 and say so.
~~~~
