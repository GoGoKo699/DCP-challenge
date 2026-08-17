import math

import numpy as np

from dcp_challenge.heralded_witness import (
    collision_states,
    finite_sample_examples,
    full_state_checks,
    minimal_four_qubit_resources,
    random_product_ratio_stress,
    separable_saturation_probabilities,
    witness_summary,
)


def test_collision_states_and_tight_ratio() -> None:
    sigma_even, sigma_odd = collision_states()
    assert np.allclose(np.trace(sigma_even), 1)
    assert np.allclose(np.trace(sigma_odd), 1)
    assert np.min(np.linalg.eigvalsh(sigma_even)) >= -1e-12
    assert np.min(np.linalg.eigvalsh(sigma_odd)) >= -1e-12
    p_even, p_odd = separable_saturation_probabilities()
    assert math.isclose(p_even, 3 / 8)
    assert math.isclose(p_odd, 1 / 8)
    assert math.isclose(p_even / p_odd, 3)


def test_full_state_dense_checks() -> None:
    for n in (1, 2):
        checks = full_state_checks(n)
        assert math.isclose(checks["trace_even"], 1.0, abs_tol=1e-12)
        assert math.isclose(checks["trace_odd"], 1.0, abs_tol=1e-12)
        assert checks["local_marginal_max_error_from_maximally_mixed"] < 1e-12
        assert math.isclose(
            checks["trace_norm_difference"],
            1 / (2**n),
            abs_tol=1e-12,
        )


def test_random_product_ratio_stress() -> None:
    checks = random_product_ratio_stress(samples=5000, seed=20260817)
    assert checks["max_ratio_observed"] <= 3 + 1e-12
    assert checks["min_ratio_observed"] >= 1 / 3 - 1e-12
    assert checks["minimum_inequality_margin"] >= -1e-12


def test_summary_and_resources() -> None:
    assert math.isclose(witness_summary(1)["honest_correct_conclusive"], 1 / 4)
    examples = finite_sample_examples()
    assert math.isclose(examples["zero_errors_among_50"], (3 / 4) ** 50)
    resources = minimal_four_qubit_resources()
    assert resources["qubits"] == 4
    assert resources["total_cnots_max"] == 3
    assert resources["non_clifford_gates"] == 0


def test_minimal_four_qubit_statevector() -> None:
    from dcp_challenge.minimal_circuit import decoded_statistics

    result = decoded_statistics()
    assert math.isclose(result["correct_conclusive"], 0.25, abs_tol=1e-12)
    assert math.isclose(result["wrong_conclusive"], 0.0, abs_tol=1e-12)
    assert math.isclose(result["inconclusive"], 0.75, abs_tol=1e-12)
    assert math.isclose(result["total"], 1.0, abs_tol=1e-12)
