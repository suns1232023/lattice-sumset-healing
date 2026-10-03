"""Conjecture M3' formulas and structural helpers."""

from __future__ import annotations
import math
from typing import List, Optional, Tuple


def block_distance(N: int, start: int, length: int) -> int:
    if not all(isinstance(x, int) for x in (N, start, length)):
        raise ValueError("N, start and length must be integers")
    if N <= 0 or length <= 0 or start < 0 or start + length > N:
        raise ValueError("void block must lie inside {0,...,N-1}")
    left_dist = start
    right_dist = (N - 1) - (start + length - 1)
    return min(left_dist, right_dist)


def predict_m3_threshold(ell: int, d: int) -> Optional[int]:
    """M3' predictor: ceil(ell/(d-1))+1 for d>=2."""
    if not isinstance(ell, int) or not isinstance(d, int):
        raise ValueError("ell and d must be integers")
    if ell <= 0:
        raise ValueError("ell must be positive")
    if d <= 1:
        return None
    return math.ceil(ell / (d - 1)) + 1


def predict_m3_from_block(N: int, start: int, length: int) -> Optional[int]:
    return predict_m3_threshold(length, block_distance(N, start, length))


def parse_void_blocks(void_set: set) -> List[Tuple[int, int]]:
    if not void_set:
        return []
    values = sorted(void_set)
    blocks: List[Tuple[int, int]] = []
    start = prev = values[0]
    for x in values[1:]:
        if x == prev + 1:
            prev = x
        else:
            blocks.append((start, prev - start + 1))
            start = prev = x
    blocks.append((start, prev - start + 1))
    return blocks


def predict_independent_threshold(N: int, void_set: set) -> Optional[int]:
    blocks = parse_void_blocks(void_set)
    if not blocks:
        return 1
    preds = [predict_m3_from_block(N, s, l) for s, l in blocks]
    return None if any(p is None for p in preds) else max(preds)


def verify_m3_algebraic_identity(ell: int, d: int) -> bool:
    if d <= 1:
        return True
    h = predict_m3_threshold(ell, d)
    if h is None:
        return True
    return (h - 1) * (d - 1) >= ell > (h - 2) * (d - 1)
