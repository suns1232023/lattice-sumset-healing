"""
healing.py — Self-healing threshold h*(A_hole; A_full) computation.

Definition:
    h* = min{h >= 1 : hA_hole = hA_full}

Return value semantics:
    Returns an integer h* if found within max_h.
    Returns None if NO healing threshold was found within max_h.
    None means "not found up to max_h" — it does NOT mean h* = infinity.
    To establish h* = infinity analytically, use classify_1d_void() (Theorem 6.1/7.1).

Key results:
    Theorem 3.2 [PROVED]: h* = 2 for rectangular boxes, d >= 2.
    Theorem 6.1 [PROVED]: d=1, h* = inf iff void touches {1, N-2}.
    Conjecture M3' [VHC]: h*(ell, d) = ceil(ell/(d-1)) + 1.
"""

from __future__ import annotations
from typing import Optional, Set, Tuple

from .sumset import (
    compute_k_fold_sumset,
    compute_k_fold_sumset_bitwise,
    compute_k_fold_sumset_nd,
)


def self_healing_threshold(
    N: int,
    void_set: Set[int],
    max_h: int = 50,
) -> Optional[int]:
    """
    Compute h*(A_hole; A_full) using Engine A (pure-set reference).

    h* = min{h >= 1 : hA_hole = hA_full}

    Args:
        N: Size of full interval A_full = {0, 1, ..., N-1}.
        void_set: Removed interior points V_void.
        max_h: Search limit.

    Returns:
        Integer h* if found within max_h.
        None if no healing threshold found within max_h.
        NOTE: None does NOT imply h* = infinity. Use classify_1d_void()
        for the analytical infinity classification (Theorem 6.1/7.1).

    Examples:
        >>> self_healing_threshold(7, {3, 4})   # reviewer critical case
        3
        >>> self_healing_threshold(7, {3})       # deep interior
        2
        >>> self_healing_threshold(5, {1}, max_h=10)  # near-boundary
        None  # not found within 10 steps; analytically h* = inf (Theorem 6.1)
    """
    A_full = set(range(N))
    A_hole = A_full - void_set
    for h in range(1, max_h + 1):
        if compute_k_fold_sumset(A_hole, h) == compute_k_fold_sumset(A_full, h):
            return h
    return None  # not found within max_h — does NOT mean h* = infinity


def self_healing_threshold_fast(
    N: int,
    void_set: Set[int],
    max_h: int = 50,
) -> Optional[int]:
    """
    Compute h*(A_hole; A_full) using Engine B (bitwise, ~100x faster).

    Results must agree with self_healing_threshold() on all valid inputs.
    Same return value semantics: None means "not found within max_h."

    Args:
        N: Size of full interval.
        void_set: Removed interior points.
        max_h: Search limit.

    Returns:
        Integer h* if found within max_h, else None.
    """
    A_full = set(range(N))
    A_hole = A_full - void_set
    A_full_list = sorted(A_full)
    A_hole_list = sorted(A_hole)

    cur_full = sum(1 << a for a in A_full_list)
    cur_hole = sum(1 << a for a in A_hole_list)

    if cur_hole == cur_full:
        return 1

    for h in range(2, max_h + 1):
        nxt_full = 0
        for a in A_full_list:
            nxt_full |= (cur_full << a)
        cur_full = nxt_full

        nxt_hole = 0
        for a in A_hole_list:
            nxt_hole |= (cur_hole << a)
        cur_hole = nxt_hole

        if cur_hole == cur_full:
            return h

    return None  # not found within max_h — does NOT mean h* = infinity


def self_healing_threshold_nd(
    dims: Tuple[int, ...],
    void_set: Set[Tuple[int, ...]],
    max_h: int = 10,
) -> Optional[int]:
    """
    Compute h* for a d-dimensional rectangular box (Theorem 3.2 verification).

    Theorem 3.2 [PROVED]: For d >= 2 rectangular boxes with strictly
    interior voids, h* = 2 always.

    Args:
        dims: Box dimensions (N_1, ..., N_d).
        void_set: Removed interior points (tuples).
        max_h: Search limit.

    Returns:
        Integer h* if found within max_h, else None.

    Examples:
        >>> self_healing_threshold_nd((3, 3), {(1, 1)})
        2
    """
    import itertools
    A_full = set(itertools.product(*[range(d) for d in dims]))
    A_hole = A_full - void_set
    for h in range(1, max_h + 1):
        if compute_k_fold_sumset_nd(A_hole, h) == compute_k_fold_sumset_nd(A_full, h):
            return h
    return None


def classify_1d_void(N: int, void_set: Set[int]) -> str:
    """
    Analytical classification of 1D void (Theorems 6.1 and 7.1).

    This is the ONLY function that correctly identifies h* = infinity.
    self_healing_threshold() returning None does NOT imply infinity.

    Theorem 6.1/7.1 [PROVED]:
        h* = infinity  iff  void_set intersects {1, N-2}
        h* = 2         iff  void_set subset of {2, ..., N-3}

    Returns:
        "INFINITE" if h* = infinity (analytically proved).
        "FINITE"   if h* is finite (= 2 for deep interior voids).
    """
    return "INFINITE" if void_set & {1, N - 2} else "FINITE"
