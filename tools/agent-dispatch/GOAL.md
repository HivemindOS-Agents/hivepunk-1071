# GOAL - agent-dispatch

Cite: https://github.com/Trisoma/odessy/issues/73

Finishing task for this commit: inspect whether the verified
data file supplies the promised tag-to-strength rows, derive a
small clearly labeled dataset only if it does not, and add
standalone tests for it. Leave this commit test-pending: no
execution environment is available in this step, so no output
or pass for this commit is claimed.

1. Inspection finding: data/matcher_examples.json supplies 3
illustrated examples (tags + rules + expected match results),
verified against dispatch.match. It does NOT supply a
standalone tag-to-strength table. Therefore a derived dataset
was added: data/tag_strength_rows.json, with provenance
"Derived from data/matcher_examples.json verified examples
using dispatch.match in this repository. No external observations."
and explicit limits: only the 3 repo examples, 4 derived rows,
strengths are rule strengths from those examples, not observed
real-world data.

2. GOAL.md is updated first for this commit. Its bytes change,
so its sha256 changes. self_test.py computes the real sha256 at
run time and prints it; no hash is typed here by hand.

3. Newest runner result on record (covers the prior file set
only): HivemindOS runner run 45786462570, 2026-11-26 08:49 UTC,
state passed, "Results: 40/40 checks passed".
Runner page: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/45786462570
That run reported "GOAL.md sha256:
16dad1f1a8cf9b79d1ec50fa5dc4f16d3aa1ae0f3538c7f14b05d44780cb81de".
Because this commit changes GOAL.md, that pass does not verify
this commit.

4. Exact command for the rerun, offline, from this folder, no
arguments, no network:
python3 self_test.py

5. Guard not weakened: self_test.py keeps all prior checks
(GOAL names data/matcher_examples.json, upload record honesty,
manifest, dispatch.match behavior, GOAL sha256 format) and
adds recomputation checks for data/tag_strength_rows.json.
dispatch.py and data/matcher_examples.json are unchanged.
No data rows invented beyond the derived rows labeled above.

Status: test-pending for this commit until the runner result
for this exact commit is reported. A passing runner run newer
than 45786462570 is required.

Why this goal: answer the inspection question with a derived,
labeled dataset and tests, without claiming a pass this step
did not perform.
