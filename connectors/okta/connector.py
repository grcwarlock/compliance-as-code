#!/usr/bin/env python3
"""Okta connector — emits user MFA and privileged-group membership records.

Usage:
    OKTA_DOMAIN=<tenant>.okta.com OKTA_TOKEN=<token> \\
    OKTA_PRIVILEGED_GROUPS=group-a,group-b \\
        python connector.py [--output PATH]
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from urllib.parse import urlencode

try:
    import requests
except ImportError:
    print("ERROR: requests is required. pip install -r requirements.txt", file=sys.stderr)
    sys.exit(2)


SOURCE = "okta"
USER_MFA_HINTS = [
    {"framework": "soc-2", "control_id": "CC6.1"},
    {"framework": "iso-27001", "control_id": "A.8.5"},
    {"framework": "nist-800-53", "control_id": "IA-2"},
]
PRIV_HINTS = [
    {"framework": "soc-2", "control_id": "CC6.2"},
    {"framework": "iso-27001", "control_id": "A.5.18"},
    {"framework": "nist-800-53", "control_id": "AC-6"},
]


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def get_paginated(session: requests.Session, url: str) -> list[dict]:
    items: list[dict] = []
    while url:
        resp = session.get(url, timeout=30)
        resp.raise_for_status()
        items.extend(resp.json())
        url = parse_link_next(resp.headers.get("Link", ""))
    return items


def parse_link_next(header: str) -> str:
    """Parse Okta's RFC 5988 Link header for the next URL."""
    for part in header.split(","):
        segs = part.strip().split(";")
        if len(segs) < 2:
            continue
        url = segs[0].strip().strip("<>")
        rel = segs[1].strip()
        if rel == 'rel="next"':
            return url
    return ""


def collect_user_mfa(session: requests.Session, base_url: str, collected_at: str) -> list[dict]:
    records: list[dict] = []
    users = get_paginated(session, f"{base_url}/api/v1/users?{urlencode({'filter': 'status eq \"ACTIVE\"', 'limit': 200})}")
    for user in users:
        user_id = user["id"]
        factors_resp = session.get(f"{base_url}/api/v1/users/{user_id}/factors", timeout=30)
        factors_resp.raise_for_status()
        factors = factors_resp.json()
        active_factors = [f for f in factors if f.get("status") == "ACTIVE"]

        records.append(
            {
                "source": SOURCE,
                "event_type": "okta_user_mfa",
                "resource_type": "user",
                "resource_id": f"okta://{user_id}",
                "collected_at": collected_at,
                "control_hints": USER_MFA_HINTS,
                "payload": {
                    "user_id": user_id,
                    "login": user["profile"].get("login"),
                    "status": user.get("status"),
                    "mfa_factor_count": len(active_factors),
                    "mfa_factor_types": sorted({f.get("factorType") for f in active_factors}),
                    "mfa_provider_types": sorted({f.get("provider") for f in active_factors}),
                },
            }
        )
    return records


def collect_privileged_membership(
    session: requests.Session, base_url: str, group_names: list[str], collected_at: str
) -> list[dict]:
    records: list[dict] = []
    for group_name in group_names:
        q = urlencode({"q": group_name})
        groups = get_paginated(session, f"{base_url}/api/v1/groups?{q}")
        match = next((g for g in groups if g.get("profile", {}).get("name") == group_name), None)
        if not match:
            print(f"WARN: privileged group not found: {group_name}", file=sys.stderr)
            continue
        members = get_paginated(session, f"{base_url}/api/v1/groups/{match['id']}/users?limit=200")
        for member in members:
            records.append(
                {
                    "source": SOURCE,
                    "event_type": "okta_privileged_group_membership",
                    "resource_type": "group_membership",
                    "resource_id": f"okta://group/{match['id']}/user/{member['id']}",
                    "collected_at": collected_at,
                    "control_hints": PRIV_HINTS,
                    "payload": {
                        "group_id": match["id"],
                        "group_name": group_name,
                        "user_id": member["id"],
                        "login": member["profile"].get("login"),
                        "status": member.get("status"),
                    },
                }
            )
    return records


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--output", "-o", help="Output file (default: stdout)")
    args = parser.parse_args()

    domain = os.environ.get("OKTA_DOMAIN", "").strip()
    token = os.environ.get("OKTA_TOKEN", "").strip()
    privileged_groups = [g.strip() for g in os.environ.get("OKTA_PRIVILEGED_GROUPS", "").split(",") if g.strip()]

    if not domain or not token:
        print("ERROR: OKTA_DOMAIN and OKTA_TOKEN environment variables are required.", file=sys.stderr)
        return 2

    base_url = f"https://{domain}"
    session = requests.Session()
    session.headers.update(
        {
            "Authorization": f"SSWS {token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
    )

    collected_at = now_iso()
    try:
        records = collect_user_mfa(session, base_url, collected_at)
        if privileged_groups:
            records.extend(collect_privileged_membership(session, base_url, privileged_groups, collected_at))
    except requests.HTTPError as e:
        print(f"ERROR: Okta API call failed: {e}", file=sys.stderr)
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
