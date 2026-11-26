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
- README.md - https://github.com/HivemindOS-Agents/hivepunk-1071/blob/main/tools/agent-dispatch/README.md (updated this commit)
- self_test.py - https://github.com/HivemindOS-Agents/hivepunk-1071/blob/main/tools/agent-dispatch/self_test.py (updated this commit: latest-run constants only)
- dispatch.py - https://github.com/HivemindOS-Agents/hivepunk-1071/blob/main/tools/agent-dispatch/dispatch.py (unchanged this commit)
- hugf_manifest.md - https://github.com/HivemindOS-Agents/hivepunk-1071/blob/main/tools/agent-dispatch/hugf_manifest.md (unchanged this commit)
- data/matcher_examples.json - https://github.com/HivemindOS-Agents/hivepunk-1071/blob/main/tools/agent-dispatch/data/matcher_examples.json (unchanged this commit)
- data/tag_strength_rows.json - https://github.com/HivemindOS-Agents/hivepunk-1071/blob/main/tools/agent-dispatch/data/tag_strength_rows.json (derived earlier, unchanged this commit)

## Exact test command
Run offline from this folder, no arguments, no network:

~~~text
python3 self_test.py
~~~

## Newest runner result (tag-strength revision)
Source: HivemindOS runner run 45804145694, 2026-11-26 10:45 UTC, state passed.
Runner page: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/45804145694
Exact command: python3 self_test.py (from tools/agent-dispatch)
Runner tail as reported:

~~~text
GOAL.md sha256: 5a254169d81c27f802dcbef90feff6788d06368c2be5305503190ea570106f3d
Results: 49/49 checks passed
~~~

Tested revision: the file set whose GOAL.md hashed to
5a254169d81c27f802dcbef90feff6788d06368c2be5305503190ea570106f3d
and which included data/tag_strength_rows.json (4 derived
rows recomputed by self_test.py from data/matcher_examples.json
via dispatch.match). This pass covers that revision only.
This commit changes GOAL.md, ARTIFACTS.md, self_test.py and
README.md, so this pass does not verify this commit.

## Prior passing runs kept as history
Run 45786462570, 2026-11-26 08:49 UTC, passed, Results: 40/40 checks passed.
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
Both were fixed in earlier commits; later runs above passed,
including run 45804145694 at 49/49.

## This commit
- GOAL.md updated first: records runner pass 45804145694,
  tested revision sha256, exact command, and test-pending
  status; no evidence-only loop after this commit.
- ARTIFACTS.md: records the exact command, the runner tail
  output, and the tested revision above.
- self_test.py: only the latest-run constants updated to
  45804145694 / 2026-11-26 10:45 UTC / 49/49; all 49 checks
  retained, including derived-row recomputation. Guard not
  weakened. No observed failure to repair (49/49 passed).
- README.md: status line refreshed to run 45804145694.
- dispatch.py, hugf_manifest.md, data/matcher_examples.json
  and data/tag_strength_rows.json unchanged. No data rows
  invented.
- Scope: this commit is test-pending. No output, count or pass
  for this commit is claimed. A passing runner run newer than
  45804145694 is required.

## Upload record

### What must not change
GOAL.md is updated for this commit only as above; dispatch.py
matcher: NOT TOUCHED. self_test.py: only latest-run constants.

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
- Updated GOAL.md first - why: instruction order for this commit.
- Recorded runner pass 45804145694 (49/49), its exact command and tested GOAL.md sha256 in ARTIFACTS.md - why: step asks for all three here.
- Updated self_test.py latest-run constants only - why: keep the recorded evidence in sync without weakening any check.
- Checked for failures to repair - why: run 45804145694 passed 49/49, so none observed and no guard changed.
- Marked this commit test-pending - why: prior passes do not verify a commit that changes GOAL.md, and no evidence-only loop follows.

## Not done in this step (blocker)
- Local run of python3 self_test.py: NOT RUN IN THIS STEP.
  Cause: no execution environment in this step. The runner
  result above is existing evidence, not a local run.
- Fetch-check of the named GitHub URLs: NOT PERFORMED. Cause: no
  network in this step.
- Hugging Face upload: NOT PERFORMED. Cause: no network and no
  upload or token step permitted in this repository.
- Current-commit self-test: UNCONFIRMED. Cause: no runner result
  for this commit reported.
- No code run against others' systems; no paid retrieval used.

Owner left: read the runner result for this commit (a pass
newer than run 45804145694), fetch-check the named GitHub
URLs, run the publish step under
hivepunk-1071-f79faf84/agent-dispatch, then replace the NOT
PERFORMED lines with the real commands, UTC timestamp and
fetch-checked public URL.
