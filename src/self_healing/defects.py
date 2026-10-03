"""Collapse points and Criterion A/B for Conjecture 14.3."""

from __future__ import annotations
from typing import Dict, List, Optional, Set, Tuple
from .sumset import compute_k_fold_sumset
from .formulas import parse_void_blocks, predict_independent_threshold


def decomposition_set(N: int, p: int) -> List[Tuple[int, int]]:
    if N <= 0:
        raise ValueError("N must be positive")
    lo, hi = max(0, p - (N - 1)), min(N - 1, p)
    return [(a, p - a) for a in range(lo, hi + 1) if a <= p - a]


def intercepted_decompositions(
    N: int, p: int, void_set: Set[int]
) -> List[Tuple[int, int]]:
    V = set(void_set)
    return [
        (a, b) for a, b in decomposition_set(N, p)
        if a in V or b in V
    ]


def collapse_points(N: int, void_set: Set[int]) -> List[int]:
    result = []
    for p in range(2 * (N - 1) + 1):
        D = decomposition_set(N, p)
        if D and len(D) == len(intercepted_decompositions(N, p, void_set)):
            result.append(p)
    return result


def build_block_map(blocks: List[Tuple[int, int]]) -> Dict[int, int]:
    return {
        e: i
        for i, (s, length) in enumerate(blocks)
        for e in range(s, s + length)
    }


def has_multi_block_synergy(
    N: int, p: int, blocks: List[Tuple[int, int]], void_set: Set[int]
) -> bool:
    block_map = build_block_map(blocks)
    D = decomposition_set(N, p)
    I = intercepted_decompositions(N, p, void_set)
    if len(D) != len(I):
        return False
    involved = set()
    for a, b in I:
        if a in block_map:
            involved.add(block_map[a])
        if b in block_map:
            involved.add(block_map[b])
    return len(involved) >= 2


def criterion_a(
    N: int, void_set: Set[int], pred: int
) -> Tuple[bool, Optional[int]]:
    blocks = parse_void_blocks(void_set)
    Hpred = compute_k_fold_sumset(set(range(N)) - set(void_set), pred)
    for p in collapse_points(N, void_set):
        if p <= pred * (N - 1) and p not in Hpred:
            if has_multi_block_synergy(N, p, blocks, void_set):
                return True, p
    return False, None


def criterion_b(
    N: int, void_set: Set[int], pred: int
) -> Tuple[bool, Optional[int]]:
    A_full = set(range(N))
    H = A_full - set(void_set)
    Hpred = compute_k_fold_sumset(H, pred)
    Fpred = compute_k_fold_sumset(A_full, pred)
    Fprev = compute_k_fold_sumset(A_full, pred - 1) if pred > 1 else {0}
    for p in sorted(Fpred - Fprev):
        if p not in Hpred:
            return True, p
    return False, None


def evaluate_criteria(N: int, void_set: Set[int]) -> Dict:
    pred = predict_independent_threshold(N, set(void_set))
    if pred is None:
        return {
            "pred": None, "criterion_a": False, "criterion_b": False,
            "triggered": False, "witness_a": None, "witness_b": None,
            "note": "boundary-adjacent void: analytical classification may be infinite",
        }
    a_trig, wa = criterion_a(N, set(void_set), pred)
    b_trig, wb = criterion_b(N, set(void_set), pred)
    return {
        "pred": pred,
        "criterion_a": a_trig,
        "criterion_b": b_trig,
        "triggered": a_trig or b_trig,
        "witness_a": wa,
        "witness_b": wb,
    }
