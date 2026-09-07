# Validation Record

## Software hardening - 7 September 2026

- Baseline tree: `93caf96908663f256de153feee54afccb358d342`, matching published `main` at `449548426b83fc22a9939fb2c2f6dede74dcd6f4`.
- Local suite: **59 tests passed**, including 458 individual result-field mutations.
- Previously overflowing binomial cases now agree with independent exact rational sums.
- Positive probability underflow is explicit; finite log tails remain available.
- All five committed result records and complete SHA-256 manifest coverage validate.
- Historical scripts and the August scientific documents/PDF are unchanged.
- The fast validator reuses archived large Monte Carlo counts and recomputes their arithmetic; it does not claim a fresh large simulation.
- The automated workflow repeats tests and integrity checks on Python 3.10, 3.11, 3.12, and 3.13. Its live execution status is recorded in GitHub Actions, not inferred from this document.

## August scientific validation

**Validation date:** 17 August 2026  
**Target:** author-correction repository state

## Scientific checks

- Exact $23/32$ versus $25/32$ counterexample reproduced with rational arithmetic.
- One-sample parity-distribution identity proved analytically and checked exactly for $n=1,\ldots,7$.
- Exact no-complementary-collision formula checked against exhaustive enumeration for $n\le3$, $m\le4$.
- Corrected exact Figure 5 honest probabilities reproduced.
- Figure 5(a) complete all-H likelihood result reproduced exactly.
- Frozen Figure 5(b,c) Monte Carlo estimates cross-checked with independent seeds.
- Bernoulli standard-error correction checked.
- Heralded-witness collision states, full two-cell ensembles, trace norms, tight separable ratio, adaptive sequential tail values, and minimal circuit checked.
- Historical chronology and maximum-confidence related work rechecked against primary sources through 17 August 2026.

## Software checks

- Test suite: **19 passed**.
- All Python files compile successfully.
- The corrected package installs in editable mode.
- Exact and integer-derived committed results validate exactly.
- Floating-point linear-algebra diagnostics validate within the tolerances encoded by the tests.
- Fixed Monte Carlo records include seeds, trial counts, estimates, and Wilson intervals.
- Internal Markdown links resolve.
- Markdown mathematics uses GitHub-supported dollar-sign delimiters.
- `pyproject.toml`, `CITATION.cff`, and the GitHub Actions YAML parse successfully.

## Historical integrity

The six original root scripts match their historical Git blob SHA-1 values exactly. Verification is executable through:

```bash
python scripts/verify_historical_files.py
```

## PDF checks

- `correction/author_correction.pdf` opens successfully and contains nine A4 pages.
- All pages were rendered and visually inspected.
- No clipping, overlap, missing glyph, broken table, or orphaned near-empty final page was found.
- `correction/author_correction.tex` is the standalone source used to build the committed PDF. A clean three-pass XeLaTeX rebuild produced zero changed rendered pages.

## Scope checks

- The original $p_B$ verification interpretation is explicitly withdrawn.
- The one-sample decoder is strengthened only within the complete one-sample all-H record.
- The ParitySolve branch is retained without overstating soundness.
- The proof-of-concept IBM experiment is left solely in the historical record and is not used in the correction.
- The heralded witness is separated from the 2022 article and labelled non-peer-reviewed.
- The sequential theorem states an instrument-level null class, predeclared stopping rule, and no-certificate outcome.
- Lee-Bae 2026 and earlier maximum-confidence prior work are credited explicitly.
- The 2022 chronology is recorded without alleging dependence or fault by later authors.
- Substantial GPT-5.6 Pro assistance is disclosed, and responsibility is retained by Ruge Lin.
- No universal-computation, speedup, device-independent, or general proof-of-quantumness claim is made for the follow-up witness.
