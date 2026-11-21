#!/usr/bin/env python3
"""Offline self-test for the safe blocker record. No network, no args.
Checks GOAL.md, ARTIFACTS.md, README.md for blocker wording and
absence of exploit/payload instructions, invented URLs or hashes.
Exits 0 only when all checks pass."""
import re
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
CHECKS = PASSED = 0
def check(cond, label):
    global CHECKS, PASSED
    CHECKS += 1
    if cond:
        PASSED += 1
        print("ok: %s" % label)
    else:
        print("FAIL: %s" % label)
def read(name):
    p = HERE / name
    return p.read_text(encoding="utf-8") if p.exists() else ""
def main():
    goal = read("GOAL.md")
    art = read("ARTIFACTS.md")
    readme = read("README.md")
    check(bool(goal), "GOAL.md present")
    check(bool(art), "ARTIFACTS.md present")
    check(bool(readme), "README.md present")
    check("not present" in goal, "GOAL states original folder missing")
    check("No verified private" in goal, "GOAL states no verified private channel")
    check("no code was" in goal.lower() or "No code was" in goal, "GOAL states no external code run")
    check("safe blocker" in art.lower(), "ARTIFACTS records safe blocker")
    check("NOT claimed" in art, "ARTIFACTS claims no publication")
    check("Untested" in readme, "README marks work untested")
    banned = ["exploit", "payload", "reproduc", "attack step"]
    all_text = (goal + art + readme).lower()
    check(all(b not in all_text for b in banned), "no exploit or payload instructions in records")
    check(not re.search(r"https?://", goal + art + readme), "no invented URLs in records")
    check(not re.search(r"\b[0-9a-f]{40,}\b", all_text), "no invented long hashes in records")
    check("python3 self_test.py" in readme, "README documents offline run command")
    print("\nResults: %d/%d checks passed" % (PASSED, CHECKS))
    return 0 if PASSED == CHECKS else 1
if __name__ == "__main__":
    sys.exit(main())
