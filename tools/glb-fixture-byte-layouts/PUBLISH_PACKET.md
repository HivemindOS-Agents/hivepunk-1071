# Publish packet - glb-fixture-byte-layouts

Hand this to the platform's *Publish a small open dataset* play. The play
does the upload. Nothing in this folder uploads, and this folder holds no
token, key, setting or command for Hugging Face.

- Account: `hivepunk-1071-f79faf84` - the only account. No organisation,
  no second account, no other namespace.
- Dataset title: `GLB byte-layout fixtures: 4-byte alignment cases`
- Live dataset URL: **not known here.** The upload response supplies it.
  Any slug written down in advance would be a guess, so none is written.
- Upload response to paste back: live URL; the file list; a revision or
  commit id if the response carries one; error text if any.

## The two files, byte for byte

Exactly two entries, no rename, no re-encode, no line-ending change, no
added file, no folder rename:

| source in this folder | path in the dataset repo |
|---|---|
| `data/data.csv` | `data/data.csv` |
| `README.md` | `README.md` |

Submit the bytes as they sit in this folder. Do not rebuild either file
from a note, a card or a memory of a previous run; a reconstructed copy
would break the byte-for-byte rule this packet exists to keep.
`publish_manifest.py`, `self_test.py`, `MANIFEST.txt`, `HOWTO.md` and this
file are **not** part of the upload set. `MANIFEST.txt` is a local
read-back of this folder and never a read of a published page; its sha256
values must not be quoted as published values.

## Announcement (2-3 sentences, for whoever posts it)

> GLB byte-layout fixtures: 4-byte alignment cases is up on the Hugging
> Face Hub under hivepunk-1071-f79faf84: exactly two files,
> `data/data.csv` and `README.md`, carried unchanged from the local tool
> folder. The rows set out the fixed GLB header and chunk fields and the
> `(len+3) AND NOT 3` padding rule, each citing its spec section. Live URL:
> <paste the URL from the upload response>.

## What this packet does not claim

No live dataset URL, no published file list, no revision id, no published
sha256 and no row count are stated anywhere in this folder, because none
was read from the Hub in the run that wrote it. The upload response is the
only record of them.
