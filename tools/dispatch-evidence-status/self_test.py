#!/usr/bin/env python3
"""Offline self-test for evidence.py: no arguments, no network.

Runs the tool's own code on its sample data plus inline cases and
compares results with what should come out. Exits 0 only when every
check passes.
"""
import json
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import evidence as e

CHECKS = 0
PASSED = 0


def check(cond, label):
    global CHECKS, PASSED
    CHECKS += 1
    if cond:
        PASSED += 1
        print("ok: %s" % label)
    else:
        print("FAIL: %s" % label)


def read_sample():
    return json.loads((HERE / "sample_input.json").read_text(encoding="utf-8"))


def full_payload(extra=None):
    observed = {f: "verbatim %s evidence" % f
                for f in e.REQUIRED_GOAL + e.REQUIRED_ARTIFACTS}
    if extra:
        observed.update(extra)
    return {"goal_md_updated_first": True, "observed": observed}


def main():
    check(e.norm("  A   B ") == "a b", "norm collapses and lowercases")

    sample = read_sample()
    r = e.evaluate(sample)
    check(r["total"] == 6, "six required evidence fields")
    check(r["confirmed"] == 1, "sample confirms exactly one field")
    check(r["order_ok"] is False, "sample does not claim GOAL.md first")
    check(r["status"] == e.PENDING, "sample is test-pending")
    check(r["flagged_claims"] == [], "sample has no publish claim")
    by_field = {row["field"]: row for row in r["fields"]}
    check(by_field["self_test_command"]["status"] == e.CONFIRMED,
          "recorded command is CONFIRMED")
    check(by_field["self_test_command"]["owner"] == "GOAL.md",
          "goal field is owned by GOAL.md")
    check(by_field["artifact_url_fetch_check"]["owner"] == "ARTIFACTS.md",
          "artifact field is owned by ARTIFACTS.md")
    check(by_field["goal_md_first"]["status"] == e.UNKNOWN,
          "null field is UNKNOWN")
    check(by_field["runner_output"]["status"] == e.BLOCKED,
          "ACCESS_BLOCKED sentinel is ACCESS-BLOCKED")
    check(by_field["runner_output"]["evidence"] is None,
          "blocked field carries no invented evidence")
    check("test-pending" in r["summary"] and "runner_output" in r["summary"],
          "summary names pending status and missing field")

    r2 = e.evaluate(full_payload())
    check(r2["status"] == e.DONE and r2["missing"] == [],
          "all confirmed with GOAL.md first is all-confirmed")

    r3 = e.evaluate(full_payload({"goal_md_first": None}))
    check(r3["status"] == e.PENDING, "a single UNKNOWN keeps it test-pending")

    r4 = e.evaluate(full_payload({"runner_output": "dataset published at example"}))
    check(r4["flagged_claims"] == ["runner_output"] and r4["status"] == e.PENDING,
          "a publish claim is flagged and cannot pass")

    r5 = e.evaluate({"goal_md_updated_first": True, "observed": {}})
    check(r5["confirmed"] == 0 and r5["status"] == e.PENDING,
          "empty observed is test-pending, not a pass")

    r6 = e.evaluate(full_payload({"goal_md_first": "posted to the list"}))
    check(r6["flagged_claims"] == ["goal_md_first"], "posting claim is flagged")

    with tempfile.TemporaryDirectory() as td:
        inp = Path(td) / "in.json"
        out = Path(td) / "out.json"
        inp.write_text(json.dumps(sample), encoding="utf-8")
        check(e.main(["evidence.py", str(inp), "--out", str(out)]) == 0,
              "CLI writes output file")
        check(json.loads(out.read_text(encoding="utf-8"))["status"] == e.PENDING,
              "CLI output matches evaluate")
        check(e.main(["evidence.py"]) == 2, "CLI requires input")
        bad = Path(td) / "bad.json"
        bad.write_text("{not json", encoding="utf-8")
        check(e.main(["evidence.py", str(bad)]) == 1, "CLI rejects bad JSON")

    print("\nResults: %d/%d checks passed" % (PASSED, CHECKS))
    return 0 if PASSED == CHECKS else 1


if __name__ == "__main__":
    sys.exit(main())
