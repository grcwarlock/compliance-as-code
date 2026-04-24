#!/usr/bin/env python3
"""Run an agent against any LLM provider supported by LiteLLM.

Usage:
    LLM_PROVIDER=openai LLM_MODEL=gpt-4o \\
        python scripts/run-agent.py <agent-name> --input <path> [--output <path>]

The agent is loaded from `agents/<agent-name>/`:
- `prompt.md` becomes the system prompt.
- `--input <path>` becomes the user message body.

Provider selection is via environment variables, parsed by LiteLLM:
- `LLM_PROVIDER` — any provider name LiteLLM recognises (openai, ollama,
  gemini, mistral, bedrock, vertex_ai, groq, cohere, and many others).
- `LLM_MODEL` — provider-specific model identifier.
- Provider-specific API keys via the conventional environment variable
  for that provider (e.g., `OPENAI_API_KEY`, `GEMINI_API_KEY`,
  `OLLAMA_API_BASE`).

This script does not assume any single provider. Install LiteLLM via:

    pip install -r scripts/requirements-runner.txt
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
AGENTS_DIR = REPO_ROOT / "agents"


def load_agent(name: str) -> tuple[Path, str]:
    """Return (agent_dir, system_prompt) for the named agent."""
    agent_dir = AGENTS_DIR / name
    if not agent_dir.is_dir():
        raise FileNotFoundError(f"Agent not found: {agent_dir}")
    prompt_path = agent_dir / "prompt.md"
    if not prompt_path.is_file():
        raise FileNotFoundError(f"Missing prompt.md for agent: {agent_dir}")
    return agent_dir, prompt_path.read_text(encoding="utf-8")


def call_litellm(system_prompt: str, user_message: str) -> str:
    try:
        from litellm import completion  # type: ignore[import-not-found]
    except ImportError:
        print(
            "ERROR: litellm is required to run agents.\n"
            "Install with: pip install -r scripts/requirements-runner.txt",
            file=sys.stderr,
        )
        sys.exit(2)

    provider = os.environ.get("LLM_PROVIDER", "").strip()
    model = os.environ.get("LLM_MODEL", "").strip()

    if not provider or not model:
        print(
            "ERROR: LLM_PROVIDER and LLM_MODEL environment variables are required.\n"
            "Examples:\n"
            "  LLM_PROVIDER=openai  LLM_MODEL=gpt-4o\n"
            "  LLM_PROVIDER=ollama  LLM_MODEL=llama3\n"
            "  LLM_PROVIDER=gemini  LLM_MODEL=gemini-2.0-flash",
            file=sys.stderr,
        )
        sys.exit(2)

    # LiteLLM uses a "provider/model" naming convention; some providers omit the prefix.
    model_id = model if "/" in model or provider == "openai" else f"{provider}/{model}"

    try:
        response = completion(
            model=model_id,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            temperature=0,
        )
    except Exception as e:  # noqa: BLE001 - surface provider errors to the user
        print(f"ERROR: provider call failed: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        return response["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as e:
        print(f"ERROR: unexpected response shape: {e}", file=sys.stderr)
        sys.exit(1)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("agent", help="Agent name (directory under agents/)")
    parser.add_argument("--input", "-i", required=True, help="Input file (markdown / JSON)")
    parser.add_argument("--output", "-o", help="Output file (default: stdout)")
    args = parser.parse_args()

    try:
        _, system_prompt = load_agent(args.agent)
    except FileNotFoundError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2

    input_path = Path(args.input)
    if not input_path.is_file():
        print(f"ERROR: input file not found: {input_path}", file=sys.stderr)
        return 2
    user_message = input_path.read_text(encoding="utf-8")

    output = call_litellm(system_prompt, user_message)

    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"wrote {len(output)} bytes to {args.output}", file=sys.stderr)
    else:
        sys.stdout.write(output)
        if not output.endswith("\n"):
            sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
