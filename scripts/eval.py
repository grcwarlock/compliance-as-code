#!/usr/bin/env python3
"""Run agent eval cases.

By default this is an OFFLINE evaluator: it reads each agent's
`tests/cases.jsonl`, loads the corresponding `output` file (a frozen example
shipped with the agent), and applies the structural checks declared in the
case. It does not call any LLM.

Use `--with-llm` to additionally call the configured LLM provider
(via LiteLLM) for each case's input, then run the same checks against
the *generated* output instead of the frozen one.

Exit non-zero on any failure.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
AGENTS_DIR = REPO_ROOT / "agents"


def get_path(obj: Any, dotted: str) -> Any:
    """Resolve a dotted path with integer-segment array indexing."""
    cur = obj
    for seg in dotted.split("."):
        if seg.isdigit() and isinstance(cur, list):
            idx = int(seg)
            if idx >= len(cur):
                raise KeyError(f"index {idx} out of range")
            cur = cur[idx]
        elif isinstance(cur, dict):
            if seg not in cur:
                raise KeyError(seg)
            cur = cur[seg]
        else:
            raise KeyError(f"cannot descend into {type(cur).__name__} with segment '{seg}'")
    return cur


def run_check(check: dict, output_text: str, output_obj: Any) -> tuple[bool, str]:
    ctype = check.get("type", "")

    if ctype == "json_valid":
        return (output_obj is not None, "expected valid JSON")

    if ctype == "regex_match":
        pat = re.compile(check["pattern"], re.MULTILINE)
        return (bool(pat.search(output_text)), f"regex /{check['pattern']}/ did not match")

    if ctype == "regex_count_at_least":
        pat = re.compile(check["pattern"], re.MULTILINE)
        n = len(pat.findall(output_text))
        return (n >= check["min"], f"regex /{check['pattern']}/ matched {n} times, expected >= {check['min']}")

    if ctype == "json_has_path":
        if output_obj is None:
            return (False, "output is not JSON")
        try:
            get_path(output_obj, check["path"])
            return (True, "")
        except KeyError as e:
            return (False, f"missing JSON path '{check['path']}': {e}")

    if ctype == "enum_in_path":
        if output_obj is None:
            return (False, "output is not JSON")
        try:
            value = get_path(output_obj, check["path"])
        except KeyError as e:
            return (False, f"missing JSON path '{check['path']}': {e}")
        return (value in check["values"], f"value '{value}' at '{check['path']}' not in {check['values']}")

    if ctype == "json_array_min_length":
        if output_obj is None:
            return (False, "output is not JSON")
        try:
            value = get_path(output_obj, check["path"])
        except KeyError as e:
            return (False, f"missing JSON path '{check['path']}': {e}")
        if not isinstance(value, list):
            return (False, f"value at '{check['path']}' is {type(value).__name__}, expected list")
        return (len(value) >= check["min"], f"array at '{check['path']}' has {len(value)} items, expected >= {check['min']}")

    return (False, f"unknown check type: {ctype}")


def parse_output(output_text: str, output_path: Path) -> Any:
    """Try to parse output as JSON; return None if it is not JSON."""
    if output_path.suffix.lower() == ".json":
        try:
            return json.loads(output_text)
        except json.JSONDecodeError:
            return None
    # Best-effort JSON parse for non-.json files (some agents emit JSON to .md outputs).
    try:
        return json.loads(output_text)
    except json.JSONDecodeError:
        return None


def evaluate_case(agent_dir: Path, case: dict, errors: list[str]) -> bool:
    case_id = case.get("id", "<no-id>")
    output_rel = case.get("output")
    if not output_rel:
        errors.append(f"{agent_dir.name}/{case_id}: case missing 'output' field")
        return False
    output_path = agent_dir / output_rel
    if not output_path.is_file():
        errors.append(f"{agent_dir.name}/{case_id}: output file not found: {output_path}")
        return False

    output_text = output_path.read_text(encoding="utf-8")
    output_obj = parse_output(output_text, output_path)

    case_ok = True
    for check in case.get("checks", []):
        ok, message = run_check(check, output_text, output_obj)
        if not ok:
            errors.append(f"{agent_dir.name}/{case_id}: {message}")
            case_ok = False
    return case_ok


def evaluate_agent(agent_dir: Path, errors: list[str]) -> tuple[int, int]:
    cases_path = agent_dir / "tests" / "cases.jsonl"
    if not cases_path.is_file():
        errors.append(f"{agent_dir.name}: missing tests/cases.jsonl")
        return (0, 0)

    cases = []
    for i, line in enumerate(cases_path.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        try:
            cases.append(json.loads(line))
        except json.JSONDecodeError as e:
            errors.append(f"{cases_path}:{i}: invalid JSON ({e})")

    passed = sum(1 for c in cases if evaluate_case(agent_dir, c, errors))
    return (passed, len(cases))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--with-llm", action="store_true", help="Also call the configured LLM and validate generated output (requires litellm).")
    parser.add_argument("--agent", help="Restrict to a single agent name (directory under agents/).")
    args = parser.parse_args()

    if args.with_llm:
        print("WARNING: --with-llm not yet implemented; running offline checks only.", file=sys.stderr)

    if not AGENTS_DIR.exists():
        print("agents directory not found; no eval to run.")
        return 0

    errors: list[str] = []
    total_passed = 0
    total_cases = 0
    agent_count = 0

    for agent_dir in sorted(AGENTS_DIR.iterdir()):
        if not agent_dir.is_dir():
            continue
        if args.agent and agent_dir.name != args.agent:
            continue
        agent_count += 1
        passed, total = evaluate_agent(agent_dir, errors)
        total_passed += passed
        total_cases += total
        status = "ok" if passed == total else "fail"
        print(f"{agent_dir.name:30s} {passed}/{total} {status}")

    print()
    print(f"agents : {agent_count}")
    print(f"cases  : {total_passed}/{total_cases} passed")

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
