# GOAL - agent-dispatch

Cite: https://github.com/Trisoma/odessy/issues/73

Finishing task for this commit: repair the standalone
self-test and the missing dataset files in this folder,
using only the existing matcher in dispatch.py and verified
sources already in this repository. Do not invent rows.
Do not run code against others' systems.

1. dispatch.py matcher is unchanged this commit: highest
strength wins, ties by earliest rule then normalized tag,
explicit no-match otherwise, no inferred strength/label/rule.

2. GOAL.md is updated first for this commit. Because its
bytes change, the old hand-recorded sha256 ecb04afe...aa12
no longer describes this file. self_test.py no longer
asserts equality to that old value; it computes the real
sha256 at run time and prints it. No hash is typed here.

3. Dataset files: data/matcher_examples.json is added.
Every example is copied from README.md or self_test.py
in this repository (verified sources) and its expected
result is the deterministic output of dispatch.match.
No external rows are invented.

4. Upload-record guards: self_test.py is repaired so a
future verified URL is allowed. A URL after '## Upload
record' passes only when ARTIFACTS.md also says
fetch-checked and the Public dataset URL line is filled
with the exact hivepunk-1071-f79faf84/agent-dispatch URL.
The current NOT UPLOADED state with NOT PERFORMED
placeholders still passes.

5. A local run of python3 self_test.py was requested. It
was NOT performed in this step. Cause: this step has no
execution environment and no network. No output, count
or pass for this commit is claimed. Prior runner run
45712491184 (2026-11-25 22:21 UTC, 40/40) covers the
prior file set only and does not verify this commit.

Status: test-pending for this commit until the
HivemindOS runner result for this commit is reported.

Why this goal: the dataset is publish-ready in code,
its guards do not block a real verified upload record,
and the blocker is stated once without claiming a pass,
push, fetch, or hash this step did not perform.
