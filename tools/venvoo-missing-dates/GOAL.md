# GOAL - venvoo-missing-dates

## Checkable goal
tools/venvoo-missing-dates/ contains an offline tool that,
given a local data directory and a supplied calendar file,
reports exactly the calendar dates with no valid YYYYMMDD
subdirectory, and never reports a date absent from the
supplied calendar as missing. The 20261029-20261105 range
is checked only from a calendar file the owner supplies
listing those dates; the tool supplies no calendar and
infers no trading days.

## Source link
Scout target for this work:
https://github.com/sledilnik/data/blob/master/check-missing-date.py
No venvoo dataset or real calendar for 20261029-20261105
was fetched or verified in this step.

## Current task
Finish this artifact: record the exact self-test command
and verbatim runner output in ARTIFACTS.md, list every
target file for owner push/fetch-check, and log the
GOAL.md hash from the committed file. Done in this step
except push/fetch and hash, blocked as recorded below.

## Tasks (3-5)
1. Done in this step: ARTIFACTS.md records `python3
   self_test.py` and the verbatim runner output supplied
   for this tool (14/14, run 45106238880).
2. Owner pushes via the authorized GitHub API, fetches
   every named public file listed in ARTIFACTS.md, and
   logs the sha256 of this committed GOAL.md in the
   daily log.
3. Owner supplies the real calendar file and data
   directory for 20261029-20261105, then runs check.py
   and records a dataset-gap claim only if the supplied
   calendar is itself verified.
4. Add a checked-in example calendar only if its source
   is cited; do not add an inferred weekend/holiday list.

## Status / untested
check.py, self_test.py, README.md and GOAL.md were built
in the prior step; this step updates GOAL.md and adds
ARTIFACTS.md. Runner execution for this new commit,
push/fetch, hash, any real dataset or calendar, and any
real missing-date claim remain untested/pending owner
or runner. No code was run against external systems.

## Daily-log hash
No hash computed or invented in this step. Precise
blocker: this step has no hash/push/fetch capability;
owner/runner must compute sha256 of the committed
GOAL.md and enter it in the daily log.
