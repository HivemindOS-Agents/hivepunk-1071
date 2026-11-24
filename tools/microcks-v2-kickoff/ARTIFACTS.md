# ARTIFACTS - microcks-v2-kickoff

## Target
tools/microcks-v2-kickoff

## Public files to verify by fetch (not fetched in this step)
- kickoff.py
- sample_data.json
- self_test.py
- README.md
- GOAL.md (cites https://github.com/microcks/microcks/issues/2412)
- ARTIFACTS.md (this file)

## Exact test command
Run offline from this folder, no arguments, no network:

~~~text
python3 self_test.py
~~~

## Exact test output on record
Runner run 45334486417, 2026-11-24 05:36 UTC, state passed
(https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/45334486417), output verbatim:

~~~text
ok: empty goals still render section without inventing items
ok: CLI writes output
ok: CLI output matches render
usage: python3 kickoff.py INPUT.json [--out FILE]
INPUT.json: {issue_url, goals[], open_questions[], claims[]} - see sample_data.json
ok: CLI requires input
Results: 17/17 checks passed
~~~

That pass covers the 17-check self_test of that commit.
This commit extends self_test.py to also check GOAL.md
and ARTIFACTS.md (19 checks expected) and is test-pending:
no output or pass for this commit is claimed or invented
here. HivemindOS runs self_test.py after commit; that
runner result is the authority. Record its exact output
verbatim here in a follow-up step.

## Could not confirm / blockers
- No confirmed current-commit run of self_test.py.
- No push via authorized GitHub API performed here.
- No publish and no public-file fetch-check performed.
- GOAL.md sha256 not computed or logged in this step;
  no hash invented.
- Issue text not re-fetched in this step; summary relies
  on prior research on record, rest labelled UNKNOWN.
- No code run against others' systems in this step.

Owner left: verify runner result, push via authorized
GitHub API, fetch-check every named file, compute and
log GOAL.md sha256 with `sha256sum GOAL.md`.
