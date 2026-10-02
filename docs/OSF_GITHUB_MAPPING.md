# OSF ↔ GitHub Mapping

## Architecture

```
OSF (Research Record)              GitHub (Verification Lab)
──────────────────────             ─────────────────────────
V2.17 Paper (PDF)             →    docs/THEOREMS.md (statements)
Research Materials            →    experiments/ (reproducible audits)
Experimental Records          →    results/ (machine-readable evidence)
Supplementary Data            →    tests/ (invariant checks)
DOI / Persistent Record       →    formalization/ (Lean 4, planned)
Version history               →    CHANGELOG.md (milestones only)
                                   .github/workflows/ (CI/CD)
```

## Single Source of Truth

| Content | Primary Location | Secondary |
|:--------|:---------------:|:---------:|
| Paper PDF | **OSF** | — |
| Full version history | **OSF** | CHANGELOG.md (milestones) |
| Raw experimental data | **OSF** | results/*.csv |
| Source code | **GitHub** | — |
| Lean formalization | **GitHub** | — |
| CI logs | **GitHub** | — |
| DOI | **OSF** | badge in README |

## What NOT to Duplicate

❌ Do NOT copy the paper PDF to GitHub  
❌ Do NOT copy the full 34-version history to GitHub  
❌ Do NOT create a "GitHub copy of OSF"  

This avoids the "which is the latest version?" problem.

## Relationship

```
OSF records "what research happened."
GitHub records "how to verify the research."
Lean records "which mathematical claims are formally proved."
```

## Links

- OSF Project: https://osf.io/czk8r/
- OSF DOI: 10.17605/OSF.IO/CZK8R
- ResearchGate DOI: 10.13140/RG.2.2.30968.61445
- Author ORCID: 0009-0002-1095-6228
