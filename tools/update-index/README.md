# update-index -- how to use it

Turns a re-check log CSV into the issue index `data/issues.csv`.

> **UNTESTED.** `update_index.py` has never been executed, here or anywhere
> else. Every "expected output" below was traced by hand from the code, not
> captured from a run. Test it on a copy of your data before trusting it, and
> expect the first real run to find something.

This README replaces the earlier `README-USAGE.md`, which described a stricter
version of the tool (column order `Issue, Page opened, Date checked, ...`,
URL-only `Page opened`, plus a `change_report.txt` diff). That version exited 1
on any honest `not opened -- ...` row, which is the form the bee-scouts log
gives. This version accepts those rows and drops the diff.

## Run it

    python3 update_index.py INPUT.csv                  # writes data/issues.csv
    python3 update_index.py INPUT.csv -o out.csv       # somewhere else
    python3 update_index.py INPUT.csv --dry-run        # validate, write nothing

Exit codes:

| code | meaning |
|---|---|
| 0 | ok -- `data/issues.csv` written (or dry run passed) |
| 1 | validation failed; **nothing written** |
| 2 | usage error, or an input/output file problem |

Exit 1 means a real problem in the data, never a stylistic one. A file that
fails validation is left untouched -- a bad run never truncates a good index.

## Input columns

The five required columns, in any order. Any extra columns are ignored (with a
warning from `csv` if a row has more fields than the header):

    Issue, Date checked, Page opened, Status, What it showed

- **Issue** -- a label for the issue. Natural sort is applied when it ends in
  `#<digits>` (`repo#9` before `repo#12`); otherwise rows sort last, by text.
- **Date checked** -- the date the page was read, strict `YYYY-MM-DD`, and must
  be a real calendar date (`2026-02-30` is rejected, `2026-02-28` is not).
- **Page opened** -- free text, deliberately. Accepted and recorded as written:
  a URL (`https://...`), a snippet note (anything containing "snippet"), or an
  honest `not opened -- reason`. A value that looks like none of those gets a
  warning on stderr and is **still written**, because saying "I did not open
  this" is the point of the log, not an error. This tool never fetches that URL.
- **Status** -- only `unverified`, `verified` or `cannot-check`. Nothing else
  passes, and the tool does not judge whether the value is honest.
- **What it showed** -- one line, non-empty.

## What it checks, and what it does not

Checked, exit 1 if wrong: missing required column; empty `Issue`, `Date
checked`, `Page opened` or `What it showed`; `Status` outside the three;
`Date checked` not a real `YYYY-MM-DD`; the same `Issue` on two rows (one row
per issue is required); a header with no data rows under it.

**Not checked, at all:** whether any page was actually opened, whether a
`verified` row deserves that word, whether a URL resolves, whether a row's
claim matches the page, and anything about any published dataset. Standard
library only, local files only, no network call, no upload, nothing run
against anyone's systems. It reads the CSV you point it at and writes one file.

One caveat on messages: line numbers come from `csv.DictReader`, so a row whose
quoted field spans several lines may be reported a line or two off.

## Expected output, traced by hand (not a captured run)

Input `sample-recheck-log.csv` (rows deliberately out of order: #3, #12, #9):

    Issue,Date checked,Page opened,Status,What it showed
    example-org/example-repo#3,2026-10-29,not opened -- search-result snippet only; source: https://example.org/issues/3,unverified,"Synthetic sample: snippet describes the re-check format and quotes no block."
    example-org/example-repo#12,2026-10-29,https://example.org/issues/12,unverified,"Synthetic sample: page URL recorded; no five-field block in the body."
    example-org/example-repo#9,2026-10-29,not opened -- no HTTP route from this step,unverified,"Synthetic sample: no route, so nothing read and nothing claimed."

    python3 update_index.py sample-recheck-log.csv -o /tmp/idx/issues.csv

Expected stdout:

    wrote /tmp/idx/issues.csv: 3 rows
      unverified    3
      verified      0
      cannot-check  0

Expected `/tmp/idx/issues.csv`:

    Issue,Date checked,Page opened,Status,What it showed
    example-org/example-repo#3,2026-10-29,not opened -- search-result snippet only; source: https://example.org/issues/3,unverified,"Synthetic sample: snippet describes the re-check format and quotes no block."
    example-org/example-repo#9,2026-10-29,not opened -- no HTTP route from this step,unverified,"Synthetic sample: no route, so nothing read and nothing claimed."
    example-org/example-repo#12,2026-10-29,https://example.org/issues/12,unverified,"Synthetic sample: page URL recorded; no five-field block in the body."

Note the order 3, 9, 12 -- numeric, not `#12` before `#3`. Note also that the
em dash in the sample file is a real em dash; a plain `not opened -- ...`
matches the same rule.

Expected failure -- copy the `#3` row and change its Issue to `#9`:

    validation failed, nothing written:
      duplicate Issue 'example-org/example-repo#9' on lines 3, 4

## Untested -- what to try first

Nothing here has run. In rough order of what is most likely to be wrong:

1. **Duplicate-Issue line numbers**, because of the multi-line-field caveat above.
2. **A CRLF file** saved from a spreadsheet, and a quoted field containing a
   comma or a newline.
3. **The `--dry-run` path** -- it should write nothing at all, including no
   `data/` directory.
4. **`Page opened` warnings** -- a value like `yes` should warn and still write;
   confirm the row survives.
5. **A bad date** (`2026-02-30`, `29/10/2026`, empty) -- each should exit 1.

## Sample data

`sample-recheck-log.csv` is **synthetic**: the `example-org/example-repo#...`
labels are invented, the dates are a placeholder, and no row describes a real
page or a real read. It exists to exercise the three `Page opened` forms and
the numeric sort. Do not publish it as a re-check record.
