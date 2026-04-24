# Evidence-as-Code Patterns

The thesis: evidence should be a side effect of normal operation, not a task scheduled before an audit.

If an engineer has to remember to collect evidence, the evidence is already unreliable. If the system emits it automatically as part of doing the thing, the evidence is as good as the thing itself.

## Anti-patterns

| Anti-pattern | Why it is brittle |
|---|---|
| Screenshots of dashboards saved to a shared drive | Not timestamped, not attributed, not re-producible. One missing screenshot = one missing control period. |
| Excel sheet of "controls we ran this quarter" | Human memory. Selection bias. No referential integrity to the actual events. |
| "Ask the team" email before the audit | Evidence that exists only in human memory is evidence the auditor will sample and find gaps in. |
| Ad-hoc SQL queries against production to "prove" a control | Unscoped, unreviewed, often privileged access. Becomes its own control failure. |

## Patterns that work

### Tagged audit events

Every control plane emits an event when a meaningful action happens (user provisioned, policy changed, secret rotated). The event carries:

```json
{
  "actor": "user:jane@corp.example",
  "action": "iam.user.create",
  "resource": "user/new-joiner-42",
  "reason": "ticket:HR-1234",
  "timestamp": "2026-04-17T14:02:11Z",
  "source": "okta",
  "control_hints": [{"framework": "soc-2", "control_id": "CC6.2"}]
}
```

The `reason` field is the control. If an action cannot cite a ticket or an approval, that is a finding, not a missing field.

### IaC drift detection as evidence

Controls that claim "production is configured according to policy" are verifiable by comparing the live state to the IaC source of truth. A nightly drift job that records the diff and alerts on non-zero rows is stronger evidence than any quarterly review.

### Policy-as-code

Rego policies gate admission. The engine logs every allow and deny. An auditor looking for "unauthorized software cannot be deployed" reads the logs, not the narrative.

### Approval receipts

Change management controls need evidence of approvals. Receipt structure:

```json
{
  "change_id": "deploy-2026-04-17-abc123",
  "approvers": ["bob@corp.example", "alice@corp.example"],
  "ticket": "PROD-9912",
  "merge_commit": "9a3f...",
  "ci_run": "https://ci.example.com/run/441122",
  "policy_checks": ["terraform-lint", "cost-guardrail", "opa-admission"],
  "deployed_at": "2026-04-17T16:05:00Z"
}
```

Each field corresponds to an auditor question. The receipt answers all of them in one record.

## A minimum evidence record schema

See [`../../../connectors/schema/evidence.schema.json`](../../../connectors/schema/evidence.schema.json) for the full shape shipped in this repo. Fields every record needs:

- **source** — which system produced it (stable string)
- **event_type** — logical category, agents and policies key on this
- **resource_type** and **resource_id** — what the event is about
- **collected_at** — RFC 3339 timestamp of collection (not the event itself)
- **control_hints** — optional framework + control ID pairs
- **payload** — connector-specific structured data, no PII

The schema forbids additional top-level properties on purpose. Connectors that want to add fields either extend the schema via a PR or put them inside `payload`.

## Tying records to controls

Two acceptable approaches:

1. **Hint at the source** — connector populates `control_hints` with its best guess. Downstream mapper can override.
2. **Map after the fact** — connector ignores controls entirely and emits shape-only events. A mapper reads a rulebook ("every iam.user.create under SOC 2 maps to CC6.2") and tags records centrally.

Pick one. Mixing leads to disagreements about what the record is for.

## Retention

SOC 2 Type 2 typically covers a 6- to 12-month observation window. Evidence must be retrievable for the full window. In practice: store raw events for ≥18 months, index them, and keep a derived "control period snapshot" table that summarizes populations for sampling.

Evidence outside the period is not disqualifying but auditors prefer population-based testing when the population is available. If your event store has gaps, expect sample-size escalation or exceptions.
