# System

my-saas (SaaS B2B product, FedRAMP Moderate baseline, AWS-hosted)

# Assessment context

- Assessor: internal audit team
- Period: 2026-01-01 through 2026-03-31
- Basis: continuous controls plus spot-check sampling
- OSCAL model: assessment-results

# Findings

## AC-2 — Account Management

**Status:** not-satisfied

**Observation:** Q3 2025 quarterly User Access Review (UAR) for the GL service was not performed. Root cause: calendar invite was declined by the primary reviewer and no backup fired. The Q4 2025 and Q1 2026 UARs were performed on time.

**Severity:** significant deficiency (candidate)

**Evidence reviewed:**

- UAR completion records in ticketing system (ticket query: `label:uar`)
- Reviewer calendar
- Backup reviewer assignment matrix

## AC-2.3 — Disable Inactive Accounts

**Status:** satisfied

**Observation:** Automated disable job ran on schedule for the entire period. Population: 1,412 active accounts at period start, 17 disabled for inactivity during period, 0 exceptions.

## AU-6(3) — Correlation of Audit Records

**Status:** satisfied

**Observation:** SIEM correlation rules active across 14 log sources throughout the period. Rule set reviewed quarterly. Population of correlation-triggered alerts: 2,431; all triaged within SLA.

# Observations

- The UAR failure in Q3 2025 was caught by internal continuous-control health check in December 2025 after the reviewer's calendar-decline pattern triggered an alert. Remediation ticket opened 2025-12-14, completed 2026-01-08 with backup reviewer logic deployed.
