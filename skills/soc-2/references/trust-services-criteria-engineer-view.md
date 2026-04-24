# Trust Services Criteria — Engineer's View

SOC 2 is built on the AICPA Trust Services Criteria (TSC). Five categories:

| Category | Code | Required |
|---|---|---|
| Security (Common Criteria) | CC | Yes, always |
| Availability | A | Optional |
| Confidentiality | C | Optional |
| Processing Integrity | PI | Optional |
| Privacy | P | Optional |

If you only pick one, it is Security — mandatory and what buyers mean when they ask for "your SOC 2." Add Availability if you have an uptime SLA. Confidentiality if you store customer IP or secrets. Processing Integrity if you run money or workflows where correctness is the product. Privacy if you handle personal data as a primary function (separate from GDPR, which is a law, not a criterion).

## Common Criteria (CC) in engineer terms

| CC group | What it is really about | System shape that produces evidence |
|---|---|---|
| CC1 | Control environment, ethics, governance | HR system acknowledgements, code of conduct, ethics training records |
| CC2 | Communication of objectives and responsibilities | RACI matrices, runbooks, onboarding docs, incident comms records |
| CC3 | Risk identification and assessment | Risk register as data, threat model outputs, pentest scorecards |
| CC4 | Monitoring the internal control environment | Control self-assessments, exception dashboards, evidence pipelines |
| CC5 | Selecting, developing, deploying control activities | IaC patterns, change management records, SDLC gate evidence |
| CC6 | Logical and physical access | IdP + MFA + RBAC + data-center access, plus drift detection and UAR automation |
| CC7 | System operations and monitoring | SIEM/SRE alerting, incident response records, vuln management tickets |
| CC8 | Change management | Merge gates, deploy records, configuration drift reports |
| CC9 | Risk mitigation for business disruptions and vendors | BCP/DR test results, third-party risk reviews, contractual evidence |

CC6 and CC7 are where engineers spend most of their time. CC5 is the meta-control ("your change management must be a real thing, not a README"). The rest are process-heavy and benefit from being stored as structured data rather than Word documents.

## 2022 Points of Focus

The 2017 TSC was updated with the 2022 Points of Focus — non-mandatory guidance auditors use when assessing whether a criterion is met. Treat them as hints about what an auditor might reasonably ask for. They are not additional criteria.

## Picking a TSC scope

1. Start with Security alone for the first Type 2. Minimum viable and already a lot of work.
2. Add Availability in year two if you sell on uptime.
3. Add Confidentiality once you have DLP and encryption-at-rest claims you can prove with evidence.
4. Avoid Privacy unless you actually have a privacy program — it is far more than a checkbox.
5. Processing Integrity is rare in practice; do not pick it without a specific reason.

## Typical CC6 / CC7 sub-criteria and their engineer interpretation

| Sub-criterion | Engineer reading |
|---|---|
| CC6.1 Logical access restriction | Deny-by-default IAM, SSO with MFA, RBAC aligned to job function |
| CC6.2 Logical access provisioning | Provisioning workflow produces a typed event (user, role, approver, timestamp) |
| CC6.3 Logical access modification | Role changes flow through the same workflow; drift detector catches out-of-band changes |
| CC6.6 Transmission of sensitive data | TLS everywhere, inventory of endpoints, cipher-suite policy enforced in load balancers |
| CC6.7 Restriction of access to data at rest | Encryption at rest plus key-access policy plus audit of key use |
| CC6.8 Prevention of unauthorized software | Signed artifacts, deploy from CI only, admission controllers, no ad-hoc SSH to prod |
| CC7.1 Detection of configuration changes | IaC drift detector + alerting pipeline |
| CC7.2 Monitoring of system components | Tagged audit events from every control plane + centralized store + alert rules with owners |
| CC7.3 Evaluation of security events | Incident triage process with ticket trail, severity classification, post-incident review |
| CC7.4 Response to incidents | Runbooks linked to paging rules, exercise evidence from game days |
| CC7.5 Recovery from incidents | Tested restore procedures, documented RTO/RPO, evidence from DR tests |

## Cross-framework mapping (quick glance)

- CC6 ≈ ISO 27001 A.5.15–A.5.18, A.8.2–A.8.5 (access)
- CC7 ≈ ISO 27001 A.8.15, A.8.16 (logging, monitoring)
- CC8 ≈ ISO 27001 A.8.32 (change management)
- CC6 / CC7 / CC8 ≈ NIST 800-53 AC, AU, CM, SI families

Cross-walk once; maintain the pointer, not duplicate evidence.
