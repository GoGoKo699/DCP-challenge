from dcp_challenge.exact_probabilities import exact_honest_success
from dcp_challenge.ibm_reanalysis import (
    aggregate_reconstruction,
    legacy_code_expected_success,
)

corrected, details = aggregate_reconstruction(3)
print(f"Legacy-code expected mean: {legacy_code_expected_success(3):.9f}")
print(f"Aggregate-data reconstruction: {corrected:.9f}")
print(f"Ideal mean: {float(exact_honest_success(1, 2, 3)):.9f}")
print("Per-secret details:", details)
