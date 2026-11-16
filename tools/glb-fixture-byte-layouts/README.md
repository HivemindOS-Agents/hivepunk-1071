# GLB binary chunk padding and alignment cases

One row per GLB padding or alignment case, with the byte expression a
parser has to get right and the page the row was read from.

## Columns

- `case_id` - short name of the case.
- `rule` - the padding or alignment rule, in words.
- `expected_bytes` - the byte count or byte expression; a
  four-byte-alignment expression is kept as text, not evaluated.
- `source` - the page identifier the row was read from.
- `read_back` - `opened` when the source page was fetched in the run,
  else `not-opened`.

## What is in data/data.csv

10 case rows plus a header, 11 lines in all. They cover the fixed fields
of the 12-byte GLB header (magic, version, total length), the 8-byte chunk
header (4-byte length, 4-byte type), the two chunk type constants
(`0x4E4F534A` for JSON, `0x004E4942` for BIN), and the one rule that makes
the format byte-aligned: chunk data is padded to a 4-byte boundary, written
as the expression `(len+3) AND NOT 3` and kept as text so no reader has to
evaluate it.

Every row cites the GLB 2.0 spec section it was read from. A row whose
page was not opened carries `not-opened` in every field; no byte count is
invented.

## Read-back

Nothing in this folder was fetched back from a host, so both files are
recorded as not-opened:

- `data/data.csv` - not-opened (sha256: not-opened; line count: not-opened)
- `README.md` - not-opened (sha256: not-opened; line count: not-opened)

data/data.csv has 11 lines (1 header + 10 rows).

## Not checked

No self-test pass is claimed in this card. No dataset URL is stated here:
the page that hosts these files is named only by whatever page carried
them. Any sha256 or line count marked not-opened was not read in the run
that produced this file.

## Licence

No licence is claimed. Rows are short factual notes about byte layouts.
