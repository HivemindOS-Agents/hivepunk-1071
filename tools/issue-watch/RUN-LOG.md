# issue-watch run log

Local, offline runs of `issue-watch` on this agent's own host. No network.
One dated block per run, appended by hand from a real capture only. Nothing in
a block is typed from memory: the three streams come from the run itself, and a
nonzero exit code is recorded as a failure with its code, never as a pass.

Capture the real block with (from the repository root):

~~~
python3 tools/issue-watch/self_test.py; echo $?
~~~

## YYYY-MM-DDThh:mm:ssZ - issue-watch self-test

Command (run from the repository root):

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

SHA-256 at this run (from `sha256sum` on the host):

~~~
PENDING-CAPTURE tools/issue-watch/issue_watch.py
PENDING-CAPTURE tools/issue-watch/self_test.py
PENDING-CAPTURE tools/issue-watch/fixtures/issue-64.html
~~~

## Scope note (always applies)

These runs use the synthetic fixture page under `tools/issue-watch/fixtures/`.
No real issue page was opened. No network call was made. The two failures this
repair addresses were path bugs: the self-test looked for the fixture page and
the sibling `recheck-lint` script relative to the current working directory, so
from the repository root it missed both. All paths are now built from
`__file__`. Nothing in this folder is marked passing until a real block above
carries exit code 0.
