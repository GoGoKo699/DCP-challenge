from dcp_challenge.exact_probabilities import (
    exact_honest_success,
    published_p_upper,
    special_outcome_decoder_success,
)
from dcp_challenge.likelihood_decoder import exact_h_bayes_success

for label, n, m, t in (("5a", 4, 6, 1), ("5b", 6, 9, 4), ("5c", 9, 21, 9)):
    exact = exact_honest_success(n, m, t)
    special = special_outcome_decoder_success(n, m, t)
    upper = published_p_upper(n, m, t)
    print(
        f"Figure {label}: p_B={float(special):.9f}, "
        f"p_upper={float(upper):.9f}, p_exact={float(exact):.9f}, "
        f"exact_gap={float(exact-special):.9f}"
    )

print(
    "Figure 5a exact optimal all-H decoder:",
    float(exact_h_bayes_success(4, 6)),
)
