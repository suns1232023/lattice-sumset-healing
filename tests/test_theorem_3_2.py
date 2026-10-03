"""
test_theorem_3_2.py — Computational sanity checks for Theorem 3.2.

Theorem 3.2 [PROVED analytically]: For d >= 2, N_i >= 3, A_full = prod{0,...,N_i-1},
and any non-empty strictly interior void V_void, h* = 2.

These tests perform COMPUTATIONAL SANITY CHECKS on specific instances.
They are NOT proofs of the theorem (which is proved analytically).

IMPORTANT: In the Dispersed Corner Decomposition tests:
    - p is a point in 2A_full (the 2-fold sumset), NOT in A_full.
    - For dims=(4,4): A_full = {0,1,2,3}^2, 2A_full = {0,...,6}^2.
    - p=(4,4) is in 2A_full (4 <= 2*(4-1)=6), not in A_full.
    - The Case 2b condition is: N_i-1 < p_i < 2*(N_i-1), i.e., 3 < 4 < 6. ✓
"""

import itertools
import pytest
from self_healing.healing import self_healing_threshold_nd
from self_healing.invariants import generate_case2b_witness
from self_healing.sumset import compute_k_fold_sumset_nd


def get_interior_points(dims):
    """Get strictly interior points of a rectangular box."""
    return {
        p for p in itertools.product(*[range(d) for d in dims])
        if all(0 < p[i] < dims[i] - 1 for i in range(len(dims)))
    }


class TestTheorem32_2D:
    """Computational sanity checks for Theorem 3.2 in 2D."""

    @pytest.mark.parametrize("dims", [
        (3, 3), (4, 3), (4, 4), (5, 3), (5, 5), (6, 4),
    ])
    def test_single_interior_void_heals_at_h2(self, dims):
        """
        Sanity check: h* = 2 for each single interior void in 2D boxes.
        Theorem 3.2 [PROVED analytically] guarantees this for all d >= 2.
        """
        interior = get_interior_points(dims)
        if not interior:
            pytest.skip(f"No interior points for dims={dims}")
        for void_pt in interior:
            h = self_healing_threshold_nd(dims, {void_pt}, max_h=5)
            assert h == 2, (
                f"Theorem 3.2 sanity check failed: dims={dims}, void={void_pt}, h*={h}"
            )

    def test_3x3_center_void(self):
        """3x3 box with center (1,1) removed: h* = 2."""
        h = self_healing_threshold_nd((3, 3), {(1, 1)}, max_h=5)
        assert h == 2

    def test_4x4_multiple_voids(self):
        """4x4 box with multiple interior voids: h* = 2."""
        h = self_healing_threshold_nd((4, 4), {(1, 1), (1, 2), (2, 1)}, max_h=5)
        assert h == 2

    def test_2fold_equality_direct(self):
        """Direct check: 2A_hole = 2A_full for 3x3 box."""
        dims = (3, 3)
        A_full = set(itertools.product(*[range(d) for d in dims]))
        A_hole = A_full - {(1, 1)}
        assert compute_k_fold_sumset_nd(A_hole, 2) == compute_k_fold_sumset_nd(A_full, 2)


class TestTheorem32_3D:
    """Computational sanity checks for Theorem 3.2 in 3D."""

    def test_3x3x3_center_void(self):
        """3x3x3 box with center (1,1,1) removed: h* = 2."""
        h = self_healing_threshold_nd((3, 3, 3), {(1, 1, 1)}, max_h=5)
        assert h == 2

    @pytest.mark.parametrize("dims", [
        (3, 3, 3), (4, 3, 3), (4, 4, 3),
    ])
    def test_all_interior_voids_3d(self, dims):
        """h* = 2 for each single interior void in 3D boxes."""
        interior = get_interior_points(dims)
        if not interior:
            pytest.skip(f"No interior points for dims={dims}")
        for void_pt in interior:
            h = self_healing_threshold_nd(dims, {void_pt}, max_h=5)
            assert h == 2, (
                f"Theorem 3.2 sanity check failed: dims={dims}, void={void_pt}, h*={h}"
            )


class TestTheorem32_4D:
    """Computational sanity checks for Theorem 3.2 in 4D."""

    def test_3x3x3x3_interior_void(self):
        """3x3x3x3 box with interior void: h* = 2."""
        h = self_healing_threshold_nd((3, 3, 3, 3), {(1, 1, 1, 1)}, max_h=5)
        assert h == 2


class TestTheorem32_Necessity_d2:
    """Verify that d >= 2 is necessary (d=1 counterexample)."""

    def test_d1_counterexample(self):
        """
        d=1 counterexample: N=5, V={1}.
        1 not in 2A_hole, so h* > 2.
        This shows d >= 2 is necessary for Theorem 3.2.
        """
        from self_healing.sumset import compute_k_fold_sumset
        N = 5
        A_full = set(range(N))
        A_hole = A_full - {1}
        result_2hole = compute_k_fold_sumset(A_hole, 2)
        result_2full = compute_k_fold_sumset(A_full, 2)
        assert result_2hole != result_2full
        assert 1 not in result_2hole
        assert 1 in result_2full


class TestCase2bWitnessGenerator:
    """
    Tests for the Case 2b Dispersed Corner Decomposition witness generator.

    IMPORTANT: These tests verify that the witness GENERATOR works correctly
    for specific instances. They do NOT prove Theorem 3.2.

    Mathematical note on p values:
        p is a point in 2A_full, NOT in A_full.
        For dims=(4,4): A_full = {0,1,2,3}^2, 2A_full = {0,...,6}^2.
        p=(4,4): satisfies 3 < 4 < 6, so it is in Case 2b of 2A_full. ✓
        p=(4,4) is NOT in A_full (which only goes up to 3).
    """

    def test_case_2b_2d_dims4x4(self):
        """
        Case 2b witness for dims=(4,4), p=(4,4).
        p=(4,4) is in 2A_full (4 <= 2*(4-1)=6), satisfies Case 2b (3 < 4 < 6).
        """
        dims = (4, 4)
        p = (4, 4)  # p in 2A_full, NOT in A_full
        success, decomp = generate_case2b_witness(dims, p)
        assert success, f"Case 2b witness generation failed for dims={dims}, p={p}"
        a_prime, b_prime = decomp
        # Verify sum
        assert tuple(a_prime[i] + b_prime[i] for i in range(2)) == p
        # Verify both in A_full (coords in [0, N_i-1])
        for i in range(2):
            assert 0 <= a_prime[i] <= dims[i] - 1
            assert 0 <= b_prime[i] <= dims[i] - 1

    def test_case_2b_3d_dims4x4x4(self):
        """
        Case 2b witness for dims=(4,4,4), p=(4,4,4).
        p=(4,4,4) is in 2A_full, satisfies Case 2b (3 < 4 < 6).
        """
        dims = (4, 4, 4)
        p = (4, 4, 4)  # p in 2A_full, NOT in A_full
        success, decomp = generate_case2b_witness(dims, p)
        assert success, f"Case 2b witness generation failed for dims={dims}, p={p}"

    def test_case_2b_2d_dims5x5(self):
        """
        Case 2b witness for dims=(5,5), p=(5,5).
        p=(5,5) is in 2A_full (5 <= 2*(5-1)=8), satisfies Case 2b (4 < 5 < 8).
        """
        dims = (5, 5)
        p = (5, 5)  # p in 2A_full, NOT in A_full
        success, decomp = generate_case2b_witness(dims, p)
        assert success

    def test_d1_fails_as_expected(self):
        """d=1: Case 2b witness cannot be generated (d >= 2 required)."""
        dims = (5,)
        p = (4,)
        success, _ = generate_case2b_witness(dims, p)
        assert not success  # d >= 2 required

    def test_boundary_point_not_case2b(self):
        """
        p=(3,3) for dims=(4,4): p_i = N_i-1 = 3, not strictly greater.
        This is Case 2a (pure boundary upper), not Case 2b.
        """
        dims = (4, 4)
        p = (3, 3)  # p_i = N_i-1, not strictly greater -> not Case 2b
        success, _ = generate_case2b_witness(dims, p)
        assert not success  # Case 2b requires p_i > N_i-1

    def test_p_not_in_2A_full_fails(self):
        """
        p=(7,7) for dims=(4,4): p_i=7 > 2*(4-1)=6, not in 2A_full.
        """
        dims = (4, 4)
        p = (7, 7)  # p_i > 2*(N_i-1), not in 2A_full
        success, _ = generate_case2b_witness(dims, p)
        assert not success
