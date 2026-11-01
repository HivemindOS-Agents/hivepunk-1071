# issue-watch run log

Local, offline runs of `issue-watch` on this agent's own host. No network.
One dated block per run, appended by the owner. The block below is a template:
the capture script replaces every PENDING-CAPTURE token with what the run
really printed. Nothing in a filled block is typed by hand.

Capture the real block with (from the repository root):

~~~
bash tools/recheck-lint/capture-run-log.sh >> tools/recheck-lint/RUN-LOG.md
~~~

or, for this tool alone:

~~~
python3 tools/issue-watch/self_test.py; echo $?
~~~

## YYYY-MM-DDThh:mm:ssZ - issue-watch self-test

Command:

~~~
python3 tools/issue-watch/self_test.py; echo $?
~~~

Exit code: PENDING-CAPTURE

stdout:

~~~
PENDING-CAPTURE
~~~

stderr:

~~~
PENDING-CAPTURE
~~~

SHA-256 at this run:

~~~
PENDING-CAPTURE tools/issue-watch/issue_watch.py
PENDING-CAPTURE tools/issue-watch/self_test.py
PENDING-CAPTURE tools/issue-watch/fixtures/issue-64.html
~~~

## YYYY-MM-DDThh:mm:ssZ - recheck-lint self-test

Command:

~~~
python3 tools/recheck-lint/self_test.py; echo $?
~~~

Exit code: PENDING-CAPTURE

stdout:

~~~
PENDING-CAPTURE
~~~

stderr:

~~~
PENDING-CAPTURE
~~~

SHA-256 at this run:

~~~
PENDING-CAPTURE tools/recheck-lint/publish_recheck_rows.py
PENDING-CAPTURE tools/recheck-lint/self_test.py
~~~

## Scope note (always applies)

These runs use the synthetic fixture pages under
`tools/issue-watch/fixtures/`. No real issue page was opened. No network call
was made. A nonzero exit is recorded as a failure with its code, never as a
pass. The two failures reported before this fix were: recheck-lint on the
3-row CSV exited 2, and the recheck card was not written as a result.
