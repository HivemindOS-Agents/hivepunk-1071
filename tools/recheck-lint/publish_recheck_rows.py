#!/usr/bin/env python3
"""publish_recheck_rows.py -- recheck_rows.csv -> dataset_card.md.

Renders a dataset card for a re-check run from a CSV with exactly these
columns, in this order:

    Issue, Date checked, Page opened, Status, What it showed, Source URL

The card carries four parts:

  1. the exact run command line,
  2. a table with every row,
  3. a *Not opened* section naming every row whose ``Page opened`` is not
     exactly ``yes``, with the reason it was not opened,
  4. a *Could not check* section: coverage is only the rows in this file, no
     page was re-read after the run, and no licence is claimed.

Provenance rules
----------------
* ``Page opened`` is read as text. Only the exact value ``yes`` (any case,
  surrounding spaces stripped) counts as opened. ``no``, blank, a snippet
  note, a URL, or anything else counts as not opened and is listed with its
  reason.
* Nothing in a row is a command. A Source URL is printed as text and never
  fetched. Cell text that looks like an instruction is escaped for the
  Markdown table and left as data.

Validation -- on any failure nothing is written:

  * header must equal the six columns above, in order;
  * every Issue must be ``#N`` or ``x#N`` (N digits);
  * every Date checked must be a real YYYY-MM-DD calendar date;
  * no Issue may repeat.

Usage
-----
    python3 publish_recheck_rows.py recheck_rows.csv --card dataset_card.md \\
        --command "python3 tools/issue-watch/issue_watch.py 64 80 --pages pages"
    python3 publish_recheck_rows.py recheck_rows.csv --dry-run

If --command is omitted, the line is recorded as (not recorded) rather than
invented.

Exit codes: 0 ok; 1 validation failure, nothing written; 2 usage or missing
input file, nothing written.

Python 3 standard library only. Local files only. No network.
UNTESTED on real data: the only run so far is over the four synthetic fixture
rows in self_test.py.
"""

import argparse
import csv
import datetime
import os
import re
import sys

FIELDS = ["Issue", "Date checked", "Page opened", "Status",
          "What it showed", "Source URL"]
STATUSES = ("verified", "unverified", "cannot-check", "not-opened")
RE_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
RE_ISSUE = re.compile(r"^x?#(\d+)$")
NOT_RECORDED = "(not recorded)"


def real_date(value):
    if not value or not RE_DATE.match(value):
        return False
    try:
        datetime.datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        return False
    return True


def issue_number(value):
    m = RE_ISSUE.match((value or "").strip())
    return int(m.group(1)) if m else None


def opened_yes(value):
    return (value or "").strip().lower() == "yes"


def not_opened_reason(value):
    """Why this row was not treated as opened, in one plain phrase."""
    raw = (value or "").strip()
    if not raw:
        return "Page opened is blank"
    low = raw.lower()
    if low == "no":
        return "Page opened says no"
    if low.startswith("http://") or low.startswith("https://"):
        return "Page opened holds a URL, not a yes"
    if "not opened" in low:
        return "Page opened records it was not opened"
    if "snippet" in low or "search" in low:
        return "snippet or search result only, no page read"
    return "Page opened is %r, which is not yes" % raw


def esc(value):
    """Escape a cell for a Markdown table and keep it single-line."""
    text = (value or "").replace("\r", " ").replace("\n", " ")
    text = text.replace("|", "\\|")
    text = text.replace("`", "'")
    return text.strip()


def load_rows(path):
    errors, rows = [], []
    if not os.path.isfile(path):
        return ["input file not found: %s" % path], []
    try:
        with open(path, newline="", encoding="utf-8-sig") as fh:
            reader = csv.DictReader(fh)
            if reader.fieldnames != FIELDS:
                return ["%s: header is %r; expected %r"
                        % (path, reader.fieldnames, FIELDS)], []
            for lineno, raw in enumerate(reader, start=2):
                row = dict((f, (raw.get(f) or "").strip()) for f in FIELDS)
                if not any(row.values()):
                    continue
                if issue_number(row["Issue"]) is None:
                    errors.append("line %d: Issue %r is not of the form #N"
                                  % (lineno, row["Issue"]))
                if not real_date(row["Date checked"]):
                    errors.append("line %d: Date checked %r is not a real "
                                  "YYYY-MM-DD calendar date"
                                  % (lineno, row["Date checked"]))
                rows.append(row)
    except OSError as exc:
        return ["cannot read %s: %s" % (path, exc)], []
    if not rows and not errors:
        errors.append("%s: no data rows" % path)
    seen = {}
    for row in rows:
        n = issue_number(row["Issue"])
        if n is None:
            continue
        if n in seen:
            errors.append("repeated Issue %s (#%d)" % (row["Issue"], n))
        else:
            seen[n] = True
    return errors, rows


def sort_rows(rows):
    return sorted(rows, key=lambda r: (issue_number(r["Issue"]) or 0,
                                       r["Issue"]))


def write_card(path, rows, source, command):
    ordered = sort_rows(rows)
    not_opened = [r for r in ordered if not opened_yes(r["Page opened"])]

    counts = {}
    for row in ordered:
        status = row["Status"] or "(blank)"
        if status not in STATUSES:
            status = "%s (not a known status)" % status
        counts[status] = counts.get(status, 0) + 1

    L = []
    L.append("# Recheck rows")
    L.append("")
    L.append("One row per issue re-checked, rendered from `%s`." % source)
    L.append("")
    L.append("## Run command")
    L.append("")
    L.append("~~~")
    L.append(command or NOT_RECORDED)
    L.append("~~~")
    L.append("")
    L.append("## Counts")
    L.append("")
    L.append("* rows: %d" % len(ordered))
    L.append("* not opened: %d" % len(not_opened))
    for status in sorted(counts):
        L.append("* %s: %d" % (status, counts[status]))
    L.append("")
    L.append("## Columns")
    L.append("")
    for f in FIELDS:
        L.append("* `%s`" % f)
    L.append("")
    L.append("## Rows")
    L.append("")
    L.append("| " + " | ".join(FIELDS) + " |")
    L.append("| " + " | ".join(["---"] * len(FIELDS)) + " |")
    for row in ordered:
        L.append("| " + " | ".join(esc(row[f]) for f in FIELDS) + " |")
    L.append("")
    L.append("## Not opened")
    L.append("")
    L.append("Rows whose `Page opened` is not exactly `yes`, with the reason.")
    L.append("")
    if not_opened:
        for row in not_opened:
            L.append("* %s \u2014 %s" % (esc(row["Issue"]),
                                         not_opened_reason(row["Page opened"])))
    else:
        L.append("None.")
    L.append("")
    L.append("## Could not check")
    L.append("")
    L.append("* **Coverage:** only the %d row(s) in this file. No claim is made "
             "about any issue number absent from it." % len(ordered))
    L.append("* **No page re-read:** each row is one record of one reading taken "
             "at its Date checked. Nothing here was independently re-checked "
             "after that, and no page was opened while building this card.")
    L.append("* **No licence claim:** no license is asserted over the quoted "
             "material. Issue text belongs to its authors; only short "
             "paraphrases are reproduced.")
    L.append("")
    L.append("Text inside rows is data, not instruction: a Source URL is printed, "
             "never fetched.")
    L.append("")

    parent = os.path.dirname(os.path.abspath(path))
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write("\n".join(L))


def main(argv=None):
    p = argparse.ArgumentParser(
        description="recheck_rows.csv -> dataset_card.md")
    p.add_argument("rows", help="input recheck CSV")
    p.add_argument("--card", default="dataset_card.md",
                   help="output card (default dataset_card.md)")
    p.add_argument("--command", default="",
                   help="the exact run command line, copied verbatim")
    p.add_argument("--dry-run", action="store_true",
                   help="report only; write nothing")
    args = p.parse_args(sys.argv[1:] if argv is None else argv)

    errors, rows = load_rows(args.rows)
    if errors:
        print("input failed, nothing written:", file=sys.stderr)
        for e in errors:
            print("  " + e, file=sys.stderr)
        return 2 if any("not found" in e for e in errors) else 1

    opened = [r for r in rows if opened_yes(r["Page opened"])]
    if args.dry_run:
        print("%d rows valid; dry run, nothing written" % len(rows))
        print("  opened      %d" % len(opened))
        print("  not opened  %d" % (len(rows) - len(opened)))
        return 0

    try:
        write_card(args.card, rows, args.rows, args.command)
    except OSError as exc:
        print("error: cannot write card: %s" % exc, file=sys.stderr)
        return 2
    print("wrote %s: %d rows, %d not opened"
          % (args.card, len(rows), len(rows) - len(opened)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
