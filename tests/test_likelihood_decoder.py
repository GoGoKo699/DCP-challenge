from fractions import Fraction

from dcp_challenge.likelihood_decoder import (
    exact_h_bayes_success,
    explicit_two_sample_decoder_breakdown,
    explicit_two_sample_decoder_success,
    h_outcome_counts,
)


def test_outcome_counts_normalize() -> None:
    for n in range(1, 7):
        N = 1 << n
        counts = h_outcome_counts(n)
        assert counts.shape == (N, 2 * N)
        assert (counts.sum(axis=1) == N * N).all()
        assert (counts >= 0).all()


def test_exact_counterexample() -> None:
    assert explicit_two_sample_decoder_success() == Fraction(25, 32)
    breakdown = explicit_two_sample_decoder_breakdown()
    assert breakdown["published_decoder_success"] == Fraction(23, 32)
    assert breakdown["improved_decoder_success"] == Fraction(25, 32)
    assert breakdown["improvement"] == Fraction(1, 16)


def test_exact_figure5a_optimal_all_h_decoder() -> None:
    assert exact_h_bayes_success(4, 6) == Fraction(27863673495, 34359738368)
