# Area 1b — public record against local: findings

Written 8 Nov 2026 by the orchestrating assistant from this folder's saved outputs (`s01`–`s10*.out`, `r2_compare.out`, `r2_builder_before.out`, `r2_pr_bodies.out`, `r2_diffs/`). No new computation; the auditor stopped before writing findings.

## Held

- PR #5 at `f3a25710`: 55/55 blobs equal the local package and 53/53 the local sources (`r2_compare.out` l.58; `s05`). The folder's tree SHA `a452a968…` is unchanged at main `4e3baaea` (l.160–163).
- PR #6: 24 of 25 files byte-identical to local; `RESULT.md` is the one derivative, mapped correctly in `PUBLICATION_TRANSFORMATIONS.json` (local `ac482f31…`, public `8e64cc2c…`) (l.218, 229). Every PR #6 manifest row has the right bytes and SHA-256 (`s07` l.92–119).
- Builder pin: reversing the one-line diff reproduces `builder_before` `f6736319…`; `builder_after` `af48e60e…` equals both `APPROVAL_RECORD.json` (`r2_builder_before.out`, `s10`).
- 46 hash links across activations, run verifications and exit receipts hold, including the hash-only check of the M2 activation's copy of M1's terminal (`s09`).
- No personal path in any PR #6 file; the withheld `ANALYSIS_EXIT_RECEIPT.json` is absent and named by hash in `RESULT.md`; all 20 relative README links resolve (l.305, 326–335).

## Findings

- **IP-1 (minor, fix).** Published PR bodies differ from the local `PR_BODY.md`: PR #6's "Also changed" was extended (correctly); both bodies carry a Claude Code session link (`claude.ai/code/session_01Jvf…`) instead of the attribution line (`s08`). A session identifier is public.
- **IP-2 (minor, reword).** Public `RESULT_VERIFICATION.json` names the local `RESULT.md` hash. The mapping is public in three root files (l.319–321); the consequence — the verifier's byte check fails on the public copy — is stated nowhere.
- **IP-3 (minor, concede or publish).** Decision records `…-20261105-01/-02` cited by public files are not public; `…-20261104-02` is public only inside the prereg folder. Disclosed in `PUBLICATION_NOTES.md` l.13.
- **IP-4 (note).** `HASHES.json`'s `corpus_manifest_sha256` and `common_rate_selection_sha256` resolve to no inventoried file (`s05b`); could not check.
- **IP-5 (note).** The manifest has no row for itself, as before (`s07` l.94).
- **IP-6 (note).** `sealed-source/GPU_CHECK.json` holds one `C:\` drive path, not a personal one (l.333).

No blocker or major.
