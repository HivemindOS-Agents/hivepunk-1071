# Self-test of card-claims-fetch

Written by HivemindOS from the self-test runner's record after the last commit to this folder. It is replaced at every run, and a copy written by the agent is not kept.

- Result: **failed**
- Ran: 2026-11-06T02:19:12Z
- Run: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/42149532037

What it printed (what failed first, then its last lines):

~~~
   ] expected: 'apache-2.0'    got: ''
PASS  [publisher               ] expected: 'example-org'   got: 'example-org'
PASS  [model_name              ] expected: 'Sparse Sample Model' got: 'Sparse Sample Model'
PASS  [date_read               ] expected: '2026-11-06'    got: '2026-11-06'
PASS  [states_context_window   ] expected: ''              got: ''
PASS  [states_license          ] expected: ''              got: ''
PASS  [source                  ] expected: 'https://huggingface.co/example-org/sparse-sample-model' got: 'https://huggingface.co/example-org/sparse-sample-model'
Test summary: FAIL
~~~
