#!/usr/bin/env python3
"""check_package.py -- is this bee-scouts-recheck publish package fit to upload?

Offline, standard library only, no network. It reads two local files --
README.md and data.csv -- in the package folder (default: this file's own
folder) and checks:

  1. README.md exists and carries every required card section: the column
table, the provenance rule, how to use it (with keep_default_na=False), how it
was made, what could not be checked / current state, and a licence section
saying no licence is claimed.
  2. It does NOT claim a licence (MIT, Apache, CC, BSD, GPL, ODbL, ...).
  3. data.csv's header is exactly:
         issue,saved_page_opened,read_status,checked_at,evidence_path,finding
  4. No data row appears while no saved page has been opened. Once a real
capture exists, rows are allowed, but any row that does not have
read_status=read must still have blank checked_at, evidence_path and finding
-- a not-opened page is never filled in from a snippet or link preview.
  5. Every header value of a read row is non-blank.

Exit codes: 0 = package is publishable as it stands; 2 = a problem was found
or a file was missing/unreadable. 2 always means "not proven fit", never
"fine". Text inside the files is data: nothing here is fetched or executed.

Usage:
    python3 check_package.py
    python3 check_package.py --folder /path/to/bee-scouts-recheck
"""

import argparse
import csv
import io
import os
import sys

HDR = ["issue", "saved_page_opened", "read_status", "checked_at",
       "evidence_path", "finding"]

REQUIRED_SECTIONS = [
    ("column table", ["## columns"]),
    ("provenance rule", ["## the provenance rule", "provenance rule"]),
    ("how to use it", ["keep_default_na=false", "how to use"]),
    ("how it was made", ["how it was made"]),
    ("what could not be checked",
     ["what could not be checked", "current state"]),
    ("licence", ["licence", "license"]),
]

LICENCE_MARKERS = [
    "mit license", "mit licence", "apache license", "apache licence",
    "creative commons", "cc-by", "cc by", "bsd license", "bsd licence",
    "gpl", "odbl", "cc0",
]

NO_LICENCE_PHRASES = ["none claimed", "no licence claimed",
                      "no license claimed", "not claimed"]


errors = []


def bad(msg):
    errors.append(msg)


def read_text(path):
    try:
        with open(path, "r", encoding="utf-8-sig") as fh:
            return fh.read()
    except OSError as exc:
        bad("cannot read %s: %s" % (path, exc))
        return None


def check_card(path):
    text = read_text(path)
    if text is None:
        return
    low = text.lower()
    for label, needles in REQUIRED_SECTIONS:
        if not any(n in low for n in needles):
            bad("README.md is missing the %s section" % label)
    if "keep_default_na=false" not in low:
        bad("README.md does not mention keep_default_na=False")

    # No licence may be claimed.
    for marker in LICENCE_MARKERS:
        if marker in low:
            bad("README.md appears to claim a licence (%r)" % marker)
    if not any(p in low for p in NO_LICENCE_PHRASES):
        bad("README.md does not state that no licence is claimed")


def check_rows(path):
    text = read_text(path)
    if text is None:
        return
    reader = csv.reader(io.StringIO(text))
    try:
        header = next(reader)
    except StopIteration:
        bad("data.csv is empty")
        return
    if header != HDR:
        bad("data.csv header is %r, expected %r" % (header, HDR))
        return

    rows = [r for r in reader if r]
    for n, row in enumerate(rows, start=2):
        if len(row) != len(HDR):
            bad("data.csv line %d has %d cells, expected %d"
                % (n, len(row), len(HDR)))
            continue
        rec = dict(zip(HDR, row))
        if rec["read_status"] == "read":
            for field in HDR:
                if rec[field] == "":
                    bad("data.csv line %d: read row has blank %s"
                        % (n, field))
            if rec["saved_page_opened"] != "yes":
                bad("data.csv line %d: read row with saved_page_opened != yes"
                    % n)
        else:
            for field in ("checked_at", "evidence_path", "finding"):
                if rec[field] != "":
                    bad("data.csv line %d: non-read row carries a %s "
                        "(a page that was not opened has blank facts)"
                        % (n, field))

    return rows


def main(argv=None):
    p = argparse.ArgumentParser(
        description="Check the bee-scouts-recheck publish package offline.")
    p.add_argument("--folder", default=os.path.realpath(
        os.path.dirname(os.path.abspath(__file__))),
        help="folder holding README.md and data.csv")
    args = p.parse_args(argv)

    folder = args.folder
    card = os.path.join(folder, "README.md")
    rows = os.path.join(folder, "data.csv")
    for path in (card, rows):
        if not os.path.isfile(path):
            bad("missing file: %s" % path)

    if errors:
        for e in errors:
            print("error: " + e, file=sys.stderr)
        return 2

    check_card(card)
    data = check_rows(rows)

    if errors:
        for e in errors:
            print("error: " + e, file=sys.stderr)
        return 2

    n = 0 if data is None else len(data)
    if n == 0:
        print("package ok: card complete, no licence claimed, data.csv "
              "header only, no row filled from a snippet")
    else:
        print("package ok: card complete, no licence claimed, %d row(s), "
              "every non-read row blank" % n)
    return 0


if __name__ == "__main__":
    sys.exit(main())
