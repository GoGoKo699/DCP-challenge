# Reproducibility Guide

## 1. Environment

Recommended:

- Python 3.10 or later;
- NumPy 1.24 or later;
- pytest 8 for tests.

Install from the repository root:

```bash
python -m pip install -e .[test]
```

Run the complete test suite:

```bash
pytest -q
```

## 2. Historical integrity

Verify that the six original root scripts are unchanged from their historical Git blobs:

```bash
python scripts/verify_historical_files.py
```

## 3. Decisive exact counterexample

```bash
python examples/reproduce_counterexample.py
```

Expected values:

```text
23/32 = 0.718750
25/32 = 0.781250
```

Both are exact rational calculations.

## 4. One-sample optimality theorem

The test suite checks, for $n=1,\ldots,7$, the exact identity

$$
P_0(r,y)-P_1(r,y)
=
\frac{(-1)^r}{N}\,\mathbf 1_{\{y=1\}},
$$

and therefore the Bayes-optimal one-sample all-H success

$$
\frac12+\frac1{2N}.
$$

Run:

```bash
python examples/reproduce_one_sample_optimality.py
pytest -q tests/test_likelihood_decoder.py
```

The committed exact records are in `results/one_sample_optimality.json`.

## 5. Exact honest probability and Figure 5

```bash
python examples/reproduce_figure5.py
```

The no-complementary-collision probability is

$$
k_{\rm nc}(N,m)
=
\frac1{N^m}
\sum_{j=1}^{\min(m,N/2)}
\binom{N/2}{j}2^j j!\,{m\brace j},
$$

and the exact honest success probability is

$$
p_{\rm exact}
=
1-\frac12\left(\frac{1+k_{\rm nc}}2\right)^t.
$$

Figure 5(a) has an exact full-likelihood all-H value. Figure 5(b) and 5(c) use frozen fixed-seed Monte Carlo records with Wilson intervals in `results/figure5_corrected.csv`; independent-seed checks are in `results/validation_crosschecks.json`.

## 6. Heralded witness

Run the exact and dense-matrix checks:

```bash
pytest -q tests/test_heralded_witness.py
python examples/simulate_minimal_four_qubit_circuit.py
```

The tests cover:

- collision-state normalization and positivity;
- the tight separable likelihood ratio $3$;
- complete two-cell ensembles for $N=2,4$;
- maximally mixed one-cell marginals;
- trace-norm and forced-guess values;
- finite-sample sequential bounds;
- the complete minimal four-qubit statevector circuit.

## 7. Validate committed result files

```bash
python scripts/validate_committed_results.py
```

Validation policy:

- exact rational, integer, and combinatorial quantities are compared exactly;
- fixed Monte Carlo records include seeds, trial counts, estimates, and Wilson intervals;
- floating-point linear-algebra diagnostics are compared within the numerical tolerances encoded by the tests;
- byte-identical portability of floating-point JSON across all numerical libraries and processors is not claimed.

To regenerate the quick committed outputs:

```bash
python scripts/generate_results.py
```

## 8. Historical software

The original scripts require their 2022 Qibo environment and are not imported by the corrected test suite. `requirements-legacy.txt` records the historical dependency request. The proof-of-concept IBM experiment is preserved but is outside the present correction.


The completed repository-level checks are summarized in [VALIDATION_RECORD.md](VALIDATION_RECORD.md).
