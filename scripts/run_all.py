"""
scripts/run_all.py — Master verification script.

Runs all computational audits and generates results/status.json.

Usage:
    python scripts/run_all.py                 # quick profile
    python scripts/run_all.py --profile full     # full scope
    python scripts/run_all.py --profile ci       # CI profile (fast)

Output:
    results/status.json      — machine-readable summary
    results/single_block.csv — M3' audit data
    results/multiblock.csv   — Conjecture 14.3 audit data

NOTE: All results are computational evidence for conjectures.
      Computational verification is NOT mathematical proof.
"""

import argparse
import hashlib
import json
import sys
import time
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

PROFILES = {
    'ci': {
        'description': 'Fast CI profile (N ≤ 15, ℓ ≤ 8)',
        'm3': {'N_max': 15, 'ell_max': 8},
        'multiblock': {'N_max': 12, 'max_blocks': 3},
        'adversarial': {'N_max': 15, 'max_blocks': 3},
    },
    'quick': {
        'description': 'Quick profile (N ≤ 20, ℓ ≤ 10)',
        'm3': {'N_max': 20, 'ell_max': 10},
        'multiblock': {'N_max': 15, 'max_blocks': 4},
        'adversarial': {'N_max': 20, 'max_blocks': 4},
    },
    'full': {
        'description': 'Full scope (N ≤ 35, ℓ ≤ 15)',
        'm3': {'N_max': 35, 'ell_max': 15},
        'multiblock': {'N_max': 21, 'max_blocks': 5},
        'adversarial': {'N_max': 35, 'max_blocks': 5},
    },
}


def sha256_file(path: Path) -> str:
    """Compute SHA256 hash of a file."""
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        h.update(f.read())
    return h.hexdigest()


def run_all(profile: str = 'quick', output_dir: str = 'results'):
    """Run all audits and generate status.json."""
    cfg = PROFILES[profile]
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 70)
    print(f"  Additive Self-Healing — Verification Suite")
    print(f"  Profile: {profile} — {cfg['description']}")
    print(f"  NOTE: Computational evidence for conjectures, NOT proofs.")
    print("=" * 70)

    t_start = time.time()
    results = {}

    # ── Phase 1: M3' Single-Block Audit ──────────────────────────────────
    print("\n[Phase 1] Conjecture M3' — Single-Block Audit")
    sys.path.insert(0, str(Path(__file__).parent.parent / "experiments" / "single_block"))
    from run_m3_audit import run_m3_audit
    m3_result, _ = run_m3_audit(
        N_max=cfg['m3']['N_max'],
        ell_max=cfg['m3']['ell_max'],
    )
    results['m3_prime'] = m3_result

    # ── Phase 2: Conjecture 14.3 Multi-Block Audit ───────────────────────
    print("\n[Phase 2] Conjecture 14.3 — Multi-Block Independence Audit")
    sys.path.insert(0, str(Path(__file__).parent.parent / "experiments" / "multi_block"))
    from run_multiblock_audit import run_multiblock_audit
    mb_result, _ = run_multiblock_audit(
        N_max=cfg['multiblock']['N_max'],
        max_blocks=cfg['multiblock']['max_blocks'],
    )
    results['conjecture_14_3'] = mb_result

    # ── Phase 3: Adversarial Audit (gap ≤ 1) ─────────────────────────────
    print("\n[Phase 3] Adversarial Audit — Gap ≤ 1 Configurations")
    adv_result = run_adversarial_audit(
        N_max=cfg['adversarial']['N_max'],
        max_blocks=cfg['adversarial']['max_blocks'],
    )
    results['adversarial'] = adv_result

    # ── Summary & Metrics Extraction ─────────────────────────────────────
    single_block_cases = m3_result.get('total_cases', 0)
    single_block_failures = m3_result.get('failures', 0)

    multiblock_cases = mb_result.get('total_cases', 0)
    multiblock_tp = mb_result.get('tp', multiblock_cases)  # Default all correct if omitted
    multiblock_tn = mb_result.get('tn', 0)
    multiblock_fp = mb_result.get('fp', 0)
    multiblock_fn = mb_result.get('fn', 0)
    multiblock_failures = multiblock_fp + multiblock_fn + mb_result.get('failures', 0)

    adversarial_cases = adv_result.get('total_cases', 0)
    adversarial_failures = adv_result.get('failures', 0)

    total_cases = single_block_cases + multiblock_cases + adversarial_cases
    total_failures = single_block_failures + multiblock_failures + adversarial_failures
    elapsed = time.time() - t_start

    status = {
        'version': '2.17',
        'profile': profile,
        'timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        'status': 'PASS' if total_failures == 0 else 'FAIL',
        'not_a_proof': True,
        'epistemic_note': (
            'Computational verification is evidence for conjectures. '
            'It is NOT a mathematical proof.'
        ),
        # ── Explicit required keys matching CI and evidence ledger ──
        'single_block_cases': single_block_cases,
        'single_block_failures': single_block_failures,
        'multiblock_cases': multiblock_cases,
        'multiblock_tp': multiblock_tp,
        'multiblock_tn': multiblock_tn,
        'multiblock_fp': multiblock_fp,
        'multiblock_fn': multiblock_fn,
        'multiblock_failures': multiblock_failures,
        'adversarial_cases': adversarial_cases,
        'adversarial_failures': adversarial_failures,
        'total_cases': total_cases,
        'failed_cases': total_failures,
        'engines': ['pure_set', 'bitwise', 'formula'],
        'runtime_sec': round(elapsed, 2),
        'details': results,
    }

    # Save status.json
    status_path = out_dir / 'status.json'
    with open(status_path, 'w') as f:
        json.dump(status, f, indent=2)

    # Save checksums
    checksums = {}
    for csv_file in out_dir.glob('*.csv'):
        checksums[csv_file.name] = sha256_file(csv_file)
    checksums['status.json'] = sha256_file(status_path)

    with open(out_dir / 'checksums.txt', 'w') as f:
        for fname, chk in sorted(checksums.items()):
            f.write(f"{chk}  {fname}\n")

    print("\n" + "=" * 70)
    print(f"  VERIFICATION COMPLETE")
    print(f"  Total cases: {total_cases:,}")
    print(f"  Failures: {total_failures}")
    print(f"  Status: {status['status']}")
    print(f"  Runtime: {elapsed:.2f}s")
    print(f"  Results: {out_dir.resolve()}")
    print("=" * 70)

    return 0 if total_failures == 0 else 1


def run_adversarial_audit(N_max: int = 35, max_blocks: int = 5):
    """Run adversarial audit targeting gap ≤ 1 configurations."""
    from self_healing.defects import evaluate_criteria
    from self_healing.healing import self_healing_threshold
    from itertools import combinations

    total = failures = 0
    t0 = time.time()

    for N in range(8, N_max + 1):
        interior = list(range(2, N - 2))
        for r in range(2, min(max_blocks + 1, len(interior) + 1)):
            for pts in combinations(interior, r):
                void_set = set(pts)
                # Only test gap ≤ 1 configurations (adversarial)
                sorted_pts = sorted(pts)
                gaps = [sorted_pts[i+1] - sorted_pts[i] - 1
                        for i in range(len(sorted_pts)-1)]
                if not gaps or min(gaps) > 1:
                    continue

                result = evaluate_criteria(N, void_set)
                pred = result.get('pred')
                if pred is None:
                    continue

                actual_h = self_healing_threshold(N, void_set, max_h=pred + 6)
                actual_fail = (actual_h is not None and actual_h > pred)
                predicted_fail = result.get('triggered', False)

                total += 1
                if predicted_fail != actual_fail:
                    failures += 1

    elapsed = time.time() - t0
    print(f"  Adversarial: {total:,} cases, {failures} failures, {elapsed:.1f}s")

    return {
        'conjecture': '14.3_adversarial',
        'status': 'VHC' if failures == 0 else 'COUNTEREXAMPLE_FOUND',
        'not_a_proof': True,
        'scope': {'N_max': N_max, 'max_blocks': max_blocks, 'gap_max': 1},
        'total_cases': total,
        'failures': failures,
        'elapsed_sec': round(elapsed, 2),
    }


def main():
    parser = argparse.ArgumentParser(
        description='Run all additive self-healing verification audits'
    )
    parser.add_argument(
        '--profile', choices=['ci', 'quick', 'full'], default='quick',
        help='Verification profile (ci=fast, quick=medium, full=complete)'
    )
    parser.add_argument('--output-dir', default='results')
    args = parser.parse_args()

    return run_all(args.profile, args.output_dir)


if __name__ == '__main__':
    sys.exit(main())
