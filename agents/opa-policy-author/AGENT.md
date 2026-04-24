---
name: opa-policy-author
description: Use when the user needs a Rego policy (for Open Policy Agent) that enforces a specific compliance control. Input is a control description and an evidence record shape; output is a valid Rego policy with explicit deny rules. Pure input → output, model-agnostic, runtime-agnostic.
when_to_use: "Writing Rego policies from control descriptions, translating compliance requirements into OPA deny rules, policy-as-code for SOC 2 / ISO 27001 / NIST 800-53 / ISO 42001 controls."
---

# OPA Policy Author Agent

Pure input → output.

- **Input:** Markdown describing a control (ID, framework, description, conditions that constitute compliance or violation) plus a JSON evidence record shape.
- **Output:** A single `.rego` file implementing `deny` rules for the control. Valid syntax, ready to run with `opa eval`.

## Invocation

Inside an agent runtime that loads agent skills: activate by prompt (e.g. "Write a Rego policy for CC6.1 given this evidence shape").

Outside a runtime, via the provider-neutral runner:

```bash
LLM_PROVIDER=openai LLM_MODEL=gpt-4o \
  python scripts/run-agent.py opa-policy-author \
    --input agents/opa-policy-author/examples/input-control-cc6-1.md \
    --output policy.rego
```

## Behaviour

1. Reads the control description and identifies concrete conditions that imply non-compliance.
2. Maps each condition to a `deny` rule referencing the input evidence shape.
3. Emits a complete Rego package with imports, rules, and structured violation messages.
4. When the control requires information the evidence shape does not carry, emits a `# TODO` comment rather than inventing fields.

## References

- [Rego patterns for compliance](references/rego-patterns.md)
- [Evidence shape contract](references/evidence-shape-contract.md)

## Verification

See `tests/cases.jsonl`. Each case's output is validated offline (no LLM call) by structural checks: the file has a `package` declaration, at least one `deny` rule, and parses via `opa check` if the OPA binary is available.
