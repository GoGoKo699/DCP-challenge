# Original 2022 Code

The immutable release `paper-2022-original` preserves the historical repository state at commit

```text
1a8f9c40d4498169c5330101195d9fbb5b4695c2
```

The six original Python scripts at the root of this corrected package are byte-for-byte identical to their historical Git blobs:

| File | Historical Git blob SHA-1 |
|---|---|
| `IBM.py` | `aa04bed4c53b66dabd5a559c6250eb81d1a935ee` |
| `benchmarking.py` | `3fe387258d18452f158b57ada6e97571b1935f3a` |
| `circuit.py` | `4d0faf0d0e1d2e496f95d81b8448bb6a97b466c4` |
| `compare.py` | `1e49ddf01fe3d21f5686670a89259ae66b9bdf3` |
| `proba.py` | `723d1e3c2fea3fb86abc7e4c11c42e8597c83808` |
| `verification.py` | `ff088128a487a3dd8963ebea37f66319e8ea278c` |

They have intentionally not been edited to rewrite the historical record.

## Interpretation warnings

- `proba.p_B` computes the special-outcome decoder probability, not a general soundness bound.
- `compare.py` selects instances using `p_upper - p_B`; this does not establish an actual honest verification gap.
- `verification.py` and `benchmarking.py` use the legacy fluctuation formula rather than the Bernoulli standard error.

The IBM script and experiment are retained only as the original proof-of-concept record and are outside the present correction.

Corrected analytical implementations are under `src/dcp_challenge/`. The modern tests do not import the original scripts.

## Historical software stack

The original code named Qibo 0.1.10 and was written for its 2022 environment. It may not run unchanged under a current Python/Qibo stack. `requirements-legacy.txt` records the historical dependency request but is not part of continuous integration.
