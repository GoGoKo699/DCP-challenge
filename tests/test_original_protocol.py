from dcp_challenge.original_protocol import (
    is_complementary,
    selected_branch_returns_parity,
)


def test_selected_branch_returns_parity_for_all_small_instances() -> None:
    for n in range(1, 7):
        N = 1 << n
        for k in range(N):
            partner = (k + N // 2) % N
            assert is_complementary(k, partner, n)
            for secret in range(N):
                assert selected_branch_returns_parity(k, partner, secret, n)
