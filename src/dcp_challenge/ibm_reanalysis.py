"""Aggregate-only reanalysis of the IBM counts archived in ``IBM.py``.

The repository does not contain raw shot records or timestamps.  This module
therefore reconstructs only the three aggregate categories available for each
preparation case: selected/q1=1, selected/q1=0, and not selected.
"""
from __future__ import annotations

from typing import Dict, Tuple

import numpy as np

# Integer expressions are copied from the original IBM.py file.
IBM_SELECTED_ONE = {
    "A": 1 + 5 + 2 + 3 + 1 + 1 + 4 + 5 + 1 + 6,
    "B": 1 + 3 + 3 + 4 + 1 + 4 + 3 + 2 + 1 + 1,
    "C": 2 + 3 + 3 + 4 + 3 + 3 + 5 + 1 + 1 + 2,
    "D": 3 + 1 + 6 + 1 + 2 + 2 + 3 + 3 + 3 + 6,
    "E": 125 + 104 + 100 + 94 + 136 + 91 + 119 + 98 + 123 + 90,
    "F": 92 + 90 + 124 + 100 + 129 + 98 + 117 + 103 + 101 + 99,
    "G": 105 + 109 + 109 + 110 + 99 + 123 + 103 + 110 + 110 + 100,
    "H": 106 + 96 + 99 + 106 + 130 + 111 + 101 + 120 + 124 + 112,
}

IBM_SELECTED_TOTAL = {
    "A": 1 + 98 + 5 + 156 + 2 + 110 + 3 + 141 + 1 + 99 + 135 + 4 + 99 + 5 + 116 + 1 + 111 + 6 + 134,
    "B": 1 + 136 + 3 + 104 + 3 + 112 + 4 + 119 + 1 + 123 + 4 + 114 + 3 + 136 + 2 + 109 + 1 + 131 + 1 + 129,
    "C": 2 + 118 + 3 + 123 + 3 + 120 + 4 + 144 + 3 + 126 + 3 + 120 + 5 + 118 + 1 + 120 + 1 + 132 + 2 + 125,
    "D": 3 + 122 + 1 + 125 + 6 + 127 + 1 + 115 + 2 + 121 + 2 + 124 + 3 + 132 + 3 + 116 + 3 + 140 + 6 + 103,
    "E": 125 + 14 + 104 + 10 + 100 + 19 + 94 + 10 + 136 + 17 + 91 + 11 + 119 + 22 + 98 + 14 + 123 + 17 + 90 + 11,
    "F": 92 + 16 + 90 + 7 + 124 + 7 + 100 + 16 + 129 + 14 + 98 + 8 + 117 + 18 + 103 + 11 + 101 + 18 + 99 + 8,
    "G": 105 + 19 + 109 + 9 + 109 + 16 + 110 + 12 + 99 + 7 + 123 + 13 + 103 + 6 + 110 + 9 + 110 + 13 + 100 + 8,
    "H": 106 + 18 + 96 + 12 + 99 + 11 + 106 + 14 + 130 + 23 + 111 + 15 + 101 + 10 + 120 + 21 + 124 + 16 + 112 + 13,
}

TOTAL_SHOTS_PER_CASE = 5 * 1024


def legacy_code_expected_success(t: int = 3) -> float:
    """Expected mean of the stochastic reconstruction implemented in IBM.py."""
    if t < 0:
        raise ValueError("t must be nonnegative")
    p_one = {
        case: IBM_SELECTED_ONE[case] / IBM_SELECTED_TOTAL[case]
        for case in IBM_SELECTED_ONE
    }
    definitive_fidelity = (
        (1.0 - p_one["B"])
        + (1.0 - p_one["C"])
        + p_one["F"]
        + p_one["G"]
    ) / 4.0
    solve_probability = 1.0 - (3.0 / 4.0) ** t
    return 0.5 + solve_probability * (definitive_fidelity - 0.5)


def aggregate_reconstruction(
    t: int = 3,
) -> Tuple[float, Dict[int, Dict[str, float]]]:
    """Reconstruct the retry rule from all eight aggregate preparation cases."""
    if t < 0:
        raise ValueError("t must be nonnegative")
    p_one = {
        case: IBM_SELECTED_ONE[case] / IBM_SELECTED_TOTAL[case]
        for case in IBM_SELECTED_ONE
    }
    selection_rate = {
        case: IBM_SELECTED_TOTAL[case] / TOTAL_SHOTS_PER_CASE
        for case in IBM_SELECTED_TOTAL
    }

    details: Dict[int, Dict[str, float]] = {}
    for secret, cases in ((0, ("A", "B", "C", "D")), (1, ("E", "F", "G", "H"))):
        correct = 0.0
        wrong = 0.0
        for case in cases:
            conditional_correct = (1.0 - p_one[case]) if secret == 0 else p_one[case]
            correct += 0.25 * selection_rate[case] * conditional_correct
            wrong += 0.25 * selection_rate[case] * (1.0 - conditional_correct)
        fail = 1.0 - correct - wrong
        if 1.0 - fail > 0.0:
            success = correct * (1.0 - fail**t) / (1.0 - fail) + 0.5 * fail**t
        else:
            success = 0.5
        details[secret] = {
            "correct_per_iteration": correct,
            "wrong_per_iteration": wrong,
            "fail_per_iteration": fail,
            "success_after_t": success,
        }

    mean = 0.5 * (details[0]["success_after_t"] + details[1]["success_after_t"])
    return mean, details


def multinomial_bootstrap(
    t: int = 3,
    trials: int = 100_000,
    seed: int = 20260817,
) -> Dict[str, float]:
    """Finite-count bootstrap for the aggregate reconstruction.

    The interval does not account for hardware drift or correlations absent
    from the archived aggregate counts.
    """
    if t < 0 or trials <= 0:
        raise ValueError("invalid bootstrap parameter")
    rng = np.random.default_rng(seed)
    cases_by_secret = {0: ("A", "B", "C", "D"), 1: ("E", "F", "G", "H")}
    category_probabilities = {
        case: np.array(
            [
                IBM_SELECTED_ONE[case],
                IBM_SELECTED_TOTAL[case] - IBM_SELECTED_ONE[case],
                TOTAL_SHOTS_PER_CASE - IBM_SELECTED_TOTAL[case],
            ],
            dtype=np.float64,
        )
        / TOTAL_SHOTS_PER_CASE
        for case in IBM_SELECTED_ONE
    }

    simulated = np.empty(trials, dtype=np.float64)
    for draw in range(trials):
        secret_success = []
        for secret, cases in cases_by_secret.items():
            correct = 0.0
            wrong = 0.0
            for case in cases:
                one, zero, _not_selected = rng.multinomial(
                    TOTAL_SHOTS_PER_CASE,
                    category_probabilities[case],
                )
                if secret == 0:
                    correct += 0.25 * zero / TOTAL_SHOTS_PER_CASE
                    wrong += 0.25 * one / TOTAL_SHOTS_PER_CASE
                else:
                    correct += 0.25 * one / TOTAL_SHOTS_PER_CASE
                    wrong += 0.25 * zero / TOTAL_SHOTS_PER_CASE
            fail = 1.0 - correct - wrong
            if 1.0 - fail > 0.0:
                success = correct * (1.0 - fail**t) / (1.0 - fail) + 0.5 * fail**t
            else:
                success = 0.5
            secret_success.append(success)
        simulated[draw] = 0.5 * sum(secret_success)

    low, high = np.quantile(simulated, [0.025, 0.975])
    return {
        "trials": trials,
        "seed": seed,
        "mean": float(np.mean(simulated)),
        "standard_deviation": float(np.std(simulated, ddof=1)),
        "percentile_2_5": float(low),
        "percentile_97_5": float(high),
    }


def aggregate_case_table() -> Dict[str, Dict[str, float]]:
    """Return the archived aggregate count table in machine-readable form."""
    table: Dict[str, Dict[str, float]] = {}
    for case in sorted(IBM_SELECTED_ONE):
        selected_one = IBM_SELECTED_ONE[case]
        selected_total = IBM_SELECTED_TOTAL[case]
        table[case] = {
            "selected_q1_one": selected_one,
            "selected_q1_zero": selected_total - selected_one,
            "not_selected": TOTAL_SHOTS_PER_CASE - selected_total,
            "selected_total": selected_total,
            "total_shots": TOTAL_SHOTS_PER_CASE,
        }
    return table
