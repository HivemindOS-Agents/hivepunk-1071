#!/usr/bin/env python3
"""Standalone offline self-test. No args, no network. Run: python3 self_test.py"""
import json
import sys
import tempfile
from pathlib import Path
HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import kickoff as k
CHECKS = PASSED = 0
def check(cond, label):
    global CHECKS, PASSED
    CHECKS += 1
    if cond:
        PASSED += 1; print("ok: %s" % label)
    else:
        print("FAIL: %s" % label)
def raises(fn):
    try:
        fn()
    except ValueError:
        return True
    return False
def load_sample():
    return json.loads((HERE / "sample_data.json").read_text(encoding="utf-8"))
def main():
    data = load_sample()
    check(data["issue_url"] == k.ISSUE_URL, "sample cites issue 2412")
    readme = (HERE / "README.md").read_text(encoding="utf-8")
    check(k.ISSUE_URL in readme and "test-pending" in readme, "README GOAL cites issue 2412 and marks tasks test-pending")
    goal = (HERE / "GOAL.md").read_text(encoding="utf-8")
    check(k.ISSUE_URL in goal, "GOAL.md cites issue 2412")
    artifacts = (HERE / "ARTIFACTS.md").read_text(encoding="utf-8")
    check("python3 self_test.py" in artifacts and "Results: 17/17 checks passed" in artifacts and "45334486417" in artifacts, "ARTIFACTS.md records exact command and 17/17 runner output")
    check(k.validate(data) is True, "sample validates")
    c = k.counts(data)
    check(c == {"FACT": 4, "DERIVED": 1, "UNKNOWN": 1}, "claim counts exact")
    text = k.render(data)
    check("# Microcks v2 kick-off summary" in text, "render has title")
    check("## Stated goals" in text and "## Open questions" in text, "render has goals and open questions sections")
    check("[FACT]" in text and "[DERIVED]" in text and "[UNKNOWN]" in text, "render labels every item")
    check("Counts: FACT=4 DERIVED=1 UNKNOWN=1 total=6" in text, "render counts line exact")
    check("1.16.0" in text, "render includes prior-research release fact")
    check(k.render(load_sample()) == text, "render is deterministic")
    bad = load_sample(); bad["issue_url"] = "https://example.com/wrong"
    check(raises(lambda: k.render(bad)), "wrong issue_url rejected")
    bad = load_sample(); bad["claims"][0]["label"] = "MAYBE"
    check(raises(lambda: k.render(bad)), "unknown label rejected")
    bad = load_sample(); bad["claims"][0]["text"] = "  "
    check(raises(lambda: k.render(bad)), "blank claim text rejected")
    bad = load_sample(); bad["goals"] = []
    check(k.render(bad).count("## Stated goals") == 1, "empty goals still render section without inventing items")
    with tempfile.TemporaryDirectory() as td:
        inp = Path(td) / "in.json"; out = Path(td) / "out.md"
        inp.write_text(json.dumps(data), encoding="utf-8")
        check(k.main(["kickoff.py", str(inp), "--out", str(out)]) == 0, "CLI writes output")
        check(out.read_text(encoding="utf-8") == text, "CLI output matches render")
        check(k.main(["kickoff.py"]) == 2, "CLI requires input")
    print("\nResults: %d/%d checks passed" % (PASSED, CHECKS))
    return 0 if PASSED == CHECKS else 1
if __name__ == "__main__":
    sys.exit(main())
