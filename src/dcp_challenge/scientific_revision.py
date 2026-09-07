"""September 2026 scientific results: optimality, rate frontiers, and source error.

The formulae are proved in correction/SCIENTIFIC_REVISION_2026_09.md.
Conclusive rates and visibilities are population/model parameters, not estimates
that may be fitted to an untrusted device's observed answers. No new runtime
dependency is required. Exact probabilities use fractions.Fraction.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import math
from typing import Literal

import numpy as np

MeasurementClass = Literal["global", "separable", "ppt", "locc"]


def _natural(value: int, name: str, minimum: int = 0) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}")
    return value


def _probability(value: Fraction | int | float, name: str) -> Fraction:
    if isinstance(value, bool) or not isinstance(value, (Fraction, int, float)):
        raise ValueError(f"{name} must be a finite probability")
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError(f"{name} must be finite")
    result = Fraction(str(value)) if isinstance(value, float) else Fraction(value)
    if not 0 <= result <= 1:
        raise ValueError(f"{name} must lie in [0,1]")
    return result


def one_sample_global_success(n: int) -> Fraction:
    """Helstrom optimum over ALL one-cell POVMs for uniform secret parity."""
    _natural(n, "n", 1)
    return Fraction(1, 2) + Fraction(1, 2 * (1 << n))


def refreshed_secret_global_success(n: int, samples: int) -> Fraction:
    """Joint-measurement optimum when ONLY the parity is shared.

    Each sample has independent uniform x and independent uniform s within a
    common parity class. This is NOT the original fixed-secret experiment.
    The commuting averaged states make product all-H measurements optimal.
    """
    _natural(n, "n", 1)
    _natural(samples, "samples")
    N = 1 << n
    return 1 - Fraction(1, 2) * Fraction(N - 1, N) ** samples


@dataclass(frozen=True)
class FrontierPoint:
    conclusive: Fraction
    correct: Fraction
    wrong: Fraction
    confidence: Fraction


def confidence_frontier(
    n: int,
    conclusive_rate: Fraction | int | float,
    measurement: MeasurementClass = "global",
    visibility: Fraction | int | float = Fraction(1),
) -> FrontierPoint:
    """Exact fixed-total-conclusive-rate optimum for the stated phase model.

    visibility v means a hidden, parity-independent random Z on the SECOND
    reflection qubit with probability (1-v)/2, BEFORE the untrusted device.
    A known local phase may first be compensated. This is not general noise.
    SEP, PPT, and LOCC frontiers coincide for this particular ensemble only.
    """
    _natural(n, "n", 1)
    q = _probability(conclusive_rate, "conclusive_rate")
    v = _probability(visibility, "visibility")
    if q == 0:
        raise ValueError("confidence is undefined at zero conclusive rate")
    if measurement not in ("global", "separable", "ppt", "locc"):
        raise ValueError("unknown measurement class")
    a = Fraction(1, 2 * (1 << n))
    advantage = v * min(q if measurement == "global" else q / 2, a)
    correct, wrong = (q + advantage) / 2, (q - advantage) / 2
    return FrontierPoint(q, correct, wrong, correct / q)


def source_score_allowance(epsilon_even: Fraction | int | float,
                           epsilon_odd: Fraction | int | float) -> Fraction:
    """Upper shift of E[+1 correct,-3 wrong,0 abstain] from source trace errors.

    D(rho_b_actual,rho_b_ideal) <= epsilon_b must hold on the COMPLETE input
    accessible to the prover, including side channels and, sequentially, after
    each history. D denotes half of the trace norm. Calibration is external.
    """
    e0 = _probability(epsilon_even, "epsilon_even")
    e1 = _probability(epsilon_odd, "epsilon_odd")
    return 2 * (e0 + e1)


def robust_separable_confidence_bound(
    conclusive_rate: Fraction | int | float,
    epsilon_even: Fraction | int | float,
    epsilon_odd: Fraction | int | float,
) -> Fraction:
    """Conservative, NOT generally tight, source-error-dependent SEP ceiling."""
    q = _probability(conclusive_rate, "conclusive_rate")
    if q == 0:
        raise ValueError("confidence is undefined at zero conclusive rate")
    beta = source_score_allowance(epsilon_even, epsilon_odd)
    return min(Fraction(1), Fraction(3, 4) + beta / (4 * q))


def fixed_round_source_error_log_bound(
    correct: int, wrong: int, inconclusive: int,
    epsilon_even: Fraction | int | float = Fraction(0),
    epsilon_odd: Fraction | int | float = Fraction(0),
) -> float:
    """Log of a Hoeffding false-certification upper bound at a FIXED horizon.

    All rounds, including loss/abstention, must be counted. The horizon and
    source-error budgets are fixed before observing results. Adaptive LOCC or
    separable instruments with separable initial memory are allowed. The actual
    sources must also be separable and the error budgets must hold conditional
    on history; alternatively enforce fresh separable memory every round.
    Returns 0 (bound 1) if the observed score does not exceed the null allowance.
    This floating-point evaluation is not an interval-arithmetic certificate.
    """
    for value, name in ((correct, "correct"), (wrong, "wrong"),
                        (inconclusive, "inconclusive")):
        _natural(value, name)
    rounds = correct + wrong + inconclusive
    if rounds == 0:
        raise ValueError("at least one completed round is required")
    gap = Fraction(correct - 3 * wrong, rounds) - source_score_allowance(
        epsilon_even, epsilon_odd)
    return 0.0 if gap <= 0 else -float(rounds * gap * gap / 8)


def _embed_block(target: np.ndarray, block: np.ndarray, N: int,
                 k: int, ell: int) -> None:
    indices = [(r1*N+k)*(2*N)+(r2*N+ell) for r1 in range(2) for r2 in range(2)]
    target[np.ix_(indices, indices)] = block


def fourier_pair_states(n: int, visibility: float = 1.0) -> tuple[np.ndarray, np.ndarray]:
    """Closed-form FULL two-cell states; dense reference only, n <= 3.

    Ordering is reflection A, Fourier-label A, reflection B, Fourier-label B.
    Unlike postselecting reported labels, this includes every label block.
    """
    _natural(n, "n", 1)
    if n > 3:
        raise ValueError("dense reference is restricted to n <= 3")
    v = float(_probability(visibility, "visibility"))
    N = 1 << n
    K = np.zeros((4, 4)); K[1, 2] = K[2, 1] = 1
    pair = []
    for b in range(2):
        rho = np.zeros((4*N*N, 4*N*N), dtype=np.complex128)
        for k in range(N):
            for ell in range(N):
                d = (ell-k) % N
                coefficient = 1 if d == 0 else ((-1)**b if d == N//2 else 0)
                _embed_block(rho, (np.eye(4)+v*coefficient*K)/(4*N*N), N, k, ell)
        pair.append(rho)
    return pair[0], pair[1]


def optimal_frontier_povm(n: int, conclusive_rate: Fraction | int | float,
                          measurement: MeasurementClass = "global") -> tuple[np.ndarray, ...]:
    """Explicit full POVM attaining the frontier for ALL visibilities in [0,1].

    SEP candidates are implementable by local Fourier labels, local X
    measurements, and classical randomization. No entangled resource is used.
    """
    point = confidence_frontier(n, conclusive_rate, measurement)
    if n > 3:
        raise ValueError("dense reference is restricted to n <= 3")
    N, q = 1 << n, float(point.conclusive)
    X = np.array([[0., 1.], [1., 0.]])
    psi_plus = np.array([0., 1., 1., 0.]) / np.sqrt(2)
    psi_minus = np.array([0., 1., -1., 0.]) / np.sqrt(2)
    if measurement == "global":
        blocks = [np.outer(psi_plus, psi_plus), np.outer(psi_minus, psi_minus)]
        q0 = 1 / (2*N)
    else:
        blocks = [(np.eye(4)+np.kron(X, X))/2, (np.eye(4)-np.kron(X, X))/2]
        q0 = 1 / N
    E0 = np.zeros((4*N*N, 4*N*N), dtype=np.complex128)
    E1 = np.zeros_like(E0)
    for k in range(N):
        _embed_block(E0, blocks[0], N, k, (k+N//2) % N)
        _embed_block(E1, blocks[1], N, k, (k+N//2) % N)
    identity = np.eye(4*N*N)
    if q <= q0:
        E0 *= q/q0; E1 *= q/q0
    else:
        common = (q-q0)/(1-q0) * (identity-E0-E1) / 2
        E0 += common; E1 += common
    return E0, E1, identity-E0-E1


def revision_reference_results() -> dict:
    """Exact derived examples; does not read stored outputs or audit files."""
    def record(f: Fraction) -> dict:
        return {"numerator": f.numerator, "denominator": f.denominator, "decimal": float(f)}
    frontiers = []
    for n in (1, 2, 4):
        N = 1 << n
        for q in (Fraction(1, 4*N), Fraction(1, 2*N), Fraction(3, 4*N),
                  Fraction(1, N), Fraction(1)):
            for v in (Fraction(1), Fraction(3, 5)):
                g = confidence_frontier(n, q, "global", v)
                s = confidence_frontier(n, q, "separable", v)
                frontiers.append({"n": n, "visibility": record(v), "conclusive_rate": record(q),
                    "global_correct": record(g.correct), "global_wrong": record(g.wrong),
                    "global_confidence": record(g.confidence), "separable_confidence": record(s.confidence),
                    "separable_correct": record(s.correct), "separable_wrong": record(s.wrong)})
    return {"revision_date": "2026-09-07", "status": "author-derived analytical results; not peer reviewed",
            "global_single_sample": [{"n": n, "success": record(one_sample_global_success(n))} for n in range(1, 8)],
            "independently_refreshed_secrets": [{"n": n, "samples": L, "joint_optimum": record(refreshed_secret_global_success(n,L))}
                for n,L in ((1,2),(2,2),(3,4),(4,6))],
            "exact_frontiers": frontiers,
            "source_error_example": {"epsilon_each": record(Fraction(1,100)),
                "null_score_allowance": record(source_score_allowance(Fraction(1,100),Fraction(1,100))),
                "fixed_round_counts": {"correct": 2500, "wrong": 0, "inconclusive": 7500},
                "log_false_certification_bound": fixed_round_source_error_log_bound(2500,0,7500,Fraction(1,100),Fraction(1,100))}}
