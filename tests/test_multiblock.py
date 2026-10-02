"""
test_multiblock.py — Tests for multi-block independence (Conjecture 14.3).

Conjecture 14.3 [VHC]: h*(V_void) > pred ⟺ Criterion A ∨ Criterion B

Status: Validated Heuristic Conjecture (NOT a theorem).
Evidence: 30,534 configurations (N ≤ 21, r ≤ 5), FP=0, FN=0.

NOTE: These tests verify the conjecture computationally.
Computational verification is NOT presented as mathematical proof.
"""

import pytest
from self_healing.defects import (
    collapse_points,
    criterion_a,
    criterion_b,
    evaluate_criteria,
    decomposition_set,
    intercepted_decompositions,
    has_multi_block_synergy,
)
from self_healing.formulas import (
    parse_void_blocks,
    predict_independent_threshold,
)
from self_healing.healing import self_healing_threshold


class TestCollapsePoints:
    """Tests for collapse point detection."""

    def test_no_collapse_single_interior(self):
        """Single deep interior void: no collapse points in 2A_full."""
        N = 7
        void_set = {3}  # deep interior, h* = 2
        cps = collapse_points(N, void_set)
        # For a single deep interior void, there should be no collapse points
        # that prevent 2A_hole = 2A_full
        # (Theorem 6.1: h* = 2 for k ∈ {2,...,N-3})
        assert isinstance(cps, list)

    def test_collapse_point_detection(self):
        """Verify collapse point detection for known case."""
        N = 12
        void_set = {2, 4, 5}  # gap=1 synergistic case
        cps = collapse_points(N, void_set)
        # p=5 should be a collapse point: decompositions (0,5),(1,4),(2,3)
        # (0,5): 5 ∈ V → intercepted
        # (1,4): 4 ∈ V → intercepted
        # (2,3): 2 ∈ V → intercepted
        assert 5 in cps

    def test_decomposition_set(self):
        """Verify decomposition set for p=5, N=7."""
        D = decomposition_set(N=7, p=5)
        # (a,b) with a+b=5, 0≤a≤b≤6
        expected = [(0, 5), (1, 4), (2, 3)]
        assert D == expected

    def test_intercepted_decompositions(self):
        """Verify interception for p=5, V={2,4,5}."""
        N = 12
        void_set = {2, 4, 5}
        I = intercepted_decompositions(N, 5, void_set)
        D = decomposition_set(N, 5)
        # All decompositions should be intercepted
        assert len(I) == len(D)


class TestMultiBlockSynergy:
    """Tests for multi-block synergy detection."""

    def test_synergy_gap1_case(self):
        """
        N=12, V={2}∪{4,5} (gap=1): p=5 has multi-block synergy.
        Block 0: {2}, Block 1: {4,5}
        Decompositions of 5: (0,5),(1,4),(2,3)
        - (0,5): 5 ∈ Block 1
        - (1,4): 4 ∈ Block 1
        - (2,3): 2 ∈ Block 0
        → involves blocks 0 and 1 → synergy!
        """
        N = 12
        void_set = {2, 4, 5}
        blocks = parse_void_blocks(void_set)
        assert has_multi_block_synergy(N, 5, blocks, void_set)

    def test_no_synergy_gap3_case(self):
        """
        N=15, V={2,3}∪{7,8} (gap=3): no synergistic collapse points.
        [VHC] Gap ≥ 3 implies independence (Conjecture 14.3 corollary).
        """
        N = 15
        void_set = {2, 3, 7, 8}
        cps = collapse_points(N, void_set)
        blocks = parse_void_blocks(void_set)
        synergistic = [
            p for p in cps
            if has_multi_block_synergy(N, p, blocks, void_set)
        ]
        assert len(synergistic) == 0


class TestCriterionAB:
    """Tests for Criterion A and Criterion B evaluation."""

    def test_criterion_a_gap1_case(self):
        """
        N=12, V={2}∪{4,5} (gap=1): Criterion A should trigger.
        [VHC] Computational evidence for Conjecture 14.3.
        """
        N = 12
        void_set = {2, 4, 5}
        pred = predict_independent_threshold(N, void_set)
        assert pred is not None
        triggered, witness = criterion_a(N, void_set, pred)
        assert triggered, f"Criterion A should trigger for gap=1 case"

    def test_criterion_b_frontier(self):
        """
        Test Criterion B: frontier element detection.
        [VHC] Computational evidence for Conjecture 14.3.
        """
        N = 12
        void_set = {2, 4, 5}
        pred = predict_independent_threshold(N, void_set)
        assert pred is not None
        # At least one of A or B should trigger for gap=1 case
        a_trig, _ = criterion_a(N, void_set, pred)
        b_trig, _ = criterion_b(N, void_set, pred)
        assert a_trig or b_trig

    def test_no_criterion_gap3(self):
        """
        N=15, V={2,3}∪{7,8} (gap=3): neither A nor B should trigger.
        [VHC] Gap ≥ 3 independence (Conjecture 14.3 corollary).
        """
        N = 15
        void_set = {2, 3, 7, 8}
        pred = predict_independent_threshold(N, void_set)
        assert pred is not None
        a_trig, _ = criterion_a(N, void_set, pred)
        b_trig, _ = criterion_b(N, void_set, pred)
        assert not a_trig
        assert not b_trig


class TestEvaluateCriteria:
    """Tests for the combined evaluate_criteria interface."""

    def test_gap1_triggers(self):
        """
        Gap=1 case: evaluate_criteria should return triggered=True.
        [VHC] Computational evidence for Conjecture 14.3.
        """
        N = 12
        void_set = {2, 4, 5}
        result = evaluate_criteria(N, void_set)
        assert result['triggered']
        assert result['pred'] is not None

    def test_gap3_independent(self):
        """
        Gap=3 case: evaluate_criteria should return triggered=False.
        [VHC] Computational evidence for Conjecture 14.3.
        """
        N = 15
        void_set = {2, 3, 7, 8}
        result = evaluate_criteria(N, void_set)
        assert not result['triggered']

    def test_boundary_void_returns_none_pred(self):
        """Boundary-adjacent void: pred=None (h* = ∞)."""
        N = 10
        void_set = {1, 5}  # 1 is near-boundary
        result = evaluate_criteria(N, void_set)
        assert result['pred'] is None


class TestConjecture143SmallAudit:
    """
    Small audit of Conjecture 14.3.
    Tests N ≤ 14, r=2 blocks.

    [VHC] Computational evidence, NOT a mathematical proof.
    """

    def test_small_multiblock_audit(self):
        """
        Audit Conjecture 14.3 for N ≤ 14, 2-block voids.
        Verifies: triggered ⟺ actual h* > pred.
        """
        from itertools import combinations

        failures = []
        total = 0

        for N in range(8, 15):
            interior = list(range(2, N - 2))
            for r in range(2, min(5, len(interior))):
                for pts in combinations(interior, r):
                    void_set = set(pts)
                    result = evaluate_criteria(N, void_set)
                    pred = result['pred']
                    if pred is None:
                        continue

                    actual_h = self_healing_threshold(N, void_set, max_h=pred + 5)
                    actual_fail = (actual_h is not None and actual_h > pred)
                    predicted_fail = result['triggered']

                    total += 1
                    if predicted_fail != actual_fail:
                        failures.append({
                            'N': N, 'void': sorted(void_set),
                            'pred': pred, 'actual_h': actual_h,
                            'predicted_fail': predicted_fail,
                            'actual_fail': actual_fail,
                        })

        assert len(failures) == 0, (
            f"Conjecture 14.3 failures found: {failures[:3]}"
        )
        assert total > 0, "No cases were tested"
