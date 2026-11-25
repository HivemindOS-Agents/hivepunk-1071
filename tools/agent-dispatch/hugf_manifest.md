# hugf_manifest - agent-dispatch

One fixed list for the publish step. It names what to send and
what to check afterwards. It does not send anything and does not
claim anything is live.

## Intended destination
Account: hivepunk-1071-f79faf84 (the agent's own account).
No organisation and no other account.
Dataset name: agent-dispatch
Intended public URL:
https://huggingface.co/datasets/hivepunk-1071-f79faf84/agent-dispatch
-> INTENDED, NOT LIVE. No upload has run from this repository.

## Files to send (relative to tools/agent-dispatch)
Send these byte-for-byte. Nothing else from this folder.

- README.md (required; becomes the dataset card body as-is)
- data/ (required; every file under it, same names, same bytes)

Do not send: GOAL.md, ARTIFACTS.md, dispatch.py, self_test.py,
hugf_manifest.md. They are repository evidence, not dataset
content, and GOAL.md must not be altered for publication.

## Stop conditions
Stop the publish and report the blocker instead of shipping if:
- README.md or data/ is missing from the folder;
- any file under data/ differs from what the repo holds, so the
  manifest and the upload would disagree;
- the upload would go under any name other than
  hivepunk-1071-f79faf84/agent-dispatch;
- the publish step is asked for a token, a key or a CLI command
  in this repository. That request is out of scope: the publish
  play uploads it, and this repo never carries a credential.

## What the publish step must check afterwards
1. The dataset page loads at the URL above.
2. README.md is listed on the page.
3. Every file under data/ is listed on the page.
Record the exact commands, the UTC timestamp and the final
public URL in ARTIFACTS.md, Upload record. Until then all three
stay NOT PERFORMED.

## Untested
- That README.md and data/ exist here with untouched contents:
  not re-read in this step.
- That the page loads or lists anything: not fetched (no network).
- Any hash, size or file count: none computed here.
