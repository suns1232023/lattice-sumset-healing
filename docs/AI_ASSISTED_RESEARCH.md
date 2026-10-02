# AI-Assisted Research — Provenance Record

## Principle

AI systems assist formalization and exploration.
They do not constitute mathematical proof.

## Epistemic Authority Chain

```
Human mathematical claim
        ↓
AI-assisted translation / candidate generation
        ↓
Human review and verification
        ↓
Lean 4 elaboration
        ↓
Lean kernel verification  ← FINAL AUTHORITY
```

## What AI Systems Were Used For

- Candidate Lean 4 statement generation
- Python code generation and review
- Documentation drafting
- Proof search suggestions
- Counterexample search

## What AI Systems Were NOT Used For

- Establishing mathematical truth
- Replacing human mathematical judgment
- Replacing Lean kernel verification

## Epistemic Labels

| Label | Meaning | AI role |
|:------|:--------|:--------|
| [PROVED] | Lean kernel verified | Assisted formalization |
| [VHC] | Computational evidence | Assisted code generation |
| [OPEN] | No proof | Assisted exploration |

## Note on Model Names

Specific AI model names are intentionally omitted.
Models change rapidly; this repository should remain valid for 10+ years.
The Lean kernel is the stable epistemic anchor.

## Key Distinction

```
AI generated Lean code  ≠  AI proved mathematics
```

The Lean kernel — not any AI system — is the final judge of formal proofs.
