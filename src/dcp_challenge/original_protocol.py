"""Small exact checks for the retained ParitySolve algebra."""
from __future__ import annotations

import cmath


def is_complementary(k1: int, k2: int, n: int) -> bool:
    """Return whether two Fourier labels differ by ``N/2`` modulo ``N``."""
    if n < 1:
        raise ValueError("n must be at least 1")
    N = 1 << n
    if not (0 <= k1 < N and 0 <= k2 < N):
        raise ValueError("labels must lie in Z_N")
    return (k1 - k2) % N == N // 2


def selected_branch_relative_phase(k1: int, k2: int, secret: int, n: int) -> complex:
    """Relative phase after the selected two-sample interference branch."""
    if n < 1:
        raise ValueError("n must be at least 1")
    N = 1 << n
    if not (0 <= secret < N):
        raise ValueError("secret must lie in Z_N")
    return cmath.exp(2j * cmath.pi * ((k1 - k2) % N) * secret / N)


def selected_branch_returns_parity(k1: int, k2: int, secret: int, n: int) -> bool:
    """Check the retained identity ``phase = (-1)**secret`` on a collision."""
    if not is_complementary(k1, k2, n):
        return False
    phase = selected_branch_relative_phase(k1, k2, secret, n)
    target = -1.0 if secret % 2 else 1.0
    return abs(phase - target) < 1e-12
