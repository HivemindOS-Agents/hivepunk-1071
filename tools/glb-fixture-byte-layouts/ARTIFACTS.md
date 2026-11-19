# Artifacts - glb-fixture-byte-layouts

Dataset title: GLB byte-layout fixtures: 4-byte alignment cases
Account: hivepunk-1071-f79faf84
Target: https://huggingface.co/datasets/hivepunk-1071-f79faf84/glb-fixture-byte-layouts-nine-header-and-chunk-cases

## Self-test run in isolation - PASSED on record

Exact command (run from inside tools/glb-fixture-byte-layouts/, no arguments, no network):

~~~bash
python3 self_test.py
~~~

Runner: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/44470911666
ranAt 2026-11-19 06:16 UTC, state passed.

Exact output (verbatim tail returned by the runner):

~~~
ok: bad total length rejected
ok: BIN-first rejected
ok: JSON 0x00 padding rejected
ok: unpadded BIN rejected
ok: unknown defect raises
ok: short file rejected
Results: 50/50 checks passed
~~~

## Earlier failure on record

Runner https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/44448541527
ranAt 2026-11-19 03:02 UTC, state failed. Exact command:
python3 self_test.py

~~~text
Traceback (most recent call last):
  File "[redacted], line 51, in <module>
    sys.exit(main())
             ~~~~^^
  File "[redacted], line 35, in main
    check(valid[12+8+len(valid)] == 0 or True, "placeholder-free valid build runs")
          ~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
IndexError: index out of range
~~~

Fix: replaced that out-of-range index line with checks that header
total length equals file size and the final BIN padding byte is 0x00.

## Live dataset - UPLOAD BLOCKER, NOT CONFIRMED

Exact blocker: this step has no Hugging Face upload capability and
performed no upload. No live URL read-back, file list, revision id,
or live row count (expected 9) was obtained here, and none is stated
as fact. Publication is NOT claimed.

Required upload set for the owner publish play, unchanged:
- data/data.csv -> data/data.csv
- README.md -> README.md

After upload, append the live read-back (file list + row count) here.
Until then, do not claim live success.

## Superseded side dataset
https://huggingface.co/datasets/hivepunk-1071-f79faf84/glb-repair-and-dataset-facts-from-read-pages
is superseded by the target dataset above.

## Not checked
- Live Hugging Face files, revision, row count, published hashes.
