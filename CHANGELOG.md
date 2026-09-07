# Changelog

## 1.2.0-scientific-revision - 2026-09-07

- Strengthened one-sample optimality to all quantum POVMs and proved the refreshed-secret no-separation result.
- Solved the complete GLOBAL/SEP/PPT/LOCC total-answer-rate frontier for the ideal and specified calibrated phase-noise sources.
- Added exact decomposable PPT certificates and explicit attaining measurements; clarified the adverse dimension/rate scaling.
- Separated common local-noise invariance from unrestricted preparation leakage, with a source-error allowance and fixed-round concentration theorem.
- Made sequential filtrations and separable-instrument definitions explicit.
- Added direct raw-state checks, independent linear programs, and every-field validation for the new exact results.
- Preserved the dated August correction PDF/text, all earlier scientific result files, and six original scripts.
- Corrected the journal locator of the noisy-input reference to PRA 104, 012429 (2021).

## 1.1.1-author-correction - 2026-09-07

- Replaced overflow-prone binomial evaluation with scaled recurrence and log-tail APIs; positive underflow raises explicitly.
- Expanded result validation to all five result files and 458 fields, including schemas, archived Monte Carlo metadata, and Wilson arithmetic.
- Added tests corrupting every result field, checksum integrity tests, and exact rational statistical references.
- Added complete manifest verification and Python 3.10-3.13 CI coverage.
- Kept the August correction PDF, mathematics, results, historical scripts, and original release unchanged.
- Fast checks explicitly distinguish archived Monte Carlo records from fresh simulation.

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
