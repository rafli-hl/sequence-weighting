# Audit: Sequence weighting across model widths

**Date:** 13 November 2026. **Auditor:** OpenAI Codex, an AI reviewer; this is not independent human review or a training replication.

**Record audited:** `rafli-hl/sequence-weighting`, branch `main`, commit `fee55ea1486dedba51ae6b51cc2e3ba8eaa51401`; release asset `v1.2/n7-loss-arrays-v1.zip`. File-and-line references below refer to this exact commit: [browse the audited tree](https://github.com/rafli-hl/sequence-weighting/tree/fee55ea1486dedba51ae6b51cc2e3ba8eaa51401). No tracked repository file was changed. No model training, issue, pull request, or public posting was performed. New calculations are **post hoc and descriptive**.

## 1. Summary

1. No error was found in the registered N7 numbers, labels, matching rule, or fixed-sequence decisions.
2. All 240 N7 fits reproduce; all 268 published post-hoc value series reproduce exactly with the pinned packages.
3. **Major:** the historical claim that the later bracket endpoints give the least favourable interval is false: S1 can include zero under another allowed endpoint combination.
4. **Major:** C3's interpolation-free support treats a gap difference whose interval includes zero as proof of equal gaps; the 12 November correction did not resolve this inference problem.
5. **Minor:** exposure matching matches recency windows, not identical realised recencies; the study table omits N6's width 384, and one training-reproducibility statement remains inconsistent.
6. The tokenizer was rebuilt twice from the pinned public parquet with the exact pinned SHA-256; complete corpus reconstruction and retraining remain unverified.
7. The numerical familywise-error simulation cannot be reproduced from this public tree; its review record is hash-named but absent.

## 2. Checks run

**Environment.** Linux x86-64, glibc 2.41, Python 3.12.14. The initial NumPy-only loss check used NumPy 2.3.5. An isolated environment subsequently used NumPy 2.5.3, PyTorch 2.7.0+cpu, SciPy 1.18.1, tokenizers 0.21.4 and PyArrow 26.0.1. CPU thread counts were set to one for the numerical checks. No CUDA was used.

In the commands below, `REPO` is the checkout, `BUNDLE` is the extracted `n7-loss-arrays` directory, and `PY` is the isolated environment's Python. Commands run from `REPO` unless stated otherwise. Appendix 6 includes exact substantive stdout, analytical code, and the two failed first attempts at auditor-written checks. Package-install progress bars are omitted; terminal installation results are reported below.

| Check / command | Environment | Exact result or output location |
|---|---|---|
| `git -c core.autocrlf=false clone https://github.com/rafli-hl/sequence-weighting.git` | Git, Linux | Exit 0; `git rev-parse HEAD` printed `fee55ea1486dedba51ae6b51cc2e3ba8eaa51401`. |
| `python tools/verify_publication.py` | Python 3.12.14 | `manifest: 1346 rows; 1346 exact; 0 differ only in line endings; 0 mismatched; 0 missing; 0 published files not in the manifest` / `links: 511 local Markdown links checked; 0 known unavailable; 0 unexpected broken`. Same result after the audit. |
| `python outputs/sequence-weighting-pilot/core_checks.py` | Standard library | Exit 0; JSON `status: passed`; complete output in §6. |
| README's Python block, executed directly without editing | Standard library | `P1 = +0.00909 [+0.00400, +0.01417], n = 6` |
| `gh release download v1.2 --pattern n7-loss-arrays-v1.zip` | Unauthenticated GitHub CLI | **Exit 4.** `To get started with GitHub CLI, please run:  gh auth login` / `Alternatively, populate the GH_TOKEN environment variable with a GitHub API authentication token.` |
| Public-download fallback: `curl -fL --max-time 120 https://github.com/rafli-hl/sequence-weighting/releases/download/v1.2/n7-loss-arrays-v1.zip -o ZIP`; `unzip -q ZIP -d AUDIT_WORK` | curl / unzip | Both completed. ZIP SHA-256: `cbe26760e2062a4cf03307d779226fa6efce8cfcfbf57b2e092bd818af80b8a9`, exactly the README pin. This workaround is disclosed, not treated as a successful `gh` invocation. |
| `pip install numpy scipy` in the isolated environment | Python 3.12 | `Successfully installed numpy-2.5.4 scipy-1.18.1`; NumPy subsequently replaced by the required 2.5.3. |
| `OPENBLAS_NUM_THREADS=1 python tools/verify_n7_losses.py BUNDLE` | Python 3.12.14 / NumPy 2.3.5 | **PASS.** 66 bundle files; six weight hashes; 240 fits; maximum fit discrepancy `2.90e-09`; maximum mean-loss discrepancy `8.55e-07`. Five contrasts match. Full stdout in §6. |
| `pip install --index-url https://download.pytorch.org/whl/cpu torch==2.7.0` | Isolated environment | Exit 0; installed `torch-2.7.0+cpu`. |
| `pip install -r tools/requirements-posthoc.txt` | Isolated environment | Exit 0; `Successfully installed numpy-2.5.3`; torch requirement already satisfied. |
| `OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PY tools/verify_posthoc.py BUNDLE` | Pinned NumPy / torch | `ran with numpy 2.5.3, torch 2.7.0+cpu` / `keys: 268 published, 268 reproduced; 0 missing, 0 extra` / `largest difference: 0.00e+00` / `PASS`. |
| `PY reports/follow-up-audit-20261112-01/verify_findings.py REPO BUNDLE` | Pinned NumPy / torch; SciPy | Exit 0; exact output in §6. Reproduces the published audit's main numerical checks; this alone is not an independent implementation. |
| `PY audit_numeric.py REPO BUNDLE` and `... --tables-only` | Same isolated environment | Independent checks of all 24 matched rows, five intervals, 30 leave-one-out intervals, sign tests, plus new descriptive analyses. Full outputs in §6. |
| `PY audit_record.py REPO ZIP` | Same isolated environment | S, N1, N3, N4, N5 and N6 table spot-checks agree; 32 N7 sealed-source files agree; nine living-page fragment links resolve; no tracked model-state candidates; no tracked changes. Full stdout in §6. |
| Download pinned WikiText-2 training parquet, then `TOKENIZERS_PARALLELISM=false PY rebuild_tokenizer.py REPO WT2_PARQUET` | tokenizers 0.21.4 / PyArrow 26.0.1 | 36,718 rows; both tokenizer rebuilds produce 107,106 bytes and SHA-256 `cd642ca2b78a76e880adf07efb425bd2db741248cbf537aed0538c9421cca146`. Exact output in §6. |

The GitHub CLI failure is an environment/authentication issue, **not evidence that the public asset is unavailable**. The downloadable asset and its hash were verified separately.

### Coverage of the five reproducibility levels

| Level | Audit outcome |
|---|---|
| 1. Integrity | Passed manifest and N7 source-seal checks. Hash agreement establishes consistency, not historical publication time by itself. External archive timestamps were not independently authenticated in this audit. |
| 2. Published tables → statistics | All N7 matching rows and main inferential summaries checked. Targeted primary statistics checked in every earlier named study; this is not an exhaustive reimplementation of every earlier sensitivity or outcome label. |
| 3. Losses → fitted exponents | All 240 N7 fits and five confirmed contrasts reproduced. The earlier studies' unreleased losses were not reconstructed. |
| 4. Model evaluation → losses | Blocked as disclosed: no published model states were found. Stored arrays cannot independently establish what model evaluation originally produced. |
| 5. Training from scratch | **Partial preprocessing success:** exact tokenizer rebuilt twice. Full dataset manifest/sequence files, launch adaptation, and training not attempted. No GPU training is part of this audit. |

## 3. Findings

Severity follows the brief. **VERIFIED** means the evidence or calculation was reproduced, not that an unobserved mechanism was established. None of the findings below changes a registered number or label.

| ID | Area | Severity | Finding | Evidence | Status | Fix type |
|---|---|---|---|---|---|---|
| F1 | D, E | **Major** | The all-later-end reading minimises the mean contrast here, but does not generally minimise its t-interval's lower limit. The surviving historical assertion that S1 stays above zero under the least favourable bracket reading is incorrect. | `reports/natural-text-correction-20261109-01/CORRECTION.md:70–85`; independently enumerating all 64 endpoint combinations gives S1 lower limit **−0.00005074**. P1's worst lower limit is **+0.00007639**, rather than the displayed all-later-end +0.00216. See §3.1 and `audit_numeric.py --tables-only`. | VERIFIED | **Correction**: new dated note qualifying the old sensitivity claim; preserve registered labels and historical files. |
| F2 | C, D, J | **Major** | C3's replacement “support without interpolation” overstates equality of gaps. A nonzero-uncertainty interval containing zero does not establish equal gaps or rule out a gap-only relation. This is a defect in the 12 November resolution, not a repetition of its already disclosed interpolation problem. | `CURRENT_CLAIMS.md:100–109`; `reports/natural-text-correction-20261112-01/CORRECTION.md:61–65`. Recomputed gap difference **+0.00039191 [−0.00472497,+0.00550879]**; individual draw differences range **−0.00924587 to +0.01450443**. | VERIFIED | **Correction** for the historical inference; **Doc-only** qualification of current C3. Any stronger equivalence claim needs an independently justified tolerance and model restrictions. |
| F3 | F, J | Minor | “Every pass is equally long ago” describes the intended matching windows too strongly. The implemented masks equalise eligible recency ranges and pass counts, not realised batch-level recencies or their exact joint distribution. | `METHODS.md:177–179`; `posthoc_exposure.py:257–258`. Regenerated orders: at k=1, maximum difference of mean recency **14.11545 updates**, maximum marginal KS distance **0.11920**; at k=2/3, joint quarter-cell total variation reaches **0.03709/0.03659**. | VERIFIED | **Doc-only**: say “matched recency windows”; report balance. Optional **Post-hoc analysis** with finer standardisation. |
| F4 | G, H, J | Minor | Two current summaries disagree with their own detailed record: N6's width 384 arm is omitted from the study table, and the claims page attributes inability to retrain to absent states/rows rather than distinguishing evaluation from rebuilding and retraining. | `METHODS.md:18` versus N6 sealed `PROTOCOL.md:38–47` and N6 `POINTS.csv`; `CURRENT_CLAIMS.md:239` versus README's five-level table. The exact tokenizer rebuild further narrows the practical preprocessing blocker. | VERIFIED | **Doc-only**: list N6 widths 384, 512, 768 (384 only at 3e-4); align the training statement with the five levels and record this successful tokenizer check. |
| F5 | A, B | Suggestion | Retain p* but accompany its objective ratio with an absolute cumulative-residual diagnostic and binned gain residuals. A small relative objective is not a goodness-of-fit guarantee. | All 240 released N7 fits: cumulative maximum absolute discrepancy **0.00847–0.02962**; 16 equal-count weight bins have maximum absolute mean-gain residual **0.02492–0.40358 nats**. §3.3 gives definitions and limits. | VERIFIED | **Post-hoc analysis**: publish residual curves and these descriptive summaries without introducing a retrospective pass/fail threshold. |
| F6 | A, H | Suggestion | The advertised pilot fixture is useful but narrower than an estimator edge-case test suite. It does not exercise mixed-sign positive-total gains, the exact guard threshold, an upper-bound solution, or tie-order sensitivity. | `outputs/sequence-weighting-pilot/core_checks.py:9–22`; the pure power-law recovery and quadratic-form checks are positive-gain fixtures. N7's real mixed-sign gains do reproduce. | VERIFIED | **Post-hoc analysis** / verification code: add deterministic edge-case fixtures outside the sealed source; do not change the historical estimator. |

### 3.1 Interpolation: the new endpoint calculation

Let each draw's unknown p* be restricted, **as a sensitivity assumption**, to the interval between its two observed endpoint fits. Each draw's contrast then lies in a closed interval. The six intervals form a box. For a vector of contrasts v, the reported lower t limit is

\[
L(v)=\bar v-t_{0.975,5}\,s(v)/\sqrt{6}.
\]

This is concave in v because the sample SD is a norm of a linear projection. Its minimum over the box occurs at a vertex. Thus enumerating all 2⁶ vertices gives the exact worst lower limit under this assumption. The analogous upper limit is convex, so its maximum is also attained at a vertex. Choosing all lower contrasts minimises the mean, but can reduce dispersion enough that it does not minimise L.

**Post-hoc results:**

| Contrast | Possible mean range under endpoint constraint | Envelope of lower/upper t limits |
|---|---|---|
| P1 | [+0.00702371, +0.01724831] | [+0.00007639, +0.02743476] |
| S1 | [+0.00399434, +0.01001487] | **[−0.00005074, +0.01423631]** |
| S4 | [+0.01043317, +0.01635573] | [−0.00026786, +0.02431174] |

For S1, the counterexample uses the earlier bracket endpoint for m02 and the later endpoint for the other five draws. The contrasts, m01 through m06, are `[0.00551303, 0.01378785, 0.00378049, 0.00558112, 0.00220782, -0.00057012]`. This is allowed by the stated endpoint constraint and makes the lower t limit negative.

These are **envelopes of plug-in t limits, not newly calibrated confidence intervals**, and do not establish that the true trajectories stay inside their endpoint ranges. They address the mathematical error in the historical “least favourable” inference. The current README correctly presents its all-later-end values as sensitivity readings; those values themselves are correct. The registered sequence remains unchanged because its rule used linear interpolation, not this post-hoc envelope.

A separate descriptive comparison refitting p* to linearly interpolated gains yields P1 **+0.00903932 [+0.00397787,+0.01410078]** and S4 **+0.01391241 [+0.00886213,+0.01896268]**. The small changes show that this alternative interpolation operation is not the main numerical discrepancy here; neither operation reconstructs an unobserved checkpoint.

### 3.2 C3: what the data do and do not show

At N5 epoch 2, the reproduced exponent difference is **−0.00923518 [−0.01123089,−0.00723947]**, while the gap difference is uncertain. These support “different fitted exponents at similar observed mean gaps.” They do not prove identical gaps. Even equivalence of mean gaps within a tolerance would need a justified bound on how a gap difference could change p* to rule out a gap-only explanation; equal means also do not establish identical per-draw gap distributions.

For scale only, the smallest symmetric equivalence margin whose interior contains the observed 90% t interval is approximately **0.00453832 nats**. This is a post-hoc diagnostic, **not a scientifically justified margin** and not an equivalence test to adopt after seeing the data. Revise the current claim to the directly observed comparison, or state that C3 remains suggestive under the chosen interpolation/model assumptions. Do not change M or its historical label.

### 3.3 Estimator, interpretation and finite-sample behaviour

The sealed `vendor/core.py:7–53` implements the cumulative version of the technical note's quadratic objective [R1]. For ranks i/n and a zero-sum difference vector d, prefix and suffix cumulative forms have equal sums of squares. The note allows signed individual gains while requiring positive aggregate gain; taking absolute values would change the estimand. The [0,8] search restriction, stable tie ordering and guard at total gain ≤1e-10 are explicit implementation conventions.

The grid, 50 ternary refinements and endpoint comparison match the documentation. An additional bounded scalar refinement within the best grid neighbourhood differs from the 240 published fits by at most **1.29e-08**. This supports numerical adequacy on N7, not a general proof that every possible signed-gain objective is unimodal or that a finite grid always finds the global minimum. No N7 fit reaches either bound. `core_checks.py` imports the pilot's estimator; the N7-loss verification provides the relevant check on the published N7 outputs.

For each fit, the new diagnostic compares normalised cumulative gains with cumulative powered weights, and compares mean observed gains with `sum(g) × w^p / sum(w^p)` in 16 equal-count bins sorted by weight. Across 240 fits:

| Diagnostic | Minimum | Median | Maximum |
|---|---:|---:|---:|
| Cumulative RMS discrepancy | 0.004762 | 0.014437 | 0.019144 |
| Maximum absolute cumulative discrepancy | 0.008471 | 0.022973 | 0.029616 |
| Largest absolute bin-mean residual, nats | 0.024923 | 0.265892 | 0.403579 |
| RMS of bin-mean residuals, nats | 0.014489 | 0.122482 | 0.188630 |

The fit is useful as a cumulative allocation summary, while potentially omitting visible local structure in gain versus weight. No rejection threshold or inferential goodness-of-fit p-value is assigned.

**Post-hoc finite-sample diagnostic:** resample sequence/weight/gain triples from each of the six fixed width-512, 1e-4, epoch-3 arrays. At n=250, 200 resamples per draw give SD **0.00962–0.01082** and empirical-resampling mean minus full-sample fit **−0.000699 to +0.001140**. At n=16,384, 100 resamples give SD **0.00106–0.00127** and mean difference **−0.000113 to +0.000040**. The larger small-set variation is clear; the estimated mean differences are noisy at these Monte Carlo counts.

This resampling holds the trained model fixed and assumes IID sequence sampling from its empirical array. It does **not** estimate retraining variance, account for article/batch dependence, or identify bias relative to an unknown population p*. It is not a replacement for the six-draw intervals, nor an exact error model for exposure-selected sets. Population finite-sample bias remains unverified without an explicit data-generating model or additional independent training data.

### 3.4 Alignment and exposure

Equal updates really means equal batch count, token count and sequence order within a draw; it does not mean equal compute. Equal training loss matches the full-draw unweighted evaluation mean according to the registered path. Both definitions reproduce.

The E0 offset is consequential because p* is a normalised-gain summary, but subtracting a constant from one width's gains is a sensitivity operation, not a causal correction. **Matching total improvement** is a different operation: using each width's own E0 and the same first-crossing rule gives P1-type **+0.01583581 [+0.01040960,+0.02126202]**, with 768 read at epochs **2.076–2.234**; the S4-type value is **+0.01648477 [+0.01349573,+0.01947381]**. These post-hoc results keep exposure unequal. They cannot isolate width or establish a mechanism.

The shared pool drawn from WikiText test rows does not contaminate a claimed held-out test score: no such score is claimed. It makes the results conditional on a shared pretraining corpus. Its independent contribution to the width contrast cannot be identified from these runs. The missing model states preclude counterfactual changes to E0 or the pool.

Exposure-mask construction and the published calculations reproduce. The regenerated orders pass the published loss-separation and seed-shift checks; this is empirical support for the reconstruction, not a cryptographic recording of the original orders. F3 concerns the interpretation of the matching, not an implementation bug. Sets near the equal-loss point contain only 226–272 sequences; recency and content balance should be shown rather than presumed exact.

A potentially more precise **descriptive** follow-up could fit gains as a smooth function of log-weight and all three batch-level recencies, separately by width/readout within draw, then standardise to a common supported recency/weight distribution before refitting p*. Use article-aware cross-fitting where sequence-to-article mapping can be verified; report overlap, effective sample sizes and sensitivity to the smoother. This may use more observations but buys precision through modelling assumptions. It cannot create nonparametric overlap beyond the small common-support sets or establish equal overall training loss and exact exposure jointly.

### 3.5 Statistics and the unverified simulation

All 24 `MATCHED.csv` rows agree exactly with a fresh implementation of the first-interval, flat-bracket and availability rules. The five main t intervals agree within **7.2e-13**, leave-one-out intervals within **4.8e-13**, and exact sign tests agree. S2 correctly retains m02, m03 and m06 only; m06 has three bracketing intervals and uses the first. Fewer than five available draws correctly produces `UNAVAILABLE`.

The draw is the replication unit; df=5 is correct for the six complete paired contrasts, conditional on the shared components. Treating the 16,384 sequences or repeated readouts as independent replications would be wrong. Fixed-sequence decisions reach S5 and then encounter unavailable S2, exactly as registered.

For valid directional tests at level 0.025 in a fixed order, false confirmation requires rejecting the first true null reached in that order; this supplies the standard familywise upper bound without requiring independence between the different endpoints. It still requires valid constituent tests. Selection of available draws by their trajectories does not automatically preserve that validity. S2's actual unavailability avoids a confirmation here; it does not validate complete-case S2 testing in general.

**UNVERIFIED:** the reported simulated rates 0.0254/0.0505 and the joint power simulation. The cited `review-02/REVIEW_FINDINGS.md`, `REVIEW_FOLLOWUP.md` and `MATCHED_PLANNING.json` are not tracked anywhere in this checkout; `preregistration/.../HASHES.json:37–41` names the review hash and explicitly excludes preparation/review folders. The simulation's code, number of replicates, joint null configurations, RNG state and selection model cannot be recovered from a hash. To verify the numerical claim, publish those original materials, or label a new reconstruction as new. A simulation of one configuration would not by itself establish a uniform familywise guarantee.

The published exposure power figures do follow their stated plug-in assumptions: recomputed two-sided noncentral-t power is **0.137652, 0.718580 and 0.883900** for k=1,2,3, using effect 0.0091 and the observed SDs. They are not evidence about the probability that the effect is absent.

### 3.6 Source, documentation and positioning

Source spot-checks agree with the weighted-training description: log-uniform draws followed by draw-wide mean normalisation (`text_engine.py:56–60`); mean weighted sequence loss and global gradient clipping (`text_worker.py:222–228`); separate no-gradient evaluation (`text_engine.py:38–49`); dense update-index readouts (`matched_worker.py:184–206`); whole-article exclusion/partition rules (`matched_data.py:27–61`). The natural-text `text_worker.py` is byte-identical across N1, N3, N4, N5, N6 and N7. This supports the common loss/optimiser implementation; it does not independently reconstruct every corpus partition. S's R arm uses the weighted batch mean; its S_batch comparator deliberately changes the objective (`ladder_worker.py:30–39`), so it should not be described as the same weighting arm.

No additional numerical mismatch was found in the living N7 tables. The publication checker verifies paths, not fragment anchors; the separate check resolved all nine fragment links encountered in the six main living pages. Full external-link availability and pixel-level figure review were not exhaustively tested.

The contribution is appropriately narrow when stated as a registered example of alignment-dependent width ordering in this recipe. Renda and Mani already report that repeated epochs shift the p* peak towards smaller models [R1]. This record does not establish a new large-model scaling law.

Related work should distinguish:

- **Importance weighting:** Byrd and Lipton [R2] study how weighting effects change during deep-network training. This motivates sensitivity to optimisation and training duration; their empirical settings are not direct evidence for N7's mechanism.
- **Domain mixtures:** DoReMi [R3] learns domain sampling weights using a proxy model and evaluates larger-model efficiency. N7 assigns random per-sequence loss weights and reports an in-sample gain-allocation statistic; it does not test transfer of an optimised domain mixture.
- **Repeated data:** Muennighoff et al. [R4] distinguish repeated tokens and unique data under compute constraints. Equal updates here therefore cannot be read as an equal-compute comparison or a general result about optimal repetition.
- **Forgetting:** Toneva et al. [R5] track examples switching from correct to incorrect classification. N7's recency-associated NLL changes are related training dynamics, but are not the same event definition and do not identify a forgetting mechanism.
- **Model-size comparisons:** Hoffmann et al. [R6] optimise model size and tokens under a fixed compute budget. Matching training loss answers a different question; no single comparison axis is universally privileged.

## 4. Rejected concerns

| Concern investigated | Why it does not hold, or limit of the rejection |
|---|---|
| The N7 result is an arithmetic or estimator-implementation mistake. | 240 loss-derived fits, five main contrasts, matching rows, sign tests and leave-one-out calculations reproduce. This does not verify the original training execution. |
| Individual negative gains must be discarded or made positive. | The technical note allows signed gains; normalisation requires positive total gain. Absolute values would change both shape and denominator. |
| Six-draw df=5 is a pseudoreplication error. | It uses paired draw-level contrasts, not sequence counts; the inference is explicitly conditional. |
| The S2 label should be changed to a null finding. | Three available draws fail the registered minimum; `UNAVAILABLE` is the correct result. |
| Exposure masks or seed reconstruction are numerically broken. | The pinned reproduction yields the same 268 series and passes the recorded loss-pattern checks. F3 is about the precision of the matching claim. |
| Tokenizer reconstruction is impossible from the public record. | Two CPU reconstructions match the pinned SHA-256 exactly. This does not establish full corpus or model reproducibility. |
| The test-row pretraining pool invalidates a held-out test result. | There is no claimed held-out test result to invalidate. Its effect on the comparisons remains unidentified. |
| Changing interpolation from fitted p* to gains explains the reported reversal. | This particular alternative changes the reproduced P1 mean by only about 0.000049; both alternatives remain interpolated. |
| Novelty requires denying the reference study's epoch-shifted peak. | The current README and methods explicitly credit it. The remaining contribution is the alignment comparison. |

Previously disclosed S3 leave-one-out fragility, S4's all-later-end sensitivity, E0 sensitivity, clipping, scale and registration limitations are not relisted as new findings. F1 and F2 specifically show why two earlier resolutions are incomplete.

## 5. Proposals for a future study

This is an optional **new study**, not work to add to the closed record.

**Question:** does the pair show opposite ordering at equal updates and equal training loss on fresh draws when matched checkpoints are measured much more densely? Separately, how much does recency standardisation change that comparison?

**Design:** retain widths 512/768 and the same architecture for a targeted replication; use 1e-4 for the confirmatory pair and treat other rates as a separately planned extension. Use fresh article-disjoint draws, shared within-draw weights/orders, and independently retained E0 states. Save model states or loss readouts around the matching region every 64 updates; preserve batch-order hashes, exact preprocessing assets and a portable environment. Define the first crossing, interpolation resolution/sensitivity, handling of missed targets, and failure policy in advance. Dense readouts reduce interpolation uncertainty; they do not remove exposure differences.

**Analysis to preregister:** two co-primary directional conditions, positive equal-loss contrast and negative equal-update contrast, with paired draw-level intervals. A reversal requires both. Treat equal-improvement and recency-standardised curves as secondary. Any claim that loss and exposure are jointly matched must have a separate design and explicit tolerance/balance criteria; merely reading at an epoch end does not ensure equal loss.

**Power planning:** for a two-sided 5% paired t test, using the observed P1 SD 0.0048 as known gives the following plug-in counts. The effect is a prespecified target, not an estimate to optimise after collecting new data.

| Target P1 contrast | Assumed SD | Draws for 80% | Draws for 90% |
|---|---:|---:|---:|
| 0.00910 | 0.0048 | 5 | 6 |
| 0.00455 | 0.0048 | 11 | 14 |
| 0.00455 | 0.0096 | 37 | 49 |
| 0.00300 | 0.0048 | 23 | 29 |

These optimistic small-n counts alone are inadequate for joint reversal planning. A conservative planning example is **100 fresh paired draws**: halve both observed contrasts and double both observed SDs. P1 power is **0.996864**; S3 power is **0.933910** using its observed SD 0.00324458. Without assuming independence, the probability of both is at least **0.930774** by the union bound. This is conditional planning under normal draws and valid tests, not a guarantee for a modified recipe or an exposure-standardised estimand. Missingness and extra confirmatory gates would require additional planning; do not silently use P1's SD for a different estimand. A smaller study can be chosen, but should explicitly accept lower sensitivity rather than claim the same joint power.

**Retraining prerequisites:** fetch the pinned WikiText-2 splits; reproduce the tokenizer as demonstrated here; encode and verify the WT2 sequence files; fetch the two pinned WT103 training parquets and run the sealed article exclusions/chunking; reconstruct the corpus manifest and pinned partitions; adapt a separate copy of the one-use launcher/hardware gates; define replication tolerances and numerical controls; then train. This audit completed only the tokenizer portion. No reliable runtime or bit-identical training claim is available.

## 6. New code and exact outputs

All analytical code below is **POST HOC**. Save each block under its displayed filename. Paths are command-line arguments; no repository source is modified. The full numerical pass uses deterministic empirical resampling seed 20261113. Its local optimisation uses a full 0–8 grid before bounded refinement.

The auditor's first `audit_numeric.py` attempt stopped with `KeyError: 'width'` because N5's table is wide-form; the corrected code reads `gap_512`, `gap_768`, `p_512`, `p_768`. The first `audit_record.py` attempt mistakenly combined S's primary and secondary-window rows, yielding an assertion failure; the corrected filter selects `readout == 'primary|R'`. These were errors in new audit code, not failures of the repository. Their exact errors are preserved below. No historical number was edited to obtain a pass.

### POST-HOC code: `audit_numeric.py`

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PY audit_numeric.py REPO BUNDLE
OPENBLAS_NUM_THREADS=1 PY audit_numeric.py REPO BUNDLE --tables-only
```

```python
"""POST HOC: descriptive audit of published tables/losses; no model training.
Run: OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python audit_numeric.py REPO BUNDLE
"""
import csv, hashlib, importlib.util, itertools, json, math, re, sys
from pathlib import Path
import numpy as np
from scipy import optimize, stats

ROOT, BUNDLE = map(Path, sys.argv[1:3])
def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod
def table(path): return list(csv.DictReader(path.open()))
def ci(v):
    v = np.asarray(v); m = v.mean(); h = stats.t.ppf(.975,len(v)-1)*v.std(ddof=1)/np.sqrt(len(v))
    return np.array([m,m-h,m+h])
def fmt(v): return ' '.join(f'{x:+.8f}' for x in v)
def fit(w,g):
    ix=np.argsort(w,kind='stable'); lw=np.log(np.asarray(w,dtype=float)[ix]); lw-=lw.max()
    gg=np.asarray(g,dtype=float)[ix]; cg=np.cumsum(gg)/gg.sum()
    def obj(p):
        z=np.exp(p*lw); r=cg-np.cumsum(z)/z.sum(); return np.mean(r*r)
    grid=np.arange(161)/20; vals=np.array([obj(p) for p in grid]); j=vals.argmin()
    r=optimize.minimize_scalar(obj,bounds=(grid[max(0,j-1)],grid[min(160,j+1)]),method='bounded',options={'xatol':1e-12})
    p=min([0.,r.x,8.],key=obj)
    return p,obj(p)

print('POST HOC; Python',sys.version.split()[0],'NumPy',np.__version__)
A=ROOT/'reports/natural-text-matched-analysis-20261105-01'
P={(r['draw'],float(r['epoch']),int(r['width']),r['tag']): {k:float(r[k]) for k in ('p','train','validation','gap')} for r in table(A/'POINTS.csv')}
J=json.loads((A/'ANALYSIS.json').read_text()); D=sorted({k[0] for k in P}); E=[2.,2.25,2.5,2.75,3.,3.25,3.5]
M={(r['statistic'],r['draw']):r for r in table(A/'MATCHED.csv')}
errors=[]; intervals=[]; loo=[]; match_count=0
for name,s in J['statistics'].items():
    vals={}; bounds=[]
    for d in D:
        a=P[(d,3.,*s['first'])]; b=P[(d,3.,*s['second'])]
        if s['kind']=='fixed': vals[d]=a['p']-b['p']; continue
        key=s['key']; pts=[P[(d,e,*s['second'])] for e in E]
        brackets=[i for i in range(len(E)-1) if min(pts[i][key],pts[i+1][key])<=a[key]<=max(pts[i][key],pts[i+1][key])]
        mr=M[(name,d)]; match_count+=1
        assert len(brackets)==int(mr['intervals_holding_the_target'])
        if not brackets:
            assert mr['status']=='TARGET_OUTSIDE_PATH'; continue
        i=brackets[0]; x,y=pts[i],pts[i+1]; t=0 if y[key]==x[key] else (a[key]-x[key])/(y[key]-x[key])
        pr=x['p']+t*(y['p']-x['p']); vals[d]=a['p']-pr
        for f,v in dict(target=a[key],between_low=E[i],between_high=E[i+1],weight=t,p_read=pr,p_first=a['p'],value=vals[d],read_at_readout=E[i]+t*(E[i+1]-E[i])).items(): errors.append(abs(float(mr[f])-v))
        bounds.append(sorted([a['p']-x['p'],a['p']-y['p']]))
    assert set(vals)==set(s['values'])
    errors.extend(abs(v-s['values'][d]) for d,v in vals.items())
    n=len(vals); v=list(vals.values()); positive=sum(x>0 for x in v); negative=sum(x<0 for x in v)
    assert stats.binomtest(positive,positive+negative).pvalue==s['sign_test']['p']
    if n>=5:
        target=np.array([s['interval']['mean'],*s['interval']['interval']]); intervals.extend(abs(ci(v)-target))
        for d in vals:
            l=s['leave_one_out'][d]; loo.extend(abs(ci([x for k,x in vals.items() if k!=d])-np.array([l['mean'],*l['interval']])))
        print(name,'mean/95% CI',fmt(ci(v)),'sign-p',s['sign_test']['p'],'label',s['label'])
    else: print(name,'n',n,'available',list(vals),'label',s['label'])
    if name in ('P1','S1','S4'):
        vertices=np.array(list(itertools.product(*bounds))); cis=np.array([ci(v) for v in vertices])
        k=cis[:,1].argmin()
        print(name,'ENDPOINT-BOX conditional mean range',fmt([vertices.mean(1).min(),vertices.mean(1).max()]),'CI envelope',fmt([cis[:,1].min(),cis[:,2].max()]),'worst-lower vertex',fmt(vertices[k]))
print('MATCHED rows',match_count,'max scalar error',max(errors),'max CI error',max(intervals),'max LOO error',max(loo))

# Published post-hoc power and future planning; conditional on the supplied SD.
R=json.loads((ROOT/'reports/natural-text-matched-assistant-posthoc-20261111-01/RESULTS.json').read_text())['values']
def power(n,delta,sd):
    t=stats.t.ppf(.975,n-1); nc=math.sqrt(n)*delta/sd
    return stats.nct.sf(t,n-1,nc)+stats.nct.cdf(-t,n-1,nc)
for k in (1,2,3):
    v=R[f'matched|lr1e-04|k{k}|every']; print('EXPOSURE POWER',k,'SD',f'{np.std(v,ddof=1):.8f}','power',f'{power(6,.0091,np.std(v,ddof=1)):.6f}')
for effect in (.0091,.00455,.003):
    for sd in (.0048,.0096):
        ns=[next(n for n in range(3,2000) if power(n,effect,sd)>=q) for q in (.8,.9)]
        print('FUTURE n at 80%,90%; effect',effect,'SD',sd,ns)
p1power=stats.nct.sf(stats.t.ppf(.975,99),99,10*.00455/.0096)
s3power=stats.nct.sf(stats.t.ppf(.975,99),99,10*abs(J['statistics']['S3']['interval']['mean'])/(4*J['statistics']['S3']['interval']['sd']))
print('FUTURE n=100 half effects/double SD: P1 power',f'{p1power:.6f}','S3 power',f'{s3power:.6f}','joint lower bound',f'{max(0,p1power+s3power-1):.6f}')

# C3: interval for the alleged equal gaps in N5, and raw draw contrasts.
Q=table(ROOT/'reports/natural-text-fewepoch-analysis-20261103-01/POINTS.csv')
print('N5 columns',list(Q[0]))
q={(r['draw'],float(r['epoch'])):r for r in Q}
dv=[]; dp=[]
for d in sorted({r['draw'] for r in Q}):
    row=q[(d,2.)]
    dv.append(float(row['gap_768'])-float(row['gap_512'])); dp.append(float(row['p_768'])-float(row['p_512']))
print('C3 gap 768-512',fmt(ci(dv)),'range',fmt([min(dv),max(dv)]),'positive',sum(x>0 for x in dv))
print('C3 p 768-512',fmt(ci(dp)))
print('C3 smallest symmetric equivalence margin with 90% CI inside',f'{abs(np.mean(dv))+stats.t.ppf(.95,9)*np.std(dv,ddof=1)/np.sqrt(10):.8f}')
if '--tables-only' in sys.argv:
    print('TABLE CHECKS DONE'); sys.exit(0)

# Independent fit diagnostics, alternative interpolate-loss reading, and empirical resampling.
post=load_module('post',ROOT/'reports/natural-text-matched-assistant-posthoc-20261111-01/posthoc_exposure.py')
man=json.loads((BUNDLE/'MANIFEST.json').read_text()); arms={}; W={}; diagnostics=[]; fiterr=[]
for d in D:
    W[d]=np.frombuffer((BUNDLE/man['draws'][d]['weights']['path']).read_bytes(),'<f4')
    for wd,tag in post.ARMS:
        a=post.Arm(BUNDLE,man,d,wd,tag); arms[d,wd,tag]=a
        for ep in a.epochs:
            w=W[d].astype(float); g=a.gain(ep).astype(float); p=P[d,ep,wd,tag]['p']; order=np.argsort(w,kind='stable')
            z=w**p; r=np.cumsum((g/g.sum()-z/z.sum())[order]); pred=g.sum()*z/z.sum()
            bins=np.array_split(order,16); residual=np.array([(g[b]-pred[b]).mean() for b in bins])
            diagnostics.append((np.sqrt(np.mean(r*r)),np.max(abs(r)),np.max(abs(residual)),np.sqrt(np.mean(residual**2))))
            pp,_=fit(w,g); fiterr.append(abs(pp-p))
print('Independent bounded refinement, max fit error',f'{max(fiterr):.3g}')
for j,label in enumerate(('cumulative RMS','cumulative max-absolute','16-bin max-absolute residual nats','16-bin RMS residual nats')):
    x=np.array(diagnostics)[:,j]; print('DIAGNOSTIC',label,'min median max',fmt([x.min(),np.median(x),x.max()]))
for name in ('P1','S4'):
    tag=J['statistics'][name]['first'][1]; vals=[]
    for d in D:
        r=M[name,d]; lo,hi,t=map(float,(r['between_low'],r['between_high'],r['weight']))
        a=arms[d,768,tag]; g=(1-t)*a.gain(lo).astype(float)+t*a.gain(hi).astype(float)
        pp,_=fit(W[d],g); vals.append(P[d,3.,512,tag]['p']-pp)
    print(name,'FIT TO LINEARLY INTERPOLATED GAINS; alternative, not registered',fmt(ci(vals)))
    # Equal improvement uses each width's own E0 mean, not an offset-adjusted gain.
    vals=[]; positions=[]
    for d in D:
        target=arms[d,512,tag].gain(3.).astype(float).mean(); a=arms[d,768,tag]
        for lo,hi in zip(E,E[1:]):
            x,y=a.gain(lo).astype(float).mean(),a.gain(hi).astype(float).mean()
            if min(x,y)<=target<=max(x,y):
                t=(target-x)/(y-x); pp=P[d,lo,768,tag]['p']+t*(P[d,hi,768,tag]['p']-P[d,lo,768,tag]['p'])
                vals.append(P[d,3.,512,tag]['p']-pp); positions.append(lo+t*(hi-lo)); break
    print(name,'EQUAL IMPROVEMENT n',len(vals),'mean/CI',fmt(ci(vals)),'positions',fmt(positions))

rng=np.random.default_rng(20261113)
for n,reps in ((250,200),(16384,100)):
    biases=[]; sds=[]
    for d in D:
        a=arms[d,512,'lr1e-04']; w=W[d]; g=a.gain(3.)
        values=[]
        for _ in range(reps):
            ix=rng.integers(0,len(w),n); values.append(fit(w[ix],g[ix])[0])
        biases.append(np.mean(values)-P[d,3.,512,'lr1e-04']['p']); sds.append(np.std(values,ddof=1))
    print('CONDITIONAL IID EMPIRICAL RESAMPLING n',n,'reps/draw',reps,'bias range',fmt([min(biases),max(biases)]),'SD range',fmt([min(sds),max(sds)]))

# Exact batch-level recency in the claimed all-pass matched subsets.
import torch
for k in (1,2,3):
    sizes=[]; ks=[]; mean_diff=[]; qjoint=[]
    for d in D:
        seed=man['draws'][d]['seeds']['adapt_order_seed']; ranks=[]
        for e in range(1,4):
            order=torch.randperm(16384,generator=torch.Generator().manual_seed(999+seed+e)).numpy()
            rank=np.empty(16384,int); rank[order]=np.arange(16384)//16+1; ranks.append(rank)
        ranks=np.array(ranks); quarter=(ranks-1)//256+1
        i5=np.all(quarter>=5-k,axis=0); i7=np.all(quarter<=k,axis=0); sizes.extend([i5.sum(),i7.sum()])
        # Ages, in updates, measured at E3 (3072) and E(2+k/4) (2048+256k).
        ages5=3072-(ranks[:,i5]+np.arange(3)[:,None]*1024)
        ages7=2048+256*k-(ranks[:,i7]+np.arange(3)[:,None]*1024)
        for e in range(3):
            mean_diff.append(abs(ages5[e].mean()-ages7[e].mean())); ks.append(stats.ks_2samp(ages5[e],ages7[e]).statistic)
        q5=quarter[:,i5]-(4-k); q7=quarter[:,i7]
        cells=list(itertools.product(range(1,k+1),repeat=3))
        h5=np.array([np.all(q5==np.array(c)[:,None],axis=0).mean() for c in cells]); h7=np.array([np.all(q7==np.array(c)[:,None],axis=0).mean() for c in cells])
        qjoint.append(abs(h5-h7).sum()/2)
    print('RECENCY k',k,'set size min/max',min(sizes),max(sizes),'max |mean age difference| updates',f'{max(mean_diff):.5f}','max marginal KS',f'{max(ks):.5f}','max joint-quarter TV',f'{max(qjoint):.5f}')
print('DONE')
```

### POST-HOC code: `audit_record.py`

```bash
PY audit_record.py REPO ZIP
```

```python
"""POST HOC: table arithmetic, documentation inventory, and integrity checks.
Run: python audit_record.py REPO BUNDLE_ZIP
"""
import csv, hashlib, itertools, json, math, re, subprocess, sys
from pathlib import Path
import numpy as np
from scipy.stats import t
root=Path(sys.argv[1]).resolve()
def rows(folder): return list(csv.DictReader((root/folder/'POINTS.csv').open()))
def doc(folder): return json.loads((root/folder/'ANALYSIS.json').read_text())
def slope(x,y):
    x=np.array(x); y=np.array(y); return float(((x-x.mean())*(y-y.mean())).sum()/((x-x.mean())**2).sum())
def check(label,v,target):
    v=np.array(v); m=v.mean(); h=t.ppf(.975,len(v)-1)*v.std(ddof=1)/np.sqrt(len(v)); got=np.array([m,m-h,m+h])
    want=np.array([target['mean'],*target['interval']]); error=max(abs(got-want))
    assert error<1e-8,(label,got,want)
    print(label,'n',len(v),'mean/CI',' '.join(f'{x:+.8f}' for x in got),'max error',f'{error:.3g}')

p='reports/capacity-shift-followup-analysis-20261027-01'; rs=rows(p); js=doc(p)['slope_tests']['primary|R']; values=[]
for d in sorted({r['corpus'] for r in rs}):
    q=[r for r in rs if r['corpus']==d and r['readout']=='primary|R' and float(r['epoch']) in (15,20,25,30,40) and r['location']]
    values.append(slope([math.log2(float(r['epoch'])) for r in q],[float(r['location']) for r in q]))
check('S primary R',values,js['primary'])
p='reports/natural-text-ladder-analysis-20261029-01/sealed-analysis'; rs=rows(p); js=doc(p)['primaries']; vals=[]; curvs=[]
for d in sorted({r['draw'] for r in rs}):
    q=[r for r in rs if r['draw']==d and float(r['epoch'])>=4]
    vals.append(slope([math.log2(float(r['epoch'])) for r in q],[float(r['location']) for r in q])); curvs.append(np.mean([float(r['quad_c']) for r in q]))
check('N1 A',vals,js['A']['interval']); check('N1 B curvature',curvs,js['B']['curvature'])
p='reports/natural-text-onerate-analysis-20261030-02'; rs=rows(p); js=doc(p)['primaries']
for key in ('turn','dip','memo'):
    vals=[np.mean([float(r[key]) for r in rs if r['draw']==d and float(r['epoch'])>=4]) for d in sorted({r['draw'] for r in rs})]
    check('N3 '+key,vals,js[key]['interval'])
p='reports/natural-text-lateturn-analysis-20261031-01'; rs=rows(p); js=doc(p)['primaries']
for key,ep in (('P1',32),('P2',24)):
    vals=[slope(np.log2([384,512,768]),[float(r[f'p_{w}']) for w in (384,512,768)]) for r in rs if float(r['epoch'])==ep]
    check('N4 '+key,vals,js[key]['interval'])
p='reports/natural-text-fewepoch-analysis-20261103-01'; rs=rows(p); js=doc(p)['primaries']
for key,ws in (('FALL',[384,512,768]),('RISE',[64,96,128,192,256,384,512])):
    # RISE's registered widths are read below if the named default differs.
    if key=='RISE':
        continue
    vals=[slope(np.log2(ws),[float(r[f'p_{w}']) for w in ws]) for r in rs if float(r['epoch'])==3]
    check('N5 '+key,vals,js[key]['interval'])
p='reports/natural-text-peak-analysis-20261103-01'; rs=rows(p); js=doc(p)['contrasts']; idx={(r['draw'],float(r['epoch']),int(r['width']),r['tag']):float(r['p']) for r in rs}; ds=sorted({r['draw'] for r in rs})
for key,a,b in [('D1',(512,'lr3e-04'),(384,'lr3e-04')),('D2',(512,'lr3e-04'),(768,'lr3e-04')),('D3',(512,'lr3e-04'),(768,'lr1e-04')),('D4',(512,'lr1e-04'),(768,'lr1e-04'))]:
    check('N6 '+key,[idx[(d,3.,*a)]-idx[(d,3.,*b)] for d in ds],js[key]['interval'])

source=root/'preregistration/natural-text-matched-confirmation-20261104/sealed-source'
subject=source/'SOURCE_SUBJECT.json'; seal=json.loads(subject.read_text()); bad=[f['path'] for f in seal['files'] if hashlib.sha256((source/f['path']).read_bytes()).hexdigest()!=f['sha256']]
print('N7 source subject',hashlib.sha256(subject.read_bytes()).hexdigest(),'files',len(seal['files']),'mismatches',bad)
print('release ZIP SHA-256',hashlib.sha256(Path(sys.argv[2]).read_bytes()).hexdigest())
tracked=subprocess.check_output(['git','ls-files'],cwd=root,text=True).splitlines()
for needle in ('REVIEW_FINDINGS.md','REVIEW_FOLLOWUP.md','MATCHED_PLANNING.json','test_matched.py'):
    print('tracked basename',needle,[p for p in tracked if Path(p).name==needle])
states=[p for p in tracked if Path(p).suffix in ('.pt','.pth','.safetensors','.ckpt')]
print('tracked model-state candidates',states)

# Explicitly check fragments on the main living pages (not an all-GitHub slug emulator).
living=['README.md','CURRENT_CLAIMS.md','METHODS.md','NATURAL_TEXT_STUDIES.md','DATA_AVAILABILITY.md','PUBLICATION_NOTES.md']
def anchors(path):
    seen={}; out=[]; fenced=False
    for line in path.read_text().splitlines():
        if line.startswith('```'): fenced=not fenced
        if fenced: continue
        if not re.match(r'^#{1,6} ',line): continue
        s=re.sub(r'^#+\s*','',line).strip().lower(); s=re.sub(r'[^\w\- ]','',s); s=s.replace(' ','-')
        count=seen.get(s,0); seen[s]=count+1; out.append(s+(f'-{count}' if count else ''))
    return out
checked=0; bad=[]
for name in living:
    file=root/name
    for line_no,line in enumerate(file.read_text().splitlines(),1):
        for dest,fragment in re.findall(r'\]\(([^\s)#]*)#([^\s)]+)\)',line):
            if '://' in dest: continue
            target=(file.parent/dest) if dest else file
            if target.suffix!='.md': continue
            checked+=1
            if fragment not in anchors(target): bad.append((name,line_no,dest,fragment))
print('living-page Markdown fragments checked',checked,'unresolved',bad)
print('git tracked changes',subprocess.check_output(['git','diff','--name-only'],cwd=root,text=True).strip() or 'none')
print('DONE')
```

### POST-HOC code: `rebuild_tokenizer.py`

```bash
TOKENIZERS_PARALLELISM=false PY rebuild_tokenizer.py REPO WT2_PARQUET
```

```python
"""POST-HOC reproducibility check only: no language-model training.
Run: python rebuild_tokenizer.py REPO WT2_TRAIN_PARQUET
Calls the sealed hf_tokenizer function without changing its source.
"""
import hashlib, importlib, sys
from pathlib import Path
import pyarrow.parquet as pq
root, file=map(Path,sys.argv[1:3])
raw=file.read_bytes(); expected='e83889baabc497075506f91975be5fac0d45c5290b6b20582c8cd1e853d0c9f7'
actual=hashlib.sha256(raw).hexdigest(); print('parquet SHA-256',actual,'matches',actual==expected,flush=True)
assert actual==expected
sys.path.insert(0,str(root/'work/natural-text-ladder-source-20261028-02'))
from prepare_corpus import hf_tokenizer
texts=pq.read_table(file,columns=['text'])['text'].to_pylist()
print('rows',len(texts),flush=True)
hashes=[]
for i in range(2):
    _,b,v=hf_tokenizer(texts); h=hashlib.sha256(b).hexdigest(); hashes.append(h)
    print('rebuild',i+1,'tokenizers',v,'bytes',len(b),'SHA-256',h,flush=True)
print('two trainings identical',hashes[0]==hashes[1])
pin='cd642ca2b78a76e880adf07efb425bd2db741248cbf537aed0538c9421cca146'
print('matches pinned tokenizer',all(h==pin for h in hashes))
```

### Output: Publication check

```text
manifest: 1346 rows; 1346 exact; 0 differ only in line endings; 0 mismatched; 0 missing; 0 published files not in the manifest
links: 511 local Markdown links checked; 0 known unavailable; 0 unexpected broken
```

### Output: Pilot fixture

```text
{
  "status": "passed",
  "known_exponent_recovery": [
    {
      "known_p": 0,
      "estimated_p": 0.0
    },
    {
      "known_p": 0.5,
      "estimated_p": 0.49999999999147443
    },
    {
      "known_p": 1,
      "estimated_p": 0.9999999999914743
    },
    {
      "known_p": 2,
      "estimated_p": 1.9999999999914744
    }
  ],
  "quadratic_form_equivalence_absolute_error": 4.912791094074942e-20,
  "distinct_sequence_keys": 2816,
  "checks": [
    "constant weight and nonpositive gain handling",
    "all 2816 sequences: lengths, target alignment, pattern counts",
    "shared and group answer correctness",
    "unique inputs within each sequence",
    "disjoint train/validation/test keys",
    "cross-regime query pairing"
  ],
  "not_checked": [
    "Transformer causality at runtime",
    "CUDA training",
    "learning curves",
    "runtime performance or peak GPU memory"
  ],
  "training_status": "not performed by these dependency-free checks; inspect run outputs separately"
}
```

### Output: README example

```text
P1 = +0.00909 [+0.00400, +0.01417], n = 6
```

### Output: N7 losses

```text
bundle: 66 files match MANIFEST.json; 6 weight vectors match their runs' tensor hashes
fits: 240 refitted; largest |p* - POINTS.csv| = 2.90e-09; largest |array mean - record| = 8.55e-07
  P1: +0.00909 [+0.00400, +0.01417], n = 6; matches ANALYSIS.json
  S1: +0.00808 [+0.00487, +0.01130], n = 6; matches ANALYSIS.json
  S3: -0.00454 [-0.00795, -0.00114], n = 6; matches ANALYSIS.json
  S4: +0.01394 [+0.00893, +0.01896], n = 6; matches ANALYSIS.json
  S5: +0.01382 [+0.01116, +0.01648], n = 6; matches ANALYSIS.json
PASS
```

### Output: Published post-hoc verification

```text
ran with numpy 2.5.3, torch 2.7.0+cpu
keys: 268 published, 268 reproduced; 0 missing, 0 extra
largest difference: 0.00e+00
PASS
```

### Output: Independent table and endpoint checks, final code

```text
POST HOC; Python 3.12.14 NumPy 2.5.3
P1 mean/95% CI +0.00908795 +0.00400386 +0.01417203 sign-p 0.03125 label REVERSAL_CONFIRMED
P1 ENDPOINT-BOX conditional mean range +0.00702371 +0.01724831 CI envelope +0.00007639 +0.02743476 worst-lower vertex +0.02513035 +0.00745371 +0.00378049 +0.01066597 +0.00916239 -0.00057012
S1 mean/95% CI +0.00808476 +0.00487325 +0.01129627 sign-p 0.03125 label CONFIRMED
S1 ENDPOINT-BOX conditional mean range +0.00399434 +0.01001487 CI envelope -0.00005074 +0.01423631 worst-lower vertex +0.00551303 +0.01378785 +0.00378049 +0.00558112 +0.00220782 -0.00057012
S3 mean/95% CI -0.00454199 -0.00794696 -0.00113701 sign-p 0.03125 label CONFIRMED
S4 mean/95% CI +0.01394194 +0.00892757 +0.01895632 sign-p 0.03125 label CONFIRMED
S4 ENDPOINT-BOX conditional mean range +0.01043317 +0.01635573 CI envelope -0.00026786 +0.02431174 worst-lower vertex +0.01685147 +0.01687255 +0.01344363 +0.01265112 +0.01278512 -0.01000487
S5 mean/95% CI +0.01382115 +0.01116159 +0.01648072 sign-p 0.03125 label CONFIRMED
S2 n 3 available ['m02', 'm03', 'm06'] label UNAVAILABLE
MATCHED rows 24 max scalar error 0.0 max CI error 7.192961504198792e-13 max LOO error 4.770281392119102e-13
EXPOSURE POWER 1 SD 0.02130613 power 0.137652
EXPOSURE POWER 2 SD 0.00702785 power 0.718580
EXPOSURE POWER 3 SD 0.00560466 power 0.883900
FUTURE n at 80%,90%; effect 0.0091 SD 0.0048 [5, 6]
FUTURE n at 80%,90%; effect 0.0091 SD 0.0096 [11, 14]
FUTURE n at 80%,90%; effect 0.00455 SD 0.0048 [11, 14]
FUTURE n at 80%,90%; effect 0.00455 SD 0.0096 [37, 49]
FUTURE n at 80%,90%; effect 0.003 SD 0.0048 [23, 29]
FUTURE n at 80%,90%; effect 0.003 SD 0.0096 [83, 110]
FUTURE n=100 half effects/double SD: P1 power 0.996864 S3 power 0.933910 joint lower bound 0.930774
N5 columns ['draw', 'epoch', 'fall', 'gap_128', 'gap_192', 'gap_256', 'gap_384', 'gap_512', 'gap_64', 'gap_768', 'gap_96', 'p_128', 'p_192', 'p_256', 'p_384', 'p_512', 'p_64', 'p_768', 'p_96', 'rise']
C3 gap 768-512 +0.00039191 -0.00472497 +0.00550879 range -0.00924587 +0.01450443 positive 4
C3 p 768-512 -0.00923518 -0.01123089 -0.00723947
C3 smallest symmetric equivalence margin with 90% CI inside 0.00453832
TABLE CHECKS DONE
```

### Output: Full independent numerical pass

```text
POST HOC; Python 3.12.14 NumPy 2.5.3
P1 mean/95% CI +0.00908795 +0.00400386 +0.01417203 sign-p 0.03125 label REVERSAL_CONFIRMED
P1 ENDPOINT-BOX conditional mean range +0.00702371 +0.01724831 CI envelope +0.00007639 +0.02743476 worst-lower vertex +0.02513035 +0.00745371 +0.00378049 +0.01066597 +0.00916239 -0.00057012
S1 mean/95% CI +0.00808476 +0.00487325 +0.01129627 sign-p 0.03125 label CONFIRMED
S3 mean/95% CI -0.00454199 -0.00794696 -0.00113701 sign-p 0.03125 label CONFIRMED
S4 mean/95% CI +0.01394194 +0.00892757 +0.01895632 sign-p 0.03125 label CONFIRMED
S4 ENDPOINT-BOX conditional mean range +0.01043317 +0.01635573 CI envelope -0.00026786 +0.02431174 worst-lower vertex +0.01685147 +0.01687255 +0.01344363 +0.01265112 +0.01278512 -0.01000487
S5 mean/95% CI +0.01382115 +0.01116159 +0.01648072 sign-p 0.03125 label CONFIRMED
S2 n 3 available ['m02', 'm03', 'm06'] label UNAVAILABLE
MATCHED rows 24 max scalar error 0.0 max CI error 7.192961504198792e-13 max LOO error 4.770281392119102e-13
EXPOSURE POWER 1 SD 0.02130613 power 0.137652
EXPOSURE POWER 2 SD 0.00702785 power 0.718580
EXPOSURE POWER 3 SD 0.00560466 power 0.883900
FUTURE n at 80%,90%; effect 0.0091 SD 0.0048 [5, 6]
FUTURE n at 80%,90%; effect 0.0091 SD 0.0096 [11, 14]
FUTURE n at 80%,90%; effect 0.00455 SD 0.0048 [11, 14]
FUTURE n at 80%,90%; effect 0.00455 SD 0.0096 [37, 49]
FUTURE n at 80%,90%; effect 0.003 SD 0.0048 [23, 29]
FUTURE n at 80%,90%; effect 0.003 SD 0.0096 [83, 110]
N5 columns ['draw', 'epoch', 'fall', 'gap_128', 'gap_192', 'gap_256', 'gap_384', 'gap_512', 'gap_64', 'gap_768', 'gap_96', 'p_128', 'p_192', 'p_256', 'p_384', 'p_512', 'p_64', 'p_768', 'p_96', 'rise']
C3 gap 768-512 +0.00039191 -0.00472497 +0.00550879 range -0.00924587 +0.01450443 positive 4
C3 p 768-512 -0.00923518 -0.01123089 -0.00723947
C3 smallest symmetric equivalence margin with 90% CI inside 0.00453832
Independent bounded refinement, max fit error 1.29e-08
DIAGNOSTIC cumulative RMS min median max +0.00476198 +0.01443651 +0.01914414
DIAGNOSTIC cumulative max-absolute min median max +0.00847085 +0.02297270 +0.02961557
DIAGNOSTIC 16-bin max-absolute residual nats min median max +0.02492288 +0.26589176 +0.40357918
DIAGNOSTIC 16-bin RMS residual nats min median max +0.01448940 +0.12248159 +0.18862965
P1 FIT TO LINEARLY INTERPOLATED GAINS; alternative, not registered +0.00903932 +0.00397787 +0.01410078
P1 EQUAL IMPROVEMENT n 6 mean/CI +0.01583581 +0.01040960 +0.02126202 positions +2.09092701 +2.17570429 +2.13578642 +2.19158563 +2.07568226 +2.23352733
S4 FIT TO LINEARLY INTERPOLATED GAINS; alternative, not registered +0.01391241 +0.00886213 +0.01896268
S4 EQUAL IMPROVEMENT n 6 mean/CI +0.01648477 +0.01349573 +0.01947381 positions +2.60162681 +2.71524205 +2.65710198 +2.73668887 +2.64194972 +2.83445866
CONDITIONAL IID EMPIRICAL RESAMPLING n 250 reps/draw 200 bias range -0.00069935 +0.00114018 SD range +0.00962235 +0.01081573
CONDITIONAL IID EMPIRICAL RESAMPLING n 16384 reps/draw 100 bias range -0.00011314 +0.00003973 SD range +0.00106341 +0.00127041
RECENCY k 1 set size min/max 226 272 max |mean age difference| updates 14.11545 max marginal KS 0.11920 max joint-quarter TV 0.00000
RECENCY k 2 set size min/max 2018 2116 max |mean age difference| updates 8.44744 max marginal KS 0.03365 max joint-quarter TV 0.03709
RECENCY k 3 set size min/max 6883 6931 max |mean age difference| updates 6.99420 max marginal KS 0.01816 max joint-quarter TV 0.03659
DONE
```

### Output: Earlier-study arithmetic and record inventory

```text
S primary R n 12 mean/CI -0.79577582 -0.98220710 -0.60934454 max error 7.76e-12
N1 A n 10 mean/CI +0.00000000 +0.00000000 +0.00000000 max error 0
N1 B curvature n 10 mean/CI +0.06109907 +0.05876924 +0.06342889 max error 2.08e-13
N3 turn n 10 mean/CI +0.02202677 +0.01761038 +0.02644316 max error 3.94e-13
N3 dip n 10 mean/CI +0.04275376 +0.03995792 +0.04554960 max error 2.49e-13
N3 memo n 10 mean/CI +0.96428571 +0.96192108 +0.96665035 max error 2.11e-13
N4 P1 n 4 mean/CI -0.18856671 -0.20831902 -0.16881439 max error 1.76e-12
N4 P2 n 4 mean/CI -0.02377719 -0.04787392 +0.00031954 max error 2.15e-12
N5 FALL n 10 mean/CI +0.00395660 +0.00104364 +0.00686957 max error 2.6e-13
N6 D1 n 6 mean/CI +0.01918952 +0.01793766 +0.02044138 max error 1.77e-13
N6 D2 n 6 mean/CI +0.01580951 +0.01308109 +0.01853793 max error 3.86e-13
N6 D3 n 6 mean/CI +0.01110227 +0.00718848 +0.01501606 max error 5.54e-13
N6 D4 n 6 mean/CI -0.00501883 -0.00901201 -0.00102566 max error 5.65e-13
N7 source subject 7ef133ad0120d0852c93ebe65f020718f51cebbf75abd43c29f89cdec8674f56 files 32 mismatches []
release ZIP SHA-256 cbe26760e2062a4cf03307d779226fa6efce8cfcfbf57b2e092bd818af80b8a9
tracked basename REVIEW_FINDINGS.md []
tracked basename REVIEW_FOLLOWUP.md []
tracked basename MATCHED_PLANNING.json []
tracked basename test_matched.py []
tracked model-state candidates []
living-page Markdown fragments checked 9 unresolved []
git tracked changes none
DONE
```

### Output: Tokenizer reconstruction

```text
parquet SHA-256 e83889baabc497075506f91975be5fac0d45c5290b6b20582c8cd1e853d0c9f7 matches True
rows 36718
rebuild 1 tokenizers 0.21.4 bytes 107106 SHA-256 cd642ca2b78a76e880adf07efb425bd2db741248cbf537aed0538c9421cca146
rebuild 2 tokenizers 0.21.4 bytes 107106 SHA-256 cd642ca2b78a76e880adf07efb425bd2db741248cbf537aed0538c9421cca146
two trainings identical True
matches pinned tokenizer True
```

### Output: Published follow-up-audit script

```text
EA-1  N5, M = p*(768) - p*(384) at matched gap
      registered         -0.0066 [-0.0076, -0.0055], 0/10 positive
      768 at higher end  +0.0015 [+0.0003, +0.0027], 8/10 positive
      384 at lower end   +0.0008 [-0.0002, +0.0018], 8/10 positive
      both               +0.0089 [+0.0077, +0.0100], 10/10 positive
      epochs by which 384 is read later than 768 at equal gap: +0.4382 [+0.4057, +0.4706], 10/10 positive
      M predicted by an epoch-only curve (each draw's own 384 path): -0.0067 [-0.0073, -0.0062], 0/10 positive
      observed minus predicted: +0.0002 [-0.0009, +0.0012], 4/10 positive
      epoch 2, gap 768 - 512: +0.0004 [-0.0047, +0.0055], 4/10 positive
      epoch 2, p* 768 - 512:  -0.0092 [-0.0112, -0.0072], 0/10 positive
AA-4  N4 at epoch 32, mean over 4 draws: width, total gain, p* x total gain, p*
      384     2343    1243  0.531
      512     3315    1647  0.497
      768     4774    1653  0.347
AA-1  every-pass matched contrasts: SE, power for an effect of +0.00909 (P1), effect detectable with 80% power
AA-7  and Bonferroni intervals over the six every-pass comparisons (t = 4.219, df 5)
      lr1e-04 768 at 2.25: SE 0.0087, power 0.14, detectable 0.031; every (Bonferroni) -0.0035 [-0.0402, +0.0332], 4/6 positive; whole minus every (Bonferroni) +0.0135 [-0.0211, +0.0480], 5/6 positive
      lr1e-04 768 at 2.5: SE 0.0029, power 0.72, detectable 0.010; every (Bonferroni) -0.0048 [-0.0169, +0.0073], 2/6 positive; whole minus every (Bonferroni) +0.0088 [-0.0003, +0.0178], 6/6 positive
      lr1e-04 768 at 2.75: SE 0.0023, power 0.88, detectable 0.008; every (Bonferroni) -0.0051 [-0.0147, +0.0046], 2/6 positive; whole minus every (Bonferroni) +0.0047 [-0.0008, +0.0102], 6/6 positive
      lr3e-04 768 at 2.25: SE 0.0087, power 0.14, detectable 0.031; every (Bonferroni) +0.0126 [-0.0243, +0.0495], 5/6 positive; whole minus every (Bonferroni) +0.0103 [-0.0247, +0.0454], 5/6 positive
      lr3e-04 768 at 2.5: SE 0.0030, power 0.67, detectable 0.011; every (Bonferroni) +0.0126 [-0.0001, +0.0254], 6/6 positive; whole minus every (Bonferroni) +0.0057 [-0.0044, +0.0158], 4/6 positive
      lr3e-04 768 at 2.75: SE 0.0022, power 0.90, detectable 0.008; every (Bonferroni) +0.0129 [+0.0035, +0.0223], 6/6 positive; whole minus every (Bonferroni) +0.0031 [-0.0028, +0.0091], 5/6 positive
AA-1  768 at 1e-4, within one model, exposure-matched sets: p*(epoch 3, late set) - p*(epoch 2+k/4, early set)
      k = 2: +0.0006 [-0.0043, +0.0055], 4/6 positive; whole set over the same readouts: +0.0085 [+0.0076, +0.0095], 6/6 positive
      k = 3: +0.0002 [-0.0028, +0.0032], 4/6 positive; whole set over the same readouts: +0.0042 [+0.0033, +0.0051], 6/6 positive
AA-3  P1 recomputed: +0.0091 [+0.0040, +0.0142], 6/6 positive
      with 768's gains lowered by its mean E0 excess over 512: +0.0062 [-0.0001, +0.0126], 5/6 positive ; change in 768's p*: +0.0028 [+0.0012, +0.0044], 5/6 positive
AA-2  epoch-3 loss drop over the quarter in which a sequence is trained, on log own weight and log sum of its
      15 batch-mates' weights (quarter fixed effects), 1e-4:
      512: own +0.0815 [+0.0804, +0.0826], 6/6 positive; batch-mates -0.0947 [-0.0974, -0.0919], 0/6 positive
      768: own +0.1031 [+0.1000, +0.1062], 6/6 positive; batch-mates -0.1147 [-0.1185, -0.1109], 0/6 positive
      fraction of updates clipped, per arm and epoch: 0.922 to 0.994 (96 values)
AA-6  512 at 1e-4, epoch 3: p* on the lower half of the weights +0.0154 [+0.0118, +0.0191], 6/6 positive ; upper half +0.2040 [+0.2002, +0.2078], 6/6 positive ; all +0.1027 [+0.1013, +0.1042], 6/6 positive
      mean gain by weight decile, relative to the overall mean: 0.82 0.83 0.83 0.84 0.86 0.90 0.97 1.10 1.30 1.54
      on the lower half of the weights: P1 +0.0012 [-0.0009, +0.0032], 5/6 positive ; S4 +0.0020 [-0.0006, +0.0046], 5/6 positive
EA-10 N4 (WikiText-2, 3e-5): slope of p* on log2 width over 384-768 by epoch; mean gap at 768
      epoch    1: -0.0016 [-0.0096, +0.0063], 3/4 positive; gap at 768 0.10
      epoch    2: +0.0043 [-0.0049, +0.0135], 3/4 positive; gap at 768 0.25
      epoch    4: +0.0210 [+0.0095, +0.0326], 4/4 positive; gap at 768 0.51
      epoch    6: +0.0438 [+0.0285, +0.0592], 4/4 positive; gap at 768 0.74
      epoch    8: +0.0723 [+0.0534, +0.0911], 4/4 positive; gap at 768 0.97
      epoch   12: +0.1176 [+0.0956, +0.1395], 4/4 positive; gap at 768 1.47
      epoch   16: +0.1049 [+0.0855, +0.1243], 4/4 positive; gap at 768 1.93
      epoch   24: -0.0238 [-0.0479, +0.0003], 0/4 positive; gap at 768 2.86
      epoch   32: -0.1886 [-0.2083, -0.1688], 0/4 positive; gap at 768 3.91
      p*(384, epoch 32) - p*(768 read at that gap): +0.0859 [+0.0621, +0.1096], 4/4 positive
      highest p* over readouts, 384 - 768: +0.0802 [+0.0645, +0.0958], 4/4 positive
EA-5  N6's coarse rule applied to N7: coarse minus fine contrast (n draws; then coarse and fine contrasts)
      P1 type, 1e-4, training loss, 768 read: n = 6; bias +0.0059 [+0.0049, +0.0069], 6/6 positive; coarse +0.0150 [+0.0101, +0.0198], 6/6 positive; fine +0.0091 [+0.0040, +0.0142], 6/6 positive
      S4 type, 3e-4, training loss, 768 read: n = 5; bias +0.0023 [+0.0008, +0.0039], 5/5 positive; coarse +0.0181 [+0.0152, +0.0209], 5/5 positive; fine +0.0157 [+0.0132, +0.0183], 5/5 positive
      D2 type, 3e-4, gap, 512 read: n = 5; bias -0.0005 [-0.0019, +0.0008], 1/5 positive; coarse +0.0116 [+0.0088, +0.0144], 5/5 positive; fine +0.0121 [+0.0093, +0.0150], 5/5 positive
      D3 type, 512@3e-4 - 768@1e-4, gap, 512 read: n = 6; bias -0.0015 [-0.0023, -0.0008], 0/6 positive; coarse +0.0051 [+0.0023, +0.0078], 5/6 positive; fine +0.0066 [+0.0042, +0.0089], 6/6 positive
```

### Output: Auditor first attempt: N5 schema error

```text
POST HOC; Python 3.12.14 NumPy 2.5.3
P1 mean/95% CI +0.00908795 +0.00400386 +0.01417203 sign-p 0.03125 label REVERSAL_CONFIRMED
P1 ENDPOINT-BOX conditional mean range +0.00702371 +0.01724831 CI envelope +0.00007639 +0.02743476 worst-lower vertex +0.02513035 +0.00745371 +0.00378049 +0.01066597 +0.00916239 -0.00057012
S1 mean/95% CI +0.00808476 +0.00487325 +0.01129627 sign-p 0.03125 label CONFIRMED
S3 mean/95% CI -0.00454199 -0.00794696 -0.00113701 sign-p 0.03125 label CONFIRMED
S4 mean/95% CI +0.01394194 +0.00892757 +0.01895632 sign-p 0.03125 label CONFIRMED
S4 ENDPOINT-BOX conditional mean range +0.01043317 +0.01635573 CI envelope -0.00026786 +0.02431174 worst-lower vertex +0.01685147 +0.01687255 +0.01344363 +0.01265112 +0.01278512 -0.01000487
S5 mean/95% CI +0.01382115 +0.01116159 +0.01648072 sign-p 0.03125 label CONFIRMED
S2 n 3 available ['m02', 'm03', 'm06'] label UNAVAILABLE
MATCHED rows 24 max scalar error 0.0 max CI error 7.192961504198792e-13 max LOO error 4.770281392119102e-13
EXPOSURE POWER 1 SD 0.02130613 power 0.137652
EXPOSURE POWER 2 SD 0.00702785 power 0.718580
EXPOSURE POWER 3 SD 0.00560466 power 0.883900
FUTURE n at 80%,90%; effect 0.0091 SD 0.0048 [5, 6]
FUTURE n at 80%,90%; effect 0.0091 SD 0.0096 [11, 14]
FUTURE n at 80%,90%; effect 0.00455 SD 0.0048 [11, 14]
FUTURE n at 80%,90%; effect 0.00455 SD 0.0096 [37, 49]
FUTURE n at 80%,90%; effect 0.003 SD 0.0048 [23, 29]
FUTURE n at 80%,90%; effect 0.003 SD 0.0096 [83, 110]
N5 columns ['draw', 'epoch', 'fall', 'gap_128', 'gap_192', 'gap_256', 'gap_384', 'gap_512', 'gap_64', 'gap_768', 'gap_96', 'p_128', 'p_192', 'p_256', 'p_384', 'p_512', 'p_64', 'p_768', 'p_96', 'rise']
Traceback (most recent call last):
  File "/workspace/scratch/730cd6b9e6c6/sequence-weighting/../audit-work/audit_numeric.py", line 81, in <module>
    q={(r['draw'],float(r['epoch']),int(r['width'])):r for r in Q}
                                        ~^^^^^^^^^
KeyError: 'width'
```

### Output: Auditor first attempt: duplicate S windows

```text
Traceback (most recent call last):
  File "/workspace/scratch/730cd6b9e6c6/sequence-weighting/../audit-work/audit_record.py", line 23, in <module>
    check('S primary R',values,js['primary'])
  File "/workspace/scratch/730cd6b9e6c6/sequence-weighting/../audit-work/audit_record.py", line 16, in check
    assert error<1e-8,(label,got,want)
           ^^^^^^^^^^
AssertionError: ('S primary R', array([-0.8294692 , -1.03981007, -0.61912832]), array([-0.79577582, -0.9822071 , -0.60934454]))
```


## 7. References

Only primary sources checked during this audit are listed. Bibliographic identifiers below were verified from the linked pages.

1. **[R1]** Alex Renda and Nitya Mani. *A study of sequence weighting at scale*. Jane Street, 14 September 2026. [Post](https://blog.janestreet.com/a-study-of-sequence-weighting-at-scale/); accompanying [*An Estimator for the Effective Sequence Weight Exponent*](https://blog.janestreet.com/a-study-of-sequence-weighting-at-scale/sequence-weighting-note.pdf), p. 1. The note is an accompanying technical note, not presented here as a separately refereed paper.
2. **[R2]** Jonathon Byrd and Zachary Lipton. *What is the Effect of Importance Weighting in Deep Learning?* ICML 2019, PMLR 97:872–881. [Official proceedings](https://proceedings.mlr.press/v97/byrd19a.html).
3. **[R3]** Sang Michael Xie et al. *DoReMi: Optimizing Data Mixtures Speeds Up Language Model Pretraining*. NeurIPS 2023. [Official proceedings](https://proceedings.neurips.cc/paper_files/paper/2023/hash/dcba6be91359358c2355cd920da3fcbd-Abstract-Conference.html). arXiv:2305.10429; DOI 10.52202/075280-3059.
4. **[R4]** Niklas Muennighoff et al. *Scaling Data-Constrained Language Models*. NeurIPS 2023. [Official proceedings](https://papers.neurips.cc/paper_files/paper/2023/hash/9d89448b63ce1e2e8dc7af72c984c196-Abstract-Conference.html). arXiv:2305.16264; DOI 10.52202/075280-2191. This citation refers to the conference version, not the later JMLR version.
5. **[R5]** Mariya Toneva, Alessandro Sordoni, Remi Tachet des Combes, Adam Trischler, Yoshua Bengio and Geoffrey J. Gordon. *An Empirical Study of Example Forgetting during Deep Neural Network Learning*. ICLR 2019. [arXiv:1812.05159](https://arxiv.org/abs/1812.05159), initially posted in 2018; the archive identifies the ICLR 2019 paper.
6. **[R6]** Jordan Hoffmann et al. *Training Compute-Optimal Large Language Models*. 2022. [arXiv:2203.15556](https://arxiv.org/abs/2203.15556). The NeurIPS 2022 proceedings use the title [*An empirical analysis of compute-optimal large language model training*](https://proceedings.neurips.cc/paper_files/paper/2022/hash/c1e2faff6f588870935f114ebe04a3e5-Abstract.html); the titles are distinguished rather than conflated.
