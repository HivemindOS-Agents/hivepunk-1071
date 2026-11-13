# recheck-log

Validate one re-check log CSV. A re-check log tracks which issue pages were
opened (re-checked) and what state they were in when checked.

## CSV format

Exactly four columns in this order:

    issue,url,state,checked_at

Extra columns are permitted but ignored. The file is UTF-8 with optional BOM.
LF or CRLF line endings.

## State values

Case- and space-sensitive. Only these three are PASS:

- `ok` — the page opened and the outcome matches expectation
- `not-opened` — the page could not be opened (network, 404, etc.)
- `NOT_RUN` — no re-check was attempted yet

## accepted checked_at formats (ISO 8601)

- `YYYY-MM-DD` (date only)
- `YYYY-MM-DDTHH:MM`
- `YYYY-MM-DDTHH:MM:SS`
- `YYYY-MM-DDTHH:MM:SS.fraction`
- With timezone: `Z`, `+HH:MM`, `-HH:MM`, `+HHMM`, `-HHMM`

A space-separated `2026-11-12 09:28` is **not** accepted (T required).

## Run it

    python3 recheck_log.py ROWS.csv
    python3 recheck_log.py --help

Stdlib only, no network, no subprocess.

## Exit codes

| code | meaning |
|---|---|
| 0 | every row PASSes |
| 1 | at least one row FAILs |
| 2 | usage error, file not found, or wrong header |

## Output format

One line per data row:

    PASS row N: issue=... url=... state=... checked_at=...
    FAIL row N: issue=... url=... state=... checked_at=... :: reason(s)

Then one summary line:

    rows=N failed=M

When a row FAILs, the script exits 1 after the summary.

## Self-test

    cd tools/recheck-log && python3 self_test.py

Builds its own fixture CSVs in a temp directory, runs recheck_log.py on each,
and checks output lines and exit codes. Exits 0 only when every check passes.
No arguments, no network, stdlib only.

## Untested

- **Never run against a real CSV from a bee-scouts dataset.** All fixtures are
  synthetic.
- The time validation regex may not catch every edge case (e.g., minutes=60 is
  caught but hours=24 is not caught unless followed by "00:00" — 24:00 is
  allowed by ISO 8601 for end-of-day but would PASS here).
- The tool reads the CSV by its exact header order `issue,url,state,checked_at`.
  If a file has those four columns in a different order it will be rejected.
- Extremely long fields (e.g., 100K URL) are printed verbatim on the output
  line and may cause display issues.
- No BOM-UTF-16LE or other encodings are handled.

## Files

| file | what it is |
|---|---|
| `recheck_log.py` | the tool |
| `self_test.py` | offline checks, run with no arguments |
| `README.md` | this file |
