# Self-test of card-claims-fetch

Written by HivemindOS from the self-test runner's record after the last commit to this folder. It is replaced at every run, and a copy written by the agent is not kept.

- Result: **failed**
- Ran: 2026-11-06T09:14:34Z
- Run: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/42193511036

What it printed (what failed first, then its last lines):

~~~
FAIL [publisher               ] expected: 'example-org'   got: 'huggingface.co'
FAIL [states_context_window   ] expected: '32768'         got: ''
FAIL [publisher               ] expected: 'example-org'   got: 'huggingface.co'
FAIL [publisher               ] expected: 'example-org'   got: 'huggingface.co'
Traceback (most recent call last):
  File "[redacted], line 133, in <module>
    check("empty body", "", fetch_cards.stated_context_window(""))
                            ~~^^^^
  File "[redacted], line 122, in stated_context_window
    val = meta.get("context_length") or meta.get("context_window")
          ^^^^^^^^
AttributeError: 'str' object has no attribute 'get'
~~~
