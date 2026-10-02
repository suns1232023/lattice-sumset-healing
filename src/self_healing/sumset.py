"""
sumset.py — Three independent sumset computation engines.

Engine A (Reference Set):  Pure Python set operations — mathematical reference.
Engine B (Bitwise):        Integer bit-shift — fast exhaustive audit (~100x faster).
Engine C (Formula):        Direct formula — conjecture audit (instant).

Agreement between all three provides cross-validation.
Disagreement signals a bug.

Mathematical definition:
    hA = {a_1 + ... + a_h : a_i in A}  (h-fold Minkowski sum)
"""

from __future__ import annotations
from typing import Set, Tuple


# ── Engine A: Pure-Set Reference ─────────────────────────────────────────────

def compute_k_fold_sumset(A: Set[int], k: int) -> Set[int]:
    """
    Engine A — pure-set reference implementation.
    Ground-truth: intentionally unoptimized for clarity and correctness.

    Examples:
        >>> compute_k_fold_sumset({0, 1, 2}, 2)
        {0, 1, 2, 3, 4}
        >>> compute_k_fold_sumset({0, 2, 3, 4}, 2)  # N=5, void={1}
        {0, 2, 3, 4, 5, 6, 7, 8}
    """
    if k == 0:
        return {0}
    if k == 1:
        return set(A)
    current = set(A)
    for _ in range(2, k + 1):
        current = {x + a for x in current for a in A}
    return current


def compute_k_fold_sumset_nd(A: Set[Tuple[int, ...]], k: int) -> Set[Tuple[int, ...]]:
    """Engine A (multi-dimensional) — for Theorem 3.2 verification."""
    if not A:
        return set()
    d = len(next(iter(A)))
    if k == 0:
        return {tuple(0 for _ in range(d))}
    if k == 1:
        return set(A)
    current = set(A)
    for _ in range(2, k + 1):
        current = {
            tuple(x[i] + a[i] for i in range(d))
            for x in current for a in A
        }
    return current


# ── Engine B: Bitwise ─────────────────────────────────────────────────────────

def compute_k_fold_sumset_bitwise(A: Set[int], k: int) -> int:
    """
    Engine B — bitwise implementation (1D only).
    Represents sumset as bitmask: bit i set iff i in kA.
    ~100x faster than Engine A for large exhaustive audits.
    """
    if k == 0:
        return 1  # {0}
    A_list = sorted(A)
    current = sum(1 << a for a in A_list)
    for _ in range(k - 1):
        nxt = 0
        for a in A_list:
            nxt |= (current << a)
        current = nxt
    return current


def bitmask_to_set(mask: int) -> Set[int]:
    """Convert bitmask back to Python set."""
    result, pos = set(), 0
    while mask:
        if mask & 1:
            result.add(pos)
        mask >>= 1
        pos += 1
    return result


# ── Convenience ───────────────────────────────────────────────────────────────

def h_sumset_1d(A: Set[int], h: int) -> Set[int]:
    """Primary 1D interface (Engine A)."""
    return compute_k_fold_sumset(A, h)


def full_interval_sumset(N: int, h: int) -> Set[int]:
    """h * {0,...,N-1} = {0,...,h*(N-1)}."""
    return set(range(h * (N - 1) + 1))
