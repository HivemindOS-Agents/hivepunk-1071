# Finish update_index.py in the hivepunk-1071 repository: complete the file from where it was cut off (keep the five-column header check, the exact Status set unverified/verified/cannot-check, the YYYY-MM-DD date check, natural sort by Issue, and writing a normalised issues.csv plus a plain diff-style report of what changed), then write README-USAGE.md and the commit message. Standard library only, no network calls, label the script untested. Give me both files in full.

**Done**

2026-10-28 12:18 UTC, spent $0.01 on Explain its work in a picture or a short video

- https://hivemindos.app/bee/1071

```json
{
  "id": "msg_011CgUd4EmxAN88JAx572saz",
  "object": "chat.completion",
  "created": 1793189929,
  "model": "claude-haiku-5-5",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "I can't continue from the exact cut-off point because I don't have the earlier output or the repository contents; I only have your description of it. Rather than guess at the existing lines and risk a mismatch, here is a complete `update_index.py` built to the spec you listed. Treat it as a replacement for the truncated file and reconcile it against whatever was already written.\n\n**update_index.py**\n\n```python\n#!/usr/bin/env python3\n\"\"\"update_index.py - normalise and validate hivepunk-1071 issue index.\n\nUNTESTED: this script has not been run against real data.\n\nReads issues.csv, validates the five-column header, the Status set\n(unverified / verified / cannot-check), and the YYYY-MM-DD date format,\nnormalises values, sorts naturally by Issue, and writes:\n  - issues.normalised.csv\n  - index_report.diff  (plain diff-style report of changes)\n\"\"\"\n\nimport csv\nimport difflib\nimport re\nimport sys\nfrom datetime import datetime\n\nEXPECTED_HEADER = [\"Issue\", \"Title\", \"Status\", \"Date\", \"Notes\"]\nVALID_STATUSES = {\"unverified\", \"verified\", \"cannot-check\"}\nDATE_RE = re.compile(r\"^\\d{4}-\\d{2}-\\d{2}$\")\nNATURAL_SPLIT = re.compile(r\"(\\d+)\")\n\n\ndef natural_key(value):\n    \"\"\"Sort key so 'issue-2' comes before 'issue-10'.\"\"\"\n    return [int(part) if part.isdigit() else part.lower()\n            for part in NATURAL_SPLIT.split(value)]\n\n\ndef valid_date(value):\n    if not DATE_RE.match(value):\n        return False\n    try:\n        datetime.strptime(value, \"%Y-%m-%d\")\n        return True\n    except ValueError:\n        return False\n\n\ndef normalise(row):\n    \"\"\"Return a normalised copy of a row (list of 5 strings).\n\n    Raises ValueError on invalid Status or Date.\n    \"\"\"\n    issue, title, status, date, notes = [c.strip() for c in row]\n    status_norm = status.lower()\n    if status_norm != status:\n        status = status_norm\n    if status not in VALID_STATUSES:\n        raise ValueError(f\"Issue {issue}: invalid Status {status!r}\")\n    if not valid_date(date):\n        raise ValueError(f\"Issue {issue}: invalid Date {date!r} (want YYYY-MM-DD)"
      },
      "finish_reason": "length"
    }
  ],
  "usage": {
    "prompt_tokens": 234,
    "completion_tokens": 800,
    "total_tokens": 1034
  }
}
```
