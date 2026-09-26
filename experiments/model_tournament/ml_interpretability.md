# ML challenger interpretability

Status: `DEVELOPMENT_ONLY`; coefficients and rules describe associations with the AI provisional target. They are not causal explanations.

## logistic_regression

```text
{
  "intercept": -1.1727743506142143,
  "top_positive_coefficients": [
    {
      "feature": "cat__length_stratum_medium_50_199",
      "coefficient": 0.9717987112411471
    },
    {
      "feature": "cat__path_case_scaffold_path",
      "coefficient": 0.7983125093924183
    },
    {
      "feature": "cat__length_stratum_long_>=200",
      "coefficient": 0.7227470735735549
    },
    {
      "feature": "cat__possible_bloom_surface_signal_candidate_low",
      "coefficient": 0.6542571792245149
    },
    {
      "feature": "num__speaker_confidence",
      "coefficient": 0.5882135114211091
    },
    {
      "feature": "cat__possible_bloom_surface_signal_no_surface_cue",
      "coefficient": 0.14123384072009265
    },
    {
      "feature": "cat__question_form_stratum_explicit_question_mark",
      "coefficient": 0.14115446571693988
    },
    {
      "feature": "num__text_length_chars",
      "coefficient": 0.09779436113347822
    },
    {
      "feature": "num__agent_confidence",
      "coefficient": 0.07744108296106084
    },
    {
      "feature": "cat__semester_2025秋",
      "coefficient": 0.06845666552719139
    }
  ],
  "top_negative_coefficients": [
    {
      "feature": "num__context_truncated",
      "coefficient": -2.3245423924801996
    },
    {
      "feature": "cat__length_stratum_short_<50",
      "coefficient": -1.695021354737766
    },
    {
      "feature": "cat__path_case_reverse_path",
      "coefficient": -0.7976591760439607
    },
    {
      "feature": "cat__possible_bloom_surface_signal_mixed_surface_cues",
      "coefficient": -0.3193767033590985
    },
    {
      "feature": "cat__possible_bloom_surface_signal_candidate_mid",
      "coefficient": -0.28999780405863934
    },
    {
      "feature": "cat__possible_bloom_surface_signal_candidate_high",
      "coefficient": -0.18659208244993264
    },
    {
      "feature": "cat__question_form_stratum_request_or_question_form",
      "coefficient": -0.10290961446299159
    },
    {
      "feature": "cat__semester_2026春",
      "coefficient": -0.06893223545025404
    },
    {
      "feature": "cat__question_form_stratum_statement_or_other",
      "coefficient": -0.03872042117701161
    },
    {
      "feature": "cat__path_case_other_or_unknown",
      "coefficient": -0.0011289032715196125
    }
  ]
}
```
## shallow_decision_tree

```text
|--- num__text_length_chars <= -0.509
|   |--- class: 0
|--- num__text_length_chars >  -0.509
|   |--- num__context_truncated <= 0.204
|   |   |--- class: 1
|   |--- num__context_truncated >  0.204
|   |   |--- class: 0

```
## random_forest

```text
{
  "feature_importance": [
    {
      "feature": "num__text_length_chars",
      "importance": 0.30716905508021164
    },
    {
      "feature": "num__context_truncated",
      "importance": 0.28380567936560464
    },
    {
      "feature": "cat__length_stratum_short_<50",
      "importance": 0.10411847821183534
    },
    {
      "feature": "cat__length_stratum_long_>=200",
      "importance": 0.05648774179127771
    },
    {
      "feature": "cat__path_case_reverse_path",
      "importance": 0.04151799058877771
    },
    {
      "feature": "cat__length_stratum_medium_50_199",
      "importance": 0.03728918621111356
    },
    {
      "feature": "cat__path_case_scaffold_path",
      "importance": 0.02735057455200542
    },
    {
      "feature": "cat__possible_bloom_surface_signal_no_surface_cue",
      "importance": 0.025473374271253537
    },
    {
      "feature": "cat__question_form_stratum_statement_or_other",
      "importance": 0.023575337222644842
    },
    {
      "feature": "cat__path_case_other_or_unknown",
      "importance": 0.01686303620660372
    },
    {
      "feature": "cat__possible_bloom_surface_signal_candidate_low",
      "importance": 0.016420760753445108
    },
    {
      "feature": "num__agent_confidence",
      "importance": 0.016134727859954987
    },
    {
      "feature": "cat__semester_2025秋",
      "importance": 0.012742566498813914
    },
    {
      "feature": "cat__semester_2026春",
      "importance": 0.009381767712540635
    },
    {
      "feature": "cat__possible_bloom_surface_signal_candidate_high",
      "importance": 0.009251546154074692
    }
  ],
  "interpretation_note": "Associational importance only; not causal."
}
```