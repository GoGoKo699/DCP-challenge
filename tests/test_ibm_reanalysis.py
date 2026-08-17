import math

from dcp_challenge.ibm_reanalysis import (
    aggregate_case_table,
    aggregate_reconstruction,
    legacy_code_expected_success,
    multinomial_bootstrap,
)


def test_aggregate_counts_are_complete() -> None:
    table = aggregate_case_table()
    assert set(table) == set("ABCDEFGH")
    for record in table.values():
        assert (
            record["selected_q1_one"]
            + record["selected_q1_zero"]
            + record["not_selected"]
            == record["total_shots"]
        )


def test_reconstruction_means() -> None:
    corrected, _ = aggregate_reconstruction(3)
    assert math.isclose(legacy_code_expected_success(3), 0.7545878022042778)
    assert math.isclose(corrected, 0.7439808124791598)


def test_small_bootstrap_tracks_point_estimate() -> None:
    result = multinomial_bootstrap(3, trials=2000, seed=20260817)
    point, _ = aggregate_reconstruction(3)
    assert abs(result["mean"] - point) < 0.001
    assert result["percentile_2_5"] < point < result["percentile_97_5"]
