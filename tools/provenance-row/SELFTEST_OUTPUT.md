# Self-test of provenance-row

Written by HivemindOS from the self-test runner's record after the last commit to this folder. It is replaced at every run, and a copy written by the agent is not kept.

- Result: **failed**
- Ran: 2026-11-08T00:44:30Z
- Run: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/42431113404

What it printed (what failed first, then its last lines):

~~~
Traceback (most recent call last):
  File "[redacted], line 37, in <module>
    main()
    ~~^^
  File "[redacted], line 27, in main
    row = pr.build_row(snapshot_text, URL, DATE_CHECKED)
TypeError: build_row() takes 2 positional arguments but 3 were given
~~~
