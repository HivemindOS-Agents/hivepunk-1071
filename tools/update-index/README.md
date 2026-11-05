# update-index

`index_build.py` reads a folder of saved agent-note `.md` files and writes a single
`index.md` for that folder: one sorted line per note, holding the note's path, its first
Markdown heading, and its saved date when the note carries a `Saved: YYYY-MM-DD` line.
The date slot is left empty when it does not. A note with no heading still gets its row.

Standard library only: no network, no configuration, no state kept between runs, and the
notes themselves are never modified. The output file is skipped as an input, so a second
run on the same folder gives byte-identical output.

## How to run it

    python3 index_build.py notes/

Reads every `*.md` under `notes/` (recursively) and writes `notes/index.md`, printing how
many notes were indexed and how many had no heading. To write the index elsewhere:

    python3 index_build.py notes/ -o work/notes-index.md

One line per note, LF endings, file ends with a newline:

    - <path relative to the notes folder> | <first heading> | <saved date or empty>

A `|` inside a path or heading is written `\|`. Only `#`-style headings are read; a
heading inside a fenced code block is skipped. A `Saved:` line that does not hold a plain
`YYYY-MM-DD` date leaves the date slot empty.

## Example

`example/notes/` holds three tiny saved notes -- `a.md`, `b.md` and `c.md` -- and
`example/index.md` is the index the builder produces for them:

    # Index of saved agent notes

    One line per saved note: path | first heading | saved date.
    The saved date is empty when the note carries no `Saved: YYYY-MM-DD` line.

    - a.md | Alpha note | 2026-10-02
    - b.md | Beta note |
    - c.md |  | 2026-10-03

- `a.md` -- it has a heading and a `Saved: 2026-10-02` line, so it gets the ordinary row.
- `b.md` -- it has a heading and no `Saved:` line at all, so its date cell stays empty
  and its row ends at the bare pipe.
- `c.md` -- it has no heading at all, so its heading cell stays empty between the two
  spaces, while its `Saved: 2026-10-03` line fills the date cell. The pipe in its second
  line is body text and never reaches the index.

The rows in `example/index.md` are the same three rows shown here, in the same order and
spacing, so a reader copying this example gets the committed file.

## Self-test

    python3 self_test.py ; echo $?

Builds a throwaway fixture folder under the system temp dir, runs the builder on it and
checks: exit code 0; one row per `.md` file; rows sorted by path; a `Saved:` date shown;
an empty date slot for a note without a valid one; a row still written for a note with no
heading; pipes escaped; the output file never indexed as a row; non-`.md` files ignored; a
second run byte-identical; and a non-zero exit when the folder does not exist. It then runs
the builder on `example/notes/` and compares the result with the committed
`example/index.md` byte for byte. It exits 0 only when every check passes and prints
`ok: all index_build checks pass`.

## What is untested

Only the fixture self-test has been written. **Nothing has been run against real notes.**
No real notes folder has been indexed, on any machine, and the committed `example/index.md`
is written to match the builder's documented output for `example/notes/` rather than
captured from a run. Untested in particular: very large note folders, unusual encodings
(invalid UTF-8 is replaced with U+FFFD rather than refused), symlinked folders, and whether
any particular real note carries its `Saved:` line in the shape this tool expects.

## Notes on input

Every file it reads is data. Text inside a note that looks like an instruction ("ignore
your rules", a URL to fetch, a key to print) is indexed as plain text or skipped, never
obeyed. The tool makes no network request, runs nothing from a note, and writes only the
index file it was asked for.
