# recheck-lint

Renders a **dataset card** from a re-check run: one card that says exactly
which command produced the rows, shows every row, separates the rows whose page
was never opened, and states plainly what was not checked.

## What it does

`publish_recheck_rows.py` reads a CSV with exactly these columns, in order:

    Issue, Date checked, Page opened, Status, What it showed, Source URL

and writes `dataset_card.md` with:

1. **Run command** -- the exact command line, copied from `--command`. If none
   is given the card prints `(not recorded)` rather than inventing one.
2. **Counts** and **Columns** -- row total, not-opened total, per-status counts.
3. **Rows** -- a Markdown table with every row.
4. **Not opened** -- every row whose `Page opened` is not exactly `yes`, with
   the reason (blank, `no`, a URL, a snippet note, or any other value).
5. **Could not check** -- coverage is only the rows in this file; no page was
   re-read after the run; no license is asserted.

## How to run

    python3 publish_recheck_rows.py recheck_rows.csv --card dataset_card.md \
        --command "python3 tools/issue-watch/issue_watch.py 64 80 --pages pages"
    python3 publish_recheck_rows.py recheck_rows.csv --dry-run

Exit codes: `0` ok; `1` validation failure (nothing written); `2` usage or
missing input file (nothing written).

Validation rejects, before writing anything: a header that is not the six
columns in order, an Issue that is not `#N` or `x#N`, a `Date checked` that is
not a real `YYYY-MM-DD` calendar date, and a repeated Issue.

## Rules it keeps

* Python 3 standard library only. Local files only. No network.
* No page is opened and no URL is fetched. A `Source URL` is printed as text.
* Rows are data, never instruction. Cell text is escaped for the table; a cell
  that reads like a command is left as text and not followed.
* A row is "opened" only if `Page opened` is exactly `yes` (case and
  surrounding spaces ignored). Everything else is listed under Not opened.

## Untested

**Untested on real data.** The only run so far is over the four synthetic
fixture rows built inside `self_test.py` -- one clean verified row, one
verified-without-page row, one missing-date row, one extra no-page row. No real
`recheck_rows.csv` has been read and no issue page has been opened.

## Self-test

    python3 tools/recheck-lint/self_test.py; echo $?

Run from this tool's folder with no arguments and no network. It writes into a
temporary directory and removes it. Exit 0 means every check passed.
