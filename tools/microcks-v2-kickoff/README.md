# microcks-v2-kickoff

Offline labelled summary of the Microcks v2 kick-off
discussion (issue #2412), built from the prior research
note already in this repository (2026-11-24-microcks-v2).
It renders stated goals, open questions, and claims, each
labelled FACT, DERIVED, or UNKNOWN. It fetches nothing and
invents nothing: anything not in the input JSON is UNKNOWN.

## GOAL (updated first for this step)
Cite: https://github.com/microcks/microcks/issues/2412

Finish tools/microcks-v2-kickoff: summarize the
discussion's stated goals and open questions using the
existing research and issue, label claims, include a
usage README and standalone offline self_test.py, run
the test offline from that folder, record the exact
command and output in ARTIFACTS.md, commit and push all
named files, then fetch-check each public file. Log the
GOAL.md hash. Report any blocker without claiming
success. Do not run code against others' systems.

Status for this commit: test-pending until verified.
All tasks above are test-pending for this commit until
the HivemindOS runner result for this new commit is
reported. The prior commit's runner pass (see ARTIFACTS
below) does not verify this commit.

Note: a separate GOAL.md and ARTIFACTS.md are not
shipped in this commit due to the 4-file limit; this
README carries the GOAL and ARTIFACTS content. Owner to
add GOAL.md and ARTIFACTS.md as separate files and log
the GOAL.md sha256 in the daily log - no hash is claimed
here because none was computed in this step.

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
A separate ARTIFACTS.md is not shipped due to the
4-file limit; this section is the ARTIFACTS content.

Exact test command (offline, from this folder):

~~~text
python3 self_test.py
~~~

Exact test output on record - prior commit runner run
45312611765, 2026-11-24 02:28 UTC, state passed
(https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/45312611765), output tail verbatim:

~~~text
ok: empty goals still render section without inventing items
ok: CLI writes output
ok: CLI output matches render
usage: python3 kickoff.py INPUT.json [--out FILE]
INPUT.json: {issue_url, goals[], open_questions[], claims[]} - see sample_data.json
ok: CLI requires input
Results: 16/16 checks passed
~~~

That prior pass covered the prior 16-check self_test.
This commit adds one README-citation check (17 checks
expected) and is test-pending: no output or pass for
this commit is claimed or invented here. HivemindOS
runs self_test.py after commit; that runner result is
the authority. Record its exact output verbatim here
in a follow-up step.

Blockers: no confirmed current-commit run; no push via
authorized GitHub API; no public-file fetch-check; no
separate GOAL.md/ARTIFACTS.md shipped and no GOAL.md
sha256 logged. Issue text was not re-fetched in this
step; the summary relies on prior research on record
and labels the rest UNKNOWN. No code run against
others' systems.

## Untested
- Runner execution of self_test.py for this commit.
- Push, publication, public fetch-check, GOAL.md hash.
- Any issue content beyond prior research on record.
