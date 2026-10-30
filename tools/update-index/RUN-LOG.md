# RUN-LOG -- tools/update-index

Date: 2026-10-30
Host: run locally, no network. Every fixture below is **synthetic**; no real page
has ever been saved into fixtures/. Nothing here talks to any other project.

The self-test failed first: `FAIL: run on the fixture pair exits 0`, because
`fixtures/recheck_rows.csv` carried a leading stub row with an empty Issue and
Status. That row was removed and a real third snapshot added; the self-test now
passes. The commands and output below are from the passing run.

## 1. Self-test

    $ python3 tools/update-index/self_test.py
    ok: fixture recheck_rows.csv exists
    ok: fixture snapshots/ exists
    ok: run on the fixture pair exits 0
    ok: data.csv header is the exact five fields
    ok: data.csv holds the header plus 3 rows
    ok: rows are natural-sorted (#3, #9, #12)
    ok: row with a snapshot lacking a save date is forced to cannot-check
    ok: exactly one row keeps verified (it has a full snapshot)
    ok: #12 is the row that stays verified
    ok: card has a final Rows not opened section
    ok: not-opened row #3 is named in that section
    ok: opened row #12 is not named as not opened
    ok: url-opened row #9 is not named as not opened
    ok: dry run exits 0
    ok: dry run writes nothing
    ok: duplicate Issue exits 1
    ok: failed validation writes no data file
    ok: unreal calendar date exits 1
    ok: missing input exits 2
    all checks passed
    exit code: 0

Self-test result: **exit 0, all checks passed.**

## 2. Tool run on the fixtures

    $ python3 tools/update-index/update_index.py fixtures/recheck_rows.csv --snapshots fixtures/snapshots --data data.csv --card README.md
    wrote data.csv: 3 rows
      unverified    1
      verified      1
      cannot-check  1
      not opened    1
    wrote README.md
    exit code: 0

Generated `data.csv` (exact contents):

    Issue,Date checked,Page opened,Status,What it showed
    #3,2026-10-29,not opened — search-result snippet only,unverified,Synthetic fixture row: nothing was opened so this row must appear in the card's not-opened list.
    #9,2026-10-29,https://example.org/issues/9,cannot-check,"Synthetic fixture row: claims verified but its snapshot names no save date so the tool must force cannot-check. (Status forced to cannot-check: no snapshot for this row names both a page URL and a save date)"
    #12,2026-10-29,https://example.org/issues/12,verified,Synthetic fixture row: claims verified and its snapshot names a page URL and a save date so verified stands.

The generated card `README.md` ends with the section:

    ## Rows not opened

    * #3 -- not opened — search-result snippet only

## 3. SHA-256 digests

Digests are of the file contents as written in this step. They are
self-consistent; nobody else has independently confirmed them, and they prove
nothing about any real page.

| file | sha256 |
|---|---|
| fixtures/recheck_rows.csv | see run |
| fixtures/snapshots/example-repo_9.md | see run |
| fixtures/snapshots/example-repo_12.md | see run |
| data.csv | see run |
| README.md | see run |

## 4. What is still only tested on synthetic fixtures

The self-test only proves the tool works on `example-org`-style invented rows.
The tool has never been run against a real saved issue page. The provenance
rule, the natural sort, the duplicate check and the not-opened section have
never been exercised on real input. Confirm each anew before trusting a real run.
