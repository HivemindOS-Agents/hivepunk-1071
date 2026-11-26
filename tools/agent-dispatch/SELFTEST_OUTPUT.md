# Self-test of agent-dispatch

Written by HivemindOS from the self-test runner's record after the last commit to this folder. It is replaced at every run, and a copy written by the agent is not kept.

- Result: **failed**
- Ran: 2026-11-26T01:59:12Z
- Run: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/45739321484
- Tested commit: 560804fcb515c8cf379cd41e86369c8db210b359
- Verified by: none
- Check from: none

What it printed (what failed first, then its last lines):

~~~
FAIL: GOAL.md names the verified data file
usage: python3 dispatch.py INPUT.json [--out FILE]
INPUT.json: {"tags": ["..."], "rules": [{"tag": "...", "strength": 1, "label": "..."}]}
ok: CLI requires input
ok: GOAL.md sha256 is 64 lowercase hex chars
ok: GOAL.md sha256 is deterministic across reads
GOAL.md sha256: c9254d7fc58f481ad523022d71846f2645bfce9072877664a0e296cc3c4d2dce
Results: 39/40 checks passed
~~~
