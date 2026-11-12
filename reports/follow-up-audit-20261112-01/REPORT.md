# Follow-up audit, 12 November 2026

**Status: read-only audit; post hoc and descriptive.** It reports no new run, changes no sealed label, and adjusts no
interval for multiplicity unless it says so.

## Why it was done

The audit of 8 November ([`AUDIT.md`](../full-audit-20261108-01/AUDIT.md)) was planned as nine fresh auditors, then
merging, verification of each finding, a search for gaps and a synthesis. It stopped at a usage limit: four areas were
finished by fresh auditors, five were written up by the orchestrating session from saved outputs, and the later stages
never ran. Of the five, three have since been covered by later work (the corrections of 9 and 11 November and the
post-hoc analysis of 11 November). Two had not been audited by a fresh auditor since: **the studies before N7**
(area 7, "earlier") and **alternative explanations** (area 5). Two of the 8 November major findings, M4 (the training
loss is defined in no prose document) and M5 (planned against realised power), had also not reached the living pages.

## Who did it

- **Auditors:** two separate sessions of Claude Fable 5.2 (`claude-fable-5-2`, Anthropic), each with no part in the
  earlier work, given the public record at commit `3b4610d` and, for the alternatives, the N7 loss-array bundle of the
  v1.0 release. Each wrote its own findings before opening the 8 November audit, then compared. Neither opened any
  run directory. Their reports are filed as returned:
  [`AUDIT_EARLIER_STUDIES.md`](AUDIT_EARLIER_STUDIES.md) and [`AUDIT_ALTERNATIVES.md`](AUDIT_ALTERNATIVES.md).
- **Supervising session:** Claude Opus 5.5 (`claude-opus-5-5`, Anthropic), which briefed the auditors, re-checked
  their main findings with separately written code ([`verify_findings.py`](verify_findings.py), output
  [`OUTPUT.txt`](OUTPUT.txt)), and drafted the resulting changes. The auditors' own scripts are not published.
- No human has checked the analysis.

## Results

Neither auditor found a blocking problem. Every number behind C1–C5 that they recomputed reproduces from the published
tables or the released losses, and every registered outcome was read as registered. The findings are about wording,
scope and missing disclosures.

| Finding | Severity (auditor) | Re-checked | Disposition |
|---|---|---|---|
| EA-1. C3's M uses whole-epoch interpolation; its sign flips at the bracket ends; an epoch-only curve predicts it | Major | Yes | C3 reworded, with support that needs no interpolation |
| EA-2. C1 worded more strongly than its source | Major | Yes (N4 peak locations) | C1 reworded |
| EA-3. Registered outcomes that did not confirm are on no living page | Major | Labels and figures read from the result reports | Listed in `CURRENT_CLAIMS.md` |
| EA-4. "19 of 59 defined fits" counts points, not fits | Minor | Taken from the auditor | Reworded |
| EA-5. "Biased upward" is wrong where 512 is the interpolated arm | Minor | Yes | [Correction](../natural-text-correction-20261112-01/CORRECTION.md) §1; living pages reworded |
| EA-6. S4's overstatement compares different draws | Minor | Yes (+0.0023 like for like) | Correction §2 |
| EA-7. "There is no N2" | Minor | Yes (evidence chains) | `NATURAL_TEXT_STUDIES.md` reworded |
| EA-8. N1's failure cause stated as fact | Minor | Yes (failure report) | `NATURAL_TEXT_STUDIES.md` reworded |
| EA-9. Units missing in C1 and C2 | Minor | — | Added |
| EA-10. C2's alignment | Note | Yes | Added to C2 |
| EA-11. N5's fixture rate is not reproducible from public files | Note | — | No change; EA-1's measured-curve check is the reproducible counterpart |
| EA-12. N6 and N7 agree at equal updates (Welch tests) | Note | Not re-checked | No change |
| AA-1. The exposure-matched null at 1e-4 has power 0.14 nearest equal loss; within one model, exposure-matched p\* barely changes from epoch 2.5 to 3 | Major | Yes | Added to C4 |
| AA-2. Clipping makes the effective weight batch-relative | Major (or minor) | Yes (coefficients and clip fractions) | Added to the scope of every claim, and as an open question |
| AA-3. p\* is close to a slope-over-gain ratio; 768's higher E0 accounts for about a third of P1 | Minor | E0 offset only | E0 offset added to C4 |
| AA-4. C2: memorisation saturation not excluded | Minor | Yes | Added to C2 |
| AA-5. The epoch-boundary step is model-wide | Minor | **No** | Added to C4, marked as not re-checked |
| AA-6. Gains are not a power of the weight; p\* depends on the weight range | Minor | Yes | Added under the estimator |
| AA-7. Bonferroni over the six exposure-matched comparisons | Minor | Yes | Added to C4 |
| AA-8. Per-draw variation tracks read epoch and gradient norm | Note | Not re-checked | No change |
| AA-9. Removing generic gain triples p\* | Note | Not re-checked | No change |
| AA-10. The record changed during the audit | Note | — | The supervising session began editing `NATURAL_TEXT_STUDIES.md` on the audit branch after the first auditor reported; the second auditor read the page as at `3b4610d` plus that diff |
| M4 (8 November). Training loss undefined | Major | Yes (sealed source) | Defined in `CURRENT_CLAIMS.md` |
| M5 (8 November). Planned against realised power | Major | Yes | Added to C4 |

### Comparison with the 8 November audit

Both auditors confirmed the 8 November findings in their areas that they recomputed. They differ from it in two
places:
- **AL-3** (other anchorings answer the exposure concern): the numbers reproduce, but the inference does not hold,
  because in every anchoring 512 has had more third-pass exposure than 768. This was already withdrawn on 11 November.
- **AL-5** (a uniform 0.037-nat offset works against the reversal): the size reproduces, but the direction is the
  other way. At equal loss the offset lowers 768's p\*, so it adds to P1.

## What is not covered

- Anything that needs run directories: p\* for S and N1–N6 from per-sequence losses, E0 values, clipping and bound-32
  refits. Only N7's per-sequence losses are published, so AA-2, AA-3 and AA-6 are shown on N7 only.
- Whether earlier protocols were sealed before their data existed, beyond internal dates and the pull-request
  snapshots.
- The mechanism of the epoch-boundary step and of recency.
- The audit and the corrections were made by AI models of one family, as was the rest of the analysis.
