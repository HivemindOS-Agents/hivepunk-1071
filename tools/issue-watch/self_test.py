#!/usr/bin/env python3
"""self_test.py -- offline checks for issue-watch.

Run with no arguments and no network. Exits 0 only when every check passes.
It (1) compiles and runs issue_watch.py on the HTML fixture, (2) checks the
CSV, and (3) builds a 3-row recheck_rows.csv in a temp dir and runs
../recheck-lint/publish_recheck_rows.py on it, asserting the non-opened row
is marked and the opened rows are left in the table.
"""

import csv
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
TOOL = os.path.join(HERE, "issue_watch.py")
FIXTURES = os.path.join(HERE, "fixtures")
RECHECK = os.path.join(HERE, "..", "recheck-lint", "publish_recheck_rows.py")

fails = []


def check(ok, label):
    print(("ok: " + label) if ok else ("FAIL: " + label))
    if not ok:
        fails.append(label)


def main():
    # 1. Compiles.
    try:
        with open(TOOL, "r", encoding="utf-8") as fh:
            compile(fh.read(), TOOL, "exec")
        check(True, "issue_watch.py compiles")
    except SyntaxError as exc:
        check(False, "issue_watch.py compiles (%s)" % exc)

    # 2. Missing --pages exits 2 and writes nothing.
    tmp = tempfile.mkdtemp(prefix="issue-watch-selftest-")
    try:
        bad_out = os.path.join(tmp, "should_not_exist.csv")
        r = subprocess.run([sys.executable, TOOL, "--pages",
                            os.path.join(tmp, "nope"), "--out", bad_out],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                           text=True, cwd=tmp)
        check(r.returncode == 2, "missing --pages exits 2 (got %d)" % r.returncode)
        check(not os.path.exists(bad_out), "missing --pages writes nothing")

        # 3. Run over the fixtures.
        out = os.path.join(tmp, "data.csv")
        r = subprocess.run([sys.executable, TOOL, "--pages", FIXTURES,
                            "--out", out], stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE, text=True, cwd=tmp)
        check(r.returncode == 0, "run over fixtures exits 0 (got %d)" % r.returncode)

        rows = []
        if os.path.exists(out):
            with open(out, newline="", encoding="utf-8") as fh:
                rows = list(csv.DictReader(fh))
        by_issue = {row["Issue"]: row for row in rows}
        check("64" in by_issue, "a row for fixture issue 64")
        if "64" in by_issue:
            r64 = by_issue["64"]
            check(r64["Page opened"] == "yes", "64: Page opened is yes")
            check(r64["Date checked"] == "2026-11-02", "64: date read")
            check(r64["Status"] == "verified", "64: status read")
            check(r64["What it showed"].startswith("Page read"),
                  "64: finding read")
            check("github.com" in r64.get("Source URL", ""),
                  "64: source URL recorded")

        # 4. Build a 3-row recheck CSV and run recheck-lint on it.
        rows_path = os.path.join(tmp, "recheck_rows.csv")
        header = "Issue,Date checked,Page opened,Status,What it showed,Source URL"
        body = [
            "#64,2026-11-02,yes,verified,Page read; one row per issue page,"
            "https://github.com/LiamVisionary/bee-scouts/issues/64",
            "#65,2026-11-02,no,cannot-check,Page never opened,",
            "#66,2026-11-02,yes,unverified,Page read; duplicate,"
            "https://github.com/LiamVisionary/bee-scouts/issues/66",
        ]
        with open(rows_path, "w", encoding="utf-8", newline="") as fh:
            fh.write(header + "\n" + "\n".join(body) + "\n")

        card = os.path.join(tmp, "dataset_card.md")
        rr = subprocess.run([sys.executable, os.path.abspath(RECHECK),
                             rows_path, "--card", card],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            text=True, cwd=tmp)
        check(rr.returncode == 0,
              "recheck-lint on 3-row CSV exits 0 (got %d)" % rr.returncode)
        check(os.path.isfile(card), "recheck-lint wrote the card")
        text = ""
        if os.path.isfile(card):
            with open(card, "r", encoding="utf-8") as fh:
                text = fh.read()
        check("## Not opened" in text, "card has a Not opened section")
        tail = text.split("## Not opened", 1)[1] if "## Not opened" in text else ""
        tail = tail.split("## Could not check", 1)[0]
        check("#65" in tail, "non-opened row #65 is marked in Not opened")
        check("#64" not in tail, "opened row #64 stays out of Not opened")
        check("#66" not in tail, "opened row #66 stays out of Not opened")
        check("#64" in text and "#66" in text,
              "opened rows remain in the main table")

        print("all checks passed")
        return 0 if not fails else 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
