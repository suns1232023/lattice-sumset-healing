"""
healing.py — Self-healing threshold h*(A_hole; A_full) computation.

Definition:
    h* = min{h >= 1 : hA_hole = hA_full}
    Returns None if h* > max_h (likely infinite).

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
    Engine A — exact h* via pure-set comparison (ground truth).

    h* = min{h >= 1 : hA_hole = hA_full}

    Args:
        N: Size of full interval {0, ..., N-1}.
        void_set: Removed interior points.
        max_h: Search limit (returns None if h* > max_h).

    Examples:
        >>> self_healing_threshold(7, {3, 4})   # reviewer critical case
        3
        >>> self_healing_threshold(5, {1})       # near-boundary -> h* = inf
        None
        >>> self_healing_threshold(7, {3})       # deep interior -> h* = 2
        2
    """
    A_full = set(range(N))
    A_hole = A_full - void_set
    for h in range(1, max_h + 1):
        if compute_k_fold_sumset(A_hole, h) == compute_k_fold_sumset(A_full, h):
            return h
    return None


def self_healing_threshold_fast(
    N: int,
    void_set: Set[int],
    max_h: int = 50,
) -> Optional[int]:
    """
    Engine B — bitwise h* (~100x faster than Engine A).
    Results must agree with self_healing_threshold() on all valid inputs.
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

    return None


def self_healing_threshold_nd(
    dims: Tuple[int, ...],
    void_set: Set[Tuple[int, ...]],
    max_h: int = 10,
) -> Optional[int]:
    """
    Multi-dimensional h* for Theorem 3.2 verification.

    Theorem 3.2 [PROVED]: For d >= 2 rectangular boxes with strictly
    interior voids, h* = 2 always.

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
    Theorem 6.1/7.1: analytical classification (no computation needed).

    Returns "INFINITE" if h* = inf, "FINITE" if h* is finite.
    """
    return "INFINITE" if void_set & {1, N - 2} else "FINITE"
