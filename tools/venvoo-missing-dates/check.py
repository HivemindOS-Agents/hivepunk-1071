#!/usr/bin/env python3
"""Compare local YYYYMMDD directories against a supplied calendar.

The calendar file is the only authority for which dates are
expected. This tool never infers trading days from weekday,
holiday, or any other rule: a date absent from the supplied
calendar is never reported as missing, even if no directory
exists for it. No network. See README.md.
"""
import json
import re
import sys
from datetime import date
from pathlib import Path

NAME_RE = re.compile(r"^\d{8}$")
TOKEN_RE = re.compile(r"^\d{8}$")

def valid_yyyymmdd(s):
    if not NAME_RE.match(s or ""):
        return False
    try:
        date(int(s[0:4]), int(s[4:6]), int(s[6:8]))
    except ValueError:
        return False
    return True

def load_calendar(path):
    expected = set()
    lines = Path(path).read_text(encoding="utf-8").splitlines()
    for lineno, raw in enumerate(lines, 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        token = re.split(r"[,;\s]+", line, maxsplit=1)[0].strip()
        if not TOKEN_RE.match(token) or not valid_yyyymmdd(token):
            raise ValueError("calendar line %d: not a valid YYYYMMDD date: %r" % (lineno, raw))
        expected.add(token)
    return sorted(expected)

def scan_data_dir(path):
    p = Path(path)
    if not p.is_dir():
        raise ValueError("data dir does not exist or is not a directory: %s" % path)
    present = set()
    ignored = []
    for entry in sorted(p.iterdir(), key=lambda e: e.name):
        if entry.is_dir() and valid_yyyymmdd(entry.name):
            present.add(entry.name)
        else:
            ignored.append(entry.name)
    return sorted(present), sorted(ignored)

def compare(data_dir, calendar_path):
    expected = load_calendar(calendar_path)
    present, ignored = scan_data_dir(data_dir)
    exp_set, pres_set = set(expected), set(present)
    return {
        "calendar": str(calendar_path),
        "data_dir": str(data_dir),
        "expected": expected,
        "present": present,
        "missing": sorted(exp_set - pres_set),
        "extra_not_in_calendar": sorted(pres_set - exp_set),
        "ignored_names": ignored,
        "counts": {
            "expected": len(expected),
            "present": len(present),
            "missing": len(sorted(exp_set - pres_set)),
            "extra_not_in_calendar": len(sorted(pres_set - exp_set)),
            "ignored": len(ignored),
        },
    }

def main(argv):
    if len(argv) < 2 or argv[1] in ("-h", "--help"):
        print("usage: python3 check.py --data-dir DIR --calendar FILE [--out FILE]")
        print("Calendar: one YYYYMMDD per line (blank/# lines skipped).")
        print("Only dates in the supplied calendar can be reported missing.")
        return 0 if len(argv) >= 2 else 2
    data_dir = calendar = out = None
    i = 1
    while i < len(argv):
        if argv[i] == "--data-dir" and i + 1 < len(argv):
            data_dir = argv[i + 1]; i += 2
        elif argv[i] == "--calendar" and i + 1 < len(argv):
            calendar = argv[i + 1]; i += 2
        elif argv[i] == "--out" and i + 1 < len(argv):
            out = argv[i + 1]; i += 2
        else:
            print("unknown or incomplete argument: %s" % argv[i]); return 2
    if not data_dir or not calendar:
        print("both --data-dir and --calendar are required"); return 2
    try:
        result = compare(data_dir, calendar)
    except ValueError as e:
        print("error: %s" % e); return 2
    text = json.dumps(result, indent=2, sort_keys=True)
    if out:
        Path(out).write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
