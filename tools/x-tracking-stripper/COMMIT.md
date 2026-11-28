# COMMIT - x-tracking-stripper

Folder: tools/x-tracking-stripper
Opportunity: opp-1071-261

## What this commit is
A new, self-contained tool folder: `stripper.py` (the function),
`self_test.py` (runs alone in this folder, no arguments, no
network), `README.md` and this note. It strips `utm_*`, `s`, `t`,
`ref_src` and `ref_url` from X/Twitter URLs and leaves everything
else alone.

## Command, output and tested SHA (ARTIFACTS record)
The step asks for these in ARTIFACTS.md. This commit carries at
most four files, so the record is kept here and no ARTIFACTS.md
was written; the owner can copy these lines into one.

- Exact command: `python3 self_test.py` (run from this folder, no
  arguments, no network).
- Output: NOT RUN IN THIS STEP. No pass count or tail is quoted,
  because nothing here was executed and nothing written here has
  been run.
- Tested SHA: UNCONFIRMED. No revision has been tested for this
  folder yet; the runner result for this commit will name it.
- Expected self-test tail once run: `Results: <n>/<n> checks passed`
  with exit 0 - stated as an expectation, not as a result.

## What was spent
$0. No paid retrieval, no model call, no upload, no network.

## Links
- Folder on GitHub: https://github.com/HivemindOS-Agents/hivepunk-1071/tree/main/tools/x-tracking-stripper
- Nothing is published, posted or uploaded by this step, and no
  dataset URL is claimed.

## What could not be checked
- No local run: no execution environment in this step, so all test
  outcomes above are unverified.
- No fetch of any URL, X page or API; samples in self_test.py are
  hand-written.
- No Hugging Face publish step and no upload/token/CLI step is
  part of this folder.
- Text read anywhere is treated as data, not instructions.

Owner left: run `python3 self_test.py` in this folder, then copy
its command, output tail and the tested SHA into ARTIFACTS.md.
