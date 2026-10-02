"""
defects.py — Collapse points, Criterion A, Criterion B (Conjecture 14.3).

Conjecture 14.3 [VHC]:
    h*(V_void) > pred  iff  Criterion A  or  Criterion B

Definitions:
    Collapse Point: p in 2A_full where every decomposition (a,b) with
        a+b=p is intercepted by V_void (a in V or b in V).
    Multi-Block Synergy: collapse point whose intercepted decompositions
        involve elements from >= 2 distinct void blocks.
    Criterion A: exists synergistic collapse point p not in pred*H.
    Criterion B: exists p in pred*A_full \\ (pred-1)*A_full, p not in pred*H.

Status: VHC — 875,658 configurations, FP=0, FN=0. NOT a proof.
"""

from __future__ import annotations
from typing import Dict, List, Optional, Set, Tuple

from .sumset import compute_k_fold_sumset
from .formulas import parse_void_blocks, predict_independent_threshold


def decomposition_set(N: int, p: int) -> List[Tuple[int, int]]:
    """All unordered (a,b) with a+b=p, a,b in {0,...,N-1}, a<=b."""
    lo, hi = max(0, p - (N - 1)), min(N - 1, p)
    return [(a, p - a) for a in range(lo, hi + 1) if a <= p - a]


def intercepted_decompositions(
    N: int, p: int, void_set: Set[int]
) -> List[Tuple[int, int]]:
    """Decompositions of p intercepted by void_set (a in V or b in V)."""
    return [(a, b) for a, b in decomposition_set(N, p)
            if a in void_set or b in void_set]


def collapse_points(N: int, void_set: Set[int]) -> List[int]:
    """Find all collapse points: p where every decomposition is intercepted."""
    result = []
    for p in range(2 * (N - 1) + 1):
        D = decomposition_set(N, p)
        if D and len(D) == len(intercepted_decompositions(N, p, void_set)):
            result.append(p)
    return result


def build_block_map(blocks: List[Tuple[int, int]]) -> Dict[int, int]:
    """Map element -> block_index."""
    return {e: i for i, (s, l) in enumerate(blocks) for e in range(s, s + l)}


def has_multi_block_synergy(
    N: int,
    p: int,
    blocks: List[Tuple[int, int]],
    void_set: Set[int],
) -> bool:
    """Check if collapse point p involves elements from >= 2 distinct blocks."""
    block_map = build_block_map(blocks)
    D = decomposition_set(N, p)
    I = intercepted_decompositions(N, p, void_set)
    if len(D) != len(I):
        return False  # not a collapse point
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
    """
    Criterion A: exists synergistic collapse point p not in pred*H.
    Returns (triggered, witness_p).
    """
    blocks = parse_void_blocks(void_set)
    Hpred = compute_k_fold_sumset(set(range(N)) - void_set, pred)
    for p in collapse_points(N, void_set):
        if p <= pred * (N - 1) and p not in Hpred:
            if has_multi_block_synergy(N, p, blocks, void_set):
                return True, p
    return False, None


def criterion_b(
    N: int, void_set: Set[int], pred: int
) -> Tuple[bool, Optional[int]]:
    """
    Criterion B: exists p in pred*A_full \\ (pred-1)*A_full, p not in pred*H.
    Returns (triggered, witness_p).
    """
    A_full = set(range(N))
    H = A_full - void_set
    Hpred = compute_k_fold_sumset(H, pred)
    Fpred = compute_k_fold_sumset(A_full, pred)
    Fprev = compute_k_fold_sumset(A_full, pred - 1) if pred > 1 else {0}
    for p in sorted(Fpred - Fprev):
        if p not in Hpred:
            return True, p
    return False, None


def evaluate_criteria(N: int, void_set: Set[int]) -> Dict:
    """
    Primary interface for Conjecture 14.3 verification.

    Returns dict with keys: pred, criterion_a, criterion_b,
    triggered, witness_a, witness_b.

    NOTE: This implements an open conjecture. Results are
    computational evidence, NOT mathematical proof.
    """
    pred = predict_independent_threshold(N, void_set)
    if pred is None:
        return {
            'pred': None,
            'criterion_a': False, 'criterion_b': False,
            'triggered': False,
            'witness_a': None, 'witness_b': None,
            'note': 'boundary-adjacent void: h* = inf',
        }
    a_trig, wa = criterion_a(N, void_set, pred)
    b_trig, wb = criterion_b(N, void_set, pred)
    return {
        'pred': pred,
        'criterion_a': a_trig, 'criterion_b': b_trig,
        'triggered': a_trig or b_trig,
        'witness_a': wa, 'witness_b': wb,
    }
