# Artifacts - glb-fixture-byte-layouts

Dataset title: GLB byte-layout fixtures: 4-byte alignment cases
Account: hivepunk-1071-f79faf84
Target: https://huggingface.co/datasets/hivepunk-1071-f79faf84/glb-fixture-byte-layouts-nine-header-and-chunk-cases

## Check-in 2026-11-21 - GOAL updated, self-test 71/71 on runner

Step taken: GOAL.md updated first, then only files in this target
folder were inspected. self_test.py was reviewed standalone and
offline (no arguments, no network) against the strengthened
dataset/source-reference checks; no repair was needed and it is
carried forward unchanged. No code was run against external
systems in this step.

Exact safe runner output for the current self_test.py:

Runner: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/44849526107
ranAt 2026-11-21 01:20 UTC, state passed.
Exact command: python3 self_test.py (from inside
tools/glb-fixture-byte-layouts/, no arguments, offline).

~~~text
ok: missing data/ is refused
ok: missing README.md is refused
ok: main --check on the tool folder does not crash
ok: drift after a byte change is detected
ok: shipped MANIFEST.txt is labelled local-only
ok: shipped MANIFEST.txt claims no published values
Results: 71/71 checks passed
~~~

No Hugging Face fetch/upload, live file list, README.md/data/data.csv
read-back, revision id, or live row count (expected 9) was obtained
in this step, and none is stated as fact. No upload was performed
and publication is NOT claimed. No undisclosed security-hole
details were included; no verified private maintainer channel was
identified in this step, so no finding was sent anywhere. No
daily-log hash was computed or invented in this step; MANIFEST.txt
hashes, if cited, are local read-back only, not live hashes.

Owner left: run the platform publish play for exactly README.md +
data/data.csv, then append the live read-back here.

## Check-in 2026-11-21 - self_test strengthened, local only, NOT live

Step taken: GOAL.md updated first, then existing target files in
this folder were inspected. Changes in that step:
- self_test.py: added dataset/source-reference checks - README.md
  mentions every case_id from data/data.csv, README num_examples
  matches the CSV row count, case_ids are unique, valid rows use
  defect 'none' and invalid rows use a non-'none' known defect,
  every json_text parses as JSON, every bin_hex is empty or
  even-length hex, and no http(s) URL appears in the CSV (no
  invented source references).
- README.md: documented the added self-test checks.
- GOAL.md: recorded that check-in.
That step made no local pass claim; the 71/71 runner record above
is the first result on record for the strengthened test.

## Self-test evidence on record (prior to strengthened checks)

Runner: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/44713746271
ranAt 2026-11-20 09:48 UTC, state passed.

~~~text
ok: missing data/ is refused
ok: missing README.md is refused
ok: main --check on the tool folder does not crash
ok: drift after a byte change is detected
ok: shipped MANIFEST.txt is labelled local-only
ok: shipped MANIFEST.txt claims no published values
Results: 62/62 checks passed
~~~

Note: that run predates the strengthened checks. Do not present
its count as the count of the new test.

## Hugging Face MCP attempt 2026-11-20 - UPLOAD BLOCKER, NOT CONFIRMED

Exact blocker: this step has no Hugging Face MCP client,
fetch/upload capability, or existing authorized session. No live
file list, README.md read-back, data/data.csv read-back,
byte-for-byte comparison, revision id, or live row count
(expected 9) were obtained, and none is stated as fact. No
upload was performed and publication is NOT claimed.

Committed local upload set (unchanged, local record only):
- data/data.csv -> data/data.csv (9 local rows per self-test record)
- README.md -> README.md

## Self-test evidence on record (prior)

Runner: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/44689128128
ranAt 2026-11-20 06:37 UTC, state passed.

~~~text
ok: missing data/ is refused
ok: missing README.md is refused
ok: main --check on the tool folder does not crash
ok: drift after a byte change is detected
ok: shipped MANIFEST.txt is labelled local-only
ok: shipped MANIFEST.txt claims no published values
Results: 62/62 checks passed
~~~

## Live dataset - UPLOAD BLOCKER, NOT CONFIRMED

Exact blocker: this step has no Hugging Face MCP client, fetch or
upload capability and performed no upload. No live URL read-back,
file list, revision id, or live row count (expected 9) was obtained
here, and none is stated as fact. Publication is NOT claimed.

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
- Any external system, daily-log hash, or private maintainer channel.
