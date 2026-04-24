# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Three agents with prompt, references, examples, and offline eval cases:
  - `opa-policy-author` — control description + evidence shape → Rego policy with deny rules.
  - `oscal-emitter` — assessment notes (markdown) → OSCAL Assessment Results JSON with deterministic UUID5.
  - `poam-classifier` — deficiency description → PCAOB AS 2201 severity classification with reasoning.
- `scripts/run-agent.py` — provider-neutral CLI runner using LiteLLM. Reads `LLM_PROVIDER` and `LLM_MODEL` from the environment; works with every provider LiteLLM supports (OpenAI, Ollama, Gemini, Mistral, Bedrock, Azure OpenAI, Vertex AI, Groq, Cohere, and more).
- `scripts/eval.py` — offline agent evaluator. Reads each agent's `tests/cases.jsonl` and applies structural checks (JSON validity, regex matches, JSON-path presence, enum membership, array length) to the shipped example outputs. CI-friendly; no LLM call required.
- `scripts/requirements-runner.txt` — runtime dependency for the agent runner (LiteLLM only).
- Three reference connectors, each a single Python script:
  - `connectors/aws-iam` — IAM user snapshots with MFA / console / access-key state (boto3).
  - `connectors/github` — branch protection rules and org admin membership (PyGithub).
  - `connectors/okta` — user MFA factors and privileged group membership (requests).
- `connectors/README.md` documenting the connector contract and discipline rules.
- Initial repository skeleton.
- `SKILL.md` shells for `soc-2`, `iso-27001`, and `nist-800-53` with engineer-voice positioning.
- Full reference library for each skill (4 topic docs per framework):
  - SOC 2: Trust Services Criteria engineer's view, evidence-as-code patterns, continuous monitoring patterns, Type 1 vs Type 2 for engineers.
  - ISO 27001: Annex A engineer's view, ISMS-as-code, risk register schema, evidence pipeline design.
  - NIST 800-53: control families overview, baselines and tailoring, control inheritance, OSCAL emission patterns.
- One end-to-end walkthrough (`examples/example.md`) per skill.
- Evidence record JSON Schema (`connectors/schema/evidence.schema.json`) defining the contract for optional connectors.
- Validation script (`scripts/validate.py`) covering frontmatter, internal links, JSON Schema parse, and connector example conformance.
- Install script (`scripts/install.sh`) that symlinks skills (and agents, when present) into a user-supplied target directory (`--target <path>`), so it does not assume any specific agent runtime.
- CI workflow running validation, markdownlint, and shellcheck on every push and PR.
- Contributor docs: `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, issue and PR templates.
