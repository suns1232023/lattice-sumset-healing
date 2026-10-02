"""
Additive Self-Healing in Lattice Sumsets with Interior Voids
============================================================

Research verification package for studying h*(A_hole; A_full).

Mathematical question:
    h*(A_hole; A_full) = min{h >= 1 : hA_hole = hA_full}

Research status (Version 2.17):
    Theorem 3.2  [PROVED]: h* = 2 for rectangular boxes, d >= 2
    Theorem 6.1  [PROVED]: d=1 single-void exact classification
    Theorem 7.1  [PROVED]: d=1 multi-void exact classification
    Conjecture M3' [VHC]: h*(ell,d) = ceil(ell/(d-1)) + 1
    Conjecture 14.3 [VHC]: Multi-block independence criterion

OSF Research Record: https://osf.io/czk8r/
Author ORCID: 0009-0002-1095-6228
"""

__version__ = "2.17.0"
__author__ = "Scott Sun"
__orcid__ = "0009-0002-1095-6228"
__osf_doi__ = "10.17605/OSF.IO/CZK8R"

from .sumset import compute_k_fold_sumset, compute_k_fold_sumset_bitwise, h_sumset_1d
from .healing import self_healing_threshold, self_healing_threshold_fast, classify_1d_void
from .formulas import predict_m3_threshold, block_distance, predict_independent_threshold
from .defects import collapse_points, criterion_a, criterion_b, evaluate_criteria

__all__ = [
    "compute_k_fold_sumset",
    "compute_k_fold_sumset_bitwise",
    "h_sumset_1d",
    "self_healing_threshold",
    "self_healing_threshold_fast",
    "classify_1d_void",
    "predict_m3_threshold",
    "block_distance",
    "predict_independent_threshold",
    "collapse_points",
    "criterion_a",
    "criterion_b",
    "evaluate_criteria",
]
