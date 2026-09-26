# 提交前状态快照

生成时间：2026-09-26T16:30:03.605494

HEAD：667ecf7e25226366014687aa0ff77cbd80d8df34

## Git status
```text
 M FORMAL_GATE_SWITCH.md
 M data/annotations/ai/pilot_ai_assisted_full_meta.json
 M data/annotations/human/pilot_worksheet_A.csv
 M handoff/ARTIFACT_INDEX.md
 M handoff/CHANGELOG.md
 M handoff/NEXT_TASK.md
 M handoff/PROJECT_STATE.md
 M paper/submission_candidate.md
 M reports/demo/index.html
 M reports/submission/TEAMID_PENDING_paper_submission_candidate.html
 M src/annotation_gate_report.py
?? .codex-finalizer/
?? data/annotations/workbuddy/
?? docs/claim_boundary.md
?? docs/literature/
?? docs/metric_dictionary.md
?? docs/model_presentation/
?? experiments/
?? handoff/PROJECT_NOW.md
?? outputs/
?? paper/development_submission_candidate.md
?? paper/submission_candidate.html
?? paper/submission_candidate.pdf
?? reports/RESEARCH_GATE_STATUS.md
?? reports/audit/
?? reports/demo/serve_demo.py
?? reports/demo/visual_acceptance.md
?? reports/demo/visual_acceptance/
?? reports/development/ablation_comparison.svg
?? reports/development/accuracy_coverage_audit.json
?? reports/development/counterexamples.svg
?? reports/development/evidence_reliability_distribution.svg
?? reports/development/explain_records.json
?? reports/development/identifiability_audit.csv
?? reports/development/identifiability_audit.json
?? reports/development/parameter_sensitivity.svg
?? reports/development/provenance_separation_audit.csv
?? reports/development/provenance_separation_audit.json
?? reports/development/raw_vs_adjusted_scatter.svg
?? reports/development/robustness_validation_summary.md
?? reports/development/what_if_sensitivity.csv
?? reports/external_transfer/
?? reports/failure_cases/
?? reports/model_paper_consistency_audit.md
?? reports/perturbation/
?? reports/reliability_component_audit.md
?? reports/review/claim_audit.md
?? reports/review/competition_alignment_audit.md
?? reports/robustness/
?? reports/verification/development_submission_consistency.json
?? reports/verification/experiment_runner_consistency.json
?? reports/verification/formal_preflight.json
?? reports/verification/untracked_files_audit_2026-09-26.json
?? reports/workbuddy_annotation_audit.json
?? reports/workbuddy_annotation_audit.md
?? reports/workbuddy_annotation_summary.json
?? reports/workbuddy_annotation_summary.md
?? slides/
?? src/accuracy_coverage_audit.py
?? src/build_core_figures.py
?? src/build_development_demo.py
?? src/build_final_artifact.py
?? src/build_submission_candidate.py
?? src/development_submission_checker.py
?? src/failure_case_pipeline.py
?? src/formal_input_adapter.py
?? src/formal_validation_pipeline.py
?? src/run_robustness_validation.py
```

## Model / data identity
- Model version: frozen deterministic Raw → Reliability → Adjusted → Decision chain; no parameter or threshold change.
- Data identity: `AI_PROVISIONAL / DEVELOPMENT_ONLY`, 70 development records; 16 readable Evidence.
- Human Gate: `PENDING_REAL_HUMAN_R1_R2` / 0/70 VALID.
- Formal Gate: `NOT_RUN`; formal preflight: `BLOCKED`.
- AI increment identification: `NOT_SUPPORTED`.

## Artifact manifest

- `paper/submission_candidate.md` — SHA256 `9e631fcb261096d0a35ccd46d9b3261cf4acad354f92fe8fb4951472b6010932`
- `paper/development_submission_candidate.md` — SHA256 `d85ec5486581e18f6b2c3cbf06af78a9a09d319cbd5a4f31207a8fcb8c4e13c3`
- `paper/submission_candidate.html` — SHA256 `6847737d275eea7d1f5e17bec89a14ca2d80d1eb333ba8c24a73e3c6ff80a4d4`
- `reports/demo/index.html` — SHA256 `491fc13aa715b6ecd937d220233bdd46c15cb4cf8efaf66fdb0cf4f417ef91e8`
- `reports/demo/demo_payload.json` — SHA256 `ef9ab8e5950cc7a699e598529c65ed1a50ae0c8a8a108a53faa5b7df228677e8`
- `outputs/final_results.json` — SHA256 `89bbeab627285f9dd8024f9bc8ef0e34a66a85ac1c180df7dc2d41936b05ce8a`
- `reports/verification/development_submission_consistency.json` — SHA256 `c99b10c139940fadd813fb24940d140a241daae1ef5e45d058d1a4aae67f79d9`
- `reports/verification/formal_preflight.json` — SHA256 `3e9fb6ca7bc6f6fb158b220aa31f5c24200d76694a18817af137654c1c2e3304`
- `reports/development/robustness_validation_summary.md` — SHA256 `69beb18c56a4dd9b555382e69a142daa79de07de21c189b52b6a56ae35093a17`
- `reports/robustness/parameter_perturbation_summary.json` — SHA256 `91175afd9b2e78b04bc8bcf71dc40db8bac58bb6642abfd0155b87f4c59a4f56`
- `reports/perturbation/controlled_parameter_variants.csv` — SHA256 `e7d9a83afa72370bd33ea9484084d25e9b99bafae5fcf540379058809c8d44c3`
- `reports/external_transfer/external_transfer_summary.json` — SHA256 `51281e0f40af18368b7ab3cb94a3d0066f4fcf5aa6071263ba0f08ce7dd8a4a4`
- `src/build_final_artifact.py` — SHA256 `c40e94de77096cbc449a496c04e4c14da5aaea402d83ed054ef22633f877d1dd`
- `src/run_robustness_validation.py` — SHA256 `2c457bbadb7e382c8431a0e92cfbbb313b0f3c0987df57e5a1c586631e165f5e`
- `experiments/transfer_finance/run_cross_strategy_validation.py` — SHA256 `e4001f26ba6847c980df35c557b1d3c52c7a679a346398c6b6c63f0343a33c69`

## Known limitations
- No formal human annotation reliability result.
- No paired Outcome_AI / Outcome_baseline.
- Parameter perturbation supports only development-stage structural stability on the current slice.
- Formal student-level ranking is NOT_APPLICABLE.
- External transfer is development-only structural support / operational feasibility, not proof of cross-domain generalization.

## Validation checks
- `run_all.py`: 32/32 passed.
- `src/development_submission_checker.py`: PASS.
- Formal preflight remains BLOCKED; no formal metrics written.