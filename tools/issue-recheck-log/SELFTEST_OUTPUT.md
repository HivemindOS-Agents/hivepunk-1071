# Self-test of issue-recheck-log

Written by HivemindOS from the self-test runner's record after the last commit to this folder. It is replaced at every run, and a copy written by the agent is not kept.

- Result: **failed**
- Ran: 2026-11-02T14:49:29Z
- Run: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/41465532171

What it printed (what failed first, then its last lines):

~~~
ok: README.md card found
ok: rows.csv found
FAIL: shipped card + rows.csv pass validation
  problem: rows: required section 'Could not check' is absent (it must stay, even when empty)
FAIL: an unopened row with a filled read_status is rejected
FAIL: snapshot fields on an unopened row are rejected
ok: a card that declares a licence is rejected
~~~
