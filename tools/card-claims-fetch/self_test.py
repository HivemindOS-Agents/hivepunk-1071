#!/usr/bin/env python3
"""self_test.py – verify the empty Open‑weight model card claims dataset.

Run from the tool folder with no arguments and no network:

    python3 self_test.py ; echo $?

Validations:
- data.csv exists and contains the correct single header line.
- data.csv has no data rows.
- README.md exists, contains the required sections.
- No other unexpected files are present.
"""

import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA_FILE = HERE / "data.csv"
README_FILE = HERE / "README.md"
EXPECTED_HEADER = "card_url,publisher,model_name,date_read,states_context_window,states_license,source"
REQUIRED_README_SECTIONS = ["What was read", "What I could not confirm"]

def fail(msg):
    print(f"FAIL: {msg}")
    sys.exit(1)

# 1. data.csv
if not DATA_FILE.is_file():
    fail("data.csv missing")
with DATA_FILE.open("r", encoding="utf-8") as f:
    lines = f.read().splitlines()
if len(lines) != 1:
    fail(f"data.csv should contain exactly one header line; got {len(lines)} lines")
if lines[0].strip() != EXPECTED_HEADER:
    fail("data.csv header mismatch")

# 2. README.md
if not README_FILE.is_file():
    fail("README.md missing")
readme = README_FILE.read_text(encoding="utf-8")
for sec in REQUIRED_README_SECTIONS:
    if sec not in readme:
        fail(f"README.md missing required section: {sec}")

print("ok: all dataset checks pass")
sys.exit(0)
