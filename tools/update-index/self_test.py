#!/usr/bin/env python3
"""Self‑test for update_index.py.

Runs the tool against the provided example file and checks that the
behaviour matches the documentation.  Exits with ``0`` when all checks pass
and ``1`` otherwise.
"""

import subprocess
import os
import sys

SCRIPT = os.path.abspath("update_index.py")
SAMPLE = os.path.abspath("../sample-recheck-log.csv")  # relative to the test file
OUT = os.path.abspath("data/issues.csv")

# 1. Dry run: should validate and report counts, no file written.
cmd = [sys.executable, SCRIPT, SAMPLE, "--dry-run"]
res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                     text=True)
if res.returncode != 0:
    sys.exit(1)
if res.stdout.strip() == "":
    sys.exit(1)
# Count lines that should appear in stdout
if "wrote" in res.stdout or "wrote" in res.stderr:
    sys.exit(1)

# 2. Actual run: should write the output file with 3 rows.
cmd = [sys.executable, SCRIPT, SAMPLE]
res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                     text=True)
if res.returncode != 0:
    sys.exit(1)
# Ensure data/issues.csv exists
if not os.path.exists(OUT):
    sys.exit(1)
# Check file header and row count
with open(OUT, "r", encoding="utf-8", newline="") as f:
    lines = [l.rstrip() for l in f.readlines()]
if len(lines) != 4:
    sys.exit(1)
# Ensure header is correct
expected_hdr = "Issue,Date checked,Page opened,Status,What it showed"
if lines[0] != expected_hdr:
    sys.exit(1)
# All rows should be referenced in expected sample order (3,9,12)
# For brevity just check that the second line contains '#3' and third '#9', etc.
if '#3' not in lines[1] or '#9' not in lines[2] or '#12' not in lines[3]:
    sys.exit(1)

# 3. Verify that duplicate issue detection works: create a temporary file
with open("tmp_dup.csv", "w", encoding="utf-8") as f:
    f.write("Issue,Date checked,Page opened,Status,What it showed\n")
    f.write("#1,2026-10-29,https://example.com,unverified,foo\n")
    f.write("#1,2026-10-29,https://example.org,unverified,bar\n")
cmd = [sys.executable, SCRIPT, "tmp_dup.csv"]
res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                     text=True)
# Should fail with duplicate I.
if res.returncode != 1:
    sys.exit(1)

# Clean up
os.remove("tmp_dup.csv")
if os.path.exists(OUT):
    os.remove(OUT)

sys.exit(0)
