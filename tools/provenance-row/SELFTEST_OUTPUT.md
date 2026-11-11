# Self-test of provenance-row

Written by HivemindOS from the self-test runner's record after the last commit to this folder. It is replaced at every run, and a copy written by the agent is not kept.

- Result: **failed**
- Ran: 2026-11-11T04:12:17Z
- Run: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/42957666686

What it printed (what failed first, then its last lines):

~~~
Traceback (most recent call last):
work/bee-self-test/bee-self-test/work/tools/provenance-row/provenance_row.py", line 160, in build_row
    text = read_snapshot(path)
  File "[redacted], line 84, in read_snapshot
    with open(path, "r", encoding="utf-8-sig", errors="replace") as handle:
         ~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
FileNotFoundError: [Errno 2] No such file or directory: "# SYNTHETIC FIXTURE -- invented text, not a real page or a real read\n\nUrl: https://github.com/example-org/example-repo/issues/58\nSaved: 2026
~~~
