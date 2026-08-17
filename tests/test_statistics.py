import math

from dcp_challenge.statistics import (
    bernoulli_standard_error,
    binomial_lower_tail,
    legacy_standard_error,
    wilson_interval,
)


def test_bernoulli_standard_error() -> None:
    p = 0.8
    assert math.isclose(
        bernoulli_standard_error(p, 1000),
        math.sqrt(0.8 * 0.2 / 1000),
    )
    assert legacy_standard_error(p, 1000) < bernoulli_standard_error(p, 1000)


def test_wilson_interval_contains_observed_fraction() -> None:
    low, high = wilson_interval(80, 100)
    assert low < 0.8 < high


def test_witness_binomial_examples() -> None:
    assert math.isclose(binomial_lower_tail(50, 0), (3.0 / 4.0) ** 50)
    assert math.isclose(
        binomial_lower_tail(200, 20),
        7.032272895493487e-08,
        rel_tol=1e-12,
    )
