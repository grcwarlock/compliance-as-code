# Control Inheritance

Most 800-53 systems do not implement every control from scratch. They inherit a meaningful chunk from their hosting provider, from shared enterprise services, and from corporate common controls.

Modeling inheritance accurately is one of the highest-leverage activities in building an SSP. Claimed inheritance that the provider does not actually deliver is a finding. Missed inheritance is wasted engineering work.

## The four responsibility types

FedRAMP uses four categorisations:

| Type | Meaning | SSP implication |
|---|---|---|
| **Inherited** | Provider implements the control fully on your behalf | You document the provider, point to their authorised SSP, and do nothing additional |
| **Shared** | Provider implements a portion; you implement the rest | SSP describes the split explicitly; evidence comes from both parties |
| **Customer-implemented** | You implement the full control in your system | Full implementation narrative + evidence |
| **Customer-configured** | Provider offers the capability; you must configure it correctly | Implementation narrative describes the configuration; evidence is your config state |

"Inherited" ≠ "I use their service." Inheritance requires that the provider's authorised SSP covers the control at your baseline, and the provider's authorisation is current.

## Common inheritance patterns for major CSPs

### AWS (GovCloud and commercial, FedRAMP Moderate authorised)

Typically inherited (verify against AWS's customer responsibility matrix for your authorisation):

- **Physical and Environmental (PE family).** Data center physical access, environmental controls.
- **MA** Maintenance of physical infrastructure.
- **MP** Media protection for physical storage devices.
- Portions of **CP** Contingency Planning — facility-level redundancy, not your application's DR.

Typically shared:

- **AC** Access Control. AWS provides IAM; you configure roles, policies, users.
- **AU** Audit. AWS provides CloudTrail; you configure what is captured, retention, review.
- **CM** Configuration Management. AWS provides the infrastructure; you configure your workloads.
- **CP** Contingency. AWS provides multi-AZ; you design multi-AZ deployment and test DR.
- **SC** System Communications. AWS provides VPC; you design segmentation and firewall rules.
- **SI** System Integrity. AWS provides some monitoring; you implement application-level detection.

Typically customer-implemented:

- **AT** Awareness and Training.
- **IR** Incident Response (beyond AWS's own incident notification).
- **PL** Planning, PS Personnel Security, PM Program Management.
- Application-level **AC**, **AU**, **SC**, **SI**.

### Azure (Commercial and Government, FedRAMP authorisations)

Similar pattern to AWS. Microsoft publishes customer responsibility matrices by service; read the one for your specific services (Azure Government is not the same boundary as commercial Azure).

### Google Cloud (FedRAMP authorisations)

Similar pattern. Google's matrix is narrower in some families than AWS/Azure at equivalent baselines — verify rather than assume.

## Common controls (organisation-level)

Independent of CSP, some controls may be centralised at your organisation level as "common controls" — implemented once by a central team, inherited by every system.

Typical common control candidates:

- **AT-2, AT-3** Security awareness and role-based training (enterprise L&D)
- **CA-5** POA&M process (governance)
- **IA-5** Authenticator management (enterprise IdP)
- **IR-4, IR-5, IR-6** Incident handling, monitoring, reporting (enterprise SOC/CSIRT)
- **PM family** Program Management (enterprise CISO function)
- **PL-2** System Security Plan (meta; the SSP itself)
- **PS family** Personnel Security (enterprise HR/IT)

When a control is common, the system's SSP inherits from a common-control SSP maintained at the organisation level. The common-control provider is named in your SSP's control description.

## Shared-control split documentation

Shared controls are the source of most audit ambiguity. Document the split concretely.

Example for `AC-2` Account Management (AWS-hosted SaaS):

> **AWS responsibility:** provides the IAM service, including the underlying infrastructure for account storage, authentication, and policy evaluation. Inherited per AWS's FedRAMP SSP, AC-2 partial inheritance.
>
> **Customer responsibility:**
>
> - Define account types and roles in the system (AC-2a): service accounts, privileged accounts, standard user accounts, break-glass.
> - Implement automated account management workflow (AC-2(1)): HRIS webhook → IdP → AWS SSO role assignment; logged in event store `evidence://aws-iam/account-lifecycle`.
> - Disable inactive accounts within 35 days (AC-2(3)): weekly scan of IAM; accounts without activity are disabled by a scheduled Lambda; exceptions require documented service-account justification.
> - Review accounts quarterly (AC-2(4)): UAR process described in [runbook].

Break the control down by sub-part (AC-2a, AC-2b, etc.). A single narrative for a shared control is almost always incomplete.

## Evidence consequences

The more a control is inherited, the fewer evidence artifacts you generate. The fewer you generate, the more you rely on the provider's authorisation being current.

This matters at audit. If your provider's ATO expired, or they changed scope (e.g., moved a service to a separate boundary), your inherited controls become uninherited overnight. Document your provider's authorisation status in the SSP and set a reminder to re-check annually or whenever the provider announces a change.

## Provider customer-responsibility matrices (CRMs)

Every FedRAMP-authorised CSP publishes a CRM describing exactly which controls and sub-parts are inherited, shared, or customer-implemented. Get the CRM for your specific authorisation (Moderate vs High, Government vs commercial) and use it as ground truth. Do not rely on general marketing material.

## Modeling inheritance in OSCAL

OSCAL Component Definition is the artifact that expresses inheritance programmatically. Each Component (service, platform, or vendor product) declares which controls it satisfies and how. Your SSP then references Components rather than re-describing the underlying controls.

Pattern:

1. Build or consume a Component Definition for each major inheritable service (AWS IAM, AWS CloudTrail, Okta, Datadog, etc.).
2. In your SSP, state for each control: "This control is satisfied by the <X> Component Definition" plus any customer-implementation narrative.
3. Generate the inheritance table from the SSP + Component Definitions, rather than maintaining it by hand.

See `oscal-emission-patterns.md` for OSCAL emission specifics.

## Common mistakes

- **Claiming inheritance from the CSP's general SOC 2 or ISO 27001 report.** Those are not FedRAMP authorisations and do not transfer inheritance for 800-53.
- **Assuming inheritance at your baseline.** A provider authorised at Moderate does not inherit controls for your High-baseline system.
- **Forgetting shared controls have two evidence sources.** Assessors will ask for both.
- **Not updating when the provider changes services.** A managed service deprecation or a move to a different boundary can silently break inheritance.
