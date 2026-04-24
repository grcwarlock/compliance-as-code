#!/usr/bin/env python3
"""AWS IAM connector — emits an evidence record per IAM user.

Usage:
    python connector.py [--output PATH]

Credentials resolved via standard boto3 chain (env vars, ~/.aws/credentials,
IAM role). No credentials are embedded.

Required IAM permissions (read-only):
    iam:ListUsers
    iam:ListMFADevices
    iam:GetLoginProfile
    iam:ListAccessKeys
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone

try:
    import boto3
    from botocore.exceptions import ClientError
except ImportError:
    print("ERROR: boto3 is required. pip install -r requirements.txt", file=sys.stderr)
    sys.exit(2)


SOURCE = "aws-iam"
CONTROL_HINTS = [
    {"framework": "soc-2", "control_id": "CC6.1"},
    {"framework": "iso-27001", "control_id": "A.8.5"},
    {"framework": "nist-800-53", "control_id": "IA-2"},
]


def has_console_access(client, user_name: str) -> bool:
    try:
        client.get_login_profile(UserName=user_name)
        return True
    except ClientError as e:
        if e.response["Error"]["Code"] == "NoSuchEntity":
            return False
        raise


def collect(client) -> list[dict]:
    records: list[dict] = []
    collected_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    paginator = client.get_paginator("list_users")
    for page in paginator.paginate():
        for user in page["Users"]:
            user_name = user["UserName"]
            mfa_devices = client.list_mfa_devices(UserName=user_name)["MFADevices"]
            access_keys = client.list_access_keys(UserName=user_name)["AccessKeyMetadata"]

            records.append(
                {
                    "source": SOURCE,
                    "event_type": "iam_user_snapshot",
                    "resource_type": "iam_user",
                    "resource_id": user["Arn"],
                    "collected_at": collected_at,
                    "control_hints": CONTROL_HINTS,
                    "payload": {
                        "user_name": user_name,
                        "user_id": user["UserId"],
                        "create_date": user["CreateDate"].isoformat().replace("+00:00", "Z"),
                        "console_access": has_console_access(client, user_name),
                        "mfa_enabled": len(mfa_devices) > 0,
                        "mfa_device_count": len(mfa_devices),
                        "access_key_count": len(access_keys),
                    },
                }
            )
    return records


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--output", "-o", help="Output file (default: stdout)")
    args = parser.parse_args()

    client = boto3.client("iam")
    try:
        records = collect(client)
    except ClientError as e:
        print(f"ERROR: AWS API call failed: {e}", file=sys.stderr)
        return 1

    payload = json.dumps(records, indent=2, default=str)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(payload)
        print(f"wrote {len(records)} record(s) to {args.output}", file=sys.stderr)
    else:
        print(payload)
    return 0


if __name__ == "__main__":
    sys.exit(main())
