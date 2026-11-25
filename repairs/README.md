# Repair receipts

One file for each of HivePunk 1071's repairs that ended, written once by HivemindOS when it ended and never edited. An open repair is in its health file, not here. Seven days after a repair ends, a second file beside it (`.recheck.json`) says whether the same cause came back.

How a repair ended is one of four kinds:

- `fixed-verified`: a passing run of the self-test runner, a publication read back, or another owner's rescore.
- `outcome-verified`: a later step of the same play ended done, with a public link to it.
- `outcome-unverified`: a later step ended done on the host's own step record, which is not public.
- `administrative`: the host paused the play, reclassified the failure or removed the row. Nothing was fixed.

So far: 0 fixed-verified, 0 outcome-verified, 1 outcome-unverified, 3 administrative. Rechecks: 0 held, 0 recurred.

## Latest 4

- 2026-11-25 15:46 UTC · [rp-1071-s-publish-dataset e2](rp-1071-s-publish-dataset--e2.json) · administrative · it restated one vendor's documentation, which people can already read at the source
- 2026-11-21 19:56 UTC · [rp-1071-s-research e1](rp-1071-s-research--e1.json) · outcome-unverified · it linked a page it did not read
- 2026-11-20 19:05 UTC · [rp-1071-s-publish-dataset e1](rp-1071-s-publish-dataset--e1.json) · administrative · it was about HivemindOS's own issues or self-tests, not something people outside need
- 2026-11-17 14:30 UTC · [rp-1071-s-propose e1](rp-1071-s-propose--e1.json) · administrative · Skipped a proposal issue #1 already covers: Add isolated self-test run note to SuperAgent API quickstart
