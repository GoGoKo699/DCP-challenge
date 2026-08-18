# Scientific Status and Claim Map

**Last updated:** 17 August 2026  
**Maintainer statement:** Ruge Lin

This file is the short authoritative status map. Detailed derivations are in `correction/AUTHOR_CORRECTION.md`; the machine-readable ledger is `correction/CLAIM_LEDGER.csv`.

## Retained

- normalized DCP sample definition;
- post-Fourier reflection phase state;
- complementary-label collision identity;
- exact parity recovery on the selected ideal ParitySolve branch;
- the special all-H outcome and its probability $1/N$;
- the published collision formulas as upper and lower bounds;
- ParitySolve as a structured DCP-derived circuit workload;
- the original ideal and noise simulations as simulations of their specified models.

## Retained and strengthened

For a single all-Hadamard sample, the published special-outcome decoder is Bayes-optimal among all classical decoders of the complete measurement record. The exact parity-conditioned distribution identity is

$$
P_0(r,y)-P_1(r,y)
=
\frac{(-1)^r}{N}\,\mathbf 1_{\{y=1\}}.
$$

Its optimal equal-prior success probability is therefore

$$
\frac12+\frac1{2N}.
$$

## Corrected

- The ideal honest success probability has an exact Stirling-number formula.
- Figure 5(a) has negative exact honest separation from the special decoder.
- Figure 5(b) has an exact honest gap of approximately 9.45 percent, not at least 10 percent.
- Figure 5(c) retains an approximately 25.03 percent difference against the special decoder, but that comparison is not sound.
- The standard error of empirical accuracy is $\sqrt{p(1-p)/r}$.

## Withdrawn

- $p_B$ bounds every weaker, product-measurement, or classically postprocessed strategy;
- $p>p_B$ verifies the claimed quantum-computation capability;
- no better nonqualifying strategy exists.

The decisive reason is reuse of the same secret across several samples. Individually parity-neutral outcomes can carry parity through their cross-sample correlations.

## Outside the correction scope

The four-qubit IBM run was a proof-of-concept experiment. It remains preserved in the historical code and is not reanalyzed or used to support the present correction.

## New follow-up result

The phase-twirled heralded witness is a separate 2026 author follow-up. Its ideal theorem supports only this claim:

> It witnesses a nonseparable joint measurement across two trusted DCP input cells against adaptive separable instruments, including LOCC, across the cell partition.

The theorem is about confidence with abstention. It does not certify universal quantum computation, speedup, the full LFC architecture, or a specific internal gate.

## Historical relationship to later work

The 2022 DCP challenge was an early DCP-specific trusted-input attempt to test joint inter-cell processing on near-term hardware. It predates Lee and Bae’s June 2026 GLOBAL-versus-SEP maximum-confidence framework, but it did not establish that framework’s sound separation. The present August 2026 reanalysis, assisted by GPT-5.6 Pro, identifies the relationship and supplies the sound DCP-specific formulation.

See `witness/HISTORICAL_CONTEXT.md` and `AI_ASSISTED_REANALYSIS.md`.

## Still open

- experimentally calibrated robustness of the heralded witness;
- implementation when hidden trusted inputs cannot be supplied independently of an untrusted cloud interface;
- adversaries with pre-shared entanglement or quantum communication across the cell partition;
- formal novelty determination for the exact DCP packaging.

## Journal record

Nothing in this repository is an APS Erratum or a replacement for the journal article. The original paper and historical code remain citable and accessible. The repository adds an explicit author-maintained correction so that later readers do not treat the withdrawn threshold interpretation as established.
