# Self-test of bee-scouts-recheck

Written by HivemindOS from the self-test runner's record after the last commit to this folder. It is replaced at every run, and a copy written by the agent is not kept.

- Result: **failed**
- Ran: 2026-11-04T09:10:20Z
- Run: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/41805218443

What it printed (what failed first, then its last lines):

~~~
ok: shipped package passes (got 0)
    package ok: card complete, no licence claimed, data.csv header only, no row filled from a snippet
ok: synthetic good package passes (got 0)
ok: card claiming a licence is rejected
ok: licence rejection exits 2 (got 2)
ok: reordered header is rejected
ok: non-read row carrying a finding is rejected
ok: unread row with blank facts is allowed (got 0)
~~~
