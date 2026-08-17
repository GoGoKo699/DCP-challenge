# Reproducibility Guide

## 1. Modern corrected analysis

Recommended environment:

- Python 3.10 or later;
- NumPy 1.24 or later;
- pytest 8 or later for tests.

Install from the repository root:

```bash
python -m pip install -e .[test]
```

Run all tests:

```bash
pytest -q
```

The release package was audited with 20 passing tests.

## 2. Decisive exact counterexample

```bash
python examples/reproduce_counterexample.py
```

Expected values:

```text
23/32 = 0.718750
25/32 = 0.781250
```

Both values are computed as exact rational numbers.

## 3. Exact honest probability and Figure 5

```bash
python examples/reproduce_figure5.py
```

The no-complementary-collision probability is

\[
k_{\rm nc}(N,m)
=
N^{-m}
\sum_j
\binom{N/2}{j}2^j j!\,{m\brace j}.
\]

The ideal success probability is

\[
p_{\rm exact}
=
1-\frac12\left(\frac{1+k_{\rm nc}}2\right)^t.
\]

The Figure 5(a) complete all-H likelihood result is exact. Figure 5(b) and Figure 5(c) use the frozen fixed-seed Monte Carlo outputs listed below.

| Figure | Trials | Seed | Estimate | Wilson 95% interval |
|---|---:|---:|---:|---:|
| 5(b) | 1,000,000 | 20260817 | 0.937289 | [0.936812, 0.937763] |
| 5(c) | 60,000 | 20260818 | 0.957183 | [0.955534, 0.958774] |

The default `scripts/generate_results.py` reuses these frozen values rather than rerunning a long Monte Carlo job. Its source identifies them explicitly. To independently rerun the large simulations, call `build_figure5_rows(run_large_monte_carlo=True)` from that script or use `h_likelihood_monte_carlo` directly.

## 4. IBM aggregate reconstruction

```bash
python examples/reproduce_ibm_reanalysis.py
```

The finite-count bootstrap committed in `results/ibm_aggregate_reanalysis.json` uses:

```text
trials = 100000
seed   = 20260817
```

It is a multinomial bootstrap of the three aggregate categories retained in `IBM.py`. It cannot recover shot order, timestamps, drift, or correlations absent from the archive.

## 5. Heralded witness

```bash
python examples/minimal_heralded_witness.py
python examples/simulate_minimal_four_qubit_circuit.py
pytest -q tests/test_heralded_witness.py
```

The random product-effect stress test committed in the results file uses:

```text
samples = 20000
seed    = 20260817
```

The analytical separable bound, not the random search, is the proof.

## 6. Regenerate machine-readable files

```bash
python scripts/generate_results.py
```

This rewrites:

- `results/correction_core_results.json`;
- `results/figure5_corrected.csv`;
- `results/ibm_aggregate_reanalysis.json`;
- `results/heralded_witness_results.json`.

## 7. Correction PDF

The compiled PDF is committed at:

```text
correction/author_correction.pdf
```

Its standalone LaTeX source is:

```text
correction/author_correction.tex
```

A standard XeLaTeX or `latexmk -xelatex` installation can rebuild it.

## 8. Integrity

`CHECKSUMS.sha256` records SHA-256 checksums of the deliverable files. The original six Python files can additionally be checked against the Git blob hashes in `ORIGINAL_2022_CODE.md`.
