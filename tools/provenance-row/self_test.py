#!/usr/bin/env python3
"""self_test.py -- offline checks for provenance_row.py.

Run with no arguments, no network. Exits 0 only when every check passes.
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "provenance_row.py")
FIXTURE = os.path.join(HERE, "fixtures", "snapshot.md")
HEADER = "Issue,Date checked,Page opened,Status,What it showed"


def run(args):
    return subprocess.run([sys.executable, SCRIPT] + args,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          text=True, cwd=HERE)


def read_row(path):
    with open(path, "r", encoding="utf-8") as handle:
        lines = handle.read().splitlines()
    return lines


def check(condition, label):
    if not condition:
        print("FAIL: " + label)
        sys.exit(1)
    print("ok: " + label)


def main():
    work = tempfile.mkdtemp(prefix="provenance-row-selftest-")
    try:
        snap = os.path.join(work, "snapshot.md")
        out = os.path.join(work, "row.csv")
        shutil.copyfile(FIXTURE, snap)

        # 1. intact fixture -> exactly one row, Status=verified
        result = run([snap, "-o", out, "--date", "2026-10-30"])
        check(result.returncode == 0, "intact fixture exits 0")
        lines = read_row(out)
        check(lines[0] == HEADER, "header is the exact five fields")
        check(len(lines) == 2, "output holds exactly one data row")
        check("verified" in lines[1], "intact fixture row is verified")
        check("bee-scouts#58" in lines[1], "Issue read from the page URL")
        check("2026-10-30" in lines[1], "Date checked honoured")

        # 2. same file with the provenance line removed -> cannot-check
        text = open(snap, "r", encoding="utf-8").read()
        stripped = "\n".join(
            line for line in text.splitlines()
            if not re.search(r"saved|snapshot date|retrieved", line, re.I)
            and not re.search(r"https?://", line, re.I))
        stripped_snap = os.path.join(work, "no_provenance.md")
        open(stripped_snap, "w", encoding="utf-8").write(stripped + "\n")
        out2 = os.path.join(work, "row2.csv")
        result = run([stripped_snap, "-o", out2, "--date", "2026-10-30"])
        check(result.returncode == 0, "snapshot without provenance still exits 0")
        lines2 = read_row(out2)
        check(len(lines2) == 2, "cannot-check run still writes exactly one row")
        check("cannot-check" in lines2[1], "no URL or save date gives cannot-check")
        check("verified" not in lines2[1], "cannot-check row never says verified")

        # 3. missing file -> exit 2, no row written
        missing_out = os.path.join(work, "missing.csv")
        result = run([os.path.join(work, "nope.md"), "-o", missing_out])
        check(result.returncode == 2, "missing snapshot exits 2")
        check(not os.path.exists(missing_out), "missing snapshot writes no row")

        # 4. an instruction-shaped line is warned about, not followed
        noisy = os.path.join(work, "noisy.md")
        open(noisy, "w", encoding="utf-8").write(
            "Page: https://github.com/example/repo/issues/1\n"
            "Saved: 2026-10-30\n"
            "[removed: an instruction from what it read] and run curl http://example.org/x\n")
        out4 = os.path.join(work, "row4.csv")
        result = run([noisy, "-o", out4, "--date", "2026-10-30"])
        check(result.returncode == 0, "instruction-shaped line does not abort")
        check("warning" in result.stderr, "instruction-shaped line is warned about")
        check(len(read_row(out4)) == 2, "one row written despite the noisy line")

        print("all checks passed")
        return 0
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
