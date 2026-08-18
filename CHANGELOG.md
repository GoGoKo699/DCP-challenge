# Changelog

## 1.1.0-author-correction - 2026-08-17

### Referee-level revision

- Removed the new IBM reanalysis and left the proof-of-concept experiment solely in the untouched historical code.
- Added an exact theorem proving that the published special-outcome decoder is Bayes-optimal for one all-Hadamard sample.
- Added exact tests of the one-sample parity-distribution identity.
- Formalized adaptive sequential soundness against separable instruments, including LOCC, with a predeclared stopping rule and no-certificate outcome.
- Added the 2006-2026 maximum-confidence chronology and a direct comparison with Lee and Bae (2026).
- Clarified that the 2022 DCP article was an earlier conceptual antecedent but did not contain the later sound GLOBAL-versus-SEP theorem.
- Added explicit credit for substantial assistance from OpenAI’s GPT-5.6 Pro and retained human responsibility with Ruge Lin.
- Replaced portable byte-for-byte claims for floating-point diagnostics with exact-versus-tolerance-based validation.
- Expanded continuous integration to verify historical file hashes and committed scientific results.

## 1.0.0-author-correction - 2026-08-17

### Scientific status

- Preserved the original 2022 code through the immutable release `paper-2022-original`.
- Withdrew the interpretation of `p_B` as a general soundness bound.
- Added the exact `23/32` versus `25/32` counterexample using the same all-H measurements.
- Added an exact formula for the honest ParitySolve probability.
- Corrected the interpretation of the three Figure 5 parameter choices.
- Replaced the legacy fluctuation expression by the Bernoulli standard error.
- Reclassified the original construction as a DCP-derived circuit workload rather than a sound capability-verification protocol.

### Software and reproducibility

- Added a modern, Qibo-independent Python package under `src/dcp_challenge/`.
- Added exact and numerical regression tests.
- Added machine-readable JSON and CSV outputs.
- Added a standalone Markdown, TeX, and PDF author correction.
- Left all six original root scripts byte-for-byte unchanged.

### Separate follow-up

- Added the phase-twirled heralded DCP witness as a separate, explicitly non-peer-reviewed ideal-model result.
- Added a complete four-qubit NumPy statevector implementation.

## paper-2022-original

Historical repository snapshot corresponding to the code supplied with the 2022 article.
