"""
invariants.py — Cross-engine validation and theorem sanity checks.

IMPORTANT NAMING CONVENTIONS:
    Functions named check_*   : computational sanity checks on theorem instances.
    Functions named verify_*  : cross-engine agreement checks.
    Functions named generate_* : witness/decomposition generators.

    None of these functions constitute mathematical proofs.
    Theorems 3.2, 6.1, 7.1 are proved analytically (see docs/THEOREMS.md).
    Python functions here perform regression / sanity checking only.

Three computation roles:
    A — Reference exact computation  (pure-set, ground truth)
    B — Independent fast exact computation  (bitwise)
    C — M3' conjecture predictor  (formula, NOT an independent h* computation)
"""

from __future__ import annotations
from typing import Optional, Set, Tuple

from .sumset import compute_k_fold_sumset, compute_k_fold_sumset_bitwise, bitmask_to_set
from .formulas import predict_m3_threshold, block_distance, verify_m3_algebraic_identity
from .healing import self_healing_threshold, self_healing_threshold_fast


# ── Cross-engine agreement (A vs B vs C) ─────────────────────────────────────

def check_ab_agreement(N: int, void_set: Set[int], h: int) -> bool:
    """
    Check that Engine A (pure-set) and Engine B (bitwise) agree on hA_hole.

    Both A and B compute exact h*. Agreement provides cross-validation.
    Disagreement signals a bug.

    Args:
        N: Size of full interval.
        void_set: Removed interior points.
        h: Number of folds to check.

    Returns:
        True if both engines produce the same sumset.
    """
    A_hole = set(range(N)) - void_set
    result_a = compute_k_fold_sumset(A_hole, h)
    result_b = bitmask_to_set(compute_k_fold_sumset_bitwise(A_hole, h))
    return result_a == result_b


def check_abc_agreement_single_block(
    N: int, start: int, length: int
) -> Tuple[bool, dict]:
    """
    Check that Engine A, Engine B, and M3' predictor (C) agree on h*.

    NOTE: Engine C (predict_m3_threshold) is the M3' CONJECTURE PREDICTOR,
    not an independent exact computation of h*. Agreement between A, B, and C
    provides computational evidence for Conjecture M3', not a proof.

    Args:
        N: Size of full interval.
        start: Start of void block.
        length: Length of void block.

    Returns:
        (all_agree, details_dict)
    """
    void_set = set(range(start, start + length))
    d = block_distance(N, start, length)

    # Engine A: exact h* (reference)
    h_a = self_healing_threshold(N, void_set, max_h=50)
    # Engine B: exact h* (independent fast)
    h_b = self_healing_threshold_fast(N, void_set, max_h=50)
    # Engine C: M3' conjecture predictor (NOT an independent h* computation)
    h_c = predict_m3_threshold(length, d) if d >= 2 else None

    all_agree = (h_a == h_b == h_c)
    return all_agree, {
        'N': N, 'start': start, 'length': length, 'd': d,
        'h_engine_a_exact': h_a,
        'h_engine_b_exact': h_b,
        'h_m3_predictor': h_c,
        'all_agree': all_agree,
        'note': 'Engine C is M3 conjecture predictor, not independent exact computation',
    }


# ── Theorem 3.2: Case 2b witness generator ───────────────────────────────────

def generate_case2b_witness(
    dims: Tuple[int, ...],
    p: Tuple[int, ...],
) -> Tuple[bool, Optional[Tuple]]:
    """
    Generate a Case 2b Dispersed Corner Decomposition witness for Theorem 3.2.

    This generates a SPECIFIC WITNESS (a', b') for ONE CASE of the proof.
    It is NOT a verification of the full theorem.

    Theorem 3.2 is proved analytically for ALL cases (1, 2a, 2b, mixed).
    This function only handles Case 2b: p_i in (N_i-1, 2(N_i-1)) for all i.

    Mathematical context:
        p must be in 2A_full (not in A_full).
        For dims=(4,4): A_full = {0,1,2,3}^2, 2A_full = {0,...,6}^2.
        p=(4,4) is in 2A_full (since 4 <= 2*(4-1)=6), not in A_full.

    Args:
        dims: Box dimensions (N_1, ..., N_d). Requires d >= 2.
        p: Target point in 2A_full (NOT in A_full). Must satisfy
           N_i-1 < p_i < 2*(N_i-1) for all i (Case 2b condition).

    Returns:
        (success, (a_prime, b_prime)) if Case 2b witness found.
        (False, None) if p does not satisfy Case 2b conditions.
    """
    d = len(dims)
    if d < 2:
        return False, None  # d >= 2 required by Theorem 3.2

    # Verify p is in 2A_full range: 0 <= p_i <= 2*(N_i-1)
    for i in range(d):
        if not (0 <= p[i] <= 2 * (dims[i] - 1)):
            return False, None  # p not in 2A_full

    # Check Case 2b condition: p_i strictly between N_i-1 and 2*(N_i-1)
    for i in range(d):
        if not (dims[i] - 1 < p[i] < 2 * (dims[i] - 1)):
            return False, None  # not Case 2b

    # Construct witness using S = {0}
    c = tuple(p[i] - (dims[i] - 1) for i in range(d))
    S = {0}  # non-empty proper subset of {0,...,d-1}
    a_prime = tuple(dims[i] - 1 if i in S else c[i] for i in range(d))
    b_prime = tuple(c[i] if i in S else dims[i] - 1 for i in range(d))

    # Verify sum
    if tuple(a_prime[i] + b_prime[i] for i in range(d)) != p:
        return False, None

    # Verify both in A_full: 0 <= coord <= N_i-1
    for i in range(d):
        if not (0 <= a_prime[i] <= dims[i] - 1 and 0 <= b_prime[i] <= dims[i] - 1):
            return False, None

    # Verify both on boundary (at least one coordinate at maximum)
    a_on_boundary = any(a_prime[i] == dims[i] - 1 for i in range(d))
    b_on_boundary = any(b_prime[i] == dims[i] - 1 for i in range(d))
    if not (a_on_boundary and b_on_boundary):
        return False, None

    return True, (a_prime, b_prime)


# ── Theorem 6.1/7.1: Sanity checks ───────────────────────────────────────────

def check_theorem_61_instance(N: int, k: int) -> bool:
    """
    Sanity check Theorem 6.1 for a single void {k} in {0,...,N-1}.

    Theorem 6.1 [PROVED analytically]:
        h* = infinity  iff  k in {1, N-2}
        h* = 2         iff  2 <= k <= N-3

    This function performs a COMPUTATIONAL SANITY CHECK on one instance.
    It is NOT a verification of the theorem (which is proved analytically).

    NOTE: For k in {1, N-2}, we check that self_healing_threshold() returns
    None within max_h=N+5. This is consistent with h*=infinity but does not
    prove it — the analytical proof is in docs/THEOREMS.md.

    Args:
        N: Size of full interval (N >= 5).
        k: Void position (1 <= k <= N-2).

    Returns:
        True if computational result is consistent with Theorem 6.1.
    """
    h = self_healing_threshold(N, {k}, max_h=N + 5)
    if k in {1, N - 2}:
        # Theorem predicts h* = infinity; we check None within N+5 steps
        return h is None
    else:
        # Theorem predicts h* = 2
        return h == 2


def check_m3_algebraic_bounds(ell: int, d: int) -> bool:
    """
    Verify the algebraic identity underlying Conjecture M3'.

    The formula h = ceil(ell/(d-1)) + 1 satisfies:
        (h-1)(d-1) >= ell > (h-2)(d-1)

    This is a DEFINITION-LEVEL algebraic identity, not an empirical claim.
    It holds by construction of the ceiling function.

    Args:
        ell: Void block length.
        d: Boundary distance (d >= 2).

    Returns:
        True if the algebraic identity holds.
    """
    return verify_m3_algebraic_identity(ell, d)
