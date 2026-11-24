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
