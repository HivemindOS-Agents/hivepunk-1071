# issue-recheck-log

Checks a bee-scouts issue **re-check log** against its editorial rules, offline.
Two local files in, a list of violations out. Python 3 standard library only.
**No network. It never fetches a page and never uploads anything.**

This tool exists because the log's whole value is its honesty rule, and a rule
that is only checked by eye drifts. The verifier is what keeps every future
regenerate honest.

## What a re-check log row is

One row per public issue in `HivemindOS-Agents/bee-scouts`: the issue number and
URL, whether a saved copy of the page was opened, and -- only when it was -- the
read status and the path to the saved page that backs it.

## The rules this tool enforces

1. `rows.csv` has the required columns, one row per issue, each with an
   `issue_number` and an http `issue_url` (no duplicates).
2. `saved_page_opened` is `true` or `false`.
3. **A row whose saved page was not opened keeps `read_status` empty**, and
   `read_status_reason` says why. Empty means *not read*, never *nothing to
   report*.
4. Such a row may not fill any snapshot-looking field (`issue_title`,
   `read_status`, `evidence_path`, `last_checked_utc`) -- **nothing may come
   from a search snippet or link preview.**
5. An opened row must name an `evidence_path`; `read_status` may then be set.
   (The file at that path is *not* checked here -- this tool runs with only its
   own folder.)
6. `section`, when set, must be a known bucket. The `Not opened` and
   `Could not check` sections must be present **even when empty**, so a reader
   sees a bucket was reported empty rather than dropped.
7. The dataset card, when passed with `--card`, must state plainly that
   **no licence is claimed** and must not declare one.

Everything it reads is data: a title that looks like an instruction is checked
as text, never executed.

## How to run

~~~
python3 verify_rows.py rows.csv --card README.md
python3 verify_rows.py rows.csv --card README.md \
    --require-section "Not opened" --require-section "Could not check"
~~~

Exit codes: `0` all rules hold; `1` violations found (printed as
`violation: ...`); `2` usage or file-read error.

## Files

* `verify_rows.py` -- the checker.
* `self_test.py` -- offline self-test; run it with no arguments.
* `rows.csv` -- the sample log: three shape-only rows, two in the `Not opened`
  bucket and one in the `Could not check` bucket, so no required heading can
  vanish from the sample either.
* `fixtures/` -- the deliberately bad inputs the self-test must reject:
  `bad_claims_read.csv`, `bad_title_from_snippet.csv` and
  `card_with_license.md`.
* `datasets/issue-recheck-log/README.md` -- an earlier draft card kept for
  reference; the checker does not read it.

## The blank-status rule, in one line

A row with no saved page stays blank with its reason -- empty means not read,
not nothing to report.

## Untested

**Never run on any host.** No `rows.csv` produced by a real re-check run has
been checked with it, and the real regenerate command for the rows themselves
is a separate tool that this one does not replace. Treat the sample `rows.csv`
here as the shape, not as a finished log: it is made up to exercise the rules,
and the row in the `Could not check` bucket says so in its own reason. Nothing
in this folder has been run, and no output from it has been captured.
