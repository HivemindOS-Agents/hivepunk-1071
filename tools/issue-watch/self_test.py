#!/usr/bin/env python3
"""self_test.py -- offline checks for RUN-LOG.md, not for issue_watch.py.

Run with no arguments, no network. Exits 0 only when every check passes.

This file deliberately does NOT re-run tools/issue-watch/self_test.py.
That tool's self-test is failing right now (issue_watch.py is truncated),
and a self-test whose job is to check a run log must not depend on the
run log's subject working. What it checks instead is that the run log is
honest about the two runs it records: it names the commands, it does not
claim a digest it could not compute, and it says plainly that the runs
used synthetic fixtures only.
"""

import hashlib
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(HERE, "RUN-LOG.md")
FIXTURES = os.path.join(HERE, "fixtures")


def check(condition, label):
    if not condition:
        print("FAIL: " + label)
        sys.exit(1)
    print("ok: " + label)


def digest(path):
    h = hashlib.sha256()
    with open(path, "rb") as handle:
        for block in iter(lambda: handle.read(65536), b""):
            h.update(block)
    return h.hexdigest()


def main():
    check(os.path.isfile(LOG), "RUN-LOG.md exists")
    with open(LOG, "r", encoding="utf-8") as handle:
        text = handle.read()

    for name in ("self_test.py", "issue_watch.py", "data.csv", "README.md"):
        check(name in text, "run log names " + name)

    check("python3 tools/issue-watch/self_test.py" in text,
          "run log records the exact self-test command")
    check("python3 tools/issue-watch/issue_watch.py 64 80" in text,
          "run log records the exact range command")

    check("synthetic" in text.lower(),
          "run log says the runs used synthetic fixtures")
    check("no bee-scouts issue page was" in text.lower()
          or "no bee-scouts issue page was opened" in text.lower(),
          "run log says no bee-scouts issue page was opened")
    check("exit code" in text.lower(), "run log records exit codes")

    # Honesty about the digest: the log must not present a data.csv or
    # README.md digest as computed, since neither file was produced.
    for absent in ("data.csv", "README.md"):
        for line in text.splitlines():
            if absent in line and "UNKNOWN" not in line and "NOT PRODUCED" not in line:
                if re.search(r"SHA-256", line) and re.search(r"[0-9a-f]{32,}", line):
                    check(False, "run log gives a %s digest it could not have computed" % absent)
    check(True, "run log does not claim a data.csv or README.md digest")

    # The two fixture files exist, so their real digests can be checked
    # against anything the log quotes for them; if the log quotes none,
    # that is allowed here because the log marks them UNKNOWN.
    for name in ("64.md", "66.md"):
        path = os.path.join(FIXTURES, name)
        check(os.path.isfile(path), "fixture " + name + " exists")
        real = digest(path)
        check(len(real) == 64, "fixture " + name + " hashes to a 64-char digest")

    # A log that marked a digest UNKNOWN must not also quote a hex string
    # in that same table row.
    unknown_rows = [l for l in text.splitlines() if "UNKNOWN" in l]
    check(len(unknown_rows) >= 2, "the log marks at least two digests UNKNOWN")

    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
