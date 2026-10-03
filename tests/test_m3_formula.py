"""
test_m3_formula.py — Tests for Conjecture M3' formula.

Conjecture M3' [VHC]: h*(ell, d) = ceil(ell/(d-1)) + 1

Status: Validated Heuristic Conjecture (NOT a theorem).
Verified for 4,640 cases (N <= 35, ell <= 15, d >= 2).

NAMING NOTE:
    Engine A = pure-set (exact h*)
    Engine B = bitwise (exact h*, independent)
    Engine C = M3' predictor (conjecture, NOT independent exact computation)
    check_abc_agreement_single_block() checks A, B, and C agree.
"""

import pytest
from self_healing.formulas import (
    predict_m3_threshold,
    block_distance,
    predict_m3_from_block,
    verify_m3_algebraic_identity,
)
from self_healing.healing import (
    self_healing_threshold,
    self_healing_threshold_fast,
)
from self_healing.invariants import check_abc_agreement_single_block


class TestBlockDistance:
    """Tests for boundary distance computation."""

    def test_reviewer_critical_case(self):
        """N=7, V={3,4}: d = min(3, 2) = 2."""
        d = block_distance(N=7, start=3, length=2)
        assert d == 2

    def test_symmetric_block(self):
        """N=9, V={3,4,5}: left=3, right=9-1-5=3, d=3."""
        d = block_distance(N=9, start=3, length=3)
        assert d == 3

    def test_left_closer(self):
        """N=10, V={2,3}: left=2, right=10-1-3=6, d=2."""
        d = block_distance(N=10, start=2, length=2)
        assert d == 2

    def test_right_closer(self):
        """N=10, V={6,7}: left=6, right=10-1-7=2, d=2."""
        d = block_distance(N=10, start=6, length=2)
        assert d == 2


class TestM3Formula:
    """Tests for Conjecture M3' formula predictions."""

    def test_reviewer_critical_case(self):
        """N=7, V={3,4}: ell=2, d=2: h* = ceil(2/1) + 1 = 3."""
        h_pred = predict_m3_threshold(ell=2, d=2)
        assert h_pred == 3

    def test_ell1_d2(self):
        """ell=1, d=2: h* = ceil(1/1) + 1 = 2."""
        assert predict_m3_threshold(1, 2) == 2

    def test_ell3_d2(self):
        """ell=3, d=2: h* = ceil(3/1) + 1 = 4."""
        assert predict_m3_threshold(3, 2) == 4

    def test_ell3_d3(self):
        """ell=3, d=3: h* = ceil(3/2) + 1 = 3."""
        assert predict_m3_threshold(3, 3) == 3

    def test_ell4_d3(self):
        """ell=4, d=3: h* = ceil(4/2) + 1 = 3."""
        assert predict_m3_threshold(4, 3) == 3

    def test_ell5_d3(self):
        """ell=5, d=3: h* = ceil(5/2) + 1 = 4."""
        assert predict_m3_threshold(5, 3) == 4

    def test_boundary_void_returns_none(self):
        """d=1 (boundary-adjacent): formula returns None."""
        assert predict_m3_threshold(3, 1) is None
        assert predict_m3_threshold(1, 0) is None


class TestM3AlgebraicIdentity:
    """Tests for the algebraic identity underlying M3'."""

    @pytest.mark.parametrize("ell,d", [
        (1, 2), (2, 2), (3, 2), (4, 2),
        (1, 3), (2, 3), (3, 3), (4, 3), (5, 3),
        (1, 4), (3, 4), (6, 4),
        (2, 5), (4, 5), (8, 5),
    ])
    def test_algebraic_identity(self, ell, d):
        """
        Verify (h-1)(d-1) >= ell > (h-2)(d-1) for all tested (ell, d).
        This is a definition-level algebraic identity, not an empirical claim.
        """
        assert verify_m3_algebraic_identity(ell, d), (
            f"Algebraic identity failed for ell={ell}, d={d}"
        )


class TestABCAgreement:
    """
    A/B/C agreement checks.

    Engine A (pure-set) and Engine B (bitwise) both compute exact h*.
    Engine C (M3' predictor) is the conjecture predictor, NOT independent exact.
    Agreement between A, B, and C provides computational evidence for M3'.

    [VHC] Computational evidence, NOT a mathematical proof.
    """

    def test_reviewer_critical_case_abc(self):
        """
        Reviewer critical case: N=7, V={3,4}.
        A=3 (exact), B=3 (exact), C=3 (M3' predictor). All agree.
        """
        agree, details = check_abc_agreement_single_block(N=7, start=3, length=2)
        assert agree, f"A/B/C disagreement: {details}"
        assert details['h_engine_a_exact'] == 3
        assert details['h_engine_b_exact'] == 3
        assert details['h_m3_predictor'] == 3

    @pytest.mark.parametrize("N,start,length", [
        (7, 3, 2),    # reviewer critical case
        (8, 2, 1),    # ell=1, d=2 -> h*=2
        (8, 3, 2),    # ell=2, d=3 -> h*=2
        (10, 2, 3),   # ell=3, d=2 -> h*=4
        (10, 3, 3),   # ell=3, d=3 -> h*=3
        (12, 2, 4),   # ell=4, d=2 -> h*=5
        (12, 3, 4),   # ell=4, d=3 -> h*=3
        (15, 4, 5),   # ell=5, d=4 -> h*=3
    ])
    def test_abc_agreement(self, N, start, length):
        """
        A/B/C agreement for selected cases.
        [VHC] Computational evidence for Conjecture M3'.
        """
        agree, details = check_abc_agreement_single_block(N=N, start=start, length=length)
        assert agree, (
            f"A/B/C disagreement for N={N}, start={start}, length={length}: {details}"
        )


class TestM3SmallExhaustive:
    """
    Small exhaustive audit of Conjecture M3'.
    Tests all (N, ell, d) with N <= 15, ell <= 8, d >= 2.

    [VHC] Computational evidence, NOT a proof.
    """

    def test_small_exhaustive_audit(self):
        """
        Exhaustive audit for N <= 15, ell <= 8.
        A, B, and C must agree on every case.
        """
        failures = []
        total = 0

        for N in range(5, 16):
            for length in range(1, 9):
                for start in range(1, N - length):
                    d = block_distance(N, start, length)
                    if d < 2:
                        continue
                    agree, details = check_abc_agreement_single_block(N, start, length)
                    total += 1
                    if not agree:
                        failures.append(details)

        assert len(failures) == 0, (
            f"A/B/C disagreements found: {failures[:5]}"
        )
        assert total > 0, "No cases were tested"
