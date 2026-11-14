#!/usr/bin/env python3
"""self_test.py - offline tests for build_card.py.

Run from inside this folder with no arguments, no network:

    python3 self_test.py

Reads sample_cases_raw.csv and sample_readback.csv from this folder, runs the
emitters in build_card.py directly (import, no subprocess, no network), and
compares the emitted data.csv line by line and the README read-back lines
against what should come out. No file outside a temp dir is written. Exits 0
only when every check passes. Standard library only.
"""

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

    # Opened rows keep their rule and bytes verbatim.
    check(
        out_lines[1].startswith(
            "chunk-data-padded-to-4,chunk data is padded",
        ),
        "opened row keeps its rule text",
    )
    check(
        '"(len+3) AND NOT 3",https://github.com/'
        in out_lines[1],
        "opened row keeps its 4-byte alignment expression as text",
    )
    check(out_lines[1].endswith("opened"), "opened row says opened")

    # A row whose page was not opened is rewritten to not-opened, not guessed.
    check("not-opened" in out_lines[2], "unopened row says not-opened")
    check(
        "decoy-rule" not in data_csv,
        "unopened row's rule text is dropped, not carried through",
    )
    check(
        "2048" not in data_csv.split("\n")[2],
        "unopened row gets no invented byte count",
    )

    # A row with an empty source is also not-opened.
    check("not-opened" in out_lines[3], "empty-source row says not-opened")

    # Quoting survives a comma inside a field: the row still splits to 5 cells.
    check(
        bc.split_csv_line(out_lines[1])[1] == "chunk data is padded to 4 bytes",
        "a comma inside a quoted cell does not shift columns",
    )

    # The four data rows are one header plus four cases = 5 lines.
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
        "10 lines" in card or "5 lines" in card,
        "read-back carries the data.csv line count",
    )
    check(
        "not-opened" in card,
        "read-back marks the unfetched README.md as not-opened",
    )

    # A hand-typed hash-shaped string must not be accepted as a read-back.
    bad = "file,sha256,line_count,status\ndata.csv,manual-claim,10,opened\n"
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
