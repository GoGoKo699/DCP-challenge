# DCP Challenge: Author Correction and Follow-Up Analysis

This repository accompanies the 2022 article:

> Ruge Lin and Weiqiang Wen, “A quantum computation capability verification protocol for NISQ devices with dihedral coset problem,” *Physical Review A* **106**, 012430 (2022).  
> DOI: `10.1103/PhysRevA.106.012430` - arXiv: `2202.06984`

## Scientific status - updated 17 August 2026

The original ParitySolve circuit is correct on its selected collision branch, but the original capability-verification interpretation is not.

The quantity denoted by $p_B$ in the article is the success probability of one specified all-Hadamard decoder. For one all-Hadamard sample, that decoder is in fact Bayes-optimal. The failure begins when several samples reuse the same hidden secret: outcomes that reveal no parity individually can become informative through their correlations.

An exact two-sample counterexample uses the same product measurements and only changes the classical decoder:

$$
 p_B=\frac{23}{32},
 \qquad
 p_{\rm better}=\frac{25}{32}.
$$

Therefore, this repository no longer presents $p>p_B$ as verification of quantum-computation capability.

**Retained:** the DCP sample construction, the Fourier-label collision mechanism, the selected ParitySolve algebra, and the circuit as a structured hardware-sensitive workload.

**Withdrawn:** the claim that the published $p_B$ threshold is an adversarially sound capability-verification bound.

The complete statement is available in:

- [Author correction in Markdown](correction/AUTHOR_CORRECTION.md)
- [Author correction in PDF](correction/author_correction.pdf)
- [Scientific status and claim map](SCIENTIFIC_STATUS.md)

> This is an author-maintained repository correction by Ruge Lin. It is not an APS Erratum, has not been peer reviewed as a replacement article, and does not alter the journal version.

The proof-of-concept IBM experiment is preserved in the historical code but is outside the scope of the present correction.

## Historical record

The repository state that accompanied the article is preserved unchanged at the immutable tag and release:

```text
paper-2022-original
```

The six original root scripts remain byte-for-byte unchanged:

```text
IBM.py
benchmarking.py
circuit.py
compare.py
proba.py
verification.py
```

They are retained for historical reproducibility and described in [ORIGINAL_2022_CODE.md](ORIGINAL_2022_CODE.md).

## Corrected results at a glance

| Figure | $(n,m,t)$ | Published $p_B$ | Published upper bound | Exact honest probability | Full-likelihood all-H |
|---|---:|---:|---:|---:|---:|
| 5(a) | $(4,6,1)$ | 0.660533 | 0.664083 | **0.652965** | **0.810940**, exact |
| 5(b) | $(6,9,4)$ | 0.716371 | 0.817392 | **0.810918** | **0.937289**, Monte Carlo |
| 5(c) | $(9,21,9)$ | 0.654461 | 0.906606 | **0.904804** | **0.957183**, Monte Carlo |

The exact honest probability is computed from the complementary-pair occupancy formula in `src/dcp_challenge/exact_probabilities.py`.

## Reproduce the correction

The corrected analysis does not require Qibo.

```bash
python -m pip install -e .[test]
python examples/reproduce_counterexample.py
python examples/reproduce_one_sample_optimality.py
python examples/reproduce_figure5.py
python scripts/verify_historical_files.py
python scripts/validate_committed_results.py
pytest -q
```

Expected central output:

```text
Published special-outcome decoder: 23/32 = 0.718750
Same measurements, better decoder: 25/32 = 0.781250
```

See [REPRODUCIBILITY.md](REPRODUCIBILITY.md) for fixed seeds, exact-versus-numerical distinctions, and validation tolerances. The completed checks are summarized in [VALIDATION_RECORD.md](VALIDATION_RECORD.md).

## Separate follow-up: phase-twirled heralded DCP witness

The directory [witness/](witness/) contains a new 2026 follow-up. It is not part of the 2022 article and is not a general proof of quantum computation.

Its narrow ideal-model claim is:

> Against adaptive separable instruments across two trusted DCP input cells, every conclusive answer has conditional error at least $1/4$, while a Bell measurement has zero error and conclusive probability $1/(2N)$.

This is a DCP-specific maximum-confidence witness of a nonseparable joint measurement. For $N=2$, the complete circuit uses four qubits, at most three CNOT gates, only Clifford operations, and no mid-circuit measurement.

The [historical chronology and relation to later work](witness/HISTORICAL_CONTEXT.md) makes the priority boundaries explicit. The 2022 DCP article predates Lee and Bae’s 2026 GLOBAL-versus-SEP maximum-confidence framework as an early trusted-input attempt to test joint inter-cell processing, but it did not prove their sound separation. The sound DCP-specific witness was developed only in the August 2026 reanalysis.

## AI-assisted reanalysis

The August 2026 correction and follow-up were developed with substantial assistance from OpenAI’s **GPT-5.6 Pro**, including literature research, adversarial mathematical checking, numerical validation, code review, and preparation of the reproducible package. Ruge Lin reviewed the resulting claims and accepts responsibility for the repository’s scientific content.

See [AI_ASSISTED_REANALYSIS.md](AI_ASSISTED_REANALYSIS.md) for the full methodology and responsibility statement.

## Repository map

```text
correction/                  Formal author correction, PDF, TeX, and claim ledger
src/dcp_challenge/           Corrected analytical implementation
examples/                    Small one-command reproductions
tests/                       Exact regression and full-state tests
results/                     Machine-readable committed outputs
witness/                     Separate non-peer-reviewed follow-up construction
AI_ASSISTED_REANALYSIS.md    AI methodology, credit, and responsibility statement
IBM.py ... verification.py   Original 2022 scripts, unchanged
```

## Machine-readable results

- `results/correction_core_results.json`
- `results/one_sample_optimality.json`
- `results/figure5_corrected.csv`
- `results/heralded_witness_results.json`
- `results/validation_crosschecks.json`

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

No software license has been added in this correction. Ordinary copyright restrictions therefore apply unless an explicit license is added later.
