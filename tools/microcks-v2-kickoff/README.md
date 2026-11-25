# microcks-v2-kickoff

Offline labelled summary of the Microcks v2 kick-off
discussion (issue #2412), built from the prior research
note already in this repository (2026-11-24-microcks-v2).
It renders stated goals, open questions, and claims, each
labelled FACT, DERIVED, or UNKNOWN. It fetches nothing and
invents nothing: anything not in the input JSON is UNKNOWN.

## GOAL
See GOAL.md in this folder. Cite:
https://github.com/microcks/microcks/issues/2412

Status for this commit: test-pending. The prior commit's
runner pass (run 45420531669, 2026-11-24 15:01 UTC, 19/19
checks passed) does not verify this commit. See ARTIFACTS.md.

## Use (offline)

~~~text
python3 kickoff.py sample_data.json
python3 kickoff.py input.json --out summary.md
python3 self_test.py
~~~

Input JSON shape: issue_url (must equal the #2412 URL),
goals[], open_questions[], claims[] - each item has a
label (FACT/DERIVED/UNKNOWN) and non-empty text. See
sample_data.json. Output is Markdown with a counts line.

## What the sample says (labelled, from prior research)
- FACT: Microcks is open-source, cloud-native API
  mocking/testing; CNCF incubating; v2 is an early
  undecided study; 1.16.0 had just been released.
- FACT goals: kick off discussion before committing a
  roadmap; set guiding principles.
- UNKNOWN: v2 timeline, migration path, and final
  architecture - not established, not guessed.

## ARTIFACTS
See ARTIFACTS.md in this folder for the target, named
public files, exact test command, prior runner output
(run 45420531669, 2026-11-24 15:01 UTC, 19/19; earlier
45388184137, 19/19; 45334486417, 17/17), and the exact
blocker. No output or pass for this commit is claimed here.

## Self-test output note
self_test.py prints "GOAL.md sha256: <value>" as the last
line before its summary, so the runner output carries the
true hash of the committed GOAL.md. Copy that line into the
daily log; no hash is typed into any file by hand.

## Untested
- Network-enabled GitHub retrieval of the named files; not
  performed in this step (no network).
- Runner execution of self_test.py for this commit.
- Push, publication, public fetch-check, and a GOAL.md hash
  stored in a file.
- Any issue content beyond prior research on record.
