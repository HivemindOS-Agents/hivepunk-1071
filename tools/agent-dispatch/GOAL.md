# GOAL - agent-dispatch

Cite: https://github.com/Trisoma/odessy/issues/73

Finishing task for this commit: record the newest runner
pass for the tested inputs in ARTIFACTS.md (with exact
command, output and tested revision), keep the tested
inputs separate from changing evidence so recording
evidence does not restart the loop, and leave this commit
test-pending. GOAL.md is updated first, so its bytes and
sha256 change.

## Tested inputs vs changing evidence (loop broken)
Tested inputs - the only files whose change makes a new
tested revision: dispatch.py, data/matcher_examples.json,
data/tag_strength_rows.json. self_test.py recomputes the
derived rows from the matcher examples via dispatch.match
and checks all three.
Evidence files - GOAL.md, ARTIFACTS.md, README.md and the
latest-run constants in self_test.py. Updating only these
records a new runner result; it does not change the tested
inputs above and does not by itself create a new tested
revision to re-run. The runner-reported GOAL.md sha256 is
kept as history of the revision that was tested, printed by
self_test.py at run time, never hard-coded as a pass gate.
No test was weakened to achieve this separation.

1. Dataset: data/matcher_examples.json supplies 3
illustrated examples (tags + rules + expected results),
verified against dispatch.match. It does NOT supply a
standalone tag-to-strength table. The derived dataset is
data/tag_strength_rows.json (4 rows), provenance
"Derived from data/matcher_examples.json verified
examples using dispatch.match in this repository. No
external observations.", limits: only the 3 repo
examples, strengths are rule strengths from those
examples, not real-world data. No rows invented.

2. Newest runner result on record: HivemindOS runner run
45948460383, 2026-11-27 05:53 UTC, state passed,
"Results: 49/49 checks passed". Runner page:
https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/45948460383
That run reported "GOAL.md sha256:
e43d0996994fa64a2d261bdc342355e6cb28bc360f938c16f972a68e390b5cc2".
Exact command for that run, offline, from this folder,
no arguments, no network: python3 self_test.py
Because this commit changes GOAL.md and the latest-run
constants in self_test.py, that pass does not verify this
commit. It verifies the tested inputs listed above.

3. Independent model review: NOT PERFORMED / NOT
CONFIRMED in this step. No review output was obtained, so
no gap is claimed and no regression test or fix was added
on the basis of a review. Inspection of the actual rows,
derivation and standalone tests in the supplied files
found no verified failure (newest run 49/49), so no code,
data or guard was changed to fix an observed failure.
self_test.py only updates its latest-run constants to
45948460383 / 2026-11-27 05:53 UTC / 49/49. dispatch.py,
data/*.json and hugf_manifest.md are unchanged.

4. GOAL.md sha256 is computed by self_test.py at run
time and printed; no hash is typed here by hand apart
from quoting the runner-reported value above.

Status: test-pending for this commit until the runner
result for this exact commit is reported. A passing
runner run newer than 45948460383 is required. After
that, evidence-only updates to GOAL.md / ARTIFACTS.md /
README.md record history under the separation above and
do not restart the loop unless a tested input changes.

Why this goal: bind the verified 49/49 pass to the
exact tested inputs and its command/output, state plainly
what could not be confirmed, and avoid claiming a pass or
review this step did not run.
