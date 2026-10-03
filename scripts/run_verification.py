"""
scripts/run_verification.py — Master verification script.

Usage:
    python scripts/run_verification.py --profile ci      # fast (~0.1s)
    python scripts/run_verification.py --profile quick   # medium (~1s)
    python scripts/run_verification.py --profile full    # complete (~minutes)

Output:
    results/status.json      — machine-readable audit summary
    results/checksums.sha256 — integrity hashes

NOTE: Computational evidence for conjectures, NOT mathematical proofs.
"""

import argparse
import hashlib
import json
import sys
import time
from itertools import combinations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from self_healing.formulas import block_distance, predict_m3_threshold, predict_independent_threshold
from self_healing.healing import self_healing_threshold, self_healing_threshold_fast
from self_healing.defects import evaluate_criteria

PROFILES = {
    'ci':    {'m3': (15, 8),  'mb': (12, 3), 'adv': (15, 3)},
    'quick': {'m3': (20, 10), 'mb': (15, 4), 'adv': (20, 4)},
    'full':  {'m3': (35, 15), 'mb': (21, 5), 'adv': (35, 5)},
}


def audit_m3(N_max: int, ell_max: int) -> dict:
    """Audit Conjecture M3' — three-engine cross-validation."""
    total = exact = 0
    for N in range(5, N_max + 1):
        for length in range(1, ell_max + 1):
            for start in range(1, N - length):
                d = block_distance(N, start, length)
                if d < 2:
                    continue
                void_set = set(range(start, start + length))
                h_c = predict_m3_threshold(length, d)
                max_h = (h_c or 50) + 5
                h_a = self_healing_threshold(N, void_set, max_h=max_h)
                h_b = self_healing_threshold_fast(N, void_set, max_h=max_h)
                total += 1
                if h_a == h_b == h_c:
                    exact += 1
    failures = total - exact
    return {
        'conjecture': "M3'",
        'not_a_proof': True,
        'total': total,
        'exact': exact,
        'failures': failures,
        'engines': ['pure_set', 'bitwise', 'formula'],
    }


def audit_multiblock(N_max: int, max_blocks: int) -> dict:
    """Audit Conjecture 14.3 — multi-block independence."""
    total = tp = tn = fp = fn = 0
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
                actual_fail = actual_h is not None and actual_h > pred
                predicted_fail = result['triggered']
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
        'conjecture': '14.3',
        'not_a_proof': True,
        'total': total,
        'tp': tp,
        'tn': tn,
        'fp': fp,
        'fn': fn,
        'failures': fp + fn,
    }


def audit_adversarial(N_max: int, max_blocks: int) -> dict:
    """Adversarial audit targeting gap <= 1 configurations."""
    total = failures = 0
    for N in range(8, N_max + 1):
        interior = list(range(2, N - 2))
        for r in range(2, min(max_blocks + 1, len(interior) + 1)):
            for pts in combinations(interior, r):
                void_set = set(pts)
                sorted_pts = sorted(pts)
                gaps = [sorted_pts[i + 1] - sorted_pts[i] - 1
                        for i in range(len(sorted_pts) - 1)]
                if not gaps or min(gaps) > 1:
                    continue
                result = evaluate_criteria(N, void_set)
                pred = result['pred']
                if pred is None:
                    continue
                actual_h = self_healing_threshold(N, void_set, max_h=pred + 6)
                actual_fail = actual_h is not None and actual_h > pred
                total += 1
                if result['triggered'] != actual_fail:
                    failures += 1
    return {
        'conjecture': '14.3_adversarial',
        'not_a_proof': True,
        'total': total,
        'failures': failures,
    }


def main():
    parser = argparse.ArgumentParser(
        description='Run additive self-healing verification audits'
    )
    parser.add_argument(
        '--profile', choices=['ci', 'quick', 'full'], default='quick',
        help='Verification profile'
    )
    parser.add_argument('--output-dir', default='results')
    args = parser.parse_args()

    cfg = PROFILES[args.profile]
    out = Path(args.output_dir)
    out.mkdir(exist_ok=True)

    print("=" * 65)
    print(f"  Additive Self-Healing — Verification Suite")
    print(f"  Profile: {args.profile}")
    print(f"  NOTE: Computational evidence for conjectures, NOT proofs.")
    print("=" * 65)

    t0 = time.time()

    print(f"\n[Phase 1] Conjecture M3' — Single-Block Audit")
    m3 = audit_m3(*cfg['m3'])
    print(f"  {m3['total']:,} cases | failures: {m3['failures']}")

    print(f"\n[Phase 2] Conjecture 14.3 — Multi-Block Audit")
    mb = audit_multiblock(*cfg['mb'])
    print(f"  {mb['total']:,} cases | FP={mb['fp']} FN={mb['fn']}")

    print(f"\n[Phase 3] Adversarial Audit (gap <= 1)")
    adv = audit_adversarial(*cfg['adv'])
    print(f"  {adv['total']:,} cases | failures: {adv['failures']}")

    total = m3['total'] + mb['total'] + adv['total']
    failed = m3['failures'] + mb['fp'] + mb['fn'] + adv['failures']
    elapsed = time.time() - t0

    # Build status.json with ALL keys needed by verification scripts
    status = {
        'version': '2.17',
        'profile': args.profile,
        'timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        'status': 'PASS' if failed == 0 else 'FAIL',
        'not_a_proof': True,
        'epistemic_note': (
            'Computational verification is evidence for conjectures. '
            'NOT a mathematical proof.'
        ),
        # Single-block (M3') audit
        'single_block_cases': m3['total'],
        'single_block_failures': m3['failures'],
        # Multi-block (14.3) audit
        'multiblock_cases': mb['total'],
        'multiblock_tp': mb['tp'],
        'multiblock_tn': mb['tn'],
        'multiblock_fp': mb['fp'],
        'multiblock_fn': mb['fn'],
        'multiblock_failures': mb['fp'] + mb['fn'],
        # Adversarial audit
        'adversarial_cases': adv['total'],
        'adversarial_failures': adv['failures'],
        # Totals
        'total_cases': total,
        'failed_cases': failed,
        'engines': ['pure_set', 'bitwise', 'formula'],
        'runtime_sec': round(elapsed, 2),
    }

    status_path = out / 'status.json'
    with open(status_path, 'w') as f:
        json.dump(status, f, indent=2)

    # Checksums
    checksums = {}
    for p in out.glob('*.json'):
        checksums[p.name] = hashlib.sha256(p.read_bytes()).hexdigest()
    with open(out / 'checksums.sha256', 'w') as f:
        for name, chk in sorted(checksums.items()):
            f.write(f"{chk}  {name}\n")

    print(f"\n{'=' * 65}")
    print(f"  Total: {total:,} | Failures: {failed} | Status: {status['status']}")
    print(f"  Runtime: {elapsed:.2f}s | Results: {out.resolve()}")
    print(f"{'=' * 65}")

    return 0 if failed == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
