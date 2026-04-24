# Security Policy

## Reporting a vulnerability

If you discover a security issue in this repository — particularly in the validation script, install script, a connector, or an agent prompt that could be reliably coerced into producing harmful output — please report it privately rather than opening a public issue.

Email: `jasonmwilson@icloud.com`

We aim to acknowledge reports within 72 hours.

## Scope

This repo ships:

- Markdown skills and agent prompts (no executable risk on their own).
- A Python validation script (`scripts/validate.py`) that performs read-only file inspection.
- A Bash install script (`scripts/install.sh`) that creates symlinks under a user-supplied target directory.
- Optional Python connectors (read-only, least-privilege; require user-supplied credentials).

We are particularly interested in reports about:

- Path traversal or arbitrary symlink creation in `scripts/install.sh`.
- Schema-validation bypass in `scripts/validate.py`.
- Connector code paths that could leak credentials, write outside the working directory, or escalate privileges.
- Prompt patterns in agents that could be reliably steered to produce dangerous output regardless of LLM provider.

## Out of scope

- Bugs in third-party LLM providers.
- Bugs in third-party agent runtimes that consume these skills.
- Generic "AI can be jailbroken" reports without a specific reproducible failure in this repo.
- Vulnerabilities in user-installed dependencies (report upstream).

## Disclosure

After a fix is merged and released, we will credit the reporter in the changelog unless they prefer otherwise.
