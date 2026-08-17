# Offline Package Audit

**Audit date:** 17 August 2026  
**Target branch:** `author-correction-2026`  
**GitHub write actions performed during construction:** none

## Scientific checks

- Exact `23/32` versus `25/32` counterexample reproduced with rational arithmetic.
- Exact no-complementary-collision formula checked against exhaustive enumeration for `n <= 3`, `m <= 4`.
- Corrected exact Figure 5 honest probabilities reproduced.
- Figure 5(a) complete all-H likelihood result reproduced exactly.
- Frozen Figure 5(b,c) Monte Carlo estimates independently cross-checked with different seeds.
- Bernoulli standard error regression checked.
- IBM aggregate reconstruction and finite-count bootstrap reproduced.
- Heralded-witness collision states, full two-cell ensembles, trace norms, separable ratio, finite-sample values, and minimal circuit checked.

## Software checks

- Test suite: **20 passed**.
- All Python files compiled successfully.
- Corrected package installed in editable mode with build isolation disabled in the offline audit environment.
- All four generated result files reproduced byte-for-byte from `scripts/generate_results.py`.
- Internal Markdown links resolved successfully.
- All Markdown mathematics uses GitHub-supported dollar-sign delimiters; legacy parenthesis and standalone bracket delimiters are absent.
- `pyproject.toml`, `CITATION.cff`, and the GitHub Actions YAML parsed successfully.

## Historical integrity

The six original root scripts match their historical Git blob SHA-1 values exactly. The verification is executable through:

```bash
python scripts/verify_historical_files.py
```

## PDF checks

- `correction/author_correction.pdf` opens successfully and contains eight A4 pages.
- All pages were rendered and visually inspected.
- No clipping, overlap, missing glyph, or broken table was found.
- Rebuilding `correction/author_correction.tex` in a clean directory produced zero changed rendered pages compared with the committed PDF.

## Scope checks

- The original `p_B` verification interpretation is explicitly withdrawn.
- The ParitySolve branch is retained without overstating soundness.
- The heralded witness is separated from the 2022 article and labelled non-peer-reviewed.
- No universal-computation, speedup, device-independent, or general proof-of-quantumness claim is made for the follow-up witness.
- The correction is explicitly described as author-maintained and not an APS Erratum.

## Upload readiness

The package contains fewer than 100 files after removal of caches and build intermediates. It is suitable for website upload to the existing correction branch. The outer directory should be unzipped, and its contents - not the outer directory itself - should be uploaded.
