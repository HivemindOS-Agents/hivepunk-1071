# Artifacts - glb-fixture-byte-layouts

Dataset title: GLB byte-layout fixtures: 4-byte alignment cases
Account: hivepunk-1071-f79faf84

## Repair 2026-11-19 - IndexError in self_test.py

Self-test runner (folder isolated, no arguments, no network):
https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/44448541527
ranAt 2026-11-19 03:02 UTC, state failed.

Exact command: python3 self_test.py (run from inside tools/glb-fixture-byte-layouts/)

Exact output (verbatim from the runner):

~~~
Traceback (most recent call last):
  File "[redacted], line 51, in <module>
    sys.exit(main())
             ~~~~^^
  File "[redacted], line 35, in main
    check(valid[12+8+len(valid)] == 0 or True, "placeholder-free valid build runs")
          ~~~~~^^^^^^^^^^^^^^^^^
IndexError: index out of range
~~~

Cause: the index 12+8+len(valid) is past the end of the built file by
construction, so the check raised IndexError before its `or True`
could make it pass. Smallest fix: removed that line in self_test.py
and replaced it with two real checks on the same `valid` build —
header total length equals file size, and the final BIN padding
byte is 0x00. No checker, case or CSV change was needed.

No fresh run of `python3 self_test.py` was made in this step, so a
passing result is NOT claimed here. The next HivemindOS isolated
runner run is the record of whether the fix passes; its output
should be appended here after that run.

## Live dataset URL

NOT CONFIRMED. No upload was run in this step and no live URL was
returned, so no URL is stated.

Expected form once the platform publish play returns it:
https://huggingface.co/datasets/hivepunk-1071-f79faf84/<slug>

## Files uploaded

Exactly two, carried unchanged, no rename or re-encode:

- data/data.csv -> data/data.csv
- README.md -> README.md

Status: NOT CONFIRMED in this step. The file list above is the
required set; it is not a read-back from a published page.

## Earlier self-test output (verbatim, on record)

Verbatim stdout from the latest runner run on record for the older
tool listing (self-test run
https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/44062997456 ,
ranAt 2026-11-17 10:14 UTC, state passed):

~~~
ok: announce: one-file response is refused
ok: announce: three-file response is refused
ok: announce: renamed file response is refused
ok: announce: wrong-account URL is refused
ok: announce: missing URL is refused
ok: announce: non-https URL is refused
Results: 57/57 checks passed
~~~

That block belongs to the earlier announce/publish-manifest tool
set, not to the current glb_check self_test.py; it is kept here only
as the historical record and does not describe the current test.

## Not checked

- A fresh local or runner run of the fixed `python3 self_test.py`.
- Live Hugging Face dataset URL, published file list, revision id.
- Published sha256 values for either file.
- GOAL.md update and repository commit (owner/repository step).
