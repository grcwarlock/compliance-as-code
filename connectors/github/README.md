# github connector

Emits evidence records describing GitHub branch-protection rules for repositories in an organisation, plus the org's admin membership.

## What it produces

Two record types per run:

1. `branch_protection_rule` (one per default-branch protection rule per repo)
2. `org_admin_snapshot` (one per organisation admin)

Records carry `control_hints` for SOC 2 CC6.1 / CC8.1, ISO 27001 A.8.4 / A.8.32, and NIST 800-53 AC-3 / CM-3.

See `examples/output.json` for a full sample.

## Required scopes

Personal access token (classic) or fine-grained token with read-only access:

- `read:org` — read organisation membership
- `repo` (read-only) — read repository settings and branch protection

For fine-grained tokens, restrict by repository allow-list and grant only the *Read* permissions for `Administration` and `Metadata`.

Recommended: use a service account with a token rotated every 90 days, or use a GitHub App with installation tokens.

## Credentials

Two environment variables:

- `GITHUB_TOKEN` — read-only token as above
- `GITHUB_ORG` — the organisation slug to enumerate

The token is read once and never logged.

## Install and run

```bash
pip install -r requirements.txt
GITHUB_TOKEN=ghp_... GITHUB_ORG=my-org python connector.py --output evidence-github.json
```

`--output` is optional; default is stdout.

## Limitations

- Single org per run.
- Default branches only. Add a flag if you need protection on other branches.
- Does not enumerate per-repo collaborators (use the GitHub audit log for that).
