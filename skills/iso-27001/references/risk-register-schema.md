# Risk Register Schema

A risk register that lives in a spreadsheet is a risk register that will not survive Stage 2. This document specifies a typed, queryable schema that holds up to certification audit scrutiny and actually informs engineering decisions.

## Core schema

```yaml
- id: RISK-2026-0014                    # stable, non-reusable
  title: "Unmonitored admin access to GL database"
  description: >
    Privileged access to the production ledger database is granted via an
    IAM role assumed by on-call engineers. Role assumptions are logged but
    no alerting exists for unusual use patterns.
  status: open                           # open | mitigated | accepted | transferred | retired
  created_at: 2026-02-14
  last_reviewed: 2026-04-01
  next_review_due: 2026-07-01
  owner: alice@corp.example              # named individual, not a team
  stakeholder_roles:
    - security-lead
    - gl-service-owner

  asset:
    id: gl-primary-rds
    type: database
    classification: confidential
    data_categories: [financial_record, customer_pii]

  threat:
    source: insider_malicious
    scenario: >
      A privileged engineer exfiltrates ledger data or modifies records.

  vulnerability:
    description: >
      No real-time alerting on unusual role-assumption patterns; no DLP on
      query result volumes.
    existing_controls:
      - A.8.2: privileged access governed by PAM workflow
      - A.8.15: role-assumption events logged

  inherent:
    likelihood: 3                        # 1-5 integer scale, defined in risk-methodology.md
    impact: 5
    score: 15

  treatment:
    decision: mitigate                   # mitigate | accept | transfer | retire
    decision_rationale: >
      Material financial impact; mitigation cost is bounded and within
      product roadmap.
    plan:
      - action: "Deploy anomaly detection on role-assumption events"
        owner: security-team
        due: 2026-06-30
        ticket: SEC-2240
      - action: "Add query-volume threshold alerts on gl-primary-rds"
        owner: data-platform
        due: 2026-07-15
        ticket: DATA-8811

  residual:
    likelihood: 1
    impact: 5
    score: 5
    assumptions: >
      Anomaly detection fires within 5 minutes; on-call responds within SLA.

  annex_a_controls:
    - A.8.2
    - A.8.15
    - A.8.16

  evidence_pointers:
    - "event_store://source=aws-cloudtrail&event_type=role_assume&resource=role/gl-admin"
    - "ticket_store://SEC-2240"
    - "ticket_store://DATA-8811"
    - "dashboard://grafana/gl-admin-activity"

  linked_risks: []
  source: "Threat model: gl-service 2026-02"
```

## Why each field matters at audit

| Field | Why it matters |
|---|---|
| `id`, `status`, timestamps | Audit trail. Every risk that existed during the period must be visible with its state over time. |
| `owner` | Individuals are auditable; teams are not. A risk with only a team as owner is a risk without accountability. |
| `asset` | Risk is only meaningful relative to an asset. Auditors will ask "which system does this risk apply to" — answer with a link, not a guess. |
| `inherent` / `residual` | Stage 2 audit verifies you followed your own methodology. Both values must be present and consistent with the methodology definition. |
| `treatment.decision` + `decision_rationale` | Risk acceptance without rationale is a finding. The rationale must be defensible and signed off by the right role. |
| `annex_a_controls` | Joins the risk to the Statement of Applicability. The SoA then pulls in evidence pointers from the risk. |
| `evidence_pointers` | The audit's shortest path: risk → control → evidence. Without these, the auditor asks 10 follow-up questions and finds gaps. |
| `next_review_due` | Overdue reviews are an audit finding. A CI job that fails on overdue reviews prevents them silently. |

## Generating the risk register

Risks should be born from structured inputs:

1. **Threat modeling outputs** (per-service) produce candidate risks. The threat model's output format should be compatible with the register schema so import is mechanical, not manual.
2. **Pen test reports** produce risks for every finding not remediated immediately.
3. **Vulnerability scans** produce risks for unpatched CVEs above severity threshold that cannot be patched within SLA.
4. **Incident retrospectives** produce risks for the root cause if it is not fully mitigated.
5. **External events** (vendor incidents, new regulatory asks, new threat intelligence) produce manually-opened risks.

Risks should not be invented in a workshop once a year. A workshop is a review mechanism, not a discovery mechanism.

## Risk methodology document

The schema above depends on a `risk-methodology.md` that defines:

- The likelihood and impact scales (what does "likelihood 3" mean concretely)
- The scoring function (multiplication, addition, custom matrix)
- The threshold for mitigation vs acceptance
- The delegation rules (who can accept a residual risk at each score level)

Stage 2 auditors will read the methodology and test that the register is consistent with it. Inconsistent application of the methodology is one of the most common non-conformities.

## Review cadence

- Per-risk review cadence depends on residual score. A common pattern: score ≥ 15 reviewed monthly, 10–14 quarterly, ≤ 9 semi-annually.
- Register-level review as part of management review (Clause 9.3).
- Register re-baseline annually or after major organisational change (new product line, acquisition, significant re-architecture).

## Queryability

Because the register is structured, you can answer typical Stage 2 questions as queries:

- "Show me all risks accepted in the period and their sign-off." — `SELECT * FROM risks WHERE status='accepted' AND decision_date IN period`
- "Show me all risks linked to A.8.2 and their current status." — filter by `annex_a_controls` contains `A.8.2`.
- "Show me all overdue reviews." — `WHERE next_review_due < today AND status='open'`.

A register in a spreadsheet cannot answer these questions reliably. A register as data can.
