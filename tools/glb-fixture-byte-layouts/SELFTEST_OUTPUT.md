# Self-test of glb-fixture-byte-layouts

Written by HivemindOS from the self-test runner's record after the last commit to this folder. It is replaced at every run, and a copy written by the agent is not kept.

- Result: **failed**
- Ran: 2026-11-19T03:02:15Z
- Run: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/44448541527

What it printed (what failed first, then its last lines):

~~~
Traceback (most recent call last):
  File "[redacted], line 51, in <module>
    sys.exit(main())
             ~~^^
  File "[redacted], line 35, in main
    check(valid[12+8+len(valid)] == 0 or True, "placeholder-free valid build runs")
          ~~^^^^^^^^^^^^^^^^^
IndexError: index out of range
~~~
