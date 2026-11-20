---
license: mit
dataset_info:
  features:
  - name: case_id
    dtype: string
  - name: expected
    dtype: string
  - name: defect
    dtype: string
  - name: description
    dtype: string
  - name: json_text
    dtype: string
  - name: bin_hex
    dtype: string
  splits:
  - name: train
    num_examples: 9
configs:
- config_name: default
  data_files: data/data.csv
---

# GLB byte-layout fixtures: 4-byte alignment cases

Nine small GLB header/chunk byte-layout cases for download and
checking. Each row of `data/data.csv` rebuilds one GLB byte string
with `glb_check.py`: 12-byte header (magic 0x46546C67, version 2,
total length equal to file size), then a JSON chunk first and an
optional BIN chunk second, each chunk length a multiple of 4, JSON
padded with 0x20 spaces and BIN padded with 0x00.

## Cases

Valid (3): `valid-minimal`, `valid-json-padded`, `valid-with-bin`.

Invalid (6): `invalid-bad-magic` (bad-magic), `invalid-bad-version`
(bad-version), `invalid-bad-total-length` (bad-total-length),
`invalid-chunk-order` (BIN before JSON), `invalid-json-bad-padding`
(JSON padded with 0x00 instead of 0x20), `invalid-bin-unpadded`
(BIN missing 0x00 padding to 4-byte alignment).

Columns: `case_id`, `expected` (valid/invalid), `defect`,
`description`, `json_text`, `bin_hex` (empty when no BIN chunk).

## Use

Rebuild and check locally with `glb_check.py` against
`data/data.csv`: valid rows must be accepted and invalid rows
must be rejected with a reason. This card describes the local
committed set only; it is not a read-back of any live page and
claims no live revision, hash, or published row count.
