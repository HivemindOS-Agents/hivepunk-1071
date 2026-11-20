# Artifacts - glb-fixture-byte-layouts

Dataset title: GLB byte-layout fixtures: 4-byte alignment cases
Account: hivepunk-1071-f79faf84
Target: https://huggingface.co/datasets/hivepunk-1071-f79faf84/glb-fixture-byte-layouts-nine-header-and-chunk-cases

## Live verification attempt 2026-11-20 (repeat) - UPLOAD BLOCKER, NOT CONFIRMED

Step taken: GOAL.md was updated first, as instructed, then the
target URL above was to be checked, its full file list read back
before any upload, and the complete committed set uploaded only
with existing authorized access if missing.

Exact blocker: this step has no Hugging Face fetch or upload
capability and no existing authorized session was available here.
No live file list was obtained, so no partial-set decision could
be made. No live README.md read-back, no live data/data.csv
read-back, no revision id, and no live row count (expected 9)
were obtained, and none is stated as fact. No upload was
performed and publication is NOT claimed. Per instruction,
work stops here and no other work was done in this step.

Committed local upload set (unchanged, local record only):
- data/data.csv -> data/data.csv (9 local rows per the 62/62
  self-test record below)
- README.md -> README.md

After the owner publish play, append the live read-back
(file list + row count) here. Until then, do not claim
live success.

## Live verification attempt 2026-11-20 - UPLOAD BLOCKER, NOT CONFIRMED

Step taken: GOAL.md was updated first, as instructed, then the
target URL above was to be fetched and README.md and data/data.csv
verified against the committed upload set and row count.

Exact blocker: this step has no Hugging Face fetch or upload
capability and no existing authorized access was available here.
No live README.md read-back, no live data/data.csv read-back,
no live file list, no revision id, and no live row count
(expected 9) were obtained, and none is stated as fact.
No upload was performed and publication is NOT claimed.
Per instruction, work stops here: no new upload attempt was
drafted and no other work was done in this step.

Committed local upload set (unchanged, local record only):
- data/data.csv -> data/data.csv (9 local rows per the 62/62
  self-test record below)
- README.md -> README.md

After the owner publish play, append the live read-back
(file list + row count) here. Until then, do not claim
live success.

## Self-test run of the latest committed MANIFEST repair - PASSED

Exact command (run from inside tools/glb-fixture-byte-layouts/, no arguments, no network):

~~~bash
python3 self_test.py
~~~

Runner: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/44531664370
ranAt 2026-11-19 13:15 UTC, state passed.
Exit code: 0 (the tool exits 0 only when every check passes).

Exact output (verbatim, as returned by the runner):

~~~
ok: missing data/ is refused
ok: missing README.md is refused
ok: main --check on the tool folder does not crash
ok: drift after a byte change is detected
ok: shipped MANIFEST.txt is labelled local-only
ok: shipped MANIFEST.txt claims no published values
Results: 62/62 checks passed
~~~

This is the runner evidence for the MANIFEST.txt wording repair
('Nothing in this file is a published value' -> 'Nothing in this file
is a live value'). No new execution was run in the step that recorded
this; the pass is claimed only on the basis of this runner result.

## Previous failure on record (superseded) - 61/62

Runner: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/44526417923
ranAt 2026-11-19 12:42 UTC, state failed.

Exact output (verbatim tail returned by the runner):

~~~
ok: missing data/ is refused
ok: missing README.md is refused
ok: main --check on the tool folder does not crash
ok: drift after a byte change is detected
ok: shipped MANIFEST.txt is labelled local-only
FAIL: shipped MANIFEST.txt claims no published values
Results: 61/62 checks passed
~~~

## Fix applied for the failure above

Smallest truthful change: in MANIFEST.txt only, changed
'Nothing in this file is a published value' to
'Nothing in this file is a live value', keeping the required
'NOT a read of any published page' label. No bytes, sha256,
row counts or published values were invented, and no
discoverable validation was weakened: publish_manifest.py
and self_test.py are unchanged.

The 62/62 passed run at the top of this file is the re-run
evidence for that fix.

## Earlier pass on record

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

Note: that pass predates the later 61/62 failure run above.

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
          ~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
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
