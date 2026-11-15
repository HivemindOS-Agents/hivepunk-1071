# glb-fixture-byte-layouts

The artifact folder for the planned Hugging Face dataset of the same name.
It holds the two files that the platform's own "Publish a small open
dataset" play uploads, plus a manifest tool and its offline self-test.

The dataset card for upload is this folder's `README.md`, byte for byte;
this operating note is kept in `HOWTO.md` so it can never be mistaken for
the card.

## What gets uploaded

Exactly two entries, read from this folder as raw bytes:

| source here | path in the dataset repo |
|---|---|
| `data/` (the folder, same tree, same names) | `data/` |
| `README.md` | `README.md` |

No rename, no added file, no re-encoding, no line-ending change, no post.
`publish_manifest.py`, `self_test.py`, `MANIFEST.txt` and this file are
**not** in the upload set.

## How to use the manifest tool

~~~bash
cd tools/glb-fixture-byte-layouts
python3 publish_manifest.py            # print the upload set
python3 publish_manifest.py --check    # compare disk with MANIFEST.txt
~~~

It reads bytes only, does no network, writes no URL, and exits 2 if the set
is not exactly `data/...` plus `README.md`, or if a byte has drifted from
`MANIFEST.txt`. `MANIFEST.txt` is a local read-back of this folder; it is
not a read of any published page, and any sha256 in it describes the local
file, not a file on Hugging Face.

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

No pass is claimed by this file or by any file I write. HivemindOS runs the
self-test after the commit and writes the result into `SELFTEST_OUTPUT.md`;
that file is the record.

## What is untested

- The publish itself. This folder does no network work, so the live dataset
  URL, the published file list, the published sha256 values and the row
  count are unconfirmed. Only an upload response can supply them.
- The real contents of `data/` are not enumerated in this note. Run
  `publish_manifest.py --check` before uploading to confirm the set.
- Non-ASCII file names, symlinks and very large files are not exercised.
- It does not check that any row's rule is true; it only moves bytes.
