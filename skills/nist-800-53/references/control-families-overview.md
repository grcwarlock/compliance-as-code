# 800-53 Rev. 5 Control Families — Engineer's View

NIST SP 800-53 Rev. 5 organises controls into **20 families**. Each family is a two-letter code. The catalog is large (1,000+ controls counting enhancements); families let you scope your effort.

## The 20 families

| Code | Family | What it is really about | Engineer-relevance |
|---|---|---|---|
| AC | Access Control | Who can do what in the system | Very high. Most customer-implemented controls. |
| AT | Awareness and Training | Role-appropriate security training | Low-medium. Mostly an L&D / HR workflow. |
| AU | Audit and Accountability | Logging, retention, log protection | Very high. Logging design is a first-order engineering choice. |
| CA | Assessment, Authorization, and Monitoring | How you assess controls and ATOs | Medium. More governance than implementation. |
| CM | Configuration Management | Baselines, change control, inventory | Very high. IaC is the implementation. |
| CP | Contingency Planning | Backups, DR, BCP | High. Tested restores and DR exercises. |
| IA | Identification and Authentication | Identifying users, devices, services | Very high. IdP + MFA + service identity. |
| IR | Incident Response | Plan, detect, respond, recover | High. The IR runbook + detection + response records. |
| MA | Maintenance | Controlled maintenance of systems | Low-medium. Mostly procedural for cloud-native. |
| MP | Media Protection | Physical media handling and destruction | Low for cloud-only; high if you ship hardware. |
| PE | Physical and Environmental Protection | Data centers, facilities, environmental | Often inherited from the CSP. |
| PL | Planning | Security plans, rules of behaviour | Medium. Documentation-heavy. |
| PM | Program Management | Security program governance | Medium. Governance and metrics. |
| PS | Personnel Security | Screening, termination, transfer | Low-medium. HR workflows with IT integration. |
| PT | PII Processing and Transparency | Privacy controls | Medium-high if you handle PII. |
| RA | Risk Assessment | Risk assessments, vulnerability scanning, supply chain | High. Vulnerability scanning and SBOM practice. |
| SA | System and Services Acquisition | Secure acquisition, development, supply chain | High. SDLC controls live here. |
| SC | System and Communications Protection | Network, encryption, boundary protection | Very high. Network design + crypto policy. |
| SI | System and Information Integrity | Malware, flaw remediation, monitoring | Very high. Patching SLAs and detection. |
| SR | Supply Chain Risk Management | Vendor risk, SBOMs, tampering | High. Newer focus area; SBOMs, signed artifacts. |

## The "big six" for most cloud-hosted systems

If you are standing up 800-53 Rev. 5 for a SaaS on a major cloud, ~80% of your customer-implemented effort is in six families:

1. **AC** — IAM, roles, access provisioning
2. **IA** — authentication, service identity
3. **AU** — logging and log protection
4. **CM** — configuration baselines and change control
5. **SC** — network segmentation, encryption in transit
6. **SI** — monitoring, patching, detection

The remaining 14 families still need attention, but they are often lighter engineering lift — inherited, policy-heavy, or straightforwardly procedural.

## Controls vs control enhancements

Rev. 5 numbers controls with a base (`AC-2`) and enhancements (`AC-2(1)` through `AC-2(13)`). Enhancements strengthen the base. Baselines select specific enhancements; you can add more under tailoring.

Enhancements often bundle non-trivial engineering work. Examples:

- `AC-2(1)` — automated account management. Implication: you can create, modify, and disable accounts programmatically, with logged evidence.
- `AC-2(3)` — disable inactive accounts. Implication: automated job that finds inactive accounts and disables them, with a tunable threshold.
- `AC-2(12)` — account monitoring for atypical usage. Implication: anomaly detection on authentication / authorization events.
- `AU-6(3)` — correlate audit review. Implication: SIEM-level correlation, not just retention.
- `SI-4(2)` — automated tools for real-time analysis. Implication: streaming analytics on log events.

When the baseline selects an enhancement, plan the engineering for the enhancement, not the bare base control.

## Withdrawn and deprecated controls

Rev. 5 withdrew some Rev. 4 controls and moved their content into others (often SC or SR). If you are migrating from Rev. 4, do not carry over withdrawn controls — the transition documentation from NIST lists the replacements.

## Control overlays

Overlays are pre-packaged sets of controls and enhancements tailored for a context (FedRAMP, CJIS, HIPAA, CNSSI, classified). An overlay is applied on top of a baseline to add or strengthen controls for a specific use case. See `baselines-and-tailoring.md` for how overlays compose with baselines.

## Looking up a control

Primary source: `https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final`. NIST also publishes the catalog as OSCAL JSON — much easier to query programmatically than the PDF. The OSCAL catalog is the right input to a tooling pipeline; the PDF is the right reference for a human reading the exact wording of a control.

## Mapping to other frameworks

NIST publishes mappings between 800-53 and other standards (ISO 27001, CSF, HIPAA Security Rule). These are starting points, not authoritative for your SSP. Use them to identify reusable evidence from an existing ISO or SOC 2 program — not as a substitute for tailoring.

## Realistic scale expectations

- **Low baseline SSP:** ~130 controls + enhancements, customer-implemented or inherited.
- **Moderate baseline SSP:** ~330 controls + enhancements. This is the FedRAMP Moderate level most SaaS providers target.
- **High baseline SSP:** ~420+ controls + enhancements. Significant additional investment over Moderate — especially in AU, IR, and SC.

If someone proposes "we will do High baseline" without a staffed program, that is a red flag. Moderate is already a full-time job for a small team.
