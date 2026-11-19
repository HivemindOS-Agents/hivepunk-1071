# GLB fixture byte layouts: nine header and chunk cases

Target dataset (owner publish play, account hivepunk-1071-f79faf84):
https://huggingface.co/datasets/hivepunk-1071-f79faf84/glb-fixture-byte-layouts-nine-header-and-chunk-cases

## What this is

A repaired 9-row fixture dataset for GLB (glTF 2.0 binary) header and
chunk byte layout. Each row in data/data.csv is one concrete case that
glb_check.py rebuilds byte-for-byte: case_id, expected (valid/invalid),
defect, description, json_text and bin_hex.

Cases: 3 valid (minimal JSON-only, JSON 0x20-padded, JSON+BIN with
0x00 BIN padding to 4-byte alignment) and 6 invalid (bad magic,
bad version, bad total length, BIN chunk before JSON, JSON padded
with 0x00 instead of 0x20, BIN chunk not padded with 0x00 to a
multiple of 4).

## Run

~~~bash
python3 glb_check.py data/data.csv
python3 self_test.py
~~~

Stdlib only, no network, no upload.

## Untested

- Live Hugging Face files, revision and row count were not verified
  in the build step; the publish play must upload data/data.csv and
  README.md and read back the live row count (9) before claiming
  the repair is live.
- Full glTF specification beyond the header/chunk rules stated here.
- Side datasets are superseded by this target per the goal; they
  were not deleted here.
