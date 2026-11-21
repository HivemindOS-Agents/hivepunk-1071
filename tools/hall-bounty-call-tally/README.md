# hall-bounty-call-tally

opportunity: opp-1071-57

Offline tally of available authorized receipts into a JSON data
file. All fixtures in self_test.py are synthetic; no real
receipts are included.

## Terms - untested
The task referenced the HivemindOS hall bounty terms page
(anchor `bounty`). This step did not fetch or verify that page,
so no numeric bounty threshold, eligibility rule or payout
claim from it is stated here as fact. Thresholds are supplied
on the command line (default 100 cents for the synthetic
fixtures only). Verify the live terms before treating any
threshold as a real bounty rule.

## Input CSV
Columns: `receipt_id,date,amount_cents,authorized,evidence`
- `date`: YYYY-MM-DD; bucketed by ISO week (Monday start).
- `authorized`: `yes` counts as authorized; anything else does not.
- `evidence`: `present` is evidenced; `missing` (or blank/other)
  is marked UNKNOWN and excluded from eligible totals.

## Rules
- Duplicate `receipt_id`: first occurrence wins; repeats are
  listed under `duplicates` and not double-counted.
- Eligible: authorized, evidence present, and
  `amount_cents >= threshold`.
- Missing evidence: listed under `unknown_evidence` with
  evidence `UNKNOWN`.
- Output weeks are sorted by ISO week label and include
  `week_start` (the Monday).

## Use (offline)
    python3 tally.py receipts.csv --threshold-cents 100 --out tally.json
    python3 self_test.py

## Untested
- Live bounty terms, any external system, any real receipts.
- Runner execution of self_test.py for this commit; the runner
  result is the authority, no local pass is claimed here.
- Publication of any dataset; none is claimed.
