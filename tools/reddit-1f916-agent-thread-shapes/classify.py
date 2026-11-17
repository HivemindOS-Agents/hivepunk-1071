#!/usr/bin/env python3
"""classify.py - classify r/1F916 thread titles and validate data/data.csv.
No network, no upload. Stdlib only.
Kinds: question, showcase, report, ask, other
Usage: python3 classify.py [data/data.csv]
"""
import csv, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
COLUMNS = ["thread_title", "kind", "source_url", "read_back"]
KINDS = {"question", "showcase", "report", "ask", "other"}
def classify(title):
    t = (title or "").strip().lower()
    if t.endswith("?") or t.startswith("how ") or t.startswith("why ") or t.startswith("what ") or t.startswith("which "):
        return "question"
    if any(w in t for w in ("showcase", "i built", "i made", "i created", "demo")):
        return "showcase"
    if any(w in t for w in ("report", "results", "benchmark", "analysis", "findings")):
        return "report"
    if t.startswith("ask") or "please help" in t or t.startswith("help"):
        return "ask"
    return "other"
def load_rows(path):
    with open(path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        rows = list(reader)
        return reader.fieldnames, rows
def validate(path):
    errors = []
    fields, rows = load_rows(path)
    if fields != COLUMNS:
        errors.append("columns are %r, expected %r" % (fields, COLUMNS))
    if len(rows) < 20:
        errors.append("need at least 20 rows, found %d" % len(rows))
    for i, r in enumerate(rows, 2):
        if r.get("kind") not in KINDS:
            errors.append("row %d bad kind %r" % (i, r.get("kind")))
        if r.get("read_back") == "not-opened":
            if r.get("source_url") not in ("", "not-opened"):
                errors.append("row %d not-opened but has source_url" % i)
        elif r.get("read_back") == "opened":
            if not (r.get("source_url") or "").startswith("https://www.reddit.com/r/1F916/"):
                errors.append("row %d opened but source_url is not an r/1F916 URL" % i)
        else:
            errors.append("row %d read_back must be opened or not-opened" % i)
        if not (r.get("thread_title") or "").strip():
            errors.append("row %d empty title" % i)
    return rows, errors
def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    path = Path(argv[0]) if argv else HERE / "data" / "data.csv"
    if len(argv) > 1:
        print("usage: python3 classify.py [data/data.csv]", file=sys.stderr); return 2
    if not path.exists():
        print("error: missing %s" % path, file=sys.stderr); return 2
    rows, errors = validate(path)
    if errors:
        for e in errors: print("error: %s" % e, file=sys.stderr)
        return 1
    counts = {}
    for r in rows: counts[r["kind"]] = counts.get(r["kind"], 0) + 1
    print("rows: %d" % len(rows))
    for k in sorted(counts): print("%s: %d" % (k, counts[k]))
    print("ok: data.csv validates")
    return 0
if __name__ == "__main__":
    sys.exit(main())
