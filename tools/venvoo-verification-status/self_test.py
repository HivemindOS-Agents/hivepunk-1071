#!/usr/bin/env python3
"""Standalone offline self-test. No args, no network."""
import json
import sys
import tempfile
from pathlib import Path
HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import status as s
CHECKS = PASSED = 0
def check(cond, label):
    global CHECKS, PASSED
    CHECKS += 1
    if cond:
        PASSED += 1; print("ok: %s" % label)
    else:
        print("FAIL: %s" % label)
def main():
    check(s.REQUIRED == ["current_commit_runner_passed", "push_via_authorized_api_done", "public_files_fetch_checked", "goal_md_sha256_logged"], "required blocker list exact")
    r = s.evaluate({})
    check(r["verdict"] == "WAIT" and r["blockers"] == s.REQUIRED, "empty state waits on every blocker")
    partial = {k: True for k in s.REQUIRED[:3]}
    r = s.evaluate(partial)
    check(r["verdict"] == "WAIT" and r["blockers"] == ["goal_md_sha256_logged"], "runner+push+fetch without hash still waits")
    full = {k: True for k in s.REQUIRED}
    r = s.evaluate(full)
    check(r["verdict"] == "READY" and r["blockers"] == [], "all items true gives READY")
    r = s.evaluate({k: "yes" for k in s.REQUIRED})
    check(r["verdict"] == "WAIT", "truthy non-True values do not clear blockers")
    try:
        s.evaluate([]); raised = False
    except ValueError:
        raised = True
    check(raised, "non-object state raises error")
    with tempfile.TemporaryDirectory() as td:
        sample = HERE / "sample_status.json"
        state = json.loads(sample.read_text(encoding="utf-8"))
        check(state.get("current_commit_runner_passed") is True, "sample records runner pass on record")
        check(state.get("push_via_authorized_api_done") is False, "sample does not claim push")
        check(state.get("public_files_fetch_checked") is False, "sample does not claim fetch-check")
        check(state.get("goal_md_sha256_logged") is False, "sample does not claim GOAL hash")
        inp = Path(td) / "in.json"; out = Path(td) / "out.json"
        inp.write_text(json.dumps(state), encoding="utf-8")
        check(s.main(["status.py", str(inp), "--out", str(out)]) == 0, "CLI writes output")
        parsed = json.loads(out.read_text(encoding="utf-8"))
        check(parsed["verdict"] == "WAIT" and "goal_md_sha256_logged" in parsed["blockers"], "CLI verdict WAIT for sample")
    print("\nResults: %d/%d checks passed" % (PASSED, CHECKS))
    return 0 if PASSED == CHECKS else 1
if __name__ == "__main__":
    sys.exit(main())
