#!/usr/bin/env python3
"""update_index.py -- upkeep for the bee-scouts issue index (hivepunk-1071).

STATUS: UNTESTED. This file has never been executed. Nothing below has been
run against real data; review and test it before trusting its output.

What it does
------------
Reads a five-column issue-index CSV, checks the header, rejects duplicate
Issue values, checks the Status set and the Date checked calendar dates,
writes a normalised issues.csv sorted naturally by Issue (bee-scouts#9
before bee-scouts#10), and writes change_report.txt with an ADDED / REMOVED /
CHANGED diff against the previous issues.csv if one is already in the output
directory.

Parsing uses the csv module, so CRLF line endings, quoted fields and commas
inside quotes are handled the way a spreadsheet writes them.

What it does NOT do
-------------------
Standard library only, local files only, no network calls. It never opens
the pages named in "Page opened" and never runs anything against anyone's
systems. Those columns are recorded text, not verified by this tool.

Input header, exactly (comma-separated):
    Issue,Page opened,Date checked,Status,What it showed

Rules enforced
--------------
  Issue           repo#number, e.g. bee-scouts#39, and unique in the file
  Page opened     http:// or https:// URL
  Date checked    a real calendar date, strict YYYY-MM-DD
  Status          exactly one of unverified / verified / cannot-check
  What it showed  non-empty

Usage
-----
    python3 update_index.py INPUT.csv [-o OUTDIR]

Exit codes: 0 ok; 1 validation failed, nothing written; 2 usage or I/O error.
"""
import argparse
import csv
import datetime
import os
import re
import sys

HEADER = ["Issue", "Page opened", "Date checked", "Status", "What it showed"]
STATUSES = ("unverified", "verified", "cannot-check")
RE_ISSUE = re.compile(r"^[^#\s]+#\d+$")
RE_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def is_date(value):
    """True only for a strict YYYY-MM-DD that is a real calendar date."""
    if not RE_DATE.match(value):
        return False
    try:
        datetime.datetime.strptime(value, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def natkey(issue):
    """Natural sort key, so #9 sorts before #10."""
    if "#" in issue:
        repo, num = issue.rsplit("#", 1)
        if num.isdigit():
            return (0, repo.lower(), int(num))
    return (1, issue.lower(), 0)


def load(path):
    """Return (rows, errors). Any error means nothing gets written."""
    rows, errors, seen = [], [], {}
    with open(path, newline="", encoding="utf-8-sig") as fh:
        reader = csv.reader(fh)
        head = next(reader, None)
        if head is None:
            return [], ["%s: file is empty" % path]
        head = [h.strip() for h in head]
        if head != HEADER:
            return [], ["%s: header is %s, expected %s" % (path, head, HEADER)]
        for n, raw in enumerate(reader, start=2):
            if not any(cell.strip() for cell in raw):
                continue
            if len(raw) != len(HEADER):
                errors.append("line %d: %d fields, expected %d" % (n, len(raw), len(HEADER)))
                continue
            row = dict(zip(HEADER, [cell.strip() for cell in raw]))
            seen.setdefault(row["Issue"], []).append(n)
            if not RE_ISSUE.match(row["Issue"]):
                errors.append('line %d: Issue "%s" is not repo#number' % (n, row["Issue"]))
            if not row["Page opened"].lower().startswith(("http://", "https://")):
                errors.append('line %d: Page opened "%s" is not a URL' % (n, row["Page opened"]))
            if not is_date(row["Date checked"]):
                errors.append('line %d: Date checked "%s" is not a real YYYY-MM-DD date'
                              % (n, row["Date checked"]))
            if row["Status"] not in STATUSES:
                errors.append('line %d: Status "%s" is not one of %s'
                              % (n, row["Status"], " / ".join(STATUSES)))
            if not row["What it showed"]:
                errors.append("line %d: What it showed is empty" % n)
            rows.append(row)
    dups = []
    for issue in sorted(seen):
        lines = seen[issue]
        if len(lines) > 1:
            dups.append('duplicate Issue "%s" on lines %s'
                        % (issue, ", ".join(str(x) for x in lines)))
    return rows, dups + errors


def diff_report(before_rows, after_rows):
    """Plain-text ADDED / REMOVED / CHANGED lines, natural order by Issue."""
    before = {r["Issue"]: r for r in before_rows}
    after = {r["Issue"]: r for r in after_rows}
    lines = []
    for issue in sorted(set(after) - set(before), key=natkey):
        lines.append("ADDED   " + issue)
    for issue in sorted(set(before) - set(after), key=natkey):
        lines.append("REMOVED " + issue)
    for issue in sorted(set(before) & set(after), key=natkey):
        for field in HEADER:
            was = before[issue].get(field, "")
            now = after[issue].get(field, "")
            if was != now:
                lines.append("CHANGED %s %s: %r -> %r" % (issue, field, was, now))
    return lines or ["no changes"]


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Validate, natural-sort and diff a bee-scouts issue-index CSV.")
    parser.add_argument("input", help="issue-index CSV to check")
    parser.add_argument("-o", "--outdir", default=".",
                        help="directory for issues.csv and change_report.txt")
    args = parser.parse_args(argv)

    try:
        rows, errors = load(args.input)
    except OSError as exc:
        print("cannot read %s: %s" % (args.input, exc), file=sys.stderr)
        return 2

    if errors:
        print("validation failed, nothing written:", file=sys.stderr)
        for line in errors:
            print("  " + line, file=sys.stderr)
        return 1

    try:
        os.makedirs(args.outdir, exist_ok=True)
        rows.sort(key=lambda r: natkey(r["Issue"]))
        out_csv = os.path.join(args.outdir, "issues.csv")
        previous = []
        if os.path.exists(out_csv):
            with open(out_csv, newline="", encoding="utf-8-sig") as fh:
                previous = [r for r in csv.DictReader(fh) if r.get("Issue")]
        with open(out_csv, "w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=HEADER, lineterminator="\n")
            writer.writeheader()
            writer.writerows(rows)
        report = diff_report(previous, rows)
        report_path = os.path.join(args.outdir, "change_report.txt")
        with open(report_path, "w", encoding="utf-8") as fh:
            fh.write("issue index change report\n")
            fh.write("rows: %d (previous: %d)\n\n" % (len(rows), len(previous)))
            fh.write("\n".join(report) + "\n")
    except OSError as exc:
        print("write failed: %s" % exc, file=sys.stderr)
        return 2

    print("%d rows ok; wrote %s and %s" % (len(rows), out_csv, report_path))
    print("\n".join(report))
    return 0


if __name__ == "__main__":
    sys.exit(main())
