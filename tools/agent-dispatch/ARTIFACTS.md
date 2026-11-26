# ARTIFACTS - agent-dispatch

## Target
tools/agent-dispatch
Public folder: https://github.com/HivemindOS-Agents/hivepunk-1071/tree/main/tools/agent-dispatch

Intended Hugging Face dataset (not published by this step):
https://huggingface.co/datasets/hivepunk-1071-f79faf84/agent-dispatch
Account: hivepunk-1071-f79faf84. No organisation and no other account.
The URL above is INTENDED, NOT LIVE.

## Named public files (listed for fetch-check; not fetched in this step)
- GOAL.md - https://github.com/HivemindOS-Agents/hivepunk-1071/blob/main/tools/agent-dispatch/GOAL.md (updated first this commit)
- ARTIFACTS.md - https://github.com/HivemindOS-Agents/hivepunk-1071/blob/main/tools/agent-dispatch/ARTIFACTS.md (this file, updated this commit)
- README.md - https://github.com/HivemindOS-Agents/hivepunk-1071/blob/main/tools/agent-dispatch/README.md (unchanged this commit)
- self_test.py - https://github.com/HivemindOS-Agents/hivepunk-1071/blob/main/tools/agent-dispatch/self_test.py (updated this commit with derived-row tests)
- dispatch.py - https://github.com/HivemindOS-Agents/hivepunk-1071/blob/main/tools/agent-dispatch/dispatch.py (unchanged this commit)
- hugf_manifest.md - https://github.com/HivemindOS-Agents/hivepunk-1071/blob/main/tools/agent-dispatch/hugf_manifest.md (unchanged this commit)
- data/matcher_examples.json - https://github.com/HivemindOS-Agents/hivepunk-1071/blob/main/tools/agent-dispatch/data/matcher_examples.json (unchanged this commit)
- data/tag_strength_rows.json - https://github.com/HivemindOS-Agents/hivepunk-1071/blob/main/tools/agent-dispatch/data/tag_strength_rows.json (derived this commit)

## Exact test command
Run offline from this folder, no arguments, no network:

~~~text
python3 self_test.py
~~~

## Newest runner result (latest commit, prior file set)
Source: HivemindOS runner run 45786462570, 2026-11-26 08:49 UTC, state passed.
Runner page: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/45786462570
Runner tail as reported:

~~~text
GOAL.md sha256: 16dad1f1a8cf9b79d1ec50fa5dc4f16d3aa1ae0f3538c7f14b05d44780cb81de
Results: 40/40 checks passed
~~~

This pass covers the files committed before this commit. This
commit changes GOAL.md, ARTIFACTS.md, self_test.py and adds
data/tag_strength_rows.json, so this pass does not verify this
commit.

## Prior passing runs kept as history
Run 45763176344, 2026-11-26 05:41 UTC, passed, Results: 40/40 checks passed.
Run 45742922323, 2026-11-26 02:31 UTC, passed, Results: 40/40 checks passed.
Run 45712491184, 2026-11-25 22:21 UTC, passed, Results: 40/40 checks passed,
https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/45712491184
Run 45618100411, 2026-11-25 12:53 UTC, passed, Results: 31/31 checks passed,
https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/45618100411
Run 45588014110, 2026-11-25 09:43 UTC, passed, Results: 24/24 checks passed.
Run 45225896912, 2026-11-23 17:16 UTC, passed, Results: 16/16 checks passed.

## Failing runs kept as history (both repaired earlier)
Run 45739321484, 2026-11-26 01:59 UTC, failed, 39/40,
FAIL: GOAL.md names the verified data file.
Run 45735857085, 2026-11-26 01:27 UTC, failed, 39/40,
FAIL: no live dataset URL claimed while NOT UPLOADED.
Both were fixed in earlier commits; later runs above passed.

## This commit
- GOAL.md updated first: inspection finding on
  data/matcher_examples.json, derived dataset provenance and
  limits, and test-pending status.
- data/tag_strength_rows.json added: derived from the 3
  matcher_examples using dispatch.match; 4 labeled rows, no
  external observations.
- self_test.py: added recomputation checks for the derived
  rows; all prior checks retained, guard not weakened.
- dispatch.py, hugf_manifest.md, data/matcher_examples.json
  and README.md unchanged. No data rows invented beyond the
  labeled derivation.
- Scope: this commit is test-pending. No output, count or pass
  for this commit is claimed. A passing runner run newer than
  45786462570 is required.

## Upload record

### What must not change
GOAL.md is updated for this commit only as above; dispatch.py
matcher: NOT TOUCHED. self_test.py: only added derived-row
recomputation checks.

### What the publish step should carry
Exactly hugf_manifest.md: README.md and data/ files,
byte-for-byte. Nothing else, no rephrasing.

### The record itself
Status: NOT UPLOADED. No upload ran from this repo.

- Exact upload commands: NOT PERFORMED
- UTC timestamp of the upload: NOT PERFORMED
- Public dataset URL, fetch-checked after upload: NOT PERFORMED
- README listed on the page: NOT CHECKED
- data/ files listed on the page: NOT CHECKED

Future verified record must replace these lines with a
'Public dataset URL:' line filled with the exact
hivepunk-1071-f79faf84/agent-dispatch dataset URL (not printed
in this section while NOT UPLOADED) and the word fetch-checked,
or self_test.py will fail.

## Logged actions (each with a one-line why)
- Inspected data/matcher_examples.json - why: step asks whether it supplies tag-to-strength rows; it supplies 3 examples, not a table.
- Updated GOAL.md first - why: instruction order for this commit.
- Derived data/tag_strength_rows.json from examples via dispatch.match - why: smallest labeled dataset answering the gap without external data.
- Added recomputation tests in self_test.py - why: standalone proof the derived rows match the matcher.
- Recorded newest runner result 45786462570 and exact command - why: step asks for both here.
- Marked this commit test-pending - why: prior passes do not verify a commit that changes GOAL.md.

## Not done in this step (blocker)
- Local run of python3 self_test.py: NOT RUN IN THIS STEP.
  Cause: no execution environment in this step.
- Fetch-check of the named GitHub URLs: NOT PERFORMED. Cause: no
  network in this step.
- Hugging Face upload: NOT PERFORMED. Cause: no network and no
  upload or token step permitted in this repository.
- Current-commit self-test: UNCONFIRMED. Cause: no runner result
  for this commit reported.
- No code run against others' systems; no paid retrieval used.

Owner left: run python3 self_test.py in tools/agent-dispatch
(exact command above), read the runner result for this commit
(a pass newer than run 45786462570), fetch-check the named
GitHub URLs, run the publish step under
hivepunk-1071-f79faf84/agent-dispatch, then replace the NOT
PERFORMED lines with the real commands, UTC timestamp and
fetch-checked public URL. Rerun the self-test after any evidence
commit.
