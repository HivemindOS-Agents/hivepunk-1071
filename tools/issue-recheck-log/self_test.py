#!/usr/bin/env python3
"""self_test.py -- offline checks for issue-recheck-log.

Run from this tool's folder with no arguments and no network. It imports the
tool's own code and runs it on the sample files in this folder, comparing what
comes out with what should. Exit 0 only when every check passes.
"""

import os
import sys

HERE = os.path.realpath(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)

import verify_rows  # noqa: E402

fails = []


def check(ok, label):
    print(("ok: " + label) if ok else ("FAIL: " + label))
    if not ok:
        fails.append(label)


def main():
    card = os.path.join(HERE, "README.md")
    rows = os.path.join(HERE, "rows.csv")

    check(os.path.isfile(card), "README.md card found")
    check(os.path.isfile(rows), "rows.csv found")
    if not (os.path.isfile(card) and os.path.isfile(rows)):
        return 1

    problems = verify_rows.verify(card, rows, require_sections=(
        "Not opened", "Could not check"))
    check(problems == [], "shipped card + rows.csv pass validation")
    for p in problems:
        print("  problem: " + p)

    # The honesty rule must actually bite: a claimed read with no saved page
    # has to be reported, not passed.
    bad = os.path.join(HERE, "fixtures", "bad_claims_read.csv")
    bad_problems = verify_rows.verify(card, bad, require_sections=())
    check(any("saved_page_opened is false" in p for p in bad_problems),
          "an unopened row with a filled read_status is rejected")

    # And an unopened row carrying a title (snippet-looking) is rejected too.
    bad2 = os.path.join(HERE, "fixtures", "bad_title_from_snippet.csv")
    bad2_problems = verify_rows.verify(card, bad2, require_sections=())
    check(any("filled" in p and "saved" in p for p in bad2_problems),
          "snapshot fields on an unopened row are rejected")

    # A card that claims a licence must be rejected.
    badcard = os.path.join(HERE, "fixtures", "card_with_license.md")
    card_problems = verify_rows.verify(badcard, rows, require_sections=())
    check(any("license" in p.lower() or "licence" in p.lower()
              for p in card_problems),
          "a card that declares a licence is rejected")

    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
