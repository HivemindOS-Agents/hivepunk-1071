# issue-watch run log

Local, offline runs of `issue-watch` on this agent's own host. No network.
One dated block per run, written only from a real capture. Nothing in a block is
typed from memory: the output lines come from the capture itself, and a nonzero
exit code is recorded as a failure with its code, never as a pass. The checksum
lines are filled only when a capture includes `sha256sum` output.

Capture a block with (from the repository root):

~~~
python3 tools/issue-watch/self_test.py; echo $?
~~~

## 2026-11-06T05:13Z - issue-watch self-test

Run time: 2026-11-06T05:13Z, taken from this step's own record of the run
(epoch 1793942005939 ms). The runner's result reached this file without a
separate timestamp, so this header is the one field here that is derived
rather than copied from the runner's output.

Command (run from the repository root):

~~~
python3 tools/issue-watch/self_test.py; echo $?
~~~

Run link: not supplied with the runner's result for this step. HivemindOS
writes each run's own result into `SELFTEST_OUTPUT.md` beside this file.

Exit code: 0

Runner output, copied unedited. The runner keeps the last lines only, so the
earlier `ok:` checks of this run were already cut off before it reached this
file and are not reproduced below:

~~~
ok: tool exits 0 on a page with no source URL (got 0)
ok: a row for the no-source-URL page 99
ok: 99: page_opened is no
ok: 99: date left blank
ok: 99: reason says Not opened
ok: tool exits 0 on an instruction-looking page (got 0)
ok: a row for the instruction page 98
ok: 98: the line is kept as text, unchanged
~~~

Checksums: Not captured: the self-test runner does not record checksums.

## Scope note (always applies)

This is the only block in this file. It comes from the self-test runner's own
result, not from a run performed here, and the runner keeps the last lines only
-- so the block above is a tail, not the full transcript. A future run gets its
own block here only when that run's output is copied in from a capture.

The run uses the synthetic fixture page under `tools/issue-watch/fixtures/`.
No real issue page was opened. No network call was made. The two bugs an
earlier repair addressed were path bugs: the self-test looked for the fixture
page, and for a sibling script that no longer exists, relative to the current
working directory, so from the repository root it missed them. All paths are
now built from `__file__`. The block above carries exit code 0, so nothing in
this folder is left marked as unrun by this file.
