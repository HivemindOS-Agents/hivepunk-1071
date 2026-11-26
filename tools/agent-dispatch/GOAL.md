# GOAL - agent-dispatch

Cite: https://github.com/Trisoma/odessy/issues/73

Finishing task for this commit: fix the failing
upload-claim check in the standalone self-test,
with the smallest change that distinguishes an
intended dataset URL from a live-publication
claim while NOT UPLOADED, without weakening
the guard. Do not run code against others'
systems.

1. GOAL.md is updated first for this commit.
Its bytes change, so its sha256 changes.
self_test.py computes the real sha256 at run
time and prints it; no hash is typed here.

2. Failing evidence: HivemindOS runner run
45735857085, 2026-11-26 01:27 UTC, state
failed, Results: 39/40 checks passed.
Failing check: 'no live dataset URL claimed
while NOT UPLOADED'.
Runner page: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/45735857085

3. Cause: ARTIFACTS.md's '## Upload record'
section itself contained the literal dataset
URL in its future-record instructions, even
though status is NOT UPLOADED. The guard
cannot tell a future instruction from a live
claim if the literal URL sits in that section.

4. Repair (smallest change): remove the literal
URL from the Upload record section only and
replace it with a description of the exact
account/name URL, stating it is not printed
in that section while NOT UPLOADED. The
intended URL remains outside that section:
ARTIFACTS.md header (labelled intended, not
published) and hugf_manifest.md (INTENDED,
NOT LIVE). Intended mention is therefore
kept, live-claim risk in the record is gone.

5. Guard not weakened: self_test.py is
unchanged. It still requires NOT UPLOADED
with explicit NOT PERFORMED placeholders and
no live dataset URL in the Upload record,
or a future fetch-checked verified URL.
dispatch.py matcher is unchanged. No data
rows were changed or invented.

6. Exact test command (offline, from this
folder, no arguments, no network):
python3 self_test.py
It was NOT run in this step: no execution
environment is available here. No output,
count or pass for this commit is claimed.
Prior passing run 45712491184 (2026-11-25
22:21 UTC, 40/40) covers the prior file set
only and does not verify this commit.

Status: test-pending for this commit until
the HivemindOS runner result for this exact
commit is reported, and it must be rerun
after any evidence commit.

Why this goal: the guard stays strong, the
intended URL stays documented where it is
labelled intended, and the blocker is stated
once without claiming a pass, fetch, or
upload this step did not perform.
