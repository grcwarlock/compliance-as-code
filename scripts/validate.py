#!/usr/bin/env python3
"""Validate skills, agents, and connectors in this repository.

Checks performed:

- Each `skills/*/SKILL.md` has YAML frontmatter with required fields
  (`name`, `description`, `when_to_use`) and `name` matches the directory.
- Each `agents/*/AGENT.md` has the same frontmatter contract.
- Internal markdown links in SKILL.md, AGENT.md, and their references resolve
  to existing files.
- `connectors/schema/evidence.schema.json` parses as a valid Draft 2020-12
  JSON Schema.
- Each `connectors/*/examples/output.json` validates against the evidence
  schema.

Exit non-zero on any failure.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print(
        "ERROR: pyyaml is required. Install with: pip install -r requirements-dev.txt",
        file=sys.stderr,
    )
    sys.exit(2)

try:
    from jsonschema import Draft202012Validator
except ImportError:
    print(
        "ERROR: jsonschema is required. Install with: pip install -r requirements-dev.txt",
        file=sys.stderr,
    )
    sys.exit(2)


REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "skills"
AGENTS_DIR = REPO_ROOT / "agents"
CONNECTORS_DIR = REPO_ROOT / "connectors"
EVIDENCE_SCHEMA_PATH = CONNECTORS_DIR / "schema" / "evidence.schema.json"

REQUIRED_FRONTMATTER = {"name", "description", "when_to_use"}

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def parse_frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    m = FRONTMATTER_RE.match(text)
    if not m:
        raise ValueError(f"{path}: missing YAML frontmatter")
    data = yaml.safe_load(m.group(1)) or {}
    if not isinstance(data, dict):
        raise ValueError(f"{path}: frontmatter is not a mapping")
    return data


def check_links(md_path: Path, errors: list[str]) -> None:
    text = md_path.read_text(encoding="utf-8")
    for match in LINK_RE.finditer(text):
        target = match.group(1).split("#", 1)[0].strip()
        if not target or target.startswith(("http://", "https://", "mailto:")):
            continue
        resolved = (md_path.parent / target).resolve()
        if not resolved.exists():
            errors.append(f"{md_path}: broken link to {target}")


def validate_definitions(
    base_dir: Path,
    filename: str,
    label: str,
    errors: list[str],
) -> int:
    if not base_dir.exists():
        return 0
    count = 0
    for definition in sorted(base_dir.glob(f"*/{filename}")):
        count += 1
        try:
            fm = parse_frontmatter(definition)
        except ValueError as e:
            errors.append(str(e))
            continue
        missing = REQUIRED_FRONTMATTER - set(fm)
        if missing:
            errors.append(
                f"{definition}: missing frontmatter fields: {sorted(missing)}"
            )
        if fm.get("name") != definition.parent.name:
            errors.append(
                f"{definition}: frontmatter name '{fm.get('name')}' "
                f"does not match directory name '{definition.parent.name}'"
            )
        check_links(definition, errors)
        ref_dir = definition.parent / "references"
        if ref_dir.exists():
            for ref in sorted(ref_dir.glob("*.md")):
                check_links(ref, errors)
        ex_dir = definition.parent / "examples"
        if ex_dir.exists():
            for ex in sorted(ex_dir.glob("*.md")):
                check_links(ex, errors)
    print(f"{label:10}: {count}")
    return count


def validate_evidence_schema(errors: list[str]) -> Draft202012Validator | None:
    if not EVIDENCE_SCHEMA_PATH.exists():
        print("schema    : absent")
        return None
    try:
        schema = json.loads(EVIDENCE_SCHEMA_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        errors.append(f"{EVIDENCE_SCHEMA_PATH}: invalid JSON ({e})")
        print("schema    : invalid")
        return None
    try:
        Draft202012Validator.check_schema(schema)
    except Exception as e:  # noqa: BLE001 - jsonschema raises various types
        errors.append(f"{EVIDENCE_SCHEMA_PATH}: invalid JSON Schema ({e})")
        print("schema    : invalid")
        return None
    print("schema    : ok")
    return Draft202012Validator(schema)


def validate_connector_examples(
    validator: Draft202012Validator | None,
    errors: list[str],
) -> int:
    if validator is None or not CONNECTORS_DIR.exists():
        print("examples  : 0")
        return 0
    count = 0
    for example in sorted(CONNECTORS_DIR.glob("*/examples/output.json")):
        count += 1
        try:
            payload = json.loads(example.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            errors.append(f"{example}: invalid JSON ({e})")
            continue
        records = payload if isinstance(payload, list) else [payload]
        for i, record in enumerate(records):
            for err in validator.iter_errors(record):
                errors.append(f"{example}[{i}]: {err.message}")
    print(f"examples  : {count}")
    return count


def main() -> int:
    errors: list[str] = []
    validate_definitions(SKILLS_DIR, "SKILL.md", "skills", errors)
    validate_definitions(AGENTS_DIR, "AGENT.md", "agents", errors)
    schema = validate_evidence_schema(errors)
    validate_connector_examples(schema, errors)

    if errors:
        print()
        print(f"FAIL ({len(errors)} issue(s)):")
        for e in errors:
            print(f"  - {e}")
        return 1
    print()
    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
