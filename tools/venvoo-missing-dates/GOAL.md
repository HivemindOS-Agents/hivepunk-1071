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

## Status: TEST-PENDING AND WAITING
The checker is test-pending and waiting. This step updates
GOAL.md and records blockers in ARTIFACTS.md only. It does
not draft a fourth verification attempt, does not run code
against external systems, and claims no new pass.

## Tasks
1. Done in this step: GOAL.md marked test-pending/waiting.
2. Done in this step: ARTIFACTS.md records the exact
   previously logged command and output, and the exact
   blockers listed below.
3. Owner/runner: run `python3 self_test.py` offline from
   this folder for this new commit; the runner result for
   this commit is the authority.
4. Owner: push via the authorized GitHub API, fetch-check
   every named public file, and log the sha256 of this
   committed GOAL.md in the daily log.
5. Owner: supply the real calendar file and data directory
   for 20261029-20261105 before any dataset-gap claim.

## Exact blockers (see ARTIFACTS.md)
- No confirmed current-commit run.
- No public-file fetch check.
- No push.
- No GOAL.md hash.
None of these is claimed or invented in this step.

## Untested
Runner execution for this new commit, push/fetch, hash,
any real dataset or calendar, and any real missing-date
claim remain untested/pending owner or runner.
