#!/usr/bin/env python3
"""self_test.py -- offline checks for update_index.py.

Run with no arguments, no network. Exits 0 only when every check passes.
Everything runs on the synthetic fixture pair in fixtures/.
"""

import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "update_index.py")
FIX_ROWS = os.path.join(HERE, "fixtures", "recheck_rows.csv")
FIX_SNAP = os.path.join(HERE, "fixtures", "snapshots")
HEADER = "Issue,Date checked,Page opened,Status,What it showed"


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
    check(os.path.exists(FIX_ROWS), "fixture recheck_rows.csv exists")
    check(os.path.isdir(FIX_SNAP), "fixture snapshots/ exists")
    work = tempfile.mkdtemp(prefix="update-index-selftest-")
    try:
        data = os.path.join(work, "data.csv")
        card = os.path.join(work, "README.md")

        result = run([FIX_ROWS, "--snapshots", FIX_SNAP, "--data", data, "--card", card])
        check(result.returncode == 0, "run on the fixture pair exits 0")

        with open(data, "r", encoding="utf-8", newline="") as handle:
            lines = [line.rstrip("\n") for line in handle.readlines()]
        check(lines[0] == HEADER, "data.csv header is the exact five fields")
        check(len(lines) == 4, "data.csv holds the header plus 3 rows")
        check("#3" in lines[1] and "#9" in lines[2] and "#12" in lines[3],
              "rows are natural-sorted (#3, #9, #12)")

        body = "\n".join(lines)
        row9 = [l for l in lines[1:] if "#9" in l][0]
        check("cannot-check" in row9,
              "row with a snapshot lacking a save date is forced to cannot-check")
        verified = [line for line in lines[1:] if ",verified," in line]
        check(len(verified) == 1, "exactly one row keeps verified (it has a full snapshot)")
        check("#12" in verified[0], "#12 is the row that stays verified")

        with open(card, "r", encoding="utf-8") as handle:
            text = handle.read()
        check("Rows not opened" in text, "card has a final Rows not opened section")
        tail = text.split("Rows not opened", 1)[1]
        check("#3" in tail, "not-opened row #3 is named in that section")
        check("#12" not in tail, "opened row #12 is not named as not opened")
        check("#9" not in tail, "url-opened row #9 is not named as not opened")

        result = run([FIX_ROWS, "--snapshots", FIX_SNAP, "--dry-run"])
        check(result.returncode == 0, "dry run exits 0")
        check("wrote" not in result.stdout, "dry run writes nothing")

        dup = os.path.join(work, "dup.csv")
        with open(dup, "w", encoding="utf-8", newline="") as handle:
            handle.write(HEADER + "\n")
            handle.write("x#1,2026-10-29,https://example.org/1,unverified,one\n")
            handle.write("x#1,2026-10-29,https://example.org/2,unverified,two\n")
        result = run([dup, "--snapshots", FIX_SNAP, "--data", os.path.join(work, "no.csv")])
        check(result.returncode == 1, "duplicate Issue exits 1")
        check(not os.path.exists(os.path.join(work, "no.csv")),
              "failed validation writes no data file")

        bad = os.path.join(work, "bad.csv")
        with open(bad, "w", encoding="utf-8", newline="") as handle:
            handle.write(HEADER + "\n")
            handle.write("x#2,2026-02-30,https://example.org/2,unverified,impossible date\n")
        result = run([bad, "--snapshots", FIX_SNAP, "--data", os.path.join(work, "no2.csv")])
        check(result.returncode == 1, "unreal calendar date exits 1")

        missing = run([os.path.join(work, "does-not-exist.csv")])
        check(missing.returncode == 2, "missing input exits 2")

        print("all checks passed")
        return 0
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
