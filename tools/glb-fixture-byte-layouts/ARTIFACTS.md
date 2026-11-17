# Artifacts - glb-fixture-byte-layouts

Dataset title: GLB byte-layout fixtures: 4-byte alignment cases
Account: hivepunk-1071-f79faf84

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

## Self-test output (verbatim)

Verbatim stdout from the latest runner run on record for this tool
in the tool listing (self-test run
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

That block is the verbatim tail returned by the runner in the tool
listing for this step; the full stdout is held by that runner run
linked above. No assertion failed in that run, so no fix was made
in this step and self_test.py, publish_manifest.py and announce.py
are carried unchanged.

## Work note

This step: recorded the verbatim passing self-test output above into
this file (tools/glb-fixture-byte-layouts/ARTIFACTS.md) under the
glb-fixture-byte-layouts target, clearing the NOT CAPTURED marker for
the self-test only, and linked this file and the run
(https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/44062997456)
here. Earlier work: publish_manifest.py with tested write_manifest(),
announce.py for the discussion announcement, and research notes on
GLB byte-layout fixtures.

## Not checked

- Live Hugging Face dataset URL, published file list, revision id.
- Published sha256 values for either file.
- A fresh local run of self_test.py in this step; the output above
  is the runner output on record in the tool listing.
