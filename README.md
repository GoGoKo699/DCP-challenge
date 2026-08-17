# DCP Challenge: Author Correction and Follow-Up Analysis

This repository accompanies the 2022 article:

> Ruge Lin and Weiqiang Wen, “A quantum computation capability verification protocol for NISQ devices with dihedral coset problem,” *Physical Review A* **106**, 012430 (2022).  
> DOI: `10.1103/PhysRevA.106.012430` - arXiv: `2202.06984`

## Scientific status - updated 17 August 2026

The original ParitySolve circuit is correct on its selected collision branch, but the original capability-verification interpretation is not.

The quantity denoted by $p_B$ in the article is the success probability of one specified all-Hadamard decoder. It is not a sound upper bound on all strategies using those measurements and classical postprocessing. An exact two-sample counterexample achieves

$$
\frac{25}{32}
$$

using the same product measurements, whereas the published decoder gives

$$
\frac{23}{32}.
$$

Therefore, this repository no longer presents the condition $p>p_B$ as a verification of quantum-computation capability.

**What remains valid:** the DCP sample construction, the Fourier-label collision mechanism, the selected ParitySolve algebra, and the use of the circuit as a structured hardware-sensitive workload.

**What is withdrawn:** the claim that the published $p_B$ threshold supplies an adversarially sound capability-verification test.

The full statement, derivations, corrected Figure 5 values, statistical correction, and IBM aggregate reanalysis are in:

- [Author correction in Markdown](correction/AUTHOR_CORRECTION.md)
- [Author correction in PDF](correction/author_correction.pdf)
- [Scientific status and claim map](SCIENTIFIC_STATUS.md)

> This is an author-maintained repository correction by Ruge Lin. It is not an APS Erratum, has not been peer reviewed as a replacement article, and does not alter the journal version.

## Historical record

The repository state that accompanied the article is preserved unchanged at the immutable tag and release:

```text
paper-2022-original
```

The six original root scripts remain byte-for-byte unchanged in the current repository:

```text
IBM.py
benchmarking.py
circuit.py
compare.py
proba.py
verification.py
```

They are retained for historical reproducibility and should be interpreted according to [ORIGINAL_2022_CODE.md](ORIGINAL_2022_CODE.md).

## Corrected results at a glance

| Figure | $(n,m,t)$ | Published $p_B$ | Published upper bound | Exact honest probability | Full-likelihood all-H |
|---|---:|---:|---:|---:|---:|
| 5(a) | $(4,6,1)$ | 0.660533 | 0.664083 | **0.652965** | **0.810940**, exact |
| 5(b) | $(6,9,4)$ | 0.716371 | 0.817392 | **0.810918** | **0.937289**, Monte Carlo |
| 5(c) | $(9,21,9)$ | 0.654461 | 0.906606 | **0.904804** | **0.957183**, Monte Carlo |

The exact honest probability is computed from the complementary-pair occupancy formula implemented in `src/dcp_challenge/exact_probabilities.py`.

## Reproduce the correction

The corrected analysis does not require Qibo.

```bash
python -m pip install -e .[test]
python examples/reproduce_counterexample.py
python examples/reproduce_figure5.py
python examples/reproduce_ibm_reanalysis.py
pytest -q
```

Expected central output:

```text
Published special-outcome decoder: 23/32 = 0.718750
Same measurements, better decoder: 25/32 = 0.781250
```

See [REPRODUCIBILITY.md](REPRODUCIBILITY.md) for full commands, fixed seeds, and the distinction between exact and Monte Carlo results.

## Separate follow-up: heralded DCP witness

The directory [witness/](witness/) contains a new phase-twirled, heralded construction. It is **not part of the 2022 article** and is **not a general proof of quantum computation**.

Its narrow ideal-model claim is:

> Against measurements separable across two trusted DCP input cells, every conclusive answer has conditional error at least $1/4$, while a Bell measurement has zero error and conclusive probability $1/(2N)$.

For $N=2$, the complete circuit uses four qubits, at most three CNOT gates, only Clifford operations, and no mid-circuit measurement. The statevector implementation is included and tested.

Start with [witness/README.md](witness/README.md).

## Repository map

```text
correction/                  Formal author correction, PDF, TeX, and claim ledger
src/dcp_challenge/           Corrected analytical implementation
examples/                    Small one-command reproductions
tests/                       Exact regression and full-state tests
results/                     Machine-readable committed outputs
witness/                     Separate non-peer-reviewed follow-up construction
IBM.py ... verification.py   Original 2022 scripts, unchanged
```

## Machine-readable results

- `results/correction_core_results.json`
- `results/figure5_corrected.csv`
- `results/ibm_aggregate_reanalysis.json`
- `results/heralded_witness_results.json`

## Citation

For the original ParitySolve construction and published article, cite:

```bibtex
@article{lin2022dcpchallenge,
  author  = {Ruge Lin and Weiqiang Wen},
  title   = {A quantum computation capability verification protocol for NISQ devices with dihedral coset problem},
  journal = {Physical Review A},
  volume  = {106},
  pages   = {012430},
  year    = {2022},
  doi     = {10.1103/PhysRevA.106.012430}
}
```

When relying on the corrected analysis, also identify:

```text
Ruge Lin, “Author Technical Correction and Updated Analysis” for the DCP challenge article,
DCP-challenge repository, author-correction-2026, 17 August 2026.
```

## License status

No software license has been added in this correction. The absence of a license means that ordinary copyright restrictions apply. This can be changed later by an explicit author decision; it is not part of the scientific correction.
