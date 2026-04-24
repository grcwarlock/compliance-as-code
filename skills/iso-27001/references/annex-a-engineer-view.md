# Annex A (2022) — Engineer's View

ISO/IEC 27001:2022 Annex A has **93 controls** grouped into **4 themes**. The 2022 revision consolidated 114 controls from the 2013 edition into 93, introduced 11 new controls, and restructured the grouping entirely. If your reference material still talks about A.5–A.18 sections, it is out of date.

## The four themes

| Theme | Range | Count | What it covers |
|---|---|---|---|
| A.5 Organisational | A.5.1–A.5.37 | 37 | Policies, roles, supplier management, incident management, business continuity |
| A.6 People | A.6.1–A.6.8 | 8 | Screening, employment terms, awareness, remote working, disciplinary |
| A.7 Physical | A.7.1–A.7.14 | 14 | Physical security perimeters, equipment, clear desk, cabling |
| A.8 Technological | A.8.1–A.8.34 | 34 | The controls engineers actually build |

A.8 is where you will spend most implementation time. A.5 has the risk management and policy scaffolding. A.6 and A.7 matter but are largely HR and facilities problems.

## A.8 Technological controls (the engineering set)

| Control | Name | What it really is in a system |
|---|---|---|
| A.8.1 | User endpoint devices | MDM enrollment, encryption, posture checks at login |
| A.8.2 | Privileged access rights | Break-glass accounts, PAM workflow, alerting on privileged group changes |
| A.8.3 | Information access restriction | RBAC/ABAC policy, deny-by-default IAM |
| A.8.4 | Access to source code | Repo permissions, branch protection, code owners |
| A.8.5 | Secure authentication | SSO + MFA everywhere; no local accounts for humans |
| A.8.6 | Capacity management | Autoscaling + capacity alerts + post-incident capacity tickets |
| A.8.7 | Protection against malware | Endpoint agent + admission control for container images |
| A.8.8 | Management of technical vulnerabilities | Scanner → ticket system with SLA by severity; patch orchestration |
| A.8.9 | Configuration management | IaC as the source of truth + drift detection |
| A.8.10 | Information deletion | Data retention policy enforced at the storage layer (TTLs, lifecycle rules) |
| A.8.11 | Data masking | Production data does not leave production; masking in non-prod data pipelines |
| A.8.12 | Data leakage prevention | Egress controls, secret scanning in repos, DLP on email/endpoints |
| A.8.13 | Information backup | Backups + tested restores (see A.8.14) |
| A.8.14 | Redundancy | HA design, multi-AZ/region posture, DR runbooks |
| A.8.15 | Logging | Centralised log store with retention; logs are immutable (or hash-chained) |
| A.8.16 | Monitoring activities | Alerting pipeline with owners, runbooks, and after-action records |
| A.8.17 | Clock synchronisation | NTP/PTP across fleet; alert on clock skew > threshold |
| A.8.18 | Use of privileged utility programs | Admission control; no ad-hoc SSH into prod without audit trail |
| A.8.19 | Installation of software on systems | Signed artifacts; deployment only via CI |
| A.8.20 | Networks security | Segmentation + default-deny between zones |
| A.8.21 | Security of network services | Service-to-service auth (mTLS, SPIFFE), TLS everywhere |
| A.8.22 | Segregation of networks | VPC/subnet design; no flat networks |
| A.8.23 | Web filtering | Egress proxy / DNS policy for endpoints |
| A.8.24 | Use of cryptography | Crypto policy; KMS-based key management with rotation |
| A.8.25 | Secure development lifecycle | SDLC with security gates (code review, SAST, deps, IaC scan) |
| A.8.26 | Application security requirements | Security requirements captured in stories; threat model per service |
| A.8.27 | Secure system architecture and engineering principles | Architecture reviews with security sign-off |
| A.8.28 | Secure coding | Coding standards, linters, security-focused code review |
| A.8.29 | Security testing in development and acceptance | SAST + DAST + dependency scan + pen test cycle |
| A.8.30 | Outsourced development | Supplier security requirements in contracts; evidence review |
| A.8.31 | Separation of development, test, and production | Separate accounts/projects; no shared credentials |
| A.8.32 | Change management | The change management process that your SOC 2 CC8 already requires |
| A.8.33 | Test information | Mask or synthesize test data; no prod data in dev |
| A.8.34 | Protection of information systems during audit testing | Controls on auditor access during testing (read-only, scoped) |

## New in 2022 (added, not merged)

- A.5.7 Threat intelligence
- A.5.23 Information security for use of cloud services
- A.5.30 ICT readiness for business continuity
- A.7.4 Physical security monitoring
- A.8.9 Configuration management
- A.8.10 Information deletion
- A.8.11 Data masking
- A.8.12 Data leakage prevention
- A.8.16 Monitoring activities
- A.8.23 Web filtering
- A.8.28 Secure coding

If you are transitioning from the 2013 standard, these 11 are the gap list.

## Engineer's filter: the 20 controls you will touch weekly

If you had to pick a subset that represents most of the real engineering work, it is roughly:

A.5.7, A.5.23, A.5.30, A.6.3 (awareness), A.8.2, A.8.3, A.8.5, A.8.8, A.8.9, A.8.12, A.8.15, A.8.16, A.8.20, A.8.22, A.8.24, A.8.25, A.8.28, A.8.29, A.8.31, A.8.32.

If these 20 are instrumented with continuous evidence, the remaining 73 are mostly policy + ownership records and can be maintained at a lower frequency.

## Mapping to SOC 2 CC

The overlap is real. Rough equivalence:

- A.5.15 + A.8.2 + A.8.3 + A.8.5 ≈ CC6.1 through CC6.3
- A.8.15 + A.8.16 ≈ CC7.1 + CC7.2
- A.8.32 ≈ CC8.1
- A.5.24 through A.5.29 (incident management) ≈ CC7.3 through CC7.5

If you already have SOC 2 Type 2 evidence, ~70% of Annex A technological and organisational evidence is reusable. Cross-walk once; do not duplicate the pipeline.
