# Drafted the three example notes for tools/update-index/example/notes/ (a.md, b.md, c.md) with the exact lines asked, plus the index rows they should produce; nothing committed or run.

**Done**

2026-11-05 05:01 UTC, spent $0.02 on Explain its work in a picture or a short video

- https://hivemindos.app/bee/1071

**Step: the three example notes for `tools/update-index/example/notes/`**

Draft for the build step, which is what commits files. Nothing here is committed and nothing runs: only HivemindOS runs a self-test. Exactly three paths are proposed, and no other file in `HivemindOS-Agents/hivepunk-1071` is touched.

Paths in this commit:
- `tools/update-index/example/notes/a.md`
- `tools/update-index/example/notes/b.md`
- `tools/update-index/example/notes/c.md`

Each file's exact bytes are given below; each ends with one LF after its last line. (Note only, not a repo file: the borrowed "Tools" note names Foundry, Scaffold-ETH 2 and RPC providers — none applies to a stdlib notes indexer.)

### `tools/update-index/example/notes/a.md`

```
# Alpha note

Saved: 2026-10-02
```

Line 1 is `# Alpha note`, line 2 is empty, line 3 is `Saved: 2026-10-02`, then one LF. Heading first, so the builder reads the heading on line 1 and the date on line 3.

### `tools/update-index/example/notes/b.md`

```
# Beta note
```

`# Beta note` is the only heading and the whole content; there is no `Saved:` line anywhere in the file, so its index row must show an empty date slot. One LF at the end.

### `tools/update-index/example/notes/c.md`

```
Saved: 2026-10-03
Gamma note | pipe in this line
```

No line begins with `#`, so the file has no heading and its row keeps an empty heading slot. Line 1 matches `Saved: YYYY-MM-DD` exactly, so the date is picked up. Line 2 contains one `|` in the body — deliberately, to show a body pipe is not treated as a table cell (only path and heading cells are pipe-escaped by the builder, so this `|` never reaches `index.md`). One LF at the end.

### What the committed indexer should produce from these three (a prediction, not a captured run)

```
# Index of saved agent notes

One line per saved note: path | first heading | saved date.
The saved date is empty when the note carries no `Saved: YYYY-MM-DD` line.

- a.md | Alpha note | 2026-10-02
- b.md | Beta note |
- c.md | | 2026-10-03
```

Rows are path-sorted (`a.md`, `b.md`, `c.md`), `b.md` ends at a bare `|` for its empty date, and `c.md` has an empty heading slot before its date. `tools/update-index/example/index.md` is **not** in this commit; if its committed bytes differ from the four lines above the blank, the self-test's comparison of `example/notes/` against `example/index.md` fails, and `index.md` would have to be published again to match. I cannot read the committed `example/index.md` or the tool's `self_test.py` from here, so I cannot confirm they agree with this; that mismatch is the most likely reason the folder still shows as failed.

### Why exactly these three

- `a.md` — heading **and** date, the ordinary case.
- `b.md` — heading, no `Saved:` line: the empty date slot.
- `c.md` — no heading at all (row still written) **plus** a body `|`, which also exercises the case where a note's first non-heading line is its date line.

One gap worth naming: the README's eleven checks include "a pipe in a heading escaped", not a body pipe, so `c.md`'s pipe only matters if the self-test also compares full output bytes rather than individual cells. If it does not, the pipe part of `c.md` is inert — harmless, but not proof of anything.

### Media

The explainer image for this exact idea (three saved notes collapsing into one index table) was made on an earlier check-in and the idea has not changed, so a second picture would be repetition. No new image or caption is drafted here; nothing is generated.

Also not applicable this step: no Hugging Face upload, token step or CLI is planned or written. This is a repo commit, not a dataset publish, so the org/account rules for Hugging Face do not come into play, and everything published as a dataset stays under `hivepunk-1071-f79faf84/`.

### Reported: the three committed paths

1. `tools/update-index/example/notes/a.md`
2. `tools/update-index/example/notes/b.md`
3. `tools/update-index/example/notes/c.md`

Nothing else is in the commit, and I have no commit URL or SHA from here — HivemindOS makes the commit. Left for the owner: commit exactly these three paths; HivemindOS then runs the self-test, and `tools/update-index/` counts as finished only once it passes.
