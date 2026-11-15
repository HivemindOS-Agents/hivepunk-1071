# Self-test of glb-fixture-byte-layouts

Written by HivemindOS from the self-test runner's record after the last commit to this folder. It is replaced at every run, and a copy written by the agent is not kept.

- Result: **failed**
- Ran: 2026-11-15T21:18:52Z
- Run: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/43762965435

What it printed (what failed first, then its last lines):

~~~
FAIL: this folder has at least data/ files plus README.md
Traceback (most recent call last):
    sys.exit(main())
             ~~^^
  File "[redacted], line 53, in main
    check(pm.check_two_entries(mine) is True, "this folder's upload set is valid")
          ~~^^^^^^
  File "[redacted], line 105, in check_two_entries
    raise ValueError("missing source %r" % source)
ValueError: missing source 'data'
~~~
