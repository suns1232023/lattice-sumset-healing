# Theorems and Conjectures

Complete mathematical statements with explicit epistemic labels.

## Epistemic Labels

| Label | Meaning |
|:------|:--------|
| **[PROVED]** | Unconditional analytic proof |
| **[VHC]** | Validated Heuristic Conjecture: computational evidence, NOT a proof |
| **[OPEN]** | Open problem |

---

## Proved Theorems

### Theorem 3.2 [PROVED — New Result, d≥2]

**Rectangular Box Self-Healing.**

Let $d \geq 2$, $N_i \geq 3$, $A_{\rm full} = \prod_{i=1}^d \{0,\ldots,N_i-1\}$,
and $\varnothing \neq V_{\rm void} \subseteq \operatorname{int}(A_{\rm full})$.
Then $2A_{\rm hole} = 2A_{\rm full}$ and $h^* = 2$.

**Proof (Dispersed Corner Decomposition):**

For any $p \in 2A_{\rm full}$, construct $a', b' \in A_{\rm hole}$ with $a'+b'=p$:

- **Case 1** (boundary-adjacent): Some $p_j \leq N_j-1$. Set $a'_j=p_j$, $b'_j=0$, $a'_i=0$, $b'_i=p_i$ for $i\neq j$. Then $a',b'\in\partial A_{\rm full}$.
- **Case 2a** (pure boundary upper): $p_i=2(N_i-1)$ for all $i$. Set $a'=b'=(N_1-1,\ldots,N_d-1)$.
- **Case 2b** (strictly interior upper): $p_i\in(N_i-1,2(N_i-1))$ for all $i$. Set $c_i=p_i-(N_i-1)$. Choose $\varnothing\neq S\subsetneq\{1,\ldots,d\}$:
$$a'_i=\begin{cases}N_i-1&i\in S\\c_i&i\notin S\end{cases},\quad b'_i=\begin{cases}c_i&i\in S\\N_i-1&i\notin S\end{cases}$$
Then $a'+b'=p$ and $a',b'\in\partial A_{\rm full}\subseteq A_{\rm hole}$.

Since $V_{\rm void}\neq\varnothing$, $h^*>1$, hence $h^*=2$. $\square$

**Remark:** $d\geq 2$ is necessary. For $d=1$, $N=5$, $V=\{1\}$: $1\notin 2A_{\rm hole}$.

---

### Theorem 6.1 [PROVED — New Result, d=1]

**Single-Void Classification.**

Let $N\geq 5$, $A_{\rm full}=\{0,\ldots,N-1\}$, $V_{\rm void}=\{k\}$. Then:
$$h^* = \begin{cases}\infty & k\in\{1,N-2\}\\ 2 & 2\leq k\leq N-3\end{cases}$$

---

### Theorem 7.1 [PROVED — New Result, d=1]

**Multi-Void Classification.**

Let $V_{\rm void}\subseteq\{1,\ldots,N-2\}$. Then:
$$h^*=\infty \iff V_{\rm void}\cap\{1,N-2\}\neq\varnothing$$

---

## Validated Heuristic Conjectures (VHC)

### Conjecture M3' [VHC]

$$h^*(\ell,d)=\left\lceil\frac{\ell}{d-1}\right\rceil+1 \qquad (d\geq 2)$$

**Evidence:** 4,640 cases, three-engine cross-audit, zero counterexamples.
**NOT a mathematical proof.**

### Conjecture 14.3 [VHC]

*Assuming Conjecture M3'*, let $\text{pred}=\max_j h^*_j$. Then:
$$h^*(V_{\rm void})>\text{pred} \iff \text{Criterion A}\lor\text{Criterion B}$$

**Evidence:** 875,658 configurations, FP=0, FN=0.
**NOT a mathematical proof.**

---

## Open Problems

1. Prove Conjecture M3' for all $N$, $\ell$, $d\geq 2$
2. Prove Conjecture 14.3 (Structural Independence)
3. Extend Theorem 3.2 to non-rectangular convex regions
4. Lean 4 formalization of all proved theorems
