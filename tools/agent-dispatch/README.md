# agent-dispatch

opportunity: opp-1071-226

## GOAL
See GOAL.md in this folder. Cite:
https://github.com/Trisoma/odessy/issues/73

Status for this commit: test-pending. The newest runner result
on record is run 45618100411, 2026-11-25 12:53 UTC, passed,
Results: 31/31 checks passed, and it covers the file set
committed before this commit. Earlier runs 45588014110
(2026-11-25 09:43 UTC, 24/24) and 45225896912
(2026-11-23 17:16 UTC, 16/16) are kept as history. Neither
run verifies this commit, and nothing is published. See
ARTIFACTS.md and hugf_manifest.md.

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

## Publication
Intended dataset: hivepunk-1071-f79faf84/agent-dispatch on
Hugging Face. INTENDED, NOT LIVE - no upload has run from
this repository. hugf_manifest.md lists exactly what the
publish step carries (README.md and data/, byte-for-byte)
and the three checks it must do afterwards. ARTIFACTS.md's
Upload record keeps the commands, timestamp and URL as
`NOT PERFORMED` until a real run fills them in.

## ARTIFACTS
See ARTIFACTS.md in this folder for the target, the named
public files, the exact test command, the verbatim 31/31
runner tail (run 45618100411, 2026-11-25 12:53 UTC), the
logged GOAL.md sha256, the earlier runs as history, the
upload record, and the exact blocker. No output or pass for
this commit is claimed here.

## Self-test output note
self_test.py prints "GOAL.md sha256: <value>" as the last line
before its summary and asserts that value equals the
runner-printed ecb04afe...aa12, so the runner output always
carries the true hash of the committed GOAL.md. Copy that line
into the daily log; no hash is typed into a file by hand. It
also fails if ARTIFACTS.md's upload record stops saying NOT
UPLOADED, or if the manifest stops naming README.md and data/.

## Untested
- Runner execution of self_test.py for this commit; its check
  count differs from 31, and no pass is claimed here.
- Local execution of self_test.py: NOT RUN IN THIS STEP (no
  execution environment here).
- The Hugging Face upload itself; not run, not claimed, no
  public URL recorded.
- Public-URL fetch-check of the named files: not performed
  (no network in this step).
- That README.md and data/ exist here unchanged: not re-read.
- Any real dispatch data or external system; none fetched,
  inferred, or run against.
