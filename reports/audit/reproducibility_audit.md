# Reproducibility Audit Summary

Date: 2026-09-26
Project root: `C:\Users\lin\Documents\Codex\2026-09-25\yu`

## 0. Restored state

- Git HEAD: `667ecf7e25226366014687aa0ff77cbd80d8df34` on `master`.
- Current worktree: 11 tracked modified paths and 235 untracked entries; it is not clean.
- Handoff: S4 Pilot Annotation Gate blocked by missing real Human R1/R2; development source is 70-row AI provisional data; Formal Gate is NOT_RUN.

## 1. Is the project reproducible?

**Development core experiment: conditionally reproducible.** Starting from the frozen 70-row `data/annotations/ai/pilot_ai_provisional.csv`, `python run_all.py` has six passing steps and 32 passing checks. Independent recomputation reproduces 70/16/19/35, 693/660/33, ABL/HOT/Gap, and weight/coverage bounds.

**Full Code -> Data -> Experiment -> Figure -> Demo -> Paper chain: not proven fully reproducible.** The provisional-label generation script is missing; `run_all.py` does not build the final artifact/figures/Paper/Demo; and two different Demo implementations exist.

## 2. Number of conflicts

The matrix has **4 `CONFLICT` rows** (the first two are two numeric manifestations of the same Demo raw/baseline naming issue):

1. Demo payload labels confidence-only theta0 12/70 as raw/baseline; unified artifact M0 Raw is 16/70, with the corresponding coverage difference 0.171429 vs 0.228571.
2. Demo defaults are lambda_prompt=0, lambda_context=0, r_medium=.75; unified adjusted defaults are .5/.5/.75.
3. Failure-case candidate export writes null raw/adjusted values for P105/P108/P072/P035 while core counterexamples and Paper/Demo provide numeric values for P105/P108.

Additional statuses: **3 `STALE`** rows (old Git receipt, old paper-directory audit, and the older submission-package Paper/Demo) and **4 `NOT_RUN`** rows (full derivative chain, provisional-label generation, accuracy/true-label failure-case audit, and runtime/requirements alignment).

## 3. Highest-risk conflicts

- Demo raw/baseline semantics and default parameters are not aligned with the unified artifact.
- The submission package carries an older Demo/Paper presentation and a separate payload wiring path; it should not be treated as the current workspace output.
- Provisional labels cannot be clean-rebuilt from the Canonical Pilot; only the frozen 70-row file can be recomputed.
- Formal Gate remains blocked: R1/R2 are 0 and Formal Gate is NOT_RUN. Do not promote development results to Formal AIV, accuracy, causal increment, or formal reliability.

## 4. Paper / Demo / Model consistency

- **Paper core table vs final artifact: consistent** (ABL/HOT/Gap 3.5625/.375/1.125; weight 16 -> 6; coverage .228571 -> .085714).
- **Demo vs model: conflict** (Demo payload raw/baseline 12/.171429 vs M0 raw 16/.228571; default parameter layer differs; main Demo is hard-coded).
- **Failure cases vs model: conflict** (P105/P108 null vs numeric).

## 5. Results without traceable origin

Yes. `pilot_ai_provisional.csv` has metadata but no executable generation script or row-level generation log. `outputs/final_results.json` also lacks input hash, Git HEAD, environment versions, and a derivative manifest.

## 6. Must fix tonight (MAIN_RESEARCH / CONVERGENCE)

- Unify Demo raw/M0, theta0/M1, and adjusted/M3 naming and defaults.
- Repair or quarantine null failure-case outputs.
- Add input SHA256, Git HEAD, Python/package versions, output manifest, and explicit post-processing steps for final artifact/figures/Paper/Demo.

## 7. Can wait until before submission

- Clean old audit receipts and synchronize package vs current Paper/Demo.
- Keep external-transfer numbers and Gate3/risk-coverage failure boundaries in the appendix.
- State `effective weight / 70 development records` on first coverage use in the formal paper.
- Run the formal adapter and replace development values only after Formal Gate PASS.

## 8. Minimal reproduction command chain

```powershell
cd C:\Users\lin\Documents\Codex\2026-09-25\yu
py -3.13 -m venv .venv
.venv\Scripts\python -m pip install --only-binary=:all: -r requirements.txt
.venv\Scripts\python run_all.py
# Expected: reports/submission/run_all_report.json -> PASS; 6 steps; 32/32 checks
.venv\Scripts\python run_all.py --mode formal
# Expected: FORMAL_MODE_BLOCKED while Gate is not PASS
```

This read-only audit is complete; no mainline files were modified. Detailed matrix: [`numerical_consistency_matrix.md`](numerical_consistency_matrix.md).
