"""Computational sanity checks and cross-engine agreement.

No function in this module is a mathematical proof.
"""

from __future__ import annotations
from typing import Optional, Set, Tuple
from .sumset import (
    compute_k_fold_sumset,
    compute_k_fold_sumset_bitwise,
    bitmask_to_set,
)
from .formulas import predict_m3_threshold, block_distance, verify_m3_algebraic_identity
from .healing import self_healing_threshold, self_healing_threshold_fast


def check_ab_agreement(N: int, void_set: Set[int], h: int) -> bool:
    A_hole = set(range(N)) - set(void_set)
    a = compute_k_fold_sumset(A_hole, h)
    b = bitmask_to_set(compute_k_fold_sumset_bitwise(A_hole, h))
    return a == b


def check_abc_agreement_single_block(
    N: int, start: int, length: int
) -> Tuple[bool, dict]:
    """A/B exact engines versus C=M3' predictor."""
    void_set = set(range(start, start + length))
    d = block_distance(N, start, length)
    h_a = self_healing_threshold(N, void_set, max_h=50)
    h_b = self_healing_threshold_fast(N, void_set, max_h=50)
    h_c = predict_m3_threshold(length, d) if d >= 2 else None
    agree = h_a == h_b == h_c
    return agree, {
        "N": N, "start": start, "length": length, "d": d,
        "h_engine_a_exact": h_a,
        "h_engine_b_exact": h_b,
        "h_m3_predictor": h_c,
        "all_agree": agree,
        "note": "Engine C is a conjecture predictor, not an independent exact engine",
    }


def generate_case2b_witness(
    dims: Tuple[int, ...], p: Tuple[int, ...]
) -> Tuple[bool, Optional[Tuple]]:
    """Generate one Case-2b dispersed-corner witness."""
    d = len(dims)
    if d < 2 or len(p) != d:
        return False, None
    if any(n < 3 for n in dims):
        return False, None
    if any(not (0 <= p[i] <= 2 * (dims[i] - 1)) for i in range(d)):
        return False, None
    if any(not (dims[i] - 1 < p[i] < 2 * (dims[i] - 1)) for i in range(d)):
        return False, None

    c = tuple(p[i] - (dims[i] - 1) for i in range(d))
    # Any nonempty proper subset works. Use S={0} as the canonical witness.
    S = {0}
    a = tuple(dims[i] - 1 if i in S else c[i] for i in range(d))
    b = tuple(c[i] if i in S else dims[i] - 1 for i in range(d))

    if tuple(a[i] + b[i] for i in range(d)) != p:
        return False, None
    if any(not (0 <= a[i] <= dims[i] - 1 and 0 <= b[i] <= dims[i] - 1)
           for i in range(d)):
        return False, None
    if not any(a[i] == dims[i] - 1 for i in range(d)):
        return False, None
    if not any(b[i] == dims[i] - 1 for i in range(d)):
        return False, None
    return True, (a, b)


def check_theorem_61_instance(N: int, k: int) -> bool:
    """Finite computational sanity check for the analytically proved T6.1."""
    h = self_healing_threshold(N, {k}, max_h=N + 5)
    if k in {1, N - 2}:
        return h is None
    return h == 2


def check_m3_algebraic_bounds(ell: int, d: int) -> bool:
    return verify_m3_algebraic_identity(ell, d)


# Backward-compatible aliases: older commits used these names.
three_engine_agree = check_abc_agreement_single_block
verify_dispersed_corner_decomposition = generate_case2b_witness
verify_theorem_61 = check_theorem_61_instance
