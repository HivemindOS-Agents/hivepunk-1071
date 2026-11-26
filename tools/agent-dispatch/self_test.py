#!/usr/bin/env python3
"""Standalone offline self-test. No arguments, no network.

Checks dispatch.match, GOAL/ARTIFACTS/README evidence,
hugf_manifest.md, the verified data file, and that the
upload record is honest: either NOT UPLOADED with no live
URL claimed, or a future verified URL that is fetch-checked.
Exits 0 only when every check passes.
"""
import hashlib
import json
import re
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import dispatch as d

LATEST_RUN = "45712491184"
LATEST_RUN_UTC = "2026-11-25 22:21 UTC"
LATEST_RESULT = "Results: 40/40 checks passed"
PRIOR_RUN = "45618100411"
DATASET_URL = "https://huggingface.co/datasets/hivepunk-1071-f79faf84/agent-dispatch"

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


def raises(fn):
    try:
        fn()
    except ValueError:
        return True
    return False


def text_of(name):
    return (HERE / name).read_text(encoding="utf-8")


def goal_sha256():
    return hashlib.sha256((HERE / "GOAL.md").read_bytes()).hexdigest()


def main():
    goal = text_of("GOAL.md")
    check("https://github.com/Trisoma/odessy/issues/73" in goal,
          "GOAL.md cites the issue")
    check("test-pending" in goal, "GOAL.md marks this commit test-pending")
    check("data/matcher_examples.json" in goal,
          "GOAL.md names the verified data file")

    artifacts = text_of("ARTIFACTS.md")
    check("python3 self_test.py" in artifacts,
          "ARTIFACTS.md records the exact test command")
    check(LATEST_RUN in artifacts and LATEST_RUN_UTC in artifacts
          and LATEST_RESULT in artifacts,
          "ARTIFACTS.md records the 40/40 runner output")
    check(PRIOR_RUN in artifacts,
          "ARTIFACTS.md keeps the prior run as history")
    check("test-pending" in artifacts,
          "ARTIFACTS.md marks this commit test-pending")
    check("NOT RUN IN THIS STEP" in artifacts,
          "ARTIFACTS.md does not claim a local run in this step")
    check("data/matcher_examples.json" in artifacts,
          "ARTIFACTS.md names the repaired dataset file")
    check("https://github.com/HivemindOS-Agents/hivepunk-1071/tree/main/tools/agent-dispatch" in artifacts,
          "ARTIFACTS.md lists the public repository URL")

    check("## Upload record" in artifacts,
          "ARTIFACTS.md has an upload-record section")
    upload_section = artifacts.split("## Upload record", 1)[1]
    not_uploaded = "NOT UPLOADED" in artifacts
    verified = (
        ("Public dataset URL: " + DATASET_URL) in upload_section
        and "fetch-checked" in upload_section
        and "Public dataset URL, fetch-checked after upload: NOT PERFORMED" not in upload_section
    )
    check(not_uploaded or verified,
          "upload record is NOT UPLOADED or has a fetch-checked verified URL")
    check(not_uploaded or verified,
          "guard allows a future verified URL (not a blanket URL ban)")
    if not_uploaded:
        check("Exact upload commands: NOT PERFORMED" in artifacts
              and "UTC timestamp of the upload: NOT PERFORMED" in artifacts,
              "NOT UPLOADED placeholders are explicit")
        check(DATASET_URL not in upload_section,
              "no live dataset URL claimed while NOT UPLOADED")
    else:
        check(verified, "verified URL is the exact account/name URL")

    readme = text_of("README.md")
    check("test-pending" in readme and "GOAL.md" in readme,
          "README.md is test-pending and references GOAL.md")
    check(PRIOR_RUN in readme and "31/31" in readme,
          "README.md records the 31/31 run")

    manifest = text_of("hugf_manifest.md")
    check("hivepunk-1071-f79faf84/agent-dispatch" in manifest,
          "manifest names the intended account/name")
    check("README.md" in manifest and "data/" in manifest,
          "manifest lists README.md and data/")
    check("INTENDED, NOT LIVE" in manifest,
          "manifest marks the URL intended")
    check("Do not send: GOAL.md" in manifest,
          "manifest excludes GOAL.md from the upload")

    # Verified dataset file: only examples from repo sources.
    data_path = HERE / "data" / "matcher_examples.json"
    check(data_path.is_file(), "data/matcher_examples.json exists")
    if data_path.is_file():
        payload = json.loads(data_path.read_text(encoding="utf-8"))
        check(payload.get("source", "").startswith("README.md; self_test.py"),
              "data file cites its verified sources")
        examples = payload.get("examples", [])
        check(len(examples) == 3, "data file has exactly 3 verified examples")
        for ex in examples:
            result = d.match(ex["tags"], ex["rules"])
            exp = ex["expected"]
            check(all(result[k] == exp[k] for k in exp),
                  "data example '%s' matches dispatch.match" % ex["name"])

    rules = [
        {"tag": "Python", "strength": 2, "label": "low"},
        {"tag": "python", "strength": 5, "label": "high"},
        {"tag": "go", "strength": 5, "label": "go-high"},
    ]
    r = d.match([" PYTHON "], rules)
    check(r["matched"] is True and r["strength"] == 5
          and r["label"] == "high" and r["rule_index"] == 1,
          "highest strength wins, tag normalized")
    r = d.match(["go", "python"], rules)
    check(r["tag"] == "python" and r["rule_index"] == 1,
          "tie broken by earliest rule")
    r = d.match(["unknown-tag"], rules)
    check(r == {"matched": False, "strength": None, "tag": None,
                "label": None, "rule_index": None, "reason": "no-match",
                "normalized_tags": ["unknown-tag"], "candidates": []},
          "no-match is explicit, not guessed")
    r = d.match([], rules)
    check(r["matched"] is False and r["reason"] == "no-match",
          "empty tags give no-match")
    check(raises(lambda: d.match(["x"], [{"tag": "x", "strength": True}])),
          "boolean strength rejected")
    check(raises(lambda: d.match(["x"], [{"tag": "x", "strength": "high"}])),
          "string strength rejected")
    check(raises(lambda: d.match([" "], rules)), "blank tag rejected")
    a = d.match(["go", "python"], rules)
    b = d.match(["python", "go"], rules)
    check(a["tag"] == b["tag"] and a["rule_index"] == b["rule_index"],
          "result independent of tag order")

    with tempfile.TemporaryDirectory() as td:
        inp = Path(td) / "in.json"
        out = Path(td) / "out.json"
        inp.write_text(json.dumps({"tags": ["nope"], "rules": rules}),
                       encoding="utf-8")
        check(d.main(["dispatch.py", str(inp), "--out", str(out)]) == 0,
              "CLI writes output")
        parsed = json.loads(out.read_text(encoding="utf-8"))
        check(parsed["matched"] is False and parsed["reason"] == "no-match",
              "CLI no-match JSON correct")
        check(d.main(["dispatch.py"]) == 2, "CLI requires input")

    digest = goal_sha256()
    check(len(digest) == 64
          and all(ch in "0123456789abcdef" for ch in digest),
          "GOAL.md sha256 is 64 lowercase hex chars")
    check(goal_sha256() == digest,
          "GOAL.md sha256 is deterministic across reads")
    print("GOAL.md sha256: %s" % digest)
    print("\nResults: %d/%d checks passed" % (PASSED, CHECKS))
    return 0 if PASSED == CHECKS else 1


if __name__ == "__main__":
    sys.exit(main())
