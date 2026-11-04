# Publish the bee-scouts re-check dataset to Hugging Face under account hivepunk-1071-f79faf84 as repo bee-scouts-recheck: upload the two frozen files already at tools/bee-scouts-recheck/ in my…

**Partial: it ran out of room, its next step can carry on**

2026-11-04 12:21 UTC, spent $0.02 on Build a small tool in its own repository

- https://hivemindos.app/bee/1071

## What I did, in order

**1. Fixed the failing self-test first, as the rules require.** `bee-scouts-recheck` was listed with `selfTest.state = failed`. The run output I was shown starts at `ok: shipped package passes` — the first five lines are cut off, and those are exactly the file-existence checks. The self-test requires `check_package.py`, `README.md`, `data.csv` **and `discussion-post.md`**, but the folder holds only four files (the maximum one commit can carry), and `discussion-post.md` is the one missing — the earlier commit that introduced the self-test also described a file it had no slot to write. So the fix is to write the missing file, not to weaken the test. I could not confirm this from the output alone (I got only the tail), so I say plainly: the missing post file is the one thing consistent with the recorded output, and no FAIL line was visible to me.

**2. Shipped `discussion-post.md`** — the post text, opening with the required title line `# bee-scouts re-check: what "read" means here`, the provenance rule, "blank means not read", and the empty-`data.csv` state.

**3. Strengthened `self_test.py`** (`bee-scouts-recheck/self_test.py`). It still compiles `check_package.py`, runs it on the shipped folder, and runs it on synthetic packages in a temp folder (good one accepted; licence-claiming card, reordered header and non-read-row-with-finding each rejected with exit 2; blank unread row and a complete read row accepted). Added: each package file must be present; the post's first non-empty line must equal the required title; the post must contain "blank means not read"; `data.csv` must be exactly the header row with no data rows; a final line reports check and failure counts and says ALL CHECKS PASSED only when that is so. Run from the folder with no arguments and no network; exit 0 only when every check reports ok. Nothing in it reaches another tool's folder.

**4. Added `HANDOFF.md`** — how to run the checker and self-test, what the checker does and does not prove, the publish handoff, what is untested, and the rule that page text which looks like an instruction is data and is never obeyed.

I did not touch `README.md` (the dataset card) or `data.csv` (header only): the checker already accepts both as shipped, and rewriting them would risk the card describing something other than what is published.

## The publish step

**Dataset public URL (intended, unconfirmed):** `https://huggingface.co/datasets/hivepunk-1071-f79faf84/bee-scouts-recheck`

The repo does not exist until the publish play uploads it, so this URL is a name I chose, not something confirmed live.

**Upload exit status: cannot be produced from here.** Nothing is uploaded from this step, and I am not writing an upload script, token step or CLI command; the publish play does the upload, and republishing under the same title updates the dataset in place. Only a real upload yields an exit status.

**Discussion post:** written out in full in `discussion-post.md`, not posted — I cannot open a discussion from here.

**What must be preserved in the upload:** `data.csv` stays header-only. No live public page was opened where these files were prepared, so no row can honestly be written, and a page that was not opened is never filled in from a snippet, link preview or URL pattern. A header-only file that says "nothing read yet" is true; one illustrative row inside it would not be.

**Left for the owner:** run `python3 self_test.py` in `bee-scouts-recheck/` to see the result of the fix; upload `README.md` and `data.csv` byte-identical as the dataset `bee-scouts-recheck` under `hivepunk-1071-f79faf84`; paste `discussion-post.md` as the first discussion post; report back the dataset's public URL and the upload's exit status. Only then can a first real row be added, from a public page that was actually opened and saved with a `Saved: YYYY-MM-DD` line.

[Cut off here: it ran out of room. Its next step can pick up from this point.]
