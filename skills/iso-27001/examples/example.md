# Example: Mapping existing SOC 2 controls onto Annex A 2022

**User prompt:** "We passed SOC 2 Type 2 last year. Now we need ISO 27001. How much of our existing evidence covers Annex A, and where are the gaps?"

## Expected working style

The skill should:

1. Acknowledge the reuse opportunity is real (70% overlap is typical).
2. Name specific SOC 2 CC → Annex A 2022 mappings — not "everything maps everywhere."
3. Identify Annex A controls that SOC 2 does not cover (these are the real gaps).
4. Flag the ISMS clauses (4–10) as a separate workstream that SOC 2 does not address at all.

## Example response shape

> Most of your CC6 and CC7 evidence is reusable. Annex A adds a small set of controls SOC 2 does not directly cover, and ISO adds a management system (Clauses 4–10) that SOC 2 has no analogue for. Breakdown:
>
> **Direct reuse (~60% of Annex A):**
>
> - CC6.1 → A.5.15, A.5.16, A.8.2, A.8.3, A.8.5. Same evidence: IdP logs, IAM snapshots, drift tickets.
> - CC6.6 → A.8.20, A.8.21, A.8.24. TLS inventory, cipher policy, KMS audit.
> - CC6.8 → A.8.1, A.8.7, A.8.19. Endpoint posture, admission control, signed artifacts.
> - CC7.1 → A.8.9. IaC drift detector.
> - CC7.2 → A.8.15, A.8.16. Log pipeline + monitoring.
> - CC7.3 → A.5.24–A.5.27. Incident response records.
> - CC8 → A.8.32. Change management.
>
> **Partial reuse (~10%):**
>
> - CC9 partially covers A.5.19–A.5.23 (supplier management) but Annex A expects a more structured supplier register than SOC 2 typically requires.
> - CC6.7 overlaps A.8.10 (information deletion) but ISO asks for a retention policy tied to data categories, which SOC 2 does not specifically require.
>
> **Genuine gaps (you will build these):**
>
> - **A.5.7 Threat intelligence.** SOC 2 is silent. ISO expects a process that pulls in threat feeds, evaluates relevance, and documents decisions.
> - **A.5.23 Information security for use of cloud services.** A cloud-specific policy covering CSP selection, shared-responsibility articulation, and exit planning.
> - **A.6.3 Awareness, education, and training.** SOC 2 accepts generic security training; ISO wants documented competence per role.
> - **A.7.x Physical controls.** If you are office-less or fully remote, document that scope decision. If not, physical controls need real evidence (badge logs, visitor registers, equipment inventories).
> - **A.8.28 Secure coding.** You probably already do this; ISO wants it written down with enforcement evidence (linters, review checklists, training records).
>
> **The Clauses 4–10 workstream:**
>
> SOC 2 has no equivalent. You will need:
>
> - Context and scope documentation (Clause 4).
> - Signed information security policy, RACI, and measurable objectives (Clause 5 + 6).
> - Competence records and document control (Clause 7).
> - Internal audit program (Clause 9.2).
> - Management review cadence with recorded minutes (Clause 9.3).
> - Non-conformity and corrective action register (Clause 10).
>
> Most Stage 1 audits fail or get caveated because Clauses 4–10 were treated as a paperwork exercise. Plan to resource this as a separate workstream, not as a layer on top of your existing SOC 2 program.

## What a bad response looks like

- "ISO 27001 is basically SOC 2 + ISMS, map them directly." (too coarse; auditor will find real gaps)
- "Here is a 93-row table mapping every Annex A control to a CC." (busy-work; most of the table is redundant)
- "Hire a consultant." (this skill is engineer-voice, not vendor-voice)

## Follow-up prompts the skill should handle well

- "What exact shape should our supplier register take for A.5.19–A.5.23?"
- "We are fully remote. How do I justify scoping out A.7 physical controls?"
- "How do I run an internal audit program without hiring a dedicated internal auditor?"
