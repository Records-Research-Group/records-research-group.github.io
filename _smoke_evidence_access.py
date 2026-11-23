#!/usr/bin/env python3
"""Smoke test: F2/F3 reconciliation evidence access paths.

GETs each public URL and checks (a) HTTP 200 and (b) expected body
content — not just that a generic HTML page was returned. Run after
deploy to verify an outside reader can reach the workbook.

    python _smoke_evidence_access.py            # live site
    python _smoke_evidence_access.py --local    # file existence instead
"""
import sys
import urllib.request

BASE = "https://records-research-group.github.io"
UA = {"User-Agent": "rrg-evidence-smoke/1.0 (content-check)"}

# (path, expected substring in body)
CHECKS = [
    ("/data/reconciliation/owrd_fy2025/", "agency_extract_owrd_fy2025.csv"),
    ("/data/reconciliation/owrd_fy2025/", "MATCHING_RULES.md"),
    ("/data/reconciliation/owrd_fy2025/README.md", "$33,982,830.31"),
    ("/data/reconciliation/owrd_fy2025/MATCHING_RULES.md", "payee"),
    ("/data/reconciliation/owrd_fy2025/reconciliation.csv", "1316558.48"),
    ("/data/reconciliation/owrd_fy2025/agency_extract_owrd_fy2025.csv", "fiscal_year"),
    ("/data/reconciliation/owrd_fy2025/portal_extract_owrd_fy2025.csv", "WATER RESOURCES"),
    ("/data/reconciliation/owrd_fy2025/RRG_F2F3_VERIFICATION_PACKET.md", "reproduce"),
    ("/data/petition_transmissions.csv", "petition_L1_odhs_ag"),
    ("/llms.txt", "reconciliation/owrd_fy2025"),
    ("/sitemap.xml", "owrd_fy2025"),
]


def check_live():
    fails = 0
    for path, needle in CHECKS:
        url = BASE + path
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=20) as r:
                body = r.read().decode("utf-8", "replace")
                code, ctype = r.status, r.headers.get("Content-Type", "")
        except Exception as e:
            print(f"FAIL {path}  GET error: {e}")
            fails += 1
            continue
        if code != 200 or needle not in body:
            print(f"FAIL {path}  {code} {ctype}  missing {needle!r}")
            fails += 1
        else:
            print(f"ok   {path}  200 {ctype}  contains {needle!r}")
    print(f"{len(CHECKS) - fails}/{len(CHECKS)} paths ok")
    return fails


if __name__ == "__main__":
    sys.exit(1 if check_live() else 0)
