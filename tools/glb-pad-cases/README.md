# glb-pad-cases

Builds the card for the dataset "GLB binary chunk padding and alignment
cases": the `data.csv`, the `README.md` card and its read-back section. It
does no network at all and never invents a byte count, a hash or a URL.

## What it does

Two inputs, both files you have already read in the same run:

- `cases.csv`: one raw case per row: `case_id,rule,expected_bytes,source`.
- `readback.csv`: one published file per row:
  `file,sha256,line_count,status`.

It writes into an output folder:

- `data.csv` with columns `case_id,rule,expected_bytes,source,read_back`.
- `README.md` card whose read-back section is generated from `readback.csv`.

Rules it enforces:

- A row whose `source` is empty or the literal `not-opened` is emitted with
  `rule=not-opened` and `expected_bytes=not-opened`. Unopened row text is
  dropped, not carried.
- A `readback.csv` row counts only when `status=opened`, `sha256` is a 64-char
  lowercase hex string and `line_count` is a positive integer. Anything else
  is written as `not-opened`. A hand-typed hash is not accepted.
- `data.csv`'s line count in the card is computed from the emitted CSV, so
  the header/row split cannot drift, and an input line count cannot override
  it.
- The card never states a dataset URL and never states a hash that was not
  read back.

## How to run

~~~bash
cd tools/glb-pad-cases
python3 build_card.py cases.csv readback.csv OUTDIR
~~~

Exit 0 on success, 2 on a usage error or a malformed input header. Stdlib
only, no network, no subprocess.

## Self-test

~~~bash
cd tools/glb-pad-cases && python3 self_test.py
~~~

It builds its own fixtures in a temp dir, runs the emitters in `build_card.py`
directly, and compares the emitted `data.csv` cells and card lines with
explicit expected values. That includes: the alignment expression survives as
text and is never evaluated; an unopened or empty-source row is not-opened in
every field with its decoy text dropped; a wrong input line count cannot
override the emitted one; a non-hex "hash" is refused; and the card contains
no dataset URL and no long hex string when no read-back was supplied. It also
parses the shipped `sample_cases_raw.csv` and `sample_readback.csv`. No
network, no subprocess, nothing written outside a temp dir. It exits 0 only
when every check passes.

On quoting: the raw fixture writes the four-byte expression `(len+3) AND NOT 3`
as a quoted CSV field, and the emitted cell comes back byte-identical; the
test compares parsed cells, not substrings across quoting.

No pass is claimed here. HivemindOS runs the self-test and writes its result
into `SELFTEST_OUTPUT.md`; that file, not this one, is the record.

## Sample data

`sample_cases_raw.csv` has four rows: two opened, one whose source is the
literal `not-opened`, one with an empty source. `sample_readback.csv` has one
opened file and one not-opened file, so both read-back branches are exercised.
The sample is synthetic and its sha256 value is a made-up placeholder used
only to exercise the opened branch.

## Upload set (owner)

Exactly two files, unchanged:

| dataset name | local source |
|---|---|
| `data.csv` | `out/data.csv` |
| `README.md` | `out/README.md` (the card, **not** this file) |

No hash, row count or dataset URL for the live dataset is stated anywhere in
this folder, because none was read from a publish run.

## Untested

- **The live fetch after an upload.** This folder does no network work, so
the sha256 values for real published files can only come from a run that
fetches them back. Every value not from the sample is untested.
- The publish itself: no upload was run from this step, so the live dataset
  URL, its file list, its sha256 values and its row count are unconfirmed.
- Non-ASCII characters in `source` (only ASCII is exercised).
- CSV files much larger than the sample, and header names with stray spaces.
- It does not check that a `source` page is live or that a rule is true; it
  records what you read.
- `out/data.csv` and `out/README.md` shipped in this folder were hand-shaped
  to match the emitter's output for the 10 real rows; the emitter was run on
  the 4-row sample only.

## Files

| file | what it is |
|---|---|
| `build_card.py` | the builder (emits data.csv, README.md, read-back lines) |
| `self_test.py` | offline checks, run with no arguments |
| `sample_cases_raw.csv` | four sample case rows, two opened |
| `sample_readback.csv` | two sample file rows, one opened |
| `out/data.csv` | the 10-row data file for upload |
| `out/README.md` | the card for upload |
| `README.md` | this file |
