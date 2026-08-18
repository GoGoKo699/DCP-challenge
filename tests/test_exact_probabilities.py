from fractions import Fraction
import math

from dcp_challenge.exact_probabilities import (
    exact_honest_success,
    no_complementary_collision_probability,
    no_complementary_collision_probability_bruteforce,
    published_k_lower,
    published_k_upper,
    special_outcome_decoder_success,
)


def test_exact_collision_matches_bruteforce() -> None:
    for n in range(1, 4):
        for m in range(0, 5):
            assert no_complementary_collision_probability(n, m) == (
                no_complementary_collision_probability_bruteforce(n, m)
            )


def test_published_collision_bounds_contain_exact_value() -> None:
    for n in range(1, 7):
        for m in range(1, 12):
            exact = no_complementary_collision_probability(n, m)
            assert published_k_lower(n, m) <= exact <= published_k_upper(n, m)


def test_special_decoder_small_value() -> None:
    assert special_outcome_decoder_success(2, 2, 1) == Fraction(23, 32)


def test_corrected_figure5_honest_values() -> None:
    assert math.isclose(float(exact_honest_success(4, 6, 1)), 0.6529648303985596)
    assert math.isclose(float(exact_honest_success(6, 9, 4)), 0.8109177566941244)
    assert math.isclose(float(exact_honest_success(9, 21, 9)), 0.9048036809266576)
