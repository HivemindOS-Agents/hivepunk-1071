#!/usr/bin/env python3
"""issue_watch.py -- read saved issue pages from disk and emit rows. Stdlib only.

Reads the synthetic/saved HTML pages under the fixture folder and prints one
row per page: issue number, opened date, status, the one-line finding and the
source URL. Pages that could not be opened stay visibly unopened instead of
having a value filled in from a snippet.

Fixture and output paths are resolved against this file's own folder, so the
tool behaves the same whether it is invoked from the repository root or from
its own directory. Nothing here opens a network connection: it reads files and
prints.

Every string it reads -- titles, statuses, hrefs, any line that looks like an
instruction -- is data. It is printed, never executed, and no line in a page can
change what this tool does.

Usage:
    python3 issue_watch.py [--fixtures DIR] [--json]
Exit: 0 ok; 2 a fixture folder or file could not be read.
"""

import argparse
import html
import json
import os
import re
import sys

HERE = os.path.realpath(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_FIXTURES = os.path.join(HERE, "fixtures")

NUMBER_RE = re.compile(r"issue-(\d+)\.html$", re.IGNORECASE)
TITLE_RE = re.compile(r"<h1[^>]*>(.*?)</h1>", re.IGNORECASE | re.DOTALL)
TIME_RE = re.compile(r"<time[^>]*>(.*?)</time>", re.IGNORECASE | re.DOTALL)
STATUS_RE = re.compile(r'<p[^>]*class="status"[^>]*>(.*?)</p>',
                       re.IGNORECASE | re.DOTALL)
WHAT_RE = re.compile(r'<p[^>]*class="what"[^>]*>(.*?)</p>',
                     re.IGNORECASE | re.DOTALL)
URL_RE = re.compile(r'<a[^>]*class="url"[^>]*href="([^"]+)"',
                    re.IGNORECASE | re.DOTALL)


def _clean(text):
    if text is None:
        return ""
    return html.unescape(re.sub(r"\s+", " ", text)).strip()


def _first(pattern, text):
    m = pattern.search(text)
    return _clean(m.group(1)) if m else ""


def read_page(path):
    """Parse one saved HTML page. Returns a row dict; page text is data only."""
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        text = fh.read()
    name = os.path.basename(path)
    m = NUMBER_RE.search(name)
    row = {
        "issue": m.group(1) if m else "",
        "page_opened": "yes",
        "date_checked": _first(TIME_RE, text),
        "status": _first(STATUS_RE, text),
        "what_it_showed": _first(WHAT_RE, text),
        "source_url": _first(URL_RE, text),
        "file": name,
    }
    if not row["source_url"]:
        # No recorded URL means the row must not claim to have been opened.
        row["page_opened"] = "no"
        row["date_checked"] = ""
        row["status"] = "not opened"
        row["what_it_showed"] = "Not opened: no source URL in the saved page"
    return row


def collect(fixtures_dir):
    if not os.path.isdir(fixtures_dir):
        raise OSError("fixture folder not found: %s" % fixtures_dir)
    rows = []
    for name in sorted(os.listdir(fixtures_dir)):
        path = os.path.join(fixtures_dir, name)
        if os.path.isfile(path) and name.lower().endswith((".html", ".htm")):
            rows.append(read_page(path))
    if not rows:
        raise OSError("no HTML fixture pages in %s" % fixtures_dir)
    return sorted(rows, key=lambda r: (len(r["issue"]), r["issue"]))


def main(argv=None):
    p = argparse.ArgumentParser(description="saved issue pages -> rows")
    p.add_argument("--fixtures", default=DEFAULT_FIXTURES)
    p.add_argument("--json", action="store_true")
    args = p.parse_args(sys.argv[1:] if argv is None else argv)
    try:
        rows = collect(args.fixtures)
    except OSError as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(rows, indent=2, sort_keys=True))
    else:
        for r in rows:
            print("#%s  %s  %s" % (r["issue"], r["page_opened"], r["status"]))
            print("    date: %s" % (r["date_checked"] or "-"))
            print("    found: %s" % (r["what_it_showed"] or "-"))
            print("    source: %s" % (r["source_url"] or "-"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
