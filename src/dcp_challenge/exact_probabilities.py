"""Exact probability formulas for the original 2022 DCP workload.

The functions in this module are independent of the legacy Qibo scripts.  All
combinatorial quantities are returned as :class:`fractions.Fraction` objects so
that the decisive small-instance checks are exact rather than floating-point
comparisons.
"""
from __future__ import annotations

from fractions import Fraction
from itertools import product
from math import comb, factorial


def _validate_parameters(n: int, m: int) -> None:
    if n < 1:
        raise ValueError("n must be at least 1")
    if m < 0:
        raise ValueError("m must be nonnegative")


def stirling_second(n: int, k: int) -> int:
    """Return the Stirling number of the second kind ``S(n, k)``."""
    if n < 0 or k < 0:
        raise ValueError("n and k must be nonnegative")
    if n == 0:
        return int(k == 0)
    if k == 0 or k > n:
        return 0

    row = [0] * (k + 1)
    row[0] = 1
    for i in range(1, n + 1):
        nxt = [0] * (k + 1)
        for j in range(1, min(i, k) + 1):
            nxt[j] = row[j - 1] + j * row[j]
        row = nxt
    return row[k]


def no_complementary_collision_probability(n: int, m: int) -> Fraction:
    """Exact probability that ``m`` labels contain no complementary pair.

    Labels are uniform in ``Z_N`` with ``N = 2**n``.  A complementary pair is
    a pair whose difference is ``N/2`` modulo ``N``.

    A collision-free sequence using exactly ``j`` complementary pairs is
    counted by

    ``C(N/2,j) * 2**j * j! * S(m,j)``.
    """
    _validate_parameters(n, m)
    if m == 0:
        return Fraction(1, 1)

    N = 1 << n
    favourable = 0
    for j in range(1, min(m, N // 2) + 1):
        favourable += (
            comb(N // 2, j)
            * (2**j)
            * factorial(j)
            * stirling_second(m, j)
        )
    return Fraction(favourable, N**m)


def no_complementary_collision_probability_bruteforce(n: int, m: int) -> Fraction:
    """Reference enumeration for small instances."""
    _validate_parameters(n, m)
    N = 1 << n
    favourable = 0
    for labels in product(range(N), repeat=m):
        collision = any(
            (labels[i] - labels[j]) % N == N // 2
            for i in range(m)
            for j in range(i + 1, m)
        )
        favourable += int(not collision)
    return Fraction(favourable, N**m)


def exact_honest_success(n: int, m: int, t: int) -> Fraction:
    """Exact ideal success of the retry rule implemented in the 2022 code."""
    _validate_parameters(n, m)
    if t < 0:
        raise ValueError("t must be nonnegative")
    k_nc = no_complementary_collision_probability(n, m)
    return Fraction(1, 1) - Fraction(1, 2) * ((1 + k_nc) / 2) ** t


def published_k_lower(n: int, m: int) -> Fraction:
    """The lower no-collision bound used in the original repository."""
    _validate_parameters(n, m)
    N = 1 << n
    value = Fraction(1, 1)
    for i in range(m):
        value *= Fraction(max(N - i, 0), N)
    return value


def published_k_upper(n: int, m: int) -> Fraction:
    """The upper no-collision bound used in the original repository."""
    _validate_parameters(n, m)
    half = 1 << (n - 1)
    value = Fraction(1, 1)
    for i in range(m):
        value *= Fraction(max(half - i, 0), half)
    return Fraction(1, 2) + Fraction(1, 2) * value


def published_p_upper(n: int, m: int, t: int) -> Fraction:
    """The published upper bound on honest success."""
    return Fraction(1, 1) - Fraction(1, 2) * ((1 + published_k_lower(n, m)) / 2) ** t


def published_p_lower(n: int, m: int, t: int) -> Fraction:
    """The published lower bound on honest success."""
    return Fraction(1, 1) - Fraction(1, 2) * ((1 + published_k_upper(n, m)) / 2) ** t


def special_outcome_decoder_success(n: int, m: int, t: int) -> Fraction:
    """Success of the *specified* all-H special-outcome decoder.

    This is the quantity denoted ``p_B`` in the 2022 article and code.  The
    name here is deliberately descriptive: it is not an upper bound over all
    product-measurement or classically postprocessed strategies.
    """
    _validate_parameters(n, m)
    if t < 0:
        raise ValueError("t must be nonnegative")
    N = 1 << n
    samples = m * t
    return Fraction(1, 1) - Fraction(1, 2) * Fraction((N - 1) ** samples, N**samples)
