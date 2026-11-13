# README and methods revision, 13 November 2026

A documentation revision of the living pages (`README.md`, the new `METHODS.md`, `CURRENT_CLAIMS.md`,
`NATURAL_TEXT_STUDIES.md`, `DATA_AVAILABILITY.md`, `PUBLICATION_NOTES.md` and the `verify` workflow). The changes are
listed in [`PUBLICATION_NOTES.md`](../../PUBLICATION_NOTES.md). No study, registered rule, label, sealed file,
historical record or published number changed.

This folder holds what the revision added beyond rewording:

| File | What it is |
|---|---|
| [`describe_fits.py`](describe_fits.py) | A descriptive summary of N7's 240 published fits (`FITS.csv`): bounds, undefined fits, objective at the fit relative to its value at p = 0, negative-gain fractions, total gains. Standard library only |
| [`matched_set_weights.py`](matched_set_weights.py) | Sizes and weight medians of the exposure-matched sets of the 11 November post-hoc analysis. Needs NumPy, PyTorch 2.7.0 and the v1.2 loss-array bundle |
| [`OUTPUT.txt`](OUTPUT.txt) | The exact output of both scripts |
| [`CHECKS.md`](CHECKS.md) | The checks run on the revised copy, and their results |

Both scripts are post hoc and descriptive. They were written after every result was known, test no hypothesis and
move no label. Like the record's other post-hoc analyses, they were produced with AI assistance and have not been
checked by an independent reviewer.
