# Dense-readout replication (N8): disclosure figures on the real draws

**Step:** the owner-run seed draw (the brief, step 5). Outcome-blind: from the corpus manifest and the seeds only. **Measured** on n01–n24 at N = 16,384. Carried by hand into the results report.

| Draw | Articles | Sequences used | Tied weights, before / after division by numpy's mean (limit 16) |
|---|---|---|---|
| n01 | 395 | 16,384 | 3 / 4 |
| n02 | 415 | 16,384 | 2 / 3 |
| n03 | 388 | 16,384 | 2 / 2 |
| n04 | 363 | 16,384 | 4 / 6 |
| n05 | 413 | 16,384 | 2 / 2 |
| n06 | 396 | 16,384 | 5 / 5 |
| n07 | 391 | 16,384 | 0 / 1 |
| n08 | 378 | 16,384 | 2 / 2 |
| n09 | 382 | 16,384 | 2 / 3 |
| n10 | 400 | 16,384 | 2 / 2 |
| n11 | 398 | 16,384 | 2 / 2 |
| n12 | 416 | 16,384 | 2 / 2 |
| n13 | 418 | 16,384 | 1 / 1 |
| n14 | 388 | 16,384 | 2 / 2 |
| n15 | 390 | 16,384 | 0 / 0 |
| n16 | 398 | 16,384 | 3 / 3 |
| n17 | 408 | 16,384 | 1 / 2 |
| n18 | 411 | 16,384 | 3 / 3 |
| n19 | 361 | 16,384 | 4 / 4 |
| n20 | 401 | 16,384 | 1 / 1 |
| n21 | 410 | 16,384 | 2 / 3 |
| n22 | 407 | 16,384 | 2 / 2 |
| n23 | 379 | 16,384 | 0 / 0 |
| n24 | 394 | 16,384 | 2 / 2 |

## Identical full text

- **Sets across the fresh draws:** 0.
- **Fresh texts equal to an assigned article's:** 0.
- **Repeated inside a draw:** 0.

The rule removes these, so zero is what it should give.

## Titles, which the rule does not remove

- **Fresh articles sharing a title with an article of N5, N6 or N7, with a different text:** 0.
- **Titles shared across the fresh draws:** 1.

## Not measured

**Exact token sequences and 64-token runs.** They would read the corpus's split files, and this step may open only the manifest. So how far token runs recur across n01–n24, N5, N6, N7, the validation set and the pool is not known here. For scale, N6's groups had 64-token runs recurring in another fresh group at a mean of 0.15%. That is N6's figure and not a measurement of these draws.

**Shared by design:** every draw shares the validation set, the pool and the tokenizer with each other and with the earlier natural-text studies.

**Tied weights:** from the stdlib draw and the IEEE cast, without Torch. The weights used are after division, by Torch's mean, so the counts from real Torch can differ by one or so.

**Limit.** Draws are treated as independent in every interval. These figures do not measure how far that is true.
