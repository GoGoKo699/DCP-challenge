"""Dependency-light statevector model of the minimal four-qubit witness circuit."""
from __future__ import annotations

from typing import Dict

import numpy as np

H = np.array([[1.0, 1.0], [1.0, -1.0]], dtype=np.complex128) / np.sqrt(2.0)
S = np.array([[1.0, 0.0], [0.0, 1j]], dtype=np.complex128)
X = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=np.complex128)


def _apply_single(state: np.ndarray, gate: np.ndarray, qubit: int, nqubits: int) -> np.ndarray:
    tensor = state.reshape([2] * nqubits)
    tensor = np.moveaxis(tensor, qubit, 0)
    tensor = np.tensordot(gate, tensor, axes=([1], [0]))
    tensor = np.moveaxis(tensor, 0, qubit)
    return tensor.reshape(-1)


def _apply_cnot(state: np.ndarray, control: int, target: int, nqubits: int) -> np.ndarray:
    output = np.zeros_like(state)
    for index, amplitude in enumerate(state):
        bits = [(index >> (nqubits - 1 - q)) & 1 for q in range(nqubits)]
        if bits[control]:
            bits[target] ^= 1
        new_index = 0
        for bit in bits:
            new_index = (new_index << 1) | bit
        output[new_index] += amplitude
    return output


def circuit_probabilities(secret: int, x1: int, x2: int, phase_index: int) -> np.ndarray:
    """Return final probabilities in qubit order ``r1,q1,r2,q2``.

    ``phase_index`` selects the shared phase ``alpha = phase_index*pi/2``.
    All measurements are deferred to the end.
    """
    if secret not in (0, 1) or x1 not in (0, 1) or x2 not in (0, 1):
        raise ValueError("secret and x values must be bits")
    if phase_index not in (0, 1, 2, 3):
        raise ValueError("phase_index must be 0, 1, 2, or 3")

    nqubits = 4
    bits = [0, x1, 0, x2]
    index = 0
    for bit in bits:
        index = (index << 1) | bit
    state = np.zeros(2**nqubits, dtype=np.complex128)
    state[index] = 1.0

    # Trusted preparation of the two DCP cells.
    state = _apply_single(state, H, 0, nqubits)
    state = _apply_single(state, H, 2, nqubits)
    phase_gate = np.linalg.matrix_power(S, phase_index)
    state = _apply_single(state, phase_gate, 0, nqubits)
    state = _apply_single(state, phase_gate, 2, nqubits)
    if secret:
        state = _apply_cnot(state, 0, 1, nqubits)
        state = _apply_cnot(state, 2, 3, nqubits)

    # Local N=2 Fourier transforms on the rotation qubits.
    state = _apply_single(state, H, 1, nqubits)
    state = _apply_single(state, H, 3, nqubits)

    # Bell-basis measurement transform on the reflection qubits.
    state = _apply_cnot(state, 0, 2, nqubits)
    state = _apply_single(state, H, 0, nqubits)
    return np.abs(state) ** 2


def decoded_statistics() -> Dict[str, float]:
    """Average the complete circuit over all trusted preparation randomness."""
    correct = 0.0
    wrong = 0.0
    inconclusive = 0.0
    weight = 1.0 / (2 * 2 * 2 * 4)
    for secret in (0, 1):
        for x1 in (0, 1):
            for x2 in (0, 1):
                for phase_index in (0, 1, 2, 3):
                    probabilities = circuit_probabilities(secret, x1, x2, phase_index)
                    for index, probability in enumerate(probabilities):
                        r1 = (index >> 3) & 1
                        q1 = (index >> 2) & 1
                        r2 = (index >> 1) & 1
                        q2 = index & 1
                        collision = q1 != q2
                        bell_psi = r2 == 1
                        if collision and bell_psi:
                            if r1 == secret:
                                correct += weight * probability
                            else:
                                wrong += weight * probability
                        else:
                            inconclusive += weight * probability
    return {
        "correct_conclusive": correct,
        "wrong_conclusive": wrong,
        "inconclusive": inconclusive,
        "total": correct + wrong + inconclusive,
    }
