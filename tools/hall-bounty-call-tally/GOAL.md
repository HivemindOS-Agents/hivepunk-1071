# GOAL - hall-bounty-call-tally

## Target
tools/hall-bounty-call-tally
Account: hivepunk-1071-f79faf84 (only account; no organisation)

## Status 2026-11-21
GOAL.md updated first in this step. Then the offline tally tool
was built in this folder only: tally.py, README.md, self_test.py
and this GOAL.md. No code was run against external systems in
this step, and no live terms page was fetched or verified here.
The bounty terms reference supplied for the task is the
HivemindOS hall bounty page (anchor bounty); its numeric terms
are NOT claimed as verified in this folder. Thresholds are
configurable inputs, and all fixture rows are synthetic.

## What it does
Tallies available authorized receipts offline into a JSON data
file. Missing evidence is marked UNKNOWN and excluded from
eligible totals. Duplicate receipt_id values are counted once
(first occurrence wins) and reported. Week boundaries use ISO
weeks (Monday start, date field per receipt).

## Daily-log hash
No hash computed or invented in this step. Any daily-log hash
must be computed by the owner/runner from committed files.

## Untested
- Live bounty terms content and threshold values.
- Runner execution of self_test.py for this commit.
- Any external system, live publication, or authorized receipt
  source. No such source was accessed or claimed.

## Next (owner)
Run python3 self_test.py from this folder offline, record the
exact runner output in the repository artifacts, verify the
live terms before using any threshold as a bounty rule, and
only then tally real authorized receipts supplied by the owner.
