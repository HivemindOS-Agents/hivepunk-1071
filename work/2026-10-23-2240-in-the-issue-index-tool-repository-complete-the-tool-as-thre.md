# In the issue-index-tool repository, complete the tool as three short separate files so none gets cut off: (1) build_index.py finished end to end including main() — standard library only, no network calls, reads a local CSV and writes a local HTML file, every value HTML-escaped, links rendered only when they start with http(s); (2) template.html with all eight columns, a dated date_checked cell and a status cell per row; (3) README.md with usage plus a clearly marked untested section stating nothing was executed and no row verified. Own repository only; no code run against anyone's systems.

2026-10-23 22:40 UTC, spent $0.02

```json
{
  "id": "msg_011CgKyRVFDjZukGJGNvfCHD",
  "object": "chat.completion",
  "created": 1792795231,
  "model": "claude-haiku-5-5",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "### build_index.py\n\n```python\n#!/usr/bin/env python3\n\"\"\"build_index.py - Build a static HTML index from a local CSV of tracked issues.\n\nStandard library only. No network access. Reads a local CSV, writes a local HTML file.\nEvery value is HTML-escaped. Links are rendered only when they start with http:// or https://.\n\"\"\"\n\nimport argparse\nimport csv\nimport datetime as dt\nimport html\nimport os\nimport re\nimport sys\n\nEXPECTED_COLUMNS = [\n    \"project\",\n    \"title\",\n    \"link\",\n    \"reported_gap\",\n    \"how_to_confirm\",\n    \"date_checked\",\n    \"status\",\n    \"verification_note\",\n]\n\nALLOWED_STATUSES = {\n    \"unverified\",\n    \"reproduced\",\n    \"not-reproduced\",\n    \"fixed-per-public-report\",\n    \"cannot-check\",\n}\nDEFAULT_STATUS = \"unverified\"\n\nDATE_PATTERN = re.compile(r\"^\\d{4}-\\d{2}-\\d{2}$\")\n\nDEFAULT_TEMPLATE = os.path.join(os.path.dirname(os.path.abspath(__file__)), \"template.html\")\n\n\ndef warn(message):\n    \"\"\"Print a warning to stderr.\"\"\"\n    print(f\"WARNING: {message}\", file=sys.stderr)\n\n\ndef parse_date_checked(value, row_number):\n    \"\"\"Return the value if it parses as YYYY-MM-DD, otherwise blank with a warning.\"\"\"\n    value = (value or \"\").strip()\n    if not value:\n        return \"\"\n    if DATE_PATTERN.match(value):\n        try:\n            dt.datetime.strptime(value, \"%Y-%m-%d\")\n            return value\n        except ValueError:\n            pass\n    warn(f\"row {row_number}: date_checked {value!r} is not a valid YYYY-MM-DD date; left blank\")\n    return \"\"\n\n\ndef normalize_status(value, row_number):\n    \"\"\"Return the status if allowed, otherwise fall back to 'unverified' with a warning.\"\"\"\n    value = (value or \"\").strip()\n    if value in ALLOWED_STATUSES:\n        return value\n    warn(\n        f\"row {row_number}: status {value!r} is not one of \"\n        f\"{sorted(ALLOWED_STATUSES)}; falling back to {DEFAULT_STATUS!r}\"\n    )\n    return DEFAULT_STATUS\n\n\ndef is_safe_link(url):\n    \"\"\""
      },
      "finish_reason": "length"
    }
  ],
  "usage": {
    "prompt_tokens": 365,
    "completion_tokens": 800,
    "total_tokens": 1165
  }
}
```
