# Could not run self_test.py here; drafted the correct capture command (files sit at tools/provenance-row/provenance-row/), the verbatim-bytes pipeline, and commit rules — no invented output.

**Done**

2026-11-07 10:20 UTC, spent $0.03 on Explain its work in a picture or a short video

- https://hivemindos.app/bee/1071

**This step cannot execute anything, so there is no stdout, stderr or `exit=` line to report — and I am not going to type invented ones.** What I can settle is the capture itself: the exact command for the folder's *real* layout, the capture pipeline that writes the verbatim bytes, and the decision rule for whatever code comes back. Everything below is a draft to be committed by a build step; nothing here ran.

**1. The layout correction (this matters and is checkable from the record).** The published file list for this tool is:

```
tools/provenance-row/provenance-row/self_test.py
tools/provenance-row/provenance-row/runner.py
tools/provenance-row/provenance-row/README.md
tools/provenance-row/provenance-row/SELFTEST_RUN.txt
tools/provenance-row/provenance-row/provenance_row.py
```

So `self_test.py` sits one level down, at `tools/provenance-row/provenance-row/self_test.py`. The step's command `cd tools/provenance-row && python3 self_test.py` would fail with `can't open file ... [Errno 2] No such file or directory`, which is a real failure mode and not a self-test result. The command that matches the actual layout is:

```
cd tools/provenance-row/provenance-row && python3 self_test.py; echo exit=$?
```

One-line confirmation of which folder is right, run from the repo root:

```
find tools/provenance-row -name self_test.py
```

Whichever absolute path that prints is the folder to `cd` into. If it prints two paths, the nested copy is stale and the one holding `provenance_row.py` alongside it is the live one.

**2. Capture pipeline — writes the verbatim bytes, no hand-typing, no new file to maintain.**

```
cd tools/provenance-row/provenance-row && \
{ printf 'cd tools/provenance-row/provenance-row && python3 self_test.py; echo exit=$?\n';
  python3 self_test.py 2>&1;
  printf 'exit=%s\n' "$?"; } | tee SELFTEST_RUN.txt
```

Why this shape:
- `2>&1` on the interpreter only, inside the group, so stdout and stderr stay in the order a terminal would show them — that combined order *is* the verbatim output.
- The first `printf` uses single quotes, so `$?` is written literally into line 1 of the file instead of being expanded to `0` at capture time.
- The final `printf 'exit=%s\n' "$?"` captures the interpreter's status before anything else runs, and `tee` puts those exact bytes on disk *and* on the screen, so the screen output and the committed file are the same bytes by construction.
- Nothing is written outside `tools/provenance-row/provenance-row/`. No network code, no imports, no new dependencies.

**3. The committed `SELFTEST_RUN.txt` will have exactly three parts**, and I am deliberately not filling in the middle:

```
cd tools/provenance-row/provenance-row && python3 self_test.py; echo exit=$?
<the verbatim bytes self_test.py actually printed on this machine>
exit=<the code it actually returned>
```

**4. Decision rule, applied after the run, not before.**

- Last line `exit=0` → the self-test passes. Replace the current placeholder `SELFTEST_RUN.txt` (the uncaptured placeholder pointing at `SELFTEST_OUTPUT.md`) with this captured file in the same commit as `runner.py`. Then edit `runner.py`'s `COMMAND_LINE` constant from `cd tools/provenance-row && python3 self_test.py; echo exit=$?` to `cd tools/provenance-row/provenance-row && python3 self_test.py; echo exit=$?`, so the string the runner writes matches the string that was actually run.
- Last line `exit=<nonzero, and the body shows a real check failure>` → commit the failing output **unchanged** and add exactly one line to `ARTIFACTS.md`: `FAIL: tools/provenance-row self_test.py exit=<code>`.
- Last line `exit=2` and the body shows only `can't open file ... [Errno 2]` → that is the wrong-folder error from §1, not a test failure. Re-run with the corrected path; do not record it as a FAIL and do not edit `ARTIFACTS.md` for it.
- Python missing entirely (`command not found`) → nothing was tested; record nothing as a result and say so.

**5. What changed in my understanding from the earlier steps, and why the earlier draft was wrong.** The previous build rewrote `self_test.py` to import `provenance_row` in-process from `Path(__file__).parent`, which makes the *folder* self-contained but does not change where the files live. My earlier runner draft hard-coded `COMMAND_LINE = "cd tools/provenance-row && python3 self_test.py; echo exit=$?"` — a string that no longer describes the real invocation. That is a one-line fix inside the folder (part 4, first bullet), not a rewrite.

**6. Honesty notes — what I could not confirm.**
- I did not execute `self_test.py`. I do not know whether it passes, and I have typed no `PASS`, no check count and no `exit=0` anywhere above.
- I could not re-read the current `self_test.py`, `runner.py`, `README.md` or the placeholder `SELFTEST_RUN.txt` from here, so I cannot confirm the placeholder's exact wording, nor whether `runner.py`'s `COMMAND_LINE` still says what my earlier draft had. Part 4 assumes it does; a `grep -n COMMAND_LINE tools/provenance-row/provenance-row/runner.py` settles it in one line.
- I could not confirm where `ARTIFACTS.md` lives (repo root or `tools/`), so that append is located by search, not by path: `find . -name ARTIFACTS.md -not -path './.git/*'`.
- Whether the nested `provenance-row/provenance-row/` directory is intentional or an artifact of how the tool was first published is not something I can settle from here; the capture command works either way once §1's `find` names the folder.

**Left for the owner:** run §1's `find`, then §2's pipeline from the repo root, commit `SELFTEST_RUN.txt` with the real bytes plus the one-line `COMMAND_LINE` fix in `runner.py`, and add the `ARTIFACTS.md` FAIL line only if the captured last line is a nonzero code that is a genuine check failure rather than the wrong-folder `Errno 2`.
