# Evidence Pipeline Design

An evidence pipeline for ISO 27001 turns operational events into Annex A-tagged records that answer audit questions. This document describes the pipeline's shape, not any specific implementation — swap in your own event store, queue, or warehouse.

## Pipeline stages

```text
sources → normalizers → evidence store → control mappers → SoA view
                                       ↘ exception detectors → tickets
```

### 1. Sources

Every system that produces meaningful security events is a source. Typical inventory for a mid-sized engineering org:

| Source | Example events |
|---|---|
| Identity provider (Okta, Entra) | User lifecycle, MFA enrolment, group membership changes |
| Cloud provider (AWS, Azure, GCP) | IAM changes, config changes, resource lifecycle |
| Source control (GitHub, GitLab) | Repository access changes, branch-protection rules, merged PRs |
| CI/CD (GitHub Actions, GitLab CI) | Build provenance, artifact signatures, deployment approvals |
| SIEM / log platform | Security alerts, investigation outcomes |
| Ticketing (Jira, Linear, ServiceNow) | Change tickets, incident tickets, access requests |
| HRIS (Workday, BambooHR) | Employee lifecycle events |
| MDM (Jamf, Intune) | Endpoint posture, encryption state |
| Secrets manager | Secret rotation events |
| Vulnerability scanner | Findings and remediation tickets |

Sources should push or be polled on their native cadence. Real-time is ideal for lifecycle events; daily snapshots are fine for config state.

### 2. Normalizers

Every record arriving from a source is normalized to a common schema before it hits the evidence store. The common schema should be minimal but typed — see the evidence-record JSON Schema shipped with this repo.

Normalizer responsibilities:

- **PII scrubbing.** Personal data not required for audit purposes is removed or tokenized at the boundary. Evidence records are widely readable; raw source data may not be.
- **Schema coercion.** Different sources use different names for the same concept (`user`, `actor`, `principal`). Pick one at the normalizer layer.
- **Control hints.** Normalizer attaches best-guess `control_hints` for each record. Downstream mappers can override.
- **Idempotency key.** Records must carry a stable key so re-ingestion does not create duplicates. Usually `source:event_id`.

### 3. Evidence store

The store is where records live for the observation period + retention margin. Requirements:

- **Indexed on control_id.** You will be asked "show me all A.8.2 evidence from Q2" hundreds of times. This must be fast.
- **Immutable or hash-chained.** Once a record is in, it cannot be silently edited. If it must be amended, the amendment is a new record that points to the original.
- **Retention.** Covers the audit period + 6 months margin; longer for regulated data categories.
- **Access-controlled.** Evidence itself is sensitive; access is logged and reviewed.

In practice the store is often a warehouse table (BigQuery, Snowflake, Postgres) + an object-storage tier for raw payloads. Keep the warehouse schema stable; that is what dashboards and mappers depend on.

### 4. Control mappers

The mapper's job is to answer "for control X in period Y, what is the evidence?"

Simplest implementation: a rulebook in YAML that maps `(source, event_type)` tuples to Annex A controls, plus any additional filters.

```yaml
- control: A.8.2
  title: "Privileged access rights"
  rules:
    - source: aws-cloudtrail
      event_type: iam_role_assume
      filter: "role matches 'admin|root|privileged'"
    - source: okta
      event_type: group_membership_change
      filter: "group_name matches 'privileged_*'"
  population_query: "events in [period] matching rules"
  sample_strategy: "all; population is small"
```

Mappers produce:

- **Population queries** — the full set of events that count as evidence for the control in the period.
- **Sample packs** — when the population is large, pre-selected samples with rationale for the sample method.
- **Exception lists** — records flagged by the mapper as potentially out-of-policy.

### 5. Statement of Applicability view

The Statement of Applicability (SoA) is a join, not a document:

```text
annex_a_controls (93 rows)
  × applicability decisions (from risk register / scope)
  × evidence_pointers (from mapper output)
  → SoA view
```

Rendered on demand. Never maintained by hand.

### 6. Exception detectors

Running alongside the mappers are continuous detectors that raise tickets when evidence implies a control is not operating:

- A.8.2: alert when a user is added to a privileged group without a matching approval ticket.
- A.8.13: alert when a scheduled backup has not produced a record in the expected window.
- A.8.16: alert when a monitoring detector has not fired a synthetic event in the expected window ("watching the watcher").

Detectors produce tickets that become part of the exception population for the control. Handled well, they become the story you tell the auditor.

## Latency and retention

- **Ingestion latency:** minutes for lifecycle events, hours is acceptable for config snapshots.
- **Query latency:** sub-minute for population queries over a one-year period. Build indexes accordingly.
- **Retention:** 18 months for Type 2 overlap with SOC 2 + ISO cycles; longer for regulated data (GDPR, HIPAA each have their own retention rules).

## Privacy considerations

Evidence often contains identifiers. Key rules:

- Never include plain email addresses or full names in indexed fields unless necessary; use stable opaque IDs and resolve at display time.
- Access to evidence is itself an A.8.2 event (meta-audit).
- Data Subject Access Requests (GDPR Article 15) may reach the evidence store. Build the store with erasure / anonymization in mind from day one.

## Cost control

An unfiltered evidence pipeline eats storage. Controls:

- **Filter at the normalizer.** Not every cloud event is evidence; only the ones that map to a control or an assertion.
- **Tiered storage.** Recent events in hot storage; older in warm; archive after retention.
- **Derived tables.** Keep summary tables for common queries; re-derive from raw on demand for edge cases.

Well-run pipelines cost in low-thousands per month, not low-tens-of-thousands. If you are spending more, the filter is too loose.
