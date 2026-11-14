#!/usr/bin/env python3
"""self_test.py - offline tests for build_card.py.

Run from inside this folder with no arguments, no network:

    python3 self_test.py

Reads sample_cases_raw.csv and sample_readback.csv from this folder, runs the
emitters in build_card.py directly (import, no subprocess, no network), and
compares the emitted data.csv line by line and the README read-back lines
against what should come out. No file outside a temp dir is written. Exits 0
only when every check passes. Standard library only.

Row order in sample_cases_raw.csv is part of the contract this test pins:

    line 1  chunk-data-padded-to-4   opened, quoted byte expression
    line 2  header-length-12         opened
    line 3  future-not-yet-read      source is the literal 'not-opened'
    line 4  no-source-row            source is empty

Assertions read emitted rows by parsed position, not by a string prefix, so
a quoting change in the sample cannot silently desynchronise them.
"""

import csv
import io
import os
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import build_card as bc  # noqa: E402

CHECKS = 0
PASSED = 0


def check(condition, label):
    global CHECKS, PASSED
    CHECKS += 1
    if not condition:
        print("FAIL: %s" % label)
        return
    PASSED += 1
    print("ok: %s" % label)


def lines_of(text):
    return text.strip("\n").split("\n")


def rows_of(text):
    """Parse emitted CSV text into header + list of dicts."""
    reader = csv.reader(io.StringIO(text))
    all_rows = list(reader)
    header = all_rows[0]
    return header, [dict(zip(header, r)) for r in all_rows[1:]]


def main():
    raw_csv = (HERE / "sample_cases_raw.csv").read_text(encoding="utf-8")
    readback_csv = (HERE / "sample_readback.csv").read_text(encoding="utf-8")

    rows = bc.read_raw_rows(raw_csv)
    check(len(rows) == 4, "sample has 4 raw case rows (got %d)" % len(rows))

    data_csv = bc.emit_data_csv(rows)
    out_lines = lines_of(data_csv)

    # Header first, exact column order.
    check(
        out_lines[0] == "case_id,rule,expected_bytes,source,read_back",
        "data.csv header is case_id,rule,expected_bytes,source,read_back",
    )

    header, emitted = rows_of(data_csv)
    check(len(emitted) == 4, "data.csv has 4 data rows (got %d)" % len(emitted))

    # --- row 0: opened, rule and byte expression kept verbatim ---
    r0 = emitted[0]
    check(
        r0["case_id"] == "chunk-data-padded-to-4",
        "row 0 is chunk-data-padded-to-4",
    )
    check(
        r0["rule"].startswith("chunk data is padded"),
        "opened row keeps its rule text",
    )
    check(
        r0["expected_bytes"] == "(len+3) AND NOT 3",
        "opened row keeps its 4-byte alignment expression as text",
    )
    check(
        '"(len+3) AND NOT 3"' in out_lines[1],
        "the alignment expression is quoted in the raw CSV text",
    )
    check(r0["read_back"] == "opened", "opened row says opened")

    # --- row 1: second opened row keeps its integer byte count ---
    r1 = emitted[1]
    check(r1["case_id"] == "header-length-12", "row 1 is header-length-12")
    check(r1["expected_bytes"] == "12", "row 1 keeps its byte count 12")
    check(r1["read_back"] == "opened", "row 1 says opened")

    # --- row 2: page not opened -> rewritten, decoy text dropped ---
    r2 = emitted[2]
    check(r2["case_id"] == "future-not-yet-read", "row 2 is the unopened row")
    check(r2["rule"] == "not-opened", "unopened row says not-opened in rule")
    check(
        r2["expected_bytes"] == "not-opened",
        "unopened row says not-opened in expected_bytes",
    )
    check(
        r2["source"] == "not-opened",
        "unopened row says not-opened in source",
    )
    check(
        r2["read_back"] == "not-opened",
        "unopened row says not-opened in read_back",
    )
    check(
        "decoy-rule" not in data_csv,
        "unopened row's rule text is dropped, not carried through",
    )
    check(
        "2048" not in out_lines[3],
        "unopened row gets no invented byte count",
    )

    # --- row 3: empty source is also not-opened ---
    r3 = emitted[3]
    check(r3["case_id"] == "no-source-row", "row 3 is the empty-source row")
    check(r3["rule"] == "not-opened", "empty-source row says not-opened")
    check(
        "decoy-rule-2" not in data_csv,
        "empty-source row's rule text is dropped too",
    )

    # A comma inside a quoted cell does not shift columns.
    check(
        bc.split_csv_line(out_lines[1])[1] == "chunk data is padded to 4 bytes",
        "a comma inside a quoted cell does not shift columns",
    )

    # One header plus four cases.
    check(len(out_lines) == 5, "data.csv is 5 lines (1 header + 4 rows)")

    # Read-back rendering, opened and not-opened branches.
    rb = bc.read_readback(readback_csv)
    check(len(rb) == 2, "readback sample has 2 file rows")
    card = bc.emit_readback_lines(rb, data_csv)
    check(
        "data.csv" in card and "sha256" in card,
        "read-back names data.csv and carries a sha256 field",
    )
    check(
        "5 lines" in card,
        "read-back carries the emitted data.csv line count",
    )
    check(
        "not-opened" in card,
        "read-back marks the unfetched README.md as not-opened",
    )

    # A hand-typed hash-shaped string must not be accepted as a read-back.
    check(
        not bc.looks_like_sha256("manual-claim"),
        "a non-hex string is not treated as a sha256",
    )
    check(
        bc.looks_like_sha256("a" * 64),
        "a 64-char hex string is treated as a sha256",
    )

    # write_outputs lands both files in a temp dir.
    tmpd = tempfile.mkdtemp(prefix="glb-pad-cases-self-test-")
    paths = bc.write_outputs(rows, rb, tmpd)
    check(os.path.isfile(paths["data_csv"]), "data.csv is written")
    check(os.path.isfile(paths["readme"]), "README.md is written")
    written = Path(paths["data_csv"]).read_text(encoding="utf-8")
    check(written == data_csv, "written data.csv matches the emitted text")

    print("\nResults: %d/%d checks passed" % (PASSED, CHECKS))
    return 0 if PASSED == CHECKS else 1


if __name__ == "__main__":
    sys.exit(main())
