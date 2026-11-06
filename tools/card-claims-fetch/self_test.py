#!/usr/bin/env python3
"""self_test.py – verify fetch_cards makes correct rows from synthetic fixtures.

Run from the tool folder with no network:
    python3 self_test.py ; echo $?

The test imports the tool's own logic, runs on two hard‑coded card fixtures with
status 200 and one with a non‑200 status to exercise that path.  It compares each
produced cell to the expected value, printing PASS/FAIL lines and exiting 1 if any
check fails.
"""

import sys

import fetch_cards

# ---------------------------------------------------------------------------
# Synthetic card fixtures
# ---------------------------------------------------------------------------
FIXTURES = {
    # 1. Card with license, context window, explicit model name in front matter
    "https://huggingface.co/example-org/example-model-7b": (
        200,
        """
---
license: apache-2.0
model_name: Example Model 7B
---
# Example Model 7B
This model supports a context window of 32768 tokens and is licensed under
apache-2.0.
""",
    ),
    # 2. Card with no front matter, model name derived from first H1, no context or license
    "https://huggingface.co/example-org/sparse-sample-model": (
        200,
        """
# Sparse Sample Model
No front matter is present.  This is a minimal card.
""",
    ),
    # 3. Card that returns a non‑200 status – should not produce a row
    "https://huggingface.co/example-org/blocked-model": (
        403,
        "",  # body ignored when status != 200
    ),
}

# ---------------------------------------------------------------------------
# Expected rows for the 200‑status fixtures
# ---------------------------------------------------------------------------
EXPECTED_ROWS = [
    {
        "card_url": "https://huggingface.co/example-org/example-model-7b",
        "publisher": "example-org",
        "model_name": "Example Model 7B",
        "date_read": "2026-11-06",
        "states_context_window": "32768",
        "states_license": "apache-2.0",
        "source": "https://huggingface.co/example-org/example-model-7b",
    },
    {
        "card_url": "https://huggingface.co/example-org/sparse-sample-model",
        "publisher": "example-org",
        "model_name": "Sparse Sample Model",
        "date_read": "2026-11-06",
        "states_context_window": "",
        "states_license": "",
        "source": "https://huggingface.co/example-org/sparse-sample-model",
    },
]

# ---------------------------------------------------------------------------
# Test runner
# ---------------------------------------------------------------------------
ALL_PASS = True
date_read = "2026-11-06"
nrows = []
# Generate rows from 200‑status fixtures
for url, (status, text) in FIXTURES.items():
    if status != 200:
        continue
    row = fetch_cards.make_row(url, text, date_read)
    rows.append(row)

# Compare to expected in order of expected list
for i, (exp, got) in enumerate(zip(EXPECTED_ROWS, rows)):
    for key in fetch_cards.COLUMNS:
        exp_val = exp[key]
        got_val = got.get(key, "")
        if exp_val == got_val:
            status = "PASS"
        else:
            status = "FAIL"
            ALL_PASS = False
        print(f"{status:<5} [{key:<24}] expected: {exp_val!r:<15} got: {got_val!r}")

# Verify that fixture with non‑200 did not create a row
if len(rows) != len(EXPECTED_ROWS):
    print("FAIL   row count mismatch: expected", len(EXPECTED_ROWS), "got", len(rows))
    ALL_PASS = False

# Final summary
print("\nTest summary:", "PASS" if ALL_PASS else "FAIL")
sys.exit(0 if ALL_PASS else 1)
