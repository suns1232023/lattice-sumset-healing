"""
formulas.py — Conjecture M3' formula (Engine C) and related predictors.

Conjecture M3' [VHC]:
    h*(ell, d) = ceil(ell / (d-1)) + 1   for d >= 2

    where d = min(left_distance, right_distance), 0-based indexing:
        left_distance  = start
        right_distance = (N-1) - (start + length - 1)
        d = min(left_distance, right_distance)

Status: VHC — 4,640 cases verified (N<=35, ell<=15, d>=2).
        Three-engine cross-audit: pure-set, bitwise, formula — all agree.
        NOT a mathematical proof.
"""

from __future__ import annotations
import math
from typing import List, Optional, Tuple


def block_distance(N: int, start: int, length: int) -> int:
    """
    Compute boundary distance d using 0-based indexing.
    d = min(left_distance, right_distance)

    Examples:
        >>> block_distance(7, 3, 2)   # V={3,4}, N=7: min(3, 2) = 2
        2
        >>> block_distance(10, 2, 3)  # V={2,3,4}: min(2, 6) = 2
        2
    """
    left_dist = start
    right_dist = (N - 1) - (start + length - 1)
    return min(left_dist, right_dist)


def predict_m3_threshold(ell: int, d: int) -> Optional[int]:
    """
    Engine C — Conjecture M3' formula.
    h*(ell, d) = ceil(ell / (d-1)) + 1  for d >= 2.
    Returns None if d <= 1 (boundary-adjacent void, h* = inf).

    Examples:
        >>> predict_m3_threshold(2, 2)   # ceil(2/1) + 1 = 3
        3
        >>> predict_m3_threshold(3, 3)   # ceil(3/2) + 1 = 3
        3
        >>> predict_m3_threshold(4, 2)   # ceil(4/1) + 1 = 5
        5
    """
    if d <= 1:
        return None
    return math.ceil(ell / (d - 1)) + 1


def predict_m3_from_block(N: int, start: int, length: int) -> Optional[int]:
    """Predict h* for a single void block (convenience wrapper)."""
    d = block_distance(N, start, length)
    return predict_m3_threshold(length, d)


def parse_void_blocks(void_set: set) -> List[Tuple[int, int]]:
    """
    Parse void set into list of (start, length) consecutive blocks.

    Examples:
        >>> parse_void_blocks({2, 3, 5, 6, 7})
        [(2, 2), (5, 3)]
    """
    if not void_set:
        return []
    sorted_void = sorted(void_set)
    blocks = []
    start = prev = sorted_void[0]
    for x in sorted_void[1:]:
        if x == prev + 1:
            prev = x
        else:
            blocks.append((start, prev - start + 1))
            start = prev = x
    blocks.append((start, prev - start + 1))
    return blocks


def predict_independent_threshold(N: int, void_set: set) -> Optional[int]:
    """
    pred = max_i h*_i (independence assumption for Conjecture 14.3).
    Returns None if any block has d <= 1 (boundary-adjacent).
    """
    blocks = parse_void_blocks(void_set)
    if not blocks:
        return 1
    preds = [predict_m3_from_block(N, s, l) for s, l in blocks]
    return None if None in preds else max(preds)


def verify_m3_algebraic_identity(ell: int, d: int) -> bool:
    """
    Verify (h-1)(d-1) >= ell > (h-2)(d-1).
    This is a definition-level algebraic identity, NOT an empirical claim.
    """
    if d <= 1:
        return True
    h = predict_m3_threshold(ell, d)
    if h is None:
        return True
    return (h - 1) * (d - 1) >= ell > (h - 2) * (d - 1)
