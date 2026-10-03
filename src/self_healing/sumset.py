"""Exact finite sumset engines."""

from __future__ import annotations
from typing import Set, Tuple


def _validate_k(k: int) -> None:
    if not isinstance(k, int) or isinstance(k, bool) or k < 0:
        raise ValueError("k must be a non-negative integer")


def compute_k_fold_sumset(A: Set[int], k: int) -> Set[int]:
    """Engine A: exact pure-set k-fold Minkowski sum."""
    _validate_k(k)
    A = set(A)
    if k == 0:
        return {0}
    if not A:
        return set()
    if k == 1:
        return A
    current = A
    for _ in range(2, k + 1):
        current = {x + a for x in current for a in A}
    return current


def compute_k_fold_sumset_nd(
    A: Set[Tuple[int, ...]], k: int
) -> Set[Tuple[int, ...]]:
    """Exact k-fold Minkowski sum for finite lattice points."""
    _validate_k(k)
    A = set(A)
    if not A:
        return set()
    d = len(next(iter(A)))
    if any(len(x) != d for x in A):
        raise ValueError("all lattice points must have the same dimension")
    if k == 0:
        return {tuple(0 for _ in range(d))}
    if k == 1:
        return A
    current = A
    for _ in range(2, k + 1):
        current = {
            tuple(x[i] + a[i] for i in range(d))
            for x in current
            for a in A
        }
    return current


def compute_k_fold_sumset_bitwise(A: Set[int], k: int) -> int:
    """Engine B: exact 1-D sumset represented as an integer bit mask."""
    _validate_k(k)
    A = set(A)
    if any((not isinstance(a, int)) or a < 0 for a in A):
        raise ValueError("bitwise engine requires non-negative integer elements")
    if k == 0:
        return 1  # {0}
    if not A:
        return 0
    current = sum(1 << a for a in A)
    for _ in range(k - 1):
        nxt = 0
        for a in A:
            nxt |= current << a
        current = nxt
    return current


def bitmask_to_set(mask: int) -> Set[int]:
    """Convert a non-negative integer bit mask into a set of positions."""
    if not isinstance(mask, int) or mask < 0:
        raise ValueError("mask must be a non-negative integer")
    result: Set[int] = set()
    pos = 0
    while mask:
        if mask & 1:
            result.add(pos)
        mask >>= 1
        pos += 1
    return result


def h_sumset_1d(A: Set[int], h: int) -> Set[int]:
    return compute_k_fold_sumset(A, h)


def full_interval_sumset(N: int, h: int) -> Set[int]:
    if not isinstance(N, int) or N <= 0:
        raise ValueError("N must be a positive integer")
    _validate_k(h)
    return set(range(h * (N - 1) + 1))
