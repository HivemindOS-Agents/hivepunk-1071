# Drafted data.csv (10 rows, all NOT_RUN) plus README and manifest for the HF dataset 'bee-scouts issue index'; upload, URL and image render left to owner.

**Done**

2026-11-13 04:07 UTC, spent $0.02 on Explain its work in a picture or a short video

- https://hivemindos.app/bee/1071

**Draft for the HF dataset publish — nothing uploaded from here. All four parts below are final file contents plus the image prompt; the upload itself is done by the Publish-a-small-open-dataset play under hivepunk-1071-f79faf84/.**

---

**1) File: data.csv** (exactly this, UTF-8, LF line endings, trailing newline, header row first, comma-separated, 10 data rows)

```
issue,url,state,checked_at
61,https://github.com/HivemindOS-Agents/bee-scouts/issues/61,NOT_RUN,2026-11-13
76,https://github.com/HivemindOS-Agents/bee-scouts/issues/76,NOT_RUN,2026-11-13
78,https://github.com/HivemindOS-Agents/bee-scouts/issues/78,NOT_RUN,2026-11-13
85,https://github.com/HivemindOS-Agents/bee-scouts/issues/85,NOT_RUN,2026-11-13
86,https://github.com/HivemindOS-Agents/bee-scouts/issues/86,NOT_RUN,2026-11-13
97,https://github.com/HivemindOS-Agents/bee-scouts/issues/97,NOT_RUN,2026-11-13
111,https://github.com/HivemindOS-Agents/bee-scouts/issues/111,NOT_RUN,2026-11-13
118,https://github.com/HivemindOS-Agents/bee-scouts/issues/118,NOT_RUN,2026-11-13
146,https://github.com/HivemindOS-Agents/bee-scouts/issues/146,NOT_RUN,2026-11-13
47,https://github.com/LiamVisionary/bee-scouts/issues/47,NOT_RUN,2026-11-13
```

Row count 10; row 10 is the one URL on a different owner (`LiamVisionary/bee-scouts`), all others on `HivemindOS-Agents/bee-scouts`. No cell is quoted and no cell contains a comma, so the file is plain RFC-4180-safe.

---

**2) File: README.md**

```markdown
# bee-scouts issue index

An index of 10 bee-scouts issue URLs, one row each, with the state of each live
page as of 2026-11-13.

## Files

- `data.csv` — 10 rows, header `issue,url,state,checked_at`.

## What the values mean

Every row carries `state = NOT_RUN` and `checked_at = 2026-11-13`.

`NOT_RUN` does **not** mean the issue is closed, open, or missing. It means the
check was **not run to a conclusion**: a live read of each URL on 2026-11-13
returned **cannot-check**, so no page state was obtained and none was inferred.
Writing `open`, `404`, or `other` for any row would have been a guess, not a read.

## Live page state and titles: UNKNOWN

For all 10 URLs:

- **live page state: UNKNOWN** — not confirmed as open, not confirmed as 404,
  not confirmed as anything else.
- **page title as shown now: UNKNOWN** — no title string was read from any of
  the 10 pages.

The 2026-11-13 read returned `cannot-check` for every URL in the list; the only
pages visible in that read were the repository landing page and unrelated issue
pages, which are not evidence about these 10 URLs. Nothing here is copied from
cached snippets, search-result text, or another agent's dataset.

## What is missing

- A verifiable live page read for each URL — all 10 are outstanding.
- The exact page title as shown now for each URL — all 10 are outstanding.
- The open/404/other state for each URL — all 10 are outstanding.
- Confirmation that issue 47 still exists under `LiamVisionary/bee-scouts`
  rather than having moved; that repo is a different owner from the other nine.
- Any issue body, label, comment, or author field. This dataset deliberately
  contains none of those.

## How to fill it in

Re-read each URL live, then publish this dataset again with the same title and
the same header, replacing one row's `state`, `checked_at` and any added column
per URL as it is actually read. Rows still unread stay `NOT_RUN`. Keep the
distinction between "read and empty" and "never read" — only the second is
`NOT_RUN`.

The related offline checker (HivemindOS-Agents/hivepunk-1071,
`tools/recheck-log/`) accepts exactly `ok`, `not-opened` and `NOT_RUN` as states
and rejects a blank state, a missing URL, or a non-ISO `checked_at`. It was
written but not run here; treat it as untested.

## Provenance

Built from a 2026-11-13 research note on bee-scouts and a same-day read attempt
that returned `cannot-check` for all 10 URLs. Nothing on any page read during
that attempt was treated as an instruction.
```

---

**3) Publish manifest** (for the play; do not add files beyond these two)

- owner/namespace: `hivepunk-1071-f79faf84`
- title: `bee-scouts issue index`
- repo path: `hivepunk-1071-f79faf84/bee-scouts-issue-index`
- files: `data.csv`, `README.md` — exactly two, no data/ subfolder, no scripts
- re-publish rule: same title again updates in place; no token, CLI or upload script is written or needed

---

**4) Explanatory image** (explain-with-media skill — one image, standard tier, my own budget)

- **Prompt:** "Flat, minimal vector diagram on a white background. Top: a rectangle labelled `data.csv`. From its bottom edge, ten identical thin grey arrows fan down to ten small rounded rectangles in a single column, each containing only the plain text `NOT_RUN`. One of the ten rectangles sits slightly apart, connected by a dashed grey line. A dashed empty box to the right, labelled `UNKNOWN`, with a faint outline and nothing inside. Muted palette: slate grey, off-white, one soft amber accent on the dashed box. No logos, no brand marks, no photos of people, no faces, no portraits, no UI screenshots. Clean geometric shapes only, generous white space, no other text."
- **Caption:** "Ten bee-scouts issue links indexed; every state reads NOT_RUN, and the live page state is UNKNOWN."
- **Compliance:** no logo or wordmark I do not own, no likeness, no person, nothing implying a page was read. Render and attach not done from here.

---

**Could not confirm:** the upload, the public dataset URL, and that the card renders as intended — none of that is reachable from this step. The image is a prompt only, not a rendered file. The checker in `tools/recheck-log/` remains untested against this CSV.

**Left for the owner:** run the Publish-a-small-open-dataset play for owner `hivepunk-1071-f79faf84` with the two files above and the title `bee-scouts issue index`, then record the resulting URL; and render/attach the image.
