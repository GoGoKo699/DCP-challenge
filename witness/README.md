# Phase-Twirled Heralded DCP Witness

> **Status:** New author follow-up, dated 2026. It is not part of the 2022 article, has not been peer reviewed, and does not restore the article's original general capability-verification claim.

## Narrow claim

Under the trusted-input and timing assumptions stated in [LIMITATIONS.md](LIMITATIONS.md), the construction witnesses a **nonseparable joint measurement across two DCP input cells** against POVMs whose effects are separable across that cell partition.

It does not certify universal quantum computation, quantum speedup, a particular physical CNOT, or the full locally fully connected architecture proposed in the original article.

## Ideal separation

For two phase-twirled cells, conditioned on complementary Fourier labels, the parity ensembles are

\[
\sigma_0=\frac14|00\rangle\langle00|
+\frac12|\Psi^+\rangle\langle\Psi^+|
+\frac14|11\rangle\langle11|,
\]

\[
\sigma_1=\frac14|00\rangle\langle00|
+\frac12|\Psi^-\rangle\langle\Psi^-|
+\frac14|11\rangle\langle11|.
\]

The honest Bell measurement has

\[
p_{\rm correct}=\frac1{2N},\qquad p_{\rm wrong}=0.
\]

Every separable strategy satisfies

\[
p_{\rm correct}\le 3p_{\rm wrong},
\]

so its conditional error, whenever it gives an answer, is at least \(1/4\).

The separation is specifically about **confidence with abstention**. If inconclusive outcomes are replaced by random guesses, joint and separable strategies both reach

\[
\frac12+\frac1{4N}.
\]

## Minimal implementation

For \(N=2\), the witness uses four qubits and only Clifford gates. A complete round has at most three CNOT gates, no ancilla, no non-Clifford gate, no mid-circuit measurement, and no dynamic feed-forward.

The dependency-light statevector implementation is:

```bash
python examples/simulate_minimal_four_qubit_circuit.py
```

Its exhaustive average gives:

```text
correct conclusive = 0.25
wrong conclusive   = 0
inconclusive       = 0.75
```

## Files

- [PROTOCOL.md](PROTOCOL.md): precise round definition and acceptance statistics.
- [PROOF.md](PROOF.md): ideal completeness and separable soundness proof.
- [CIRCUIT.md](CIRCUIT.md): minimal four-qubit circuit and decoder.
- [LIMITATIONS.md](LIMITATIONS.md): trust model, excluded adversaries, robustness status, and claim boundaries.
- [REFERENCES.md](REFERENCES.md): related primary literature.
- `src/dcp_challenge/heralded_witness.py`: analytical and dense-matrix checks.
- `src/dcp_challenge/minimal_circuit.py`: static four-qubit statevector model.
- `results/heralded_witness_results.json`: committed numerical checks.
