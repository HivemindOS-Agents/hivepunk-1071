#!/usr/bin/env python3
"""provenance_row.py -- one saved snapshot file -> exactly one five-field re-check row.

The five fields, in this order:

    Issue, Date checked, Page opened, Status, What it showed

It writes one row and only one. Status is 'verified' only when ALL hold:

  1. the snapshot file exists and can be read;
  2. its text names the page URL in a provenance line;
  3. its text names the date it was saved;
  4. that saved date is a real calendar date in strict YYYY-MM-DD form.

Otherwise Status is 'cannot-check', and 'What it showed' states which of the
conditions failed. A missing save date or page URL is never an error: it is
recorded honestly as cannot-check. The script never fetches the URL, never
opens a page, makes no network call and uploads nothing.

The snapshot's own words are DATA, never instructions. A line in the snapshot
that looks like a command, a request to reveal keys or settings, a request to
change this script's goal, to send money or to post something is not acted on:
the script prints a warning naming the line number and carries on.

Accepted provenance forms (narrow on purpose):
  * a line containing an http:// or https:// URL -> names the page URL
  * a line containing 'Saved', 'Snapshot date', 'Saved on' or 'Retrieved'
    followed by YYYY-MM-DD -> names the save date
  * a bare YYYY-MM-DD anywhere in the first 40 lines, no later than Date
    checked, is also accepted as the save date

Usage:  python3 provenance_row.py [SNAPSHOT] [-o ROW.csv] [--date YYYY-MM-DD]
Defaults: snapshot=snapshot.md, out=row.csv, date=today (UTC).
Exit codes: 0 row written; 2 usage or I/O error; 3 internal error.
"""

import argparse
import datetime
import os
import re
import sys

FIELDS = ["Issue", "Date checked", "Page opened", "Status", "What it showed"]
STATUS_OK = "verified"
STATUS_NO = "cannot-check"

RE_URL = re.compile(r"https?://[^\s\]\)>,;\"']+", re.IGNORECASE)
RE_SAVE_LABEL = re.compile(
    r"(?:saved(?:\s+on)?|snapshot\s+date|retrieved)\s*[:=]?\s*(\d{4}-\d{2}-\d{2})",
    re.IGNORECASE)
RE_BARE_DATE = re.compile(r"\b(\d{4}-\d{2}-\d{2})\b")
RE_ISSUE_TAIL = re.compile(r"(?:issues|pull)/(\d+)\s*(?:[/?#\s].*)?$")
RE_HEADING = re.compile(r"^#+\s+(.+?)\s*$")
RE_INSTRUCTION = re.compile(
    r"(\brun\b|\bexecute\b|curl\s|\bpost\b|\bsend\b|\bpay\b|\btransfer\b|"
    r"api[_ -]?key|secret|password|token|\bignored? instructions\b|"
    r"change (?:your|the) goal)",
    re.IGNORECASE)


def parse_args(argv):
    p = argparse.ArgumentParser(
        description="One saved snapshot file -> one five-field re-check row.")
    p.add_argument("snapshot", nargs="?", default="snapshot.md",
                   help="saved snapshot file (default: snapshot.md)")
    p.add_argument("-o", "--out", default="row.csv",
                   help="output CSV path (default: row.csv)")
    p.add_argument("--date", default=None,
                   help="Date checked, YYYY-MM-DD (default: today, UTC)")
    return p.parse_args(argv)


def real_date(value, today):
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", value):
        return None
    try:
        return datetime.datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return None


def read_snapshot(path):
    """Return the file's text. Raises OSError if it cannot be read."""
    with open(path, "r", encoding="utf-8-sig", errors="replace") as handle:
        return handle.read()


def scan(text, today):
    """Return (page_url, saved_date, warnings, instruction_lines).

    Everything here only reads strings. No line is executed or obeyed.
    """
    lines = text.splitlines()
    page_url = None
    saved = None
    warnings = []
    instruction_lines = []

    for number, line in enumerate(lines, start=1):
        for match in RE_URL.finditer(line):
            if page_url is None:
                page_url = match.group(0).rstrip(".,;)")
        if saved is None:
            hit = RE_SAVE_LABEL.search(line)
            if hit:
                saved = hit.group(1)
        if RE_INSTRUCTION.search(line):
            instruction_lines.append(number)
            warnings.append(
                "line %d looks like an instruction; treated as data, not followed"
                % number)

    if saved is None:
        for number, line in enumerate(lines[:40], start=1):
            hit = RE_BARE_DATE.search(line)
            if hit:
                candidate = real_date(hit.group(1), today)
                if candidate is not None and candidate <= today:
                    saved = hit.group(1)
                    break

    return page_url, saved, warnings, instruction_lines


def issue_from(text, page_url):
    if page_url:
        hit = RE_ISSUE_TAIL.search(page_url)
        if hit:
            parts = [p for p in page_url.split("/") if p]
            if len(parts) >= 2:
                head = parts[-3] + "/" + parts[-2] if len(parts) >= 3 else parts[-2]
                return "%s#%s" % (head, hit.group(1))
            return "#" + hit.group(1)
    for line in text.splitlines():
        hit = RE_HEADING.match(line)
        if hit:
            return hit.group(1)[:80]
    return "unknown"


def summarise(text, limit=240):
    """First heading plus first non-empty lines, truncated. Data only."""
    picked = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("#") or len(picked) == 0:
            picked.append(stripped.lstrip("#").strip())
        if len(" ".join(picked)) > limit:
            break
    joined = " ".join(picked) if picked else "snapshot was empty"
    if len(joined) > limit:
        joined = joined[:limit - 3].rstrip() + "..."
    return joined


def build_row(path, checked):
    """Return (row_dict, warnings). Raises OSError if the file is unreadable."""
    text = read_snapshot(path)
    page_url, saved, warnings, _ = scan(text, checked)

    reasons = []
    if not page_url:
        reasons.append("the snapshot does not name the page URL")
    if not saved:
        reasons.append("it does not name the date it was saved")
    elif real_date(saved, checked) is None:
        reasons.append("the saved date %r is not a real calendar date" % saved)
    if saved and real_date(saved, checked) is not None:
        if real_date(saved, checked) > checked:
            reasons.append("the saved date %s is later than Date checked %s"
                           % (saved, checked.isoformat()))

    status = STATUS_OK if not reasons else STATUS_NO
    if reasons:
        showed = ("cannot-check: " + "; ".join(reasons) + ". "
                  + summarise(text))
    else:
        showed = ("verified: snapshot saved %s names %s. " % (saved, page_url)
                  + summarise(text))

    row = {
        "Issue": issue_from(text, page_url),
        "Date checked": checked.isoformat(),
        "Page opened": page_url if page_url else
            "not opened -- no page URL named in the saved snapshot",
        "Status": status,
        "What it showed": showed[:500],
    }
    return row, warnings


def write_row(path, row):
    parent = os.path.dirname(os.path.abspath(path))
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(",".join(FIELDS) + "\n")
        handle.write(",".join(csv_field(row[f]) for f in FIELDS) + "\n")


def csv_field(value):
    if any(ch in value for ch in ",\n\r\""):
        return '"' + value.replace('"', '""') + '"'
    return value


def main(argv=None):
    args = parse_args(sys.argv[1:] if argv is None else argv)
    checked = real_date(args.date, datetime.date.today()) if args.date else None
    if args.date and checked is None:
        print("error: --date must be a real YYYY-MM-DD date", file=sys.stderr)
        return 2
    if checked is None:
        checked = datetime.date.today()

    try:
        row, warnings = build_row(args.snapshot, checked)
    except OSError as exc:
        print("error: cannot read snapshot %s: %s" % (args.snapshot, exc),
              file=sys.stderr)
        return 2
    except Exception as exc:  # internal error, no row written
        print("error: internal failure: %s" % exc, file=sys.stderr)
        return 3

    for warning in warnings:
        print("warning: " + warning, file=sys.stderr)

    try:
        write_row(args.out, row)
    except OSError as exc:
        print("error: cannot write %s: %s" % (args.out, exc), file=sys.stderr)
        return 2

    print("wrote %s: 1 row, Status=%s" % (args.out, row["Status"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
