# microcks-v2-kickoff

opportunity: opp-1071-15

Offline labelled summary of the Microcks v2 kick-off
discussion (issue #2412), built from the prior research
note already in this repository (2026-11-24-microcks-v2).
It renders stated goals, open questions, and claims, each
labelled FACT, DERIVED, or UNKNOWN. It fetches nothing and
invents nothing: anything not in the input JSON is UNKNOWN.

## GOAL (updated first for this tool)
Cite: https://github.com/microcks/microcks/issues/2412

Finish tools/microcks-v2-kickoff: summarize the
discussion's stated goals and open questions using the
existing research and issue, label claims, and include a
usage README and standalone offline self_test.py.
Status: code, sample_data.json, this README (with GOAL and
ARTIFACTS sections), and self_test.py are committed in
this step. Runner execution for this commit, push,
public fetch-check, separate GOAL.md file, and GOAL.md
hash are blockers - see ARTIFACTS section below. No pass
is claimed here. A separate GOAL.md is not shipped due
to the 4-file limit; this section is the committed GOAL
content for this step. Owner to add GOAL.md and hash it.

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
Target: tools/microcks-v2-kickoff
Public files to verify by fetch (not fetched here):
kickoff.py, sample_data.json, self_test.py, README.md.

Exact test command (offline, from this folder):

~~~text
python3 self_test.py
~~~

Exact test output for this commit: NOT RUN IN THIS STEP.
No output or pass is claimed or invented here. HivemindOS
runs self_test.py after commit; the runner result for
this new commit is the authority.

Blockers: no confirmed current-commit run; no push via
authorized GitHub API; no public-file fetch-check; no
separate GOAL.md shipped and no GOAL.md hash logged.
Issue text was not re-fetched in this step; the summary
relies on prior research on record and labels the rest
UNKNOWN. No code run against others' systems.

## Untested
- Runner execution of self_test.py for this commit.
- Push, publication, public fetch-check, GOAL.md hash.
- Any issue content beyond prior research on record.
