# Final Visual Evidence Convergence Handoff

**Stage:** `VISUAL_EVIDENCE_CONVERGENCE = DONE`  
**Role:** `MAIN_RESEARCH / VISUAL_CONVERGENCE`  
**Evidence status:** `AI_PROVISIONAL · DEVELOPMENT_ONLY · Formal Gate NOT_RUN`

## Final F1–F6 files

| ID | File | Main placement |
|---|---|---|
| F1 | `reports/visual_evidence/final/F1_model_flow.svg` | Paper method figure; Demo home; 3-minute opening |
| F2 | `reports/visual_evidence/final/F2_raw_vs_adjusted.svg` | Paper result figure; Demo home; P108 explanation |
| F3 | `reports/visual_evidence/final/F3_evidence_degradation.svg` | Paper result figure; Demo home; refusal boundary |
| F4 | `reports/visual_evidence/final/F4_parameter_perturbation.svg` | Paper robustness figure; backup evidence |
| F5 | `reports/visual_evidence/final/F5_ablation_refusal.svg` | Paper ablation/failure figure; backup evidence |
| F6 | `reports/visual_evidence/final/F6_external_structural_transfer.svg` | Paper External Transfer / Limitations; not the education main result |

The placement map is machine-readable in `reports/visual_evidence/final/manifest.json`. The renderer is `reports/visual_evidence/build_final_figures.py`; it only reads existing CSV/JSON artifacts and does not fit, tune, or alter the model.

## Unified visual facts

- Development input: 70 records; 16 readable Evidence; 54 `NO_EFFECTIVE_EVIDENCE`.
- Raw ABL/HOT/Gap = `3.5625 / 0.375 / 1.125`.
- Effective weight/coverage = `16 / 0.228571 → 6 / 0.085714`, denominator `N=70`.
- `HUMAN_R1=0/70 VALID`, `HUMAN_R2=0/70`, Formal Human Gate=`NOT_RUN`.
- `AI_INCREMENT_IDENTIFICATION=NOT_SUPPORTED`.
- Undefined evidence is never rendered as score zero.

## Paper and Demo synchronization

- Paper candidates reference F1–F5 in the main visual evidence section and F6 under external structural transfer / limitations:
  - `paper/submission_candidate.md`
  - `paper/development_submission_candidate.md`
  - `paper/submission_candidate.html`
- Demo home uses exactly the three strongest results and the F1–F3 strip:
  - P108: `L6 → R=.375 → adjusted contribution=2.25 → LOW_SUPPORT / ABSTAIN`.
  - Overall support: `16→6`, coverage `.228571→.085714`, `N=70`.
  - P072: `NO_EFFECTIVE_EVIDENCE`; missing evidence is not zero.
  - `reports/demo/index.html`
- The canonical fact index points to F1–F6:
  - `outputs/final_results.json`

## Stopped mainline references

The following remain as historical artifacts but are no longer referenced by the main Paper/Demo/fact-index chain:

- `reports/development/reliability_sensitivity.svg`
- `reports/development/evidence_reliability_distribution.svg`
- `reports/development/counterexamples.svg`
- `reports/development/core_figure_2_support_heatmap.svg`
- `reports/development/core_figure_3_prompt_vs_effective_evidence.svg`
- `experiments/transfer_finance/figure1-4.svg`
- `reports/external_transfer/three_raw_signals_quality.svg`

## Consistency and risk check

No Paper/Demo/F1–F6 numerical conflict was found after synchronization. The six SVGs pass XML parsing and path/index checks; a separate screenshot-based visual gate for these newly generated SVGs remains a UI-polish follow-up. The remaining research risks are unchanged: missing real Human R1/R2, Formal Gate not run, no paired `Outcome_AI`/`Outcome_baseline`, homogeneous readable development slice, and external transfer being partial structural evidence only. F6 retains Strategy C's ordering failure and a no-trading-claim boundary.

## Change boundary and Git state

- No model, parameter, threshold, data label, Formal Gate, or Human R1/R2 file was changed for visual convergence.
- Current branch: `master`.
- Git HEAD at inspection: `667ecf7e25226366014687aa0ff77cbd80d8df34`.
- Workspace contains existing modifications and untracked project artifacts from prior windows; this stage adds the final visual layer and synchronized references only.

## Next stage

Visual evidence convergence is frozen. The project may proceed to UI polish and Paper polish using these six files, without expanding the figure set or recalculating results. Formal values can replace the development values only after the frozen Human Gate workflow passes.
