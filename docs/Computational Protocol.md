# Computational Protocol

How to independently reproduce all computational results in Version 2.17.

## Environment

```
Python: 3.9+
OS: Linux / macOS / Windows
Dependencies: none (standard library only)
```

## Installation

```bash
git clone https://github.com/suns1232023/additive-self-healing.git
cd additive-self-healing
pip install -e .
```

## Reproduce All Results

```bash
# Full scope (matches paper claims)
python scripts/run_verification.py --profile full --output-dir results

# Expected output:
# Total: 875,658 | Failures: 0 | Status: PASS
```

## Verify Integrity

```bash
sha256sum results/*.json
diff results/checksums.sha256 -
```

## Reviewer Critical Case

```bash
python -c "
from self_healing import self_healing_threshold, predict_m3_threshold
from self_healing.formulas import block_distance

N, void_set = 7, {3, 4}
d = block_distance(N=7, start=3, length=2)   # d = min(3,2) = 2
h_pred = predict_m3_threshold(ell=2, d=2)    # ceil(2/1)+1 = 3
h_actual = self_healing_threshold(N, void_set)  # -> 3
print(f'd={d}, h_pred={h_pred}, h_actual={h_actual}')
assert h_pred == h_actual == 3
print('PASS: reviewer critical case verified')
"
```

## Three-Engine Cross-Audit (M3')

```bash
python experiments/single_block/run_m3_audit.py --N-max 35 --ell-max 15
# Expected: 4,640 cases, 3-engine agreement, 0 failures
```

## Multi-Block Audit (Conjecture 14.3)

```bash
python experiments/multi_block/run_multiblock_audit.py --N-max 21 --max-blocks 5
# Expected: 397,210 cases, FP=0, FN=0
```

## Epistemic Note

> Computational verification is evidence for conjectures.
> It is NOT a mathematical proof.
> Code can verify a claim; code does not silently upgrade a claim into a theorem.

## OSF Research Record

The paper (V2.17) and full research materials are archived at:
- OSF: https://osf.io/czk8r/ (DOI: 10.17605/OSF.IO/CZK8R)
- ResearchGate: DOI: 10.13140/RG.2.2.30968.61445
