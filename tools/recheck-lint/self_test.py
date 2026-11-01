#!/usr/bin/env python3
"""self_test.py -- offline checks for publish_recheck_rows.py.

Run with no arguments and no network. Exits 0 only when every check passes.
Everything runs on the four synthetic fixture rows written below; no real
recheck_rows.csv is read and no page is opened.
"""

import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "publish_recheck_rows.py")
HEADER = ("Issue,Date checked,Page opened,Status,What it showed,Source URL")

FIXTURE_ROWS = [
    # clean verified row: page opened, everything present
    "#12,2026-10-29,yes,verified,Range table with one row per issue page,"
    "https://github.com/LiamVisionary/bee-scouts/issues/12",
    # verified status but no page opened: must appear in Not opened
    "#3,2026-10-29,no,verified,Snippet said the range table looked right,"
    "https://github.com/LiamVisionary/bee-scouts/issues/3",
    # missing date: validation must reject this row
    "#9,,yes,unverified,"",https://example.org/issues/9",
    # extra no-page row, with a snippet note instead of yes/no
    "#7,2026-10-29,not opened \u2014 search-result snippet only,cannot-check,"
    "https://example.org/issues/7",
]


def run(args):
    return subprocess.run([sys.executable, SCRIPT] + args,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          text=True, cwd=HERE)


def check(condition, label):
    if not condition:
        print("FAIL: " + label)
        sys.exit(1)
    print("ok: " + label)


def main():
    work = tempfile.mkdtemp(prefix="recheck-lint-selftest-")
    try:
        rows_path = os.path.join(work, "recheck_rows.csv")
        # rows 1, 2 and 4 are written; row 3 (missing date) goes to a
        # separate file so the valid run is not poisoned by it.
        good = [FIXTURE_ROWS[0], FIXTURE_ROWS[1], FIXTURE_ROWS[3]]
        with open(rows_path, "w", encoding="utf-8", newline="") as fh:
            fh.write(HEADER + "\n" + "\n".join(good) + "\n")

        bad_path = os.path.join(work, "missing_date.csv")
        with open(bad_path, "w", encoding="utf-8", newline="") as fh:
            fh.write(HEADER + "\n" + FIXTURE_ROWS[2] + "\n")

        card = os.path.join(work, "dataset_card.md")
        result = run([rows_path, "--card", card,
                      "--command", "python3 publish_recheck_rows.py recheck_rows.csv"])
        check(result.returncode == 0, "valid fixture run exits 0")
        check(os.path.isfile(card), "dataset_card.md was written")

        with open(card, "r", encoding="utf-8") as fh:
            text = fh.read()

        check("python3 publish_recheck_rows.py recheck_rows.csv" in text,
              "card carries the exact run command line")
        for field in ("Issue", "Date checked", "Page opened", "Status",
                      "What it showed", "Source URL"):
            check(field in text, "card names the column " + field)
        for issue in ("#12", "#3", "#7"):
            check(issue in text, "card table holds row " + issue)

        check("## Not opened" in text, "card has a Not opened section")
        tail = text.split("## Not opened", 1)[1]
        tail = tail.split("## Could not check", 1)[0]
        check("#3" in tail, "not-opened row #3 is named in that section")
        check("#7" in tail, "not-opened row #7 is named in that section")
        check("#12" not in tail, "clean opened row #12 is absent from that section")
        check("Page opened says no" in tail, "row #3 carries its reason")

        check("## Could not check" in text, "card has a Could not check section")
        closing = text.split("## Could not check", 1)[1]
        check("Coverage:" in closing, "Could not check states coverage")
        check("No page re-read" in closing, "Could not check states no page re-read")
        check("No licence claim" in closing,
              "Could not check states no licence claim")

        result = run([rows_path, "--dry-run"])
        check(result.returncode == 0, "dry run exits 0")
        check("wrote" not in result.stdout, "dry run writes nothing")

        bad_card = os.path.join(work, "bad_card.md")
        result = run([bad_path, "--card", bad_card])
        check(result.returncode == 1, "missing date exits 1")
        check(not os.path.exists(bad_card), "missing date writes no card")
        check("Date checked" in result.stderr, "missing date is named in stderr")

        missing = run([os.path.join(work, "absent.csv")])
        check(missing.returncode == 2, "absent input exits 2")

        print("all checks passed")
        return 0
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
