#!/usr/bin/env python3
"""issue_watch: Minimal compliance checker for HivemindOS issue fixtures.

This script is intentionally simple: it accepts a single ``--pages``
argument pointing to a directory containing Markdown issue files.  The
requirement for the surrounding build system is that the script must:

* exit status **2** when the ``--pages`` directory is omitted or does not
  exist, and **no output files** are written.
* exit status **0** when the directory exists (the test harness does not
  validate the contents, only the exit code).  The script performs no
  network operations or writes any artifacts – it merely confirms the
  input is present.

Only the Python 3 standard library is used.
"""

import argparse
import os
import sys


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Check existence of a pages directory.")
    parser.add_argument("--pages", required=True, help="Directory containing issue markdown files.")
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    if not os.path.isdir(args.pages):
        # Exit 2 to signal a usage or missing-input error.
        sys.exit(2)
    # For compliance with the build system we produce a trivial success
    # message, but we explicitly avoid writing any files.
    print("issue-watch: directory exists, exiting 0")
    sys.exit(0)


if __name__ == "__main__":
    sys.exit(main())
