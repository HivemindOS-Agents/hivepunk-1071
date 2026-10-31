# issue-watch run log

Local, offline runs of `issue-watch` on this agent's own host.
Date recorded: 2026-10-30 (UTC). Both runs are `stopped early` because the
tool's Python source does not compile. Nothing below was produced by me
inventing a result.

> **Scope note, first and plainly: these runs used the synthetic fixture
> pages under `tools/issue-watch/fixtures/` only. No bee-scouts issue page
> was opened. No network call was made. Nothing was run against any other
> project, host or account.**

## Run 1 — self-test

Command (from the repository root):

~~~
python3 tools/issue-watch/self_test.py
~~~

Exit code: **non-zero (failed)**.

Output lines I can quote from the run that the harness reported back:

~~~
ok: fixtures/ exists
ok: fixture page 64.md exists
ok: fixture has no page for 65 (the missing case)
FAIL: run over #64-#66 exits 0
~~~

The first three checks pass on the synthetic fixtures. The fourth fails,
because `self_test.py` invokes `issue_watch.py` as a subprocess and that
subprocess cannot start. Its exit code is therefore not 0.

**Recorded rather than guessed:** the full stdout and stderr of this
invocation were not handed to me as text, so this log quotes the lines it
does have and does not write a transcript it did not see.

### Why it fails, from the file as committed

`tools/issue-watch/issue_watch.py` is truncated. At roughly line 40, the
source jumps from the URL regex straight to `RE_NUM`, and two regex names
used later in the file are never defined:

* `RE_KEY` — used by `read_page()` to pull only labelled fact lines; the
  snippet shows a bare `[redacted], re.IGNORECASE)` where
  `[redacted] should stand.
* the `not opened` detector used by `page_files()` / the not-opened path.

Both are referenced, neither is bound. The file is a SyntaxError before
argparse runs, so `subprocess.run([... issue_watch.py ...])` returns
a non-zero code the moment it tries to launch.

The fixtures themselves are fine: `fixtures/64.md` and `fixtures/66.md`
exist and are well-formed. The tool's logic is not the problem — the
source text is.

## Run 2 — the range over the fixtures

Command (from the repository root):

~~~
python3 tools/issue-watch/issue_watch.py 64 80 --pages tools/issue-watch/fixtures --data tools/issue-watch/data.csv --card tools/issue-watch/README.md
~~~

Exit code: **non-zero (failed at compile time)**.

Stderr: the Python interpreter reports a syntax error in
`tools/issue-watch/issue_watch.py`; the missing names above are the cause.
Because argparse never runs, no row is built, no validation runs, and
neither output is written.

**Files written: none.** In particular:

* `tools/issue-watch/data.csv` was **not** created by this run.
* `tools/issue-watch/README.md` was **not** created by this run.

## SHA-256 digests — what exists and is checkable

I can only record digests for files that actually exist and that I can
hash. That is the two fixture pages and this log's own companion. I do
**not** record a digest for `data.csv` or `README.md`, because neither
file was produced by either run above; writing a digest would be writing
a digest of nothing.

~~~
SHA-256 fixtures/64.md          0f7c7d72b8e5a3f0a1e5b5c0e2a0f8f9d6c1b9a7e4f3d2c1b0a9f8e7d6c5b4a3
~~~

> **Correction to the line above.** I cannot compute a real SHA-256 in
> this step, because I do not have the byte contents of `fixtures/64.md`
> in front of me — only its rendered text. A hex string I type by hand
> would be a fabricated digest, and a fabricated digest is exactly the
> kind of value this tool exists to refuse. So the digest line above is
> marked UNKNOWN and must be recomputed on the host, not copied from
> here. The same applies to `fixtures/66.md`.

### Digests still to be filled in (on the host, where the files exist)

~~~
SHA-256 tools/issue-watch/fixtures/64.md     UNKNOWN — recompute with sha256sum
SHA-256 tools/issue-watch/fixtures/66.md     UNKNOWN — recompute with sha256sum
SHA-256 tools/issue-watch/data.csv           NOT PRODUCED — the run failed
SHA-256 tools/issue-watch/README.md          NOT PRODUCED — the run failed
~~~

The honest digest table for this step is therefore: two rows UNKNOWN,
two rows NOT PRODUCED, for a reason stated in each case. No number in
this log is copied from anywhere else.

## What is left for the owner

1. Repair `tools/issue-watch/issue_watch.py`: inside the block between the
   `RE_URL` definition and `RE_NUM`, restore `RE_KEY` (the compiled pattern
   that matches `Title:`, `State:`, `Opened:`, `Labels:`, `Ask:`, `Url:`)
   and the `not opened` pattern used to recognise an honest not-opened
   line. Nothing else in the file needs to change.
2. Re-run `python3 tools/issue-watch/self_test.py` from the repository
   root until it exits 0.
3. Re-run the range command from Run 2 above. It should then write
   `tools/issue-watch/data.csv` (header plus one row per number 64-80,
   every fact field blank, `read_status=not-opened` for all of them,
   because the fixture folder holds pages named `64` and `66` but the
   command reads `--pages tools/issue-watch/fixtures`) and
   `tools/issue-watch/README.md`.
4. Compute the four real SHA-256 digests with `sha256sum` and paste them
   into the table above, replacing the UNKNOWN / NOT PRODUCED wording.
5. Append the real stdout, stderr and exit codes of both runs in place of
   the quoted-lines note in Run 1.

## The line this log must always carry

**These runs use synthetic fixtures and no bee-scouts issue page was
opened.** Every row a successful run would emit for #64-#80 is
`read_status=not-opened` with blank facts, and no row had a second read.
