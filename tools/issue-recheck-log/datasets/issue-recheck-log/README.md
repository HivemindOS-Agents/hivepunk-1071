# issue‑recheck‑log

A small public log of re‑checked issue pages.

## What this is
Each row records a public issue report that was scanned by the `issue‑watch` tool.
A row is **marked** as a read only when a saved page in this repository backs it;
otherwise the *read_status* column is left blank and a *status_reason* explains why.

The dataset is **unlicensed** – it contains only provenance data and short
metadata; the text of the issue page itself is not reproduced.

## How the CSV was produced
`tools/recheck-lint/publish_recheck_rows.py` emits a CSV when run on the host:

```bash
python3 tools/recheck-lint/publish_recheck_rows.py rows.jsonl \
    --card "<issue‑URL>" > datasets/issue-recheck-log/rows.csv
```

The run command is copied verbatim to the **Run command** section of the card and
recorded in the *May‑2026‑log* file.

## Columns
| column | description |
|---|---|
| `id` | internal stable row identifier |
| `source_url` | public issue URL |
| `title` | title of the issue |
| `first_seen_utc` | when the tool first saw the issue |
| `last_checked_utc` | when the last re‑check ran |
| `read_status` | `read` only when a saved page backs it |
| `status_reason` | why `read_status` is blank – either *Not opened* or *Could not check* |
| `evidence_path` | path to the saved page if present |
| `notes` | free‑form notes from the tool |

## Not opened
Rows that were never fetched have `read_status` blank and `status_reason` starting with:

```
Not opened: never fetched this run
```

## Could not check
Rows where a fetch was attempted but failed (HTTP error, timeout, etc.) have:

```
Could not check: <error description>
```

## No license claimed
Only the metadata produced by the tool is in this dataset; no part of an issue
page is reproduced. The CSV is raw data and may be reused freely.

## How to update
Run the command above again, replace the CSV, and re‑upload the dataset. The card
source (`<issue‑URL>`) should be updated to the current run.

---

The CSV file is in `datasets/issue-recheck-log/rows.csv`.
