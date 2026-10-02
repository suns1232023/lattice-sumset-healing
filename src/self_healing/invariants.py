"""
invariants.py — Cross-engine validation and theorem invariant checks.

Provides:
1. Three-engine agreement checks (A vs B vs C)
2. Theorem 3.2 Dispersed Corner Decomposition verification
3. Theorem 6.1 analytical invariant checks
"""

from __future__ import annotations
from typing import Optional, Set, Tuple

from .sumset import compute_k_fold_sumset, compute_k_fold_sumset_bitwise, bitmask_to_set
from .formulas import predict_m3_threshold, block_distance, verify_m3_algebraic_identity
from .healing import self_healing_threshold, self_healing_threshold_fast


def three_engine_agree(N: int, start: int, length: int) -> Tuple[bool, dict]:
    """
    Check Engine A (pure-set), B (bitwise), C (formula) all agree on h*.

    Returns (all_agree, details_dict).
    """
    void_set = set(range(start, start + length))
    d = block_distance(N, start, length)
    h_a = self_healing_threshold(N, void_set, max_h=50)
    h_b = self_healing_threshold_fast(N, void_set, max_h=50)
    h_c = predict_m3_threshold(length, d) if d >= 2 else None
    all_agree = (h_a == h_b == h_c)
    return all_agree, {
        'N': N, 'start': start, 'length': length, 'd': d,
        'h_engine_a': h_a, 'h_engine_b': h_b, 'h_engine_c': h_c,
        'all_agree': all_agree,
    }


def verify_dispersed_corner_decomposition(
    dims: Tuple[int, ...],
    p: Tuple[int, ...],
) -> Tuple[bool, Optional[Tuple]]:
    """
    Verify Case 2b of Theorem 3.2 proof (Dispersed Corner Decomposition).

    For p_i in (N_i-1, 2(N_i-1)) for all i, constructs a', b' in
    boundary(A_full) with a' + b' = p using subset S = {0}.

    Returns (success, (a_prime, b_prime)).
    """
    d = len(dims)
    if d < 2:
        return False, None  # d >= 2 required

    # Check Case 2b: all coordinates strictly interior upper
    for i in range(d):
        if not (dims[i] - 1 < p[i] < 2 * (dims[i] - 1)):
            return False, None

    c = tuple(p[i] - (dims[i] - 1) for i in range(d))
    S = {0}  # non-empty proper subset
    a_prime = tuple(dims[i] - 1 if i in S else c[i] for i in range(d))
    b_prime = tuple(c[i] if i in S else dims[i] - 1 for i in range(d))

    # Verify sum
    if tuple(a_prime[i] + b_prime[i] for i in range(d)) != p:
        return False, None

    # Verify both in A_full
    for i in range(d):
        if not (0 <= a_prime[i] <= dims[i] - 1 and 0 <= b_prime[i] <= dims[i] - 1):
            return False, None

    # Verify both on boundary
    a_bnd = any(a_prime[i] == dims[i] - 1 for i in range(d))
    b_bnd = any(b_prime[i] == dims[i] - 1 for i in range(d))
    if not (a_bnd and b_bnd):
        return False, None

    return True, (a_prime, b_prime)


def verify_theorem_61(N: int, k: int) -> bool:
    """
    Verify Theorem 6.1 computationally for single void {k}.
    Theorem: h* = inf iff k in {1, N-2}; h* = 2 iff 2 <= k <= N-3.
    """
    h = self_healing_threshold(N, {k}, max_h=N + 5)
    return (h is None) if k in {1, N - 2} else (h == 2)
