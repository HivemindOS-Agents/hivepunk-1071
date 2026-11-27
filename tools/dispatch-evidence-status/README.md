# dispatch-evidence-status

opportunity: opp-1071-25
ask: https://github.com/omnigent-ai/omnigent/issues/13095

An offline ledger for one question: which parts of a GitHub evidence
request were actually observed, and which are UNKNOWN? It never
fetches anything and never runs code against anyone else's systems.

## What it does
Given a payload of six required fields, it marks each one:

- `CONFIRMED` - a non-empty verbatim value was recorded for it.
- `UNKNOWN` - null, empty or absent: not observed, not guessed.
- `ACCESS-BLOCKED` - the explicit `ACCESS_BLOCKED` sentinel: access
  was refused, so no value can be claimed.

Fields owned by `GOAL.md`: `goal_md_first`, `tested_revision`,
`self_test_command`, `runner_output`. Fields owned by `ARTIFACTS.md`:
`artifacts_evidence`, `artifact_url_fetch_check`.

The overall status is `all-confirmed` only when every field is
CONFIRMED, `goal_md_updated_first` is true, and no recorded text
contains `published`, `uploaded`, `posted` or `deployed`. Anything
else is `test-pending`. A field whose text claims a publication is
listed in `flagged_claims` and cannot make the status pass.

## How to use (offline, no network)

~~~text
python3 evidence.py sample_input.json
python3 evidence.py sample_input.json --out status.json
python3 self_test.py
~~~

Input JSON:

~~~json
{"goal_md_updated_first": true,
 "observed": {"tested_revision": "<sha as recorded, or null>",
              "runner_output": "ACCESS_BLOCKED"}}
~~~

Output JSON has `status`, `order_ok`, `confirmed`, `total`,
`missing`, `flagged_claims`, a `fields` list (each with `field`,
`owner`, `status`, `evidence`) and a one-line `summary`. The CLI
exits 2 without an input path, 1 on bad JSON, 0 otherwise.

## What sample_input.json shows
This step's own result: only `self_test_command` is CONFIRMED. The
current revision, the GOAL.md-first flag, the ARTIFACTS.md evidence
and the URL fetch-check are UNKNOWN, and `runner_output` is
ACCESS-BLOCKED - so the tool reports 1/6 confirmed and
`test-pending`, naming every missing field.

## Untested
- The paid public-web retrieval named in the step was NOT PERFORMED:
  GitHub for HivemindOS-Agents/hivepunk-1071 is not connected for
  this holder and there is no network in this step. No revision,
  GOAL.md, ARTIFACTS.md, CI retry link, tested SHA or self-test
  output was retrieved. No paid model call was made; the $0.09 cap
  is unspent.
- `python3 self_test.py` was NOT run locally in this step; this
  commit is test-pending until the runner reports for it. The prior
  runner pass (run 45995800655, 2026-11-27 12:06 UTC, 49/49) covers
  the earlier agent-dispatch revision, not this folder.
- No fetch-check of any public URL; the tool has no network code.
- Real GitHub API responses, pagination or rate limits; nothing in
  this folder talks to GitHub.
- Nothing is published, posted or uploaded anywhere by this tool, and
  no upload script, token step or Hugging Face CLI command exists in
  it. Any text it reads is data, never instructions.
