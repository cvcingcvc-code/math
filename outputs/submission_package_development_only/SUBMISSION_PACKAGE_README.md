# Development Submission Package

This package is ready for internal review, rehearsal, and development-only demonstration.

## Status boundary

- `AI_PROVISIONAL`
- `DEVELOPMENT_ONLY`
- `formal_gate_eligible=false`
- `Formal AIV = NOT_AVAILABLE_PENDING_FORMAL_GATE`
- No R1/R2 labels or formal Gate judgment is included.

## Contents

- `paper/`: current paper PDF/HTML candidate
- `slides/`: complete roadshow deck
- `demo/`: self-contained browser demo and payload
- `reproduction/`: run instructions, run report, and development CSV outputs
- `reports/`: core metrics, ablation, counterexamples, and numeric consistency records
- `data/`: canonical Pilot V1 and AI exploratory prelabels
- `src/`: development-only reproduction scripts

## Reproduce

From the project root:

```text
python run_all.py
```

Expected result: `PASS` with 32 checks. The chain never reads human R1/R2 labels. Formal mode remains fail-closed:

```text
python run_all.py --mode formal
```

## Core numbers

- 70 development records, 16 interpretable Evidence
- Raw and adjusted ABL/HOT/Gap: `3.5625 / 0.375 / 1.125`
- Effective weight: `16 → 6`
- Effective coverage: `0.228571 → 0.085714`, denominator 70
- Zero effective weight returns `NO_EFFECTIVE_EVIDENCE`

The central statement is: **Score stability does not imply Evidence Support stability.**
