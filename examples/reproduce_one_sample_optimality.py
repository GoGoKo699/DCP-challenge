"""Reproduce the exact one-sample all-H optimality theorem."""
from dcp_challenge.likelihood_decoder import one_sample_optimal_all_h_success

for n in range(1, 8):
    N = 1 << n
    value = one_sample_optimal_all_h_success(n)
    print(f"n={n:2d}, N={N:3d}: {value} = {float(value):.9f}")
