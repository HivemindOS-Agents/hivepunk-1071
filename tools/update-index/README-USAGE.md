# issue-index upkeep -- how to run it

Run `python3 update_index.py INPUT.csv -o OUTDIR` on a five-column index
(`Issue, Page opened, Date checked, Status, What it showed`). It writes
`OUTDIR/issues.csv` (natural sort by Issue) and `OUTDIR/change_report.txt`
(ADDED / REMOVED / CHANGED against the previous `issues.csv`).

Exit codes: **0** ok, **1** validation failed (nothing written), **2** usage or
I/O error.

`update_index.py` is **UNTESTED**: never executed, stdlib only, local files
only, no network. The expected outputs below were traced by hand from the code,
not captured from a run.

## Rules it enforces

- header exactly `Issue,Page opened,Date checked,Status,What it showed`
- `Issue` is `repo#number` and **unique** -- a duplicate is an error, and the
exit-1 message names every offending line number
- `Page opened` starts with `http://` or `https://`
- `Date checked` is a real calendar date, strict `YYYY-MM-DD`
- `Status` is exactly one of `unverified` / `verified` / `cannot-check`
- `What it showed` is non-empty

Parsing uses the `csv` module, so CRLF files, quoted fields and commas inside
quotes are read correctly. Output `issues.csv` is written with LF endings and
quotes only where needed.

## First test run (nothing outside your machine is touched)

    python3 update_index.py sample_input.csv -o /tmp/idx    # 4 rows ok, 4 ADDED
    python3 update_index.py sample_input.csv -o /tmp/idx    # 4 rows ok, no changes

The first run has no previous `issues.csv`, so every row is ADDED. The second
run diffs against it and finds nothing.

## Worked example: `sample_input.csv`

Input (rows out of order on purpose: 43, 28, 44, 39):

    Issue,Page opened,Date checked,Status,What it showed
    bee-scouts#43,https://github.com/LiamVisionary/bee-scouts/issues/43,2026-10-28,unverified,"Listing states the dataset card spec: single named page per row, five-field row, three Status values."
    bee-scouts#28,https://github.com/LiamVisionary/bee-scouts/issues/28,2026-10-28,unverified,"Listing asks for a dated re-check line for hivemind#173 in issue-index-tool RECHECK-LOG.md. Page body not opened."
    bee-scouts#44,https://github.com/LiamVisionary/bee-scouts/issues/44,2026-10-28,unverified,"Listing refers to an attribution-docs-check fixtures dataset spec and a real run line for issue #33."
    bee-scouts#39,https://github.com/LiamVisionary/bee-scouts/issues/39,2026-10-28,unverified,"Listing says the issues.csv row for hivemind#173 should be corrected to status unverified."

### Expected `/tmp/idx/issues.csv` (after the first run)

    Issue,Page opened,Date checked,Status,What it showed
    bee-scouts#28,https://github.com/LiamVisionary/bee-scouts/issues/28,2026-10-28,unverified,"Listing asks for a dated re-check line for hivemind#173 in issue-index-tool RECHECK-LOG.md. Page body not opened."
    bee-scouts#39,https://github.com/LiamVisionary/bee-scouts/issues/39,2026-10-28,unverified,Listing says the issues.csv row for hivemind#173 should be corrected to status unverified.
    bee-scouts#43,https://github.com/LiamVisionary/bee-scouts/issues/43,2026-10-28,unverified,"Listing states the dataset card spec: single named page per row, five-field row, three Status values."
    bee-scouts#44,https://github.com/LiamVisionary/bee-scouts/issues/44,2026-10-28,unverified,"Listing refers to an attribution-docs-check fixtures dataset spec and a real run line for issue #33."

Note the order 28, 39, 43, 44 -- numeric, not `#43` before `#44` by string --
and that the `#39` row has no commas in its last field, so it is unquoted.

### Expected `/tmp/idx/change_report.txt` (first run)

    issue index change report
    rows: 4 (previous: 0)

    ADDED   bee-scouts#28
    ADDED   bee-scouts#39
    ADDED   bee-scouts#43
    ADDED   bee-scouts#44

### Expected `/tmp/idx/change_report.txt` (immediate re-run)

    issue index change report
    rows: 4 (previous: 4)

    no changes

### Expected failure: a duplicate Issue

Change the `#43` line's Issue to `bee-scouts#28` and run again. Nothing is
written, exit code is 1, stderr says:

    validation failed, nothing written:
      duplicate Issue "bee-scouts#28" on lines 2, 3

(line numbers count the header as line 1, and blank lines still count.)

## Commit message

    Add update_index.py: validate, natural-sort and diff the bee-scouts issue index

    - checks the fixed five-column header (Issue, Page opened, Date checked, Status, What it showed)
    - parses with the csv module, so CRLF and quoted commas work
    - rejects duplicate Issue values, exit 1, naming every offending line
    - enforces Status in unverified / verified / cannot-check
    - requires Date checked to be a real YYYY-MM-DD calendar date
    - writes issues.csv (natural sort by Issue) and change_report.txt (ADDED/REMOVED/CHANGED)
    - UNTESTED: never executed; stdlib only; local files only; no network

## Untested

Everything: no run has happened. Worth checking first -- the duplicate-Issue
message and its line numbers, a CRLF copy of the input, a quoted field
containing a comma, and the second-run "no changes" diff.
