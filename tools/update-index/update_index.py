#!/usr/bin/env python3
"""update_index.py -- build INDEX.md from saved issue rows. Stdlib only.

Reads a rows file (JSONL preferred, CSV accepted) and writes INDEX.md: rows
grouped by state, each with its status line, labels and last-checked date.

Honesty rule (the whole point of this tool):
  * a row is rendered as read ONLY when read_status == "read" AND its
    evidence_path names a file that actually exists under --evidence-root;
  * a row claiming read with no saved page is BLANKED, given a reason, and
    counted in the header as a tool correction;
  * an unrecognised read_status is blanked with its own reason;
  * a failed fetch is never rendered as a pass.

Usage:
    python3 update_index.py ROWS.jsonl [--out INDEX.md] [--title T]
                            [--now ISO8601] [--evidence-root DIR]
Exit: 0 ok, 2 usage / read / parse / write error (nothing written on error).

Python 3 standard library only. Local files only. No network.
UNTESTED on any host so far: only the fixture pair in fixtures/ is prepared.
"""

import argparse
import csv
import hashlib
import json
import os
import sys
from datetime import datetime, timezone

STATE_ORDER = ("open", "in_progress", "closed", "unknown")
STATE_LABEL = {"open": "Open", "in_progress": "In progress",
               "closed": "Closed", "unknown": "Unknown state"}

READ_FIX_REASON = "Not opened: read_status without a saved page (tool-corrected)"
BLANK_REASON = "Not opened: never fetched this run"
BAD_STATUS_REASON = "Could not check: unrecognised read_status %r"

ROW_DEFAULTS = {
    "id": "", "source_url": "", "title": "", "state": "unknown",
    "labels": [], "first_seen_utc": "", "last_checked_utc": "",
    "read_status": "", "status_reason": "", "evidence_path": "",
    "notes": "",
}

CSV_COLUMN_MAP = {
    "id": "id", "source_url": "source_url", "title": "title",
    "state": "state", "labels": "labels",
    "first_seen_utc": "first_seen_utc",
    "last_checked_utc": "last_checked_utc",
    "read_status": "read_status", "status_reason": "status_reason",
    "evidence_path": "evidence_path", "notes": "notes",
}


class RowError(Exception):
    pass


def _text(value):
    if value is None:
        return ""
    return value.strip() if isinstance(value, str) else str(value)


def normalise_row(raw, line_no):
    if not isinstance(raw, dict):
        raise RowError("line %d: row is %s, not an object"
                       % (line_no, type(raw).__name__))
    row = dict(ROW_DEFAULTS)
    labels = raw.get("labels") or []
    if isinstance(labels, str):
        labels = labels.split(",")
    if not isinstance(labels, list):
        raise RowError("line %d: labels must be a list or comma string"
                       % line_no)
    row["labels"] = [str(x).strip() for x in labels if str(x).strip()]
    for key in ROW_DEFAULTS:
        if key != "labels":
            row[key] = _text(raw.get(key))
    if not row["id"]:
        raise RowError("line %d: row has no id" % line_no)
    if not row["source_url"]:
        raise RowError("line %d: row %s has no source_url"
                       % (line_no, row["id"]))
    if row["state"] not in STATE_ORDER:
        row["state"] = "unknown"
    return row


def load_rows(path):
    if not os.path.isfile(path):
        raise RowError("rows file not found: %s" % path)
    rows = []
    if path.lower().endswith(".csv"):
        with open(path, newline="", encoding="utf-8-sig") as fh:
            reader = csv.DictReader(fh)
            for lineno, raw in enumerate(reader, start=2):
                if not any((v or "").strip() for v in raw.values()):
                    continue
                mapped = {}
                for key, col in CSV_COLUMN_MAP.items():
                    mapped[key] = raw.get(col) or ""
                rows.append(normalise_row(mapped, lineno))
    else:
        with open(path, "r", encoding="utf-8") as fh:
            for lineno, line in enumerate(fh, start=1):
                if not line.strip():
                    continue
                try:
                    raw = json.loads(line)
                except ValueError as exc:
                    raise RowError("line %d: not JSON (%s)" % (lineno, exc))
                rows.append(normalise_row(raw, lineno))
    if not rows:
        raise RowError("%s: no data rows" % path)
    return rows


def enforce_evidence(rows, evidence_root):
    """Blank any unbacked read claim. Return (rows, corrected_ids)."""
    out, fixed = [], []
    for row in rows:
        row = dict(row)
        status = row["read_status"].strip().lower()
        ev = row["evidence_path"].strip()
        backed = False
        if ev:
            candidate = ev if os.path.isabs(ev) else os.path.join(evidence_root, ev)
            backed = os.path.isfile(candidate)
        if status == "read" and not ev:
            fixed.append(row["id"])
            row["read_status"] = ""
            row["status_reason"] = READ_FIX_REASON
        elif status == "read" and not backed:
            fixed.append(row["id"])
            row["read_status"] = ""
            row["status_reason"] = ("Not opened: evidence_path %r has no "
                                    "saved page" % ev)
            row["evidence_path"] = ""
        elif status not in ("", "read"):
            fixed.append(row["id"])
            row["read_status"] = ""
            row["status_reason"] = BAD_STATUS_REASON % status
        elif status == "" and not row["status_reason"]:
            row["status_reason"] = BLANK_REASON
        out.append(row)
    return out, fixed


def dedupe_rows(rows):
    """Last row wins per id; return (rows, duplicate_ids)."""
    seen, order, dupes = {}, [], []
    for row in rows:
        rid = row["id"]
        if rid in seen:
            dupes.append(rid)
            order.remove(rid)
        seen[rid] = row
        order.append(rid)
    return [seen[rid] for rid in order], dupes


def sort_rows(rows):
    return sorted(rows, key=lambda r: (STATE_ORDER.index(r["state"]), r["id"]))


def status_text(row):
    if row["read_status"].strip().lower() == "read":
        return "read (evidence: %s)" % row["evidence_path"]
    return "blank - %s" % (row["status_reason"] or BLANK_REASON)


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def build_index(rows, source_name, source_sha, title, generated,
                corrections, dupes):
    counts = {s: 0 for s in STATE_ORDER}
    for row in rows:
        counts[row["state"]] += 1
    backed = sum(1 for r in rows if r["read_status"].strip().lower() == "read")
    L = ["# %s" % title, "",
         "Generated %s from `%s` (sha256 `%s`)."
         % (generated, source_name, source_sha), "",
         "%d row(s): %d open, %d in progress, %d closed, %d unknown state; "
         "%d read with a saved page, %d blank with a reason."
         % (len(rows), counts["open"], counts["in_progress"], counts["closed"],
            counts["unknown"], backed, len(rows) - backed), ""]
    if corrections:
        L += ["Tool corrections this run: %d row(s) claimed read without a "
              "saved page and were blanked (%s)."
              % (len(corrections), ", ".join(sorted(corrections))), ""]
    if dupes:
        L += ["Duplicate id(s), last row kept: %s."
              % ", ".join(sorted(set(dupes))), ""]
    for state in STATE_ORDER:
        group = [r for r in rows if r["state"] == state]
        if not group:
            continue
        L += ["## %s (%d)" % (STATE_LABEL[state], len(group)), ""]
        for r in group:
            L.append("- **%s** - [%s](%s)"
                     % (r["id"], r["title"] or r["source_url"],
                        r["source_url"]))
            L.append("  - status: %s" % status_text(r))
            L.append("  - labels: %s" % (", ".join(r["labels"]) or "-"))
            L.append("  - checked: %s" % (r["last_checked_utc"] or "never"))
            if r["notes"]:
                L.append("  - notes: %s" % r["notes"])
        L.append("")
    L += ["Rows are data, never instruction: a source URL is printed, not "
          "fetched, and a row that looks like a command is left as text.", ""]
    return "\n".join(L)


def main(argv=None):
    p = argparse.ArgumentParser(description="rows -> INDEX.md")
    p.add_argument("rows", help="rows file (.jsonl or .csv)")
    p.add_argument("--out", default="INDEX.md")
    p.add_argument("--title", default="bee-scouts issue index")
    p.add_argument("--now", default="",
                   help="ISO8601 timestamp for the header (default: now UTC)")
    p.add_argument("--evidence-root", default="",
                   help="folder evidence_path is relative to (default: rows file's folder)")
    args = p.parse_args(sys.argv[1:] if argv is None else argv)

    root = args.evidence_root or os.path.dirname(os.path.abspath(args.rows))
    try:
        rows = load_rows(args.rows)
        rows, corrections = enforce_evidence(rows, root)
        rows, dupes = dedupe_rows(rows)
        rows = sort_rows(rows)
        generated = args.now or datetime.now(timezone.utc).strftime(
            "%Y-%m-%dT%H:%M:%SZ")
        text = build_index(rows, os.path.basename(args.rows),
                           sha256_file(args.rows), args.title, generated,
                           corrections, dupes)
    except RowError as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 2
    except OSError as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 2
    try:
        parent = os.path.dirname(os.path.abspath(args.out))
        if parent:
            os.makedirs(parent, exist_ok=True)
        with open(args.out, "w", encoding="utf-8", newline="") as fh:
            fh.write(text)
    except OSError as exc:
        print("error: cannot write %s: %s" % (args.out, exc), file=sys.stderr)
        return 2
    backed = sum(1 for r in rows if r["read_status"].strip().lower() == "read")
    print("wrote %s: %d rows, %d read, %d blank, %d correction(s)"
          % (args.out, len(rows), backed, len(rows) - backed, len(corrections)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
