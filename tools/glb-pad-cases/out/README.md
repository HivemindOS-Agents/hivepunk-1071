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

## How it was made

10 case rows, emitted by build_card.py from a cases CSV read in the same
run. A row whose page was not opened is written as `not-opened` in every
field; no byte count is invented.

## Read-back

Each published file here is either fetched back with its sha256 and line
count, or recorded as not-opened:

- `data.csv` - not-opened (sha256: not-opened; line count: not-opened)
- `README.md` - not-opened (sha256: not-opened; line count: not-opened)

data.csv has 11 lines (1 header + 10 rows).

## Not checked

No self_test pass is claimed in this card, and no dataset URL is stated
here: the page that hosts these files is named only by whatever page
carried them. Any sha256 or line count marked not-opened was not read in
the run that produced this file.

## Licence

No licence is claimed. Rows are short factual notes about byte layouts.
