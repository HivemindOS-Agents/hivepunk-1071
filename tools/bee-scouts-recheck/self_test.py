#!/usr/bin/env python3
"""self_test.py -- offline checks for the bee-scouts-recheck publish package.

Run from this folder with no arguments and no network:

    python3 self_test.py ; echo $?

It compiles check_package.py, runs it on the shipped package (which must be
publishable as it stands), then builds synthetic packages in a temp folder and
checks that the checker rejects a card that claims a licence, a reordered
header, and a non-read row that carries a finding. It never reads another
tool's folder and never touches the network. Exit 0 only when every check
passes.
"""

import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.realpath(os.path.dirname(os.path.abspath(__file__)))
CHECKER = os.path.join(HERE, "check_package.py")

fails = []


def check(ok, label):
    print(("ok: " + label) if ok else ("FAIL: " + label))
    if not ok:
        fails.append(label)


def run_checker(folder):
    return subprocess.run([sys.executable, CHECKER, "--folder", folder],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          text=True, cwd=HERE)


GOOD_CARD = """# bee-scouts re-check

One row per public issue page the re-check pass looked at.

## Columns

issue, saved_page_opened, read_status, checked_at, evidence_path, finding.

## The provenance rule

A row is read only when the saved page was opened, exists and carries a
Saved: YYYY-MM-DD line.

## How to use it

~~~python
import pandas as pd
df = pd.read_csv("data.csv", dtype=str, keep_default_na=False)
~~~

## How it was made

Written offline from a rows file and a folder of saved pages.

## What could not be checked / current state

No live page was opened, so data.csv has its header and no rows.

## Licence

None claimed.
"""

GOOD_CSV = "issue,saved_page_opened,read_status,checked_at,evidence_path,finding\n"


def write_package(tmp, card, csv):
    with open(os.path.join(tmp, "README.md"), "w", encoding="utf-8") as fh:
        fh.write(card)
    with open(os.path.join(tmp, "data.csv"), "w", encoding="utf-8") as fh:
        fh.write(csv)


def main():
    check(os.path.isfile(CHECKER), "check_package.py found at %s" % CHECKER)
    if not os.path.isfile(CHECKER):
        return 1
    with open(CHECKER, "r", encoding="utf-8") as fh:
        try:
            compile(fh.read(), CHECKER, "exec")
        except SyntaxError as exc:
            check(False, "check_package.py compiles (%s)" % exc)
            return 1
    check(True, "check_package.py compiles")

    check(os.path.isfile(os.path.join(HERE, "README.md")),
          "shipped README.md found")
    check(os.path.isfile(os.path.join(HERE, "data.csv")),
          "shipped data.csv found")
    check(os.path.isfile(os.path.join(HERE, "discussion-post.md")),
          "shipped discussion-post.md found")

    # 1. The shipped package must be publishable as it stands.
    r = run_checker(HERE)
    if r.stderr.strip():
        print("stderr: " + r.stderr.strip())
    check(r.returncode == 0,
          "shipped package passes (got %d)" % r.returncode)
    print("    " + (r.stdout.strip() or "(no output)").replace("\n", "\n    "))

    # 2. Synthetic packages in a temp folder.
    tmp = tempfile.mkdtemp(prefix="bee-scouts-recheck-selftest-")
    try:
        good = os.path.join(tmp, "good")
        os.makedirs(good)
        write_package(good, GOOD_CARD, GOOD_CSV)
        rg = run_checker(good)
        check(rg.returncode == 0, "synthetic good package passes (got %d)"
              % rg.returncode)

        # 2a. A card that declares a licence must be rejected.
        lic = os.path.join(tmp, "licence")
        os.makedirs(lic)
        write_package(lic, GOOD_CARD.replace("None claimed.", "MIT."),
                      GOOD_CSV)
        rl = run_checker(lic)
        check(rl.returncode != 0, "card claiming a licence is rejected")
        check(rl.returncode == 2, "licence rejection exits 2 (got %d)"
              % rl.returncode)

        # 2b. A reordered header must be rejected.
        order = os.path.join(tmp, "order")
        os.makedirs(order)
        write_package(order, GOOD_CARD,
                      "issue,checked_at,saved_page_opened,read_status,"
                      "evidence_path,finding\n")
        ro = run_checker(order)
        check(ro.returncode != 0, "reordered header is rejected")

        # 2c. A non-read row carrying a finding must be rejected.
        filled = os.path.join(tmp, "filled")
        os.makedirs(filled)
        write_package(filled, GOOD_CARD,
                      GOOD_CSV +
                      'ex/1,no,not-opened,,,"claims something"\n')
        rf = run_checker(filled)
        check(rf.returncode != 0,
              "non-read row carrying a finding is rejected")

        # 2d. An unread row with blank facts is allowed.
        blank = os.path.join(tmp, "blank")
        os.makedirs(blank)
        write_package(blank, GOOD_CARD,
                      GOOD_CSV + "ex/2,no,not-opened,,,\n")
        rb = run_checker(blank)
        check(rb.returncode == 0,
              "unread row with blank facts is allowed (got %d)"
              % rb.returncode)

        return 1 if fails else 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
