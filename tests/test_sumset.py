"""
test_sumset.py — Unit tests for sumset computation engines.

Tests Engine A (pure-set) and Engine B (bitwise) for correctness
and mutual agreement.
"""

import pytest
from self_healing.sumset import (
    compute_k_fold_sumset,
    compute_k_fold_sumset_bitwise,
    compute_k_fold_sumset_nd,
    bitmask_to_set,
    h_sumset_1d,
    full_interval_sumset,
)


class TestEngineA:
    """Tests for Engine A: pure-set reference implementation."""

    def test_k1_identity(self):
        """1-fold sumset is the set itself."""
        A = {0, 1, 3}
        assert compute_k_fold_sumset(A, 1) == A

    def test_k0_zero(self):
        """0-fold sumset is {0}."""
        A = {1, 2, 3}
        assert compute_k_fold_sumset(A, 0) == {0}

    def test_arithmetic_progression(self):
        """AP {0,1,2} + {0,1,2} = {0,1,2,3,4}."""
        A = {0, 1, 2}
        assert compute_k_fold_sumset(A, 2) == {0, 1, 2, 3, 4}

    def test_full_interval_2fold(self):
        """Full interval {0,...,N-1}: 2-fold = {0,...,2(N-1)}."""
        N = 5
        A = set(range(N))
        result = compute_k_fold_sumset(A, 2)
        expected = set(range(2 * (N - 1) + 1))
        assert result == expected

    def test_hole_set_2fold(self):
        """A_hole = {0,2,3,4} (N=5, void={1}): 2A_hole misses 1."""
        A_hole = {0, 2, 3, 4}
        A_full = {0, 1, 2, 3, 4}
        result_hole = compute_k_fold_sumset(A_hole, 2)
        result_full = compute_k_fold_sumset(A_full, 2)
        assert 1 not in result_hole
        assert 1 in result_full

    def test_reviewer_critical_case(self):
        """
        Reviewer critical case: N=7, V={3,4}.
        2A_hole should miss element 9.
        h* = 3 (matches M3' prediction: ⌈2/1⌉ + 1 = 3).
        """
        N = 7
        void_set = {3, 4}
        A_full = set(range(N))
        A_hole = A_full - void_set
        result_2hole = compute_k_fold_sumset(A_hole, 2)
        result_2full = compute_k_fold_sumset(A_full, 2)
        assert 9 not in result_2hole
        assert 9 in result_2full

    def test_3fold_sumset(self):
        """3-fold sumset of {0,1,2} = {0,1,2,3,4,5,6}."""
        A = {0, 1, 2}
        result = compute_k_fold_sumset(A, 3)
        assert result == set(range(7))


class TestEngineB:
    """Tests for Engine B: bitwise implementation."""

    def test_k1_identity(self):
        """1-fold bitwise sumset matches Engine A."""
        A = {0, 1, 3}
        mask = compute_k_fold_sumset_bitwise(A, 1)
        assert bitmask_to_set(mask) == A

    def test_k0_zero(self):
        """0-fold bitwise sumset is {0}."""
        A = {1, 2, 3}
        mask = compute_k_fold_sumset_bitwise(A, 0)
        assert bitmask_to_set(mask) == {0}

    def test_agreement_with_engine_a(self):
        """Engine B agrees with Engine A for various inputs."""
        test_cases = [
            ({0, 1, 2}, 2),
            ({0, 2, 3, 4}, 2),
            ({0, 1, 3, 5}, 3),
            ({0, 2, 4}, 4),
        ]
        for A, k in test_cases:
            result_a = compute_k_fold_sumset(A, k)
            result_b = bitmask_to_set(compute_k_fold_sumset_bitwise(A, k))
            assert result_a == result_b, f"Engines disagree for A={A}, k={k}"

    def test_reviewer_critical_case_bitwise(self):
        """
        Reviewer critical case (N=7, V={3,4}) via Engine B.
        2A_hole should miss element 9.
        """
        N = 7
        void_set = {3, 4}
        A_hole = set(range(N)) - void_set
        mask = compute_k_fold_sumset_bitwise(A_hole, 2)
        result = bitmask_to_set(mask)
        assert 9 not in result


class TestEngineAMultiDimensional:
    """Tests for multi-dimensional Engine A."""

    def test_2d_box_2fold(self):
        """2D box {0,1}×{0,1}: 2-fold = {0,1,2}×{0,1,2}."""
        A = {(0, 0), (1, 0), (0, 1), (1, 1)}
        result = compute_k_fold_sumset_nd(A, 2)
        expected = {(i, j) for i in range(3) for j in range(3)}
        assert result == expected

    def test_3x3_box_with_void(self):
        """3×3 box minus center: 2-fold should equal full 2-fold."""
        import itertools
        A_full = set(itertools.product(range(3), repeat=2))
        A_hole = A_full - {(1, 1)}
        result_full = compute_k_fold_sumset_nd(A_full, 2)
        result_hole = compute_k_fold_sumset_nd(A_hole, 2)
        assert result_hole == result_full  # Theorem 3.2


class TestFullIntervalSumset:
    """Tests for full_interval_sumset helper."""

    def test_h1(self):
        """1-fold of {0,...,N-1} = {0,...,N-1}."""
        assert full_interval_sumset(5, 1) == set(range(5))

    def test_h2(self):
        """2-fold of {0,...,N-1} = {0,...,2(N-1)}."""
        N = 6
        assert full_interval_sumset(N, 2) == set(range(2 * (N - 1) + 1))
