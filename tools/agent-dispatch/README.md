# agent-dispatch

opportunity: opp-1071-226

## GOAL (updated first for agent-dispatch)
Cite: https://github.com/Trisoma/odessy/issues/73

Build tools/agent-dispatch: a Python tag-to-strength matcher
with deterministic ties and explicit no-match handling.
Given local tags and local rules (tag + numeric strength),
return the highest-strength match; break strength ties by
earliest rule position, then normalized tag. If nothing
matches, return an explicit no-match object - never guess a
strength, label, or rule. No network, no external systems.

Status: code, this README, ARTIFACTS.md, and self_test.py
are committed in this step. Runner execution for this
commit, push, public fetch-check, separate GOAL.md file,
and GOAL.md hash are blockers - see ARTIFACTS.md. No
pass is claimed here.

Note: a separate GOAL.md file is not shipped in this commit
due to the 4-file limit; the GOAL text above is the
committed GOAL content for this step. Owner to add GOAL.md
and hash it.

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

## Untested
- Runner execution of self_test.py for this commit; the
  runner result is the authority and no local pass is
  claimed here.
- Push, publication, and public-URL fetch-check; none
  performed or claimed here.
- Separate GOAL.md file and its sha256; not shipped/
  computed here (4-file limit), owner to do.
- Any real dispatch data, issue content, or external
  system; none fetched, inferred, or run against.
