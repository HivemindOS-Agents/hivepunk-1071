#!/usr/bin/env python3
"""Standalone offline self-test. No args, no network.
Exits 0 only when every check passes."""
import json
import sys
import tempfile
from pathlib import Path
HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import dispatch as d
CHECKS = PASSED = 0
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
def main():
    rules = [
        {"tag": "Python", "strength": 2, "label": "low"},
        {"tag": "python", "strength": 5, "label": "high"},
        {"tag": "go", "strength": 5, "label": "go-high"},
    ]
    r = d.match([" PYTHON "], rules)
    check(r["matched"] is True and r["strength"] == 5 and r["label"] == "high" and r["rule_index"] == 1, "highest strength wins, tag normalized")
    r = d.match(["go", "python"], rules)
    check(r["tag"] == "python" and r["rule_index"] == 1, "tie broken by earliest rule")
    r = d.match(["go"], list(reversed(rules)))
    check(r["matched"] is True and r["strength"] == 5, "reversed rules still match go")
    r = d.match(["unknown-tag"], rules)
    check(r == {"matched": False, "strength": None, "tag": None, "label": None, "rule_index": None, "reason": "no-match", "normalized_tags": ["unknown-tag"], "candidates": []}, "no-match is explicit, not guessed")
    r = d.match([], rules)
    check(r["matched"] is False and r["reason"] == "no-match", "empty tags give no-match")
    r = d.match(["Python", "python", " PYTHON "], rules)
    check(r["normalized_tags"] == ["python"], "duplicate tags deduplicated after normalization")
    r = d.match(["a  b"], [{"tag": "A B", "strength": 1.5}])
    check(r["matched"] is True and r["strength"] == 1.5, "whitespace collapsed, float strength kept")
    check(raises(lambda: d.match(["x"], [{"tag": "x", "strength": True}])), "boolean strength rejected")
    check(raises(lambda: d.match(["x"], [{"tag": "x", "strength": "high"}])), "string strength rejected")
    check(raises(lambda: d.match([" "], rules)), "blank tag rejected")
    check(raises(lambda: d.match([1], rules)), "non-string tag rejected")
    check(raises(lambda: d.match(["x"], [{"tag": "x"}])), "rule without strength rejected")
    a = d.match(["go", "python"], rules)
    b = d.match(["python", "go"], rules)
    check(a["tag"] == b["tag"] and a["strength"] == b["strength"] and a["rule_index"] == b["rule_index"], "result independent of tag order")
    with tempfile.TemporaryDirectory() as td:
        inp = Path(td) / "in.json"
        out = Path(td) / "out.json"
        inp.write_text(json.dumps({"tags": ["nope"], "rules": rules}), encoding="utf-8")
        check(d.main(["dispatch.py", str(inp), "--out", str(out)]) == 0, "CLI writes output")
        parsed = json.loads(out.read_text(encoding="utf-8"))
        check(parsed["matched"] is False and parsed["reason"] == "no-match", "CLI no-match JSON correct")
        check(d.main(["dispatch.py"]) == 2, "CLI requires input")
    print("\nResults: %d/%d checks passed" % (PASSED, CHECKS))
    return 0 if PASSED == CHECKS else 1
if __name__ == "__main__":
    sys.exit(main())
