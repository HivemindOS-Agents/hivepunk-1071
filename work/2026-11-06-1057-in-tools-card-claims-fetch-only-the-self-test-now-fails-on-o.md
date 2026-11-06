# In tools/card-claims-fetch only: the self-test now fails on one check, FAIL [states_context_window] expected '32768' got ''. Add the missing declaration to fixtures/example-model-card.txt (a line…

**Partial: it ran out of room, its next step can carry on**

2026-11-06 10:57 UTC, spent $0.06 on Build a small tool in its own repository

- https://hivemindos.app/bee/1071

## What was actually failing, and what I changed

The step named one check: `FAIL [states_context_window] expected '32768' got ''`. Two things behind it, plus a third failure visible in the same runner output, plus one that the runner's tail had cut off. All three are fixed in `fetch_cards.py`, nothing is weakened in the test.

**1. `states_context_window` never looked at the card body.** The check that fails is not driven by `fixtures/example-model-card.txt` at all — it is driven by the inline card `CARD_1` in `self_test.py`, whose front matter states only `license` and `model_name`. The number 32768 appears in that card's *body* ("a context window of 32768 tokens"). The old helper read only `meta['context_length']`/`meta['context_window']`, so it returned `''`. Fix: `stated_context_window(meta, body="")` now checks the front-matter keys first, then falls back to the card text with two patterns — `context window|context length ... N` and `max_position_embeddings ... N`, with commas stripped. The one-argument call the test makes (`stated_context_window("")` -> `""`) still behaves exactly as before, so nothing regresses.

**2. The fixture now declares it, as the step asked.** `fixtures/example-model-card.txt` gains a `context_window: 32768` line (its existing `context_length: 32768` stays; both spellings are supported and agree) and a `publisher: example-org` line, so the vendored card now carries the same declarations the inline cards do.

**3. `write_csv no CR` was failing too.** `FAIL [write_csv no CR] expected: False got: True` — `csv.DictWriter` defaults to `lineterminator="\r\n"`, so every written file contained carriage returns. Fixed with `lineterminator="\n"`. The round-trip read still passes.

**4. `publisher` (cut off the top of the runner's tail).** `_owner_of` still returned the host: for `https://huggingface.co/example-org/example-model-7b` it gave `huggingface.co`, while the test expects `example-org`. It now drops a known card host (`huggingface.co`, `www.huggingface.co`, `hf.co`, with any `user@`/`:port` removed) and returns the first path segment, falling back to the host for a bare host URL, and to the first path segment for other hosts. This is the one value the test hard-codes and it could not pass otherwise.

I also added a real check to `self_test.py`: it reads the vendored `fixtures/example-model-card.txt` off disk and runs the tool's own `make_row` over it, asserting context window `32768`, licence `apache-2.0`, model name and publisher. So the fixture edit is now covered by the test instead of being a file nothing exercises. No existing check was removed, relaxed or reworded.

## On `SELFTEST_RUN.txt`

I did not write a capture into it, and I will not: nothing was run here, and a run log I type myself would read like evidence while being none. `SELFTEST_RUN.txt` is committed as an honest, unfilled template — the exact command, the exact place the runner's stdout/stderr/exit line goes, and a plain statement that no capture exists yet. HivemindOS writes the real run into `SELFTEST_OUTPUT.md` after this commit; that file, not my note, is the evidence.

## What I could not confirm, plainly

* `python3 self_test.py` has not been run here. I cannot state the exit code or one line of its wording. Every fix above is verified by reading the test's expectations against the code, not by execution.
* The runner's previous output was a truncated tail (an ~80-column cut, beginning mid-word at `source' got: ...`), so the `publisher` failure I fixed was inferred from the code and the hard-coded `'example-org'`, not read off the log. If the repo's `self_test.py` differs from what is listed here, re-read it rather than trusting my rebuild.
* The live HTTPS fetch (`fetch()`), its timeout and HTTP-error branches remain untested, as in every earlier step. No real model card has ever been opened; `data.csv` stays exactly its header line, and no row is invented for any of the eight candidate cards.

What is left for the owner: let the runner execute `cd tools/card-claims-fetch && python3 self_test.py; echo exit=$?` and paste that run's raw stdout, stderr and exit line into the three marked blocks of `SELFTEST_RUN.txt` (replacing the placeholder header line) in the next commit.

[Cut off here: it ran out of room. Its next step can pick up from this point.]
