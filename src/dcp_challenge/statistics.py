"""Statistical utilities used by the corrected analysis."""
from __future__ import annotations

from math import comb, sqrt
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


def binomial_lower_tail(
    conclusive: int,
    errors: int,
    null_error_probability: float = 0.25,
) -> float:
    """Binomial lower tail used by the adaptive sequential witness bound."""
    if conclusive < 0 or not 0 <= errors <= conclusive:
        raise ValueError("require 0 <= errors <= conclusive")
    if not 0.0 <= null_error_probability <= 1.0:
        raise ValueError("null error probability must lie in [0, 1]")
    return sum(
        comb(conclusive, j)
        * null_error_probability**j
        * (1.0 - null_error_probability) ** (conclusive - j)
        for j in range(errors + 1)
    )



def adaptive_sequential_lower_tail_bound(
    conclusive: int,
    errors: int,
    conditional_error_lower_bound: float = 0.25,
) -> float:
    """Upper bound for an adaptive sequence with conditional error at least ``p``.

    Independence is not assumed.  If every successive conclusive answer has
    conditional error probability at least ``p`` given all previous public
    history, then its error count stochastically dominates ``Binomial(C,p)``;
    hence the probability of at most ``E`` errors is bounded by this lower tail.
    """
    return binomial_lower_tail(
        conclusive,
        errors,
        null_error_probability=conditional_error_lower_bound,
    )
