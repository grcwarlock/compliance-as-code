# Control: CC6.1 (SOC 2)

## Description

The entity implements logical access security software, infrastructure, and architectures over protected information assets to protect them from security events to meet the entity's objectives.

## Conditions for compliance

1. An identity accessing the system must be authenticated.
2. A privileged identity must have MFA enforced.
3. A role assignment must be approved via a documented workflow (approval ticket reference).
4. A service account must not carry interactive console credentials.

## Evidence record shape

```json
{
  "source": "string",
  "event_type": "iam_identity_snapshot",
  "resource_type": "identity",
  "resource_id": "string (ARN or stable identity id)",
  "collected_at": "date-time",
  "payload": {
    "identity_name": "string",
    "identity_type": "human | service",
    "authenticated": "boolean",
    "privileged": "boolean",
    "mfa_enabled": "boolean",
    "role": "string",
    "approval_ticket": "string (optional)",
    "console_password_set": "boolean"
  }
}
```
