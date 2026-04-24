---
name: oscal-emitter
description: Use when the user needs to turn prose assessment notes into a valid OSCAL JSON artifact (Assessment Results, Component Definition, or POA&M fragment). Input is markdown with control findings and observations; output is OSCAL JSON with deterministic UUIDs and normalized control IDs. Pure input → output, model-agnostic.
when_to_use: "Emitting OSCAL JSON from assessment notes, producing Assessment Results or Component Definitions, converting markdown control narratives to machine-readable OSCAL, deterministic UUID5 for stable diffs."
---

# OSCAL Emitter Agent

Pure input → output.

- **Input:** Markdown assessment notes — control IDs, findings, observations, status, evidence pointers.
- **Output:** A single OSCAL JSON document, valid against the OSCAL JSON Schema for the target model (default: Assessment Results).

## Supported OSCAL models

- Assessment Results (default) — `assessment-results`
- Component Definition — `component-definition`
- POA&M (Plan of Action and Milestones) — `plan-of-action-and-milestones`

Pass the target model via the prompt or the runner's `--model` flag (the runner defaults to `assessment-results`).

## Invocation

```bash
LLM_PROVIDER=openai LLM_MODEL=gpt-4o \
  python scripts/run-agent.py oscal-emitter \
    --input agents/oscal-emitter/examples/input-assessment-notes.md \
    --output assessment-results.json
```

## Behaviour

1. Reads assessment notes, normalises control IDs to OSCAL form (`ac-2`, `ac-2.3`, `cc6-1`).
2. Emits OSCAL JSON with the required metadata block (title, last-modified, version, oscal-version).
3. Uses UUID5 with a fixed namespace for every identifier — stable across regenerations, meaningful diffs.
4. Includes findings and observations with links back to the source notes where possible.
5. Validates the output shape against the OSCAL JSON Schema before emitting (runner-side check).

## References

- [OSCAL Assessment Results schema](references/oscal-assessment-results-schema.md)
- [Deterministic UUID pattern](references/deterministic-uuid-pattern.md)

## Verification

See `tests/cases.jsonl`. Each case validates the output JSON parses, contains the required OSCAL top-level key, and has the required metadata block. If the NIST OSCAL schema file is available locally, the runner can fully validate; the offline structural checks always run.
