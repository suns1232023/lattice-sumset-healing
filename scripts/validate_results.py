"""
scripts/validate_results.py — Canonical schema validation for results/status.json.

Pipeline:
    run_verification.py → status.json → validate_results.py → generate_evidence.py → evidence.json

Rules:
    - Required fields must exist. Missing fields → FAIL with clear message.
    - No silent defaults for required scientific data.
    - Arithmetic consistency is verified.
    - not_a_proof must be True for computational conjecture audits.
"""

import json
import sys
from pathlib import Path

REQUIRED_FIELDS = {
    'version':                    str,
    'profile':                    str,
    'timestamp':                  str,
    'status':                     str,
    'not_a_proof':                bool,
    'epistemic_note':             str,
    'single_block_cases':         int,
    'single_block_failures':      int,
    'multiblock_cases':           int,
    'multiblock_tp':              int,
    'multiblock_tn':              int,
    'multiblock_fp':              int,
    'multiblock_fn':              int,
    'multiblock_failures':        int,
    'adversarial_cases':          int,
    'adversarial_failures':       int,
    'total_cases':                int,
    'failed_cases':               int,
    'runtime_sec':                (int, float),
}

VALID_STATUSES = {'PASS', 'FAIL'}
VALID_PROFILES = {'ci', 'quick', 'full'}


def require_field(data, field, expected_type):
    if field not in data:
        print(f"SCHEMA ERROR: Required field '{field}' is missing from status.json.")
        print("  This field must be written by run_verification.py.")
        print("  Do NOT add a default value here — fix run_verification.py instead.")
        sys.exit(1)
    value = data[field]
    if not isinstance(value, expected_type):
        actual = type(value).__name__
        expected = ' or '.join(t.__name__ for t in expected_type) if isinstance(expected_type, tuple) else expected_type.__name__
        print(f"SCHEMA ERROR: Field '{field}' has wrong type. Expected: {expected}, Actual: {actual} (value={value!r})")
        sys.exit(1)
    return value


def validate(status_path):
    if not status_path.exists():
        print(f"VALIDATION ERROR: {status_path} does not exist.")
        print("  Run 'python scripts/run_verification.py' first.")
        sys.exit(1)
    with open(status_path) as f:
        try:
            s = json.load(f)
        except json.JSONDecodeError as e:
            print(f"VALIDATION ERROR: {status_path} is not valid JSON: {e}")
            sys.exit(1)

    errors = []

    print("Checking required fields...")
    for field, expected_type in REQUIRED_FIELDS.items():
        require_field(s, field, expected_type)
    print(f"  ✓ All {len(REQUIRED_FIELDS)} required fields present with correct types.")

    if s['status'] not in VALID_STATUSES:
        errors.append(f"'status' must be one of {VALID_STATUSES}, got {s['status']!r}")
    if s['profile'] not in VALID_PROFILES:
        errors.append(f"'profile' must be one of {VALID_PROFILES}, got {s['profile']!r}")
    if s['not_a_proof'] is not True:
        errors.append("'not_a_proof' must be True for computational conjecture audits.")

    expected_total = s['single_block_cases'] + s['multiblock_cases'] + s['adversarial_cases']
    if s['total_cases'] != expected_total:
        errors.append(f"Arithmetic: total_cases={s['total_cases']} but sum={expected_total}")

    expected_failed = s['single_block_failures'] + s['multiblock_failures'] + s['adversarial_failures']
    if s['failed_cases'] != expected_failed:
        errors.append(f"Arithmetic: failed_cases={s['failed_cases']} but sum={expected_failed}")

    expected_mb = s['multiblock_tp'] + s['multiblock_tn'] + s['multiblock_fp'] + s['multiblock_fn']
    if s['multiblock_cases'] != expected_mb:
        errors.append(f"Arithmetic: multiblock_cases={s['multiblock_cases']} but TP+TN+FP+FN={expected_mb}")

    expected_mb_fail = s['multiblock_fp'] + s['multiblock_fn']
    if s['multiblock_failures'] != expected_mb_fail:
        errors.append(f"Arithmetic: multiblock_failures={s['multiblock_failures']} but FP+FN={expected_mb_fail}")

    if s['status'] == 'PASS' and s['failed_cases'] != 0:
        errors.append(f"Logical: status=PASS but failed_cases={s['failed_cases']} != 0")
    if s['status'] == 'FAIL' and s['failed_cases'] == 0:
        errors.append("Logical: status=FAIL but failed_cases=0")

    for field in ['single_block_cases', 'single_block_failures', 'multiblock_cases',
                  'multiblock_tp', 'multiblock_tn', 'multiblock_fp', 'multiblock_fn',
                  'multiblock_failures', 'adversarial_cases', 'adversarial_failures',
                  'total_cases', 'failed_cases']:
        if s[field] < 0:
            errors.append(f"Field '{field}' must be non-negative, got {s[field]}")
    if s['runtime_sec'] < 0:
        errors.append(f"'runtime_sec' must be non-negative, got {s['runtime_sec']}")

    if errors:
        print(f"\nVALIDATION FAILED: {len(errors)} error(s) found:")
        for i, err in enumerate(errors, 1):
            print(f"  {i}. {err}")
        sys.exit(1)

    print("  ✓ Enum values valid (status, profile).")
    print("  ✓ not_a_proof = True (computational audit correctly labeled).")
    print("  ✓ Arithmetic consistency verified.")
    print("  ✓ All counts non-negative.")
    return s


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Validate results/status.json against canonical schema.')
    parser.add_argument('--results-dir', default='results')
    args = parser.parse_args()

    status_path = Path(args.results_dir) / 'status.json'
    print(f"Validating {status_path}...")
    s = validate(status_path)

    print()
    print("=== Validated Results Summary ===")
    print(f"  Version:  {s['version']}")
    print(f"  Profile:  {s['profile']}")
    print(f"  Status:   {s['status']}")
    print(f"  Single-block (M3'):  {s['single_block_cases']:,} cases, {s['single_block_failures']} failures")
    print(f"  Multi-block (14.3):  {s['multiblock_cases']:,} cases, TP={s['multiblock_tp']} TN={s['multiblock_tn']} FP={s['multiblock_fp']} FN={s['multiblock_fn']}")
    print(f"  Adversarial:         {s['adversarial_cases']:,} cases, {s['adversarial_failures']} failures")
    print(f"  Total:               {s['total_cases']:,} cases, {s['failed_cases']} failures")
    print(f"  Runtime:             {s['runtime_sec']}s")
    print(f"  not_a_proof:         {s['not_a_proof']}")
    print(f"  EPISTEMIC NOTE: {s['epistemic_note']}")
    print("SCHEMA VALIDATION PASSED ✓")


if __name__ == '__main__':
    main()
