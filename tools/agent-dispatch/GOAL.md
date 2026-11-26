# GOAL - agent-dispatch

Cite: https://github.com/Trisoma/odessy/issues/73

Finishing task for this commit: fix the sole failing
check in runner run 45739321484, 'GOAL.md names the
verified data file', with the smallest correction.
GOAL.md is updated first for this commit. Do not
run code against others' systems.

1. GOAL.md is updated first for this commit.
Its bytes change, so its sha256 changes.
self_test.py computes the real sha256 at run
time and prints it; no hash is typed here.

2. Failing evidence: HivemindOS runner run
45739321484, 2026-11-26 01:59 UTC, state
failed, Results: 39/40 checks passed.
Failing check: 'GOAL.md names the verified
data file'.
Runner page: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/45739321484
Runner tail as reported:

~~~text
FAIL: GOAL.md names the verified data file
GOAL.md sha256: c9254d7fc58f481ad523022d71846f2645bfce9072877664a0e296cc3c4d2dce
Results: 39/40 checks passed
~~~

3. Cause: the previous GOAL.md stated the goal
at length but never named the verified data
file, even though that file exists in the
folder. The self-test requires the exact path
to appear in GOAL.md.

4. Repair (smallest change): name the actual
verified data file in this GOAL.md:
data/matcher_examples.json
That file already exists under data/ in this
folder, with 3 examples verified against
dispatch.match and sourced only from
README.md and self_test.py. It is genuinely
present, so no file needs to be added and no
rows are invented. The exact path above is
the correction.

5. Guard not weakened: self_test.py is
unchanged. It still requires GOAL.md to name
data/matcher_examples.json, requires
NOT UPLOADED with explicit NOT PERFORMED
placeholders and no live dataset URL in the
Upload record, or a future fetch-checked
verified URL. dispatch.py matcher and the
data file are unchanged.

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
after any evidence commit. A passing runner
run newer than 45739321484 is required.

Why this goal: naming the real verified file
in GOAL.md satisfies the check without
weakening it, adding an unnecessary file,
or claiming a pass this step did not run.
