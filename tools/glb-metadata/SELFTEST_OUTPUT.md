# Self-test of glb-metadata

Written by HivemindOS from the self-test runner's record after the last commit to this folder. It is replaced at every run, and a copy written by the agent is not kept.

- Result: **passed**
- Ran: 2026-11-13T09:04:01Z
- Run: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/43398181419

What it printed (what failed first, then its last lines):

~~~
ok: bad magic: fixture is 12 bytes
ok: bad magic: tool reports wrong magic
ok: bad magic: check_glb returns False
ok: length mismatch: fixture still writes 24 bytes
ok: length mismatch: tool reports the mismatch
ok: length mismatch: check_glb returns False
Results: 13/13 checks passed
~~~
