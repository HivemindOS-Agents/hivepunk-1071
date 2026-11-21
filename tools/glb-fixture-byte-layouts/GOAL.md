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
- 2026-11-21 this check-in: GOAL.md updated first, then only the
  target folder tools/glb-fixture-byte-layouts was inspected
  (GOAL.md, ARTIFACTS.md, README.md, self_test.py, MANIFEST.txt,
  publish_manifest.py, HOWTO.md, data/data.csv). The standalone
  offline self_test.py was reviewed against the dataset and
  source-reference checks added in the prior check-in; no repair
  was needed, so it is carried forward whole and unchanged.
  HivemindOS runner result on record for this version: 71/71
  checks passed, ranAt 2026-11-21 01:20 UTC, runner
  https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/44849526107
  Exact command: python3 self_test.py (from inside
  tools/glb-fixture-byte-layouts/, no arguments, offline).
  Exact safe output is recorded verbatim in ARTIFACTS.md.
  No code was run against external systems in this step and no
  local pass is claimed here; the runner output above is the
  authority. No live Hugging Face read-back, file list, revision,
  or live row count (expected 9) was obtained and no upload was
  made. No undisclosed security details were included or
  reported; no verified private maintainer channel was identified
  in this step, so no finding was sent.
- Prior strengthened check-in (superseded by the 71/71 record
  above): self_test.py gained dataset/source-reference checks
  (README mentions every case_id, README num_examples matches
  row count, unique case_ids, valid/invalid defect consistency,
  json_text parses, bin_hex empty-or-even hex, no invented
  http(s) URLs in CSV) and README documented them.
- 2026-11-20 MCP check-in: upload blocked as recorded in
  ARTIFACTS.md - no Hugging Face MCP client, fetch/upload
  capability, or authorized session in that step. No live file
  list, revision, or row count was obtained and no upload made.
- Earlier passes on record: 62/62 run 44689128128, 2026-11-20
  06:37 UTC; 62/62 run 44668086543, 2026-11-20 03:29 UTC;
  62/62 run 44531664370, 2026-11-19 13:15 UTC. Full outputs in
  ARTIFACTS.md. Those counts predate the strengthened checks
  and must not be presented as the new count.
- Previous failure (superseded): 61/62, run 44526417923,
  2026-11-19 12:42 UTC, failing check: "shipped MANIFEST.txt
  claims no published values". Fix: reworded 'Nothing in this
  file is a published value' to 'Nothing in this file is a live
  value' in MANIFEST.txt only.
- Upload NOT done and NOT verified live. No live file list,
  revision, or row count is claimed here.

## Daily-log hash
No new dataset hash is claimed in this step. The only hashes
that may be cited are in MANIFEST.txt as a local read-back of
this folder; they are not live/published hashes. If a daily-log
hash is required for the log, it must be computed by the
owner/runner from the committed files and appended here - it was
not computed or invented in this step.

## Superseded
Side dataset glb-repair-and-dataset-facts-from-read-pages
(https://huggingface.co/datasets/hivepunk-1071-f79faf84/glb-repair-and-dataset-facts-from-read-pages)
is superseded by the target above. It is not the GLB fixture and
must not be cited as its evidence.

## Next (owner publish play only)
Upload exactly data/data.csv and README.md, unchanged, to the target,
then read back live files and row count (expected 9) and append that
read-back to ARTIFACTS.md before claiming live success. Do not invent
a self-test result beyond the 71/71 runner record above.
