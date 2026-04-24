# PCAOB AS 2201 Severity Framework

PCAOB Auditing Standard 2201 defines three severity tiers for internal control deficiencies over financial reporting (ICFR). Classification drives disclosure obligations and remediation urgency.

## The three tiers

### Control deficiency

A control is missing or operates such that the objective is not met.

- Magnitude could be small; may not meet materiality thresholds.
- No SOX disclosure required.
- Managed within normal control-improvement processes.

### Significant deficiency

A deficiency (or combination) that is *less severe* than a material weakness but important enough to merit attention by those responsible for oversight of financial reporting.

- Reported to the audit committee.
- Documented in the auditor's communication of internal control matters.
- Does not trigger public disclosure but is a meaningful governance event.

### Material weakness

A deficiency (or combination) such that there is a *reasonable possibility* that a *material* misstatement of the annual or interim financial statements will not be prevented or detected on a timely basis.

- Disclosed in 10-K and 10-Q ICFR reports.
- Triggers re-evaluation of management's ICFR conclusion.
- Auditor may issue adverse opinion on ICFR.
- Often material to share price; may trigger SEC scrutiny.

## Classification signals

The agent evaluates five primary signals:

| Signal | Question | Typical values |
|---|---|---|
| **Magnitude** | How large a misstatement could this deficiency allow? | `low` (below materiality by an order of magnitude), `medium` (could approach materiality), `high` (could exceed materiality) |
| **Likelihood** | How likely is the misstatement occurring or going undetected? | `remote` (theoretical), `reasonably_possible` (the PCAOB threshold word), `probable` |
| **Compensating controls** | Do other controls detect the misstatement before reporting? | `none`, `partial`, `effective` |
| **Period of exposure** | How long did the deficiency exist? | String: "full period", "one quarter", "two weeks", etc. |
| **Pervasiveness** | Is the deficiency isolated to one system/process or systemic? | `isolated`, `systemic` |

## Decision logic

The three-tier mapping is not a simple arithmetic formula, but the dominant drivers are:

- **Material weakness** requires both high magnitude *and* reasonably possible (or higher) likelihood *and* ineffective compensating controls. Pervasiveness escalates toward MW.
- **Significant deficiency** is the middle ground: magnitude and likelihood high enough to matter for oversight, but either compensated or contained enough that a material misstatement is not reasonably possible.
- **Control deficiency** is the default when magnitude is low, likelihood is remote, or compensating controls are effective.

When signals conflict or are missing, the agent chooses the higher tier and flags the missing inputs in `required_human_judgment`. Erring toward the higher tier is the PCAOB-aligned default.

## Aggregation

Multiple individually-classified deficiencies can aggregate into a higher-severity finding if they affect the same risk area, the same financial-statement assertion, or share a common root cause. Auditors evaluate aggregation explicitly. The agent does not aggregate across inputs; aggregation is a human judgment reserved for the SOX PMO and the auditor.

## Disclosure implications

| Tier | Disclosure |
|---|---|
| Control deficiency | Internal management report only. |
| Significant deficiency | Audit committee; written communication from auditor. |
| Material weakness | Disclosed in management's ICFR report (10-K/10-Q); auditor reports adverse opinion on ICFR; investor disclosure may be required. |

Remediation of a material weakness must be documented and re-tested before management can assert ICFR is effective in a subsequent period.
