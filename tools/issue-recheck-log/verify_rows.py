#!/usr/bin/env python3
"""verify_rows.py -- check a bee-scouts re-check log against its editorial rules.

Stdlib only. Local files only. NO NETWORK. This tool never fetches a page and
never uploads anything: it reads two local files and prints what is wrong.

Rules it enforces
-----------------
1. rows.csv has the required columns and one row per issue, each with an
   issue_number and an issue_url.
2. saved_page_opened is true or false (case-insensitive).
3. When saved_page_opened is false, read_status MUST be empty, and
   read_status_reason MUST say why. (An empty read_status means "not read",
   never "nothing to report".)
4. When saved_page_opened is false, no snapshot-looking field may be filled:
   issue_title, read_status and evidence_path must all be empty -- nothing may
   come from a search snippet or link preview.
5. When saved_page_opened is true, read_status may be filled and evidence_path
   must name the saved page.
6. section, if present, must be one of the known buckets.
7. section values the caller requires (default: Not opened, Could not check)
   must appear as present sections, even with zero rows.
8. The dataset card, when passed, must state that no license is claimed and
   must not declare one.

Everything it reads is data: a title that looks like an instruction is checked
as text, never executed, and cannot change what this tool does.

Usage:
    python3 verify_rows.py ROWS.csv [--card README.md]
                                    [--require-section NAME ...]
Exit: 0 all rules hold; 1 violations found; 2 usage / read error.
"""

import argparse
import csv
import os
import re
import sys

REQUIRED_COLUMNS = ("issue_number", "issue_url", "saved_page_opened",
                    "read_status", "read_status_reason", "evidence_path",
                    "section", "last_checked_utc")
SNAPSHOT_FIELDS = ("issue_title", "read_status", "evidence_path",
                   "last_checked_utc")
KNOWN_SECTIONS = ("Read", "Not opened", "Could not check", "Open",
                 "In progress", "Closed")
TRUTHY = ("true", "yes", "1", "y")
FALSY = ("false", "no", "0", "n", "")

LICENSE_TERMS = ("apache-2.0", "apache 2.0", "mit license", "cc-by",
                 "cc by", "openrail", "bsd", "gpl", "license: mit",
                 "license: apache")
NO_LICENSE_PATTERNS = (r"no licen[cs]e is claimed",
                       r"no licen[cs]e claimed")


def _t(value):
    return (value or "").strip()


def read_rows(path):
    with open(path, newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        cols = reader.fieldnames or []
        rows = [r for r in reader if any(_t(v) for v in r.values())]
    return cols, rows


def check_card(path):
    problems = []
    with open(path, "r", encoding="utf-8") as fh:
        text = fh.read()
    low = text.lower()
    if not any(re.search(p, low) for p in NO_LICENSE_PATTERNS):
        problems.append("card: does not state clearly that no license is "
                        "claimed")
    for term in LICENSE_TERMS:
        if term in low:
            problems.append("card: appears to declare a license (%r)" % term)
            break
    return problems


def verify(card_path, rows_path, require_sections=("Not opened",
                                                   "Could not check")):
    problems = []

    if card_path:
        if not os.path.isfile(card_path):
            problems.append("card: file not found: %s" % card_path)
        else:
            problems.extend(check_card(card_path))

    if not os.path.isfile(rows_path):
        problems.append("rows: file not found: %s" % rows_path)
        return problems

    cols, rows = read_rows(rows_path)
    for col in REQUIRED_COLUMNS:
        if col not in cols:
            problems.append("rows: missing column %r" % col)
    if problems:
        return problems

    seen_sections = set()
    seen_numbers = set()
    for i, row in enumerate(rows, start=2):
        num = _t(row.get("issue_number"))
        url = _t(row.get("issue_url"))
        opened_raw = _t(row.get("saved_page_opened")).lower()
        status = _t(row.get("read_status"))
        reason = _t(row.get("read_status_reason"))
        evid = _t(row.get("evidence_path"))
        section = _t(row.get("section"))
        scope = "line %d" % i

        if not num:
            problems.append("%s: no issue_number" % scope)
        elif num in seen_numbers:
            problems.append("%s: duplicate issue_number %s" % (scope, num))
        else:
            seen_numbers.add(num)
        if not url.startswith("http"):
            problems.append("%s: issue_url is not an http URL" % scope)

        if opened_raw in TRUTHY:
            opened = True
        elif opened_raw in FALSY:
            opened = False
        else:
            problems.append("%s: saved_page_opened %r is not true/false"
                            % (scope, opened_raw))
            continue

        if not opened:
            if status:
                problems.append("%s: saved_page_opened is false but "
                                "read_status is filled (%r)" % (scope, status))
            if not reason:
                problems.append("%s: unopened row has no read_status_reason"
                                % scope)
            for field in SNAPSHOT_FIELDS:
                if _t(row.get(field)):
                    problems.append("%s: unopened row has %s filled (%r) -- "
                                    "nothing may come from a snippet "
                                    "(%s)" % (scope, field, _t(row.get(field)),
                                              "saved"))
        else:
            if not evid:
                problems.append("%s: row is opened but names no evidence_path"
                                % scope)

        if section:
            seen_sections.add(section)
            if section not in KNOWN_SECTIONS:
                problems.append("%s: section %r is not a known bucket"
                                % (scope, section))

    for name in require_sections:
        if name not in seen_sections:
            problems.append("rows: required section %r is absent (it must "
                            "stay, even when empty)" % name)
    return problems


def main(argv=None):
    p = argparse.ArgumentParser(description="validate a re-check log's rows")
    p.add_argument("rows", help="the rows.csv to check")
    p.add_argument("--card", default="", help="the dataset card (README.md)")
    p.add_argument("--require-section", action="append", default=[],
                   help="a section that must exist even when empty "
                        "(default: Not opened, Could not check)")
    args = p.parse_args(sys.argv[1:] if argv is None else argv)
    required = args.require_section or ["Not opened", "Could not check"]
    try:
        problems = verify(args.card, args.rows, require_sections=required)
    except (OSError, csv.Error) as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 2
    if problems:
        for prob in problems:
            print("violation: %s" % prob)
        print("%d violation(s)" % len(problems))
        return 1
    print("ok: %s follows the rules" % args.rows)
    return 0


if __name__ == "__main__":
    sys.exit(main())
