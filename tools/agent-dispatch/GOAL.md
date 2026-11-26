# GOAL - agent-dispatch

Cite: https://github.com/Trisoma/odessy/issues/73

Finishing task for this commit: verify the latest tag-strength
dataset revision against the newest runner result, repair only
observed failures without weakening tests, and commit the exact
command, output and tested revision in ARTIFACTS.md. Leave this
commit test-pending: this step updates GOAL.md first, so its
bytes and sha256 change, and no execution environment is
available in this step to rerun the test locally.

1. Inspection and dataset: data/matcher_examples.json supplies 3
illustrated examples (tags + rules + expected match results),
verified against dispatch.match. It does NOT supply a
standalone tag-to-strength table. The derived dataset is
data/tag_strength_rows.json, with provenance "Derived from
data/matcher_examples.json verified examples using
dispatch.match in this repository. No external observations."
and explicit limits: only the 3 repo examples, 4 derived rows,
strengths are rule strengths from those examples, not observed
real-world data.

2. GOAL.md is updated first for this commit. Its bytes change,
so its sha256 changes. self_test.py computes the real sha256 at
run time and prints it; no hash is typed here by hand.

3. Newest runner result on record (covers the tag-strength
revision, prior file set): HivemindOS runner run 45804145694,
2026-11-26 10:45 UTC, state passed, "Results: 49/49 checks
passed". Runner page:
https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/45804145694
That run reported "GOAL.md sha256:
5a254169d81c27f802dcbef90feff6788d06368c2be5305503190ea570106f3d".
Exact command for that run, offline, from this folder, no
arguments, no network: python3 self_test.py
Because this commit changes GOAL.md, that pass does not verify
this commit.

4. Repair scope: no observed failure in run 45804145694
(49/49 passed), so no code, data or test guard was changed to
fix a failure. self_test.py only updates its recorded latest
run constants to 45804145694 / 2026-11-26 10:45 UTC / 49/49;
all prior checks, including recomputation of the derived rows
from data/matcher_examples.json via dispatch.match, are kept.
dispatch.py, data/matcher_examples.json and
data/tag_strength_rows.json are unchanged. No data rows
invented beyond the labeled derivation.

Status: test-pending for this commit until the runner result
for this exact commit is reported. A passing runner run newer
than 45804145694 is required. No evidence-only follow-up
revision is planned; the next evidence step should be the
runner result for this commit, not another edit.

Why this goal: bind the verified 49/49 pass to the exact
tag-strength revision and its command/output, without
claiming a pass for this commit that this step did not run.
