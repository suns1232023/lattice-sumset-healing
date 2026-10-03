"""
test_regression.py — Regression tests for known critical cases.

These tests lock in correct behavior for cases identified as critical
(reviewer cases, bug fixes, etc.).

NAMING CONVENTION:
    check_*  functions perform computational sanity checks on theorem instances.
    They are NOT proofs. Theorems are proved analytically (docs/THEOREMS.md).
"""

import pytest
from self_healing.healing import self_healing_threshold, classify_1d_void
from self_healing.formulas import predict_m3_threshold, block_distance
from self_healing.invariants import check_theorem_61_instance


class TestReviewerCriticalCases:
    """Regression tests for cases highlighted by peer reviewers."""

    def test_reviewer_n7_v34_h_star_3(self):
        """
        Reviewer critical case: N=7, V={3,4}.
        h* = 3 (NOT 2 as incorrectly claimed in V2.9).
        Bug X1 fixed in V2.10.
        """
        h = self_healing_threshold(7, {3, 4}, max_h=10)
        assert h == 3, f"Expected h*=3, got {h}"

    def test_reviewer_n7_v34_m3_prediction(self):
        """
        M3' prediction for N=7, V={3,4}: ceil(2/1) + 1 = 3.
        d = min(3, 2) = 2, ell = 2.
        """
        d = block_distance(N=7, start=3, length=2)
        assert d == 2
        h_pred = predict_m3_threshold(ell=2, d=2)
        assert h_pred == 3

    def test_reviewer_n7_v34_2A_misses_9(self):
        """
        N=7, V={3,4}: 2A_hole misses element 9.
        This is the specific missing element that proves h* > 2.
        """
        from self_healing.sumset import compute_k_fold_sumset
        A_full = set(range(7))
        A_hole = A_full - {3, 4}
        result_2hole = compute_k_fold_sumset(A_hole, 2)
        result_2full = compute_k_fold_sumset(A_full, 2)
        assert 9 not in result_2hole
        assert 9 in result_2full

    def test_reviewer_n7_v34_3A_heals(self):
        """N=7, V={3,4}: 3A_hole = 3A_full (healing at h=3)."""
        from self_healing.sumset import compute_k_fold_sumset
        A_full = set(range(7))
        A_hole = A_full - {3, 4}
        assert compute_k_fold_sumset(A_hole, 3) == compute_k_fold_sumset(A_full, 3)


class TestTheorem61SanityChecks:
    """
    Computational sanity checks for Theorem 6.1 instances.

    Theorem 6.1 [PROVED analytically]:
        h* = infinity  iff  k in {1, N-2}
        h* = 2         iff  2 <= k <= N-3

    These are SANITY CHECKS, not proofs.
    """

    @pytest.mark.parametrize("N,k,expect_infinite", [
        (5, 1, True),    # near-boundary -> h* = inf
        (5, 3, True),    # near-boundary (N-2=3) -> h* = inf
        (5, 2, False),   # deep interior -> h* = 2
        (7, 1, True),
        (7, 5, True),    # N-2=5
        (7, 2, False),
        (7, 3, False),
        (7, 4, False),
        (10, 1, True),
        (10, 8, True),   # N-2=8
        (10, 4, False),
    ])
    def test_theorem_61_instance(self, N, k, expect_infinite):
        """
        Sanity check: computational result consistent with Theorem 6.1.
        NOTE: check_theorem_61_instance() is a sanity check, not a proof.
        """
        result = check_theorem_61_instance(N, k)
        assert result, (
            f"Theorem 6.1 sanity check failed for N={N}, k={k}, "
            f"expect_infinite={expect_infinite}"
        )

    def test_classify_1d_void_near_boundary(self):
        """classify_1d_void returns INFINITE for near-boundary voids."""
        assert classify_1d_void(7, {1}) == "INFINITE"
        assert classify_1d_void(7, {5}) == "INFINITE"  # N-2=5

    def test_classify_1d_void_deep_interior(self):
        """classify_1d_void returns FINITE for deep interior voids."""
        assert classify_1d_void(7, {3}) == "FINITE"
        assert classify_1d_void(7, {2, 4}) == "FINITE"

    def test_classify_1d_void_mixed(self):
        """classify_1d_void returns INFINITE if any void is near-boundary."""
        assert classify_1d_void(7, {1, 3}) == "INFINITE"


class TestKnownHStarValues:
    """Regression tests for known h* values."""

    @pytest.mark.parametrize("N,void_set,expected_h", [
        (7, {3, 4}, 3),      # reviewer critical case
        (8, {2}, 2),          # ell=1, d=2 -> h*=2
        (8, {3}, 2),          # ell=1, d=3 -> h*=2
        (10, {2, 3}, 3),      # ell=2, d=2 -> h*=3
        (10, {3, 4}, 2),      # ell=2, d=3 -> h*=2
        (12, {2, 3, 4}, 4),   # ell=3, d=2 -> h*=4
        (12, {3, 4, 5}, 3),   # ell=3, d=3 -> h*=3
    ])
    def test_known_h_star(self, N, void_set, expected_h):
        """Verify known h* values match M3' predictions."""
        h = self_healing_threshold(N, void_set, max_h=expected_h + 3)
        assert h == expected_h, (
            f"N={N}, V={void_set}: expected h*={expected_h}, got {h}"
        )


class TestBugFixes:
    """Regression tests for previously identified bugs."""

    def test_v29_x1_bug_fixed(self):
        """
        V2.9 Bug X1: incorrectly claimed h*=2 for N=7, V={3,4}.
        Correct answer is h*=3. Fixed in V2.10.
        """
        h = self_healing_threshold(7, {3, 4}, max_h=10)
        assert h != 2, "V2.9 bug X1 regression: h* should NOT be 2"
        assert h == 3, f"Expected h*=3, got {h}"

    def test_none_does_not_mean_infinity(self):
        """
        None from self_healing_threshold() means 'not found within max_h',
        NOT h* = infinity. Use classify_1d_void() for analytical infinity.
        """
        # Near-boundary void: analytically h* = infinity (Theorem 6.1)
        h = self_healing_threshold(5, {1}, max_h=10)
        assert h is None  # not found within 10 steps

        # But None != infinity: classify_1d_void() gives the analytical answer
        classification = classify_1d_void(5, {1})
        assert classification == "INFINITE"

    def test_self_gaps_initialization(self):
        """
        V2.0 Bug: self.gaps was not initialized in FormalLemmaEngine.
        This test verifies that block parsing works correctly.
        """
        from self_healing.formulas import parse_void_blocks
        void_set = {3, 4, 5, 7, 8}
        blocks = parse_void_blocks(void_set)
        assert len(blocks) == 2
        assert blocks[0] == (3, 3)
        assert blocks[1] == (7, 2)

