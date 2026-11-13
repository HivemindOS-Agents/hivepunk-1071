#!/usr/bin/env python3
"""recheck_log.py — validate one re-check log CSV.

Reads a CSV with header
    issue,url,state,checked_at
and prints one PASS/FAIL line per data row, then a summary, exits 1 if any
row FAILs. Stdlib only, no network, no subprocess.

Usage:
    python3 recheck_log.py ROWS.csv
    python3 recheck_log.py --help

Exit codes:
    0   all rows PASS
    1   at least one row FAIL
    2   usage error, file not found, or wrong header

A row is a FAIL when any of:
  - state is blank or whitespace-only
  - state is not exactly one of: ok, not-opened, NOT_RUN
  - url is blank
  - checked_at is empty
  - checked_at is not ISO 8601 (date or datetime with T separator)
  - checked_at is not a real calendar date or has impossible clock values

The exact header line is required; extra columns are permitted but ignored.
Trailing spaces in fields are not trimmed (a field with trailing space is
considered different because the CSV is raw).
"""

import csv
import re
import sys

_RE_ISO_DATE = re.compile(
    r'^'
    r'(\d{4})-(\d{2})-(\d{2})'  # YYYY-MM-DD
    r'(?:'
    r'T'
    r'(\d{2}):(\d{2})(?::(\d{2})(?:\.\d+)?)?'  # HH:MM[:SS[.fraction]]
    r'(Z|[+-]\d{2}(?::?\d{2})?)?'  # timezone
    r')?'
    r'$'
)
_VALID_STATES = frozenset(["ok", "not-opened", "NOT_RUN"])


def _is_real_date(yy, mm, dd):
    """Return True if (yy, mm, dd) is a real calendar date."""
    try:
        import calendar
        return 1 <= mm <= 12 and 1 <= dd <= calendar.monthrange(yy, mm)[1]
    except ValueError:
        return False


def _check_row(n, row):
    """Print PASS or FAIL for one row. Return True on PASS."""
    issue = row.get("issue", "")
    url = row.get("url", "")
    state = row.get("state", "")
    checked = row.get("checked_at", "")

    reasons = []

    # state checks
    if not state or state.strip() == "":
        reasons.append("state is blank")
    elif state not in _VALID_STATES:
        reasons.append(
            "state %r is not in {ok, not-opened, NOT_RUN}" % state)

    # url checks
    if not url or url.strip() == "":
        reasons.append("url is blank")

    # checked_at checks
    if not checked or checked.strip() == "":
        reasons.append("checked_at is empty")
    else:
        m = _RE_ISO_DATE.match(checked.strip())
        if not m:
            reasons.append(
                "checked_at %r is not ISO 8601" % checked)
        else:
            yy, mm, dd = int(m.group(1)), int(m.group(2)), int(m.group(3))
            if not _is_real_date(yy, mm, dd):
                reasons.append(
                    "checked_at %r is not a real calendar date" % checked)
            elif m.group(4) is not None:
                # Has time part
                hh, mn = int(m.group(4)), int(m.group(5))
                if hh > 23 or mn > 59:
                    reasons.append(
                        "checked_at %r has impossible time" % checked)
                ss = m.group(6)
                if ss is not None and int(ss) > 59:
                    reasons.append(
                        "checked_at %r has impossible seconds" % checked)

    if reasons:
        print("FAIL row %d: issue=%s url=%s state=%s checked_at=%s :: %s"
              % (n, issue, url, state, checked, "; ".join(reasons)))
        return False
    print("PASS row %d: issue=%s url=%s state=%s checked_at=%s"
          % (n, issue, url, state, checked))
    return True


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    if not argv:
        print(
            "Usage: python3 recheck_log.py ROWS.csv",
            file=sys.stderr)
        return 2

    path = argv[0]
    if path in ("-h", "--help"):
        print(__doc__)
        return 0

    try:
        with open(path, "r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            if reader.fieldnames is None:
                print("error: empty CSV", file=sys.stderr)
                return 2
            # Check required header fields
            required = ["issue", "url", "state", "checked_at"]
            for col in required:
                if col not in reader.fieldnames:
                    print(
                        "error: header must contain exactly %s; "
                        "missing column %r" % (required, col),
                        file=sys.stderr,
                    )
                    return 2

            passed = 0
            failed = 0
            for i, row in enumerate(reader, start=1):
                if _check_row(i, row):
                    passed += 1
                else:
                    failed += 1

        print("rows=%d failed=%d" % (passed + failed, failed))
        return 1 if failed > 0 else 0

    except FileNotFoundError:
        print("error: file not found: %s" % path, file=sys.stderr)
        return 2
    except PermissionError:
        print("error: permission denied: %s" % path, file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
