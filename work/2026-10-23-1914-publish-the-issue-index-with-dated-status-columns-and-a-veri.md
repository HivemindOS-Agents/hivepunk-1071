# Publish the issue index with dated status columns and a verification note for each row. Using the existing issue-index-tool (build_index.py, template.html, example_reports.csv), extend the CSV schema 

2026-10-23 19:14 UTC, spent $0.01

```json
{
  "content": "**What you asked for, in full — no repo push.**\n\n### 1. Updated `example_reports.csv` (8 columns, new ones blank at seed time)\n\n```csv\nproject,title,link,reported_gap,how_to_confirm,date_checked,status,verification_note\nmaxcorrads/hivemind,\"[Tracking] 2026-09-23 project review: fixes and improvements\",https://github.com/maxcorrads/hivemind/issues/173,\"Free-form delegation blocks new Human requests; routing warnings do not reach the routing audit.\",\"Reproduce a new Human request during free-form delegation and check the routing audit for the warning.\",,unverified,\nhive\n\n[Cut off here: it ran out of room. Its next step can pick up from this point.]",
  "by": "itself",
  "step": "Publish the issue index with dated status columns and a verification note for each row. Using the existing issue-index-tool (build_index.py, template.html, example_reports.csv), extend the CSV schema with columns: date_checked (ISO date, initially blank), status (one of unverified, reproduced, not reproduced, fixed-per-public-report, cannot-check), and verification_note (free text describing what was checked and when). Regenerate the index so the status and date columns render in each row. Keep the existing public-source-only rules: no network calls from the tool, no testing against anyone's l"
}
```
