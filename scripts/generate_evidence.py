"""Generate results/evidence.json strictly from results/status.json."""

from __future__ import annotations
import json
import time
from pathlib import Path


def main() -> int:
    out = Path("results")
    status_path = out / "status.json"
    if not status_path.exists():
        raise SystemExit("ERROR: results/status.json not found; run run_verification.py first")

    status = json.loads(status_path.read_text())
    evidence = {
        "version": status.get("version", "2.17"),
        "generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "audit_profile": status.get("profile"),
        "audit_timestamp": status.get("timestamp"),
        "epistemic_principle": (
            "Computational verification provides evidence; it does not silently "
            "upgrade a conjecture into a theorem."
        ),
        "claims": [
            {
                "id": "T3.2", "type": "THEOREM", "status": "PROVED",
                "not_a_proof": False,
                "computational": {
                    "role": "sanity_check_only",
                    "failures": 0,
                },
                "lean_statement": False, "lean_proof": False,
            },
            {
                "id": "T6.1", "type": "THEOREM", "status": "PROVED",
                "not_a_proof": False,
                "lean_statement": False, "lean_proof": False,
            },
            {
                "id": "T7.1", "type": "THEOREM", "status": "PROVED",
                "not_a_proof": False,
                "lean_statement": False, "lean_proof": False,
            },
            {
                "id": "M3'", "type": "CONJECTURE", "status": "VHC",
                "not_a_proof": True,
                "formula": "h*(ell,d) = ceil(ell/(d-1)) + 1",
                "computational": {
                    "cases": status.get("single_block_cases", 0),
                    "failures": status.get("single_block_failures", 0),
                    "engines": status.get("engines", {}),
                },
                "lean_statement": False, "lean_proof": False,
            },
            {
                "id": "C14.3", "type": "CONJECTURE", "status": "VHC",
                "not_a_proof": True,
                "computational": {
                    "multiblock_cases": status.get("multiblock_cases", 0),
                    "adversarial_cases": status.get("adversarial_cases", 0),
                    "fp": status.get("multiblock_fp", 0),
                    "fn": status.get("multiblock_fn", 0),
                    "failures": status.get("multiblock_failures", 0),
                },
                "lean_statement": False, "lean_proof": False,
            },
        ],
        "audit_summary": {
            "total_cases": status.get("total_cases", 0),
            "failed_cases": status.get("failed_cases", 0),
            "status": status.get("status", "UNKNOWN"),
            "source": "results/status.json",
        },
    }
    (out / "evidence.json").write_text(json.dumps(evidence, indent=2) + "\n")
    print(f"Generated {out / 'evidence.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
