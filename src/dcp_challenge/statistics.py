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
    """Probability of at most ``errors`` under a binomial null model."""
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
