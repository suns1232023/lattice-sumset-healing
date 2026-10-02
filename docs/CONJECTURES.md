# Conjecture Registry

All conjectures with explicit status, evidence, and open questions.

## Status Labels

| Label | Meaning |
|:------|:--------|
| **[VHC]** | Validated Heuristic Conjecture: extensive computational evidence |
| **[OPEN]** | Open conjecture, limited evidence |

> **Epistemic note:** Computational verification is NOT mathematical proof.
> VHC status means: strong finite evidence, no counterexample found, no proof.

---

## Conjecture M3' [VHC]

**Single-Block Healing Formula**

$$h^*(\ell, d) = \left\lceil\frac{\ell}{d-1}\right\rceil + 1$$

where $\ell$ = void block length, $d = \min(\text{left}, \text{right})$ (0-based).

**Heuristic:** The left segment $\{0,\ldots,d-1\}$ gains $d-1$ new reachable
elements per Minkowski addition round, requiring $\lceil\ell/(d-1)\rceil$ rounds
to bridge the gap, plus 1 for the initial step.

**Algebraic identity (definition-level, not empirical):**
$(h-1)(d-1) \geq \ell > (h-2)(d-1)$

**Computational evidence:**

| Scope | Cases | Engines | FP | FN |
|:------|------:|:-------:|:--:|:--:|
| N≤35, ℓ≤15, d≥2 | 4,640 | 3 / 3 | 0 | 0 |

**Lean formalization:** planned

**Open:** Analytic proof for all N, ℓ, d ≥ 2.

---

## Conjecture 14.3 [VHC]

**Multi-Block Structural Independence**

*Assuming Conjecture M3'*, let $V_{\rm void} = B_1 \cup \cdots \cup B_k$ ($k\geq 2$)
and $\text{pred} = \max_j h^*_j$. Then:

$$h^*(V_{\rm void}) > \text{pred} \iff \text{Criterion A} \lor \text{Criterion B}$$

**Criterion A:** $\exists$ synergistic collapse point $p \in 2A_{\rm full}$
with $p \notin \text{pred} \cdot H$.

**Criterion B:** $\exists p \in \text{pred} \cdot A_{\rm full} \setminus (\text{pred}-1) \cdot A_{\rm full}$
with $p \notin \text{pred} \cdot H$.

**Computational evidence:**

| Scope | Cases | FP | FN |
|:------|------:|:--:|:--:|
| N≤21, r≤5 (exact) | 397,210 | 0 | 0 |
| N≤35, gap≤1 (adversarial) | 478,448 | 0 | 0 |
| **Total** | **875,658** | **0** | **0** |

**Lean formalization:** planned

**Open:** Analytic proof. Chapter A (single-block absorption) and
Chapter D (gap≥3 routing) are incomplete proof sketches.

---

## Conjecture 4.3 [OPEN]

**8-Neighbor Boundary Witness Principle**

For any convex lattice region $A_{\rm full} = P \cap \mathbb{Z}^d$ ($d\geq 2$)
and any $V_{\rm void} \subseteq \operatorname{int}_8(A_{\rm full})$:
$$2(A_{\rm full} \setminus V_{\rm void}) = 2A_{\rm full}$$

**Status:** Verified for rectangular boxes (Theorem 3.2), hexagons, triangles,
diamonds in 2D. General convex regions: open.
