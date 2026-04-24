#!/usr/bin/env python3
"""GitHub connector — emits branch-protection and org-admin evidence records.

Usage:
    GITHUB_TOKEN=<token> GITHUB_ORG=<org> python connector.py [--output PATH]

Required token scopes (read-only):
    read:org
    repo (read)
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone

try:
    from github import Github, GithubException
except ImportError:
    print("ERROR: PyGithub is required. pip install -r requirements.txt", file=sys.stderr)
    sys.exit(2)


SOURCE = "github"
PROTECTION_HINTS = [
    {"framework": "soc-2", "control_id": "CC8.1"},
    {"framework": "iso-27001", "control_id": "A.8.32"},
    {"framework": "nist-800-53", "control_id": "CM-3"},
]
ADMIN_HINTS = [
    {"framework": "soc-2", "control_id": "CC6.1"},
    {"framework": "iso-27001", "control_id": "A.8.2"},
    {"framework": "nist-800-53", "control_id": "AC-6"},
]


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def collect_branch_protection(client: Github, org_name: str, collected_at: str) -> list[dict]:
    records: list[dict] = []
    org = client.get_organization(org_name)
    for repo in org.get_repos():
        try:
            default_branch = repo.get_branch(repo.default_branch)
            try:
                protection = default_branch.get_protection()
                req_status = protection.required_status_checks
                req_reviews = protection.required_pull_request_reviews
                payload = {
                    "repo_full_name": repo.full_name,
                    "default_branch": repo.default_branch,
                    "protection_enabled": True,
                    "required_status_checks": [c for c in req_status.contexts] if req_status else [],
                    "required_review_count": req_reviews.required_approving_review_count if req_reviews else 0,
                    "dismiss_stale_reviews": getattr(req_reviews, "dismiss_stale_reviews", False),
                    "enforce_admins": protection.enforce_admins,
                }
            except GithubException as e:
                if e.status == 404:
                    payload = {
                        "repo_full_name": repo.full_name,
                        "default_branch": repo.default_branch,
                        "protection_enabled": False,
                    }
                else:
                    raise
        except GithubException as e:
            print(f"WARN: skipping {repo.full_name}: {e}", file=sys.stderr)
            continue

        records.append(
            {
                "source": SOURCE,
                "event_type": "branch_protection_rule",
                "resource_type": "repository",
                "resource_id": f"github://{repo.full_name}",
                "collected_at": collected_at,
                "control_hints": PROTECTION_HINTS,
                "payload": payload,
            }
        )
    return records


def collect_org_admins(client: Github, org_name: str, collected_at: str) -> list[dict]:
    records: list[dict] = []
    org = client.get_organization(org_name)
    for member in org.get_members(role="admin"):
        records.append(
            {
                "source": SOURCE,
                "event_type": "org_admin_snapshot",
                "resource_type": "user",
                "resource_id": f"github://{org_name}/{member.login}",
                "collected_at": collected_at,
                "control_hints": ADMIN_HINTS,
                "payload": {
                    "org": org_name,
                    "login": member.login,
                    "user_id": member.id,
                    "two_factor_authentication": getattr(member, "two_factor_authentication", None),
                },
            }
        )
    return records


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--output", "-o", help="Output file (default: stdout)")
    args = parser.parse_args()

    token = os.environ.get("GITHUB_TOKEN", "").strip()
    org_name = os.environ.get("GITHUB_ORG", "").strip()
    if not token or not org_name:
        print("ERROR: GITHUB_TOKEN and GITHUB_ORG environment variables are required.", file=sys.stderr)
        return 2

    client = Github(token)
    collected_at = now_iso()
    try:
        records = collect_branch_protection(client, org_name, collected_at)
        records.extend(collect_org_admins(client, org_name, collected_at))
    except GithubException as e:
        print(f"ERROR: GitHub API call failed: {e}", file=sys.stderr)
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
