#!/usr/bin/env python3
"""index_build.py -- build index.md for a folder of saved agent-note .md files.

Standard library only. Reads every *.md under the notes folder (recursively),
takes each note's first Markdown heading and its "Saved: YYYY-MM-DD" line when
the note carries one, and writes one sorted line per note to index.md. The date
slot is left empty for a note with no such line; a note with no heading still
gets its row. The notes themselves are never modified, and the output file is
skipped as an input so a second run is byte-identical.
"""

import argparse
import re
import sys
from pathlib import Path

SAVED_RE = re.compile(r"^Saved:[ \t]*(\d{4}-\d{2}-\d{2})[ \t]*$")
HEAD_RE = re.compile(r"^#{1,6}[ \t]+(\S.*?)[ \t]*#*[ \t]*$")
FENCE_RE = re.compile(r"^[ \t]*(?:```|~~~)")


def scan(text):
    """Return (first heading, saved date); either may be an empty string."""
    heading = saved = ""
    in_fence = False
    for line in text.splitlines():
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if not heading:
            match = HEAD_RE.match(line)
            if match:
                heading = match.group(1).strip()
        if not saved:
            match = SAVED_RE.match(line)
            if match:
                saved = match.group(1)
        if heading and saved:
            break
    return heading, saved


def cell(value):
    return value.replace("|", "\\|").replace("\n", " ").strip()


def build(notes_dir, out_path):
    """Write out_path from the .md files under notes_dir.

    Returns (notes, no_heading). Raises SystemExit on a missing folder or an
    unreadable note.
    """
    notes_dir = Path(notes_dir)
    out_path = Path(out_path)
    if not notes_dir.is_dir():
        raise SystemExit("error: not a folder: %s" % notes_dir)
    rows = []
    for path in sorted(notes_dir.rglob("*.md")):
        if path.resolve() == out_path.resolve():
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            raise SystemExit("error: cannot read %s: %s" % (path, exc))
        heading, saved = scan(text)
        rows.append((path.relative_to(notes_dir).as_posix(), heading, saved))
    rows.sort(key=lambda row: row[0])
    lines = [
        "# Index of saved agent notes",
        "",
        "One line per saved note: path | first heading | saved date.",
        "The saved date is empty when the note carries no `Saved: YYYY-MM-DD` line.",
        "",
    ]
    for rel, heading, saved in rows:
        date_cell = cell(saved)
        lines.append("- %s | %s |%s" % (cell(rel), cell(heading),
                                        " " + date_cell if date_cell else ""))
    if not rows:
        lines.append("_(no .md files found)_")
    lines.append("")
    with open(out_path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write("\n".join(lines))
    no_heading = sum(1 for row in rows if not row[1])
    return len(rows), no_heading


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Build index.md for a folder of saved agent notes.")
    parser.add_argument("notes_dir",
                        help="folder of saved .md notes (read recursively)")
    parser.add_argument("-o", "--output", default=None,
                        help="index file to write (default: NOTES_DIR/index.md)")
    args = parser.parse_args(argv)
    notes_dir = Path(args.notes_dir)
    out_path = Path(args.output) if args.output else notes_dir / "index.md"
    notes, no_heading = build(notes_dir, out_path)
    print("wrote %s: %d note(s), %d without a heading"
          % (out_path, notes, no_heading))
    return 0


if __name__ == "__main__":
    sys.exit(main())
