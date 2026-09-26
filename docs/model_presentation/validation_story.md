# Validation story

## What was tested

The frozen chain is tested with small parameter changes, controlled evidence changes, controlled parameter variants, and a fixed external transfer artifact. Education records are AI provisional development data; no result below is a Human Gate result.

## Parameter changes

At λ_prompt=0.50, λ_context=0.50, and r_medium=0.75, changing each one by ±10% and ±20% produces no decision-state changes; formal student-level ranking is NOT_APPLICABLE in the 70-record slice. The 16 readable records remain LOW_SUPPORT and 54 records remain NO_EFFECTIVE_EVIDENCE. Support changes, while normalized ABL stays 3.5625. The result supports local structural stability and exposes the limit of this slice: context is not varied among readable records.

## Evidence changes

P108 keeps Raw Evidence L6 but its reliability rises from 0.375 to 0.750 when prompt risk is removed, changing LOW_SUPPORT to DEVELOPMENT_ONLY_STRUCTURAL_SUPPORT. This is the frozen formula's mechanical response to a hypothetical input-field change, not a real observation or causal prompt effect. P072 stays NO_EFFECTIVE_EVIDENCE when context is restored alone because its evidence label remains undetermined. The model therefore changes support when evidence quality changes and refuses to fill missing evidence with a score.

## External transfer

The fixed historical paper simulation runs the same Raw → Reliability → Adjusted → ACCEPT/ABSTAIN structure for momentum, RSI mean reversion, and MA20/50 trend. The first two show qualified reliability separation; the third is a failure boundary. Missing, delayed, conflicting, and low-trust conditions reduce coverage and increase abstention. This is limited development-only structural transfer evidence / operational feasibility, not proof of generalization or trading value.

## Judge-facing message

The model is not locked to one exact parameter point: nearby settings preserve the same decision structure, while support changes are visible. When the evidence itself is weakened, the reliability and decision change; when evidence disappears, the model abstains. The same logic can run on three different fixed signal types, with one strategy showing the expected limitation.
