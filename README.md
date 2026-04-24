# compliance-as-code

> Open-source agent skills, agents, and reference connectors for compliance engineers. SOC 2, ISO 27001, NIST 800-53 — written for the people instrumenting the systems, not the people writing the report.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Frameworks](https://img.shields.io/badge/frameworks-3-0A1F44)](#whats-inside)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

## Why this exists

Most compliance content is written for auditors. It tells you what an auditor expects to see, what evidence to collect, what the control IDs mean. That is useful — once a year.

The other 364 days, someone has to actually instrument the systems, write the policies, emit the artifacts, and keep it all running. That is an engineering job, and engineering jobs need engineering tools.

This repo is a small kit for that job:

- **Skills** that brief any compatible agent runtime on a framework from an engineer's perspective — event types, evidence shapes, what a continuous control looks like, how to design for "no quarterly screenshot."
- **Agents** that produce concrete artifacts: Rego policies, OSCAL JSON, PCAOB severity classifications. Pure input → output. No databases, no daemons, no cloud credentials at runtime.
- **Optional connectors** that emit evidence records from real systems (AWS IAM, GitHub, Okta) using a shared JSON schema. Skills and agents work without these; they are reference implementations, not a platform.

Vendor-neutral, MIT-licensed, model-agnostic, runtime-agnostic.

## What's inside

### Skills

| Skill | Activates on | SKILL.md |
|---|---|---|
| `soc-2` | SOC 2 TSC implementation, evidence-as-code, continuous controls, instrumenting for audit | [view](skills/soc-2/SKILL.md) |
| `iso-27001` | ISMS, Annex A engineering view, risk register schemas, evidence pipelines | [view](skills/iso-27001/SKILL.md) |
| `nist-800-53` | Control families, baselines and tailoring, control inheritance, OSCAL emission | [view](skills/nist-800-53/SKILL.md) |

### Agents

| Agent | Input → Output | AGENT.md |
|---|---|---|
| `opa-policy-author` | Control description + evidence shape → Rego policy with deny rules | [view](agents/opa-policy-author/AGENT.md) |
| `oscal-emitter` | Assessment notes (markdown) → OSCAL Assessment Results JSON | [view](agents/oscal-emitter/AGENT.md) |
| `poam-classifier` | Deficiency description + context → PCAOB severity (deficiency / SD / MW) with reasoning | [view](agents/poam-classifier/AGENT.md) |

### Optional connectors

| Connector | Emits | README |
|---|---|---|
| `aws-iam` | IAM user snapshots with MFA / console / access-key state | [view](connectors/aws-iam/README.md) |
| `github` | Branch protection rules, org admin membership | [view](connectors/github/README.md) |
| `okta` | User MFA factors, privileged group membership | [view](connectors/okta/README.md) |

Each connector is a single Python script that emits records conforming to [`connectors/schema/evidence.schema.json`](connectors/schema/evidence.schema.json). Anyone can write one. Three reference implementations ship with the repo.

## Install

### Skills

```bash
git clone https://github.com/<your-handle>/compliance-as-code.git
cd compliance-as-code
./scripts/install.sh --target /path/to/your/agent/skills/dir
```

The script symlinks each skill (and each agent, when present) into the target directory. Set `--target` to wherever your agent runtime expects to discover skills. Use `--dry-run` to preview, `--force` to overwrite existing symlinks.

To copy one skill manually instead:

```bash
cp -r skills/soc-2 /path/to/your/agent/skills/dir/soc-2
```

After install, restart your agent runtime so it picks up the new skills.

### Agents

Same install pattern as skills (the install script symlinks `agents/<name>/` into your `--target` directory). Outside an agent runtime, use the provider-neutral runner:

```bash
pip install -r scripts/requirements-runner.txt
LLM_PROVIDER=openai LLM_MODEL=gpt-4o \
  python scripts/run-agent.py oscal-emitter \
    --input agents/oscal-emitter/examples/input-assessment-notes.md \
    --output assessment-results.json
```

### Connectors

Standalone Python scripts.

```bash
pip install -r connectors/aws-iam/requirements.txt
python connectors/aws-iam/connector.py --output evidence-aws.json
```

Connectors are optional. Skills and agents work without any connector installed. Each connector's README documents its required scopes / IAM minimums.

## Usage

### In an agent runtime

Each skill declares a trigger in its frontmatter `description`. A compatible runtime loads the skill when your prompt matches.

```text
What evidence does an auditor expect for SOC 2 CC6.1, and how would I make it continuous?
```

```text
Walk me through scoping ISO 27001 Annex A controls for a 50-person SaaS that already has SOC 2.
```

```text
Map our AWS IAM controls to NIST SP 800-53 Rev. 5 AC family at the moderate baseline.
```

When a skill is active, the runtime cites specific control IDs, pulls in templates from the skill's `references/` folder on demand, and flags anything that requires a licensed auditor or lawyer.

### Model-agnostic

Skills are pure markdown. They work in any agent runtime that understands the agent skills frontmatter format described in [How agent skills work](#how-agent-skills-work).

Agents (when shipped) ship as the same markdown plus a small Python runner that uses [LiteLLM](https://github.com/BerriAI/litellm) for provider abstraction:

```bash
LLM_PROVIDER=openai LLM_MODEL=gpt-4o            python scripts/run-agent.py oscal-emitter --input notes.md
LLM_PROVIDER=ollama LLM_MODEL=llama3            python scripts/run-agent.py opa-policy-author --control cc6-1.md
LLM_PROVIDER=gemini LLM_MODEL=gemini-2.0-flash  python scripts/run-agent.py poam-classifier --input deficiency.md
```

No specific provider's API key is required to use this repo. Use whatever model you have credentials for, or run local with Ollama.

## How agent skills work

A skill is a directory containing a `SKILL.md` file with YAML frontmatter — at minimum `name`, `description`, and `when_to_use`. Compatible agent runtimes auto-discover skills in a configured directory and activate them when conversation matches the description. The `SKILL.md` stays short; longer reference material (control lists, templates, checklists) lives in `references/` and gets loaded on demand.

```text
skills/soc-2/
  SKILL.md              # frontmatter + short body, links to references
  examples/example.md
  references/
    trust-services-criteria-engineer-view.md
    evidence-as-code-patterns.md
    continuous-monitoring-patterns.md
    type-1-vs-type-2-for-engineers.md
```

Agents follow the same shape (`AGENT.md` instead of `SKILL.md`, plus a `prompt.md`). This file format is vendor-neutral; any agent runtime that respects the frontmatter contract can load these skills.

## Contributing

PRs welcome — new frameworks, improved references, better agents, more connectors, bug fixes. Before opening a PR:

1. Read [CONTRIBUTING.md](CONTRIBUTING.md) for the authoring style guide.
2. Run `python scripts/validate.py` to catch frontmatter, link, and schema errors.
3. Use the issue templates if you want a new framework, agent, or connector before building it.

## Roadmap

- **v0.1 (current)** — Three skills (SOC 2, ISO 27001, NIST 800-53) with full reference docs. Three agents (`opa-policy-author`, `oscal-emitter`, `poam-classifier`) with offline eval harness. Three reference connectors (AWS IAM, GitHub, Okta).
- **v0.2** — Additional frameworks (PCI DSS, HIPAA, GDPR, EU AI Act). Additional connectors (GCP, Azure, Snowflake). End-to-end integration examples piping connector output into agents. `--with-llm` mode in the eval harness.
- **v0.3** — Cross-framework crosswalk skill. Real eval benchmark numbers for agent output quality across providers.

## License

MIT &copy; 2026. See [LICENSE](LICENSE).

Community contributions are licensed under MIT by their authors.

## Acknowledgements

Built on the public work of NIST, ISO/IEC, AICPA, the Open Policy Agent project, and the OSCAL working group.
