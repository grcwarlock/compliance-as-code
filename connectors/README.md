# Connectors (optional)

Reference implementations of evidence connectors. **Skills and agents in this repo work without any connector installed** — these exist to show how to feed real-system evidence into agents and to provide a starting point for your own connectors.

## What a connector does

Reads from a source system, emits one or more evidence records as JSON to stdout (or a file). Records must conform to [`schema/evidence.schema.json`](schema/evidence.schema.json).

## Hard rules every connector follows

1. **One file.** Standard library plus one SDK only.
2. **Output to stdout or `--output <file>`.** No daemons, no scheduler, no persistent state.
3. **Read-only and least-privilege.** The connector's README states the exact scopes / IAM minimums required.
4. **Credentials from environment or standard SDK resolution.** No bundled secrets, no config files in the repo.
5. **Optional `control_hints`** in each record. Mappers downstream make the authoritative call.

## Reference connectors

| Connector | Source | Emits |
|---|---|---|
| [`aws-iam`](aws-iam/) | AWS IAM (boto3) | IAM user snapshots with MFA, console access, key state |
| [`github`](github/) | GitHub REST API | Repository branch protection rules, org admin membership |
| [`okta`](okta/) | Okta API | User MFA factors, privileged group membership |

## Using connector output with an agent

```bash
# Collect evidence
python connectors/aws-iam/connector.py --output evidence-aws.json

# Pipe individual record into a policy-author agent
python scripts/run-agent.py opa-policy-author \
  --input some-control-description.md \
  --output policy.rego

# Evaluate the policy against collected evidence
opa eval -d policy.rego -i evidence-aws.json "data.compliance"
```

## Writing your own connector

Use one of the reference implementations as a template. Stay within the hard rules above. Open a PR with a new directory under `connectors/<source>/` containing:

- `README.md` describing what it does and what scopes it needs
- `connector.py` (single file)
- `requirements.txt`
- `examples/output.json` — sample output that validates against the schema (CI checks this)

The repo will not accept connector frameworks, plugin systems, or shared base classes. Each connector is independent on purpose.
