#!/usr/bin/env python3
"""issue-watch: read saved issue pages, extract facts, write a CSV.

Python 3 standard library only. Local files only. No network.

Usage:
    python3 issue_watch.py --pages fixtures --out data.csv

Exit codes:
    0  ran and wrote the CSV
    2  --pages is missing or is not a directory  (no file written)

Pages that are not HTML are still listed as rows, marked ``Page opened=no``
with blank facts, so an unopened page stays visibly unopened.
"""

import argparse
import csv
import os
import sys
from html.parser import HTMLParser

FIELDS = ["Issue", "Date checked", "Page opened", "Status",
          "What it showed", "Source URL"]
HTML_EXT = (".html", ".htm")


class IssueParser(HTMLParser):
    """Pull the few labelled facts issue-watch keeps out of a saved page."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.facts = {"issue": "", "date": "", "status": "",
                      "what": "", "url": ""}
        self._slot = None
        self._buf = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        cls = a.get("class", "").lower()
        slot = None
        if tag in ("h1", "h2", "h3") and "issue" in cls:
            slot = "issue"
        elif tag == "time":
            slot = "date"
        elif tag == "p" and "status" in cls:
            slot = "status"
        elif tag == "p" and "what" in cls:
            slot = "what"
        elif tag == "a" and "url" in cls:
            slot = "url"
        self._flush()
        self._slot = slot

    def handle_endtag(self, tag):
        self._flush()

    def handle_data(self, data):
        if self._slot:
            self._buf.append(data)

    def _flush(self):
        if self._slot and self._buf:
            text = " ".join("".join(self._buf).split())
            if text and not self.facts[self._slot]:
                self.facts[self._slot] = text
        self._slot = None
        self._buf = []

    def close(self):
        super().close()
        self._flush()


def read_page(path):
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        html = fh.read()
    p = IssueParser()
    p.feed(html)
    p.close()
    return p.facts


def main(argv=None):
    ap = argparse.ArgumentParser(prog="issue_watch.py")
    ap.add_argument("--pages", required=True)
    ap.add_argument("--out", default="data.csv")
    args = ap.parse_args(argv)

    if not os.path.isdir(args.pages):
        print("error: --pages directory not found: %s" % args.pages,
              file=sys.stderr)
        return 2

    rows = []
    for name in sorted(os.listdir(args.pages)):
        full = os.path.join(args.pages, name)
        if not os.path.isfile(full) or not name.lower().endswith(HTML_EXT):
            continue
        f = read_page(full)
        rows.append({
            "Issue": f["issue"] or name,
            "Date checked": f["date"],
            "Page opened": "yes",
            "Status": f["status"],
            "What it showed": f["what"],
            "Source URL": f["url"],
        })
    for name in sorted(os.listdir(args.pages)):
        full = os.path.join(args.pages, name)
        if not os.path.isfile(full) or name.lower().endswith(HTML_EXT):
            continue
        rows.append({
            "Issue": name, "Date checked": "", "Page opened": "no",
            "Status": "", "What it showed": "", "Source URL": "",
        })

    parent = os.path.dirname(os.path.abspath(args.out))
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(args.out, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)
    print("wrote %s (%d rows)" % (args.out, len(rows)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
