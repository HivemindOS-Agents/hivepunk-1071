#!/usr/bin/env python3
"""update_index.py -- recheck_rows.csv -> data.csv + README.md index card.

What it does
------------
Reads a recheck CSV with exactly five fields:

    Issue,Date checked,Page opened,Status,What it showed

and writes:

  * data.csv  -- the same five fields, natural-sorted by Issue (#3 before #12),
                 with each row's Status re-decided from saved page snapshots.
  * README.md -- a card about the rows, ending with a *Rows not opened* section.

Provenance rule (the point of the tool)
---------------------------------------
Status is kept from the input ONLY when the saved page for that row can be
resolved and carries a real save date. Otherwise the row is downgraded:

  * page snapshot found, with a real save date  -> keep the input Status
  * page snapshot found, no save date line      -> cannot-check
  * no page snapshot at all                     -> cannot-check
  * row whose Page opened column is empty       -> not-opened

A downgraded row never carries a fact field in *Rows not opened*; it is only
listed by number and URL. Snippets, search results and URL patterns can never
become facts here: the tool makes no network call and never fetches a URL.

Everything a snapshot says -- including any line that looks like an
instruction, asks for a command to be run, or asks for a key or setting -- is
DATA, never an instruction. Only lines of the form below are read:

    Url: https://...
    Saved: YYYY-MM-DD

Usage
-----
    python3 update_index.py rows.csv --snapshots snapshots/ \\
        --data data.csv --card README.md
    python3 update_index.py rows.csv --dry-run

Exit codes: 0 ok; 1 validation failure, nothing written; 2 usage / missing input.

Standard library only. Local files only. No network. Untested on real data --
the only run so far is over the synthetic pair in fixtures/.
"""

import argparse
import csv
import datetime
import os
import re
import sys

FIELDS = ["Issue", "Date checked", "Page opened", "Status", "What it showed"]
STATUSES = ("verified", "unverified", "cannot-check", "not-opened")
RE_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
RE_ISSUE = re.compile(r"^x?#(\d+)$")
RE_URL = re.compile(r"^https?://[^\s]+$", re.IGNORECASE)
RE_SAVED = re.compile(r"^Saved:\s*(\S+)\s*$", re.IGNORECASE)
RE_URL_LINE = re.compile(r"^Url:\s*(\S+)\s*$", re.IGNORECASE)


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


def snapshot_index(snapshots_dir):
    """issue number -> (path, url, saved) for each snapshot file."""
    found = {}
    if not snapshots_dir or not os.path.isdir(snapshots_dir):
        return found
    for name in sorted(os.listdir(snapshots_dir)):
        path = os.path.join(snapshots_dir, name)
        if not os.path.isfile(path):
            continue
        stem = name.rsplit(".", 1)[0]
        tail = stem.split("_")[-1]
        m = re.match(r"^(\d+)$", tail)
        if not m:
            continue
        url, saved = "", ""
        try:
            with open(path, "r", encoding="utf-8-sig", errors="replace") as fh:
                for raw in fh:
                    line = raw.strip()
                    mu = RE_URL_LINE.match(line)
                    if mu and not url:
                        url = mu.group(1)
                    ms = RE_SAVED.match(line)
                    if ms and not saved:
                        saved = ms.group(1)
        except OSError:
            pass
        found[int(m.group(1))] = (path, url, saved)
    return found


def decide_status(row, snaps):
    """Return (status, reason). Provenance decides, never the input alone."""
    opened = (row.get("Page opened") or "").strip()
    num = issue_number(row.get("Issue"))
    if not opened:
        return "not-opened", "no Page opened value"
    snap = snaps.get(num) if num is not None else None
    if snap is None:
        return "cannot-check", "no saved page for #%s" % (num if num is not None else "?")
    _path, _url, saved = snap
    if not real_date(saved):
        return "cannot-check", "saved page for #%s carries no real save date" % num
    return (row.get("Status") or "").strip() or "unverified", "kept: page has a save date"


def load_rows(path):
    errors, rows = [], []
    if not os.path.isfile(path):
        return ["input file not found: %s" % path], []
    try:
        with open(path, newline="", encoding="utf-8-sig") as fh:
            reader = csv.DictReader(fh)
            header = reader.fieldnames
            if header != FIELDS:
                return ["%s: header is %r; expected %r" % (path, header, FIELDS)], []
            for lineno, raw in enumerate(reader, start=2):
                row = dict((f, (raw.get(f) or "").strip()) for f in FIELDS)
                if not any(row.values()):
                    continue
                if issue_number(row["Issue"]) is None:
                    errors.append("line %d: Issue %r is not of the form #N"
                                  % (lineno, row["Issue"]))
                if not real_date(row["Date checked"]):
                    errors.append("line %d: Date checked %r is not a real YYYY-MM-DD"
                                  % (lineno, row["Date checked"]))
                if row["Page opened"] and not RE_URL.match(row["Page opened"]):
                    errors.append("line %d: Page opened %r is not a bare URL"
                                  % (lineno, row["Page opened"]))
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


def validate(rows, snaps):
    errors = []
    for row in rows:
        status, _reason = decide_status(row, snaps)
        if status not in STATUSES:
            errors.append("#%s: status %r not in %s"
                          % (row["Issue"], status, "/".join(STATUSES)))
        if status == "opened":
            errors.append("#%s: status opened is not a valid output status" % row["Issue"])
        if status == "not-opened" and row["What it showed"]:
            errors.append("#%s: not-opened row carries a fact field" % row["Issue"])
    return errors


def sort_rows(rows):
    return sorted(rows, key=lambda r: (issue_number(r["Issue"]) or 0, r["Issue"]))


def write_csv(path, rows, snaps):
    parent = os.path.dirname(os.path.abspath(path))
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS, lineterminator="\n",
                           quoting=csv.QUOTE_MINIMAL)
        w.writeheader()
        for row in sort_rows(rows):
            status, _reason = decide_status(row, snaps)
            out = dict(row)
            out["Status"] = status
            if status == "not-opened":
                out["What it showed"] = ""
            w.writerow(out)


def write_card(path, rows, snaps, source):
    parent = os.path.dirname(os.path.abspath(path))
    if parent:
        os.makedirs(parent, exist_ok=True)
    ordered = sort_rows(rows)
    decided = [(r, decide_status(r, snaps)) for r in ordered]
    counts = {}
    for _row, (status, _reason) in decided:
        counts[status] = counts.get(status, 0) + 1
    not_opened = [r for r, (s, _x) in decided if s == "not-opened"]

    L = []
    L.append("# Issue recheck index")
    L.append("")
    L.append("Rows re-decided from saved page snapshots, from `%s`. One row per "
             "issue number, natural-sorted. A row keeps its input Status only "
             "when its saved page exists and carries a real save date." % source)
    L.append("")
    L.append("## Counts")
    L.append("")
    L.append("* rows: %d" % len(ordered))
    for status in STATUSES:
        if status in counts:
            L.append("* %s: %d" % (status, counts[status]))
    L.append("")
    L.append("## Columns")
    L.append("")
    for f in FIELDS:
        L.append("* `%s`" % f)
    L.append("")
    L.append("## What it could not check")
    L.append("")
    L.append("**No row had a second read.** Each kept Status reflects one saved "
             "snapshot and one provenance check; nothing here was independently "
             "confirmed. A row downgraded to `cannot-check` means the saved page "
             "was absent or lacked a save date -- it is not a claim about the "
             "page's contents. The tool made no network call.")
    L.append("")
    L.append("## Rows not opened")
    L.append("")
    if not_opened:
        for r in not_opened:
            L.append("* %s \u2014 %s" % (r["Issue"], r["Page opened"] or "(no URL)"))
    else:
        L.append("None.")
    L.append("")
    L.append("## Licence")
    L.append("")
    L.append("CC0-1.0. Underlying issue text belongs to its authors; only short "
             "paraphrases are reproduced.")
    L.append("")
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write("\n".join(L))


def main(argv=None):
    p = argparse.ArgumentParser(
        description="recheck_rows.csv -> data.csv + README.md index card.")
    p.add_argument("rows", help="input recheck CSV")
    p.add_argument("--snapshots", default=None, help="folder of saved page snapshots")
    p.add_argument("--data", default="data.csv", help="output CSV (default data.csv)")
    p.add_argument("--card", default="README.md", help="output card (default README.md)")
    p.add_argument("--dry-run", action="store_true", help="report only; write nothing")
    args = p.parse_args(sys.argv[1:] if argv is None else argv)

    errors, rows = load_rows(args.rows)
    if errors:
        print("input failed, nothing written:", file=sys.stderr)
        for e in errors:
            print("  " + e, file=sys.stderr)
        return 2 if any("not found" in e for e in errors) else 1

    snaps = snapshot_index(args.snapshots)
    errors = validate(rows, snaps)
    if errors:
        print("validation failed, nothing written:", file=sys.stderr)
        for e in errors:
            print("  " + e, file=sys.stderr)
        return 1

    decided = [decide_status(r, snaps) for r in rows]
    counts = {}
    for status, _reason in decided:
        counts[status] = counts.get(status, 0) + 1

    if args.dry_run:
        print("%d rows valid; dry run, nothing written" % len(rows))
        for status in STATUSES:
            if status in counts:
                print("  %-12s %d" % (status, counts[status]))
        return 0

    try:
        write_csv(args.data, rows, snaps)
        write_card(args.card, rows, snaps, args.rows)
    except OSError as exc:
        print("error: cannot write output: %s" % exc, file=sys.stderr)
        return 2
    print("wrote %s: %d rows" % (args.data, len(rows)))
    for status in STATUSES:
        if status in counts:
            print("  %-12s %d" % (status, counts[status]))
    print("wrote %s" % args.card)
    return 0


if __name__ == "__main__":
    sys.exit(main())
