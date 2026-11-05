# Public AI model release pages

A dataset of rows, one per public AI model release page fetched during a single session. Each row records what the page itself states for each field. Empty cells mean the page did not state a value.

## Columns

| Column | Description |
|--------|-------------|
| `page_url` | Full URL of the public page read |
| `publisher` | Publisher or developer as stated on the page |
| `title` | Title of the model or release as stated on the page |
| `date_read` | Date (YYYY-MM-DD) when the page was read |
| `states_context_window` | `yes` or blank; `yes` if the page explicitly states a context window number, blank if not mentioned |

## What was read

No pages were fetched this session. The dataset currently contains only the header row. Rows will be added after live pages are read.

## What I could not confirm

- All cells are blank because no pages were fetched.
- No pages failed to load (zero attempted).

## Usage

This CSV may be loaded into any spreadsheet or analysis tool. The `states_context_window` column uses `yes` only when the page contains an explicit numeric context window (e.g., 128K, 1M tokens). A blank means the page does not state a context window.

## Notes

Every value is taken only from the page content. No value is inferred from the URL, the publisher's other models, or any external tracker. If a page lists a publisher but does not mention context window, the `states_context_window` cell stays blank.

---

Created by bee #1071.
