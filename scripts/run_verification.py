"""Master computational audit runner."""

from __future__ import annotations
import argparse
import hashlib
import json
import sys
import time
from itertools import combinations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from self_healing.formulas import block_distance, predict_m3_threshold
from self_healing.healing import self_healing_threshold, self_healing_threshold_fast
from self_healing.defects import evaluate_criteria

PROFILES = {
    "ci":    {"m3": (15, 8),  "mb": (12, 3), "adv": (15, 3)},
    "quick": {"m3": (20, 10), "mb": (15, 4), "adv": (20, 4)},
    "full":  {"m3": (35, 15), "mb": (21, 5), "adv": (35, 5)},
}


def audit_m3(N_max: int, ell_max: int) -> dict:
    total = exact = 0
    for N in range(5, N_max + 1):
        for length in range(1, ell_max + 1):
            for start in range(1, N - length):
                d = block_distance(N, start, length)
                if d < 2:
                    continue
                V = set(range(start, start + length))
                pred = predict_m3_threshold(length, d)
                max_h = pred + 5 if pred is not None else 50
                a = self_healing_threshold(N, V, max_h=max_h)
                b = self_healing_threshold_fast(N, V, max_h=max_h)
                total += 1
                if a == b == pred:
                    exact += 1
    return {
        "conjecture": "M3'",
        "not_a_proof": True,
        "total": total,
        "agreement": exact,
        "failures": total - exact,
        "engines": {
            "A": "pure_set_exact",
            "B": "bitwise_exact",
            "C": "M3_predictor",
        },
    }


def audit_multiblock(N_max: int, max_blocks: int) -> dict:
    total = tp = tn = fp = fn = 0
    for N in range(8, N_max + 1):
        interior = list(range(2, N - 2))
        for r in range(2, min(max_blocks + 1, len(interior) + 1)):
            for pts in combinations(interior, r):
                V = set(pts)
                result = evaluate_criteria(N, V)
                pred = result["pred"]
                if pred is None:
                    continue
                actual_h = self_healing_threshold(N, V, max_h=pred + 5)
                # None means no healing was observed within the declared horizon.
                # For this finite audit it is conservatively classified as a failure
                # of the independent-threshold prediction.
                actual_fail = actual_h is None or actual_h > pred
                predicted_fail = bool(result["triggered"])
                total += 1
                if predicted_fail and actual_fail:
                    tp += 1
                elif predicted_fail and not actual_fail:
                    fp += 1
                elif not predicted_fail and actual_fail:
                    fn += 1
                else:
                    tn += 1
    return {
        "conjecture": "14.3",
        "not_a_proof": True,
        "total": total,
        "tp": tp, "tn": tn, "fp": fp, "fn": fn,
        "failures": fp + fn,
    }


def audit_adversarial(N_max: int, max_blocks: int) -> dict:
    total = failures = 0
    for N in range(8, N_max + 1):
        interior = list(range(2, N - 2))
        for r in range(2, min(max_blocks + 1, len(interior) + 1)):
            for pts in combinations(interior, r):
                V = set(pts)
                sorted_pts = sorted(pts)
                gaps = [
                    sorted_pts[i + 1] - sorted_pts[i] - 1
                    for i in range(len(sorted_pts) - 1)
                ]
                if not gaps or min(gaps) > 1:
                    continue
                result = evaluate_criteria(N, V)
                pred = result["pred"]
                if pred is None:
                    continue
                actual_h = self_healing_threshold(N, V, max_h=pred + 6)
                actual_fail = actual_h is None or actual_h > pred
                if bool(result["triggered"]) != actual_fail:
                    failures += 1
                total += 1
    return {
        "conjecture": "14.3_adversarial",
        "not_a_proof": True,
        "total": total,
        "failures": failures,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", choices=PROFILES, default="quick")
    parser.add_argument("--output-dir", default="results")
    args = parser.parse_args()

    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)
    cfg = PROFILES[args.profile]
    t0 = time.time()

    m3 = audit_m3(*cfg["m3"])
    mb = audit_multiblock(*cfg["mb"])
    adv = audit_adversarial(*cfg["adv"])

    total = m3["total"] + mb["total"] + adv["total"]
    failed = m3["failures"] + mb["failures"] + adv["failures"]
    status = {
        "version": "2.17",
        "profile": args.profile,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "status": "PASS" if failed == 0 else "FAIL",
        "not_a_proof": True,
        "single_block_cases": m3["total"],
        "single_block_failures": m3["failures"],
        "multiblock_cases": mb["total"],
        "multiblock_tp": mb["tp"],
        "multiblock_tn": mb["tn"],
        "multiblock_fp": mb["fp"],
        "multiblock_fn": mb["fn"],
        "multiblock_failures": mb["failures"],
        "adversarial_cases": adv["total"],
        "adversarial_failures": adv["failures"],
        "total_cases": total,
        "failed_cases": failed,
        "engines": m3["engines"],
        "runtime_sec": round(time.time() - t0, 2),
    }

    (out / "status.json").write_text(json.dumps(status, indent=2) + "\n")
    checksum = hashlib.sha256((out / "status.json").read_bytes()).hexdigest()
    (out / "checksums.sha256").write_text(f"{checksum}  status.json\n")

    print(json.dumps(status, indent=2))
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
