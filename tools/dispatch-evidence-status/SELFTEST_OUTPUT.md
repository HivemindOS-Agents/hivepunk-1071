# Self-test of dispatch-evidence-status

Written by HivemindOS from the self-test runner's record after the last commit to this folder. It is replaced at every run, and a copy written by the agent is not kept.

- Result: **passed**
- Ran: 2026-11-27T20:31:47Z
- Run: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/46064215889
- Tested commit: 3e17ca87787dc98c5fc9f8f2373b2da5a691d05d
- Verified by: runner
- Check from: same-change

What it printed (what failed first, then its last lines):

~~~
usage: python3 evidence.py INPUT.json [--out FILE]
INPUT.json: {goal_md_updated_first, observed{field: text|ACCESS_BLOCKED|null}}
fields: goal_md_first, tested_revision, self_test_command, runner_output, artifacts_evidence, artifact_url_fetch_check
ok: CLI requires input
error: Expecting property name enclosed in double quotes: line 1 column 2 (char 1)
ok: CLI rejects bad JSON
Results: 22/22 checks passed
~~~
