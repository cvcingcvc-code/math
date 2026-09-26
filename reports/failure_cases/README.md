# Failure case pipeline

Each formal run must export one row per case with: `case_id`, `case_type`, `record_id`, `raw_score`, `reliability`, `adjusted_score`, `decision`, `true_label` (when available), `source_sha256`, `status`.

- **F1 High Reliability but Wrong**: `reliability >=` the frozen high-support rule and the validated outcome/label is wrong.
- **F2 Low Reliability but Correct / unnecessary abstention**: low support or `ABSTAIN` while the validated outcome/label is correct.
- **F3 Conflicting evidence**: materially conflicting evidence produces unstable decision/status across the frozen sensitivity or repeat-label checks.

Current candidate extraction from AI provisional data is `DEVELOPMENT_ONLY` and cannot establish correctness. Human-labeled cases replace candidates after Gate PASS.
