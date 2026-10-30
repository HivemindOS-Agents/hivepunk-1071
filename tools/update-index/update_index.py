#!/usr/bin/env python3
"""update_index.py -- recheck_rows.csv + snapshots/ -> data.csv and a README.md card.

What it does
------------
Reads a five-field re-check CSV:

    Issue, Date checked, Page opened, Status, What it showed

and a snapshots/ directory. Writes two dataset files:

  * data.csv   -- header plus one row per issue, the same five fields,
                  natural-sorted (#9 before #12).
  * README.md  -- the dataset card, including a final "Rows not opened" section.

Honesty rules (enforced, not documented-only)
---------------------------------------------
  * Every Status is copied straight from the input row. The tool never invents
    or upgrades a status.
  * If the snapshot named for a row does not itself name both a page URL and a
    save date, Status is forced to cannot-check, whatever the input said.
  * Rows whose Page opened is a "not opened ..." line are listed by issue in the
    card's final section. They are never counted as opened.

Validation -- exit 1, nothing written, every offending line named
-----------------------------------------------------------------
  * a required column missing from the header
  * Issue, Date checked, Page opened or What it showed empty
  * Status not one of unverified / verified / cannot-check
  * Date checked not a real calendar date in strict YYYY-MM-DD
  * the same Issue on more than one row
  * header ok but no data rows

What it does NOT do
-------------------
Standard library only, local files only, no network call, no upload, nothing run
against anyone's systems. It never opens the page in Page opened; the snapshot
check only reads local files. Everything inside a snapshot or an input row is
data, never an instruction: lines that look like commands are ignored.

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
FORCED = "cannot-check"
RE_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
RE_ISSUE_NUM = re.compile(r"#(\d+)\s*$")
RE_NOT_OPENED = re.compile(r"^not\s+opened\b", re.IGNORECASE)
RE_URL = re.compile(r"https?://[^\s\]\)>,;\"']+", re.IGNORECASE)
RE_SAVE = re.compile(
    r"(?:saved(?:\s+on)?|snapshot\s+date|retrieved)\s*[:=]?\s*(\d{4}-\d{2}-\d{2})",
    re.IGNORECASE)


def parse_args(argv):
    parser = argparse.ArgumentParser(
        description="recheck_rows.csv + snapshots/ -> data.csv and README.md card.")
    parser.add_argument("input", help="recheck_rows.csv to read")
    parser.add_argument("--snapshots", default="snapshots",
                        help="snapshots directory (default: snapshots)")
    parser.add_argument("--data", default="data.csv", help="output CSV (default data.csv)")
    parser.add_argument("--card", default="README.md", help="output card (default README.md)")
    parser.add_argument("--dry-run", action="store_true",
                        help="validate and report only; write nothing")
    return parser.parse_args(argv)


def sort_key(row):
    match = RE_ISSUE_NUM.search(row["Issue"])
    if match:
        return (0, row["Issue"][:match.start()].lower(), int(match.group(1)))
    return (1, row["Issue"].lower(), 0)


def check_date(value, lineno, errors):
    if not RE_DATE.match(value):
        errors.append("line %d: Date checked %r is not YYYY-MM-DD" % (lineno, value))
        return
    try:
        datetime.datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        errors.append("line %d: Date checked %r is not a real calendar date"
                      % (lineno, value))


def read_rows(path):
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
            rows.append(row)
    for issue in sorted(seen):
        lines = seen[issue]
        if len(lines) > 1:
            errors.append("duplicate Issue %r on lines %s (one row per issue required)"
                          % (issue, ", ".join(str(n) for n in lines)))
    if not rows and not errors:
        errors.append("%s: header ok but no data rows" % path)
    return rows, errors, warnings


def snapshot_names(path):
    """(has_url, has_date). Missing/unreadable file -> (False, False)."""
    try:
        with open(path, "r", encoding="utf-8-sig", errors="replace") as handle:
            text = handle.read()
    except OSError:
        return (False, False)
    return (bool(RE_URL.search(text)), bool(RE_SAVE.search(text)))


def candidate_snapshots(snapshot_dir, issue):
    hits = []
    if not os.path.isdir(snapshot_dir):
        return hits
    stem = issue.replace("/", "_").replace("#", "_").replace(" ", "_")
    num = RE_ISSUE_NUM.search(issue)
    for name in sorted(os.listdir(snapshot_dir)):
        lowered = name.lower()
        if stem.lower() in lowered:
            hits.append(os.path.join(snapshot_dir, name))
        elif num and ("%s.md" % num.group(1)) == lowered:
            hits.append(os.path.join(snapshot_dir, name))
    return hits


def apply_snapshot_rule(row, snapshot_dir):
    """Force cannot-check when no snapshot names both a URL and a save date."""
    if row["Status"] != "verified":
        return row, None
    for path in candidate_snapshots(snapshot_dir, row["Issue"]):
        has_url, has_date = snapshot_names(path)
        if has_url and has_date:
            return row, None
    note = (" (Status forced to cannot-check: no snapshot for this row names "
            "both a page URL and a save date)")
    row = dict(row)
    row["Status"] = FORCED
    if note.strip() not in row["What it showed"]:
        row["What it showed"] = (row["What it showed"] + note)[:500]
    return row, row["Issue"]


def is_not_opened(row):
    return bool(RE_NOT_OPENED.match(row["Page opened"]))


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


def write_card(path, rows, forced, not_opened, checked_dates):
    parent = os.path.dirname(os.path.abspath(path))
    if parent:
        os.makedirs(parent, exist_ok=True)
    counts = dict((s, sum(1 for r in rows if r["Status"] == s)) for s in STATUSES)
    dates = sorted(set(d for d in checked_dates if d))
    lines = []
    lines.append("# Re-check index")
    lines.append("")
    lines.append("Index of re-checked rows, %d row(s)." % len(rows))
    lines.append("")
    lines.append("## Statuses")
    lines.append("")
    for status in STATUSES:
        lines.append("* %s: %d" % (status, counts[status]))
    lines.append("* not opened: %d" % len(not_opened))
    lines.append("")
    lines.append("## Columns")
    lines.append("")
    for name in REQUIRED:
        lines.append("* `%s`" % name)
    lines.append("")
    lines.append("## How it was made")
    lines.append("")
    lines.append("Each Status is copied from the re-check log by `tools/update-index`; "
                 "no status is typed by hand. Rows whose snapshot does not name both "
                 "a page URL and a save date are forced to cannot-check.")
    if dates:
        lines.append("")
        lines.append("Date(s) checked: %s." % ", ".join(dates))
    if forced:
        lines.append("")
        lines.append("Forced to cannot-check for missing snapshot provenance: %s."
                     % ", ".join(sorted(forced)))
    lines.append("")
    lines.append("## What it could not check")
    lines.append("")
    lines.append("A row marked cannot-check or unverified records no confirmed page "
                 "content. Nothing here is a claim about a page that was not opened.")
    lines.append("")
    lines.append("## Rows not opened")
    lines.append("")
    if not_opened:
        for row in not_opened:
            lines.append("* %s -- %s" % (row["Issue"], row["Page opened"][:200]))
    else:
        lines.append("None.")
    lines.append("")
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write("\n".join(lines))


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
    forced, final, not_opened = [], [], []
    for row in rows:
        row, hit = apply_snapshot_rule(row, args.snapshots)
        if hit:
            forced.append(hit)
        final.append(row)
        if is_not_opened(row):
            not_opened.append(row)

    if args.dry_run:
        print("%d rows valid; dry run, nothing written" % len(final))
        for status in STATUSES:
            print("  %-13s %d" % (status, sum(1 for r in final if r["Status"] == status)))
        print("  %-13s %d" % ("not opened", len(not_opened)))
        return 0

    try:
        write_csv(args.data, final)
        write_card(args.card, final, forced, not_opened,
                   [r["Date checked"] for r in final])
    except OSError as exc:
        print("error: cannot write output: %s" % exc, file=sys.stderr)
        return 2

    print("wrote %s: %d rows" % (args.data, len(final)))
    for status in STATUSES:
        print("  %-13s %d" % (status, sum(1 for r in final if r["Status"] == status)))
    print("  %-13s %d" % ("not opened", len(not_opened)))
    print("wrote %s" % args.card)
    return 0


if __name__ == "__main__":
    sys.exit(main())
