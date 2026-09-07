"""Statistical utilities used by the corrected analysis."""
from __future__ import annotations

from math import comb, exp, expm1, fsum, isfinite, log, log1p, sqrt
from operator import index
from typing import Tuple


def bernoulli_standard_error(p: float, repetitions: int) -> float:
    """Standard error of an empirical correct/incorrect success fraction."""
    if not 0.0 <= p <= 1.0:
        raise ValueError("p must lie in [0, 1]")
    if repetitions <= 0:
        raise ValueError("repetitions must be positive")
    return sqrt(p * (1.0 - p) / repetitions)


def legacy_standard_error(p: float, repetitions: int) -> float:
    """Formula printed by the original scripts, retained only for comparison."""
    if not 0.0 <= p <= 1.0:
        raise ValueError("p must lie in [0, 1]")
    if repetitions <= 0:
        raise ValueError("repetitions must be positive")
    return sqrt((1.0 - p) / (2.0 * repetitions))


def wilson_interval(
    successes: int,
    trials: int,
    z: float = 1.959963984540054,
) -> Tuple[float, float]:
    """Two-sided Wilson score interval; default confidence is approximately 95%."""
    if trials <= 0:
        raise ValueError("trials must be positive")
    if not 0 <= successes <= trials:
        raise ValueError("successes must lie between 0 and trials")
    p = successes / trials
    denominator = 1.0 + z * z / trials
    center = (p + z * z / (2.0 * trials)) / denominator
    radius = (
        z
        * sqrt((p * (1.0 - p) + z * z / (4.0 * trials)) / trials)
        / denominator
    )
    return center - radius, center + radius


def _tail_parameters(conclusive: int, errors: int, probability: float) -> tuple[int, int, float]:
    """Reject fractional counts, booleans, NaNs, and out-of-domain inputs."""
    if isinstance(conclusive, bool) or isinstance(errors, bool):
        raise TypeError("counts must be integers, not booleans")
    try:
        n, k = index(conclusive), index(errors)
    except TypeError as exc:
        raise TypeError("counts must be integers") from exc
    if n < 0 or not 0 <= k <= n:
        raise ValueError("require 0 <= errors <= conclusive")
    p = float(probability)
    if not isfinite(p) or not 0.0 <= p <= 1.0:
        raise ValueError("null error probability must be finite and lie in [0, 1]")
    return n, k, p


def _log_left_tail(n: int, k: int, log_p: float, log_q: float) -> float:
    """Log of a lower tail below the mean, scaled by its largest term.

    ``comb`` remains a Python integer: only its logarithm is converted to a
    float. The downward PMF ratios are at most one. Summation therefore cannot
    overflow or lose the entire tail when the unscaled probability underflows.
    """
    def scaled_terms():
        term = 1.0
        yield term
        for j in range(k, 0, -1):
            term *= exp(fsum((log(j), -log(n - j + 1), log_q, -log_p)))
            if term == 0.0:
                break
            yield term

    log_mass = fsum((log(comb(n, k)), k * log_p, (n - k) * log_q))
    return min(0.0, fsum((log_mass, log(fsum(scaled_terms())))))


def binomial_log_lower_tail(
    conclusive: int,
    errors: int,
    null_error_probability: float = 0.25,
) -> float:
    """Natural logarithm of ``P[Binomial(C,p) <= E]``.

    Uses a scaled PMF recurrence, or the reflected upper tail when above the
    mean. No SciPy dependency is needed. Exact-zero endpoint probabilities
    return ``-inf``; positive tails remain finite even below float range.
    These are floating-point evaluations, not interval-arithmetic certificates.
    Work and integer storage increase with the experiment size.
    """
    n, k, p = _tail_parameters(conclusive, errors, null_error_probability)
    if k == n or p == 0.0:
        return 0.0
    if p == 1.0:
        return -float("inf")
    log_p, log_q = log(p), log1p(-p)
    if k < n * p:
        return _log_left_tail(n, k, log_p, log_q)
    # P[X > k] = P[Binomial(n,1-p) <= n-k-1]. Swap logs rather than
    # forming 1-p again, which could round to one for very small p.
    log_upper = _log_left_tail(n, n - k - 1, log_q, log_p)
    if log_upper < -log(2.0):
        return log1p(-exp(log_upper))
    return log(-expm1(log_upper))


def binomial_lower_tail(
    conclusive: int,
    errors: int,
    null_error_probability: float = 0.25,
) -> float:
    """Binomial lower tail, with explicit protection against false zeros.

    If a positive probability would underflow to zero, raise
    ``FloatingPointError`` and direct the caller to the log-probability API.
    A returned zero is reserved for a mathematically impossible endpoint.
    """
    log_probability = binomial_log_lower_tail(conclusive, errors, null_error_probability)
    probability = exp(log_probability)
    if probability == 0.0 and isfinite(log_probability):
        raise FloatingPointError(
            "positive tail is below floating-point range; use binomial_log_lower_tail"
        )
    return probability


def adaptive_sequential_lower_tail_bound(
    conclusive: int,
    errors: int,
    conditional_error_lower_bound: float = 0.25,
) -> float:
    """Evaluate the adaptive bound under the sequential null in witness/PROOF.md.

    This evaluates the analytical binomial bound; it does not test the physical
    assumptions or an arbitrary stopping/restarting rule. See the protocol's
    predeclared (C,E,R) rule. Positive underflow raises FloatingPointError.
    """
    return binomial_lower_tail(conclusive, errors, conditional_error_lower_bound)


def adaptive_sequential_log_lower_tail_bound(
    conclusive: int,
    errors: int,
    conditional_error_lower_bound: float = 0.25,
) -> float:
    """Natural-log version of the same analytical adaptive bound."""
    return binomial_log_lower_tail(conclusive, errors, conditional_error_lower_bound)
