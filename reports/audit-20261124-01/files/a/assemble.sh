#!/usr/bin/env bash
# Assembles FINDINGS.md from the narrative (part1.tmp) and the saved outputs. Auditor A; writes only in this folder.
set -u
cd "$(dirname "$0")"
emit() {
  printf '### `%s`\n\n%s\n\nSHA-256 `%s`. Command: `%s`\n\n~~~\n' "$1" "$2" "$(sha256sum "$1" | cut -c1-64)" "$3"
  tr -d '\r' < "$4"
  printf '~~~\n\n'
}
{
  cat part1.tmp
  emit a1_envelope.py "F1: the 64-combination envelope from N7's POINTS.csv and MATCHED.csv. Standard library, own t quantile." "PY a1_envelope.py REPO" a1_envelope.out
  emit a2_gap.py "F2: independent recomputation of the gap scale from N5's POINTS.csv, with one further descriptive scale." "PY a2_gap.py REPO" a2_gap.out
  emit a3_recency.py "F3: the emulated batch orders, their validation, and the recency maxima." "PY a3_recency.py REPO BUNDLE" a3_recency.out
  emit a3b_order_hashes.py "The emulated order files against the 12 hashes pinned in N8's HASHES.json." "PY a3b_order_hashes.py REPO BUNDLE" a3b_order_hashes.out
  emit a3c_orders_json.py "Which version strings rebuild the pinned ORDERS.json (12 pairs tried)." "PY a3c_orders_json.py REPO BUNDLE" a3c_orders_json.out
  emit a6_make_orders.py "Writes the two order folders." "PY a6_make_orders.py BUNDLE orders_as_pinned 2.7.0+cu126 2.2.6 ; PY a6_make_orders.py BUNDLE orders_public_install 2.7.0+cpu 2.5.3" a6_make_orders.out
  emit a3d_ks.py "The audit's KS balance figures, from the emulated orders." "PY a3d_ks.py orders_as_pinned" a3d_ks.out
  emit a4_numbers.py "Numbers quoted on the living pages, from MATCHED.csv and the 11 November RESULTS.json." "PY a4_numbers.py REPO" a4_numbers.out
  emit a5_links.py "Local links and fragment anchors of 11 pages." "PY a5_links.py REPO" a5_links.out
  printf '## 5. Commands that matter, with exact output\n\nRun in `REPO` unless stated.\n\n'
  printf '### C1. History of the correction (A1)\n\n~~~\n'; cat c_a1.out; printf '~~~\n\n'
  printf '### C2. Living pages, versions, dates, files changed, archives, tags, protocol (E1 to E7, F-a2, F-a3)\n\n~~~\n'; cat c_e.out; printf '~~~\n\n'
  printf '### C3. The record'"'"'s `test_on_n7.py`, run twice on N7'"'"'s public data (F-a1)\n\n'
  printf 'Command: `PY REPO/preregistration/natural-text-dense-replication-20261114/analysis/test_on_n7.py REPO BUNDLE <orders folder>`. Full outputs are in `test_on_n7_as_pinned.out` and `test_on_n7_public_install.out` (78 lines each). Apart from timing lines they differ only here (`<` pinned strings, `>` public-install strings):\n\n~~~\n'
  diff <(grep -v "elapsed\|analyse()" test_on_n7_as_pinned.out) <(grep -v "elapsed\|analyse()" test_on_n7_public_install.out)
  printf '~~~\n\nThe F1 and F3 lines, identical in both runs:\n\n~~~\n'
  grep "envelope over 64\|S-b, 768 at" test_on_n7_as_pinned.out | sort -u
  printf '~~~\n\n### C4. `gap_scale.py` (F2), the README example, and the state of the clone\n\n~~~\n'
  echo '$ PY reports/natural-text-correction-20261123-01/gap_scale.py > SCRATCH/gap_scale_rerun.out   (exit 0)'
  echo '$ tr -d "\r" < SCRATCH/gap_scale_rerun.out | sha256sum ; sha256sum reports/natural-text-correction-20261123-01/GAP_SCALE.txt'
  tr -d '\r' < gap_scale_rerun.out | sha256sum
  (cd ../repo && sha256sum reports/natural-text-correction-20261123-01/GAP_SCALE.txt)
  echo '$ PY SCRATCH/readme_block.py   (README.md lines 205 to 226, unedited)'
  echo 'P1 = +0.00909 [+0.00400, +0.01417], n = 6'
  echo '$ git status --porcelain | wc -l ; git rev-parse HEAD   (after all work)'
  (cd ../repo && git status --porcelain | wc -l && git rev-parse HEAD)
  printf '~~~\n'
} > FINDINGS.md
wc -c FINDINGS.md
