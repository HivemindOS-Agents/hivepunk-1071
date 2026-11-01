# recheck-lint run log

Local, offline runs of `recheck-lint` on this agent's own host. Stdlib only,
local files only, no network. No page was opened and no URL was fetched for any
run below.

> **Scope note, first and plainly:** every run below uses the synthetic fixture
> rows built inside `tools/recheck-lint/self_test.py`. No real `recheck_rows.csv`
> was read. No bee-scouts issue page was opened. Nothing was run against any
> other project, host or account.

## Where the two previously failing tools stand

`tools/update-index` and `tools/provenance-row` are both reported as
`selfTest: failed`. I do not hold their current file contents or the full
failing output in this step, so I have written no change to either -- a fix I
cannot compile or run would be a guess, and recording a guess as a fix is the
one thing this log must not do. `recheck-lint` is written to stand alone of
both.

## Run 1 -- self-test (this tool)

Command (from the tool's own folder):

tools/recheck-lint/self_test.py, run with the Python 3 interpreter that is on the
host, no arguments.

Status: **not yet run on the host.** I wrote the file in this step and cannot
execute code here, so I record the command and the checks it makes; the real
stdout, real stderr and exit code are to be pasted in below on the next host
run. Nothing below is presented as output that was observed.

The self-test runs on four synthetic fixture rows:

| fixture row | shape | what it proves |
|---|---|---|
| `#12` | `Page opened=yes`, real date, `verified` | the clean row goes in the table and stays out of Not opened |
| `#3` | `Page opened=no`, real date, `verified` | a verified status does **not** exempt a row from Not opened |
| `#9` | `Date checked` empty | validation rejects the row and writes no card |
| `#7` | `Page opened` is a snippet note | any value that is not `yes` is listed with a reason |

~~~
$ <python3> tools/recheck-lint/self_test.py; echo $?
PENDING -- to be filled from the host run. Expected checks:
  valid fixture run exits 0
  dataset_card.md was written
  card carries the exact run command line
  card names the column Issue / Date checked / Page opened / Status /
    What it showed / Source URL
  card table holds row #12 / #3 / #7
  card has a Not opened section
  not-opened row #3 is named in that section
  not-opened row #7 is named in that section
  clean opened row #12 is absent from that section
  row #3 carries its reason
  card has a Could not check section
  Could not check states coverage
  Could not check states no page re-read
  Could not check states no licence claim
  dry run exits 0
  dry run writes nothing
  missing date exits 1
  missing date writes no card
  missing date is named in stderr
  absent input exits 2
  all checks passed
~~~

## Files written by a passing run

A passing run writes only the `--card` path (default `dataset_card.md`) and
`--dry-run` writes nothing at all. The self-test writes inside a temporary
directory and removes it. Neither writes any file outside this tool's own
folder tree.

## SHA-256

The self-test's fixture rows are built as string literals inside `self_test.py`,
so the file that must be hashed is `self_test.py` itself. The digest is left
**UNKNOWN** here because I cannot compute it in this step; a hex string typed by
hand would be a fabricated digest.

~~~
SHA-256 tools/recheck-lint/self_test.py    UNKNOWN -- recompute with sha256sum on the host
SHA-256 tools/recheck-lint/publish_recheck_rows.py  UNKNOWN -- recompute with sha256sum on the host
~~~

## What is left for the owner

1. Run the self-test from this tool's folder and paste the real stdout, real
   stderr and exit code into Run 1, replacing the PENDING block.
2. Replace the two UNKNOWN digest rows with real `sha256sum` output.
3. Decide whether `tools/update-index` and `tools/provenance-row` should be
   repaired next; their current file contents are needed to do that.

## The line this log must always carry

**These runs use synthetic fixtures. No real recheck_rows.csv was read and no
page was opened.**
