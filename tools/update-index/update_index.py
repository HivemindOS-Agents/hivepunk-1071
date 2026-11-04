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
``read`` but the evidence file does not exist, the tool strips the claim
and notes the correction.

The output format is designed to satisfy the self‑test expectations: it
starts with a header, lists the rows in numeric order (using ``**#123**``
blocks), and includes special sections for duplicates and corrections.

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

    out_blocks = []  # blocks per row
    corrections = []
    duplicate_reports = []

    # data order key: numeric if possible
    def sort_key(item):
        k = item[0]
        try:
            return int(k)
        except Exception:
            return k

    for rid, rlist in sorted(ids.items(), key=sort_key):
        # handle duplicates – keep last
        dup_count = len(rlist) - 1
        last = rlist[-1]
        if dup_count:
            duplicate_reports.append((rid, dup_count))

        # compute evidence path if declared
        ev_rel = last.get("evidence_path") or ""
        ev_abs = Path(evidence_root) / ev_rel if ev_rel else None
        has_evidence = ev_abs and ev_abs.is_file()

        # decide how to render
        # Blank if claimed read but no evidence or no "Saved:" line
        if last.get("read_status") and has_evidence:
            # validate that saved date line exists
            saved_line_present = False
            try:
                with ev_abs.open("r", encoding="utf-8") as fh:
                    for l in fh:
                        if l.lower().startswith("saved:"):
                            saved_line_present = True
                            break
            except Exception:
                saved_line_present = False
            if saved_line_present:
                # OK read
                out_blocks.append(
                    f"**#{int(rid)}** – {last.get('issue_title', '(no title)')} – {last.get('status', '(no status)')} – read (evidence: {ev_rel if ev_rel else 'None'})"
                )
                continue
        # If we reach here, we need to blank the row
        reason = None
        if not has_evidence:
            reason = "evidence file missing"
        else:
            # evidence file exists but lacks Saved:
            reason = "no Saved:"  # to match test expectation
        # Determine status text: keep previous status if present
        status_text = last.get('status') or '(no status)'
        # we consider it failed or undescribed; use reason
        corrections.append(f"# {rid} – {last.get('issue_title', '(no title)')} – claimed read but {reason}")
        out_blocks.append(
            f"**#{int(rid)}** – {last.get('issue_title', '(no title)')} – {status_text} – unbacked read – {reason}"
        )

    # prepare final document
    lines = []
    lines.append(f"# Issue Index – {now}")
    lines.append("")
    lines.append(f"Rows: {len(rows)}")
    lines.append("")

    # Rows blocks in order
    for blk in out_blocks:
        lines.append(blk)
        lines.append("")

    # duplicate report
    if duplicate_reports:
        lines.append("## Duplicate IDs")
        for dup_id, count in duplicate_reports:
            lines.append(f"Duplicate id(s), last row kept: {dup_id}")
        lines.append("")

    # corrections
    if corrections:
        lines.append("## Corrections")
        for c in corrections:
            lines.append(c)
        lines.append("")

    lines.append(f"**Tool corrections this run:** {len(corrections)} row(s)")

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
