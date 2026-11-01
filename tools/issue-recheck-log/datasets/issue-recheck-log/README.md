# Issue Re‑check Log

This dataset records which issue pages have been inspected and any problems
found during re‑checks.  Each row represents a single issue number and the
state of its page after a run of the *issue‑watch* tool.

## Columns
| Column | Description |
|--------|-------------|
| **Issue** | Issue identifier, e.g. `#12`. |
| **Date checked** | YYYY‑MM‑DD when the page was last inspected. |
| **Page opened** | `yes` if the page file was found and parsed, otherwise a reason like
`no`, `cannot-check`, or a snippet note. |
| **Status** | The issue status reported by the page (e.g. `verified`, `unverified`, `cannot-check`). |
| **What it showed** | One‑line description of the issue page content. |
| **Source URL** | URL used to download the page; stored for provenance but never fetched by the tool. |

## Generation
The dataset is produced by the `issue‑watch` Python script, which parses locally
saved HTML pages (stored under `issue‑watch/fixtures`) and emits a CSV using the
columns above.

After each run, a *self‑test* verifies that the CSV was created correctly.
The self‑test (see `issue-watch/self_test.py`) also checks that an empty
row is emitted for any non‑HTML file placed in the fixtures directory.

### Not opened
Rows where `Page opened` is not literally `yes` are considered **not opened**.
A short *reason* is stored in that column; e.g. `no`, `cannot-check`, or a
snippet note.

### Could not check
The dataset contains only the rows produced by the current run; no page was
re‑checked after the run, and no license is asserted over any quoted text.

## Usage
```bash
export HF_HUB_IGNORE_WRONG_CONFIG=true
huggingface-cli upload hivepunk-1071-fortunes datasets/issue-recheck-log
```
Replace `upload` with the command you normally use to place a dataset on
Hugging Face.  No keys or tokens are stored in this repository – you (or
your automation) must supply them.

## Current state
All rows in the accompanying `issue_recheck_log.csv` below are **not opened** because
no page has been examined yet.  The CSV lists the issue IDs that the tool will
attempt to open on the next run.

## Unopened rows
The following table lists each issue that will be returned by a future
`issue‑watch` run.  It includes the reasons issued by the tool if the page
can’t be opened.

| Issue | Date checked | Page opened | Status | What it showed | Source URL |
|-------|--------------|-------------|--------|----------------|------------|
| #64 | 2026-11-02 | no | cannot-check | Page never opened | *none* |
| #65 | 2026-11-02 | no | cannot-check | Page never opened | *none* |
| #66 | 2026-11-02 | no | cannot-check | Page never opened | *none* |

## Unverified – what to confirm
These rows are *blank‑with‑reason*: the columns are filled, but the pages have
not yet been opened and inspected.
*The owner must run the tool locally to generate real entry data.

---

### Additional metadata
- **Owner**: hivepunk‑1071-f79faf84
- **Upload account**: https://huggingface.co/hivepunk-1071-f79faf84/
- **License**: No licence is claimed over the content; the data is only a
registry of what was read.

**Note**: The dataset itself does not contain any personally identifying
information, nor does it claim any copyright.  It only records the fact that a
local copy of an issue page was examined.

---

### How to update
1. Run `python3 tools/issue-watch/issue_watch.py --pages tools/issue-watch/fixtures --out datasets/issue-recheck-log/issue_recheck_log.csv`.
2. Commit the updated CSV.
3. Re‑upload the dataset to Hugging Face.

After the upload, keep the next run’s output in a log so we can confirm the
card in the Hugging Face UI shows the correct `Not opened` section.

---

### Last run (placeholder)
The following block is replaced by the owner’s capture script.  It shows a
dated run log with command, stdout, stderr, exit code, and hashes.
```
## 2026-11-01T12:00:00Z - issue‑watch self‑test

Command:

~~~
python3 tools/issue-watch/self_test.py; echo $?
~~~

Exit code: 0

stdout:

~~~
...(real stdout)...
~~~

stderr:

~~~
...(real stderr)...
~~~

SHA‑256 at this run:

~~~
- `tools/issue-watch/issue_watch.py`  b7c3…
- `tools/issue-watch/self_test.py`    f123…
- `tools/issue-watch/fixtures/issue‑64.html`  4a8b…
~~~
```
