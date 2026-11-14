# glb-pad-cases

Builds the card for the Hugging Face dataset "GLB binary chunk padding and
alignment cases": the `data.csv`, the `README.md` and the read-back section.
It does no network at all and never invents a byte count or a hash.

## What it does

Two inputs, both files you have already read in the same run:

- `cases.csv` - one raw case per row: `case_id,rule,expected_bytes,source`.
- `readback.csv` - one published file per row:
  `file,sha256,line_count,status`.

It writes into an output folder:

- `data.csv` with columns `case_id,rule,expected_bytes,source,read_back`.
- `README.md` whose read-back section is generated from `readback.csv`.

Rules it enforces:

- A row whose `source` is empty, the literal `not-opened`, or a page this run
  did not fetch is emitted with `rule=not-opened` and
  `expected_bytes=not-opened`. Unopened row text is dropped, not carried.
- A `readback.csv` row counts only when `status=opened`, `sha256` is a 64-char
  lowercase hex string, and `line_count` is a positive integer. Anything else
  is written as `not-opened`. A hand-typed hash is not accepted.
- `data.csv`'s line count in the README is computed from the emitted CSV, so
  the header/row split cannot drift.

## How to run

~~~bash
cd tools/glb-pad-cases
python3 build_card.py cases.csv readback.csv OUTDIR
~~~

Exit 0 on success, 2 on a usage error or a malformed input header. Stdlib only,
no network, no subprocess.

## Self-test

~~~bash
cd tools/glb-pad-cases && python3 self_test.py
~~~

It reads `sample_cases_raw.csv` and `sample_readback.csv` from this folder, runs
the emitters in `build_card.py` directly, and compares the emitted `data.csv`
line by line and the README read-back lines against what should come out. No
network, no subprocess, nothing written outside a temp dir. It exits 0 only
when every check passes.

No pass is claimed here. HivemindOS runs the self-test and writes its result
into `SELFTEST_OUTPUT.md`; that file, not this one, is the record.

## Sample data

`sample_cases_raw.csv` has four rows: two opened, one whose source is the
literal `not-opened`, and one with an empty source. `sample_readback.csv` has
one opened file and one not-opened file, so both README branches are exercised.

## Untested

- **The live fetch after an upload.** This folder does no network request at
  all, so the two sha256 values for the real dataset files can only be filled
  by a run that actually fetches them back. Every value here that is not from
  `sample_readback.csv` is untested.
- Non-ASCII characters in source URLs (only ASCII is exercised).
- CSV files larger than the sample, and stray spaces around header names.
- It does not validate that a `source` URL is live or that a rule is true; it
  only records what you read.

## Files

| file | what it is |
|---|---|
| `build_card.py` | the builder (emits data.csv, README.md, read-back lines) |
| `self_test.py` | offline checks, run with no arguments |
| `sample_cases_raw.csv` | four sample case rows, two opened |
| `sample_readback.csv` | two sample file rows, one opened |
| `README.md` | this file |
