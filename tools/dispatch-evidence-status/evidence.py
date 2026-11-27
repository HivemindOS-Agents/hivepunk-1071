#!/usr/bin/env python3
"""Offline evidence-status ledger for the GitHub inspection step.

No network, no arguments beyond an input JSON. It never fetches
anything: it records what was observed, marks what was not observed
as UNKNOWN or ACCESS-BLOCKED, and reports test-pending unless every
required field carries verbatim evidence, GOAL.md was updated first,
and no field claims a publish/upload/post.
"""
import json
import sys
from pathlib import Path

ACCESS_BLOCKED = "ACCESS_BLOCKED"
CONFIRMED = "CONFIRMED"
UNKNOWN = "UNKNOWN"
BLOCKED = "ACCESS-BLOCKED"
PENDING = "test-pending"
DONE = "all-confirmed"

REQUIRED_GOAL = ["goal_md_first", "tested_revision",
                 "self_test_command", "runner_output"]
REQUIRED_ARTIFACTS = ["artifacts_evidence", "artifact_url_fetch_check"]
ALL_FIELDS = REQUIRED_GOAL + REQUIRED_ARTIFACTS
CLAIM_WORDS = ("published", "uploaded", "posted", "deployed")

USAGE = ("usage: python3 evidence.py INPUT.json [--out FILE]\n"
         "INPUT.json: {goal_md_updated_first, observed{field: text|"
         + ACCESS_BLOCKED + "|null}}\n"
         "fields: " + ", ".join(ALL_FIELDS))


def norm(text):
    return " ".join(str(text).strip().lower().split())


def field_row(field, owner, observed):
    raw = observed.get(field)
    if raw == ACCESS_BLOCKED:
        return {"field": field, "owner": owner, "status": BLOCKED,
                "evidence": None}
    if raw is None or (isinstance(raw, str) and not raw.strip()):
        return {"field": field, "owner": owner, "status": UNKNOWN,
                "evidence": None}
    return {"field": field, "owner": owner, "status": CONFIRMED,
            "evidence": str(raw)}


def flagged_claims(rows):
    """Fields whose recorded text claims something was published outside."""
    out = []
    for row in rows:
        text = (row.get("evidence") or "").lower()
        if any(word in text for word in CLAIM_WORDS):
            out.append(row["field"])
    return out


def evaluate(payload):
    observed = payload.get("observed") or {}
    rows = [field_row(f, "GOAL.md", observed) for f in REQUIRED_GOAL]
    rows += [field_row(f, "ARTIFACTS.md", observed) for f in REQUIRED_ARTIFACTS]
    order_ok = bool(payload.get("goal_md_updated_first"))
    claims = flagged_claims(rows)
    confirmed = [row for row in rows if row["status"] == CONFIRMED]
    missing = [row["field"] for row in rows if row["status"] != CONFIRMED]
    complete = order_ok and not missing and not claims
    status = DONE if complete else PENDING
    summary = ("%d/%d evidence fields confirmed; GOAL.md updated first: %s; "
               "flagged publish claims: %s; missing or blocked: %s; "
               "status: %s"
               % (len(confirmed), len(rows), str(order_ok).lower(),
                  ", ".join(claims) or "none",
                  ", ".join(missing) or "none", status))
    return {"status": status, "order_ok": order_ok,
            "confirmed": len(confirmed), "total": len(rows),
            "missing": missing, "flagged_claims": claims,
            "fields": rows, "summary": summary}


def main(argv):
    if len(argv) < 2:
        print(USAGE)
        return 2
    path = argv[1]
    out = None
    if "--out" in argv:
        i = argv.index("--out")
        if i + 1 >= len(argv):
            print(USAGE)
            return 2
        out = argv[i + 1]
    try:
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print("error: %s" % exc)
        return 1
    if not isinstance(payload, dict):
        print("error: input must be a JSON object")
        return 1
    text = json.dumps(evaluate(payload), indent=2, sort_keys=True) + "\n"
    if out:
        Path(out).write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
