# Model trade-offs and decision record

## Sample-in behavior

The 16 observable records have mean Raw Signal 3.5625 and common `R=0.375`. A therefore has mean 1.3359; B has 3.25 (λ=.5) or 2.9375 (λ=1); D has 2.1816 (γ=.5), 1.3359 (γ=1), or 0.5010 (γ=2). C abstains on all 16 records at τ=.5. These are descriptive transformations, not accuracy scores.

## Robustness and missing data

A and D are mathematically closed at both endpoints and strongly suppress high Raw values as R falls. B is numerically stable but does not make low support decisive: a Raw L6 remains 5.0–5.5 at R=0. C makes the uncertainty decision explicit, but its coverage depends sharply on the fixed threshold. All four preserve missing Evidence as `NO_EFFECTIVE_EVIDENCE`.

## Extreme scenarios and interpretability

A is simplest and has a direct support interpretation. B is easy to explain but its penalty has score-scale units and can be too weak for high Raw values. C has the clearest operational meaning for a teaching workflow because it separates `ACCEPT` from `ABSTAIN`; it pays for that clarity with reduced coverage. D offers controlled curvature, but γ adds a sensitivity choice without evidence in this slice.

## Complexity and external transfer

A has zero new parameters. B has two registered λ values; C one threshold; D three registered γ values. The external structural replay does not establish generalization. It shows only how each formula behaves when the signal scale and reliability range differ.

## Judgment

No model can be declared best by score because the current pilot has no independent target, no paired baseline, and only one common reliability pattern among readable records. For a robustness check, A remains the fixed control. C is the strongest candidate when the product requirement prioritizes explicit refusal under low support. B should not replace A because it preserves too much unsupported Raw signal at `R→0`. D is useful as a bounded stress test, especially γ=2, but not as a data-selected replacement. The multiplication structure remains defensible as the transparent reference; the experiment does not establish it as uniquely correct.

## Suitable paper use

The results can enter an **Alternative Model Specification / Robustness Check** section as a preregistered structural comparison, with `DEVELOPMENT_ONLY` and `AI_PROVISIONAL` labels. Report endpoint behavior, missing-evidence handling, coverage trade-off, and the absence of an independent accuracy target. Do not report a winning accuracy, formal AIV, causal effect, or generalization claim.
