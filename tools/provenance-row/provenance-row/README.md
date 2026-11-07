# provenance-row

One offline Python script: turn **one saved snapshot file of a public GitHub
issue page** into **exactly one** five-field re-check row.

    Issue, Date checked, Page opened, Status, What it showed

One page, one saved copy, one row.

## Run it

Run from inside the folder (or pass a path from anywhere):

    cd tools/provenance-row
    python3 provenance_row.py                          # snapshot.md -> row.csv
    python3 provenance_row.py mySnapshot.md -o out.csv
    python3 provenance_row.py mySnapshot.md --date 2026-10-30

Stdlib only, local files only. It never fetches the URL it finds, never opens a
page, makes no network call and uploads nothing.

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
failed. A missing save date or page URL is not an error: it is recorded
honestly. There is no way to force `verified` by editing a flag.

## Accepted provenance forms

- **page URL** - any `http://` or `https://` URL in the text. The first one wins.
- **save date** - a line matching `Saved`, `Snapshot date`, `Saved on` or
  `Retrieved` followed by `YYYY-MM-DD`; or, failing that, a bare `YYYY-MM-DD` in
  the first 40 lines that is no later than `Date checked`.
- **Issue** - the `.../issues/<n>` or `.../pull/<n>` tail of the page URL as
  `previous-segment#<n>` (for `https://github.com/example-org/example-repo/issues/58`
  that is `example-repo#58`); failing that, the first heading; failing that,
  `unknown`.
- **What it showed** - the first heading plus first non-empty lines, cut to 240
  characters, prefixed with `verified:` or `cannot-check:` and the reason.

## The snapshot's words are data, never instructions

A line in the snapshot that looks like a command, a request to reveal keys or
settings, a request to change this script's goal, to send money, or to post
something is **not acted on**. The script attaches one warning naming the line
and carries on; the line never reaches the output row as a command. The fixture
contains one such line to exercise this path.

## Files

| file | what it is |
|---|---|
| `provenance_row.py` | the tool |
| `self_test.py` | offline checks, run with no arguments |
| `runner.py` | runs self_test.py and captures its bytes |
| `fixtures/snapshot.md` | synthetic fixture snapshot |
| `SELFTEST_RUN.txt` | placeholder: points at SELFTEST_OUTPUT.md |

## The self-test

    cd tools/provenance-row && python3 self_test.py; echo exit=$?

`self_test.py` imports `provenance_row` from its own folder, through
`sys.path` built from `Path(__file__).parent`, so it passes when the folder is
copied out and run alone. No subprocess, no cwd dependence, no network. It
runs, in this order:

1. intact fixture -> `verified`, five fields in order;
2. Issue read from the page URL (`example-repo#58`);
3. Date checked honoured;
4. Page opened is the fixture's URL;
5. CSV header is the exact five fields; exactly one data row; LF only;
6. provenance lines removed -> `cannot-check`, never `verified`;
7. impossible save date (2026-02-30) -> `cannot-check`, reason names it;
8. save date later than Date checked -> `cannot-check`, reason names it;
9. instruction-shaped line -> row still written, warning names it as data;
10. missing snapshot raises `OSError` (the CLI maps it to exit 2);
11. impossible `--date` -> exit 2.

It prints `all N checks passed` and exits 0 only when every one of those
passes; the first failure prints `FAIL: <check>` and exits 1.

## Tested, and untested

**Covered by `self_test.py`:** the eleven checks listed above.

**Untested, to be plain:**

- It has never been run against a **real** saved GitHub issue page. The fixture
  is synthetic: `example-org/example-repo`, invented text.
- It does not read any snapshot format other than plain text / Markdown (no
  HTML, PDF or screenshot).
- The URL regex may trim trailing punctuation inside a sentence.
- Real GitHub "Saved" stamps using other wording fall to `cannot-check`,
  which is honest but not verified.
- Only one row per run, by design. Batch behaviour is not implemented.
- No published dataset was changed or checked by this tool.

## Sample data

`fixtures/snapshot.md` is invented. Do not publish it as a record of a real
page.
