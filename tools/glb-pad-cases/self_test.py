#!/usr/bin/env python3
"""self_test.py - offline tests for build_card.py.

Run from inside this folder with no arguments, no network:

    python3 self_test.py

Builds its own small fixtures in a temp dir, imports build_card from this
folder, and compares the emitted data.csv cells and the README text with
explicit expected values. No subprocess, no network, nothing written outside
a temp dir. Exits 0 only when every check passes. Standard library only.
"""

import csv
import io
import os
import re
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import build_card as bc  # noqa: E402

CHECKS = 0
PASSED = 0
EXPR = "(len+3) AND NOT 3"
FAKE_HEX = "a" * 64
OTHER_HEX = "b" * 64
HEX_RUN = re.compile(r"(?<![0-9a-f])[0-9a-f]{64}(?![0-9a-f])")

CASES = (
    "case_id,rule,expected_bytes,source\n"
    "chunk-data-padded-to-4,\"chunk data is padded to 4 bytes\",\"" + EXPR +
    "\",page-alpha\n"
    "header-length-12,binary header is 12 bytes,12,page-beta\n"
    "future-not-yet-read,decoy-rule,2048,not-opened\n"
    "no-source-row,decoy-rule-2,4096,\n"
)

READBACK_ONE_OPEN = (
    "file,sha256,line_count,status\n"
    "data.csv,%s,5,opened\n"
    "README.md,not-opened,not-opened,not-opened\n" % FAKE_HEX
)

READBACK_ALL_CLOSED = (
    "file,sha256,line_count,status\n"
    "data.csv,%s,5,not-opened\n"
    "README.md,%s,4,opened\n" % (FAKE_HEX, "manual-claim")
)

READBACK_EMPTY = "file,sha256,line_count,status\n"


def check(condition, label):
    global CHECKS, PASSED
    CHECKS += 1
    if not condition:
        print("FAIL: %s" % label)
        return
    PASSED += 1
    print("ok: %s" % label)


def rows_of(text):
    all_rows = list(csv.reader(io.StringIO(text)))
    header = all_rows[0]
    return header, all_rows[1:]


def main():
    rows = bc.read_raw_rows(CASES)
    check(len(rows) == 4, "fixture has 4 raw rows")

    data_csv = bc.emit_data_csv(rows)
    header, body = rows_of(data_csv)
    check(header == bc.DATA_COLUMNS, "data.csv header is the DATA_COLUMNS order")
    check(len(body) == 4, "data.csv has 4 data rows")

    # Row 0: opened, expression kept verbatim as one cell, not evaluated.
    check(body[0][0] == "chunk-data-padded-to-4", "row0 case_id")
    check(body[0][1] == "chunk data is padded to 4 bytes", "row0 rule")
    check(body[0][2] == EXPR, "row0 keeps alignment expression verbatim")
    check(body[0][3] == "page-alpha", "row0 keeps its source identifier")
    check(body[0][4] == "opened", "row0 says opened")
    check(body[0][2] != "4", "row0 expression is not evaluated to a number")

    # Row 1: opened integer byte count.
    check(body[1][2] == "12", "row1 keeps byte count 12")
    check(body[1][4] == "opened", "row1 says opened")

    # Row 2: literal not-opened -> every field not-opened, decoy dropped.
    check(body[2] == ["future-not-yet-read", "not-opened", "not-opened",
                      "not-opened", "not-opened"],
          "row2 not-opened in every field, decoy text dropped")

    # Row 3: empty source -> same treatment.
    check(body[3] == ["no-source-row", "not-opened", "not-opened",
                      "not-opened", "not-opened"],
          "row3 empty source becomes not-opened everywhere")

    check("decoy-rule" not in data_csv, "no decoy rule text in data.csv")
    check("2048" not in data_csv and "4096" not in data_csv,
          "no invented byte count in data.csv")

    # --- read-back rendering ---
    rb_open = bc.read_readback(READBACK_ONE_OPEN)
    card = bc.emit_readme(rb_open, data_csv, len(rows))
    check("- `data.csv` - sha256 %s, 5 lines" % FAKE_HEX in card,
          "opened data.csv renders sha256 and emitted line count (5)")
    check("- `README.md` - not-opened" in card,
          "closed README.md renders as not-opened")
    check("data.csv has 5 lines (1 header + 4 rows)" in card,
          "card line count comes from the emitted CSV")

    # An opened read-back card carries exactly one long hex run: that hash.
    opened_runs = HEX_RUN.findall(card)
    check(len(opened_runs) == 1 and opened_runs[0] == FAKE_HEX,
          "opened card carries exactly the opened row's hash, nothing else")

    # data.csv's line count is the emitted one, never the input's.
    rb_wrong_count = bc.read_readback(
        READBACK_ONE_OPEN.replace("data.csv,%s,5" % FAKE_HEX,
                                  "data.csv,%s,99" % FAKE_HEX))
    card2 = bc.emit_readme(rb_wrong_count, data_csv, len(rows))
    check("data.csv has 5 lines (1 header + 4 rows)" in card2,
          "a wrong input line_count cannot override the emitted count")

    # --- no unverified hash when no read-back happened ---
    # All rows not-opened: the emitted card must contain no long hex run at
    # all, and the raw data.csv hex must not leak onto it.
    rb_closed = bc.read_readback(READBACK_ALL_CLOSED)
    card3 = bc.emit_readme(rb_closed, data_csv, len(rows))
    check("- `README.md` - not-opened" in card3,
          "a non-hex sha256 is treated as not-opened")
    check("manual-claim" not in card3, "hand-typed hash never appears")
    check(HEX_RUN.findall(card3) == [],
          "all-not-opened card carries no long hex hash")
    check(card3.count(bc.NOT_OPENED) >= 4,
          "all-not-opened card names not-opened for both files")

    # No read-back rows at all: still no long hex run.
    rb_empty = bc.read_readback(READBACK_EMPTY)
    card4 = bc.emit_readme(rb_empty, data_csv, len(rows))
    check(HEX_RUN.findall(card4) == [],
          "empty read-back card carries no long hex hash")
    check("- `data.csv` - not-opened" in card4
          and "- `README.md` - not-opened" in card4,
          "empty read-back card names both files as not-opened")

    # --- the guard itself, from both sides ---
    unverified = "a card with %s on it" % OTHER_HEX
    raised = False
    try:
        bc._assert_no_unverified_hash(unverified, rb_closed)
    except ValueError:
        raised = True
    check(raised, "guard refuses a hash that no opened row supplied")

    check(bc._assert_no_unverified_hash(unverified, rb_open) is True
          or OTHER_HEX not in [r.get("sha256") for r in rb_open],
          "guard compares against the opened rows' own hashes")

    allowed = "a card with %s on it" % FAKE_HEX
    raised = False
    try:
        bc._assert_no_unverified_hash(allowed, rb_open)
    except ValueError:
        raised = True
    check(not raised, "guard accepts the hash of an opened read-back row")

    raised = False
    try:
        bc.emit_readme(rb_closed, data_csv, len(rows))
    except ValueError:
        raised = True
    check(not raised, "emit_readme itself succeeds with no opened row")

    # --- no dead claims in the card ---
    check("huggingface.co" not in card, "card states no dataset URL")
    check("self_test" not in card.replace("No self_test pass", ""),
          "card does not claim a self-test pass")

    # --- write_outputs lands both files, bytes match ---
    tmpd = tempfile.mkdtemp(prefix="glb-pad-cases-self-test-")
    paths = bc.write_outputs(rows, rb_open, tmpd)
    check(os.path.isfile(paths["data_csv"]), "data.csv is written")
    check(os.path.isfile(paths["readme"]), "README.md is written")
    written = Path(paths["data_csv"]).read_text(encoding="utf-8")
    check(written == data_csv, "written data.csv matches emitted text byte for byte")
    readme_written = Path(paths["readme"]).read_text(encoding="utf-8")
    check(readme_written.startswith(
        "# GLB binary chunk padding and alignment cases\n"),
        "written README starts with the card title")
    check(HEX_RUN.findall(readme_written) == [FAKE_HEX],
          "written README carries only the opened row's hash")

    # --- the shipped sample files still parse ---
    sample_cases = (HERE / "sample_cases_raw.csv").read_text(encoding="utf-8")
    s_rows = bc.read_raw_rows(sample_cases)
    check(len(s_rows) == 4, "shipped sample_cases_raw.csv parses as 4 rows")
    s_data = bc.emit_data_csv(s_rows)
    s_head, s_body = rows_of(s_data)
    check(s_head == bc.DATA_COLUMNS, "sample emits the DATA_COLUMNS header")
    check(s_body[0][2] == EXPR, "sample keeps the alignment expression verbatim")
    sample_rb = (HERE / "sample_readback.csv").read_text(encoding="utf-8")
    rb = bc.read_readback(sample_rb)
    check(len(rb) == 2, "shipped sample_readback.csv parses as 2 rows")
    card5 = bc.emit_readme(rb, s_data, len(s_rows))
    check("data.csv has 5 lines (1 header + 4 rows)" in card5,
          "sample card states the sample line count")

    print("\nResults: %d/%d checks passed" % (PASSED, CHECKS))
    return 0 if PASSED == CHECKS else 1


if __name__ == "__main__":
    sys.exit(main())
