#!/usr/bin/env python3
"""self_test.py - run from inside folder: python3 self_test.py
Imports classify.py, runs it on sample titles and shipped data.csv.
"""
import sys, tempfile
from pathlib import Path
HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path: sys.path.insert(0, str(HERE))
import classify
CHECKS = PASSED = 0
def check(cond, label):
    global CHECKS, PASSED
    CHECKS += 1
    if cond: PASSED += 1; print("ok: %s" % label)
    else: print("FAIL: %s" % label)
def main():
    check(classify.classify("How does this work?") == "question", "question for ? title")
    check(classify.classify("Showcase: I built a bot") == "showcase", "showcase for built title")
    check(classify.classify("Weekly report and results") == "report", "report for results title")
    check(classify.classify("Ask: please help with setup") == "ask", "ask for help title")
    check(classify.classify("Random notes") == "other", "other fallback")
    check(classify.classify("") == "other", "empty title is other")
    fields, rows = classify.load_rows(HERE / "data" / "data.csv")
    check(fields == classify.COLUMNS, "shipped header matches COLUMNS")
    check(len(rows) >= 20, "shipped data.csv has at least 20 rows (%d)" % len(rows))
    check(all(r["kind"] in classify.KINDS for r in rows), "all shipped kinds valid")
    check(all(r["read_back"] in ("opened", "not-opened") for r in rows), "all read_back values valid")
    check(all(r["read_back"] == "not-opened" for r in rows), "all shipped rows honestly marked not-opened")
    rows2, errors = classify.validate(HERE / "data" / "data.csv")
    check(errors == [], "validate() passes shipped data.csv")
    check(len(rows2) == len(rows), "validate returns same row count")
    tmp = Path(tempfile.mkdtemp()) / "bad.csv"
    tmp.write_text("thread_title,kind,source_url,read_back\nOnly one,other,not-opened,not-opened\n", encoding="utf-8")
    _, errs = classify.validate(tmp)
    check(any("at least 20" in e for e in errs), "short file fails row count")
    tmp2 = Path(tempfile.mkdtemp()) / "bad2.csv"
    tmp2.write_text("thread_title,kind,source_url,read_back\n" + "".join("T%d,other,not-opened,not-opened\n" % i for i in range(20)), encoding="utf-8")
    _, errs2 = classify.validate(tmp2)
    check(errs2 == [], "20-row not-opened fixture passes")
    tmp3 = Path(tempfile.mkdtemp()) / "bad3.csv"
    tmp3.write_text("thread_title,kind,source_url,read_back\n" + "".join("T%d,other,https://example.com/x,opened\n" % i for i in range(20)), encoding="utf-8")
    _, errs3 = classify.validate(tmp3)
    check(len(errs3) >= 1, "opened rows with non-reddit URLs fail")
    print("\nResults: %d/%d checks passed" % (PASSED, CHECKS))
    return 0 if PASSED == CHECKS else 1
if __name__ == "__main__":
    sys.exit(main())
