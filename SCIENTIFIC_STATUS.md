# Scientific Status and Claim Map

**Last scientific revision:** 7 September 2026  
**Maintainer statement:** Ruge Lin

The current scientific synthesis is [the September revision](correction/SCIENTIFIC_REVISION_2026_09.md). The [August correction](correction/AUTHOR_CORRECTION.md) and its PDF remain dated historical statements of the earlier analysis. The machine-readable map is [the claim ledger](correction/CLAIM_LEDGER.csv).

## What remains withdrawn

The original shared-secret implication $p>p_B$ certifies quantum-computation capability is false. The exact all-Hadamard counterexample gives $25/32$ instead of $23/32$ by changing classical decoding alone. No September result reinstates that implication.

No general channel-security, computational-speedup, or universal-capability claim is adopted by this repository.

## What remains valid

The normalized DCP input, post-Fourier phase state, complementary-label collision algebra, and selected noiseless ParitySolve branch are valid. The old circuit is a structured workload. The exact occupancy formula, corrected Figure 5 probabilities, and Bernoulli standard error remain as established in August. Legacy noise simulations illustrate their specified models; they do not supply an adversarial robustness theorem.

## Stronger one-sample conclusion

The original special-outcome all-Hadamard decoder reaches

$$
p_{\rm ALL}^{(1)}=\frac12+\frac1{2N}
$$

over **all one-cell quantum POVMs**, for uniform preparation labels and equal parity priors. This strictly strengthens the August proof about decoding one all-H record.

If each sample independently refreshes its full secret within a fixed parity class, the averaged states commute. The joint optimum for $L$ samples is exactly

$$
1-\frac12(1-1/N)^L,
$$

already reached by the original product decoder. Refreshing those secrets is therefore not a route to an accuracy-based quantum separation. It is a different ensemble from the original same-secret task.

## Exact capability-witness frontier

Let $q$ be the total conclusive probability over all rounds. For the ideal phase-twirled pair, the optimum correct-conclusive probabilities are

$$
c_{\rm G}^{\max}(q)=\frac{q+\min(q,1/(2N))}{2},
$$

$$
c_{\rm SEP}^{\max}(q)=c_{\rm PPT}^{\max}(q)=c_{\rm LOCC}^{\max}(q)
=\frac{q+\min(q/2,1/(2N))}{2}.
$$

These are exact achieved optima, not heuristic baselines. A confidence advantage exists only at $0<q<1/N$. The largest gap is $1/4$ for every $N$; the zero-error answer rate decreases as $1/(2N)$. The DCP wrapping is not resource-minimal or a computational-hardness certificate.

The single-round factor-three bound extends to positive-partial-transpose (PPT) effects. Violation thus witnesses a negative-partial-transpose (NPT) effective conclusive effect under the trusted-input assumptions. This does not identify a gate or certify every possible entangled measurement.

## Source errors and sequential testing

- A common separable source channel independent of every hidden preparation variable preserves $c\le3w$. Local loss, dephasing, and other local channels can reduce honest performance without invalidating that null.
- For a specified, externally calibrated phase-flip source model, exact noisy confidence frontiers are proved. At any nonzero dephasing, exactly zero-error nonzero-rate discrimination is lost.
- General trace-distance source errors satisfy the conservative allowance $c-3w\le2(\epsilon_0+\epsilon_1)$. Small leakage together with selective abstention can defeat an unadjusted 75 percent confidence threshold.
- The September note proves a fixed-total-round Hoeffding test with this allowance. Source-error budgets must hold conditional on history and include side channels. Persistent-memory soundness additionally needs separable actual sources or fresh separable memory per round.
- The ideal conclusive-count binomial test is not automatically valid for general imperfect sources. Both statistical procedures require their respective predeclared stopping rules; neither permits discarded failed runs.

These are model theorems, not laboratory validation. Actual source characterization, calibration uncertainty, and physical isolation remain to be established for an experiment.

## Scope and chronology

The IBM experiment remains outside the correction scope; its original script is unchanged. The 2022 DCP challenge is an earlier DCP-specific trusted-input proposal, not a proof of the 2026 maximum-confidence theorem. The August reanalysis retains its explicit GPT-5.6 Pro acknowledgment. September's stronger statements have their own date and are also AI-assisted, with scientific responsibility remaining with Ruge Lin.

General maximum-confidence and fixed-inconclusive-rate discrimination are established prior art. See [historical context](witness/HISTORICAL_CONTEXT.md) and [references](witness/REFERENCES.md). No exhaustive novelty determination has been made.

No repository document is an APS Erratum, an independently peer-reviewed replacement, or a claim of universal computation, speedup, or device independence.
