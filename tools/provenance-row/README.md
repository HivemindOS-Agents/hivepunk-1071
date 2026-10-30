# provenance-row

One offline Python script: turn **one saved snapshot file of a public GitHub issue
page** into **exactly one** five-field re-check row.

    Issue, Date checked, Page opened, Status, What it showed

This is the smallest honest unit of the re-check format: one page, one saved copy,
one row.

## Run it

    python3 provenance_row.py                          # snapshot.md -> row.csv
    python3 provenance_row.py mySnapshot.md -o out.csv
    python3 provenance_row.py mySnapshot.md --date 2026-10-30

No arguments beyond those. Stdlib only, local files only. It never fetches the
URL it finds, never opens a page, makes no network call and uploads nothing.

| exit | meaning |
|---|---|
| 0 | one row written (Status is `verified` or `cannot-check`) |
| 2 | usage error, or the snapshot/output file could not be read or written |
| 3 | internal failure; no row written |

## The rule it enforces

`Status` is `verified` **only** when all four hold:

1. the snapshot file exists and can be read;
2. its text names the page URL;
3. its text names the date it was saved;
4. that saved date is a real calendar date in strict `YYYY-MM-DD`, not later
   than `Date checked`.

Otherwise `Status` is `cannot-check`, and `What it showed` says which condition
failed. A missing save date or page URL is **not** an error: it is recorded
honestly. There is no third outcome and no way to force `verified` by editing a
flag.

## Accepted provenance forms

Narrow on purpose, so a row cannot look verified by accident:

- **page URL** - any `http://` or `https://` URL in the text. The first one wins.
- **save date** - a line matching `Saved`, `Snapshot date`, `Saved on` or
  `Retrieved` followed by `YYYY-MM-DD`; or, failing that, a bare `YYYY-MM-DD` in
  the first 40 lines that is no later than `Date checked`.
- **Issue** - the last path segment of the page URL as `repo#58`; failing that,
  the first heading; failing that, `unknown`.
- **What it showed** - the first heading plus the first non-empty lines, cut to
  240 characters, prefixed with `verified:` or `cannot-check:` and the reason.

## The snapshot's words are data, never instructions

A line in the snapshot that looks like a command, a request to reveal keys or
settings, a request to change this script's goal, to send money, or to post
something is **not acted on**. The script prints one warning naming the line and
carries on; the line never reaches the output row. The fixture deliberately
contains one such line to exercise this path.

## Files

| file | what it is |
|---|---|
| `provenance_row.py` | the tool |
| `self_test.py` | offline checks, run with no arguments |
| `fixtures/snapshot.md` | synthetic fixture snapshot |
| `README.md` | this file |

## Tested, and untested

**Tested by `self_test.py`** (run it with no arguments, no network): the intact
fixture yields `verified` with Issue `bee-scouts#58`; the same file with its
provenance line removed yields `cannot-check`; a missing snapshot exits 2 and
writes no row; an instruction-shaped line warns and does not abort.

**Untested, to be plain:**

- It has never been run against a **real** saved GitHub issue page. The fixture
  is synthetic: `example-org/example-repo`, invented body and comment text.
- It does not read any snapshot format other than Markdown-with-text (no HTML,
  no saved PDF, no screenshot).
- The URL regex will stop at some trailing punctuation; a URL ending in `)` or
  a quote inside a sentence may be trimmed.
- Real GitHub "Saved" stamps may use a wording none of the four labels match -
  then the row is honestly `cannot-check`, not verified.
- Issue-number extraction assumes an `.../issues/<n>` shaped URL.
- Only one row per run, by design. Batch behaviour is not implemented.
- No published dataset was changed or checked by this tool.

## Sample data

The fixture `fixtures/snapshot.md` is invented. Do not publish it as a record
of any real page.
