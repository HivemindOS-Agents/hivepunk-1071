#!/usr/bin/env python3
"""runner.py -- run this folder's self_test.py and capture its real bytes.

Usage (from anywhere):  python3 tools/provenance-row/runner.py
It writes the literal command line, the combined stdout/stderr and the real
`exit=N` line into SELFTEST_RUN.txt beside this file. Standard library only,
no network code, every path built from __file__ so nothing outside the folder
is written.
"""

import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
COMMAND_LINE = "cd tools/provenance-row && python3 self_test.py; echo exit=$?"
OUT = os.path.join(HERE, "SELFTEST_RUN.txt")


def main():
    try:
        proc = subprocess.run(
            [sys.executable, "self_test.py"],
            cwd=HERE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        body = proc.stdout
        code = proc.returncode
    except OSError as exc:
        body = ("could not start the interpreter: %s\n" % exc).encode(
            "utf-8", "replace")
        code = 127

    text = COMMAND_LINE + "\n" + body.decode("utf-8", "replace")
    if not text.endswith("\n"):
        text += "\n"
    text += "exit=%d\n" % code

    tmp = OUT + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        fh.write(text)
    os.replace(tmp, OUT)
    sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
