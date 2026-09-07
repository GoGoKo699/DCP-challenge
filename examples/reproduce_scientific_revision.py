"""Print exact revised conclusions; no result files are modified."""
from fractions import Fraction as F
from dcp_challenge.scientific_revision import (
    one_sample_global_success, refreshed_secret_global_success, confidence_frontier,
    fixed_round_source_error_log_bound,
)

print("One-sample unrestricted optimum at N=4:",one_sample_global_success(2))
print("Refreshed-secret joint optimum at N=4, L=2:",refreshed_secret_global_success(2,2))
for q in (F(1,8),F(1,4),F(3,8),F(1,2),F(1)):
    g=confidence_frontier(1,q,"global")
    s=confidence_frontier(1,q,"separable")
    print(f"N=2, q={q}: global confidence={g.confidence}; SEP/PPT/LOCC={s.confidence}")
print("Illustrative calibrated fixed-R log bound:",
      fixed_round_source_error_log_bound(2500,0,7500,F(1,100),F(1,100)))
