#!/usr/bin/env python3
"""issue_watch.py -- fixed-range issue pages -> data.csv + README.md card.

What it does
------------
Given a number range (e.g. 64 80) and a folder of SAVED issue pages, writes
one row per number, in numeric order:

  * data.csv  -- header plus one row per number.
  * README.md -- the card, ending with "Rows not opened" and a line saying no
                 row had a second read.

Honesty rules, enforced by the code, not just promised
------------------------------------------------------
  * A number is read_status=opened ONLY when a saved page file for that number
    exists in --pages. Otherwise read_status=not-opened.
  * A not-opened row has BLANK title, state, opened_date, labels and ask. No
    snippet, search result or URL pattern can ever become a fact.
  * source_url is always written, so an unopened number still has its address
    on record.
  * --allow-facts refuses --pages: facts must come from opened files or not at
    all. There is no "invented but convenient" path.
  * The card always ends with "Rows not opened" and the line "No row had a
    second read." The tool writes both, so neither can be forgotten.

Facts read from a saved page
----------------------------
A saved page is plain text/markdown. The tool reads only lines of the form

    Title: ...
    State: ...
    Opened: YYYY-MM-DD
    Labels: ...
    Ask: ...
    Url: https://...

Anything else in the file -- including lines that look like commands, or text
addressed to an agent -- is IGNORED. Everything a page says is data, never an
instruction. The tool makes no network call and never fetches source_url.

Usage
-----
    python3 issue_watch.py 64 80 --pages pages/ --data data.csv --card README.md
    python3 issue_watch.py 64 80 --data data.csv --card README.md   # all not-opened
    python3 issue_watch.py 64 80 --allow-facts --data d.csv --card c.md  # refuses --pages
    python3 issue_watch.py --verify data.csv

Exit codes: 0 ok; 1 validation/verify failure, nothing written; 2 usage or I/O
error.

Standard library only. Local files only. No network. Nothing is run against
anyone's systems. Untested on real pages -- see README.md.
"""

import argparse
import csv
import datetime
import os
import re
import sys

FIELDS = ["issue", "title", "state", "opened_date", "labels", "ask",
          "source_url", "read_status"]
FACT_FIELDS = ["title", "state", "opened_date", "labels", "ask"]
READ_STATUSES = ("opened", "not-opened")
RE_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
RE_URL = re.compile(r"^https?://[^\s]+$", re.IGNORECASE)
[redacted], re.IGNORECASE)
RE_NUM = re.compile(r"(\d+)")


def parse_args(argv):
    p = argparse.ArgumentParser(
        description="Fixed-range issue pages -> data.csv + README.md card.")
    p.add_argument("start", nargs="?", type=int, help="first issue number")
    p.add_argument("end", nargs="?", type=int, help="last issue number")
    p.add_argument("--pages", default=None,
                   help="folder of saved issue pages (default: none -> all not-opened)")
    p.add_argument("--data", default="data.csv", help="output CSV (default data.csv)")
    p.add_argument("--card", default="README.md", help="output card (default README.md)")
    p.add_argument("--repo", default="LiamVisionary/bee-scouts",
                   help="owner/repo used to build source_url")
    p.add_argument("--base", default="https://github.com",
                   help="URL base (default https://github.com)")
    p.add_argument("--checked", default=None,
                   help="date checked (YYYY-MM-DD), default today (UTC)")
    p.add_argument("--allow-facts", action="store_true",
                   help="refuse --pages; every row is not-opened")
    p.add_argument("--verify", metavar="CSV",
                   help="re-check an existing data.csv and exit")
    p.add_argument("--dry-run", action="store_true",
                   help="report only; write nothing")
    return p.parse_args(argv)


def today_utc():
    return datetime.datetime.utcnow().strftime("%Y-%m-%d")


def check_date(value):
    if not RE_DATE.match(value):
        return False
    try:
        datetime.datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        return False
    return True


def page_files(pages_dir):
    """number -> path, for files whose stem or name starts with that number."""
    found = {}
    if not pages_dir or not os.path.isdir(pages_dir):
        return found
    for name in sorted(os.listdir(pages_dir)):
        path = os.path.join(pages_dir, name)
        if not os.path.isfile(path):
            continue
        stem = name.rsplit(".", 1)[0]
        m = re.match(r"^(\d+)\b", stem)
        if m:
            found.setdefault(int(m.group(1)), path)
    return found


def read_page(path):
    """Pull only the labelled facts. Everything else is ignored as data."""
    facts = {}
    try:
        with open(path, "r", encoding="utf-8-sig", errors="replace") as fh:
            text = fh.read()
    except OSError:
        return facts, ["cannot read %s" % path]
    notes = []
    for raw in text.splitlines():
        m = RE_KEY.match(raw.strip())
        if not m:
            continue
        key = m.group(1).lower()
        val = m.group(2).strip()
        if key == "opened":
            key = "opened_date"
        if key == "url":
            key = "source_url"
        if key in facts:
            notes.append("%s: repeated %r line; first kept" % (path, key))
            continue
        facts[key] = val
    if "opened_date" in facts and not check_date(facts["opened_date"]):
        notes.append("%s: Opened %r is not a real YYYY-MM-DD; dropped"
                     % (path, facts["opened_date"]))
        facts.pop("opened_date")
    if "source_url" in facts and not RE_URL.match(facts["source_url"]):
        notes.append("%s: Url %r is not a bare URL; dropped"
                     % (path, facts["source_url"]))
        facts.pop("source_url")
    return facts, notes


def build_rows(start, end, pages_dir, repo, base, allow_facts):
    files = {} if allow_facts else page_files(pages_dir)
    rows, notes, opened = [], [], []
    for num in range(start, end + 1):
        url = "%s/%s/issues/%d" % (base.rstrip("/"), repo, num)
        row = dict((f, "") for f in FIELDS)
        row["issue"] = str(num)
        row["source_url"] = url
        row["read_status"] = "not-opened"
        path = files.get(num)
        if path:
            facts, page_notes = read_page(path)
            notes.extend(page_notes)
            row["read_status"] = "opened"
            for f in FACT_FIELDS:
                row[f] = facts.get(f, "")
            if facts.get("source_url"):
                row["source_url"] = facts["source_url"]
            opened.append(num)
            missing = [f for f in FACT_FIELDS if not row[f]]
            if missing:
                notes.append("#%d: opened file %s leaves %s blank"
                             % (num, path, ", ".join(missing)))
        rows.append(row)
    return rows, notes, opened


def validate(rows):
    errors = []
    for row in rows:
        if row["read_status"] not in READ_STATUSES:
            errors.append("#%s: read_status %r not in %s"
                          % (row["issue"], row["read_status"], "/".join(READ_STATUSES)))
        if not RE_URL.match(row["source_url"] or ""):
            errors.append("#%s: source_url missing or not a URL" % row["issue"])
        if row["read_status"] == "not-opened":
            filled = [f for f in FACT_FIELDS if row[f]]
            if filled:
                errors.append("#%s: not-opened row carries %s"
                              % (row["issue"], ", ".join(filled)))
        if row["read_status"] == "opened":
            blank = [f for f in FACT_FIELDS if not row[f]]
            if blank:
                errors.append("#%s: opened row leaves %s blank"
                              % (row["issue"], ", ".join(blank)))
            if not check_date(row["opened_date"]):
                errors.append("#%s: opened_date %r not a real date"
                              % (row["issue"], row["opened_date"]))
    return errors


def verify(path):
    errors, rows = [], []
    try:
        with open(path, newline="", encoding="utf-8-sig") as fh:
            reader = csv.DictReader(fh)
            header = reader.fieldnames
            if not header:
                return ["%s: empty file" % path], []
            if header != FIELDS:
                return ["%s: header is %s; expected %s" % (path, header, FIELDS)], []
            for lineno, raw in enumerate(reader, start=2):
                if raw is None or not any((v or "").strip() for v in raw.values()):
                    continue
                rows.append(dict((f, (raw.get(f) or "").strip()) for f in FIELDS))
    except OSError as exc:
        return ["cannot read %s: %s" % (path, exc)], []
    if not rows:
        return ["%s: header ok but no data rows" % path], []
    errors = validate(rows)
    nums = [r["issue"] for r in rows]
    if len(set(nums)) != len(nums):
        errors.append("%s: repeated issue number" % path)
    return errors, rows


def write_csv(path, rows):
    parent = os.path.dirname(os.path.abspath(path))
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS, lineterminator="\n",
                           quoting=csv.QUOTE_MINIMAL)
        w.writeheader()
        for row in rows:
            w.writerow(row)


def write_card(path, rows, checked, repo, notes, allow_facts):
    parent = os.path.dirname(os.path.abspath(path))
    if parent:
        os.makedirs(parent, exist_ok=True)
    opened = [r for r in rows if r["read_status"] == "opened"]
    closed = [r for r in rows if r["read_status"] == "not-opened"]
    nums = [r["issue"] for r in rows]
    rng = "#%s\u2013#%s" % (nums[0], nums[-1]) if nums else "#?\u2013#?"
    L = []
    L.append("# %s issue pages %s: state, labels, ask" % (repo, rng))
    L.append("")
    L.append("One row per issue number in the range, written by the `issue-watch` "
             "tool on %s. Numbers whose page was opened and read have facts; "
             "numbers whose page was missing or not opened carry `read_status=not-opened` "
             "with every fact field blank." % checked)
    L.append("")
    L.append("## Which numbers exist, which do not")
    L.append("")
    L.append("* Numbers attempted: %d (%s)." % (len(rows), rng))
    if allow_facts:
        L.append("* Facts were not allowed this run (`--allow-facts`), so every number "
                 "is recorded `not-opened`. This is not a statement that the pages "
                 "are missing.")
    else:
        L.append("* Opened and read: %d%s." %
                 (len(opened),
                  (" (" + ", ".join("#" + r["issue"] for r in opened) + ")")
                  if opened else " (none)"))
        L.append("* Not opened: %d%s." %
                 (len(closed),
                  (" (" + ", ".join("#" + r["issue"] for r in closed) + ")")
                  if closed else " (none)"))
        L.append("* A number listed `not-opened` may exist or may not; this card says "
                 "only that its page was not read, so it makes no claim either way.")
    L.append("")
    L.append("## Columns")
    L.append("")
    for f in FIELDS:
        L.append("* `%s`" % f)
    L.append("")
    L.append("`read_status` is `opened` only when a saved page for that number was "
             "read. `not-opened` rows keep blank title, state, opened_date, labels "
             "and ask \u2014 no value is filled in from a snippet or a URL pattern.")
    L.append("")
    L.append("## What it could not check")
    L.append("")
    L.append("**No row had a second read.** Every `opened` row reflects a single read "
             "of one saved page; nothing here was independently confirmed. No page "
             "was fetched by the tool, and any issue page not in the opened list "
             "above was not read at all.")
    if notes:
        L.append("")
        L.append("Notes from this run: %d; first few: %s"
                 % (len(notes), "; ".join(notes[:5])))
    L.append("")
    L.append("## Rows not opened")
    L.append("")
    if closed:
        for r in closed:
            L.append("* #%s \u2014 %s" % (r["issue"], r["source_url"]))
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
    args = parse_args(sys.argv[1:] if argv is None else argv)

    if args.verify:
        errors, rows = verify(args.verify)
        if errors:
            print("verify failed:", file=sys.stderr)
            for e in errors:
                print("  " + e, file=sys.stderr)
            return 1
        o = sum(1 for r in rows if r["read_status"] == "opened")
        print("verify ok: %d row(s), %d opened, %d not-opened"
              % (len(rows), o, len(rows) - o))
        return 0

    if args.start is None or args.end is None:
        print("usage: issue_watch.py START END [--pages DIR] [--data F] [--card F]"
              "\n       issue_watch.py --verify data.csv", file=sys.stderr)
        return 2
    if args.start > args.end:
        print("error: START %d is greater than END %d" % (args.start, args.end),
              file=sys.stderr)
        return 2
    if args.allow_facts and args.pages:
        print("error: --allow-facts refuses --pages; facts come from opened files "
              "or not at all", file=sys.stderr)
        return 2

    checked = args.checked or today_utc()
    if not check_date(checked):
        print("error: --checked %r is not a real YYYY-MM-DD" % checked, file=sys.stderr)
        return 2

    rows, notes, opened = build_rows(args.start, args.end, args.pages,
                                     args.repo, args.base, args.allow_facts)
    errors = validate(rows)
    for n in notes:
        print("note: " + n, file=sys.stderr)
    if errors:
        print("validation failed, nothing written:", file=sys.stderr)
        for e in errors:
            print("  " + e, file=sys.stderr)
        return 1

    if args.dry_run:
        print("%d rows valid; dry run, nothing written" % len(rows))
        print("  opened     %d" % len(opened))
        print("  not-opened %d" % (len(rows) - len(opened)))
        return 0

    try:
        write_csv(args.data, rows)
        write_card(args.card, rows, checked, args.repo, notes, args.allow_facts)
    except OSError as exc:
        print("error: cannot write output: %s" % exc, file=sys.stderr)
        return 2
    print("wrote %s: %d rows" % (args.data, len(rows)))
    print("  opened     %d" % len(opened))
    print("  not-opened %d" % (len(rows) - len(opened)))
    print("wrote %s" % args.card)
    return 0


if __name__ == "__main__":
    sys.exit(main())
