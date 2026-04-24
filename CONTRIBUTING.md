# Contributing

Thanks for considering a contribution. The value of this repo comes from quality, not volume — a well-written reference doc beats five rushed ones.

## Authoring style

Engineer-voice, not auditor-voice.

| Don't | Do |
|---|---|
| "The auditor will sample 25 user provisioning events." | "If you instrument provisioning as a webhook plus a tagged audit event, you can produce the full population on demand." |
| "Implement access controls per CC6.1." | "CC6.1 requires logical access restriction. The continuous version: deny-by-default IAM, drift detector, alert on privilege escalation." |
| "Document a risk assessment process." | "A risk register is a typed list. Schema in `references/risk-register-schema.md`. Source it from threat-model output and IaC drift." |

Other rules:

- **Cite control IDs precisely.** `CC6.1`, `A.5.15`, `AC-2(3)`. Generic advice is not useful.
- **Show the system shape.** Event types, resource types, schemas, code snippets when relevant.
- **Default to continuous controls.** Quarterly screenshots are a fallback, not a target. If a control can be replaced with a real-time check + alert + remediation, propose that.
- **Flag everything that requires a licensed auditor or lawyer.** Don't pretend the skill can opine on a SOC 2 report.

## Skill structure

```
skills/<framework>/
  SKILL.md                  # frontmatter + short body, links to references
  examples/example.md       # one walkthrough end-to-end
  references/
    <topic>.md              # one topic per file, ~3-5 KB each, load-on-demand
```

Required frontmatter fields: `name`, `description`, `when_to_use`. The `name` must match the directory.

## Agent structure

```
agents/<agent-name>/
  AGENT.md                  # frontmatter: name, description, when_to_use, tools (optional)
  prompt.md                 # the system prompt
  references/
    <topic>.md
  examples/
    input-<case>.md
    output-<case>.<ext>
  tests/cases.jsonl         # eval cases
```

Agents must be:

- **Pure input → output.** Take a defined input (markdown, JSON), produce a defined output (Rego, JSON, classification). No state, no infrastructure dependency, no cloud credentials at runtime.
- **Model-agnostic.** Plain instruction prompts. No vendor-specific tags or tool-use syntax.
- **Verifiable offline.** Each agent ships eval cases that validate output structure (JSON schema, `opa check`, enum match) without an LLM call.

## Connector structure

```
connectors/<source>/
  README.md                 # what it does, what it requires, scopes/IAM minimums
  connector.py              # standalone CLI, ~100-200 lines
  requirements.txt
  examples/output.json      # validated against connectors/schema/evidence.schema.json in CI
```

Hard rules for connectors:

1. **One file per connector.** Stdlib plus one SDK only.
2. **Output conforms to `connectors/schema/evidence.schema.json`.** Validated in CI.
3. **Read-only and least-privilege.** Document required scopes / IAM minimums in the connector README.
4. **Pure CLI.** Output to stdout or a file. No daemons, no scheduler, no persistent state.
5. **Skills and agents must work without any connector installed.** Connectors are optional convenience.

## Quality checks

Before opening a PR:

```bash
pip install -r requirements-dev.txt
python scripts/validate.py
```

CI runs the same validation plus markdownlint. All checks must pass.

## Out of scope

Things this repo will not accept:

- Connector frameworks, plugin systems, or shared connector base classes. Each connector is independent on purpose.
- Agents that need a database, persistent state, or live cloud credentials at runtime.
- Skills that promote a specific commercial product.
- Reference docs lifted from copyrighted material without permission. Cite the standard, write fresh prose.

## License

By contributing, you agree your contribution is licensed under MIT.
