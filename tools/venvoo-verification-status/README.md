# venvoo-verification-status

opportunity: opp-1071-177

Offline tool that prevents a premature "verified" claim for
tools/venvoo-missing-dates. It reads a JSON verification-state
file and returns `WAIT` unless every required item is
explicitly `true`: current-commit runner pass, push via the
authorized GitHub API, public-file fetch-check, and GOAL.md
sha256 logged in the daily log.

## Why this exists
The latest runner record supplied for venvoo-missing-dates was
run 45160199680, 2026-11-23 10:54 UTC, passed, 14/14 checks.
That alone does not prove push, fetch-check, or hash. This
step left the venvoo folder untouched and did not launch a
new run or draft a new verification attempt; this tool only
records that the remaining blockers are still open.

## Use (offline)

~~~text
python3 status.py sample_status.json
python3 status.py state.json --out result.json
python3 self_test.py
~~~

`sample_status.json` models the state on record at this step:
runner pass true, push/fetch/hash false, verdict WAIT.

## Untested
- Runner execution of this tool's own self_test.py for this
  commit; the runner result is the authority and no local
  pass is claimed here.
- Owner push, public-file fetch-check, and GOAL.md hash for
  venvoo-missing-dates; none performed or claimed here.
- Any real venvoo dataset, calendar, trading days, or gaps;
  none fetched, inferred, or claimed here.
