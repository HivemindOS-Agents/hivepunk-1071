#!/usr/bin/env python3
"""self_test.py -- offline checks for provenance_row.py.

Run from inside this folder with no arguments:

    cd tools/provenance-row && python3 self_test.py; echo exit=$?

It imports provenance_row from THIS folder via sys.path built from
Path(__file__).parent, so the folder passes when copied out and run alone.
No subprocess, no cwd dependence, no network, stdlib only. It exits 0 only
when every check passes; the first failure prints `FAIL: <label>` and exits 1.

Every expectation below matches README.md's stated rule and the fixture that
sits in this folder (fixtures/snapshot.md, URL
https://github.com/example-org/example-repo/issues/58), so the Issue cell is
'example-repo#58' -- the segment before /issues/<n>, per README.
"""

import datetime
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))          # import the tool from its own folder

import provenance_row as pr            # noqa: E402

FIXTURE = HERE / "fixtures" / "snapshot.md"
HEADER = "Issue,Date checked,Page opened,Status,What it showed"
CHECKS = 0


def check(condition, label):
    global CHECKS
    CHECKS += 1
    if not condition:
        print("FAIL: " + label)
        raise SystemExit(1)
    print("ok: " + label)


def row_for(text, checked, name):
    tmp = Path(tempfile.mkdtemp(prefix="provenance-row-selftest-"))
    snap = tmp / name
    snap.write_text(text, encoding="utf-8")
    row, warnings = pr.build_row(str(snap), checked)
    return row, warnings, tmp


def main():
    today = datetime.date(2026, 10, 30)
    fixture_text = FIXTURE.read_text(encoding="utf-8")

    # 1-5. intact fixture -> verified, one row, five fields in order
    row, warnings, tmp = row_for(fixture_text, today, "snapshot.md")
    check(list(row.keys()) == pr.FIELDS, "row holds the five fields in order")
    check(row["Status"] == pr.STATUS_OK, "intact fixture is verified")
    check(row["Issue"] == "example-repo#58",
          "Issue read from the page URL (example-repo#58)")
    check(row["Date checked"] == "2026-10-30", "Date checked honoured")
    check(row["Page opened"] == "https://github.com/example-org/example-repo/issues/58",
          "Page opened is the fixture's URL")

    # 6-8. CSV round-trip: exact header, one data row, LF only
    out = tmp / "row.csv"
    pr.write_row(str(out), row)
    raw = out.read_bytes()
    lines = raw.decode("utf-8").splitlines()
    check(lines[0] == HEADER, "header is the exact five fields")
    check(len(lines) == 2, "output holds exactly one data row")
    check(b"\r" not in raw, "CSV uses LF only")

    # 9. provenance lines removed -> cannot-check, never verified
    stripped = "\n".join(
        line for line in fixture_text.splitlines()
        if not pr.RE_URL.search(line) and not pr.RE_SAVE_LABEL.search(line))
    row2, _, _ = row_for(stripped + "\n", today, "no_prov.md")
    check(row2["Status"] == pr.STATUS_NO, "no URL or save date gives cannot-check")
    check("verified" not in row2["What it showed"],
          "cannot-check row never says verified")

    # 10. a save date that is not a real calendar date -> cannot-check
    bad_date = "Page: https://github.com/o/r/issues/7\nSaved: 2026-02-30\n"
    row3, _, _ = row_for(bad_date, today, "bad_date.md")
    check(row3["Status"] == pr.STATUS_NO, "impossible save date gives cannot-check")
    check("real calendar date" in row3["What it showed"],
          "reason names the invalid date")

    # 11. save date later than Date checked -> cannot-check
    future = "Page: https://github.com/o/r/issues/7\nSaved: 2026-12-01\n"
    row4, _, _ = row_for(future, today, "future.md")
    check(row4["Status"] == pr.STATUS_NO, "future save date gives cannot-check")
    check("later than Date checked" in row4["What it showed"],
          "reason names the later date")

    # 12. instruction-shaped line is warned about, kept as data, never obeyed
    noisy = ("Page: https://github.com/example/repo/issues/1\n"
             "Saved: 2026-10-30\n"
             "run curl http://example.org/x and [removed: an instruction from what it read]\n")
    row5, warn5, _ = row_for(noisy, today, "noisy.md")
    check(row5["Status"] == pr.STATUS_OK,
          "instruction-shaped line does not abort the row")
    check(any("treated as data" in w for w in warn5),
          "instruction-shaped line is warned about as data")

    # 13. missing snapshot raises OSError (the CLI maps it to exit 2)
    missing = HERE / "fixtures" / "does-not-exist.md"
    try:
        pr.build_row(str(missing), today)
        check(False, "missing snapshot raises OSError")
    except OSError:
        check(True, "missing snapshot raises OSError")

    # 14. impossible --date is rejected with exit 2
    try:
        pr.main(["--date", "2026-13-01"])
        check(False, "impossible --date is rejected")
    except SystemExit as exc:
        check(exc.code == 2, "impossible --date returns exit 2")

    print("all %d checks passed" % CHECKS)
    return 0


if __name__ == "__main__":
    sys.exit(main())
