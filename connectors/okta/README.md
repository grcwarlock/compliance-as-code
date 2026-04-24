# okta connector

Emits evidence records describing Okta user MFA enrollment and privileged group membership.

## What it produces

Two record types per run:

1. `okta_user_mfa` (one per active user)
2. `okta_privileged_group_membership` (one per member per privileged group)

Records carry `control_hints` for SOC 2 CC6.1 / CC6.2, ISO 27001 A.8.5 / A.5.18, and NIST 800-53 IA-2 / AC-6.

See `examples/output.json` for a full sample.

## Required scopes

Okta API token created from a service account with these admin role scopes (read-only):

- Read-only Administrator (or a custom role limited to: Users — Read; Groups — Read)

Recommended: rotate the token every 90 days; do not reuse human admin tokens.

## Configuration

Two environment variables:

- `OKTA_DOMAIN` — your tenant, e.g. `example.okta.com`
- `OKTA_TOKEN` — the read-only API token
- `OKTA_PRIVILEGED_GROUPS` — comma-separated list of group names that are considered privileged (e.g., `engineering-admins,it-superusers`)

## Install and run

```bash
pip install -r requirements.txt
OKTA_DOMAIN=example.okta.com OKTA_TOKEN=00... OKTA_PRIVILEGED_GROUPS=engineering-admins \
  python connector.py --output evidence-okta.json
```

`--output` is optional; default is stdout.

## Limitations

- Reads up to 200 users per page (Okta default). Large tenants will paginate; the connector handles this transparently but may take time on tens of thousands of users.
- Group privilege classification is by name (configured), not by Okta admin role assignments. Augment if your privilege model is more nuanced.
- Does not enumerate factors used in recent authentications — that requires the System Log API; out of scope here.
