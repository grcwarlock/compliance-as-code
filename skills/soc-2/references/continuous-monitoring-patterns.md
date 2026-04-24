# Continuous Monitoring Patterns

Most controls described in SOC 2 can be implemented two ways: as a periodic manual review (quarterly user access review, annual restore test) or as a continuous check (real-time drift detection, automated weekly restores with verification).

Continuous versions are strictly better for audit assurance — they reduce the observation window for failure from months to minutes — and strictly better for operations because they catch problems before an auditor does.

Below are common manual → continuous pairings.

## Access management

| Manual | Continuous |
|---|---|
| Quarterly User Access Review with CSV exports | Daily diff job: IdP group membership vs HRIS active employees. Any row in "IdP but not HRIS" or "wrong role for department" opens a ticket automatically. |
| Annual privileged-user review | Real-time alert when a user is added to a privileged group. Weekly reconciliation against an approved list stored as code. |
| Termination ticket with SLA | HRIS webhook → IdP deprovisioning workflow → per-app revocation jobs. Metric: time from termination event to last access revocation. |
| Password policy attestation | IdP config read by a nightly job, diffed against an expected policy stored in git. |

## Change management

| Manual | Continuous |
|---|---|
| Sampled review of production changes | Every merge produces a structured approval receipt (see evidence-as-code-patterns.md). Reviews become queries over the receipts table. |
| Emergency change process with retrospective approval | Emergency changes tagged in CI with an "emergency=true" label. Nightly report of all emergency changes in the period requires reviewer signoff within 5 business days; un-signed items escalate. |
| Quarterly environment drift walkthrough | IaC drift detector runs on every production config change. Non-zero drift opens a P2 ticket. Monthly drift report for the audit narrative. |

## System operations

| Manual | Continuous |
|---|---|
| Annual restore test | Automated weekly restore from a recent backup to a staging environment, with integrity checks. Failure opens a P1. |
| Quarterly vulnerability scan review | Every scan result landed in a ticketing system with SLA by severity. Evidence is the ticket history, not the scan PDF. |
| Annual incident-response tabletop | Game-day exercises with recorded runbook execution and lessons-learned tickets. One per quarter, rotating scenarios. |

## Monitoring (CC7)

| Manual | Continuous |
|---|---|
| Monthly review of SIEM alerts | Every high-severity alert is a page with a ticket. The ticket captures triage, action, and root cause. Monthly reports are queries, not re-reviews. |
| Annual "our logs are flowing" attestation | Synthetic log generator in every environment; alert if synthetic events do not appear in the SIEM within the configured latency budget. |
| Quarterly configuration audit | Tag-based asset inventory; continuous policy check ("every prod RDS instance has encryption enabled") with alerts on violation. |

## Risk management (CC3)

| Manual | Continuous |
|---|---|
| Annual risk assessment workshop | Risk register as a typed data store; new risks opened from threat model output, pentest findings, incidents. Quarterly review is a query on risks aged > 90 days with status `open`. |
| Vendor risk review spreadsheet | Vendor onboarding workflow produces structured assessment records. Re-review triggered by contract renewal, score drop, or incident involvement. |

## When manual is still the right answer

Continuous is not universally better. Manual is appropriate when:

- The control requires human judgment (board oversight of the security program, hiring decisions, vendor risk acceptance).
- The frequency is already low enough that automation cost exceeds the value (annual policy ratification).
- The evidence is a signed statement from a human (risk acceptance, CISO sign-off). Automation cannot forge accountability.

For these controls, the continuous improvement is to make the inputs to the human decision queryable — not to eliminate the human.

## How auditors react to continuous controls

Favorably, when:

- The detector, alert, and remediation evidence are all available for the period.
- Exception handling is documented (what happens when the detector itself fails).
- The continuous control is old enough to have a track record (multiple remediated exceptions, not just clean runs).

Skeptically, when:

- The continuous control was stood up shortly before the audit.
- There are no exceptions on record — either the detector is not running, or the threshold is too loose.

The easiest way to satisfy an auditor reviewing a continuous control is to show them a real incident the control caught, with the ticket trail and remediation evidence. Silence is not evidence of operation.
