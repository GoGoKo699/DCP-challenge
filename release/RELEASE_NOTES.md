# DCP Challenge 1.2.1: reviewed correction and current technical note

This release freezes the author-maintained correction and follow-up analysis, including the September scientific conclusions. It is not an APS Erratum, does not alter the 2022 journal article, and has not received independent peer review.

## Read first

`DCP-current-technical-note.pdf` is the current self-contained exposition. The source archive includes its Markdown and build script. The dated August correction is included separately and remains unchanged.

## Scientific content

The original shared-secret p_B verification implication remains withdrawn. Retained results include the exact 23/32 versus 25/32 counterexample, exact honest probabilities, and corrected statistical uncertainty. The September extension establishes unrestricted one-cell optimality, the independently refreshed-secret limitation, exact total-answer-rate confidence frontiers, the single-round PPT certificate, and source-error-aware statistics under explicit conditional trust assumptions.

Version 1.2.1 consolidates these results and adds a focused release audit. It does not change the v1.2.0 theorems, thresholds, or stored scientific results.

## Validation

The release workflow verifies the complete source manifest, six historical files, all committed scientific records, the regression suite, the 96-case raw-state optimization audit, and the additional full-space and adaptive-stopping audit. Exact validation outputs and software versions accompany the release.

## Provenance

The 2022 source remains at the separate immutable `paper-2022-original` release. The August reanalysis's GPT-5.6 Pro credit is preserved; the September work and this release review are also AI-assisted. Ruge Lin retains responsibility. No universal-computation, computational-speedup, exhaustive-novelty, or completed-hardware-calibration claim is made.

## Assets

- `DCP-challenge-1.2.1.zip`: complete tracked repository tree, including hidden configuration files.
- `DCP-current-technical-note.pdf` and `.tex`: current note and standalone typesetting source.
- `author_correction_August_2026.pdf`: unchanged earlier correction.
- `RELEASE_REVIEW.md`: claim-by-claim audit disposition.
- `VALIDATION.txt` and `ENVIRONMENT.txt`: actual release-build checks and environment.
- `RELEASE_COMMIT.txt`: the exact archived commit.
- `SHA256SUMS`: hashes of all attached files other than this manifest itself.

The numerical probability routines are floating-point evaluations, not rigorous interval enclosures. Fast validation checks archived large Monte Carlo records and their uncertainty metadata rather than rerunning the original large simulations. No software license is added by this release.
