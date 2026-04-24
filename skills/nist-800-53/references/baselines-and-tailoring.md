# Baselines and Tailoring

NIST SP 800-53B defines three baselines — **Low**, **Moderate**, and **High** — plus a **Privacy** baseline. A baseline is a pre-selected set of controls and enhancements appropriate for systems at that FIPS 199 impact level.

You do not start from 800-53's full catalog. You start from a baseline and tailor.

## FIPS 199 impact categorisation

Impact is categorised against three objectives: **Confidentiality**, **Integrity**, **Availability**. Each is rated Low, Moderate, or High. The overall system impact is the highest of the three (high-water mark rule).

| Impact | Typical system example |
|---|---|
| Low | Public-facing marketing site; no sensitive data |
| Moderate | Internal business apps; customer data of moderate sensitivity; most SaaS products |
| High | Systems that, if compromised, have severe or catastrophic effect on operations, assets, or individuals — critical infrastructure, many federal systems |

Most commercial SaaS that ends up in 800-53 land is Moderate. FedRAMP Moderate authorisation is the common target.

## Baseline control counts (approximate)

Exact counts drift by Rev. 5 revision; the catalog is authoritative. Rough scale:

| Baseline | Controls + enhancements (approx.) |
|---|---|
| Low | ~130 |
| Moderate | ~330 |
| High | ~420 |
| Privacy | ~95 (adds to any of the above) |

## Tailoring actions

Tailoring is the process of adjusting the baseline for your system. Actions permitted:

1. **Identifying and designating common controls** — controls inherited from a provider or enterprise service, implemented once for many systems.
2. **Applying scoping considerations** — adjusting controls based on functional, technical, operational, or physical applicability.
3. **Selecting compensating controls** — substituting a control when the baseline control is genuinely infeasible, with documented rationale.
4. **Assigning values to organisation-defined parameters** — 800-53 controls often contain `[Assignment: organization-defined values]`. Tailoring fills these in (e.g., "inactive account threshold: 30 days").
5. **Supplementing baselines** — adding controls or enhancements beyond the baseline because your risk assessment says so.
6. **Providing additional specification information** — clarifying how a control is implemented.

Everything except #4 (parameter assignment) requires explicit rationale in the SSP.

## Assignment parameters — the high-value tailoring

Most tailoring effort goes into organisation-defined parameters. Examples from moderate baseline:

- `AC-2` account types in use: [internal, service, privileged, shared]
- `AC-2(3)` inactive account disable threshold: [35 days]
- `AU-11` audit record retention: [1 year online, 3 years archive]
- `CM-7(2)` software execution restriction technique: [allow-listing via admission controller]
- `IA-5(1)` password complexity: [14 characters, upper, lower, digit, symbol] or [federated SSO; no local passwords]
- `SI-2` patching time from release: [critical: 72 hours, high: 15 days, medium: 30 days]

Parameters drive concrete engineering commitments. Parameter drift — saying "critical in 72 hours" and patching in 14 days — is the most common moderate-baseline finding.

## Overlays

An overlay is a named tailoring applied to a baseline. Common overlays:

| Overlay | Source | Adds / strengthens |
|---|---|---|
| FedRAMP Moderate | FedRAMP PMO | Additional controls and tightened parameters beyond 800-53 Moderate; specific audit expectations |
| FedRAMP High | FedRAMP PMO | Similar, for High baseline |
| FedRAMP Low+ | FedRAMP PMO | Hybrid between Low and Moderate for lower-risk SaaS |
| CJIS | FBI Criminal Justice Information Services | Criminal justice data handling |
| HIPAA | HHS | Health information privacy and security |
| CNSSI 1253 | Committee on National Security Systems | Classified and national security systems |
| StateRAMP | StateRAMP PMO | State and local government, largely mirrors FedRAMP |
| TX-RAMP, AZ-RAMP, etc. | Respective state programs | State-level authorisations |

Overlays compose with baselines. FedRAMP Moderate = 800-53 Moderate + FedRAMP-specific tailoring.

## Baseline selection decision

For most commercial teams:

1. If you are federal-market: the agency tells you the baseline. Typically Moderate.
2. If you are state-market: the overlay tells you. Typically mirrors FedRAMP Moderate.
3. If you are commercial-only but want 800-53 for rigour: Moderate is the practical starting point. Low is too thin for serious production systems; High is unjustifiable without a regulatory driver.
4. If your customer is healthcare/finance: they will tell you. Layer the relevant overlay (HIPAA, FFIEC, etc.) on Moderate.

## Supplementation that almost everyone does

Beyond the baseline, most mature programs add:

- `SI-4(2)` automated tools for real-time analysis (not in Low; in Moderate and above).
- `SI-4(4)` inbound/outbound communications traffic (often tightened beyond baseline).
- `AU-6(3)` correlation across sources (not in Low; in Moderate and above).
- `CM-7(2)` least functionality — explicit application allow-listing.
- `SR-3` supply chain controls — SBOM generation and review.
- `IA-5(1)` strengthened authenticator management parameters.

These are not required but are consistent with the direction of risk-based thinking in Rev. 5.

## Inheritance documentation

The SSP must describe, per control, which parts are:

- **Inherited** from a provider (marked with the provider)
- **Shared** between the provider and the system (marked with the split)
- **Customer-implemented**

See `control-inheritance.md` for the inheritance model.

## OSCAL baseline artifacts

NIST publishes all three baselines as OSCAL Profiles. A Profile is a tailored selection from the Catalog. Using the OSCAL Profile as the starting point for your SSP saves you from manually maintaining the control list; your SSP becomes "this Profile + our parameter values + our implementation narrative," expressed as OSCAL.

## Common mistakes

- **Inventing controls not in the catalog.** If you want something the catalog does not specify, capture it as a supplement with a clear rationale. Do not rename it to match a catalog ID.
- **Setting parameters aspirationally.** "We patch critical in 24 hours" on paper, 21 days in practice. The gap becomes the finding.
- **Ignoring enhancements.** Baseline selection includes specific enhancements; skipping them ("we only implemented AC-2, not AC-2(1)") is a finding, not a scope decision.
- **Parameter inconsistency across documents.** SSP says 30 days; runbook says 45 days. Auditor picks the weaker one. Keep parameters in one canonical location referenced by both.
