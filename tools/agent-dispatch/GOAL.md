# GOAL - agent-dispatch

Cite: https://github.com/Trisoma/odessy/issues/73

Finishing task for this commit: prepare the existing
agent-dispatch tag-to-strength dataset for publication in
its own repository; do not create a different dataset and
do not touch parked folders.

1. The matcher in dispatch.py is existing and unchanged in
this commit: given local tags and local rules (tag +
numeric strength), return the highest-strength match, break
strength ties by earliest rule position, then by normalized
tag, and return an explicit no-match object when nothing
matches. No strength, label, or rule is inferred.

2. The runner result now on record (run 45225896912,
2026-11-23 17:16 UTC, state passed, "Results: 16/16 checks
passed", https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/45225896912)
covers the prior commit only. It does not verify this
commit.

3. A local run of `python3 self_test.py` in this folder was
requested. It was NOT performed in this step. Cause: this
step has no network access, no authorized push, and no
execution environment. No evidence of any other cause was
obtained, so no other cause is claimed. No output, count,
or pass for this commit is claimed here.

4. The GOAL.md sha256 is NOT typed into this file. A
hand-typed hash cannot be verified here. Instead
self_test.py computes the real sha256 of this file at run
time and prints "GOAL.md sha256: <value>" as the last line
before its summary, so the runner output carries the true
hash of the committed GOAL.md. Owner: copy that printed
line into the daily log.

Status: test-pending for this commit until the HivemindOS
runner result for this commit is reported. A prior runner
pass on record does not verify this commit.

Why this goal: so the dataset is prepared for publication
with the blocker stated once, accurately, without claiming
a pass, push, fetch, or hash that this step did not perform.
