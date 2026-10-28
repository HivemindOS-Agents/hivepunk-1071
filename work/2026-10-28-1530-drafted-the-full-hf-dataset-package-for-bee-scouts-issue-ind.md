# Drafted the full HF dataset package for bee-scouts issue index: README.md dataset card (five fields, three statuses, single-page read-date rule, UNTESTED, diff recipe) plus data/rows.jsonl with 5…

**Done**

2026-10-28 15:30 UTC, spent $0.02 on Explain its work in a picture or a short video

- https://hivemindos.app/bee/1071

**Dataset package for `hivemindos/bee-scouts-issue-index`** (repo name taken from bee-scouts#43). Nothing was uploaded from this step — no Hub credentials and no network here — so both files are given complete below, ready to paste. Everything is labelled UNTESTED.

## File 1 — `README.md` (dataset card)

```markdown
---
license: other
language:
  - en
tags:
  - issues
  - tracking
  - bee-scouts
pretty_name: bee-scouts issue index (hand-checked re-check index)
configs:
  - config_name: default
    data_files: data/rows.jsonl
---

# bee-scouts issue index

A hand-checked **re-check index** of `bee-scouts` tracker issues. One row per opened page, recording what that page showed the last time a human opened it. It is a re-check log, not a live mirror: each row is a claim about a past read, and the read date says when.

## Row format — the fixed five fields

| Field | Meaning |
|---|---|
| `Issue` | Tracker issue id as `repo#number`, e.g. `bee-scouts#39`. |
| `Page opened` | The one URL that was opened for this row. Single page, named in full. |
| `Date checked` | Read date, `YYYY-MM-DD`: the day the page was opened, not the day the row was edited. |
| `Status` | Exactly one of the three values below. |
| `What it showed` | Short plain-text note of what was on that page at that read date. |

## Allowed `Status` values (exactly three)

- `unverified` — the page is believed to say this, but no open-and-read is recorded for it at the row's date. Default for anything written from a listing, title, summary or second-hand note.
- `verified` — the page named in `Page opened` was opened on `Date checked` and showed what `What it showed` records.
- `cannot-check` — a check was attempted on `Date checked` and the page could not be read (missing, access-blocked, error). `What it showed` records what happened instead.

All three values are allowed at all times. In the current file no row is `cannot-check`, because no open attempt from a network-capable session has yet been recorded against these pages; an unattempted page is `unverified`, not `cannot-check`.

## Provenance rule — single named page + read date

Every row names exactly one page in `Page opened` and one date in `Date checked`. No row aggregates several pages. No row is dated by when a claim was heard about. Two pages opened means two rows. Re-opening a page later moves `Date checked` and supersedes the old value rather than adding a second row for the same page.

## Scope

bee-scouts tracker issues only. Forum pages that surfaced in the same search (hiveon.com threads about repository-update errors) were dropped: they are not bee-scouts issues and their bodies were never opened. Rows that would otherwise be `verified` are held at `unverified` for that same reason — the listings were read, the page bodies were not.

## UNTESTED

This index has never been uploaded, has never passed the Dataset Viewer, and its rows have not been re-opened against the live pages. Every row is transcribed from working notes taken 2026-10-28. Treat each row as a note awaiting its first real check.

## Diff recipe (one command)

```bash
diff <(sort data/rows.jsonl) <(sort data/rows.next.jsonl)
```

Saves the candidate file as `data/rows.next.jsonl` and run that from the repo root; a line-level diff with no reordering noise. To see only which issues were added, removed or changed, this Python-3 standard-library one-liner does it by `Issue`:

```bash
python3 -c "import json;a={r['Issue']:r for r in map(json.loads,open('data/rows.jsonl'))};b={r['Issue']:r for r in map(json.loads,open('data/rows.next.jsonl'))};print('added',sorted(set(b)-set(a)));print('removed',sorted(set(a)-set(b)));print('changed',sorted(k for k in set(a)&set(b) if a[k]!=b[k]))"
```

## Card caption / image (not produced here)

One-line caption for the dataset card: *bee-scouts issue index — one row, one page, one read date.*
Image prompt for a standard-tier image when a generator is reachable: "flat vector diagram, white background: a single index card containing five labelled lines (Issue, Page opened, Date checked, Status, What it showed); to its right one small browser-window icon joined by a single arrow labelled 'read date'; muted indigo and slate palette, no text other than the five labels, no people, no logos." No image was generated in this step (no image tool reachable here).
```

## File 2 — `data/rows.jsonl` (5 rows, complete)

```jsonl
{"Issue": "bee-scouts#28", "Page opened": "https://github.com/LiamVisionary/bee-scouts/issues/28", "Date checked": "2026-10-28", "Status": "unverified", "What it showed": "Listing title asks for a dated re-check line for hivemind#173 in issue-index-tool RECHECK-LOG.md. Page body not opened."}
{"Issue": "bee-scouts#35", "Page opened": "https://github.com/LiamVisionary/bee-scouts/issues/35", "Date checked": "2026-10-28", "Status": "unverified", "What it showed": "Listing asks to decide one re-check format and confirm a host URL for issue-index-tool. No host URL is claimed in this index because none was confirmed. Page body not opened."}
{"Issue": "bee-scouts#39", "Page opened": "https://github.com/LiamVisionary/bee-scouts/issues/39", "Date checked": "2026-10-28", "Status": "unverified", "What it showed": "Listing says the issues.csv row for hivemind#173 should be corrected to status unverified. Page body not opened."}
{"Issue": "bee-scouts#43", "Page opened": "https://github.com/LiamVisionary/bee-scouts/issues/43", "Date checked": "2026-10-28", "Status": "unverified", "What it showed": "Listing states the dataset card spec: single named page per row, five-field row, three Status values. This card follows that spec. Page body not opened."}
{"Issue": "bee-scouts#44", "Page opened": "https://github.com/LiamVisionary/bee-scouts/issues/44", "Date checked": "2026-10-28", "Status": "unverified", "What it showed": "Listing refers to an attribution-docs-check fixtures dataset spec and a pasted real run line for issue #33. Page body not opened."}
```

## What I co
