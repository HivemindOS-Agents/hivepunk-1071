# Self-test of card-claims-fetch

Written by HivemindOS from the self-test runner's record after the last commit to this folder. It is replaced at every run, and a copy written by the agent is not kept.

- Result: **passed**
- Ran: 2026-11-06T12:35:12Z
- Run: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/42218746215

What it printed (what failed first, then its last lines):

~~~
ource' got: 'card_url,publisher,model_name,date_read,states_context_window,stat
PASS [write_csv header        ] expected: 'card_url,publisher,model_name,date_read,states_context_window,states_license,source' got: 'card_url,publisher,model_name,date_read,states_context_window,stat
PASS [write_csv rows          ] expected: 3               got: 3
PASS [write_csv no CR         ] expected: False           got: False
PASS [round-trip cell         ] expected: 'apache-2.0'    got: 'apache-2.0'
PASS [round-trip cell 2       ] expected: 'Sparse Sample Model' got: 'Sparse Sample Model'
Test summary: PASS
~~~
