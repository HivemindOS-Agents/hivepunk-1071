# wizz-air-se-sas-number-check

opportunity: opp-1071-122

Offline checker for a reported airline phone number (for example
a number reported in Vyber07/cyber-security discussion 22)
against official airline evidence supplied as input.

## Verdict rule
- `UNKNOWN` unless the discussion text was actually retrieved, a
  claimed number is supplied, the claimed entity is an airline,
  and official numbers for that airline are supplied.
- `MATCH` only when the normalised claimed number is in the
  supplied official list.
- `MISMATCH` only when both sides are supplied and the normalised
  claimed number is not in the official list.
- A mismatch is never inferred from a missing page, a search
  snippet, or software documentation.

## Entities - do not confuse SAS software with the airline
- `sas_airline`: SAS / Scandinavian Airlines.
- `sas_software`: SAS Institute and SAS software, analytics or
  programming services. Software contact details are not airline
  evidence; `check.py` returns `UNKNOWN` for them.
- `wizz_air`: Wizz Air.
- `unknown`: anything else.

## Current evidence status - untested
Existing research did not retrieve discussion 22 text, so its
reported number and airline are UNKNOWN. It also did not retrieve
a live official Wizz Air Sweden number. SAS Sweden numbers seen
in prior research (+46 8 522 170 00, +46 8 522 171 60,
+46 8 797 0000) are unverified reference values from earlier
search results in this repository, not live-verified in this
step and not established as SAS Scandinavian Airlines numbers
as opposed to SAS software contacts. Treat them as untested.
No mismatch is claimed on their basis.

## Use (offline)
Input JSON keys: `claimed_airline`, `claimed_number`,
`official_numbers` (list), `discussion_text_retrieved` (bool),
`discussion_text` (string).

~~~text
python3 check.py input.json --out result.json
python3 self_test.py
~~~

## Self-test status on record
Latest runner result supplied to this step: 17/17 checks passed,
run 44989998381, 2026-11-22 05:34 UTC. The runner result for
this new commit is the authority; no local pass is claimed here.

## Untested
- Discussion 22 content; live official airline pages.
- Runner execution of self_test.py for this commit.
- Any push, publication or public URL verification; none is
  claimed here, pending owner push/fetch.
