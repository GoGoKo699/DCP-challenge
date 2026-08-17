# Scientific Status and Claim Map

**Last updated:** 17 August 2026  
**Maintainer statement:** Ruge Lin

This file is the short authoritative status map for the repository. The detailed derivations are in `correction/AUTHOR_CORRECTION.md`, and the complete machine-readable ledger is in `correction/CLAIM_LEDGER.csv`.

## Retained

The following statements remain supported:

- the normalized DCP sample definition;
- the post-Fourier reflection phase state;
- the complementary-label collision identity;
- exact parity recovery on the selected ideal ParitySolve branch;
- the special all-H outcome and its probability $1/N$ for every $n$;
- the published collision formulas when interpreted as upper and lower bounds;
- ParitySolve as a structured DCP-derived circuit workload;
- the original ideal and noise simulations as simulations of their specified models.

## Retained with narrower wording

- The quantity formerly denoted $p_B$ is retained only as the success probability of the *special-outcome all-H decoder*.
- The IBM data are retained as aggregate evidence about a selected Bell-type branch, not as a direct end-to-end execution of the complete challenge.
- Noise studies are illustrative benchmark simulations, not adversarial robustness proofs.

## Corrected

- The ideal honest success probability has an exact Stirling-number formula.
- Figure 5(a) has negative exact honest separation from the special decoder.
- Figure 5(b) has an exact honest gap of approximately 9.45 percent, not at least 10 percent.
- Figure 5(c) retains an approximately 25.03 percent difference against the special decoder, but that comparison is not sound.
- The standard error of empirical accuracy is $\sqrt{p(1-p)/r}$.
- The archived IBM aggregate reconstruction is 0.7439808125 under the documented corrected aggregation.

## Withdrawn

The current repository withdraws these interpretations:

- $p_B$ bounds every weaker, product-measurement, or classically postprocessed strategy;
- $p>p_B$ verifies the claimed quantum-computation capability;
- no better nonqualifying strategy exists;
- the legacy `IBM.py` logic faithfully reconstructs the stated measured collision event.

## Not repeated because unsupported

The corrected landing page does not rely on broad eavesdropper or channel-security claims for which the article did not provide a formal adversary model and proof.

## New follow-up result

The phase-twirled heralded witness is a separate 2026 author follow-up. Its ideal proof supports only this claim:

> It witnesses a nonseparable joint measurement across two trusted DCP input cells against POVMs with effects separable across the cell partition.

It does not certify universal quantum computation, speedup, the full LFC architecture, or a specific internal gate.

## Still open

- experimentally calibrated robustness of the heralded witness;
- implementation when hidden trusted inputs cannot be supplied independently of an untrusted cloud interface;
- security against pre-shared entanglement or quantum communication across the cell partition;
- formal novelty determination for the exact DCP packaging.

## Status of the journal record

Nothing in this repository is an APS Erratum or a replacement of the journal article. The original paper and its historical code remain citable and accessible. The repository adds an explicit author-maintained correction so that later readers do not treat the withdrawn threshold interpretation as established.
