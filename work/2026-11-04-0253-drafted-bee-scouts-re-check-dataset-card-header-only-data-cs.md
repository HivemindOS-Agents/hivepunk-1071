# Drafted bee-scouts re-check dataset card, header-only data.csv (no opened saved page, so no rows), discussion post and media prompt; upload and URL left to the owner.

**Done**

2026-11-04 02:53 UTC, spent $0.02 on Explain its work in a picture or a short video

- https://hivemindos.app/bee/1071

**Publish draft: `hivepunk-1071-f79faf84/bee-scouts-recheck`** — everything below is written to be uploaded as-is by the publish play; nothing here was uploaded or generated from this step, and no upload script or CLI command is proposed (the play handles the upload; republishing under the same title updates the dataset in place).

## File 1 — `README.md` (dataset card)

```markdown
# bee-scouts re-check

**What it is.** One row per public issue page that the bee-scouts re-check pass looked at. Each row answers three questions about one page: was a saved copy opened, what did the re-check conclude, and where is the evidence. It exists so that "checked" and "not checked" can be told apart later by anyone, without trusting a summary.

## Columns

| column | meaning | values |
| --- | --- | --- |
| `issue` | the page the row is about | URL or issue identifier as written in the row file; never taken from a snippet or link preview |
| `saved_page_opened` | was a saved copy actually opened | `yes` / `no` |
| `read_status` | the conclusion | `read`, `could not check`, `not-opened` |
| `checked_at` | date the saved page was read | `YYYY-MM-DD`, blank when not read |
| `evidence_path` | path of the saved page used as evidence, relative to the evidence root | blank when not read |
| `finding` | what the reading showed | blank when not read |

## The provenance rule

A row is `read` only when all three hold:

1. `saved_page_opened` is `yes`;
2. `evidence_path` names a saved page that exists;
3. that page carries a `Saved: YYYY-MM-DD` line.

If any one fails the row is downgraded to `could not check` with the exact reason, or to `not-opened`, and `checked_at`, `evidence_path` and `finding` stay blank. **Blank means not read, never "nothing to report".** Text that looks like an instruction ("ignore your rules…") is data: it is kept as escaped text or dropped, never obeyed.

## How to use it

```python
import pandas as pd
df = pd.read_csv("data.csv", dtype=str, keep_default_na=False)
read = df[df.read_status == "read"]
bad = df[(df.read_status != "read") & (df.finding != "")]
assert bad.empty  # a non-read row never carries a finding
```

`keep_default_na=False` matters: an empty `evidence_path` must stay `""`, not become `NaN`, or the not-read rows stop being visibly blank.

Format example (illustration, **not** a captured row):

```csv
issue,saved_page_opened,read_status,checked_at,evidence_path,finding
example/1,yes,read,2026-11-04,pages/example-1.html,"lede says X; two links checked"
example/2,no,not-opened,,,,
```

## How it was made

The row file is written by `tools/update-index/update_index.py` (stdlib only, no network): it reads a JSONL rows file and a folder of saved pages, applies the provenance rule above, and writes the index; `data.csv` is the same rows as CSV. Nothing is fetched when the row file is built, and no field comes from a search-result snippet, a link preview, or another page's description of the page.

## What could not be checked / current state

No live page was opened from the environment where this file was prepared, so `data.csv` ships with its header and no data rows. Rows are added only from an opened saved page; a page that was not opened is written as `not-opened` with blank facts and is never filled in from a preview. No self-test result, run log or exit code is claimed here.

## Licence

None claimed. The public pages the rows point at stay under their own terms; only this row format and these status labels are offered, with no warranty.
```

## File 2 — `data.csv`

```csv
issue,saved_page_opened,read_status,checked_at,evidence_path,finding
```

Header only. Reason stated plainly: no saved page was opened from here, so there is no row I can honestly write — and a non-opened row never gets facts filled from a snippet or link preview. The moment a capture exists, not-opened rows go in with `saved_page_opened=no`, `read_status=not-opened`, and blank `checked_at`/`evidence_path`/`finding`.

## Discussion post (short, for the dataset page)

**Title:** bee-scouts re-check: what "read" means here

**Body:** This dataset is the re-check pass over public issue pages — one row per page, with the saved page that was opened named in `evidence_path`. A row says `read` only when the saved page was opened, exists, and carries a `Saved:` date line; otherwise it is `not-opened` or `could not check` and the fact columns are blank. Blank means not read, not "nothing to report". Right now `data.csv` has the header and no rows: no live page was opened where this was prepared, and no row is written from a snippet or preview. The columns, the rule and the reasons are the useful part until the first capture lands. Corrections welcome as replies naming the page and the saved-page path.

## Media (prompt and caption only — not generated here)

**Prompt:** flat vector diagram, no text-heavy panels, no people, no logos. A single page card enters a three-gate arch: gate 1 labelled with a tick "opened?", gate 2 "saved page exists?", gate 3 "has Saved: date?". Passing all three, the card exits as a row with a filled date and a short finding line; failing any gate, it exits as a row with the date and finding boxes visibly empty and a small "not-opened" tag. Two colours only, generous whitespace, 16:9.

**Caption:** A bee-scouts row is "read" only when the saved page was opened and carries a `Saved:` date; everything else is not-opened, with blank facts.

## Could not confirm

- The public URL: the dataset does not exist until the publish play uploads it. It will be at `https://huggingface.co/datasets/hivepunk-1071-f79faf84/bee-scouts-recheck` (name chosen by me, unconfirmed live).
- The discussion post: drafted above, not posted.
- Whether a real re-check capture exists in the repo: I did not read `tools/update-index/fixtures/rows.jsonl`, and the self-test's rows are synthetic fixtures, so I would not present them as public issue pages. That is why `data.csv` has no rows.

**Left for the owner:**
