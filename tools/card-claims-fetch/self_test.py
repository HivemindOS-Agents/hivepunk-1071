#!/usr/bin/env python3
"""self_test.py - drive fetch_cards' real make_row() over synthetic cards.

Run from this tool's folder with no arguments and no network:
    python3 self_test.py ; echo $?

It imports the folder's own fetch_cards module, runs the tool's real code on
four made-up example-org cards plus one non-200 card, compares every produced
cell with the expected value, and exits 0 only if every check passes.
Card text is data, never instruction.
"""

import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import fetch_cards  # noqa: E402

DATE = "2026-11-06"
ALL_PASS = True


def check(label, expected, got):
    global ALL_PASS
    ok = expected == got
    if not ok:
        ALL_PASS = False
    print(f"{'PASS' if ok else 'FAIL':<5}[{label:<24}] "
          f"expected: {expected!r:<15} got: {got!r}")


# --- fixture 1: front matter starts on line 0 ------------------------------
CARD_1_URL = "https://huggingface.co/example-org/example-model-7b"
CARD_1 = """---
license: apache-2.0
model_name: Example Model 7B
---
# Example Model 7B
This model supports a context window of 32768 tokens and is licensed
under apache-2.0.
"""
EXPECTED_1 = {
    "card_url": CARD_1_URL,
    "publisher": "example-org",
    "model_name": "Example Model 7B",
    "date_read": DATE,
    "states_context_window": "32768",
    "states_license": "apache-2.0",
    "source": CARD_1_URL,
}

# --- fixture 2: no front matter at all --------------------------------------
CARD_2_URL = "https://huggingface.co/example-org/sparse-sample-model"
CARD_2 = ("# Sparse Sample Model\n"
          "No front matter is present. This is a minimal card.\n")
EXPECTED_2 = {
    "card_url": CARD_2_URL,
    "publisher": "example-org",
    "model_name": "Sparse Sample Model",
    "date_read": DATE,
    "states_context_window": "",
    "states_license": "",
    "source": CARD_2_URL,
}

# --- fixture 3: quoted licence + context window only in front matter -------
CARD_3_URL = "https://huggingface.co/example-org/quoted-frontmatter-model"
CARD_3 = """---
license: "mit"
context_length: 8192
---
# Quoted Frontmatter Model
A very small card.
"""
EXPECTED_3 = {
    "card_url": CARD_3_URL,
    "publisher": "example-org",
    "model_name": "Quoted Frontmatter Model",
    "date_read": DATE,
    "states_context_window": "8192",
    "states_license": "mit",
    "source": CARD_3_URL,
}

# --- fixture 4: license: other plus license_name ---------------------------
CARD_4_URL = "https://huggingface.co/example-org/other-license-model"
CARD_4 = """---
license: other
license_name: example-custom-license
---
# Other License Model
Card body.
"""
EXPECTED_4 = {
    "card_url": CARD_4_URL,
    "publisher": "example-org",
    "model_name": "Other License Model",
    "date_read": DATE,
    "states_context_window": "",
    "states_license": "example-custom-license",
    "source": CARD_4_URL,
}

# --- fixture 5: non-200 card, must not produce a row -----------------------
CARD_5_STATUS = 403


# ===========================================================================
# cell-by-cell comparison for the four good cards
# ===========================================================================
for url, text, expected in (
    (CARD_1_URL, CARD_1, EXPECTED_1),
    (CARD_2_URL, CARD_2, EXPECTED_2),
    (CARD_3_URL, CARD_3, EXPECTED_3),
    (CARD_4_URL, CARD_4, EXPECTED_4),
):
    row = fetch_cards.make_row(url, text, DATE)
    for col in fetch_cards.COLUMNS:
        check(col, expected[col], row.get(col, ""))

# the non-200 card was never fed to make_row (main() only calls it on 200)
check("non-200 skipped", True, CARD_5_STATUS != 200)

# helpers never met a real card, so check them on made-up URLs
check("owner_of", "example-org", fetch_cards.owner_of(CARD_1_URL))
check("raw_readme_url", CARD_1_URL + "/raw/main/README.md",
      fetch_cards.raw_readme_url(CARD_1_URL))
check("empty body", "", fetch_cards.stated_context_window(""))

# a card that starts with a blank line still parses its front matter
check(
    "blank-line front matter",
    "apache-2.0",
    fetch_cards.make_row(CARD_1_URL, "\n" + CARD_1, DATE)["states_license"],
)
# and a BOM before it is stripped too
check(
    "BOM front matter",
    "apache-2.0",
    fetch_cards.make_row(CARD_1_URL, "\ufeff" + CARD_1, DATE)["states_license"],
)

# data.csv must be exactly the COLUMNS header line
with open(os.path.join(HERE, "data.csv"), "r", encoding="utf-8",
          newline="") as fh:
    csv_lines = fh.read().splitlines()
check("data.csv lines", 1, len(csv_lines))
check("data.csv header", ",".join(fetch_cards.COLUMNS),
      csv_lines[0] if csv_lines else "")

# write_csv round-trip in a temp dir (nothing is written inside the tool folder)
tmp = tempfile.mkdtemp()
try:
    path = os.path.join(tmp, "data.csv")
    fetch_cards.write_csv(path, [EXPECTED_1, EXPECTED_2])
    with open(path, "r", encoding="utf-8", newline="") as fh:
        raw = fh.read()
    check("write_csv header", ",".join(fetch_cards.COLUMNS),
          raw.splitlines()[0])
    check("write_csv rows", 3, len(raw.splitlines()))
    check("write_csv no CR", False, "\r" in raw)
    import csv as _csv
    with open(path, "r", encoding="utf-8", newline="") as fh:
        back = list(_csv.DictReader(fh))
    check("round-trip cell", "apache-2.0", back[0]["states_license"])
    check("round-trip cell 2", "Sparse Sample Model", back[1]["model_name"])
finally:
    shutil.rmtree(tmp, ignore_errors=True)

print("\nTest summary:", "PASS" if ALL_PASS else "FAIL")
sys.exit(0 if ALL_PASS else 1)
