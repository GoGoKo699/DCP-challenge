# Trust Model and Limitations

The ideal theorem is narrow. All of the following assumptions are material.

## Trusted quantum inputs

The verifier prepares the input states. A cloud submission that exposes the gates encoding \(s\) or the shared phase \(\alpha\) does not implement the stated adversarial model. Side-channel leakage can likewise invalidate the soundness claim.

## Shared hidden phase

The two cells require the same phase

\[
\alpha\in\{0,\pi/2,\pi,3\pi/2\}.
\]

The phase must remain hidden from the prover. Independent phases would change the collision ensembles; a disclosed phase would permit different attacks.

## Fresh sequential rounds

The secret and phase are fresh in every round. The prover returns \(0,1\), or \(\perp\) before receiving the next pair. This prevents accumulation of many copies carrying the same hidden bit, which was the decisive problem in the original protocol.

## Null class

The proved null class consists of POVMs with effects separable across the two complete cell Hilbert spaces. It allows arbitrary local ancillas, arbitrary local operations, adaptive measurements, and classical communication. It excludes:

- a nonseparable joint operation across the cells;
- quantum communication across the cell partition;
- pre-shared entanglement used to implement such a measurement.

The witness certifies the measurement resource, not the internal physical mechanism. A distributed prover with pre-shared entanglement could implement a nonseparable measurement by teleportation.

## What is not certified

The construction does not certify:

- universal quantum computation;
- a computational speedup;
- the entire locally fully connected architecture;
- a particular hardware CNOT;
- device independence;
- correctness of arbitrary outputs from the device.

## Noise and robustness

The committed theorem is ideal-model. If the two actual parity ensembles are within trace distances \(\epsilon_0\) and \(\epsilon_1\) of their ideal values, the equal-prior linear score can shift by at most

\[
2(\epsilon_0+\epsilon_1),
\]

because the score range has width four. This observation is not yet a complete calibrated experimental soundness theorem. A practical deployment must characterize trusted-input errors and incorporate them into the null threshold.

## Novelty status

The ingredients overlap established work on unambiguous state comparison, maximum-confidence discrimination, semiquantum games, and certification of entangled measurements. No exact prior construction with this DCP packaging was identified during the preparatory search, but this is not a formal novelty determination.

The core two-reflection-qubit comparison task also has a simpler direct realization without DCP rotation registers. The DCP construction should be described as an embedding and continuity result, not a resource-minimal primitive.
