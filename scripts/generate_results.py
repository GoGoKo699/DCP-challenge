"""Regenerate the machine-readable results committed in ``results/``."""
from __future__ import annotations

import csv
import json
import math
from fractions import Fraction
from pathlib import Path
from typing import Any

from dcp_challenge.exact_probabilities import (
    exact_honest_success,
    published_p_upper,
    special_outcome_decoder_success,
)
from dcp_challenge.heralded_witness import (
    finite_sample_examples,
    full_state_checks,
    minimal_four_qubit_resources,
    random_product_ratio_stress,
    separable_saturation_probabilities,
    witness_summary,
)
from dcp_challenge.likelihood_decoder import (
    exact_h_bayes_success,
    explicit_two_sample_decoder_breakdown,
    explicit_two_sample_decoder_success,
    h_likelihood_monte_carlo,
    one_sample_optimal_all_h_success,
    one_sample_parity_difference,
)
from dcp_challenge.statistics import (
    adaptive_sequential_lower_tail_bound,
    bernoulli_standard_error,
    legacy_standard_error,
)

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
RESULTS.mkdir(exist_ok=True)


def fraction_record(value: Fraction) -> dict[str, float | int]:
    return {
        "numerator": value.numerator,
        "denominator": value.denominator,
        "decimal": float(value),
    }


def canonicalize(value: Any) -> Any:
    """Normalize floating diagnostics without pretending to exact bit portability."""
    if isinstance(value, dict):
        return {key: canonicalize(item) for key, item in value.items()}
    if isinstance(value, list):
        return [canonicalize(item) for item in value]
    if isinstance(value, tuple):
        return [canonicalize(item) for item in value]
    if isinstance(value, float):
        if not math.isfinite(value):
            return value
        if abs(value) < 5e-15:
            return 0.0
        return float(f"{value:.14g}")
    return value


def build_figure5_rows(run_large_monte_carlo: bool) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for label, n, m, t in (("5a", 4, 6, 1), ("5b", 6, 9, 4), ("5c", 9, 21, 9)):
        exact = exact_honest_success(n, m, t)
        special = special_outcome_decoder_success(n, m, t)
        row: dict[str, object] = {
            "figure": label,
            "n": n,
            "N": 2**n,
            "m": m,
            "t": t,
            "samples": m * t,
            "p_B_special": float(special),
            "p_upper_published": float(published_p_upper(n, m, t)),
            "p_exact_honest": float(exact),
            "exact_gap_honest_minus_p_B": float(exact - special),
        }
        if label == "5a":
            result = exact_h_bayes_success(n, m * t)
            row.update(
                {
                    "all_H_full_likelihood": float(result),
                    "all_H_method": "exact",
                    "all_H_trials": "",
                    "all_H_seed": "",
                    "all_H_ci_low": "",
                    "all_H_ci_high": "",
                }
            )
        elif run_large_monte_carlo:
            if label == "5b":
                trials, seed, batch = 1_000_000, 20260817, 500
            else:
                trials, seed, batch = 60_000, 20260818, 25
            result = h_likelihood_monte_carlo(n, m * t, trials, seed, batch)
            row.update(
                {
                    "all_H_full_likelihood": result.estimate,
                    "all_H_method": "Monte Carlo, Wilson 95% interval",
                    "all_H_trials": result.trials,
                    "all_H_seed": result.seed,
                    "all_H_ci_low": result.wilson_low,
                    "all_H_ci_high": result.wilson_high,
                }
            )
        else:
            reference = {
                "5b": (0.937289, 1_000_000, 20260817, 0.9368121396967324, 0.9377625006608012),
                "5c": (0.9571833333333334, 60_000, 20260818, 0.955533995616519, 0.9587741330997164),
            }[label]
            row.update(
                {
                    "all_H_full_likelihood": reference[0],
                    "all_H_method": "frozen Monte Carlo, Wilson 95% interval",
                    "all_H_trials": reference[1],
                    "all_H_seed": reference[2],
                    "all_H_ci_low": reference[3],
                    "all_H_ci_high": reference[4],
                }
            )
        rows.append(row)
    return rows


def one_sample_records() -> list[dict[str, object]]:
    rows = []
    for n in range(1, 8):
        N = 1 << n
        difference = one_sample_parity_difference(n)
        support = [index for index, value in enumerate(difference) if value]
        rows.append(
            {
                "n": n,
                "N": N,
                "optimal_all_H_success": fraction_record(one_sample_optimal_all_h_success(n)),
                "special_decoder_success": fraction_record(special_outcome_decoder_success(n, 1, 1)),
                "difference_support_outcomes_rN_plus_y": support,
                "difference_values": [fraction_record(difference[index]) for index in support],
            }
        )
    return rows


def main(run_large_monte_carlo: bool = False) -> None:
    figure_rows = build_figure5_rows(run_large_monte_carlo)
    fieldnames = sorted({key for row in figure_rows for key in row})
    with (RESULTS / "figure5_corrected.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(figure_rows)

    p_figure5b = float(exact_honest_success(6, 9, 4))
    one_sample = one_sample_records()
    witness = canonicalize(
        {
            "N2": witness_summary(1),
            "N4": witness_summary(2),
            "separable_saturating_product_effect_probabilities": separable_saturation_probabilities(),
            "finite_sample_examples": finite_sample_examples(),
            "adaptive_sequential_examples": {
                "zero_errors_among_50": adaptive_sequential_lower_tail_bound(50, 0),
                "at_most_20_errors_among_200": adaptive_sequential_lower_tail_bound(200, 20),
            },
            "dense_full_state_N2": full_state_checks(1),
            "dense_full_state_N4": full_state_checks(2),
            "random_product_ratio_stress": random_product_ratio_stress(20_000, 20260817),
            "minimal_four_qubit_resources": minimal_four_qubit_resources(),
        }
    )

    core = {
        "small_exact_counterexample": {
            "published_special_decoder": fraction_record(special_outcome_decoder_success(2, 2, 1)),
            "explicit_same_measurements_better_decoder": fraction_record(explicit_two_sample_decoder_success()),
            "breakdown": {
                key: fraction_record(value)
                for key, value in explicit_two_sample_decoder_breakdown().items()
            },
        },
        "one_sample_optimality": one_sample,
        "figure5": figure_rows,
        "standard_error_example_figure5b_r1000": {
            "p": p_figure5b,
            "legacy_formula": legacy_standard_error(p_figure5b, 1000),
            "correct_bernoulli_formula": bernoulli_standard_error(p_figure5b, 1000),
        },
        "heralded_witness": witness,
        "validation_policy": {
            "exact_quantities": "exact rational or integer comparison",
            "monte_carlo": "committed seeds, trial counts, Wilson intervals, and independent-seed cross-checks",
            "floating_linear_algebra": "numerical tolerances encoded in the tests; byte-identical portability is not claimed",
        },
    }

    with (RESULTS / "correction_core_results.json").open("w", encoding="utf-8") as handle:
        json.dump(core, handle, indent=2, sort_keys=True)
        handle.write("\n")
    with (RESULTS / "one_sample_optimality.json").open("w", encoding="utf-8") as handle:
        json.dump(one_sample, handle, indent=2, sort_keys=True)
        handle.write("\n")
    with (RESULTS / "heralded_witness_results.json").open("w", encoding="utf-8") as handle:
        json.dump(witness, handle, indent=2, sort_keys=True)
        handle.write("\n")

    print(json.dumps(core, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
