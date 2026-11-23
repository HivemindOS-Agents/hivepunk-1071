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
import check as c
CHECKS = PASSED = 0
def check(cond, label):
    global CHECKS, PASSED
    CHECKS += 1
    if cond:
        PASSED += 1; print("ok: %s" % label)
    else:
        print("FAIL: %s" % label)
def make(td, dirs, calendar_lines, files=()):
    data = Path(td) / "data"; data.mkdir()
    for d in dirs:
        (data / d).mkdir()
    for f in files:
        (data / f).write_text("x", encoding="utf-8")
    cal = Path(td) / "calendar.txt"
    cal.write_text("\n".join(calendar_lines) + "\n", encoding="utf-8")
    return data, cal
def main():
    check(c.valid_yyyymmdd("20261029") and not c.valid_yyyymmdd("20261301") and not c.valid_yyyymmdd("2026-10-29") and not c.valid_yyyymmdd(""), "date validation accepts real YYYYMMDD only")
    with tempfile.TemporaryDirectory() as td:
        data, cal = make(td, ["20261029", "20261030", "20261102"], ["20261029", "20261030", "20261102", "20261103"])
        r = c.compare(str(data), str(cal))
        check(r["missing"] == ["20261103"], "missing date in supplied calendar reported")
        check(r["present"] == ["20261029", "20261030", "20261102"], "present dates sorted")
    with tempfile.TemporaryDirectory() as td:
        # Dates absent from the calendar (e.g. a weekend/holiday the
        # owner left out) are NOT missing, even with no directory.
        data, cal = make(td, ["20261029"], ["20261029", "20261030"])
        r = c.compare(str(data), str(cal))
        check("20261031" not in r["missing"] and "20261101" not in r["missing"], "dates absent from supplied calendar never reported missing")
        check(r["missing"] == ["20261030"], "only supplied-calendar date reported missing")
    with tempfile.TemporaryDirectory() as td:
        data, cal = make(td, ["20261029", "20261105"], ["# comment", "", "20261029", "20261029", "20261030,note"])
        r = c.compare(str(data), str(cal))
        check(r["expected"] == ["20261029", "20261030"], "calendar comments/blanks/duplicates handled")
        check(r["extra_not_in_calendar"] == ["20261105"], "extra directory reported as extra, not missing")
        check(r["counts"]["missing"] == 1, "counts consistent")
    with tempfile.TemporaryDirectory() as td:
        data, cal = make(td, ["20261029", "notes", "20261301", "2026103"], ["20261029"], files=["20261030"])
        r = c.compare(str(data), str(cal))
        check(r["present"] == ["20261029"], "only valid YYYYMMDD directories count as present")
        check(sorted(r["ignored_names"]) == ["2026103", "20261030", "20261301", "notes"], "files and invalid names ignored, not present")
    with tempfile.TemporaryDirectory() as td:
        data, cal = make(td, [], ["2026-10-29"])
        try:
            c.compare(str(data), str(cal)); raised = False
        except ValueError:
            raised = True
        check(raised, "invalid calendar line raises error")
    with tempfile.TemporaryDirectory() as td:
        data, cal = make(td, ["20261029"], ["20261029", "20261030"])
        out = Path(td) / "out.json"
        check(c.main(["check.py", "--data-dir", str(data), "--calendar", str(cal), "--out", str(out)]) == 0, "CLI writes output")
        parsed = json.loads(out.read_text(encoding="utf-8"))
        check(parsed["missing"] == ["20261030"], "CLI JSON missing correct")
        check(c.main(["check.py", "--data-dir", str(data)]) == 2, "CLI requires calendar")
    print("\nResults: %d/%d checks passed" % (PASSED, CHECKS))
    return 0 if PASSED == CHECKS else 1
if __name__ == "__main__":
    sys.exit(main())
