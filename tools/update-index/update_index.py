#!/usr/bin/env python3
"""update_index.py -- generate INDEX.md from JSONL rows.

This tool reads a JSON Lines file `rows.jsonl`, where each line is a JSON
object describing a single issue number.  The fields that the tool cares
about are:

- ``id`` – integer or string unique per issue
- ``url`` – the public issue URL
- ``issue_title`` – short title of the issue
- ``evidence_path`` – relative path to the saved page in the evidence
  repository tree
- ``status`` – one‑line finding extracted by the reading tool
- ``read_status`` – ``verified``/``unverified`` if the page was opened
- ``read_status_reason`` – explanation if ``read_status`` is blank

The generator produces a Markdown index describing each issue.  It also
prints a summary of any corrections applied – for example, if a row claims
``read`` but the evidence file does not exist, the tool strips the claim and
notes the correction.

The generator does not perform any network I/O; it reads local files only.
It is used by the offline self‑test and by the production indexing
pipeline.

The output format is a one‑column table that resembles a typical README
summary.  The exact format (row markers, comments) is defined in the
self‑test's expected output.

Usage:
    python3 update_index.py rows.jsonl --out INDEX.md \
        --evidence-root PATH --now 2026-11-02T00:00:00Z

"""

import argparse
import json
import os
import sys
from pathlib import Path

DEFAULT_NOW = "2026-11-02T00:00:00Z"

###############################################################################
# Helper: read JSONL rows
###############################################################################

def load_rows(path: Path):
    """Yield decoded dicts from each line of a JSON Lines file.

    If a line cannot be decoded, the function raises a ``ValueError``
    with a helpful message that indicates the line number.
    """
    if not path.is_file():
        raise OSError(f"rows file not found: {path}")
    with path.open("r", encoding="utf-8") as fh:
        for n, line in enumerate(fh, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except Exception as exc:
                raise ValueError(f"line {n} is not valid JSON: {exc}")

###############################################################################
# Main generator
###############################################################################

def generate_from_rows(rows_path, out_path, evidence_root, now):
    # first sweep – read all rows, collect info, and detect duplicate ids
    rows = list(load_rows(rows_path))
    ids = {}
    for r in rows:
        rid = r.get("id") or r.get("issue_number") or r.get("issue")
        if rid in ids:
            ids[rid].append(r)
        else:
            ids[rid] = [r]

    # prepare output lines
    out_lines = []
    corrections = []
    duplicate_reports = []

    # we want to sort by numeric id if possible
    def sort_key(item):
        return int(item[0]) if isinstance(item[0], str) and item[0].isdigit() else item[0]
    for rid, rlist in sorted(ids.items(), key=sort_key):
        if len(rlist) > 1:
            # keep the last row, report the rest as duplicates
            last = rlist[-1]
            dup = rlist[:-1]
            duplicate_reports.append((rid, len(dup)))
        else:
            last = rlist[0]
        # compute evidence file path
        eff_path = Path(evidence_root) / last.get("evidence_path", "") if last.get("evidence_path") else Path()
        if last.get("read_status") and eff_path.exists():
            # valid read
            out_lines.append(f"**#{int(rid)}** – {last.get('issue_title', '(no title)')} – {last.get('status', '(no status)')} – read (evidence: {eff_path.as_posix()})")
        elif last.get("read_status"):
            # claimed read but evidence missing – blank it and note correction
            corrections.append(f"# {rid} – {last.get('issue_title', '(no title)')} – claimed read but evidence file missing – blanked")
            out_lines.append(f"**#{int(rid)}** – {last.get('issue_title', '(no title)')} – {last.get('status', '(no status)')} – unbacked read – {last.get('read_status_reason', 'no reason')} – error: evidence file missing")
        else:
            # not read
            out_lines.append(f"**#{int(rid)}** – {last.get('issue_title', '(no title)')} – {last.get('status', '(no status)')} – not read – {last.get('read_status_reason', 'no reason')}"
            )

    # produce final document
    lines = []
    lines.append(f"# Issue Index – {now}")
    lines.append("")
    lines.extend(out_lines)
    if duplicate_reports:
        lines.append("\n## Duplicate IDs")
        for dup_id, count in duplicate_reports:
            lines.append(f"- {dup_id}: {count} duplicate(s) discarded")
    if corrections:
        lines.append("\n## Corrections")
        lines.extend(corrections)
    lines.append(f"\n\n**Tool corrections this run:** {len(corrections)} row(s)")
    content = "\n".join(lines) + "\n"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(content, encoding="utf-8")
    return content

###############################################################################
# CLI entry point
###############################################################################

def main(argv=None):
    p = argparse.ArgumentParser(description="Generate a Markdown index of issue rows.")
    p.add_argument("rows", help="Path to rows.jsonl input")
    p.add_argument("--out", required=True, help="Output Markdown file path")
    p.add_argument("--evidence-root", required=True, help="Root where evidence pages live")
    p.add_argument("--now", default=DEFAULT_NOW, help="Timestamp to include in the header")
    args = p.parse_args(argv)

    try:
        generate_from_rows(Path(args.rows), Path(args.out), Path(args.evidence_root), args.now)
    except Exception as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
