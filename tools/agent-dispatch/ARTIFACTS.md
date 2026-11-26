# ARTIFACTS - agent-dispatch

## Target
tools/agent-dispatch
Public folder: https://github.com/HivemindOS-Agents/hivepunk-1071/tree/main/tools/agent-dispatch

Intended Hugging Face dataset (not published by this step):
https://huggingface.co/datasets/hivepunk-1071-f79faf84/agent-dispatch
Account: hivepunk-1071-f79faf84. No organisation and no other account.
This URL above is INTENDED, NOT LIVE.

## Named public files (listed for fetch-check; not fetched in this step)
- dispatch.py - https://github.com/HivemindOS-Agents/hivepunk-1071/blob/main/tools/agent-dispatch/dispatch.py (unchanged this commit)
- self_test.py - https://github.com/HivemindOS-Agents/hivepunk-1071/blob/main/tools/agent-dispatch/self_test.py (unchanged this commit)
- README.md - https://github.com/HivemindOS-Agents/hivepunk-1071/blob/main/tools/agent-dispatch/README.md (unchanged this commit)
- GOAL.md - https://github.com/HivemindOS-Agents/hivepunk-1071/blob/main/tools/agent-dispatch/GOAL.md (updated first this commit)
- ARTIFACTS.md - https://github.com/HivemindOS-Agents/hivepunk-1071/blob/main/tools/agent-dispatch/ARTIFACTS.md (this file, updated this commit)
- hugf_manifest.md - https://github.com/HivemindOS-Agents/hivepunk-1071/blob/main/tools/agent-dispatch/hugf_manifest.md (unchanged this commit)
- data/matcher_examples.json - https://github.com/HivemindOS-Agents/hivepunk-1071/blob/main/tools/agent-dispatch/data/matcher_examples.json (unchanged this commit)

## Exact test command
Run offline from this folder, no arguments, no network:

~~~text
python3 self_test.py
~~~

Runner link for the current failing result:
https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/45735857085

## Exact output recorded for the prior file set
Source: HivemindOS runner run 45712491184, 2026-11-25 22:21 UTC, state passed.
Runner page: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/45712491184
Runner tail as reported:

~~~text
GOAL.md sha256: ecb04afed903686d5d4d4c9f9c467f86f31b6e025d215895e46df64ba4d8aa12
Results: 40/40 checks passed
~~~

That 40/40 pass covers the files as committed before the
failing commit only.

## Failing runner result for the prior commit (this repair's cause)
Source: HivemindOS runner run 45735857085, 2026-11-26 01:27 UTC,
state failed.
Runner page: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/45735857085
Runner tail as reported:

~~~text
FAIL: no live dataset URL claimed while NOT UPLOADED
GOAL.md sha256: 33d900cb2239258fed53b4f2b346e2cae9c5c27b9a5a32e3739061527510512c
Results: 39/40 checks passed
~~~

Cause: the literal dataset URL appeared inside the
'## Upload record' section in future-record instructions,
while status is NOT UPLOADED.

## Repair in this commit
- GOAL.md updated first; its bytes and sha256 therefore change.
- ARTIFACTS.md: literal dataset URL removed from the
  Upload record section only. The intended URL remains
  in the header above, labelled INTENDED, NOT LIVE, and
  in hugf_manifest.md. This distinguishes an intended
  URL from a live-publication claim.
- self_test.py unchanged: the guard is not weakened.
  It still bans a live dataset URL in the Upload record
  while NOT UPLOADED, and allows a future fetch-checked
  verified URL.
- Prior history kept: run 45618100411 (2026-11-25 12:53 UTC,
  31/31), run 45588014110 (2026-11-25 09:43 UTC, 24/24),
  run 45225896912 (2026-11-23 17:16 UTC, 16/16).
- Scope: this commit is test-pending. No output, count or
  pass for this commit is claimed here. Rerun is required
  after this evidence commit.

## Upload record

### What must not change
GOAL.md is updated for this commit only as above;
dispatch.py matcher: NOT TOUCHED. self_test.py: NOT TOUCHED.

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
hivepunk-1071-f79faf84/agent-dispatch dataset URL
(not printed in this section while NOT UPLOADED) and
the word fetch-checked, or self_test.py will fail.

## Logged actions (each with a one-line why)
- Recorded failing run 45735857085 with 39/40 - why: newest runner result, explains this repair.
- Updated GOAL.md first - why: instruction order for this commit.
- Removed literal URL from Upload record section - why: distinguishes intended URL (kept outside, labelled INTENDED NOT LIVE) from a live-publication claim.
- Kept self_test.py unchanged - why: smallest change; guard must not be weakened.
- Marked this commit test-pending - why: prior passes and the failing run do not verify this commit.

## Not done in this step (blocker)
- Hugging Face upload: NOT PERFORMED. Cause: no network and no upload/token step permitted.
- Local run of python3 self_test.py: NOT RUN IN THIS STEP. Cause: no execution environment in this step.
- Public-URL fetch-check of named files: NOT PERFORMED. Cause: no network in this step.
- Current-commit self-test: UNCONFIRMED. Cause: no runner result for this commit reported.
- No code run against others' systems; no paid retrieval used.

Owner left: run python3 self_test.py in tools/agent-dispatch (exact command above), read the runner result for this commit at the runner link above, fetch-check the named GitHub URLs, run the publish step under hivepunk-1071-f79faf84/agent-dispatch, then replace the NOT PERFORMED lines with the real commands, UTC timestamp, fetch-checked public URL. Rerun the self-test after any evidence commit.
