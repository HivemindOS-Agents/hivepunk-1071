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

## Tasks (3-5)
1. Run `python3 self_test.py` offline from this folder via
   the runner and record the exact output in ARTIFACTS.md.
2. Owner supplies the real calendar file and data directory
   for 20261029-20261105, then runs check.py and records
   the missing list as a dataset-gap claim only if the
   supplied calendar is itself verified.
3. Owner pushes via the authorized GitHub API, fetches every
   named public file, and logs the sha256 of this GOAL.md
   in the daily log.
4. Add a checked-in example calendar only if its source is
   cited; do not add an inferred weekend/holiday list.

## Status / untested
Built in this step: check.py, self_test.py, README.md,
GOAL.md. Runner execution for this commit, push/fetch,
hash, ARTIFACTS.md update, any real dataset or calendar,
and any real missing-date claim remain untested/pending
owner or runner. No code was run against external systems.

## Daily-log hash
No hash computed or invented in this step; owner/runner
must compute sha256 of the committed GOAL.md.
