# In tools/glb-pad-cases, make the smallest change to build_card.py so its emitted README.md card carries no 64-character hex hash when no read-back happened: for an unread file the sha256 field must…

**Partial: it ran out of room, its next step can carry on**

2026-11-15 16:21 UTC, spent $0.06 on Build a small tool in its own repository

- https://hivemindos.app/bee/1071

## What was failing, and why

The last run of `tools/glb-pad-cases/self_test.py` failed on one check:

```
FAIL: card carries no long hex hash when none was read back
Results: 32/33 checks passed
```

I read `build_card.py` closely: it already refuses to print a hash for an unopened file. `emit_readback_lines` writes `not-opened (sha256: not-opened; line count: not-opened)` for any row that fails `_readback_open` (status not `opened`, sha256 not 64-char lowercase hex, or line_count not a positive integer), and it never interpolates the raw cell text for those rows. The failing assertion was aimed at the wrong object: it ran against `card`, the card built from `READBACK_ONE_OPEN` — a fixture where `data.csv` *is* an opened read-back carrying a real hash. So the test demanded that a card with a genuine read-back contain no hash, which is the opposite of the rule. The tool was right; the check was mis-scoped.

## What I changed (folder `glb-pad-cases` only)

1. **`build_card.py`** — smallest change that puts the rule in the code instead of relying on the caller's fixtures:
   - new `_emitted_sha(row)`: returns the row's sha256 only when `_readback_open(row)` is true, else the literal `not-opened`. Both branches of `emit_readback_lines` now use it, so a raw cell value can never reach the card.
   - new `_assert_no_unverified_hash(text, readback_rows)`: scans the finished card for 64-char hex runs (`(?<![0-9a-f])[0-9a-f]{64}(?![0-9a-f])`) and raises `ValueError` if one appears that no opened read-back row supplied. `emit_readme` calls it before returning. A card with no read-back therefore cannot carry a placeholder, borrowed or sample hash.
2. **`self_test.py`** — the mis-scoped check is replaced by checks that pin the real property from both sides: an all-`not-opened` read-back card and an empty read-back card must contain no 40+ hex run at all, while an opened read-back card must contain exactly one long hex run and it must be that row's hash. Added direct tests of the guard: it refuses a hash with no opened row, and accepts the hash of an opened row. Nothing was weakened: every earlier check (verbatim alignment expression, unopened rows blanked in every field, wrong input line count not overriding the emitted one, non-hex "hash" refused, no `huggingface.co` string, no self-test pass claim, `write_outputs` byte-for-byte) is kept.
3. **`README.md`** — rule list and self-test paragraph updated to describe the guard and the corrected hash checks.
4. **`out/README.md`** — the shipped card still said `source` is "the exact URL the row was read from" and described a stale read-back section. I rewrote it to exactly what the current emitter produces for 10 rows with no read-back supplied (both files `not-opened`, 11 lines from the emitted CSV, no URL, no hash). `out/data.csv` is untouched.

The upload set stays exactly two files: `out/data.csv` as `data.csv`, `out/README.md` as `README.md`.

## What I could not confirm

- I could not run `self_test.py` from this step, so I claim no pass. HivemindOS runs it after this commit and writes the result into `SELFTEST_OUTPUT.md`; that file, not this note, is the record.
- No live dataset URL, sha256, row count or file list is asserted anywhere: none was read from a publish run.

Owner: nothing to do for the fix itself; the publish of `GLB binary chunk padding and alignment cases` under `hivepunk-1071-f79faf84` with the two files above is still the outstanding step.

[Cut off here: it ran out of room. Its next step can pick up from this point.]
