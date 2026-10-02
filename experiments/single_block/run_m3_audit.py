"""
experiments/single_block/run_m3_audit.py
========================================
Full-scope audit of Conjecture M3' using three independent engines.

Conjecture M3' [VHC]: h*(ℓ, d) = ⌈ℓ/(d-1)⌉ + 1

Scope: N ≤ 35, ℓ ≤ 15, d ≥ 2
Expected: 4,640 cases, FP=0, FN=0, three-engine agreement

Usage:
    python experiments/single_block/run_m3_audit.py
    python experiments/single_block/run_m3_audit.py --N-max 20 --ell-max 8

NOTE: This is computational evidence for a conjecture, NOT a proof.
"""

import argparse
import csv
import json
import sys
import time
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from self_healing.formulas import block_distance, predict_m3_threshold
from self_healing.healing import self_healing_threshold, self_healing_threshold_fast


def run_m3_audit(N_max: int = 35, ell_max: int = 15, verbose: bool = False):
    """
    Run the full M3' audit.

    Returns:
        dict with audit results.
    """
    print(f"[M3' Audit] Scope: N ≤ {N_max}, ℓ ≤ {ell_max}, d ≥ 2")
    print("[M3' Audit] NOTE: Computational evidence for VHC, not a proof.\n")

    total = 0
    exact_matches = 0
    failures = []
    rows = []

    t0 = time.time()

    for N in range(5, N_max + 1):
        for length in range(1, ell_max + 1):
            for start in range(1, N - length):
                d = block_distance(N, start, length)
                if d < 2:
                    continue

                void_set = set(range(start, start + length))
                h_formula = predict_m3_threshold(length, d)
                h_set = self_healing_threshold(N, void_set, max_h=h_formula + 5 if h_formula else 50)
                h_bit = self_healing_threshold_fast(N, void_set, max_h=h_formula + 5 if h_formula else 50)

                total += 1
                all_agree = (h_set == h_bit == h_formula)

                if all_agree:
                    exact_matches += 1
                else:
                    failures.append({
                        'N': N, 'start': start, 'length': length, 'd': d,
                        'h_formula': h_formula, 'h_set': h_set, 'h_bit': h_bit,
                    })

                rows.append({
                    'N': N, 'start': start, 'length': length, 'd': d,
                    'ell': length, 'h_formula': h_formula,
                    'h_engine_a': h_set, 'h_engine_b': h_bit,
                    'all_agree': all_agree,
                })

                if verbose and not all_agree:
                    print(f"  MISMATCH: N={N}, start={start}, ℓ={length}, d={d}: "
                          f"formula={h_formula}, set={h_set}, bit={h_bit}")

    elapsed = time.time() - t0

    print(f"[M3' Audit] Total cases: {total}")
    print(f"[M3' Audit] Exact matches (3-engine): {exact_matches} ({100*exact_matches/total:.2f}%)")
    print(f"[M3' Audit] Failures: {len(failures)}")
    print(f"[M3' Audit] Elapsed: {elapsed:.3f}s")

    if failures:
        print(f"\n[M3' Audit] FAILURES FOUND:")
        for f in failures[:5]:
            print(f"  {f}")

    return {
        'conjecture': "M3'",
        'status': 'VHC' if len(failures) == 0 else 'COUNTEREXAMPLE_FOUND',
        'not_a_proof': True,
        'scope': {'N_max': N_max, 'ell_max': ell_max, 'd_min': 2},
        'total_cases': total,
        'exact_matches': exact_matches,
        'failures': len(failures),
        'failure_examples': failures[:3],
        'elapsed_sec': round(elapsed, 3),
        'engines': ['pure_set', 'bitwise', 'formula'],
    }, rows


def main():
    parser = argparse.ArgumentParser(description="Audit Conjecture M3'")
    parser.add_argument('--N-max', type=int, default=35)
    parser.add_argument('--ell-max', type=int, default=15)
    parser.add_argument('--verbose', action='store_true')
    parser.add_argument('--output-dir', type=str, default='results')
    args = parser.parse_args()

    result, rows = run_m3_audit(args.N_max, args.ell_max, args.verbose)

    # Save results
    out_dir = Path(args.output_dir)
    out_dir.mkdir(exist_ok=True)

    with open(out_dir / 'single_block.csv', 'w', newline='') as f:
        if rows:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)

    print(f"\n[M3' Audit] Results saved to {out_dir}/single_block.csv")
    return 0 if result['failures'] == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
