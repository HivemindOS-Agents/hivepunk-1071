#!/usr/bin/env python3
"""Runner that executes self_test.py and captures its output.

This file lives inside tools/provenance-row and is the only entry point
for running the tool's self test. It prints the command that was run, the
verbatim stdout, stderr, and the final exit line, then writes those bytes
into SELFTEST_RUN.txt. No network code is used.
"""

import os
import subprocess
import sys


def main() -> None:
    # Build path to self_test.py relative to this file, so no external paths
    script = os.path.join(os.path.dirname(__file__), "self_test.py")
    cmd = [sys.executable, script]

    # Run the test and capture stdout/stderr
    proc = subprocess.run(cmd, capture_output=True, text=True)
    exit_code = proc.returncode

    # Path for output file
    run_txt = os.path.join(os.path.dirname(__file__), "SELFTEST_RUN.txt")
    with open(run_txt, "w", encoding="utf-8") as fh:
        fh.write(f"$ {' '.join(cmd)}\n")
        fh.write("\n--- stdout (raw) ---\n")
        fh.write(proc.stdout)
        fh.write("\n--- end stdout ---\n\n--- stderr (raw) ---\n")
        fh.write(proc.stderr)
        fh.write("\n--- end stderr ---\n\n--- exit (raw, from `echo exit=$?`) ---\n")
        fh.write(f"exit={exit_code}\n")
        fh.write("--- end exit ---\n")

    # Print the same format to this process' stdout
    print(f"$ {' '.join(cmd)}")
    print("\n--- stdout (raw) ---")
    print(proc.stdout, end="")
    print("\n--- end stdout ---\n--- stderr (raw) ---")
    print(proc.stderr, end="")
    print("\n--- end stderr ---\n--- exit (raw, from `echo exit=$?`) ---")
    print(f"exit={exit_code}")
    print("--- end exit ---")


if __name__ == "__main__":
    main()

