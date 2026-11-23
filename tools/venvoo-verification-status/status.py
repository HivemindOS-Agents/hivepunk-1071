#!/usr/bin/env python3
"""Offline verification-blocker status for venvoo-missing-dates.

Reads a JSON state file naming whether each verification item
was actually done, and reports WAIT unless every item is true.
It never infers push, fetch, hash, or runner success: a missing
or false field is a blocker. No network, no external systems.
"""
import json
import sys
from pathlib import Path

REQUIRED = [
    "current_commit_runner_passed",
    "push_via_authorized_api_done",
    "public_files_fetch_checked",
    "goal_md_sha256_logged",
]

def evaluate(state):
    if not isinstance(state, dict):
        raise ValueError("state must be a JSON object")
    blockers = []
    for key in REQUIRED:
        if state.get(key) is not True:
            blockers.append(key)
    detail = state.get("detail") if isinstance(state.get("detail"), dict) else {}
    return {
        "verdict": "READY" if not blockers else "WAIT",
        "blockers": blockers,
        "required": list(REQUIRED),
        "detail": detail,
        "note": "READY only when every required item is explicitly true; otherwise WAIT. No push, fetch, hash, or run is claimed by this tool.",
    }

def main(argv):
    if len(argv) < 2 or argv[1] in ("-h", "--help"):
        print("usage: python3 status.py STATE.json [--out FILE]")
        print("STATE.json keys: " + ", ".join(REQUIRED) + ", detail {}")
        return 0 if len(argv) >= 2 else 2
    try:
        state = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
        result = evaluate(state)
    except (ValueError, OSError) as exc:
        print("error: %s" % exc)
        return 2
    out = None
    i = 2
    while i < len(argv):
        if argv[i] == "--out" and i + 1 < len(argv):
            out = argv[i + 1]; i += 2
        else:
            print("unknown argument: %s" % argv[i]); return 2
    text = json.dumps(result, indent=2, sort_keys=True)
    if out:
        Path(out).write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
