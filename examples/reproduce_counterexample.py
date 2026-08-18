from dcp_challenge.exact_probabilities import special_outcome_decoder_success
from dcp_challenge.likelihood_decoder import (
    explicit_two_sample_decoder_breakdown,
    explicit_two_sample_decoder_success,
)

published = special_outcome_decoder_success(2, 2, 1)
improved = explicit_two_sample_decoder_success()
print(f"Published special-outcome decoder: {published} = {float(published):.6f}")
print(f"Same measurements, better decoder: {improved} = {float(improved):.6f}")
print("Breakdown:")
for key, value in explicit_two_sample_decoder_breakdown().items():
    print(f"  {key}: {value} = {float(value):.6f}")
