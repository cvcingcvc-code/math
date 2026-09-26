# MULTIPROCESS STATE

> Single Source of Truth for Codex windows working on the competition project.
> Read this file after the canonical handoff files. Edit it through `scripts/project_manager.py` when possible.

- PROJECT: `C:\Users\lin\Documents\Codex\2026-09-25\yu`
- STATUS: `ACTIVE_WITH_FORMAL_BLOCKER`
- LAST_UPDATED: `2026-09-26T18:22:29+08:00`
- MAIN_WINDOW: `NONE`
- CURRENT_PHASE: `MAIN_RESEARCH / PRESENTATION_CONVERGENCE`
- FORMAL_GATE_STATUS: `NOT_RUN`
- HUMAN_GATE_STATUS: `BLOCKED_BY_HUMAN_ANNOTATION`

## WORKSTREAMS

| Workstream | Status | Owner | Task | Evidence / boundary |
|---|---|---|---|---|
| MAIN_RESEARCH | FROZEN | - | Research story human review and freeze preparation: audit summary against disk, Git, handoff, and experiment state; write freeze review only | handoff/PROJECT_NOW.md |
| BASELINE | FROZEN | - | Development-only raw/rule/linear baseline evidence is recorded | experiments/model_tournament/baselines/ |
| ML_CHALLENGER | HANDOFF_COMPLETE | - | Development challenger handoff complete with bounded claim | experiments/model_tournament/ML_CHALLENGER_HANDOFF.md |
| ALTERNATIVE_FORMULATIONS | FROZEN | - | Multiplicative/additive/gated/nonlinear comparison complete | experiments/model_tournament/formulations/ |
| EXTERNAL_TRANSFER | HANDOFF_COMPLETE | - | Auxiliary structural transfer is documented | experiments/transfer_finance/ |
| AUDIT | RUNNING | WINDOW_20260926_180938 | Window 3 Experiment Registry / Single Source of Truth: reconcile formal experiment artifacts and create registry deliverables without changing experiments, model, labels, or demo styling | reports/audit/ |
| LITERATURE | PARTIAL | - | Model support matrix exists; canonical literature review remains absent | docs/literature/model_support_matrix.md |
| FIGURES | FROZEN | - | Core figures and captions are complete for development package | reports/development/ |
| DEMO_UI | REVIEW_REQUIRED | - | Visual gate passed; numerical consistency review remains open | reports/demo/visual_acceptance.md |
| PAPER | WAITING | - | Development-only paper candidate ready pending Formal values | paper/submission_candidate.* |
| PPT | FROZEN | - | Ten-slide roadshow deck complete; styling paused | outputs/education_ai_evidence_roadshow_final.pptx |
| MODEL_PRESENTATION | FROZEN | - | Model overview, stories, QA, and script are converged | docs/model_presentation/ |
| HUMAN_GATE | BLOCKED | - | Owner completes R1, waits 24h, completes R2, then runs Gate | reports/annotation_gate_report.json |
| FORMAL_VALIDATION | BLOCKED | - | Fail-closed until real Human Gate PASS | FORMAL_GATE_SWITCH.md |
| SUBMISSION | WAITING | - | Development-only package may be reviewed with boundaries visible | outputs/submission_package_development_only/ |

## ACTIVE_WINDOWS

| Window | Role | Mode | Status | Scope | Task | Last update |
|---|---|---|---|---|---|---|
| WINDOW_20260926_180857 | AUDIT | READONLY | RUNNING | - | DATA_EVIDENCE_AUDIT / SAMPLE_STRUCTURE; audit effective evidence, homogeneity, validation coverage, claim support, and post-Human-Gate recheck checklist; independent reports only | 2026-09-26T18:09:16+08:00 |
| WINDOW_20260926_180938 | AUDIT | WRITE | RUNNING | AUDIT_REGISTRY | Window 3 Experiment Registry / Single Source of Truth: reconcile formal experiment artifacts and create registry deliverables without changing experiments, model, labels, or demo styling | 2026-09-26T18:22:29+08:00 |
| WINDOW_20260926_181033 | FORMAL_VALIDATION | READONLY | REGISTERED | - | POST_GATE_RETEST protocol audit; read-only evidence and blockers; independent report only | 2026-09-26T18:10:33+08:00 |
| WINDOW_20260926_181208 | FORMAL_VALIDATION | READONLY | RUNNING | - | FORMAL_HUMAN_VALIDATION / POST_GATE_RETEST: fail-closed readiness audit and post-human validation workflow; no Gate execution before complete R1/R2 | 2026-09-26T18:13:43+08:00 |

## WRITE_LOCKS

| Scope | Owner |
|---|---|
| AUDIT_REGISTRY | WINDOW_20260926_180938 |

## READONLY_TASKS

- Red-team audit
- Literature review
- Claim checks
- Figure planning
- Failure-case checks
- Reproducibility checks
- File-consistency checks

## PENDING_HANDOFFS

- None

## KNOWN_RISKS

- Real HUMAN_R1/R2 labels are missing; Formal Gate is NOT_RUN.
- Development inputs are AI_PROVISIONAL / DEVELOPMENT_ONLY.
- Latest audit reports Demo/unified-artifact numerical conflicts.
- No paired Outcome_AI / Outcome_baseline supports a causal increment claim.
- The worktree is dirty and contains untracked deliverables; do not reset or delete.

## NEXT_ALLOWED_TASKS

- Owner completes R1, waits at least 24h, completes R2, then runs python src/run_s4_gate.py.
- A READONLY audit may reconcile the listed Demo/artifact conflicts in an independent report.
- MAIN_RESEARCH may open an explicitly bounded supplement after reading existing handoff.

## MACHINE_STATE

<!-- MULTIPROCESS_STATE_JSON_START -->
{
  "PROJECT": "C:\\Users\\lin\\Documents\\Codex\\2026-09-25\\yu",
  "STATUS": "ACTIVE_WITH_FORMAL_BLOCKER",
  "LAST_UPDATED": "2026-09-26T18:22:29+08:00",
  "MAIN_WINDOW": null,
  "CURRENT_PHASE": "MAIN_RESEARCH / PRESENTATION_CONVERGENCE",
  "FORMAL_GATE_STATUS": "NOT_RUN",
  "HUMAN_GATE_STATUS": "BLOCKED_BY_HUMAN_ANNOTATION",
  "ACTIVE_WINDOWS": [
    {
      "window_id": "WINDOW_20260926_180857",
      "role": "AUDIT",
      "task": "DATA_EVIDENCE_AUDIT / SAMPLE_STRUCTURE; audit effective evidence, homogeneity, validation coverage, claim support, and post-Human-Gate recheck checklist; independent reports only",
      "mode": "READONLY",
      "status": "RUNNING",
      "write_scope": null,
      "started_at": "2026-09-26T18:08:57+08:00",
      "last_update": "2026-09-26T18:09:16+08:00",
      "handoff_path": "handoff\\multiprocess\\WINDOW_20260926_180857.md",
      "pid": 21988,
      "cwd": "C:\\Users\\lin\\Documents\\Codex\\2026-09-25\\yu",
      "workstream_status_before": "REVIEW_REQUIRED"
    },
    {
      "window_id": "WINDOW_20260926_180938",
      "role": "AUDIT",
      "task": "Window 3 Experiment Registry / Single Source of Truth: reconcile formal experiment artifacts and create registry deliverables without changing experiments, model, labels, or demo styling",
      "mode": "WRITE",
      "status": "RUNNING",
      "write_scope": "AUDIT_REGISTRY",
      "started_at": "2026-09-26T18:09:38+08:00",
      "last_update": "2026-09-26T18:22:29+08:00",
      "handoff_path": "handoff\\multiprocess\\WINDOW_20260926_180938.md",
      "pid": 12104,
      "cwd": "C:\\Users\\lin\\Documents\\Codex\\2026-09-25\\yu",
      "workstream_status_before": "REVIEW_REQUIRED"
    },
    {
      "window_id": "WINDOW_20260926_181033",
      "role": "FORMAL_VALIDATION",
      "task": "POST_GATE_RETEST protocol audit; read-only evidence and blockers; independent report only",
      "mode": "READONLY",
      "status": "REGISTERED",
      "write_scope": null,
      "started_at": "2026-09-26T18:10:33+08:00",
      "last_update": "2026-09-26T18:10:33+08:00",
      "handoff_path": "handoff\\multiprocess\\WINDOW_20260926_181033.md",
      "pid": 20564,
      "cwd": "C:\\Users\\lin\\Documents\\Codex\\2026-09-25\\yu",
      "workstream_status_before": "BLOCKED"
    },
    {
      "window_id": "WINDOW_20260926_181208",
      "role": "FORMAL_VALIDATION",
      "task": "FORMAL_HUMAN_VALIDATION / POST_GATE_RETEST: fail-closed readiness audit and post-human validation workflow; no Gate execution before complete R1/R2",
      "mode": "READONLY",
      "status": "RUNNING",
      "write_scope": null,
      "started_at": "2026-09-26T18:12:08+08:00",
      "last_update": "2026-09-26T18:13:43+08:00",
      "handoff_path": "handoff\\multiprocess\\WINDOW_20260926_181208.md",
      "pid": 4444,
      "cwd": "C:\\Users\\lin\\Documents\\Codex\\2026-09-25\\yu",
      "workstream_status_before": "BLOCKED"
    }
  ],
  "COMPLETED_WORKSTREAMS": [
    "BASELINE",
    "ML_CHALLENGER",
    "ALTERNATIVE_FORMULATIONS",
    "EXTERNAL_TRANSFER",
    "FIGURES",
    "MODEL_PRESENTATION",
    "PPT"
  ],
  "FROZEN_WORKSTREAMS": [
    "BASELINE",
    "ALTERNATIVE_FORMULATIONS",
    "FIGURES",
    "MODEL_PRESENTATION",
    "PPT"
  ],
  "WRITE_LOCKS": {
    "AUDIT_REGISTRY": "WINDOW_20260926_180938"
  },
  "READONLY_TASKS": [
    "Red-team audit",
    "Literature review",
    "Claim checks",
    "Figure planning",
    "Failure-case checks",
    "Reproducibility checks",
    "File-consistency checks"
  ],
  "PENDING_HANDOFFS": [],
  "KNOWN_RISKS": [
    "Real HUMAN_R1/R2 labels are missing; Formal Gate is NOT_RUN.",
    "Development inputs are AI_PROVISIONAL / DEVELOPMENT_ONLY.",
    "Latest audit reports Demo/unified-artifact numerical conflicts.",
    "No paired Outcome_AI / Outcome_baseline supports a causal increment claim.",
    "The worktree is dirty and contains untracked deliverables; do not reset or delete."
  ],
  "NEXT_ALLOWED_TASKS": [
    "Owner completes R1, waits at least 24h, completes R2, then runs python src/run_s4_gate.py.",
    "A READONLY audit may reconcile the listed Demo/artifact conflicts in an independent report.",
    "MAIN_RESEARCH may open an explicitly bounded supplement after reading existing handoff."
  ],
  "WORKSTREAMS": {
    "MAIN_RESEARCH": {
      "status": "FROZEN",
      "owner": null,
      "task": "Research story human review and freeze preparation: audit summary against disk, Git, handoff, and experiment state; write freeze review only",
      "mode": "WRITE",
      "write_scope": null,
      "priority": "P0",
      "dependency": "HUMAN_GATE",
      "evidence": "handoff/PROJECT_NOW.md",
      "risk": "No unilateral research-direction change"
    },
    "BASELINE": {
      "status": "FROZEN",
      "owner": null,
      "task": "Development-only raw/rule/linear baseline evidence is recorded",
      "mode": null,
      "write_scope": null,
      "priority": "P2",
      "dependency": null,
      "evidence": "experiments/model_tournament/baselines/",
      "risk": "Final matrix still marks Simple Linear as PENDING"
    },
    "ML_CHALLENGER": {
      "status": "HANDOFF_COMPLETE",
      "owner": null,
      "task": "Development challenger handoff complete with bounded claim",
      "mode": null,
      "write_scope": null,
      "priority": "P2",
      "dependency": "FORMAL_GATE",
      "evidence": "experiments/model_tournament/ML_CHALLENGER_HANDOFF.md",
      "risk": "No strong ML claim or winner"
    },
    "ALTERNATIVE_FORMULATIONS": {
      "status": "FROZEN",
      "owner": null,
      "task": "Multiplicative/additive/gated/nonlinear comparison complete",
      "mode": null,
      "write_scope": null,
      "priority": "P2",
      "dependency": null,
      "evidence": "experiments/model_tournament/formulations/",
      "risk": "NO_SINGLE_DOMINANT_MODEL"
    },
    "EXTERNAL_TRANSFER": {
      "status": "HANDOFF_COMPLETE",
      "owner": null,
      "task": "Auxiliary structural transfer is documented",
      "mode": null,
      "write_scope": null,
      "priority": "P2",
      "dependency": "FORMAL_GATE",
      "evidence": "experiments/transfer_finance/",
      "risk": "No trading/generalization claim; shadow has 0 evaluated records"
    },
    "AUDIT": {
      "status": "RUNNING",
      "owner": "WINDOW_20260926_180938",
      "task": "Window 3 Experiment Registry / Single Source of Truth: reconcile formal experiment artifacts and create registry deliverables without changing experiments, model, labels, or demo styling",
      "mode": "WRITE",
      "write_scope": "AUDIT_REGISTRY",
      "priority": "P1",
      "dependency": null,
      "evidence": "reports/audit/",
      "risk": "4 conflicts, 3 stale rows, 4 not-run checks"
    },
    "LITERATURE": {
      "status": "PARTIAL",
      "owner": null,
      "task": "Model support matrix exists; canonical literature review remains absent",
      "mode": null,
      "write_scope": null,
      "priority": "P2",
      "dependency": null,
      "evidence": "docs/literature/model_support_matrix.md",
      "risk": "literature_review_v1.md not found"
    },
    "FIGURES": {
      "status": "FROZEN",
      "owner": null,
      "task": "Core figures and captions are complete for development package",
      "mode": null,
      "write_scope": null,
      "priority": "P2",
      "dependency": "MAIN_RESEARCH",
      "evidence": "reports/development/",
      "risk": "Do not rerun without bounded task"
    },
    "DEMO_UI": {
      "status": "REVIEW_REQUIRED",
      "owner": null,
      "task": "Visual gate passed; numerical consistency review remains open",
      "mode": null,
      "write_scope": null,
      "priority": "P1",
      "dependency": "AUDIT",
      "evidence": "reports/demo/visual_acceptance.md",
      "risk": "Raw/default conflicts in latest audit"
    },
    "PAPER": {
      "status": "WAITING",
      "owner": null,
      "task": "Development-only paper candidate ready pending Formal values",
      "mode": null,
      "write_scope": null,
      "priority": "P1",
      "dependency": "HUMAN_GATE",
      "evidence": "paper/submission_candidate.*",
      "risk": "Formal numbers and transfer appendix remain pending"
    },
    "PPT": {
      "status": "FROZEN",
      "owner": null,
      "task": "Ten-slide roadshow deck complete; styling paused",
      "mode": null,
      "write_scope": null,
      "priority": "P2",
      "dependency": null,
      "evidence": "outputs/education_ai_evidence_roadshow_final.pptx",
      "risk": "Do not modify until user reopens PPT work"
    },
    "MODEL_PRESENTATION": {
      "status": "FROZEN",
      "owner": null,
      "task": "Model overview, stories, QA, and script are converged",
      "mode": null,
      "write_scope": null,
      "priority": "P2",
      "dependency": null,
      "evidence": "docs/model_presentation/",
      "risk": "Formal/Human status unchanged"
    },
    "HUMAN_GATE": {
      "status": "BLOCKED",
      "owner": null,
      "task": "Owner completes R1, waits 24h, completes R2, then runs Gate",
      "mode": null,
      "write_scope": null,
      "priority": "P0",
      "dependency": null,
      "evidence": "reports/annotation_gate_report.json",
      "risk": "AI labels cannot substitute"
    },
    "FORMAL_VALIDATION": {
      "status": "BLOCKED",
      "owner": null,
      "task": "Fail-closed until real Human Gate PASS",
      "mode": null,
      "write_scope": null,
      "priority": "P0",
      "dependency": "HUMAN_GATE",
      "evidence": "FORMAL_GATE_SWITCH.md",
      "risk": "No formal metrics or AIV"
    },
    "SUBMISSION": {
      "status": "WAITING",
      "owner": null,
      "task": "Development-only package may be reviewed with boundaries visible",
      "mode": null,
      "write_scope": null,
      "priority": "P1",
      "dependency": "HUMAN_GATE",
      "evidence": "outputs/submission_package_development_only/",
      "risk": "Formal submission closure is not allowed"
    }
  },
  "WINDOW_HISTORY": [
    {
      "window_id": "WINDOW_20260926_175451",
      "role": "MAIN_RESEARCH",
      "task": "Research story convergence and evidence integration: research question, rationale, main conclusion, five-line validation, summary",
      "mode": "WRITE",
      "status": "FROZEN",
      "write_scope": "CORE_MODEL",
      "started_at": "2026-09-26T17:54:51+08:00",
      "last_update": "2026-09-26T18:05:48+08:00",
      "handoff_path": "C:\\Users\\lin\\Documents\\Codex\\2026-09-25\\yu\\handoff\\multiprocess\\WINDOW_20260926_175451.md",
      "pid": 5580,
      "cwd": "C:\\Users\\lin\\Documents\\Codex\\2026-09-25\\yu",
      "workstream_status_before": "WAITING"
    },
    {
      "window_id": "WINDOW_20260926_181347",
      "role": "MAIN_RESEARCH",
      "task": "Research story human review and freeze preparation: audit summary against disk, Git, handoff, and experiment state; write freeze review only",
      "mode": "WRITE",
      "status": "FROZEN",
      "write_scope": "CORE_MODEL",
      "started_at": "2026-09-26T18:13:47+08:00",
      "last_update": "2026-09-26T18:20:23+08:00",
      "handoff_path": "C:\\Users\\lin\\Documents\\Codex\\2026-09-25\\yu\\handoff\\multiprocess\\WINDOW_20260926_181347.md",
      "pid": 21456,
      "cwd": "C:\\Users\\lin\\Documents\\Codex\\2026-09-25\\yu",
      "workstream_status_before": "FROZEN"
    }
  ]
}
<!-- MULTIPROCESS_STATE_JSON_END -->
