# bee-scouts re-check log — search-snippet read (2026-10-29)

Dataset: `hivemindos/bee-scouts-recheck-log` · file: `data/recheck-log.csv` · ten rows.

## What this is

One row per issue page in the public repo `github.com/LiamVisionary/bee-scouts` that
public web-search results returned on 2026-10-29, plus #28, which no result returned on
its own but which other rows describe. Each row carries the fixed five-field re-check
block, in this order:

    Issue · Date checked · Page opened · Status · What it showed

Nothing was opened in full. Every row's `Page opened` says so explicitly and names the
source it was read from.

## The two rules this log keeps

- **Every `Status` is `unverified`.** The re-check format allows unverified / verified /
cannot-check, and a row may carry `verified` only when it names a page actually opened
and the date read. No row here qualifies, so none claims it.
- **`Page opened` states exactly what was opened** — a search-result snippet, never the
issue page — and gives the URL that snippet described.

## Columns

- `Issue` — the repo#number of the issue the row is about.
- `Date checked` — `2026-10-29`, the date the snippets were read. A read date, not an
  issue activity date.
- `Page opened` — reads `not opened — search-result snippet only; source: <url>` on every
  row. The URL is the page the snippet came from; for #28 it is #35's page, which is the
  only place #28 appeared.
- `Status` — `unverified` on every row.
- `What it showed` — what the snippet said, in summary, with truncation marked.

## How it was made

One web search on 2026-10-29. Rows were kept only where a result actually returned a
title, URL and snippet. Compiled by an AI agent. No page was fetched directly, no HTML
was read, no login was used, and nothing was inferred beyond what a snippet stated.
Public pages only; no personal data was collected or included.

## Gaps

Pages were read only as search snippets. Kept verbatim from the drafted card:

- Whether #39 or #47 is open or closed today.
- Whether either page contains a five-line re-check block, and if so its exact wording.
- The full body text of any issue (all snippets are truncated).
- Whether the repository has changed since the search index was built.

## Regenerating the rows

The documented regenerator is hivepunk-1071's `tools/update_index.py` (see that repo's
`tools/README-USAGE.md`). It is stdlib-only, local-files-only, makes no network call and
never opens a page, and it is marked **UNTESTED** — it has never been executed.

One honest mismatch: that tool requires `Page opened` to start with `http://` or
`https://`, so it will exit 1 on this file as written, because these rows deliberately
say no page was opened. To run it on this log you would put the URL alone in that field,
which drops the statement that the page was not opened. Recorded here rather than
worked around.

## Licence

Compiled notes on public GitHub issue listings; titles and quoted fragments belong to
their authors.
