# Self-test of glb-structure-check

Written by HivemindOS from the self-test runner's record after the last commit to this folder. It is replaced at every run, and a copy written by the agent is not kept.

- Result: **failed**
- Ran: 2026-11-10T13:30:54Z
- Run: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/42825164870

What it printed (what failed first, then its last lines):

~~~
FAIL: sample file not found: [redacted]
FAIL: Expected 4 passes, got 0
FAIL: valid_minimal.glb returned exit code -1, expected 0
Testing bad_magic.glb...
FAIL: sample file not found: [redacted]
FAIL: bad_magic.glb should report magic failure
FAIL: bad_magic.glb returned exit code -1, expected 1
Some self-tests failed.
exit=1
~~~
