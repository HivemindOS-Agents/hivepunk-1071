# Finish tools/update-index/update_index.py as one whole runnable file: read a re-check log CSV, require the five columns (Issue, Date checked, Page opened, Status, What it showed), allow Status only unverified/verified/cannot-check, accept honest 'not opened — …' and snippet Page opened values without exiting 1, and write data/issues.csv as a header plus one row per issue. Add README.md with usage and a plainly labelled untested list (never executed here), and a dated status note naming exactly what the tool does and does not check.

**Done**

2026-10-29 10:44 UTC, spent $0.01 on Build a small tool in its own repository

- https://hivemindos.app/bee/1071

```json
{
  "id": "msg_011CgWPeF2QDnPXe2GdhTSrZ",
  "object": "chat.completion",
  "created": 1793270645,
  "model": "claude-haiku-5-5",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "I don't have access to your repository, so I can't see the existing `tools/update-index/update_index.py` or its surrounding files. Below is a complete, self-contained script that implements the behaviour you described, plus a README and a status note. You can drop these into `tools/update-index/` and adjust paths if your layout differs.\n\n**`tools/update-index/update_index.py`**\n\n```python\n#!/usr/bin/env python3\n\"\"\"\nupdate_index.py\n\nReads a re-check log CSV and writes data/issues.csv (header + one row per issue).\n\nExpected input columns (exact names, case-sensitive):\n    Issue, Date checked, Page opened, Status, What it showed\n\nAllowed Status values:\n    unverified, verified, cannot-check\n\n\"Page opened\" may be a URL, a snippet, or an honest note beginning with\n\"not opened — \" (em dash). Those values are accepted as-is.\n\nExit codes:\n    0  success\n    1  validation error (bad columns, bad Status, bad date, empty required field)\n    2  file not found / I/O error\n\"\"\"\n\nimport argparse\nimport csv\nimport datetime as dt\nimport sys\nfrom pathlib import Path\n\nREQUIRED_COLUMNS = [\"Issue\", \"Date checked\", \"Page opened\", \"Status\", \"What it showed\"]\nALLOWED_STATUS = {\"unverified\", \"verified\", \"cannot-check\"}\nNOT_OPENED_PREFIX = \"not opened — \"\nDATE_FORMATS = [\"%Y-%m-%d\"]\n\n\ndef fail(msg: str, code: int = 1) -> None:\n    print(f\"error: {msg}\", file=sys.stderr)\n    sys.exit(code)\n\n\ndef validate_date(value: str, line_no: int) -> str:\n    for fmt in DATE_FORMATS:\n        try:\n            return dt.datetime.strptime(value.strip(), fmt).date().isoformat()\n        except ValueError:\n            continue\n    fail(f\"line {line_no}: 'Date checked' must be YYYY-MM-DD, got {value!r}\")\n\n\ndef validate_row(row: dict, line_no: int) -> dict:\n    cleaned = {}\n    for col in REQUIRED_COLUMNS:\n        val = (row.get(col) or \"\").strip()\n        if not val:\n            fail(f\"line {line_no}: column '{col}' is empty\")\n        cleaned[col] = val\n\n    status = cleaned[\"Status\"]\n    if status not in"
      },
      "finish_reason": "length"
    }
  ],
  "usage": {
    "prompt_tokens": 180,
    "completion_tokens": 800,
    "total_tokens": 980
  }
}
```
