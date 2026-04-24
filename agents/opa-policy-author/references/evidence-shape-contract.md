# Evidence Shape Contract

The agent expects each input evidence record to follow the shape defined in [`connectors/schema/evidence.schema.json`](../../../connectors/schema/evidence.schema.json).

## Envelope (required)

| Field | Rego access |
|---|---|
| `source` | `input.source` |
| `event_type` | `input.event_type` |
| `resource_type` | `input.resource_type` |
| `resource_id` | `input.resource_id` |
| `collected_at` | `input.collected_at` |
| `payload` | `input.payload.<field>` |

## Optional

- `control_hints` — array of `{framework, control_id}`. The policy does not usually need to read these; they are consumed by the mapping layer, not the policy.

## Payload is connector-specific

The `payload` field's shape varies per connector. The control description supplied to the agent includes the expected payload fields. The agent writes Rego that references those fields under `input.payload.<field>`.

## Missing fields

If the control requires a field the evidence shape does not carry:

1. The agent does **not** invent the field.
2. The agent emits a Rego comment: `# TODO: need <field_name> in payload`.
3. The corresponding `deny` rule is omitted until the evidence shape is extended.

This keeps the policy safe to deploy (it will not silently pass because of a missing field).

## Testing the policy

```bash
opa eval -d policy.rego -i sample_evidence.json "data.compliance.<framework>.<control>.deny"
```

Expected output when compliant: `"deny": []`.
When non-compliant: an array of violation messages.
