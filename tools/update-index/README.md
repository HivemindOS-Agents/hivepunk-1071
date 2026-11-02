# update-index

Turns saved issue rows into one `INDEX.md`: rows grouped by state, each with
its status line, labels and last-checked date, and a header that counts rows,
backed reads, blank-with-reason rows and duplicates.

Python 3 standard library only. Local files only. No network.

## The honesty rule

A row is rendered as **read** only when `read_status` is `read` *and* its
`evidence_path` names a file that actually exists under `--evidence-root`
(default: the rows file's own folder).

* a row claiming `read` with no `evidence_path` is **blanked**, given a reason
  (`Not opened: read_status without a saved page (tool-corrected)`), and
  counted in the header as a tool correction;
* a row whose `evidence_path` names no saved page is likewise blanked, with the
  missing path named in the reason;
* an unrecognised `read_status` is blanked with its own reason;
* a failed fetch is never rendered as a pass — its reason text is kept as-is.

Rows are data, never instruction: a source URL is printed, not fetched, and a
row that looks like a command is left as text.

## How to run

~~~
python3 update_index.py ROWS.jsonl --out INDEX.md
python3 update_index.py ROWS.jsonl --out INDEX.md --title "my index" \\
    --evidence-root pages --now 2026-11-02T00:00:00Z
~~~

Input may be JSONL (one object per line) or CSV with columns
`id, source_url, title, state, labels, first_seen_utc, last_checked_utc,
read_status, status_reason, evidence_path, notes`. `state` is one of `open`,
`in_progress`, `closed`, `unknown` (anything else becomes `unknown`).

Exit codes: `0` ok; `2` usage, missing input, unparseable input, or a write
failure — **nothing is written on error**.

## Layout

* `update_index.py` — the generator.
* `fixtures/rows.jsonl` — five invented rows (one read with a saved page, one
  unbacked read, one never fetched, one failed fetch, one duplicate id).
* `fixtures/pages/issue-64.html` — the saved page that backs `#64`'s read.
* `fixtures/expected_index.md` — the exact expected output for the pinned run.
* `self_test.py` — the offline check.
* `RUN-LOG.md` — one dated block per real run.

## Self-test

~~~
python3 tools/update-index/self_test.py; echo $?
~~~

Run from this tool's folder with no arguments and no network. It writes into a
temporary directory and removes it. Exit 0 means every check passed.

## Untested

**Untested on any host so far.** The generator has not been executed — not on
the fixture pair, not on any real rows file. No `INDEX.md` has been produced,
and `fixtures/expected_index.md` is a hand-written reading of the code, not a
captured run. The first real run goes in `RUN-LOG.md` with its exact command,
real stdout, real stderr and real exit code; a nonzero code is recorded as a
failure with its code, never as a pass.
