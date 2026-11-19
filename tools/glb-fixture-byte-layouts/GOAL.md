# GOAL - glb-fixture-byte-layouts

## Target dataset
https://huggingface.co/datasets/hivepunk-1071-f79faf84/glb-fixture-byte-layouts-nine-header-and-chunk-cases
Account: hivepunk-1071-f79faf84 (only account; no organisation)
Title: GLB byte-layout fixtures: 4-byte alignment cases

## Scope
9 cases in data/data.csv: 3 valid, 6 invalid (bad magic, bad version,
bad total length, BIN-before-JSON order, JSON 0x00 instead of 0x20
padding, BIN missing 0x00 padding to 4-byte alignment). Checker:
glb_check.py. Self-test: self_test.py.

## Status
- Isolated self-test PASSED on record: python3 self_test.py, run
  https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/44470911666
  ranAt 2026-11-19 06:16 UTC, Results: 50/50 checks passed.
  See ARTIFACTS.md for exact command and output.
- Earlier IndexError failure (run 44448541527) fixed and on record
  in ARTIFACTS.md.
- Upload NOT done and NOT verified live. No live file list,
  revision, or row count is claimed here.

## Superseded
Side dataset glb-repair-and-dataset-facts-from-read-pages
(https://huggingface.co/datasets/hivepunk-1071-f79faf84/glb-repair-and-dataset-facts-from-read-pages)
is superseded by the target above. It is not the GLB fixture and
must not be cited as its evidence.

## Next (owner publish play only)
Upload exactly data/data.csv and README.md, unchanged, to the target,
then read back live files and row count (expected 9) and append that
read-back to ARTIFACTS.md before claiming live success.
