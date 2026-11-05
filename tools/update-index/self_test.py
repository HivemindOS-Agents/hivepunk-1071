#!/usr/bin/env python3
"""self_test.py -- offline checks for update-index (index_build.py).

Run from this folder with no arguments and no network:

    python3 self_test.py ; echo $?

It builds a throwaway notes folder under the system temp dir, runs
index_build.py on it, and checks: exit 0; one row per .md; rows sorted by path;
a saved date shown; an empty date slot for a note without one; a row still
written for a note with no heading; pipes escaped; the output file never
indexed as a row; non-.md files ignored; a second run byte-identical; a
non-zero exit when the folder is missing. It then runs the builder on the
shipped example/notes/ folder and compares with the committed example/index.md
byte for byte. It never reaches another tool's folder. Exit 0 only when every
check passes.
"""

import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.realpath(os.path.dirname(os.path.abspath(__file__)))
TOOL = os.path.join(HERE, "index_build.py")
EXAMPLE = os.path.join(HERE, "example")

fails = []


def check(ok, label):
    print(("ok: " + label) if ok else ("FAIL: " + label))
    if not ok:
        fails.append(label)


def run(notes_dir, out_path):
    return subprocess.run(
        [sys.executable, TOOL, notes_dir, "-o", out_path],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=HERE)


NOTE_A = """# Check-in 12

Saved: 2026-11-04
Some body text.
"""

NOTE_B = """Saved: 2026-11-03

Body first, heading later.

## A | heading with a pipe

More text.
"""

NOTE_C = """Just a paragraph, no heading at all.
Saved: not-a-date
"""


def write_fixture(tmp):
    notes = os.path.join(tmp, "notes")
    os.makedirs(os.path.join(notes, "sub"), exist_ok=True)
    with open(os.path.join(notes, "a.md"), "w", encoding="utf-8") as fh:
        fh.write(NOTE_A)
    with open(os.path.join(notes, "b.md"), "w", encoding="utf-8") as fh:
        fh.write(NOTE_B)
    with open(os.path.join(notes, "sub", "c.md"), "w", encoding="utf-8") as fh:
        fh.write(NOTE_C)
    # A non-.md file must be ignored entirely.
    with open(os.path.join(notes, "draft.txt"), "w", encoding="utf-8") as fh:
        fh.write("# Should not appear\n\nSaved: 2026-11-01\n")
    return notes


def main():
    check(os.path.isfile(TOOL), "index_build.py found at %s" % TOOL)
    if not os.path.isfile(TOOL):
        return 1
    with open(TOOL, "r", encoding="utf-8") as fh:
        try:
            compile(fh.read(), TOOL, "exec")
        except SyntaxError as exc:
            check(False, "index_build.py compiles (%s)" % exc)
            return 1
    check(True, "index_build.py compiles")

    tmp = tempfile.mkdtemp(prefix="update-index-selftest-")
    try:
        notes = write_fixture(tmp)
        out = os.path.join(tmp, "index.md")

        r = run(notes, out)
        if r.stderr.strip():
            print("stderr: " + r.stderr.strip())
        check(r.returncode == 0, "builder exits 0 (got %d)" % r.returncode)
        if not os.path.isfile(out):
            check(False, "index.md written")
            return 1
        check(True, "index.md written")
        with open(out, "r", encoding="utf-8") as fh:
            got = fh.read()

        row_a = "- a.md | Check-in 12 | 2026-11-04"
        row_b = "- b.md | A \\| heading with a pipe | 2026-11-03"
        row_c = "- sub/c.md |  |"

        check(row_a in got, "one row for a.md with its heading and saved date")
        check(row_b in got, "pipe in the heading is escaped as \\|")
        check(row_c in got, "a note with no heading still gets a row")
        check("sub/c.md |  | 2026" not in got,
              "a non-date Saved: line leaves the date slot empty")
        check("draft.txt" not in got, "non-.md files are ignored")

        positions = [got.index(row_a), got.index(row_b), got.index(row_c)]
        check(positions == sorted(positions), "rows are sorted by path")

        body = [ln for ln in got.splitlines() if ln.startswith("- ")]
        check(len(body) == 3, "exactly one row per .md file (got %d)" % len(body))
        check("- index.md |" not in got,
              "the output file is not indexed as a row")
        check(got.endswith("\n"), "the index ends with a newline")

        out2 = os.path.join(tmp, "index2.md")
        r2 = run(notes, out2)
        check(r2.returncode == 0, "second run exits 0")
        with open(out2, "r", encoding="utf-8") as fh:
            got2 = fh.read()
        check(got == got2, "a second run over the same folder is byte-identical")

        r3 = run(os.path.join(tmp, "does-not-exist"),
                 os.path.join(tmp, "index3.md"))
        check(r3.returncode != 0, "a missing folder exits non-zero (got %d)"
              % r3.returncode)

        # The shipped example must match what the builder produces.
        shipped = os.path.join(EXAMPLE, "index.md")
        check(os.path.isfile(shipped), "example/index.md found")
        if os.path.isfile(shipped):
            ex_out = os.path.join(tmp, "example-index.md")
            r4 = run(os.path.join(EXAMPLE, "notes"), ex_out)
            check(r4.returncode == 0, "builder runs on example/notes/")
            if os.path.isfile(ex_out):
                with open(shipped, "r", encoding="utf-8") as fh:
                    want = fh.read()
                with open(ex_out, "r", encoding="utf-8") as fh:
                    have = fh.read()
                check(want == have,
                      "example/index.md matches the builder on example/notes/")
            else:
                check(False, "builder produced the example index")

        if fails:
            print("\n%d check(s) failed" % len(fails))
            return 1
        print("\nok: all index_build checks pass")
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
