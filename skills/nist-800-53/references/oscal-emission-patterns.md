# OSCAL Emission Patterns

OSCAL (Open Security Controls Assessment Language) is the machine-readable expression of NIST control catalogs, baselines, system security plans, assessments, and POA&M. It exists in JSON, XML, and YAML; JSON is the most common in tooling pipelines.

If your team is producing 800-53 artifacts in Word and Excel today, OSCAL is the path away from that.

## Models you will care about

| Model | Purpose | Who produces it |
|---|---|---|
| **Catalog** | The control catalog itself | NIST publishes 800-53 Rev. 5 as Catalog |
| **Profile** | A baseline (selection + tailoring of a Catalog) | NIST publishes Low/Moderate/High/Privacy as Profiles |
| **Component Definition** | What controls a service or product satisfies | You (or your vendor) produces this for each major service |
| **System Security Plan (SSP)** | Description of how a system implements controls | You produce this for each authorisation boundary |
| **Assessment Plan (AP)** | How an assessment will be conducted | Assessor produces this |
| **Assessment Results (AR)** | Findings from an assessment | Assessor produces this |
| **Plan of Action and Milestones (POA&M)** | Tracking remediation of findings | You produce this; assessor reviews |

You consume Catalog and Profile (NIST publishes them). You produce Component Definitions, SSP, and POA&M.

## Deterministic UUIDs

OSCAL uses UUIDs heavily — every control implementation, party, role, component, and statement has a UUID. The natural temptation is `uuid.uuid4()` for each.

**Do not use uuid4 for OSCAL.** Use UUID5 with a fixed namespace.

Reasoning: OSCAL artifacts are regenerated frequently. If every regeneration produces new UUIDs, every diff is meaningless noise — every reviewer sees "the entire SSP changed" when nothing changed. With UUID5 keyed on stable inputs (system ID + control ID + statement ID), the same logical thing always gets the same UUID.

Pattern:

```python
import uuid

OSCAL_NS = uuid.UUID("00000000-0000-0000-0000-000000000000")  # pick once, never change

def oscal_uuid(*parts: str) -> str:
    key = ":".join(parts)
    return str(uuid.uuid5(OSCAL_NS, key))

# Usage
oscal_uuid("system", "my-saas")                                # SSP UUID
oscal_uuid("system", "my-saas", "ac-2")                        # control implementation UUID
oscal_uuid("system", "my-saas", "ac-2", "stmt-a")              # statement UUID
oscal_uuid("component", "okta-idp")                            # Component UUID
```

Pin the namespace UUID in your repo and never change it. Every artifact in the family uses the same namespace; UUIDs become stable across regenerations and stable across teams.

## Control ID normalisation

OSCAL expects lowercase control IDs with hyphens: `ac-2`, `ac-2.3`, `cc6-1`. NIST publishes catalog IDs in this form. Tools and humans often refer to controls in mixed-case (`AC-2`, `AC-2(3)`, `CC6.1`).

Normalise at the boundary. Pattern:

```python
import re

def normalise_control_id(s: str) -> str:
    # AC-2(3) -> ac-2.3 ; CC6.1 -> cc6-1
    s = s.strip().lower()
    s = re.sub(r"\((\d+)\)", r".\1", s)         # enhancements
    s = s.replace(".", "-", 1) if re.match(r"^[a-z]+\d+\.\d+$", s) else s
    return s
```

Test against your actual catalog. Edge cases (privacy controls, CSF subcategories) may need adjustment.

## Schema validation

Every OSCAL model has a published JSON Schema (and XML XSD). Validate on emit, every time, in CI.

```python
import json
from jsonschema import Draft202012Validator

with open("oscal_schema_ssp.json") as f:
    schema = json.load(f)

with open("my_ssp.json") as f:
    ssp = json.load(f)

validator = Draft202012Validator(schema)
errors = sorted(validator.iter_errors(ssp), key=lambda e: e.path)
if errors:
    for e in errors:
        print(f"{list(e.path)}: {e.message}")
    raise SystemExit(1)
```

NIST publishes the schemas at `https://csrc.nist.gov/projects/oscal`. Pin a specific schema version in your build; when NIST releases a new version, update intentionally and re-validate the whole corpus.

## Emission patterns

### From SSP narrative to OSCAL SSP

If your SSP today is markdown, build an emitter that:

1. Reads the markdown structure (one section per control, frontmatter for metadata).
2. Emits the OSCAL SSP JSON with deterministic UUIDs keyed on (system_id, control_id, statement_id).
3. Validates against the OSCAL SSP schema.
4. Writes the JSON alongside the markdown.

The markdown stays editable; the JSON is generated. Reviewers diff the markdown; tooling reads the JSON.

### Component Definitions for inheritance

For each major inheritable service:

```json
{
  "component-definition": {
    "uuid": "...",
    "metadata": { ... },
    "components": [
      {
        "uuid": "...",
        "type": "service",
        "title": "Okta SSO + MFA",
        "control-implementations": [
          {
            "uuid": "...",
            "source": "https://raw.githubusercontent.com/usnistgov/oscal-content/main/nist.gov/SP800-53/rev5/json/NIST_SP-800-53_rev5_catalog.json",
            "implemented-requirements": [
              {
                "uuid": "...",
                "control-id": "ac-2",
                "statements": [...]
              }
            ]
          }
        ]
      }
    ]
  }
}
```

The system's SSP references the Component by UUID; the inheritance is computed, not duplicated.

### Assessment Results from continuous controls

If you run continuous controls (see `../../soc-2/references/continuous-monitoring-patterns.md`), emit OSCAL AR records for each control's evidence in the period:

```json
{
  "assessment-results": {
    "uuid": "...",
    "metadata": { ... },
    "results": [
      {
        "uuid": "...",
        "title": "Continuous AC-2 evidence — 2026-Q1",
        "start": "2026-01-01T00:00:00Z",
        "end": "2026-03-31T23:59:59Z",
        "findings": [...],
        "observations": [...]
      }
    ]
  }
}
```

Assessors find this format easier to consume than ad-hoc evidence packs.

## Round-trip: NIST catalog → your SSP → assessor's AR

The whole point of OSCAL is round-tripability:

1. Pull NIST 800-53 Rev. 5 Catalog (OSCAL JSON).
2. Apply the appropriate Profile (Moderate, with FedRAMP overlay).
3. Generate your SSP referencing the Profile + Component Definitions for inheritance + your customer-implementation narrative.
4. Hand SSP to assessor.
5. Assessor produces Assessment Plan and Assessment Results referencing your SSP.
6. Findings produce POA&M entries referencing the SSP and AR.

Every artifact references the previous by UUID; the chain is auditable. Compare to the Word/Excel pipeline where the same control is described differently in five documents and reconciliation is a manual job.

## Tooling

There is a small ecosystem of OSCAL tooling — the NIST oscal-cli for validation and conversion, GovReady-Q for SSP authoring, Compliance Trestle for round-tripping in CI/CD, several XML/JSON converters. None is mandatory; the schema is the contract. Pick what fits your existing build pipeline.

Avoid tools that hide OSCAL behind a proprietary intermediate model. The point of OSCAL is interoperability; if your tool can only emit "OSCAL after a transformation," you have re-introduced lock-in.

## Common mistakes

- Using `uuid4` everywhere — diffs become noise, regenerations break consumers.
- Not normalising control IDs — `AC-2` and `ac-2` and `Ac-2` cause silent mismatches.
- Skipping schema validation in CI — invalid OSCAL discovered by an assessor is worse than discovered by a build.
- Treating OSCAL as a destination format only — round-trip is the point. If you cannot regenerate the SSP from inputs, you have a Word document with extra steps.
- Hand-editing emitted OSCAL JSON — once you do this, the markdown source and the JSON drift. Always regenerate.
