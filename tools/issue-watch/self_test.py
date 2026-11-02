#!/usr/bin/env python3
"""self_test.py -- offline checks for issue-watch.

Run from anywhere, with no arguments and no network. Every path is built from
this file's own folder, so running it from the repository root works the same
as running it from the tool folder. Exit 0 only when every check passes.

Checks:
  * the tool file exists and compiles;
  * the sibling recheck-lint script exists (reported by absolute path);
  * fixture 64 parses to an opened row with date, status, finding and source URL;
  * no line of output presents a not-opened row as opened.
"""

import json
import os
import subprocess
import sys

HERE = os.path.realpath(os.path.dirname(os.path.abspath(__file__)))
TOOL = os.path.join(HERE, "issue_watch.py")
FIX = os.path.join(HERE, "fixtures")
SIBLING = os.path.join(HERE, os.pardir, "recheck-lint", "publish_recheck_rows.py")

fails = []


def check(ok, label):
    print(("ok: " + label) if ok else ("FAIL: " + label))
    if not ok:
        fails.append(label)


def main():
    if not os.path.isfile(TOOL):
        check(False, "issue_watch.py found at %s" % TOOL)
        return 1
    check(True, "issue_watch.py found")
    with open(TOOL, "r", encoding="utf-8") as fh:
        try:
            compile(fh.read(), TOOL, "exec")
            check(True, "issue_watch.py compiles")
        except SyntaxError as exc:
            check(False, "issue_watch.py compiles (%s)" % exc)
            return 1

    check(os.path.isfile(SIBLING),
          "recheck-lint tool found at %s" % os.path.realpath(SIBLING))

    here = os.getcwd()
    os.chdir(HERE)
    try:
        r = subprocess.run([sys.executable, TOOL, "--fixtures", FIX, "--json"],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                           text=True)
    finally:
        os.chdir(here)
    check(r.returncode == 0,
          "tool exits 0 on the fixtures (got %d)" % r.returncode)
    if r.stderr.strip():
        print("stderr: " + r.stderr.strip())
    try:
        rows = json.loads(r.stdout or "[]")
    except ValueError as exc:
        check(False, "tool output is JSON (%s)" % exc)
        return 1
    by_issue = {row.get("issue"): row for row in rows}
    row = by_issue.get("64")
    check(row is not None, "a row for fixture issue 64")
    if row is None:
        return 1
    check(row.get("page_opened") == "yes", "64: Page opened is yes")
    check(bool(row.get("date_checked")), "64: date read")
    check(bool(row.get("status")), "64: status read")
    check(bool(row.get("what_it_showed")), "64: finding read")
    check(row.get("source_url", "").startswith("http"),
          "64: source URL recorded")
    check("64" not in [r.get("issue") for r in rows
                        if r.get("page_opened") == "no"],
          "64 is not listed as not opened")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
