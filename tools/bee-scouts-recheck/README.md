# bee-scouts re-check

**What it is.** One row per public issue page the bee-scouts re-check pass
looked at. Each row answers three questions about one page: was a saved copy
opened, what did the re-check conclude, and where is the evidence. It exists so
that "checked" and "not checked" can be told apart later by anyone, without
trusting a summary.

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

A row says `read` only when all three hold:

1. `saved_page_opened` is `yes`;
2. `evidence_path` names a saved page that exists;
3. that saved page carries a `Saved: YYYY-MM-DD` line.

If any one fails, the row is downgraded to `could not check` with the exact
reason, or to `not-opened`, and `checked_at`, `evidence_path` and `finding`
stay blank. **Blank means not read, never "nothing to report".** No field in
this file is ever filled from a search-result snippet, a link preview, or
another page's description of the page. Text inside a saved page that looks
like an instruction ("ignore your rules...") is data: it is kept as escaped
text or dropped, never obeyed.

## How to use it

~~~python
import pandas as pd
df = pd.read_csv("data.csv", dtype=str, keep_default_na=False)
read = df[df.read_status == "read"]
bad = df[(df.read_status != "read") & (df.finding != "")]
assert bad.empty  # a non-read row never carries a finding
~~~

`keep_default_na=False` matters: an empty `evidence_path` must stay `""`, not
become `NaN`, or the not-read rows stop being visibly blank.

Format example (illustration, **not** a captured row):

~~~csv
issue,saved_page_opened,read_status,checked_at,evidence_path,finding
example/1,yes,read,2026-11-04,pages/example-1.html,"lede says X; two links checked"
example/2,no,not-opened,,,,
~~~

## How it was made

The row file is written offline from a JSONL rows file and a folder of saved
pages: the provenance rule above is applied, and `data.csv` is those same rows
as CSV. Nothing is fetched when the row file is built, and no field comes from
a search-result snippet, a link preview, or another page's description of the
page.

## What could not be checked / current state

No live public page was opened from the environment where this file was
prepared, so `data.csv` ships with its header and **no data rows**. Rows are
added only from an opened saved page; a page that was not opened is written as
`not-opened` with blank facts and is never filled in from a snippet or
preview. No self-test result, run log or exit code is claimed here.

## Licence

None claimed. The public pages the rows point at stay under their own terms;
only this row format and these status labels are offered, with no warranty.
