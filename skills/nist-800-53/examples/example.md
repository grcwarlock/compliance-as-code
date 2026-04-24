# Example: Tailoring moderate baseline for a SaaS on AWS

**User prompt:** "Tailor the moderate baseline for a SaaS app hosted on AWS — what can we inherit and what is customer-implemented? We also need to be FedRAMP Moderate ready."

## Expected working style

The skill should:

1. Confirm baseline and overlay (Moderate + FedRAMP Moderate).
2. Name specific controls in families where inheritance is typical vs customer-implemented.
3. Reference AWS's customer responsibility matrix as the source of truth, not generic claims.
4. Flag the parameter-assignment work that is easy to underestimate.
5. Point to OSCAL as the production format, not Word.

## Example response shape

> **Baseline:** 800-53 Rev. 5 Moderate + FedRAMP Moderate overlay. ~330 controls base, FedRAMP adds tailoring on top. Assume AWS commercial (us-east / us-west regions); for GovCloud the inheritance differs slightly.
>
> **Reliable inheritance from AWS (verify against current AWS customer responsibility matrix):**
>
> - `PE` family (Physical and Environmental Protection) — fully inherited.
> - `MA` Maintenance — physical maintenance inherited; logical maintenance of your workloads is yours.
> - `MP` Media Protection — physical media inherited; digital media handling in your application is yours.
> - Portions of `CP` — facility-level redundancy inherited; your application's DR design and tested restores are yours.
>
> **Typically shared (you implement the customer portion):**
>
> - `AC-2` Account Management — AWS provides IAM; you define account types, implement automated account lifecycle, disable inactive accounts, review quarterly. Enhancements `AC-2(1)`, `AC-2(3)`, `AC-2(4)` are in the baseline and demand concrete engineering.
> - `AU-2`, `AU-3`, `AU-6`, `AU-9`, `AU-11` — AWS provides CloudTrail; you configure events, retention, review, protection, and correlation. `AU-6(3)` (correlation across sources) is a SIEM-level engineering commitment.
> - `CM-2`, `CM-3`, `CM-6`, `CM-7`, `CM-8` — AWS provides the infrastructure; you configure baselines (IaC), change control, configuration settings, least functionality, inventory. `CM-7(2)` (execution restriction via allow-listing) typically means admission controllers in your container platform.
> - `SC-7` Boundary Protection — AWS provides VPC; you design segmentation, firewall rules, managed services boundaries. Multiple enhancements apply.
> - `SC-8`, `SC-13`, `SC-28` — AWS provides the crypto primitives (TLS, KMS); you configure ciphers, key policies, encryption at rest.
> - `SI-2`, `SI-3`, `SI-4` — AWS provides some monitoring; you implement application-level flaw remediation (patch SLAs), malware defences, and real-time monitoring with correlation.
>
> **Customer-implemented in full:**
>
> - `AC` application-level access (RBAC in your app, not AWS IAM).
> - `AT` family — your training program.
> - `IR` family — your incident response plan, detection, and drills (beyond AWS's own incident notifications).
> - `PL`, `PM`, `PS` — program-level documentation and personnel security.
> - `RA` — your risk assessment cadence and vulnerability scanning of your workloads.
> - `SA` — your SDLC controls: code review, SAST, dependency scanning, IaC scanning, release management.
> - `SR` — supply chain controls: SBOM generation, artifact signing, vendor risk management.
>
> **Parameter assignments that bite:**
>
> The Moderate baseline leaves many controls with `[Assignment: organization-defined values]`. These are engineering commitments disguised as words. Key ones:
>
> - `AC-2(3)` Inactive account threshold — FedRAMP requires ≤35 days.
> - `AU-11` Audit record retention — FedRAMP requires 1 year online, 3 years archive minimum.
> - `CM-7(2)` Execution restriction technique — you must pick one (allow-listing, deny-listing, role-based) and enforce it.
> - `IA-5(1)` Authenticator requirements — or "federated SSO with NIST SP 800-63B AAL2+ authenticator" if you have no local accounts.
> - `SI-2` Flaw remediation timelines — FedRAMP is strict: critical 30 days, high 30 days, moderate 90 days.
>
> Each parameter is a concrete engineering SLO. Set them once in a canonical location and reference from SSP, runbooks, and tickets — drift is a finding.
>
> **Production format:**
>
> Use OSCAL. NIST publishes the Catalog and Profiles as OSCAL JSON; tooling will thank you later. Produce your SSP as OSCAL JSON with deterministic UUID5 keys (see `references/oscal-emission-patterns.md`). The markdown narrative can stay as markdown for editing; emit OSCAL from it in CI.
>
> **Before you start:**
>
> - Get the specific AWS customer responsibility matrix for your authorisation (Moderate, commercial, not GovCloud if that is your target). AWS publishes different CRMs per authorisation boundary.
> - Get the FedRAMP Moderate Baseline (OSCAL Profile). NIST publishes 800-53 Moderate; FedRAMP publishes the Moderate overlay.
> - Inventory your services. Each inheritable service (Okta, CrowdStrike, Datadog, etc.) has its own CRM. Wire them in as Component Definitions, not narrative.

## What a bad response looks like

- "Inherit PE, MA, MP from AWS." (correct but insufficient; skips the shared controls that drive most of the work)
- Claiming inheritance from AWS's SOC 2 report. (SOC 2 is not a FedRAMP authorisation)
- "Use FedRAMP templates." (true but glosses over the engineering commitments buried in parameters)

## Follow-up prompts the skill should handle well

- "Write the customer-implementation narrative for AC-2 for our system."
- "What evidence does FedRAMP expect for SI-2 patch timelines?"
- "Generate an OSCAL Component Definition skeleton for Okta covering AC-2, AC-3, IA-2, IA-5."
