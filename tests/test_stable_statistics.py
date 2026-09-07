"""Independent rational references for overflow, underflow, and tail boundaries."""
import math
from fractions import Fraction

import pytest

from dcp_challenge.statistics import (
    adaptive_sequential_log_lower_tail_bound,
    adaptive_sequential_lower_tail_bound,
    binomial_log_lower_tail,
    binomial_lower_tail,
)


def exact_tail(n, k, p):
    a, b = p.numerator, p.denominator
    return Fraction(sum(math.comb(n, j) * a**j * (b-a)**(n-j)
                        for j in range(k+1)), b**n)


def test_small_tails_against_exact_rationals():
    for n in range(26):
        for k in range(n+1):
            for p in (Fraction(0), Fraction(1, 8), Fraction(1, 4),
                      Fraction(1, 2), Fraction(3, 4), Fraction(7, 8), Fraction(1)):
                expected = float(exact_tail(n, k, p))
                value = binomial_lower_tail(n, k, float(p))
                assert 0 <= value <= 1
                assert math.isclose(value, expected, rel_tol=2e-13, abs_tol=0)
                log_value = binomial_log_lower_tail(n, k, float(p))
                assert log_value <= 0
                assert math.isclose(math.exp(log_value), expected, rel_tol=2e-13, abs_tol=0)


@pytest.mark.parametrize("n,k", [(1500, 300), (2000, 400), (2000, 1600)])
def test_previously_overflowing_cases(n, k):
    expected = float(exact_tail(n, k, Fraction(1, 4)))
    assert math.isclose(binomial_lower_tail(n, k), expected, rel_tol=2e-12)
    assert adaptive_sequential_lower_tail_bound(n, k) == binomial_lower_tail(n, k)


def test_positive_underflow_is_not_reported_as_zero():
    expected_log = 10000 * math.log(0.75)
    assert math.isclose(binomial_log_lower_tail(10000, 0), expected_log, rel_tol=1e-14)
    assert math.isfinite(adaptive_sequential_log_lower_tail_bound(10000, 0))
    with pytest.raises(FloatingPointError, match="log_lower_tail"):
        binomial_lower_tail(10000, 0)
    with pytest.raises(FloatingPointError):
        adaptive_sequential_lower_tail_bound(10000, 0)
    # Exact-zero endpoints remain distinguishable from numerical underflow.
    assert binomial_lower_tail(10, 0, 1.0) == 0.0
    assert binomial_log_lower_tail(10, 0, 1.0) == -math.inf


def test_monotonicity_symmetry_and_extreme_probabilities():
    for p in (1e-300, 1e-12, 0.25, 0.5, 0.9, math.nextafter(1.0, 0.0)):
        values = [binomial_log_lower_tail(200, k, p) for k in range(201)]
        assert all(a <= b + 1e-12 for a, b in zip(values, values[1:]))
    for n in (101, 501, 2001):
        assert math.isclose(binomial_lower_tail(n, n//2, 0.5), 0.5, rel_tol=2e-12)
    # Preserve a tiny but representable near-one log-CDF via the complement.
    assert math.isclose(binomial_log_lower_tail(1, 0, 1e-300), -1e-300, rel_tol=1e-14)


@pytest.mark.parametrize("n,k,p", [(-1, 0, .25), (1, -1, .25), (2, 3, .25),
    (10, 1, float("nan")), (10, 1, float("inf")), (10, 1, -.1), (10, 1, 1.1)])
def test_tail_rejects_invalid_parameters(n, k, p):
    with pytest.raises(ValueError):
        binomial_log_lower_tail(n, k, p)


@pytest.mark.parametrize("n,k", [(True, 0), (3, False), (3.5, 1), (3, 1.0)])
def test_tail_requires_integer_counts(n, k):
    with pytest.raises(TypeError):
        binomial_lower_tail(n, k)
