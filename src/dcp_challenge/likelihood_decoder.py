"""Complete classical decoding of the original all-H measurement record."""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import sqrt
from typing import Dict, Tuple

import numpy as np

from .statistics import wilson_interval


def _fwht_inplace(array: np.ndarray) -> np.ndarray:
    """In-place unnormalized fast Walsh-Hadamard transform."""
    h = 1
    while h < len(array):
        for i in range(0, len(array), 2 * h):
            left = array[i : i + h].copy()
            right = array[i + h : i + 2 * h].copy()
            array[i : i + h] = left + right
            array[i + h : i + 2 * h] = left - right
        h *= 2
    return array


def h_outcome_counts(n: int) -> np.ndarray:
    """Return integer counts ``c[s,o]`` for one all-H measurement.

    ``o = r*N + y`` with ``r`` the reflection result and ``y`` the rotation
    result.  The conditional probability is ``c[s,o] / N**2`` after averaging
    over the uniformly random preparation label ``x``.
    """
    if n < 1:
        raise ValueError("n must be at least 1")
    N = 1 << n
    x = np.arange(N, dtype=np.int64)
    counts = np.zeros((N, 2 * N), dtype=np.int64)
    for secret in range(N):
        difference = np.bitwise_xor(x, (x + secret) % N)
        histogram = np.bincount(difference, minlength=N).astype(np.int64)
        walsh = _fwht_inplace(histogram.copy())
        counts[secret, :N] = (N + walsh) // 2
        counts[secret, N:] = (N - walsh) // 2
    return counts


def explicit_two_sample_decoder_success() -> Fraction:
    """Exact success of the ``N=4`` decoder used in the correction note.

    The decoder uses exactly the original all-H product measurements:

    * if either ``y`` equals 1, output its reflection bit;
    * otherwise, if both ``y`` values are in ``{2,3}``, output ``r1 xor r2``;
    * otherwise guess uniformly.
    """
    n = 2
    N = 1 << n
    counts = h_outcome_counts(n)
    outcomes = [(r, y) for r in (0, 1) for y in range(N)]
    total = Fraction(0, 1)
    for secret in range(N):
        for r1, y1 in outcomes:
            p1 = Fraction(int(counts[secret, r1 * N + y1]), N * N)
            for r2, y2 in outcomes:
                p2 = Fraction(int(counts[secret, r2 * N + y2]), N * N)
                prediction = None
                if y1 == 1:
                    prediction = r1
                elif y2 == 1:
                    prediction = r2
                elif y1 in (2, 3) and y2 in (2, 3):
                    prediction = r1 ^ r2
                success = (
                    Fraction(1, 2)
                    if prediction is None
                    else Fraction(int(prediction == secret % 2), 1)
                )
                total += Fraction(1, N) * p1 * p2 * success
    return total


def explicit_two_sample_decoder_breakdown() -> Dict[str, Fraction]:
    """Transparent probability decomposition of the ``23/32`` to ``25/32`` gap."""
    special_event = Fraction(7, 16)  # at least one of two uniform y labels is 1
    extra_event = Fraction(1, 4)     # neither y is 1 and both are in {2,3}
    baseline = special_event + (1 - special_event) * Fraction(1, 2)
    improved = (
        special_event
        + extra_event * Fraction(3, 4)
        + (1 - special_event - extra_event) * Fraction(1, 2)
    )
    return {
        "special_event_probability": special_event,
        "extra_correlated_event_probability": extra_event,
        "extra_event_conditional_success": Fraction(3, 4),
        "published_decoder_success": baseline,
        "improved_decoder_success": improved,
        "improvement": improved - baseline,
    }


def exact_h_bayes_success(
    n: int,
    samples: int,
    max_likelihood_states: int = 2_000_000,
) -> Fraction:
    """Exact Bayes-optimal parity success for small all-H records.

    All samples share one uniformly random secret.  Outcome sequences producing
    the same secret-likelihood vector are merged, which makes the published
    Figure 5(a) instance exactly tractable.
    """
    if n < 1 or samples < 0:
        raise ValueError("require n >= 1 and samples >= 0")
    N = 1 << n
    columns = h_outcome_counts(n).T
    states: Dict[Tuple[int, ...], int] = {tuple([1] * N): 1}
    for _ in range(samples):
        updated: Dict[Tuple[int, ...], int] = {}
        for likelihood, multiplicity in states.items():
            for column in columns:
                product = tuple(int(a) * int(b) for a, b in zip(likelihood, column))
                updated[product] = updated.get(product, 0) + multiplicity
        states = updated
        if len(states) > max_likelihood_states:
            raise RuntimeError(
                "likelihood-state count exceeds max_likelihood_states; "
                "use Monte Carlo for this instance"
            )

    numerator = 0
    for likelihood, multiplicity in states.items():
        even = sum(likelihood[0::2])
        odd = sum(likelihood[1::2])
        numerator += multiplicity * max(even, odd)
    return Fraction(numerator, N * N ** (2 * samples))


def _logsumexp(array: np.ndarray, axis: int) -> np.ndarray:
    maximum = np.max(array, axis=axis, keepdims=True)
    finite = np.isfinite(maximum)
    with np.errstate(invalid="ignore", divide="ignore", over="ignore"):
        shifted = np.where(finite, array - maximum, -np.inf)
        summed = np.sum(np.exp(shifted), axis=axis, keepdims=True)
        output = maximum + np.log(summed)
    return np.squeeze(np.where(finite, output, -np.inf), axis=axis)


@dataclass(frozen=True)
class MonteCarloResult:
    successes: int
    trials: int
    estimate: float
    wilson_low: float
    wilson_high: float
    seed: int


def h_likelihood_monte_carlo(
    n: int,
    samples: int,
    trials: int,
    seed: int,
    batch_size: int = 250,
) -> MonteCarloResult:
    """Estimate optimal classical decoding of complete all-H product data."""
    if n < 1 or samples < 0 or trials <= 0 or batch_size <= 0:
        raise ValueError("invalid simulation parameter")
    N = 1 << n
    rng = np.random.default_rng(seed)
    counts = h_outcome_counts(n)
    with np.errstate(divide="ignore"):
        log_counts = np.log(counts.astype(np.float64))
    parity_lookup = np.array([value.bit_count() & 1 for value in range(N)])

    successes = 0
    for start in range(0, trials, batch_size):
        size = min(batch_size, trials - start)
        secret = rng.integers(0, N, size=size, dtype=np.int64)
        x = rng.integers(0, N, size=(size, samples), dtype=np.int64)
        y = rng.integers(0, N, size=(size, samples), dtype=np.int64)
        shifted = (x + secret[:, None]) % N
        r = parity_lookup[x & y] ^ parity_lookup[shifted & y]
        outcome = r * N + y

        log_likelihood = np.zeros((size, N), dtype=np.float64)
        for j in range(samples):
            log_likelihood += log_counts[:, outcome[:, j]].T
        even = _logsumexp(log_likelihood[:, 0::2], axis=1)
        odd = _logsumexp(log_likelihood[:, 1::2], axis=1)
        prediction = (odd > even).astype(np.int64)
        ties = odd == even
        if np.any(ties):
            prediction[ties] = rng.integers(0, 2, size=int(np.sum(ties)))
        successes += int(np.sum(prediction == (secret & 1)))

    low, high = wilson_interval(successes, trials)
    return MonteCarloResult(
        successes=successes,
        trials=trials,
        estimate=successes / trials,
        wilson_low=low,
        wilson_high=high,
        seed=seed,
    )
