# glb-fixture-byte-layouts

The artifact folder for the Hugging Face dataset *GLB byte-layout
fixtures: 4-byte alignment cases*. It holds the two files that the
platform's own "Publish a small open dataset" play uploads, plus a
manifest tool, its offline self-test and the publish packet.

The dataset card for upload is this folder's `README.md`, byte for byte;
the operating notes live in `HOWTO.md` and `PUBLISH_PACKET.md` so they can
never be mistaken for the card. The card now describes the 10 rows that
are actually in `data/data.csv` and no longer mentions `build_card.py`.

## What gets uploaded

Exactly two entries, read from this folder as raw bytes:

| source here | path in the dataset repo |
|---|---|
| `data/data.csv` | `data/data.csv` |
| `README.md` | `README.md` |

No rename, no added file, no re-encoding, no line-ending change.
`publish_manifest.py`, `self_test.py`, `MANIFEST.txt`, `HOWTO.md` and
`PUBLISH_PACKET.md` are **not** in the upload set.

## Publish packet

`PUBLISH_PACKET.md` carries the account, the title, the exact two-file map,
the fields to paste back from the upload response and the announcement
draft. This folder does not upload anything and does not know the live URL.

## How to use the manifest tool

~~~bash
cd tools/glb-fixture-byte-layouts
python3 publish_manifest.py            # print the upload set
python3 publish_manifest.py --write    # refresh MANIFEST.txt from disk
python3 publish_manifest.py --check    # compare disk with MANIFEST.txt
~~~

It reads bytes only, does no network, writes no URL, and exits 2 if the set
is not exactly `data/...` plus `README.md`, or if a byte has drifted from
`MANIFEST.txt`. `MANIFEST.txt` is a local read-back of this folder; any
sha256 in it describes the local file, not a file on Hugging Face. Run
`--write` then `--check` after any byte change, before the play runs.

## Self-test

~~~bash
cd tools/glb-fixture-byte-layouts && python3 self_test.py
~~~

Offline, no arguments: builds a throwaway artifact folder in a temp dir,
drives `publish_manifest.py`'s own functions, and checks the two-entry set,
the kept `data/` tree names, the byte counts and sha256 values against the
bytes it wrote, that a changed byte changes the hash, that a traversal or
absolute path is refused, that an extra file outside the two sources is not
uploaded, and that an empty or README-less folder fails the check.

It also reads this real folder. The upload set here is the `data/` tree
plus `README.md` - in this checkout `data/data.csv` plus `README.md`, two
entries. An earlier version of the test demanded three or more entries and
failed on a folder that was correct; it now asserts that every upload-set
source exists, that `README.md` and at least one `data/` file are present,
and that nothing outside those two sources is in the set.

No pass is claimed by this file or by any file I write. HivemindOS runs the
self-test after the commit and writes the result into `SELFTEST_OUTPUT.md`;
that file is the record.

## What is untested

- The publish itself. This folder does no network work, so the live dataset
  URL, the published file list, the published sha256 values and the row
  count are unconfirmed. Only an upload response can supply them.
- `MANIFEST.txt` is a placeholder until someone runs
  `publish_manifest.py --write`; `--check` fails until then.
- Non-ASCII file names, symlinks and very large files are not exercised.
- It does not check that any row's rule is true; it only moves bytes.
