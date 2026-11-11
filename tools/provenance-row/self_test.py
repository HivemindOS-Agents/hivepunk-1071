#!/usr/bin/env python3
"""self_test.py -- offline checks for provenance_row.py.

Run from inside the folder:
    python3 self_test.py; echo exit=$?
"""

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

def main():
    # Read the snapshot text
    snapshot_text = FIXTURE.read_text(encoding="utf-8")
    # Build the provenance row using the tool's API
    row = pr.build_row(snapshot_text, DATE_CHECKED)
    # Assert the Issue cell is as expected
    if row["Issue"] != "example-repo#58":
        print(f"FAIL: Issue cell is {row['Issue']}, expected example-repo#58")
        sys.exit(1)
    print("ok: Issue cell is example-repo#58")
    sys.exit(0)

if __name__ == "__main__":
    main()
