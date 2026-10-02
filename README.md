# Lattice Sumset Healing

### Interior Voids, Iterated Sumsets, and Additive Defect-Recovery Thresholds

[![CI](https://github.com/suns1232023/lattice-sumset-healing/actions/workflows/ci.yml/badge.svg)](https://github.com/suns1232023/lattice-sumset-healing/actions/workflows/ci.yml)
[![Verification](https://github.com/suns1232023/lattice-sumset-healing/actions/workflows/verification.yml/badge.svg)](https://github.com/suns1232023/lattice-sumset-healing/actions/workflows/verification.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![OSF](https://img.shields.io/badge/OSF-CZK8R-blue)](https://osf.io/czk8r/)
[![Zenodo](https://img.shields.io/badge/Zenodo-10.5281%2Fzenodo.21885380-blue)](https://doi.org/10.5281/zenodo.21885380)
[![ORCID](https://img.shields.io/badge/ORCID-0009--0002--1095--6228-green)](https://orcid.org/0009-0002-1095-6228)

> **OSF is the archival research record.**  
> **GitHub is the executable verification environment.**  
> **Lean provides the formal verification layer.**

**Author:** Scott Sun  
**Research record:** Version 2.17 · August 2026  
**Repository:** `suns1232023/lattice-sumset-healing`

---

## 1. Research Question

Let \(A_{\mathrm{full}}\) be a finite lattice set and let

\[
A_{\mathrm{hole}}
=
A_{\mathrm{full}}\setminus V_{\mathrm{void}},
\]

where \(V_{\mathrm{void}}\) is a nonempty interior defect.

For \(h\ge 1\), define the \(h\)-fold iterated sumset by

\[
hA
=
\underbrace{A+\cdots+A}_{h\text{ times}}.
\]

The **self-healing threshold** is

\[
\boxed{
h^*(A_{\mathrm{hole}};A_{\mathrm{full}})
=
\min\{h\ge1:hA_{\mathrm{hole}}=hA_{\mathrm{full}}\}
}
\]

when such an \(h\) exists.

### Central question

> **When does repeated additive combination erase a local defect in a lattice set?**

The project studies this question through exact finite computation, structural mathematics, and formal verification.

```text
FULL LATTICE             INTERIOR VOID             ITERATED SUMSET

████████████████         ████████████████          ████████████████
████████████████         ██████░░░░██████          ████████████████
████████████████   →     ██████░░░░██████    →     ████████████████
████████████████         ████████████████          ████████████████

 A_full                   A_hole                   h A_hole
                          local defect             defect recovery?
```

---

## 2. Research Record and Verification Repository

This repository is **not a duplicate of the research archive**.

| Resource | Primary role |
|---|---|
| **OSF** | Research record, paper versions, research materials and persistent project record |
| **Zenodo** | Versioned research/software archive and DOI |
| **ResearchGate** | Public research publication and discussion record |
| **GitHub** | Source code, computational verification, tests, evidence and formalization |
| **Lean 4 + Mathlib** | Formal mathematical statements and kernel-checked proofs |

The current research record is:

**Additive Self-Healing in Lattice Sumsets with Interior Voids, Version 2.17**

OSF project:

`10.17605/OSF.IO/CZK8R`

Zenodo record:

`10.5281/zenodo.21885380`

ResearchGate record:

`10.13140/RG.2.2.30968.61445`

The published V2.17 record distinguishes unconditional theorems from computational conjectures and reports 875,658 computational verifications for the multi-block investigation.

---

# 3. Evidence Status

This repository follows a strict epistemic separation:

> **Computation can provide evidence.  
> Formalization can make a statement precise.  
> A Lean proof can establish a formally encoded theorem.  
> None of these layers silently upgrades a conjecture into a theorem.**

| Result | Mathematical status | Computational evidence | Lean statement | Lean proof |
|---|---|---:|---:|---:|
| Theorem 2.1 | **[PROVED]** | analytic | planned | planned |
| Theorem 3.2 | **[PROVED]** | supporting computation | planned | planned |
| Theorem 6.1 | **[PROVED]** | analytic | planned | planned |
| Theorem 7.1 | **[PROVED]** | analytic | planned | planned |
| Conjecture M3′ | **[VHC]** | 4,640 cases | planned | OPEN |
| Conjecture 14.3 | **[VHC]** | 875,658 cases | planned | OPEN |

### Status definitions

- **[PROVED]** — unconditional mathematical result in the research record.
- **[VHC]** — Validated Heuristic Conjecture: extensive computational support, but not a mathematical proof.
- **[FORMALIZED]** — mathematical statement encoded in Lean.
- **[LEAN-PROVED]** — formal proof checked by the Lean kernel.
- **[OPEN]** — no formal proof currently established in this repository.

A computational result remains computational evidence even when multiple independent implementations agree.

---

# 4. Verification Dashboard

The current V2.17 computational record contains:

| Audit | Cases | Independent engines | FP | FN | Result |
|---|---:|---:|---:|---:|---|
| Single-block M3′ | 4,640 | 3 | 0 | 0 | PASS |
| Multi-block 14.3 | 397,210 | 2 | 0 | 0 | PASS |
| Adversarial configurations | 478,448 | 2 | 0 | 0 | PASS |
| **Total** | **875,658** | — | **0** | **0** | **PASS** |

These are **finite computational audits**. They do not constitute mathematical proofs.

The repository is designed so that the numerical evidence can be regenerated independently rather than treated as a static claim.

---

# 5. Three Verification Layers

The project deliberately separates three forms of mathematical evidence.

```text
                    MATHEMATICAL CLAIM
                           │
             ┌─────────────┴─────────────┐
             │                           │
             ▼                           ▼
     Computational Evidence       Formal Statement
             │                           │
             │                           ▼
             │                    Lean 4 / Mathlib
             │                           │
             └─────────────┬─────────────┘
                           ▼
                    Formal Proof
                           │
                           ▼
                    Lean Kernel
```

### Layer 1 — Computational

Exact enumeration, independent implementations, regression tests and adversarial audits.

### Layer 2 — Formalization

Precise encoding of definitions, theorems and conjectures in Lean 4.

### Layer 3 — Formal Proof

Where a proof exists, Lean's kernel checks the formal proof term against the encoded statement.

**AI-assisted tools may assist exploration, translation, proof search or code generation. They are not treated as mathematical authorities.**

---

# 6. Formalization Strategy

The Lean component lives under:

```text
formalization/
```

rather than in a separate repository.

The initial structure is:

```text
formalization/
├── AdditiveSelfHealing/
│   ├── Basic.lean
│   ├── Sumset.lean
│   ├── LatticeBox.lean
│   ├── Void.lean
│   ├── Healing.lean
│   ├── Theorem3_2.lean
│   ├── ConjectureM3.lean
│   └── Conjecture14_3.lean
│
├── AdditiveSelfHealing.lean
├── Audit.lean
├── README.md
├── lakefile.toml
├── lake-manifest.json
└── lean-toolchain
```

The intended progression is:

```text
Definitions
    ↓
Elementary lemmas
    ↓
Structural sumset identities
    ↓
Theorem 3.2
    ↓
Formal statement of M3′
    ↓
Formal statement of Conjecture 14.3
    ↓
Future formal proofs
```

The project does **not** assume that a conjecture becomes a theorem merely because it has been formalized.

This distinction follows the broader Lean formalization ecosystem, where a conjecture may be formally stated without possessing a formal proof. Google DeepMind's `formal-conjectures` project explicitly uses this separation and also emphasizes human review of formalization accuracy.

---

# 7. Relationship to AI-Assisted Formal Mathematics

The repository may use modern AI systems as research assistants for tasks such as:

- translating mathematical definitions into Lean;
- proposing candidate lemmas;
- searching for proof strategies;
- reviewing implementation consistency;
- generating documentation;
- identifying possible edge cases.

However:

```text
LLM / AI system
      ↓
candidate
      ↓
human mathematical review
      ↓
Lean elaboration
      ↓
Lean kernel
```

The final formal status is determined by the mathematical statement and its formal verification, not by the identity of the AI system that assisted in producing it.

The repository may therefore record AI assistance for provenance and reproducibility, while keeping the epistemic authority of the formal layer independent of any particular model or vendor.

---

# 8. Core Theorem: Rectangular-Box Self-Healing

For

\[
A_{\mathrm{full}}
=
\prod_{i=1}^{D}\{0,\ldots,N_i-1\},
\]

with \(D\ge2\), \(N_i\ge3\), and a nonempty strictly interior void

\[
\varnothing\ne V_{\mathrm{void}}
\subset
\operatorname{int}(A_{\mathrm{full}}),
\]

the research establishes

\[
\boxed{
2A_{\mathrm{hole}}
=
2A_{\mathrm{full}}
}
\]

and consequently

\[
\boxed{
h^*=2.
}
\]

The result is established analytically in the V2.17 research record using the Dispersed Corner Decomposition. The proof separates the interior and boundary-constrained cases.

### Important scope condition

The result depends essentially on the multidimensional structure \(D\ge2\).

The one-dimensional case behaves differently and requires separate classification.

---

# 9. One-Dimensional Classification

For the one-dimensional full lattice interval

\[
A_{\mathrm{full}}
=
\{0,\ldots,N-1\},
\]

the V2.17 research record establishes separate results for single and multiple voids.

For a single interior void \(V_{\mathrm{void}}=\{v\}\), with \(1\le v\le N-2\),

\[
h^*=\infty
\quad\text{if}\quad
v\in\{1,N-2\},
\]

while

\[
h^*=2
\quad\text{for}\quad
2\le v\le N-3.
\]

The multi-void classification is given separately as Theorem 7.1.

These results motivate the central distinction between:

- multidimensional defect recovery;
- one-dimensional boundary-sensitive behavior;
- multi-block interaction.

---

# 10. Conjecture M3′

The principal single-block conjecture is

\[
\boxed{
h^*(\ell,d)
=
\left\lceil
\frac{\ell}{d-1}
\right\rceil+1
}
\]

for \(d\ge2\), where \(d\) denotes the corrected distance parameter

\[
d=\min(d_{\mathrm{left}},d_{\mathrm{right}}).
\]

The conjecture has been tested over **4,640 exact cases** in the current computational record.

### Status

```text
Formal mathematical statement     OPEN
Computational evidence             4,640 cases
Observed falsifications            0
Formal Lean proof                  OPEN
```

Therefore:

> **M3′ remains a conjecture.**

The computational audit is evidence for the conjecture, not a proof.

---

# 11. Conjecture 14.3 — Multi-Block Structural Independence

The multi-block problem investigates whether the healing threshold can be predicted from independently healing blocks, except where specific structural interactions occur.

The current formulation is expressed through **Criterion A** and **Criterion B**.

The V2.17 research record reports:

```text
397,210  multi-block A/B configurations
478,448  adversarial configurations
-------------------------------------
875,658  total computational audits
0        reported FP
0        reported FN
```

The result is classified as a **Validated Heuristic Conjecture (VHC)**.

It is not currently claimed as a theorem.

---

# 12. Minimal Example

A small one-dimensional example illustrates the distinction between prediction and exact computation.

```python
from self_healing import (
    self_healing_threshold,
    predict_m3_threshold,
)
from self_healing.formulas import block_distance

N = 7
void_set = {3, 4}

d = block_distance(
    N=N,
    start=3,
    length=2,
)

h_pred = predict_m3_threshold(
    ell=2,
    d=d,
)

h_actual = self_healing_threshold(
    N,
    void_set,
)

assert h_pred == h_actual == 3
```

Here,

\[
d=\min(3,2)=2
\]

and therefore

\[
\left\lceil\frac{2}{2-1}\right\rceil+1=3.
\]

This example demonstrates agreement between the prediction and the exact computation for one finite case. It is **not** evidence of a proof of M3′.

---

# 13. Reproducibility

Clone the repository and install the development environment:

```bash
git clone https://github.com/suns1232023/lattice-sumset-healing.git
cd lattice-sumset-healing

pip install -e ".[dev]"
```

Run the test suite:

```bash
python -m pytest tests/ -v
```

Run the continuous-integration verification profile:

```bash
python scripts/run_verification.py --profile ci
```

Run the full computational audit:

```bash
python scripts/run_verification.py --profile full
```

Generate the machine-readable evidence ledger:

```bash
python scripts/generate_evidence.py
```

The repository is designed so that published numerical claims can be regenerated from source rather than relying solely on precomputed tables.

---

# 14. Repository Structure

```text
lattice-sumset-healing/
│
├── README.md
├── CITATION.cff
├── LICENSE
├── CHANGELOG.md
│
├── src/
│   └── self_healing/
│       ├── lattice.py
│       ├── sumset.py
│       ├── defects.py
│       ├── healing.py
│       ├── formulas.py
│       └── invariants.py
│
├── tests/
│
├── experiments/
│   ├── single_block/
│   ├── multi_block/
│   ├── adversarial/
│   └── scaling/
│
├── results/
│   ├── status.json
│   ├── evidence.json
│   └── checksums.sha256
│
├── formalization/
│   ├── AdditiveSelfHealing/
│   ├── AdditiveSelfHealing.lean
│   ├── Audit.lean
│   ├── lakefile.toml
│   ├── lake-manifest.json
│   └── lean-toolchain
│
├── docs/
│   ├── DEFINITIONS.md
│   ├── THEORY.md
│   ├── THEOREMS.md
│   ├── CONJECTURES.md
│   ├── COMPUTATIONAL_PROTOCOL.md
│   ├── FORMALIZATION.md
│   ├── REPRODUCIBILITY.md
│   ├── OSF_GITHUB_MAPPING.md
│   └── AI_ASSISTED_RESEARCH.md
│
├── benchmarks/
│   ├── small/
│   ├── medium/
│   └── large/
│
├── scripts/
│   ├── run_verification.py
│   ├── generate_evidence.py
│   ├── validate_results.py
│   └── update_dashboard.py
│
└── .github/
    └── workflows/
        ├── ci.yml
        ├── verification.yml
        ├── lean.yml
        ├── reproducibility.yml
        └── release.yml
```

---

# 15. Machine-Readable Evidence

The repository maintains computational evidence separately from mathematical claims.

A typical evidence record has the following conceptual structure:

```json
{
  "claim": "M3'",
  "status": "VHC",
  "cases": 4640,
  "failures": 0,
  "engines": [
    "reference",
    "bitset",
    "formula"
  ],
  "lean_statement": false,
  "lean_proof": false,
  "not_a_proof": true
}
```

The machine-readable ledger is intended to prevent accidental status inflation.

In particular:

```text
0 computational failures
        ≠
mathematical proof
```

and

```text
Lean formalized statement
        ≠
Lean formal proof
```

---

# 16. Formal Audit Policy

The formalization layer will distinguish:

```text
FORMALIZED
    │
    ├── statement encoded in Lean
    │
    └── proof not necessarily available

LEAN-PROVED
    │
    ├── proof term accepted by Lean
    └── audited for unintended axioms / placeholders
```

Proof modules intended for a verified release should contain no unresolved proof placeholders.

The formal audit will report, as appropriate:

- unresolved `sorry`;
- `admit`;
- unexpected axioms;
- `unsafe` declarations;
- proof dependencies;
- Lean and Mathlib versions;
- reproducible build status.

This follows the broader practice of formal mathematics repositories that explicitly distinguish formal statements from formally verified proofs.

---

# 17. Computational Engines

The verification framework is designed around independent computational paths rather than a single implementation.

```text
                 Test Case
                    │
       ┌────────────┼────────────┐
       ▼            ▼            ▼
   Engine A      Engine B     Engine C
   Reference      Bitset       Formula
       │            │            │
       └────────────┼────────────┘
                    ▼
              Cross-validation
                    │
                    ▼
              Evidence Ledger
```

Agreement between independent implementations reduces the risk of implementation-specific errors.

It does not remove the distinction between computation and proof.

---

# 18. Related Mathematical Context

The project sits within the broader theory of:

- additive combinatorics;
- iterated sumsets;
- Minkowski sums;
- lattice-point geometry;
- finite-set growth and stabilization;
- additive structure and local defects.

The purpose of this repository is not to reproduce the existing literature, but to make the **additive self-healing observable and its associated conjectures computationally reproducible and formally inspectable**.

Selected references and research-context material are maintained separately in:

```text
docs/LITERATURE_REVIEW.md
```

This keeps the README focused on the research object and its verification status.

---

# 19. Citation

```bibtex
@software{sun2026lattice,
  author  = {Sun, Scott},
  title   = {Lattice Sumset Healing:
             Interior Voids, Iterated Sumsets,
             and Additive Defect-Recovery Thresholds},
  version = {2.17},
  year    = {2026},
  doi     = {10.17605/OSF.IO/CZK8R},
  url     = {https://github.com/suns1232023/lattice-sumset-healing},
  orcid   = {0009-0002-1095-6228}
}
```

For the archived research record, cite the corresponding OSF / Zenodo version.

For the Version 2.17 publication record, the ResearchGate DOI is:

```text
10.13140/RG.2.2.30968.61445
```

---

# 20. Research Philosophy

This repository follows one simple rule:

> **No verification layer silently substitutes for another.**

Mathematical analysis asks:

> Why should the result hold?

Computation asks:

> How broadly does the result survive exact finite testing?

Formalization asks:

> What exactly is the mathematical statement?

Lean asks:

> Does the formal proof term satisfy the formal statement under the declared foundations?

These are related questions, but they are not the same question.

The project therefore aims to maintain a transparent chain:

```text
Mathematical Definition
        ↓
Mathematical Argument
        ↓
Independent Computation
        ↓
Machine-Readable Evidence
        ↓
Lean Formalization
        ↓
Kernel-Checked Proof
        ↓
Reproducible Release
```

The ultimate goal is not merely to obtain more computational confirmations.

It is to make the boundary between **theorem, computation, conjecture, formal statement, and formal proof** explicit enough that every reader can independently determine what has actually been established.
