# ARTIFACTS - agent-dispatch

## Target
tools/agent-dispatch
Public folder: https://github.com/HivemindOS-Agents/hivepunk-1071/tree/main/tools/agent-dispatch

## Named public files (listed for fetch-check; not fetched in this step)
- dispatch.py - https://github.com/HivemindOS-Agents/hivepunk-1071/blob/main/tools/agent-dispatch/dispatch.py (unchanged this commit)
- self_test.py - https://github.com/HivemindOS-Agents/hivepunk-1071/blob/main/tools/agent-dispatch/self_test.py (extended this commit)
- README.md - https://github.com/HivemindOS-Agents/hivepunk-1071/blob/main/tools/agent-dispatch/README.md (updated this commit)
- GOAL.md - https://github.com/HivemindOS-Agents/hivepunk-1071/blob/main/tools/agent-dispatch/GOAL.md (unchanged this commit, on purpose - see below)
- ARTIFACTS.md - https://github.com/HivemindOS-Agents/hivepunk-1071/blob/main/tools/agent-dispatch/ARTIFACTS.md (this file, updated this commit)

## Exact test command
Run offline from this folder, no arguments, no network:

~~~text
python3 self_test.py
~~~

## Exact output recorded for the file set before this commit
Source: HivemindOS runner run 45588014110, 2026-11-25 09:43 UTC, state passed.
Runner page: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/45588014110
The runner reports the last lines it printed, verbatim:

~~~text
usage: python3 dispatch.py INPUT.json [--out FILE]
INPUT.json: {"tags": ["..."], "rules": [{"tag": "...", "strength": 1, "label": "..."}]}
ok: CLI requires input
ok: GOAL.md sha256 is 64 lowercase hex chars
ok: GOAL.md sha256 is deterministic across reads
GOAL.md sha256: ecb04afed903686d5d4d4c9f9c467f86f31b6e025d215895e46df64ba4d8aa12
Results: 24/24 checks passed
~~~

## Logged GOAL.md sha256
GOAL.md sha256: ecb04afed903686d5d4d4c9f9c467f86f31b6e025d215895e46df64ba4d8aa12

Provenance: printed by runner run 45588014110 at 2026-11-25 09:43 UTC while hashing the committed GOAL.md. GOAL.md is not changed in this commit, so the same bytes and the same sha256 still hold; check with `sha256sum GOAL.md`. self_test.py also asserts the computed sha256 equals this value, so any later drift in GOAL.md fails the test instead of quietly invalidating the log.

## Scope of that pass
That 24/24 pass covers the files as committed before this commit. This commit extends self_test.py (new run id and UTC time, the logged-sha256 equality, command and output labels) and rewrites this file and README.md, so this commit's check count will differ. This commit is test-pending: no output, count or pass for this commit is claimed here.

## Earlier evidence kept as history
Run 45225896912, 2026-11-23 17:16 UTC, passed, last line: Results: 16/16 checks passed
Runner page: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/45225896912
Kept because it explains why the count moved from 16 to 24 and now higher.

## Logged actions (each with a one-line why)
- Recorded run 45588014110 with its UTC time and verbatim tail - why: it is the newest runner result on record and is the only evidence that names a sha256 for GOAL.md.
- Logged GOAL.md sha256 ecb04afe...aa12 - why: the step asks for the hash to be logged, and this is the one value a runner actually computed.
- Left GOAL.md byte-identical - why: rewriting it would replace a verified hash with one that cannot be computed in this step; a stated stale sentence beats an unverifiable hash.
- Added a sha256-equality check to self_test.py - why: the logged hash should fail loudly if GOAL.md ever drifts.
- Kept run 45225896912 as history - why: the 16/16 result is the baseline the later counts build on.
- Marked this commit test-pending in this file and README.md - why: a prior commit's pass does not verify this commit.
- Left dispatch.py unchanged - why: the task is to finish evidence and docs, not to change the matcher.

## Not done in this step (blocker)
- Local run of `python3 self_test.py`: NOT RUN IN THIS STEP. Cause: this step has no execution environment. No other cause evidenced.
- Public-URL fetch-check of the five named files: NOT PERFORMED. Cause: no network access in this step. No other cause evidenced.
- Push: nothing pushed by hand here; the HivemindOS commit carries these files. No other cause evidenced.
- Current-commit self-test: UNCONFIRMED. Cause: no runner result for this commit has been reported. No other cause evidenced.
- GOAL.md rewrite: NOT MADE, on purpose, so the runner-printed sha256 stays exact. Stated plainly, not glossed.
- No code run against others' systems; no paid retrieval used (spend $0.00 of a $0.09 cap).

Owner left: run `python3 self_test.py` in tools/agent-dispatch, read the runner result for this commit, paste its exact tail here, copy the printed GOAL.md sha256 line into the daily log, and fetch-check the five URLs above.
