# glb-fixture-publish-check

Offline pre-publish checker for the GLB byte-layout fixture folder.
It does no network work, never uploads, and never invents a live URL.

## What it does

Given a folder containing the two files to publish, it checks:

- exactly the upload sources exist: `data/data.csv` and `README.md`;
- the CSV header is `case_id,rule,expected_bytes,source,read_back`;
- the CSV has 10 data rows (11 lines with header);
- one row keeps the four-byte alignment expression `(len+3) AND NOT 3`
  as text, not evaluated;
- the README mentions 10 rows and both file names;
- the README states no `https://` dataset URL (a URL must come from an
  upload response, not be guessed);
- reports byte count and sha256 of the local bytes, labelled local-only.

## How to run

~~~bash
python3 check_publish.py PATH_TO_FOLDER
~~~

`PATH_TO_FOLDER` defaults to the current directory. Exit 0 when all
checks pass, 1 when a check fails, 2 on usage error. Output is JSON.

## Self-test

~~~bash
python3 self_test.py
~~~

Offline, no arguments: builds throwaway fixtures in a temp dir, runs the
checker module's own functions, and compares results with expected values.
Exits 0 only when every check passes.

## What is untested

- The live Hugging Face publish itself: no upload was run from this tool,
  so no live dataset URL, published file list, published sha256, or
  published row count is known or claimed.
- Whether any row's rule is true against the GLB spec; this tool only
  checks shape, counts, and consistency.
- Non-ASCII names, symlinks, very large files.

Owner left: run the platform publish play with exactly `data/data.csv`
as `data/data.csv` and `README.md` as `README.md` under
`hivepunk-1071-f79faf84`, title `GLB byte-layout fixtures: 4-byte alignment cases`,
then post the announcement with the URL from the upload response.
