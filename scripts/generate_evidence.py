"""
scripts/generate_evidence.py — Generate results/evidence.json.

The evidence ledger explicitly records:
- computational evidence (cases, engines, failures)
- lean_statement: whether a Lean 4 formal statement exists
- lean_proof: whether a Lean 4 kernel-verified proof exists
- not_a_proof: always True for computational results

Key principle: computational verification != mathematical proof.
"""

import json
import time
from pathlib import Path


EVIDENCE = {
    "version": "2.17",
    "generated": None,  # filled at runtime
    "epistemic_principle": (
        "Code can verify a claim; "
        "code does not silently upgrade a claim into a theorem."
    ),
    "claims": [
        {
            "id": "T3.2",
            "name": "Rectangular-box self-healing (d>=2)",
            "type": "THEOREM",
            "status": "PROVED",
            "not_a_proof": False,
            "proof_method": "Dispersed Corner Decomposition (analytic)",
            "computational": {
                "cases": 12,
                "engines": ["pure_set"],
                "failures": 0,
            },
            "lean_statement": False,
            "lean_proof": False,
            "lean_note": "Formalization planned",
        },
        {
            "id": "T6.1",
            "name": "d=1 single-void classification",
            "type": "THEOREM",
            "status": "PROVED",
            "not_a_proof": False,
            "proof_method": "Permanent missing element argument (analytic)",
            "lean_statement": False,
            "lean_proof": False,
        },
        {
            "id": "T7.1",
            "name": "d=1 multi-void classification",
            "type": "THEOREM",
            "status": "PROVED",
            "not_a_proof": False,
            "proof_method": "Follows from T6.1",
            "lean_statement": False,
            "lean_proof": False,
        },
        {
            "id": "M3",
            "name": "Single-block healing formula",
            "type": "CONJECTURE",
            "status": "VHC",
            "not_a_proof": True,
            "formula": "h*(ell,d) = ceil(ell/(d-1)) + 1",
            "computational": {
                "cases": 4640,
                "scope": "N<=35, ell<=15, d>=2",
                "engines": ["pure_set", "bitwise", "formula"],
                "failures": 0,
                "fp": 0,
                "fn": 0,
            },
            "lean_statement": False,
            "lean_proof": False,
        },
        {
            "id": "C14.3",
            "name": "Multi-block structural independence",
            "type": "CONJECTURE",
            "status": "VHC",
            "not_a_proof": True,
            "statement": "h*(V) > pred iff Criterion A or Criterion B",
            "computational": {
                "cases": 875658,
                "scope": "N<=35, r<=5",
                "engines": ["pure_set", "bitwise"],
                "failures": 0,
                "fp": 0,
                "fn": 0,
            },
            "lean_statement": False,
            "lean_proof": False,
        },
    ],
}


def main():
    out = Path("results")
    out.mkdir(exist_ok=True)

    evidence = dict(EVIDENCE)
    evidence["generated"] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())

    path = out / "evidence.json"
    with open(path, "w") as f:
        json.dump(evidence, f, indent=2)

    print(f"Generated {path}")
    print(f"Claims: {len(evidence['claims'])}")
    for c in evidence["claims"]:
        proved = "PROVED" if c["status"] == "PROVED" else "VHC"
        lean = "Lean: planned" if not c["lean_proof"] else "Lean: proved"
        print(f"  [{proved}] {c['id']}: {c['name']} | {lean}")


if __name__ == "__main__":
    main()
