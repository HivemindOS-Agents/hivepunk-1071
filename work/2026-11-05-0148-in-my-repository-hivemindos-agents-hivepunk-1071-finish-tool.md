# In my repository HivemindOS-Agents/hivepunk-1071, finish tools/update-index/ by committing exactly the four files already written in my last note and nothing else: index_build.py (stdlib-only…

**Partial: it ran out of room, its next step can carry on**

2026-11-05 01:48 UTC, spent $0.04 on Explain its work in a picture or a short video

- https://hivemindos.app/bee/1071

**`tools/update-index/` — the four paths for the commit, and no other file**

Draft for the build step, which is what commits files. Nothing here is committed, and no self-test has been run: only HivemindOS runs one.

Paths in this commit:
- `tools/update-index/index_build.py` — unchanged, written whole in my last note; its output contract is pinned below so the other three files match it exactly.
- `tools/update-index/README.md` — full text below.
- `tools/update-index/self_test.py` — full text below (replaces the old JSONL self-test at that path).
- `tools/update-index/example/` — the three notes and `example/index.md` below.

**index_build.py output contract (must not drift)**

```
# Index of saved agent notes

One line per saved note: path | first heading | saved date.
The saved date is empty when the note carries no `Saved: YYYY-MM-DD` line.

- <path relative to the notes folder> | <first heading> | <saved date>
```

A note with no readable `Saved:` line ends its row with a bare `|` (the empty date slot). A note with no heading still gets its row. Rows sorted by path, LF endings, file ends with a newline, the output file skipped as an input.

**README.md**

```markdown
# update-index

`index_build.py` reads a folder of saved agent-note `.md` files and writes one `index.md`
for that folder: one row per note, sorted by path, holding the note's path, its first
Markdown heading, and its saved date when the note carries a `Saved: YYYY-MM-DD` line.
The date slot is left empty when it does not. A note with no heading still gets its row.

Standard library only. No network, no configuration, no state kept between runs, and the
notes themselves are never modified. The output file is skipped as an input, so a second
run on the same folder gives byte-identical output.

## How to run it

    python3 tools/update-index/index_build.py notes/

Reads every `*.md` under `notes/` recursively and writes `notes/index.md`, printing how
many notes were indexed and how many had no heading. To write the index somewhere else:

    python3 tools/update-index/index_build.py notes/ -o work/notes-index.md

One row per note, LF endings, and the file ends with a newline:

    - <path relative to the notes folder> | <first heading> | <saved date or empty>

A pipe inside a path or heading is written with a backslash before it. Only `#`-style
headings are read, and a heading inside a fenced code block is skipped.

`example/notes/` holds three tiny notes, and `example/index.md` is the index they produce:

    python3 tools/update-index/index_build.py example/notes -o example/index.md

## Self-test

    python3 tools/update-index/self_test.py

Builds a throwaway fixture folder under the system temp dir and runs the builder on it,
checking eleven behaviours: exit code 0; one row per `.md` file; rows sorted by path; a
saved date shown; an empty date slot when there is no readable `Saved:` line; a row still
written for a note with no heading; a pipe in a heading escaped; the output file not
indexed as a row; non-`.md` files ignored; a second run byte-identical; a non-zero exit
when the folder does not exist. It prints `ok: all 11 index_build checks passed` and exits
0 only when every check passes; otherwise it names the failed checks and exits 1.

## What is untested

Only `self_test.py` exercises the builder, and **it has not been run**: its eleven checks
are unproven, and `example/index.md` is written from the rules above rather than captured
from a run. No notes folder outside the fixture has been indexed. HivemindOS runs the
self-test after the commit; `tools/update-index/` counts as finished only once it passes.
```

**self_test.py**

```python
#!/usr/bin/env python3
'''Self-test for index_build.py. Standard library only.

Builds a throwaway fixture folder under the system temp dir, runs index_build.py
on it, and checks the eleven behaviours the README lists. Prints one line per
check, then 'ok: all 11 index_build checks passed' and exits 0 only when every
check passed; otherwise it names the failed checks and exits 1.
'''
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
BUILDER = HERE / 'index_build.py'
PIPE = chr(92) + '|'          # an escaped pipe, as index_build.py writes it

FIXTURE = {
    'a.md': '# Alpha note\n\nSaved: 2026-10-

[Cut off here: it ran out of room. Its next step can pick up from this point.]
