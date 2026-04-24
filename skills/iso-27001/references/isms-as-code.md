# ISMS-as-Code

The Information Security Management System (ISMS) is the thing that gets certified. ISO 27001 Clauses 4–10 define what an ISMS must contain. Most implementations treat each clause as a document ("we have a Context Establishment document, see sharepoint://..."). That satisfies the letter of the standard but produces an ISMS that goes stale the week after the audit.

ISMS-as-code treats each clause as a system artifact — a record store, a workflow, a pipeline — so the ISMS is continuously maintainable.

## Clauses 4–10 mapped to system shapes

### Clause 4 — Context of the organisation

**Traditional:** a document describing internal and external issues, interested parties, and the ISMS scope.

**As code:** three structured datasets, each versioned in a repository:

- `context/issues.yaml` — internal and external issues with date, owner, review cadence.
- `context/interested-parties.yaml` — stakeholder registry with requirements and communication channels.
- `context/isms-scope.md` — scope statement pointing to systems, locations, and exclusions. Each referenced system should link to an asset inventory record.

A quarterly job compares the scope declaration to the actual asset inventory. Deltas open tickets.

### Clause 5 — Leadership

**Traditional:** a signed information security policy and an accountability matrix in a slide deck.

**As code:** 

- Policy repository with every policy as markdown, signed by commit + PR approval from the CISO (or equivalent). Signature is the git commit, not a signature page.
- RACI entries as YAML, queryable. New services register themselves and inherit RACI from service templates.

### Clause 6 — Planning

**Traditional:** risk assessment methodology as a document; risk register as a spreadsheet; Statement of Applicability as a PDF.

**As code:** see `risk-register-schema.md`. The risk register is a typed data store with referential integrity to Annex A controls and to evidence sources. The Statement of Applicability is a derived view — a join of Annex A × applicability decision × evidence source. No one maintains it by hand.

### Clause 7 — Support

**Traditional:** training slides and attendance records in an LMS export.

**As code:**

- Competence matrix as YAML (role × required competences).
- Training records in the LMS, queried via API into an evidence store.
- Documented information handled by git + review workflow — every controlled document has a version, an owner, and a review date that fires a ticket 30 days before expiry.

### Clause 8 — Operation

**Traditional:** change management procedure as a Word doc; operational controls described narratively.

**As code:**

- Change management is the actual pipeline — merge gates, approval receipts, deployment records (the same pipeline SOC 2 CC8 uses).
- Annex A control implementations are pointers to the system or repo that instantiates them, with evidence of operation.

### Clause 9 — Performance evaluation

**Traditional:** KPIs in a quarterly slide deck; internal audit reports as PDFs; management review minutes as Word docs.

**As code:**

- Security KPIs as dashboards backed by the event store (MTTR for vulnerabilities, percentage of deprovisioning events within SLA, drift-ticket close time).
- Internal audit reports structured as issue trackers with findings, owners, and remediation dates. The audit itself can be automated for control designs where evidence is continuous.
- Management review as a quarterly agenda template + recorded minutes + decision log, all in the same document system as other governance records.

### Clause 10 — Improvement

**Traditional:** nonconformity register as a spreadsheet.

**As code:** nonconformity register is a dedicated table with state machine (open → investigated → root cause identified → corrective action → closed), SLA timers, and links to the originating finding (internal audit, external audit, incident, risk review).

## Minimum viable ISMS-as-code

If you are starting from scratch, the lowest-cost implementation that satisfies the clauses:

1. One git repository: `isms/` with `policies/`, `risk/`, `soa/`, `context/`, `governance/`, `nonconformity/`.
2. Every file has YAML frontmatter: `owner`, `review_due`, `last_reviewed`, `version`.
3. CI job that fails if any `review_due` is in the past.
4. Periodic job that produces a derived Statement of Applicability markdown from the risk register + Annex A decisions.
5. Issue tracker for nonconformities, with labels mapping to clause numbers.

This is enough to pass Stage 1 (documentation review) and enough structure to keep the ISMS maintained between audits. The remainder is Annex A implementation (Clause 8), which is where the real engineering lives.

## What auditors think of this

Most ISO auditors are not surprised by code-based ISMS implementations anymore; many prefer them because evidence retrieval is faster. The common pushback is "where is the signed PDF of the policy?" — answer: the commit has an author, a timestamp, and a digital signature (if the repo enforces signed commits). Offer to export a rendered PDF per policy on request.

Auditors sometimes want to see that the ISMS has been "adopted" — that the living document system is actually used, not a performance. The evidence for adoption is activity: commit history on policies, closed nonconformities, management review decisions referencing specific records. If the repo is silent for 11 months of the year and then lights up in audit month, that is its own finding.
