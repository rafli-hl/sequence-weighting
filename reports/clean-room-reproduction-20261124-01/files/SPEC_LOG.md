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
