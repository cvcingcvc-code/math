# Model Trade-off Figure Specification

**Purpose:** reusable Demo/PPT figure for explaining model choice without ranking candidates.

## Design

- **Chart type:** two-dimensional trade-off map with labeled candidate points and a five-dimension annotation strip.
- **X-axis:** missing-evidence safety, increasing from “confident output without support” to “explicit abstain/undefined semantics”.
- **Y-axis:** research-question alignment, increasing from “observed score only” to “observable performance plus evidence support”.
- **Point size:** interpretability/transparency, larger means easier record-level audit.
- **Point outline:** robustness/sensitivity status: solid for reproducible development checks, dashed when formal validation is pending.
- **Point label suffix:** additional assumptions/complexity (`low`, `threshold`, `lambda`, or `gamma`); descriptive only.

## Candidate placement

- **Current Evidence Reliability Model:** upper-middle/right; large point; low structural complexity; dashed outline for pending formal validation.
- **Raw-only Baseline:** left/lower-middle; largest point; lowest complexity.
- **Rule-based Gated Baseline:** far right/middle; large point; threshold marker; emphasize coverage cost.
- **Multiplicative Formulation:** upper-right near the current model; large point; no extra attenuation parameter.
- **Additive Formulation:** middle; lambda marker; annotate “weak-evidence output can remain high”.
- **Nonlinear Formulation:** upper-middle; gamma marker; annotate “curvature not outcome-identified”.

## Required annotations

1. Header: `DEVELOPMENT_ONLY · NO_SINGLE_DOMINANT_MODEL`.
2. Current-model callout: `retained for research-question alignment + transparency + explicit missing-evidence semantics`.
3. Gated-rule callout: `strong abstention safety; current threshold has zero defined outputs on observed evidence`.
4. Additive/nonlinear callout: `useful behavioral contrasts; no predictive superiority claim`.
5. Footer: `Formal Human Gate, formal holdout fit, parameter stability, and outcome-based transfer remain pending.`

## Prohibited visual language

Do not use rank numbers, winner badges, “best model”, accuracy leaderboards, or a single composite score. Do not imply that point position is a formal empirical estimate; all positions are qualitative summaries of the frozen development comparison.
