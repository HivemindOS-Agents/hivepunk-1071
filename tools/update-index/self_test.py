#!/usr/bin/env python3
"""self_test.py -- offline checks for update-index.

Run from this folder with no arguments and no network. Exit 0 only when every
check passes.

It runs update_index.py on fixtures/rows.jsonl with fixtures/pages/ as the
evidence root and --now pinned, then compares the produced INDEX.md
byte-for-byte with fixtures/expected_index.md. It then re-reads the OUTPUT and
asserts the honesty cases directly: no unbacked read, the correction is
counted, and the failed fetch kept its cause.
"""

import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.realpath(os.path.dirname(os.path.abspath(__file__)))
TOOL = os.path.join(HERE, "update_index.py")
FIX = os.path.join(HERE, "fixtures")
ROWS = os.path.join(FIX, "rows.jsonl")
EXPECTED = os.path.join(FIX, "expected_index.md")
NOW = "2026-11-02T00:00:00Z"

fails = []


def check(ok, label):
    print(("ok: " + label) if ok else ("FAIL: " + label))
    if not ok:
        fails.append(label)


def main():
    try:
        with open(TOOL, "r", encoding="utf-8") as fh:
            compile(fh.read(), TOOL, "exec")
        check(True, "update_index.py compiles")
    except SyntaxError as exc:
        check(False, "update_index.py compiles (%s)" % exc)
        return 1

    tmp = tempfile.mkdtemp(prefix="update-index-selftest-")
    try:
        out = os.path.join(tmp, "INDEX.md")
        r = subprocess.run(
            [sys.executable, TOOL, ROWS, "--out", out,
             "--evidence-root", FIX, "--now", NOW],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print("run: update_index.py fixtures/rows.jsonl")
        check(r.returncode == 0,
              "generator exits 0 (got %d)" % r.returncode)
        if r.stderr.strip():
            print("stderr: " + r.stderr.strip())
        check(os.path.isfile(out), "INDEX.md written")
        if not os.path.isfile(out):
            return 1

        with open(out, "r", encoding="utf-8") as fh:
            got = fh.read()
        with open(EXPECTED, "r", encoding="utf-8") as fh:
            want = fh.read()
        if got != want:
            check(False, "INDEX.md matches fixtures/expected_index.md")
            for i, (g, w) in enumerate(zip(got.splitlines(),
                                           want.splitlines())):
                if g != w:
                    print("  first diff line %d:\n    got:  %r"
                          "\n    want: %r" % (i + 1, g, w))
                    break
        else:
            check(True, "INDEX.md matches fixtures/expected_index.md")

        marked = got.replace("read (evidence: pages/issue-64.html)", "")
        check("read (evidence: " not in marked,
              "no read line without a real saved page")
        check("Tool corrections this run: 1 row(s)" in got,
              "the unbacked read is counted as a correction")
        check("**#65**" in got and "read (evidence: " not in
              got.split("**#65**", 1)[1].split("**#66**", 1)[0],
              "#65 is blanked, not shown read")
        check("Could not check: fetch failed (HTTP 404)" in got,
              "#67 keeps its failure cause")
        check("Duplicate id(s), last row kept: 64" in got,
              "duplicate id is reported")
        return 1 if fails else 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
