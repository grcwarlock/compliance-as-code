# Example: Designing a continuous CC6.1 control

**User prompt:** "How would I instrument CC6.1 (logical access) so the evidence emits itself? We run on AWS with Okta for SSO."

## Expected working style

The skill should:

1. Ground the answer in CC6.1's actual requirement (restriction of logical access consistent with the entity's security criteria).
2. Translate that into a system design: event sources, assertion, remediation path.
3. Name the evidence the auditor will want, and describe it as a queryable record — not a screenshot.
4. Flag any part that still requires human judgment.

## Example response shape

> CC6.1 requires that logical access to information and system resources is restricted to authorized users. In your stack, that has three instrumentation points: identity, authorization, and drift.
>
> **Identity (source of truth for who):** Okta is the IdP. Evidence is the Okta admin API audit log — every user create, group change, and factor enrollment is a structured event. Ingest these into your event store with `source: okta`, `event_type: iam_user_event`, `resource_type: iam_user`. Tag each record with `control_hints: [{framework: soc-2, control_id: CC6.1}]`.
>
> **Authorization (who has access to what):** AWS IAM, mediated through SSO roles + group assignment. Evidence is a daily snapshot of the IAM state (IAM users, attached policies, role-assume permissions). Store the snapshot as one evidence record per principal per day. The continuous control is a drift job: expected role membership lives in Terraform; actual membership comes from the snapshot; any delta opens a ticket.
>
> **Drift and human override:** the exception population for CC6.1 is the drift tickets themselves. An auditor will ask for the full population of CC6.1 exceptions in the period and evidence that each was investigated and closed (or accepted as a documented exception). Make sure closed tickets carry a resolution comment, not just a status change.
>
> **What still needs a human:** role design — deciding which Okta group gets which AWS role — is a judgment call that should go through change management (CC8). The continuous control above only enforces the design; it does not create the design.
>
> **Minimum viable evidence for CC6.1 Type 2:**
>
> - Okta audit log, retained for the period (population).
> - Daily IAM snapshots, retained for the period (observation of configuration).
> - Drift tickets with resolution evidence (exception population).
> - Terraform repository with the role → group mapping as the declared expectation.

## What a bad response looks like

- "Implement least-privilege access." (no system shape, no evidence)
- "Run a quarterly access review." (the skill should default to continuous; quarterly is a fallback)
- "The auditor will sample 25 users and ask for their provisioning tickets." (auditor-voice, not engineer-voice)

## Follow-up prompts the skill should handle well

- "What if we do not have Okta audit logs older than 90 days?"
- "How do I prove the drift job itself is running reliably?"
- "Can I reuse this for ISO 27001 A.5.15?"
