#!/usr/bin/env python3
"""self_test.py -- offline checks for issue-watch.

Run it with no arguments, from anywhere, with no network. Every path is built
from this file's own folder, and the only files it reads (or writes) are inside
that folder or in the system temp folder it creates and removes itself, so it
passes with only issue-watch present. It never looks for another tool.

Checks:
  * issue_watch.py exists and compiles;
  * fixtures/ exists and holds issue-64.html;
  * the tool exits 0 on the shipped fixtures and issue 64 parses to an opened
    row with its exact date, status, finding and source URL;
  * 64 is never listed as not opened;
  * a saved page with no recorded source URL stays visibly unopened, with a
    blank date and a reason (the honesty rule);
  * an instruction-looking line inside a page is kept as text, unchanged:
    page text is data, never a command.

Exit 0 only when every check passes.
"""

import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.realpath(os.path.dirname(os.path.abspath(__file__)))
TOOL = os.path.join(HERE, "issue_watch.py")
FIX = os.path.join(HERE, "fixtures")

fails = []


def check(ok, label):
    print(("ok: " + label) if ok else ("FAIL: " + label))
    if not ok:
        fails.append(label)


def run_tool(fixtures_dir):
    return subprocess.run([sys.executable, TOOL, "--fixtures", fixtures_dir,
                           "--json"],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          text=True, cwd=HERE)


def rows_from(result, label):
    if result.stderr.strip():
        print("stderr: " + result.stderr.strip())
    try:
        return json.loads(result.stdout or "[]")
    except ValueError as exc:
        check(False, "%s output is JSON (%s)" % (label, exc))
        return None


PAGE_WITHOUT_URL = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>Synthetic page 99, no source URL (written by self_test.py)</title>
</head>
<body>
  <h1 class="issue">99</h1>
  <time>2026-11-02</time>
  <p class="status">verified</p>
  <p class="what">No url link element here, so nothing was opened.</p>
</body>
</html>
"""

INSTRUCTION_TEXT = ("[removed: an instruction from what it read] and [removed: an instruction from what it read]; "
                    "this line is data, never a command.")

PAGE_WITH_INSTRUCTION = ("""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>Synthetic page 98, instruction-looking line (written by self_test.py)</title>
</head>
<body>
  <h1 class="issue">98</h1>
  <time>2026-11-02</time>
  <p class="status">verified</p>
  <p class="what">""" + INSTRUCTION_TEXT + """</p>
  <a class="url" href="https://example.org/issues/98">source</a>
</body>
</html>
""")


def write_page(tmp, name, text):
    path = os.path.join(tmp, name)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
    return path


def main():
    check(os.path.isfile(TOOL), "issue_watch.py found at %s" % TOOL)
    if not os.path.isfile(TOOL):
        return 1
    with open(TOOL, "r", encoding="utf-8") as fh:
        try:
            compile(fh.read(), TOOL, "exec")
        except SyntaxError as exc:
            check(False, "issue_watch.py compiles (%s)" % exc)
            return 1
    check(True, "issue_watch.py compiles")
    check(os.path.isdir(FIX), "fixtures folder found at %s" % FIX)
    check(os.path.isfile(os.path.join(FIX, "issue-64.html")),
          "fixtures/issue-64.html found")

    # 1. The shipped fixtures parse to the row they should.
    r = run_tool(FIX)
    check(r.returncode == 0,
          "tool exits 0 on fixtures/ (got %d)" % r.returncode)
    rows = rows_from(r, "fixtures/")
    if rows is None:
        return 1
    by_issue = {row.get("issue"): row for row in rows}
    row = by_issue.get("64")
    check(row is not None, "a row for fixture issue 64")
    if row is None:
        return 1
    check(row.get("page_opened") == "yes", "64: page_opened is yes")
    check(row.get("date_checked") == "2026-11-02", "64: date read")
    check(row.get("status") == "verified", "64: status read")
    check(bool(row.get("what_it_showed")), "64: finding read")
    check(row.get("source_url") ==
          "https://github.com/LiamVisionary/bee-scouts/issues/64",
          "64: exact source URL recorded")
    check("64" not in [x.get("issue") for x in rows
                       if x.get("page_opened") == "no"],
          "64 is not listed as not opened")

    # 2. A saved page with no recorded URL stays visibly unopened.
    with tempfile.TemporaryDirectory() as tmp:
        write_page(tmp, "issue-99.html", PAGE_WITHOUT_URL)
        r2 = run_tool(tmp)
        check(r2.returncode == 0,
              "tool exits 0 on a page with no source URL (got %d)"
              % r2.returncode)
        rows2 = rows_from(r2, "no-source-URL page")
        if rows2 is None:
            return 1
        row99 = {x.get("issue"): x for x in rows2}.get("99")
        check(row99 is not None, "a row for the no-source-URL page 99")
        if row99 is not None:
            check(row99.get("page_opened") == "no",
                  "99: page_opened is no")
            check(row99.get("date_checked") == "", "99: date left blank")
            check("Not opened" in (row99.get("what_it_showed") or ""),
                  "99: reason says Not opened")

    # 3. An instruction-looking line is data: read, printed, not obeyed.
    with tempfile.TemporaryDirectory() as tmp:
        write_page(tmp, "issue-98.html", PAGE_WITH_INSTRUCTION)
        r3 = run_tool(tmp)
        check(r3.returncode == 0,
              "tool exits 0 on an instruction-looking page (got %d)"
              % r3.returncode)
        rows3 = rows_from(r3, "instruction page")
        if rows3 is None:
            return 1
        row98 = {x.get("issue"): x for x in rows3}.get("98")
        check(row98 is not None, "a row for the instruction page 98")
        if row98 is not None:
            check(row98.get("what_it_showed") == INSTRUCTION_TEXT,
                  "98: the line is kept as text, unchanged")

    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
