# Development Submission Package

This package is ready for internal review, rehearsal, and development-only demonstration.

## Status boundary

- `AI_PROVISIONAL`
- `DEVELOPMENT_ONLY`
- `formal_gate_eligible=false`
- `Formal AIV = NOT_AVAILABLE_PENDING_FORMAL_GATE`
- No R1/R2 labels or formal Gate judgment is included.

## Contents

- `paper/`: final paper PDF/Markdown/editable DOCX plus submission candidate copies
- `slides/`: complete 10-page final roadshow deck
- `demo/`: self-contained Chinese browser demo and payload
- `development/`: final F1–F6 SVG evidence figures
- `reproduction/`: run instructions, run report, and development CSV outputs
- `reports/`: core metrics, ablation, counterexamples, and numeric consistency records
- `data/`: canonical Pilot V1 and AI exploratory prelabels
- `src/`: development-only reproduction scripts

## Reproduce

From the project root:

```text
python run_all.py
```

The chain never reads human R1/R2 labels. The included package contains the frozen development outputs and audit records; Formal mode remains fail-closed:

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
