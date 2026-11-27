# GOAL - agent-dispatch

Cite: https://github.com/Trisoma/odessy/issues/73

Finishing task for this commit: record the newest runner
pass for the tag-strength dataset revision in ARTIFACTS.md
(with exact command, output and tested revision), and
leave this commit test-pending. GOAL.md is updated first,
so its bytes and sha256 change.

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

2. Newest runner result on record (covers the
tag-strength revision): HivemindOS runner run
45891956381, 2026-11-26 20:34 UTC, state passed,
"Results: 49/49 checks passed". Runner page:
https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/45891956381
That run reported "GOAL.md sha256:
43ea88d3c5b508844f88d8a27923b349f9535c0e1a0ac437a8819a32cc13ba88".
Exact command for that run, offline, from this folder,
no arguments, no network: python3 self_test.py
Because this commit changes GOAL.md, that pass does
not verify this commit.

3. Independent model review: NOT PERFORMED / NOT
CONFIRMED in this step (earlier step likewise). No
review output was obtained, so no gap is claimed and no
regression test or fix was added on the basis of a
review. Inspection of the actual rows, derivation and
standalone tests in the supplied files found no verified
failure (newest run 49/49), so no code, data or guard was
changed to fix an observed failure. self_test.py only
updates its latest-run constants to 45891956381 /
2026-11-26 20:34 UTC / 49/49. dispatch.py, data/*.json and
hugf_manifest.md are unchanged.

4. GOAL.md sha256 is computed by self_test.py at run
time and printed; no hash is typed here by hand apart
from quoting the runner-reported value above.

Status: test-pending for this commit until the runner
result for this exact commit is reported. A passing
runner run newer than 45891956381 is required. No
evidence-only follow-up loop is planned.

Why this goal: bind the verified 49/49 pass to the
exact tag-strength revision and its command/output,
state plainly what could not be confirmed, and avoid
claiming a pass or review this step did not run.
