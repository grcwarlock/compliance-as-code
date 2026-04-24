# aws-iam connector

Emits an evidence record per AWS IAM user describing console access, MFA enrollment, and access-key state.

## What it produces

One `iam_user_snapshot` evidence record per IAM user found in the account. Records carry `control_hints` for SOC 2 CC6.1, ISO 27001 A.8.5, and NIST 800-53 IA-2.

Sample shape (see `examples/output.json` for a complete example):

```json
{
  "source": "aws-iam",
  "event_type": "iam_user_snapshot",
  "resource_type": "iam_user",
  "resource_id": "arn:aws:iam::123456789012:user/jane",
  "collected_at": "2026-04-17T14:02:11Z",
  "control_hints": [
    {"framework": "soc-2", "control_id": "CC6.1"},
    {"framework": "iso-27001", "control_id": "A.8.5"},
    {"framework": "nist-800-53", "control_id": "IA-2"}
  ],
  "payload": {
    "user_name": "jane",
    "user_id": "AIDAEXAMPLE",
    "create_date": "2024-09-12T10:14:00Z",
    "console_access": true,
    "mfa_enabled": true,
    "mfa_device_count": 1,
    "access_key_count": 0
  }
}
```

## Required permissions

Read-only IAM permissions:

```text
iam:ListUsers
iam:ListMFADevices
iam:GetLoginProfile
iam:ListAccessKeys
```

Recommended: a dedicated read-only role assumed via SSO or a scoped IAM user with these permissions only. Do not run as an admin role.

## Credentials

Standard boto3 resolution — environment variables, `~/.aws/credentials`, IAM instance profile, or SSO session. Do not embed credentials in the script.

## Install and run

```bash
pip install -r requirements.txt
python connector.py --output evidence-aws.json
```

`--output` is optional; default is stdout.

## Limitations

- Single AWS account per run. Iterate externally for multi-account collection.
- Does not enumerate roles, policies, or service-linked identities. Add separate connectors for those if needed.
- No pagination tuning; relies on boto3 default page size.

## CI / repo example

`examples/output.json` is a hand-curated sample that validates against `connectors/schema/evidence.schema.json`. CI checks this on every push.
