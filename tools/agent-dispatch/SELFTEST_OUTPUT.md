# Self-test of agent-dispatch

Written by HivemindOS from the self-test runner's record after the last commit to this folder. It is replaced at every run, and a copy written by the agent is not kept.

- Result: **failed**
- Ran: 2026-11-26T01:27:41Z
- Run: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/45735857085
- Tested commit: 5f9b29077e7d5fd04d6c8c2f200b026f190aa0b7
- Verified by: none
- Check from: none

What it printed (what failed first, then its last lines):

~~~
FAIL: no live dataset URL claimed while NOT UPLOADED
usage: python3 dispatch.py INPUT.json [--out FILE]
INPUT.json: {"tags": ["..."], "rules": [{"tag": "...", "strength": 1, "label": "..."}]}
ok: CLI requires input
ok: GOAL.md sha256 is 64 lowercase hex chars
ok: GOAL.md sha256 is deterministic across reads
GOAL.md sha256: 33d900cb2239258fed53b4f2b346e2cae9c5c27b9a5a32e3739061527510512c
Results: 39/40 checks passed
~~~
