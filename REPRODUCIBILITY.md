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
python scripts/verify_checksums.py
```

The result validator checks all six JSON/CSV records, every field, duplicate
representations in the core JSON, schemas, and finite-number requirements.
It recomputes exact counterexamples, one-sample records, all Figure 5 analytical
probabilities, the exact Figure 5(a) likelihood result, witness summaries,
dense-matrix diagnostics, the 20,000-product-effect diagnostic, and tail examples.
Expected values are built without reading the files under validation.

Integer and rational fields must agree exactly. Ordinary nonzero floating
quantities use relative tolerance `1e-12` and zero absolute tolerance. Only the
dense-matrix marginal residual permits absolute tolerance `1e-12`; this is not
used to round small probabilities to zero. Byte-identical floating-point
portability is not claimed. Validation uses explicit exceptions, so it also
runs under `python -O`.

**Monte Carlo boundary:** fast validation does not repeat the million-trial
Figure 5(b) or the 60,000-trial Figure 5(c) experiment. It checks archived success
counts, seeds, trial counts, estimates, and recomputed Wilson intervals, including
the independent-seed cross-check records. These are archived evidence, not fresh
simulation results. Deliberate-corruption tests alter each of the 1268 result
fields and require rejection, including changes made to duplicate records together.

The checksum verifier additionally checks all tracked file bytes and complete
manifest coverage. For an extracted source ZIP without Git, it checks the file
tree excluding recognized local caches/build directories. Checksums detect
snapshot changes, not scientific correctness or authenticity.

To regenerate outputs without overwriting the archived files:

```bash
python scripts/generate_results.py --output /tmp/dcp-reference-results
```

To explicitly rerun the larger Figure 5 simulations, use:

```bash
python scripts/generate_results.py --monte-carlo --output /tmp/dcp-fresh-monte-carlo
```

The latter still retains the separate historical independent-seed cross-check
records. Fresh Monte Carlo output need not be byte-identical across numerical
environments; it must not silently replace the archived record or be confused
with the fast validator. Regeneration may change harmless last-bit diagnostics.

## 8. Stable statistical evaluation

The binomial routines use a scaled probability-mass recurrence and logarithms
instead of multiplying huge coefficients by tiny powers. They require no new
runtime dependency. For example, `binomial_lower_tail(2000, 400)` evaluates to
approximately `7.183777008e-8` instead of overflowing.

```python
from dcp_challenge.statistics import (
    binomial_lower_tail,
    binomial_log_lower_tail,
    adaptive_sequential_log_lower_tail_bound,
)

probability = binomial_lower_tail(2000, 400)
log_probability = binomial_log_lower_tail(10000, 0)
# log_probability is approximately -2876.8207245, not negative infinity.
log_bound = adaptive_sequential_log_lower_tail_bound(10000, 0)
```

All logarithms are natural. When a positive tail would underflow to zero, the
ordinary probability function raises `FloatingPointError` directing callers to
the log API. A zero return is reserved for an exact-zero endpoint. Counts must
be integers and probabilities must be finite and in `[0, 1]`.

These are floating-point evaluations of the analytical bound, not certified
interval-arithmetic enclosures. They do not validate physical trust assumptions,
experimental stopping rules, or repeated selective restarts. Work and integer
storage increase with experiment size. Tests include exact rational references,
endpoint checks, tail monotonicity, and the previously overflowing cases.

## 9. Historical software

The original scripts require their 2022 Qibo environment and are not imported by the corrected test suite. `requirements-legacy.txt` records the historical dependency request. The proof-of-concept IBM experiment is preserved but is outside the present correction.


The completed repository-level checks are summarized in [VALIDATION_RECORD.md](VALIDATION_RECORD.md).


## September scientific revision

`python examples/reproduce_scientific_revision.py` prints the unrestricted one-sample optimum, refreshed-secret limitation, exact confidence-rate values, and a fixed-round source-error example. `python -m pytest -q tests/test_scientific_revision.py` independently constructs raw states, verifies operator certificates, and checks explicit measurements attaining the frontier.

`results/scientific_revision_results.json` is recomputed without reading its stored contents and participates in every-field mutation validation. The earlier five result files are unchanged.

For an independent optimization check, install the optional audit dependency with `python -m pip install -e '.[audit]'` and run `python scripts/audit_scientific_frontier.py`. Its 96 GLOBAL/PPT linear programs start from explicit raw source states. The runtime package still needs only NumPy. Mathematical proofs, rather than numerical optimizer output, establish the general claims.

The August correction PDF remains a dated record. September's revised conclusions are stated in `correction/SCIENTIFIC_REVISION_2026_09.md`; they are not backdated into that PDF.
