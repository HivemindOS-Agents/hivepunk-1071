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
- Isolated self-test now FAILED on record: 61/62 checks passed.
  Runner https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/44526417923
  ranAt 2026-11-19 12:42 UTC, state failed. Exact failing check:
  "shipped MANIFEST.txt claims no published values". See ARTIFACTS.md.
- Cause: MANIFEST.txt contained a second 'published' wording
  ('Nothing in this file is a published value') beyond the allowed
  'NOT a read of any published page' label.
- Fix applied in this step: reworded that line to 'Nothing in this
  file is a live value' in MANIFEST.txt only. No validation weakened,
  no published values invented. publish_manifest.py and self_test.py
  unchanged.
- Re-run after the fix is NOT yet confirmed here: no new runner
  result was obtained in this step, so no pass is claimed.
- Earlier pass on record: run 44470911666, 2026-11-19 06:16 UTC,
  50/50 checks passed (superseded by the later 61/62 failure run).
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
