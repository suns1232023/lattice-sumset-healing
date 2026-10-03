"""Lattice Sumset Healing — computational verification package."""

__version__ = "2.17.0"
__author__ = "Scott Sun"
__orcid__ = "0009-0002-1095-6228"
__osf_doi__ = "10.17605/OSF.IO/CZK8R"

from .sumset import (
    compute_k_fold_sumset,
    compute_k_fold_sumset_bitwise,
    compute_k_fold_sumset_nd,
    bitmask_to_set,
    h_sumset_1d,
    full_interval_sumset,
)
from .healing import (
    self_healing_threshold,
    self_healing_threshold_fast,
    self_healing_threshold_nd,
    classify_1d_void,
)
from .formulas import (
    predict_m3_threshold,
    block_distance,
    predict_m3_from_block,
    parse_void_blocks,
    predict_independent_threshold,
)
from .defects import (
    collapse_points,
    criterion_a,
    criterion_b,
    evaluate_criteria,
)

__all__ = [
    "compute_k_fold_sumset",
    "compute_k_fold_sumset_bitwise",
    "compute_k_fold_sumset_nd",
    "bitmask_to_set",
    "h_sumset_1d",
    "full_interval_sumset",
    "self_healing_threshold",
    "self_healing_threshold_fast",
    "self_healing_threshold_nd",
    "classify_1d_void",
    "predict_m3_threshold",
    "block_distance",
    "predict_m3_from_block",
    "parse_void_blocks",
    "predict_independent_threshold",
    "collapse_points",
    "criterion_a",
    "criterion_b",
    "evaluate_criteria",
]
