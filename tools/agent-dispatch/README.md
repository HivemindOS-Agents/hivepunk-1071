# agent-dispatch

opportunity: opp-1071-226

## GOAL
See GOAL.md in this folder. Cite:
https://github.com/Trisoma/odessy/issues/73

Status for this commit: test-pending. The prior commit's
runner pass (run 45225896912, 2026-11-23 17:16 UTC, 16/16
checks passed) does not verify this commit. See ARTIFACTS.md.
A separate GOAL.md file is now shipped in this folder.

Build tools/agent-dispatch: a Python tag-to-strength matcher
with deterministic ties and explicit no-match handling.
Given local tags and local rules (tag + numeric strength),
return the highest-strength match; break strength ties by
earliest rule position, then normalized tag. If nothing
matches, return an explicit no-match object - never guess a
strength, label, or rule. No network, no external systems.

## Use (offline)

~~~text
python3 dispatch.py input.json --out result.json
python3 dispatch.py input.json
python3 self_test.py
~~~

Input JSON:

~~~json
{"tags": ["Python", "go"],
 "rules": [{"tag": "python", "strength": 5, "label": "high"},
           {"tag": "go", "strength": 5, "label": "go-high"}]}
~~~

Output JSON has `matched`, `strength`, `tag`, `label`,
`rule_index`, `reason` (`matched` or `no-match`),
`normalized_tags`, and sorted `candidates`. With no match,
`matched` is false and `strength`/`tag`/`label`/`rule_index`
are null.

## Rules
- Tags and rule tags are normalized: stripped, lowercased,
  internal whitespace collapsed. Duplicates deduplicated.
- Strength must be an int/float; booleans and strings are
  rejected with an error, not coerced.
- Winner: highest strength, then earliest rule, then tag.
  Result is independent of tag order.

## ARTIFACTS
See ARTIFACTS.md in this folder for the target, named
public files, exact test command, prior runner output
(run 45225896912, 2026-11-23 17:16 UTC, 16/16), and the
exact blocker. No output or pass for this commit is claimed
here.

## Self-test output note
self_test.py prints "GOAL.md sha256: <value>" as the last
line before its summary, so the runner output carries the
true hash of the committed GOAL.md. Copy that line into the
daily log; no hash is typed into any file by hand.

## Untested
- Runner/local execution of self_test.py for this commit;
  no pass is claimed here.
- Push, publication, and public-URL fetch-check; none
  performed or claimed here.
- A GOAL.md sha256 stored in a file; the value is printed
  by the self-test at run time for the owner to log.
- Any real dispatch data, issue content beyond the citation,
  or external system; none fetched, inferred, or run against.
