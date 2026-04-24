# OSCAL Assessment Results — Structure

Minimal valid shape for an Assessment Results document (OSCAL 1.1.x).

## Top-level

```json
{
  "assessment-results": {
    "uuid": "<uuid5>",
    "metadata": { ... },
    "import-ap": { "href": "..." },
    "results": [ ... ]
  }
}
```

`import-ap` references the Assessment Plan this result corresponds to. If not yet available, use a placeholder `"href": "#pending"` with a `remarks` field.

## Metadata (required)

```json
{
  "title": "Q1 2026 continuous assessment — my-saas",
  "last-modified": "2026-04-17T14:02:11Z",
  "version": "1.0.0",
  "oscal-version": "1.1.2"
}
```

Optional but recommended:

- `published` — first publication date
- `parties` — assessors, system owner, authorising official
- `roles` — role definitions
- `responsible-parties` — who played which role

## Results entry

```json
{
  "uuid": "<uuid5>",
  "title": "Q1 2026 continuous assessment",
  "start": "2026-01-01T00:00:00Z",
  "end": "2026-03-31T23:59:59Z",
  "local-definitions": { ... },
  "reviewed-controls": {
    "control-selections": [
      { "include-controls": [{"control-id": "ac-2"}, {"control-id": "ac-2.3"}] }
    ]
  },
  "findings": [ ... ],
  "observations": [ ... ]
}
```

## Finding entry

```json
{
  "uuid": "<uuid5>",
  "title": "AC-2 user access review — one quarter missed",
  "description": "Q3 2025 quarterly UAR for the GL service was not performed. Root cause ...",
  "target": {
    "type": "objective-id",
    "target-id": "ac-2",
    "status": { "state": "not-satisfied" }
  },
  "related-observations": [ { "observation-uuid": "<uuid5>" } ]
}
```

`target.status.state` values: `satisfied`, `not-satisfied`, `other`.

## Observation entry

```json
{
  "uuid": "<uuid5>",
  "title": "Missing UAR evidence for Q3 2025",
  "methods": ["EXAMINE"],
  "types": ["finding"],
  "description": "No record of UAR execution for GL service in Q3 2025 observation window.",
  "collected": "2026-04-15T10:00:00Z"
}
```

`methods` values: `EXAMINE`, `INTERVIEW`, `TEST`. `types` values: `finding`, `evidence`, `milestone`, etc.

## Omitting fields

OSCAL is permissive in several places. Omit optional fields rather than populating them with empty strings or nulls. Empty strings fail validation in fields expecting `NonEmptyString`.

## Common validation errors

- Missing `oscal-version` in metadata.
- `last-modified` without timezone (must be RFC 3339).
- Control IDs not normalised (`AC-2` in a `control-id` field where `ac-2` is required).
- Duplicate UUIDs (use UUID5 with distinct keys per entity).
- `uuid` fields that are not valid UUIDs (four hyphens, 8-4-4-4-12 hex).

## Beyond structural validity

Schema validation is necessary but not sufficient. A schema-valid document can still be wrong:

- Findings that reference control IDs not in the assessment scope.
- `start` > `end` on a result period.
- Observations referenced by findings but not present in the observations array.

These semantic checks are not part of the agent's job — they should be caught by a downstream validator or a human review. The agent's responsibility is: valid JSON, valid schema, plausible content shaped by the input notes.
