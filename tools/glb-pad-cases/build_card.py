#!/usr/bin/env python3
"""build_card.py - emit the GLB padding-cases data.csv, README.md and card.

This tool does no network at all. It takes two inputs, both files you have
already read in the same run:

    cases.csv      one raw case per row: case_id,rule,expected_bytes,source
    readback.csv   one published file per row: file,sha256,line_count,status

and writes data.csv plus README.md into an output folder.

Rules this tool enforces:

* Every output row keeps source as the exact URL it was read from. A row whose
  source is empty, the literal 'not-opened', or a page not listed in
  cases.csv as opened is emitted with rule='not-opened' and
  expected_bytes='not-opened'. A byte count is never invented.
* readback.csv drives the README read-back lines. A file row with status
  'opened' must carry a 64-char lowercase hex sha256 and a positive integer
  line_count; anything else is written as not-opened. No hash is written by
  hand.
* The card text states which files were fetched back and which were not, and
  never claims a self_test.py pass.

Usage:
    python3 build_card.py cases.csv readback.csv OUTDIR
    python3 build_card.py --help

Stdlib only, no network, no subprocess. Exit 0 on success, 2 on usage error.
"""

import csv
import io
import re
import sys
from pathlib import Path

DATA_COLUMNS = ["case_id", "rule", "expected_bytes", "source", "read_back"]
NOT_OPENED = "not-opened"
_HEX64 = re.compile(r"^[0-9a-f]{64}$")


def split_csv_line(line):
    """Split one CSV line into cells, honouring double quotes."""
    return next(csv.reader(io.StringIO(line)))


def read_raw_rows(text):
    """Parse the raw cases CSV text into a list of dicts.

    Required columns: case_id, rule, expected_bytes, source.
    """
    reader = csv.DictReader(io.StringIO(text))
    if reader.fieldnames is None:
        raise ValueError("empty cases CSV")
    for col in ("case_id", "rule", "expected_bytes", "source"):
        if col not in reader.fieldnames:
            raise ValueError("cases CSV missing column %r" % col)
    return [dict(r) for r in reader]


def _is_unopened(value):
    v = (value or "").strip()
    return v == "" or v.lower() == NOT_OPENED


def emit_data_csv(rows):
    """Return the data.csv text for the given raw rows."""
    out = io.StringIO()
    writer = csv.writer(out, lineterminator="\n")
    writer.writerow(DATA_COLUMNS)
    for row in rows:
        source = (row.get("source") or "").strip()
        unopened = _is_unopened(source)
        if unopened:
            writer.writerow([
                (row.get("case_id") or "").strip(),
                NOT_OPENED,
                NOT_OPENED,
                NOT_OPENED,
                NOT_OPENED,
            ])
        else:
            writer.writerow([
                (row.get("case_id") or "").strip(),
                (row.get("rule") or "").strip(),
                (row.get("expected_bytes") or "").strip(),
                source,
                "opened",
            ])
    return out.getvalue()


def read_readback(text):
    """Parse readback.csv text into a list of dicts."""
    reader = csv.DictReader(io.StringIO(text))
    if reader.fieldnames is None:
        raise ValueError("empty readback CSV")
    for col in ("file", "sha256", "line_count", "status"):
        if col not in reader.fieldnames:
            raise ValueError("readback CSV missing column %r" % col)
    return [dict(r) for r in reader]


def looks_like_sha256(value):
    return bool(_HEX64.match((value or "").strip()))


def _readback_open(row):
    """True only when this row is a real, well-formed read-back."""
    if (row.get("status") or "").strip().lower() != "opened":
        return False
    if not looks_like_sha256(row.get("sha256")):
        return False
    try:
        return int((row.get("line_count") or "").strip()) > 0
    except ValueError:
        return False


def emit_readback_lines(readback_rows, data_csv_text):
    """Return the README read-back bullet lines."""
    known = {r["file"].strip(): r for r in readback_rows if r.get("file")}
    lines = []
    data_lines = len(data_csv_text.strip("\n").split("\n"))
    default_files = ["data.csv", "README.md"]
    seen = set()
    for name in default_files:
        seen.add(name)
        row = known.get(name)
        if row is not None and _readback_open(row):
            if name == "data.csv":
                n = data_lines
            else:
                n = int(row["line_count"].strip())
            lines.append(
                "- `%s` - sha256 %s, %d lines"
                % (name, row["sha256"].strip(), n)
            )
        else:
            lines.append(
                "- `%s` - not-opened (sha256: not-opened; line count: not-opened)"
                % name
            )
    for name in known:
        if name in seen:
            continue
        row = known[name]
        if _readback_open(row):
            lines.append(
                "- `%s` - sha256 %s, %s lines"
                % (name, row["sha256"].strip(), row["line_count"].strip())
            )
        else:
            lines.append(
                "- `%s` - not-opened (sha256: not-opened; line count: not-opened)"
                % name
            )
    return "\n".join(lines)


def emit_readme(readback_rows, data_csv_text, case_count):
    """Return the full README.md text."""
    rb = emit_readback_lines(readback_rows, data_csv_text)
    n_lines = len(data_csv_text.strip("\n").split("\n"))
    return (
        "# GLB binary chunk padding and alignment cases\n\n"
        "One row per GLB padding or alignment case, with the byte expression a"
        " parser has to get right and the page the row was read from.\n\n"
        "## Columns\n\n"
        "- `case_id` - short name of the case.\n"
        "- `rule` - the padding or alignment rule, in words.\n"
        "- `expected_bytes` - the byte count or byte expression; a\n"
        "  four-byte-alignment expression is kept as text, not evaluated.\n"
        "- `source` - the exact URL the row was read from.\n"
        "- `read_back` - `opened` when the source page was fetched in the run,\n"
        "  else `not-opened`.\n\n"
        "## How it was made\n\n"
        "%d case rows, emitted by build_card.py from a cases CSV read in the same\n"
        "run. A row whose page was not opened is written as `not-opened` in every\n"
        "field; no byte count is invented.\n\n"
        "## Read-back\n\n"
        "Each published file here is either fetched back with its sha256 and line\n"
        "count, or recorded as not-opened:\n\n"
        "%s\n\n"
        "data.csv has %d lines (1 header + %d rows).\n\n"
        "## Not checked\n\n"
        "No `self_test.py` pass is claimed in this card. Any sha256 or line count\n"
        "marked not-opened was not read in the run that produced this file.\n\n"
        "## Licence\n\n"
        "No licence is claimed. Rows are short factual notes about byte layouts.\n"
        % (case_count, rb, n_lines, case_count)
    )


def write_outputs(rows, readback_rows, outdir):
    """Write data.csv and README.md into outdir. Return their paths."""
    out = Path(outdir)
    out.mkdir(parents=True, exist_ok=True)
    data_csv_text = emit_data_csv(rows)
    readme_text = emit_readme(readback_rows, data_csv_text, len(rows))
    data_path = out / "data.csv"
    readme_path = out / "README.md"
    data_path.write_text(data_csv_text, encoding="utf-8")
    readme_path.write_text(readme_text, encoding="utf-8")
    return {"data_csv": str(data_path), "readme": str(readme_path)}


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    if not argv or argv[0] in ("-h", "--help"):
        print(
            "Usage: python3 build_card.py cases.csv readback.csv OUTDIR\n"
            "  cases.csv     columns: case_id,rule,expected_bytes,source\n"
            "  readback.csv  columns: file,sha256,line_count,status\n"
            "  OUTDIR        folder to write data.csv and README.md into"
        )
        return 0 if argv else 2
    if len(argv) != 3:
        print("error: need exactly 3 arguments", file=sys.stderr)
        return 2
    cases_path, readback_path, outdir = argv
    try:
        rows = read_raw_rows(Path(cases_path).read_text(encoding="utf-8"))
        readback_rows = read_readback(
            Path(readback_path).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 2
    paths = write_outputs(rows, readback_rows, outdir)
    print("wrote %s" % paths["data_csv"])
    print("wrote %s" % paths["readme"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
