"""
test_theorem_3_2.py — Tests for Theorem 3.2 (Proved, d≥2).

Theorem 3.2 [PROVED]: Let d ≥ 2, N_i ≥ 3, A_full = ∏{0,...,N_i-1},
and ∅ ≠ V_void ⊆ int(A_full). Then 2A_hole = 2A_full and h* = 2.

These tests verify the theorem computationally for small configurations.
The theorem is proved analytically via the Dispersed Corner Decomposition.
"""

import itertools
import pytest
from self_healing.healing import self_healing_threshold_nd
from self_healing.invariants import verify_dispersed_corner_decomposition
from self_healing.sumset import compute_k_fold_sumset_nd


def get_interior_points(dims):
    """Get strictly interior points of a rectangular box."""
    return {
        p for p in itertools.product(*[range(d) for d in dims])
        if all(0 < p[i] < dims[i] - 1 for i in range(len(dims)))
    }


class TestTheorem32_2D:
    """Computational verification of Theorem 3.2 for 2D boxes."""

    @pytest.mark.parametrize("dims", [
        (3, 3), (4, 3), (4, 4), (5, 3), (5, 5), (6, 4),
    ])
    def test_single_interior_void(self, dims):
        """h* = 2 for each single interior void in 2D boxes."""
        interior = get_interior_points(dims)
        if not interior:
            pytest.skip(f"No interior points for dims={dims}")
        for void_pt in interior:
            h = self_healing_threshold_nd(dims, {void_pt}, max_h=5)
            assert h == 2, (
                f"Theorem 3.2 violated: dims={dims}, void={void_pt}, h*={h}"
            )

    def test_3x3_center_void(self):
        """3×3 box with center (1,1) removed: h* = 2."""
        dims = (3, 3)
        void_set = {(1, 1)}
        h = self_healing_threshold_nd(dims, void_set, max_h=5)
        assert h == 2

    def test_4x4_multiple_voids(self):
        """4×4 box with multiple interior voids: h* = 2."""
        dims = (4, 4)
        void_set = {(1, 1), (1, 2), (2, 1)}
        h = self_healing_threshold_nd(dims, void_set, max_h=5)
        assert h == 2

    def test_2fold_equality(self):
        """Direct check: 2A_hole = 2A_full for 3×3 box."""
        dims = (3, 3)
        A_full = set(itertools.product(*[range(d) for d in dims]))
        A_hole = A_full - {(1, 1)}
        result_full = compute_k_fold_sumset_nd(A_full, 2)
        result_hole = compute_k_fold_sumset_nd(A_hole, 2)
        assert result_hole == result_full


class TestTheorem32_3D:
    """Computational verification of Theorem 3.2 for 3D boxes."""

    def test_3x3x3_center_void(self):
        """3×3×3 box with center (1,1,1) removed: h* = 2."""
        dims = (3, 3, 3)
        void_set = {(1, 1, 1)}
        h = self_healing_threshold_nd(dims, void_set, max_h=5)
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
                f"Theorem 3.2 violated: dims={dims}, void={void_pt}, h*={h}"
            )


class TestTheorem32_4D:
    """Computational verification of Theorem 3.2 for 4D boxes."""

    def test_3x3x3x3_interior_void(self):
        """3×3×3×3 box with interior void: h* = 2."""
        dims = (3, 3, 3, 3)
        void_set = {(1, 1, 1, 1)}
        h = self_healing_threshold_nd(dims, void_set, max_h=5)
        assert h == 2


class TestTheorem32_Necessity_d2:
    """Verify that d ≥ 2 is necessary (d=1 counterexample)."""

    def test_d1_counterexample(self):
        """
        d=1 counterexample: N=5, V={1}.
        1 ∉ 2A_hole, so h* > 2 (in fact h* = ∞).
        This shows d ≥ 2 is necessary.
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


class TestDispersedCornerDecomposition:
    """Tests for the Dispersed Corner Decomposition (proof mechanism)."""

    def test_case_2b_2d(self):
        """Case 2b: strictly interior upper point in 2D."""
        dims = (4, 4)
        # p = (4, 4) = (N_1-1 + c_1, N_2-1 + c_2) with c_1=c_2=1
        p = (4, 4)
        success, decomp = verify_dispersed_corner_decomposition(dims, p)
        assert success
        a_prime, b_prime = decomp
        assert tuple(a_prime[i] + b_prime[i] for i in range(2)) == p

    def test_case_2b_3d(self):
        """Case 2b: strictly interior upper point in 3D."""
        dims = (4, 4, 4)
        p = (4, 4, 4)
        success, decomp = verify_dispersed_corner_decomposition(dims, p)
        assert success

    def test_d1_fails(self):
        """d=1 case: Dispersed Corner Decomposition cannot be applied."""
        dims = (5,)
        p = (4,)
        success, _ = verify_dispersed_corner_decomposition(dims, p)
        assert not success  # d ≥ 2 required
