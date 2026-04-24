# Rego Patterns for Compliance

Patterns the agent uses when translating controls to Rego.

## Package naming

```text
package compliance.<framework>.<control_id_normalized>
```

Examples:

- `compliance.soc2.cc6_1`
- `compliance.iso27001.a_8_2`
- `compliance.nist80053.ac_2`
- `compliance.nist80053.ac_2_3` (enhancement)

Normalisation:

- Lowercase
- Dots → underscores
- Hyphens → underscores
- Parenthesised enhancements → leading underscore (`(3)` → `_3`)

## Default deny-by-default

```rego
package compliance.soc2.cc6_1

default allow := false

deny[msg] {
  # conditions that imply non-compliance
  msg := {
    "control_id": "cc6_1",
    "reason": "...",
    "resource": input.resource_id,
  }
}
```

No `deny` matches means compliant. Any match produces a violation message.

## Structured violation messages

Minimum fields: `control_id`, `reason`, `resource`. Add `severity` when implied by the control.

```rego
deny[msg] {
  not input.payload.mfa_enabled
  msg := {
    "control_id": "cc6_1",
    "reason": "MFA is not enabled",
    "resource": input.resource_id,
    "severity": "high",
  }
}
```

## Testing field presence

```rego
# fires if the field is absent or falsy
deny[msg] {
  not input.payload.owner
  msg := {"control_id": "...", "reason": "resource has no owner", "resource": input.resource_id}
}
```

## Composite conditions — prefer many small rules

Good:

```rego
deny[msg] {
  input.payload.privileged
  not input.payload.mfa_enabled
  msg := {...}
}

deny[msg] {
  input.payload.privileged
  not input.payload.approval_ticket
  msg := {...}
}
```

Avoid:

```rego
deny[msg] {
  input.payload.privileged
  not input.payload.mfa_enabled
  not input.payload.approval_ticket
  msg := {...}
}
```

Multiple rules produce one violation per independent failure, which is better diagnostics for the operator and better evidence for the auditor.

## Helper predicates

```rego
is_privileged_role(role) {
  role == "admin"
}

is_privileged_role(role) {
  role == "owner"
}

deny[msg] {
  is_privileged_role(input.payload.role)
  not input.payload.approved
  msg := {...}
}
```

Multiple rule bodies with the same head act as logical OR.

## What to avoid

- **Concrete identifier matching.** `input.payload.name == "bob@corp.example"` bakes test data into policy. Evaluate field values, not identities.
- **Provider-specific literals.** `input.source == "aws"` is fine only when the policy genuinely differs by source; otherwise accept any source.
- **Nested `not`.** Rego safety rules make double negation error-prone. Flip the condition.
- **Unit-tested string prefixes without anchors.** `startswith(input.role, "admin")` can match `admin` and `administrator`; use `==` when an exact match is intended.
