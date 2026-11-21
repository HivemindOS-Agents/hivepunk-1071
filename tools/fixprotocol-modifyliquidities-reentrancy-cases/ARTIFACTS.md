# Artifacts - fixprotocol-modifyliquidities-reentrancy-cases

## Check-in 2026-11-21 - safe blocker, original folder missing

Step taken: GOAL.md updated first, then only this target folder
was inspected. It was not present in the supplied tools, so no
original self_test.py could be repaired or run. No code was run
against external systems in this step.

Exact safe blocker: original folder missing from supplied tools;
no verified private reporting channel identified; no finding
sent; no vulnerability details included or published.

No Hugging Face fetch/upload, live file list, revision, hash,
or row count was obtained, and none is claimed. No upload was
performed and publication is NOT claimed.

Owner left: restore the original folder or confirm a verified
private channel, then rerun the offline self-test in this folder.

## Check-in 2026-11-21 - false-positive fix, 12/13 prior runner

Prior runner: bee-self-test run 44881294942
ranAt 2026-11-21 07:40 UTC, state failed, 12/13 checks passed.
Non-sensitive detail: the only failure was the banned-word safety
check, triggered by README.md describing that check in its own
banned words. The failing line itself is not quoted here because
quoting it would retrigger the same check.

Change: README.md sentence reworded only. self_test.py unchanged,
so no safety check was weakened. No code was run against external
systems in this step and no local pass is claimed here; the
runner result for this fix is the authority and is left for the
owner/runner to record.

## Check-in 2026-11-21 - URL removal fix, 12/13 latest runner

Latest runner: bee-self-test run 44883707193
ranAt 2026-11-21 08:11 UTC, state failed, 12/13 checks passed.
Exact non-sensitive output of that run:

~~~text
ok: ARTIFACTS claims no publication
ok: README marks work untested
ok: no harmful instructions in records
FAIL: no invented URLs in records
ok: no invented long hashes in records
ok: README documents offline run command
Results: 12/13 checks passed
~~~

Cause: the record files here contained a full web URL for a
runner run, and the unchanged check flags any web URL in these
records. Change: removed the URL text from GOAL.md and
ARTIFACTS.md, replacing it with plain run-number references
only. self_test.py unchanged, so no safety check was weakened.
No code was run against external systems in this step and no
local pass is claimed here; the runner result for this fix is
the authority and is left for the owner/runner to record.

## Not checked
- Original folder contents, original self_test.py, data integrity.
- Any external system, private maintainer channel, or live dataset.
