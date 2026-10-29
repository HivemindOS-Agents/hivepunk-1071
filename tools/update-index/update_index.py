#!/usr/bin/env python3
"""update_index.py -- turn a re-check log CSV into data/issues.csv.

STATUS: UNTESTED. This file has never been executed, here or anywhere else.
Every expected-output line in README.md was traced by hand from the code below
rather than captured from a run. Treat statements about its behaviour as claims
to test, not as facts.

What it does
------------
Reads a re-check log CSV whose rows carry the fixed five fields

    Issue, Date checked, Page opened, Status, What it showed

and writes the index out as CSV: a header plus exactly one row per issue, in
those same five fields, sorted naturally by issue number (#9 before #12).

Validation – exit 1, nothing written, every offending line named
---------------------------------------------------------------
  * one of the five required columns is missing from the header
  * Issue, Date checked, Page opened or What it showed is empty
  * Status is not one of: unverified / verified / cannot-check
  * Date checked is not a real calendar date in strict YYYY-MM-DD form
  * the same Issue value appears on more than one row
  * the header is fine but the file holds no data rows

Nothing else exits 1. Columns past the five are ignored, not an error;
a row with more fields than the header earns a warning and its extras are dropped.

Page opened is free text by design. A URL, a snippet note, or an honest
"not opened -- …" line are all accepted and recorded verbatim.

What it does NOT do
-------------------
Standard library only, local files only, no network call, no upload, nothing
run against anyone's systems. It never opens the page in Page opened.

Exit codes: 0 ok; 1 validation failed, nothing written; 2 usage or I/O error.
"""

import argparse
import csv
import datetime
import os
import re
import sys

REQUIRED = ["Issue", "Date checked", "Page opened", "Status", "What it showed"]
STATUSES = ("unverified", "verified", "cannot-check")
RE_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
RE_ISSUE_NUM = re.compile(r"#(\d+)\s*$")
RE_NOT_OPENED = re.compile(r"^not\s+opened\b", re.IGNORECASE)
RE_URL = re.compile(r"^https?://", re.IGNORECASE)


def parse_args(argv):
    parser = argparse.ArgumentParser(
        description="Validate a re-check log CSV and write data/issues.csv.")
    parser.add_argument("input", help="re-check log CSV to read")
    parser.add_argument("-o", "--out", default=os.path.join("data", "issues.csv"),
                        help="output CSV path (default: data/issues.csv)")
    parser.add_argument("--dry-run", action="store_true",
                        help="validate and report only; write nothing")
    return parser.parse_args(argv)


def sort_key(row):
    """Natural sort: repo#9 before repo#12; non-numeric Issue values last."""
    match = RE_ISSUE_NUM.search(row["Issue"])
    if match:
        return (0, row["Issue"][:match.start()].lower(), int(match.group(1)))
    return (1, row["Issue"].lower(), 0)


def check_date(value, lineno, errors):
    """A real YYYY-MM-DD calendar date, or an error."""
    if not RE_DATE.match(value):
        errors.append('line %d: Date checked %r is not YYYY-MM-DD' % (lineno, value))
        return
    try:
        datetime.datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        errors.append('line %d: Date checked %r is YYYY-MM-DD shaped but not a real '
                      'calendar date' % (lineno, value))


def read_rows(path):
    """Return (rows, errors, warnings). Raises OSError if the file cannot be read."""
    errors, warnings, rows, seen = [], [], [], {}

    with open(path, newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        raw_header = reader.fieldnames
        if not raw_header:
            return [], ["%s: file is empty -- no header row" % path], warnings

        header = [name.strip() for name in raw_header]
        missing = [name for name in REQUIRED if name not in header]
        if missing:
            return [], ["%s: header is %s; missing required column(s): %s"
                        % (path, raw_header, ", ".join(missing))], warnings
        by_name = dict(zip(header, raw_header))

        for lineno, raw in enumerate(reader, start=2):
            if raw is None:
                continue
            if not any((value or "").strip() for value in raw.values()):
                continue
            if raw.get(None):
                warnings.append("line %d: %d extra field(s) past the header; ignored"
                                % (lineno, len(raw[None])))
            row = dict((name, (raw.get(by_name[name]) or "").strip()) for name in REQUIRED)

            empty = [name for name in REQUIRED if name != "Status" and not row[name]]
            if empty:
                errors.append("line %d: empty %s"
                              % (lineno, " and ".join("'%s'" % name for name in empty)))
            if row["Status"] not in STATUSES:
                errors.append("line %d: Status %r is not one of %s"
                              % (lineno, row["Status"], " / ".join(STATUSES)))
            if row["Date checked"]:
                check_date(row["Date checked"], lineno, errors)
            if row["Issue"]:
                seen.setdefault(row["Issue"], []).append(lineno)
            opened = row["Page opened"]
            if opened and not (RE_URL.match(opened) or RE_NOT_OPENED.match(opened)
                               or "snippet" in opened.lower()):
                warnings.append('line %d: Page opened %r is not a URL, a snippet note or a '
                                '"not opened" line; recorded as written'
                                % (lineno, opened[:60]))
            rows.append(row)

    for issue in sorted(seen):
        lines = seen[issue]
        if len(lines) > 1:
            errors.append("duplicate Issue %r on lines %s (one row per issue is required)"
                          % (issue, ", ".join(str(n) for n in lines)))

    if not rows and not errors:
        errors.append("%s: header ok but no data rows" % path)
    return rows, errors, warnings


def report_counts(rows):
    for status in STATUSES:
        count = sum(1 for row in rows if row["Status"] == status)
        print("  %-13s %d" % (status, count))


def write_csv(path, rows):
    parent = os.path.dirname(os.path.abspath(path))
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=REQUIRED,
                                lineterminator="\n", quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def main(argv=None):
    args = parse_args(sys.argv[1:] if argv is None else argv)
    try:
        rows, errors, warnings = read_rows(args.input)
    except OSError as exc:
        print("error: cannot read %s: %s" % (args.input, exc), file=sys.stderr)
        return 2

    for warning in warnings:
        print("warning: " + warning, file=sys.stderr)
    if errors:
        print("validation failed, nothing written:", file=sys.stderr)
        for line in errors:
            print("  " + line, file=sys.stderr)
        return 1

    rows.sort(key=sort_key)
    if args.dry_run:
        print("%d rows valid; dry run, nothing written" % len(rows))
        report_counts(rows)
        return 0

    try:
        write_csv(args.out, rows)
    except OSError as exc:
        print("error: cannot write %s: %s" % (args.out, exc), file=sys.stderr)
        return 2

    print("wrote %s: %d rows" % (args.out, len(rows)))
    report_counts(rows)
    return 0


if __name__ == "__main__":
    sys.exit(main())
