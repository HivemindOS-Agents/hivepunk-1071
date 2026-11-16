# glb-fixture-byte-layouts

The artifact folder for the Hugging Face dataset *GLB byte-layout
fixtures: 4-byte alignment cases*. It holds the two files that the
platform's own "Publish a small open dataset" play uploads, plus a
manifest tool, its offline self-test and the publish packet.

## What gets uploaded

Exactly two entries, read from this folder as raw bytes:

| source here | path in the dataset repo |
|---|---|
| `data/data.csv` | `data/data.csv` |
| `README.md` | `README.md` |

No rename, no added file, no re-encoding, no line-ending change.
`publish_manifest.py`, `self_test.py`, `MANIFEST.txt`, `HOWTO.md` and
`PUBLISH_PACKET.md` are **not** in the upload set.

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

Offline, no arguments: it now includes an explicit exact-2-entry fixture
(data/data.csv + README.md) as a regression for the earlier named failure
where a >=3-entry demand failed a correct 2-entry set, plus the original
3-entry fixture, hash/size, traversal, stray-file and missing-file checks.
No pass is claimed here; HivemindOS runs it and writes SELFTEST_OUTPUT.md.

## What is untested

- The publish itself: live dataset URL, published file list and published
  hashes are unconfirmed until the platform publish play returns them.
- MANIFEST.txt may need regeneration with --write before --check passes.
- Non-ASCII names, symlinks, very large files are not exercised.
- Rule truth against the GLB spec is not checked; only bytes are moved.
