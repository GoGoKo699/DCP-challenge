"""Ideal-model analysis of the phase-twirled heralded DCP witness.

This module implements exact density-matrix checks for small ``N`` and the
statistics of the narrow claim documented in ``witness/``: certification of a
nonseparable joint measurement across two trusted DCP input cells against POVMs
whose effects are separable across that partition.
"""
from __future__ import annotations

from math import sqrt
from typing import Dict, Tuple

import numpy as np

from .statistics import adaptive_sequential_lower_tail_bound


def _projector(vector: np.ndarray) -> np.ndarray:
    return np.outer(vector, vector.conj())


def collision_states() -> Tuple[np.ndarray, np.ndarray]:
    """Return the parity-conditioned two-reflection-qubit collision states."""
    zero = np.array([1.0, 0.0], dtype=np.complex128)
    one = np.array([0.0, 1.0], dtype=np.complex128)
    psi_plus = (np.kron(zero, one) + np.kron(one, zero)) / sqrt(2.0)
    psi_minus = (np.kron(zero, one) - np.kron(one, zero)) / sqrt(2.0)
    sigma_even = (
        0.25 * _projector(np.kron(zero, zero))
        + 0.50 * _projector(psi_plus)
        + 0.25 * _projector(np.kron(one, one))
    )
    sigma_odd = (
        0.25 * _projector(np.kron(zero, zero))
        + 0.50 * _projector(psi_minus)
        + 0.25 * _projector(np.kron(one, one))
    )
    return sigma_even, sigma_odd


def witness_summary(n: int) -> Dict[str, float]:
    if n < 1:
        raise ValueError("n must be at least 1")
    N = 1 << n
    return {
        "N": N,
        "honest_correct_conclusive": 1.0 / (2.0 * N),
        "honest_wrong_conclusive": 0.0,
        "honest_linear_score": 1.0 / (2.0 * N),
        "separable_conditional_error_lower_bound": 0.25,
        "separable_confidence_upper_bound": 0.75,
        "forced_guess_optimal_success_both_joint_and_separable": 0.5 + 1.0 / (4.0 * N),
    }


def separable_saturation_probabilities() -> Tuple[float, float]:
    """Probabilities of the product effect ``|++><++|`` on the two states."""
    sigma_even, sigma_odd = collision_states()
    plus = np.array([1.0, 1.0], dtype=np.complex128) / sqrt(2.0)
    vector = np.kron(plus, plus)
    p_even = float(np.real(vector.conj() @ sigma_even @ vector))
    p_odd = float(np.real(vector.conj() @ sigma_odd @ vector))
    return p_even, p_odd


def full_state_fourier(n: int, parity: int) -> np.ndarray:
    """Dense two-cell ensemble in the local Fourier-label basis.

    Intended only for independent small-system checks.
    """
    if n < 1 or parity not in (0, 1):
        raise ValueError("require n >= 1 and parity in {0,1}")
    N = 1 << n
    cell_dim = 2 * N
    zero = np.array([1.0, 0.0], dtype=np.complex128)
    one = np.array([0.0, 1.0], dtype=np.complex128)
    labels = np.eye(N, dtype=np.complex128)
    rho = np.zeros((cell_dim * cell_dim, cell_dim * cell_dim), dtype=np.complex128)
    secrets = list(range(parity, N, 2))
    phases = (0.0, np.pi / 2.0, np.pi, 3.0 * np.pi / 2.0)

    for secret in secrets:
        for alpha in phases:
            local = []
            for k in range(N):
                reflection = (
                    zero
                    + np.exp(1j * (alpha + 2.0 * np.pi * k * secret / N)) * one
                ) / sqrt(2.0)
                local.append(np.kron(reflection, labels[:, k]))
            for k in range(N):
                for ell in range(N):
                    rho += _projector(np.kron(local[k], local[ell]))
    rho /= len(secrets) * len(phases) * N * N
    return rho


def _partial_trace_second(rho: np.ndarray, first_dim: int, second_dim: int) -> np.ndarray:
    reshaped = rho.reshape(first_dim, second_dim, first_dim, second_dim)
    return np.trace(reshaped, axis1=1, axis2=3)


def full_state_checks(n: int) -> Dict[str, float]:
    """Check normalization, local privacy, trace distance, and Helstrom value."""
    N = 1 << n
    cell_dim = 2 * N
    rho_even = full_state_fourier(n, 0)
    rho_odd = full_state_fourier(n, 1)
    marginal_even = _partial_trace_second(rho_even, cell_dim, cell_dim)
    marginal_odd = _partial_trace_second(rho_odd, cell_dim, cell_dim)
    trace_norm = float(np.sum(np.linalg.svd(rho_even - rho_odd, compute_uv=False)))
    maximally_mixed = np.eye(cell_dim) / cell_dim
    return {
        "trace_even": float(np.real(np.trace(rho_even))),
        "trace_odd": float(np.real(np.trace(rho_odd))),
        "local_marginal_max_error_from_maximally_mixed": float(
            max(
                np.max(np.abs(marginal_even - maximally_mixed)),
                np.max(np.abs(marginal_odd - maximally_mixed)),
            )
        ),
        "trace_norm_difference": trace_norm,
        "expected_trace_norm_difference": 1.0 / N,
        "forced_guess_helstrom_success": 0.5 + trace_norm / 4.0,
    }


def random_product_ratio_stress(
    samples: int = 10_000,
    seed: int = 0,
) -> Dict[str, float]:
    """Numerically stress-test the tight product-effect likelihood ratio 3."""
    if samples <= 0:
        raise ValueError("samples must be positive")
    sigma_even, sigma_odd = collision_states()
    rng = np.random.default_rng(seed)
    maximum = 0.0
    minimum = float("inf")
    worst_margin = float("inf")
    for _ in range(samples):
        a = rng.normal(size=2) + 1j * rng.normal(size=2)
        c = rng.normal(size=2) + 1j * rng.normal(size=2)
        a /= np.linalg.norm(a)
        c /= np.linalg.norm(c)
        vector = np.kron(a, c)
        p_even = float(np.real(vector.conj() @ sigma_even @ vector))
        p_odd = float(np.real(vector.conj() @ sigma_odd @ vector))
        if p_odd > 0.0:
            ratio = p_even / p_odd
            maximum = max(maximum, ratio)
            minimum = min(minimum, ratio)
        worst_margin = min(
            worst_margin,
            3.0 * p_odd - p_even,
            3.0 * p_even - p_odd,
        )
    return {
        "samples": samples,
        "seed": seed,
        "max_ratio_observed": maximum,
        "min_ratio_observed": minimum,
        "minimum_inequality_margin": worst_margin,
    }


def finite_sample_examples() -> Dict[str, float]:
    return {
        "zero_errors_among_50": adaptive_sequential_lower_tail_bound(50, 0),
        "at_most_20_errors_among_200": adaptive_sequential_lower_tail_bound(200, 20),
    }


def minimal_four_qubit_resources() -> Dict[str, int]:
    """Maximum ideal gate counts for the ``N=2`` static implementation."""
    return {
        "qubits": 4,
        "ancillas": 0,
        "preparation_cnots_max": 2,
        "bell_measurement_cnots": 1,
        "total_cnots_max": 3,
        "non_clifford_gates": 0,
        "mid_circuit_measurements": 0,
        "dynamic_feed_forward": 0,
    }
