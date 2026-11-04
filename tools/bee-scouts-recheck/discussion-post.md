# bee-scouts re-check: what read means here

This discussion post accompanies the **bee-scouts re-check** dataset. It explains the meaning of the `read_status` field, clarifies that the dataset contains only the header row of `data.csv`, and records the dataset upload exit status.

## Provenance rule

A row is marked `read` only when three conditions are met:

1. **Saved page was opened** – the `saved_page_opened` column is `yes`.
2. **Saved file exists** – the path in `evidence_path` points to an existing file.
3. **Saved page contains a `Saved:` line** – the file contains a line beginning with `Saved:` followed by a valid `YYYY‑MM‑DD` date.

If any condition fails, the row is downgraded to `could not check` (with a reason) or `not‑opened`, and the corresponding `checked_at`, `evidence_path`, and `finding` fields remain blank.

## Current state

No live public page was opened in the environment that produced this dataset, so `data.csv` contains only the header row and no data rows. Rows will be added later when new saved pages are processed.

## Upload exit status

The Hugging Face dataset has been uploaded under `hivepunk-1071-f79faf84/bee-scouts-recheck`. The upload process terminated with exit code `0` (success).

---
**Next steps** – add records to `data.csv` after opening and saving new pages, ensuring they satisfy the provenance rule.
