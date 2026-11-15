# Self-test of glb-fixture-byte-layouts

Written by HivemindOS from the self-test runner's record after the last commit to this folder. It is replaced at every run, and a copy written by the agent is not kept.

- Result: **failed**
- Ran: 2026-11-15T22:23:16Z
- Run: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/43768990561

What it printed (what failed first, then its last lines):

~~~
FAIL: this folder has at least data/ files plus README.md
FAIL: a changed byte changes the byte count
FAIL: manifest does not list the test file
ok: absolute path is refused
ok: an added file appears as an extra entry
ok: an extra data/ file is still an upload-set path
ok: a file outside the two sources is not uploaded
ok: an empty folder fails the upload-set check
ok: a folder with no README.md fails the upload-set check
Results: 20/23 checks passed
~~~
