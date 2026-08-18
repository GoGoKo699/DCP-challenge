# Historical Chronology and Relation to Later Work

This file records chronology, conceptual priority, and the boundary between the 2022 article and the sound 2026 follow-up.

## Chronology

### 2006 - maximum-confidence measurements

Croke, Andersson, Barnett, Gilson, and Jeffers introduced maximum-confidence quantum measurements, where a detected outcome is judged by the posterior probability that its associated state was prepared and an inconclusive result is allowed.

- [Phys. Rev. Lett. 96, 070401 (2006)](https://doi.org/10.1103/PhysRevLett.96.070401)

### December 2021 / September 2022 - semi-device-independent maximum-confidence certification

Flatt, Lee, Roch i Carceller, Brask, and Bae posted their preprint on 17 December 2021 and published it in September 2022. They developed semi-device-independent certification of maximum-confidence measurements against noncontextual models. This general maximum-confidence certification direction therefore predates the DCP preprint, although it did not formulate the GLOBAL-versus-separable task used here.

- [arXiv:2112.09626](https://arxiv.org/abs/2112.09626)
- [PRX Quantum 3, 030337 (2022)](https://doi.org/10.1103/PRXQuantum.3.030337)

### February / July 2022 - the DCP challenge

The DCP challenge was submitted to arXiv on 14 February 2022 and published in *Physical Review A* on 22 July 2022. It proposed trusted DCP input states, a one-way quantum channel, joint inter-cell processing, and a near-term hardware challenge.

This was an early DCP-specific attempt to test joint quantum processing from trusted quantum inputs. Its experimental architecture and ambition are genuine historical antecedents of later work on certifying global measurements. However, its forced-guess accuracy threshold $p>p_B$ was not sound and did not establish a GLOBAL-versus-separable confidence separation.

- [arXiv:2202.06984](https://arxiv.org/abs/2202.06984)
- [Phys. Rev. A 106, 012430 (2022)](https://doi.org/10.1103/PhysRevA.106.012430)

### 2024 - nonlocal maximum confidence

Ha and Kim developed a general connection between maximum confidence inaccessible to LOCC, separable operators, and entanglement witnesses.

- [Scientific Reports 14, 23815 (2024)](https://doi.org/10.1038/s41598-024-75149-y)

### June 2026 - explicit GLOBAL-versus-SEP certification

Lee and Bae posted *Semi-Device-Independent Certification for Nonlocality without Entanglement* on 11 June 2026. They gave a sound maximum-confidence framework for trusted separable input ensembles and showed, for an antiparallel-state ensemble,

$$
C_{\rm GLOBAL}=1,
\qquad
C_{\rm SEP}=\frac34.
$$

They also treated outcome rates and imperfect detection in a broader optimization framework.

- [arXiv:2606.13667](https://arxiv.org/abs/2606.13667)

Their paper does not cite the 2022 DCP article. The DCP article could reasonably have been cited as an earlier trusted-input attempt to test joint processing, but the omission is understandable: the terminology, state ensemble, optimization framework, and mathematical claim are different, and the original DCP separator was unsound. No dependence, misconduct, or fault is alleged.

### August 2026 - GPT-assisted author reanalysis

Ruge Lin, with substantial assistance from OpenAI’s GPT-5.6 Pro, carried out an adversarial reanalysis of the 2022 protocol. The work:

- identified the exact multi-sample failure of the original $p_B$ threshold;
- proved that the original decoder was nevertheless optimal for one all-Hadamard sample;
- recognized the structural relation to maximum-confidence GLOBAL-versus-SEP certification;
- constructed and checked the phase-twirled heralded DCP witness;
- formalized its ideal and adaptive sequential soundness.

Ruge Lin reviewed the claims and accepts responsibility for the repository. See [AI-assisted methodology](../AI_ASSISTED_REANALYSIS.md).

## Precise relationship between the constructions

| Feature | 2022 DCP challenge | Lee-Bae 2026 | Present DCP follow-up |
|---|---|---|---|
| Inputs | Trusted DCP samples | Trusted antiparallel product states | Trusted phase-twirled DCP cell pair |
| Target | Secret parity accuracy | State-identification confidence | Parity confidence with abstention |
| Honest resource | Inter-cell interference | GLOBAL measurement | Bell-type nonseparable measurement |
| Restricted class | Not formally optimized | SEP / LOCC | Adaptive separable instruments / LOCC |
| Sound separator | No | Yes | Yes, ideal model |
| Confidence gap | Not formulated | $1$ versus $3/4$ | $1$ versus at most $3/4$ |
| Status | Published precursor with flawed soundness | Independent later framework | New non-peer-reviewed DCP-specific realization |

## Priority statement

The strongest defensible summary is:

> The 2022 DCP challenge appears to be an early DCP-specific trusted-input proposal for testing joint quantum processing on near-term hardware. It did not establish a sound global-versus-separable measurement separation. Independent maximum-confidence work, culminating in Lee and Bae’s 2026 framework, supplied the correct general perspective. The August 2026 author reanalysis then produced a sound DCP-specific realization using phase twirling, abstention, fresh rounds, and a proved separable-confidence bound.

No novelty is claimed for the general maximum-confidence certification principle. The possible novelty is limited to the exact DCP-specific construction, proof, and four-qubit embedding; no formal novelty determination has been made.
