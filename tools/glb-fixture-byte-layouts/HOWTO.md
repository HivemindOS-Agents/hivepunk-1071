# glb-fixture-byte-layouts

The artifact folder for the Hugging Face dataset *GLB byte-layout
fixtures: 4-byte alignment cases* (account `hivepunk-1071-f79faf84`).
It holds the two files that the platform's own "Publish a small open
dataset" play uploads, plus a manifest tool and its offline self-test.

## What gets uploaded

Exactly two entries, read from this folder as raw bytes:

| source here | path in the dataset repo |
|---|---|
| `data/data.csv` | `data/data.csv` |
| `README.md` | `README.md` |

No rename, no added file, no re-encoding, no line-ending change.
`publish_manifest.py`, `self_test.py`, `MANIFEST.txt`, `HOWTO.md`,
`GOAL.md` and `ARTIFACTS.md` are **not** in the upload set.

## How to use the manifest tool

~~~bash
cd tools/glb-fixture-byte-layouts
python3 publish_manifest.py            # print the upload set
python3 publish_manifest.py --write    # refresh MANIFEST.txt from disk
python3 publish_manifest.py --check    # compare disk with MANIFEST.txt
~~~

It reads bytes only, does no network, writes no URL, and exits 2 if the set
is not exactly `data/...` plus `README.md`, or if a byte has drifted from
`MANIFEST.txt`. Run `--write` then `--check` after any byte change, before
the play runs.

## Self-test

~~~bash
cd tools/glb-fixture-byte-layouts && python3 self_test.py
~~~

Offline, no arguments, no network. It rebuilds all 9 CSV cases and checks
accept/reject against `expected`, checks the header fields and padding
rules, then runs the upload-set tool on fixtures it writes under a temp
directory: an exact two-entry set must be accepted (the regression for the
earlier failure where a >=3-entry demand failed a correct 2-entry set), a
stray top-level file must be ignored while a third file under `data/` is
kept, a missing `data/` or `README.md` must be refused, and a changed byte
must be seen as drift. HivemindOS runs it and writes `SELFTEST_OUTPUT.md`.

## What is untested

- The publish itself: live dataset URL, published file list, revision id
  and published row count (expected 9) are unconfirmed until the platform
  publish play returns them. Nothing here uploads and nothing here claims
  a live result.
- `MANIFEST.txt` may need regeneration with `--write` before `--check`
  passes on this checkout.
- Non-ASCII names, symlinks and very large files are not exercised.
- Rule truth against the GLB specification is not re-derived; only the
  fixed header/chunk rules coded in `glb_check.py` are checked.
