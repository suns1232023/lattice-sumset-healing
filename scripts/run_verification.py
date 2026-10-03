#!/usr/bin/env python3
"""Validate the machine-readable verification contract.

This script checks schema integrity only. It does not prove any mathematical
claim.
"""

from __future__ import annotations

import json
from pathlib import Path

REQUIRED_STATUS_KEYS = {
    "version",
    "profile",
    "timestamp",
    "status",
    "not_a_proof",
    "single_block_cases",
    "single_block_failures",
    "multiblock_cases",
    "multiblock_tp",
    "multiblock_tn",
    "multiblock_fp",
    "multiblock_fn",
    "multiblock_failures",
    "adversarial_cases",
    "adversarial_failures",
    "total_cases",
    "failed_cases",
    "engines",
    "runtime_sec",
    "epistemic_note",
}


def load_json(path: Path) -> dict:
    if not path.exists():
        raise SystemExit(f"ERROR: {path} not found")
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        raise SystemExit(f"ERROR: invalid JSON in {path}: {exc}") from exc


def main() -> int:
    status = load_json(Path("results/status.json"))
    missing = sorted(REQUIRED_STATUS_KEYS - status.keys())
    if missing:
        raise SystemExit(
            "ERROR: results/status.json is missing required keys: "
            + ", ".join(missing)
        )

    if status["status"] not in {"PASS", "FAIL"}:
        raise SystemExit("ERROR: status.status must be PASS or FAIL")

    if status["not_a_proof"] is not True:
        raise SystemExit(
            "ERROR: status.not_a_proof must remain true for computational audits"
        )

    expected_total = (
        status["single_block_cases"]
        + status["multiblock_cases"]
        + status["adversarial_cases"]
    )
    if status["total_cases"] != expected_total:
        raise SystemExit(
            f"ERROR: total_cases={status['total_cases']} "
            f"!= component total={expected_total}"
        )

    expected_failed = (
        status["single_block_failures"]
        + status["multiblock_failures"]
        + status["adversarial_failures"]
    )
    if status["failed_cases"] != expected_failed:
        raise SystemExit(
            f"ERROR: failed_cases={status['failed_cases']} "
            f"!= component failures={expected_failed}"
        )

    if status["status"] == "PASS" and status["failed_cases"] != 0:
        raise SystemExit("ERROR: PASS result cannot contain failures")

    print("Result schema: PASS")
    print("Epistemic guard: PASS")
    print("No mathematical proof is inferred from computational PASS.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
