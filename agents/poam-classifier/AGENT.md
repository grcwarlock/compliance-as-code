---
name: poam-classifier
description: Use when the user needs to classify an internal-control deficiency under the PCAOB AS 2201 severity framework (control deficiency, significant deficiency, material weakness). Input is a deficiency description plus context signals (magnitude, likelihood, compensating controls, period of exposure, pervasiveness); output is a structured classification with reasoning. Pure input → output, model-agnostic.
when_to_use: "Classifying internal control deficiencies under PCAOB AS 2201, distinguishing control deficiency vs significant deficiency vs material weakness, SOX ITGC severity assessment, POA&M severity tagging, disclosure-trigger analysis."
---

# POA&M Classifier Agent

Pure input → output.

- **Input:** Markdown description of a deficiency plus structured context signals (magnitude, likelihood, compensating controls in effect, period of exposure, pervasiveness).
- **Output:** JSON object with a severity classification and reasoning.

## Severity tiers (PCAOB AS 2201)

| Tier | Key | Implication |
|---|---|---|
| Control deficiency | `deficiency` | Internal management tracking only |
| Significant deficiency | `significant_deficiency` | Reportable to the audit committee |
| Material weakness | `material_weakness` | Disclosed in 10-K/10-Q ICFR; triggers re-evaluation |

## Invocation

```bash
LLM_PROVIDER=openai LLM_MODEL=gpt-4o \
  python scripts/run-agent.py poam-classifier \
    --input agents/poam-classifier/examples/input-deficiency.md \
    --output classification.json
```

## Behaviour

1. Reads the deficiency description and context signals.
2. Evaluates magnitude (potential financial-statement impact), likelihood (reasonably possible vs remote), compensating controls, period of exposure, and pervasiveness.
3. Emits a JSON object with the chosen tier, the signal values, and a reasoning paragraph that explains the call.
4. Flags dependency on missing inputs (e.g., materiality threshold, specific financial-system scope) rather than guessing.

## References

- [PCAOB AS 2201 severity framework](references/pcaob-as2201-severity.md)
- [Worked examples](references/worked-examples.md)

## Verification

See `tests/cases.jsonl`. Each case's output is validated offline for:

- Valid JSON.
- `severity` is one of `deficiency`, `significant_deficiency`, `material_weakness`.
- Required fields present (`severity`, `reasoning`, `signals`).
- `signals.magnitude`, `signals.likelihood` are within defined enums.

## Out of scope

- The agent is a drafting aid. Final severity classification for SOX ICFR disclosure is a judgment call reserved for the SOX PMO, Internal Audit, or external auditor. The agent's output is a recommendation with reasoning, not a signed assessment.
