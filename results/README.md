# Machine-Readable Results

- `correction_core_results.json`: central exact values, one-sample theorem records, corrected Figure 5 data, statistical correction, and witness checks.
- `one_sample_optimality.json`: exact parity-distribution support and Bayes-optimal success for $n=1,\ldots,7$.
- `figure5_corrected.csv`: corrected Figure 5 table and simulation metadata.
- `heralded_witness_results.json`: dense-state checks, tight product-effect values, adaptive finite-sample examples, and circuit resources.
- `validation_crosschecks.json`: independent-seed Monte Carlo checks of the frozen Figure 5 likelihood estimates.

Files are generated or validated by `scripts/generate_results.py` and `scripts/validate_committed_results.py`.

Exact rational, integer, and combinatorial quantities reproduce exactly. Floating-point linear-algebra diagnostics are validated within declared test tolerances; byte-identical portability across all platforms is not claimed.
