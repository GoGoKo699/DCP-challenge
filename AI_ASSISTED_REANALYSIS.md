# AI-Assisted Reanalysis and Responsibility

## Public methodology statement

The August 2026 author correction and follow-up analysis were developed with substantial assistance from OpenAI’s **GPT-5.6 Pro**.

The model was used for:

- literature discovery and chronology checking;
- adversarial examination of the 2022 soundness argument;
- derivation and independent checking of exact probability formulas;
- construction and testing of the $23/32$ versus $25/32$ counterexample;
- formulation and proof checking of the phase-twirled heralded witness;
- numerical-test design, code generation, and code review;
- notation consistency and technical-document preparation.

In particular, the AI-assisted reanalysis helped identify that the published $p_B$ rule is optimal for one all-Hadamard sample but fails when multiple samples share the same secret. It also helped recognize the structural relationship between the 2022 DCP challenge and later maximum-confidence certification of GLOBAL versus separable measurements, including Lee and Bae’s June 2026 work.

## Responsibility

GPT-5.6 Pro is not an author and cannot assume responsibility for scientific claims. Ruge Lin:

- selected the claims included in this repository;
- reviewed the mathematical arguments and numerical evidence;
- chose the scope and wording of the correction;
- accepts responsibility for the repository’s scientific content.

The source code, exact tests, machine-readable results, proof limitations, and historical snapshot are supplied so that the work can be checked independently rather than accepted on the basis of AI assistance.

## Chronology

- **14 February 2022:** the DCP challenge first appeared on arXiv.
- **22 July 2022:** the article was published in *Physical Review A*.
- **11 June 2026:** Lee and Bae posted a sound maximum-confidence framework for certifying GLOBAL rather than separable measurements on trusted product-state ensembles.
- **August 2026:** Ruge Lin, assisted by GPT-5.6 Pro, identified the original DCP threshold failure, connected the project to the later framework, and developed the corrected DCP-specific witness.

This chronology does not allege that later work depended on the DCP article. It records that the 2022 project was an earlier conceptual and experimental antecedent, while the sound DCP-specific theorem was obtained only in the 2026 reanalysis.
