# Changelog

## 1.0.0-author-correction - 2026-08-17

### Scientific status

- Preserved the original 2022 code through the immutable release `paper-2022-original`.
- Withdrew the interpretation of `p_B` as a general soundness bound.
- Added the exact `23/32` versus `25/32` counterexample using the same all-H measurements.
- Added an exact formula for the honest ParitySolve probability.
- Corrected the interpretation of the three Figure 5 parameter choices.
- Replaced the legacy fluctuation expression by the Bernoulli standard error.
- Added an aggregate-only reanalysis of the IBM counts and documented the missing raw-shot limitation.
- Reclassified the original construction as a DCP-derived circuit workload rather than a sound capability-verification protocol.

### Software and reproducibility

- Added a modern, Qibo-independent Python package under `src/dcp_challenge/`.
- Added exact and numerical regression tests.
- Added machine-readable JSON and CSV outputs.
- Added a standalone Markdown, TeX, and PDF author correction.
- Left all six original root scripts byte-for-byte unchanged.
- Standardized Markdown mathematics to GitHub-supported delimiters and added explicit hidden-file upload checks for the CI workflow and `.gitignore`.

### Separate follow-up

- Added the phase-twirled heralded DCP witness as a separate, explicitly non-peer-reviewed ideal-model result.
- Added a complete four-qubit NumPy statevector implementation.

## paper-2022-original

Historical repository snapshot corresponding to the code supplied with the 2022 article.
