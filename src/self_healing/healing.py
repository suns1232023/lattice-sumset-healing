"""Self-healing threshold computations."""

from __future__ import annotations
from typing import Optional, Set, Tuple
from .sumset import (
    compute_k_fold_sumset,
    compute_k_fold_sumset_bitwise,
    compute_k_fold_sumset_nd,
    bitmask_to_set,
)


def _validate_1d_inputs(N: int, void_set: Set[int]) -> set[int]:
    if not isinstance(N, int) or N <= 0:
        raise ValueError("N must be a positive integer")
    V = set(void_set)
    if any(not isinstance(v, int) for v in V):
        raise ValueError("void_set must contain integers")
    if not V <= set(range(N)):
        raise ValueError("void_set contains points outside {0,...,N-1}")
    return V


def self_healing_threshold(
    N: int, void_set: Set[int], max_h: int = 50
) -> Optional[int]:
    """Engine A: exact h* within the requested finite search horizon."""
    if not isinstance(max_h, int) or max_h < 1:
        raise ValueError("max_h must be a positive integer")
    V = _validate_1d_inputs(N, void_set)
    A_full = set(range(N))
    A_hole = A_full - V
    for h in range(1, max_h + 1):
        if compute_k_fold_sumset(A_hole, h) == compute_k_fold_sumset(A_full, h):
            return h
    return None


def self_healing_threshold_fast(
    N: int, void_set: Set[int], max_h: int = 50
) -> Optional[int]:
    """Engine B: independent exact 1-D computation using bit masks."""
    if not isinstance(max_h, int) or max_h < 1:
        raise ValueError("max_h must be a positive integer")
    V = _validate_1d_inputs(N, void_set)
    A_full = set(range(N))
    A_hole = A_full - V

    full_mask = compute_k_fold_sumset_bitwise(A_full, 1)
    hole_mask = compute_k_fold_sumset_bitwise(A_hole, 1)
    if hole_mask == full_mask:
        return 1

    cur_full, cur_hole = full_mask, hole_mask
    full_list, hole_list = sorted(A_full), sorted(A_hole)
    for h in range(2, max_h + 1):
        nxt_full = 0
        for a in full_list:
            nxt_full |= cur_full << a
        cur_full = nxt_full

        nxt_hole = 0
        for a in hole_list:
            nxt_hole |= cur_hole << a
        cur_hole = nxt_hole

        if cur_hole == cur_full:
            return h
    return None


def self_healing_threshold_nd(
    dims: Tuple[int, ...],
    void_set: Set[Tuple[int, ...]],
    max_h: int = 10,
) -> Optional[int]:
    """Exact finite-dimensional threshold computation."""
    if len(dims) < 1 or any(not isinstance(n, int) or n <= 0 for n in dims):
        raise ValueError("dims must be a non-empty tuple of positive integers")
    if not isinstance(max_h, int) or max_h < 1:
        raise ValueError("max_h must be a positive integer")
    d = len(dims)
    A_full = set(__import__("itertools").product(*[range(n) for n in dims]))
    V = set(void_set)
    if any(len(v) != d or any(not isinstance(x, int) for x in v) for v in V):
        raise ValueError("void_set contains invalid lattice points")
    if not V <= A_full:
        raise ValueError("void_set contains points outside A_full")
    A_hole = A_full - V
    for h in range(1, max_h + 1):
        if compute_k_fold_sumset_nd(A_hole, h) == compute_k_fold_sumset_nd(A_full, h):
            return h
    return None


def classify_1d_void(N: int, void_set: Set[int]) -> str:
    """Analytical classification label; independent of finite search horizon."""
    V = _validate_1d_inputs(N, void_set)
    return "INFINITE" if V & {1, N - 2} else "FINITE"
