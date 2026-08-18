# Trust Model and Limitations

The ideal theorem is narrow. All assumptions below are material.

## Trusted quantum inputs

The verifier prepares the input states. A cloud submission that exposes the gates encoding $s$ or the shared phase $\alpha$ does not implement the stated adversarial model. Side-channel leakage can invalidate the soundness claim.

## Shared hidden phase

The two cells require the same hidden phase

$$
\alpha\in\{0,\pi/2,\pi,3\pi/2\}.
$$

Independent phases change the collision ensembles; a disclosed phase permits different attacks.

## Fresh sequential rounds

The secret and phase are fresh in every round. The prover returns $0$, $1$, or $\perp$ before receiving the next pair. This prevents accumulation of many copies carrying the same hidden bit, which caused the decisive failure in the original protocol.

## Single-round and sequential null classes

For one round, the proved null class consists of POVMs whose effects are separable across the two complete cell Hilbert spaces.

For repeated rounds, a stronger instrument-level condition is required. The prover begins with separable persistent memory and uses adaptive separable instruments, including LOCC instruments, across the cell partition. Each conditional branch must preserve separability. Merely requiring the displayed outcome probabilities to arise from separable effects would not rule out a hidden instrument that creates entangled memory for later rounds.

The null class allows:

- arbitrary local ancillas and quantum memory;
- arbitrary local operations;
- adaptive measurements;
- classical communication;
- arbitrary dependence on preceding public history.

It excludes:

- a nonseparable joint operation across the cells;
- quantum communication across the cell partition;
- pre-shared entanglement used to implement such a measurement.

The witness certifies the measurement resource, not the internal physical mechanism. A distributed prover with pre-shared entanglement could implement a nonseparable measurement by teleportation.

## Reporting and stopping

The sequential test requires predeclared $(C,E,R)$. Fewer than $C$ conclusive outcomes by round $R$ produce no certificate. Selectively abandoning and hiding unsuccessful runs invalidates the single-run significance statement unless all attempts are reported or corrected for multiple testing.

## What is not certified

The construction does not certify:

- universal quantum computation;
- a computational speedup;
- the entire locally fully connected architecture;
- a particular hardware CNOT;
- device independence;
- correctness of arbitrary device outputs.

## Noise and robustness

The committed theorem is ideal-model. If the two actual parity ensembles are within trace distances $\epsilon_0$ and $\epsilon_1$ of their ideal values, the equal-prior linear score can shift by at most

$$
2(\epsilon_0+\epsilon_1),
$$

because the score range has width four. This is not a complete calibrated experimental soundness theorem. A practical deployment must characterize trusted-input errors and incorporate them into the null threshold.

## Relation to prior work

Maximum-confidence discrimination and semi-device-independent certification existed before this follow-up. Ha and Kim developed nonlocal maximum confidence in 2024, and Lee and Bae gave an explicit GLOBAL-versus-SEP certification framework in June 2026 with the same ideal confidence values $1$ and $3/4$ for a different product-state ensemble.

The 2022 DCP challenge was earlier as a DCP-specific trusted-input attempt to test joint processing, but it did not contain the sound maximum-confidence theorem. The present contribution is limited to the DCP-specific phase-twirled construction, elementary factor-three proof, sequential formulation, and four-qubit embedding.

See [HISTORICAL_CONTEXT.md](HISTORICAL_CONTEXT.md).

## Novelty status

No exact prior DCP-specific construction with this phase twirl, complementary Fourier block, and tight separable bound was located as of 17 August 2026. This is not a formal novelty determination.

The core two-reflection-qubit comparison task also has a simpler direct realization without DCP rotation registers. The DCP construction should be described as an embedding and continuity result, not a resource-minimal primitive.
