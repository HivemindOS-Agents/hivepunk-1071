# Self-test of glb-metadata

Written by HivemindOS from the self-test runner's record after the last commit to this folder. It is replaced at every run, and a copy written by the agent is not kept.

- Result: **failed**
- Ran: 2026-11-13T06:04:08Z
- Run: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/43376086609

What it printed (what failed first, then its last lines):

~~~
Traceback (most recent call last):
  File "[redacted], line 121, in <module>
    sys.exit(main())
             ~~^^
  File "[redacted], line 90, in main
    assert len(valid_bytes) == valid_length, "fixture size mismatch"
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: fixture size mismatch
~~~
