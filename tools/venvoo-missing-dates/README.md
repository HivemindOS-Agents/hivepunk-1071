# venvoo-missing-dates

opportunity: opp-1071-180

Offline checker that compares local `YYYYMMDD` data directories
against a **supplied** trading-calendar file and prints the
expected dates with no directory.

## Rule: no inferred trading days
The supplied calendar is the only authority. This tool never
uses weekday, holiday, exchange, or any other rule to decide
what should exist. A date that is not in the supplied calendar
is never reported as missing, even if no directory exists for
it. If you supply a calendar for 20261029-20261105, only the
dates listed in that file can appear in `missing`.

## Inputs
- `--data-dir DIR`: immediate subdirectories whose names are
  valid `YYYYMMDD` dates count as present. Files, and
  directories with other names (including invalid dates such
  as `20261301`), are listed in `ignored_names` and do not
  count as present.
- `--calendar FILE`: one `YYYYMMDD` per line; blank lines and
  `#` comment lines are skipped, duplicates are counted once,
  an invalid date line is an error. Extra fields after a comma
  or whitespace are ignored.

## Output (JSON)
`expected`, `present`, `missing` (expected with no directory),
`extra_not_in_calendar` (present but not expected; reported
for information only, never as missing), `ignored_names`, and
`counts`. All date lists are sorted.

## Example (offline, supplied calendar only)

~~~text
python3 check.py --data-dir data --calendar calendar.txt --out result.json
python3 self_test.py
~~~

For the step range 20261029-20261105 the owner supplies a
calendar file listing exactly the dates to check; this tool
does not supply or verify that calendar, and does not fetch
any venvoo dataset. Example calendar lines would be the dates
the owner chooses to list, e.g. `20261029` through `20261105`
as listed by the owner - weekends or holidays are excluded
only because the owner left them out of the file, never by
inference in this code.

## Self-test
Run offline from this folder with no arguments:

~~~text
python3 self_test.py
~~~

It builds temporary fixtures only; no network, no external
systems, no real dataset.

## Untested
- Runner execution of `self_test.py` for this commit; the
  runner result is the authority and no local pass is claimed
  here.
- Any real venvoo data directory or real trading calendar for
  20261029-20261105; none was fetched, supplied, or verified
  in this step, and no gap in any real dataset is claimed.
- Push, publication, and public-URL verification; none is
  claimed here, pending owner push/fetch.
