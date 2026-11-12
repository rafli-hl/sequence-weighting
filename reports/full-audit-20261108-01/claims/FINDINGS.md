# Area 4 — claims against evidence, and the paper draft: findings

Written 8 Nov 2026 by the orchestrating assistant from `RECOMPUTE_CLAIMS_OUTPUT.txt`, `PUBLIC_BLOB_CHECK_OUTPUT.txt` and the paper files (`main.tex`, `make_figures.py`, `references.bib`, written after the auditors ran). N6-interpolation figures: `../earlier/RECOMPUTE_EARLIER.log`, re-derived in `../verify_orchestrator.py` (V2).

## Traces

Every N7 number in RESPONSE §5, the note, RESEARCH_GOAL's 6 Nov sections, public `NATURAL_TEXT_STUDIES.md`, the PR #6 body and the paper reproduces from `POINTS.csv` to ≤7e-13, including the LOO sides and the bound +0.00702 [+0.00216, +0.01189]. The 72/100 categories sum to 72. `make_figures.py` asserts its contrasts against `ANALYSIS.json`; its N6 constants equal RESPONSE §4.

## Findings

- **C-1 (major, reword).** "+0.0132, post hoc" and "the 384→512 rise is mostly training progress (+0.0027)" (RESPONSE §5 claim 4; RESEARCH_GOAL; `make_figures.py` N6 dict; paper Fig. 3 "the same contrasts on N6's draws"). N6's values interpolate linearly over E2–E3; N7 shows p\* jumps in the first quarter after a boundary, so on N7's draws the coarse rule inflates P1 +0.0059, S1 +0.0032, S4 +0.0041 (V2); transferred to N6, D4 ≈ +0.0064 and D1 ≈ +0.011 (earlier E-1). Say "coarse, upper-biased"; drop "mostly training progress"; tell the reader N7's smaller effects are partly resolution.
- **C-2 (minor, reword).** "Each of N6's means lies inside N7's interval" is true; N7's means lie outside N6's for P1 and S4. Say both.
- **C-3 (major, reword).** Paper abstract "six independent draws": draws share the validation set (512 sequences), pool and tokenizer; independence is assumed (PROTOCOL §11).
- **C-4 (minor, reword).** "preregistered before any of its data were generated" is true of PR #5 but silent that the hypothesis is N6's post-hoc finding.
- **C-5 (minor, verify).** "p\* rises throughout training in every arm": true for N7's 24 arm-draws; N5 and N6's 384 arm not checked here.
- **C-6 (minor, reword).** §4.3 title "The comparison axis reverses the ordering": at 1e-4 only.
- **C-7 (minor, reword).** "least favourable reading" (public index, paper §4.4) needs its condition: only if p\* stays between the bracketing readouts.
- **C-8 (major, state).** S4 "CONFIRMED" depends on the interpolation: later-end reading +0.0104 [−0.0003, +0.0211] (V1).
- **C-9 (minor, trace).** Untraced paper numbers: "0.7–35 M parameters", "0.2–2.1 M unique tokens", "R² = 0.90".
`make_figures.py` follows the protocol's rule and path. Table 1 has TODO cells; "N7 Epochs 3.5" should read "readouts to 3.5, contrasts at 3". No causal language beyond the sealed readings.
