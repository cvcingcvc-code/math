# Defense Q&A: Model Selection

1. **Why choose this model?**  No universal winner is claimed. The current model is retained for development diagnostics because it makes reliability attenuation and `NO_EFFECTIVE_EVIDENCE` explicit. The gated rule is safer when abstention is the priority.
2. **Why not a simpler model?**  Raw-only is included as the reference. It is simpler, but it cannot represent evidence reliability. Whether that added structure is worth it remains conditional on formal labels and outcomes.
3. **Why not machine learning?**  No ML challenger has supplied a common split, tuning log, leakage audit, or reproducible result. It cannot be preferred without those artifacts.
4. **Is the model overfit?**  Formal overfit assessment is pending. The development runner declares fixed grids and no data-driven tuning, but the provisional slice is small and structurally homogeneous.
5. **Were parameters hand-tuned?**  The received formulation runner declares fixed parameter grids and `tuning: none`. Preferred parameters are not selected from a formal outcome holdout because that holdout does not exist.
6. **Will it work on new data?**  Outcome-based transfer is pending. Existing external material is synthetic/controlled structural transfer only.
7. **What if reliability is wrong?**  Sensitivity and alternative formulations show output changes as reliability changes; the model must expose uncertainty or abstain when support is insufficient. The gated formulation demonstrates the safety option.
8. **Why multiplication rather than addition?**  Multiplication preserves the interpretation that unsupported evidence attenuates the observed signal proportionally. Addition is retained as a challenger; its lambda=0.5 version is closer to raw scores in development, so multiplication is not declared universally superior.
9. **Were there failed experiments?**  Yes. The gated rule abstains on all 16 observed evidence records at threshold 0.5, and external Gate 3 (low reliability predicting higher future error) is unsupported in the existing transfer artifact.
10. **Does another model win on some metrics?**  Yes. Additive lambda=0.5 has lower development RMSE versus raw; the gated rule has safer counterexample abstention; raw-only has lowest complexity. These trade-offs are why the conclusion is `NO_SINGLE_DOMINANT_MODEL`.
