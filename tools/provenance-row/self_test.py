#!/usr/bin/env python3
"""self_test.py -- offline check for provenance_row.py.

Run from inside the folder with no arguments:
    python3 self_test.py; echo exit=$?

It imports provenance_row from THIS folder (sys.path built from
Path(__file__).parent), builds one row from the synthetic fixture snapshot,
and checks the Issue cell. No subprocess, no cwd dependence, no network,
stdlib only. Exits 0 only when the check passes.
"""

import datetime
import sys
from pathlib import Path

# Ensure the tool can be imported from this folder
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import provenance_row as pr

# Fixture snapshot and test parameters
FIXTURE = HERE / "fixtures" / "snapshot.md"
URL = "https://github.com/example-org/example-repo/issues/58"
DATE_CHECKED = "2026-11-07"
EXPECTED_ISSUE = "example-repo/issues#58"


def main():
    # build_row takes the fixture's PATH, not its text: it opens the file itself
    row, _warnings = pr.build_row(str(FIXTURE), datetime.date.fromisoformat(DATE_CHECKED))
    if row["Issue"] != EXPECTED_ISSUE:
        print("FAIL: Issue cell is %r, expected %s" % (row["Issue"], EXPECTED_ISSUE))
        return 1
    print("ok: Issue cell is example-repo/issues#58")
    return 0


if __name__ == "__main__":
    sys.exit(main())
