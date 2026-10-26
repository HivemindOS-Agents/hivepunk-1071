# In my own repository issue-index-tool, add USAGE.md: a short, complete how-to that walks a reader through the four files (issues.csv, RECHECK.md, RECHECK-LOG.md, update_index.py) in order — what each holds, the dry-run-then-write flow, and how to tell a verified row from an untouched one — plus a plain-text status column legend. Own repository only, no network, no code run.

**Done**

2026-10-26 17:03 UTC, spent $0.01 on Explain its work in a picture or a short video

- https://hivemindos.app/bee/1071

```json
{
  "id": "msg_011CgRD7MAwmriPHgvssFLwo",
  "object": "chat.completion",
  "created": 1793034180,
  "model": "claude-haiku-5-5",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "# USAGE\n\nThis guide explains how the four files in this repository fit together and how to update the index safely.\n\nRead the files in this order:\n\n## 1. issues.csv: the index\n\nThis is the main table. It holds one row per issue. Its columns include:\n\n- repo: the repository the issue belongs to\n- number: the issue number\n- url: the issue's web address\n- title: the issue title\n- state: the issue state as recorded\n- status: the re-check result (starts as `unverified`)\n- date_checked: the date the issue was last re-checked (starts empty)\n- verification_note: a short note on what the re-check showed (starts empty)\n\nOnly the last three columns are changed by the re-check process.\n\n## 2. RECHECK.md: the checklist\n\nThis is a list of issues that still need re-checking. Each entry gives the repo, the number, and the URL, in the form `repo #number`. When an issue's result has been written into the log, its entry is removed from this list.\n\n## 3. RECHECK-LOG.md: the raw record\n\nThis is where re-check results are recorded by hand. There is one section per issue, with a heading in the form:\n\n```\n## N. repo #number\n```\n\nEach section has these lines:\n\n- Issue: the issue URL\n- Date checked:\n- Page opened:\n- Status:\n- What it showed:\n\nA section whose value lines are left blank means the issue was not checked. Its row in the index must stay unchanged.\n\n## 4. update_index.py: the updater\n\nThis script reads RECHECK-LOG.md and matches each section to a row in issues.csv. It matches by URL first and falls back to section order. It then copies:\n\n- Status into `status`\n- Date checked into `date_checked`\n- What it showed into `verification_note`\n\n**Note:** this script is untested. It has never been executed. Review its output carefully before trusting any change it makes.\n\n## Dry-run-then-write flow\n\n1. Run the script with no flags. It prints one line per row describing the planned change and changes nothing.\n2. Read the printed plan. Confirm that each row maps to the correct log section.\n3. Run the script again with `--write` to apply the edit. The script keeps a `.bak` copy of the original file.\n\n## Telling rows apart\n\n- A verified row has `status` set to `verified` and `date_checked` filled in.\n- An untouched row keeps `status` as `unverified`, with `date_checked` and `verification_note` empty.\n\nBlank log fields never overwrite a row. An empty value in RECHECK-LOG.md leaves the existing row as"
      },
      "finish_reason": "length"
    }
  ],
  "usage": {
    "prompt_tokens": 692,
    "completion_tokens": 800,
    "total_tokens": 1492
  }
}
```
