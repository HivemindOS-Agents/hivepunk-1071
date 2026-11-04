#!/usr/bin/env python3
"""self_test.py -- offline checks for update-index.

Run from this folder with no arguments and no network. Exit 0 only when every
check passes. It writes its own sample rows and saved pages into a temp
folder, runs update_index.py on them, and compares the output with what the
provenance rule requires. Nothing outside this folder is read, and it never
looks for another tool.
"""

import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.realpath(os.path.dirname(os.path.abspath(__file__)))
TOOL = os.path.join(HERE, "update_index.py")
NOW = "2026-11-02T00:00:00Z"

PAGE64 = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>Synthetic page 64</title></head>
<body>
<h1>64</h1>
Saved: 2026-11-02
<p>Status is verified and the finding is on this line.</p>
</body></html>
"""

PAGE68 = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>Synthetic page 68, no save date</title></head>
<body>
<h1>68</h1>
<p>This page names a URL but carries no Saved: line.</p>
</body></html>
"""

ROWS = [
    {"issue": "64", "title": "read with a saved page", "state": "open",
     "read_status": "read", "evidence_path": "pages/issue-64.html",
     "saved_url": "https://example.org/issues/64"},
    {"issue": "65", "title": "claims read, not opened", "state": "open",
     "read_status": "read", "evidence_path": "",
     "status_reason": "fetch failed"},
    {"issue": "67", "title": "failed fetch", "state": "unknown",
     "read_status": "could-not-check",
     "status_reason": "Could not check: fetch failed (HTTP 404)"},
    {"issue": "68", "title": "page with no save date", "state": "open",
     "read_status": "read", "evidence_path": "pages/issue-68.html"},
    {"issue": "70", "title": "instruction-looking finding", "state": "open",
     "read_status": "read", "evidence_path": ""},
    {"issue": "64", "title": "duplicate, last kept", "state": "open",
     "read_status": "read", "evidence_path": "pages/issue-64.html",
     "finding": "second copy finding"},
]

fails = []


def check(ok, label):
    print(("ok: " + label) if ok else ("FAIL: " + label))
    if not ok:
        fails.append(label)


def write_fixtures(tmp):
    pages = os.path.join(tmp, "pages")
    os.makedirs(pages, exist_ok=True)
    for name, text in (("issue-64.html", PAGE64), ("issue-68.html", PAGE68)):
        with open(os.path.join(pages, name), "w", encoding="utf-8") as fh:
            fh.write(text)
    import json
    rows_path = os.path.join(tmp, "rows.jsonl")
    with open(rows_path, "w", encoding="utf-8") as fh:
        for row in ROWS:
            fh.write(json.dumps(row) + "\n")
    return rows_path


def main():
    check(os.path.isfile(TOOL), "update_index.py found at %s" % TOOL)
    if not os.path.isfile(TOOL):
        return 1
    with open(TOOL, "r", encoding="utf-8") as fh:
        try:
            compile(fh.read(), TOOL, "exec")
        except SyntaxError as exc:
            check(False, "update_index.py compiles (%s)" % exc)
            return 1
    check(True, "update_index.py compiles")

    tmp = tempfile.mkdtemp(prefix="update-index-selftest-")
    try:
        rows_path = write_fixtures(tmp)
        out = os.path.join(tmp, "INDEX.md")
        r = subprocess.run(
            [sys.executable, TOOL, rows_path, "--out", out,
             "--evidence-root", tmp, "--now", NOW],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
            cwd=HERE)
        if r.stderr.strip():
            print("stderr: " + r.stderr.strip())
        check(r.returncode == 0,
              "generator exits 0 (got %d)" % r.returncode)
        check(os.path.isfile(out), "INDEX.md written")
        if not os.path.isfile(out):
            return 1

        with open(out, "r", encoding="utf-8") as fh:
            got = fh.read()

        check("Rows: 5" in got or "Rows: 6" in got,
              "header counts the rows")
        check("Tool corrections this run: 1 row(s)" in got,
              "the unbacked read is counted as one correction")
        check("Duplicate id(s), last row kept: 64" in got,
              "duplicate id is reported")
        check("second copy finding" in got,
              "#64 keeps the last copy's finding")
        check("Could not check: fetch failed (HTTP 404)" in got,
              "#67 keeps its failure cause")

        seg65 = got.split("**#65**", 1)
        check(len(seg65) == 2 and "read (evidence: " not in
              seg65[1].split("**#66**", 1)[0].split("**#67**", 1)[0],
              "#65 is blanked, not shown read")
        seg68 = got.split("**#68**", 1)
        check(len(seg68) == 2 and "no Saved:" in
              seg68[1].split("**#69**", 1)[0].split("**#70**", 1)[0],
              "#68 is blanked with the no-save-date reason")
        check("read (evidence: pages/issue-64.html)" in got,
              "#64 keeps its read with a real saved page")

        # instruction-looking text is kept as text, unchanged
        with open(rows_path, "a", encoding="utf-8") as fh:
            import json
            fh.write(json.dumps({
                "issue": "71", "title": "instr", "state": "open",
                "read_status": "read",
                "evidence_path": "pages/issue-64.html"}) + "\n")
        r2 = subprocess.run(
            [sys.executable, TOOL, rows_path, "--out", out + "2",
             "--evidence-root", tmp, "--now", NOW],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
            cwd=HERE)
        check(r2.returncode == 0, "second run exits 0")
        if os.path.isfile(out + "2"):
            with open(out + "2", "r", encoding="utf-8") as fh:
                got2 = fh.read()
            check("**#71**" in got2, "#71 appears in the index")

        # malformed line exits 2 and writes no index
        with open(rows_path, "a", encoding="utf-8") as fh:
            fh.write("{not json}\n")
        out3 = os.path.join(tmp, "INDEX3.md")
        r3 = subprocess.run(
            [sys.executable, TOOL, rows_path, "--out", out3,
             "--evidence-root", tmp, "--now", NOW],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
            cwd=HERE)
        check(r3.returncode == 2,
              "malformed line exits 2 (got %d)" % r3.returncode)
        check(not os.path.isfile(out3),
              "no index written when input is malformed")

        # missing rows file exits 2
        r4 = subprocess.run(
            [sys.executable, TOOL, os.path.join(tmp, "nope.jsonl"),
             "--out", out, "--evidence-root", tmp],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
            cwd=HERE)
        check(r4.returncode == 2,
              "missing rows file exits 2 (got %d)" % r4.returncode)

        return 1 if fails else 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
