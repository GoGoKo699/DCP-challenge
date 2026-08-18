"""Fast validation of committed exact values and numerical tolerances."""
from __future__ import annotations

import csv
import json
import math
from fractions import Fraction
from pathlib import Path

from dcp_challenge.exact_probabilities import exact_honest_success, special_outcome_decoder_success
from dcp_challenge.heralded_witness import full_state_checks, witness_summary
from dcp_challenge.likelihood_decoder import (
    explicit_two_sample_decoder_success,
    one_sample_optimal_all_h_success,
)

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"


def assert_close(actual: float, expected: float, tolerance: float = 1e-12) -> None:
    if not math.isclose(actual, expected, rel_tol=tolerance, abs_tol=tolerance):
        raise AssertionError(f"{actual!r} != {expected!r} within {tolerance}")


def main() -> None:
    core = json.loads((RESULTS / "correction_core_results.json").read_text())
    small = core["small_exact_counterexample"]
    assert (small["published_special_decoder"]["numerator"], small["published_special_decoder"]["denominator"]) == (23, 32)
    assert (small["explicit_same_measurements_better_decoder"]["numerator"], small["explicit_same_measurements_better_decoder"]["denominator"]) == (25, 32)
    assert explicit_two_sample_decoder_success() == Fraction(25, 32)

    one_sample = json.loads((RESULTS / "one_sample_optimality.json").read_text())
    for row in one_sample:
        n = int(row["n"])
        expected = one_sample_optimal_all_h_success(n)
        stored = row["optimal_all_H_success"]
        assert (stored["numerator"], stored["denominator"]) == (expected.numerator, expected.denominator)
        assert expected == special_outcome_decoder_success(n, 1, 1)

    with (RESULTS / "figure5_corrected.csv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    for row in rows:
        n, m, t = int(row["n"]), int(row["m"]), int(row["t"])
        assert_close(float(row["p_exact_honest"]), float(exact_honest_success(n, m, t)), 1e-14)

    witness = json.loads((RESULTS / "heralded_witness_results.json").read_text())
    assert_close(witness["N2"]["honest_correct_conclusive"], witness_summary(1)["honest_correct_conclusive"])
    for n, key in ((1, "dense_full_state_N2"), (2, "dense_full_state_N4")):
        fresh = full_state_checks(n)
        assert_close(witness[key]["trace_norm_difference"], fresh["trace_norm_difference"], 1e-12)
        assert witness[key]["local_marginal_max_error_from_maximally_mixed"] <= 1e-12

    print("Committed result validation passed.")


if __name__ == "__main__":
    main()
