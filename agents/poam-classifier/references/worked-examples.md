# Worked Examples

Reference classifications for calibrating the agent. These examples should be classified consistently; they are also useful as human training for reviewers comparing the agent's output against expected outcomes.

## Example 1 — single missed termination, no production access

**Description:** A terminated employee was not deprovisioned from the IdP within SLA. The user had no access to financial systems in their role. Deprovisioning completed seven days late, after the monthly HRIS-IdP reconciliation caught the gap.

**Signals:** magnitude=low, likelihood=remote, compensating=effective (monthly reconciliation caught it), period=one event, pervasiveness=isolated.

**Classification:** `deficiency`

**Reasoning:** Low magnitude because the user lacked financial-system access. The compensating control (monthly reconciliation) operated as designed and closed the gap. No pattern evident.

## Example 2 — quarterly UAR missed for general ledger

**Description:** Quarterly User Access Review for the GL service in Q3 was not performed. Reviewer declined calendar invite; no backup was assigned. Q4 and subsequent reviews performed on time.

**Signals:** magnitude=medium, likelihood=reasonably_possible, compensating=partial (inline SoD remained enforced; provisioning still required approval), period=one quarter, pervasiveness=isolated.

**Classification:** `significant_deficiency`

**Reasoning:** UAR is the primary detective control for inappropriate GL access. Without it, drift over the quarter is not caught. Inline SoD and provisioning approvals are partial compensation but do not detect role-accumulation over time. One missed quarter is isolated, not systemic.

## Example 3 — developer with production deploy access to ERP deployed own pricing-engine change

**Description:** A developer held production-deploy access to the ERP. The developer reviewed and deployed their own change to the pricing engine. Change affected revenue recognition for subscription products. No post-deploy reconciliation was performed.

**Signals:** magnitude=high, likelihood=reasonably_possible, compensating=none, period=single event but reflects a design gap, pervasiveness=affects revenue-relevant system.

**Classification:** `material_weakness` (candidate, subject to compensating-control review)

**Reasoning:** Self-review and self-deploy of a revenue-relevant change is a classic material-weakness pattern. Magnitude is high because pricing affects a material financial-statement line. No compensating control prevented or detected the unreviewed change. The design gap (developers holding prod-deploy) is the root cause and may apply to other changes in the period; aggregation must be considered.

**Required human judgment:** verify whether any post-deploy reconciliation or substantive analytical procedure detected the misstatement downstream; aggregation analysis across prior developer-deployed changes in the period.

## Example 4 — backup job monitored, restore never tested

**Description:** Production database backups ran successfully throughout the period according to job logs. No restore test was performed during the period. A restore test was overdue by 14 months.

**Signals:** magnitude=medium (disaster recovery, not daily reporting), likelihood=reasonably_possible (unknown if backups are actually restorable), compensating=none, period=full period, pervasiveness=affects DR posture.

**Classification:** `significant_deficiency`

**Reasoning:** Backups without tested restore are an unverified control. Financial-reporting impact depends on whether a disaster would affect current-period reporting; typically this is a significant deficiency absent a material incident during the period. If a disaster occurred and backups failed to restore, the classification would escalate.

## Example 5 — SSO misconfiguration allowed bypass of MFA for one week

**Description:** An SSO configuration change removed MFA enforcement for a subset of admin users for seven days. Detected by a scheduled drift check; remediated the same day. No known unauthorised access during the window.

**Signals:** magnitude=medium-high (admin users, multiple financial systems downstream), likelihood=reasonably_possible (exposure existed even if not exploited), compensating=partial (IAM session logging still captured activity), period=7 days, pervasiveness=isolated.

**Classification:** `significant_deficiency`

**Reasoning:** The exposure window affected admin users across multiple systems. The compensating detective control (drift check) operated as designed and caught the misconfiguration. No evidence of exploitation, but the preventive control did not operate for the window. Rises to significant deficiency because admin access to financial systems was affected; does not rise to material weakness because the window was short, detection was effective, and no misstatement was identified.

## Example 6 — legacy system with weak authentication but no financial data

**Description:** A legacy internal tool stores operational metadata and lacks MFA. It is not connected to financial systems and does not process financial data.

**Signals:** magnitude=low, likelihood=remote (no ICFR relevance), compensating=not applicable, period=ongoing, pervasiveness=isolated.

**Classification:** `deficiency`

**Reasoning:** Not ICFR-relevant. Classified as a control deficiency for completeness, with `required_human_judgment` flagging that ICFR relevance should be confirmed by the SOX PMO before this is added to the POA&M.

## Calibration notes

- A single missed instance of a control is not automatically more than a deficiency. Compensating controls and magnitude carry weight.
- Multiple instances affecting the same risk area aggregate upward (per AS 2201 aggregation guidance) but aggregation is a human call.
- Magnitude cannot be quantified without a materiality threshold. The agent should flag this when magnitude is decisive.
- "Reasonably possible" is the PCAOB phrase for the middle likelihood tier. Do not substitute "plausible" or "likely" — match the framework vocabulary.
