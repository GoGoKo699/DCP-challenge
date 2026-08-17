"""Corrected analytical tools for the DCP challenge repository."""

from .exact_probabilities import (
    exact_honest_success,
    no_complementary_collision_probability,
    special_outcome_decoder_success,
)
from .likelihood_decoder import (
    exact_h_bayes_success,
    explicit_two_sample_decoder_success,
    h_likelihood_monte_carlo,
)

__all__ = [
    "exact_honest_success",
    "no_complementary_collision_probability",
    "special_outcome_decoder_success",
    "exact_h_bayes_success",
    "explicit_two_sample_decoder_success",
    "h_likelihood_monte_carlo",
]

__version__ = "1.0.0"
