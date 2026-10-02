"""
experiments/multi_block/run_multiblock_audit.py
================================================
Audit of Conjecture 14.3 (Structural Independence) for multi-block voids.

Conjecture 14.3 [VHC]:
    h*(V_void) > pred ⟺ Criterion A ∨ Criterion B

Scope: N ≤ 21, r ≤ 5 (30,534 configurations)
Expected: FP=0, FN=0

Usage:
    python experiments/multi_block/run_multiblock_audit.py
    python experiments/multi_block/run_multiblock_audit.py --N-max 15 --max-blocks 3

NOTE: Computational evidence for VHC, NOT a mathematical proof.
"""

import argparse
import csv
import json
import sys
import time
from itertools import combinations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from self_healing.defects import evaluate_criteria
from self_healing.formulas import predict_independent_threshold
from self_healing.healing import self_healing_threshold


def run_multiblock_audit(
    N_max: int = 21,
    max_blocks: int = 5,
    verbose: bool = False,
):
    """
    Run the multi-block independence audit (Conjecture 14.3).

    Returns:
        (result_dict, rows_list)
    """
    print(f"[Conjecture 14.3 Audit] Scope: N ≤ {N_max}, r ≤ {max_blocks}")
    print("[Conjecture 14.3 Audit] NOTE: VHC — computational evidence, not a proof.\n")

    total = 0
    tp = tn = fp = fn = 0
    rows = []
    counterexamples = []

    t0 = time.time()

    for N in range(8, N_max + 1):
        interior = list(range(2, N - 2))
        for r in range(2, min(max_blocks + 1, len(interior) + 1)):
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

                if predicted_fail and actual_fail:
                    tp += 1
                elif predicted_fail and not actual_fail:
                    fp += 1
                    counterexamples.append({
                        'type': 'FP', 'N': N, 'void': sorted(void_set),
                        'pred': pred, 'actual_h': actual_h,
                    })
                elif not predicted_fail and actual_fail:
                    fn += 1
                    counterexamples.append({
                        'type': 'FN', 'N': N, 'void': sorted(void_set),
                        'pred': pred, 'actual_h': actual_h,
                    })
                else:
                    tn += 1

                rows.append({
                    'N': N, 'void': str(sorted(void_set)),
                    'pred': pred, 'actual_h': actual_h,
                    'criterion_a': result['criterion_a'],
                    'criterion_b': result['criterion_b'],
                    'triggered': predicted_fail,
                    'actual_fail': actual_fail,
                    'correct': predicted_fail == actual_fail,
                })

                if verbose and predicted_fail != actual_fail:
                    print(f"  MISMATCH: N={N}, V={sorted(void_set)}, "
                          f"pred={pred}, actual_h={actual_h}, "
                          f"triggered={predicted_fail}")

        if N % 3 == 0:
            elapsed = time.time() - t0
            print(f"  N={N:2d} | cumulative={total:8d} | FP={fp} FN={fn} | {elapsed:.1f}s")

    elapsed = time.time() - t0

    print(f"\n[Conjecture 14.3 Audit] Total: {total}")
    print(f"[Conjecture 14.3 Audit] TP={tp}, TN={tn}, FP={fp}, FN={fn}")
    if total > 0:
        recall = tp / (tp + fn) if (tp + fn) > 0 else 1.0
        precision = tp / (tp + fp) if (tp + fp) > 0 else 1.0
        print(f"[Conjecture 14.3 Audit] Recall={recall:.4f}, Precision={precision:.4f}")
    print(f"[Conjecture 14.3 Audit] Elapsed: {elapsed:.2f}s")

    return {
        'conjecture': '14.3',
        'status': 'VHC' if fp == 0 and fn == 0 else 'COUNTEREXAMPLE_FOUND',
        'not_a_proof': True,
        'scope': {'N_max': N_max, 'max_blocks': max_blocks},
        'total_cases': total,
        'tp': tp, 'tn': tn, 'fp': fp, 'fn': fn,
        'counterexamples': counterexamples[:5],
        'elapsed_sec': round(elapsed, 2),
    }, rows


def main():
    parser = argparse.ArgumentParser(description="Audit Conjecture 14.3")
    parser.add_argument('--N-max', type=int, default=21)
    parser.add_argument('--max-blocks', type=int, default=5)
    parser.add_argument('--verbose', action='store_true')
    parser.add_argument('--output-dir', type=str, default='results')
    args = parser.parse_args()

    result, rows = run_multiblock_audit(args.N_max, args.max_blocks, args.verbose)

    out_dir = Path(args.output_dir)
    out_dir.mkdir(exist_ok=True)

    with open(out_dir / 'multiblock.csv', 'w', newline='') as f:
        if rows:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)

    print(f"\n[Conjecture 14.3 Audit] Results saved to {out_dir}/multiblock.csv")
    return 0 if result['fp'] == 0 and result['fn'] == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
