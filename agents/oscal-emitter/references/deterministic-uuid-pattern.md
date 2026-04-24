# Deterministic UUIDs for OSCAL

OSCAL documents are regenerated frequently. If every regeneration produces new UUIDs, every diff is noise — reviewers see "everything changed" when nothing changed.

Use **UUID5** (name-based) with a fixed namespace.

## Namespace

Pick one UUID once; use it for all OSCAL emissions in the project. Pin it in a comment in the emitter.

```
00000000-0000-0000-0000-000000000000
```

The actual value does not matter as long as it is stable. Do not change it — changing the namespace invalidates every UUID emitted previously.

## Key construction

Build a stable, colon-separated string that uniquely describes what the UUID identifies.

| Entity | Key example |
|---|---|
| System | `system:my-saas` |
| Assessment results (per period) | `results:my-saas:2026-Q1` |
| Finding | `finding:my-saas:ac-2:uar-missed-q3-2025` |
| Observation | `observation:my-saas:ac-2:uar-missed-q3-2025` |
| Component | `component:okta-sso` |
| Control implementation | `control-impl:okta-sso:ac-2` |
| Party (person) | `party:<stable-id-of-person>` |
| POA&M item | `poam:my-saas:2026-Q1:ac-2:uar-missed` |

Rules for keys:

- Include entity kind as the first segment. Prevents collisions between different entity types sharing an identifier.
- Use stable identifiers, not display names. `ac-2` not `"Account Management"`.
- Normalise before hashing: trim whitespace, lowercase, replace spaces with hyphens.

## Pseudocode

```python
import uuid

OSCAL_NS = uuid.UUID("00000000-0000-0000-0000-000000000000")

def oscal_uuid(*parts: str) -> str:
    key = ":".join(p.strip().lower() for p in parts)
    return str(uuid.uuid5(OSCAL_NS, key))

# Examples
oscal_uuid("system", "my-saas")
# → 'b1b4...'
oscal_uuid("finding", "my-saas", "ac-2", "uar-missed-q3-2025")
# → '9e11...'
```

## Why this matters at scale

- **Stable diffs.** Regenerating SSP.json because one finding was updated produces a diff of one finding, not every UUID in the document.
- **Cross-artifact references.** A POA&M item references an observation by UUID. If the observation's UUID is stable, the POA&M does not need regeneration when the assessment is re-emitted.
- **Audit trail.** Assessors can cite a finding by UUID; the UUID still points to the same finding in next quarter's assessment results.

## What to avoid

- **uuid4 anywhere in OSCAL.** Random UUIDs produce noisy diffs and break cross-artifact references.
- **Using display titles in keys.** Titles change; UUIDs must not.
- **Changing the namespace mid-project.** If you must (e.g., shipping to a new org), regenerate everything at once and treat it as a migration.
- **Reusing keys across entity kinds.** `"my-saas:ac-2"` as both a finding key and an observation key will collide.
