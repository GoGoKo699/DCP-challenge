# Scientific Release Review

**7 September 2026 | Reviewed science: v1.2.0 | Consolidated release: v1.2.1**

This is an author/AI-assisted adversarial audit, not independent peer review. The reviewed baseline is commit `0508d0697a3c12183149eed354281b085ee85c90`, tree `bceb165d695686593425c2a87605705e71aa2311`. A fresh extraction of the supplied source archive produced exactly that Git tree before any edits.

## Disposition

No theorem, numerical result, or scientific null threshold requires alteration. The release consolidates the existing conclusions and adds independent checks. Source calibration, side channels, memory separation, and stopping rules remain material assumptions, not verified experimental properties.

| Claim | Disposition | Proof in current technical note | Adversarial check |
|---|---|---|---|
| Shared-secret threshold fails | Retained | Sections 2.2 and 3 | Exact 23/32 versus 25/32 regression |
| Exact ParitySolve probability | Retained for the declared retry policy | Section 3.1 | Exhaustive occupancy enumeration |
| Bernoulli uncertainty | Retained for independent original repetitions | Section 3.3 | Exact variance identity and regression |
| Unrestricted one-cell optimum | Retained under uniform-secret priors and no side information | Section 4.1 | Raw-state spectral discrimination, not a forced Fourier measurement |
| Refreshed-secret limitation | Retained only for independently refreshed full secrets within a fixed parity | Section 4.2 | Raw tensor powers and unrestricted binary optimum |
| Exact global and restricted rate frontiers | Retained; total answer rate, not selected-outcome rate | Section 6 | Full-space upper certificates, complete attaining POVMs, and 96 independent LPs |
| PPT strengthening | Retained for single-round effects; no new sequential PPT-instrument claim | Section 6 | Both decomposable operator identities in computational coordinates |
| Ideal sequential soundness | Retained under product-Kraus instruments and conditional separable memory | Section 7 | Finite-horizon supermartingale and exact optimization over adaptive abstention |
| Common separable source noise | Retained with hidden-label independence and all flags included | Section 8.1 | Adjoint-map proof and local-channel tests |
| Arbitrarily small leakage | Retained counterexample to a uniform low-rate confidence ceiling | Section 8.2 | Locally readable orthogonal-flag construction |
| General source-error allowance | Retained as conservative, externally calibrated, and conditional | Sections 8.3-8.4 | Spectral-range proof and conditional moment-bound vertex checks |
| Novelty and chronology | Narrowed claims already appropriate; no new priority claim | Section 11 | Primary-source dates and the distinction between per-outcome and total rates |

## Checks performed

The baseline passed all 98 tests, all 71 manifest entries, all six historical Git blob checks, and all six scientific records (1,268 fields). Its separate raw-preparation linear-program audit passed 96 global/PPT cases, with maximum observed absolute objective difference `1.39e-16`.

The added `scripts/audit_release_science.py` imports no `dcp_challenge` functions. It checks:

- 30 complete-space PPT decompositions for N=2,4,8 and five phase visibilities, in both likelihood-ratio directions;
- 9 raw one-cell/tensor-power Helstrom optima;
- 360 exact finite-horizon adaptive-stopping problems, including incomplete-run cutoffs;
- 144 conditional Hoeffding moment-bound vertex cases.

The largest observed matrix identity residual was below `9e-17`; the smallest nominally nonnegative eigenvalue was above `-9e-17`. These are floating-point diagnostics, not interval-arithmetic proofs. The stopping computations use exact rational arithmetic.

Unlike the earlier optimization audit, the new complete-space operator check does not assume that the receiver's effects are Bell-diagonal or Fourier-block diagonal. It evaluates certificates that apply to arbitrary full-cell PPT effects. No claim is made that a general-purpose unrestricted SDP was independently solved.

## Statistical and operational qualifications

The finite-horizon proof bounds the probability of accepting one predeclared run. It is not a probability conditional on having completed or reported a run. Correctness indicators belong to the proof filtration even when hidden from the receiver. Ideal inputs remain separable after conditioning on the full preparation record.

For faulty sources with persistent memory, a sufficient condition is conditional separation of the fresh input from retained receiver memory, separable actual input pairs, and calibrated trace-distance budgets after each history. Average input closeness alone does not supply this. Resetting receiver memory is an alternative only together with the requisite source assumptions. Calibration uncertainty is not silently absorbed into the displayed score exponent.

The original maximum-confidence principle, fixed-inconclusive-rate framework, PPT techniques, and concentration methods are not claimed as new. The Lee-Bae paper's per-outcome rates are not interchanged with the DCP total answer rate.

## Documentation and archival result

`docs/CURRENT_TECHNICAL_NOTE.md` is the unified exposition. Its PDF and standalone TeX are built with `python scripts/build_current_note.py` and attached to the release. The local 13-page PDF was rendered and visually inspected; the build also rejects missing-character, undefined-command, and overfull-box diagnostics. Automated builds cannot replace visual review of changed layouts.

The six 2022 scripts, dated August correction Markdown/TeX/PDF, September scientific note, six scientific result records, and August GPT-5.6 Pro acknowledgment are preserved unchanged. A later review is not attributed retroactively to the original article. Ruge Lin retains responsibility.

## Completion boundary

The declarations, proofs, source-code outputs, and adversarial checks agree for this release. Archive this state rather than continually expanding the correction. Reopen it only for a reproducible new discrepancy or a clearly separated research question. No hardware experiment or source calibration is part of this release.
