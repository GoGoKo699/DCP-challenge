# Phase-Twirled Heralded DCP Witness

> **Status:** New author follow-up, dated August 2026. It is not part of the 2022 article, has not been peer reviewed, and does not restore the article’s original general capability-verification claim.

## September scientific extension

[The complete scientific revision](../correction/SCIENTIFIC_REVISION_2026_09.md) proves the full answer-rate frontier and strengthens the single-round bound to PPT effects. The confidence advantage disappears at total conclusive rate $q\ge1/N$. A specified calibrated phase-noise model is solved exactly. General preparation errors require an adjusted statistical test: ideal loss tolerance is not immunity to hidden-label leakage.

## Narrow claim

Under the trusted-input, timing, and memory assumptions in [LIMITATIONS.md](LIMITATIONS.md), the construction witnesses a **nonseparable joint measurement across two DCP input cells** against adaptive separable instruments, including LOCC, across that cell partition.

It does not certify universal quantum computation, quantum speedup, a particular physical CNOT, or the full locally fully connected architecture proposed in the original article.

## Maximum-confidence interpretation

The witness is a DCP-specific maximum-confidence task. A conclusive result is evaluated by its posterior confidence rather than by forced-guess average accuracy.

For two phase-twirled cells, conditioned on complementary Fourier labels, the parity ensembles are

$$
\sigma_0=\frac14|00\rangle\langle00|
+\frac12|\Psi^+\rangle\langle\Psi^+|
+\frac14|11\rangle\langle11|,
$$

$$
\sigma_1=\frac14|00\rangle\langle00|
+\frac12|\Psi^-\rangle\langle\Psi^-|
+\frac14|11\rangle\langle11|.
$$

The honest Bell measurement has

$$
p_{\rm correct}=\frac1{2N},
\qquad
p_{\rm wrong}=0.
$$

Every separable strategy satisfies

$$
p_{\rm correct}\le 3p_{\rm wrong},
$$

so its confidence cannot exceed $3/4$ whenever it gives an answer. The factor is tight.

If inconclusive outcomes are replaced by random guesses, joint and separable strategies both reach

$$
\frac12+\frac1{4N}.
$$

The separation is therefore specifically about **confidence with abstention**.

## Adaptive sequential test

Fresh pairs are supplied one at a time. The prover answers $0$, $1$, or $\perp$ before receiving the next pair. Against adaptive separable instruments with separable memory, the conditional error probability of each successive conclusive answer remains at least $1/4$, even after conditioning on the preceding public history.

Predeclare integers $(C,E,R)$:

- stop after $C$ conclusive answers or $R$ total rounds;
- issue no certificate if fewer than $C$ conclusive answers occur;
- otherwise accept only if at most $E$ conclusive answers are wrong.

The false-certification probability is bounded by

$$
\sum_{j=0}^{E}
\binom{C}{j}
\left(\frac14\right)^j
\left(\frac34\right)^{C-j},
$$

without assuming independent errors or fair sampling.

## Minimal implementation

For $N=2$, the witness uses four qubits and only Clifford gates. A complete round has at most three CNOT gates, no ancilla, no non-Clifford gate, no mid-circuit measurement, and no dynamic feed-forward.

```bash
python examples/simulate_minimal_four_qubit_circuit.py
```

Expected exhaustive average:

```text
correct conclusive = 0.25
wrong conclusive   = 0
inconclusive       = 0.75
```

## Historical context

The 2022 DCP article predates Lee and Bae’s 2026 GLOBAL-versus-SEP maximum-confidence framework as an earlier trusted-input attempt to test joint inter-cell processing, but it did not prove the later sound separation. The August 2026 reanalysis, assisted by GPT-5.6 Pro, identified both the original error and the relationship to later work.

See [HISTORICAL_CONTEXT.md](HISTORICAL_CONTEXT.md) for the full chronology and careful priority statement.

## Files

- [PROTOCOL.md](PROTOCOL.md): round definition, null class, and acceptance statistics.
- [PROOF.md](PROOF.md): ideal completeness, separable soundness, and adaptive sequential theorem.
- [CIRCUIT.md](CIRCUIT.md): minimal four-qubit circuit and decoder.
- [LIMITATIONS.md](LIMITATIONS.md): trust model, excluded adversaries, robustness status, and claim boundaries.
- [HISTORICAL_CONTEXT.md](HISTORICAL_CONTEXT.md): chronology and relation to later work.
- [REFERENCES.md](REFERENCES.md): primary literature.
- `src/dcp_challenge/heralded_witness.py`: analytical and dense-matrix checks.
- `src/dcp_challenge/minimal_circuit.py`: static four-qubit statevector model.
- `results/heralded_witness_results.json`: committed numerical checks.
